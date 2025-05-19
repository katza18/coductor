# Coductor
An AI based CLI tool that manages your projects for you from start to finish.

## Project Summary
A local CLI-based AI development assistant that manages your project like a technical lead. It scaffolds files, writes summaries, maintains a dynamic todo list, develops a comprehensive test suite, answers questions, and evolves the codebase alongside the developer.

## Project Structure
coductor/
├── core/                    # Core logic
│   ├── agent.py               # LLM-driven reasoning engine
│   ├── commands/              # CLI commands
│   │   ├── build.py           # Creates a new project from prompt
│   │   ├── scaffold.py
│   │   ├── add_feature.py     # Adds a feature to the project
│   │   ├── todo.py            # Returns todo items or marks them complete
│   │   ├── generate_tests.py  # Generates test cases
│   │   ├── ask.py
│   ├── memory.py              # Project memory/todo state
│   ├── project_analyzer.py    # Parses repo, file trees, summaries
│   ├── file_writer.py         # Writes files safely
│   └── prompts/               # YAML or txt prompt templates
│       ├── scaffold.yml
│       └── add_feature.yml
├── tests/
│   └── test_scaffold.py
├── .coductor/                 # Project-local memory, logs, cache
│   ├── memory.json            # task/todo list
│   ├── logs/                  # chat and operation logs
│   ├── cache/                 # temp file summaries and LLM responses
├── main.py                    # Entry point (Typer app)
├── README.md
├── requirements.txt
├── .gitignore
└── pyproject.toml             # For packaging
