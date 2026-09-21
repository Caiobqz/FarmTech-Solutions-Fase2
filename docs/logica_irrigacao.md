# Lógica de irrigação — FarmTech Solutions Fase 2

Este documento define a regra funcional do sistema **antes** da implementação em C/C++. A intenção é que o grupo consiga explicar a decisão da bomba em linguagem natural e depois transforme essa regra em código.

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
- chuva prevista: poderá impedir a irrigação no opcional Python.

> O limite de 50% é uma aproximação didática para o Wokwi. Um DHT22 não mede água disponível no solo e não substitui um sensor agrícola real.

## Regra principal da bomba

A **umidade** será o fator principal para decidir a irrigação.

### Bomba ligada

A irrigação deve ser ligada quando:

1. a umidade simulada estiver abaixo de 50%; e
2. não houver previsão de chuva, caso o opcional meteorológico esteja sendo utilizado.

### Bomba desligada

A irrigação deve permanecer desligada quando:

- a umidade estiver em 50% ou mais; ou
- houver previsão de chuva no cenário do opcional Python.

## Como pH e NPK entram na lógica

pH e nutrientes são importantes para o estado agronômico da cultura, mas uma deficiência nutricional ou um pH fora da faixa não significa, por si só, que a planta precise receber mais água.

Por isso:

- pH fora de 5,5 a 6,0 gera **alerta de pH**;
- N inadequado gera **alerta de nitrogênio**;
- P inadequado gera **alerta de fósforo**;
- K inadequado gera **alerta de potássio**;
- esses alertas aparecem no Monitor Serial;
- a decisão de ligar a bomba continua sendo baseada principalmente na umidade e, opcionalmente, na previsão de chuva.

Essa separação evita confundir **manejo hídrico** com **correção química/nutricional**.

## Regra em linguagem natural

1. Ler os estados dos botões N, P e K.
2. Ler o valor do LDR.
3. Converter o valor do LDR para um pH simulado.
4. Ler a umidade do DHT22.
5. Verificar se N, P e K estão adequados.
6. Verificar se o pH está entre 5,5 e 6,0.
7. Gerar alertas para qualquer condição inadequada de NPK ou pH.
8. Verificar a umidade.
9. Se a umidade for menor que 50%, considerar que há necessidade de irrigação.
10. Se o opcional meteorológico estiver ativo e houver chuva prevista, cancelar a irrigação.
11. Caso contrário, ligar o relé.
12. Mostrar as leituras, alertas e decisão no Monitor Serial.

## Tabela de decisão base

| Cenário | N | P | K | pH | Umidade | Chuva | Resultado esperado |
|---|---|---|---|---:|---:|---|---|
| 1 | adequado | adequado | adequado | 5,8 | 70% | não | bomba OFF |
| 2 | adequado | adequado | adequado | 5,8 | 35% | não | bomba ON |
| 3 | adequado | adequado | adequado | 4,8 | 35% | não | bomba ON + alerta de pH |
| 4 | inadequado | adequado | adequado | 5,8 | 40% | não | bomba ON + alerta de N |
| 5 | adequado | adequado | adequado | 5,8 | 35% | sim | bomba OFF por previsão de chuva |
| 6 | inadequado | inadequado | inadequado | 6,7 | 75% | não | bomba OFF + alertas de NPK e pH |

## Exemplo de informações no Monitor Serial

O formato exato será definido durante a implementação, mas a saída deverá permitir entender facilmente o estado do sistema:

```text
===== FARMTECH SOLUTIONS =====
N: ADEQUADO
P: ADEQUADO
K: ADEQUADO
pH simulado: 5.8
Umidade simulada: 35%
Chuva prevista: NAO

Status: IRRIGACAO LIGADA
```

## Comportamento solicitado durante a demonstração

Ao alterar os botões N, P ou K, o grupo também deve alterar o LDR para representar uma mudança do pH, conforme orientado no enunciado da atividade.

## Próxima etapa

Com a lógica definida, a próxima tarefa é montar o circuito conforme `docs/conexoes_wokwi.md` e validar cada entrada individualmente antes de programar a decisão completa da bomba.
