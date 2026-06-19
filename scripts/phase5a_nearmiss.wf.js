export const meta = {
  name: 'phase5a-nearmiss-proliferation',
  description: '표적 4질문(C1/C3/C4/A4)의 near-miss 노이즈를 LLM 증식 + 적대 audit — grep recall은 유지하되 rank를 무너뜨리는 건초더미',
  phases: [
    { title: 'Generate', detail: '질문별 near-miss raw N건 생성(키워드 일치·정답 없음)' },
    { title: 'Audit', detail: 'near-miss 규약 위반(정답 누설·future-leak·형식) 적대 검증' },
  ],
}

// Workflow args가 이 환경에서 문자열로 전달되는 이슈 → 데이터를 스크립트에 직접 인라인(Phase 3 검증 패턴)
const CHARTER = `회사: Nimbus Pay (국내 PG·결제 인프라. 가맹점에 결제 API/SDK + 정산 제공).
인물 (성격 고정):
  결제팀(pay-dev): 김도현(테크리드,결정승인자), 박서연(시니어 백엔드,멱등성/DB,fail-closed 강경), 이준호(백엔드,PG어댑터/웹훅,키보드 잘 삼), 최민지(PM/CS,가맹점 소통·환불운영, 정산PM 겸임).
  정산팀(settlement): 한지우(리드,D+1배치/수수료/명세서,회계 정합성 깐깐), 오세훈(백엔드,배치잡/payout/CSV).
  인프라팀(infra): 정유진(SRE리드,Redis/PG운영·배포·알람), 강민석(플랫폼,K8s/오토스케일/모니터링).
채널: #pay-dev #pay-incident #pay-random #settlement #infra #platform-announce.
팀 활성: 정산팀은 2024-08부터. 인프라·결제는 2024-07부터.`

const RULES = `절대 규약:
1. in-the-moment: 그 시점 그대로. 사후 주석·결론 요약 금지.
2. future-leak 금지: 시간창 이후 사건·결정·용어 금지.
3. 노이즈 성격: 일상 잡담·배포알림·운영한담·주간단신. 큰 사건 새로 만들지 말 것.
4. frontmatter 필수.
5. 인물 성격·소속 일관성.
6. 다양성: 날짜·작성자·주제 안 겹치게. 수치는 그럴듯하게 흩뿌림.`

