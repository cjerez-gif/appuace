import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Terminal Financiera | Broker Simulation",
    page_icon="📈",
    layout="wide"
)

# --- INYECCIÓN DE CSS ESTILO BROKER / TRADING ---
st.markdown("""
    <style>
        /* Importar fuente tipo Terminal */
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* Fondo general */
        .stApp {
            background-color: #0b0e14;
            color: #e1e6ed;
        }

        /* Títulos estilizados */
        h1, h2, h3 {
            color: #00e676 !important;
            text-shadow: 0 0 10px rgba(0, 230, 118, 0.2);
            letter-spacing: -0.5px;
        }

        /* Contenedores con efecto Cristal / Glassmorphism */
        div[data-testid="stMetric"], .stAlert {
            background: rgba(21, 25, 34, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 8px !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        /* Métricas numéricas estilo Terminal */
        div[data-testid="stMetricValue"] {
            font-size: 24px !important;
            color: #00e676 !important;
            font-weight: 700;
        }

        /* Botón de Ejecutar / Procesar estilo Orden de Compra */
        button[kind="primary"] {
            background: linear-gradient(90deg, #00e676 0%, #00b0ff 100%) !important;
            color: #000000 !important;
            font-weight: bold !important;
            border: none !important;
            box-shadow: 0 0 15px rgba(0, 230, 118, 0.4);
            transition: all 0.3s ease;
        }
        button[kind="primary"]:hover {
            transform: scale(1.02);
            box-shadow: 0 0 25px rgba(0, 230, 118, 0.7);
        }

        /* Borde para las cajas de noticias */
        .stAlert {
            border-left: 4px solid #ff9100 !important;
        }

        /* Tablas tipo Bloomberg */
        .dataframe {
            background-color: #151922 !important;
            color: #e1e6ed !important;
            border: 1px solid #2a2e39 !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE LAS ETAPAS Y NOTICIAS ---
ETAPAS_CONFIG = {
    1: {
        "titulo": "Etapa 1: Divergencia de Políticas y Rendimientos Reales",
        "noticias": (
            "⚡ [MACRO FEED - ETAPA 1]\n"
            "• FED 'HAWKISH': Incremento imprevisto en las tasas reales de interés.\n"
            "• S&P 500: Resiliencia técnica impulsada por balances corporativos de cobertura.\n"
            "• OPENAI: Shock de oferta inelástica tras firma de megacontrato institucional."
        ),
        "activos_disponibles": ["OpenAI", "Oro", "S&P 500"],
        "rendimientos": {"OpenAI": 0.35, "Oro": -0.15, "S&P 500": 0.02}
    },
    2: {
        "titulo": "Etapa 2: Curva Invertida y Especulación Líquida",
        "noticias": (
            "⚡ [MACRO FEED - ETAPA 2]\n"
            "• YIELD CURVE 2s10s: Inversión crítica; crece la prima de riesgo macro.\n"
            "• ANTHROPIC: Rumores de IPO inminente absorben volumen de liquidez del mercado.\n"
            "• COMMODITIES: Rotación de capital saliendo del Oro hacia activos de alta beta."
        ),
        "activos_disponibles": ["OpenAI", "Oro", "S&P 500"],
        "rendimientos": {"OpenAI": 0.20, "Oro": -0.05, "S&P 500": 0.08}
    },
    3: {
        "titulo": "Etapa 3: IPO de Anthropic y Efecto Desplazamiento",
        "noticias": (
            "⚡ [MACRO FEED - ETAPA 3]\n"
            "🔥 TRADING ALERT: Listing oficial de ANTHROPIC en bolsa con valuación récord.\n"
            "• CROWDING-OUT: Salida masiva de liquidez del S&P 500 para fondear la IPO.\n"
            "• OPENAI: Absorbe la volatilidad y mantiene tendencia lateral positiva.\n"
            "• ORO: Soporte técnico activado; frena presión de venta."
        ),
        "activos_disponibles": ["OpenAI", "Oro", "S&P 500", "Anthropic"],
        "rendimientos": {"OpenAI": 0.05, "Oro": 0.00, "S&P 500": -0.12, "Anthropic": 0.80}
    },
    4: {
        "titulo": "Etapa 4: Escalada Geopolítica y Shock de Suministros",
        "noticias": (
            "⚡ [MACRO FEED - ETAPA 4]\n"
            "• GEOPOLÍTICA: Tensiones en rutas de semiconductores afectan la cadena de IA.\n"
            "• SPECULATION: OpenAI y Anthropic disparan volatilidad implícita.\n"
            "• SAFE HAVEN: Entrada agresiva de capitales refugio hacia el Oro (+15%)."
        ),
        "activos_disponibles": ["OpenAI", "Oro", "S&P 500", "Anthropic"],
        "rendimientos": {"OpenAI": 0.25, "Oro": 0.15, "S&P 500": -0.06, "Anthropic": 0.40}
    },
    5: {
        "titulo": "Etapa 5: Reversión a la Media y Crisis de Rendimientos",
        "noticias": (
            "⚡ [MACRO FEED - ETAPA 5]\n"
            "🔴 MARKET CRASH: Auditorías revelan sobrevaloración estructural en Tech IA. Estallido de burbuja.\n"
            "• LIQUIDACIONES FORZOSAS: Ventas masivas en OpenAI y Anthropic (-55% / -65%).\n"
            "• DEFENSIVE ROTATION: El S&P 500 mitiga caídas; el Oro alcanza Máximo Histórico (+30%)."
        ),
        "activos_disponibles": ["OpenAI", "Oro", "S&P 500", "Anthropic"],
        "rendimientos": {"OpenAI": -0.55, "Oro": 0.30, "S&P 500": -0.02, "Anthropic": -0.65}
    }
}

# --- ESTADO EN STREAMLIT ---
if "etapa_actual" not in st.session_state:
    st.session_state.etapa_actual = 1

if "equipos" not in st.session_state:
    st.session_state.equipos = {
        1: {"nombre": "Despacho Alpha", "capital_actual": 100000.0, "historico_patrimonio": [100000.0], "historial_decisiones": []}
    }

if "precios_activos" not in st.session_state:
    st.session_state.precios_activos = {"OpenAI": 100.0, "Oro": 2000.0, "S&P 500": 450.0, "Anthropic": 500.0}

if "historico_precios" not in st.session_state:
    st.session_state.historico_precios = {
        "Etapa": [0], "OpenAI": [100.0], "Oro": [2000.0], "S&P 500": [450.0], "Anthropic": [np.nan]
    }

if "decisiones_etapa_actual" not in st.session_state:
    st.session_state.decisiones_etapa_actual = {}

# --- FUNCIONES DE LÓGICA ---
def procesar_etapa():
    etapa = st.session_state.etapa_actual
    config = ETAPAS_CONFIG[etapa]
    rendimientos = config["rendimientos"]
    activos_disp = config["activos_disponibles"]

    for id_eq, eq in st.session_state.equipos.items():
        if id_eq not in st.session_state.decisiones_etapa_actual:
            if eq["historial_decisiones"]:
                ultimo_porto = eq["historial_decisiones"][-1]["Pesos"]
                def_portfolio = {}
                suma_h = 0
                for activo in activos_disp:
                    v = ultimo_porto.get(activo, 0)
                    def_portfolio[activo] = v
                    suma_h += v

                if suma_h != 100:
                    dif = 100 - suma_h
                    comodin = "S&P 500" if "S&P 500" in activos_disp else activos_disp[0]
                    def_portfolio[comodin] = def_portfolio.get(comodin, 0) + dif
            else:
                def_portfolio = {a: 0 for a in activos_disp}
                def_portfolio["S&P 500" if "S&P 500" in activos_disp else activos_disp[0]] = 100

            st.session_state.decisiones_etapa_actual[id_eq] = def_portfolio

    for id_eq, pesos in st.session_state.decisiones_etapa_actual.items():
        eq = st.session_state.equipos[id_eq]
        cap_previo = eq["capital_actual"]
        ganancia = 0
        detalles = {}

        for activo, peso in pesos.items():
            monto = cap_previo * (peso / 100.0)
            rend = rendimientos.get(activo, 0.0)
            nuevo_monto = monto * (1 + rend)
            ganancia += (nuevo_monto - monto)
            detalles[activo] = {"Invertido": monto, "Rendimiento": rend * 100, "Resultado": nuevo_monto}

        eq["capital_actual"] = cap_previo + ganancia
        eq["historico_patrimonio"].append(eq["capital_actual"])
        eq["historial_decisiones"].append({
            "Etapa": etapa, "Capital Inicial": cap_previo, "Pesos": pesos.copy(), "Capital Final": eq["capital_actual"], "Detalles": detalles
        })

    for activo in ["OpenAI", "Oro", "S&P 500", "Anthropic"]:
        if etapa < 3 and activo == "Anthropic":
            st.session_state.precios_activos[activo] = 500.0
        else:
            r = rendimientos.get(activo, 0.0)
            st.session_state.precios_activos[activo] *= (1 + r)

    st.session_state.historico_precios["Etapa"].append(etapa)
    st.session_state.historico_precios["OpenAI"].append(st.session_state.precios_activos["OpenAI"])
    st.session_state.historico_precios["Oro"].append(st.session_state.precios_activos["Oro"])
    st.session_state.historico_precios["S&P 500"].append(st.session_state.precios_activos["S&P 500"])
    
    if etapa >= 3:
        st.session_state.historico_precios["Anthropic"].append(st.session_state.precios_activos["Anthropic"])
    else:
        st.session_state.historico_precios["Anthropic"].append(np.nan)

    st.session_state.decisiones_etapa_actual.clear()
    st.session_state.etapa_actual += 1

def reiniciar_juego():
    st.session_state.etapa_actual = 1
    st.session_state.equipos = {
        1: {"nombre": "Despacho Alpha", "capital_actual": 100000.0, "historico_patrimonio": [100000.0], "historial_decisiones": []}
    }
    st.session_state.precios_activos = {"OpenAI": 100.0, "Oro": 2000.0, "S&P 500": 450.0, "Anthropic": 500.0}
    st.session_state.historico_precios = {
        "Etapa": [0], "OpenAI": [100.0], "Oro": [2000.0], "S&P 500": [450.0], "Anthropic": [np.nan]
    }
    st.session_state.decisiones_etapa_actual = {}

# --- GRÁFICOS ESTILO TRADINGVIEW / DARK ---
def render_graficos():
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 3.8))
    
    # Transparencia para acoplar al tema
    fig.patch.set_facecolor('#0b0e14')
    ax1.set_facecolor('#151922')
    ax2.set_facecolor('#151922')

    etapas = st.session_state.historico_precios["Etapa"]

    p_openai = (np.array(st.session_state.historico_precios["OpenAI"]) / 100.0) * 100
    p_oro = (np.array(st.session_state.historico_precios["Oro"]) / 2000.0) * 100
    p_sp = (np.array(st.session_state.historico_precios["S&P 500"]) / 450.0) * 100
    p_anthropic = (np.array(st.session_state.historico_precios["Anthropic"]) / 500.0) * 100

    # Colores Neón Trading
    ax1.plot(etapas, p_openai, label="OpenAI", marker='o', color='#b388ff', linewidth=2)
    ax1.plot(etapas, p_oro, label="Oro", marker='o', color='#ffd700', linewidth=2)
    ax1.plot(etapas, p_sp, label="S&P 500", marker='o', color='#00b0ff', linewidth=2)
    ax1.plot(etapas, p_anthropic, label="Anthropic", marker='s', linestyle='--', color='#ff5252', linewidth=2)
    
    ax1.set_title("EVOLUCIÓN DE PRECIOS (BASE 100)", fontsize=10, color='#00e676', fontweight='bold')
    ax1.grid(True, linestyle=':', alpha=0.3, color='#2a2e39')
    ax1.legend(facecolor='#151922', edgecolor='#2a2e39', fontsize=8)

    # Curvas de Equipos
    colores_equipos = ['#00e676', '#ff9100', '#00b0ff', '#e040fb', '#ffd600', '#ff5252']
    for idx, (id_eq, eq) in enumerate(st.session_state.equipos.items()):
        c = colores_equipos[idx % len(colores_equipos)]
        ax2.plot(range(len(eq["historico_patrimonio"])), eq["historico_patrimonio"], marker='D', linewidth=2, label=eq["nombre"], color=c)

    ax2.axhline(y=100000, color='#787b86', linestyle='--', alpha=0.5, label="Cap. Base")
    ax2.set_title("VALOR DE PORTAFOLIOS (USD)", fontsize=10, color='#00e676', fontweight='bold')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))
    ax2.grid(True, linestyle=':', alpha=0.3, color='#2a2e39')
    ax2.legend(facecolor='#151922', edgecolor='#2a2e39', fontsize=8)

    plt.tight_layout()
    return fig

# --- HEADER TERMINAL ---
st.title("📟 TRADING TERMINAL | PORTFOLIO SIMULATOR")

# Ticker de precios actualizados arriba
col_t1, col_t2, col_t3, col_t4 = st.columns(4)
col_t1.metric("OPENAI", f"${st.session_state.precios_activos['OpenAI']:.2f}")
col_t2.metric("ORO", f"${st.session_state.precios_activos['Oro']:.2f}")
col_t3.metric("S&P 500", f"${st.session_state.precios_activos['S&P 500']:.2f}")
col_t4.metric("ANTHROPIC", f"${st.session_state.precios_activos['Anthropic']:.2f}" if st.session_state.etapa_actual >= 3 else "NO LISTADO")

# BARRA LATERAL
with st.sidebar:
    st.markdown("### ⚙️ TERMINAL CONTROL")
    if st.button("⚠️ REINICIAR SESIÓN", use_container_width=True):
        reiniciar_juego()
        st.rerun()

    st.markdown("---")
    st.markdown("### 👥 MESAS DE TRADING")
    num_equipos = st.slider("Mesas Activas:", 1, 10, len(st.session_state.equipos))
    
    if num_equipos > len(st.session_state.equipos):
        for i in range(1, num_equipos + 1):
            if i not in st.session_state.equipos:
                st.session_state.equipos[i] = {
                    "nombre": f"Mesa {i}", "capital_actual": 100000.0, "historico_patrimonio": [100000.0], "historial_decisiones": []
                }
    elif num_equipos < len(st.session_state.equipos):
        for i in list(st.session_state.equipos.keys()):
            if i > num_equipos:
                st.session_state.equipos.pop(i, None)
                st.session_state.decisiones_etapa_actual.pop(i, None)

    eq_sel = st.selectbox("Configurar Mesa:", options=list(st.session_state.equipos.keys()), format_func=lambda x: st.session_state.equipos[x]["nombre"])
    nuevo_nombre = st.text_input("Alias Comercial:", key="input_nuevo_nombre")
    if st.button("Actualizar Nombre"):
        if nuevo_nombre.strip():
            st.session_state.equipos[eq_sel]["nombre"] = nuevo_nombre.strip()
            st.rerun()

# PANEL PRINCIPAL: GRÁFICOS
st.pyplot(render_graficos())

# FIN DEL JUEGO / LEADERBOARD
if st.session_state.etapa_actual > 5:
    st.balloons()
    st.subheader("🏆 BOARD DE RENDIMIENTOS FINALES")
    
    res_data = []
    for id_eq, eq in sorted(st.session_state.equipos.items(), key=lambda x: x[1]['capital_actual'], reverse=True):
        rend = ((eq['capital_actual'] - 100000.0) / 100000.0) * 100
        res_data.append({
            "Mesa / Fondo": eq["nombre"],
            "Cap. Inicial": "$100,000.00",
            "Cap. Final": f"${eq['capital_actual']:,.2f}",
            "ROI Total": f"{rend:+.2f}%"
        })
    st.table(pd.DataFrame(res_data))

else:
    # PANEL DE OPERACIONES
    config_etapa = ETAPAS_CONFIG[st.session_state.etapa_actual]
    
    st.markdown(f"### 📍 {config_etapa['titulo'].upper()}")
    st.warning(config_etapa["noticias"])

    st.markdown("### 📑 ORDEN DE ASIGNACIÓN DE CAPITAL")
    
    c1, c2 = st.columns([1, 2.5])
    with c1:
        equipo_sel_id = st.selectbox(
            "Mesa a Operar:",
            options=list(st.session_state.equipos.keys()),
            format_func=lambda x: st.session_state.equipos[x]["nombre"]
        )

    activos = config_etapa["activos_disponibles"]
    valores_defecto = {}
    if equipo_sel_id in st.session_state.decisiones_etapa_actual:
        valores_defecto = st.session_state.decisiones_etapa_actual[equipo_sel_id]
    elif st.session_state.equipos[equipo_sel_id]["historial_decisiones"]:
        valores_defecto = st.session_state.equipos[equipo_sel_id]["historial_decisiones"][-1]["Pesos"]

    pesos_input = {}
    with c2:
        cols = st.columns(len(activos))
        for idx, activo in enumerate(activos):
            val_init = valores_defecto.get(activo, 0)
            pesos_input[activo] = cols[idx].number_input(
                f"% {activo}", min_value=0, max_value=100, step=5, value=val_init, key=f"{equipo_sel_id}_{activo}"
            )

    suma_porcentajes = sum(pesos_input.values())
    st.caption(f"**MARGEN ASIGNADO:** `{suma_porcentajes}%` / `100%`")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("💾 CONFIRMAR ORDEN DE PORTAFOLIO", use_container_width=True):
            if suma_porcentajes != 100:
                st.error(f"❌ ERROR DE MARGEN: La suma de pesos debe ser 100%. Actual: {suma_porcentajes}%")
            else:
                st.session_state.decisiones_etapa_actual[equipo_sel_id] = pesos_input
                st.success(f"✅ Orden confirmada para: {st.session_state.equipos[equipo_sel_id]['nombre']}")

    # TRACKER DE OPERACIONES ENVIADAS
    listos = [st.session_state.equipos[i]['nombre'] for i in st.session_state.decisiones_etapa_actual.keys()]
    pendientes = [st.session_state.equipos[i]['nombre'] for i in st.session_state.equipos.keys() if i not in st.session_state.decisiones_etapa_actual]

    st.markdown(f"**ORDENES CONFIRMADAS:** `{', '.join(listos) if listos else 'NINGUNA'}` | **PENDIENTES:** `{', '.join(pendientes) if pendientes else 'NINGUNA'}`")

    st.markdown("---")
    if st.button("⚡ EJECUTAR ETAPA Y PROCESAR MERCADO", type="primary", use_container_width=True):
        procesar_etapa()
        st.rerun()
