# Python — Ir Além 1: API meteorológica

## Objetivo

Consultar uma API meteorológica pública e transformar a previsão de chuva em uma informação simples para a lógica de irrigação do ESP32.

A API escolhida é a **Open-Meteo Weather Forecast API**.

## Critério utilizado

O programa analisa as próximas 6 horas. `chuva_prevista` será verdadeiro quando pelo menos uma destas condições ocorrer:

- probabilidade máxima de precipitação >= 40%; ou
- precipitação acumulada prevista >= 1,0 mm.

Esses limites são critérios didáticos definidos para a simulação, e não uma recomendação agronômica universal.

## Execução

Na raiz do repositório:

```bash
python python/clima_api.py --latitude LATITUDE --longitude LONGITUDE
```

Exemplo:

```bash
python python/clima_api.py --latitude -19.9678 --longitude -44.1983
```

O script utiliza apenas a biblioteca padrão do Python, portanto não exige instalação de pacote externo.

## Saída

Quando a consulta funciona, o programa mostra a previsão e gera:

```text
CHUVA=SIM
```

ou:

```text
CHUVA=NAO
```

Esse comando pode ser copiado para o Monitor Serial do Wokwi.

## Falhas de conexão

O script trata:

- timeout;
- falha de conexão;
- erro HTTP;
- resposta JSON inválida;
- ausência de dados suficientes de precipitação.

Quando a consulta falha, nenhum comando `CHUVA=SIM/NAO` é gerado. Isso evita transformar uma falha de rede em uma decisão automática de irrigação.

## Integração com o ESP32

```text
Open-Meteo
    ↓
Python
    ↓
probabilidade + precipitação
    ↓
CHUVA=SIM / CHUVA=NAO
    ↓
Monitor Serial Wokwi
    ↓
ESP32
    ↓
Lógica de irrigação
    ↓
Relé / bomba
```

O ESP32 também aceita:

```text
STATUS
```
