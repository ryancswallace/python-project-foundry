"""Tests for the Python Project Foundry command-line interface."""

from pathlib import Path

from copier._template import Template

from python_project_foundry import cli


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
