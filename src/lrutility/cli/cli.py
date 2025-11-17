from pathlib import Path
from typing import Annotated

import typer
from typer import Typer

from lrutility.cli.delete_rate_1 import delete_rate_1
from lrutility.cli.zip_chunker import zip_chunker

app = Typer(
    name="lru",
    help="LrUtility: A collection of utilities for Adobe Lightroom",
)


@app.command("delete-rate-1")
def delete_rate_1_runner(
    directory: Annotated[
        Path, typer.Argument(help="Target directory to search for XMP files")
    ],
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            "-d",
            help="Perform a dry run without actually deleting files",
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Enable verbose logging (DEBUG level)",
        ),
    ] = False,
) -> None:
    delete_rate_1(directory, dry_run, verbose)


@app.command(name="zip-chunker")
def zip_chunker_runner(
    directory: Annotated[
        Path, typer.Argument(help="Target directory to search for files")
    ],
    size_chunk: Annotated[
        int,
        typer.Option(
            "--size-chunk",
            "-s",
            help="Size of each chunk in bytes",
        ),
    ] = 20 * 1024**3,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Enable verbose logging (DEBUG level)",
        ),
    ] = False,
) -> None:
    zip_chunker(directory, size_chunk, verbose)
