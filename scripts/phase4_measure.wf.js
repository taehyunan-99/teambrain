export const meta = {
  name: 'phase4-routing-limit-measure',
  description: 'index.md 라우팅(agentic retrieval)이 16개 질문에서 어디까지 답하나 측정 + 채점',
  phases: [
    { title: 'Retrieve', detail: '질문별 에이전트가 index.md→파일 직접읽기로 답 시도' },
    { title: 'Grade', detail: 'truth_fact 대조 채점 + 실패유형 분류' },
  ],
}

// __QUESTIONS__ 인라인 교체 / __INDEX__ 인라인 교체
const questions = __QUESTIONS__
const INDEX_MD = __INDEX__

const RETRIEVE_SCHEMA = {
  type: 'object',
  required: ['answer', 'files_opened', 'reached', 'confidence', 'notes'],
  properties: {
    answer: { type: 'string', description: '최종 답변(찾은 만큼만, 모르면 모른다고)' },
    files_opened: { type: 'array', items: { type: 'string' }, description: '실제로 열어본 파일 경로(순서대로). 라우팅 경로 추적용.' },
    reached: { type: 'boolean', description: '질문에 실질적으로 답했다고 스스로 판단하면 true, 못 찾았으면 false' },
    confidence: { type: 'string', enum: ['high', 'medium', 'low', 'none'] },
    notes: { type: 'string', description: '탐색 중 막힌 지점/추측한 부분/index.md에 단서가 있었는지' },
  },
}

const GRADE_SCHEMA = {
  type: 'object',
  required: ['verdict', 'failure_type', 'reason', 'hit_truth_file'],
  properties: {
    verdict: { type: 'string', enum: ['correct', 'partial', 'wrong', 'no-answer'] },
    failure_type: {
      type: 'string',
      enum: ['none', 'proper-noun-miss', 'vocab-mismatch', 'haystack-buried', 'relation-miss', 'hallucination'],
      description: '실패 원인. correct면 none. proper-noun-miss=고유명사를 라우팅이 못짚음, vocab-mismatch=어휘달라 못찾음, haystack-buried=노이즈에 묻혀 못찾음, relation-miss=관계 못이음, hallucination=없는걸 지어냄',
    },
    hit_truth_file: { type: 'boolean', description: 'files_opened가 truth_files 중 하나라도 포함하면 true' },
    reason: { type: 'string', description: '판정 근거 1~2줄' },
  },
}

const results = await pipeline(
  questions,
  // Stage 1: retrieve (index.md만 보고 출발)
  (q) =>
    agent(
      `너는 Nimbus Pay 팀 위키를 검색하는 어시스턴트다. 아래 index.md(개념 카탈로그)를 단서로 삼아 질문에 답하라.

== 동작 규칙 (실제 시스템 재현) ==
- 출발점은 index.md뿐이다. 여기 링크된 wiki 아티클(wiki/*.md)을 Read로 열어볼 수 있고, 아티클의 sources/wikilink를 따라 raw/*.md도 열 수 있다.
- index.md에 단서가 없으면 wiki/ 디렉토리를 Glob/Grep으로 뒤지거나 raw/를 직접 탐색해도 된다(단 raw는 987개라 다 못 읽는다 — 현실적으로 키워드 grep에 의존).
- 찾은 만큼만 답하라. 모르면 솔직히 "못 찾음". 지어내지 마라.
- 어떤 파일을 열었는지 files_opened에 순서대로 정확히 기록하라.

== index.md ==
${INDEX_MD}

== 질문 ==
${q.q}`,
      { label: `retrieve:${q.id}`, phase: 'Retrieve', schema: RETRIEVE_SCHEMA, agentType: 'Explore' }
    ).then((r) => ({ q, retrieve: r })),
  // Stage 2: grade
  (prev) => {
    if (!prev || !prev.retrieve) return prev
    const q = prev.q
    const r = prev.retrieve
    const hitTruth = (r.files_opened || []).some((f) => q.truth_files.some((t) => f.includes(t.replace('raw/', '').replace('wiki/', '')) || t.includes(f)))
    return agent(
      `채점자다. 질문에 대한 검색 답변을 정답과 대조해 판정하라.

== 질문 ==
${q.q}

== 정답(truth_fact) ==
${q.truth_fact}

== 정답이 든 파일(truth_files) ==
${q.truth_files.join(', ')}

== 이 질문의 측정 의도(probe) ==
${q.probe}

== 검색 결과 ==
답변: ${r.answer}
스스로 답했다 판단: ${r.reached} (confidence=${r.confidence})
열어본 파일: ${(r.files_opened || []).join(', ') || '(없음)'}
탐색 메모: ${r.notes}
(truth_file 도달 추정: ${hitTruth})

핵심 사실을 맞췄으면 correct, 일부만 partial, 틀리면 wrong, 못 찾았으면 no-answer.
실패면 failure_type을 probe 의도에 비춰 정확히 분류하라(고유명사 못짚음/어휘불일치/노이즈매몰/관계못이음/환각).`,
      { label: `grade:${q.id}`, phase: 'Grade', schema: GRADE_SCHEMA }
    ).then((g) => ({ ...prev, grade: g, hitTruth }))
  }
)

const ok = results.filter(Boolean)
const byType = {}
for (const r of ok) {
  const t = r.q.type
  byType[t] = byType[t] || { total: 0, correct: 0, partial: 0, fail: 0 }
  byType[t].total++
  if (r.grade?.verdict === 'correct') byType[t].correct++
  else if (r.grade?.verdict === 'partial') byType[t].partial++
  else byType[t].fail++
}
const failTypes = {}
for (const r of ok) {
  const ft = r.grade?.failure_type
  if (ft && ft !== 'none') failTypes[ft] = (failTypes[ft] || 0) + 1
}

return {
  total: ok.length,
  byType,
  failTypes,
  rows: ok.map((r) => ({
    id: r.q.id,
    type: r.q.type,
    q: r.q.q,
    verdict: r.grade?.verdict,
    failure_type: r.grade?.failure_type,
    confidence: r.retrieve?.confidence,
    reached: r.retrieve?.reached,
    hitTruth: r.hitTruth,
    files_opened: r.retrieve?.files_opened,
    answer: r.retrieve?.answer,
    grade_reason: r.grade?.reason,
  })),
}
