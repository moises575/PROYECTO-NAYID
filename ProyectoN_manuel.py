import streamlit as st
import pandas as pd

df = pd.read_csv("ncr_ride_bookings.csv")
df.columns = df.columns.str.strip()

st.subheader("Estado de los Viajes")

status_count = df["Booking Status"].value_counts()
status_percent = (status_count / status_count.sum()) * 100

st.bar_chart(status_count)

st.write("Porcentaje de cada estado:")
st.write(status_percent.round(2))