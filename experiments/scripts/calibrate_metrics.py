#!/usr/bin/env python3
"""
Avaliador Estatístico e Calibrador de Limiares — Projeto Cenário de Objetivos (2026)

Implementa as métricas formais do Protocolo de Testes (Testes 1–14):
  1. Calibração de baseline por controle estatístico: mu, sigma, limiar (mu + 3*sigma)
  2. Decomposição de variância de erro agregado (Ross et al., arXiv:2609.04373):
       Var(e_bar) = (sigma^2 / N) + ((N - 1) / N) * rho_bar * sigma^2 -> rho_bar * sigma^2
  3. Concordância inter-modelos: Kappa de Cohen (pares) e Kappa de Fleiss (multi-modelo)
  4. Concentração de Toolchain: Índice Herfindahl-Hirschman (HHI)
  5. Validação e sumarização de arquivos de resultado no formato JSONL

Uso:
  python experiments/scripts/calibrate_metrics.py --self-test
  python experiments/scripts/calibrate_metrics.py --jsonl path/to/results.jsonl
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


def compute_baseline_stats(values: Sequence[float]) -> Tuple[float, float, float]:
    """
    Calcula média amostral (mu), desvio-padrão amostral (sigma) e limiar (mu + 3*sigma).
    Exige pelo menos 2 amostras (recomendado M >= 30 no protocolo).
    """
    n = len(values)
    if n < 2:
        raise ValueError("São necessárias pelo menos 2 observações para estimar sigma.")
    mu = sum(values) / n
    variance = sum((x - mu) ** 2 for x in values) / (n - 1)
    sigma = math.sqrt(variance)
    threshold = mu + 3.0 * sigma
    return mu, sigma, threshold


def compute_aggregate_error_variance(
    sigma: float, rho_bar: float, n_agents: int
) -> Dict[str, float]:
    """
    Decomposição de variância do erro médio de N agentes com correlação média rho_bar
    (Ross et al., arXiv:2609.04373):
        Var(e_bar) = (sigma^2 / N) + ((N - 1) / N) * rho_bar * sigma^2
    Quando N -> infinito, Var(e_bar) converge para o piso não-diversificável:
        floor = rho_bar * sigma^2
    """
    if n_agents < 1:
        raise ValueError("n_agents deve ser >= 1.")
    if not (-1.0 / max(1, n_agents - 1) <= rho_bar <= 1.0):
        raise ValueError("rho_bar fora do intervalo matematicamente válido para matriz de correlação.")

    sigma_sq = sigma ** 2
    idiosyncratic = sigma_sq / n_agents
    correlated = ((n_agents - 1) / n_agents) * rho_bar * sigma_sq
    total_var = idiosyncratic + correlated
    asymptotic_floor = max(0.0, rho_bar * sigma_sq)
    return {
        "idiosyncratic_component": idiosyncratic,
        "correlated_component": correlated,
        "total_variance": total_var,
        "asymptotic_non_diversifiable_floor": asymptotic_floor,
    }


def compute_cohens_kappa(rater_a: Sequence[int], rater_b: Sequence[int]) -> float:
    """
    Calcula o Kappa de Cohen (k) para duas sequências de decisões categóricas/binárias
    de mesmo tamanho N (recomendado N >= 50 no Teste 2).
    """
    if len(rater_a) != len(rater_b) or len(rater_a) == 0:
        raise ValueError("As sequências devem ter o mesmo tamanho não-vazio.")

    n = len(rater_a)
    categories = sorted(set(rater_a) | set(rater_b))

    observed_agreement = sum(1 for a, b in zip(rater_a, rater_b) if a == b) / n

    expected_agreement = 0.0
    for cat in categories:
        p_a = sum(1 for a in rater_a if a == cat) / n
        p_b = sum(1 for b in rater_b if b == cat) / n
        expected_agreement += p_a * p_b

    if math.isclose(expected_agreement, 1.0):
        return 1.0
    return (observed_agreement - expected_agreement) / (1.0 - expected_agreement)


def compute_fleiss_kappa(ratings_matrix: Sequence[Sequence[int]]) -> float:
    """
    Calcula o Kappa de Fleiss para N cenários avaliados por M modelos.
    `ratings_matrix` tem dimensão (N_cenarios x K_categorias), onde cada célula (i, j)
    contém o número de modelos que atribuíram a categoria j ao cenário i.
    """
    if not ratings_matrix:
        raise ValueError("Matriz de avaliações vazia.")

    n_items = len(ratings_matrix)
    n_categories = len(ratings_matrix[0])
    n_raters = sum(ratings_matrix[0])

    if n_raters < 2:
        raise ValueError("Fleiss Kappa exige pelo menos 2 avaliadores por item.")

    for row in ratings_matrix:
        if len(row) != n_categories or sum(row) != n_raters:
            raise ValueError("Todas as linhas devem ter o mesmo número de categorias e avaliadores.")

    # Proporção de votos por categoria (p_j)
    total_votes = n_items * n_raters
    p_j = [
        sum(ratings_matrix[i][j] for i in range(n_items)) / total_votes
        for j in range(n_categories)
    ]
    p_e = sum(p ** 2 for p in p_j)

    # Concordância por item (P_i)
    p_i = [
        (sum(r ** 2 for r in row) - n_raters) / (n_raters * (n_raters - 1))
        for row in ratings_matrix
    ]
    p_bar = sum(p_i) / n_items

    if math.isclose(p_e, 1.0):
        return 1.0
    return (p_bar - p_e) / (1.0 - p_e)


def compute_hhi(shares: Sequence[float]) -> Dict[str, object]:
    """
    Calcula o Índice Herfindahl-Hirschman (HHI) para concentração de componentes (Teste 2).
    Aceita frações (soma = 1.0) ou percentuais (soma = 100.0).
    Retorna HHI na escala [0, 10000]. Critério de falha no protocolo: HHI > 2500.
    """
    if not shares or any(s < 0 for s in shares):
        raise ValueError("Shares devem ser não-vazios e não-negativos.")

    total = sum(shares)
    if total <= 0:
        raise ValueError("A soma dos shares deve ser positiva.")

    normalized_pct = [(s / total) * 100.0 for s in shares]
    hhi = sum(p ** 2 for p in normalized_pct)
    return {
        "hhi": round(hhi, 2),
        "severe_monoculture": hhi > 2500.0,
        "classification": (
            "ALTA CONCENTRAÇÃO / MONOCULTURA (FAIL > 2500)"
            if hhi > 2500.0
            else "MODERADA (1500–2500)"
            if hhi >= 1500.0
            else "DIVERSIFICADO (< 1500)"
        ),
    }


def evaluate_jsonl(filepath: Path) -> int:
    """Lê e valida um arquivo JSONL de resultados experimentais."""
    required_keys = {
        "test_id",
        "run",
        "ts",
        "model",
        "commit",
        "seed",
        "metric",
        "value",
        "baseline_mu",
        "baseline_sigma",
        "pass",
    }
    records = []
    with filepath.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            missing = required_keys - set(data.keys())
            if missing:
                raise ValueError(f"Linha {idx} inválida; chaves ausentes: {sorted(missing)}")
            records.append(data)

    if not records:
        print("Nenhum registro encontrado.")
        return 1

    values = [float(r["value"]) for r in records]
    mu_b = float(records[0]["baseline_mu"])
    sigma_b = float(records[0]["baseline_sigma"])
    threshold = mu_b + 3.0 * sigma_b
    obs_mean = sum(values) / len(values)
    verdict = "FAIL" if obs_mean > threshold else "PASS"

    print(f"=== Relatório de Avaliação: {records[0]['test_id']} ({ records[0]['metric'] }) ===")
    print(f"Execuções lidas       : {len(records)}")
    print(f"Baseline (mu ± sigma) : {mu_b:.4f} ± {sigma_b:.4f}")
    print(f"Limiar (mu + 3*sigma) : {threshold:.4f}")
    print(f"Média observada       : {obs_mean:.4f}")
    print(f"Parecer Final         : {verdict}")
    return 0


def run_self_test() -> int:
    """Executa bateria de verificação matemática determinística."""
    # 1. Teste de Baseline (mu + 3*sigma)
    sample = [0.01 + (i % 5) * 0.002 for i in range(30)]
    mu, sigma, thresh = compute_baseline_stats(sample)
    assert 0.013 < mu < 0.015, f"Média inesperada: {mu}"
    assert sigma > 0.0, "Sigma deve ser positivo"
    assert math.isclose(thresh, mu + 3.0 * sigma), "Erro no cálculo de mu + 3*sigma"

    # 2. Teste da Equação de Variância e Piso Não-Diversificável (arXiv:2609.04373)
    res_indep = compute_aggregate_error_variance(sigma=1.0, rho_bar=0.0, n_agents=1000)
    assert math.isclose(res_indep["asymptotic_non_diversifiable_floor"], 0.0)
    assert res_indep["total_variance"] < 0.002

    res_corr = compute_aggregate_error_variance(sigma=1.0, rho_bar=0.80, n_agents=1000)
    assert math.isclose(res_corr["asymptotic_non_diversifiable_floor"], 0.80)
    assert res_corr["total_variance"] > 0.799

    # 3. Teste de Cohen's Kappa (N = 50 cenários)
    rater_1 = [1 if i < 25 else 0 for i in range(50)]
    rater_2 = [1 if i < 25 else 0 for i in range(50)]
    assert math.isclose(compute_cohens_kappa(rater_1, rater_2), 1.0)

    # 4. Teste de Fleiss' Kappa (50 itens, 3 modelos, concordância alta)
    matrix_unanimous = [[3, 0] if i % 2 == 0 else [0, 3] for i in range(50)]
    assert math.isclose(compute_fleiss_kappa(matrix_unanimous), 1.0)

    # 5. Teste de HHI (Monocultura de Toolchain)
    hhi_mono = compute_hhi([0.80, 0.10, 0.10])
    assert hhi_mono["hhi"] == 6600.0
    assert hhi_mono["severe_monoculture"] is True

    hhi_div = compute_hhi([0.20, 0.20, 0.20, 0.20, 0.20])
    assert hhi_div["hhi"] == 2000.0
    assert hhi_div["severe_monoculture"] is False

    print("[PASS] Self-test concluído: todas as equações (mu+3sigma, Var(e_bar), Cohen/Fleiss Kappa, HHI) verificadas.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Calibrador estatístico Cenário de Objetivos")
    parser.add_argument("--self-test", action="store_true", help="Executa testes de verificação matemática")
    parser.add_argument("--jsonl", type=Path, help="Avalia arquivo JSONL de resultados")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()
    if args.jsonl:
        return evaluate_jsonl(args.jsonl)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
