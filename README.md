# Coductor
## Overview
A local CLI-based AI development assistant that manages your project like a technical lead. It scaffolds files, writes summaries, maintains a dynamic todo list, develops a comprehensive test suite, answers questions, and evolves the codebase alongside the developer.

## Motivation
This project was built to rapidly scaffold and organize new projects, so developers can turn an idea into a structured project in seconds. 

## Key Features
- Scaffolding: Generates a folder structure for a users project idea
- Test generation: Suggests unit tests for existing code
- Task management: Creates and updates a running TODO list for the dev

## Project Structure
```
coductor/
├── core/                      # Core logic
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
│   ├── file_writer.py         # Safe overwriting functionality
│   └── prompts/               # YAML or txt prompt templates
│       ├── add_feature.yml
│       ├── generate_name_and_stack.yml
│       ├── plan_project.yml
│       └── prompt_load.py
├── tests/
│   └── test_scaffold.py
├── .coductor/                 # Project-local memory, logs, cache
|   ├── todo.yml               # YAML file to track TODO items
|   ├── memory.yml             # Stores project goals, decisions, summaries
|   ├── history.log            # Optional: Running log of agent-user interactions
│   ├── logs/                  # chat and operation logs
│   └── cache/                 # temp file summaries and LLM responses
├── main.py                    # Entry point (Typer app)
├── README.md
├── requirements.txt
└── .gitignore
```

## Installation and Setup
```bash
# 1. Clone the repo
git clone http://www.github.com/katza18/coductor.git

# 2. Setup a venv and install requirements
cd coductor
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 3. Add your OpenAI API Key
export OPENAI_API_KEY="your API key"

# 4. Build a new project
python main.py build new
```

## Future Plans
- Add skeleton code generation that generates the main functionality of the app,
but leaves the main logic in functions to be filled by the developer.
