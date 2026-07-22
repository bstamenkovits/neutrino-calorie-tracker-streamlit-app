import streamlit as st
import core.database as db
from agent import Agent
from core.models import FoodLog, AvailableMeal, User

agent = Agent()


st.title("AI Food Logger")
user:User = st.segmented_control("Select a user", options=db.list_users(), format_func=lambda x: x.name)
meal:AvailableMeal = st.segmented_control(label="Select a meal", options=db.list_meals(), format_func=lambda x: x.name)

description = st.text_area(label="Description", placeholder="Enter your message here...", height=200, label_visibility="collapsed")

st.session_state.setdefault("parsed_items", None)

if st.button("Parse Description"):
    if not description:
        st.error("Please enter a description")
        st.stop()

    with st.spinner("Parsing description..."):
        st.session_state.parsed_items = agent.parse_description(description)

# Render the preview and log button whenever we have parsed items, regardless
# of which button triggered the current rerun.
if st.session_state.parsed_items is not None:
    output = st.session_state.parsed_items

    with st.spinner("Generating preview..."):
        preview_items = [
            db.preview_food_log(item['ingredient_id'], item['serving_id'], item['quantity'])
            for item in output
        ]

    st.write("**Preview:**")
    for item in preview_items:
        st.write(f"* {item}")

    if st.button("Log These Items"):
        with st.spinner("Logging items..."):
            for item in output:
                db.insert_food_log(food_log=FoodLog(
                    user_id=user.id,
                    meal_id=meal.id,
                    ingredient_id=item['ingredient_id'],
                    serving_id=item['serving_id'],
                    quantity=item['quantity']
                ))

        st.success("Items logged successfully!")
        st.session_state.parsed_items = None