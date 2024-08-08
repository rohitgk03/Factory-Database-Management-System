import mysql.connector as sql
import streamlit as st
import pandas as pd

conn = sql.connect(host='localhost', user='root',
                   password='kulkarni03', database='factorydb')

cursor = conn.cursor()


def validate_user(username, password):
    cursor.execute(
        "SELECT * FROM users WHERE ContactNo = '{username}' AND pass_word = '{password}'")
    result = cursor.fetchall()
    return len(result) > 0


def create_new_user(username, password, phone_number):
    query = "INSERT INTO users (CustomerName, pass_word, ContactNo) VALUES (%s, %s, %s)"
    try:
        cursor.execute(query, (username, password, phone_number))
        conn.commit()
        st.success("User insertion successful!")
    except sql.Error as err:
        st.error(f"User insertion unsuccessful: {err}")


def signup():
    st.title('SignUp Page')
    if 'signup' not in st.session_state:
        st.session_state.signup = False
    if not st.session_state.signup:
        new_username = st.text_input("Enter New Username:")
        new_password = st.text_input(
            "Enter New Password:", type="password")
        new_phone_number = st.text_input("Enter Phone Number:")

        signup_button = st.button("Sign Up")
        if signup_button:
            if not validate_user(new_username, new_password):
                create_new_user(
                    new_username, new_password, new_phone_number)
                # st.success("Signed up successfully!")
                return "signup", None
            else:
                st.warning(
                    "Username already exists. Please choose a different username.")

    return None, None


signup()
