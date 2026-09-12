"""
modelos/indicador_economico.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Camada MODEL do padrão MVC.

Responsabilidade: definir a estrutura de dados do domínio.
Este módulo não sabe nada sobre a interface (Streamlit) nem sobre
como os dados são lidos do disco — ele apenas representa o "o quê"
que o sistema manipula.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class IndicadorEconomico:
    """
    Representa um registro anual de indicadores econômicos de um país.

    Atributos
    ----------
    country : str
        Nome do país em inglês (padrão World Bank).
    country_code : str
        Código ISO 3166-1 alfa-3 do país (ex: "BRA").
    region : str
        Região geográfica do país conforme classificação World Bank.
    year : int
        Ano de referência do indicador.
    gdp_trillion_usd : float
        PIB total em trilhões de dólares americanos (USD correntes).
    gdp_per_capita_usd : float
        PIB per capita em dólares americanos (USD correntes).
    population_million : float
        População total em milhões de habitantes.
    growth_rate_pct : float
        Taxa de crescimento do PIB em relação ao ano anterior (%).
    inflation_pct : float
        Taxa de inflação anual (%).
    unemployment_pct : float
        Taxa de desemprego anual (%).
    """

    country: str
    country_code: str
    region: str
    year: int
    gdp_trillion_usd: float
    gdp_per_capita_usd: float
    population_million: float
    growth_rate_pct: float
    inflation_pct: float
    unemployment_pct: float
