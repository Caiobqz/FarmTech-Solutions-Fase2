# ESP32 / Wokwi

Esta pasta será usada para os arquivos do circuito e do código principal do ESP32.

## Arquivos esperados ao final

- `sketch.ino` — código C/C++ do ESP32;
- `diagram.json` — definição do circuito no Wokwi.

## Componentes obrigatórios

- 1 ESP32;
- 3 botões para N, P e K;
- 1 LDR para representar pH;
- 1 DHT22 para representar umidade do solo;
- 1 relé para representar a bomba d'água.

## O que o grupo deve implementar

- leitura dos três botões;
- leitura analógica do LDR;
- conversão do LDR para uma escala de pH simulada definida pelo grupo;
- leitura da umidade do DHT22;
- lógica de decisão da irrigação;
- acionamento do relé;
- mensagens claras no Monitor Serial.

## Antes de programar

1. terminar a pesquisa em `docs/pesquisa_cafe.md`;
2. preencher a lógica em `docs/logica_irrigacao.md`;
3. definir os pinos usados no circuito;
4. só então transformar essa lógica em código.

Este arquivo não contém código pronto propositalmente, para que a implementação seja realizada e compreendida pelo grupo.
