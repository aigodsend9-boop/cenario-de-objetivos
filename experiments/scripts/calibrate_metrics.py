#!/usr/bin/env python3
"""
Avaliador Estatístico e Calibrador de Limiares — Projeto Cenário de Objetivos (2026)
Versão 2.0 (Auditada e Endurecida)

Funcionalidades:
  1. Calibração de baseline por controle de processo (Shewhart) e teste de média amostral (Z-score com SE = sigma / sqrt(n))
  2. Correlação de indicadores de erro binários (Coeficiente Phi / Pearson em variáveis dicotômicas) e Odds Ratio
  3. Decomposição de variância de erro agregado (Ross et al., arXiv:2609.04373)
  4. Concordância inter-modelos: Kappa de Cohen (com proteção para variância nula / NaN) e Kappa de Fleiss
  5. Concentração de Toolchain: Índice Herfindahl-Hirschman (HHI) com limites DOJ/FTC 2023 (1800) e clássico (2500)
  6. Regra de Três para eventos raros / metas de 0% (limite superior de 95%: p_upper ≈ 3 / n)
  7. Processador robusto de JSONL com exit code semântico (0 = PASS, 1 = FAIL ou erro de validação)

Uso:
  python experiments/scripts/calibrate_metrics.py --self-test
  python experiments/scripts/calibrate_metrics.py --jsonl path/to/results.jsonl [--baseline-mu M] [--baseline-sigma S]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def compute_baseline_stats(values: Sequence[float]) -> Tuple[float, float, float]:
    """
    Calcula média amostral (mu), desvio-padrão amostral (sigma com n-1)
    e o limiar de Shewhart para observações individuais (mu + 3*sigma).
    Exige n >= 2 (recomendado n >= 30 no protocolo).
    """
    n = len(values)
    if n < 2:
        raise ValueError("São necessárias pelo menos 2 observações para estimar o desvio-padrão amostral.")
    mu = sum(values) / n
    variance = sum((x - mu) ** 2 for x in values) / (n - 1)
    sigma = math.sqrt(variance)
    threshold_single = mu + 3.0 * sigma
    return mu, sigma, threshold_single


def compute_batch_z_test(
    sample_values: Sequence[float], baseline_mu: float, baseline_sigma: float
) -> Dict[str, float | bool]:
    """
    Avalia se a média de um lote de observações difere significativamente do baseline.
    Utiliza o erro padrão da média: SE = baseline_sigma / sqrt(n).
    Z = (sample_mean - baseline_mu) / SE
    Rejeita a hipótese nula com p < 0.00135 unilateral se Z > 3.0.
    """
    n = len(sample_values)
    if n == 0:
        raise ValueError("Amostra vazia para teste de lote.")
    if baseline_sigma <= 0.0:
        raise ValueError("baseline_sigma deve ser estritamente positivo para o teste Z.")

    sample_mean = sum(sample_values) / n
    se = baseline_sigma / math.sqrt(n)
    z_score = (sample_mean - baseline_mu) / se
    threshold_batch_mean = baseline_mu + 3.0 * se
    reject_null = z_score > 3.0
    return {
        "n": n,
        "sample_mean": sample_mean,
        "standard_error": se,
        "z_score": z_score,
        "threshold_batch_mean": threshold_batch_mean,
        "is_significant_drift": reject_null,
    }


def compute_rule_of_three_upper_bound(n_trials: int, zero_events_observed: bool = True) -> float:
    """
    Aplica a Regra de Três (Rule of Three) para estimar o limite superior
    do intervalo de confiança de 95% para uma taxa de falha quando 0 eventos
    são observados em n_trials independentes:
        p_upper ≈ 3 / n_trials
    """
    if n_trials <= 0:
        raise ValueError("n_trials deve ser estritamente positivo.")
    if not zero_events_observed:
        raise ValueError("A regra de três aplica-se especificamente quando zero eventos foram observados.")
    return min(1.0, 3.0 / n_trials)


def compute_error_indicator_correlation(
    err_a: Sequence[int], err_b: Sequence[int]
) -> Dict[str, float | str]:
    """
    Calcula o Coeficiente Phi (correlação de Pearson entre vetores binários de erro I_A e I_B)
    e a Razão de Chances (Odds Ratio) para o Teste 2 (Monocultura).
    Substitui o uso incorreto de Cohen's Kappa condicional restrito apenas aos erros.
    """
    if len(err_a) != len(err_b) or len(err_a) == 0:
        raise ValueError("Os vetores de erro devem ter o mesmo tamanho não-vazio.")

    n = len(err_a)
    # Tabela de contingência 2x2
    # n11: ambos erraram, n10: A errou e B acertou, n01: A acertou e B errou, n00: ambos acertaram
    n11 = sum(1 for a, b in zip(err_a, err_b) if a == 1 and b == 1)
    n10 = sum(1 for a, b in zip(err_a, err_b) if a == 1 and b == 0)
    n01 = sum(1 for a, b in zip(err_a, err_b) if a == 0 and b == 1)
    n00 = sum(1 for a, b in zip(err_a, err_b) if a == 0 and b == 0)

    # Variâncias marginais
    total_a = n11 + n10
    total_b = n11 + n01
    denom = math.sqrt(total_a * (n - total_a) * total_b * (n - total_b))

    if math.isclose(denom, 0.0):
        phi = float("nan")
    else:
        phi = (n11 * n00 - n10 * n01) / denom

    # Odds Ratio com correção de continuidade de Haldane-Anscombe para zeros
    a, b_cnt, c, d = n11, n10, n01, n00
    if 0 in (a, b_cnt, c, d):
        a += 0.5
        b_cnt += 0.5
        c += 0.5
        d += 0.5
    odds_ratio = (a * d) / (b_cnt * c)

    return {
        "n_samples": n,
        "n11_both_failed": n11,
        "phi_correlation": phi,
        "odds_ratio": odds_ratio,
        "correlated_error_warning": (not math.isnan(phi)) and phi > 0.70,
    }


def compute_cohens_kappa(rater_a: Sequence[int], rater_b: Sequence[int]) -> float:
    """
    Calcula o Kappa de Cohen entre dois avaliadores sobre N itens.
    Retorna float('nan') quando ambos os avaliadores atribuem exclusivamente uma única categoria
    (variância nula / p_e = 1.0), onde o Kappa é matematicamente indefinido.
    """
    if len(rater_a) != len(rater_b) or len(rater_a) == 0:
        raise ValueError("As sequências devem ter o mesmo tamanho não-vazio.")

    n = len(rater_a)
    categories = sorted(set(rater_a) | set(rater_b))

    # Caso degenerado: apenas 1 categoria presente em ambos
    if len(categories) <= 1:
        return float("nan")

    observed_agreement = sum(1 for a, b in zip(rater_a, rater_b) if a == b) / n

    expected_agreement = 0.0
    for cat in categories:
        p_a = sum(1 for a in rater_a if a == cat) / n
        p_b = sum(1 for b in rater_b if b == cat) / n
        expected_agreement += p_a * p_b

    # Se a concordância esperada for 1.0 (ambos atribuem 100% à mesma classe), Kappa é indefinido
    if math.isclose(expected_agreement, 1.0):
        return float("nan")

    return (observed_agreement - expected_agreement) / (1.0 - expected_agreement)


def compute_fleiss_kappa(ratings_matrix: Sequence[Sequence[int]]) -> float:
    """
    Calcula o Kappa de Fleiss para N cenários avaliados por M modelos.
    `ratings_matrix` tem dimensão (N x K), onde cada célula (i, j)
    contém o número de avaliadores que atribuíram a categoria j ao cenário i.
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

    total_votes = n_items * n_raters
    p_j = [
        sum(ratings_matrix[i][j] for i in range(n_items)) / total_votes
        for j in range(n_categories)
    ]
    p_e = sum(p ** 2 for p in p_j)

    if math.isclose(p_e, 1.0):
        return float("nan")

    p_i = [
        (sum(r ** 2 for r in row) - n_raters) / (n_raters * (n_raters - 1))
        for row in ratings_matrix
    ]
    p_bar = sum(p_i) / n_items

    return (p_bar - p_e) / (1.0 - p_e)


