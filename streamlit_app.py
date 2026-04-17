import streamlit as st
import pandas as pd 

#Lähteet: http://docs.streamlit.io
#jatka videosta kohdasta 14:17..

# datan lataus ja tarkastelu:

df = pd.read_csv("001_hotel_Rovaniemi.csv")

st.markdown(
'''# Hotellit Rovaniemessä
Kuukausittainen hotelli kapasiteetti ja majoitustiedot ''')

st.dataframe(df.head())

st.write("Sarakkeet:")
st.write(df.columns)


