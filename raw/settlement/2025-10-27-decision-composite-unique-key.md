---
created: 2025-10-27
tags: [decision, settlement, database, idempotency]
---

# 결정: 정산 테이블 복합 유니크 키 (merchant_id, settlement_date)

- 일시: 2025-10-27
- 결정자: 한지우, 오세훈

## 배경
9월에 배치가 중간에 끊긴 뒤 실패 가맹점만 재처리하는 과정에서 일부 가맹점의 정산 행이 중복 생성됐다. 같은 가맹점·같은 정산일에 행이 둘씩 잡혀 집계 금액이 두 배로 나온 케이스가 CS로 들어왔고, 손으로 중복 행을 골라 지웠다. D+1 배치는 부분 재실행을 전제로 운영돼 왔는데 정작 "한 정산일 한 가맹점 한 행"을 보장하는 장치가 코드 레벨에만 있었다.

## 검토한 대안
1. 애플리케이션단 중복 체크: INSERT 전에 SELECT로 기존 행 존재 여부 확인. → 조회와 삽입 사이 경쟁 조건 여지. 동시에 두 워커가 같은 가맹점을 처리하면 둘 다 "없음"을 보고 둘 다 INSERT. 약함. 탈락.
2. **복합 유니크 (merchant_id, settlement_date) + upsert (채택)**: DB(MySQL)에 복합 유니크 제약을 걸고, 재실행 INSERT가 충돌하면 `ON DUPLICATE KEY UPDATE`로 기존 행을 갱신.
3. 별도 `settlement_key` 컬럼: `merchant_id|settlement_date`를 문자열로 합친 단일 유니크 컬럼. → (merchant_id, settlement_date)가 이미 그 키를 표현함. 불필요한 중복 컬럼. 탈락.

## 결정
- 정산 테이블에 **복합 유니크 제약 `UNIQUE(merchant_id, settlement_date)`**를 건다.
- 배치 재실행은 INSERT가 아니라 **`INSERT ... ON DUPLICATE KEY UPDATE`**(upsert)로 처리. 복합 유니크 충돌 시 기존 행의 집계 금액·수수료·상태를 갱신.
- 정합성의 최종 보증은 코드가 아니라 **DB 제약**이 진다.

## 근거
- 한 정산일에 한 가맹점은 한 행이어야 한다. 이건 비즈니스 불변식이고, 불변식은 DB가 강제하는 게 맞다.
- 사람이 배치를 두 번 돌리든, 워커가 동시에 같은 가맹점을 잡든, 코드에 버그가 있든 — 어떤 경우에도 중복 행이 물리적으로 생길 수 없게 된다.
- 애플리케이션 체크는 "대부분의 경우" 막아주지만 경쟁 조건에서 뚫린다. 돈 다루는 테이블에서 "대부분"은 부족하다.

## 리스크
- **이미 송금된 행을 upsert가 덮어쓰는 위험**: 재실행이 PAID 상태 행까지 UPDATE하면 송금 완료된 정산을 미정산처럼 되돌릴 수 있다.
  - → upsert의 UPDATE에 **PAID 보호** 가드. 이미 PAID인 행은 갱신하지 않고 그대로 둔다. (MySQL이라 `ON DUPLICATE KEY UPDATE`에 WHERE를 못 거니까, `IF(status='PAID', status, VALUES(status))` 식으로 PAID면 기존 값을 유지하게 컬럼별로 막는다.)
- 기존 테이블에 이미 들어 있는 중복 행 정리 후에 제약을 걸어야 함 → 마이그레이션 전에 중복 정리 스크립트 선행.
