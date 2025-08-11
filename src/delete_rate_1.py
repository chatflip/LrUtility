import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from loguru import logger

from utils import configure_loguru


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


def delete_image_and_xmp(raw_path: Path, xmp_path: Path, dry_run: bool) -> None:
    if dry_run:
        logger.debug(f"[DRY RUN] Deleted: {raw_path}")
        logger.debug(f"[DRY RUN] Deleted: {xmp_path}")
    else:
        raw_path.unlink()
        logger.info(f"Deleted: {raw_path}")
        xmp_path.unlink()
        logger.info(f"Deleted: {xmp_path}")


def main(args: argparse.Namespace) -> None:
    configure_loguru(args.verbose)

    logger.info(f"Target Directory: {args.target.resolve()}")
    if not args.target.exists():
        logger.error(f"Target Directory Does Not Exist: {args.target.resolve()}")
        return

    meta_paths = args.target.glob("**/*.xmp")
    for meta_path in meta_paths:
        meta_dict = load_xmp(meta_path)
        if "Rating" not in meta_dict:
            logger.debug(f"No Rating in xmp: {meta_path}")
            continue
        rating = meta_dict["Rating"]
        raw_filename = meta_dict["RawFileName"]
        raw_path = args.target / raw_filename
        if rating == "1":
            delete_image_and_xmp(raw_path, meta_path, args.dry_run)


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
    main(args)
