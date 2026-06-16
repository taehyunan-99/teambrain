# _log — 빌드 감사 로그

> `wiki-build` 스킬이 실행될 때마다 결과를 append한다.

## 2026-06-12 00:00 빌드 (1회차 — 초기 빌드)

- [NEW] wiki/sources/hybrid-search-overview.md — 소스 요약 생성
- [NEW] wiki/sources/rrf-algorithm.md — 소스 요약 생성
- [NEW] wiki/sources/sqlite-vec-local-vector-search.md — 소스 요약 생성
- [NEW] wiki/sources/bm25-sparse-retrieval.md — 소스 요약 생성
- [NEW] wiki/hybrid-search.md — 개념 아티클 생성 (sources: hybrid-search-overview, rrf-algorithm, sqlite-vec-local-vector-search, bm25-sparse-retrieval)
- [NEW] wiki/rrf.md — 개념 아티클 생성 (sources: rrf-algorithm, hybrid-search-overview, sqlite-vec-local-vector-search, bm25-sparse-retrieval)
- [NEW] wiki/bm25.md — 개념 아티클 생성 (sources: bm25-sparse-retrieval, hybrid-search-overview, sqlite-vec-local-vector-search)
- [NEW] wiki/sqlite-vec.md — 개념 아티클 생성 (sources: sqlite-vec-local-vector-search, hybrid-search-overview, bm25-sparse-retrieval)
- [UPDATE] index.md — auto 마커 영역 갱신 (4개 개념 카탈로그)

빌드 요약: 신규 8개 (source 4 + concept 4), 갱신 1개 (index.md), 스킵 0개, 실패 0개

## 2026-06-12 00:01 빌드 (2회차 — 멱등성 검증)

- [SKIP:변경없음] raw/hybrid-search-overview.md — source_hash 일치 (b505bee2...)
- [SKIP:변경없음] raw/rrf-algorithm.md — source_hash 일치 (64072238...)
- [SKIP:변경없음] raw/sqlite-vec-local-vector-search.md — source_hash 일치 (6c4f0849...)
- [SKIP:변경없음] raw/bm25-sparse-retrieval.md — source_hash 일치 (4079f79f...)

빌드 요약: 신규 0개, 갱신 0개, 스킵 4개 (변경없음), 실패 0개

## 2026-06-12 00:02 빌드 (3회차 — 증분 갱신 검증)

- [SKIP:변경없음] raw/hybrid-search-overview.md — source_hash 일치 (b505bee2...)
- [UPDATE] raw/rrf-algorithm.md → wiki/sources/rrf-algorithm.md, wiki/rrf.md — source_hash 변경 (64072238... → 298e92fa...), 내용: k값 튜닝 정보 추가
- [SKIP:변경없음] raw/sqlite-vec-local-vector-search.md — source_hash 일치 (6c4f0849...)
- [SKIP:변경없음] raw/bm25-sparse-retrieval.md — source_hash 일치 (4079f79f...)

빌드 요약: 신규 0개, 갱신 1개 (rrf), 스킵 3개 (변경없음), 실패 0개

## 2026-06-12 00:03 빌드 (4회차 — 손수정 보호 검증)

- [SKIP:변경없음] raw/hybrid-search-overview.md — source_hash 일치
- [SKIP:변경없음] raw/rrf-algorithm.md — source_hash 일치
- [SKIP:변경없음] raw/sqlite-vec-local-vector-search.md — source_hash 일치
- [SKIP:변경없음] raw/bm25-sparse-retrieval.md — source_hash 일치
- [SKIP:손수정] wiki/bm25.md — llmwiki:auto 마커 없음, 손수정 보호

빌드 요약: 신규 0개, 갱신 0개, 스킵 4개 (변경없음 3 + 손수정 1), 실패 0개

## 2026-06-12 00:04 빌드 (5회차 — 실패 격리 검증)

- [SKIP:변경없음] raw/hybrid-search-overview.md — source_hash 일치
- [SKIP:변경없음] raw/rrf-algorithm.md — source_hash 일치
- [SKIP:실패] raw/sqlite-vec-local-vector-search.md — 빈 파일, 파싱 불가 (hash 변경: 6c4f0849... → e69de29b...) — 나머지 빌드 계속
- [SKIP:변경없음] raw/bm25-sparse-retrieval.md — source_hash 일치

