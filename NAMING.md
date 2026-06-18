# 파일 명명 규칙 (Naming Convention)

본 레포(`xiaohua-corpus`)의 모든 텍스트·데이터 파일은 아래 규칙을 따른다.
책 → 권 → 部 → 층위 순으로 정보를 담아, 다른 部·다른 책으로 확장해도
정렬과 인용이 깨지지 않도록 한다.

## 1. 기본 형식

```
{work}_{juan}_{section}_{layer}.{ext}
```

| 슬롯 | 의미 | 표기 | 예 |
|------|------|------|----|
| `work`    | 책   | 소문자 병음 | `xiaofu`(笑府), `gujin`(古今譚概), `xiaolin`(笑林廣記) |
| `juan`    | 권   | `j` + 2자리 숫자 | `j10`(卷十) |
| `section` | 部   | 소문자 병음 | `xingtibu`(形體部) |
| `layer`   | 층위 | 아래 §2 | `text`, `comment`, `apparatus` |
| `ext`     | 형식 | 소문자 | `txt`, `jsonl`, `csv` |

규칙: **소문자·언더바·ASCII만** 사용한다. 공백·한자·대문자를 파일명에 넣지 않는다.
숫자는 0-padding 하여(`j09`, `j10`) 사전식 정렬이 곧 권 순서가 되게 한다.

## 2. 층위 코드 (워크북 ①②③에 대응)

| 코드 | 내용 | 분석상 위치 |
|------|------|-------------|
| `text`      | 笑話 본문 (웃음의 대상) | ① 주분석 코퍼스 |
| `comment`   | 評語 · 小序 (편자의 framing) | ② register 대비 코퍼스 |
| `apparatus` | 異文 · 校勘 · 夾註 (방언·교감 주기) | ③ 분석 제외 |

## 3. 버전 관리

버전 번호(`v1`, `v2`, `final` 등)를 **파일명에 넣지 않는다.**
버전은 Git commit·tag·`CITATION.cff` 로 관리한다. 파일명에 버전을 박으면
인용 링크와 스크립트 경로가 깨진다.

## 4. 현재 수록 파일

| 파일 | 내용 |
|------|------|
| `witnesses/xiaofu_j10_xingtibu_text.txt`   | 形體部 笑話 본문 58편 (사람이 읽는 정리본) |
| `witnesses/xiaofu_j10_xingtibu_text.jsonl` | 위와 동일 내용의 기계가독 정본 |

## 5. 확장 예시

| 내용 | 파일명 |
|------|--------|
| 形體部 評語·小序 | `xiaofu_j10_xingtibu_comment.txt` |
| 形體部 교감 데이터 | `xiaofu_j10_xingtibu_apparatus.csv` |
| 다른 部(예: 腐流部) 본문 | `xiaofu_jNN_furliubu_text.txt` |
| 古今譚概 해당 部 본문 | `gujin_jNN_xxxbu_text.txt` |

## 6. JSONL 필드 규격 (`*_text.jsonl`)

각 줄은 笑話 1편 = 1 레코드.

| 필드 | 형 | 설명 |
|------|----|------|
| `id`        | int     | 部 내 연속 번호 (1–58) |
| `work`      | string  | 책명 (笑府) |
| `juan`      | int     | 권 (10) |
| `section`   | string  | 部 (形體部) |
| `title`     | string\|null | 篇名. `又` 및 篇名 없는 추가편은 `null` |
| `topic`     | string  | 소속 主題 = 직전 篇名 (又·추가편이 상속) |
| `you`       | bool    | `true` = 直前 篇名과 同題의 추가편(又) |
| `n_han_raw` | int     | 본문 한자 수 (구두점 제외, **정규화 이전 raw 값**) |
| `text`      | string  | 笑話 본문 |

`title`·`you` 두 필드만으로 세 유형이 구분된다.
- 篇名 있음: `title != null`
- 又(同題 추가편): `you == true`
- 篇名 없는 同題 추가 소화: `title == null && you == false`

> `n_han_raw` 는 파일 자체의 글자 수이며, 워크북의 정규화 후 빈도 분석값
> (① 본문 3,366자 등)과 산정 범위·기준이 다르다. 빈도 분석에는 워크북 수치를 쓴다.
