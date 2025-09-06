# Dashboard Airbnb NYC

Este repositório contém um dashboard interativo desenvolvido em Python utilizando a biblioteca Dash para explorar dados do Airbnb em Nova York. O projeto foi criado como parte do 3º Semestre e está hospedado online para acesso público.

## Descrição
O dashboard permite visualizar e analisar dados de anúncios do Airbnb em Nova York com base no dataset `AB_NYC_2019.csv`. Ele oferece filtros interativos, estatísticas descritivas e gráficos dinâmicos para explorar informações como preço, tipo de acomodação, região, avaliações e ocupação.

## Funcionalidades
- Filtros: Selecione regiões (ex.: Manhattan, Brooklyn), tipos de acomodação (ex.: Entire home/apt), faixas de preço, número de avaliações e quantidade de anúncios por região.
- Estatísticas: Calcule média, moda, mediana, quartis, percentis, desvio padrão, coeficiente de variação e soma total das colunas quantitativas (assimetria e curtose não estão disponíveis por falta da biblioteca scipy).
- Gráficos: Acomodações por região (barras), anúncios por tipo de acomodação (barras), mapas interativos de localização (agrupado por região e por anúncio), preço médio por região (barras), distribuição de preços e noites mínimas (histogramas), ocupação ao longo do ano (histograma), total de avaliações por região e tipo de acomodação (barras), e número de reviews por data (linha).

## Deploy
O dashboard está disponível online em: https://dashboard-airbnb-production.up.railway.app/. Acesse o link para interagir com o dashboard em tempo real!

