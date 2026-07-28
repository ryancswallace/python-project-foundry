"""Generate mkdocstrings API reference pages for public package modules."""

from pathlib import Path

import mkdocs_gen_files

PACKAGE_NAME = "python_project_foundry"
PACKAGE_ROOT = Path("src") / PACKAGE_NAME
REFERENCE_ROOT = Path("reference/api")


def _iter_public_modules() -> list[tuple[str, Path, Path]]:
    """Return import path, source path, and generated documentation path."""
    modules: list[tuple[str, Path, Path]] = []
    for source_path in sorted(PACKAGE_ROOT.glob("*.py")):
        if source_path.name.startswith("_") and source_path.name != "__init__.py":
            continue

        module_parts = source_path.relative_to("src").with_suffix("").parts
        import_path = ".".join(part for part in module_parts if part != "__init__")
        docs_name = "index.md" if source_path.name == "__init__.py" else f"{source_path.stem}.md"
        modules.append((import_path, source_path, REFERENCE_ROOT / docs_name))

    return modules


for module, source, docs_path in _iter_public_modules():
    title = "Package" if module == PACKAGE_NAME else module.rsplit(".", 1)[-1].replace("_", " ").title()
    with mkdocs_gen_files.open(docs_path, "w") as output:
        output.write(f"# {title}\n\n")
        output.write(f"::: {module}\n")

    mkdocs_gen_files.set_edit_path(docs_path, source)
