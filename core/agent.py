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
import openai
from pathlib import Path
import tiktoken
import yaml

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
PROMPTS_DIR = Path(__file__).parent / "prompts"
DEFAULT_MODEL = "gpt-4o-mini"
MAX_TOKENS = 128000  # adjust depending on the model

def load_prompt(name: str, context:dict) -> str:
    """
    Load a prompt template from the prompts directory.
    """
    with open(PROMPTS_DIR / f"{name}.yml", "r") as file:
        template = yaml.safe_load(file)

    system = template.get("system", "")
    user = template.get("user", "").format(**context)
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]

def send_prompt(prompt: str, context: dict, stream: bool, model: str = DEFAULT_MODEL):
    """
    Send a prompt to the LLM and return the response.
    """

    # Load the prompt from a template file
    messages = load_prompt(prompt, context)

    # Initialize the OpenAI client
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        stream=stream,
        temperature=0.7,
    )

    # Check if the context is too large
    prompt_tokens = count_chat_tokens(messages, model=DEFAULT_MODEL)
    expected_response_tokens = 2048  # Estimate based on desired response length

    if prompt_tokens + expected_response_tokens > MAX_TOKENS:
        raise ValueError("Prompt too long! Please shorten input or reduce memory.")

    # Extract the content from the response
    if stream:
        for chunk in response:
            if "choices" in chunk and chunk.choices[0].delta.get("content"):
                yield chunk.choices[0].delta.content
    else:
        return response.choices[0].message.content

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
