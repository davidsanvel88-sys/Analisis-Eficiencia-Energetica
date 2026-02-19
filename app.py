import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página
st.set_page_config(page_title="Dashboard Eficiencia Energética", layout="wide")

# Título y Descripción
st.title("📊 Dashboard de Eficiencia Energética en Edificios - México")
st.markdown("""
Este dashboard permite analizar el consumo energético de 5,000 clientes, 
identificando ineficiencias y patrones de costo por estado y tipo de cliente.
""")

# Cargar datos
@st.cache_data
def load_data():
    # Intentar cargar el procesado, si no, cargar el original y procesar
    try:
        df = pd.read_csv('energy_consumption_processed.csv')
    except FileNotFoundError:
        df = pd.read_csv('energy_consumption_mexico.csv')
        # Procesamiento básico si no existe el procesado
        df['costo_por_m2'] = df['costo_energia_mxn'] / df['superficie_m2']
        df['costo_por_ocupante'] = df['costo_energia_mxn'] / df['ocupantes']
    return df

df = load_data()

# Sidebar - Filtros
st.sidebar.header("Filtros")
tipo_filter = st.sidebar.multiselect(
    "Tipo de Cliente",
    options=df['tipo_cliente'].unique(),
    default=df['tipo_cliente'].unique()
)

estados_list = sorted(df['estado'].unique())
estado_filter = st.sidebar.multiselect(
    "Estado",
    options=estados_list,
    default=estados_list
)

# Filtrar DataFrame
df_filtered = df[
    (df['tipo_cliente'].isin(tipo_filter)) &
    (df['estado'].isin(estado_filter))
]

# KPI Cards
st.subheader("Métricas Clave (KPIs)")
col1, col2, col3, col4 = st.columns(4)

avg_cost = df_filtered['costo_energia_mxn'].mean()
avg_cost_m2 = df_filtered['costo_por_m2'].mean()
avg_cost_occ = df_filtered['costo_por_ocupante'].mean()

# Ineficiencia (usando umbral global para consistencia)
umbral_ineficiencia = df['costo_por_m2'].quantile(0.75)
pct_ineficientes = (df_filtered['costo_por_m2'] > umbral_ineficiencia).mean() * 100

col1.metric("Costo Promedio Mensual", f"${avg_cost:.2f} MXN")
col2.metric("Costo Promedio / m²", f"${avg_cost_m2:.2f} MXN")
col3.metric("Costo Promedio / Ocupante", f"${avg_cost_occ:.2f} MXN")
col4.metric("% Clientes Ineficientes", f"{pct_ineficientes:.1f}%", help="Clientes por encima del P75 global de Costo/m²")

# Gráficos
st.markdown("---")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("Top 10 Estados por Costo Promedio")
    # Agrupar por estado y ordenar
    top_states = df_filtered.groupby('estado')['costo_energia_mxn'].mean().sort_values(ascending=False).head(10).reset_index()
    
    fig_bar = px.bar(
        top_states, 
        x='costo_energia_mxn', 
        y='estado', 
        orientation='h',
        title="Costo Promedio de Energía por Estado",
        labels={'costo_energia_mxn': 'Costo Promedio (MXN)', 'estado': 'Estado'},
        color='costo_energia_mxn',
        color_continuous_scale='Reds'
    )
    fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_bar, width='stretch')
    st.caption("Interpretación: Identifica qué estados tienen costos estructuralmente más altos.")

with col_right:
    st.subheader("Relación Superficie vs Costo")
    # Scatter plot
    fig_scatter = px.scatter(
        df_filtered,
        x='superficie_m2',
        y='costo_energia_mxn',
        color='tipo_cliente',
        size='ocupantes',
        title="Análisis de Correlación: Superficie vs Costo",
        labels={'superficie_m2': 'Superficie (m²)', 'costo_energia_mxn': 'Costo Mensual (MXN)'},
        opacity=0.6
    )
    st.plotly_chart(fig_scatter, width='stretch')
    st.caption("Interpretación: Se espera una tendencia positiva. Puntos muy por encima de la tendencia indican ineficiencia.")

# Sección de Ineficiencia
st.markdown("---")
st.subheader("🔍 Análisis de Ineficiencia")

ineficientes_df = df_filtered[df_filtered['costo_por_m2'] > umbral_ineficiencia]

st.markdown(f"Mostrando **{len(ineficientes_df)}** clientes categorizados como ineficientes (Costo/m² > ${umbral_ineficiencia:.2f}).")

with st.expander("Ver lista de clientes ineficientes"):
    st.dataframe(ineficientes_df)
    
    csv = ineficientes_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar CSV de Clientes Ineficientes",
        data=csv,
        file_name='clientes_ineficientes.csv',
        mime='text/csv',
    )
