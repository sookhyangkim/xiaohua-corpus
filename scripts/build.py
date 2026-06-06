"""
빌드 스크립트: witnesses/, types/의 .md(YAML frontmatter)를 읽어
분석용 산출물(build/corpus.jsonl, build/corpus.sqlite)로 컴파일한다.

.md 파일이 진실의 원천이고, build/는 언제든 재생성 가능한 파생물이다.
(그래서 build/는 .gitignore 대상이며 release에만 첨부한다.)

설치: pip install pyyaml
사용: python scripts/build.py
"""
from __future__ import annotations
import json
import sqlite3
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
WITNESS_DIR = ROOT / "witnesses"
TYPE_DIR = ROOT / "types"
BUILD_DIR = ROOT / "build"


def parse_frontmatter(path: Path) -> dict:
    """--- 로 감싼 YAML frontmatter를 dict로 반환. 본문은 무시."""
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return {}
    _, fm, *_ = raw.split("---", 2)
    data = yaml.safe_load(fm) or {}
    data["_file"] = str(path.relative_to(ROOT))
    return data


def collect(directory: Path) -> list[dict]:
    return [parse_frontmatter(p) for p in sorted(directory.rglob("*.md"))]


def build() -> None:
    BUILD_DIR.mkdir(exist_ok=True)
    witnesses = collect(WITNESS_DIR)
    types = collect(TYPE_DIR)

    # 1) JSONL (이본 한 줄 = 한 레코드)
    jsonl_path = BUILD_DIR / "corpus.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as f:
        for w in witnesses:
            f.write(json.dumps(w, ensure_ascii=False) + "\n")

    # 2) SQLite (쿼리용 평면 테이블)
    db_path = BUILD_DIR / "corpus.sqlite"
    db_path.unlink(missing_ok=True)
    con = sqlite3.connect(db_path)
    con.execute("""
        CREATE TABLE witness (
            id TEXT PRIMARY KEY, type_id TEXT, source TEXT, juan TEXT,
            editor TEXT, register TEXT, folk INTEGER, file TEXT
        )""")
    con.execute("CREATE TABLE operation (witness_id TEXT, op TEXT)")
    con.execute("CREATE TABLE type (id TEXT PRIMARY KEY, label TEXT, file TEXT)")

    for w in witnesses:
        con.execute(
            "INSERT INTO witness VALUES (?,?,?,?,?,?,?,?)",
            (w.get("id"), w.get("type_id"), w.get("source"), w.get("juan"),
             w.get("editor"), w.get("register"),
             1 if w.get("folk") else 0, w.get("_file")),
        )
        for op in (w.get("operations") or []):
            con.execute("INSERT INTO operation VALUES (?,?)", (w.get("id"), op))
    for t in types:
        con.execute("INSERT INTO type VALUES (?,?,?)",
                    (t.get("id"), t.get("label"), t.get("_file")))
    con.commit()
    con.close()

    print(f"이본 {len(witnesses)}건, 유형 {len(types)}건 → {BUILD_DIR}/")


if __name__ == "__main__":
    build()
