"""Testes simples da regra meteorológica sem acessar a internet."""

import unittest

from clima_api import analisar_chuva


class TestAnaliseChuva(unittest.TestCase):
    def test_sem_chuva_prevista(self):
        dados = {
            "hourly": {
                "precipitation_probability": [10, 20, 30],
                "precipitation": [0.0, 0.0, 0.0],
            }
        }

        chuva, probabilidade, precipitacao = analisar_chuva(dados)

        self.assertFalse(chuva)
        self.assertEqual(probabilidade, 30.0)
        self.assertEqual(precipitacao, 0.0)

    def test_probabilidade_no_limite_indica_chuva(self):
        dados = {
            "hourly": {
                "precipitation_probability": [15, 40, 20],
                "precipitation": [0.0, 0.0, 0.0],
            }
        }

        chuva, _, _ = analisar_chuva(dados)

        self.assertTrue(chuva)

    def test_precipitacao_acumulada_no_limite_indica_chuva(self):
        dados = {
            "hourly": {
                "precipitation_probability": [10, 15, 20],
                "precipitation": [0.4, 0.3, 0.3],
            }
        }

        chuva, _, precipitacao = analisar_chuva(dados)

        self.assertTrue(chuva)
        self.assertAlmostEqual(precipitacao, 1.0)

    def test_valores_nulos_sao_ignorados(self):
        dados = {
            "hourly": {
                "precipitation_probability": [None, 25, None],
                "precipitation": [None, 0.2, None],
            }
        }

        chuva, probabilidade, precipitacao = analisar_chuva(dados)

        self.assertFalse(chuva)
        self.assertEqual(probabilidade, 25.0)
        self.assertEqual(precipitacao, 0.2)

    def test_resposta_sem_dados_horarios_e_rejeitada(self):
        with self.assertRaises(ValueError):
            analisar_chuva({})


if __name__ == "__main__":
    unittest.main()
