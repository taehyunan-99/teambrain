---
created: 2025-04-18
tags:
  - weekly
  - raw-dump
  - infra
---

# 인프라팀 주간 단신 (2025-04-14 ~ 04-18)

## 한 일
- redis prometheus exporter 설정 정리 (job 이름 `redis-pay-prod`, scrape 30s) — 강민석
- 로그 수집 노드 retention 30일 → 14일 단축, 디스크 80% 알람 추가 — 강민석
- vault TLS 인증서 갱신 — 정유진
- B스토어 결제 지연 CS 확인 (PG 응답 변동, 자체 인프라 이상 없음) — 정유진

## 이슈
- redis 알람 threshold 아직 미정 (메모리 사용 패턴 더 관찰 필요)
- 결제 access 로그 증가 추세 — 트래픽 늘면 디스크 재검토

## 다음 주
- redis used_memory 기본 알람 임계치 잡아보기
- K8s 노드 리소스 사용률 대시보드 정리
