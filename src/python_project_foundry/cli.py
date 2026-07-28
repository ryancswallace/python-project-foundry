"""Command-line interface for Python Project Foundry."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

import copier


def _template_path() -> Path:
    """Return the path to the Copier template bundled with this package."""
    bundled_template = Path(__file__).parent / "_template"
    if bundled_template.is_dir():
        return bundled_template

    # Editable installs and direct source-tree test runs use the repository copy.
    source_checkout = Path(__file__).parents[2]
    if (source_checkout / "copier.yaml").is_file():
        return source_checkout

    msg = "The Python Project Foundry template could not be found."
    raise FileNotFoundError(msg)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ppf",
        description="Scaffold Python projects with Python Project Foundry.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    template_parser = subparsers.add_parser(
        "template",
        help="Create a project from the Python Project Foundry template.",
    )
    template_parser.add_argument("destination", type=Path, help="Directory in which to create the project.")
    template_parser.add_argument(
        "--defaults",
        action="store_true",
        help="Use default answers instead of prompting.",
    )
    template_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite files that already exist.",
    )
    template_parser.add_argument(
        "--pretend",
        action="store_true",
        help="Show what Copier would do without writing files.",
    )
    template_parser.add_argument(
        "--skip-tasks",
        action="store_true",
        help="Render the project without running template tasks.",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the Python Project Foundry command-line interface."""
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments and arguments[0] not in {"template", "-h", "--help"}:
        arguments.insert(0, "template")

    args = _build_parser().parse_args(arguments)

    if args.command == "template":
        # Copier exports run_copy dynamically via __getattr__; BasedPyright cannot resolve it.
        copier.run_copy(  # pyright: ignore[reportAttributeAccessIssue]
            src_path=str(_template_path()),
            dst_path=args.destination,
            defaults=args.defaults,
            overwrite=args.overwrite,
            pretend=args.pretend,
            skip_tasks=args.skip_tasks,
            unsafe=True,  # Run tasks
        )

    return 0
