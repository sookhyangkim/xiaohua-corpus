# 明清笑話 코퍼스 (xiaohua-corpus)

명청대 소화(笑話) 텍스트의 연구용 코퍼스. 졸레스(André Jolles)의 단순형/현재화
(simple form / aktualisierte Form) 구분을 데이터 모델의 척추로 삼아, 한 농담형이
여러 선집에서 어떻게 다르게 실현·재편집되었는지를 추적할 수 있게 설계되었다.

## 데이터 모델: 2층 구조

| 레이어 | 위치 | 한 항목 = | 핵심 질문 |
|--------|------|-----------|-----------|
| **유형(type)** | `types/` | 추상적 농담형 하나 | 이 농담의 구조적 핵(매듭/풀림)은 무엇인가 |
| **이본(witness)** | `witnesses/<선집>/` | 선집에 실제 실현된 출현 하나 | 이 선집은 그 농담을 어떻게 현재화했는가 |

두 레이어는 이본의 `type_id`로 연결된다. 이 분리가 cross-anthology 분석
(선집별 편집 조작 빈도, 雅/俗 위계, 民間笑話 하위코퍼스 추출 등)의 토대다.

## 디렉터리

```
schema/      통제 어휘·서지·데이터 사전 (분석의 기준)
types/       유형 항목 (XH-####.md)
witnesses/   선집별 이본 항목
scripts/     정규화·빌드·통계 스크립트
build/        파생 산출물 (gitignore; release에만 첨부)
```

## 워크플로

1. `witnesses/`, `types/`에 `.md` 항목을 사람이 편집한다 (**진실의 원천**).
2. `python scripts/build.py` → `build/corpus.jsonl` + `build/corpus.sqlite` 생성.
3. `python scripts/stats.py` → 선집별 조작 빈도표 등 점검.
4. 의미 있는 상태마다 git tag(`v0.1`, `v0.2`…)로 코퍼스 버전을 고정한다.

## 버전·인용

- **Releases/Tags** = 코퍼스 버전. 논문은 이 태그를 핀으로 박아 인용한다.
- GitHub–Zenodo 연동을 켜면 release마다 DOI가 발급된다 → 재현 가능한 인용.
- `CITATION.cff` 참조.

## 라이선스 (레이어 분리)

- **원문(text_orig / text_normalized)**: 전근대 텍스트로 퍼블릭 도메인.
- **번역·역주·태그·유형 기술**: 저자의 지적 산물. CC BY-NC 4.0 적용.

자세한 내용은 `LICENSE` 참조.
