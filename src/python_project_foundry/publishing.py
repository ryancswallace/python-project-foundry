"""Explicit GitHub publishing for generated projects."""

from __future__ import annotations

import shlex
import shutil
import subprocess
import tomllib
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


class PublishError(RuntimeError):
    """Raised when a project cannot be safely published."""


@dataclass(frozen=True)
class ProjectPublishingConfig:
    """Metadata required to publish a generated project."""

    root: Path
    repository: str
    description: str
    documentation_url: str


def _run_command(
    command: list[str],
    *,
    cwd: Path,
    capture_output: bool = False,
) -> subprocess.CompletedProcess[str]:
    """Run a publishing command and translate failures into user-facing errors."""
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            check=True,
            capture_output=capture_output,
            text=True,
        )
    except FileNotFoundError as error:
        raise PublishError(f"Required command not found: {command[0]}") from error
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or error.stdout or "").strip()
        suffix = f": {detail}" if detail else ""
        raise PublishError(f"Command failed: {shlex.join(command)}{suffix}") from error


def _command_output(command: list[str], *, cwd: Path) -> str:
    """Run a command and return stripped stdout."""
    return _run_command(command, cwd=cwd, capture_output=True).stdout.strip()


def _repository_from_url(source_url: str) -> str:
    """Convert a canonical GitHub source URL to OWNER/REPOSITORY."""
    parsed = urlparse(source_url)
    path_parts = parsed.path.strip("/").removesuffix(".git").split("/")
    if parsed.scheme != "https" or parsed.netloc.lower() != "github.com" or len(path_parts) != 2:
        raise PublishError("project.urls.Source must be an HTTPS github.com OWNER/REPOSITORY URL.")
    return "/".join(path_parts)


def load_project_publishing_config(project_path: Path) -> ProjectPublishingConfig:
    """Load publishing metadata from a generated project's pyproject.toml."""
    root = project_path.expanduser().resolve()
    pyproject_path = root / "pyproject.toml"
    if not pyproject_path.is_file():
        raise PublishError(f"Generated project metadata not found: {pyproject_path}")

    try:
        pyproject = tomllib.loads(pyproject_path.read_text())
        project = pyproject["project"]
        urls = project["urls"]
        description = str(project["description"])
        source_url = str(urls["Source"])
        documentation_url = str(urls["Documentation"])
    except (KeyError, TypeError, tomllib.TOMLDecodeError) as error:
        raise PublishError(f"Invalid generated project metadata in {pyproject_path}") from error

    return ProjectPublishingConfig(
        root=root,
        repository=_repository_from_url(source_url),
        description=description,
        documentation_url=documentation_url,
    )


def _preflight(config: ProjectPublishingConfig, *, remote: str, require_gh: bool) -> None:
    """Ensure publishing can proceed without overwriting remote state."""
    if shutil.which("git") is None:
        raise PublishError("Git is required to publish a project.")
    if require_gh and shutil.which("gh") is None:
        raise PublishError("GitHub CLI is required. Install it from https://cli.github.com/.")

    repository_root = Path(_command_output(["git", "rev-parse", "--show-toplevel"], cwd=config.root)).resolve()
    if repository_root != config.root:
        raise PublishError(f"Project path is not the Git repository root: {config.root}")

    if status := _command_output(["git", "status", "--porcelain"], cwd=config.root):
        raise PublishError(f"The project has uncommitted changes. Commit or discard them before publishing.\n{status}")

    branch = _command_output(["git", "branch", "--show-current"], cwd=config.root)
    if branch != "main":
        raise PublishError(f"Publishing requires the generated main branch; current branch is {branch!r}.")

    remotes = _command_output(["git", "remote"], cwd=config.root).splitlines()
    if remote in remotes:
        raise PublishError(f"Git remote {remote!r} already exists; refusing to replace it.")

    if require_gh:
        _run_command(
            ["gh", "auth", "status", "--active", "--hostname", "github.com"],
            cwd=config.root,
            capture_output=True,
        )


def _publish_commands(
    config: ProjectPublishingConfig,
    *,
    visibility: str,
    remote: str,
    configure_pages: bool,
) -> list[list[str]]:
    """Build the external commands used to publish the project."""
    create_command = [
        "gh",
        "repo",
        "create",
        config.repository,
        f"--{visibility}",
        "--source=.",
        f"--remote={remote}",
        "--push",
        f"--description={config.description}",
        f"--homepage={config.documentation_url}",
        "--disable-wiki",
    ]
    commands = [create_command]
    if configure_pages:
        commands.append(
            [
                "gh",
                "api",
                "--method",
                "POST",
                f"repos/{config.repository}/pages",
                "--raw-field",
                "build_type=workflow",
                "--silent",
            ]
        )
    return commands


def publish_project(
    project_path: Path,
    *,
    visibility: str,
    remote: str = "origin",
    configure_pages: bool = True,
    dry_run: bool = False,
) -> None:
    """Create and push a GitHub repository, then optionally enable Pages."""
    config = load_project_publishing_config(project_path)
    commands = _publish_commands(
        config,
        visibility=visibility,
        remote=remote,
        configure_pages=configure_pages,
    )
    _preflight(config, remote=remote, require_gh=not dry_run)

    if dry_run:
        print(f"Would publish {config.root} to {config.repository}:")
        for command in commands:
            print(f"  {shlex.join(command)}")
        return

    _run_command(commands[0], cwd=config.root)
    if configure_pages:
        try:
            _run_command(commands[1], cwd=config.root)
        except PublishError as error:
            repository_url = f"https://github.com/{config.repository}"
            raise PublishError(
                f"Repository created and pushed to {repository_url}, but GitHub Pages "
                f"configuration failed. Retry the Pages API command shown by --dry-run.\n{error}"
            ) from error

    print("Published successfully.")
    print(f"  repository: https://github.com/{config.repository}")
    if configure_pages:
        print(f"  documentation: {config.documentation_url}")
        print("  GitHub Actions will build and deploy the documentation from main.")
    else:
        print("  documentation: Pages configuration skipped")
