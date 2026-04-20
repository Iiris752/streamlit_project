import streamlit as st
import pandas as pd 

#Lähteet: http://docs.streamlit.io
# Oma streamlit app: https://appproject-kno.streamlit.app/

# DATAN LATAUS JA TARKASTELU:

df = pd.read_csv("001_hotel_Rovaniemi.csv")

st.markdown(
'''# Hotellit Rovaniemessä
Kuukausittainen hotelli kapasiteetti ja majoitustiedot ''')

st.dataframe(df.head())

st.write("Sarakkeet:")
st.write(df.columns)


# SIMPLE OVERALL TREND
# lähteet: https://docs.streamlit.io/develop/api-reference/charts/st.line_chart
# https://stackoverflow.com/questions/47139203/transpose-pandas-dataframe-and-change-the-column-headers-to-a-list

st.title("Rovaniemen hotellitilastot")

# Valitaan sarakkeista vain alkaen "kotimaiset yöpymiset vuodelta 2025"
cols_2025 = [
    col for col in df.columns
    if col.startswith("Domestic nights 2025")
]

#  Käännetään transposella rivit ja sarakkaeet
hoteldata_df = (
    df[cols_2025]
    .T
    .reset_index()
    .rename(columns={"index": "Month", 0: "Value"})
)

# Poimitan lyhyesti vain kuukausi
hoteldata_df["Month"] = hoteldata_df["Month"].str[-3:]

# Otsikko ja kaavio
st.subheader("Kotimaisten yöpymisten kuukausittainen trendi vuonna 2025")
st.line_chart(hoteldata_df, x="Month", y="Value")
st.text("Kotimaan matkailu sijoittuu lähinnä kesäkuukausille")

#---------------- YEARLY TOTALS------------------------
#valitaan kokonaisyöpymiset:
cols_total = [
    col for col in df.columns
    if col.startswith("Nights spent")
]

#tehdään transpose
yearly_df = (
    df[cols_total]
    .T
    .reset_index()
    .rename(columns={"index": "Period", 0: "Value"})
)

#poimitaan vuosi sarakkaeen nimestä
yearly_df["Year"] = yearly_df["Period"].str.extract(r"(\d{4})")

#lasketaan summa
yearly_totals = (
    yearly_df
    .groupby("Year", as_index=False)["Value"]
    .sum()
)

#piirretään pylväsdiagrammi
st.subheader("Vuosittaiset kokonaisyöpymiset")
st.bar_chart(yearly_totals, x="Year", y="Value")
st.text("Koronavuodet näkyvät selkeänä romahduksena matkailussa, muuten matkailutrendi näyttää olevan nouseva")


# -------------------DOMESTIC VS. FOREIGN----------------------
#Valitaan oikeet sarakkeet:
domestic_cols = [
    col for col in df.columns
    if col.startswith("Domestic nights 2025")
]

foreign_cols = [
    col for col in df.columns
    if col.startswith("Foreign nights 2025")
]

#tehdään transposet:
domestic_df = (
    df[domestic_cols]
    .T
    .reset_index()
    .rename(columns={"index": "Month", 0: "Domestic"})
)
domestic_df["Month"] = domestic_df["Month"].str[-3:]

foreign_df = (
    df[foreign_cols]
    .T
    .reset_index()
    .rename(columns={"index": "Month", 0: "Foreign"})
)
foreign_df["Month"] = foreign_df["Month"].str[-3:]

#yhdistetään datat samaan taulukkoon
compare_df = domestic_df.merge(foreign_df, on="Month")

#näytetään datataulukko ja viivakaavio
st.subheader("Kotimaiset vs. ulkomaiset yöpymiset (2025)")
st.dataframe(compare_df)
st.line_chart(
    compare_df.set_index("Month")[["Domestic", "Foreign"]]
)
st.text("Ulkomaisten matkailijoiden määrä on suurta etenkin talvisaikaan (jouluturismi Rovaniemellä)")
#----------------------VERTAILU TOISEEN KUNTAAN-------------------------------------
df_compare = pd.read_csv("001_hotel_Kittilä.csv")

# Valitaan kokonaisyöpymiset vuodelta 2025 molemmilta kaupungeilta:

# Rovaniemi
total_cols_rovaniemi = [
    col for col in df.columns
    if col.startswith("Nights spent 2025")
]

# Kittilä
total_cols_kittila = [
    col for col in df_compare.columns
    if col.startswith("Nights spent 2025")
]

# Rovaniemi transpose
rovaniemi_data = (
    df[total_cols_rovaniemi]
    .T
    .reset_index()
    .rename(columns={"index": "Month", 0: "Rovaniemi"})
)
rovaniemi_data["Month"] = rovaniemi_data["Month"].str[-3:]

# Kittilä transpose
kittila_data = (
    df_compare[total_cols_kittila]
    .T
    .reset_index()
    .rename(columns={"index": "Month", 0: "Kittilä"})
)
kittila_data["Month"] = kittila_data["Month"].str[-3:]

# Yhdistetään 
attached_df = rovaniemi_data.merge(kittila_data, on="Month")

# Otsikko ja viivakaavio
st.subheader("Kokonaisyöpymiset: Rovaniemi vs. Kittilä, 2025")
st.line_chart(
    attached_df.set_index("Month")[["Rovaniemi", "Kittilä"]]
)

# ---------------------- DOWNLOAD BUTTON ----------------------
# Lähde: https://docs.streamlit.io/develop/api-reference/widgets/st.download_button

@st.cache_data
def convert_for_download(df):
    return df.to_csv(index=False).encode("utf-8")

csv_data = convert_for_download(attached_df)

st.download_button(
    label="Lataa vertailudata (CSV)",
    data=csv_data,
    file_name="rovaniemi_vs_kemi_2025.csv",
    mime="text/csv",
    icon=":material/download:"
)

# Lopuksi: Olen käyttänyt tehtävien teossa jälleen tuntien oppimateriaaleja sekä linkeistä löytyvää
# asiaa. Käytin kuitenkin tekoälyä muutamassa kohdassa tarkistamaan koodia, kun jäin jumittamaan jonkun
# pilkun, pisteen tai muotoilun vuoksi
