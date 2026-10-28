import datetime
import os
import requests
import pytz
import yaml
from smolagents import (
    CodeAgent,
    DuckDuckGoSearchTool,
    HfApiModel,
    OpenAIServerModel,
    load_tool,
    tool,
)
from tools.final_answer import FinalAnswerTool

from Gradio_UI import GradioUI

# Below is an example of a tool that does nothing. Amaze us with your creativity !
@tool
def my_sum_tool(arg1:int, arg2:int)-> int: #it's import to specify the return type
    #Keep this format for the description / args / args description but feel free to modify the tool
    """A tool that adds two integers.
    Args:
        arg1: the first integer
        arg2: the second integer
    """
    return arg1 + arg2

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


final_answer = FinalAnswerTool()


def create_model():
    provider = os.getenv("MODEL_PROVIDER", "ollama").strip().lower()
    temperature = 0.5
    max_tokens = 2096

    if provider == "ollama":
        return OpenAIServerModel(
            model_id=os.getenv("OLLAMA_MODEL", "llama:latest"),
            api_base=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
            api_key="ollama",
            temperature=temperature,
            max_tokens=max_tokens,
        )

    if provider == "hf":
        return HfApiModel(
            max_tokens=max_tokens,
            temperature=temperature,
            model_id=os.getenv("HF_MODEL", "Qwen/Qwen2.5-Coder-32B-Instruct"),
            custom_role_conversions=None,
        )

    raise ValueError("Unsupported MODEL_PROVIDER. Choose 'ollama' or 'hf'.")


model = create_model()


# Import tool from Hub
# image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)
    
agent = CodeAgent(
    model=model,
    tools=[final_answer, my_sum_tool, get_current_time_in_timezone], ## add your tools here (don't remove final answer)
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)


GradioUI(agent).launch()