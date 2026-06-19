export const meta = {
  name: 'phase5a-reinforce-hard-nearmiss',
  description: '5a 곡선 보강 — A4(코지홈) 2차 + C5(헬스체크 오탐 타임아웃)·C6(커넥션풀 고갈) 신규 재현 표적의 hard near-miss 생성 + 적대 audit',
  phases: [
    { title: 'Generate', detail: '표적별 hard near-miss 생성(변별 키워드 흉내, 정답 사건은 금지)' },
    { title: 'Audit', detail: 'answer-leak·변별흉내 적정성·future-leak 적대 검증' },
  ],
}

const CHARTER = `회사: Nimbus Pay (국내 PG·결제 인프라).
인물: 결제팀 김도현(테크리드) 박서연(멱등성/DB) 이준호(PG/웹훅) 최민지(PM/CS).
정산팀 한지우(리드) 오세훈(배치/payout). 인프라팀 정유진(SRE) 강민석(플랫폼).
채널: #pay-dev #pay-incident #pay-random #settlement #infra #platform-announce.
팀 활성: 정산 2024-08~, 인프라·결제 2024-07~.`

const RULES = `절대 규약:
1. in-the-moment(그 시점 그대로, 사후주석 금지). 2. future-leak 금지(시간창 밖 용어/사건 금지).
3. 노이즈 성격(일상 잡담·배포·운영한담·단신, 큰 사건 새로 만들지 말 것).
4. frontmatter 필수. 5. 인물 일관성. 6. 다양성(날짜·작성자·주제 안 겹치게).`

