"""
This is a "fake" function that does not actually exist. The System Prompt of the agent explicitly tells it to submit a
log, so by having a tool called submit_log we know it will call this tool last. When it does, it will format the input
as a python dictionary as described by "input_schema" below. Instead of letting the agent call "submit_log" (it can't,
it does not exist), we will return the input dictionary as the return value of the final function call. This ensures
the output of the agent is always a dictionary formatted the way we want.

See class `Agent` for the implementation of the aforementioned logic.
"""


submit_log_definition = {
    "name": "submit_log",
    "description": "Submit the final food log once an ingredient, serving, and quantity are chosen for every item eaten.",
    "input_schema": {
        "type": "object",
        "properties": {
            "entries": {
                "type": "array",
                "description": "One entry per logged food item",
                "items": {
                    "type": "object",
                    "properties": {
                        "ingredient_id": {"type": "string", "description": "The ingredient ID"},
                        "ingredient_name": {"type": "string", "description": "The ingredient name"},
                        "serving_id": {"type": "string", "description": "The serving ID"},
                        "serving_name": {"type": "string", "description": "The serving name"},
                        "quantity": {"type": "number", "description": "Number of servings eaten"},
                    },
                    "required": ["ingredient_id", "ingredient_name", "serving_id", "serving_name", "quantity"],
                },
            }
        },
        "required": ["entries"],
    },
}