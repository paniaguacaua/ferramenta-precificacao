import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import random

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Ferramenta de Precificação",
    page_icon="💲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# PALETA DE CORES
# ─────────────────────────────────────────────
COR_TEAL   = "#00AE9D"
COR_VERDE  = "#7DB61C"
COR_ROXO   = "#49479D"
COR_ESCURO = "#003641"
COR_TEXTO  = "#E8F4F3"
COR_MUTED  = "#7FAAA5"
COR_CARD   = "#004D5C"
COR_BORDER = "#005F71"
COR_BG     = "#002B36"

# ─────────────────────────────────────────────
# CSS CUSTOMIZADO
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

:root {{
    --bg:      {COR_BG};
    --card:    {COR_CARD};
    --border:  {COR_BORDER};
    --teal:    {COR_TEAL};
    --verde:   {COR_VERDE};
    --roxo:    {COR_ROXO};
    --escuro:  {COR_ESCURO};
    --text:    {COR_TEXTO};
    --muted:   {COR_MUTED};
}}

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}}
.stApp {{ background-color: var(--bg); }}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {COR_ESCURO} 0%, #001F28 100%) !important;
    border-right: 1px solid var(--border);
}}
[data-testid="stSidebar"] * {{ color: var(--text) !important; }}
[data-testid="stSidebar"] label {{
    color: var(--muted) !important;
    font-size: 0.74rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}}

/* Selectbox e Multiselect — fundo e texto visíveis */
[data-testid="stSidebar"] [data-baseweb="select"] > div,
[data-testid="stSidebar"] [data-baseweb="select"] > div:hover {{
    background-color: #00536A !important;
    border: 1px solid {COR_BORDER} !important;
    border-radius: 8px !important;
}}
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] div,
[data-testid="stSidebar"] [data-baseweb="select"] input,
[data-testid="stSidebar"] [data-baseweb="select"] [data-testid="stMarkdown"] {{
    color: {COR_TEXTO} !important;
    background-color: transparent !important;
}}
/* Placeholder text */
[data-testid="stSidebar"] [data-baseweb="select"] [aria-placeholder],
[data-testid="stSidebar"] [data-baseweb="select"] .placeholder {{
    color: {COR_MUTED} !important;
    opacity: 1 !important;
}}
/* Dropdown list */
[data-baseweb="popover"] [data-baseweb="menu"],
[data-baseweb="popover"] ul {{
    background-color: #004455 !important;
    border: 1px solid {COR_BORDER} !important;
}}
[data-baseweb="popover"] li,
[data-baseweb="popover"] [role="option"] {{
    color: {COR_TEXTO} !important;
    background-color: transparent !important;
}}
[data-baseweb="popover"] li:hover,
[data-baseweb="popover"] [role="option"]:hover {{
    background-color: {COR_TEAL}22 !important;
}}
/* Tags multiselect */
[data-testid="stSidebar"] [data-baseweb="tag"] {{
    background-color: {COR_TEAL}33 !important;
    border: 1px solid {COR_TEAL} !important;
    border-radius: 6px !important;
}}
[data-testid="stSidebar"] [data-baseweb="tag"] span {{
    color: {COR_TEXTO} !important;
}}

/* Header */
.main-header {{
    background: linear-gradient(135deg, {COR_ESCURO} 0%, #005060 55%, {COR_ESCURO} 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 40px;
    margin-bottom: 22px;
    position: relative;
    overflow: hidden;
}}
.main-header::before {{
    content: '';
    position: absolute;
    top: -40%; right: -5%;
    width: 360px; height: 360px;
    background: radial-gradient(circle, rgba(0,174,157,0.18) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}}
.main-header h1 {{
    font-family: 'Syne', sans-serif;
    font-size: 1.95rem;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(90deg, {COR_TEXTO}, {COR_TEAL}, {COR_VERDE});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    position: relative; z-index: 1;
}}
.main-header p {{
    color: var(--muted);
    font-size: 0.88rem;
    margin: 6px 0 0;
    font-weight: 300;
    position: relative; z-index: 1;
}}

/* Section title */
.section-title {{
    font-family: 'Syne', sans-serif;
    font-size: 0.73rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: {COR_TEAL};
    margin: 26px 0 12px;
    display: flex;
    align-items: center;
    gap: 10px;
}}
.section-title::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}}

