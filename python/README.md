# Python — Ir Além 1: API meteorológica

## Objetivo

Consultar uma base meteorológica pública e transformar a previsão de chuva em uma variável simples para a lógica de irrigação do ESP32.

A API escolhida é a **Open-Meteo Weather Forecast API**, que disponibiliza previsão horária, incluindo probabilidade de precipitação e precipitação. A documentação oficial está em https://open-meteo.com/en/docs.

## Por que Open-Meteo?

- API pública;
- não exige chave de API para este uso acadêmico;
- possui previsão horária;
- fornece `precipitation_probability` e `precipitation`;
- permite consultar a localização por latitude e longitude.

## Critério utilizado

O programa analisa as próximas 6 horas. A variável `chuva_prevista` será `True` quando pelo menos uma destas condições ocorrer:

- probabilidade máxima de precipitação >= 40%; ou
- precipitação acumulada prevista >= 1,0 mm.

Esses limites são **critérios didáticos definidos pelo grupo para a simulação**, e não uma recomendação agronômica universal.

## Execução

No terminal:

```bash
python clima_api.py --latitude LATITUDE --longitude LONGITUDE
```

Exemplo apenas para teste:

```bash
python clima_api.py --latitude -23.5505 --longitude -46.6333
```

Use as coordenadas da área que o grupo deseja representar como fazenda.

## Integração com o ESP32/Wokwi

No plano gratuito, a integração automática entre um Python local e o Monitor Serial do Wokwi não é necessária para cumprir o enunciado. O programa imprime um comando:

```text
CHUVA=SIM
```

ou:

```text
CHUVA=NAO
```

Esse comando pode ser copiado para o Monitor Serial do Wokwi.

O ESP32 aceita também:

```text
STATUS
```

## Fluxo

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
