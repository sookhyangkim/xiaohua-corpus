"""
간번체 정규화 유틸리티 (OpenCC 기반).

코퍼스의 정본 정규화 로직. 논문 저장소에서 동일 결과가 필요하면
이 파일을 vendoring 하거나, 코퍼스를 버전 고정해 import 한다.

설치: pip install opencc-python-reimplemented
사용:
    python scripts/normalize.py "汉字简体测试"      # 기본 s2t (간→번)
    python scripts/normalize.py --mode t2s "漢字"   # 번→간
"""
from __future__ import annotations
import argparse

try:
    from opencc import OpenCC
except ImportError:  # 친절한 안내
    OpenCC = None


def normalize(text: str, mode: str = "s2t") -> str:
    """text를 지정 모드로 변환. mode: s2t(간→번, 기본) / t2s(번→간)."""
    if OpenCC is None:
        raise RuntimeError(
            "opencc 미설치. `pip install opencc-python-reimplemented` 후 사용."
        )
    return OpenCC(mode).convert(text)


def main() -> None:
    p = argparse.ArgumentParser(description="OpenCC 간번체 정규화")
    p.add_argument("text", help="변환할 문자열")
    p.add_argument("--mode", default="s2t", choices=["s2t", "t2s"],
                   help="s2t: 간→번(기본), t2s: 번→간")
    args = p.parse_args()
    print(normalize(args.text, args.mode))


if __name__ == "__main__":
    main()
