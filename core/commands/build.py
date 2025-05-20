'''
Purpose: Initializes a brand new project from a user prompt.
Creates a readme, todo list, project structure, and docstrings
to describe each file.

Responsibilities:
- Accept user description and goals
- Choose tech stack and architecture
- Create base folder + README.md, .gitignore, etc.

Spec:
@app.command("new") - Main entry point for the command

Output: Project directory with scaffolding + summaries
'''
import asyncio
import typer
from rich.console import Console
from core.agent import send_prompt
from core.file_writer import safe_write_file, create_structure_from_dict
from core.prompts.prompt_loader import load_prompt

# Init typer app and rich console
app = typer.Typer()
console = Console()

def get_project_idea() -> str:
    '''
    Prompt the user for a project idea.
    '''
    console.print("[bold green]What do you want to build?[/bold green]")
    return typer.prompt("Describe your project idea")


async def ask_coductor_for_name_and_stack(idea: str) -> dict[str, str]:
    '''
    Ask Coductor for a project name and tech stack.
    '''
    template = load_prompt("generate_name_and_stack")
    prompt = template.render(idea=idea)
    return await send_prompt(prompt)


def confirm_name_and_stack(name: str, stack: str) -> bool:
    '''
    Confirm the project name and tech stack with the user.
    '''
    console.print(f"[bold cyan]Project Name:[/bold cyan] {name}")
    console.print(f"[bold cyan]Tech Stack:[/bold cyan] {stack}")

    return typer.confirm("\nDo you want to proceed with this name and stack?")


async def ask_coductor_to_plan(idea: str, name: str, stack: str) -> dict:
    '''
    Ask Coductor to plan the project.
    '''
    template = load_prompt("plan_project")
    prompt = template.render(idea=idea, stack=stack, name=name)
    return await send_prompt(prompt)


def confirm_plan(plan: dict) -> bool:
    '''
    Confirm the plan with the user.
    '''
    console.print("[bold cyan]TODO List:[/bold cyan]")
    for i, item in enumerate(plan['todo'], 1):
        console.print(f"{i}. {item}")

    console.print(f"[bold cyan]File Structure:[/bold cyan]")
    console.print(plan['structure'])

    return typer.confirm("\nDo you want to proceed with this plan?")


def scaffold_project(file_structure: dict, root: str = "./") -> None:
    '''
    Create the project structure based on the plan.
    '''
    # Create the project directory
    create_structure_from_dict(file_structure, base_path=root)


def generate_readme(project_name: str, idea: str, tech_stack: str) -> str:
    '''
    Generate a README.md file based on the project name and plan.
    '''
    readme_content = f"# {project_name}\n\n"
    readme_content += "## Project Overview\n\n"
    readme_content += f"**Idea:** {idea}\n\n"
    readme_content += "## Tech Stack\n\n"
    readme_content += f"{tech_stack}\n\n"

    safe_write_file("README.md", readme_content)


def generate_todo(todo_dict: dict) -> str:
    '''
    Generate a TODO.md file based on the project name and plan.
    '''
    todo_content = "# TODO"
    for goal, tasks in todo_dict.items():
        todo_content += f"\n\n## {goal}"
        for task in tasks:
            todo_content += f"\n- [ ] {task}"

    safe_write_file("TODO.md", todo_content)


@app.command("new")
def build_new():
    asyncio.run(_build_new())

async def _build_new():
    try:
        console.print("[bold green]Welcome to the Coductor Project Builder![/bold green]")

        # Get project idea from user
        idea = get_project_idea()

        # Ask Coductor for a project name and tech stack
        name_stack = await ask_coductor_for_name_and_stack(idea)

        # Confirm the name and stack with the user
        if not confirm_name_and_stack(name_stack["name"], name_stack["stack"]):
            console.print("[red]Aborted by user.[/red]")
            raise typer.Abort()

        # Ask Coductor to plan the project
        plan = await ask_coductor_to_plan(idea, name_stack["name"], name_stack["stack"])

        # Confirm the plan with the user
        if not confirm_plan(plan):
            console.print("[red]Aborted by user.[/red]")
            raise typer.Abort()

        # Scaffold the project based on the plan
        scaffold_project(plan['structure'])
        generate_readme(name_stack['name'], idea, name_stack['stack'])
        generate_todo(plan['todo'])

        console.print("[green]Project initialized successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Abort()
