import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ==========================================
# CONFIGURACIÓN Y ESTILOS (Versión Quirúrgica) 
# ==========================================
st.set_page_config(page_title="RFData - Simulador Montecarlo", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .card-blue { background-color: #f0f9ff; border-left: 5px solid #0ea5e9; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
    h1, h2, h3 { color: #0f172a; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
""", unsafe_allow_html=True)

leyenda_movil = dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5)

# ==========================================
# CUERPO ÚNICO: SIMULACIÓN DE MONTECARLO
# ==========================================
st.title("📈 Simulador de Inversión Inteligente")
st.markdown("Basado en la **Estadística y el Modelo de Montecarlo**. Modifica los parámetros en la barra lateral para proyectar 200 futuros posibles de la economía mundial.")

st.markdown("""
<div class="card-blue">
    <p style="margin: 0; font-size: 16px;">Este modelo matemático evalúa escenarios que van desde crisis profundas o guerras, hasta periodos de máxima expansión económica. Los datos demuestran el peso real del interés compuesto a lo largo del tiempo.</p>
</div>
""", unsafe_allow_html=True)

# Parámetros interactivos directamente en la barra lateral para que la pantalla quede limpia
with st.sidebar:
    st.title("📊 Panel de Datos")
    st.markdown("---")
    m3_cap = st.number_input("Aportación Inicial (€)", value=5000, step=500)
    m3_ap = st.number_input("Inversión mensual constante (€)", value=100, step=50)
    m3_anios = st.slider("Horizonte de Inversión (Años)", 5, 40, value=15)
    st.markdown("---")
    st.caption("Desarrollado por Raúl Fuster | Data Finance")

# ==========================================
# CÁLCULO MATEMÁTICO (Tu motor estadístico)
# ==========================================
meses = m3_anios * 12
np.random.seed(42)
sims = np.zeros((meses + 1, 200))
sims[0] = m3_cap
aportado = np.zeros(meses + 1)
aportado[0] = m3_cap
    
for m in range(1, meses + 1):
    sims[m] = sims[m-1] * (1 + np.random.normal(0.08 / 12, 0.15 / np.sqrt(12), 200)) + m3_ap
    aportado[m] = aportado[m-1] + m3_ap

p10 = np.percentile(sims, 10, axis=1)
p50 = np.percentile(sims, 50, axis=1)
p90 = np.percentile(sims, 90, axis=1)
t_eje = np.linspace(0, m3_anios, meses + 1)
    
# Mostrar KPIs arriba del gráfico
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("⛈️ Peor Escenario (Crisis/Mala suerte)", f"{p10[-1]:,.0f} €")
kpi2.metric("⛅ Escenario Probable (Objetivo)", f"{p50[-1]:,.0f} €")
kpi3.metric("☀️ Mejor Escenario (Economía a tope)", f"{p90[-1]:,.0f} €")
    
# Gráfico de Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=list(t_eje)+list(t_eje)[::-1], y=list(p90)+list(p10)[::-1], fill='toself', fillcolor='rgba(34, 197, 94, 0.15)', line=dict(color='rgba(255,255,255,0)'), name='Rango del Mercado Real'))
fig.add_trace(go.Scatter(x=t_eje, y=p50, mode='lines', name='Rentabilidad Mediana Esperada', line=dict(color='#22c55e', width=3)))
fig.add_trace(go.Scatter(x=t_eje, y=aportado, mode='lines', name='El Dinero Guardado en el Cajón', line=dict(color='#ef4444', width=2, dash='dash')))

fig.update_layout(template="simple_white", hovermode="x unified", height=500, margin=dict(t=20, b=50), yaxis_title="Patrimonio Acumulado (€)", legend=leyenda_movil)
st.plotly_chart(fig, use_container_width=True)
