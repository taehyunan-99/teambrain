export const meta = {
  name: 'phase5a-remeasure-reinforce',
  description: '보강 재측정 — A4(코지홈 2차)·C5(헬스체크 오탐)·C6(커넥션풀 고갈)을 hard near-miss 증식 후 recall/rank 분리 채점',
  phases: [
    { title: 'Retrieve', detail: '질문별 에이전트가 index.md→파일 직접읽기로 답 시도, 연 파일 기록' },
    { title: 'Grade', detail: 'recall/rank 분리 채점 — 정답파일 열었나 vs 열고도 못 골랐나' },
  ],
}

// 보강 측정 대상: A4(고유명사, 버티는 쪽 2번째) + C5/C6(C3 동형, 깨지는 쪽 재현).
const questions = [
  {
    id: 'A4', type: '고유명사-정밀',
    q: '코지홈 가맹점이 환불 관련해서 뭐 문의했었어?',
    truth_files: ['raw/slack/2025-09-05-merchant-partial-refund-cs.md'],
    truth_fact: '5만원 결제건 중 2만원만 환불 가능한지 문의 → 당시는 전액 취소만 가능, 부분환불 미지원 안내',
  },
  {
    id: 'C5', type: '건초더미-매몰',
    q: '2024년 7월에 헬스체크 알람이 새벽에 오탐 떴던 적 있지? 그 원인이 뭐였어?',
    truth_files: ['raw/infra/slack/2024-07-23-infra-healthcheck-alert-false-positive.md'],
    truth_fact: '새벽 4시 백업(DB 덤프) 도는 동안 응답 지연 → 헬스체크 타임아웃(2초) 걸림 → 타임아웃 2초→5초로 상향',
  },
  {
    id: 'C6', type: '건초더미-매몰',
    q: '2024년 10월에 결제 승인이 갑자기 느려졌던 적 있지? 그때 원인이랑 어떻게 잡았어?',
    truth_files: ['raw/slack/2024-10-30-db-connection-exhaustion.md'],
    truth_fact: 'HikariCP 커넥션 풀 max 기본값 10이 온보딩 가맹점 트래픽 5~6배에 고갈(동기 PG 승인이 커넥션 점유)→30초 타임아웃. 해결=풀 30, connectionTimeout 5초, maxLifetime 30분',
  },
]

const INDEX_MD = __INDEX__

const RETRIEVE_SCHEMA = {
  type: 'object',
  required: ['answer', 'files_opened', 'candidates_seen', 'reached', 'confidence', 'notes'],
  properties: {
    answer: { type: 'string', description: '최종 답변(찾은 만큼만, 모르면 모른다고)' },
    files_opened: { type: 'array', items: { type: 'string' }, description: '실제로 Read로 연 파일 경로(순서대로).' },
    candidates_seen: { type: 'number', description: 'grep/Glob으로 후보로 떠오른 파일 대략 개수(열기 전 검색 결과 수). 후보 폭증 측정용.' },
    reached: { type: 'boolean', description: '질문에 실질적으로 답했다 스스로 판단하면 true' },
    confidence: { type: 'string', enum: ['high', 'medium', 'low', 'none'] },
    notes: { type: 'string', description: '후보가 너무 많아 못 좁혔는지, 정답 파일을 봤는데 놓쳤는지, 어디서 막혔는지.' },
  },
}

const GRADE_SCHEMA = {
  type: 'object',
  required: ['verdict', 'recall', 'rank', 'failure_type', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['correct', 'partial', 'wrong', 'no-answer'] },
    recall: { type: 'boolean', description: 'files_opened가 truth_files 중 하나라도 포함하면 true (정답 후보에 도달했나).' },
    rank: { type: 'string', enum: ['hit', 'missed-in-pile', 'never-reached', 'na'], description: 'recall=true인데 정답 못 맞히면 missed-in-pile(후보엔 있었으나 못 고름=랭킹 실패). recall=false면 never-reached. correct면 hit. no-answer/대조군 정상이면 na.' },
    failure_type: { type: 'string', enum: ['none', 'haystack-buried-rank', 'haystack-buried-recall', 'proper-noun-miss', 'vocab-mismatch', 'hallucination'] },
    reason: { type: 'string', description: '판정 근거. 특히 recall과 rank를 왜 그렇게 봤는지.' },
  },
}

