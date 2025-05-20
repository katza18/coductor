"""
Unit tests for the functions defined in build.py.
These tests isolate each function to ensure correctness, side-effect behavior,
and user interaction handling without requiring actual CLI execution.
"""

import pytest
from unittest.mock import patch, MagicMock, mock_open
from core.commands.build import (
    get_project_idea,
    ask_coductor_for_name_and_stack,
    confirm_name_and_stack,
    ask_coductor_to_plan,
    confirm_plan,
    scaffold_project,
    generate_readme,
    generate_todo
)

# -----------------------
# get_project_idea
# -----------------------
@patch("typer.prompt", return_value="Build an AI assistant.")
@patch("core.commands.build.console.print")
def test_get_project_idea(mock_print, mock_prompt):
    result = get_project_idea()
    assert result == "Build an AI assistant."
    mock_print.assert_called_once()
    mock_prompt.assert_called_once()


# -----------------------
# ask_coductor_for_name_and_stack
# -----------------------
@patch("core.commands.build.send_prompt", return_value=("Coductor", "Python + Typer"))
@patch("core.commands.build.load_prompt")
def test_ask_coductor_for_name_and_stack(mock_load_prompt, mock_send_prompt):
    template = MagicMock()
    template.render.return_value = "Prompt text"
    mock_load_prompt.return_value = template

    result = ask_coductor_for_name_and_stack("AI assistant")
    assert result == ("Coductor", "Python + Typer")
    template.render.assert_called_once_with(idea="AI assistant")
    mock_send_prompt.assert_called_once()


# -----------------------
# confirm_name_and_stack
# -----------------------
@patch("typer.confirm", return_value=True)
@patch("core.commands.build.console.print")
def test_confirm_name_and_stack_yes(mock_print, mock_confirm):
    result = confirm_name_and_stack("Coductor", "Python + Typer")
    assert result is True
    assert mock_confirm.called
    assert mock_print.call_count == 2


# -----------------------
# ask_coductor_to_plan
# -----------------------
@patch("core.commands.build.send_prompt", return_value={"todo": {}, "structure": {}, "stack": "Python", "file_structure": "some/dir"})
@patch("core.commands.build.load_prompt")
def test_ask_coductor_to_plan(mock_load_prompt, mock_send_prompt):
    template = MagicMock()
    template.render.return_value = "Rendered prompt"
    mock_load_prompt.return_value = template

    result = ask_coductor_to_plan("Build something", "Coductor", "Python")
    assert isinstance(result, dict)
    template.render.assert_called_once_with(idea="Build something", name="Coductor", stack="Python")
    mock_send_prompt.assert_called_once()


# -----------------------
# confirm_plan
# -----------------------
@patch("typer.confirm", return_value=True)
@patch("core.commands.build.console.print")
def test_confirm_plan(mock_print, mock_confirm):
    plan = {
        "todo": ["Set up CLI", "Write README"],
        "structure": {"src": {"main.py": ""}},
    }
    result = confirm_plan(plan)
    assert result is True
    assert mock_confirm.called
    assert mock_print.call_count >= 3  # prints for stack, todo, structure


# -----------------------
# scaffold_project
# -----------------------
@patch("core.commands.build.create_structure_from_dict")
def test_scaffold_project(mock_create_structure):
    dummy_structure = {"project": ["main.py"]}
    scaffold_project(dummy_structure, root="./test")
    mock_create_structure.assert_called_once_with(dummy_structure, base_path="./test")


# -----------------------
# generate_readme
# -----------------------
@patch("core.commands.build.safe_write_file")
def test_generate_readme(mock_write_file):
    generate_readme("Coductor", "Build an assistant", "Python + Typer")
    expected_content = (
        "# Coductor\n\n"
        "## Project Overview\n\n"
        "**Idea:** Build an assistant\n\n"
        "## Tech Stack\n\n"
        "Python + Typer\n\n"
    )
    mock_write_file.assert_called_once_with("README.md", expected_content)


# -----------------------
# generate_todo
# -----------------------
@patch("core.commands.build.safe_write_file")
def test_generate_todo(mock_write_file):
    todo_dict = {
        "Setup": ["Initialize repo", "Install dependencies"],
        "Development": ["Build CLI", "Write tests"]
    }
    generate_todo(todo_dict)
    assert mock_write_file.call_count == 1
    content = mock_write_file.call_args[0][1]

    assert "# TODO" in content
    assert "## Setup" in content
    assert "- [ ] Initialize repo" in content
    assert "- [ ] Install dependencies" in content
    assert "## Development" in content
