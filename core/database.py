from typing import Any

import streamlit as st
from supabase import create_client, Client

from core.models import AvailableMeal, User, AvailableIngredient, FoodLog, Combination, FoodSummary
from core.util import ttl_cache


SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ADMIN_KEY"]


db:Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


def new_user(email, password):
    db.auth.sign_up(dict(
        email=email,
        password=password
    ))


def list_users() -> list[User]:
    # return db.schema("auth").table("users").select('*').execute()
    user_data = db.auth.admin.list_users()
    return [User(id=user.id, name=user.email) for user in user_data]


@ttl_cache(minutes=10)
def list_meals() -> list[AvailableMeal]:
    response = db.schema("app").table("meals").select("*").execute()
    return [AvailableMeal(**meal) for meal in response.data]




@ttl_cache(minutes=10)
def list_ingredients() -> list[AvailableIngredient]:
    response = db.schema("app").table("ingredients").select("id, name, calories_kcal").execute()
    return [AvailableIngredient(**ingredient) for ingredient in response.data]


def get_ingredient_serving_combinations(ingredient_ids: list[str]) -> list[Combination]:
    response =  (
        db.schema("app").table("ingredient_serving_combinations")
        .select("*")
        .in_("ingredient_id", ingredient_ids)
    ).execute()
    return [Combination(**row) for row in response.data]




def insert_food_log(food_log:FoodLog):
    food_log_data = food_log.model_dump(mode='json')
    db.schema("app").table("food_logs").insert(food_log_data).execute()


def update_food_log(food_log:FoodLog):
    food_log_data = food_log.model_dump(mode='json')
    query = db.schema("app").table("food_logs").update(food_log_data).eq("id", food_log.id)
    response = query.execute()
    return response.data

def update_food_log_column(food_log_id:str, column_name:str, value:Any):
    query = db.schema("app").table("food_logs").update({column_name:value}).eq("id", food_log_id)
    response = query.execute()
    return response.data



def list_food_logs(
    user_id: str | None = None,
    consumed_on=None,
) -> list[FoodLog]:
    query = db.schema("app").table("food_logs").select("*")

    if user_id:
        query = query.filter(column="user_id", operator="eq", criteria=user_id)
    if consumed_on:
        query = query.filter(column="consumed_on", operator="eq", criteria=consumed_on)

    response = query.execute()
    return [FoodLog(**food_log) for food_log in response.data]


def list_food_summary(
    user_id: str | None = None,
    consumed_on=None,
    meal_name=None
) -> list[FoodSummary]:
    query = db.schema("app").table("food_summary").select("*")

    if user_id:
        query = query.filter(column="user_id", operator="eq", criteria=user_id)
    if consumed_on:
        query = query.filter(column="date", operator="eq", criteria=consumed_on)
    if meal_name:
        query = query.filter(column="meal_name", operator="eq", criteria=meal_name)

    response = query.execute()
    return [FoodSummary(**food_summary) for food_summary in response.data]






