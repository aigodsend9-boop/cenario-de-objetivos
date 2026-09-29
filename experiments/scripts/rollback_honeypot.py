#!/usr/bin/env python3
"""
Script de Rollback e Expurgo de Honeypots / Atratores Agênticos
Projeto Cenário de Objetivos (2026) — Salvaguarda Operacional do Charter

Função:
  Executa a desmontagem atômica e irreversível de artefatos de teste,
  atratores de paisagem (T5), bancos vetoriais efêmeros (T6), credenciais de canary
  e caches gerados durante os experimentos de Red Team.

Uso:
  python rollback_honeypot.py --env staging --purge-vector-store
  python rollback_honeypot.py --dry-run
  python rollback_honeypot.py --status
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def get_default_workspace() -> Path:
    """Retorna a raiz do repositório/workspace."""
    current = Path(__file__).resolve().parent
    # Sobe de scripts -> experiments -> root
    if current.name == "scripts" and current.parent.name == "experiments":
        return current.parent.parent
    return current


def calculate_dir_hash(directory: Path) -> str:
    """Calcula hash SHA-256 consolidado dos arquivos em um diretório (se existir)."""
    if not directory.exists():
        return "DIR_NOT_FOUND"
    hasher = hashlib.sha256()
    for file_path in sorted(directory.rglob("*")):
        if file_path.is_file():
            hasher.update(file_path.name.encode("utf-8"))
            try:
                hasher.update(file_path.read_bytes())
            except Exception:
                pass
    return hasher.hexdigest()[:16]


def purge_vector_store(target_dir: Path, dry_run: bool = False) -> Dict[str, str | bool]:
    """Expurga índices vetoriais de teste e atratores de embeddings."""
    res = {"target": str(target_dir), "existed": target_dir.exists(), "purged": False}
    if not target_dir.exists():
        res["detail"] = "Diretorio vetorial efemero nao existe ou ja foi expurgado."
        return res

    pre_hash = calculate_dir_hash(target_dir)
    res["pre_hash"] = pre_hash

    if dry_run:
        res["detail"] = f"[DRY-RUN] Expurgo de {target_dir} simulado (hash: {pre_hash})."
        res["purged"] = True
        return res

    try:
        shutil.rmtree(target_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        # Cria arquivo sentinela indicando estado limpo
        sentinel = target_dir / ".purged_marker"
        sentinel.write_text(f"PURGED_AT={time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\n")
        res["purged"] = True
        res["detail"] = "Armazenamento vetorial resetado e marcador de expurgo gravado."
    except Exception as exc:
        res["purged"] = False
        res["error"] = str(exc)
    return res


def revoke_canary_tokens(token_registry: Path, dry_run: bool = False) -> Dict[str, str | int]:
    """Invalida tokens canary e chaves efêmeras usadas nos testes."""
    res = {"registry": str(token_registry), "revoked_count": 0}
    if not token_registry.exists():
        res["detail"] = "Nenhum registro de canary tokens ativo encontrado."
        return res

    if dry_run:
        res["detail"] = f"[DRY-RUN] Simulando revogação de tokens em {token_registry}."
        return res

    try:
        lines = token_registry.read_text(encoding="utf-8").splitlines()
        revoked = []
        for line in lines:
            if line.strip() and not line.startswith("#"):
                revoked.append(f"# REVOKED_{int(time.time())}: {line}")
            else:
                revoked.append(line)
        token_registry.write_text("\n".join(revoked) + "\n", encoding="utf-8")
        res["revoked_count"] = len(lines)
        res["detail"] = f"Total de {len(lines)} entradas de canary invalidadas com sucesso."
    except Exception as exc:
        res["error"] = str(exc)
    return res


def check_status(workspace: Path) -> int:
    """Verifica e exibe o status de contenção de artefatos de teste."""
    print("=" * 70)
    print("STATUS DE CONTENCAO E HIGIENE DE ARTEFATOS AGENTICOS")
    print("=" * 70)
    print(f"Workspace inspecionado: {workspace}")

    candidates = [
        workspace / "experiments" / "data" / "vector_store",
        workspace / "experiments" / "data" / "honeypots",
        workspace / "scratch" / "ephemeral_store",
    ]

    clean = True
    for c in candidates:
        if c.exists():
            files = list(c.rglob("*"))
            non_empty = [f for f in files if f.is_file() and f.name != ".purged_marker"]
            if non_empty:
                clean = False
                print(f"  [ATENCAO] Diretorio ativo contendo {len(non_empty)} artefatos: {c}")
            else:
                print(f"  [LIMPO] {c} (Vazio ou expurgado)")
        else:
            print(f"  [OK] {c} (Nao presente)")

    print("-" * 70)
    if clean:
        print("PARECER: Ambiente limpo e desarmado. Nao ha atratores ativos detectados.")
        return 0
    else:
        print("PARECER: Existem artefatos pendentes de expurgo! Execute com --purge-vector-store.")
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Script de Rollback e Expurgo de Honeypots/Atratores (Charter Salvaguarda)"
    )
    parser.add_argument(
        "--env",
        choices=["local", "staging", "homolog", "test"],
        default="local",
        help="Ambiente de execucao (default: local)",
    )
    parser.add_argument(
        "--purge-vector-store",
        action="store_true",
        help="Expurga indices vetoriais efemeros e atratores de memoria (T5 e T6)",
    )
    parser.add_argument(
        "--revoke-tokens",
        action="store_true",
        help="Invalida arquivos de credenciais canary e mock keys",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula as acoes de expurgo sem remover arquivos em disco",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Inspeciona e reporta o status de artefatos efemeros ativos",
    )
    parser.add_argument(
        "--vector-path",
        type=Path,
        default=None,
        help="Caminho customizado do armazenamento vetorial a ser limpo",
    )

    args = parser.parse_args()
    workspace = get_default_workspace()

    if args.status:
        return check_status(workspace)

    print("=" * 70)
    print(f"INICIANDO PROCEDIMENTO DE ROLLBACK / EXPURGO AGENTICO [{args.env.upper()}]")
    if args.dry_run:
        print("MODO: DRY-RUN (Nenhuma alteracao permanente sera gravada)")
    print("=" * 70)

    target_vector = args.vector_path or (workspace / "experiments" / "data" / "vector_store")
    token_registry = workspace / "experiments" / "data" / "canary_tokens.txt"

    # Se nenhum argumento especifico foi dado alem do ambiente, executa limpeza completa
    do_all = not (args.purge_vector_store or args.revoke_tokens)

    success = True

    if args.purge_vector_store or do_all:
        print(f"[*] Executando expurgo do armazenamento vetorial: {target_vector}")
        res_v = purge_vector_store(target_vector, dry_run=args.dry_run)
        print(f"    Resultado: {res_v.get('detail', 'OK')}")
        if "error" in res_v:
            print(f"    [ERRO]: {res_v['error']}")
            success = False

    if args.revoke_tokens or do_all:
        print(f"[*] Executando revogacao de canary tokens: {token_registry}")
        res_t = revoke_canary_tokens(token_registry, dry_run=args.dry_run)
        print(f"    Resultado: {res_t.get('detail', 'OK')}")
        if "error" in res_t:
            print(f"    [ERRO]: {res_t['error']}")
            success = False

    print("-" * 70)
    if success:
        print("[SUCESSO] Procedimento de rollback concluido conforme salvaguardas do Charter.")
        return 0
    else:
        print("[FALHA] Ocorreram erros durante o procedimento de rollback.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
