import streamlit as st
import pandas as pd

st.title("Grafico de tipos de vehiculos utilizados por los choferes")
st.caption("Moises Porras Valverde")

df = pd.read_csv("ncr_ride_bookings.csv")
df.columns = df.columns.str.strip()

st.subheader("Fintro por autos usados por los choferes")

if "Vehicle Type" in df.columns:

    opciones = df["Vehicle Type"].dropna().unique()

    seleccion = st.multiselect(
        "Selecciona tipo de auto:",
        options=opciones,
        default=opciones
    )

    df_filtrado = df[df["Vehicle Type"].isin(seleccion)]

    st.write("Cantidad de registros:", df_filtrado.shape[0])

    with st.expander("Ver tabla de datos"):
        st.dataframe(df_filtrado)

    conteo = df_filtrado["Vehicle Type"].value_counts()
    st.bar_chart(conteo)

else:
    st.error("Error en columnas del archivo")

