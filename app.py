Python
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- HEADER PRINCIPAL ---
st.title("🚀 STONKS | TERMINAL DE TRADING")

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
            border-left: 4px solid #ff9100 !important;
        }

        .dataframe {
            background-color: #151922 !important;
            color: #e1e6ed !important;
            border: 1px solid #2a2e39 !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- NOTICIAS CLARAS Y AMIGABLES ---
ETAPAS_CONFIG = {
    1: {
        "titulo": "Etapa 1: Subida de Tasas e Impulso Tecnológico",
        "noticias": (
            "📰 NOTICIAS DEL MERCADO - ETAPA 1:\n"
            "• 🏦 El Banco Central sube las tasas de interés para controlar la inflación, haciendo que guardar dinero rinda más.\n"
            "• 📈 El S&P 500 se mantiene estable gracias a las ganancias sólidas de las grandes empresas.\n"
            "• 🤖 OpenAI cierra un contrato gigante de Inteligencia Artificial y sus acciones se disparan."
        ),
        "activos_disponibles": ["OpenAI", "Oro", "S&P 500"],
        "rendimientos": {"OpenAI": 0.35, "Oro": -0.15, "S&P 500": 0.02}
    },
    2: {
        "titulo": "Etapa 2: Miedo a la Recesión y Expectativa de IA",
        "noticias": (
            "📰 NOTICIAS DEL MERCADO - ETAPA 2:\n"
            "• ⚠️ Los analistas advierten sobre un posible estancamiento económico en los próximos meses.\n"
            "• 🚀 Suenan fuertes rumores de que la empresa de IA 'Anthropic' saldrá pronto a la bolsa de valores.\n"
            "• 💡 Los inversionistas prefieren apostar por la tecnología y vender su Oro para buscar mayores ganancias."
        ),
        "activos_disponibles": ["OpenAI", "Oro", "S&P 500"],
        "rendimientos": {"OpenAI": 0.20, "Oro": -0.05, "S&P 500": 0.08}
    },
    3: {
        "titulo": "Etapa 3: ¡Anthropic Sale a Bolsa! (IPO)",
        "noticias": (
            "📰 NOTICIAS DEL MERCADO - ETAPA 3:\n"
            "🔥 ¡DEBUT HISTÓRICO! Anthropic ya cotiza en la bolsa y la fiebre de los inversionistas hace explotar su precio (+80%).\n"
            "• 💸 Todo el mundo vende sus acciones tradicionales del S&P 500 para comprar Anthropic, provocando una caída en el índice.\n"
            "• 📊 OpenAI sigue subiendo de forma moderada pero estable.\n"
            "• 🟡 El Oro frena sus caídas y se mantiene congelado."
        ),
        "activos_disponibles": ["OpenAI", "Oro", "S&P 500", "Anthropic"],
        "rendimientos": {"OpenAI": 0.05, "Oro": 0.00, "S&P 500": -0.12, "Anthropic": 0.80}
    },
    4: {
        "titulo": "Etapa 4: Tensiones Internacionales y Refugio Financiero",
        "noticias": (
            "📰 NOTICIAS DEL MERCADO - ETAPA 4:\n"
            "• 🌍 Conflictos geopolíticos amenazan la fabricación de microchips para Inteligencia Artificial.\n"
            "• 🤖 Pese a los problemas de suministros, la especulación vuelve a impulsar con fuerza a OpenAI y Anthropic.\n"
            "• 🛡️ Ante la incertidumbre mundial, los inversionistas corren a protegerse comprando Oro (+15%).\n"
            "• 📉 Las empresas del S&P 500 sufren por el aumento en costos de transporte."
        ),
        "activos_disponibles": ["OpenAI", "Oro", "S&P 500", "Anthropic"],
        "rendimientos": {"OpenAI": 0.25, "Oro": 0.15, "S&P 500": -0.06, "Anthropic": 0.40}
    },
    5: {
        "titulo": "Etapa 5: Estallido de la Burbuja de IA",
        "noticias": (
            "📰 NOTICIAS DEL MERCADO - ETAPA 5:\n"
            "💥 ¡SE ROMPE LA BURBUJA! Reportes revelan que la Inteligencia Artificial no está dando las ganancias prometidas.\n"
            "• 🔴 Pánico total: Las acciones de OpenAI y Anthropic caen en picada (-55% y -65%).\n"
            "• 🏆 El Oro se convierte en el gran ganador del año alcanzando un récord histórico (+30%).\n"
            "• 🛡️ El S&P 500 amortigua la caída gracias a empresas estables de supermercados y energía."
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

# --- GRÁFICOS ESTILO CHART DE BOLSA ---
def render_graficos():
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    fig.patch.set_facecolor('#0b0e14')
    ax1.set_facecolor('#11151c')
    ax2.set_facecolor('#11151c')

    etapas = st.session_state.historico_precios["Etapa"]

    p_openai = (np.array(st.session_state.historico_precios["OpenAI"]) / 100.0) * 100
    p_oro = (np.array(st.session_state.historico_precios["Oro"]) / 2000.0) * 100
    p_sp = (np.array(st.session_state.historico_precios["S&P 500"]) / 450.0) * 100
    p_anthropic = (np.array(st.session_state.historico_precios["Anthropic"]) / 500.0) * 100

    ax1.plot(etapas, p_openai, color='#b388ff', linewidth=2.5, marker='o', label="OpenAI")
    ax1.fill_between(etapas, p_openai, alpha=0.15, color='#b388ff')

    ax1.plot(etapas, p_oro, color='#ffd700', linewidth=2.5, marker='o', label="Oro")
    ax1.fill_between(etapas, p_oro, alpha=0.10, color='#ffd700')

    ax1.plot(etapas, p_sp, color='#00b0ff', linewidth=2.5, marker='o', label="S&P 500")
    ax1.fill_between(etapas, p_sp, alpha=0.15, color='#00b0ff')

    ax1.plot(etapas, p_anthropic, color='#ff5252', linewidth=2.5, linestyle='--', marker='s', label="Anthropic")
    ax1.fill_between(etapas, p_anthropic, alpha=0.15, color='#ff5252')

    ax1.set_title("CHART DE RENDIMIENTO DE ACTIVOS (BASE 100)", fontsize=10, color='#00e676', fontweight='bold', pad=12)
    ax1.grid(True, linestyle='--', alpha=0.2, color='#2a2e39')
    ax1.set_xticks(etapas)
    ax1.set_xticklabels([f"E{e}" for e in etapas])
    ax1.legend(facecolor='#151922', edgecolor='#2a2e39', fontsize=8, loc='upper left')

    colores_equipos = ['#00e676', '#ff9100', '#00b0ff', '#e040fb', '#ffd600', '#ff5252']
    for idx, (id_eq, eq) in enumerate(st.session_state.equipos.items()):
        c = colores_equipos[idx % len(colores_equipos)]
        patrimonio = eq["historico_patrimonio"]
        x_axis = range(len(patrimonio))
        
        ax2.plot(x_axis, patrimonio, marker='D', linewidth=2.5, label=eq["nombre"], color=c)
        ax2.fill_between(x_axis, patrimonio, 100000, alpha=0.08, color=c)

    ax2.axhline(y=100000, color='#787b86', linestyle=':', alpha=0.6, label="Cap. Base")
    ax2.set_title("EVOLUCIÓN DE CAPITAL DE EQUIPOS (USD)", fontsize=10, color='#00e676', fontweight='bold', pad=12)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))
    ax2.grid(True, linestyle='--', alpha=0.2, color='#2a2e39')
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
    
    st.markdown(f"### 📍 {config_etapa['titulo'].upper()}")
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
                f"% {activo}", min_value=0, max_value=100, step=5, value=val_init, key=f"{equipo_sel_id}_{activo}"
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