/* st.metric override */
[data-testid="stMetric"] {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 22px !important;
    position: relative;
    overflow: hidden;
}}
[data-testid="stMetric"]::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, {COR_TEAL}, {COR_VERDE});
    border-radius: 14px 0 0 14px;
}}
[data-testid="stMetric"] label {{
    font-size: 0.68rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}}
[data-testid="stMetricValue"] {{
    font-family: 'Syne', sans-serif !important;
    font-size: 1.55rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
}}
[data-testid="stMetricDelta"] svg {{ display: none; }}
[data-testid="stMetricDelta"] {{
    font-size: 0.75rem !important;
    color: {COR_VERDE} !important;
}}

/* Plotly transparent */
.js-plotly-plot .plotly {{ background: transparent !important; }}

/* Scrollbar */
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: var(--bg); }}
::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}

/* Layout */
.block-container {{ padding-top: 1.4rem !important; }}

/* Sidebar helpers */
.sb-divider {{ height: 1px; background: var(--border); margin: 14px 0; }}
.sb-logo {{
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem; font-weight: 800;
    color: {COR_TEAL}; padding-bottom: 2px; letter-spacing: 0.02em;
}}
.sb-sub {{ font-size: 0.7rem; color: var(--muted); margin-bottom: 14px; }}

/* No-data */
.no-data {{
    text-align: center; padding: 50px 20px;
    background: var(--card);
    border: 1px dashed var(--border);
    border-radius: 14px;
    color: var(--muted); font-size: 0.88rem;
}}

/* Login — input e botao */
div[data-testid="stTextInput"] input {{
    background: {COR_CARD} !important;
    border: 1px solid {COR_BORDER} !important;
    border-radius: 10px !important;
    color: {COR_TEXTO} !important;
    font-size: 0.95rem !important;
    padding: 12px 16px !important;
}}
div[data-testid="stTextInput"] input:focus {{
    border-color: {COR_TEAL} !important;
    box-shadow: 0 0 0 3px rgba(0,174,157,0.18) !important;
}}
div[data-testid="stTextInput"] input::placeholder {{
    color: {COR_MUTED} !important;
    opacity: 1 !important;
}}
.stButton > button {{
    background: linear-gradient(135deg, {COR_TEAL}, {COR_VERDE}) !important;
    color: #003641 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 28px !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    transition: opacity 0.2s !important;
}}
.stButton > button:hover {{ opacity: 0.88 !important; }}

/* Footer */
.footer {{
    text-align: center; margin-top: 46px; padding: 16px;
    color: #2E6070; font-size: 0.74rem;
    border-top: 1px solid var(--border);
}}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HIERARQUIA CENTRAL → COOPERATIVA
# ─────────────────────────────────────────────
HIERARQUIA = {
    "Central Norte":   ["Cooperativa Amazônia", "Cooperativa Pará", "Cooperativa Tocantins"],
    "Central Sul":     ["Cooperativa Gaúcha", "Cooperativa Catarinense", "Cooperativa Paranaense"],
    "Central Leste":   ["Cooperativa Mineira", "Cooperativa Capixaba", "Cooperativa Fluminense"],
    "Central Oeste":   ["Cooperativa Goiana", "Cooperativa Mato-Grossense", "Cooperativa Sulmatense"],
    "Central Sudeste": ["Cooperativa Paulista", "Cooperativa ABC", "Cooperativa Vale"],
}

SUBMODALIDADES = [
    "Capital de Giro", "Investimento", "Giro Rápido",
    "Crédito Estruturado", "Agronegócio", "Crédito Imobiliário",
    "Microcrédito", "Financiamento de Equipamentos",
]
RISCOS      = [f"R{i}" for i in range(1, 21)]
INDEXADORES = ["CDI", "IPCA", "Prefixado", "TJLP", "SELIC"]


# ─────────────────────────────────────────────
# FUNÇÕES
# ─────────────────────────────────────────────

