from agents import Agent, handoff

from config.model import model
from guardrails.output_guardrail import restaurant_output_guardrail
from tools.menu_tools import (
    search_menu,
    check_item_availability,
    calculate_order_total,
)
from restaurant_agents.order_agent import order_agent


menu_agent = Agent(
    name="Menu Agent",
    handoff_description=(
        "Handles menu questions, food availability, prices, "
        "and multi-item price calculations."
    ),
    instructions="""
You are a restaurant menu specialist.

Handle questions about:
- menu items
- prices
- categories
- availability
- food descriptions
- calculating the total price of multiple items

Use the available tools whenever you need menu information.

For requests involving multiple items:
1. Check the requested items.
2. Check their availability.
3. Calculate the total price when appropriate.

If the customer wants to actually place/create an order,
first verify the requested items and calculate the total,
then hand off to the Order Agent.

Do not create orders yourself.

Do not invent menu information.
""",
    model=model,
    tools=[
        search_menu,
        check_item_availability,
        calculate_order_total,
    ],
    handoffs=[
        handoff(
            agent=order_agent,
            tool_name_override="transfer_to_order_agent",
            tool_description_override=(
                "Transfer to Order Agent when the customer wants "
                "to actually place or create an order."
            ),
        )
    ],
    output_guardrails=[
        restaurant_output_guardrail
    ],
)