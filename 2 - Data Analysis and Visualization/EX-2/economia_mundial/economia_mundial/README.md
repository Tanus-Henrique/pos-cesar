# 🌍 Dashboard de Economia Mundial

Dashboard interativo desenvolvido com **Streamlit** para a disciplina de **Visualização de Dados — Atividade II**.

---

## 📋 Requisitos Contemplados

| Requisito | Implementação | Peso |
|-----------|--------------|------|
| ✅ Gráfico Interativo 1 | Linha — Evolução do PIB ao longo do tempo | 20% |
| ✅ Gráfico Interativo 2 | Barras — Ranking de PIB por país (ano mais recente) | 20% |
| ✅ Widget 1 | Multiselect — Seleção de países para comparação | 20% |
| ✅ Widget 2 | Slider — Filtro de intervalo de anos | 20% |
| ✅ Figura Fixa | Banner ilustrativo gerado com Matplotlib | 20% |
| 🎁 Bônus | Gráfico de crescimento anual do PIB | — |
| 🎁 Bônus | Scatter plot: Inflação × Desemprego | — |
| 🎁 Bônus | 6 KPIs dinâmicos (PIB, crescimento, inflação, desemprego...) | — |

---

## 🏗️ Arquitetura MVC

```
economia_mundial/
│
├── app.py                          ← Ponto de entrada (orquestra o MVC)
│
├── modelos/                        ← MODEL
│   ├── __init__.py
│   └── indicador_economico.py      ← Estrutura de dados do domínio
│
├── controladores/                  ← CONTROLLER
│   ├── __init__.py
│   └── dados_economicos.py         ← Lógica: leitura, filtro, métricas
│
├── visoes/                         ← VIEW
│   ├── __init__.py
│   ├── tema.py                     ← Paleta, CSS global, layout Plotly
│   ├── graficos.py                 ← Componentes de gráficos Plotly
│   └── componentes.py              ← Widgets, KPIs, tabela, rodapé
│
├── dados/
│   └── indicadores_mundiais.csv    ← Dataset com 6 indicadores × 20 países × 6 anos
│
├── assets/
│   └── banner.png                  ← Figura fixa de cabeçalho
│
├── requirements.txt
└── README.md
```

### Responsabilidades por camada

| Camada | Arquivo | Faz | Não faz |
|--------|---------|-----|---------|
| **Model** | `modelos/indicador_economico.py` | Define a estrutura de dados | Lê CSV, renderiza UI |
| **Controller** | `controladores/dados_economicos.py` | Lê, filtra, calcula | Renderiza UI, define estilos |
| **View** | `visoes/graficos.py` + `componentes.py` | Renderiza a interface | Faz cálculos, acessa arquivos |
| **App** | `app.py` | Orquestra as três camadas | Nenhuma lógica de negócio |

---

## 📊 Indicadores Disponíveis

| Indicador | Descrição |
|-----------|-----------|
| PIB Total | GDP em USD Trilhões (correntes) |
| PIB per Capita | GDP per capita em USD |
| Taxa de Crescimento | Variação anual do PIB (%) |
| Inflação | Taxa de inflação anual (%) |
| Desemprego | Taxa de desemprego anual (%) |
| População | Total em milhões de habitantes |

---

## 🌐 Países Incluídos (20 economias)

| Região | Países |
|--------|--------|
| North America | United States, Canada |
| East Asia | China, Japan, South Korea |
| Europe | Germany, UK, France, Italy, Spain, Netherlands, Russia |
| South Asia | India |
| Latin America | Brazil, Mexico, Argentina |
| Southeast Asia | Indonesia |
| Middle East | Saudi Arabia |
| Sub-Saharan Africa | Nigeria |
| Oceania | Australia |

---

## 🚀 Como executar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar (dentro da pasta economia_mundial/)
streamlit run app.py
```

O dashboard abrirá em `http://localhost:8501`.

---

## 🔗 Fonte dos Dados

- **API:** [World Bank Open Data](https://data.worldbank.org/)
- **Indicador:** `NY.GDP.MKTP.CD` — GDP (current US$)
- **Endpoint:** `http://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json`
- **Período:** 2018 a 2023
