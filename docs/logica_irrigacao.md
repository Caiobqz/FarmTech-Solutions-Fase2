# Lógica de irrigação — FarmTech Solutions Fase 2

Este documento registra a regra funcional adotada pelo grupo e sua correspondência com a implementação do ESP32.

## Entradas do sistema

| Entrada | Componente | Tipo | Interpretação na simulação |
|---|---|---|---|
| Nitrogênio (N) | Botão | booleano | pressionado = condição adequada; solto = condição inadequada |
| Fósforo (P) | Botão | booleano | pressionado = condição adequada; solto = condição inadequada |
| Potássio (K) | Botão | booleano | pressionado = condição adequada; solto = condição inadequada |
| pH | LDR | analógico convertido | valor do LDR convertido didaticamente para escala de 0 a 14 |
| Umidade | DHT22 | numérico | usada como umidade simulada do solo |
| Chuva prevista | Python/API (opcional) | booleano | true = há previsão de chuva; false = não há |

## Saída principal

| Saída | Componente | Estados |
|---|---|---|
| Irrigação | Relé | ligada / desligada |

O relé representa a bomba d'água.

## Valores adotados para a simulação

Com base na pesquisa registrada em `docs/pesquisa_cafe.md`:

- pH simulado adequado: **5,5 a 6,0**;
- umidade simulada baixa: **menor que 50%**;
- umidade simulada suficiente: **50% ou mais**;
- N, P e K: estados booleanos;
- chuva prevista: pode impedir a irrigação no opcional Python.

> O limite de 50% é uma aproximação didática para o Wokwi. Um DHT22 não mede água disponível no solo e não substitui um sensor agrícola real.

## Regra principal da bomba

A **umidade** é o fator principal para decidir a irrigação.

### Bomba ligada

A irrigação é ligada quando:

1. a umidade simulada está abaixo de 50%; e
2. não há chuva prevista.

### Bomba desligada

A irrigação permanece desligada quando:

- a umidade está em 50% ou mais; ou
- há chuva prevista.

## Como pH e NPK entram na lógica

pH e nutrientes são importantes para o estado agronômico da cultura, mas uma deficiência nutricional ou um pH fora da faixa não significa, por si só, necessidade de mais água.

Por isso:

- pH fora de 5,5 a 6,0 gera **alerta de pH**;
- N inadequado gera **alerta de nitrogênio**;
- P inadequado gera **alerta de fósforo**;
- K inadequado gera **alerta de potássio**;
- esses alertas aparecem no Monitor Serial;
- a decisão de ligar a bomba continua baseada na umidade e na previsão de chuva.

Essa separação evita confundir **manejo hídrico** com **correção química/nutricional**.

## Fluxo em linguagem natural

1. Ler os botões N, P e K.
2. Ler o LDR.
3. Converter o LDR para pH simulado.
4. Ler a umidade do DHT22.
5. Verificar NPK e pH e gerar alertas.
6. Verificar se a umidade está abaixo de 50%.
7. Verificar a condição de chuva recebida pelo Monitor Serial.
8. Se o solo estiver seco e não houver chuva prevista, ligar o relé.
9. Caso contrário, manter o relé desligado.
10. Mostrar leituras, alertas e decisão no Monitor Serial.

## Tabela de decisão base

| Cenário | N | P | K | pH | Umidade | Chuva | Resultado esperado |
|---|---|---|---|---:|---:|---|---|
| 1 | adequado | adequado | adequado | 5,8 | 70% | não | bomba OFF |
| 2 | adequado | adequado | adequado | 5,8 | 35% | não | bomba ON |
| 3 | adequado | adequado | adequado | 4,8 | 35% | não | bomba ON + alerta de pH |
| 4 | inadequado | adequado | adequado | 5,8 | 40% | não | bomba ON + alerta de N |
| 5 | adequado | adequado | adequado | 5,8 | 35% | sim | bomba OFF por previsão de chuva |
| 6 | inadequado | inadequado | inadequado | 6,7 | 75% | não | bomba OFF + alertas de NPK e pH |

## Comportamento durante a demonstração

Ao alterar os botões N, P ou K, o grupo também deve alterar o LDR para representar uma mudança do pH, conforme orientado no enunciado.

## Estado atual

A lógica já foi transformada em código em `esp32/sketch.ino`. A próxima etapa é **validar no Wokwi** os cenários descritos em `docs/roteiro_testes.md` e registrar os resultados reais.
