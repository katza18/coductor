'''
Purpose: Central LLM-powered reasoning engine.

Responsibilities:
- Send contextual prompts to the LLM (e.g., OpenAI API)
- Accept system + user inputs, return structured responses
- Handle retries, model selection, formatting

Spec:
- run_prompt(prompt: str, context: dict) -> str
- load_prompt_template(name: str) -> str
'''
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pathlib import Path
import tiktoken
import json
from rich.console import Console

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
PROMPTS_DIR = Path(__file__).parent / "prompts"
DEFAULT_MODEL = "gpt-4o-mini"
MAX_TOKENS = 128000  # adjust depending on the model
SESSION_HISTORY_FILE = Path(__file__).parent.parent / ".coductor" / "session.json"
console = Console()


# def load_prompt(name: str, context:dict) -> str:
#     """
#     Load a prompt template from the prompts directory.
#     """
#     with open(PROMPTS_DIR / f"{name}.yml", "r") as file:
#         template = yaml.safe_load(file)

#     system = template.get("system", "")
#     user = template.get("user", "").format(**context)
#     return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def load_history() -> list[dict]:
    '''
    Load the conversation history from a file.
    '''
    if not SESSION_HISTORY_FILE.exists():
        # Create the session history file if it doesn't exist
        SESSION_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SESSION_HISTORY_FILE, "w") as file:
            json.dump([], file)
        return []
    with open(SESSION_HISTORY_FILE, "r") as file:
        return json.load(file)


def save_history(session_history: list[dict]):
    '''
    Save the conversation history.
    '''
    with open(SESSION_HISTORY_FILE, "w") as file:
        json.dump(session_history, file, indent=4)


async def send_prompt(prompt: str, model: str = DEFAULT_MODEL) -> dict:
    """
    Send a prompt to the LLM and return the response.
    """
    # Get the current session history
    session_history = load_history()
    session_history.append({"role": "user", "content": prompt})
    
    try:
        client = AsyncOpenAI(api_key=API_KEY)
        # Initialize the OpenAI client
        response = await client.chat.completions.create(
            model=model,
            messages=session_history,
            stream=False,
            temperature=0.7,
        )

        # Check if the context is too large
        prompt_tokens = count_chat_tokens(session_history, model=DEFAULT_MODEL)
        expected_response_tokens = 2048  # Estimate based on desired response length

        if prompt_tokens + expected_response_tokens > MAX_TOKENS:
            raise ValueError("Prompt too long! Please shorten input or reduce memory.")

        
        # Can be added later for streaming ai output
        # if stream:
        #     for chunk in response:
        #         if "choices" in chunk and chunk.choices[0].delta.get("content"):
        #             yield chunk.choices[0].delta.content
        
        # Save messages to session history and return the response
        session_history.append({"role": "assistant", "content": response.choices[0].message.content})
        save_history(session_history)
        return json.loads(response.choices[0].message.content)
    
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return {}



def count_tokens(text: str, model: str = DEFAULT_MODEL) -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def count_chat_tokens(messages: list[dict], model: str = DEFAULT_MODEL) -> int:
    encoding = tiktoken.encoding_for_model(model)
    tokens_per_message = 3  # system, user, assistant structure
    tokens_per_name = 1     # if 'name' is used in the message

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3         # Every reply has priming tokens
    return num_tokens