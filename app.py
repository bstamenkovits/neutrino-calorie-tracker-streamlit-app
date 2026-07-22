import streamlit as st
from supabase import create_client, Client

st.title("Hello World")
st.write("This is a test")

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ADMIN_KEY"]



db = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


def list_ingredients():
    response = db.schema("app").table("ingredients").select("id, name").execute()
    return response.data


st.write(list_ingredients())