const targets = [
  {
    qid: 'C4', dir: 'raw', count: 40, channel: '',
    q: '추석 연휴 때 배포나 배치 일정 어떻게 챙겼어?',
    answer_must_not: "도현이 인프라/정산에 핑 돌려 명절 전 점검, 명절 전 배포/배치 점검 사실. 이걸 절대 재현 금지.",
    keyword_must: '추석, 연휴, 명절, weekly, 9월, 배포, 배치',
    theme: "추석/명절을 스치지만 '일정 점검' 사실은 없는 9월 weekly·잡담: 명절 선물 얘기, 연휴 계획 잡담, 추석 끝나고 복귀 인사, 명절과 무관한 그 주 단신(다른 이슈 위주). 배포/배치 단어는 나오되 '명절 전 점검 핑' 사실은 없음.",
    window: '2025-08-15 ~ 2025-10-05', persona: '김도현, 정유진, 한지우, 최민지',
  },
  {
    qid: 'C1', dir: 'raw/infra/slack', count: 40, channel: '#infra',
    q: '로그 서버 디스크 꽉 찼던 적 있었나? 몇 퍼센트까지 갔었어?',
    answer_must_not: "디스크 82%까지 참, 정리 후 54%. 이 수치와 '꽉 참' 사건을 절대 재현 금지.",
    keyword_must: '디스크, 로그, 서버, 용량, df, 정리, cleanup',
    theme: "디스크/로그/용량을 언급하지만 '꽉 참(82%)' 사건은 없는 운영 한담: 디스크 여유 있음 확인, 정기 점검 OK, 로그 로테이션 설정 잡담, 다른 서버의 다른 수치(40%대 등 한가함), 모니터링 알람 안 울림.",
    window: '2024-09-15 ~ 2024-11-15', persona: '정유진, 강민석',
  },
  {
    qid: 'C3', dir: 'raw/infra/slack', count: 40, channel: '#infra',
    q: '2025년 1월에 CI 빌드 간헐적으로 깨지던 문제 원인이 뭐였어?',
    answer_must_not: "캐시 만료 시간 검증 테스트의 sleep 타이밍 의존, CI 러너 부하 때 flaky. 이 원인을 절대 재현 금지.",
    keyword_must: 'CI, 빌드, build, 파이프라인, 테스트, flaky, 깨짐',
    theme: "CI/빌드/테스트를 언급하지만 'flaky 원인(sleep 타이밍)'은 없는 잡담: 빌드 그린 축하, CI 속도 개선 잡담, 새 잡 추가, 빌드 시간 단축, 테스트 커버리지 얘기, 다른 종류의 빌드 실패(의존성 버전 등 flaky 아님).",
    window: '2024-12-15 ~ 2025-02-15', persona: '정유진, 강민석, 이준호',
  },
  {
    qid: 'A4', dir: 'raw/slack', count: 40, channel: '#pay-dev',
    q: '코지홈 가맹점이 환불 관련해서 뭐 문의했었어?',
    answer_must_not: "코지홈이 5만원 중 2만원만 부분환불 가능한지 문의, 당시 전액취소만 가능 안내. 이 사실을 절대 재현 금지.",
    keyword_must: '환불, 부분환불, 취소, 가맹점, CS, 문의',
    theme: "환불/부분환불/취소를 언급하지만 '코지홈의 2만원 문의'는 없는 다른 가맹점 CS: 다른 가맹점명(예: 마트·카페·쇼핑몰 가상 상호)의 다른 환불 문의(전액환불 시점, 환불 지연, 취소 절차 안내), 환불 정책 일반 잡담. 코지홈은 등장 금지.",
    window: '2025-07-01 ~ 2025-11-30', persona: '최민지',
  },
]

const GEN_SCHEMA = {
  type: 'object',
  required: ['files'],
  properties: {
    files: {
      type: 'array',
      description: '이 질문의 near-miss raw 파일들(키워드는 일치, 정답 사실은 없음)',
      items: {
        type: 'object',
        required: ['filename', 'date', 'content', 'why_nearmiss'],
        properties: {
          filename: { type: 'string', description: '대상 디렉토리 기준 파일명만(예: 2024-10-15-infra-disk-ok-chatter.md). 날짜-주제-kind 형식, 기존과 안 겹치게.' },
          date: { type: 'string', description: 'created 날짜 YYYY-MM-DD, 지정된 window 안.' },
          content: { type: 'string', description: 'frontmatter 포함 raw 전문. 키워드는 자연스럽게 등장하되 정답 사실은 절대 없음.' },
          why_nearmiss: { type: 'string', description: '왜 이게 near-miss인가 1줄: 어떤 키워드로 grep에 걸리고, 왜 정답이 아닌지.' },
        },
      },
    },
  },
}

const AUDIT_SCHEMA = {
  type: 'object',
  required: ['verdict', 'violations'],
  properties: {
    verdict: { type: 'string', enum: ['clean', 'dirty'] },
    violations: {
      type: 'array',
      items: {
        type: 'object',
        required: ['filename', 'rule', 'detail'],
        properties: {
          filename: { type: 'string' },
          rule: { type: 'string', enum: ['answer-leak', 'future-leak', 'keyword-missing', 'frontmatter', 'character', 'duplicate'] },
          detail: { type: 'string' },
        },
      },
    },
  },
}

