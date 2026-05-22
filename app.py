import base64
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "manifesto_eletronico.xlsx"
LOGO_PATH = BASE_DIR / "assets" / "logo_rossi.png"

st.set_page_config(
    page_title="Dashboard Rossi | Manifesto Eletrônico",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------
# Identidade visual ROSSI — Tema adaptativo claro/escuro
# -------------------------
THEME_MODE = st.sidebar.radio(
    "🎨 Tema visual",
    ["Claro", "Escuro"],
    horizontal=True,
    help="Escolha o tema do dashboard. O layout, filtros, cards e gráficos se ajustam automaticamente.",
)

ROSSI_BLUE = "#0057D9"
ROSSI_BLUE_2 = "#0B3F91"
ROSSI_RED = "#E53935"
GREEN = "#16A34A"
AMBER = "#F59E0B"

if THEME_MODE == "Escuro":
    BG = "#07111F"
    BG_2 = "#0B1628"
    SURFACE = "#12223A"
    SURFACE_2 = "#182A45"
    SIDEBAR = "#081324"
    BORDER = "#36506E"
    TEXT = "#FFFFFF"
    MUTED = "#D6E2F2"
    GRID = "#2C4058"
    INPUT_BG = "#0F1E33"
    SHADOW = "0 18px 42px rgba(0,0,0,.32)"
    HERO_BG = "linear-gradient(135deg, rgba(0,87,217,.32), rgba(18,34,58,.98) 58%, rgba(229,57,53,.20))"
else:
    BG = "#F5F7FA"
    BG_2 = "#F8FAFC"
    SURFACE = "#FFFFFF"
    SURFACE_2 = "#F8FAFC"
    SIDEBAR = "#FFFFFF"
    BORDER = "#E2E8F0"
    TEXT = "#1E293B"
    MUTED = "#64748B"
    GRID = "#E2E8F0"
    INPUT_BG = "#FFFFFF"
    SHADOW = "0 12px 28px rgba(15, 23, 42, 0.08)"
    HERO_BG = "linear-gradient(135deg, rgba(0,87,217,.08), rgba(255,255,255,.96) 55%, rgba(229,57,53,.045))"


def img_to_base64(path: Path) -> str:
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode()


logo_b64 = img_to_base64(LOGO_PATH)


def apply_theme_css() -> None:
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {{
        --theme-mode: {THEME_MODE};
        --rossi-blue: {ROSSI_BLUE};
        --rossi-red: {ROSSI_RED};
        --bg: {BG};
        --bg2: {BG_2};
        --surface: {SURFACE};
        --surface2: {SURFACE_2};
        --border: {BORDER};
        --text: {TEXT};
        --muted: {MUTED};
        --input-bg: {INPUT_BG};
    }}

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background: linear-gradient(180deg, var(--bg2) 0%, var(--bg) 100%);
        color: var(--text);
    }}

    /* Barra superior ajustada ao tema: sem faixa preta e sem esconder o botão da sidebar */
    header[data-testid="stHeader"] {{
        background: var(--bg2) !important;
        height: 46px !important;
        box-shadow: none !important;
        border-bottom: 1px solid transparent !important;
    }}

    [data-testid="stDecoration"],
    #MainMenu,
    footer {{
        display: none !important;
        visibility: hidden !important;
    }}

    /* Sidebar responsiva: aberta com 300px; recolhida sem reservar espaço */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {SIDEBAR} 0%, {BG_2} 100%);
        border-right: 1px solid var(--border);
        box-shadow: 8px 0 24px rgba(15, 23, 42, 0.08);
    }}

    [data-testid="stSidebar"][aria-expanded="true"] {{
        min-width: 300px !important;
        max-width: 300px !important;
    }}

    [data-testid="stSidebar"][aria-expanded="false"] {{
        min-width: 0 !important;
        max-width: 0 !important;
        width: 0 !important;
    }}

    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {{
        width: 300px !important;
        min-width: 300px !important;
    }}

    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {{
        width: 0 !important;
        min-width: 0 !important;
    }}

    /* Botão nativo de abrir/fechar sidebar visível e sem travar o layout */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"],
    button[title="Open sidebar"],
    button[title="Close sidebar"],
    button[aria-label="Open sidebar"],
    button[aria-label="Close sidebar"] {{
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 999999 !important;
        align-items: center !important;
        justify-content: center !important;
        background: var(--surface) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 22px rgba(15,23,42,.14) !important;
    }}

    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"] {{
        position: fixed !important;
        top: 8px !important;
        left: 12px !important;
        width: 38px !important;
        height: 38px !important;
    }}

    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapsedControl"] svg,
    button[title="Open sidebar"] svg,
    button[title="Close sidebar"] svg,
    button[aria-label="Open sidebar"] svg,
    button[aria-label="Close sidebar"] svg {{
        color: var(--text) !important;
        fill: var(--text) !important;
        stroke: var(--text) !important;
    }}

    [data-testid="stSidebar"] * {{ color: var(--text); }}
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] label p {{ color: var(--muted) !important; }}

    .block-container {{
        padding-top: 0.85rem;
        padding-bottom: 2rem;
        max-width: 100% !important;
        padding-left: clamp(1rem, 3vw, 2.5rem);
        padding-right: clamp(1rem, 3vw, 2.5rem);
    }}

    .hero {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 24px;
        padding: 16px 24px;
        margin-bottom: 14px;
        border-radius: 20px;
        border: 1px solid var(--border);
        background: {HERO_BG};
        box-shadow: {SHADOW};
        position: relative;
        overflow: hidden;
    }}
    .hero:before {{
        content: "";
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 5px;
        background: linear-gradient(180deg, var(--rossi-blue), var(--rossi-red));
    }}

    .hero-title {{
        font-size: clamp(22px, 1.7vw, 28px);
        font-weight: 800;
        letter-spacing: -0.03em;
        margin: 0;
        color: var(--text);
    }}

    .hero-subtitle {{
        color: var(--muted);
        margin-top: 5px;
        font-size: 13px;
        line-height: 1.45;
    }}

    .hero-logo {{
        height: 50px;
        object-fit: contain;
        filter: drop-shadow(0 10px 18px rgba(0,87,217,.16));
    }}

    .metric-card {{
        min-height: 104px;
        padding: 14px 16px;
        border-radius: 18px;
        background: var(--surface);
        border: 1px solid var(--border);
        box-shadow: {SHADOW};
        position: relative;
        overflow: hidden;
        margin-bottom: 22px;
    }}
    .metric-card:before {{
        content: "";
        position: absolute;
        top: 0; left: 0; bottom: 0;
        width: 4px;
        background: var(--rossi-blue);
    }}
    .metric-card:after {{
        content: "";
        position: absolute;
        right: -20px; top: -20px;
        width: 70px; height: 70px;
        border-radius: 50%;
        background: rgba(0,87,217,.08);
    }}
    .metric-label {{
        color: var(--muted);
        font-size: 10.5px;
        text-transform: uppercase;
        letter-spacing: .06em;
        font-weight: 800;
        min-height: 25px;
        position: relative;
        z-index: 1;
    }}
    .metric-value {{
        font-size: 28px;
        font-weight: 800;
        margin-top: 5px;
        letter-spacing: -0.03em;
        position: relative;
        z-index: 1;
    }}
    .metric-note {{
        color: var(--muted);
        font-size: 11px;
        margin-top: 3px;
        position: relative;
        z-index: 1;
    }}
    .ok {{ color: {GREEN}; }}
    .blue {{ color: {ROSSI_BLUE}; }}
    .red {{ color: {ROSSI_RED}; }}
    .amber {{ color: {AMBER}; }}

    .section-card {{
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 20px;
        box-shadow: {SHADOW};
        margin-bottom: 16px;
    }}

    .stTabs {{
        margin-top: 8px;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background: var(--surface);
        padding: 8px;
        border-radius: 18px;
        border: 1px solid var(--border);
        box-shadow: {SHADOW};
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 14px;
        padding: 10px 16px;
        color: var(--muted);
        font-weight: 800;
    }}
    .stTabs [aria-selected="true"] {{
        background: var(--rossi-blue);
        color: white !important;
    }}

    div[data-testid="stDataFrame"] {{
        border: 1px solid var(--border);
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 6px 18px rgba(15,23,42,.08);
    }}

    .filter-card {{
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 14px 16px 8px;
        margin-bottom: 14px;
        box-shadow: {SHADOW};
    }}
    .filter-title {{
        font-size: 13px;
        font-weight: 800;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: .06em;
        margin-bottom: 8px;
    }}

    .stButton button, .stDownloadButton button {{
        background: var(--rossi-blue);
        color: white;
        border-radius: 12px;
        border: 1px solid var(--rossi-blue);
        font-weight: 700;
    }}

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="base-input"],
    [data-testid="stDateInput"] input,
    [data-testid="stFileUploader"] section {{
        background: var(--input-bg) !important;
        color: var(--text) !important;
        border-color: var(--border) !important;
        border-radius: 12px !important;
    }}

    div[data-baseweb="tag"] {{
        background: rgba(0,87,217,.12) !important;
        color: var(--text) !important;
        border: 1px solid rgba(0,87,217,.22) !important;
    }}

    [data-testid="stFileUploader"] {{
        background: rgba(79,140,255,.08) !important;
        border: 1.5px dashed #6AA3FF !important;
        border-radius: 16px !important;
        padding: 10px !important;
    }}
    [data-testid="stFileUploader"] button {{
        background: #6AA3FF !important;
        color: #FFFFFF !important;
        border: 1px solid #6AA3FF !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        box-shadow: 0 6px 16px rgba(79,140,255,.24) !important;
    }}
    [data-testid="stFileUploader"] button:hover {{
        background: #8DB8FF !important;
        border-color: #8DB8FF !important;
    }}
    [data-testid="stFileUploader"] section small,
    [data-testid="stFileUploader"] section span {{
        color: var(--muted) !important;
    }}
    .upload-help {{
        background: rgba(34,197,94,.08);
        border-left: 4px solid #22C55E;
        padding: 10px 12px;
        border-radius: 10px;
        margin-top: 10px;
        font-size: 12px;
        color: var(--muted);
    }}

    h1, h2, h3, h4, h5, h6, p, label, span, div {{
        color: inherit;
    }}



    /* Legibilidade reforçada para tema escuro */
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label,
    .stMarkdown, .stMarkdown p, .stMarkdown span,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span {{
        color: var(--text) !important;
    }}

    label, label p, [data-testid="stWidgetLabel"], [data-testid="stWidgetLabel"] p {{
        color: var(--muted) !important;
        font-weight: 600 !important;
    }}

    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] input,
    [data-testid="stDateInput"] input {{
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
        opacity: 1 !important;
    }}

    div[data-baseweb="select"] svg,
    [data-testid="stDateInput"] svg {{
        color: var(--muted) !important;
        fill: var(--muted) !important;
    }}

    .filter-title,
    .metric-label,
    .metric-note,
    .hero-subtitle,
    .footer {{
        color: var(--muted) !important;
    }}

    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] span {{
        color: var(--muted) !important;
        opacity: 1 !important;
    }}

    .stTabs [aria-selected="true"] p,
    .stTabs [aria-selected="true"] span {{
        color: #FFFFFF !important;
    }}

    /* Evita textos quase invisíveis nos gráficos em tema escuro */
    .js-plotly-plot .plotly text {{
        fill: var(--text) !important;
    }}

    .footer {{
        margin-top: 20px;
        padding: 18px 8px 0;
        color: var(--muted);
        border-top: 1px solid var(--border);
        font-size: 12px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


apply_theme_css()

def yes_rate(series: pd.Series) -> float:
    if series is None or len(series) == 0:
        return 0.0
    s = series.astype(str).str.strip().str.upper()
    return float((s == "SIM").mean()) if len(s) else 0.0


def pct(value: float) -> str:
    return f"{value * 100:,.1f}%".replace(",", "X").replace(".", ",").replace("X", ".")


def int_br(value: int | float) -> str:
    return f"{int(value):,}".replace(",", ".")


def status_color(value: float) -> str:
    if value >= 0.95:
        return "ok"
    if value >= 0.85:
        return "amber"
    return "red"


def card(label: str, value: str, note: str = "", color_class: str = "blue"):
    st.markdown(
        f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value {color_class}">{value}</div>
          <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_excel_from_path(path: str) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="CONTROLE_DIARIO", header=4)
    df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]
    df = df.dropna(how="all")
    df = df[df["Data Auditoria"].notna()]
    df["Data Auditoria"] = pd.to_datetime(df["Data Auditoria"], errors="coerce")
    df = df[df["Data Auditoria"].notna()].copy()

    for col in ["Loja", "Motorista", "Status SANTRI", "Assinatura Motorista?", "Foto Entrega?", "Assinatura Cliente?", "Baixado?", "Evidência Completa", "OK/NOK", "Erro Padrão", "Auditado por", "Gerente Resp."]:
        if col in df.columns:
            df[col] = df[col].fillna("Não informado").astype(str).str.strip()
            df.loc[df[col].isin(["", "0", "nan", "None"]), col] = "Não informado"

    # Recalcula segurança dos principais campos, caso a planilha venha com fórmulas ou células vazias.
    if "Evidência Completa" not in df.columns:
        df["Evidência Completa"] = np.where(
            (df["Foto Entrega?"].str.upper() == "SIM") & (df["Assinatura Cliente?"].str.upper() == "SIM"),
            "SIM", "NÃO"
        )
    if "OK/NOK" not in df.columns:
        df["OK/NOK"] = np.where(
            (df["Assinatura Motorista?"].str.upper() == "SIM") &
            (df["Baixado?"].str.upper() == "SIM") &
            (df["Evidência Completa"].str.upper() == "SIM"),
            "OK", "NOK"
        )

    df["OK/NOK"] = df["OK/NOK"].astype(str).str.strip().str.upper()
    df.loc[~df["OK/NOK"].isin(["OK", "NOK"]), "OK/NOK"] = np.where(
        (df["Assinatura Motorista?"].str.upper() == "SIM") &
        (df["Baixado?"].str.upper() == "SIM") &
        (df["Evidência Completa"].str.upper() == "SIM"),
        "OK", "NOK"
    )
    df["Mês"] = df["Data Auditoria"].dt.to_period("M").astype(str)
    df["Dia"] = df["Data Auditoria"].dt.strftime("%d/%m/%Y")
    return df


@st.cache_data(show_spinner=False)
def load_uploaded(file_bytes) -> pd.DataFrame:
    import io
    # Mantido por compatibilidade. O carregamento principal usa arquivo temporário.
    tmp = BASE_DIR / ".uploaded_tmp.xlsx"
    tmp.write_bytes(file_bytes)
    return load_excel_from_path(str(tmp))


# Cabeçalho
st.markdown(
    f"""
    <div class="hero">
      <div>
        <h1 class="hero-title">Dashboard Executivo — Manifesto Eletrônico SANTRI</h1>
        <div class="hero-subtitle">Monitoramento de conformidade, evidências, baixa, assinatura do motorista, falhas e performance por loja.</div>
      </div>
      {'<img class="hero-logo" src="data:image/png;base64,' + logo_b64 + '">' if logo_b64 else '<b>ROSSI SOLUÇÕES</b>'}
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    if logo_b64:
        st.markdown(f"<div style='text-align:center; padding: 12px 0 20px;'><img src='data:image/png;base64,{logo_b64}' style='max-width:190px;'></div>", unsafe_allow_html=True)
    st.markdown("### 📂 Atualização da base")
    uploaded = st.file_uploader(
        "Arraste ou selecione uma planilha Excel",
        type=["xlsx"],
        help="A planilha deve conter a aba CONTROLE_DIARIO."
    )
    st.markdown(
        """
        <div class="upload-help">
        📌 <b>Dica:</b><br>
        Envie uma nova planilha para atualizar os indicadores. Se nada for enviado, será usada a base padrão da pasta <b>/data</b>.
        </div>
        """,
        unsafe_allow_html=True,
    )

try:
    if uploaded is not None:
        df = pd.read_excel(uploaded, sheet_name="CONTROLE_DIARIO", header=4)
        tmp_path = BASE_DIR / ".uploaded_tmp.xlsx"
        with open(tmp_path, "wb") as f:
            f.write(uploaded.getvalue())
        df = load_excel_from_path(str(tmp_path))
    else:
        df = load_excel_from_path(str(DATA_PATH))
except Exception as e:
    st.error(f"Não consegui carregar a planilha. Verifique se existe a aba CONTROLE_DIARIO e se os cabeçalhos estão na linha correta. Erro: {e}")
    st.stop()

# Filtros horizontais — opcionais
with st.sidebar:
    st.markdown("---")
    st.caption("ROSSI SOLUÇÕES • Eficiência que conecta, resultados que entregam.")

st.markdown('<div class="filter-card"><div class="filter-title">🎛️ Filtros rápidos</div>', unsafe_allow_html=True)
min_date, max_date = df["Data Auditoria"].min().date(), df["Data Auditoria"].max().date()
lojas = sorted(df["Loja"].dropna().unique().tolist())
motoristas = sorted(df["Motorista"].dropna().unique().tolist())
gerentes = sorted(df["Gerente Resp."].dropna().unique().tolist()) if "Gerente Resp." in df.columns else []
auditores = sorted(df["Auditado por"].dropna().unique().tolist()) if "Auditado por" in df.columns else []
status = sorted(df["Status SANTRI"].dropna().unique().tolist())

f1, f2, f3, f4, f5, f6 = st.columns([1.25, 1, 1, 1, 1, 1])
with f1:
    data_range = st.date_input("Período", value=(min_date, max_date), min_value=min_date, max_value=max_date, format="DD/MM/YYYY")
with f2:
    loja_sel = st.multiselect("Loja", lojas, default=[], placeholder="Todas")
with f3:
    motorista_sel = st.multiselect("Motorista", motoristas, default=[], placeholder="Todos")
with f4:
    status_sel = st.multiselect("Status SANTRI", status, default=[], placeholder="Todos")
with f5:
    gerente_sel = st.multiselect("Gerente", gerentes, default=[], placeholder="Todos") if gerentes else []
with f6:
    auditor_sel = st.multiselect("Auditor", auditores, default=[], placeholder="Todos") if auditores else []
st.markdown('</div>', unsafe_allow_html=True)

if isinstance(data_range, tuple) and len(data_range) == 2:
    start_date, end_date = data_range
else:
    start_date, end_date = min_date, max_date

fdf = df[
    (df["Data Auditoria"].dt.date >= start_date) &
    (df["Data Auditoria"].dt.date <= end_date)
].copy()

# Filtros opcionais:
# quando nada é selecionado, o dashboard mostra todos os registros.
# quando selecionar um ou mais itens, ele filtra somente pelos escolhidos.
if loja_sel:
    fdf = fdf[fdf["Loja"].isin(loja_sel)]
if motorista_sel:
    fdf = fdf[fdf["Motorista"].isin(motorista_sel)]
if status_sel:
    fdf = fdf[fdf["Status SANTRI"].isin(status_sel)]
if gerente_sel and "Gerente Resp." in fdf.columns:
    fdf = fdf[fdf["Gerente Resp."].isin(gerente_sel)]
if auditor_sel and "Auditado por" in fdf.columns:
    fdf = fdf[fdf["Auditado por"].isin(auditor_sel)]

# KPIs
if fdf.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

total = len(fdf)
ok = int((fdf["OK/NOK"] == "OK").sum())
nok = int((fdf["OK/NOK"] == "NOK").sum())
tcpe = ok / total if total else 0
assinatura = yes_rate(fdf["Assinatura Motorista?"])
evidencia = yes_rate(fdf["Evidência Completa"])
baixado = yes_rate(fdf["Baixado?"])
saude = np.mean([tcpe, assinatura, evidencia, baixado])
falhas = nok
periodo_txt = f"{start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}"

col_header1, col_header2, col_header3 = st.columns([1.6, 1, 1])
with col_header1:
    st.markdown(f"**Período analisado:** {periodo_txt}")
with col_header2:
    st.markdown(f"**Registros filtrados:** {int_br(total)}")
with col_header3:
    st.markdown(f"**Atualizado:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")

cols = st.columns(7)
with cols[0]: card("Taxa de conformidade", pct(tcpe), "OK / Total auditado", status_color(tcpe))
with cols[1]: card("Saúde operacional", pct(saude), "Média dos principais KPIs", status_color(saude))
with cols[2]: card("Assinatura motorista", pct(assinatura), "Manifestos assinados", status_color(assinatura))
with cols[3]: card("Evidência completa", pct(evidencia), "Foto + assinatura cliente", status_color(evidencia))
with cols[4]: card("Baixado", pct(baixado), "Entregas baixadas", status_color(baixado))
with cols[5]: card("Falhas identificadas", int_br(falhas), "Registros NOK", "red" if falhas else "ok")
with cols[6]: card("Pedidos 100% OK", int_br(ok), "Registros conformes", "ok")

# Espaço visual entre os cards de indicadores e a barra de abas
st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# Tema dos gráficos
plotly_template = "plotly_dark" if THEME_MODE == "Escuro" else "plotly_white"
common_layout = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0)",
    font=dict(color=TEXT, family="Inter", size=13),
    margin=dict(l=20, r=20, t=55, b=20),
    legend=dict(orientation="h", y=-0.2),
    template=plotly_template,
    xaxis=dict(gridcolor=GRID, zerolinecolor=BORDER),
    yaxis=dict(gridcolor=GRID, zerolinecolor=BORDER),
)

# Tabs
visao, lojas_tab, falhas_tab, pessoas_tab, dados_tab = st.tabs(["📊 Visão executiva", "🏪 Lojas", "🚨 Falhas", "👥 Pessoas", "📋 Base de dados"])

with visao:
    c1, c2 = st.columns([1.45, 1])

    mensal = fdf.groupby("Mês", as_index=False).agg(
        Total=("OK/NOK", "size"),
        OK=("OK/NOK", lambda x: (x == "OK").sum()),
        NOK=("OK/NOK", lambda x: (x == "NOK").sum()),
    )
    mensal["TCPE"] = mensal["OK"] / mensal["Total"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=mensal["Mês"], y=mensal["TCPE"] * 100, mode="lines+markers+text", text=[pct(v) for v in mensal["TCPE"]], textposition="top center", name="TCPE", line=dict(color=ROSSI_BLUE, width=4)))
    fig.add_hline(y=95, line_dash="dash", line_color=GREEN, annotation_text="Meta 95%", annotation_position="top left")
    fig.update_yaxes(range=[0, 105], ticksuffix="%")
    fig.update_layout(title={"text": "Evolução mensal da taxa de conformidade", "font": {"color": TEXT, "size": 16, "family": "Inter"}}, **common_layout)
    c1.plotly_chart(fig, use_container_width=True)

    status_counts = fdf["OK/NOK"].value_counts().reset_index()
    status_counts.columns = ["Status", "Quantidade"]
    fig2 = px.pie(status_counts, values="Quantidade", names="Status", hole=.62, title="OK x NOK", color="Status", color_discrete_map={"OK": GREEN, "NOK": ROSSI_RED})
    fig2.update_layout(**common_layout)
    fig2.update_traces(textinfo="percent+label")
    c2.plotly_chart(fig2, use_container_width=True)

    c3, c4, c5 = st.columns(3)
    status_santri = fdf["Status SANTRI"].value_counts().reset_index().head(8)
    status_santri.columns = ["Status", "Quantidade"]
    fig3 = px.bar(status_santri, x="Quantidade", y="Status", orientation="h", title="Status SANTRI", text="Quantidade", color_discrete_sequence=[ROSSI_BLUE])
    fig3.update_layout(**common_layout)
    fig3.update_yaxes(categoryorder="total ascending")
    c3.plotly_chart(fig3, use_container_width=True)

    diarios = fdf.groupby("Dia", as_index=False).agg(Total=("OK/NOK", "size"), OK=("OK/NOK", lambda x: (x == "OK").sum()))
    diarios["TCPE"] = diarios["OK"] / diarios["Total"] * 100
    fig4 = px.line(diarios, x="Dia", y="TCPE", markers=True, title="Tendência diária", color_discrete_sequence=[ROSSI_BLUE])
    fig4.update_yaxes(ticksuffix="%", range=[0, 105])
    fig4.update_layout(**common_layout)
    c4.plotly_chart(fig4, use_container_width=True)

    qualidade = pd.DataFrame({
        "Indicador": ["Assinatura Motorista", "Evidência Completa", "Baixado", "TCPE"],
        "Percentual": [assinatura * 100, evidencia * 100, baixado * 100, tcpe * 100],
    })
    fig5 = px.bar(qualidade, x="Indicador", y="Percentual", title="Qualidade operacional", text=qualidade["Percentual"].map(lambda x: f"{x:.1f}%".replace(".", ",")), color="Indicador", color_discrete_sequence=[ROSSI_BLUE, GREEN, ROSSI_BLUE_2, ROSSI_RED])
    fig5.update_yaxes(range=[0, 105], ticksuffix="%")
    fig5.update_layout(**common_layout, showlegend=False)
    c5.plotly_chart(fig5, use_container_width=True)

with lojas_tab:
    loja_perf = fdf.groupby("Loja", as_index=False).agg(
        Total=("OK/NOK", "size"),
        OK=("OK/NOK", lambda x: (x == "OK").sum()),
        NOK=("OK/NOK", lambda x: (x == "NOK").sum()),
    )
    loja_perf["TCPE"] = loja_perf["OK"] / loja_perf["Total"] * 100
    loja_perf = loja_perf.sort_values("TCPE", ascending=False)

    c1, c2 = st.columns([1.2, 1])
    fig = px.bar(loja_perf, x="Loja", y="TCPE", text=loja_perf["TCPE"].map(lambda x: f"{x:.1f}%".replace(".", ",")), title="Ranking de lojas por conformidade", color="TCPE", color_continuous_scale=[ROSSI_RED, AMBER, GREEN])
    fig.update_yaxes(range=[0,105], ticksuffix="%")
    fig.update_layout(**common_layout, coloraxis_showscale=False)
    c1.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(loja_perf, x="Loja", y=["OK", "NOK"], title="Volume OK x NOK por loja", barmode="group", color_discrete_map={"OK": GREEN, "NOK": ROSSI_RED})
    fig2.update_layout(**common_layout)
    c2.plotly_chart(fig2, use_container_width=True)

    exibir = loja_perf.copy()
    exibir["TCPE"] = exibir["TCPE"].map(lambda x: f"{x:.1f}%".replace(".", ","))
    st.dataframe(exibir, use_container_width=True, hide_index=True)

with falhas_tab:
    base_falhas = fdf[fdf["OK/NOK"] == "NOK"].copy()
    c1, c2 = st.columns([1.1, 1])
    if not base_falhas.empty:
        erros = base_falhas["Erro Padrão"].replace("Não informado", "Sem classificação").value_counts().reset_index().head(12)
        erros.columns = ["Falha", "Ocorrências"]
        erros["%"] = erros["Ocorrências"] / erros["Ocorrências"].sum() * 100
        fig = px.bar(erros, x="Ocorrências", y="Falha", orientation="h", title="Ranking de falhas", text="Ocorrências", color_discrete_sequence=[ROSSI_RED])
        fig.update_layout(**common_layout)
        fig.update_yaxes(categoryorder="total ascending")
        c1.plotly_chart(fig, use_container_width=True)

        pareto = erros.sort_values("Ocorrências", ascending=False).copy()
        pareto["Acumulado"] = pareto["Ocorrências"].cumsum() / pareto["Ocorrências"].sum() * 100
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=pareto["Falha"], y=pareto["Ocorrências"], name="Ocorrências", marker_color=ROSSI_RED))
        fig2.add_trace(go.Scatter(x=pareto["Falha"], y=pareto["Acumulado"], name="% acumulado", yaxis="y2", mode="lines+markers", line=dict(color=ROSSI_BLUE, width=3)))
        fig2.update_layout(title={"text": "Pareto de falhas", "font": {"color": TEXT, "size": 16, "family": "Inter"}}, yaxis2=dict(overlaying="y", side="right", ticksuffix="%", range=[0,105]), **common_layout)
        c2.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Plano de ação sugerido")
        acao = erros.head(5).copy()
        acao["Ação recomendada"] = acao["Falha"].apply(lambda x: "Revisar rotina, orientar responsável e acompanhar reincidência por 7 dias")
        st.dataframe(acao, use_container_width=True, hide_index=True)
    else:
        st.success("Nenhuma falha encontrada no filtro atual.")

with pessoas_tab:
    motorista = fdf.groupby("Motorista", as_index=False).agg(
        Entregas=("OK/NOK", "size"),
        OK=("OK/NOK", lambda x: (x == "OK").sum()),
        NOK=("OK/NOK", lambda x: (x == "NOK").sum()),
    )
    motorista["TCPE"] = motorista["OK"] / motorista["Entregas"] * 100
    motorista = motorista.sort_values(["TCPE", "Entregas"], ascending=[False, False])

    c1, c2 = st.columns(2)
    top = motorista.head(12)
    fig = px.bar(top, x="TCPE", y="Motorista", orientation="h", title="Motoristas — maior conformidade", text=top["TCPE"].map(lambda x: f"{x:.1f}%".replace(".", ",")), color_discrete_sequence=[GREEN])
    fig.update_xaxes(range=[0,105], ticksuffix="%")
    fig.update_layout(**common_layout)
    fig.update_yaxes(categoryorder="total ascending")
    c1.plotly_chart(fig, use_container_width=True)

    atencao = motorista.sort_values(["NOK", "Entregas"], ascending=False).head(12)
    fig2 = px.bar(atencao, x="NOK", y="Motorista", orientation="h", title="Motoristas — maior quantidade de NOK", text="NOK", color_discrete_sequence=[ROSSI_RED])
    fig2.update_layout(**common_layout)
    fig2.update_yaxes(categoryorder="total ascending")
    c2.plotly_chart(fig2, use_container_width=True)

    motorista_display = motorista.copy()
    motorista_display["TCPE"] = motorista_display["TCPE"].map(lambda x: f"{x:.1f}%".replace(".", ","))
    st.dataframe(motorista_display, use_container_width=True, hide_index=True)

    if "Gerente Resp." in fdf.columns:
        st.markdown("### Performance por gerente responsável")
        ger = fdf.groupby("Gerente Resp.", as_index=False).agg(Total=("OK/NOK", "size"), OK=("OK/NOK", lambda x: (x == "OK").sum()), NOK=("OK/NOK", lambda x: (x == "NOK").sum()))
        ger["TCPE"] = ger["OK"] / ger["Total"] * 100
        ger["TCPE"] = ger["TCPE"].map(lambda x: f"{x:.1f}%".replace(".", ","))
        st.dataframe(ger.sort_values("Total", ascending=False), use_container_width=True, hide_index=True)

with dados_tab:
    st.markdown("### Base filtrada")
    st.dataframe(fdf.sort_values("Data Auditoria", ascending=False), use_container_width=True, hide_index=True)
    csv = fdf.to_csv(index=False, sep=";", encoding="utf-8-sig")
    st.download_button("⬇️ Baixar base filtrada em CSV", csv, file_name="base_filtrada_rossi.csv", mime="text/csv")

st.markdown("<div class='footer'>ROSSI SOLUÇÕES — Dashboard profissional desenvolvido para acompanhamento executivo e operacional do Manifesto Eletrônico SANTRI.</div>", unsafe_allow_html=True)