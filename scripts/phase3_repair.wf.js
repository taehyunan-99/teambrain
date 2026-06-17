export const meta = {
  name: 'phase3-repair-future-leaks',
  description: 'Phase 3 노이즈 raw 중 future-leak 16건을 in-the-moment로 정밀 수리 + 재audit',
  phases: [
    { title: 'Repair', detail: 'future-leak 문장만 그 시점 일상으로 교정' },
    { title: 'Reaudit', detail: '수리본에 미래 누설이 남았는지 재검증' },
  ],
}

// __ITEMS__ 가 인라인으로 교체됨
const items = __ITEMS__

const REPAIR_SCHEMA = {
  type: 'object',
  required: ['filename', 'content', 'changes'],
  properties: {
    filename: { type: 'string' },
    content: { type: 'string', description: '수리된 파일 전체(frontmatter 포함). future-leak만 제거하고 나머지는 보존.' },
    changes: { type: 'string', description: '무엇을 어떻게 고쳤는지 1~2줄' },
  },
}

const REAUDIT_SCHEMA = {
  type: 'object',
  required: ['clean', 'remaining'],
  properties: {
    clean: { type: 'boolean', description: 'future-leak이 모두 제거됐으면 true' },
    remaining: { type: 'string', description: '남은 위반이 있으면 설명, 없으면 빈 문자열' },
  },
}

const results = await pipeline(
  items,
  // Stage 1: 수리
  (it) => {
    const vio = it.violations.map((v, i) => `  ${i + 1}. [${v.rule}] ${v.detail}`).join('\n')
    const allowed = Object.entries(it.allowed_this_month).map(([t, ts]) => `  [${t}] ${ts.join(' / ')}`).join('\n') || '  (이 달 백본 없음 — 순수 일상만 허용)'
    const prev = Object.entries(it.allowed_prev_month).map(([t, ts]) => `  [${t}] ${ts.join(' / ')}`).join('\n') || '  (직전월 없음)'
    return agent(
      `너는 Nimbus Pay 위키의 더미 raw를 수리한다. 이 파일은 ${it.month} 시점의 일상 노이즈인데, 적대적 audit이 future-leak(미래 사건/용어 누설)을 잡았다.

규칙:
- 지적된 future-leak 문장/표현만 그 시점에 자연스러운 일상으로 바꾸거나 삭제한다. 미래에 일어날 사건·결정·고유용어(예: 온보딩 가맹점명, ProxySQL, fail-closed 원칙, 부분환불, 자동 D+1 배치 등 아직 없는 것)를 곁눈질로라도 전제하지 말 것.
- 나머지(잡담·인물·말투·날짜·frontmatter)는 최대한 보존. 톤은 그대로.
- in-the-moment 유지: 사후 주석 금지.
- 길이는 비슷하게. 문장을 들어내면 그 자리에 그 시점에 맞는 평범한 일상 한담으로 메운다(억지로 사건 만들지 말 것).

== 이 시점(${it.month})에 허용된 사건 맥락(이것까지만 알 수 있음) ==
${allowed}
직전월 힌트:
${prev}

== audit이 잡은 위반 ==
${vio}

== 수리 대상 파일 (${it.filename}) ==
${it.current_content}

위반을 제거한 전체 파일을 반환하라.`,
      { label: `repair:${it.filename}`, phase: 'Repair', schema: REPAIR_SCHEMA }
    ).then((r) => ({ it, repair: r }))
  },
  // Stage 2: 재audit
  (prev) => {
    if (!prev || !prev.repair) return prev
    const it = prev.it
    const allowed = Object.entries(it.allowed_this_month).map(([t, ts]) => `  [${t}] ${ts.join(' / ')}`).join('\n') || '  (없음)'
    return agent(
      `적대적 재검증. ${it.month} 시점 노이즈 raw 수리본에 미래 누설(future-leak)이 남았는지 본다. 의심되면 clean=false.

이 시점에 허용된 사건 맥락(이것까지만):
${allowed}
(특히 금지: Postgres 이주(2026), INC-204(2026-04), INC-231/payout_log(2026-05), ProxySQL/multi-PG, fail-closed 원칙 확립, 부분환불 등은 각 사건 시점 이후에만)

원래 잡혔던 위반: ${it.violations.map((v) => v.detail.slice(0, 120)).join(' | ')}

== 수리본 ==
${prev.repair.content}`,
      { label: `reaudit:${it.filename}`, phase: 'Reaudit', schema: REAUDIT_SCHEMA }
    ).then((v) => ({ ...prev, reaudit: v }))
  }
)

const ok = results.filter(Boolean)
const stillDirty = ok.filter((r) => r.reaudit && r.reaudit.clean === false)

return {
  repaired: ok.length,
  clean: ok.filter((r) => r.reaudit?.clean === true).length,
  stillDirty: stillDirty.map((r) => ({ filename: r.it.filename, remaining: r.reaudit.remaining })),
  files: ok.map((r) => ({
    path: r.it.path,
    filename: r.repair.filename,
    content: r.repair.content,
    changes: r.repair.changes,
    clean: r.reaudit?.clean,
  })),
}
