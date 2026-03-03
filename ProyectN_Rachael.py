import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Uber", layout="wide")

st.title("Dashboard de Viajes por Hora")

#  Cargar archivo automáticamente
df = pd.read_csv("ncr_ride_bookings.csv")

# Convertir columna 'time' a datetime
df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
df = df.dropna(subset=["Time"])

# Extraer hora
df["hour"] = df["Time"].dt.hour

# Filtro de rango de horas
st.sidebar.header("Filtros")

min_hour = int(df["hour"].min())
max_hour = int(df["hour"].max())

selected_range = st.sidebar.slider(
    "Selecciona el rango de horas",
    min_value=min_hour,
    max_value=max_hour,
    value=(min_hour, max_hour)
)

# Aplicar filtro
df_filtered = df[
    (df["hour"] >= selected_range[0]) &
    (df["hour"] <= selected_range[1])
]

# Contar viajes por hora
hourly_trips = df_filtered["hour"].value_counts().sort_index()

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Total de Viajes", len(df_filtered))

if not hourly_trips.empty:
    col2.metric("Hora con Más Viajes", hourly_trips.idxmax())
    col3.metric("Cantidad Máxima", hourly_trips.max())
else:
    col2.metric("Hora con Más Viajes", "N/A")
    col3.metric("Cantidad Máxima", "N/A")

st.subheader("Viajes por Hora")

# Preparar datos para gráfico
chart_data = hourly_trips.reset_index()
chart_data.columns = ["Hora", "Cantidad"]
chart_data = chart_data.set_index("Hora")

# Gráfico
st.bar_chart(chart_data)