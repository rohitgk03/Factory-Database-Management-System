import mysql.connector as sql
import streamlit as st
import pandas as pd



# Connect to MySQL database

conn = sql.connect(host='localhost', user='root',
                   password='kulkarni03', database='factorydb')
# sql.connect() establishes a connection to the MySQL database with the specified parameters:
# host='localhost' specifies the database server location.
# user='root' specifies the username to connect with.
# password='kulkarni03' specifies the password for the user.
# database='factorydb' specifies the name of the database to connect to.

cursor = conn.cursor()
# conn.cursor() creates a cursor object to interact with the database.



# Custom CSS styles for the page
custom_styles = """
    <style>
        body {
            background-color: #f8f4e6;  /* Ivory */
            font-family: 'Arial', sans-serif;
            color: #2c3e50;  /* Dark Slate Gray */
        }
        .title {
            font-size: 36px;
            color: #3498db;  /* Dodger Blue */
            text-align: center;
            padding: 20px;
            margin-bottom: 30px;
            border-bottom: 2px solid #3498db;  /* Dodger Blue */
        }
        .subtitle {
            font-size: 24px;
            color: #27ae60;  /* White */
            margin-bottom: 20px;
        }
    </style>
"""
# A multi-line string custom_styles is created, containing CSS code that defines styles for the web page:
# body styles the entire page with an ivory background, Arial font, and dark slate gray text color.
# .title styles the title element with a large font size, dodger blue color, centered text, padding, margin, and a bottom border.
# .subtitle styles the subtitle element with a slightly smaller font size and emerald green color.



# Apply custom styles
st.markdown(custom_styles, unsafe_allow_html=True)
# uses Streamlit's markdown function to apply the custom CSS styles to the web page.
# The unsafe_allow_html=True parameter allows HTML and CSS to be rendered.



# Set the title with custom CSS styling using markdown
st.markdown("<h1 class='title'>Welcome to Factory Management Database</h1>",
            unsafe_allow_html=True)

# Add a subtitle with custom styling
st.markdown("<p class='subtitle'>Manage your factory efficiently!</p>",
            unsafe_allow_html=True)





# Example Breakdown
# In the given code example:

# Back End:

# The code connects to a MySQL database using mysql.connector.
# It creates a cursor object to interact with the database.
# Front End:

# Custom CSS styles are defined and applied using st.markdown().
# A title and subtitle are displayed on the web page using st.markdown() with HTML.