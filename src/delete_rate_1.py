import argparse
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from loguru import logger

from utils import RAW_EXT, configure_loguru


def load_xmp(xmp_path: Path) -> dict[str, str]:
    tree = ET.parse(xmp_path)
    root = tree.getroot()
    pattern = r"\{.*?\}(.*)"
    attr_dict = {}
    for elem in root.iter():
        for attr in elem.keys():
            match = re.search(pattern, attr)
            if not match:
                continue
            attr_name = match.group(1)
            attr_value = elem.get(attr)
            attr_dict[attr_name] = attr_value
    return attr_dict  # type: ignore[return-value]


def delete_image_and_xmp(raw_path: str, xmp_path: str) -> None:
    os.remove(raw_path)
    os.remove(xmp_path)


def main(args: argparse.Namespace) -> None:
    configure_loguru(args.verbose)

    logger.info(f"target directory: {args.target.resolve()}")
    filenames = args.target.glob("**/*")
    for filename in filenames:
        if filename.suffix.lower() not in RAW_EXT:
            continue
        xmp_path = filename.with_suffix(".xmp")
        if not xmp_path.exists():
            continue
        meta_dict = load_xmp(xmp_path)
        if "Rating" not in meta_dict:
            continue
        rating = meta_dict["Rating"]
        if rating == "1":
            delete_image_and_xmp(filename, xmp_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--target",
        type=Path,
        # required=True,
        default=Path("~/Desktop/raw_temp"),
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
    )
    args = parser.parse_args()
    main(args)
