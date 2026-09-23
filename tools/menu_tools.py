import json
from pathlib import Path

from agents import function_tool


MENU_FILE = Path(__file__).parent.parent / "data" / "menu.json"


def load_menu():
    with open(MENU_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


@function_tool
def search_menu(query: str) -> str:
    """Search the restaurant menu by item name or category."""

    menu = load_menu()

    query = query.lower()

    results = [
        item
        for item in menu
        if query in item["name"].lower()
        or query in item["category"].lower()
    ]

    if not results:
        return "No matching menu items were found."

    return json.dumps(results, indent=2)

@function_tool
def check_item_availability(item_name: str) -> str:
    """Check whether a menu item is currently available."""

    menu = load_menu()

    for item in menu:
        if item["name"].lower() == item_name.lower():
            if item["available"]:
                return f"{item['name']} is currently available."
            else:
                return f"{item['name']} is currently unavailable."

    return f"{item_name} was not found on the menu."


@function_tool
def calculate_order_total(item_names: list[str]) -> str:
    """Calculate the total price of multiple menu items."""
    menu = load_menu()

    total = 0
    selected_items = []

    for item_name in item_names:
        for item in menu:
            if item["name"].lower() == item_name.lower():
                if item["available"]:
                    total += item["price"]
                    selected_items.append(item["name"])
                break

    if not selected_items:
        return "No available items were found."

    return f"Items: {', '.join(selected_items)}\nTotal: {total}"