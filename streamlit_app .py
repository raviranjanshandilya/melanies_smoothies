# Import python packages

# Write directly to the app
import streamlit as st
st.title("Custom Smoothie Order Form :balloon:")
st.write(
    """Enjoy your Smoothie!!
    """
)

from snowflake.snowpark.functions import col


name_on_order = st.text_input("Name on Smoothie")
st.write("The name of the Smoothie is", name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect('Choose up to 5 ingredient:'
                               , my_dataframe
                               )
if ingredients_list:
    ingredients_string = ''

    for fruits_chosen in ingredients_list:
        ingredients_string += fruits_chosen + ' '
        
    st.write(ingredients_string)
    
my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

#st.write(my_insert_stmt)
time_to_insert=st.button('Submit Ordr')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smotthie is ordered ',icon="✅")

