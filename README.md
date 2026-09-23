# 🍽️ Restaurant Operations AI

A multi-agent restaurant assistant built with the **OpenAI Agents SDK**, **OpenRouter**, **Python**, and **Streamlit**.

The system can answer restaurant-related questions, search the menu, check item availability, calculate order totals, create orders, check order status, route requests between specialized agents, maintain conversation history, and protect the application using input and output guardrails.

---

## 🚀 Features

- 🤖 Multi-agent restaurant assistant
- 🔀 Agent-to-agent handoffs
- 🍔 Menu search
- ✅ Menu item availability checking
- 💰 Multi-item price calculation
- 🛒 Order creation
- 📦 Order status tracking
- 🛡️ Input guardrails
- 🔒 Output guardrails
- 🧠 Conversation memory using `SQLiteSession`
- 🧰 Multiple custom function tools
- 🌐 OpenRouter API integration
- 💬 Streamlit chat interface
- 🔄 Persistent async event loop for Streamlit
- 📁 JSON-based menu and order data

---

## 🏗️ Architecture

The application follows a multi-agent architecture:

```text
                         USER
                           │
                           ▼
                  ┌─────────────────┐
                  │  Input Guardrail │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Triage Agent   │
                  └────────┬────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
      ┌───────────────┐         ┌───────────────┐
      │  Menu Agent   │         │  Order Agent  │
      └───────┬───────┘         └───────┬───────┘
              │                         │
              ▼                         ▼
        Menu Tools                Order Tools
              │                         │
              └────────────┬────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Output Guardrail│
                  └────────┬────────┘
                           │
                           ▼
                       RESPONSE
```

---

## 🤖 Agents

### 1. Triage Agent

The Triage Agent is the main entry point.

Its job is to understand the user's request and route it to the correct specialized agent.

It handles routing for:

- Menu questions
- Food questions
- Prices
- Categories
- Availability
- Multiple-item checks
- Price calculations
- Order creation requests
- Existing order status
- Order tracking

The Triage Agent does not handle specialist requests itself. It hands them off to the appropriate agent.

### 2. Menu Agent

The Menu Agent handles restaurant menu-related requests.

It can:

- Search menu items
- Check availability
- Provide prices
- Provide categories
- Provide food descriptions
- Calculate totals for multiple items
- Verify items before an order is created

The Menu Agent can hand off order creation requests to the Order Agent.

It does not create orders itself.

### 3. Order Agent

The Order Agent handles actual restaurant orders.

It can:

- Create new orders
- Check existing order status
- Track existing orders

It uses the order tools to interact with the order data.

---

## 🔀 Agent Handoffs

Agents communicate through handoffs.

For example, when a user asks:

> I want a Zinger Burger and Regular Fries. Please place the order for me.

The flow is:

```
Triage Agent
      ↓
Menu Agent
      ↓
Check item availability
      ↓
Calculate total
      ↓
Order Agent
      ↓
Create order
```

The final response can contain the generated order ID, total price, and order status.

---

## 🧰 Tools

The project uses custom tools created with the OpenAI Agents SDK `function_tool`.

### Menu Tools

Located in:

```
tools/menu_tools.py
```

#### `search_menu`

Searches the restaurant menu by:

- Item name
- Category

Example:

> Search for burgers

#### `check_item_availability`

Checks whether a specific menu item is available.

Example:

> Is Chicken Burger available?

#### `calculate_order_total`

Calculates the total price of multiple available menu items.

Example:

> Calculate the price of a Zinger Burger and Regular Fries.

### Order Tools

Located in:

```
tools/order_tools.py
```

#### `create_order`

Creates a new order using available menu items.

It:

- Loads the menu
- Validates requested items
- Checks availability
- Calculates the total
- Generates an order ID
- Saves the order
- Returns the created order

Example:

> I want a Chicken Burger and Regular Fries.

#### `get_order_status`

