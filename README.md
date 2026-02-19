# Proyecto de Análisis de Eficiencia Energética en Edificios 🇲🇽

## 1. Problema de Negocio
El objetivo de este proyecto es analizar el consumo energético de 5,000 inmuebles en México para identificar ineficiencias y oportunidades de ahorro. Se busca responder preguntas clave sobre costos por metro cuadrado, diferencias entre tipos de clientes y patrones geográficos.

## 2. Datos
El dataset `energy_consumption_mexico.csv` contiene 5,000 registros con las siguientes variables:
- **Identificadores**: `cliente_id`, `tipo_cliente` (Residencial/Comercial).
- **Geografía**: `estado` (25 estados de México).
- **Métricas Físicas**: `superficie_m2` (17-77 m²), `ocupantes` (1-4).
- **Métrica Financiera**: `costo_energia_mxn` (Mensual).

## 3. Metodología
El análisis se realizó utilizando Python (Pandas, Numpy, Scipy) y se visualizó mediante un dashboard interactivo en Streamlit.

### Pasos Clave:
1.  **Limpieza y Validación**: Se verificó la integridad de los datos (sin nulos) y se detectaron outliers usando el rango intercuartil (IQR).
2.  **Ingeniería de Características**: Se crearon métricas normalizadas:
    *   `costo_por_m2`: Para comparar inmuebles de distinto tamaño.
    *   `costo_por_ocupante`: Para evaluar eficiencia per cápita.
    *   `eficiencia_relativa`: Escala 0-1.
3.  **Análisis Estadístico**: Se aplicó la prueba U de Mann-Whitney para comparar segmentos y se definieron umbrales de ineficiencia basados en percentiles (P75).

## 4. Resultados Principales 📊

| Pregunta de Negocio | Hallazgo | Dato Duro |
| :--- | :--- | :--- |
| **¿Estado con mayor costo/m²?** | Quintana Roo es el estado más caro en promedio. | **~$10.71 MXN/m²** |
| **¿Comercial vs Residencial?** | No existe diferencia significativa en eficiencia entre ambos tipos. | **p-value = 0.62** (Mann-Whitney) |
| **¿Volumen de Ineficiencia?** | El 25% de la base de clientes se considera ineficiente. | **1,250 clientes** > P75 |
| **¿Oportunidad de Ahorro?** | Ahorro potencial si los ineficientes mejoran al promedio. | **~$130 MXN al mes** por cliente |

### Insigths Adicionales
- **Foco Geográfico**: Aunque Quintana Roo tiene el costo promedio más alto, **Aguascalientes** concentra el mayor número de clientes ineficientes (104).
- **Impacto**: Optimizar a los clientes ineficientes podría generar un ahorro total estimado de más de **$160,000 MXN mensuales** en la cartera analizada.

## 5. Cómo ejecutar este proyecto

### Requisitos
Asegúrate de tener instaladas las librerías necesarias:
```bash
pip install pandas numpy matplotlib seaborn plotly streamlit scipy
```

### Ejecutar el Dashboard
Para interactuar con los datos y filtros:
```bash
streamlit run app.py
```

### Reproducir el Análisis
El script de análisis detallado y generación de reporte se encuentra en los archivos python adjuntos o en el notebook.
