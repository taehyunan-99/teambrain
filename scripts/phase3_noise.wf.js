export const meta = {
  name: 'phase3-noise-proliferation',
  description: 'Nimbus Pay 팀×월 그리드로 일상 노이즈 raw 822건 LLM 증식 + 타임라인 audit',
  phases: [
    { title: 'Generate', detail: '71셀 각각에서 그 달 백본에 매달리는 일상 raw N건 생성' },
    { title: 'Audit', detail: '셀별 타임라인 위반(미래 누설)·인물·형식 적대 검증' },
  ],
}

// args = [{month, team, n, bb:{team:[titles]}, prev:{team:[titles]}}, ...] 71셀
const cells = args

// 캐릭터/채널 규약 — 모든 셀 프롬프트에 주입 (SIM-DESIGN §1·§2·§7)
const CHARTER = `
회사: Nimbus Pay (국내 PG·결제 인프라. 가맹점에 결제 API/SDK + 정산 제공).
인물 (성격 고정):
  결제팀(pay-dev): 김도현(테크리드,결정승인자), 박서연(시니어 백엔드,멱등성/DB,fail-closed 강경), 이준호(백엔드,PG어댑터/웹훅,키보드 잘 삼), 최민지(PM/CS,가맹점 소통·환불운영, 정산PM 겸임).
  정산팀(settlement): 한지우(리드,D+1배치/수수료/명세서,회계 정합성 깐깐), 오세훈(백엔드,배치잡/payout/CSV).
  인프라팀(infra): 정유진(SRE리드,Redis/PG운영·배포·알람), 강민석(플랫폼,K8s/오토스케일/모니터링).
채널: #pay-dev(결제 일상) #pay-incident(전사 장애) #pay-random(전사 잡담) #settlement(정산) #infra(인프라) #platform-announce(인프라→전사 공지).
팀 활성: 정산팀은 2024-08부터 존재. 인프라·결제는 2024-07부터.
`

const RULES = `
절대 규약 (어기면 audit 탈락):
1. in-the-moment: 그 시점 그대로 쓴다. 사후 주석·"나중에 ~됨"·결론 요약 금지. 관계 발견은 wiki-build의 몫.
2. 미래 누설 금지: 이 달(또는 직전월)에 아직 일어나지 않은 사건·결정·용어를 언급 금지.
   - 예: 2025-01에 "Postgres 이주"(2026), "INC-204"(2026-04), "payout_log 유니크"(2026-05) 언급 절대 금지.
   - 주어진 "이 달 백본"과 "직전월 힌트"에 있는 것까지만 안다고 가정.
3. 노이즈 성격: 이건 "건초더미"다. 일상 잡담·배포알림·CS문의·코드리뷰 한담·주간단신 위주.
   결정/장애 같은 큰 사건을 새로 만들지 말 것(그건 백본의 몫). 백본 사건을 곁눈질로 스치는 정도만.
4. frontmatter 필수: created(YYYY-MM-DD, 이 달 안의 날짜), tags([slack|pr|weekly|cs, raw-dump, ...]), slack이면 channel.
5. 인물 성격·소속 일관성 유지.
6. 다양성: 같은 셀 안에서 날짜·작성자·주제가 겹치지 않게. 수치(건수·지연·금액)는 그럴듯하게 흩뿌린다.
`

const NOISE_KINDS = `
일상 raw 유형(이 중 섞어서):
- deploy-notify: #infra/#platform-announce 배포 알림("vN.N.N 배포 완료, 롤백 절차 ~"). 짧음.
- random-chat: #pay-random 잡담(점심·날씨·밈·축하·신간). 업무 거의 없음. 진짜 노이즈.
- cs-inquiry: 최민지가 옮긴 가맹점 문의("A몰: 정산 며칠에 들어오나요?"). 사소.
- code-review: PR 코멘트 한담(리뷰 nit, 변수명, 칭찬). 큰 설계논쟁 아님.
- weekly: 그 주 단신 모음(한 일/이슈/다음주). 짧고 정형.
- ops-chatter: #infra/#settlement 운영 한담(알람 울림·배치 돌았나·디스크·점검창).
`

function teamDir(t) {
  if (t === 'settlement') return 'raw/settlement/slack'
  if (t === 'infra') return 'raw/infra/slack'
  return 'raw/slack'
}

const GEN_SCHEMA = {
  type: 'object',
  required: ['files'],
  properties: {
    files: {
      type: 'array',
      description: '이 셀에서 생성한 일상 raw 파일들',
      items: {
        type: 'object',
        required: ['filename', 'content', 'kind', 'date'],
        properties: {
          filename: { type: 'string', description: '예: 2025-01-08-pay-random-lunch.md (날짜-채널/유형-주제슬러그). 영문 슬러그.' },
          date: { type: 'string', description: 'YYYY-MM-DD, 반드시 이 셀의 달 안' },
          kind: { type: 'string', enum: ['deploy-notify', 'random-chat', 'cs-inquiry', 'code-review', 'weekly', 'ops-chatter'] },
          content: { type: 'string', description: 'frontmatter(---) + 본문 마크다운 전체. in-the-moment.' },
        },
      },
    },
  },
}

