import streamlit as st
import core.database as db
import datetime
import time

from core.models import FoodLog, Combination, AvailableIngredient, User, AvailableMeal

st.title("Overview")

user:User = st.selectbox("Select a user", options=db.list_users(), format_func=lambda x: x.name)
date = datetime.date.today()


def on_ingredient_change(food_log_id, ingredient_dropdown_id):
    new_ingredient_id = st.session_state[ingredient_dropdown_id].id
    new_ingredient_id = str(new_ingredient_id)

    db.update_food_log_column(
        food_log_id=food_log_id,
        column_name="ingredient_id",
        value=new_ingredient_id,
    )

def on_combination_change(food_log_id, combination_dropdown_id):
    new_serving_id = st.session_state[combination_dropdown_id].serving_id
    new_serving_id = str(new_serving_id)

    db.update_food_log_column(
        food_log_id=food_log_id,
        column_name="serving_id",
        value=new_serving_id,
    )


meals:list[AvailableMeal] = db.list_meals()


for meal in meals:
    meal_data = db.list_food_summary(
        user_id=user.id,
        consumed_on=date,
        meal_name=meal.name
    )
    total_calories = sum([food.total_calories_kcal for food in meal_data])
    title = f"**{meal.name}: {total_calories:.0f} kcal**"
    st.write(title)
    with st.expander("details", key=f'expander__food_log__{meal.name}', on_change="rerun"):
        for food_item in meal_data:
            available_ingredients = db.list_ingredients()

            active_ingredient_idx = next(
                (i for i, ingredient in enumerate(available_ingredients)
                 if ingredient.id == food_item.ingredient_id)
            , 0)

            ingredient_key = f'food_log__{meal.name}__{food_item.id}__ingredient'
            ingredient:AvailableIngredient = st.selectbox(
                label="Select an ingredient",
                options=db.list_ingredients(),
                format_func=lambda x: x.name,
                index=active_ingredient_idx,
                label_visibility="collapsed",
                key=ingredient_key,
                on_change=on_ingredient_change,
                args=(food_item.id, ingredient_key),
            )

            combination_key = f'food_log__{meal.name}__{food_item.id}__combination'
            combination:Combination = st.selectbox(
                label="Select a serving type",
                options=db.get_ingredient_serving_combinations([ingredient.id]),
                format_func=lambda x: x.serving_name,
                label_visibility="collapsed",
                key=combination_key,
                on_change=on_combination_change,
                args=(food_item.id, combination_key),
            )

            quantity = st.number_input(
                label="Enter quantity",
                value=float(food_item.quantity),
                label_visibility="collapsed",
                min_value=0.,
                step=1.,
                format="%f",
                key=f'food_log__{meal.name}__{food_item.id}__quantity',
            )

            st.write(f"**{food_item.total_calories_kcal:.0f} kcal** ({food_item.total_weight_g:.0f} g)")

            st.divider()

        if st.button("Add Food Item", key=f'button__food_log__add_item__{meal.name}'):
            db.insert_food_log(food_log=FoodLog(
                user_id=user.id,
                meal_id=meal.id,
                ingredient_id=available_ingredients[0].id,
                serving_id=db.get_ingredient_serving_combinations([available_ingredients[0].id])[0].serving_id,
                quantity=1,
            ))
            st.success("New Food Item Added")
            time.sleep(1)
            st.rerun()

