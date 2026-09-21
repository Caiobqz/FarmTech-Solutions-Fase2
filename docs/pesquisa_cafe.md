# Pesquisa da cultura — Café

Este documento reúne informações técnicas que vão justificar a lógica de irrigação do projeto FarmTech Solutions — Fase 2.

> **Importante:** o projeto usa substituições didáticas definidas pela atividade. O DHT22 mede umidade do ar, mas será tratado como umidade do solo; o LDR mede intensidade luminosa, mas será convertido para uma escala de pH; e os botões N, P e K representam apenas estados booleanos (presente/adequado ou ausente/inadequado). Esses valores não substituem sensores agrícolas reais.

## Cultura escolhida

**Café (Coffea arabica)**

A escolha mantém continuidade com a Fase 1 do projeto e é coerente com a cafeicultura de Minas Gerais.

## pH

- **Faixa de referência para o projeto:** 5,5 a 6,0.
- O Manual do Café da EMATER-MG classifica pH de 5,5 a 6,0 como faixa agronomicamente boa.
- Materiais técnicos também indicam que o cafeeiro não tolera solos muito ácidos e que a correção da acidez deve ser feita com base em análise de solo.
- Trabalhos acadêmicos citam uma faixa mais ampla de 5,5 a 6,5 para o cafeeiro. Para a simulação, será usada a faixa mais conservadora de 5,5 a 6,0.

**Uso no projeto:** o valor analógico do LDR será convertido didaticamente para uma escala de 0 a 14. O intervalo de 5,5 a 6,0 será considerado "pH adequado" na lógica simulada.

**Fontes:**
- EMATER-MG — Manual do Café: Manejo de Cafezais em Produção: https://www.emater.mg.gov.br/download.do?id=17572
- Embrapa Ater+ Digital — Preparo do Solo e da Área: https://www.atermaisdigital.cnptia.embrapa.br/web/cafe/preparo-do-solo-e-da-%C3%A1rea
- UFLA — referências de solo para cafeeiro: https://repositorio.ufla.br/

## Umidade / necessidade de irrigação

A Embrapa destaca que não existe uma porcentagem única de umidade que possa ser aplicada a qualquer solo. O manejo real depende de propriedades do solo, disponibilidade de água e risco de estresse hídrico.

Como referência, a irrigação deve começar antes que o solo alcance o ponto de murcha. O material da Embrapa cita como condição crítica aproximadamente **50% da Água Facilmente Disponível (AFD)**, para evitar estresse que possa prejudicar floração e enchimento dos grãos.

**Regra didática proposta para a simulação:**
- DHT22 >= 50%: condição considerada suficiente para não acionar irrigação apenas por umidade.
- DHT22 < 50%: condição considerada seca e candidata a irrigação.

> **Limitação:** 50% de umidade relativa medida pelo DHT22 não é igual a 50% da Água Facilmente Disponível no solo. O valor será usado apenas como aproximação didática para permitir a lógica no Wokwi, conforme a própria atividade determina a substituição do sensor de solo pelo DHT22.

**Fontes:**
- Embrapa Ater+ Digital — Manejo Hídrico do Café: https://www.atermaisdigital.cnptia.embrapa.br/web/cafe/fase-de-producao-ou-manutencao
- Embrapa — Necessidade de irrigação para a cultura do café (Coffea arabica): https://www.embrapa.br/en/busca-de-publicacoes/-/publicacao/557897/necessidade-de-irrigacao-para-a-cultura-do-cafe-coffea-arabica-nos-latossolos-do-distrito-federal

## Nitrogênio (N)

O nitrogênio é um dos nutrientes mais exigidos pelo cafeeiro. Na fase de formação, a Embrapa destaca nitrogênio e potássio como nutrientes especialmente importantes para o crescimento de ramos e folhas.

**Representação no projeto:**
- botão pressionado = condição de N considerada adequada;
- botão não pressionado = condição de N considerada inadequada.

