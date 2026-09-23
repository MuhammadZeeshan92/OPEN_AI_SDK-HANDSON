from agents import Agent

from config.model import model
from guardrails.output_guardrail import restaurant_output_guardrail
from tools.order_tools import create_order,get_order_status


order_agent = Agent(
    name="Order Agent",
    instructions="""
You are a restaurant order specialist.

Handle questions about:
- creating new orders
- order status
- order tracking
- existing orders

For creating an order:
- Use create_order.
- Never invent an order ID.
- Never claim an order was created unless the tool confirms it.

For existing orders:
- Use get_order_status.
- Never invent order information.
""",
    model=model,
    tools=[
        create_order,
        get_order_status,
    ],
    output_guardrails=[
        restaurant_output_guardrail
    ],
)