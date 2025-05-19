# ✅ Coductor Project — Complete TODO Checklist

## 🔧 1. Project Initialization
- [x] Create the `coductor/` folder
- [x] Set up a virtual environment: `python -m venv .venv`
- [x] Activate environment and upgrade `pip`
- [x] Initialize a Git repository and create a `.gitignore`
- [x] Create an empty `README.md`
- [x] Create folders and files:
  - [x] `core/commands/`
  - [x] `core/prompts/`
  - [x] `tests/`
  - [x] `.coductor/`
  - [x] `main.py`
  - [x] `pyproject.toml` or `requirements.txt`

---

## 📦 2. Install Dependencies
- [ ] Install runtime packages: `typer`, `openai`, `pyyaml`, `rich`, `tiktoken`, `dotenv`
- [ ] Install dev tools: `pytest`, `black`, `isort`, `mypy`, `pre-commit`
- [ ] Create a `.env` file and store OpenAI API key
- [ ] Load `.env` key in `agent.py`

---

## 🧠 3. Core Logic

### `core/agent.py` (LLM Engine)
- [x] Load OpenAI API key securely
- [x] Implement prompt send function (text + streaming)
- [x] Add token management helpers
- [ ] Integrate prompt templates

### `core/memory.py` (Project State)
- [x] Track todos (`.coductor/todo.yml`)
- [x] Load/save memory (summaries, history, goals)
- [x] Support modifying todo statuses

### `core/file_writer.py` (Safe Writes)
- [x] Safely write or append to files
- [x] Preview diffs with `rich`
- [x] Add overwrite protection and confirmation

### `core/project_analyzer.py` (Repo Parsing)
- [x] Recursively scan file tree
- [x] Extract function names, classes, docstrings
- [x] Summarize file purpose
- [x] Skip excluded dirs (`venv`, `.git`, `.coductor`)

---

## 🧩 4. CLI Commands in `core/commands/`

### `build.py`
- [x] Ask user: “What do you want to build?”
- [x] Ask LLM for stack recommendation and plan
- [x] Confirm scaffold with user
- [x] Generate base structure + README + TODO + tests

### `add.py`
- [x] Ask: “What feature would you like to add?”
- [x] Analyze codebase to suggest changes
- [x] Use LLM to generate necessary code
- [x] Apply with `file_writer`

### `scaffold.py`
- [ ] Scan repo and create function expectations
- [ ] Annotate files with doc comments
- [ ] Populate summaries in memory

### `tests.py`
- [x] Analyze code and extract logic units
- [x] Ask LLM to generate tests
- [x] Write to `tests/test_*.py`

### Global
- [ ] Add initial prompt if the project has no session history.

---

## 🧪 5. Testing
- [ ] Create `tests/test_build.py`
- [ ] Add unit tests for core logic (`memory`, `file_writer`, etc.)
- [ ] Use `pytest` and fixtures
- [ ] Optional: Add test watcher (`pytest-watch`)

---

## 🛠️ 6. Tooling & Dev Experience
- [ ] Set up `black`, `isort`, `mypy`
- [ ] Configure `pre-commit` hooks
- [ ] Create `Makefile` or `scripts/` folder with helper commands

---

## 💬 7. CLI Entry (`main.py`)
- [ ] Set up `typer.Typer()` and register commands
- [ ] Route each command to its script
- [ ] Add help strings and CLI docs

---

## 📄 8. Documentation
- [ ] Write full `README.md` with:
  - [ ] Overview
  - [ ] Install instructions
  - [ ] CLI command list
  - [ ] Example workflow
- [ ] Add license (MIT?)
- [ ] Optional: add live GIFs or screenshots
- [ ] Optional: publish with `mkdocs` or GitHub Pages

---

## 🚀 9. Bonus Features (Post-MVP)
- [ ] `coductor doctor` – analyze repo health
- [ ] `coductor explain file.py` – explain file purpose
- [ ] Framework plugins (e.g., Flask, React)
- [ ] Optional: VS Code extension

---

## 📦 10. Packaging & Distribution
- [ ] Define project metadata in `pyproject.toml`
- [ ] Add `console_scripts` entry point for CLI use
- [ ] Optional: publish to PyPI

---

## 📸 11. Portfolio Polish
- [ ] Record a demo video (walkthrough use case)
- [ ] Write a blog post about the project
- [ ] Share to GitHub, LinkedIn, Reddit, etc.

---

## ✅ Final Review Table

| Step                        | Status |
|-----------------------------|--------|
| Project initialized         | [ ]    |
| Core engine implemented     | [ ]    |
| CLI working                 | [ ]    |
| Testing complete            | [ ]    |
| Docs written                | [ ]    |
| Portfolio polish complete   | [ ]    |
