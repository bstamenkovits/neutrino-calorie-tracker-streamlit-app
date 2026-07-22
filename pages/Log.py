import streamlit as st
import core.database as db
from core.models.user import User
from core.models.food_log import FoodLog
import datetime

st.title("Food Logging")


user = st.selectbox("Select a user", options=db.list_users(), format_func=lambda x: x.name)
date = datetime.date.today()

food_logs = db.list_food_logs(
    user_id=user.id,
    consumed_on=date
)

st.write(food_logs)


# st.write(user)

meal = st.selectbox("Select a meal", options=db.list_meals(), format_func=lambda x: x.name)
# st.write(meal)

ingredient = st.selectbox("Select an ingredient", options=db.list_ingredients(), format_func=lambda x: x.name)
# st.write(ingredient)

combination = st.selectbox(
    label="Select a serving type",
    options=db.get_ingredient_serving_combinations([ingredient.id]),
    format_func=lambda x: x.serving_name
)
# st.write(serving_type)

quantity = st.number_input("Enter quantity")


if st.button("Submit"):
    food_log = FoodLog(
        user_id=user.id,
        meal_id=meal.id,
        ingredient_id=combination.ingredient_id,
        serving_id=combination.serving_id,
        quantity=quantity,
    )
    db.insert_food_log(food_log)
    st.rerun()