Checks the current status of an existing order.

Example:

> What is the status of order ORD001?

---

## 🛡️ Guardrails

The application implements both input and output guardrails.

### Input Guardrail

Located in:

```
guardrails/input_guardrail.py
```

The input guardrail checks whether the user's request is related to the restaurant.

For example, a restaurant request such as:

> Is Chicken Burger available?

is allowed.

An unrelated request is rejected with:

> Sorry, I can only help with restaurant-related questions.

### Output Guardrail

Located in:

```
guardrails/output_guardrail.py
```

The output guardrail checks the agent's response for sensitive information such as:

- API keys
- Passwords
- Authentication tokens
- Internal prompts
- Private database information
- Secret credentials

If the response violates the output guardrail, the application returns:

> Sorry, I cannot provide that information.

---

## 🧠 Conversation Memory

The Streamlit application supports multi-turn conversations using:

```
SQLiteSession
```

This allows the agent to understand follow-up messages based on previous messages.

For example:

**User:**
> Is Chicken Burger available?

**Assistant:**
> The Chicken Burger is available...

**User:**
> yes pls order a chicken burger for me

The second message can be understood in the context of the previous conversation.

The session is created with:

```python
SQLiteSession("restaurant_chat")
```

and passed to:

```python
Runner.run()
```

This allows the Agents SDK to maintain the conversation history between turns.

---

## ⚡ Async Event Loop Handling

The Streamlit frontend uses a persistent:

```python
asyncio.Runner()
```

instead of creating a new event loop with:

```python
asyncio.run()
```

for every message.

This is important because the project uses an asynchronous OpenRouter client through:

```python
AsyncOpenAI
```

The persistent runner allows multiple chat requests to reuse the same event loop.

The runner is stored in Streamlit session state:

```python
if "async_runner" not in st.session_state:
    st.session_state.async_runner = asyncio.Runner()
```

The agent is then executed with:

```python
result = st.session_state.async_runner.run(
    run_agent(user_message)
)
```

---

## 🌐 OpenRouter Integration

The project uses OpenRouter instead of the direct OpenAI API.

The OpenRouter client is configured in:

```
config/model.py
```

The project uses:

```python
AsyncOpenAI
```

with the OpenRouter base URL:

```
https://openrouter.ai/api/v1
```

The Agents SDK uses:

```python
OpenAIChatCompletionsModel
```

to communicate with the selected OpenRouter model.

---

## 📁 Project Structure

```
restaurant-operations-ai/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
│
├── config/
│   ├── __init__.py
│   └── model.py
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── streamlit_app.py
│
├── restaurant_agents/
│   ├── __init__.py
│   ├── restaurant_agent.py
│   ├── menu_agent.py
│   ├── order_agent.py
│   └── triage_agent.py
│
├── tools/
│   ├── __init__.py
│   ├── menu_tools.py
│   └── order_tools.py
│
├── guardrails/
│   ├── __init__.py
│   ├── input_guardrail.py
│   └── output_guardrail.py
│
├── data/
│   ├── menu.json
│   └── orders.json
│
└── tests/
    └── __init__.py
```

---

## 📄 Data

The project uses JSON files for simple restaurant data storage.

### `data/menu.json`

Contains restaurant menu items with information such as:

```json
{
    "id": "M002",
    "name": "Chicken Burger",
    "category": "Burgers",
    "price": 350,
    "available": true,
    "description": "Grilled chicken burger with lettuce and mayo."
}
```

### `data/orders.json`

Stores created restaurant orders.

Example:

```json
{
    "order_id": "ORD001",
    "items": [
        "Zinger Burger",
        "Regular Fries"
    ],
    "total": 630,
    "status": "Preparing"
}
```

---

## ⚙️ Requirements

- Python 3.12
- OpenRouter API key
- OpenAI Agents SDK
- Streamlit
- python-dotenv

---

## 📦 Installation

Clone the repository:

