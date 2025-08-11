from pathlib import Path

from loguru import logger


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
