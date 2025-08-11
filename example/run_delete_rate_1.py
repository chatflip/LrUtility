import argparse
from pathlib import Path

from lrutility.delete_rate_1 import delete_rate_1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--target",
        type=Path,
        # required=True,
        default=Path("tests/assets"),
    )
    parser.add_argument(
        "-d",
        "--dry_run",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
    )
    args = parser.parse_args()
    delete_rate_1(args)
