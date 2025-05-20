"""
Unit tests for the functions defined in file_writer.py.
These tests isolate each function to ensure correctness, side-effect behavior,
and user interaction handling without requiring actual CLI execution.
"""

import pytest
from unittest.mock import patch, MagicMock, mock_open
from core.file_writer import (
    safe_write_file,
    append_to_file,
    append_docstring,
    create_structure_from_dict,
    append_to_todo
)
from pathlib import Path


@pytest.fixture
def mock_file_exists():
    with patch("core.file_writer.Path.exists", return_value=True) as mock_exists:
        yield mock_exists

@pytest.fixture
def mock_file_not_exists():
    with patch("core.file_writer.Path.exists", return_value=False) as mock_not_exists:
        yield mock_not_exists

@pytest.fixture
def mock_file_write():
    with patch("core.file_writer.Path.write_text") as mock_write, \
         patch("core.file_writer.Path.mkdir") as mock_mkdir:
        yield mock_write, mock_mkdir

@pytest.fixture
def mock_console_print():
    with patch("core.file_writer.console.print") as mock_print:
        yield mock_print

@pytest.fixture
def mock_user_confirm():
    with patch("core.file_writer.Confirm.ask", return_value=True) as mock_confirm:
        yield mock_confirm

@pytest.fixture
def mock_user_decline():
    with patch("core.file_writer.Confirm.ask", return_value=False) as mock_decline:
        yield mock_decline

@pytest.fixture
def mock_file_read():
    with patch("core.file_writer.Path.read_text", return_value="old content") as mock_read:
        yield mock_read

@pytest.fixture
def mock_file_append():
    with patch("core.file_writer.open", mock_open(read_data="old content")) as mock_append:
        yield mock_append


# -----------------------
# safe_write_file
# -----------------------
def test_safe_write_file_overwrite(mock_user_confirm, mock_file_read, mock_file_exists, mock_file_write, mock_console_print): 
    """
    Test safe_write_file when the file exists and the content is different 
    and the user chooses to overwrite.
    """
    filepath = "test.txt"
    new_content = "new content"
    safe_write_file(filepath, new_content)

    # Assert file read exists, is read, user confirms, file is written
    mock_file_read.assert_called_once()
    mock_file_exists.assert_called_once()
    mock_user_confirm.assert_called_once()
    mock_file_write[0].assert_called_once_with(new_content)
    mock_file_write[1].assert_called_once_with(parents=True, exist_ok=True)


def test_safe_write_file_create(mock_file_not_exists, mock_file_write, mock_file_read, mock_user_confirm, mock_console_print):
    """
    Test safe_write_file when the file does not exist.
    """
    filepath = "test.txt"
    new_content = "new content"
    safe_write_file(filepath, new_content)

    # Assert file does not exist, file is not read, user is not called to confirm, new file is created
    mock_file_not_exists.assert_called_once()
    mock_file_read.assert_not_called()
    mock_user_confirm.assert_not_called()
    mock_file_write[0].assert_called_once_with(new_content)
    mock_file_write[1].assert_called_once_with(parents=True, exist_ok=True)


def test_safe_write_file_no_overwrite(mock_file_exists, mock_file_read, mock_file_write, mock_console_print, mock_user_decline):
    """
    Test safe_write_file when the file exists and the content is different,
    but the user chooses not to overwrite.
    """
    filepath = "test.txt"
    new_content = "new content"
    safe_write_file(filepath, new_content)

    # Assert file exists, is read, user declines, file is not written
    mock_file_read.assert_called_once()
    mock_file_exists.assert_called_once()
    mock_user_decline.assert_called_once()
    mock_file_write[0].assert_not_called()
    mock_file_write[1].assert_not_called()


def test_safe_write_file_no_change(mock_file_exists, mock_file_read, mock_file_write, mock_user_confirm, mock_console_print):
    """
    Test safe_write_file when the file exists and the content is the same.
    """
    filepath = "test.txt"
    new_content = "old content"
    safe_write_file(filepath, new_content)

    # Assert file exists, is read, user is not called to confirm, file is not written
    mock_file_read.assert_called_once()
    mock_file_exists.assert_called_once()
    mock_user_confirm.assert_not_called()
    mock_file_write[0].assert_not_called()
    mock_file_write[1].assert_not_called()


# -----------------------
# append_to_file
# -----------------------
def test_append_to_file_new_file(mock_file_append, mock_console_print):
    """
    Test append_to_file when the file does not exist.
    """
    filepath = "test.txt"
    content_to_append = "new content"
    append_to_file(filepath, content_to_append)

    # Assert file is created and content is appended
    mock_file_append.assert_called_once()


def test_append_to_file_existing_file(mock_file_append, mock_console_print):
    """
    Test append_to_file when the file exists.
    """
    filepath = "test.txt"
    content_to_append = "new content"
    append_to_file(filepath, content_to_append)

    # Assert file is opened and content is appended
    mock_file_append.assert_called_once()


# -----------------------
# append_docstring
# -----------------------
def test_append_docstring_existing_file_no_docstring(mock_file_exists, mock_file_write, mock_file_read, mock_console_print):
    """
    Test append_docstring when the file exists and the docstring is not present.
    """
    filepath = "test.txt"
    docstring = "This is a docstring"
    append_docstring(filepath, docstring)

    # Assert file is read, docstring is added with the file content
    mock_file_exists.assert_called_once()
    mock_file_write[0].assert_called_once_with('"""' + docstring + '"""' + "\nold content")
    mock_file_write[1].assert_called_once_with(parents=True, exist_ok=True)


def test_append_docstring_new_file(mock_file_not_exists, mock_file_write, mock_console_print):
    """
    Test append_docstring when the file does not exist.
    """
    filepath = "test.txt"
    docstring = "This is a docstring"
    append_docstring(filepath, docstring)

    # Assert file is created and docstring is appended
    mock_file_not_exists.assert_called_once()
    mock_file_write[0].assert_called_once_with('"""' + docstring + '"""')
    mock_file_write[1].assert_called_once_with(parents=True, exist_ok=True)


def test_append_docstring_existing_file_declined(mock_file_exists, mock_file_read, mock_user_decline, mock_file_write, mock_console_print):
    """
    Test append_docstring when the file exists and the docstring is already present
    and the user chooses not to overwrite.
    """
    filepath = "test.txt"
    docstring = "This is a docstring"
    mock_file_read.return_value = '"""Existing docstring"""'

    append_docstring(filepath, docstring)

    # Assert file is read, docstring is not added
    mock_file_exists.assert_called_once()
    mock_file_read.assert_called_once()
    mock_user_decline.assert_called_once()
    mock_file_write[0].assert_not_called()
    mock_file_write[1].assert_called_once_with(parents=True, exist_ok=True)


def test_append_docstring_existing_file_confirm(mock_file_exists, mock_file_read, mock_user_confirm, mock_file_write, mock_console_print):

    """
    Test append_docstring when the file exists and the docstring is already present
    and the user chooses to overwrite.
    """
    filepath = "test.txt"
    docstring = "This is a docstring"
    mock_file_read.return_value = '"""Existing docstring"""'

    append_docstring(filepath, docstring)

    # Assert file is read, docstring is added
    mock_file_exists.assert_called_once()
    mock_file_read.assert_called_once()
    mock_file_write[0].assert_called_once_with('"""' + docstring + '"""\n')
    mock_file_write[1].assert_called_once_with(parents=True, exist_ok=True)


# -------------------------
# create_structure_from_dict
# -------------------------
