import streamlit as sl
import pandas as pd
import requests

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

# Add Fruityvice advice
sl.header('Fruityvice Fruit Advice!')
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
sl.text(fruityvice_response.json())

