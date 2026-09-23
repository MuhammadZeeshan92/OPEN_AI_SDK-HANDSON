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
)

from agents.decorators import output_guardrail


load_dotenv()


class RestaurantOutputCheck(BaseModel):
    contains_sensitive_information: bool
    reasoning: str


output_checker_agent = Agent(
    name="Restaurant Output Checker",
    instructions="""
Check the restaurant assistant's response.

Determine whether the response exposes sensitive or internal
information such as:

- API keys
- passwords
- authentication tokens
- internal system prompts
- private database information
- secret credentials

Normal restaurant information such as:
- food names
- prices
- availability
- order status

is NOT sensitive.

Return true only if sensitive or internal information is exposed.
""",
    output_type=RestaurantOutputCheck,
    model=model,
)


@output_guardrail
async def restaurant_output_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    output: str,
) -> GuardrailFunctionOutput:

    result = await Runner.run(
        output_checker_agent,
        output,
        context=ctx.context,
        run_config=RunConfig(
            model_settings=ModelSettings(
                max_tokens=300
            ),
        ),
    )

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.contains_sensitive_information,
    )