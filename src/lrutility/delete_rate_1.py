import argparse
from pathlib import Path

from loguru import logger

from lrutility.logger import configure_loguru
from lrutility.utils import delete_image_and_xmp
from lrutility.XMPParser import XMPParser


def delete_rate_1(args: argparse.Namespace) -> None:
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


def delete_rate_1_cli() -> None:
    """CLIエントリーポイント: レーティング1の画像ファイルとXMPファイルを削除。"""
    parser = argparse.ArgumentParser(
        description="Delete image files and XMP files with rating 1"
    )
    parser.add_argument(
        "-t",
        "--target",
        type=Path,
        required=True,
        help="Target directory to search for XMP files (default: tests/assets)",
    )
    parser.add_argument(
        "-d",
        "--dry_run",
        action="store_true",
        help="Perform a dry run without actually deleting files",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging (DEBUG level)",
    )

    args = parser.parse_args()
    delete_rate_1(args)