@st.cache_data
def carregar_dados() -> pd.DataFrame:
    """Gera base de dados simulada de contratos."""
    random.seed(42)
    np.random.seed(42)

    todas_coop = [
        (central, coop)
        for central, coops in HIERARQUIA.items()
        for coop in coops
    ]

    n = 300
    datas = pd.date_range("2023-01-01", "2025-03-01", periods=n)
    registros = []

    for i in range(n):
        central, coop = random.choice(todas_coop)
        tipo_pessoa = random.choice(["PF", "PJ"])
        submod      = random.choice(SUBMODALIDADES)
        risco       = random.choice(RISCOS)
        fab_limite  = random.choice(["Sim", "Não"])
        indexador   = random.choice(INDEXADORES)

        if tipo_pessoa == "PF":
            valor = round(np.random.uniform(10_000,  300_000),  2)
            taxa  = round(np.random.uniform(8, 18),             2)
        else:
            valor = round(np.random.uniform(100_000, 5_000_000), 2)
            taxa  = round(np.random.uniform(6, 15),              2)

        prazo = random.choice([12, 24, 36, 48, 60, 84, 120])

        registros.append({
            "proposta":      f"PRO-{2023 + i // 150}-{str(i+1).zfill(4)}",
            "central":       central,
            "cooperativa":   coop,
            "cliente":       f"Cliente {i+1:04d}",
            "tipo_pessoa":   tipo_pessoa,
            "submodalidade": submod,
            "risco":         risco,
            "fab_limite":    fab_limite,
            "indexador":     indexador,
            "valor_contrato":valor,
            "taxa_juros":    taxa,
            "prazo_meses":   prazo,
            "data_contrato": datas[i],
            "status":        random.choice(["Ativo","Ativo","Ativo","Em Análise","Encerrado"]),
        })

    df = pd.DataFrame(registros)
    df["ano_mes"]  = df["data_contrato"].dt.to_period("M").astype(str)
    df["risco_num"]= df["risco"].str.replace("R","").astype(int)
    return df


def aplicar_filtros(
    df: pd.DataFrame,
    central: str,
    cooperativa: str,
    ano_mes_sel: list,
    submod_sel: list,
    fab_limite_sel: list,
    tipo_pessoa_sel: list,
) -> pd.DataFrame:
    """Aplica todos os filtros ao DataFrame."""
    dff = df.copy()
    if central != "Todas":
        dff = dff[dff["central"] == central]
    if cooperativa != "Todas":
        dff = dff[dff["cooperativa"] == cooperativa]
    if ano_mes_sel:
        dff = dff[dff["ano_mes"].isin(ano_mes_sel)]
    if submod_sel:
        dff = dff[dff["submodalidade"].isin(submod_sel)]
    if fab_limite_sel:
        dff = dff[dff["fab_limite"].isin(fab_limite_sel)]
    if tipo_pessoa_sel:
        dff = dff[dff["tipo_pessoa"].isin(tipo_pessoa_sel)]
    return dff


def gerar_metricas(df: pd.DataFrame) -> dict:
    """Calcula métricas principais."""
    if df.empty:
        return dict(total_contratos=0, valor_total=0.0,
                    taxa_media=0.0, prazo_medio=0.0,
                    pf_count=0, pj_count=0)
    return dict(
        total_contratos=len(df),
        valor_total    =df["valor_contrato"].sum(),
        taxa_media     =df["taxa_juros"].mean(),
        prazo_medio    =df["prazo_meses"].mean(),
        pf_count       =(df["tipo_pessoa"] == "PF").sum(),
        pj_count       =(df["tipo_pessoa"] == "PJ").sum(),
    )


