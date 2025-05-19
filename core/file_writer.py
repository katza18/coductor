'''
Purpose: Safe writing and creation of files.

Responsibilities:
- Prevent overwrite unless approved
- Ensure directories exist
- Apply templates

Spec:
- write_file(path: str, content: str)
- create_folder(path: str)
- backup_existing(path: str)
'''

from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm
from rich.syntax import Syntax
from difflib import unified_diff

console = Console()

def safe_write_file(filepath: Path, new_content: str, force: bool = False):
    filepath = Path(filepath)
    old_content = ""

    if filepath.exists():
        old_content = filepath.read_text()

        if old_content.strip() == new_content.strip():
            console.print(f"[green]No changes needed for {filepath}[/green]")
            return

        # Show diff
        diff = unified_diff(
            old_content.splitlines(),
            new_content.splitlines(),
            fromfile=str(filepath),
            tofile=str(filepath),
            lineterm=""
        )
        console.print(f"[yellow]Proposed changes to {filepath}:[/yellow]\n")
        console.print("\n".join(diff), style="bold")

        if not force:
            confirm = Confirm.ask(f"Overwrite {filepath}?")
            if not confirm:
                console.print(f"[red]Aborted write to {filepath}[/red]")
                return

    # Write the file
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(new_content)
    console.print(f"[green]Wrote to {filepath}[/green]")

def append_to_file(filepath: Path, content_to_append: str):
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "a") as f:
        f.write("\n" + content_to_append)

    console.print(f"[green]Appended to {filepath}[/green]")

def append_docstring(filepath: Path, docstring: str):
    '''
    Append a docstring to the beginning of a file.
    '''
    # If there is no docstring, add the docstring to the begging of the file.
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "r") as f:
        content = f.read()
        if content.startswith('"""'):
            # There is likely a docstring, so we will need to overwrite it.
            # Find the end of the docstring
            end_index = content.find('"""', 3)
            if end_index == -1:
                raise ValueError(f"Docstring not closed in {filepath}")
        elif content.startswith("'''"):
            end_index = content.find("'''", 3)
            if end_index == -1:
                raise ValueError(f"Docstring not closed in {filepath}")
        else:
            end_index = 0
        new_content = "'''" + docstring + "'''" + content[end_index:]

    # Show diff and ask for confirmation
    diff = unified_diff(
        content.splitlines(),
        new_content.splitlines(),
        fromfile=str(filepath),
        tofile=str(filepath),
        lineterm=""
    )
    console.print(f"[yellow]Proposed changes to {filepath}:[/yellow]\n")
    console.print("\n".join(diff), style="bold")
    if not Confirm.ask(f"Overwrite {filepath}?"):
        console.print(f"[red]Aborted write to {filepath}[/red]")
        return

    # Write the file
    filepath.write_text(new_content)
    console.print(f"[green]Wrote to {filepath}[/green]")


def create_structure_from_dict(file_structure: dict, base_path: Path = Path('.')):
    '''
    Create a directory structure based on a dictionary.
    '''
    for name, content in file_structure.items():
        path = base_path / name
        if isinstance(content, dict):
            # If the content is a dictionary, create a folder and recurse
            path.mkdir(parents=True, exist_ok=True)
            create_structure_from_dict(content, path)
        else:
            if not path.exists():
                # Create a file with the content
                safe_write_file(path, content)
                console.print(f"[green]Created file:[/green]{path}")
            else:
                # Add the docstring to the begging if the file exists
                append_docstring(path, content)


def append_to_todo(category: str, tasks: list[str]):
    '''
    Append a TODO to the TODO list in project root.
    '''
    filepath = Path("./TODO.md")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "a") as f:
        f.write("\n\n" + category)
        f.write("\n" + "\n".join(tasks))
    console.print(f"[green]Appended to {filepath}[/green]")
