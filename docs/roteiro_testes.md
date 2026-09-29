# Roteiro de testes — FarmTech Solutions Fase 2

Este documento será usado para validar o projeto antes da gravação do vídeo. Cada cenário deve ser executado no Wokwi e o resultado real deve ser comparado com o resultado esperado.

> Observação sobre os cenários numerados: os valores definidos abaixo servem como roteiro de referência. As evidências registradas ao final do documento correspondem aos valores realmente observados no Wokwi. Quando um cenário não foi reproduzido exatamente (por exemplo, N/P/K simultaneamente adequados), ele não deve ser tratado como execução exata, mesmo que a regra funcional correspondente tenha sido validada.

## Teste 1 — Solo simulado com umidade suficiente

**Objetivo:** confirmar que a bomba permanece desligada quando não há necessidade de irrigação.

- N: adequado
- P: adequado
- K: adequado
- pH simulado: 5,8
- Umidade: 70%
- Chuva prevista: não
- Resultado esperado: **relé OFF**
- Alertas esperados: nenhum
- Resultado obtido: foi validado um cenário real com umidade em aproximadamente 70,5%, pH em 5,98, chuva = NÃO e relé OFF. N, P e K estavam inadequados, portanto o cenário exato acima não foi reproduzido.
- Status: **regra hídrica validada; cenário exato não reproduzido**.

## Teste 2 — Umidade baixa

**Objetivo:** confirmar o acionamento básico da irrigação.

- N: adequado
- P: adequado
- K: adequado
- pH simulado: 5,8
- Umidade: 35%
- Chuva prevista: não
- Resultado esperado: **relé ON**
- Alertas esperados: nenhum
- Resultado obtido: umidade em 34,5%, pH em 5,98, chuva = NÃO e relé ON. N, P e K estavam inadequados.
- Status: **regra de acionamento por baixa umidade validada; cenário exato não reproduzido**.

## Teste 3 — Umidade baixa com pH inadequado

**Objetivo:** verificar se o sistema separa necessidade hídrica de condição química.

- N: adequado
- P: adequado
- K: adequado
- pH simulado: 4,8
- Umidade: 35%
- Chuva prevista: não
- Resultado esperado: **relé ON**
- Alerta esperado: pH fora da faixa
- Resultado obtido: umidade em 34,5%, pH em 4,81, chuva = NÃO, alerta de pH exibido e relé ON. N, P e K estavam inadequados.
- Status: **separação entre alerta de pH e decisão hídrica validada; cenário exato não reproduzido**.

## Teste 4 — Umidade baixa com nutriente inadequado

**Objetivo:** confirmar a leitura de NPK sem transformar deficiência nutricional diretamente em necessidade de água.

- N: inadequado
- P: adequado
- K: adequado
- pH simulado: 5,8
- Umidade: 40%
- Chuva prevista: não
- Resultado esperado: **relé ON**
- Alerta esperado: nitrogênio inadequado
- Resultado obtido: os botões N, P e K foram validados individualmente; com umidade baixa a bomba permaneceu ligada independentemente dos alertas nutricionais. A combinação exata N inadequado + P/K adequados não foi mantida simultaneamente.
- Status: **comportamento funcional validado; cenário exato não reproduzido**.

## Teste 5 — Alteração de NPK acompanhada de pH

**Objetivo:** demonstrar a exigência do enunciado de modificar também o LDR quando os estados de NPK forem alterados.

- Estado inicial dos botões: N, P e K inadequados;
- Botão alterado: N;
- Estado final observado: N adequado durante o acionamento; P e K inadequados;
- pH antes: 3,84;
- pH depois: 5,87;
- Resultado esperado: demonstrar alteração de NPK acompanhada por alteração do LDR/pH;
- Resultado obtido: alteração demonstrada no Wokwi e registrada no Monitor Serial;
- Passou? [x] Sim [ ] Não

## Teste 6 — Umidade alta com várias condições inadequadas

**Objetivo:** confirmar que alertas agronômicos não acionam a bomba quando a umidade já é suficiente.

- N: inadequado
- P: inadequado
- K: inadequado
- pH simulado: 6,7
- Umidade: 75%
- Chuva prevista: não
- Resultado esperado: **relé OFF**
- Alertas esperados: N, P, K e pH
- Resultado obtido: com umidade em aproximadamente 70,5%, N/P/K inadequados, pH em 5,98 e chuva = NÃO, o relé permaneceu OFF e os alertas nutricionais foram exibidos. O pH não estava fora da faixa nesse ensaio.
- Status: **bloqueio da irrigação por umidade suficiente validado; cenário exato não reproduzido**.

## Teste 7 — Previsão de chuva (opcional Python)

**Objetivo:** validar o bloqueio da irrigação por condição meteorológica.

- Umidade: 35%
- Chuva prevista pela API: sim
- Forma de transferência para ESP32: [x] manual via Monitor Serial
- Resultado esperado: **relé OFF por previsão de chuva**
- Resultado obtido: com umidade baixa e `CHUVA=SIM`, o relé permaneceu OFF e o Monitor Serial informou que havia chuva prevista.
- Passou? [x] Sim [ ] Não

## Teste 8 — Análise em R (opcional)

