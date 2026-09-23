import os

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel, set_tracing_disabled

load_dotenv()

set_tracing_disabled(True)

client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

model = OpenAIChatCompletionsModel(
    model=os.getenv("OPENROUTER_MODEL"),
    openai_client=client,
)