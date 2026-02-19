# %% [markdown]
# # Proyecto de Análisis de Eficiencia Energética en Edificios - México
# 
# ## 1. Carga y Validación de Datos
# Objetivo: Comprender la estructura del dataset y verificar su calidad.

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Configuración visual
plt.style.use('ggplot')
sns.set_palette("viridis")

# Cargar dataset
try:
    df = pd.read_csv('energy_consumption_mexico.csv')
    print("Dataset cargado exitosamente.")
except FileNotFoundError:
    print("Error: Archivo no encontrado. Asegúrate de tener 'energy_consumption_mexico.csv'.")
    # Generar datos dummy si no existe (opcional)
    exit()

# %%
# Exploración inicial
print(f"Dimensiones: {df.shape}")
print(df.dtypes)
print("\nVerificación de nulos:")
print(df.isnull().sum())

# Estadísticas básicas
print(df.describe())

# %% [markdown]
# ## 2. Creación de Métricas Derivadas
# Calcularemos métricas normalizadas para comparar justamente entre inmuebles.

# %%
# Costo por m2
df['costo_por_m2'] = df['costo_energia_mxn'] / df['superficie_m2']

# Costo por ocupante
df['costo_por_ocupante'] = df['costo_energia_mxn'] / df['ocupantes']

# Eficiencia relativa (0-1)
min_val = df['costo_por_m2'].min()
max_val = df['costo_por_m2'].max()
df['eficiencia_relativa'] = (df['costo_por_m2'] - min_val) / (max_val - min_val)

print(df[['costo_por_m2', 'costo_por_ocupante', 'eficiencia_relativa']].head())

# %% [markdown]
# ## 3. Detección de Outliers (IQR)
# Identificaremos valores atípicos en el costo total.

# %%
Q1 = df['costo_energia_mxn'].quantile(0.25)
Q3 = df['costo_energia_mxn'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df['costo_energia_mxn'] < lower_bound) | (df['costo_energia_mxn'] > upper_bound)]
print(f"Límites de Outliers: {lower_bound:.2f} - {upper_bound:.2f}")
print(f"Número de outliers detectados: {len(outliers)}")

# %% [markdown]
# ## 4. Análisis Exploratorio (EDA)
# Visualizaremos las distribuciones y relaciones clave.

# %%
# Distribución de Costo por Tipo de Cliente
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='costo_energia_mxn', hue='tipo_cliente', kde=True)
plt.title('Distribución de Costo Energético por Tipo de Cliente')
plt.show()

# Boxplot de Costo por m2 por Estado
plt.figure(figsize=(12, 8))
order = df.groupby('estado')['costo_por_m2'].median().sort_values(ascending=False).index
sns.boxplot(data=df, x='costo_por_m2', y='estado', order=order)
plt.title('Costo por m² por Estado')
plt.show()

# Scatter: Superficie vs Costo
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='superficie_m2', y='costo_energia_mxn', hue='tipo_cliente', alpha=0.6)
plt.title('Relación Superficie vs Costo')
plt.show()

# %% [markdown]
# ## 5. Análisis por Segmento y Recomendaciones
# Identificaremos patrones de ineficiencia.

# %%
# Top 5 Estados con mayor costo/m2
top_states = df.groupby('estado')['costo_por_m2'].mean().sort_values(ascending=False).head(5)
print("Top 5 Estados (Costo/m2):")
print(top_states)

# Prueba Mann-Whitney (Comercial vs Residencial)
comercial = df[df['tipo_cliente'] == 'Comercial']['costo_por_m2']
residencial = df[df['tipo_cliente'] == 'Residencial']['costo_por_m2']
stat, p_val = stats.mannwhitneyu(comercial, residencial)
print(f"Mann-Whitney p-value: {p_val:.4f}")

# Umbral de Ineficiencia (> P75)
umbral = df['costo_por_m2'].quantile(0.75)
ineficientes = df[df['costo_por_m2'] > umbral].copy()

print(f"Umbral de Ineficiencia: {umbral:.2f}")
print(f"Clientes Ineficientes: {len(ineficientes)}")

# Ahorro Potencial
ahorro_total = (ineficientes['costo_por_m2'] - df['costo_por_m2'].mean()) * ineficientes['superficie_m2']
print(f"Ahorro Mensual Potencial Total: ${ahorro_total.sum():,.2f}")

# %%
# Guardar datos procesados
df.to_csv('energy_consumption_processed.csv', index=False)
