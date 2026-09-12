# Expõe as funções públicas do controller diretamente do pacote.
from .dados_economicos import (
    carregar_dados,
    listar_paises,
    obter_intervalo_anos,
    filtrar_dados,
    calcular_metricas_resumo,
    preparar_ranking,
    preparar_tabela_exibicao,
)

__all__ = [
    "carregar_dados",
    "listar_paises",
    "obter_intervalo_anos",
    "filtrar_dados",
    "calcular_metricas_resumo",
    "preparar_ranking",
    "preparar_tabela_exibicao",
]
