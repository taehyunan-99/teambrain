export const meta = {
  name: 'phase5a-hard-nearmiss-proliferation',
  description: '2차 증식 — 변별 키워드(고유명사/수치)까지 흉내낸 hard near-miss로 grep 격리를 뚫는 임계 탐색 + 적대 audit',
  phases: [
    { title: 'Generate', detail: '질문별 hard near-miss 생성(변별 키워드 흉내, 정답 사실은 없음)' },
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

// hard near-miss = 변별 키워드(고유명사·수치)까지 자연스럽게 등장시키되, 정답 사실은 절대 없음.
// 목적: grep이 변별 키워드로 정답을 격리하는 강점마저 무력화되는 임계를 탐색.
const targets = [
  {
    qid: 'A4', dir: 'raw/slack', count: 60, channel: '#pay-dev',
    q: '코지홈 가맹점이 환불 관련해서 뭐 문의했었어?',
    answer_must_not: "코지홈이 '5만원 중 2만원만 부분환불' 가능한지 문의, 당시 전액취소만 가능 안내. 이 사실(부분환불 문의+전액취소 안내)을 절대 재현 금지.",
    discriminator: "고유명사 '코지홈'을 자연스럽게 등장시켜라(grep이 코지홈으로 격리 못 하게). 단 코지홈의 '부분환불 2만원 문의'는 절대 금지 — 코지홈이 다른 문의(정산일·입금확인·영수증·로그인·연동·배포 안내 수신 등 환불 외)를 하거나, 코지홈이 환불을 언급해도 다른 환불(전액환불 완료 확인, 환불 지연 문의 등 '부분환불 가부'가 아닌 것)만.",
    keyword_must: '코지홈, 환불, 부분환불, 취소, 가맹점, CS, 문의',
    theme: "코지홈이 등장하는 다양한 CS/잡담(환불 외 문의, 또는 부분환불 가부가 아닌 환불 문의). 코지홈 외 다른 가맹점의 부분환불 문의도 섞어 — '부분환불'이라는 키워드가 여러 가맹점에 분산되게.",
    window: '2025-06-01 ~ 2025-12-15', persona: '최민지, 이준호',
  },
  {
    qid: 'C1', dir: 'raw/infra/slack', count: 50, channel: '#infra',
    q: '로그 서버 디스크 꽉 찼던 적 있었나? 몇 퍼센트까지 갔었어?',
    answer_must_not: "로그 서버 디스크가 '82%까지 참 → 정리 후 54%' 사건. 이 사건(꽉 참+82/54 조합)을 절대 재현 금지.",
    discriminator: "수치 '82%'와 '디스크 찼다'는 표현을 변별 못 하게, 다른 서버/다른 맥락에서 82·80·85 같은 수치와 '찼다/가득' 표현을 등장시켜라. 단 '로그 서버가 82%까지 차서 정리해 54%로 내렸다'는 사건은 금지 — DB 서버 디스크 82%(다른 서버), 메모리 82%(디스크 아님), CPU 82%, 백업 디스크 80% 같은 다른 자원/다른 서버의 수치만.",
    keyword_must: '디스크, 로그, 서버, 82, 80, 용량, 찼, 가득, 정리',
    theme: "디스크/용량 수치(80%대)가 다른 서버·다른 자원(DB/메모리/CPU/백업)에서 등장하는 운영 한담. '로그 서버가 꽉 찬' 그 사건만 아니면 됨.",
    window: '2024-08-01 ~ 2025-03-31', persona: '정유진, 강민석',
  },
  {
    qid: 'C3', dir: 'raw/infra/slack', count: 50, channel: '#infra',
    q: '2025년 1월에 CI 빌드 간헐적으로 깨지던 문제 원인이 뭐였어?',
    answer_must_not: "2025-01 CI flaky의 원인이 '캐시 만료 검증 테스트의 sleep 타이밍이 러너 부하 때 어긋남'. 이 원인(sleep 타이밍+캐시 만료 테스트 조합)을 절대 재현 금지.",
    discriminator: "'flaky', '간헐적', 'sleep', '타이밍', '캐시' 같은 변별어를 다른 맥락에서 등장시켜라. 단 '2025년 1월 CI 빌드가 캐시 만료 검증 테스트 sleep 타이밍 때문에 flaky'는 금지 — 다른 시기(2024-12, 2025-02)의 flaky, 다른 원인(네트워크 타임아웃·의존성·OOM)의 flaky, sleep을 다른 코드에서 쓴 얘기, 캐시를 다른 맥락(CDN·Redis)에서 쓴 얘기만.",
    keyword_must: 'CI, 빌드, flaky, 간헐적, sleep, 타이밍, 캐시, 테스트, 깨짐',
    theme: "flaky/간헐적 빌드 실패가 다른 시기·다른 원인으로 등장하는 잡담. 2025-01 캐시-sleep 그 원인만 아니면 됨.",
    window: '2024-11-01 ~ 2025-03-15', persona: '정유진, 강민석, 이준호',
  },
  {
    qid: 'C4', dir: 'raw', count: 50, channel: '',
    q: '추석 연휴 때 배포나 배치 일정 어떻게 챙겼어?',
    answer_must_not: "'도현이 추석 끼는 달이라 배포/배치 일정 미리 챙기자고 인프라/정산에 핑 돌림'(09-02 weekly), '명절 전 배포 freeze 인프라랑 협의 중'(09-09 weekly). 이 두 사실을 절대 재현 금지.",
    discriminator: "추석/명절/배포/배치를 '본격 운영 문서'처럼 그럴듯하게 등장시켜라(holiday-ops·freeze·schedule 류). 단 '도현이 weekly로 인프라/정산에 핑 돌려 점검 분산' 사실은 금지 — 명절과 무관한 배포 freeze(평소 주말 freeze), 다른 명절(설날), 추석 끝난 후 회고, 추석 잡담만. C4가 1차에서 recall 실패했으니 이 '그럴듯한 미끼'를 더 두텁게.",
    keyword_must: '추석, 연휴, 명절, 배포, 배치, freeze, 동결, 점검, 일정, weekly',
    theme: "추석/배포/배치 키워드가 풍부한 '그럴듯한 운영 문서'(freeze 공지·온콜·스케줄·회고). 정답인 '도현 weekly 핑'만 아니면 됨. recall을 더 압박.",
    window: '2025-08-15 ~ 2025-10-10', persona: '김도현, 정유진, 한지우, 강민석',
  },
]

const GEN_SCHEMA = {
  type: 'object', required: ['files'],
  properties: { files: { type: 'array', items: {
    type: 'object', required: ['filename', 'date', 'content', 'why_nearmiss'],
    properties: {
      filename: { type: 'string', description: '대상 디렉토리 기준 파일명만. 날짜-주제-kind, 기존과 안 겹치게. (1차 5a 파일명과도 겹치지 말 것)' },
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
hard near-miss = 표적 질문의 **변별 키워드(고유명사·수치)까지 흉내내** grep으로 정답과 한 덩어리로 묶이지만, **정답 사실은 전혀 없는** raw.
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

파일명은 ${t.dir} 기준. 날짜는 ${t.window} 안에 흩뿌려라. 1차 생성분과 파일명 겹치지 마라.`,
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
