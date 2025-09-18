import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title('My parents new healthy diet')
st.write("Choose the fruits you want in your custom smoothie.")

name_on_order = st.text_input('Name on smoothie:')
st.write('The name on your smoothie will be', name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit options from Snowflake and convert to list
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
fruit_options = my_dataframe.collect()
fruit_list = [row['FRUIT_NAME'] for row in fruit_options]

# Multi-select input
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_list,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)

    my_insert_stmt = f"""
        insert into smoothies.public.orders(ingredients, name_on_order)
        values ('{ingredients_string}', '{name_on_order}')
    """

    st.write(my_insert_stmt)

    if st.button('Submit order'):
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
