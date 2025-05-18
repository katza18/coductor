'''
Purpose: Analyze current repo to summarize structure and intent.

Responsibilities:
- Walk the directory tree
- Read and parse files (imports, docstrings, functions)
- Generate file summaries

Spec:
- get_file_structure(root: str) -> dict
- summarize_file(path: str) -> str
'''

import ast
import os
from pathlib import Path
from typing import List, Dict
from rich.console import Console
import yaml

console = Console()

EXCLUDED_DIRS = {".git", "venv", ".coductor", "__pycache__"}

def get_python_files(root: Path) -> List[Path]:
    return [
        f for f in root.rglob("*.py")
        if not any(excluded in f.parts for excluded in EXCLUDED_DIRS)
    ]

def analyze_file(filepath: Path) -> Dict:
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source, filename=str(filepath))

    classes = []
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "docstring": ast.get_docstring(node)
            })
        elif isinstance(node, ast.ClassDef):
            classes.append({
                "name": node.name,
                "docstring": ast.get_docstring(node)
            })

    return {
        "file": str(filepath),
        "classes": classes,
        "functions": functions,
        "summary": summarize_structure(filepath, classes, functions),
    }

def summarize_structure(filepath, classes, functions) -> str:
    summary = f"{filepath.name} defines:\n"
    if classes:
        summary += "- Classes: " + ", ".join(c['name'] for c in classes) + "\n"
    if functions:
        summary += "- Functions: " + ", ".join(f['name'] for f in functions) + "\n"
    return summary.strip()

def analyze_project(root: Path) -> List[Dict]:
    py_files = get_python_files(root)
    results = []

    for file in py_files:
        console.print(f"[cyan]Analyzing {file}[/cyan]")
        result = analyze_file(file)
        results.append(result)

    return results

def save_summaries(summaries: List[Dict], path: Path = Path(".coductor/summaries.yml")):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(summaries, f)

if __name__ == "__main__":
    root = Path(".")  # current repo
    summaries = analyze_project(root)
    save_summaries(summaries)
