import streamlit as st
import pandas as pd


df = pd.read_csv("ncr_ride_bookings.csv")
df.columns = df.columns.str.strip()

st.subheader("Estado de los Viajes")

status_count = df["Booking Status"].value_counts()

status_percent = (status_count / status_count.sum()) * 100


traduccion = {
    "Completed": "Completado",
    "Incomplete": "Incompleto",
    "Canceled": "Cancelado",
    "Cancelled": "Cancelado",
    "Cancelled by Driver": "Cancelado por el conductor",
    "Cancelled by Customer": "Cancelado por el cliente",
    "No Driver Found": "No se encontró conductor"
}


status_percent.index = status_percent.index.map(lambda x: traduccion.get(x, x))


st.bar_chart(status_percent)


tabla_porcentaje = status_percent.round(0).astype(int).astype(str) + "%"
tabla_porcentaje = tabla_porcentaje.reset_index()
tabla_porcentaje.columns = ["Estado del Viaje", "Porcentaje"]

st.write("Porcentaje de cada estado:")
st.table(tabla_porcentaje)