export const meta = {
  name: 'phase5b-design-critique',
  description: '5b 하이브리드 검색 설계를 독립 렌즈로 적대 검토 — 구현 전 결함 발견',
  phases: [{ title: 'Critique' }, { title: 'Synthesize' }],
}

const PLAN = `# Phase 5b 하이브리드 검색 설계 요약 (검토 대상)
스택: Python + SQLite(FTS5 BM25 + sqlite-vec 384d). 0원, 로컬.

5a 측정 배경: raw 1576 슬랙더미. 6개 표적질문 측정에서 모든 실패가 recall 실패(정답을 top후보로 못 엶), rank실패 0건.
- C3(CI flaky)·C5(헬스체크 오탐): 일반어 변별키워드가 near-miss에 흉내나 BM25격리 붕괴->정답 못 엶.
- A4(코지홈 환불): 정답 파일명에 'cozyhome' 토큰 없고 본문에만 있음->파일명색인 grep이 못잡음.
- C1(로그서버 디스크): 한정어 토큰 생존->버팀. C6(커넥션풀): 정답이 wiki합성됨->라우팅 우회 버팀.

설계 결정:
1. 청크 = 파일 1개(분할 안함). 슬랙더미 짧으니까. truth_files가 파일경로라 채점단위 일치.
2. 색인텍스트 = frontmatter 제외 본문 전체(파일명 아님). 대상 raw 1576 + wiki/sources 169 = 1745.
3. 임베딩 = paraphrase-multilingual-MiniLM-L12-v2 (384d, 다국어). 대안 embeddinggemma-300m(768d).
4. BM25 토크나이저 = FTS5 unicode61(형태소분석기 없음).
5. RRF k=60, BM25/벡터 동등가중. top-N=50, 최종top-k=10.
6. 재측정 = 6질문 x {BM25단독, 임베딩단독, 하이브리드} recall@10 비교. truth_files가 top10에 들었나.`

const SCHEMA = {
  type: 'object', required: ['verdict', 'issues'],
  properties: {
    verdict: { type: 'string', enum: ['sound', 'needs-fix', 'flawed'] },
    issues: { type: 'array', items: {
      type: 'object', required: ['severity', 'area', 'problem', 'fix'],
      properties: {
        severity: { type: 'string', enum: ['blocker', 'major', 'minor'] },
        area: { type: 'string' },
        problem: { type: 'string' },
        fix: { type: 'string' },
      } } } },
}

const lenses = [
  { key: 'measurement-validity', focus: '측정 타당성 — 재측정이 5a 결과와 공정하게 비교되는가. recall@10 채점에 누수/편향 없나(예: top-N=50인데 recall@10? near-miss가 색인에 포함돼 정답을 밀어내나? 6질문 단일채점). C3/C5/A4가 하이브리드로 회복되는지를 이 설계가 진짜 증명하나, 아니면 자기충족적인가.' },
  { key: 'retrieval-correctness', focus: '검색 정확성 — 한국어+영문코드 혼합 슬랙체에서 unicode61로 BM25 토큰화 제대로 되나(코지홈, HikariPool, 82%). MiniLM 384d가 한국어 의미 충분히 잡나. RRF 동등가중/k=60/top-N=50이 1745 코퍼스에 적절한가. 파일=청크가 BM25 길이정규화·임베딩 품질에 주는 영향.' },
  { key: 'implementation-risk', focus: '구현 리스크 — sqlite-vec vec0와 FTS5 content-table rowid 동기화, 임베딩 1745건 생성 시간/배치, frontmatter 파싱 견고성, 측정 재현성. 빠뜨린 엣지(빈 본문, 중복 path, _archive 참고문서가 색인에 섞이면 안 됨 등).' },
]

const crits = await parallel(lenses.map((l) => () =>
  agent(
    '너는 검색시스템 설계 리뷰어다. 아래 Phase 5b 하이브리드 검색 설계를 "' + l.focus + '" 렌즈로 적대적으로 검토하라.\n실제 결함만 보고하라(트집 금지). 각 이슈에 severity/area/problem/fix. 설계가 건전하면 verdict=sound.\n\n' + PLAN,
    { label: 'critique:' + l.key, phase: 'Critique', schema: SCHEMA, model: 'sonnet' }
  ).then((r) => ({ lens: l.key, verdict: r.verdict, issues: r.issues || [] }))
))

const valid = crits.filter(Boolean)
const allIssues = valid.flatMap((c) => c.issues.map((i) => ({ lens: c.lens, ...i })))
const blockers = allIssues.filter((i) => i.severity === 'blocker')
const majors = allIssues.filter((i) => i.severity === 'major')

const synth = await agent(
  '너는 설계 리드다. 3명의 리뷰어가 5b 검색 설계를 검토했다. 아래 이슈들을 종합해, 구현 전 반드시 고칠 것과 무시해도 될 것을 가른다.\n중복 제거하고, 각 이슈가 진짜인지(설계를 실제로 깨는지) 냉정히 판정하라. 과한 우려는 기각.\n\n설계 요약:\n' + PLAN +
  '\n\n리뷰어 verdict: ' + valid.map((c) => c.lens + '=' + c.verdict).join(', ') +
  '\n\n이슈들(' + allIssues.length + '개, blocker ' + blockers.length + ' / major ' + majors.length + '):\n' +
  allIssues.map((i, n) => '[' + n + '] (' + i.severity + '/' + i.lens + ') ' + i.area + ': ' + i.problem + ' -> fix: ' + i.fix).join('\n') +
  '\n\n출력: 구현 전 must-fix 목록(우선순위순, 각 1줄 액션) + 기각한 이슈와 이유. 솔직하게.',
  { label: 'synthesize', phase: 'Synthesize', model: 'sonnet' }
)

return { verdicts: valid.map((c) => ({ lens: c.lens, verdict: c.verdict })), blockers, majors, allIssues, synthesis: synth }
