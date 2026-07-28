"""Tests for explicit GitHub publishing."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from python_project_foundry import publishing


def _write_generated_project(project: Path) -> None:
    project.mkdir()
    (project / "pyproject.toml").write_text(
        """
[project]
name = "orbit-tools"
description = "Reliable orbital calculations."

[project.urls]
Source = "https://github.com/space-labs/orbit-tools"
Documentation = "https://space-labs.github.io/orbit-tools/"
""".strip()
    )


def test_publish_creates_repository_and_configures_pages(monkeypatch, tmp_path: Path) -> None:
    project = tmp_path / "orbit-tools"
    _write_generated_project(project)
    calls: list[list[str]] = []

    outputs = {
        ("git", "rev-parse", "--show-toplevel"): str(project),
        ("git", "status", "--porcelain"): "",
        ("git", "branch", "--show-current"): "main",
        ("git", "remote"): "",
    }

    def run_command(
        command: list[str],
        *,
        cwd: Path,
        capture_output: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        assert cwd == project
        calls.append(command)
        return subprocess.CompletedProcess(
            command,
            0,
            stdout=outputs.get(tuple(command), ""),
            stderr="",
        )

    monkeypatch.setattr(publishing.shutil, "which", lambda command: f"/usr/bin/{command}")
    monkeypatch.setattr(publishing, "_run_command", run_command)

    publishing.publish_project(project, visibility="private")

    assert calls[-2] == [
        "gh",
        "repo",
        "create",
        "space-labs/orbit-tools",
        "--private",
        "--source=.",
        "--remote=origin",
        "--push",
        "--description=Reliable orbital calculations.",
        "--homepage=https://space-labs.github.io/orbit-tools/",
        "--disable-wiki",
    ]
    assert calls[-1] == [
        "gh",
        "api",
        "--method",
        "POST",
        "repos/space-labs/orbit-tools/pages",
        "--raw-field",
        "build_type=workflow",
        "--silent",
    ]


def test_publish_rejects_dirty_working_tree_before_github_calls(monkeypatch, tmp_path: Path) -> None:
    project = tmp_path / "orbit-tools"
    _write_generated_project(project)
    calls: list[list[str]] = []

    def run_command(
        command: list[str],
        *,
        cwd: Path,
        capture_output: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        del cwd, capture_output
        calls.append(command)
        stdout = str(project) if command[1:] == ["rev-parse", "--show-toplevel"] else " M README.md"
        return subprocess.CompletedProcess(command, 0, stdout=stdout, stderr="")

    monkeypatch.setattr(publishing.shutil, "which", lambda command: f"/usr/bin/{command}")
    monkeypatch.setattr(publishing, "_run_command", run_command)

    with pytest.raises(publishing.PublishError, match="uncommitted changes"):
        publishing.publish_project(project, visibility="public")

    assert all(command[0] != "gh" for command in calls)


def test_publish_dry_run_prints_commands_without_requiring_gh(monkeypatch, tmp_path: Path, capsys) -> None:
    project = tmp_path / "orbit-tools"
    _write_generated_project(project)

    outputs = {
        ("git", "rev-parse", "--show-toplevel"): str(project),
        ("git", "status", "--porcelain"): "",
        ("git", "branch", "--show-current"): "main",
        ("git", "remote"): "",
    }

    def run_command(
        command: list[str],
        *,
        cwd: Path,
        capture_output: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        del cwd, capture_output
        return subprocess.CompletedProcess(command, 0, stdout=outputs[tuple(command)], stderr="")

    monkeypatch.setattr(publishing.shutil, "which", lambda command: "/usr/bin/git" if command == "git" else None)
    monkeypatch.setattr(publishing, "_run_command", run_command)

    publishing.publish_project(project, visibility="internal", dry_run=True)

    output = capsys.readouterr().out
    assert "gh repo create space-labs/orbit-tools --internal" in output
    assert "build_type=workflow" in output
