"""
visoes/componentes.py
━━━━━━━━━━━━━━━━━━━━━
Camada VIEW — componentes de interface reutilizáveis.

Este módulo contém funções que renderizam partes da UI do Streamlit:
sidebar com os widgets, cartões de métricas, legendas e rodapé.
Cada função é independente e pode ser chamada individualmente no app principal.
"""

import os
from typing import List, Tuple

import streamlit as st
from PIL import Image

from .tema import PALETA_REGIOES, CORES


# ─── Sidebar com widgets de controle ──────────────────────────────────────────

def renderizar_sidebar(
    lista_paises: List[str],
    ano_min: int,
    ano_max: int,
) -> Tuple[List[str], Tuple[int, int]]:
    """
    Renderiza a barra lateral com os dois widgets de controle
    e retorna os valores selecionados pelo usuário.

    WIDGET 1 — Multiselect de países
    WIDGET 2 — Slider de intervalo de anos

    Parameters
    ----------
    lista_paises : List[str]
        Todos os países disponíveis no dataset.
    ano_min : int
        Menor ano disponível.
    ano_max : int
        Maior ano disponível.

    Returns
    -------
    Tuple[List[str], Tuple[int, int]]
        (paises_selecionados, (ano_inicio, ano_fim))
    """
    with st.sidebar:
        st.markdown("## ⚙️ Filtros")
        st.markdown("---")

        # ── WIDGET 1: Seleção de países ──────────────────────────────────────
        # Permite ao usuário escolher quais países comparar no dashboard.
        # O padrão traz as 5 maiores economias para uma visão inicial relevante.
        paises_padrao = [
            p for p in ["United States", "China", "Germany", "Brazil", "India"]
            if p in lista_paises
        ]
        paises_selecionados = st.multiselect(
            label="Selecione os países:",
            options=lista_paises,
            default=paises_padrao,
            help="Escolha um ou mais países para comparar no dashboard.",
        )

        st.markdown("---")

        # ── WIDGET 2: Intervalo de anos ───────────────────────────────────────
        # Controla o período de análise exibido em todos os gráficos.
        intervalo_anos = st.slider(
            label="Intervalo de anos:",
            min_value=ano_min,
            max_value=ano_max,
            value=(ano_min, ano_max),
            step=1,
            help="Arraste as extremidades para filtrar o período analisado.",
        )

        st.markdown("---")

        # Nota de fonte dos dados
        st.markdown(
            "<p style='color:#64748B;font-size:0.74rem;line-height:1.6;'>"
            "📊 <b style='color:#94A3B8'>Fonte:</b> World Bank Open Data<br>"
            "📌 <b style='color:#94A3B8'>Indicador:</b> NY.GDP.MKTP.CD<br>"
            "💵 <b style='color:#94A3B8'>Unidade:</b> USD correntes<br>"
            "📅 <b style='color:#94A3B8'>Período:</b> 2018 – 2023"
            "</p>",
            unsafe_allow_html=True,
        )

    return paises_selecionados, intervalo_anos


# ─── Banner / imagem fixa ──────────────────────────────────────────────────────

def renderizar_banner(caminho_assets: str) -> None:
    """
    Exibe a imagem de cabeçalho do dashboard (FIGURA FIXA — requisito da atividade).

    Parameters
    ----------
    caminho_assets : str
        Caminho absoluto para a pasta 'assets/' do projeto.
    """
    caminho_imagem = os.path.join(caminho_assets, "banner.png")

    if os.path.exists(caminho_imagem):
        banner = Image.open(caminho_imagem)
        st.image(banner, use_container_width=True)
    else:
        # Fallback caso o banner não seja encontrado
        st.warning("⚠️ Imagem de banner não encontrada em assets/banner.png")

    st.markdown(
        "<p style='text-align:center;color:#475569;font-size:0.75rem;margin-top:4px;'>"
        "Fonte: World Bank Open Data · Indicador NY.GDP.MKTP.CD · "
        "Valores em USD Trilhões a preços correntes"
        "</p>",
        unsafe_allow_html=True,
    )


# ─── Cartões de métricas (KPIs) ───────────────────────────────────────────────

