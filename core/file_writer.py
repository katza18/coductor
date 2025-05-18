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
