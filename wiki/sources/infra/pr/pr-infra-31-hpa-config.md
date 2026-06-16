---
type: source
of: raw/infra/pr/pr-infra-31-hpa-config.md
source_hash: a33d23a3209d66520a8380d1dd369ee1f30318ff
tags: [source]
---

## Summary
결제 API HPA 도입+resource 조정 PR #31에서 정유진이 maxReplicas와 DB 커넥션 한도 연동(파드당 풀 20→10, maxReplicas 10→8로 8×10=80<100), scaleDown stabilizationWindow 0초의 플래핑 위험(scaleUp 즉시/scaleDown 300초 비대칭 설정), HPA averageUtilization 분모인 requests.cpu 실측 기반 산정(250m/limits 500m, 타깃 70%)을 지적해 반영시켰다.

## Concepts
- 오토스케일링 HPA
- MySQL HA/백업
- Kubernetes 마이그레이션
