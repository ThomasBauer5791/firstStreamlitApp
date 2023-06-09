#main python file
import streamlit
import pandas
import requests   # $ python -m pip install requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('First Test App')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Display the table on the page.
streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the selected lines
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data (input_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + input_fruit_choice)
    # streamlit.text(fruityvice_response.json())
    # displaying the JSON as a table
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
    
# new section to display response of Fruityvice API (http  requests)
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  # streamlit.write('The user entered ', fruit_choice)
  if not fruit_choice:
    streamlit.error("Please enter a fruit to get information")
  else:
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
  streamlit.error()

streamlit.header("The fruit load list contains:")
# Snowflake related functions:
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from demo_db.public.fruit_load_list")
        return my_cur.fetchall() # fetchone()
# add button:
if streamlit.button ('get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into demo_db.public.fruit_load_list values ('" + add_my_fruit + "')") 
        return "Thanks for adding: " + add_my_fruit

add_my_fruit = streamlit.text_input('Which fruit would you like to add?')
if streamlit.button ('Add a fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    streamlit.text(insert_row_snowflake(add_my_fruit))
    my_cnx.close()

streamlit.stop()
# write to Snowflake table
# check_DB = my_cur.execute("SELECT CURRENT_ROLE(), current_database(), current_warehouse()")
# write(check_DB)
