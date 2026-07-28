# How it works

Python Project Foundry has three layers:

1. `uvx` obtains the published Python package and runs it in an isolated
   environment.
2. The `python-project-foundry` command translates its focused options into a
   Copier invocation.
3. The Copier template bundled inside the wheel asks project questions,
   renders the selected files, and runs trusted setup tasks.

Bundling the template in the wheel makes a published package version a
repeatable unit: its CLI and its template travel together. The source checkout
remains usable for developing and testing changes before they are released.

## Trust model

Copier templates can execute tasks. Python Project Foundry deliberately enables
its bundled template tasks because they initialize and prepare the generated
project. Users should install releases from the expected PyPI project and
review changes before overwriting an existing destination.

## Source layout

| Path | Responsibility |
| --- | --- |
| `src/python_project_foundry/` | Published CLI package. |
| `copier.yaml` and `copier/` | Copier questions and behavior. |
| `template/` | Files rendered into a generated project. |
| `docs/` | This documentation site. |
