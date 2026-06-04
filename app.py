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
    .card-lock { background-color: #f8fafc; border-left: 5px solid #64748b; padding: 20px; border-radius: 5px; margin-bottom: 20px; border: 1px solid #e2e8f0; }
    h1, h2, h3, h4 { color: #0f172a; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
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
    <p style="margin: 0; font-size: 16px;">Este modelo matemático evalúa escenarios reales que van desde crisis profundas o guerras, hasta periodos de máxima expansión económica. Los datos demuestran el peso real del interés compuesto a lo largo del tiempo.</p>
</div>
""", unsafe_allow_html=True)

# Parámetros interactivos en la barra lateral para la versión pública
with st.sidebar:
    st.title("📊 Panel de Datos")
    st.markdown("---")
    m3_cap = st.number_input("Aportación Inicial (€)", value=5000, step=500)
    m3_ap = st.number_input("Inversión mensual constante (€)", value=150, step=50) # Sincronizado con tus 150€ del Reel
    m3_anios = st.slider("Horizonte de Inversión (Años)", 5, 40, value=15)
    
    st.markdown("### 📉 Factor Macro")
    m3_inf = st.number_input("Inflación media anual (%)", value=2.5, step=0.1)
    
    st.markdown("---")
    st.caption("Desarrollado por Raúl Fuster | Data Finance")

# ==========================================
# ESTRUCTURA DE PESTAÑAS (Efecto Escaparate / FOMO)
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 1. Simulador Estocástico", 
    "🔒 2. Test de Salud Financiera", 
    "🔒 3. Optimización Fiscal (IRPF)",
    "🔒 4. Estrategia Operativa",
    "🔒 5. Informe Patrimonial (IA)"
])

# ==========================================
# CÁLCULO MATEMÁTICO (Motor del Simulador)
# ==========================================
meses = m3_anios * 12
np.random.seed(42)
sims = np.zeros((meses + 1, 200))
sims[0] = m3_cap
aportado = np.zeros(meses + 1)
aportado[0] = m3_cap
aportado_real = np.zeros(meses + 1)
aportado_real[0] = m3_cap

inf_mensual = (m3_inf / 100) / 12
    
for m in range(1, meses + 1):
    sims[m] = sims[m-1] * (1 + np.random.normal(0.08 / 12, 0.15 / np.sqrt(12), 200)) + m3_ap
    aportado[m] = aportado[m-1] + m3_ap
    aportado_real[m] = aportado_real[m-1] * (1 - inf_mensual) + m3_ap

p10 = np.percentile(sims, 10, axis=1)
p50 = np.percentile(sims, 50, axis=1)
p90 = np.percentile(sims, 90, axis=1)
t_eje = np.linspace(0, m3_anios, meses + 1)

# ------------------------------------------
# PESTAÑA 1: Módulo Abierto (Simulador Público)
# ------------------------------------------
with tab1:
    st.markdown("### 🏦 El coste de no hacer nada (Dinero en el banco)")
    banco1, banco2 = st.columns(2)
    banco1.metric("Dinero acumulado (Línea Roja)", f"{aportado[-1]:,.0f} €", "Lo que marcará el banco")
    
    perdida_inflacion = aportado[-1] - aportado_real[-1]
    banco2.metric("Poder adquisitivo real", f"{aportado_real[-1]:,.0f} €", f"-{perdida_inflacion:,.0f} € devorados por la inflación", delta_color="inverse")
    
    st.markdown("### 📈 El poder de la estrategia (Dinero invertido)")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("⛈️ Peor Escenario (Crisis/Mala suerte)", f"{p10[-1]:,.0f} €")
    kpi2.metric("⛅ Escenario Probable (Mediana)", f"{p50[-1]:,.0f} €")
    kpi3.metric("☀️ Mejor Escenario (Expansión)", f"{p90[-1]:,.0f} €")
    
    # Gráfico de Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(t_eje)+list(t_eje)[::-1], y=list(p90)+list(p10)[::-1], fill='toself', fillcolor='rgba(34, 197, 94, 0.15)', line=dict(color='rgba(255,255,255,0)'), name='Rango del Mercado Real'))
    fig.add_trace(go.Scatter(x=t_eje, y=p50, mode='lines', name='Rentabilidad Mediana Esperada', line=dict(color='#22c55e', width=3)))
    fig.add_trace(go.Scatter(x=t_eje, y=aportado, mode='lines', name='Dinero en el banco (Espejismo)', line=dict(color='#ef4444', width=2)))
    fig.add_trace(go.Scatter(x=t_eje, y=aportado_real, mode='lines', name='Valor real tras Inflación', line=dict(color='#f97316', width=2, dash='dot')))
    
    fig.update_layout(template="simple_white", hovermode="x unified", height=500, margin=dict(t=20, b=50), yaxis_title="Patrimonio Acumulado (€)", legend=leyenda_movil)
    st.plotly_chart(fig, width='stretch', config={'scrollZoom': False, 'displayModeBar': False, 'staticPlot': True})

# ------------------------------------------
# PESTAÑA 2: locked - Test de Salud Financiera
# ------------------------------------------
with tab2:
    st.markdown("### 🩺 Auditoría de Flujos de Caja e Índice de Salud")
    st.markdown("""
    <div class="card-lock">
        <h4 style="margin-top:0; color: #64748b;">🔒 Módulo Bloqueado</h4>
        <p style="font-size: 15px; color: #475569;">Esta sección realiza una auditoría completa de tus flujos de entrada y salida de capital. Calcula tu <b>Índice de Salud Financiera</b> exacto frente a métricas de eficiencia teórica, optimiza tus costes fijos y detecta tu capacidad real oculta de inversión mensual.</p>
        <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 15px 0;">
        <p style="font-size: 14px; font-style: italic; color: #0ea5e9;"><b>💡 Disponible exclusivamente en la Consultoría 1 a 1.</b> Escríbeme un mensaje privado en Instagram con la palabra <b>'CONSULTORÍA'</b> para auditar tus cuentas y desbloquear tu diagnóstico.</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------
# PESTAÑA 3: locked - Optimización Fiscal
# ------------------------------------------
with tab3:
    st.markdown("### ⚖️ Planificación Fiscal Avanzada (Neto post-IRPF)")
    st.markdown("""
    <div class="card-lock">
        <h4 style="margin-top:0; color: #64748b;">🔒 Módulo Bloqueado</h4>
        <p style="font-size: 15px; color: #475569;">Invertir en España sin estrategia fiscal es regalar tu rentabilidad. Este módulo calcula el impacto real del <b>impuesto del ahorro en el IRPF (escalas del 19% al 28%)</b> aplicado a los escenarios estocásticos de tu patrimonio acumulado según tu Comunidad Autónoma.</p>
        <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 15px 0;">
        <p style="font-size: 14px; font-style: italic; color: #0ea5e9;"><b>💡 Disponible exclusivamente en la Consultoría 1 a 1.</b> Si quieres calcular tu dinero neto real libre de impuestos, solicita tu análisis patrimonial por mensaje privado.</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------
# PESTAÑA 4: locked - Estrategia Operativa
# ------------------------------------------
with tab4:
    st.markdown("### 🧠 Vehículos de Inversión y Asset Allocation")
    st.markdown("""
    <div class="card-lock">
        <h4 style="margin-top:0; color: #64748b;">🔒 Módulo Bloqueado</h4>
        <p style="font-size: 15px; color: #475569;">El simulador te enseña <i>cuánto</i> puedes conseguir, pero en esta fase determinamos exactamente <b><i>dónde y cómo</i> ponerlo a trabajar</b>. Diseño de carteras diversificadas globalmente mediante Fondos Indexados de bajo coste y estrategias DCA (Dollar Cost Averaging) automatizadas.</p>
        <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 15px 0;">
        <p style="font-size: 14px; font-style: italic; color: #0ea5e9;"><b>💡 Disponible exclusivamente en la Consultoría 1 a 1.</b> Da el salto de los números a la acción real. Diseñemos tu cartera óptima según tu perfil de riesgo.</p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------
# PESTAÑA 5: locked - Exportar Informe IA
# ------------------------------------------
with tab5:
    st.markdown("### 📋 Generación del Informe de Planificación Patrimonial (IA)")
    st.markdown("""
    <div class="card-lock">
        <h4 style="margin-top:0; color: #64748b;">🔒 Módulo Bloqueado</h4>
        <p style="font-size: 15px; color: #475569;">Este módulo recopila todas tus variables cuantitativas y cualitativas de la sesión de consultoría y las procesa a través de un motor de Inteligencia Artificial para redactar tu <b>Informe Final estructurado en PDF</b>, completamente personalizado con tu plan de acción.</p>
        <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 15px 0;">
        <p style="font-size: 14px; font-style: italic; color: #0ea5e9;"><b>💡 Disponible exclusivamente en la Consultoría 1 a 1.</b> Llévate tu hoja de ruta financiera por escrito y blindada matemáticamente tras nuestra sesión privada.</p>
    </div>
    """, unsafe_allow_html=True)
