"""Consulta a API pública Open-Meteo e gera a condição de chuva para o ESP32.

Uso:
    python clima_api.py --latitude -23.5505 --longitude -46.6333

O script verifica as próximas 6 horas e considera chuva prevista quando:
- a probabilidade máxima de precipitação for >= 40%; OU
- a precipitação acumulada prevista for >= 1.0 mm.

A saída inclui um comando que pode ser copiado para o Monitor Serial do Wokwi:
    CHUVA=SIM
ou
    CHUVA=NAO
"""

import argparse
import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

API_URL = "https://api.open-meteo.com/v1/forecast"
HORAS_ANALISADAS = 6
PROBABILIDADE_LIMITE = 40
PRECIPITACAO_LIMITE_MM = 1.0
TIMEOUT_SEGUNDOS = 30


def consultar_previsao(latitude: float, longitude: float) -> dict:
    parametros = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "precipitation_probability,precipitation",
        "forecast_hours": HORAS_ANALISADAS,
        "timezone": "auto",
    }
    url = f"{API_URL}?{urllib.parse.urlencode(parametros)}"

    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_SEGUNDOS) as resposta:
            return json.load(resposta)
    except urllib.error.HTTPError as erro:
        raise RuntimeError(
            f"A API respondeu com erro HTTP {erro.code}."
        ) from erro
    except urllib.error.URLError as erro:
        motivo = getattr(erro, "reason", erro)
        raise RuntimeError(
            f"Nao foi possivel conectar a API: {motivo}"
        ) from erro
    except TimeoutError as erro:
        raise RuntimeError(
            "A API demorou muito para responder."
        ) from erro
    except json.JSONDecodeError as erro:
        raise RuntimeError(
            "A API retornou uma resposta que nao pode ser interpretada como JSON."
        ) from erro


def analisar_chuva(dados: dict) -> tuple[bool, float, float]:
    hourly = dados.get("hourly")

    if not isinstance(hourly, dict):
        raise ValueError("A resposta da API nao contem dados horarios validos.")

    probabilidades = hourly.get("precipitation_probability", [])
    precipitacoes = hourly.get("precipitation", [])

    probabilidades_validas = [
        valor for valor in probabilidades
        if isinstance(valor, (int, float))
    ]
    precipitacoes_validas = [
        valor for valor in precipitacoes
        if isinstance(valor, (int, float))
    ]

    if not probabilidades_validas or not precipitacoes_validas:
        raise ValueError(
            "A resposta da API nao contem dados suficientes de precipitacao."
        )

    probabilidade_maxima = max(probabilidades_validas)
    precipitacao_total = sum(precipitacoes_validas)

    chuva_prevista = (
        probabilidade_maxima >= PROBABILIDADE_LIMITE
        or precipitacao_total >= PRECIPITACAO_LIMITE_MM
    )

    return chuva_prevista, probabilidade_maxima, precipitacao_total


def main() -> int:
    parser = argparse.ArgumentParser(description="Consulta chuva no Open-Meteo.")
    parser.add_argument("--latitude", type=float, required=True)
    parser.add_argument("--longitude", type=float, required=True)
    args = parser.parse_args()

    try:
        dados = consultar_previsao(args.latitude, args.longitude)
        chuva, probabilidade, precipitacao = analisar_chuva(dados)
    except (RuntimeError, ValueError) as erro:
        print("===== FARMTECH SOLUTIONS =====")
        print("Falha na consulta meteorologica.")
        print("Motivo:", erro)
        print()
        print(
            "Nenhum comando CHUVA=SIM/NAO foi gerado. "
            "Use o ultimo dado valido ou repita a consulta."
        )
        return 1

    print("===== FARMTECH SOLUTIONS =====")
    print("API: Open-Meteo")
    print(f"Consulta: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Latitude: {args.latitude}")
    print(f"Longitude: {args.longitude}")
    print(
        f"Probabilidade maxima de precipitacao "
        f"(proximas {HORAS_ANALISADAS}h): {probabilidade:.0f}%"
    )
    print(f"Precipitacao acumulada prevista: {precipitacao:.2f} mm")
    print(f"Chuva prevista: {'SIM' if chuva else 'NAO'}")
    print()
    print("Comando para o Monitor Serial do Wokwi:")
    print(f"CHUVA={'SIM' if chuva else 'NAO'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