**Fonte:**
- Embrapa Ater+ Digital — Fase de Formação do Café: https://www.atermaisdigital.cnptia.embrapa.br/web/cafe/faseformacao

## Fósforo (P)

O fósforo apresenta baixa mobilidade no solo. A Embrapa recomenda atenção à fosfatagem na implantação, pois o nutriente é importante para o arranque inicial e para o desenvolvimento do sistema radicular.

**Representação no projeto:**
- botão pressionado = condição de P considerada adequada;
- botão não pressionado = condição de P considerada inadequada.

**Fonte:**
- Embrapa Ater+ Digital — Preparo do Solo e da Área: https://www.atermaisdigital.cnptia.embrapa.br/web/cafe/preparo-do-solo-e-da-%C3%A1rea

## Potássio (K)

O potássio está relacionado ao crescimento e à fisiologia do cafeeiro. Materiais técnicos apontam seu papel na regulação osmótica, ativação enzimática e processos associados à fotossíntese e formação dos frutos. Na fase de formação, N e K aparecem entre os nutrientes mais exigidos para crescimento de ramos e folhas.

**Representação no projeto:**
- botão pressionado = condição de K considerada adequada;
- botão não pressionado = condição de K considerada inadequada.

**Fontes:**
- Embrapa Ater+ Digital — Fase de Formação do Café: https://www.atermaisdigital.cnptia.embrapa.br/web/cafe/faseformacao
- Incaper — Nutrição do Cafeeiro Conilon (referência complementar sobre funções do K): https://biblioteca.incaper.es.gov.br/digital/bitstream/item/702/1/livro2007cafeconilon11.pdf

## Chuva e irrigação

A irrigação do cafeeiro deve considerar a disponibilidade de água. Em um sistema inteligente, previsão de chuva pode ser usada para evitar irrigação desnecessária e reduzir desperdício.

**Aplicação no projeto opcional:**
1. o programa Python consulta uma API meteorológica;
2. identifica precipitação ou previsão de chuva;
3. produz uma informação simples, como `chuva_prevista = true`;
4. esse resultado poderá ser transferido manualmente ou via Monitor Serial ao ESP32;
5. se houver chuva prevista, a irrigação poderá ser suspensa mesmo que a umidade simulada esteja baixa.

**Fonte principal para manejo hídrico:**
- Embrapa Ater+ Digital — Fase de Produção / Manejo Hídrico: https://www.atermaisdigital.cnptia.embrapa.br/web/cafe/fase-de-producao-ou-manutencao

## Resumo dos valores que poderão ser usados na simulação

| Variável | Regra didática inicial |
|---|---|
| Cultura | Café arábica |
| pH simulado adequado | 5,5 a 6,0 |
| Umidade simulada adequada | >= 50% |
| Umidade simulada baixa | < 50% |
| N | booleano pelo botão |
| P | booleano pelo botão |
| K | booleano pelo botão |
| Chuva prevista | poderá bloquear a irrigação no opcional Python |

## Cuidados na definição da lógica

- A **umidade** deve ser o principal fator relacionado diretamente ao acionamento da irrigação.
- pH e NPK representam condições agronômicas relevantes, mas deficiência de nutriente não significa automaticamente necessidade de água.
- Por isso, a lógica final não deve tratar "N/P/K inadequado" simplesmente como sinônimo de "ligar a bomba".
- A atividade permite que o grupo combine os fatores; a combinação escolhida deverá ser explicada no README.
- Durante a demonstração, ao alterar N, P ou K, também deve ser alterado o LDR/pH conforme solicitado no enunciado.

## Próxima decisão do grupo

Com a pesquisa registrada, o próximo passo é preencher `docs/logica_irrigacao.md` e responder:

1. Quando exatamente a bomba deve ligar?
2. Em quais situações ela deve permanecer desligada?
3. Como pH e NPK entram na decisão sem confundir correção nutricional com irrigação?
4. Como a previsão de chuva do opcional Python poderá cancelar uma irrigação?
