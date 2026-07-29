"""Tests for the Python Project Foundry command-line interface."""

import shutil
import subprocess
from pathlib import Path

import pytest
from copier._template import Template
from copier.errors import UserMessageError

from python_project_foundry import cli


def _git(repository: Path, *arguments: str) -> None:
    subprocess.run(
        ["git", *arguments],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )


def test_template_invokes_copier(monkeypatch, tmp_path: Path) -> None:
    destination = tmp_path / "new-project"
    calls: list[dict[str, object]] = []
    source_observations: list[dict[str, object]] = []

    def observe_copy(**kwargs: object) -> None:
        source = Path(str(kwargs["src_path"]))
        calls.append(kwargs)
        source_observations.append(
            {
                "exists_during_copy": source.is_dir(),
                "is_git_repository": (source / ".git").exists(),
                "has_config": (source / "copier.yaml").is_file(),
                "has_template": (source / "template").is_dir(),
            }
        )

    monkeypatch.setattr(cli.copier, "run_copy", observe_copy)
    monkeypatch.setattr(cli, "version", lambda _package: "9.8.7")

    result = cli.main(
        [
            "template",
            str(destination),
            "--defaults",
            "--overwrite",
            "--pretend",
            "--skip-tasks",
        ]
    )

    assert result == 0
    assert len(calls) == 1
    copier_call = calls[0].copy()
    assert isinstance(copier_call.pop("src_path"), str)
    assert copier_call == {
        "dst_path": destination,
        "data": {
            "_ppf_template_source": cli.TEMPLATE_UPDATE_SOURCE,
            "_ppf_template_version": "9.8.7",
        },
        "defaults": True,
        "overwrite": True,
        "pretend": True,
        "skip_tasks": True,
        "unsafe": True,
    }
    assert source_observations == [
        {
            "exists_during_copy": True,
            "is_git_repository": False,
            "has_config": True,
            "has_template": True,
        }
    ]


def test_version_flag_prints_installed_package_version(monkeypatch, capsys) -> None:
    monkeypatch.setattr(cli, "version", lambda _package: "9.8.7")

    with pytest.raises(SystemExit, match="0"):
        cli.main(["--version"])

    assert capsys.readouterr().out == "ppf 9.8.7\n"


def test_update_invokes_copier_with_recorded_template_version(monkeypatch, tmp_path: Path) -> None:
    project = tmp_path / "generated-project"
    calls: list[dict[str, object]] = []
    monkeypatch.setattr(cli.copier, "run_update", lambda **kwargs: calls.append(kwargs))
    monkeypatch.setattr(cli, "version", lambda _package: "9.8.7")

    result = cli.main(
        [
            "update",
            str(project),
            "--defaults",
            "--pretend",
            "--skip-tasks",
            "--conflict",
            "rej",
        ]
    )

    assert result == 0
    assert calls == [
        {
            "dst_path": project,
            "data": {
                "_ppf_template_source": cli.TEMPLATE_UPDATE_SOURCE,
                "_ppf_template_version": "9.8.7",
            },
            "answers_file": cli.ANSWERS_FILE,
            "vcs_ref": "v9.8.7",
            "defaults": True,
            "overwrite": True,
            "pretend": True,
            "conflict": "rej",
            "unsafe": True,
            "skip_answered": True,
            "skip_tasks": True,
        }
    ]


def test_update_reports_copier_errors(monkeypatch, capsys) -> None:
    def fail_update(**_kwargs: object) -> None:
        raise UserMessageError("Destination repository is dirty.")

    monkeypatch.setattr(cli.copier, "run_update", fail_update)

    result = cli.main(["update"])

    assert result == 2
    assert capsys.readouterr().err == "error: Destination repository is dirty.\n"


def test_update_merges_a_new_tag_into_a_generated_repository(monkeypatch, tmp_path: Path) -> None:
    template_repository = tmp_path / "template-repository"
    template_repository.mkdir()
    shutil.copy2(cli._template_path() / "copier.yaml", template_repository)
    shutil.copytree(cli._template_path() / "copier", template_repository / "copier")
    shutil.copytree(cli._template_path() / "template", template_repository / "template")
    _git(template_repository, "init", "-b", "main")
    _git(template_repository, "config", "user.name", "Template Test")
    _git(template_repository, "config", "user.email", "template@example.com")
    _git(template_repository, "add", ".")
    _git(template_repository, "commit", "-m", "Initial template")
    _git(template_repository, "tag", "v1.0.0")

    monkeypatch.setattr(cli, "_template_path", lambda: template_repository)
    monkeypatch.setattr(cli, "TEMPLATE_UPDATE_SOURCE", str(template_repository))
    monkeypatch.setattr(cli, "version", lambda _package: "1.0.0")

    project = tmp_path / "generated-project"
    assert cli.main(["template", str(project), "--defaults", "--skip-tasks"]) == 0
    _git(project, "init", "-b", "main")
    _git(project, "config", "user.name", "Project Test")
    _git(project, "config", "user.email", "project@example.com")
    _git(project, "add", ".")
    _git(project, "commit", "-m", "Initial project")

    marker = template_repository / "template/UPDATED.md"
    marker.write_text("Updated by a tagged template release.\n")
    _git(template_repository, "add", ".")
    _git(template_repository, "commit", "-m", "Add update marker")
    _git(template_repository, "tag", "v1.1.0")
    monkeypatch.setattr(cli, "version", lambda _package: "1.1.0")

    assert cli.main(["update", str(project), "--defaults", "--skip-tasks"]) == 0
    assert (project / "UPDATED.md").read_text() == "Updated by a tagged template release.\n"
    assert "_commit: v1.1.0" in (project / cli.ANSWERS_FILE).read_text()


def test_template_source_is_available() -> None:
    assert (cli._template_path() / "copier.yaml").is_file()
    assert (cli._template_path() / "template").is_dir()


def test_editable_template_source_uses_working_tree_questions() -> None:
    with cli._template_source() as source:
        template = Template(url=str(source))
        questions = template.questions_data
        task_commands = [task.cmd for task in template.tasks]

    assert {
        "project_name",
        "project_slug",
        "package_name",
        "python_min_version",
        "repository_owner",
        "documentation_url",
        "author_email",
    } <= questions.keys()
    assert "make setup" not in task_commands
    assert "make hooks-install" in task_commands
    assert "make install npm-install" in task_commands


def test_destination_without_subcommand_defaults_to_template(monkeypatch, tmp_path: Path) -> None:
    destination = tmp_path / "new-project"
    calls: list[dict[str, object]] = []

    monkeypatch.setattr(cli.copier, "run_copy", lambda **kwargs: calls.append(kwargs))

    result = cli.main([str(destination), "--skip-tasks"])

    assert result == 0
    assert calls[0]["dst_path"] == destination
    assert calls[0]["skip_tasks"] is True


def test_publish_invokes_explicit_github_publishing(monkeypatch, tmp_path: Path) -> None:
    project = tmp_path / "generated-project"
    calls: list[dict[str, object]] = []

    monkeypatch.setattr(cli, "publish_project", lambda *args, **kwargs: calls.append({"args": args, **kwargs}))

    result = cli.main(
        [
            "publish",
            str(project),
            "--visibility",
            "private",
            "--remote",
            "upstream",
            "--skip-pages",
            "--dry-run",
        ]
    )

    assert result == 0
    assert calls == [
        {
            "args": (project,),
            "visibility": "private",
            "remote": "upstream",
            "configure_pages": False,
            "dry_run": True,
        }
    ]