// hard near-miss = 변별 키워드(고유명사·수치·일반 기술어)까지 흉내내되, 정답 사실은 절대 없음.
// A4 = 버티는 쪽 2번째 증거(고유명사). C5/C6 = 깨지는 쪽 재현(C3 동형: 일반어 변별 키워드).
const targets = [
  {
    qid: 'A4', dir: 'raw/slack', count: 60, channel: '#pay-dev',
    q: '코지홈 가맹점이 환불 관련해서 뭐 문의했었어?',
    answer_must_not: "코지홈이 '5만원 중 2만원만 부분환불' 가능한지 문의, 당시 전액취소만 가능 안내. 이 사실(코지홈+부분환불 가부 문의+전액취소 안내)을 절대 재현 금지.",
    discriminator: "고유명사 '코지홈'을 자연스럽게 등장시켜라(grep이 코지홈으로 격리 못 하게). 단 코지홈의 '부분환불 2만원 가부 문의'는 절대 금지 — 코지홈이 다른 문의(정산일·입금확인·영수증·로그인·연동·배포 안내 수신 등 환불 외)를 하거나, 코지홈이 환불을 언급해도 다른 환불(전액환불 완료 확인, 환불 지연 문의 등 '부분환불 가부'가 아닌 것)만.",
    keyword_must: '코지홈, 환불, 부분환불, 취소, 가맹점, CS, 문의',
    theme: "코지홈이 등장하는 다양한 CS/잡담(환불 외 문의, 또는 부분환불 가부가 아닌 환불 문의). 코지홈 외 다른 가맹점의 부분환불 문의도 섞어 — '부분환불' 키워드가 여러 가맹점에 분산되게.",
    window: '2025-06-01 ~ 2025-12-15', persona: '최민지, 이준호',
  },
  {
    qid: 'C5', dir: 'raw/infra/slack', count: 54, channel: '#infra',
    q: '2024년 7월에 헬스체크 알람이 새벽에 오탐 떴던 적 있지? 그 원인이 뭐였어?',
    answer_must_not: "2024-07-23 헬스체크 알람 오탐의 원인이 '새벽 4시 백업(DB 덤프) 도는 동안 응답 지연 → 헬스체크 타임아웃(2초)에 걸림 → 타임아웃 2초→5초로 상향'. 이 사건(백업 덤프 겹침+2초/5초 헬스체크 타임아웃 조합)을 절대 재현 금지.",
    discriminator: "일반어 'timeout/타임아웃', '오탐/false positive', '헬스체크', '알람'을 다른 맥락에서 등장시켜라. 단 '새벽 백업 덤프가 헬스체크 타임아웃을 유발해 2→5초로 늘린' 그 사건은 금지 — 다른 타임아웃(PG 승인 타임아웃, DB 커넥션 타임아웃, registry/DNS 타임아웃, Redis 응답 타임아웃), 다른 오탐(메모리 알람 오탐, 디스크 알람 오탐), 헬스체크를 다른 맥락(엔드포인트 추가·임계치 다른 값 조정)에서 다룬 잡담만. 백업 시간대(새벽 4시)와 무관하게.",
    keyword_must: '헬스체크, 알람, 오탐, 타임아웃, timeout, 임계치, 새벽, 모니터링',
    theme: "타임아웃·알람·오탐 키워드가 다른 원인·다른 시스템에서 등장하는 운영 한담. '2024-07 백업 덤프 → 헬스체크 2→5초' 그 사건만 아니면 됨.",
    window: '2024-06-15 ~ 2024-09-30', persona: '정유진, 강민석',
  },
  {
    qid: 'C6', dir: 'raw/slack', count: 54, channel: '#infra',
    q: '2024년 10월에 결제 승인이 갑자기 느려졌던 적 있지? 그때 원인이랑 어떻게 잡았어?',
    answer_must_not: "2024-10-30 결제 승인 지연의 원인이 'HikariCP 커넥션 풀 max가 기본값 10이라, 온보딩 가맹점 트래픽 5~6배에 동기 PG 승인이 커넥션을 물고 있어 풀 고갈 → 30초 타임아웃. 해결=maximumPoolSize 10→30, connectionTimeout 30s→5s, maxLifetime 30분'. 이 사건(커넥션 풀 기본값 10 고갈+온보딩 트래픽+풀30/5초 튜닝 조합)을 절대 재현 금지.",
    discriminator: "일반어 '커넥션 풀', 'connection pool', '타임아웃', '승인 지연', 'HikariPool', 'maximumPoolSize'를 다른 맥락에서 등장시켜라. 단 '2024-10 온보딩 트래픽 5~6배로 풀 기본값 10이 고갈돼 30→5초 줄이고 풀 30으로 올린' 그 사건은 금지 — 다른 커넥션 이슈(ProxySQL 도입 후 커넥션 안정화 잡담, 다른 시기 풀 튜닝, Redis 커넥션, 정산 배치 DB 커넥션), 다른 승인 지연(PG사 장애로 인한 지연, 네트워크 지연), 커넥션 풀을 일반론으로 논한 잡담만. 2024-10 그 고갈 사건만 아니면 됨.",
    keyword_must: '커넥션, 풀, connection, pool, 승인, 지연, 타임아웃, HikariPool, maximumPoolSize, 트래픽',
    theme: "커넥션 풀·타임아웃·승인 지연 키워드가 다른 시기·다른 원인으로 등장하는 운영 한담. '2024-10 풀 기본값 10 고갈→30 튜닝' 그 사건만 아니면 됨.",
    window: '2024-09-01 ~ 2025-01-31', persona: '정유진, 김도현, 박서연, 이준호',
  },
]

const GEN_SCHEMA = {
  type: 'object', required: ['files'],
  properties: { files: { type: 'array', items: {
    type: 'object', required: ['filename', 'date', 'content', 'why_nearmiss'],
    properties: {
      filename: { type: 'string', description: '대상 디렉토리 기준 파일명만. 날짜-주제-kind, 기존과 안 겹치게. (1·2차 5a 파일명과도 겹치지 말 것)' },
      date: { type: 'string' }, content: { type: 'string', description: 'frontmatter 포함 전문. 변별 키워드 등장, 정답 사실 없음.' },
      why_nearmiss: { type: 'string', description: '어떤 변별 키워드를 흉내냈고 왜 정답이 아닌지 1줄.' },
    } } } },
}
const AUDIT_SCHEMA = {
  type: 'object', required: ['verdict', 'violations'],
  properties: { verdict: { type: 'string', enum: ['clean', 'dirty'] }, violations: { type: 'array', items: {
    type: 'object', required: ['filename', 'rule', 'detail'],
    properties: { filename: { type: 'string' }, rule: { type: 'string', enum: ['answer-leak', 'future-leak', 'keyword-missing', 'frontmatter', 'character', 'duplicate'] }, detail: { type: 'string' } } } } },
}

