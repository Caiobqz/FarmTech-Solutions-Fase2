# Planejamento das conexões no Wokwi

Este documento define uma proposta de pinos e a função de cada componente antes da montagem do circuito. A montagem deverá ser feita e conferida pelo grupo no Wokwi.

## Componentes obrigatórios

- 1 ESP32;
- 3 botões para representar N, P e K;
- 1 LDR/fotorresistor para representar pH;
- 1 DHT22 para representar umidade do solo;
- 1 módulo relé para representar a bomba d'água.

## Distribuição sugerida de pinos

| Componente | Função | Pino sugerido no ESP32 | Tipo |
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

## Ordem recomendada de montagem

1. Adicionar o ESP32.
2. Adicionar apenas o botão N e testar.
3. Adicionar P e K e testar os três.
4. Adicionar o LDR e observar a leitura analógica.
5. Adicionar o DHT22 e conferir a leitura de umidade.
6. Adicionar o relé e testar ON/OFF.
7. Somente depois juntar toda a lógica de irrigação.

Essa ordem facilita encontrar erros de ligação.

## O que salvar no repositório

Quando o circuito estiver funcionando, adicionar em `esp32/`:

- `sketch.ino` — código C/C++;
- `diagram.json` — circuito do Wokwi.

E em `imagens/`:

- `circuito-wokwi.png`;
- `irrigacao-ligada.png`;
- `irrigacao-desligada.png`.

## Checklist de montagem

- [ ] ESP32 adicionado;
- [ ] botão N conectado e testado;
- [ ] botão P conectado e testado;
- [ ] botão K conectado e testado;
- [ ] LDR conectado ao pino analógico;
- [ ] DHT22 conectado;
- [ ] relé conectado;
- [ ] todos os componentes compartilham as referências de alimentação/GND necessárias;
- [ ] Monitor Serial consegue mostrar as entradas;
- [ ] relé responde ao comando do ESP32;
- [ ] `diagram.json` foi salvo.

## Próximo passo prático

Depois de conferir este planejamento, abrir o Wokwi e montar **primeiro ESP32 + botão N**. Testar um componente por vez antes de montar o circuito inteiro.