def renderizar_metricas(metricas: dict) -> None:
    """
    Exibe os cartões de KPI no topo do dashboard com base no dicionário
    retornado por `calcular_metricas_resumo` do controller.

    Layout: 4 cartões na primeira linha, 3 na segunda.

    Parameters
    ----------
    metricas : dict
        Dicionário retornado por `controladores.calcular_metricas_resumo`.
    """
    ano = metricas["ultimo_ano"]

    # ── Linha 1: indicadores de PIB ───────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="PIB Total da Seleção",
            value=f"US$ {metricas['pib_total']:.1f} T",
            delta=f"Ano {ano}",
        )
    with col2:
        st.metric(
            label="Maior Economia",
            value=metricas["maior_economia"],
            delta=f"US$ {metricas['maior_pib']:.1f} T",
        )
    with col3:
        st.metric(
            label="PIB per Capita Médio",
            value=f"US$ {metricas['pib_per_capita_medio']:,.0f}",
        )
    with col4:
        st.metric(
            label="Países Analisados",
            value=str(metricas["num_paises"]),
            delta="na seleção",
        )

    # ── Linha 2: indicadores macroeconômicos ──────────────────────────────────
    col5, col6, col7, _ = st.columns(4)

    with col5:
        crescimento = metricas["crescimento_medio"]
        st.metric(
            label="Crescimento Médio (PIB)",
            value=f"{crescimento:+.1f}%",
            delta="média da seleção",
            delta_color="normal",
        )
    with col6:
        st.metric(
            label="Inflação Média",
            value=f"{metricas['inflacao_media']:.1f}%",
            delta="média da seleção",
            delta_color="inverse",  # inflação alta = ruim → vermelho
        )
    with col7:
        st.metric(
            label="Desemprego Médio",
            value=f"{metricas['desemprego_medio']:.1f}%",
            delta="média da seleção",
            delta_color="inverse",  # desemprego alto = ruim → vermelho
        )


# ─── Cabeçalho de seção ───────────────────────────────────────────────────────

def cabecalho_secao(titulo: str) -> None:
    """
    Renderiza um cabeçalho de seção com barra lateral colorida (estilo accent).

    Parameters
    ----------
    titulo : str
        Texto do cabeçalho, pode incluir emoji.
    """
    st.markdown(
        f"<div class='cabecalho-secao'>"
        f"<h3 style='margin:0;color:{CORES['accent_azul']}'>{titulo}</h3>"
        f"</div>",
        unsafe_allow_html=True,
    )


# ─── Legenda de regiões ───────────────────────────────────────────────────────

def renderizar_legenda_regioes(regioes_presentes: List[str]) -> None:
    """
    Renderiza a legenda de cores por região geográfica abaixo do gráfico de ranking.

    Parameters
    ----------
    regioes_presentes : List[str]
        Lista de regiões que aparecem no gráfico atual.
    """
    st.markdown("**Regiões geográficas:**")
    colunas = st.columns(len(regioes_presentes))

    for idx, regiao in enumerate(sorted(regioes_presentes)):
        cor = PALETA_REGIOES.get(regiao, CORES["texto_secundario"])
        with colunas[idx]:
            st.markdown(
                f"<span class='legenda-regiao'>"
                f"<span class='ponto-cor' style='background:{cor}'></span>"
                f"{regiao}"
                f"</span>",
                unsafe_allow_html=True,
            )


# ─── Tabela de dados brutos ────────────────────────────────────────────────────

def renderizar_tabela_dados(df_exibicao: "pd.DataFrame") -> None:
    """
    Exibe a tabela de dados brutos dentro de um expander colapsável.

    Parameters
    ----------
    df_exibicao : pd.DataFrame
        DataFrame já formatado pelo `controladores.preparar_tabela_exibicao`.
    """
    with st.expander("📋  Ver tabela de dados completa"):
        st.dataframe(df_exibicao, use_container_width=True, hide_index=True)


# ─── Rodapé ───────────────────────────────────────────────────────────────────

def renderizar_rodape() -> None:
    """
    Exibe o rodapé com informações sobre o projeto e a fonte dos dados.
    """
    st.markdown(
        "<p class='rodape'>"
        "Dashboard desenvolvido com <b>Streamlit</b> &amp; <b>Plotly</b> · "
        "Dados: <b>World Bank Open Data API</b> (NY.GDP.MKTP.CD) · "
        "Visualização de Dados — Atividade II · César School"
        "</p>",
        unsafe_allow_html=True,
    )
