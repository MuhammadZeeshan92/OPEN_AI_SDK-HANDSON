import asyncio

from agents import (
    Runner,
    RunConfig,
    ModelSettings,
)
from agents.exceptions import InputGuardrailTripwireTriggered
from restaurant_agents.triage_agent import triage_agent

from agents.exceptions import (
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
)


async def main():

        try:
            result = await Runner.run(
            triage_agent,
            "I want to know the status of order ORD001.",
            run_config=RunConfig(
                model_settings=ModelSettings(
                    max_tokens=1000
                )
            )
        )

            print("\nRestaurant AI:")
            print(result.final_output)

            print("\nTool calls:")

            for item in result.new_items:
                if hasattr(item, "raw_item"):
                    raw_item = item.raw_item

                    print("\nType:", type(raw_item).__name__)
                    print("Data:", raw_item)

        except InputGuardrailTripwireTriggered:
            print("\nRestaurant AI:")
            print("Sorry, I can only help with restaurant-related questions.")

        except OutputGuardrailTripwireTriggered:
            print("\nRestaurant AI:")
            print("Sorry, I cannot provide that information.")


if __name__ == "__main__":
    asyncio.run(main())