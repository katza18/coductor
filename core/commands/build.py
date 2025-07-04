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
from rich.prompt import Prompt, Confirm
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
    return Prompt.ask("\n[bold cyan]What do you want to build?[/bold cyan]")


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
    console.rule(style="bold cyan")
    console.print("\n[bold cyan]Coductor's Proposal[/bold cyan]")
    console.print(f"\n[bold cyan]Project Name:[/bold cyan] {name}")
    console.print(f"[bold cyan]Tech Stack:[/bold cyan] {stack}\n")
    console.rule(style="bold cyan")

    return Confirm.ask("[bold cyan]\nDo you want to proceed with this name and stack?[/bold cyan]")


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
    console.print("\n[bold cyan]TODO:[/bold cyan]")
    for i, (goal, tasks) in enumerate(plan['todo'].items(), 1):
        console.print(f"{i}. {goal}")
        for task in tasks:
            console.print(f"- [ ] {task}")

    console.print(f"\n[bold cyan]File Structure:[/bold cyan]")
    console.print(plan['structure'])

    return Confirm.ask("\n[bold cyan]Do you want to proceed with this plan?[/bold cyan]")


def scaffold_project(file_structure: dict, root: str = "./") -> None:
    '''
    Create the project structure based on the plan.
    '''
    # Create the project directory
    create_structure_from_dict(file_structure, base_path=root)


def generate_readme(project_name: str, idea: str, tech_stack: str, project_root: str) -> str:
    '''
    Generate a README.md file based on the project name and plan.
    '''
    readme_content = f"# {project_name}\n\n"
    readme_content += "## Project Overview\n\n"
    readme_content += idea
    readme_content += "\n\n## Tech Stack"
    for category, stack in tech_stack.items():
        readme_content += f"\n- **{category}**: {', '.join(stack)}"

    safe_write_file(project_root + "README.md", readme_content)


def generate_todo(todo_dict: dict, parent_path: str) -> str:
    '''
    Generate a TODO.md file based on the project name and plan.
    '''
    todo_content = "# TODO"
    for goal, tasks in todo_dict.items():
        todo_content += f"\n\n## {goal}"
        for task in tasks:
            todo_content += f"\n- [ ] {task}"

    safe_write_file(parent_path + "TODO.md", todo_content)

def print_title_message():
    title = """                             
 ██████╗ ██████╗ ██████╗ ██╗   ██╗ ██████╗████████╗ ██████╗ ██████╗ 
██╔════╝██╔═══██╗██╔══██╗██║   ██║██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
██║     ██║   ██║██║  ██║██║   ██║██║        ██║   ██║   ██║██████╔╝
██║     ██║   ██║██║  ██║██║   ██║██║        ██║   ██║   ██║██╔══██╗
╚██████╗╚██████╔╝██████╔╝╚██████╔╝╚██████╗   ██║   ╚██████╔╝██║  ██║
 ╚═════╝ ╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝                
    """
    console.clear()
    console.rule(style="bold cyan")
    console.print(title, style="bold cyan")
    console.rule(style="bold cyan")
    console.print(
        """
Coductor takes a project idea and builds a complete project structure
with a README, TODO list, and docstrings to help you get started.
        """)
    console.rule(style="bold cyan")

@app.command("new")
def build_new(parent_path: str = "./"):
    asyncio.run(_build_new(parent_path))

async def _build_new(parent_path: str):
    try:
        print_title_message()

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
        md_file_path = parent_path + name_stack['name'] + "/"
        scaffold_project(plan['structure'], parent_path)
        generate_readme(name_stack['name'], idea, name_stack['stack'], md_file_path)
        generate_todo(plan['todo'], md_file_path)

        console.print("[green]Project initialized successfully![/green]")
    except Exception as e:
        raise typer.Abort()
