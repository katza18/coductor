'''
Purpose: Adds a new feature across the project intelligently.

Responsibilities:
- Accept natural language feature request
- Analyze structure and update/create files
- Append tasks to TODO list

Spec:
@app.command("add") - Ex: coductor feature add "Add user password reset flow"
'''
import typer
from rich.console import Console
from core.prompts.prompt_loader import load_prompt
from core.agent import send_prompt
from pathlib import Path
from core.file_writer import append_to_todo, create_structure_from_dict

app = typer.Typer()
console = Console()

def ask_coductor_to_add_feature(feature: str) -> dict:
    '''
    Ask Coductor to add a feature to the project.
    '''
    # Load the prompt template for adding a feature
    template = load_prompt("add_feature")
    prompt = template.render(feature=feature)

    # Send the prompt to Coductor and get the response
    return send_prompt(prompt)


app.command("feature")
def add_feature(feature: str):
    '''
    Add a new feature to the project.
    '''
    console.print(f"[bold green]Adding feature:[/bold green] {feature}")

    # Run the prompt to add the feature to the project
    plan = ask_coductor_to_add_feature(feature)

    # Update or create files as needed
    create_structure_from_dict(plan["structure"])

    # Update file structure in readme


    # Append TODOs to the TODO list
    for goal, tasks in plan["todo"].items():
        append_to_todo(goal, tasks)

    # Notify the user of the changes
    console.print(f"[bold green]Feature added successfully![/bold green]")
