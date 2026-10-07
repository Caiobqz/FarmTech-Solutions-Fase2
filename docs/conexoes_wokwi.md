# Conexões do circuito no Wokwi

Este documento registra os pinos definidos para o circuito em `esp32/diagram.json` e a função de cada componente. As conexões foram validadas durante a simulação no Wokwi.

## Componentes obrigatórios

- 1 ESP32;
- 3 botões para representar N, P e K;
- 1 LDR/fotorresistor para representar pH;
- 1 DHT22 para representar umidade do solo;
- 1 módulo relé para representar a bomba d'água.

## Distribuição de pinos utilizada

| Componente | Função | Pino no ESP32 | Tipo |
|---|---|---:|---|
| Botão N | estado do nitrogênio | GPIO 18 | digital |
| Botão P | estado do fósforo | GPIO 19 | digital |
| Botão K | estado do potássio | GPIO 21 | digital |
| LDR | pH simulado | GPIO 34 | analógico |
| DHT22 | umidade simulada do solo | GPIO 15 | digital |
| Relé | bomba de irrigação | GPIO 23 | saída digital |

Esses pinos foram escolhidos para manter a montagem simples e separar claramente entradas digitais, entrada analógica e saída.

## Botões N, P e K

Sugestão de montagem:

- um terminal do botão ligado ao GPIO correspondente;
- outro terminal ligado ao GND;
- no código, utilizar o resistor interno de pull-up do ESP32.

Com essa configuração:

- botão solto → leitura HIGH;
- botão pressionado → leitura LOW.

Na lógica do projeto, será necessário converter esse comportamento elétrico para a interpretação escolhida:

- pressionado → nutriente em condição adequada;
- solto → nutriente em condição inadequada.

> Essa inversão entre LOW elétrico e "adequado" é normal quando se utiliza `INPUT_PULLUP`. O grupo deve saber explicar isso.

## LDR como pH simulado

O LDR será conectado a uma entrada analógica, sugerida como **GPIO 34**.

O ESP32 trabalha normalmente com leituras analógicas em uma escala aproximada de:

```text
0 ... 4095
```

Para a atividade, esse valor será convertido didaticamente para:

```text
pH 0 ... 14
```

A faixa considerada adequada para a simulação será:

```text
5,5 ... 6,0
```

O LDR **não mede pH real**. Ele é apenas a substituição solicitada no enunciado.

## DHT22 como umidade do solo simulada

O pino de dados do DHT22 será ligado ao **GPIO 15**.

Na prática, o DHT22 mede umidade relativa do ar e temperatura. Para esta atividade, a leitura de umidade será interpretada como se fosse a umidade do solo.

Regra didática inicial:

- menor que 50% → solo simulado seco;
- 50% ou mais → umidade simulada suficiente.

## Relé como bomba

O sinal de controle do relé será ligado ao **GPIO 23**.

O relé representa a bomba d'água:

- relé ativo → irrigação ligada;
- relé inativo → irrigação desligada.

No Wokwi, o grupo deve observar se o componente escolhido trabalha como ativo em HIGH ou ativo em LOW e ajustar a lógica de acordo com o comportamento real da simulação.

## Alimentação

As conexões de alimentação dependem do componente selecionado no Wokwi. Durante a montagem:

- conferir VCC de cada componente;
- conferir GND comum;
- nunca definir a alimentação apenas pela aparência do componente;
- usar a documentação/descrição do próprio Wokwi quando houver dúvida.

## Ordem recomendada de validação

O circuito completo já está descrito em `esp32/diagram.json`. Para encontrar erros com facilidade, validar cada parte nesta ordem:

1. confirmar os três botões N, P e K;
2. variar o LDR e observar o pH simulado;
3. variar a umidade do DHT22;
4. testar o relé ligado e desligado;
5. testar `CHUVA=SIM`, `CHUVA=NAO` e `STATUS`;
6. executar os cenários completos de `docs/roteiro_testes.md`.

## O que salvar no repositório

Quando o circuito estiver funcionando, adicionar em `esp32/`:

- `sketch.ino` — código C/C++;
- `diagram.json` — circuito do Wokwi.

E em `imagens/`:

- `circuito-wokwi.png`;
- `irrigacao-ligada.png`;
- `irrigacao-desligada.png`.

## Checklist de montagem

- [x] ESP32 adicionado;
- [x] botão N conectado e testado;
- [x] botão P conectado e testado;
- [x] botão K conectado e testado;
- [x] LDR conectado ao pino analógico;
- [x] DHT22 conectado;
- [x] relé conectado;
- [x] todos os componentes compartilham as referências de alimentação/GND necessárias;
- [x] Monitor Serial consegue mostrar as entradas;
- [x] relé responde ao comando do ESP32;
- [x] `diagram.json` foi salvo.

## Estado da validação

O circuito foi compilado e validado no Wokwi. Os resultados observados estão documentados em `docs/roteiro_testes.md` e `docs/revisao_tecnica.md`.
