# FarmTech Solutions — Fase 2

Projeto acadêmico da FIAP voltado à simulação de um sistema de irrigação inteligente com ESP32 no Wokwi.

## Integrantes

- Caio Barros Queiroz
- Suellen Hellen Pereira Silva
- Paulo Vitor Isidoro Silva
- Kauê Cavalcanti Araujo

## Objetivo

Construir e documentar um sistema que simule a tomada de decisão de irrigação de uma lavoura a partir de:

- Nitrogênio (N) representado por botão;
- Fósforo (P) representado por botão;
- Potássio (K) representado por botão;
- pH representado por LDR;
- umidade do solo representada por DHT22;
- relé representando a bomba d'água.

A lógica de quando ligar ou desligar a irrigação será definida pelo grupo com base em uma cultura agrícola e em referências confiáveis.

## Cultura escolhida

**Café**

> Os limites de pH, umidade e demais critérios de irrigação ainda devem ser pesquisados e documentados com fonte antes de serem implementados no código.

## Estrutura planejada

```text
FarmTech-Solutions-Fase2/
├── esp32/          # circuito e código do ESP32
├── python/         # opcional: API meteorológica
├── r/              # opcional: análise estatística
├── dados/          # dados para análise, caso utilizados
├── imagens/        # imagens do circuito e testes
├── docs/           # pesquisa, lógica e roteiro de testes
├── CONTRIBUTING.md
└── README.md
```

## Requisitos obrigatórios

- [ ] Montar circuito no Wokwi com ESP32;
- [ ] Adicionar 3 botões para representar N, P e K;
- [ ] Adicionar LDR para simular o pH;
- [ ] Adicionar DHT22 para simular umidade do solo;
- [ ] Adicionar relé para representar a bomba;
- [ ] Programar a leitura dos sensores em C/C++;
- [ ] Definir e implementar a lógica de irrigação;
- [ ] Exibir leituras e estado da irrigação no Monitor Serial;
- [ ] Salvar o código C/C++ no GitHub;
- [ ] Salvar o `diagram.json` do Wokwi no GitHub;
- [ ] Adicionar imagens do circuito ao README;
- [ ] Explicar toda a lógica e as substituições didáticas no README;
- [ ] Publicar vídeo de até 5 minutos como não listado no YouTube;
- [ ] Adicionar o link do vídeo ao GitHub.

## Programa Ir Além

### Opcional 1 — Python + API meteorológica

- [ ] Consultar uma API meteorológica pública usando Python;
- [ ] Obter uma informação útil para a irrigação, como previsão/ocorrência de chuva;
- [ ] Integrar esse resultado à lógica do ESP32 de forma automática ou manual;
- [ ] Documentar como a integração funciona.

### Opcional 2 — R

- [ ] Criar uma análise estatística relacionada à irrigação;
- [ ] Utilizar dados como umidade, pH simulado ou acionamentos da bomba;
- [ ] Explicar como a análise poderia apoiar a decisão de irrigar ou não.

## Substituições didáticas da atividade

| Componente no Wokwi | Representação no projeto |
|---|---|
| Botão | nível/presença de N, P ou K |
| LDR | pH do solo |
| DHT22 | umidade do solo |
| Relé | bomba d'água |

Esses componentes não substituem sensores agrícolas reais. Eles serão utilizados somente para a simulação proposta pela atividade.

## Etapas do projeto

1. Pesquisar as necessidades do café;
2. Definir limites e critérios com fontes;
3. Criar a tabela de decisão da irrigação;
4. Montar o circuito no Wokwi;
5. Implementar as leituras no ESP32;
6. Implementar a decisão da bomba;
7. Testar diferentes cenários;
8. Desenvolver os opcionais, se o grupo decidir realizá-los;
9. Registrar imagens;
10. Finalizar documentação;
11. Gravar o vídeo;
12. Fazer a revisão final antes da entrega.

## Referências

As referências utilizadas para justificar pH, umidade, NPK e critérios de irrigação deverão ser adicionadas aqui pelo grupo.

Fontes recomendadas para pesquisa:

- Embrapa;
- EPAMIG;
- CONAB;
- IBGE;
- artigos científicos e materiais técnicos confiáveis.

## Vídeo

O link do vídeo de demonstração será adicionado aqui após a conclusão do projeto.
