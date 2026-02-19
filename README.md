# ⚡ Análisis de Eficiencia Energética en Edificios — México

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://zdokdmw6iu9ggaybxbfptd.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly)

> Proyecto de portafolio: Análisis de datos de consumo energético para 5,000 inmuebles en 25 estados de México. Incluye detección de ineficiencias, pruebas estadísticas y un dashboard interactivo desplegado en la nube.

---

## 🎯 Problema de Negocio

Las empresas de distribución eléctrica necesitan identificar **clientes con consumo ineficiente** para:
- Ofrecer programas de eficiencia energética focalizados
- Reducir la demanda pico en estados con infraestructura limitada
- Generar ahorros mensurables tanto para la empresa como para el cliente

## 📊 Dataset

| Variable | Tipo | Descripción |
|:---------|:-----|:------------|
| `cliente_id` | string | Identificador único (5,000 registros) |
| `tipo_cliente` | string | Residencial / Comercial |
| `estado` | string | 25 estados de México |
| `superficie_m2` | float | Superficie del inmueble (17–77 m²) |
| `ocupantes` | int | Número de personas (1–4) |
| `costo_energia_mxn` | float | Costo mensual en pesos (~200–603 MXN) |

### Métricas Derivadas
- **`costo_por_m2`** = costo / superficie → Normaliza por tamaño
- **`costo_por_ocupante`** = costo / ocupantes → Normaliza por uso
- **`eficiencia_relativa`** = Min-Max scaling de costo_por_m2 (0 = eficiente, 1 = ineficiente)

## 🔬 Metodología

1. **Limpieza y validación**: 0 nulos, detección de outliers con IQR (242 detectados)
2. **EDA**: Distribuciones, boxplots por estado, scatter con línea de tendencia
3. **Análisis estadístico**: Prueba U de Mann-Whitney para comparar segmentos
4. **Detección de ineficiencia**: Umbral basado en Percentil 75 del costo/m²

## 📈 Resultados Principales

| Pregunta | Hallazgo | Evidencia |
|:---------|:---------|:----------|
| ¿Estado más caro por m²? | **Quintana Roo** | ~$10.71 MXN/m² |
| ¿Comercial vs Residencial? | **Sin diferencia significativa** | Mann-Whitney p = 0.62 |
| ¿Cuántos son ineficientes? | **1,250 clientes** (25%) | Costo/m² > P75 ($13.01) |
| ¿Ahorro potencial? | **~$130 MXN/mes** por cliente | Si bajan al promedio |

### 💡 Recomendaciones

**Hallazgo:** Quintana Roo tiene el costo/m² más alto ($10.71 MXN/m²).  
**Causa probable:** Climatización intensa por temperatura y humedad elevadas.  
**Acción recomendada:** Programa de aislamiento térmico y aire acondicionado eficiente.  
**Ahorro estimado:** 15-20% en costo mensual.

**Hallazgo:** 1,250 clientes (25%) superan el umbral de ineficiencia.  
**Causa probable:** Equipos antiguos, malas prácticas de consumo o aislamiento deficiente.  
**Acción recomendada:** Auditoría energética focalizada en el Top 10% de ineficientes.  
**Ahorro estimado:** ~$130 MXN mensuales por cliente = $162,500 MXN/mes en total.

## 🖥️ Dashboard en Vivo

👉 **[Acceder al Dashboard](https://zdokdmw6iu9ggaybxbfptd.streamlit.app)**

Características:
- Filtros dinámicos por tipo de cliente y estado
- KPIs en tiempo real
- 4 pestañas con visualizaciones interactivas (Plotly)
- Tabla de clientes ineficientes descargable como CSV
- Diseño glassmorphism con tema oscuro profesional

## 🚀 Cómo Ejecutar Localmente

```bash
# 1. Clonar el repositorio
git clone https://github.com/davidsanvel88-sys/Analisis-Eficiencia-Energetica.git
cd Analisis-Eficiencia-Energetica

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Lanzar el dashboard
streamlit run app.py
```

## 🛠️ Stack Tecnológico

- **Python 3.9+** — Lenguaje principal
- **Pandas & NumPy** — Manipulación y análisis de datos
- **Matplotlib & Seaborn** — Visualizaciones estáticas (notebook)
- **Plotly** — Gráficos interactivos (dashboard)
- **Streamlit** — Framework del dashboard
- **SciPy** — Pruebas estadísticas (Mann-Whitney U)

## 📁 Estructura del Proyecto

```
├── app.py                          # Dashboard interactivo (Streamlit)
├── notebook.py                     # Análisis exploratorio completo
├── energy_consumption_mexico.csv   # Dataset original
├── requirements.txt                # Dependencias
├── README.md                       # Este archivo
└── .gitignore
```

---

<p align="center">
  Desarrollado por <strong>David Sánchez</strong> · 
  <a href="https://github.com/davidsanvel88-sys">GitHub</a>
</p>
