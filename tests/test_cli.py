"""Tests for the Python Project Foundry command-line interface."""

from pathlib import Path

from python_project_foundry import cli


def test_template_invokes_copier(monkeypatch, tmp_path: Path) -> None:
    destination = tmp_path / "new-project"
    calls: list[dict[str, object]] = []

    monkeypatch.setattr(cli.copier, "run_copy", lambda **kwargs: calls.append(kwargs))

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
    assert calls == [
        {
            "src_path": str(cli._template_path()),
            "dst_path": destination,
            "defaults": True,
            "overwrite": True,
            "pretend": True,
            "skip_tasks": True,
            "unsafe": True,
        }
    ]


def test_template_source_is_available() -> None:
    assert (cli._template_path() / "copier.yaml").is_file()
    assert (cli._template_path() / "template").is_dir()


def test_destination_without_subcommand_defaults_to_template(monkeypatch, tmp_path: Path) -> None:
    destination = tmp_path / "new-project"
    calls: list[dict[str, object]] = []

    monkeypatch.setattr(cli.copier, "run_copy", lambda **kwargs: calls.append(kwargs))

    result = cli.main([str(destination), "--skip-tasks"])

    assert result == 0
    assert calls[0]["dst_path"] == destination
    assert calls[0]["skip_tasks"] is True
