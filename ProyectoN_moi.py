import streamlit as st

import pandas as pd



st.title("GRAFICO DE TIPOS DE VEICULOS UTILISADOS POR LOS CHOFERES")

st.caption("Moisés Porras Valverde")



#dato para moi osea yo jajja de aca esta el fintro

st.title("Filtro por Booking Status")
 
df = pd.read_csv("ncr_ride_bookings.csv")
df.columns = df.columns.str.strip()
   
if "Booking Status" in df.columns:

    opciones = df["Booking Status"].dropna().unique()

    seleccion = st.multiselect(
        "Selecciona Booking Status:",
        options=opciones,
        default=opciones
    )

    df_filtrado = df[df["Booking Status"].isin(seleccion)]

     
    st.write("Cantidad de registros:", df_filtrado.shape[0])

    with st.expander("📋 Ver tabla de datos"):
        st.dataframe(df_filtrado)

else:
    st.error("La columna 'Booking Status' no existe.")
    st.write("Columnas disponibles:", df.columns)

  

# datos para moi o sea yo de aca esta el grafico

st.title("Booking Status")

df = pd.read_csv("ncr_ride_bookings.csv")

df.columns = df.columns.str.strip()

conteo = df["Booking Status"].value_counts()

st.bar_chart(conteo)