```bash
git clone <your-repository-url>
```

Move into the project:

```bash
cd restaurant-operations-ai
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_actual_openrouter_api_key
OPENROUTER_MODEL=openai/gpt-4o-mini
```

Do not commit the `.env` file to GitHub.

The `.env` file should be included in `.gitignore`.

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app/streamlit_app.py
```

The application will open in the browser at:

```
http://localhost:8501
```

---

## 💬 Example Usage

### Menu Search

> What burgers are available?

The request is routed to the Menu Agent, which uses the menu tools to find the relevant items.

### Check Availability

> Is Chicken Burger available?

The Menu Agent uses:

```
check_item_availability
```

### Calculate Multiple Items

> How much would a Zinger Burger and Regular Fries cost?

The Menu Agent can check the items and use:

```
calculate_order_total
```

### Place an Order

> I want a Zinger Burger and Regular Fries. Please place the order for me.

The complete flow is:

```
Triage Agent
    ↓
Menu Agent
    ↓
check_item_availability
    ↓
calculate_order_total
    ↓
Order Agent
    ↓
create_order
```

Example response:

```
Your order for a Zinger Burger and Regular Fries has been successfully placed!

Order ID: ORD001
Total: 630
Status: Preparing
```

### Track an Order

> I want to know the status of order ORD001.

The flow is:

```
Triage Agent
    ↓
Order Agent
    ↓
get_order_status
```

Example response:

```
Order ORD001 is currently Preparing.
```

### Multi-Turn Conversation

The application also supports contextual follow-up messages.

Example:

**User:**
> Is Chicken Burger available?

**Assistant:**
> The Chicken Burger is available!

**User:**
> yes pls order a chicken burger for me

The conversation session allows the agent to understand that the second message refers to the Chicken Burger discussed previously.

---

## 🔄 End-to-End Example

A complete order request can travel through multiple agents and tools:

```
User
 │
 ▼
Input Guardrail
 │
 ▼
Triage Agent
 │
 ├── transfer_to_menu_agent
 │
 ▼
Menu Agent
 │
 ├── check_item_availability
 │
 ├── check_item_availability
 │
 ├── calculate_order_total
 │
 └── transfer_to_order_agent
 │
 ▼
Order Agent
 │
 └── create_order
 │
 ▼
Output Guardrail
 │
 ▼
Final Response
```

This demonstrates a real multi-agent, multi-tool workflow where different agents are responsible for different parts of the task.

---

## 📋 Assignment Requirements

This project implements the required Agents SDK concepts:

| Requirement | Implementation |
|---|---|
| Agent with system prompt | Triage, Menu, and Order Agents |
| Custom tools | Menu and Order tools |
| Multiple tools | Menu and Order tool sets |
| Multiple specialized agents | Triage, Menu, and Order Agents |
| Agent handoffs | Triage → Menu / Order, Menu → Order |
| Input guardrail | Restaurant input validation |
| Output guardrail | Sensitive information protection |
| OpenRouter integration | OpenAIChatCompletionsModel |
| Multi-tool agent | Menu and Order workflows |
| End-to-end task | Menu verification → calculation → order creation |
| Conversation memory | SQLiteSession |
| Frontend | Streamlit |

---

## 🛠️ Technologies Used

- Python
- OpenAI Agents SDK
- OpenRouter
- AsyncOpenAI
- OpenAIChatCompletionsModel
- Streamlit
- python-dotenv
- SQLiteSession
- JSON

---

## 📌 Main Project Goal

The purpose of this project is to demonstrate a complete restaurant operations assistant using the OpenAI Agents SDK.

It demonstrates:

- Agent creation
- System instructions
- Custom function tools
- Multiple tools
- Specialized agents
- Agent handoffs
- Input guardrails
- Output guardrails
- OpenRouter model integration
- Multi-turn conversation
- End-to-end agent workflows
- Streamlit frontend integration