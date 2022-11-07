import streamlit as sl
import pandas as pd
import requests
import snowflake.connector as sfc
from urllib.error import URLError

# Add Main Title
sl.title('My Parents New Healthy Diner.')

# Add Menu 1
sl.header('Breakfast Favorites')

sl.text('🥣 Omega 3 & Blueberry Oatmeal')
sl.text('🥗 Kail, Spinach & Rocket Smoothy')
sl.text('🐔 Hard-Boiled Free-Range Egg')
sl.text('🥑🍞 Avocado Toast')

# Add Menu 2
sl.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Add list of fruit from external link
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

# Add picklist so users can choose fruit from list and set examples in [ ]. Store fruits selected by user in variable.
fruits_selected = sl.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display full list in table
# sl.dataframe(my_fruit_list)

# Display selected items in table
sl.dataframe(fruits_to_show)

# New section to show Fruitvice API & Add Title for Fruityvice advice!
sl.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = sl.text_input('What fruit would you like information about?')
  if not fruit_choice:
    sl.error("Please select a fruit to get information.")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json()) # Normalize JSON response & show data in dataframe
    sl.dataframe(fruityvice_normalized)
except URLError as e:
  sl.error()
                                         
sl.stop()

# # Add Title for Snowflake and Query Data from Snowflake
my_cnx = sfc.connect(**sl.secrets["snowflake"])
my_cur = my_cnx.cursor()
## my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()") -OLD
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
# my_data_row = my_cur.fetchone() -- Fetches only 1 record
my_data_rows = my_cur.fetchall() # Fetches all records
sl.header("The Fruit Load List Contains:")
sl.dataframe(my_data_rows)

# Add another input box to add fruit!
add_my_fruit = sl.text_input('What fruit would you like to add?','Kiwi')
sl.write('Thanks for adding ',add_my_fruit)
my_cur.execute("INSERT INTO fruit_load_list VALUES ('from sl')")
