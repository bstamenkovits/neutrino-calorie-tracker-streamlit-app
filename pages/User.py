import streamlit as st
import core.database as db



email = st.text_input("Email", value="NewUser@mail.com")
password = st.text_input("Password", value="newuser")

if st.button("Create User"):
    db.new_user(email, password)

st.write(db.list_users())