빌드 요약: 신규 0개, 갱신 0개, 스킵 4개 (변경없음 3 + 실패 1), 실패 0개 (전체 차단 없음)

## 2026-06-12 회사 더미 빌드 (Nimbus Pay 결제팀)

- [ARCHIVE] 기술 샘플(hybrid-search/rrf/bm25/sqlite-vec) → _archive/ 이동 (회사 데이터와 분리)
- [NEW] wiki/idempotency.md — 멱등성 (sources: 3/11결정·INC-204·4/29결정·INC-231·5/20트러블슈팅)
- [NEW] wiki/async-payment-approval.md — 비동기 결제 승인
- [NEW] wiki/payment-gateway-abstraction.md — PG 추상화
- [NEW] wiki/webhook-delivery.md — 웹훅 전송 (재시도+서명)
- [NEW] wiki/settlement-batch.md — 정산 배치
- [NEW] wiki/postgresql-choice.md — PostgreSQL 선택
- [NEW] wiki/fail-closed-principle.md — fail-closed 원칙
- sources 11개 생성, dangling 없음

## 2026-06-12 비정형 대량 빌드 (raw 75개 신규)

- dirty: 신규 75 (slack 35 / pr 20 / transcript 8 / weekly 12) · 기존 11 = hash 일치 스킵
- [NEW] wiki/sources/ 75개 (미러 구조: sources/slack/, sources/pr/, sources/transcripts/)
- [NEW] wiki/fee-calculation.md — 수수료 절사 (PR-127 + 약관 5조2항)
- [NEW] wiki/oncall-and-alerting.md — 온콜 로테이션(슬랙 결정) + 알람 단계화
- [NEW] wiki/refund-flow.md — Q3 과제 (미착수 상태 명시)
- [UPDATE] idempotency — PR-112 fail-open 기원, 구현 디테일(ON CONFLICT/request_hash/SDK), TTL 48h 미결 추가
- [UPDATE] async-payment-approval — 폴링 워커, bulkhead 산정식, 킥오프 배경(전 회사 트라우마)
- [UPDATE] payment-gateway-abstraction — 동기/비동기 경계, 에러 매핑 규칙, Q3 라우팅
- [UPDATE] webhook-delivery — jitter, at-least-once 모델, raw bytes 서명, 시크릿 관리(슬랙 결정), PR-159 보류
- [UPDATE] settlement-batch — 복합 유니크 키(슬랙 결정), 반개구간, payout 가드 상세, 락 선택 논쟁, CSV 진행중
- [UPDATE] postgresql-choice — NUMERIC(19,4) 근거, FOR UPDATE 락 순서, pgcrypto
- [UPDATE] fail-closed-principle — PR-112 기원 서사, 도메인 의존 개념, 적용 사례 확대
- [UPDATE] index.md — 10개 개념 카탈로그
- 잡담 2건(회식·키보드)은 소스 요약에 '개념 없음' 처리. dangling 없음 목표

## 2026-06-16 빌드 (증분 — dirty 2건)

- [NEW] wiki/sources/slack/2026-06-15-idem-ttl-48h-approved.md — 소스 요약 생성
- [NEW] wiki/sources/2026-06-16-decision-multi-pg-routing.md — 소스 요약 생성
- [UPDATE] wiki/idempotency.md — 머지 갱신: TTL 24h→48h 승인 반영 (sources: raw/slack/2026-06-15-idem-ttl-48h-approved.md)
- [UPDATE] wiki/payment-gateway-abstraction.md — 머지 갱신: 멀티 PG 라우팅 Q3 착수 결정 반영 (sources: raw/2026-06-16-decision-multi-pg-routing.md)
- [UPDATE] index.md — auto 마커 영역 갱신 (idempotency·payment-gateway-abstraction 상태 문구)
- [SKIP:변경없음] raw/* (위 2건 외 전부) — git untracked 아님 + source_hash 일치
