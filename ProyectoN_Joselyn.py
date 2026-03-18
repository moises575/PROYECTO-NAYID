import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Uber", layout="wide")

st.title("Dashboard de Viajes por Hora")

df = pd.read_csv("ncr_ride_bookings.csv")

df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
df = df.dropna(subset=["Time"])

df["hour"] = df["Time"].dt.hour

df["hora_formato"] = df["Time"].dt.strftime("%H:00")

st.sidebar.header("Filtros")

min_hour = int(df["hour"].min())
max_hour = int(df["hour"].max())

selected_range = st.sidebar.slider(
    "Selecciona el rango de horas",
    min_value=min_hour,
    max_value=max_hour,
    value=(min_hour, max_hour)
)

df_filtered = df[
    (df["hour"] >= selected_range[0]) &
    (df["hour"] <= selected_range[1])
]

hourly_trips = df_filtered["hora_formato"].value_counts().sort_index()


col1, col2, col3 = st.columns(3)

col1.metric("Total de Viajes", len(df_filtered))

if not hourly_trips.empty:
    col2.metric("Hora con Más Viajes", hourly_trips.idxmax())
    col3.metric("Viajes en esa hora", hourly_trips.max())
else:
    col2.metric("Hora con Más Viajes", "N/A")
    col3.metric("Viajes en esa hora", "N/A")

st.subheader("Viajes por Hora")

chart_data = hourly_trips.reset_index()
chart_data.columns = ["Hora", "Cantidad"]
chart_data = chart_data.set_index("Hora")

st.bar_chart(chart_data)

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

st.set_page_config(page_title="Dashboard Uber", layout="wide")

st.title("Dashboard de Viajes")


df = pd.read_csv("ncr_ride_bookings.csv")
df.columns = df.columns.str.strip()


df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
df = df.dropna(subset=["Time"])

df["hour"] = df["Time"].dt.hour
df["hora_formato"] = df["Time"].dt.strftime("%H:00")


st.sidebar.header("Filtros")

min_hour = int(df["hour"].min())
max_hour = int(df["hour"].max())

selected_range = st.sidebar.slider(
    "Selecciona el rango de horas",
    min_value=min_hour,
    max_value=max_hour,
    value=(min_hour, max_hour),
    key="slider_horas"
)

opciones = df["Booking Status"].dropna().unique()

seleccion = st.sidebar.multiselect(
    "Selecciona Booking Status:",
    options=opciones,
    default=opciones,
    key="filtro_status"
)


df_filtered = df[
    (df["hour"] >= selected_range[0]) &
    (df["hour"] <= selected_range[1]) &
    (df["Booking Status"].isin(seleccion))
]


st.subheader("Resumen")

col1, col2, col3 = st.columns(3)

hourly_trips = df_filtered["hora_formato"].value_counts().sort_index()

col1.metric("Total de Viajes", len(df_filtered))

if not hourly_trips.empty:
    col2.metric("Hora con Más Viajes", hourly_trips.idxmax())
    col3.metric("Viajes en esa hora", hourly_trips.max())
else:
    col2.metric("Hora con Más Viajes", "N/A")
    col3.metric("Viajes en esa hora", "N/A")

st.subheader("Viajes por Hora")

chart_data = hourly_trips.reset_index()
chart_data.columns = ["Hora", "Cantidad"]
chart_data = chart_data.set_index("Hora")

st.bar_chart(chart_data)


st.subheader("Tipos de Vehículos Utilizados")

conteo = df_filtered["Vehicle Type"].value_counts()
st.bar_chart(conteo)


st.subheader("Estado de los Viajes (%)")

status_count = df_filtered["Booking Status"].value_counts()
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

st.table(tabla_porcentaje)