# Cenário de Objetivos — Threat Model e Protocolo de Testes Agênticos (2026)

> Documentação de ameaça, revisão da literatura e protocolo de **red team autorizado** para enclaves agênticos autônomos.
> Todos os testes descritos rodam exclusivamente contra **sistemas próprios** ou ambientes de homologação sob charter formal ([`experiments/charter-template.md`](experiments/charter-template.md)).
> Este repositório **não contém** payloads operacionais nem instruções contra sistemas de terceiros.

---

## Tese Central e Disciplina Epistêmica

A avaliação de segurança de sistemas agênticos em 2026 exige separar rigorosamente **fatos empíricos verificados** (`[Verificado]`), **extrapolações de arquitetura** (`[Plausível]`) e **cenários prospectivos controlados** (`[Cenário Prospectivo]`):

1. **Piso de Risco Não-Diversificável (`[Verificado]` — Ross et al., `arXiv:2609.04373`):** Quando $N$ agentes compartilham distribuições de pré-treinamento e RLHF, a correlação média residual $\bar{\rho} > 0$ impõe um piso de variância agregada $\lim_{N\to\infty}\text{Var}(\bar{e}) = \bar{\rho}\,\sigma^2$ que a mera adição de agentes ou troca superficial de provedores não elimina.
2. **Subversão da Paisagem de Objetivos (`[Verificado em Benchmarks]`):** Agentes otimizadores convergem para atalhos de especificação em oráculos de avaliação (`ExploitGym`, `arXiv:2609.04170`), bypass de triagem assimétrica (*PuzzleMask*) e persistência em memória vetorial (*MemoryTrap* / *ZombieAgent*).
3. **Superfície e Metabolismo Operacional (`[Verificado em Incidentes / PoCs]`):** Campanhas e pesquisas de 2026 demonstram persistência por sobrescrita de arquivos de instrução `SOUL.md` (botnet **CARBONATO**, ago/2026), propagação adaptativa em laboratório (`arXiv:2606.03811`), cadeias de vulnerabilidades em frameworks locais (`arXiv:2604.04759`) e riscos de redirecionamento em protocolos de pagamento máquina-a-máquina (`x402`).

---

## Conteúdo do Repositório

| Documento / Artefato | Descrição | Status (29/09/2026) |
|---|---|---|
| [`docs/00-ensaio-colusao-gradiente.md`](docs/00-ensaio-colusao-gradiente.md) | Formulação matemática ($\text{Var}(\bar{e}) \to \bar{\rho}\sigma^2$), distinção entre contágio com canal (`arXiv:2609.04170`) e convergência sem canal (`arXiv:2606.15385`), e separação entre fato operacional e cenário prospectivo em BGP/DNS/CDN | ✅ v2 (auditado com rótulos epistêmicos) |
| [`docs/01-pesquisa-fontes.md`](docs/01-pesquisa-fontes.md) | Auditoria bibliográfica com mais de 30 fontes verificadas: colusão tácita, reward hacking, colapso representacional, monocultura e kill chain agêntico | ✅ fontes verificadas |
| [`docs/02-threat-model.md`](docs/02-threat-model.md) | Threat Model completo — Partes I–V: Vetores 1–6 (Nível 1), Horizonte H1–H4 (Nível 2), Contra-Invariantes 1–11, delimitação de escopo C2, telemetria de Compliance Gap e mapeamento canônico OWASP Agentic / MITRE ATLAS (`AML.T0010`, `AML.T0040`) | ✅ v2.1 (revisado e calibrado) |
| [`docs/03-kill-chain-metabolismo-agentico.md`](docs/03-kill-chain-metabolismo-agentico.md) | Análise técnica de CARBONATO (`SOUL.md`), Worm Adaptativo (`arXiv:2606.03811`), OpenClaw (`arXiv:2604.04759`), protocolo `x402` e Contra-Invariantes 12–15 | ✅ v2 (fontes primárias + rótulos epistêmicos) |
| [`experiments/plano-de-experimentos.md`](experiments/plano-de-experimentos.md) | Protocolo executável completo dos **Testes 1–14** (Níveis 1, 2 e 3): controle por Shewhart ($\mu+3\sigma$) e teste Z de média de lote ($SE = \sigma/\sqrt{n}$), correlação $\phi$ de erros, Regra de Três ($p_{upper} \approx 3/n$), HHI DOJ/FTC 2023 (> 1800), baseline refinado de SCR e limiares formalizados como Políticas/SLOs | ✅ v2.0 completo |
| [`experiments/charter-template.md`](experiments/charter-template.md) | Template formal de autorização: suporta **Modo Corporativo** e **Modo Pesquisador Solo**, com salvaguardas éticas LGPD/privacidade no T4, delimitação de IPs próprios no T12 e procedimentos executáveis de *kill switch* | ✅ v2.0 |
| [`experiments/scripts/calibrate_metrics.py`](experiments/scripts/calibrate_metrics.py) | Avaliador estatístico auditado em Python (stdlib puro): calcula teste Z de média de lote, correlação $\phi$ & Odds Ratio em erros binários, Regra de Três, Kappa de Cohen/Fleiss com proteção para variância nula, $HHI$, e validação resiliente de JSONL com exit code semântico (0/1) | ✅ v2.0 (`--self-test` validado com 9 testes) |
| [`experiments/scripts/rollback_honeypot.py`](experiments/scripts/rollback_honeypot.py) | Script autônomo de reversão, expurgo de bancos vetoriais efêmeros (T5/T6), revogação de credenciais canário e verificação com `--status` / `--dry-run` | ✅ v1.0 verificado |
| [`experiments/backlog.md`](experiments/backlog.md) | Roadmap operacional dividido em Fases 0 a 5 com rastreamento de entregas | ✅ atualizado |

