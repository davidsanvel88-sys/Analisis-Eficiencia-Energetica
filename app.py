import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import os

# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Eficiencia Energética MX",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS PERSONALIZADO — Diseño profesional de portafolio
# ============================================================
st.markdown("""
<style>
    /* Tipografía */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Fondo principal */
    .stApp { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.95);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #e0e0e0;
    }

    /* KPI Cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px 24px;
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.3);
    }
    div[data-testid="stMetric"] label { color: #a5b4fc !important; font-weight: 500; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #ffffff !important; font-weight: 700; }

    /* Headers */
    h1 { color: #e0e7ff !important; font-weight: 700 !important; }
    h2, h3 { color: #c7d2fe !important; }
    p, span { color: #cbd5e1; }
    
    /* Expander */
    details { 
        background: rgba(255,255,255,0.03) !important; 
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        color: #a5b4fc;
        padding: 8px 20px;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99, 102, 241, 0.3) !important;
        color: #fff !important;
    }

    /* Dividers */
    hr { border-color: rgba(255,255,255,0.08) !important; }

    /* Download button */
    .stDownloadButton button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# CARGA DE DATOS
# ============================================================
@st.cache_data
def load_data():
    """Carga el CSV y genera métricas derivadas."""
    # Determinar la ruta del archivo
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'energy_consumption_mexico.csv')
    
    df = pd.read_csv(csv_path)
    
    # Métricas derivadas
    df['costo_por_m2'] = df['costo_energia_mxn'] / df['superficie_m2']
    df['costo_por_ocupante'] = df['costo_energia_mxn'] / df['ocupantes']
    
    # Eficiencia relativa (0 = más eficiente, 1 = menos eficiente)
    min_val = df['costo_por_m2'].min()
    max_val = df['costo_por_m2'].max()
    df['eficiencia_relativa'] = (df['costo_por_m2'] - min_val) / (max_val - min_val)
    
    return df

df = load_data()

# Umbral global de ineficiencia (Percentil 75)
UMBRAL_INEFICIENCIA = df['costo_por_m2'].quantile(0.75)

# ============================================================
# SIDEBAR — Filtros y Metadata
# ============================================================
with st.sidebar:
    st.markdown("## ⚡ Panel de Control")
    st.markdown("---")
    
    st.markdown("### 🔎 Filtros")
    tipo_filter = st.multiselect(
        "Tipo de Cliente",
        options=sorted(df['tipo_cliente'].unique()),
        default=sorted(df['tipo_cliente'].unique())
    )
    
    estado_filter = st.multiselect(
        "Estado",
        options=sorted(df['estado'].unique()),
        default=sorted(df['estado'].unique())
    )
    
    st.markdown("---")
    st.markdown("### 📋 Sobre este proyecto")
    st.markdown("""
    Análisis de eficiencia energética para **5,000 inmuebles** 
    en **25 estados** de México.
    
    **Objetivo:** Identificar ineficiencias de consumo 
    y oportunidades de ahorro.
    
    **Autor:** David Sánchez  
    **Stack:** Python · Pandas · Plotly · Streamlit
    """)

# ============================================================
# FILTRAR DATOS
# ============================================================
df_filtered = df[
    (df['tipo_cliente'].isin(tipo_filter)) &
    (df['estado'].isin(estado_filter))
]

# ============================================================
# HEADER
# ============================================================
st.markdown("# ⚡ Análisis de Eficiencia Energética en Edificios")
st.markdown("##### México — 5,000 inmuebles · 25 estados · Residencial & Comercial")
st.markdown("---")

# ============================================================
# KPI CARDS
# ============================================================
col1, col2, col3, col4 = st.columns(4)

avg_cost = df_filtered['costo_energia_mxn'].mean()
avg_cost_m2 = df_filtered['costo_por_m2'].mean()
avg_cost_occ = df_filtered['costo_por_ocupante'].mean()
pct_ineficientes = (df_filtered['costo_por_m2'] > UMBRAL_INEFICIENCIA).mean() * 100
n_ineficientes = (df_filtered['costo_por_m2'] > UMBRAL_INEFICIENCIA).sum()

col1.metric("💰 Costo Promedio Mensual", f"${avg_cost:,.0f} MXN")
col2.metric("📐 Costo / m²", f"${avg_cost_m2:.2f} MXN")
col3.metric("👤 Costo / Ocupante", f"${avg_cost_occ:.0f} MXN")
col4.metric("🚨 Clientes Ineficientes", f"{n_ineficientes:,} ({pct_ineficientes:.1f}%)")

st.markdown("---")

# ============================================================
# GRÁFICOS PRINCIPALES (Tabs)
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Costos por Estado", 
    "🔬 Superficie vs Costo", 
    "📈 Distribuciones",
    "🗺️ Mapa de Ineficiencia"
])

# --- TAB 1: Top estados ---
with tab1:
    col_a, col_b = st.columns([3, 2])
    
    with col_a:
        top_states = (df_filtered.groupby('estado')['costo_por_m2']
                      .mean()
                      .sort_values(ascending=True)
                      .tail(15)
                      .reset_index())
        
        fig_bar = px.bar(
            top_states,
            x='costo_por_m2',
            y='estado',
            orientation='h',
            title="Top 15 Estados — Costo Promedio por m²",
            labels={'costo_por_m2': 'Costo / m² (MXN)', 'estado': ''},
            color='costo_por_m2',
            color_continuous_scale='Inferno'
        )
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#cbd5e1',
            title_font_size=18,
            showlegend=False,
            coloraxis_showscale=False,
            height=500
        )
        st.plotly_chart(fig_bar, width='stretch')
    
    with col_b:
        st.markdown("#### 🔍 Interpretación")
        top5 = (df_filtered.groupby('estado')['costo_por_m2']
                .mean()
                .sort_values(ascending=False)
                .head(5))
        
        st.markdown(f"""
        **Estado más caro:** {top5.index[0]} con **${top5.iloc[0]:.2f} MXN/m²**
        
        Los 5 estados con mayor costo por m² son:
        """)
        for i, (estado, costo) in enumerate(top5.items(), 1):
            st.markdown(f"{i}. **{estado}** — ${costo:.2f}/m²")
        
        st.markdown(f"""
        ---
        **Promedio nacional:** ${df_filtered['costo_por_m2'].mean():.2f}/m²
        
        Los estados con mayor costo superan el promedio 
        en un **{((top5.iloc[0] / df_filtered['costo_por_m2'].mean()) - 1) * 100:.1f}%**.
        """)

# --- TAB 2: Scatter ---
with tab2:
    fig_scatter = px.scatter(
        df_filtered,
        x='superficie_m2',
        y='costo_energia_mxn',
        color='tipo_cliente',
        size='ocupantes',
        title="Correlación: Superficie vs Costo Energético",
        labels={
            'superficie_m2': 'Superficie (m²)',
            'costo_energia_mxn': 'Costo Mensual (MXN)',
            'tipo_cliente': 'Tipo'
        },
        opacity=0.5,
        color_discrete_map={'Residencial': '#6366f1', 'Comercial': '#f97316'},
        hover_data=['cliente_id', 'estado', 'costo_por_m2']
    )
    
    # Línea de tendencia
    z = np.polyfit(df_filtered['superficie_m2'], df_filtered['costo_energia_mxn'], 1)
    x_line = np.linspace(df_filtered['superficie_m2'].min(), df_filtered['superficie_m2'].max(), 100)
    y_line = z[0] * x_line + z[1]
    fig_scatter.add_trace(go.Scatter(
        x=x_line, y=y_line,
        mode='lines',
        name=f'Tendencia (pendiente={z[0]:.2f})',
        line=dict(color='#f43f5e', width=2, dash='dash')
    ))
    
    fig_scatter.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#cbd5e1',
        title_font_size=18,
        height=550
    )
    st.plotly_chart(fig_scatter, width='stretch')
    
    st.info(f"""
    📌 **Interpretación:** La pendiente de la regresión es **{z[0]:.2f} MXN por m² adicional**. 
    Los puntos que se encuentran muy por encima de la línea roja son clientes con potencial de mejora.
    Correlación (Pearson): **{df_filtered['superficie_m2'].corr(df_filtered['costo_energia_mxn']):.3f}**
    """)

# --- TAB 3: Distribuciones ---
with tab3:
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        fig_hist = px.histogram(
            df_filtered,
            x='costo_energia_mxn',
            color='tipo_cliente',
            marginal='box',
            title="Distribución de Costo Energético",
            labels={'costo_energia_mxn': 'Costo (MXN)', 'tipo_cliente': 'Tipo'},
            color_discrete_map={'Residencial': '#6366f1', 'Comercial': '#f97316'},
            barmode='overlay',
            opacity=0.7
        )
        fig_hist.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#cbd5e1',
            height=450
        )
        st.plotly_chart(fig_hist, width='stretch')
    
    with col_d2:
        # Heatmap de correlación
        numeric_cols = ['superficie_m2', 'ocupantes', 'costo_energia_mxn', 
                        'costo_por_m2', 'costo_por_ocupante', 'eficiencia_relativa']
        corr_matrix = df_filtered[numeric_cols].corr()
        
        fig_heatmap = px.imshow(
            corr_matrix,
            text_auto='.2f',
            title="Matriz de Correlación",
            color_continuous_scale='RdBu_r',
            aspect='auto'
        )
        fig_heatmap.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#cbd5e1',
            height=450
        )
        st.plotly_chart(fig_heatmap, width='stretch')

# --- TAB 4: Mapa de Ineficiencia ---
with tab4:
    col_m1, col_m2 = st.columns([3, 2])
    
    with col_m1:
        inef_by_state = (df_filtered
                         .groupby('estado')
                         .agg(
                             pct_ineficientes=('costo_por_m2', lambda x: (x > UMBRAL_INEFICIENCIA).mean() * 100),
                             costo_medio_m2=('costo_por_m2', 'mean'),
                             n_clientes=('cliente_id', 'count')
                         )
                         .reset_index()
                         .sort_values('pct_ineficientes', ascending=True))
        
        fig_inef = px.bar(
            inef_by_state,
            x='pct_ineficientes',
            y='estado',
            orientation='h',
            title="Porcentaje de Clientes Ineficientes por Estado",
            labels={'pct_ineficientes': '% Ineficientes', 'estado': ''},
            color='pct_ineficientes',
            color_continuous_scale='YlOrRd',
            hover_data=['costo_medio_m2', 'n_clientes']
        )
        fig_inef.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#cbd5e1',
            title_font_size=18,
            coloraxis_showscale=False,
            height=600
        )
        st.plotly_chart(fig_inef, width='stretch')
    
    with col_m2:
        st.markdown("#### 📊 Estadísticas de Ineficiencia")
        
        # Mann-Whitney
        comercial = df_filtered[df_filtered['tipo_cliente'] == 'Comercial']['costo_por_m2']
        residencial = df_filtered[df_filtered['tipo_cliente'] == 'Residencial']['costo_por_m2']
        
        if len(comercial) > 0 and len(residencial) > 0:
            _, p_val = stats.mannwhitneyu(comercial, residencial)
            significativo = "✅ Sí" if p_val < 0.05 else "❌ No"
            
            st.markdown(f"""
            **Prueba Mann-Whitney U**  
            *(Comercial vs Residencial)*
            
            | Métrica | Valor |
            |:--------|:------|
            | p-value | {p_val:.4f} |
            | ¿Significativo? | {significativo} |
            | Media Comercial | ${comercial.mean():.2f}/m² |
            | Media Residencial | ${residencial.mean():.2f}/m² |
            """)
        
        st.markdown("---")
        
        # Ahorro potencial
        inef_df = df_filtered[df_filtered['costo_por_m2'] > UMBRAL_INEFICIENCIA]
        promedio_global = df_filtered['costo_por_m2'].mean()
        
        if len(inef_df) > 0:
            ahorro_individual = ((inef_df['costo_por_m2'] - promedio_global) * inef_df['superficie_m2']).mean()
            ahorro_total = ((inef_df['costo_por_m2'] - promedio_global) * inef_df['superficie_m2']).sum()
            
            st.markdown(f"""
            **💡 Oportunidad de Ahorro**
            
            | Concepto | Valor |
            |:---------|:------|
            | Umbral P75 | ${UMBRAL_INEFICIENCIA:.2f}/m² |
            | Clientes afectados | {len(inef_df):,} |
            | Ahorro/cliente/mes | **${ahorro_individual:,.0f} MXN** |
            | Ahorro total/mes | **${ahorro_total:,.0f} MXN** |
            """)

# ============================================================
# SECCIÓN: CLIENTES INEFICIENTES (Descargable)
# ============================================================
st.markdown("---")
st.markdown("### 🚨 Tabla de Clientes Ineficientes")

ineficientes_df = df_filtered[df_filtered['costo_por_m2'] > UMBRAL_INEFICIENCIA].sort_values('costo_por_m2', ascending=False)

st.markdown(f"Mostrando **{len(ineficientes_df):,}** clientes con Costo/m² > **${UMBRAL_INEFICIENCIA:.2f}** (Percentil 75 global)")

with st.expander("📋 Ver tabla completa", expanded=False):
    display_cols = ['cliente_id', 'tipo_cliente', 'estado', 'superficie_m2', 
                    'ocupantes', 'costo_energia_mxn', 'costo_por_m2', 'costo_por_ocupante']
    st.dataframe(
        ineficientes_df[display_cols].head(100),
        use_container_width=True,
        hide_index=True
    )
    
    csv = ineficientes_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Descargar CSV completo de clientes ineficientes",
        data=csv,
        file_name='clientes_ineficientes.csv',
        mime='text/csv',
    )

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 14px; padding: 20px;">
    Desarrollado por <strong>David Sánchez</strong> · 
    Proyecto de Portafolio · 
    Python · Pandas · Plotly · Streamlit · 
    <a href="https://github.com/davidsanvel88-sys" style="color: #6366f1;">GitHub</a>
</div>
""", unsafe_allow_html=True)