def gerar_graficos(df: pd.DataFrame, risco_sel: list):
    """Gera os três gráficos do dashboard."""

    BASE_LAYOUT = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor ="rgba(0,0,0,0)",
        font=dict(family="Inter", color=COR_MUTED, size=11),
    )
    MARGIN_BAR  = dict(l=50, r=30, t=20, b=60)
    MARGIN_PIE  = dict(l=10, r=10, t=20, b=40)
    MARGIN_RISK = dict(l=50, r=30, t=30, b=60)

    # ── 7.1 Valor contratado por mês ─────────────────────────────────
    if not df.empty:
        df_mes = (
            df.groupby("ano_mes")["valor_contrato"]
            .sum().reset_index().sort_values("ano_mes")
        )
        # Formata eixo X para Mês/Ano legível
        df_mes["label"] = pd.to_datetime(df_mes["ano_mes"]).dt.strftime("%b/%Y")

        fig_mes = go.Figure()
        fig_mes.add_trace(go.Bar(
            x=df_mes["label"],
            y=df_mes["valor_contrato"],
            marker=dict(
                color=df_mes["valor_contrato"],
                colorscale=[[0, COR_ESCURO],[0.5, COR_TEAL],[1, COR_VERDE]],
                showscale=False,
            ),
            # Sem text nas barras — valor aparece no hover
            hovertemplate="<b>%{x}</b><br>R$ %{y:,.0f}<extra></extra>",
        ))
        fig_mes.update_layout(
            **BASE_LAYOUT,
            margin=MARGIN_BAR,
            xaxis=dict(
                gridcolor=COR_BORDER,
                tickangle=-40,
                tickfont=dict(size=11, color=COR_TEXTO),
            ),
            yaxis=dict(
                gridcolor=COR_BORDER,
                tickformat=",.0f",
                title="R$",
                tickfont=dict(size=11, color=COR_TEXTO),
                title_font=dict(color=COR_MUTED),
            ),
            height=360,
        )
    else:
        fig_mes = go.Figure()
        fig_mes.update_layout(**BASE_LAYOUT, margin=MARGIN_BAR, height=360)

    # ── 7.2 Tipo de pessoa ────────────────────────────────────────────
    if not df.empty:
        df_tp = df.groupby("tipo_pessoa")["valor_contrato"].sum().reset_index()
        fig_tp = go.Figure(go.Pie(
            labels=df_tp["tipo_pessoa"],
            values=df_tp["valor_contrato"],
            hole=0.52,
            marker=dict(
                colors=[COR_ROXO, COR_TEAL],
                line=dict(color=COR_BG, width=3),
            ),
            textinfo="label+percent",
            textfont=dict(size=13, color="#FFFFFF"),
            textposition="inside",
            pull=[0.03, 0.03],
            hovertemplate="<b>%{label}</b><br>R$ %{value:,.0f}<br>%{percent}<extra></extra>",
        ))
        fig_tp.update_layout(
            **BASE_LAYOUT,
            margin=MARGIN_PIE,
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                orientation="h",
                y=-0.08,
                font=dict(color=COR_TEXTO, size=12),
            ),
            height=360,
        )
    else:
        fig_tp = go.Figure()
        fig_tp.update_layout(**BASE_LAYOUT, height=360)

    # ── 7.3 Risco × Valor contratado ─────────────────────────────────
    if not df.empty:
        df_risco = (
            df.groupby(["risco","risco_num"])["valor_contrato"]
            .sum().reset_index().sort_values("risco_num")
        )
        if risco_sel:
            df_risco = df_risco[df_risco["risco"].isin(risco_sel)]

        mediana = df_risco["valor_contrato"].median() if not df_risco.empty else 0
        cores = [COR_VERDE if v < mediana else COR_TEAL
                 for v in df_risco["valor_contrato"]]

        fig_risco = go.Figure()
        fig_risco.add_trace(go.Bar(
            x=df_risco["risco"],
            y=df_risco["valor_contrato"],
            marker_color=cores,
            name="Valor Contratado",
            hovertemplate="<b>%{x}</b><br>R$ %{y:,.0f}<extra></extra>",
        ))
        fig_risco.add_trace(go.Scatter(
            x=df_risco["risco"],
            y=df_risco["valor_contrato"],
            mode="lines+markers",
            line=dict(color=COR_ROXO, width=2.5, dash="dot"),
            marker=dict(color=COR_ROXO, size=8,
                        line=dict(color="#FFFFFF", width=1)),
            name="Tendência",
            hovertemplate="<b>%{x}</b><br>R$ %{y:,.0f}<extra></extra>",
        ))
        fig_risco.update_layout(
            **BASE_LAYOUT,
            margin=MARGIN_RISK,
            xaxis=dict(
                gridcolor=COR_BORDER,
                title="Nível de Risco",
                tickfont=dict(size=11, color=COR_TEXTO),
                title_font=dict(color=COR_MUTED),
            ),
            yaxis=dict(
                gridcolor=COR_BORDER,
                tickformat=",.0f",
                title="R$",
                tickfont=dict(size=11, color=COR_TEXTO),
                title_font=dict(color=COR_MUTED),
            ),
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                font=dict(color=COR_TEXTO, size=12),
                orientation="h",
                y=1.06,
            ),
            height=380,
        )
    else:
        fig_risco = go.Figure()
        fig_risco.update_layout(**BASE_LAYOUT, height=380)

    return fig_mes, fig_tp, fig_risco


