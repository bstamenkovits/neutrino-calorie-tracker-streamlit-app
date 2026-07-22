import os
import anthropic
import streamlit as st
from typing import List, Dict, Any

from agent.tools import tool_functions, tool_definitions

ANTHROPIC_API_KEY = st.secrets["ANTHROPIC_API_KEY"]

class Agent:

    SYSTEM_PROMPT = (
        "You log meals. Given a free-text description of what the user ate, use "
        "search_ingredients to find the right ingredient and serving for each item "
        "(search all items in parallel), then call submit_log. For each item pick the "
        "best-matching ingredient, the serving that best fits how it was described, and "
        "the quantity (number of servings). Do not ask questions; make your best guess."
    )

    tools = tool_definitions
    tool_functions = tool_functions

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def _reason(self, description:str) -> List[Dict[str, Any]]:
        messages = [{"role": "user", "content": description}]
        while True:
            response = self.client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                system=self.SYSTEM_PROMPT,
                tools=self.tools,
                messages=messages,
            )

            # Record the assistant's turn (text and/or tool_use blocks).
            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason != "tool_use":
                # Model stopped without submitting a log.
                return []

            # Run every requested tool and feed the results back.
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue

                if block.name == "submit_log":
                    # Final structured answer — enrich with weight/calories and return.
                    return block.input["entries"]

                result = self.tool_functions[block.name](**block.input)
                print(f"{block.name}({block.input}) -> {result}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                })

            messages.append({"role": "user", "content": tool_results})

    def parse_description(self, description:str) -> List[Dict[str, Any]]:
        return self._reason(description)