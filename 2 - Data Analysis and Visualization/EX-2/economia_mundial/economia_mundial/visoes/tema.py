"""
visoes/tema.py
━━━━━━━━━━━━━━
Define a paleta de cores, o CSS global e os estilos dos gráficos Plotly.

Centralizar o tema aqui garante consistência visual e facilita
trocas de identidade visual sem tocar em cada gráfico individualmente.
"""

# ─── Paleta de cores base ──────────────────────────────────────────────────────

CORES = {
    # Fundos
    "fundo_app":      "#0F172A",  # azul-noturno profundo
    "fundo_card":     "#1E293B",  # azul-slate escuro
    "fundo_borda":    "#334155",  # borda sutil

    # Texto
    "texto_primario":   "#F1F5F9",
    "texto_secundario": "#94A3B8",
    "texto_muted":      "#475569",

    # Destaque (accent)
    "accent_azul":    "#38BDF8",
    "accent_rosa":    "#F472B6",
    "accent_verde":   "#34D399",
    "accent_amarelo": "#FBBF24",
    "accent_roxo":    "#A78BFA",
    "accent_laranja": "#FB923C",
    "accent_vermelho":"#F87171",
    "accent_ciano":   "#2DD4BF",
}

# Paleta sequencial para gráficos com múltiplas séries
PALETA_SERIES = [
    CORES["accent_azul"],
    CORES["accent_rosa"],
    CORES["accent_verde"],
    CORES["accent_amarelo"],
    CORES["accent_roxo"],
    CORES["accent_laranja"],
    CORES["accent_vermelho"],
    CORES["accent_ciano"],
    "#60A5FA",
    "#E879F9",
    "#4ADE80",
    "#FCD34D",
]

# Paleta por região geográfica (usada nas barras do ranking)
PALETA_REGIOES = {
    "North America":     CORES["accent_azul"],
    "East Asia":         CORES["accent_rosa"],
    "Europe":            CORES["accent_verde"],
    "South Asia":        CORES["accent_amarelo"],
    "Latin America":     CORES["accent_roxo"],
    "Southeast Asia":    CORES["accent_laranja"],
    "Middle East":       CORES["accent_vermelho"],
    "Sub-Saharan Africa":"#60A5FA",
    "Oceania":           CORES["accent_ciano"],
}


# ─── Layout padrão Plotly ──────────────────────────────────────────────────────

def layout_grafico(altura: int = 420, margem_direita: int = 20) -> dict:
    """
    Retorna o dicionário de layout padrão para gráficos Plotly,
    garantindo consistência de fundo, tipografia e grades entre todos os gráficos.

    Parameters
    ----------
    altura : int
        Altura do gráfico em pixels.
    margem_direita : int
        Margem direita em pixels (aumentar quando há rótulos externos).

    Returns
    -------
    dict
        Dicionário compatível com `fig.update_layout(**layout_grafico())`.
    """
    eixo_padrao = dict(
        gridcolor=CORES["fundo_card"],
        tickfont=dict(color=CORES["texto_secundario"]),
        title_font=dict(color=CORES["texto_secundario"]),
        linecolor=CORES["fundo_borda"],
    )

    return dict(
        plot_bgcolor=CORES["fundo_app"],
        paper_bgcolor=CORES["fundo_app"],
        font_color=CORES["texto_primario"],
        height=altura,
        margin=dict(l=20, r=margem_direita, t=20, b=20),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor=CORES["fundo_card"],
            font_color=CORES["texto_primario"],
            bordercolor=CORES["fundo_borda"],
        ),
        legend=dict(
            bgcolor=CORES["fundo_card"],
            bordercolor=CORES["fundo_borda"],
            borderwidth=1,
            font=dict(color=CORES["texto_primario"]),
        ),
        xaxis=eixo_padrao,
        yaxis=eixo_padrao,
    )


# ─── CSS global injetado no Streamlit ─────────────────────────────────────────

CSS_GLOBAL = f"""
<style>
    /* ── Fundo e texto geral ── */
    .stApp {{
        background-color: {CORES['fundo_app']};
        color: {CORES['texto_primario']};
    }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background-color: {CORES['fundo_card']};
    }}

    /* ── Cartões de métricas ── */
    [data-testid="stMetric"] {{
        background-color: {CORES['fundo_card']};
        border: 1px solid {CORES['fundo_borda']};
        border-radius: 12px;
        padding: 16px;
    }}
    [data-testid="stMetricValue"] {{
        color: {CORES['accent_azul']} !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {CORES['texto_secundario']} !important;
        font-size: 0.78rem !important;
    }}

    /* ── Cabeçalhos ── */
    h1, h2, h3 {{
        color: {CORES['texto_primario']} !important;
    }}

    /* ── Divisores ── */
    hr {{
        border-color: {CORES['fundo_borda']};
    }}

    /* ── Cabeçalho de seção com barra lateral colorida ── */
    .cabecalho-secao {{
        background: linear-gradient(90deg, #1E3A5F 0%, {CORES['fundo_app']} 100%);
        border-left: 3px solid {CORES['accent_azul']};
        padding: 10px 16px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 14px;
    }}

    /* ── Legenda de regiões ── */
    .legenda-regiao {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.78rem;
        color: {CORES['texto_primario']};
    }}
    .ponto-cor {{
        display: inline-block;
        width: 11px;
        height: 11px;
        border-radius: 3px;
    }}

    /* ── Rodapé ── */
    .rodape {{
        text-align: center;
        color: {CORES['texto_muted']};
        font-size: 0.73rem;
        margin-top: 32px;
        padding-top: 12px;
        border-top: 1px solid {CORES['fundo_borda']};
    }}
</style>
"""
