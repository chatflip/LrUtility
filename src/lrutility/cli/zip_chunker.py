import zipfile
from pathlib import Path

from loguru import logger
from tqdm import tqdm

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


def zip_chunker(directory: Path, size_chunk: int, verbose: bool) -> None:
    configure_loguru(verbose=verbose)

    if not directory.is_dir():
        logger.error(f"{directory} is not a valid directory")
        return

    files = [f for f in directory.iterdir() if f.is_file()]
    files.sort()
    if not files:
        logger.error(f"No files found in {directory}")
        return

    groups: list[list[Path]] = group_files(files, size_chunk)

    for i, group in enumerate(groups, start=1):
        archive_path = directory.parent / f"{directory.name}_{i}.zip"
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for file_path in tqdm(group, desc=f"Adding files to {archive_path}"):
                arcname = str(file_path.relative_to(directory))
                zf.write(str(file_path), arcname=arcname)
        logger.info(f"Created {archive_path}")
