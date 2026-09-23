import asyncio
import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    Runner,
    set_tracing_disabled,
)

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

menu_agent = Agent(
    name="Menu Agent",
    instructions="""
You are a restaurant menu specialist.

You have no tools for this test.

Simply answer:
"Menu Agent received the request."
""",
    model=model,
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="""
If the user asks anything about the menu,
immediately hand off to Menu Agent.
""",
    model=model,
    handoffs=[menu_agent],
)


async def main():

    result = await Runner.run(
        triage_agent,
        "Tell me about the menu."
    )

    print("FINAL:", result.final_output)
    print("LAST AGENT:", result.last_agent.name)

    print("\nITEMS:")

    for item in result.new_items:
        if hasattr(item, "raw_item"):
            print(type(item.raw_item).__name__)
            print(item.raw_item)


if __name__ == "__main__":
    asyncio.run(main())