const results = await pipeline(
  targets,
  // Stage 1: 질문별 near-miss 생성
  (t) =>
    agent(
      `너는 Nimbus Pay 팀의 과거 슬랙/문서 더미를 만든다. 아래 "표적 질문"의 near-miss 노이즈를 ${t.count}건 생성하라.

== near-miss의 정의 (이 작업의 핵심) ==
near-miss = 표적 질문과 **같은 키워드로 grep에 걸리지만, 정답 사실은 전혀 없는** raw다.
목적: 누군가 이 질문을 grep으로 검색하면 정답 파일과 함께 이 near-miss들이 한꺼번에 후보로 잡혀,
"키워드는 맞지만 정답 아닌" 건초가 정답 바늘을 덮게 만든다. (찾기는 되는데 고르기가 안 되게)

== 표적 질문 ==
질문: ${t.q}
이 질문의 정답(절대 재현·누설 금지): ${t.answer_must_not}
반드시 포함할 키워드(grep에 걸리도록, 자연스럽게): ${t.keyword_must}
near-miss 테마(이 방향으로 그럴듯하게): ${t.theme}

== 절대 규약 ==
1. answer-leak 금지: 위 "정답 사실"을 절대 담지 마라. 수치·결론·핵심 사건을 흉내내지도 마라.
   예) 디스크 질문이면 "82%까지 찼다"는 절대 금지 — "디스크 여유 있다/점검했다/다른 수치"는 OK.
2. keyword 필수: "${t.keyword_must}" 중 최소 하나는 자연스럽게 등장(grep 후보로 걸려야 함).
3. in-the-moment: 그 시점 그대로. 사후 주석·"나중에 ~됨" 금지.
4. future-leak 금지: 시간창(${t.window}) 이후의 사건·용어·결정 언급 금지.
5. frontmatter 필수: created(${t.window} 안), tags([${t.channel ? 'slack' : 'weekly'}, raw-dump, ...])${t.channel ? `, channel: ${t.channel}` : ''}.
6. 다양성: ${t.count}건의 날짜·작성자·세부 주제가 서로 겹치지 않게. 같은 문구 반복 금지.
7. 인물 성격·소속 일관성. 주 등장: ${t.persona}.

${CHARTER}
${RULES}

파일명은 대상 디렉토리(${t.dir}) 기준 파일명만 준다. 날짜는 ${t.window} 안에서 흩뿌려라.`,
      { label: `gen:${t.qid}`, phase: 'Generate', schema: GEN_SCHEMA, model: 'sonnet' }
    ).then((g) => ({ t, gen: g })),
  // Stage 2: 적대 audit
  (prev) => {
    if (!prev || !prev.gen) return prev
    const t = prev.t
    const files = prev.gen.files || []
    return agent(
      `너는 적대적 audit이다. 아래 near-miss raw들이 규약을 지켰는지 검사하라. 의심스러우면 dirty.

== 표적 질문 ==
${t.q}
== 이 질문의 정답(이게 새 나가면 answer-leak 위반) ==
${t.answer_must_not}
== 필수 키워드(없으면 keyword-missing 위반) ==
${t.keyword_must}
== 시간창(밖이면 future-leak) ==
${t.window}

검사 항목:
- answer-leak: 정답 사실(수치·결론·핵심 사건)을 담거나 흉내냈는가? → 가장 중요. 조금이라도 정답을 누설하면 dirty.
- keyword-missing: 필수 키워드가 하나도 없어 grep 후보로 안 걸리는가? (near-miss 자격 미달)
- future-leak: 시간창 이후 용어·사건이 있는가?
- frontmatter/character/duplicate: 형식·인물·중복.

== 검사 대상 raw들 ==
${files.map((f, i) => `[${i}] ${f.filename} (${f.date})\nwhy_nearmiss: ${f.why_nearmiss}\n${f.content}`).join('\n\n---\n\n')}`,
      { label: `audit:${t.qid}`, phase: 'Audit', schema: AUDIT_SCHEMA, model: 'sonnet' }
    ).then((a) => ({ ...prev, audit: a }))
  }
)

const ok = results.filter(Boolean)
return {
  targets: ok.map((r) => ({
    qid: r.t.qid,
    dir: r.t.dir,
    generated: (r.gen?.files || []).length,
    verdict: r.audit?.verdict,
    violations: r.audit?.violations || [],
    files: (r.gen?.files || []).map((f) => ({
      filename: f.filename,
      date: f.date,
      content: f.content,
      why_nearmiss: f.why_nearmiss,
    })),
  })),
}
