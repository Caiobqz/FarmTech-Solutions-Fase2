# Planejamento da lógica de irrigação

Este arquivo será preenchido antes da implementação do código C/C++. A ideia é definir a regra de decisão primeiro e só depois transformá-la em código.

## Entradas do sistema

| Entrada | Componente | Tipo de dado | Significado |
|---|---|---|---|
| N | botão | booleano | nível/presença simulada de nitrogênio |
| P | botão | booleano | nível/presença simulada de fósforo |
| K | botão | booleano | nível/presença simulada de potássio |
| pH | LDR | analógico convertido | pH simulado |
| Umidade | DHT22 | numérico | umidade simulada do solo |
| Chuva | Python/API, opcional | booleano ou numérico | condição meteorológica usada no Ir Além |

## Saída

| Saída | Componente | Estado |
|---|---|---|
| Irrigação | relé | ligada/desligada |

## Valores que ainda precisam ser definidos pelo grupo

- faixa de pH utilizada: **a pesquisar**;
- limite de umidade utilizado: **a pesquisar**;
- influência de N, P e K na decisão: **a definir**;
- comportamento quando houver previsão de chuva: **a definir**.

## Tabela de decisão

Preencher depois da pesquisa:

| Cenário | N | P | K | pH | Umidade | Chuva | Resultado esperado |
|---|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |

## Fluxo lógico em linguagem natural

Preencher com frases antes de programar, por exemplo:

1. Ler os sensores.
2. Conferir se os valores estão dentro das condições definidas pelo grupo.
3. Avaliar a umidade.
4. Avaliar a condição meteorológica, se o opcional for implementado.
5. Decidir se o relé deve ligar ou desligar.
6. Mostrar as leituras e a decisão no Monitor Serial.

> Este documento propositalmente não contém a solução final. A lógica deverá ser definida pelo grupo após a pesquisa.
