---
created: 2026-06-10
tags: [pr-review, raw-dump, settlement]
pr: 162
---

# PR #162 — feat: 정산명세서 CSV 내보내기 (draft)

> 작성: 박서연 (준호 휴가로 초안만) / 리뷰: 미시작 / 상태: draft

**박서연**: 가맹점 C 요구 컬럼(거래ID/승인일시/금액/수수료/정산액)으로 draft 올려둡니다. 준호님 복귀하면 인계. 명세서 생성 로직에 exporter 인터페이스만 하나 추가한 구조라 PDF/CSV가 같은 데이터 소스를 봐요
**박서연**: TODO — 인코딩(엑셀 호환 BOM), 10만 행 스트리밍, 대시보드 다운로드 버튼
