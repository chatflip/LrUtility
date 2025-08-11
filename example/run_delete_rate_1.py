import argparse
from pathlib import Path

from loguru import logger

from lrutility.logger import configure_loguru
from lrutility.XMPParser import XMPParser


def delete_image_and_xmp(raw_path: Path, xmp_path: Path, dry_run: bool) -> None:
    message_template = "Deleted: {path}"
    if dry_run:
        logger.debug(f"[DRY RUN]: {message_template.format(path=raw_path)}")
        logger.debug(f"[DRY RUN]: {message_template.format(path=xmp_path)}")
    else:
        raw_path.unlink()
        logger.info(message_template.format(path=raw_path))
        xmp_path.unlink()
        logger.info(message_template.format(path=xmp_path))


def main(args: argparse.Namespace) -> None:
    configure_loguru(args.verbose)

    logger.info(f"Target Directory: {args.target.resolve()}")
    if not args.target.exists():
        logger.error(f"Target Directory Does Not Exist: {args.target.resolve()}")
        return

    parser = XMPParser()  # XMPParserインスタンスを作成

    meta_paths = args.target.glob("**/*.xmp")
    for meta_path in meta_paths:
        metadata = parser.parse(meta_path)  # parseメソッドを使用
        if metadata.xmp_info.rating is None:
            logger.debug(f"No Rating in xmp: {meta_path}")
            continue
        rating = metadata.xmp_info.rating
        raw_filename = metadata.camera_raw_settings.raw_file_name
        raw_path = args.target / raw_filename
        if rating == 1:
            delete_image_and_xmp(raw_path, meta_path, args.dry_run)


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
    main(args)
