import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("GRAFICO DE TIPOS DE VEHICULOS UTILIZADOS POR LOS CHOFERES")
st.caption("Moisés Porras Valverde")

df = pd.read_csv("ncr_ride_bookings.csv")
df.columns = df.columns.str.strip()

st.sidebar.title("Filtros")

opciones = df["Booking Status"].dropna().unique()

seleccion = st.sidebar.multiselect(
    "Selecciona Booking Status:",
    options=opciones,
    default=opciones
)

df_filtrado = df[df["Booking Status"].isin(seleccion)]

st.subheader("Cantidad de registros")
st.write(df_filtrado.shape[0])

with st.expander("Ver tabla de datos"):
    st.dataframe(df_filtrado)

st.subheader("TIPO DE AUTOS MAS USADOS POR LOS CHOFERES")

conteo = df_filtrado["Vehicle Type"].value_counts()

st.bar_chart(conteo)