const AUDIT_SCHEMA = {
  type: 'object',
  required: ['verdict', 'violations'],
  properties: {
    verdict: { type: 'string', enum: ['pass', 'fail'] },
    violations: {
      type: 'array',
      description: '발견한 위반. 없으면 빈 배열.',
      items: {
        type: 'object',
        required: ['filename', 'rule', 'detail', 'severity'],
        properties: {
          filename: { type: 'string' },
          rule: { type: 'string', enum: ['future-leak', 'in-the-moment', 'frontmatter', 'character', 'team-active'] },
          detail: { type: 'string' },
          severity: { type: 'string', enum: ['critical', 'minor'] },
        },
      },
    },
  },
}

log(`Phase 3: ${cells.length}셀, 노이즈 총 ${cells.reduce((s, c) => s + c.n, 0)}건 증식 시작`)

const results = await pipeline(
  cells,
  // Stage 1: 생성
  (cell) => {
    const bbStr = Object.entries(cell.bb).map(([t, ts]) => `  [${t}] ${ts.join(' / ')}`).join('\n') || '  (이 달 백본 사건 없음 — 순수 일상만)'
    const prevStr = Object.entries(cell.prev || {}).map(([t, ts]) => `  [${t}] ${ts.join(' / ')}`).join('\n') || '  (직전월 힌트 없음)'
    return agent(
      `너는 Nimbus Pay ${cell.team}팀의 ${cell.month} 한 달치 "일상 노이즈" raw를 ${cell.n}건 생성한다.
${CHARTER}
${RULES}
${NOISE_KINDS}

== 이 셀 ==
대상 팀: ${cell.team}
달: ${cell.month} (모든 created 날짜는 이 달 안)
생성 건수: 정확히 ${cell.n}건

== 이 달 백본 사건 (전팀, 곁눈질로만 스치기) ==
${bbStr}

== 직전월 힌트 (이미 알아도 되는 과거) ==
${prevStr}

위 백본/직전월에 없는 미래 사건·용어는 절대 언급 금지. ${cell.team}팀 관점의 일상을 ${cell.n}건, 날짜·작성자·주제를 흩뿌려 생성하라. 파일명은 날짜로 시작하는 영문 슬러그.`,
      { label: `gen:${cell.month}/${cell.team}`, phase: 'Generate', schema: GEN_SCHEMA }
    ).then((r) => ({ cell, gen: r }))
  },
  // Stage 2: 타임라인 audit (해당 셀만 적대 검증)
  (prev) => {
    if (!prev || !prev.gen || !prev.gen.files) return prev
    const cell = prev.cell
    const filesStr = prev.gen.files.map((f) => `### ${f.filename} (kind=${f.kind}, date=${f.date})\n${f.content}`).join('\n\n---\n\n')
    const allowedBB = Object.values(cell.bb).flat().concat(Object.values(cell.prev || {}).flat())
    return agent(
      `너는 적대적 검증자다. Nimbus Pay ${cell.team}팀 ${cell.month} 노이즈 raw ${prev.gen.files.length}건을 검사한다.
규약 위반을 찾아라. 의심되면 fail 쪽으로 기울여라.

검사 항목:
- future-leak(critical): ${cell.month}(+직전월)에 아직 없는 미래 사건·결정·용어 언급. 허용된 사건 맥락은 다음뿐:
${allowedBB.map((x) => `    · ${x}`).join('\n') || '    (없음 — 순수 일상만 허용)'}
  특히 금지 용어 예: Postgres/postgresql 이주(2026), INC-204(2026-04), INC-231/payout_log 유니크(2026-05), multi-PG 라우팅 등은 그 시점 이후에만.
- in-the-moment(critical): 사후 주석·"나중에 ~로 이어짐"·결론 요약.
- frontmatter(minor): created 누락/이 달 밖 날짜, tags 누락, slack인데 channel 누락.
- character(minor): 인물 성격·소속 모순.
- team-active(critical): 정산팀인데 ${cell.month}이 2024-08 이전.

== 검사 대상 ==
${filesStr}`,
      { label: `audit:${cell.month}/${cell.team}`, phase: 'Audit', schema: AUDIT_SCHEMA }
    ).then((v) => ({ ...prev, audit: v }))
  }
)

const ok = results.filter(Boolean)
const totalFiles = ok.reduce((s, r) => s + (r.gen?.files?.length || 0), 0)
const failed = ok.filter((r) => r.audit?.verdict === 'fail')
const critical = ok.flatMap((r) => (r.audit?.violations || []).filter((v) => v.severity === 'critical').map((v) => ({ cell: `${r.cell.month}/${r.cell.team}`, ...v })))

log(`생성 완료: ${totalFiles}건, fail 셀: ${failed.length}, critical 위반: ${critical.length}`)

return {
  totalCells: cells.length,
  okCells: ok.length,
  totalFiles,
  failedCells: failed.map((r) => `${r.cell.month}/${r.cell.team}`),
  criticalViolations: critical.slice(0, 50),
  // 디스크 기록용 전체 파일 (셀 메타 포함)
  files: ok.flatMap((r) =>
    (r.gen?.files || []).map((f) => ({
      month: r.cell.month,
      team: r.cell.team,
      filename: f.filename,
      kind: f.kind,
      content: f.content,
      auditVerdict: r.audit?.verdict || 'unknown',
    }))
  ),
}