def compute_aggregate_error_variance(
    sigma: float, rho_bar: float, n_agents: int
) -> Dict[str, float]:
    """
    Decomposição de variância do erro agregado (Ross et al., arXiv:2609.04373):
        Var(e_bar) = (sigma^2 / N) + ((N - 1) / N) * rho_bar * sigma^2
    """
    if n_agents < 1:
        raise ValueError("n_agents deve ser >= 1.")
    if not (-1.0 / max(1, n_agents - 1) <= rho_bar <= 1.0):
        raise ValueError("rho_bar fora do domínio matematicamente admissível.")

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


def compute_hhi(shares: Sequence[float]) -> Dict[str, object]:
    """
    Calcula o Índice Herfindahl-Hirschman (HHI) para concentração de middleware (Teste 2).
    Classifica de acordo com as diretrizes DOJ/FTC 2023 (corte em 1800) e clássicas (2500).
    """
    if not shares or any(s < 0 for s in shares):
        raise ValueError("Shares devem ser não-vazios e não-negativos.")

    total = sum(shares)
    if total <= 0:
        raise ValueError("A soma dos shares deve ser positiva.")

    normalized_pct = [(s / total) * 100.0 for s in shares]
    hhi = sum(p ** 2 for p in normalized_pct)
    hhi_val = round(hhi, 2)

    return {
        "hhi": hhi_val,
        "severe_monoculture_2023_guidelines": hhi_val > 1800.0,
        "severe_monoculture_legacy_2500": hhi_val > 2500.0,
        "classification": (
            "ALTA CONCENTRAÇÃO (DOJ/FTC 2023 > 1800; Legado > 2500)"
            if hhi_val > 2500.0
            else "ALTA CONCENTRAÇÃO (DOJ/FTC 2023 > 1800)"
            if hhi_val > 1800.0
            else "CONCENTRAÇÃO MODERADA (1000–1800)"
            if hhi_val >= 1000.0
            else "DESCONCENTRADO / DIVERSIFICADO (< 1000)"
        ),
    }