const results = await pipeline(
  targets,
  (t) =>
    agent(
      `너는 Nimbus Pay 팀 과거 슬랙/문서 더미를 만든다. 아래 표적 질문의 "hard near-miss"를 ${t.count}건 생성하라.

== hard near-miss의 정의 (이 작업의 핵심) ==
hard near-miss = 표적 질문의 **변별 키워드(고유명사·수치·일반 기술어)까지 흉내내** grep으로 정답과 한 덩어리로 묶이지만, **정답 사실은 전혀 없는** raw.
목적: grep이 변별 키워드로 정답을 정밀 격리하는 강점마저 무력화되는지(임계) 측정. 정답 바늘이 "변별 키워드까지 같은" 건초에 묻히게.

== 표적 질문 ==
질문: ${t.q}
정답(절대 재현·누설 금지): ${t.answer_must_not}
변별 키워드 흉내 지침: ${t.discriminator}
포함할 키워드: ${t.keyword_must}
테마: ${t.theme}

== 절대 규약 ==
1. answer-leak 금지: 위 "정답 사실"을 담거나 흉내내지 마라. (변별 키워드는 흉내내되 정답 사건은 절대 금지 — 이 경계가 핵심)
2. keyword 필수: "${t.keyword_must}" 중 여럿을 자연스럽게.
3. in-the-moment / future-leak 금지(시간창 ${t.window}). 4. frontmatter 필수${t.channel ? `(channel: ${t.channel})` : ''}. 5. 다양성. 6. 인물 일관성(주: ${t.persona}).

${CHARTER}
${RULES}

파일명은 ${t.dir} 기준. 날짜는 ${t.window} 안에 흩뿌려라. 기존 생성분과 파일명 겹치지 마라.`,
      { label: `gen:${t.qid}`, phase: 'Generate', schema: GEN_SCHEMA, model: 'sonnet' }
    ).then((g) => ({ t, gen: g })),
  (prev) => {
    if (!prev || !prev.gen) return prev
    const t = prev.t
    const files = prev.gen.files || []
    return agent(
      `적대적 audit. hard near-miss들이 규약을 지켰는지 검사. 의심되면 dirty.

== 표적 질문 ==
${t.q}
== 정답(누설되면 answer-leak) ==
${t.answer_must_not}
== 변별 키워드는 흉내내도 됨(이건 위반 아님), 단 정답 사건은 금지 ==
${t.discriminator}
== 필수 키워드 / 시간창 ==
${t.keyword_must} / ${t.window}

검사: answer-leak(정답 사건을 담거나 흉내냈나? 변별 키워드만 같은 건 OK, 정답 사실이 들어가면 dirty) / keyword-missing / future-leak / frontmatter / character / duplicate.

== 대상 ==
${files.map((f, i) => `[${i}] ${f.filename} (${f.date})\nwhy: ${f.why_nearmiss}\n${f.content}`).join('\n\n---\n\n')}`,
      { label: `audit:${t.qid}`, phase: 'Audit', schema: AUDIT_SCHEMA, model: 'sonnet' }
    ).then((a) => ({ ...prev, audit: a }))
  }
)

const ok = results.filter(Boolean)
return {
  targets: ok.map((r) => ({
    qid: r.t.qid, dir: r.t.dir,
    generated: (r.gen?.files || []).length,
    verdict: r.audit?.verdict, violations: r.audit?.violations || [],
    files: (r.gen?.files || []).map((f) => ({ filename: f.filename, date: f.date, content: f.content, why_nearmiss: f.why_nearmiss })),
  })),
}
