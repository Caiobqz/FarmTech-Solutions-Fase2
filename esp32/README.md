# ESP32 / Wokwi

Esta pasta contém o circuito e o código principal do sistema de irrigação da Fase 2.

## Arquivos

- `sketch.ino` — código C/C++ do ESP32;
- `diagram.json` — definição do circuito no Wokwi;
- `libraries.txt` — biblioteca necessária para o DHT22 no ESP32.

## Componentes

- 1 ESP32;
- 3 botões para representar N, P e K;
- 1 LDR para representar pH;
- 1 DHT22 para representar umidade do solo;
- 1 relé para representar a bomba d'água.

## Biblioteca do DHT22

O projeto utiliza:

```cpp
#include <DHTesp.h>
```

e o arquivo `libraries.txt` contém:

```text
DHT sensor library for ESPx
```

Essa combinação foi escolhida para manter o código alinhado à biblioteca recomendada pelo Wokwi para DHT22 com ESP32.

## Pinos

| Componente | GPIO |
|---|---:|
| Botão N | 18 |
| Botão P | 19 |
| Botão K | 21 |
| LDR | 34 |
| DHT22 | 15 |
| Relé | 23 |

## Lógica implementada

- botões N/P/K usam `INPUT_PULLUP`;
- LDR é convertido didaticamente para pH de 0 a 14;
- pH entre 5,5 e 6,0 é considerado adequado;
- umidade abaixo de 50% indica solo simulado seco;
- a bomba liga quando há umidade baixa e não há chuva prevista;
- `CHUVA=SIM` bloqueia a irrigação;
- NPK e pH inadequados geram alertas no Monitor Serial.

## Comandos do Monitor Serial

```text
CHUVA=SIM
CHUVA=NAO
STATUS
```

## Próxima etapa

A implementação está pronta para validação no Wokwi. Ainda é necessário executar os cenários de `docs/roteiro_testes.md` e registrar os resultados reais antes da gravação do vídeo.
