"""
Unit tests for the 'build' command in build.py.

These tests ensure the command behaves correctly by:
- Mocking user input prompts
- Mocking Coductor agent responses
- Validating project scaffolding and file generation logic

Note: External effects like file writing and LLM calls are mocked.
"""

import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock
from core.commands.build import app

runner = CliRunner()

@pytest.fixture
def mock_send_prompt():
    with patch("core.commands.build.send_prompt") as mock:
        yield mock

@pytest.fixture
def mock_prompt_and_confirm():
    with patch("core.commands.build.typer.prompt", return_value="A web app that helps people track habits"), \
         patch("core.commands.build.typer.confirm", return_value=True):
        yield

@pytest.fixture
def mock_console_print():
    with patch("core.commands.build.console.print"):
        yield

@pytest.fixture
def mock_io_helpers():
    with patch("core.commands.build.create_structure_from_dict") as mock_create_structure, \
         patch("core.commands.build.safe_write_file") as mock_write_file:
        yield mock_create_structure, mock_write_file

def test_build_new_project_success(mock_send_prompt, mock_prompt_and_confirm, mock_io_helpers):
    # Mocking LLM responses for name/stack and plan
    mock_send_prompt.side_effect = [
        {"name": "HabitTracker", "stack": {"Lanugage": ["Python"], "Frameworks": ["FastAPI", "React"]}},
        {
            "todo": {"file.py": ["Design UI", "Set up backend"]},
            "structure": {"habittracker": {"__init__.py": ""}},
        }
    ]

    result = runner.invoke(app, [])

    print(result.output)  # For debugging purposes

    assert result.exit_code == 0
    assert "Project initialized successfully!" in result.output
    mock_io_helpers[0].assert_called_once()
    assert mock_io_helpers[1].call_count == 2  # README.md and TODO.md

def test_user_aborts_after_name_confirmation(mock_send_prompt):
    with patch("core.commands.build.typer.prompt", return_value="Some idea"), \
         patch("core.commands.build.typer.confirm", return_value=False):

        mock_send_prompt.return_value = {"name": "TestProj", "stack": "Python"}

        result = runner.invoke(app, [])
        assert result.exit_code != 0
        assert "Aborted by user." in result.output
