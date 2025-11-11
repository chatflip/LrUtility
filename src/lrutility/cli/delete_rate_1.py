import argparse
from pathlib import Path

from loguru import logger

from lrutility.utils.logger import configure_loguru
from lrutility.xmp.XMPParser import XMPParser


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


def delete_rate_1(args: argparse.Namespace) -> None:
    configure_loguru(args.verbose)
    if args.directory is None:
        logger.error("Target Directory is not specified")
        return

    logger.info(f"Target Directory: {args.directory}")
    if not args.directory.exists():
        logger.error(f"Target Directory Does Not Exist: {args.directory}")
        return

    parser = XMPParser()

    meta_paths = args.directory.glob("**/*.xmp")
    meta_paths = sorted(meta_paths)
    for meta_path in meta_paths:
        metadata = parser.parse(meta_path)
        if metadata.xmp_info.rating is None:
            logger.debug(f"No Rating in xmp: {meta_path}")
            continue
        rating = metadata.xmp_info.rating
        raw_filename = metadata.camera_raw_settings.raw_file_name
        raw_path = args.directory / raw_filename
        if rating == 1:
            delete_image_and_xmp(raw_path, meta_path, args.dry_run)


def delete_rate_1_cli() -> None:
    """CLI entry point: Delete image files and XMP files with rating 1."""
    parser = argparse.ArgumentParser(
        description="Delete image files and XMP files with rating 1"
    )
    parser.add_argument(
        "directory",
        type=Path,
        nargs="?",
        help="Target directory to search for XMP files",
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