**Objetivo:** verificar se os dados coletados podem gerar informação estatística útil.

- Status: **não realizado**;
- Motivo: etapa opcional não priorizada para esta entrega;
- Observação: a entrega obrigatória e o opcional Python foram priorizados.

## Testes individuais dos componentes

Antes de testar a lógica completa, validar separadamente:

- [x] botão N muda de estado;
- [x] botão P muda de estado;
- [x] botão K muda de estado;
- [x] LDR apresenta valor analógico variável;
- [x] conversão do LDR altera o pH simulado;
- [x] DHT22 fornece valor de umidade;
- [x] relé pode ser ligado;
- [x] relé pode ser desligado;
- [x] Monitor Serial apresenta as leituras.

## Checklist antes do vídeo

- [x] todos os componentes aparecem no circuito;
- [x] nomes/funções dos componentes podem ser explicados pelo grupo;
- [x] Monitor Serial mostra as leituras;
- [x] relé liga e desliga nos cenários definidos;
- [x] alteração de NPK é demonstrável;
- [x] LDR é alterado junto com NPK durante a demonstração;
- [x] DHT22 pode ser ajustado durante o teste;
- [x] cenário de umidade baixa foi validado;
- [x] cenário de umidade suficiente foi validado;
- [x] opcional Python funciona, se for apresentado;
- [ ] opcional R funciona, se for apresentado;
- [ ] imagens finais foram salvas em `imagens/`;
- [x] README está atualizado;
- [ ] link do vídeo foi adicionado ao README.


## Evidência real já obtida no Wokwi

Validação parcial executada em 28/09/2026 com o circuito real do projeto:

- compilação e inicialização do ESP32: **aprovadas**;
- Monitor Serial: **aprovado**;
- leitura do DHT22: **24,0 °C e 40,0%**;
- leitura do LDR: **1123**, convertida para **pH 3,84**;
- N, P e K soltos: **INADEQUADOS**;
- alertas de N, P, K e pH: **aprovados**;
- com umidade em 40% e chuva = NÃO: **relé ON / bomba ligada**;
- após comando `CHUVA=SIM`, mantendo umidade em 40%: **relé OFF / bomba desligada**.

Esses resultados comprovam a regra principal com solo seco e o bloqueio da irrigação por previsão de chuva. Os cenários numerados acima ainda devem ser executados nos valores exatos definidos para fechar a validação formal.


### Validação dos botões NPK

Os três botões foram validados individualmente no Wokwi com `INPUT_PULLUP`:

- N pressionado: passou de INADEQUADO para ADEQUADO;
- P pressionado: passou de INADEQUADO para ADEQUADO;
- K pressionado: passou de INADEQUADO para ADEQUADO.

A bomba permaneceu desligada durante esses testes porque a umidade estava em aproximadamente 70,5%, confirmando que os alertas de nutrientes não acionam irrigação por si só.


### Umidade baixa com pH adequado — evidência parcial

Foi executado no Wokwi um cenário com:

- pH simulado: 5,98;
- umidade: 34,5%;
- chuva prevista: NÃO;
- N, P e K: inadequados.

Resultado observado: **relé ON / bomba ligada**, com a mensagem de que a umidade estava abaixo de 50% e não havia chuva prevista.

Esse resultado valida a regra hídrica com pH adequado, mas não encerra formalmente o Teste 2 porque os três nutrientes ainda não estavam simultaneamente em estado ADEQUADO.


### Umidade baixa com pH inadequado — evidência parcial

Foi executado no Wokwi um cenário com:

- pH simulado: 4,81;
- umidade: 34,5%;
- chuva prevista: NÃO;
- N, P e K: inadequados.

Resultado observado: o sistema exibiu alerta de pH fora da faixa e manteve **relé ON / bomba ligada** por causa da umidade abaixo de 50% e ausência de chuva prevista.

Esse resultado confirma que pH inadequado gera alerta agronômico, mas não bloqueia a irrigação quando há necessidade hídrica. O Teste 3 formal ainda pode ser repetido com N, P e K em estado ADEQUADO para reproduzir exatamente o cenário definido no roteiro.


### Comando STATUS

O comando `STATUS` foi validado no Monitor Serial. Com a condição meteorológica atual configurada como sem chuva, o ESP32 respondeu:

```text
[STATUS] Chuva prevista = NAO
```

Resultado: **aprovado**.


### Validação visual do relé

Foi confirmada no Wokwi a mudança visual do módulo de relé ao alternar a condição meteorológica entre `CHUVA=SIM` e `CHUVA=NAO`. A alteração visual acompanhou os estados exibidos no Monitor Serial (`RELE: OFF` e `RELE: ON`).

Resultado: **aprovado**.


### Teste 5 — demonstração final validada

A exigência de alterar NPK e também modificar o LDR/pH durante a demonstração foi validada no Wokwi.

Evidência observada:
- estado inicial recorrente: N inadequado e pH 3,84;
- o LDR foi alterado até o pH chegar a 5,87;
- em seguida, o botão N foi acionado e o Monitor Serial registrou N = ADEQUADO mantendo o pH em 5,87;
- a bomba permaneceu ligada porque a umidade estava em 40% e não havia chuva prevista.

Resultado: **aprovado**.
