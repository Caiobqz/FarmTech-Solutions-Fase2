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
import urllib.parse
import urllib.request
from datetime import datetime

API_URL = "https://api.open-meteo.com/v1/forecast"
HORAS_ANALISADAS = 6
PROBABILIDADE_LIMITE = 40
PRECIPITACAO_LIMITE_MM = 1.0


def consultar_previsao(latitude: float, longitude: float) -> dict:
    parametros = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "precipitation_probability,precipitation",
        "forecast_hours": HORAS_ANALISADAS,
        "timezone": "auto",
    }
    url = f"{API_URL}?{urllib.parse.urlencode(parametros)}"

    with urllib.request.urlopen(url, timeout=15) as resposta:
        return json.load(resposta)


def analisar_chuva(dados: dict) -> tuple[bool, float, float]:
    hourly = dados["hourly"]
    probabilidades = hourly.get("precipitation_probability", [])
    precipitacoes = hourly.get("precipitation", [])

    probabilidade_maxima = max(probabilidades, default=0)
    precipitacao_total = sum(precipitacoes)

    chuva_prevista = (
        probabilidade_maxima >= PROBABILIDADE_LIMITE
        or precipitacao_total >= PRECIPITACAO_LIMITE_MM
    )

    return chuva_prevista, probabilidade_maxima, precipitacao_total


def main() -> None:
    parser = argparse.ArgumentParser(description="Consulta chuva no Open-Meteo.")
    parser.add_argument("--latitude", type=float, required=True)
    parser.add_argument("--longitude", type=float, required=True)
    args = parser.parse_args()

    dados = consultar_previsao(args.latitude, args.longitude)
    chuva, probabilidade, precipitacao = analisar_chuva(dados)

    print("===== FARMTECH SOLUTIONS =====")
    print("API: Open-Meteo")
    print(f"Consulta: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Latitude: {args.latitude}")
    print(f"Longitude: {args.longitude}")
    print(f"Probabilidade maxima de precipitacao (proximas {HORAS_ANALISADAS}h): {probabilidade:.0f}%")
    print(f"Precipitacao acumulada prevista: {precipitacao:.2f} mm")
    print(f"Chuva prevista: {'SIM' if chuva else 'NAO'}")
    print()
    print("Comando para o Monitor Serial do Wokwi:")
    print(f"CHUVA={'SIM' if chuva else 'NAO'}")


if __name__ == "__main__":
    main()
