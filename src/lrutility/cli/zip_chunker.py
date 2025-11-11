import argparse
import zipfile
from pathlib import Path

from loguru import logger

from lrutility.utils.logger import configure_loguru


def group_files(files: list[Path], max_group_size: int) -> list[list[Path]]:
    """Group files into chunks with size <= max_group_size.

    Args:
        files (list[Path]): List of file paths to be grouped.
        max_group_size (int): Maximum size of each chunk in bytes.
    """
    groups = []
    current_group = []  # type: ignore[var-annotated]
    current_group_size = 0
    for file in files:
        try:
            file_size = file.stat().st_size
        except OSError:
            logger.error(f"Failed to get file size: {file}")
            continue

        if current_group and current_group_size + file_size > max_group_size:
            groups.append(current_group)
            current_group = []
            current_group_size = 0
        current_group.append(file)
        current_group_size += file_size
    if current_group:
        groups.append(current_group)
    return groups


def zip_chunker(args: argparse.Namespace) -> None:
    configure_loguru(args.verbose)
    if not args.directory.is_dir():
        logger.error(f"{args.directory} is not a valid directory")
        return

    files = [f for f in args.directory.iterdir() if f.is_file()]
    files.sort()
    if not files:
        logger.error(f"No files found in {args.directory}")
        return

    groups: list[list[Path]] = group_files(files, args.size_chunk)

    for i, group in enumerate(groups, start=1):
        archive_path = args.directory.parent / f"{args.directory.name}_{i}.zip"
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for file_path in group:
                arcname = str(file_path.relative_to(args.directory))
                zf.write(str(file_path), arcname=arcname)
        logger.info(f"Created {archive_path}")


def zip_chunker_cli() -> None:
    """CLI entry point: Group files into chunks and zip them."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory",
        type=Path,
        nargs="?",
        help="Target directory to search for XMP files",
    )
    parser.add_argument(
        "-s",
        "--size_chunk",
        type=int,
        help="Size of each chunk in bytes",
        default=20 * 1024**3,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose logging (DEBUG level)",
    )
    args = parser.parse_args()
    zip_chunker(args)