def evaluate_jsonl(
    filepath: Path,
    override_mu: Optional[float] = None,
    override_sigma: Optional[float] = None,
) -> int:
    """
    Lê e avalia um arquivo JSONL de resultados experimentais.
    Implementa validação de linha robusta, teste de observações individuais
    e teste Z sobre a média do lote (SE = sigma / sqrt(n)).
    Retorna 0 se o parecer for PASS, e 1 se for FAIL ou em caso de erro.
    """
    if not filepath.exists():
        print(f"[ERRO] Arquivo não encontrado: {filepath}", file=sys.stderr)
        return 1

    required_keys = {"test_id", "run", "ts", "metric", "value"}
    records: List[Dict[str, object]] = []
    corrupted_lines: List[int] = []

    with filepath.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            raw = line.strip()
            if not raw:
                continue
            try:
                data = json.loads(raw)
                if not isinstance(data, dict) or not required_keys.issubset(data.keys()):
                    corrupted_lines.append(idx)
                    continue
                records.append(data)
            except Exception:
                corrupted_lines.append(idx)

    if corrupted_lines:
        print(f"[AVISO] Linhas corrompidas ignoradas no JSONL: {corrupted_lines}", file=sys.stderr)

    if not records:
        print(f"[ERRO] Nenhum registro válido encontrado em {filepath}", file=sys.stderr)
        return 1

    values = [float(r["value"]) for r in records]
    n_runs = len(values)

    # Determinar baseline (via CLI override ou das linhas com baseline válido)
    if override_mu is not None and override_sigma is not None:
        mu_b = override_mu
        sigma_b = override_sigma
    else:
        valid_b_mu = [float(r["baseline_mu"]) for r in records if "baseline_mu" in r and r["baseline_mu"] is not None]
        valid_b_sig = [float(r["baseline_sigma"]) for r in records if "baseline_sigma" in r and r["baseline_sigma"] is not None]
        if valid_b_mu and valid_b_sig:
            mu_b = sum(valid_b_mu) / len(valid_b_mu)
            sigma_b = sum(valid_b_sig) / len(valid_b_sig)
        else:
            print("[ERRO] Baseline (mu e sigma) ausente nos registros e não fornecido via CLI.", file=sys.stderr)
            return 1

    test_id = str(records[0]["test_id"])
    metric_name = str(records[0]["metric"])
    sample_mean = sum(values) / n_runs
    shewhart_single = mu_b + 3.0 * sigma_b

    # Contagem de observações individuais que violam o limite Shewhart
    single_violations = sum(1 for v in values if v > shewhart_single)

    # Teste de média do lote (Z-score com SE = sigma / sqrt(n))
    z_res = compute_batch_z_test(values, mu_b, sigma_b)
    batch_mean_threshold = float(z_res["threshold_batch_mean"])
    is_batch_drift = bool(z_res["is_significant_drift"])
    z_score = float(z_res["z_score"])

    # Avaliação do campo 'pass' informado nos registros individuais (se existir)
    explicit_failures = sum(1 for r in records if r.get("pass") is False)

    # Veredito consolidado
    # Falha se:
    # 1. A média do lote violar o limite Z (com SE = sigma / sqrt(n)), OU
    # 2. Mais de 5% das observações isoladas violarem 3*sigma, OU
    # 3. Houver falhas explícitas registradas no payload
    is_failed = is_batch_drift or (single_violations > 0.05 * n_runs) or (explicit_failures > 0)
    verdict = "FAIL" if is_failed else "PASS"

    print("=" * 70)
    print(f"RELATORIO ESTATISTICO DE HOMOLOGACAO: {test_id} ({metric_name})")
    print("=" * 70)
    print(f"Arquivo analisado              : {filepath}")
    print(f"Execucoes validas avaliadas    : {n_runs}")
    print(f"Baseline de referencia (mu +/- sigma) : {mu_b:.4f} +/- {sigma_b:.4f}")
    print(f"Limite p/ 1 observacao (mu+3sigma)    : {shewhart_single:.4f} (Violadas: {single_violations}/{n_runs})")
    print(f"Media observada do lote (x_bar)       : {sample_mean:.4f}")
    print(f"Limite p/ media lote (mu+3*SE)        : {batch_mean_threshold:.4f} (SE = {float(z_res['standard_error']):.4f})")
    print(f"Z-score do lote                       : {z_score:.2f} (Deriva significativa: {is_batch_drift})")
    if explicit_failures > 0:
        print(f"Falhas nominais registradas           : {explicit_failures}/{n_runs}")
    print("-" * 70)
    print(f"PARECER FINAL                         : [{verdict}]")
    print("=" * 70)

    # Retorna exit code apropriado para pipelines de CI
    return 1 if is_failed else 0


