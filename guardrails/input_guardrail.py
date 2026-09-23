import os

from dotenv import load_dotenv
from pydantic import BaseModel

from config.model import model

from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    RunConfig,
    ModelSettings,
    TResponseInputItem,
)

from agents.decorators import input_guardrail


load_dotenv()


class RestaurantInputCheck(BaseModel):
    is_restaurant_related: bool
    reasoning: str


guardrail_agent = Agent(
    name="Restaurant Input Checker",
    instructions="""
Determine whether the user's request is related to restaurant operations.

Restaurant-related requests include:
- menu
- food
- prices
- availability
- orders
- order tracking
- payments
- delivery
- restaurant services

If the request is not related to a restaurant, mark it as false.
""",
    output_type=RestaurantInputCheck,
    model=model,
)


@input_guardrail
async def restaurant_input_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:

    result = await Runner.run(
        guardrail_agent,
        input,
        context=ctx.context,
        run_config=RunConfig(
            model_settings=ModelSettings(
                max_tokens=300
            ),
        ),  
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_restaurant_related,
    )