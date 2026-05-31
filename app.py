import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ==========================================
# CONFIGURACIÓN Y ESTILOS
# ==========================================
st.set_page_config(page_title="RFData - Optimiza tu Dinero", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .card-red { background-color: #fef2f2; border-left: 5px solid #ef4444; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
    .card-green { background-color: #f0fdf4; border-left: 5px solid #22c55e; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
    .card-blue { background-color: #f0f9ff; border-left: 5px solid #0ea5e9; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
    .card-yellow { background-color: #fffbeb; border-left: 5px solid #f59e0b; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
    h1, h2, h3 { color: #0f172a; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .metric-valor { font-size: 2rem; font-weight: bold; margin: 0; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# MEMORIA PERMANENTE DE LA APLICACIÓN
# ==========================================
def inicializar_estado(clave, valor_inicial):
    if clave not in st.session_state:
        st.session_state[clave] = valor_inicial

inicializar_estado('m1_ingresos', 2000)
inicializar_estado('m1_fijos', 1000)
inicializar_estado('m1_ocio', 500)
inicializar_estado('m1_deuda', 100)

inicializar_estado('m2_cap', 10000)
inicializar_estado('m2_inf', 3.0)
inicializar_estado('m2_anios', 15)

inicializar_estado('m3_cap', 5000)
inicializar_estado('m3_ap', 200)
inicializar_estado('m3_anios', 20)

leyenda_movil = dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5)

# ==========================================
# NAVEGACIÓN LATERAL
# ==========================================
with st.sidebar:
    st.title("📊 RFData")
    st.caption("Programa Práctico: Optimiza tu Dinero")
    st.markdown("---")
    menu = st.radio(
        "Tu Ruta de Aprendizaje:",
        ["📍 Presentación del Programa",
         "🩺 1. Test de Salud Financiera",
         "🗺️ 2. El Ladrón Invisible y tu Plan",
         "📈 3. Inversión con Sentido Común",
         "🧠 4. Psicología y Plan de Acción"]
    )
    st.markdown("---")
    st.markdown("💡 *Al terminar estas 4 fases, tendrás un nivel de gestión patrimonial superior al 90% de la población.*")

# ==========================================
# MÓDULOS DE LA APLICACIÓN
# ==========================================

if menu == "📍 Presentación del Programa":
    st.title("Optimiza tus finanzas y diseña tu libertad")
    st.markdown("""
<div class="card-blue">
    <h3 style="margin-top:0;">Bienvenido a tu transformación financiera</h3>
    <p style="font-size: 18px;">¿Sabes que debes invertir pero no sabes por dónde empezar? ¿Tienes dudas sobre si estás gestionando bien tu dinero hoy? Este no es un curso teórico más. Es un simulador interactivo.</p>
    <p style="font-size: 16px;"><b>El Método RFData:</b></p>
    <ul>
        <li><b>Fase 1:</b> Mediremos tu salud financiera exacta y detectaremos fugas de capital.</li>
        <li><b>Fase 2:</b> Trazaremos un plan matemático hacia tus objetivos vitales.</li>
        <li><b>Fase 3:</b> Te enseñaremos la receta de inversión a largo plazo que la estadística demuestra que funciona. Sin cuentos, promesas falsas ni pelotazos.</li>
        <li><b>Fase 4:</b> Estableceremos las reglas psicológicas para mantener el éxito en el tiempo.</li>
    </ul>
    <p style="font-size: 16px;"><i>Todo el progreso se guarda automáticamente. Vamos a sentar unas bases sólidas.</i></p>
</div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
elif menu == "🩺 1. Test de Salud Financiera":
    st.title("Fase 1: Conoce tu punto de partida")
    
    st.markdown("Antes de correr, hay que saber caminar. Priorizaremos lo importante midiendo cómo distribuyes tus ingresos frente al método más eficiente de ahorro: **La Regla 50/30/20**.")
        
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Ingresa tus datos actuales")
        m1_ingresos = st.number_input("Nómina Neta Mensual (€)", value=st.session_state.m1_ingresos, step=100)
        st.session_state.m1_ingresos = m1_ingresos
        
        m1_fijos = st.number_input("Supervivencia (Casa, luz, súper) (€)", value=st.session_state.m1_fijos, step=50)
        st.session_state.m1_fijos = m1_fijos
        
        m1_ocio = st.number_input("Calidad de Vida (Ocio, cenas, ropa) (€)", value=st.session_state.m1_ocio, step=50)
        st.session_state.m1_ocio = m1_ocio
        
        m1_deuda = st.number_input("Préstamos y Deudas (€)", value=st.session_state.m1_deuda, step=50)
        st.session_state.m1_deuda = m1_deuda
    
    with col2:
        total = st.session_state.m1_ingresos
        fijos = st.session_state.m1_fijos
        ocio = st.session_state.m1_ocio
        deuda = st.session_state.m1_deuda
        
        if total > 0:
            p_fijos = ((fijos + deuda) / total) * 100
            p_ocio = (ocio / total) * 100
            ahorro_real_euros = total - fijos - ocio - deuda
            p_ahorro = (ahorro_real_euros / total) * 100
            
            # CÁLCULO DEL SCORE DE SALUD FINANCIERA (0-100)
            score = 100
            if p_fijos > 50: score -= (p_fijos - 50) * 1.5
            if p_ocio > 30: score -= (p_ocio - 30) * 1.5
            if p_ahorro < 20: score -= (20 - p_ahorro) * 2
            score = max(0, min(100, score))
            
            color_score = "#22c55e" if score >= 80 else "#f59e0b" if score >= 50 else "#ef4444"
            
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background-color: white; border-radius: 10px; border: 2px solid {color_score}; margin-bottom: 20px;">
                <h2 style="margin: 0; color: #334155;">Tu Puntuación de Salud Financiera</h2>
                <h1 style="margin: 0; font-size: 3rem; color: {color_score};">{score:.0f} / 100</h1>
            </div>
            """, unsafe_allow_html=True)
            
            categorias = ['Gastos Fijos + Deuda', 'Ocio y Deseos', 'Ahorro para Inversión']
            obj_optimo = [50, 30, 20]
            gasto_real = [p_fijos, p_ocio, max(0, p_ahorro)]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Tu Realidad Actual', x=categorias, y=gasto_real, marker_color='#ef4444', text=[f"{v:.1f}%" for v in gasto_real], textposition='auto'))
            fig.add_trace(go.Bar(name='El Equilibrio Perfecto', x=categorias, y=obj_optimo, marker_color='#22c55e', text=[f"{v}%" for v in obj_optimo], textposition='auto'))
            fig.update_layout(barmode='group', template="simple_white", height=300, margin=dict(t=10, b=50), yaxis_title="% de tus ingresos", legend=leyenda_movil)
            st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
elif menu == "🗺️ 2. El Ladrón Invisible y tu Plan":
    st.title("Fase 2: Por qué ahorrar no es suficiente")
    
    st.markdown("Ahora que sabemos cuánto puedes apartar al mes, vamos a fijar un rumbo. El primer paso es entender que el dinero parado en el banco es dinero perdiendo valor por culpa de la **Inflación**.")

    col1, col2 = st.columns([1, 2.5])
    
    with col1:
        st.markdown("### Proyección a Futuro")
        m2_cap = st.number_input("Tus ahorros actuales (€)", value=st.session_state.m2_cap, step=1000)
        st.session_state.m2_cap = m2_cap
        
        m2_inf = st.slider("Inflación Estimada (%)", 0.0, 10.0, value=float(st.session_state.m2_inf), step=0.5)
        st.session_state.m2_inf = m2_inf
        
        m2_anios = st.slider("Años hacia tu meta", 1, 30, value=st.session_state.m2_anios)
        st.session_state.m2_anios = m2_anios
        
    with col2:
        cap = st.session_state.m2_cap
        inf = st.session_state.m2_inf
        anios = st.session_state.m2_anios
        
        t = np.arange(0, anios + 1)
        val_nominal = np.full(len(t), cap)
        val_banco = cap / ((1 + inf/100)**t)
        val_mercado = cap * ((1 + 0.10)**t) 
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t, y=val_nominal, mode='lines', name='El saldo en tu App bancaria', line=dict(color='#94a3b8', dash='dash')))
        fig.add_trace(go.Scatter(x=t, y=val_banco, mode='lines', name='Lo que realmente podrás comprar (Inflación)', line=dict(color='#ef4444', width=3)))
        fig.add_trace(go.Scatter(x=t, y=val_mercado, mode='lines', name='Si inviertes (Crecimiento Histórico Medio)', line=dict(color='#22c55e', width=3)))
        fig.update_layout(template="simple_white", hovermode="x unified", height=400, margin=dict(t=10, b=50), yaxis_title="Euros (€)", legend=leyenda_movil)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div class="card-yellow">
            <h4 style="margin-top:0;">El coste de la inacción</h4>
            <p style="margin-bottom:0;">En {anios} años, el banco te dirá que sigues teniendo {cap}€, pero en el mundo real equivaldrán a <b>{val_banco[-1]:,.0f}€</b>. Necesitamos una estrategia para saltar a la línea verde.</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
elif menu == "📈 3. Inversión con Sentido Común":
    st.title("Fase 3: Nuestra estrategia a largo plazo")
    
    st.markdown("Aquí no encontrarás métodos milagrosos. Invertir de forma inteligente requiere tocar de pies en el suelo. Usamos la **Estadística (Simulación de Montecarlo)** para mostrarte 200 futuros posibles basados en el comportamiento real de la economía mundial.")
        
    col1, col2 = st.columns([1, 2.5])
    with col1:
        st.markdown("### Simula tu Estrategia")
        m3_cap = st.number_input("Aportación Inicial (€)", value=st.session_state.m3_cap, step=500)
        st.session_state.m3_cap = m3_cap
        
        # Le sugerimos automáticamente el ahorro que le salió en la Fase 1
        ahorro_sugerido = st.session_state.m1_ingresos - st.session_state.m1_fijos - st.session_state.m1_ocio - st.session_state.m1_deuda
        m3_ap = st.number_input("Inversión mensual constante (€)", value=int(ahorro_sugerido) if ahorro_sugerido > 0 else 100, step=50)
        st.session_state.m3_ap = m3_ap
        
        m3_anios = st.slider("Horizonte de Inversión (Años)", 5, 40, value=st.session_state.m3_anios)
        st.session_state.m3_anios = m3_anios
        
    with col2:
        cap = st.session_state.m3_cap
        ap = st.session_state.m3_ap
        anios = st.session_state.m3_anios
        
        meses = anios * 12
        np.random.seed(42)
        sims = np.zeros((meses + 1, 200))
        sims[0] = cap
        aportado = np.zeros(meses + 1)
        aportado[0] = cap
        
        for m in range(1, meses + 1):
            sims[m] = sims[m-1] * (1 + np.random.normal(0.08 / 12, 0.15 / np.sqrt(12), 200)) + ap
            aportado[m] = aportado[m-1] + ap

        p10 = np.percentile(sims, 10, axis=1)
        p50 = np.percentile(sims, 50, axis=1)
        p90 = np.percentile(sims, 90, axis=1)
        t_eje = np.linspace(0, anios, meses + 1)
        
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("⛈️ Tormenta (Peor suerte)", f"{p10[-1]:,.0f} €")
        kpi2.metric("⛅ Lo Probable (El objetivo)", f"{p50[-1]:,.0f} €")
        kpi3.metric("☀️ Cielo Despejado", f"{p90[-1]:,.0f} €")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(t_eje)+list(t_eje)[::-1], y=list(p90)+list(p10)[::-1], fill='toself', fillcolor='rgba(34, 197, 94, 0.15)', line=dict(color='rgba(255,255,255,0)'), name='Rango del Mercado Real'))
        fig.add_trace(go.Scatter(x=t_eje, y=p50, mode='lines', name='Rentabilidad Mediana Esperada', line=dict(color='#22c55e', width=3)))
        fig.add_trace(go.Scatter(x=t_eje, y=aportado, mode='lines', name='El Dinero Guardado en el Cajón', line=dict(color='#ef4444', width=2, dash='dash')))
        fig.update_layout(template="simple_white", hovermode="x unified", height=450, margin=dict(t=10, b=50), yaxis_title="Patrimonio Acumulado (€)", legend=leyenda_movil)
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
elif menu == "🧠 4. Psicología y Plan de Acción":
    st.title("Fase 4: Claves del Éxito y Tu Rutina Financiera")
    
    st.markdown("""
    Optimizar el dinero hoy es fácil; mantener la disciplina durante años es el verdadero reto. La psicología y la sistematización son el 90% del éxito en las finanzas personales.
    """)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
<div style="background-color: white; padding: 30px; border-radius: 10px; border-top: 5px solid #0ea5e9; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
    <h3 style="margin-top:0; color: #0f172a;">Tus 3 Mandamientos Financieros</h3>
    <ol style="font-size: 16px; line-height: 1.8; color: #475569;">
        <li><b>Págate a ti mismo primero:</b> No ahorres lo que te sobra después de gastar. Gasta lo que te sobra después de haber apartado tus <b>{st.session_state.m3_ap}€</b>.</li>
        <li><b>Las crisis son tu supermercado:</b> Mantén tu inversión mensual aunque el mundo entre en pánico. Es cuando comprarás más barato y garantizarás el crecimiento futuro.</li>
        <li><b>Aleja las emociones:</b> Una vez automatizado el sistema, revisa tu cuenta de inversión máximo 2 veces al año. El aburrimiento es el mejor indicador de una buena inversión.</li>
    </ol>
</div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
<div style="background-color: white; padding: 30px; border-radius: 10px; border-top: 5px solid #22c55e; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
    <h3 style="margin-top:0; color: #0f172a;">Tu Plan de Acción (Hoy)</h3>
    <p style="font-size: 16px; color: #475569;">Basado en tu diagnóstico, estos son tus pasos exactos:</p>
    <ul style="font-size: 16px; line-height: 1.8; color: #475569;">
        <li>Abre tu cuenta en un Fondo Indexado de bajo coste.</li>
        <li>Entra en la app de tu banco actual.</li>
        <li>Configura una <b>Transferencia Automática Permanente</b> de <b>{st.session_state.m3_ap}€</b> a tu cuenta de inversión.</li>
        <li>Fija la fecha de ejecución para el <b>día 2 de cada mes</b>.</li>
        <li><b>¡Enhorabuena! Has automatizado tu camino hacia la libertad financiera.</b></li>
    </ul>
</div>
        """, unsafe_allow_html=True)