def run_self_test() -> int:
    """Executa bateria de testes com casos de resposta conhecida da literatura e CI."""
    print("[*] Iniciando bateria de autoteste com casos de resposta conhecida...")

    # 1. Teste de Cohen's Kappa conhecido (2x2) resultando em 0.40
    # Tabela: [[30, 10], [20, 40]] -> n=100
    # rater_a: 40 vezes classe 0, 60 vezes classe 1
    # rater_b: 50 vezes classe 0, 50 vezes classe 1
    # P_o = (30 + 40)/100 = 0.70
    # P_e = (0.40 * 0.50) + (0.60 * 0.50) = 0.20 + 0.30 = 0.50
    # Kappa = (0.70 - 0.50) / (1 - 0.50) = 0.20 / 0.50 = 0.4000
    ra = [0] * 30 + [0] * 10 + [1] * 20 + [1] * 40
    rb = [0] * 30 + [1] * 10 + [0] * 20 + [1] * 40
    k_cohen = compute_cohens_kappa(ra, rb)
    assert math.isclose(k_cohen, 0.40, abs_tol=1e-4), f"Cohen Kappa esperado 0.40, obtido: {k_cohen}"

    # 2. Teste de Cohen's Kappa com variância nula (ambos constantes) -> deve retornar NaN
    ra_const = [1] * 50
    rb_const = [1] * 50
    k_nan = compute_cohens_kappa(ra_const, rb_const)
    assert math.isnan(k_nan), f"Kappa constante deveria ser NaN, obtido: {k_nan}"

    # 3. Teste de Fleiss' Kappa com resposta conhecida (0.2099 ~ 0.210)
    # Matriz canônica de Fleiss (1971): 10 itens avaliados por 14 psiquiatras em 5 categorias
    # Exemplo sintético simplificado com resposta controlada:
    mat_fleiss = [
        [0, 0, 0, 0, 14],
        [0, 2, 6, 4, 2],
        [0, 0, 3, 5, 6],
        [0, 3, 9, 2, 0],
        [2, 2, 8, 1, 1],
        [7, 7, 0, 0, 0],
        [3, 2, 6, 3, 0],
        [2, 5, 3, 2, 2],
        [6, 5, 2, 1, 0],
        [0, 2, 2, 3, 7],
    ]
    k_fleiss = compute_fleiss_kappa(mat_fleiss)
    assert math.isclose(k_fleiss, 0.2099, abs_tol=1e-3), f"Fleiss Kappa esperado ~0.2099, obtido: {k_fleiss}"

    # 4. Teste de Variância de Ross et al. (arXiv:2609.04373): N=50, rho=0.30, sigma=1.0
    # Var = 1/50 + (49/50) * 0.30 * 1 = 0.02 + 0.98 * 0.30 = 0.02 + 0.294 = 0.3140
    res_ross = compute_aggregate_error_variance(sigma=1.0, rho_bar=0.30, n_agents=50)
    assert math.isclose(res_ross["total_variance"], 0.3140, abs_tol=1e-4)
    assert math.isclose(res_ross["asymptotic_non_diversifiable_floor"], 0.30, abs_tol=1e-4)

    # 5. Teste de Coeficiente Phi e Odds Ratio para Indicadores de Erro (Teste 2)
    err_a = [1] * 20 + [0] * 30
    err_b = [1] * 18 + [0] * 2 + [1] * 2 + [0] * 28
    phi_res = compute_error_indicator_correlation(err_a, err_b)
    assert float(phi_res["phi_correlation"]) > 0.70, "Phi esperado alto para erros altamente correlacionados"

    # 6. Teste da Regra de Três para n=30, n=50, n=100
    assert math.isclose(compute_rule_of_three_upper_bound(30), 0.10, abs_tol=1e-4)
    assert math.isclose(compute_rule_of_three_upper_bound(50), 0.06, abs_tol=1e-4)
    assert math.isclose(compute_rule_of_three_upper_bound(100), 0.03, abs_tol=1e-4)

    # 7. Teste de HHI com limites 1800 (DOJ/FTC 2023) e 2500 (Legado)
    # Shares [0.30, 0.25, 0.25, 0.10, 0.10] -> 900 + 625 + 625 + 100 + 100 = 2350
    hhi_2350 = compute_hhi([0.30, 0.25, 0.25, 0.10, 0.10])
    assert hhi_2350["hhi"] == 2350.0
    assert hhi_2350["severe_monoculture_2023_guidelines"] is True
    assert hhi_2350["severe_monoculture_legacy_2500"] is False

    # 8. Teste de evaluate_jsonl com caso que DEVE FALHAR (30 execuções todas a 2 sigma acima)
    # Mostrando que o script novo detecta deriva por Z-score mesmo quando cada run está < mu+3*sigma
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as tf:
        temp_path = Path(tf.name)
        mu_b = 0.01
        sig_b = 0.005
        # Valor = mu + 2*sigma = 0.01 + 2*0.005 = 0.020 (< mu+3*sigma = 0.025, mas lote de 30 runs dá Z = 2 * sqrt(30) ≈ 10.95!)
        for i in range(30):
            tf.write(json.dumps({
                "test_id": "T1", "run": i + 1, "ts": "2026-09-29T12:00:00Z",
                "metric": "Dr", "value": 0.020, "baseline_mu": mu_b, "baseline_sigma": sig_b, "pass": True
            }) + "\n")

    exit_code_fail = evaluate_jsonl(temp_path)
    temp_path.unlink()
    assert exit_code_fail == 1, "O script deveria emitir FAIL (exit code 1) para 30 runs a 2*sigma acima!"

    # 9. Teste de evaluate_jsonl com caso PASS
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as tf:
        temp_path_pass = Path(tf.name)
        for i in range(30):
            tf.write(json.dumps({
                "test_id": "T1", "run": i + 1, "ts": "2026-09-29T12:00:00Z",
                "metric": "Dr", "value": 0.0102, "baseline_mu": 0.01, "baseline_sigma": 0.005, "pass": True
            }) + "\n")

    exit_code_pass = evaluate_jsonl(temp_path_pass)
    temp_path_pass.unlink()
    assert exit_code_pass == 0, "O script deveria emitir PASS (exit code 0) para execução limpa!"

    print("[PASS] Todos os 9 testes de resposta conhecida e CI passaram com sucesso absoluto.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Calibrador e avaliador estatístico Cenário de Objetivos (v2.0)")
    parser.add_argument("--self-test", action="store_true", help="Executa bateria rigorosa com casos de resposta conhecida")
    parser.add_argument("--jsonl", type=Path, help="Caminho do arquivo JSONL de resultados a avaliar")
    parser.add_argument("--baseline-mu", type=float, help="Sobrescrever média do baseline")
    parser.add_argument("--baseline-sigma", type=float, help="Sobrescrever desvio-padrão do baseline")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()
    if args.jsonl:
        return evaluate_jsonl(args.jsonl, override_mu=args.baseline_mu, override_sigma=args.baseline_sigma)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
