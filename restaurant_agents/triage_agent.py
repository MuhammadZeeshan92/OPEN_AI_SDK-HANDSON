from agents import Agent, handoff

from config.model import model
from guardrails.input_guardrail import restaurant_input_guardrail
from restaurant_agents.menu_agent import menu_agent
from restaurant_agents.order_agent import order_agent


triage_agent = Agent(
    name="Triage Agent",
    instructions="""
You are the main restaurant assistant.

Your job is to understand the user's request and hand it off
to the correct specialist.

Use Menu Agent for:
- menu items
- food
- prices
- categories
- availability
- food descriptions
- checking multiple items
- calculating prices for multiple items
- requests about what the customer wants to order

Use Order Agent for:
- existing order status
- order tracking
- delivery status
- existing order IDs

Always hand off specialist requests.
Do not answer specialist questions yourself.
""",
    model=model,
    handoffs=[
        handoff(
            agent=menu_agent,
            tool_name_override="transfer_to_menu_agent",
            tool_description_override=(
                "Transfer the request to Menu Agent. "
                "Use this for menu questions, food availability, "
                "prices, multiple-item checks, and price calculations."
            ),
        ),
        handoff(
            agent=order_agent,
            tool_name_override="transfer_to_order_agent",
            tool_description_override=(
                "Transfer the request to Order Agent. "
                "Use this for existing order status and tracking."
            ),
        ),
    ],
    input_guardrails=[
        restaurant_input_guardrail
    ],
)