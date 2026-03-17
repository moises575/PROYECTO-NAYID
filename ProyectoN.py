import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Uber", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
}
h1 {
    color: #f8fafc;
    font-size: 2rem;
}
h2, h3 {
    color: #94a3b8;
}
[data-testid="stSidebar"] {
    background-color: #1e293b;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1e293b, #334155);
    border: 1px solid #475569;
    border-radius: 12px;
    padding: 16px !important;
}
[data-testid="metric-container"] label {
    color: #94a3b8 !important;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}
[data-testid="metric-container"] [data-testid="metric-value"] {
    color: #38bdf8 !important;
    font-size: 2rem;
    font-weight: 700;
}
table {
    border-collapse: collapse;
    width: 100%;
    border-radius: 10px;
    overflow: hidden;
}
thead tr th {
    background-color: #1d4ed8 !important;
    color: white !important;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 10px 14px !important;
}
tbody tr:nth-child(odd) td {
    background-color: #1e293b !important;
    color: #e2e8f0 !important;
    padding: 9px 14px !important;
}
tbody tr:nth-child(even) td {
    background-color: #0f172a !important;
    color: #cbd5e1 !important;
    padding: 9px 14px !important;
}
[data-testid="stExpander"] {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def cargar_datos():
    df = pd.read_csv("ncr_ride_bookings.csv")
    df.columns = df.columns.str.strip()
    df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
    df = df.dropna(subset=["Time"])
    df["hour"] = df["Time"].dt.hour
    df["hora_formato"] = df["Time"].dt.strftime("%H:00")
    return df

df = cargar_datos()

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

st.title("Dashboard de Viajes")
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
st.bar_chart(chart_data, color="#38bdf8", height=350)

st.subheader("TIPO DE AUTOS MÁS USADOS POR LOS CHOFERES")
conteo = df_filtered["Vehicle Type"].value_counts()
conteo_df = conteo.reset_index()
conteo_df.columns = ["Tipo de Vehículo", "Cantidad"]
vehicle_colors = ["#f59e0b", "#10b981", "#8b5cf6", "#ef4444", "#06b6d4", "#ec4899", "#84cc16"]
conteo_wide = conteo_df.set_index("Tipo de Vehículo").T
st.bar_chart(conteo_wide, color=vehicle_colors[:len(conteo_df)], height=350)

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
status_colors = {
    "Completado":                  "#10b981",
    "Incompleto":                  "#f59e0b",
    "Cancelado":                   "#ef4444",
    "Cancelado por el conductor":  "#8b5cf6",
    "Cancelado por el cliente":    "#ec4899",
    "No se encontró conductor":    "#06b6d4",
}
status_percent.index = status_percent.index.map(lambda x: traduccion.get(x, x))
status_df = status_percent.reset_index()
status_df.columns = ["Estado", "Porcentaje"]
status_wide = status_df.set_index("Estado").T
bar_colors = [status_colors.get(e, "#64748b") for e in status_df["Estado"]]
st.bar_chart(status_wide, color=bar_colors, height=350)

tabla_porcentaje = status_percent.round(0).astype(int).astype(str) + "%"
tabla_porcentaje = tabla_porcentaje.reset_index()
tabla_porcentaje.columns = ["Estado del Viaje", "Porcentaje"]
st.table(tabla_porcentaje)

st.subheader("Cantidad de registros")
st.write(df_filtered.shape[0])

with st.expander("Ver tabla de datos"):
    st.dataframe(df_filtered)