from typing import Dict, List, Any

from core.database import list_ingredients, get_ingredient_serving_combinations
from rapidfuzz import process, fuzz


search_ingredient_serving_combinations_definition = {
    "name": "search_ingredient_serving_combinations",
    "description": (
        "Fuzzy search available ingredients by name/description. Returns the best "
        "matching ingredients, each with its available servings (id, name)."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "ingredient_query": {"type": "string", "description": "A string to search for a specific ingredient"},
        },
        "required": ["ingredient_query"],
    },
}


def search_ingredient_serving_combinations(ingredient_query: str) -> List[Dict[str, Any]]:
    """
    Fuzzy match ingredients by name and return each with its available servings.

    Args:
        ingredient_query: A string to search for a specific ingredient (e.g. "milk")
    Returns:
        output: A list of dictionaries, each containing the fields ingredient_id, ingredient_name, serving_id, serving_name
    """
    ingredients = {ingredient.id: ingredient.name for ingredient in list_ingredients()}

    # get top 3 best matching ingredients to ingredient_query
    matched_ingredients = process.extract(
        query=ingredient_query,
        choices=ingredients,
        scorer=fuzz.WRatio,
        limit=3,
    )

    ingredient_ids = [ingredient[2] for ingredient in matched_ingredients]
    combinations = get_ingredient_serving_combinations(ingredient_ids)

    return [combination.model_dump() for combination in combinations]

