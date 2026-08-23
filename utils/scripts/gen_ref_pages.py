import ast
from pathlib import Path

import mkdocs_gen_files

ROOT = Path(__file__).parent.parent
PACKAGE = ROOT / "utils"

nav = mkdocs_gen_files.Nav()

def get_module_name(path: Path) -> str:
    parts = list(path.relative_to(ROOT).with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def get_public_members(path: Path) -> tuple[list[str], list[str]]:
    tree = ast.parse(path.read_text())
    functions, classes = [], []

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            if not node.name.startswith("_"):
                classes.append(node.name)

    return functions, classes


def get_class_methods(path: Path, class_name: str) -> list[str]:
    tree = ast.parse(path.read_text())

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return [
                child.name
                for child in node.body
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
                and not child.name.startswith("_")
            ]

    return []

def write_page(
    page_path: Path,
    title: str,
    identifier: str,
    nav_key: list[str],
    source_path: Path,
    show_root_heading: bool = True,
) -> None:
    with mkdocs_gen_files.open(page_path, "w") as fd:
        print(f"# `{title}`", file=fd)
        print(file=fd)
        print(f"::: {identifier}", file=fd)
        if not show_root_heading:
            print("    options:", file=fd)
            print("      show_root_heading: false", file=fd)

    nav[nav_key] = page_path.as_posix()
    mkdocs_gen_files.set_edit_path(page_path, source_path.relative_to(ROOT))

for path in sorted(PACKAGE.rglob("*.py")):
    module = get_module_name(path)
    if not module:
        continue

    nav_parts = module.split(".")[1:]
    if not nav_parts:
        continue

    module_dir = Path("reference", *nav_parts[:-1]) / nav_parts[-1]
    functions, classes = get_public_members(path)

    write_page(
        page_path=Path("reference", *nav_parts).with_suffix(".md"),
        title=module,
        identifier=module,
        nav_key=nav_parts,
        source_path=path,
        show_root_heading=False,
    )

    for function in functions:
        write_page(
            page_path=module_dir / "functions" / f"{function}.md",
            title=function,
            identifier=f"{module}.{function}",
            nav_key=[*nav_parts, "Functions", function],
            source_path=path,
        )

    for class_name in classes:
        write_page(
            page_path=module_dir / "classes" / f"{class_name}.md",
            title=class_name,
            identifier=f"{module}.{class_name}",
            nav_key=[*nav_parts, class_name],
            source_path=path,
        )

        for method in get_class_methods(path, class_name):
            write_page(
                page_path=module_dir / "classes" / class_name / f"{method}.md",
                title=method,
                identifier=f"{module}.{class_name}.{method}",
                nav_key=[*nav_parts, class_name, method],
                source_path=path,
            )