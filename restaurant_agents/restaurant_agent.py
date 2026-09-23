import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

from agents import Agent,OpenAIChatCompletionsModel, OpenAIProvider, set_tracing_disabled

from tools.menu_tools import search_menu
from tools.menu_tools import search_menu, check_item_availability


load_dotenv()

set_tracing_disabled(True)

openrouter_client = AsyncOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

model = OpenAIChatCompletionsModel(
    model=os.getenv("OPENROUTER_MODEL"),
    openai_client=openrouter_client,
)

restaurant_agent = Agent(
    name="Restaurant Assistant",
    instructions="""
You are a restaurant operations assistant.

You help customers with restaurant menu questions.

When the user asks about menu items, prices, categories,
availability, or food descriptions, use the available tools.

Do not invent menu information.

Be concise and helpful.
""",
    model=model,
    tools=[
        search_menu,
        check_item_availability,
    ],
)