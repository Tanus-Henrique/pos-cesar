"""
app.py — Ponto de entrada do Dashboard de Economia Mundial
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Disciplina : Visualização de Dados — Atividade II
Fonte dados: World Bank Open Data (NY.GDP.MKTP.CD)

Arquitetura MVC
───────────────
  MODEL       → modelos/indicador_economico.py
                Define a estrutura de dados do domínio.

  CONTROLLER  → controladores/dados_economicos.py
                Carrega, filtra e calcula métricas sobre os dados.

  VIEW        → visoes/graficos.py      (gráficos Plotly)
                visoes/componentes.py   (widgets, KPIs, tabela)
                visoes/tema.py          (CSS, paleta, layout Plotly)

Este arquivo (app.py) apenas orquestra as três camadas:
recebe os filtros da view → passa ao controller → entrega resultados à view.
Nunca faz lógica de dados nem renderização diretamente.

Para executar:
    streamlit run app.py
"""

import os
import streamlit as st

# Importa as três camadas do padrão MVC
import controladores
import visoes.componentes as componentes
import visoes.graficos    as graficos
from visoes.tema          import CSS_GLOBAL


# ─── Configuração da página ────────────────────────────────────────────────────
# Deve ser a primeira chamada Streamlit do script.

st.set_page_config(
    page_title="Economia Mundial — World Bank",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─── CSS global ───────────────────────────────────────────────────────────────

st.markdown(CSS_GLOBAL, unsafe_allow_html=True)


# ─── Carregamento dos dados (MODEL → CONTROLLER) ──────────────────────────────
# O @st.cache_data do Streamlit evita releitura desnecessária do CSV.

@st.cache_data
def obter_dados():
    """Carrega e cacheia o dataset completo via controller."""
    return controladores.carregar_dados()


df_completo = obter_dados()

# Extrai metadados para alimentar os widgets da sidebar
lista_paises  = controladores.listar_paises(df_completo)
ano_min, ano_max = controladores.obter_intervalo_anos(df_completo)


# ─── SIDEBAR — Widgets de controle (VIEW → input do usuário) ──────────────────

paises_selecionados, intervalo_anos = componentes.renderizar_sidebar(
    lista_paises=lista_paises,
    ano_min=ano_min,
    ano_max=ano_max,
)

# Valida se pelo menos um país foi selecionado antes de continuar
if not paises_selecionados:
    st.warning("⚠️ Selecione pelo menos um país na barra lateral para visualizar o dashboard.")
    st.stop()


# ─── CONTROLLER — Filtragem e métricas ────────────────────────────────────────

df_filtrado = controladores.filtrar_dados(
    df=df_completo,
    paises=paises_selecionados,
    ano_inicio=intervalo_anos[0],
    ano_fim=intervalo_anos[1],
)

metricas    = controladores.calcular_metricas_resumo(df_filtrado)
df_ranking  = controladores.preparar_ranking(df_filtrado)
df_tabela   = controladores.preparar_tabela_exibicao(df_filtrado)


# ─── VIEW — Renderização do dashboard ─────────────────────────────────────────

# ── Figura fixa (requisito da atividade — 20%) ──────────────────────────────
caminho_assets = os.path.join(os.path.dirname(__file__), "assets")
componentes.renderizar_banner(caminho_assets)

st.markdown("---")

# ── Cartões de KPIs ─────────────────────────────────────────────────────────
componentes.renderizar_metricas(metricas)

st.markdown("---")

# ── GRÁFICO 1: Evolução do PIB (requisito — 20%) ────────────────────────────
componentes.cabecalho_secao("📈  Evolução do PIB ao longo do tempo")
fig_linha = graficos.grafico_evolucao_pib(df_filtrado)
st.plotly_chart(fig_linha, use_container_width=True)

st.markdown("---")

# ── GRÁFICO 2: Ranking de PIB (requisito — 20%) ──────────────────────────────
componentes.cabecalho_secao(
    f"🏆  Ranking de PIB — {metricas['ultimo_ano']}"
)
fig_ranking = graficos.grafico_ranking_pib(df_ranking)
st.plotly_chart(fig_ranking, use_container_width=True)

# Legenda de regiões abaixo do gráfico de barras
regioes_presentes = df_ranking["region"].unique().tolist()
componentes.renderizar_legenda_regioes(regioes_presentes)

st.markdown("---")

# ── GRÁFICO 3 (bônus): Taxa de Crescimento do PIB ───────────────────────────
componentes.cabecalho_secao("📊  Taxa de Crescimento Anual do PIB (%)")
fig_crescimento = graficos.grafico_crescimento_pib(df_filtrado)
st.plotly_chart(fig_crescimento, use_container_width=True)

st.markdown("---")

# ── GRÁFICO 4 (bônus): Inflação × Desemprego (scatter de bolhas) ─────────────
componentes.cabecalho_secao(
    f"🔵  Inflação × Desemprego — {metricas['ultimo_ano']} "
    f"<span style='font-size:0.8rem;color:#64748B'>"
    f"(tamanho da bolha = PIB)</span>"
)
fig_scatter = graficos.grafico_inflacao_desemprego(df_filtrado)
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# ── Tabela de dados brutos ────────────────────────────────────────────────────
componentes.renderizar_tabela_dados(df_tabela)

# ── Rodapé ────────────────────────────────────────────────────────────────────
componentes.renderizar_rodape()
