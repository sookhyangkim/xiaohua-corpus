"""
점검용 통계: 선집별 편집 조작 빈도, 유형 커버리지 등.
build.py를 먼저 실행해 build/corpus.sqlite를 만든 뒤 사용한다.

사용: python scripts/stats.py
"""
from __future__ import annotations
import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "build" / "corpus.sqlite"


def main() -> None:
    if not DB.exists():
        raise SystemExit("build/corpus.sqlite 없음. 먼저 `python scripts/build.py` 실행.")
    con = sqlite3.connect(DB)

    print("== 선집별 이본 수 ==")
    for src, n in con.execute(
            "SELECT source, COUNT(*) FROM witness GROUP BY source ORDER BY 2 DESC"):
        print(f"  {src:24} {n}")

    print("\n== 선집 × 편집 조작 빈도 ==")
    rows = con.execute("""
        SELECT w.source, o.op, COUNT(*) AS n
        FROM operation o JOIN witness w ON w.id = o.witness_id
        GROUP BY w.source, o.op ORDER BY w.source, n DESC
    """)
    for src, op, n in rows:
        print(f"  {src:24} {op:16} {n}")

    print("\n== 유형 커버리지 (type_id별 이본 수) ==")
    for tid, n in con.execute("""
            SELECT COALESCE(type_id,'(미연결)'), COUNT(*)
            FROM witness GROUP BY type_id ORDER BY 2 DESC"""):
        print(f"  {tid:12} {n}")

    con.close()


if __name__ == "__main__":
    main()
