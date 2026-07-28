"""Integration tests for the bundled Copier template."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tomllib
from pathlib import Path

import copier
import yaml

PROJECT_ROOT = Path(__file__).parents[1]
PLACEHOLDER_NAMES = {
    "author_email",
    "author_name",
    "copyright_year",
    "coverage_fail_under",
    "documentation_url",
    "exception_class_name",
    "github_environment_reviewer_id",
    "initial_version",
    "license",
    "package_name",
    "project_description",
    "project_name",
    "project_slug",
    "python_default_version",
    "python_max_version_exclusive",
    "python_min_version",
    "repository_name",
    "repository_owner",
    "repository_url",
}
UNRENDERED_PLACEHOLDER = re.compile(r"{{\s*(" + "|".join(sorted(PLACEHOLDER_NAMES)) + r")\b")


def _copy_template_source(destination: Path) -> Path:
    """Copy the working template without its Git metadata.

    Copier intentionally renders committed revisions when its source is a Git
    checkout. A metadata-free snapshot lets this test exercise working-tree
    template changes before they are committed.
    """
    source = destination / "template-source"
    source.mkdir()
    shutil.copy2(PROJECT_ROOT / "copier.yaml", source)
    shutil.copytree(PROJECT_ROOT / "copier", source / "copier")
    shutil.copytree(PROJECT_ROOT / "template", source / "template")
    return source


def test_custom_answers_render_a_consistent_project(tmp_path: Path) -> None:
    source = _copy_template_source(tmp_path)
    destination = tmp_path / "orbit-tools"
    answers = {
        "project_name": "Orbit Tools",
        "project_description": "Reliable tools for orbital calculations.",
        "initial_version": "1.2.3",
        "project_slug": "orbit-tools",
        "package_name": "orbit_tools",
        "exception_class_name": "OrbitToolsError",
        "license": "BSD-3-Clause",
        "python_min_version": "3.12",
        "python_default_version": "3.14",
        "python_max_version_exclusive": "3.15",
        "coverage_fail_under": 91,
        "initialize_git_repository": False,
        "run_setup_tasks": False,
        "repository_owner": "space-labs",
        "repository_name": "orbit-tools-python",
        "repository_url": "https://github.com/space-labs/orbit-tools-python",
        "github_environment_reviewer_id": "123456",
        "documentation_url": "https://space-labs.github.io/orbit-tools-python/",
        "author_name": "Ada Example",
        "author_email": "ada@example.org",
        "copyright_year": 2027,
    }

    copier.run_copy(  # pyright: ignore[reportAttributeAccessIssue]
        src_path=str(source),
        dst_path=destination,
        data=answers,
        defaults=True,
        overwrite=True,
        skip_tasks=True,
        unsafe=True,
        quiet=True,
    )

    assert (destination / "src/orbit_tools/__init__.py").is_file()
    assert "BSD 3-Clause License" in (destination / "LICENSE").read_text()

    pyproject = tomllib.loads((destination / "pyproject.toml").read_text())
    assert pyproject["project"]["name"] == "orbit-tools"
    assert pyproject["project"]["requires-python"] == ">=3.12,<3.15"
    assert "License :: OSI Approved :: BSD License" in pyproject["project"]["classifiers"]
    assert "Programming Language :: Python :: 3.11" not in pyproject["project"]["classifiers"]

    package_json = json.loads((destination / "package.json").read_text())
    assert package_json["name"] == "orbit-tools"

    dockerfile = (destination / "Dockerfile").read_text()
    assert "uv sync --locked --no-dev --group test" in dockerfile

    make_environment = {**os.environ, "UV_PROJECT_ENVIRONMENT": "/tmp/shared-uv-environment"}
    make_result = subprocess.run(
        [
            "make",
            "--no-print-directory",
            "--eval=print-uv-project-environment:\n\t@printf '%s' '$(UV_PROJECT_ENVIRONMENT)'",
            "print-uv-project-environment",
        ],
        cwd=destination,
        env=make_environment,
        check=True,
        capture_output=True,
        text=True,
    )
    assert make_result.stdout == ".venv"

    workflow = yaml.safe_load((destination / ".github/workflows/ci.yml").read_text())
    versions = [
        entry["python-version"]
        for entry in workflow["jobs"]["tests"]["strategy"]["matrix"]["include"]
        if entry["os"] == "ubuntu-24.04"
    ]
    assert versions == ["3.12", "3.13", "3.14"]

    recorded_answers = yaml.safe_load((destination / ".python-project-foundry.answers.yaml").read_text())
    assert answers.items() <= recorded_answers.items()

    for rendered_file in destination.rglob("*"):
        if rendered_file.is_file():
            content = rendered_file.read_text(errors="ignore")
            assert not UNRENDERED_PLACEHOLDER.search(content), rendered_file


def test_every_template_placeholder_has_a_question() -> None:
    template_placeholders: set[str] = set()
    for template_file in (PROJECT_ROOT / "template").rglob("*.jinja"):
        template_placeholders.update(UNRENDERED_PLACEHOLDER.findall(template_file.read_text()))

    assert template_placeholders == PLACEHOLDER_NAMES