const results = await pipeline(
  questions,
  (q) =>
    agent(
      `너는 Nimbus Pay 팀 위키를 검색하는 어시스턴트다. index.md(개념 카탈로그)를 단서로 질문에 답하라.

== 동작 규칙 ==
- 출발점은 index.md. 링크된 wiki/*.md를 Read로 열고, sources/wikilink로 raw/*.md도 열 수 있다.
- index.md에 단서 없으면 wiki/·raw/를 Glob/Grep으로 뒤져도 된다(raw는 1000개 이상이라 다 못 읽음 — 키워드 grep 의존).
- 중요: grep/Glob으로 후보를 뽑았을 때 그 후보가 몇 개였는지 candidates_seen에 대략 기록하라. 후보가 많아 다 못 열었으면 솔직히 notes에 적어라.
- 찾은 만큼만 답하라. 모르면 "못 찾음". 지어내지 마라.
- 연 파일을 files_opened에 순서대로 정확히 기록.

== index.md ==
${INDEX_MD}

== 질문 ==
${q.q}`,
      { label: `retrieve:${q.id}`, phase: 'Retrieve', schema: RETRIEVE_SCHEMA, agentType: 'Explore' }
    ).then((r) => ({ q, retrieve: r })),
  (prev) => {
    if (!prev || !prev.retrieve) return prev
    const q = prev.q
    const r = prev.retrieve
    const hitTruth = (r.files_opened || []).some((f) => q.truth_files.some((t) => f.includes(t.replace('raw/', '').replace('wiki/', '')) || t.includes(f)))
    return agent(
      `채점자다. 검색 답변을 정답과 대조하되, recall(정답 후보 도달)과 rank(후보 중 정답 식별)를 분리 판정하라.

== 질문 ==
${q.q}
== 정답(truth_fact) ==
${q.truth_fact}
== 정답이 든 파일(truth_files) ==
${q.truth_files.join(', ')}

== 검색 결과 ==
답변: ${r.answer}
스스로 답함: ${r.reached} (confidence=${r.confidence})
연 파일: ${(r.files_opened || []).join(', ') || '(없음)'}
검색 후보 수(candidates_seen): ${r.candidates_seen}
메모: ${r.notes}
(truth_file 도달 자동추정: ${hitTruth})

판정 기준:
- recall = 연 파일에 truth_file이 하나라도 있으면 true.
- rank = recall true인데 정답을 못 맞혔으면 'missed-in-pile'(후보엔 정답이 있었으나 다른 near-miss에 묻혀 못 고름 = 랭킹 실패, 이게 핵심 측정 대상).
         recall false면 'never-reached'(애초에 후보에 못 도달). correct면 'hit'.
- failure_type: 후보엔 있었는데 못 골랐으면 haystack-buried-rank, 후보에도 못 갔으면 haystack-buried-recall.
- 핵심 사실 맞으면 correct, 일부 partial, 틀리면 wrong, 못 찾으면 no-answer.`,
      { label: `grade:${q.id}`, phase: 'Grade', schema: GRADE_SCHEMA }
    ).then((g) => ({ ...prev, grade: g, hitTruth }))
  }
)

const ok = results.filter(Boolean)
return {
  total: ok.length,
  rows: ok.map((r) => ({
    id: r.q.id,
    q: r.q.q,
    verdict: r.grade?.verdict,
    recall: r.grade?.recall,
    rank: r.grade?.rank,
    failure_type: r.grade?.failure_type,
    candidates_seen: r.retrieve?.candidates_seen,
    confidence: r.retrieve?.confidence,
    files_opened: r.retrieve?.files_opened,
    answer: r.retrieve?.answer,
    reason: r.grade?.reason,
  })),
}
