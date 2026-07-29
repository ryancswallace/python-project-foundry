"""End-to-end validation for a freshly generated repository."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from python_project_foundry import cli

RUN_GENERATED_E2E = os.environ.get("PPF_RUN_GENERATED_E2E") == "1"


@pytest.mark.skipif(
    not RUN_GENERATED_E2E,
    reason="set PPF_RUN_GENERATED_E2E=1 to run the generated-project toolchain",
)
def test_generated_project_bootstraps_checks_and_builds(tmp_path: Path) -> None:
    destination = tmp_path / "generated-project"

    assert cli.main(["template", str(destination), "--defaults"]) == 0

    subprocess.run(
        [
            "make",
            "lock-check",
            "lint",
            "typecheck",
            "test",
            "deps",
            "markdownlint",
            "docker-lint",
            "workflow-lint",
            "spellcheck",
            "docs",
            "secrets",
            "security",
            "build",
        ],
        cwd=destination,
        check=True,
        env={**os.environ, "UV_PROJECT_ENVIRONMENT": ".venv"},
    )

    expected_artifacts = {
        "generated_project-0.1.0-py3-none-any.whl",
        "generated_project-0.1.0.tar.gz",
        "generated-project.cdx.json",
    }
    assert expected_artifacts <= {artifact.name for artifact in (destination / "dist").iterdir()}
    assert (destination / "site/index.html").is_file()
