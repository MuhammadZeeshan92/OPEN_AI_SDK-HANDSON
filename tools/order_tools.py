import json
from pathlib import Path
from agents import function_tool

ORDERS_FILE = Path(__file__).parent.parent / "data" / "orders.json"


def load_orders():
    with open(ORDERS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_orders(orders):
    with open(ORDERS_FILE, "w", encoding="utf-8") as file:
        json.dump(orders, file, indent=2)


@function_tool
def create_order(item_names: list[str]) -> str:
    """Create a new restaurant order from available menu items."""
    from tools.menu_tools import load_menu

    menu = load_menu()
    orders = load_orders()

    selected_items = []
    total = 0

    for item_name in item_names:
        for item in menu:
            if item["name"].lower() == item_name.lower():
                if not item["available"]:
                    return f"{item['name']} is currently unavailable."

                selected_items.append(item["name"])
                total += item["price"]
                break
        else:
            return f"{item_name} was not found on the menu."

    if not selected_items:
        return "No items were provided."

    order_number = len(orders) + 1
    order_id = f"ORD{order_number:03d}"

    order = {
        "order_id": order_id,
        "items": selected_items,
        "total": total,
        "status": "Preparing",
    }

    orders.append(order)
    save_orders(orders)

    return json.dumps(order, indent=2)


@function_tool
def get_order_status(order_id: str) -> str:
    """Get the current status of a restaurant order."""
    orders = load_orders()

    for order in orders:
        if order["order_id"].upper() == order_id.upper():
            return (
                f"Order {order['order_id']} is currently "
                f"{order['status']}."
            )

    return f"No order was found with ID {order_id}."