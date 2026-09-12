"""
visoes/graficos.py
━━━━━━━━━━━━━━━━━━
Camada VIEW — componentes de gráficos.

Cada função recebe um DataFrame já preparado pelo controller e devolve
uma figura Plotly pronta para ser exibida com `st.plotly_chart()`.

As funções aqui NÃO fazem cálculos de negócio — apenas constroem a
representação visual dos dados que recebem.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .tema import PALETA_SERIES, PALETA_REGIOES, layout_grafico, CORES


def grafico_evolucao_pib(df: pd.DataFrame) -> go.Figure:
    """
    Gráfico de linhas com a evolução do PIB por país ao longo dos anos.

    Inclui uma região sombreada destacando o ano de impacto da COVID-19 (2020),
    e marcadores nos pontos de dado para facilitar a leitura.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame filtrado com colunas: year, gdp_trillion_usd, country.

    Returns
    -------
    go.Figure
        Figura Plotly pronta para exibição.
    """
    fig = px.line(
        df,
        x="year",
        y="gdp_trillion_usd",
        color="country",
        markers=True,
        color_discrete_sequence=PALETA_SERIES,
        labels={
            "year":            "Ano",
            "gdp_trillion_usd": "PIB (USD Trilhões)",
            "country":          "País",
        },
        hover_data={"gdp_trillion_usd": ":.2f"},
    )

    fig.update_layout(**layout_grafico(altura=420))
    fig.update_layout(
        xaxis=dict(dtick=1, gridcolor=CORES["fundo_card"]),
        yaxis=dict(ticksuffix=" T", gridcolor=CORES["fundo_card"]),
    )
    fig.update_traces(line=dict(width=2.5), marker=dict(size=7))

    # Destaque visual para o ano da pandemia de COVID-19
    fig.add_vrect(
        x0=2019.5, x1=2020.5,
        fillcolor=CORES["accent_vermelho"],
        opacity=0.07,
        layer="below",
        line_width=0,
        annotation_text="COVID-19 (2020)",
        annotation_position="top left",
        annotation_font_color=CORES["accent_vermelho"],
        annotation_font_size=10,
    )

    return fig


def grafico_ranking_pib(df_ranking: pd.DataFrame) -> go.Figure:
    """
    Gráfico de barras horizontais com o ranking de PIB dos países
    para o ano mais recente da seleção, colorido por região geográfica.

    Parameters
    ----------
    df_ranking : pd.DataFrame
        DataFrame com colunas: country, gdp_trillion_usd, region.
        Deve vir ordenado de forma crescente (menor → maior) para que
        a barra mais alta apareça no topo do gráfico.

    Returns
    -------
    go.Figure
        Figura Plotly pronta para exibição.
    """
    # Mapeia a cor de cada barra pela região do país
    cores_barras = df_ranking["region"].map(PALETA_REGIOES).fillna(CORES["texto_secundario"])

    fig = go.Figure(
        go.Bar(
            y=df_ranking["country"],
            x=df_ranking["gdp_trillion_usd"],
            orientation="h",
            marker_color=cores_barras,
            text=df_ranking["gdp_trillion_usd"].apply(lambda v: f"US$ {v:.2f} T"),
            textposition="outside",
            textfont=dict(color=CORES["texto_primario"], size=11),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "PIB: US$ %{x:.2f} T<br>"
                "<extra></extra>"
            ),
        )
    )

    altura_dinamica = max(350, len(df_ranking) * 42)

    fig.update_layout(**layout_grafico(altura=altura_dinamica, margem_direita=110))
    fig.update_layout(
        xaxis=dict(ticksuffix=" T", gridcolor=CORES["fundo_card"]),
        yaxis=dict(tickfont=dict(color=CORES["texto_primario"], size=12)),
        showlegend=False,
    )

    return fig


def grafico_crescimento_pib(df: pd.DataFrame) -> go.Figure:
    """
    Gráfico de barras agrupadas mostrando a taxa de crescimento anual do PIB
    por país, com barras coloridas em verde (positivo) ou vermelho (negativo).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame filtrado com colunas: year, country, growth_rate_pct.

    Returns
    -------
    go.Figure
        Figura Plotly pronta para exibição.
    """
    fig = px.bar(
        df,
        x="year",
        y="growth_rate_pct",
        color="country",
        barmode="group",
        color_discrete_sequence=PALETA_SERIES,
        labels={
            "year":           "Ano",
            "growth_rate_pct": "Crescimento do PIB (%)",
            "country":         "País",
        },
        hover_data={"growth_rate_pct": ":.1f"},
    )

    fig.update_layout(**layout_grafico(altura=380))
    fig.update_layout(
        xaxis=dict(dtick=1, gridcolor=CORES["fundo_card"]),
        yaxis=dict(ticksuffix="%",  gridcolor=CORES["fundo_card"], zeroline=True,
                   zerolinecolor=CORES["fundo_borda"], zerolinewidth=1),
    )

    return fig


def grafico_inflacao_desemprego(df: pd.DataFrame) -> go.Figure:
    """
    Scatter plot de bolhas relacionando inflação e desemprego por país
    no ano mais recente da seleção. O tamanho da bolha representa o PIB,
    dando uma terceira dimensão de leitura.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame filtrado. A função usa apenas o ano mais recente.

    Returns
    -------
    go.Figure
        Figura Plotly pronta para exibição.
    """
    ultimo_ano = df["year"].max()
    df_ano = df[df["year"] == ultimo_ano].copy()

    fig = px.scatter(
        df_ano,
        x="inflation_pct",
        y="unemployment_pct",
        size="gdp_trillion_usd",
        color="region",
        text="country_code",
        color_discrete_sequence=PALETA_SERIES,
        labels={
            "inflation_pct":    "Inflação (%)",
            "unemployment_pct": "Desemprego (%)",
            "gdp_trillion_usd": "PIB (USD Tri)",
            "region":           "Região",
        },
        hover_data={
            "country":          True,
            "inflation_pct":    ":.1f",
            "unemployment_pct": ":.1f",
            "gdp_trillion_usd": ":.2f",
            "country_code":     False,
        },
        size_max=60,
    )

    fig.update_traces(textposition="top center", textfont=dict(size=9, color=CORES["texto_secundario"]))
    fig.update_layout(**layout_grafico(altura=400))
    fig.update_layout(
        xaxis=dict(ticksuffix="%", gridcolor=CORES["fundo_card"]),
        yaxis=dict(ticksuffix="%", gridcolor=CORES["fundo_card"]),
    )

    return fig
