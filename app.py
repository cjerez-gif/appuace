import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Stonks 🚀 | Simulador de Inversiones",
    page_icon="🚀",
    layout="wide"
)

# --- INYECCIÓN DE CSS ESTILO BROKER / TRADING ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'JetBrains Mono', monospace !important;
        }

        .stApp {
            background-color: #0b0e14;
            color: #e1e6ed;
        }

        h1, h2, h3 {
            color: #00e676 !important;
            text-shadow: 0 0 10px rgba(0, 230, 118, 0.2);
            letter-spacing: -0.5px;
        }

        div[data-testid="stMetric"], .stAlert {
            background: rgba(21, 25, 34, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 8px !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        div[data-testid="stMetricValue"] {
            font-size: 24px !important;
            color: #00e676 !important;
            font-weight: 700;
        }

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

        .stAlert {
            border-left: 4px solid #00e676 !important;
        }

        .dataframe {
            background-color: #151922 !important;
            color: #e1e6ed !important;
            border: 1px solid #2a2e39 !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- NOTICIAS SUGERENTES Y EVENTOS SURREALISTAS (ESTILO BLUMBERG) ---
ETAPAS_CONFIG = {
    1: {
        "noticias": (
            "📺 NOTICIAS FINANCIERAS CON BLUMBERG\n\n"
            "• 🏦 La Reserva Federal adopta una postura 'hawkish' ajustando liquidez en los bancos para frenar la inflación.\n"
            "• 💼 Informes corporativos de consumo e industria muestran márgenes estables pero sin catalizadores de crecimiento.\n"
            "• 🤖 Rumores de alianzas estratégicas en Silicon Valley anticipan el despliegue de infraestructura de IA de última generación."
        ),
        "activos_disponibles": ["OpenAI", "Oro", "S&P 500"],
        "rendimientos": {"OpenAI": 0.35, "Oro": -0.15, "S&P 500": 0.02}
    },
    2: {
        "noticias": (
            "📺 NOTICIAS FINANCIERAS CON BLUMBERG\n\n"
            "• ⚠️ Curva de rendimiento de bonos del tesoro sugiere desaceleración en el crédito comercial e industrial.\n"
            "• 🚀 Un laboratorio rival de modelos masivos de lenguaje contrata bancos de inversión para alistar su debut en bolsa.\n"
            "• 📉 Salidas registradas de capital en bóvedas de resguardo físico hacia mercados de mayor volatilidad."
        ),
        "activos_disponibles": ["OpenAI", "Oro", "S&P 500"],
        "rendimientos": {"OpenAI": 0.20, "Oro": -0.05, "S&P 500": 0.08}
    },
    3: {
        "noticias": (
            "📺 NOTICIAS FINANCIERAS CON BLUMBERG\n\n"
            "🔔 APERTURA DE MERCADO: Anthropic debuta oficialmente en la bolsa de valores tras meses de especulación.\n"
            "• 💸 Rotación institucional masiva: Administradores de fondos reequilibran posiciones vendiendo índices diversificados para acumular la nueva IPO.\n"
            "• 📊 Empresas consolidadas del sector corporativo muestran volúmenes de transacción dentro de promedios históricos.\n"
            "• 🟡 Mercado de metales preciosos registra baja liquidez y movimiento lateral."
        ),
        "activos_disponibles": ["OpenAI", "Oro", "S&P 500", "Anthropic"],
        "rendimientos": {"OpenAI": 0.05, "Oro": 0.00, "S&P 500": -0.12, "Anthropic": 0.80}
    },
    4: {
        "noticias": (
            "📺 NOTICIAS FINANCIERAS CON BLUMBERG\n\n"
            "🚨 ÚLTIMA HORA | EVENTO CISNE NEGRO EN SECTOR DE DEFENSA:\n"
            "• 🤖 Reportes de inteligencia confirman que un agente autónomo de IA instalado en un dron militar sufrió una falla lógica severa y atacó a las fuerzas aliadas dentro de un batallón.\n"
            "• 💀 Gobiernos convocan a reuniones de emergencia para debatir regulaciones extremas e interrupciones operativas al sector tecnológico.\n"
            "• 🛡️ Pánico generalizado en mercados internacionales; inversionistas buscan coberturas físicas de supervivencia e insumos primarios."
        ),
        "activos_disponibles": ["OpenAI", "Oro", "S&P 500", "Anthropic"],
        "rendimientos": {"OpenAI": 0.25, "Oro": 0.15, "S&P 500": -0.06, "Anthropic": 0.40}
    },
    5: {
        "noticias": (
            "📺 NOTICIAS FINANCIERAS CON BLUMBERG\n\n"
            "• 📊 Auditorías contables independientes revelan que los costos operativos de infraestructura superan por mucho los retornos reales por suscripción en firmas tech.\n"
            "• 🔴 Fondos de cobertura reducen abruptamente la exposición en activos con ratios P/E desproporcionados.\n"
            "• 🏛️ Sectores defensivos tradicionales y reservas tangibles reciben flujos en busca de preservación patrimonial."
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
        1: {"nombre": "Equipo Alpha", "capital_actual": 100000.0, "historico_patrimonio": [100000.0], "historial_decisiones": []}
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
        1: {"nombre": "Equipo Alpha", "capital_actual": 100000.0, "historico_patrimonio": [100000.0], "historial_decisiones": []}
    }
    st.session_state.precios_activos = {"OpenAI": 100.0, "Oro": 2000.0, "S&P 500": 450.0, "Anthropic": 500.0}
    st.session_state.historico_precios = {
        "Etapa": [0], "OpenAI": [100.0], "Oro": [2000.0], "S&P 500": [450.0], "Anthropic": [np.nan]
    }
    st.session_state.decisiones_etapa_actual = {}

# --- GENERADOR DE MOVIMIENTO / FLUCTUACIÓN REALISTA DE PRECIOS ---
def generar_movimiento_continuo(valores_etapas, seed=42):
    np.random.seed(seed)
    puntos_x = []
    puntos_y = []
    subpasos = 10

    if len(valores_etapas) == 1:
        base = valores_etapas[0]
        if np.isnan(base):
            return [0], [np.nan]
        puntos_x = np.linspace(0, 0.2, subpasos)
        ruido = np.random.normal(0, 0.01, subpasos)
        puntos_y = base * (1 + ruido)
        puntos_y[0] = base
        return puntos_x, puntos_y

    for i in range(len(valores_etapas) - 1):
        v_inicio = valores_etapas[i]
        v_fin = valores_etapas[i + 1]

        if np.isnan(v_inicio) and np.isnan(v_fin):
            x_segmento = np.linspace(i, i + 1, subpasos)
            y_segmento = [np.nan] * subpasos
        elif np.isnan(v_inicio) and not np.isnan(v_fin):
            x_segmento = np.linspace(i, i + 1, subpasos)
            y_segmento = np.linspace(v_fin * 0.8, v_fin, subpasos) + np.random.normal(0, v_fin * 0.02, subpasos)
            y_segmento[-1] = v_fin
        else:
            x_segmento = np.linspace(i, i + 1, subpasos)
            tendencia = np.linspace(v_inicio, v_fin, subpasos)
            onda = np.sin(np.linspace(0, np.pi * 2, subpasos)) * (v_fin - v_inicio) * 0.15
            ruido = np.random.normal(0, abs(v_fin - v_inicio) * 0.03 + 0.5, subpasos)
            y_segmento = tendencia + onda + ruido
            y_segmento[0] = v_inicio
            y_segmento[-1] = v_fin

        if i > 0:
            x_segmento = x_segmento[1:]
            y_segmento = y_segmento[1:]

        puntos_x.extend(x_segmento)
        puntos_y.extend(y_segmento)

    return puntos_x, puntos_y

# --- RENDERIZADO DE GRÁFICOS ---
def render_graficos():
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.2))
    
    fig.patch.set_facecolor('#0b0e14')
    ax1.set_facecolor('#11151c')
    ax2.set_facecolor('#11151c')

    etapas = st.session_state.historico_precios["Etapa"]

    p_openai_raw = (np.array(st.session_state.historico_precios["OpenAI"]) / 100.0) * 100
    p_oro_raw = (np.array(st.session_state.historico_precios["Oro"]) / 2000.0) * 100
    p_sp_raw = (np.array(st.session_state.historico_precios["S&P 500"]) / 450.0) * 100
    p_anthropic_raw = (np.array(st.session_state.historico_precios["Anthropic"]) / 500.0) * 100

    config_activos = [
        ("OpenAI", p_openai_raw, '#b388ff', 101),
        ("Oro", p_oro_raw, '#ffd700', 102),
        ("S&P 500", p_sp_raw, '#00b0ff', 103),
        ("Anthropic", p_anthropic_raw, '#ff5252', 104)
    ]

    for nombre, valores, color, seed in config_activos:
        x_smooth, y_smooth = generar_movimiento_continuo(valores, seed=seed)
        ax1.plot(x_smooth, y_smooth, color=color, linewidth=1.8, label=nombre)
        ax1.fill_between(x_smooth, y_smooth, alpha=0.10, color=color)

    ax1.set_title("CHART DE PRECIOS CONTINUOS (BASE 100)", fontsize=10, color='#00e676', fontweight='bold', pad=12)
    ax1.grid(True, linestyle='--', alpha=0.18, color='#2a2e39')
    ax1.set_xticks(etapas)
    ax1.set_xticklabels([f"E{e}" for e in etapas])
    ax1.legend(facecolor='#151922', edgecolor='#2a2e39', fontsize=8, loc='upper left')

    colores_equipos = ['#00e676', '#ff9100', '#00b0ff', '#e040fb', '#ffd600', '#ff5252']
    for idx, (id_eq, eq) in enumerate(st.session_state.equipos.items()):
        c = colores_equipos[idx % len(colores_equipos)]
        patrimonio = eq["historico_patrimonio"]
        x_smooth, y_smooth = generar_movimiento_continuo(patrimonio, seed=200 + id_eq)
        
        ax2.plot(x_smooth, y_smooth, linewidth=2.0, label=eq["nombre"], color=c)
        ax2.fill_between(x_smooth, y_smooth, 100000, alpha=0.08, color=c)

    ax2.axhline(y=100000, color='#787b86', linestyle=':', alpha=0.6, label="Cap. Base")
    ax2.set_title("EVOLUCIÓN EN VIVO DEL CAPITAL (USD)", fontsize=10, color='#00e676', fontweight='bold', pad=12)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))
    ax2.grid(True, linestyle='--', alpha=0.18, color='#2a2e39')
    ax2.set_xticks(range(len(etapas)))
    ax2.set_xticklabels([f"E{e}" for e in etapas])
    ax2.legend(facecolor='#151922', edgecolor='#2a2e39', fontsize=8, loc='upper left')

    plt.tight_layout()
    return fig

# --- HEADER PRINCIPAL STONKS ---
st.title("🚀 STONKS | TERMINAL DE TRADING")

col_t1, col_t2, col_t3, col_t4 = st.columns(4)
col_t1.metric("OPENAI", f"${st.session_state.precios_activos['OpenAI']:.2f}")
col_t2.metric("ORO", f"${st.session_state.precios_activos['Oro']:.2f}")
col_t3.metric("S&P 500", f"${st.session_state.precios_activos['S&P 500']:.2f}")
col_t4.metric("ANTHROPIC", f"${st.session_state.precios_activos['Anthropic']:.2f}" if st.session_state.etapa_actual >= 3 else "NO LISTADO")

# BARRA LATERAL
with st.sidebar:
    st.markdown("### ⚙️ CONTROL DE STONKS")
    if st.button("🔄 REINICIAR SIMULACIÓN", use_container_width=True):
        reiniciar_juego()
        st.rerun()

    st.markdown("---")
    st.markdown("### 👥 MESAS DE TRADING")
    num_equipos = st.slider("Cantidad de Equipos:", 1, 10, len(st.session_state.equipos))
    
    if num_equipos > len(st.session_state.equipos):
        for i in range(1, num_equipos + 1):
            if i not in st.session_state.equipos:
                st.session_state.equipos[i] = {
                    "nombre": f"Equipo {i}", "capital_actual": 100000.0, "historico_patrimonio": [100000.0], "historial_decisiones": []
                }
    elif num_equipos < len(st.session_state.equipos):
        for i in list(st.session_state.equipos.keys()):
            if i > num_equipos:
                st.session_state.equipos.pop(i, None)
                st.session_state.decisiones_etapa_actual.pop(i, None)

    eq_sel = st.selectbox("Seleccionar Equipo:", options=list(st.session_state.equipos.keys()), format_func=lambda x: st.session_state.equipos[x]["nombre"])
    nuevo_nombre = st.text_input("Cambiar Nombre:", key="input_nuevo_nombre")
    if st.button("Guardar Nombre"):
        if nuevo_nombre.strip():
            st.session_state.equipos[eq_sel]["nombre"] = nuevo_nombre.strip()
            st.rerun()

st.pyplot(render_graficos())

if st.session_state.etapa_actual > 5:
    st.balloons()
    st.subheader("🏆 TABLA DE POSICIONES FINALES - STONKS")
    
    res_data = []
    for id_eq, eq in sorted(st.session_state.equipos.items(), key=lambda x: x[1]['capital_actual'], reverse=True):
        rend = ((eq['capital_actual'] - 100000.0) / 100000.0) * 100
        res_data.append({
            "Equipo": eq["nombre"],
            "Capital Inicial": "$100,000.00",
            "Capital Final": f"${eq['capital_actual']:,.2f}",
            "Rendimiento Total": f"{rend:+.2f}%"
        })
    st.table(pd.DataFrame(res_data))

else:
    config_etapa = ETAPAS_CONFIG[st.session_state.etapa_actual]
    
    st.info(config_etapa["noticias"])

    st.markdown("### 📑 CONFIGURAR PORTAFOLIO")
    
    c1, c2 = st.columns([1, 2.5])
    with c1:
        equipo_sel_id = st.selectbox(
            "Equipo a Operar:",
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
                f"% {activo}", min_value=0, max_value=100, step=1, value=val_init, key=f"{equipo_sel_id}_{activo}"
            )

    suma_porcentajes = sum(pesos_input.values())
    st.caption(f"**DISTRIBUCIÓN DEL PORTAFOLIO:** `{suma_porcentajes}%` / `100%`")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("💾 CONFIRMAR PORTAFOLIO DEL EQUIPO", use_container_width=True):
            if suma_porcentajes != 100:
                st.error(f"❌ La suma de porcentajes debe ser exactamente 100%. Suma actual: {suma_porcentajes}%")
            else:
                st.session_state.decisiones_etapa_actual[equipo_sel_id] = pesos_input
                st.success(f"✅ Portafolio guardado para: {st.session_state.equipos[equipo_sel_id]['nombre']}")

    listos = [st.session_state.equipos[i]['nombre'] for i in st.session_state.decisiones_etapa_actual.keys()]
    pendientes = [st.session_state.equipos[i]['nombre'] for i in st.session_state.equipos.keys() if i not in st.session_state.decisiones_etapa_actual]

    st.markdown(f"**EQUIPOS LISTOS:** `{', '.join(listos) if listos else 'NINGUNO'}` | **PENDIENTES:** `{', '.join(pendientes) if pendientes else 'NINGUNO'}`")

    st.markdown("---")
    if st.button("🚀 AVANZAR A LA SIGUIENTE ETAPA", type="primary", use_container_width=True):
        procesar_etapa()
        st.rerun()
