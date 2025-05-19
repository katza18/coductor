'''
Purpose: Generates test stubs or specs based on project code.

Responsibilities:
Analyze functions/files
Produce pytest stubs or YAML test plans
Place in tests/ directory

Spec:
@app.command("gen")
- Options: --mode [stubs|specs|full]
- Output: tests/test_<module>.py
'''

import typer
from pathlib import Path
from core.prompts import load_prompt
from rich.console import Console
from core.agent import send_prompt

app = typer.Typer()
console = Console()

@app.command("gen")
def generate_tests(line_start: int, line_end: int, file_path: str, mode: str = "stubs"):
    """
    Generate test stubs or specs based on project code.

    Args:
        mode (str): The mode of generation. Options are 'stubs', 'specs', or 'full'.
    """
    if mode not in ["stubs", "specs", "full"]:
        raise ValueError("Invalid mode. Choose from 'stubs', 'specs', or 'full'.")

    # Get the file content
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist.")
    with open(file_path, "r") as f:
        file_content = f.readlines()
    # Extract the relevant lines
    relevant_lines = file_content[line_start-1:line_end]

    # Load prompt
    template = load_prompt("generate_tests")
    prompt = template.render(
        mode=mode,
        code="\n".join(relevant_lines)
    )

    # Send the prompt to Coductor and get the response
    response = send_prompt(prompt)

    # Create the tests directory if it doesn't exist
    tests_dir = Path("tests")
    tests_dir.mkdir(parents=True, exist_ok=True)

    # Write the response to a test file if it doesn't exist
    test_file_path = tests_dir / f"test_{file_path.stem}.py"
    if not test_file_path.exists():
        with open(test_file_path, "w") as f:
            f.write(response)
        console.print(f"[bold green]Test file created:[/bold green] {test_file_path}")
    else:
        # Append to the existing test file
        with open(test_file_path, "a") as f:
            f.write("\n" + response)
        console.print(f"[bold yellow]Test file already exists. Appended to:[/bold yellow] {test_file_path}")
