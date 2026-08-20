# Import python packages
import streamlit as st
import os
from snowflake.snowpark.context import get_active_session #needed to add this line to get active session info
from snowflake.snowpark.functions import col    #for selecting specific columns in session table

# Write directly to the app
##st.title(f"Example Streamlit App :cup_with_straw: {st.__version__}")
st.title(f"Customise Your Smoothie! :cup_with_straw:")
st.write(
  """**If you're new to Streamlit,** check
  out our easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  \nChoose the **fruits** you want in your custom smoothie~!
  """
)

##option = st.selectbox(
##    "What is your fav fruit?",
##    ("Banana", "Strawbeerries", "Peaches"),
##)
##st.write("You  fav fruit is:", option)

name_on_order=st.text_input('Enter your name:') #don’t use labels with apostrophes like “Gina’s Smoothie.” 
st.write('Name on smoothie is:',name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect(
'Choose up to 5 ingredients:'
,my_dataframe
,max_selections=5
)

if(ingredients_list):
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen+' '

    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('""" + ingredients_string +"""','""" +name_on_order+ """')"""

    #st.write(my_insert_stmt)
    #st.stop()  #stop script from processing after this line
    time_to_insert=st.button('Submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