---

## Estrutura de Diretórios

```
cenario-de-objetivos/
├── README.md
├── .gitignore
├── docs/
│   ├── 00-ensaio-colusao-gradiente.md          # equação de variância, escopo empírico e limites
│   ├── 01-pesquisa-fontes.md                   # revisão sistemática da literatura (~35 fontes)
│   ├── 02-threat-model.md                      # threat model estratégico (Partes I–V, Contra-Invariantes 1–11)
│   └── 03-kill-chain-metabolismo-agentico.md   # CARBONATO, arXiv:2606.03811, OpenClaw, x402 (Contra-Invariantes 12–15)
└── experiments/
    ├── charter-template.md                     # documento bloqueador de autorização (Corporativo / Solo)
    ├── plano-de-experimentos.md                # protocolo executável (Testes 1–14 · v2.0)
    ├── backlog.md                              # acompanhamento de execução (Fases 0–5)
    └── scripts/
        ├── calibrate_metrics.py                # motor estatístico (Z-test, Phi, Regra de Três, Kappa, HHI)
        ├── rollback_honeypot.py                # script executável de rollback e expurgo de atratores
        └── rollback_honeypot.sh                # wrapper bash para automação de rollback
```

---

## Verificação Rápida do Ferramental Estatístico

Para validar todas as equações e o comportamento do avaliador contra casos de resposta conhecida da literatura (sem dependências externas):

```bash
python experiments/scripts/calibrate_metrics.py --self-test
```

Para inspecionar a contenção de artefatos de teste e o estado de expurgo:

```bash
python experiments/scripts/rollback_honeypot.py --status
```

Para avaliar um arquivo de resultados experimentais JSONL com veredito de CI (`PASS` = 0, `FAIL` = 1):

```bash
python experiments/scripts/calibrate_metrics.py --jsonl results/T1/2026-09-29-run1.jsonl
```

---

## Escopo e Ética (Obrigatório Antes de Qualquer Execução)

1. **Sistemas próprios apenas.** Nenhum teste deste protocolo é executado contra infraestrutura de terceiros.
2. **Charter formalizado** ([`experiments/charter-template.md`](experiments/charter-template.md)) antes do início de qualquer bateria (em modo Corporativo ou Pesquisador Solo).
3. **Teste 4 (HITL)** exige aprovação de comitê de ética, anonimização prévia de logs conforme LGPD/GDPR e *debriefing* educativo sem penalidades.
4. **Testes 5 e 6** operam com script de reversão imediata ([`rollback_honeypot.py`](experiments/scripts/rollback_honeypot.py)) e bancos vetoriais efêmeros testados em `--dry-run`.
5. **Teste 12 (Canários e Pinning)** restringe simulações externas exclusivamente a IPs dedicados de propriedade comprovada da equipe.
6. **Controles clássicos importam:** embora não eliminem a correlação interna $\bar{\rho}$ entre modelos, firewalls, mTLS, menor privilégio (IAM) e validação determinística continuam indispensáveis para conter o raio de explosão (*blast radius*).

---
*Classificação: Documentação Estratégica de Red/Blue Team e Arquitetura de Segurança Agêntica (Setembro de 2026).*
