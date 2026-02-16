import streamlit as st
import pandas as pd

st.title("GRAFICO DE TIPOS DE VEICULOS UTILISADOS POR LOS CHOFERES")
st.caption("Moisés Porras Valverde")

st.title("FINTRO DE AUTOS MAS USADOS POR LOS CHOFERES")

df = pd.read_csv("ncr_ride_bookings.csv")
df.columns = df.columns.str.strip()

opciones = df["Booking Status"].dropna().unique()

seleccion = st.multiselect(
    "Selecciona Booking Status:",
    options=opciones,
    default=opciones
)

df_filtrado = df[df["Booking Status"].isin(seleccion)]

st.write("Cantidad de registros:", df_filtrado.shape[0])

with st.expander("Ver tabla de datos"):
    st.dataframe(df_filtrado)

st.title("TIPO DE AUTOS MAS USADOS POR LOS CHOFERES")

conteo = df_filtrado["Vehicle Type"].value_counts()

st.bar_chart(conteo)

