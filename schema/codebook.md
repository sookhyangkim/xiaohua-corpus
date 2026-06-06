# 데이터 사전 (codebook)

코퍼스를 신뢰·인용·재사용하려면 모든 필드의 정의가 명확해야 한다.
필드를 추가·변경하면 반드시 여기에 반영한다.

## 이본(witness) 필드 — `witnesses/<source>/*.md`

| 필드 | 필수 | 타입 | 정의 |
|------|------|------|------|
| `id` | ✓ | str | 이본 고유 ID. `<source-slug>-####` 형식. |
| `type_id` | ✓ | str | 연결되는 유형 ID (`XH-####`). 미정이면 `null`. |
| `source` | ✓ | str | `schema/sources.yaml`의 키. |
| `juan` | | str | 권/회 위치 (예: 卷三). |
| `editor` | | str | 편자명. |
| `operations` | | list | `schema/operations.yaml`의 키 목록. |
| `register` | | str | 雅 / 俗 / 雅俗混 중 하나. |
| `folk` | | bool | 民間笑話 여부. |
| `text_orig` | ✓ | str | 저본 그대로. 異體字·簡繁 혼입 보존. |
| `text_normalized` | | str | OpenCC 번체 정규화본. build 시 자동 생성 가능. |
| `translation_ko` | | str | 한국어 역. |
| `comment_orig` | | str | 편자 평(評) 원문. |
| `notes` | | str | 교감·역주·변이형 기록. |

## 유형(type) 필드 — `types/*.md`

| 필드 | 필수 | 타입 | 정의 |
|------|------|------|------|
| `id` | ✓ | str | 유형 ID (`XH-####`). |
| `label` | ✓ | str | 짧은 유형명. |
| `knot` | | str | 매듭(Verknotung): 농담이 세우는 긴장·기대. |
| `unknot` | | str | 풀림(Entknotung): 그 긴장을 무너뜨리는 전환점. |
| `xref` | | list | 외부 색인 교차참조 (ATU·기존 소화 유형색인 등). |
| `notes` | | str | 비고. |

## 통제 규칙

- `register` 값은 위 세 가지로 한정. 새 값 도입 시 여기 먼저 등록.
- `operations`는 `operations.yaml`에 없는 키를 쓰지 않는다.
- 본문은 `text_orig`가 정본이며, `text_normalized`는 파생물로 간주한다.
