# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
requests

# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: CUSTOMIZE YOUR SMOOTHIE :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom smoothie.""")

name_on_order = st.text_input('name on smoothie:')
st.write('the name on your smoothie will be', name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections =5 
)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
                        values ('""" + ingredients_string.strip() + """', '""" + name_on_order + """')"""

    st.write(my_insert_stmt)

    time_to_insert = st.button('submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
  import requests
  smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
  st.text(smoothiefroot_response)

