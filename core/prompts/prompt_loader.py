import yaml
from jinja2 import Template
from pathlib import Path

def load_prompt(name: str) -> Template:
    '''
    Load a prompt from the prompts directory.
    '''
    path = Path(__file__).parent / f"{name}.yml"
    with open(path, "r") as file:
        template = yaml.safe_load(file)
    return Template(template['prompt'])