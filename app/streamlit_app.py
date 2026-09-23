import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import asyncio
import streamlit as st

from agents import Runner, RunConfig, ModelSettings, SQLiteSession
from agents.exceptions import (
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
)

from restaurant_agents.triage_agent import triage_agent


st.set_page_config(
    page_title="Restaurant AI",
    page_icon="🍽️",
    layout="centered",
)


st.title("Restaurant AI")
st.caption("Ask about the menu, place an order, or track an existing order.")


if "messages" not in st.session_state:
    st.session_state.messages = []


if "async_runner" not in st.session_state:
    st.session_state.async_runner = asyncio.Runner()


if "session" not in st.session_state:
    st.session_state.session = SQLiteSession("restaurant_chat")


async def run_agent(user_message: str):
    result = await Runner.run(
        triage_agent,
        user_message,
        session=st.session_state.session,
        run_config=RunConfig(
            model_settings=ModelSettings(
                max_tokens=1000
            )
        ),
    )

    return result


user_message = st.chat_input(
    "Ask something about the restaurant..."
)


if user_message:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        with st.spinner("Restaurant AI is thinking..."):

            try:
                result = st.session_state.async_runner.run(
                    run_agent(user_message)
                )

                response = result.final_output

                with st.expander("Agent & Tool Calls"):
                    for item in result.new_items:
                        if hasattr(item, "raw_item"):
                            raw_item = item.raw_item

                            st.write(
                                "Type:",
                                type(raw_item).__name__
                            )

                            st.write(
                                "Data:",
                                raw_item
                            )

            except InputGuardrailTripwireTriggered:
                response = (
                    "Sorry, I can only help with "
                    "restaurant-related questions."
                )

            except OutputGuardrailTripwireTriggered:
                response = (
                    "Sorry, I cannot provide that information."
                )

            except Exception as error:
                response = (
                    "Something went wrong while processing "
                    "your request."
                )

                st.error(str(error))

        st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )