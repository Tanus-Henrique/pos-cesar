"""
controladores/dados_economicos.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Camada CONTROLLER do padrão MVC.

Responsabilidade: orquestrar a lógica de negócio entre os dados brutos
e a interface. O controller:
  - lê e valida o dataset CSV
  - aplica filtros recebidos da view (países, anos)
  - calcula métricas derivadas (crescimento, ranking, médias)
  - devolve DataFrames prontos para consumo pela view

A view nunca acessa o CSV diretamente — tudo passa por aqui.
"""

import os
import pandas as pd
from typing import List, Tuple


# ─── Constantes de configuração ────────────────────────────────────────────────

# Caminho absoluto do CSV relativo à localização deste arquivo
_ARQUIVO_DADOS = os.path.join(
    os.path.dirname(__file__), "..", "dados", "indicadores_mundiais.csv"
)

# Mapeamento dos nomes internos das colunas para rótulos legíveis em português
ROTULOS_COLUNAS = {
    "country":            "País",
    "country_code":       "Código",
    "region":             "Região",
    "year":               "Ano",
    "gdp_trillion_usd":   "PIB (USD Tri)",
    "gdp_per_capita_usd": "PIB per Capita (USD)",
    "population_million": "População (mi)",
    "growth_rate_pct":    "Crescimento (%)",
    "inflation_pct":      "Inflação (%)",
    "unemployment_pct":   "Desemprego (%)",
}


# ─── Funções públicas do controller ───────────────────────────────────────────

def carregar_dados() -> pd.DataFrame:
    """
    Lê o arquivo CSV e retorna o DataFrame bruto com tipagem correta.

    Returns
    -------
    pd.DataFrame
        DataFrame com todos os países e anos disponíveis.

    Raises
    ------
    FileNotFoundError
        Se o arquivo CSV não for encontrado no caminho esperado.
    """
    caminho = os.path.normpath(_ARQUIVO_DADOS)

    if not os.path.exists(caminho):
        raise FileNotFoundError(
            f"Arquivo de dados não encontrado em: {caminho}\n"
            "Verifique se o arquivo 'indicadores_mundiais.csv' está na pasta 'dados/'."
        )

    df = pd.read_csv(caminho)

    # Garante que os tipos numéricos estão corretos após a leitura
    df["year"] = df["year"].astype(int)

    return df


def listar_paises(df: pd.DataFrame) -> List[str]:
    """
    Retorna a lista de países disponíveis em ordem alfabética.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame bruto carregado pelo `carregar_dados`.

    Returns
    -------
    List[str]
        Lista de nomes de países únicos, ordenada alfabeticamente.
    """
    return sorted(df["country"].unique().tolist())


def obter_intervalo_anos(df: pd.DataFrame) -> Tuple[int, int]:
    """
    Retorna o menor e o maior ano presentes no dataset.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame bruto.

    Returns
    -------
    Tuple[int, int]
        Tupla (ano_minimo, ano_maximo).
    """
    return int(df["year"].min()), int(df["year"].max())


def filtrar_dados(
    df: pd.DataFrame,
    paises: List[str],
    ano_inicio: int,
    ano_fim: int,
) -> pd.DataFrame:
    """
    Aplica filtros de países e período sobre o DataFrame bruto.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame bruto completo.
    paises : List[str]
        Países a incluir na análise.
    ano_inicio : int
        Primeiro ano do intervalo (inclusive).
    ano_fim : int
        Último ano do intervalo (inclusive).

    Returns
    -------
    pd.DataFrame
        Subconjunto do DataFrame com apenas os registros filtrados.
    """
    return df[
        (df["country"].isin(paises)) &
        (df["year"] >= ano_inicio) &
        (df["year"] <= ano_fim)
    ].copy()


def calcular_metricas_resumo(df_filtrado: pd.DataFrame) -> dict:
    """
    Calcula os indicadores-chave (KPIs) exibidos no topo do dashboard.

    Os cálculos são feitos sobre o ano mais recente do DataFrame filtrado,
    garantindo que os cartões de métricas sempre reflitam o último período
    disponível na seleção atual do usuário.

    Parameters
    ----------
    df_filtrado : pd.DataFrame
        DataFrame já filtrado por países e período.

    Returns
    -------
    dict
        Dicionário com os seguintes campos:
        - pib_total         : soma do PIB (USD tri) no último ano
        - pib_per_capita_medio : média do PIB per capita no último ano
        - maior_economia    : nome do país com maior PIB
        - maior_pib         : valor do maior PIB
        - crescimento_medio : média da taxa de crescimento no último ano
        - inflacao_media    : média da inflação no último ano
        - desemprego_medio  : média do desemprego no último ano
        - num_paises        : quantidade de países na seleção
        - ultimo_ano        : ano de referência dos KPIs
    """
    ultimo_ano = df_filtrado["year"].max()
    df_ultimo = df_filtrado[df_filtrado["year"] == ultimo_ano]

    idx_maior = df_ultimo["gdp_trillion_usd"].idxmax()

    return {
        "pib_total":            df_ultimo["gdp_trillion_usd"].sum(),
        "pib_per_capita_medio": df_ultimo["gdp_per_capita_usd"].mean(),
        "maior_economia":       df_ultimo.loc[idx_maior, "country"],
        "maior_pib":            df_ultimo.loc[idx_maior, "gdp_trillion_usd"],
        "crescimento_medio":    df_ultimo["growth_rate_pct"].mean(),
        "inflacao_media":       df_ultimo["inflation_pct"].mean(),
        "desemprego_medio":     df_ultimo["unemployment_pct"].mean(),
        "num_paises":           df_filtrado["country"].nunique(),
        "ultimo_ano":           ultimo_ano,
    }


def preparar_ranking(df_filtrado: pd.DataFrame) -> pd.DataFrame:
    """
    Gera o DataFrame de ranking de PIB para o ano mais recente,
    ordenado do menor para o maior (para plotagem horizontal).

    Parameters
    ----------
    df_filtrado : pd.DataFrame
        DataFrame filtrado.

    Returns
    -------
    pd.DataFrame
        DataFrame com colunas country, gdp_trillion_usd, region,
        ordenado de forma crescente por PIB.
    """
    ultimo_ano = df_filtrado["year"].max()
    return (
        df_filtrado[df_filtrado["year"] == ultimo_ano]
        [["country", "gdp_trillion_usd", "region"]]
        .sort_values("gdp_trillion_usd", ascending=True)
        .reset_index(drop=True)
    )


def preparar_tabela_exibicao(df_filtrado: pd.DataFrame) -> pd.DataFrame:
    """
    Formata o DataFrame filtrado para exibição na tabela de dados brutos,
    traduzindo os cabeçalhos para português e formatando os valores numéricos.

    Parameters
    ----------
    df_filtrado : pd.DataFrame
        DataFrame filtrado.

    Returns
    -------
    pd.DataFrame
        DataFrame com colunas em português e valores formatados como strings.
    """
    df_exibir = df_filtrado.copy()

    # Formata colunas numéricas para leitura humana
    df_exibir["gdp_trillion_usd"]   = df_exibir["gdp_trillion_usd"].map(lambda v: f"US$ {v:.2f} T")
    df_exibir["gdp_per_capita_usd"] = df_exibir["gdp_per_capita_usd"].map(lambda v: f"US$ {v:,.0f}")
    df_exibir["population_million"] = df_exibir["population_million"].map(lambda v: f"{v:.1f} mi")
    df_exibir["growth_rate_pct"]    = df_exibir["growth_rate_pct"].map(lambda v: f"{v:+.1f}%")
    df_exibir["inflation_pct"]      = df_exibir["inflation_pct"].map(lambda v: f"{v:.1f}%")
    df_exibir["unemployment_pct"]   = df_exibir["unemployment_pct"].map(lambda v: f"{v:.1f}%")

    # Renomeia colunas para português
    df_exibir = df_exibir.rename(columns=ROTULOS_COLUNAS)

    return df_exibir.sort_values(["Ano", "País"])