# ── Formatação ───────────────────────────────
def fmt_moeda(v: float) -> str:
    if v >= 1_000_000:
        return f"R$ {v/1_000_000:.2f}M"
    if v >= 1_000:
        return f"R$ {v/1_000:.1f}K"
    return f"R$ {v:.2f}"

def fmt_moeda_full(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")


# ─────────────────────────────────────────────
# LAYOUT PRINCIPAL
# ─────────────────────────────────────────────


SENHA_CORRETA = "sicoob123"


def tela_login():
    """Tela de login centralizada."""
    st.markdown("""
    <style>
    [data-testid="stSidebar"]        { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    .block-container { padding-top: 0 !important; }
    /* Remove tooltip 'Press Enter to apply' */
    div[data-testid="stTextInput"] div[data-testid="InputInstructions"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:14vh'></div>", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.15, 1])
    with col:
        st.markdown(f"""
        <style>
        div[data-testid="stTextInput"] input {{
            background: {COR_ESCURO} !important;
            border: 1px solid {COR_BORDER} !important;
            border-radius: 9px !important;
            color: {COR_TEXTO} !important;
            font-size: 0.9rem !important;
            padding: 9px 14px !important;
        }}
        div[data-testid="stTextInput"] input::placeholder {{
            color: {COR_MUTED} !important; opacity:1 !important;
        }}
        div[data-testid="stTextInput"] input:focus {{
            border-color: {COR_TEAL} !important;
            box-shadow: 0 0 0 2px rgba(0,174,157,0.2) !important;
        }}
        .stButton > button {{
            background: linear-gradient(135deg, {COR_TEAL}, {COR_VERDE}) !important;
            color: {COR_ESCURO} !important;
            border: none !important;
            border-radius: 9px !important;
            font-weight: 700 !important;
            font-size: 0.9rem !important;
            letter-spacing: 0.04em !important;
            height: 42px !important;
            margin-top: 4px !important;
        }}
        .stButton > button:hover {{ opacity: 0.88 !important; }}
        </style>

        <div style="
            background:{COR_CARD};
            border:1px solid {COR_BORDER};
            border-radius:20px;
            padding:36px 36px 32px;
            text-align:center;
            box-shadow:0 24px 64px rgba(0,0,0,0.5);">
            <div style="font-size:2.2rem;margin-bottom:8px;">&#128178;</div>
            <div style="
                font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;
                background:linear-gradient(90deg,{COR_TEXTO},{COR_TEAL});
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                background-clip:text;margin-bottom:4px;">PricePro</div>
            <div style="color:{COR_MUTED};font-size:0.78rem;margin-bottom:0;">
                Ferramenta de Precificação &middot; Acesso Restrito</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            f"<p style='color:{COR_TEXTO};font-size:0.74rem;font-weight:600;"
            f"letter-spacing:0.09em;text-transform:uppercase;margin:18px 0 6px;'>"
            f"&#128274; Senha de acesso</p>",
            unsafe_allow_html=True,
        )

        senha = st.text_input(
            "senha",
            type="password",
            placeholder="Digite a senha...",
            label_visibility="collapsed",
            key="senha_input",
        )

        entrar = st.button("Entrar", use_container_width=True, key="btn_entrar")

        if entrar:
            if senha == SENHA_CORRETA:
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.markdown(
                    "<p style='color:#FF6B6B;font-size:0.8rem;"
                    "text-align:center;margin-top:4px;'>"
                    "&#10060; Senha incorreta. Tente novamente.</p>",
                    unsafe_allow_html=True,
                )


def main():
    # Autenticacao
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False
    if not st.session_state["autenticado"]:
        tela_login()
        st.stop()

    df = carregar_dados()

    # ════════════════════════════════════════
    # SIDEBAR
    # ════════════════════════════════════════
    with st.sidebar:
        st.markdown("""
        <div class="sb-logo">💲 PricePro</div>
        <div class="sb-sub">Ferramenta de Precificação</div>
        <div class="sb-divider"></div>
        """, unsafe_allow_html=True)

        # ── Central / Cooperativa ────────────
        st.markdown("**🏦 Central / Cooperativa**")

        centrais    = ["Todas"] + sorted(HIERARQUIA.keys())
        central_sel = st.selectbox("Central", centrais,
                                   label_visibility="collapsed", key="central")

        if central_sel == "Todas":
            coops = ["Todas"] + sorted(c for lst in HIERARQUIA.values() for c in lst)
        else:
            coops = ["Todas"] + sorted(HIERARQUIA[central_sel])

        coop_sel = st.selectbox("Cooperativa", coops,
                                label_visibility="collapsed", key="coop")

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

        # ── Filtros adicionais ───────────────
        st.markdown("**🔎 Filtros Adicionais**")

        ano_mes_opts = sorted(df["ano_mes"].unique().tolist())
        ano_mes_sel  = st.multiselect("📅 Ano-Mês", ano_mes_opts,
                                      placeholder="Todos os períodos")

        submod_opts = sorted(df["submodalidade"].unique().tolist())
        submod_sel  = st.multiselect("📂 Submodalidade", submod_opts,
                                     placeholder="Todas")

        fab_sel = st.multiselect("🏭 Fábrica de Limites", ["Sim","Não"],
                                 placeholder="Sim / Não")

        tp_sel  = st.multiselect("👤 Tipo de Pessoa", ["PF","PJ"],
                                 placeholder="PF / PJ")

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

        # ── Filtro de Risco (gráfico) ────────
        st.markdown("**⚠️ Risco (Gráfico)**")
        risco_sel = st.multiselect("Nível de Risco", RISCOS, default=RISCOS,
                                   label_visibility="collapsed")

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
        st.caption(f"Base: {len(df):,} contratos carregados")

    # ════════════════════════════════════════
    # CONTEÚDO PRINCIPAL
    # ════════════════════════════════════════

    # ── Header ──────────────────────────────
    st.markdown("""
    <div class="main-header">
        <h1>💲 Ferramenta de Precificação</h1>
        <p>Análise de contratos · Central e Cooperativa · Indicadores em tempo real</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Aplicar filtros ──────────────────────
    df_filtrado = aplicar_filtros(
        df,
        central        =central_sel,
        cooperativa    =coop_sel,
        ano_mes_sel    =ano_mes_sel,
        submod_sel     =submod_sel,
        fab_limite_sel =fab_sel,
        tipo_pessoa_sel=tp_sel,
    )

    metricas = gerar_metricas(df_filtrado)

    # ── Tags de filtros ativos ───────────────
    tags = []
    if central_sel != "Todas":
        tags.append(f"Central: **{central_sel}**")
    if coop_sel != "Todas":
        tags.append(f"Coop: **{coop_sel}**")
    if ano_mes_sel:
        tags.append(f"Período: **{len(ano_mes_sel)} meses**")
    if submod_sel:
        tags.append(f"Submod: **{len(submod_sel)} selecionadas**")
    if fab_sel:
        tags.append(f"Fáb. Limites: **{', '.join(fab_sel)}**")
    if tp_sel:
        tags.append(f"Pessoa: **{', '.join(tp_sel)}**")
    if tags:
        st.markdown("🔍 Filtros ativos: &nbsp;" + " &nbsp;·&nbsp; ".join(tags),
                    unsafe_allow_html=True)

    # ── Indicadores Principais (st.metric) ──
    st.markdown('<div class="section-title">📊 Indicadores Principais</div>',
                unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    pf    = metricas["pf_count"]
    pj    = metricas["pj_count"]
    total = (pf + pj) or 1

    with c1:
        st.metric(
            label="Valor Total Contratado",
            value=fmt_moeda(metricas["valor_total"]),
            delta=f"{metricas['total_contratos']:,} contratos",
        )
    with c2:
        st.metric(
            label="Taxa Média (% a.a.)",
            value=f"{metricas['taxa_media']:.2f}%",
            delta="Taxa média da carteira",
        )
    with c3:
        st.metric(
            label="Prazo Médio",
            value=f"{metricas['prazo_medio']:.0f} meses",
            delta=f"≈ {metricas['prazo_medio']/12:.1f} anos",
        )
    with c4:
        st.metric(
            label="Contratos PF / PJ",
            value=f"{pf} / {pj}",
            delta=f"PF {pf/total*100:.0f}%  ·  PJ {pj/total*100:.0f}%",
        )

    # ── Gráficos ─────────────────────────────
    if df_filtrado.empty:
        st.markdown("""
        <div class="no-data">
            🔎 Nenhum contrato encontrado para os filtros selecionados.<br>
            Ajuste os filtros na barra lateral para ver os dados.
        </div>
        """, unsafe_allow_html=True)
    else:
        fig_mes, fig_tp, fig_risco = gerar_graficos(df_filtrado, risco_sel)

        # Linha 1
        st.markdown('<div class="section-title">📈 Análise de Contratos</div>',
                    unsafe_allow_html=True)
        col_g1, col_g2 = st.columns([3, 2])
        with col_g1:
            st.markdown(
                f'<p style="font-family:Syne,sans-serif;font-size:0.95rem;'
                f'font-weight:700;color:{COR_TEXTO};margin:0 0 4px 4px;">'
                f'📅 Valor Contratado por Mês</p>',
                unsafe_allow_html=True,
            )
            st.plotly_chart(fig_mes, use_container_width=True)
        with col_g2:
            st.markdown(
                f'<p style="font-family:Syne,sans-serif;font-size:0.95rem;'
                f'font-weight:700;color:{COR_TEXTO};margin:0 0 4px 4px;">'
                f'👤 Tipo de Pessoa — Valor Contratado</p>',
                unsafe_allow_html=True,
            )
            st.plotly_chart(fig_tp,  use_container_width=True)

        # Linha 2 — Risco (largura total)
        st.markdown('<div class="section-title">⚠️ Exposição por Nível de Risco</div>',
                    unsafe_allow_html=True)
        st.markdown(
            f'<p style="font-family:Syne,sans-serif;font-size:0.95rem;'
            f'font-weight:700;color:{COR_TEXTO};margin:0 0 4px 4px;">'
            f'⚠️ Risco × Valor Contratado</p>',
            unsafe_allow_html=True,
        )
        st.plotly_chart(fig_risco, use_container_width=True)

        # ── Tabela resumo ────────────────────
        st.markdown('<div class="section-title">📋 Resumo por Submodalidade</div>',
                    unsafe_allow_html=True)

        df_resumo = (
            df_filtrado
            .groupby("submodalidade")
            .agg(
                Contratos    =("proposta",       "count"),
                Valor_Total  =("valor_contrato", "sum"),
                Taxa_Media   =("taxa_juros",     "mean"),
                Prazo_Medio  =("prazo_meses",    "mean"),
            )
            .reset_index()
            .sort_values("Valor_Total", ascending=False)
        )
        df_resumo["Valor_Total"] = df_resumo["Valor_Total"].apply(fmt_moeda_full)
        df_resumo["Taxa_Media"]  = df_resumo["Taxa_Media"].apply(lambda x: f"{x:.2f}%")
        df_resumo["Prazo_Medio"] = df_resumo["Prazo_Medio"].apply(lambda x: f"{x:.0f} meses")
        df_resumo.columns = ["Submodalidade","Contratos","Valor Total","Taxa Média","Prazo Médio"]
        st.dataframe(df_resumo, use_container_width=True, hide_index=True)

    # ── Rodapé ───────────────────────────────
    st.markdown("""
    <div class="footer">
        Ferramenta de Precificação &nbsp;|&nbsp;
        Desenvolvido com Streamlit &amp; Python &nbsp;|&nbsp;
        Dados simulados para demonstração
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()