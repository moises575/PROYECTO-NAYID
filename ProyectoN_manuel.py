import streamlit as st
import pandas as pd

st.subheader("Estado de los Viajes")

status_count = filtered_df['booking_status'].value_counts()

status_percent = (status_count / status_count.sum()) * 100

status_count.index = status_count.index.map({
    "Completed": "Completado",
    "Incomplete": "Incompleto",
    "Canceled": "Cancelado"
})

status_percent.index = status_percent.index.map({
    "Completed": "Completado",
    "Incomplete": "Incompleto",
    "Canceled": "Cancelado"
})

st.bar_chart(status_count)

tabla_porcentaje = status_percent.round(2).reset_index()
tabla_porcentaje.columns = ["Estado del Viaje", "Porcentaje (%)"]

st.write("### Porcentaje de cada estado")
st.dataframe(tabla_porcentaje)