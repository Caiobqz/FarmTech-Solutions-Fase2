# Revisão técnica — Fase 2

Revisão realizada após a entrada do circuito ESP32/Wokwi e do opcional Python no repositório.

## O que já está implementado

- circuito definido em `esp32/diagram.json`;
- código C/C++ em `esp32/sketch.ino`;
- botões N, P e K;
- LDR para pH simulado;
- DHT22 para umidade simulada;
- relé como bomba;
- comandos `CHUVA=SIM`, `CHUVA=NAO` e `STATUS`;
- lógica de irrigação baseada em umidade e previsão de chuva;
- API Open-Meteo em `python/clima_api.py`;
- documentação de pesquisa, lógica e testes.

## Ajustes técnicos já realizados

### DHT22 no ESP32

O código foi alinhado à biblioteca `DHT sensor library for ESPx`, indicada no projeto para uso com ESP32/Wokwi.

Agora:

```cpp
#include <DHTesp.h>
```

e `esp32/libraries.txt` contém somente a biblioteca necessária.

### API meteorológica

`python/clima_api.py` passou a tratar:

- timeout;
- falha de conexão;
- erro HTTP;
- JSON inválido;
- ausência de dados suficientes.

Em caso de falha, o programa não gera automaticamente `CHUVA=SIM` ou `CHUVA=NAO`.

### Refatoração de legibilidade

O código foi reorganizado sem alterar a regra de negócio:

- `esp32/sketch.ino` foi dividido em funções menores para leitura de sensores, decisão de irrigação, controle do relé e mensagens do Monitor Serial;
- as leituras do ESP32 passaram a ser agrupadas em `LeiturasSensores`;
- pinos, limites e intervalo de leitura usam constantes nomeadas;
- `python/clima_api.py` foi dividido em funções para argumentos, URL, consulta, análise e exibição;
- latitude e longitude agora são validadas antes da consulta;
- o comportamento em caso de falha da API permanece seguro: nenhum comando de chuva é gerado sem dado válido.

### Serial Monitor no Wokwi

Durante a validação real, o Serial Monitor só passou a exibir corretamente a saída após ligar explicitamente a UART do ESP32 ao monitor virtual no `diagram.json`:

```text
ESP32 TX -> Serial Monitor RX
ESP32 RX -> Serial Monitor TX
```

O monitor também foi configurado com `display: "always"`. Essa configuração foi incorporada ao circuito versionado.

## Validações que ainda precisam ser executadas no Wokwi

- [x] circuito compila sem erro;
- [x] botão N altera o estado;
- [x] botão P altera o estado;
- [x] botão K altera o estado;
- [x] LDR modifica o pH simulado;
- [x] DHT22 modifica a umidade;
- [x] umidade < 50% e sem chuva liga o relé;
- [x] umidade >= 50% mantém o relé desligado;
- [x] `CHUVA=SIM` impede irrigação com solo seco;
- [x] `CHUVA=NAO` permite irrigação com solo seco;
- [x] `STATUS` mostra a condição atual de chuva;
- [x] alertas de NPK e pH aparecem corretamente.

## Entregáveis ainda pendentes

- [ ] preencher resultados reais em `docs/roteiro_testes.md`;
- [ ] adicionar `imagens/circuito-wokwi.png`;
- [ ] adicionar `imagens/irrigacao-ligada.png`;
- [ ] adicionar `imagens/irrigacao-desligada.png`;
- [ ] inserir as imagens no README principal;
- [ ] decidir se o grupo fará o opcional em R;
- [ ] gravar vídeo de até 5 minutos;
- [ ] publicar o vídeo como não listado;
- [ ] adicionar o link do vídeo ao README;
- [ ] revisão final antes da entrega.

## Prioridade

Nenhuma nova funcionalidade deve ser adicionada antes de validar o circuito atual. A próxima etapa é **teste funcional no Wokwi**.


### Confirmação visual do relé

A mudança visual do módulo de relé foi confirmada no Wokwi e acompanhou corretamente os estados ON/OFF informados pelo Monitor Serial.


### NPK + alteração do LDR/pH

A demonstração exigida no enunciado foi validada: o LDR foi alterado até pH 5,87 e o botão N foi acionado, aparecendo como ADEQUADO no Monitor Serial. A mudança de NPK e a mudança do pH foram demonstradas na mesma sequência de teste.
