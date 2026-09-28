# Roteiro de testes — FarmTech Solutions Fase 2

Este documento será usado para validar o projeto antes da gravação do vídeo. Cada cenário deve ser executado no Wokwi e o resultado real deve ser comparado com o resultado esperado.

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
- Resultado obtido:
- Passou? [ ] Sim [ ] Não

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
- Resultado obtido:
- Passou? [ ] Sim [ ] Não

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
- Resultado obtido:
- Passou? [ ] Sim [ ] Não

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
- Resultado obtido:
- Passou? [ ] Sim [ ] Não

## Teste 5 — Alteração de NPK acompanhada de pH

**Objetivo:** demonstrar a exigência do enunciado de modificar também o LDR quando os estados de NPK forem alterados.

- Estado inicial dos botões:
- Botão alterado:
- Estado final:
- pH antes:
- pH depois:
- Resultado esperado:
- Resultado obtido:
- Passou? [ ] Sim [ ] Não

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
- Resultado obtido:
- Passou? [ ] Sim [ ] Não

## Teste 7 — Previsão de chuva (opcional Python)

**Objetivo:** validar o bloqueio da irrigação por condição meteorológica.

- Umidade: 35%
- Chuva prevista pela API: sim
- Forma de transferência para ESP32: [ ] manual [ ] Monitor Serial
- Resultado esperado: **relé OFF por previsão de chuva**
- Resultado obtido:
- Passou? [ ] Sim [ ] Não

## Teste 8 — Análise em R (opcional)

**Objetivo:** verificar se os dados coletados podem gerar informação estatística útil.

- Arquivo utilizado:
- Quantidade de leituras:
- Média de umidade:
- Desvio padrão:
- Outras estatísticas:
- Interpretação:
- Passou? [ ] Sim [ ] Não

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

- [ ] todos os componentes aparecem no circuito;
- [ ] nomes/funções dos componentes podem ser explicados pelo grupo;
- [ ] Monitor Serial mostra as leituras;
- [ ] relé liga e desliga nos cenários definidos;
- [ ] alteração de NPK é demonstrável;
- [ ] LDR é alterado junto com NPK durante a demonstração;
- [ ] DHT22 pode ser ajustado durante o teste;
- [ ] cenário de umidade baixa foi validado;
- [ ] cenário de umidade suficiente foi validado;
- [ ] opcional Python funciona, se for apresentado;
- [ ] opcional R funciona, se for apresentado;
- [ ] imagens finais foram salvas em `imagens/`;
- [ ] README está atualizado;
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
