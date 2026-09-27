"""Consulta a previsão de chuva no Open-Meteo para apoiar a irrigação.

Exemplo:
    python clima_api.py --latitude -19.9678 --longitude -44.1983

Regra didática:
- chuva prevista se a probabilidade máxima nas próximas 6 horas for >= 40%; OU
- chuva prevista se a precipitação acumulada nas próximas 6 horas for >= 1,0 mm.

Quando a consulta é válida, o programa gera um comando para o ESP32:
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


def criar_argumentos() -> argparse.Namespace:
    """Lê e valida latitude e longitude informadas pelo usuário."""
    parser = argparse.ArgumentParser(
        description="Consulta a previsão de chuva no Open-Meteo."
    )
    parser.add_argument("--latitude", type=float, required=True)
    parser.add_argument("--longitude", type=float, required=True)

    argumentos = parser.parse_args()

    if not -90 <= argumentos.latitude <= 90:
        parser.error("latitude deve estar entre -90 e 90.")

    if not -180 <= argumentos.longitude <= 180:
        parser.error("longitude deve estar entre -180 e 180.")

    return argumentos


def montar_url(latitude: float, longitude: float) -> str:
    """Monta a URL da consulta meteorológica."""
    parametros = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "precipitation_probability,precipitation",
        "forecast_hours": HORAS_ANALISADAS,
        "timezone": "auto",
    }

    return f"{API_URL}?{urllib.parse.urlencode(parametros)}"


def consultar_previsao(latitude: float, longitude: float) -> dict:
    """Consulta a API e retorna a resposta JSON convertida em dicionário."""
    url = montar_url(latitude, longitude)

    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_SEGUNDOS) as resposta:
            return json.load(resposta)

    except urllib.error.HTTPError as erro:
        raise RuntimeError(
            f"A API respondeu com erro HTTP {erro.code}."
        ) from erro

    except TimeoutError as erro:
        raise RuntimeError(
            "A API demorou muito para responder."
        ) from erro

    except urllib.error.URLError as erro:
        motivo = getattr(erro, "reason", erro)
        raise RuntimeError(
            f"Nao foi possivel conectar a API: {motivo}"
        ) from erro

    except (json.JSONDecodeError, UnicodeDecodeError) as erro:
        raise RuntimeError(
            "A API retornou uma resposta invalida."
        ) from erro


def somente_numeros(valores: list) -> list[float]:
    """Remove valores nulos ou inesperados retornados pela API."""
    return [
        float(valor)
        for valor in valores
        if isinstance(valor, (int, float)) and not isinstance(valor, bool)
    ]


def analisar_chuva(dados: dict) -> tuple[bool, float, float]:
    """Calcula probabilidade máxima, precipitação total e decisão de chuva."""
    dados_horarios = dados.get("hourly")

    if not isinstance(dados_horarios, dict):
        raise ValueError("A resposta da API nao contem dados horarios validos.")

    probabilidades = somente_numeros(
        dados_horarios.get("precipitation_probability", [])
    )
    precipitacoes = somente_numeros(
        dados_horarios.get("precipitation", [])
    )

    if not probabilidades or not precipitacoes:
        raise ValueError(
            "A resposta da API nao contem dados suficientes de precipitacao."
        )

    probabilidade_maxima = max(probabilidades)
    precipitacao_total = sum(precipitacoes)

    chuva_prevista = (
        probabilidade_maxima >= PROBABILIDADE_LIMITE
        or precipitacao_total >= PRECIPITACAO_LIMITE_MM
    )

    return chuva_prevista, probabilidade_maxima, precipitacao_total


def exibir_resultado(
    latitude: float,
    longitude: float,
    chuva_prevista: bool,
    probabilidade: float,
    precipitacao: float,
) -> None:
    """Exibe o resumo da consulta e o comando para o Monitor Serial."""
    comando = "CHUVA=SIM" if chuva_prevista else "CHUVA=NAO"

    print("===== FARMTECH SOLUTIONS =====")
    print("API: Open-Meteo")
    print(f"Consulta: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")
    print(
        "Probabilidade maxima de precipitacao "
        f"(proximas {HORAS_ANALISADAS}h): {probabilidade:.0f}%"
    )
    print(f"Precipitacao acumulada prevista: {precipitacao:.2f} mm")
    print(f"Chuva prevista: {'SIM' if chuva_prevista else 'NAO'}")
    print()
    print("Comando para o Monitor Serial do Wokwi:")
    print(comando)


def exibir_erro(erro: Exception) -> None:
    """Mostra uma falha sem gerar uma decisão meteorológica inválida."""
    print("===== FARMTECH SOLUTIONS =====")
    print("Falha na consulta meteorologica.")
    print("Motivo:", erro)
    print()
    print(
        "Nenhum comando CHUVA=SIM/NAO foi gerado. "
        "Use o ultimo dado valido ou repita a consulta."
    )


def main() -> int:
    argumentos = criar_argumentos()

    try:
        dados = consultar_previsao(argumentos.latitude, argumentos.longitude)
        chuva, probabilidade, precipitacao = analisar_chuva(dados)
    except (RuntimeError, ValueError) as erro:
        exibir_erro(erro)
        return 1

    exibir_resultado(
        argumentos.latitude,
        argumentos.longitude,
        chuva,
        probabilidade,
        precipitacao,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
