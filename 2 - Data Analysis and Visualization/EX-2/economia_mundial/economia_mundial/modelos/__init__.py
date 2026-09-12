# Exporta o modelo principal para que outros módulos possam importar
# diretamente de `modelos` sem precisar conhecer a estrutura interna.
from .indicador_economico import IndicadorEconomico

__all__ = ["IndicadorEconomico"]
