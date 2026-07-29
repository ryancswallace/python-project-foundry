"""Command-line interface for Python Project Foundry."""

from __future__ import annotations

import argparse
import shutil
import sys
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from importlib.metadata import version
from pathlib import Path
from tempfile import TemporaryDirectory

import copier
from copier.errors import CopierError  # pyright: ignore[reportMissingImports]

from python_project_foundry.publishing import PublishError, publish_project

ANSWERS_FILE = Path(".python-project-foundry.answers.yaml")
PACKAGE_NAME = "python-project-foundry"
TEMPLATE_UPDATE_SOURCE = "https://github.com/ryancswallace/python-project-foundry.git"


def _template_tracking_data() -> dict[str, str]:
    """Return metadata that lets generated repositories use tagged updates."""
    return {
        "_ppf_template_source": TEMPLATE_UPDATE_SOURCE,
        "_ppf_template_version": version(PACKAGE_NAME),
    }


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


@contextmanager
def _template_source() -> Iterator[Path]:
    """Yield a Copier source containing the current template files.

    Copier treats any local Git repository as a versioned template and renders
    its committed revision. For editable installs, snapshot the template inputs
    without ``.git`` so uncommitted questionnaire and template changes are
    available during local development.
    """
    source = _template_path()
    if not (source / ".git").exists():
        yield source
        return

    with TemporaryDirectory(prefix="python-project-foundry-") as temporary_directory:
        snapshot = Path(temporary_directory)
        shutil.copy2(source / "copier.yaml", snapshot)
        shutil.copytree(source / "copier", snapshot / "copier")
        shutil.copytree(source / "template", snapshot / "template")
        yield snapshot


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ppf",
        description="Scaffold Python package/library repositories with Python Project Foundry.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {version(PACKAGE_NAME)}",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    template_parser = subparsers.add_parser(
        "template",
        help="Create a Python package/library repository from the template.",
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

    update_parser = subparsers.add_parser(
        "update",
        help="Update a generated repository to this Foundry version.",
    )
    update_parser.add_argument(
        "project",
        type=Path,
        nargs="?",
        default=Path("."),
        help="Generated project directory (default: current directory).",
    )
    update_parser.add_argument(
        "--defaults",
        action="store_true",
        help="Use defaults for newly introduced questions without prompting.",
    )
    update_parser.add_argument(
        "--pretend",
        action="store_true",
        help="Preview the update without changing the repository.",
    )
    update_parser.add_argument(
        "--skip-tasks",
        action="store_true",
        help="Apply files and migrations without running regular template tasks.",
    )
    update_parser.add_argument(
        "--conflict",
        choices=("inline", "rej"),
        default="inline",
        help="Write conflicts inline or to .rej files (default: inline).",
    )

    publish_parser = subparsers.add_parser(
        "publish",
        help="Explicitly create and push a generated project to GitHub.",
    )
    publish_parser.add_argument(
        "project",
        type=Path,
        nargs="?",
        default=Path("."),
        help="Generated project directory (default: current directory).",
    )
    publish_parser.add_argument(
        "--visibility",
        required=True,
        choices=("private", "public", "internal"),
        help="GitHub repository visibility; must be selected explicitly.",
    )
    publish_parser.add_argument(
        "--remote",
        default="origin",
        help="Git remote name to create (default: origin).",
    )
    publish_parser.add_argument(
        "--skip-pages",
        action="store_true",
        help="Create and push the repository without enabling GitHub Pages.",
    )
    publish_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run local preflight checks and print external commands without executing them.",
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the Python Project Foundry command-line interface."""
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments and arguments[0] not in {"template", "update", "publish", "-h", "--help", "--version"}:
        arguments.insert(0, "template")

    args = _build_parser().parse_args(arguments)

    if args.command == "template":
        tracking_data = _template_tracking_data()
        with _template_source() as template_source:
            # Copier exports run_copy dynamically via __getattr__; BasedPyright cannot resolve it.
            copier.run_copy(  # pyright: ignore[reportAttributeAccessIssue]
                src_path=str(template_source),
                dst_path=args.destination,
                data=tracking_data,
                defaults=args.defaults,
                overwrite=args.overwrite,
                pretend=args.pretend,
                skip_tasks=args.skip_tasks,
                unsafe=True,  # Run tasks
            )

    if args.command == "update":
        tracking_data = _template_tracking_data()
        try:
            # Copier exports run_update dynamically via __getattr__; BasedPyright cannot resolve it.
            copier.run_update(  # pyright: ignore[reportAttributeAccessIssue]
                dst_path=args.project,
                data=tracking_data,
                answers_file=ANSWERS_FILE,
                vcs_ref=f"v{tracking_data['_ppf_template_version']}",
                defaults=args.defaults,
                overwrite=True,
                pretend=args.pretend,
                conflict=args.conflict,
                unsafe=True,  # Run trusted template migrations and tasks
                skip_answered=True,
                skip_tasks=args.skip_tasks,
            )
        except CopierError as error:
            print(f"error: {error}", file=sys.stderr)
            return 2

    if args.command == "publish":
        try:
            publish_project(
                args.project,
                visibility=args.visibility,
                remote=args.remote,
                configure_pages=not args.skip_pages,
                dry_run=args.dry_run,
            )
        except PublishError as error:
            print(f"error: {error}", file=sys.stderr)
            return 2

    return 0
