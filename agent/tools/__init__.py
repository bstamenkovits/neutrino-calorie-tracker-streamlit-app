from agent.tools.search_ingredient_serving_combinations import search_ingredient_serving_combinations, search_ingredient_serving_combinations_definition
from agent.tools.submit_log import submit_log_definition


tool_definitions = [
    search_ingredient_serving_combinations_definition,
    submit_log_definition,
]


tool_functions = {
    "search_ingredient_serving_combinations": search_ingredient_serving_combinations,
}
