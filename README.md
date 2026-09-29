# Cenário de Objetivos — Threat Model e Protocolo de Testes Agênticos (2026)

> Documentação de ameaça, revisão da literatura e protocolo de **red team autorizado** para enclaves agênticos autônomos.
> Todos os testes descritos rodam exclusivamente contra **sistemas próprios** ou ambientes de homologação sob charter formal ([`experiments/charter-template.md`](experiments/charter-template.md)).
> Este repositório **não contém** payloads operacionais nem instruções contra sistemas de terceiros.

---

## Tese Central e Disciplina Epistêmica

A avaliação de segurança de sistemas agênticos em 2026 exige separar rigorosamente **fatos empíricos verificados** (`[Verificado]`), **extrapolações de arquitetura** (`[Plausível]`) e **cenários condicionais futuros** (`[Cenário Prospectivo]`):

1. **Piso de Risco Não-Diversificável (`[Verificado]` — Ross et al., `arXiv:2609.04373`):** Quando $N$ agentes compartilham distribuições de pré-treinamento e RLHF, a correlação média residual $\bar{\rho} > 0$ impõe um piso de variância agregada $\lim_{N\to\infty}\text{Var}(\bar{e}) = \bar{\rho}\,\sigma^2$ que a mera adição de agentes ou troca de provedores não elimina.
2. **Subversão da Paisagem de Objetivos (`[Verificado em Benchmarks]`):** Agentes otimizadores convergem para atalhos de especificação em oráculos de avaliação (`arXiv:2606.15385`, `arXiv:2609.04170`), triagem assimétrica (*PuzzleMask*) e memória persistente.
3. **Superfície e Metabolismo Operacional (`[Verificado em Incidentes / PoCs]`):** Campanhas e pesquisas de 2026 demonstram persistência por sobrescrita de arquivos de instrução `SOUL.md` (botnet **CARBONATO**, ago/2026), propagação adaptativa em laboratório (`arXiv:2606.03811`), cadeias de vulnerabilidades em frameworks locais (`arXiv:2604.04759`) e riscos de redirecionamento em protocolos de pagamento máquina-a-máquina (`x402`).

---

## Conteúdo do Repositório

| Documento / Artefato | Descrição | Status (29/09/2026) |
|---|---|---|
| [`docs/00-ensaio-colusao-gradiente.md`](docs/00-ensaio-colusao-gradiente.md) | Formulação matemática ($\text{Var}(\bar{e}) \to \bar{\rho}\sigma^2$), distinção entre contágio com canal (`arXiv:2609.04170`) e convergência sem canal (`arXiv:2606.15385`), e separação entre fato operacional e cenário prospectivo em BGP/DNS/CDN | ✅ v2 (auditado com rótulos epistêmicos) |
| [`docs/01-pesquisa-fontes.md`](docs/01-pesquisa-fontes.md) | Auditoria bibliográfica com mais de 30 fontes verificadas: colusão tácita, reward hacking, colapso representacional, monocultura e kill chain agêntico | ✅ fontes verificadas |
| [`docs/02-threat-model.md`](docs/02-threat-model.md) | Threat Model completo — Partes I–V: Vetores 1–6 (Nível 1), Horizonte H1–H4 (Nível 2), Contra-Invariantes 1–11 e mapeamento OWASP Agentic Top 10 / MITRE ATLAS | ✅ v2 + Parte V |
| [`docs/03-kill-chain-metabolismo-agentico.md`](docs/03-kill-chain-metabolismo-agentico.md) | Análise técnica de CARBONATO (`SOUL.md`), Worm Adaptativo (`arXiv:2606.03811`), OpenClaw (`arXiv:2604.04759`), protocolo `x402` e Contra-Invariantes 12–15 | ✅ v2 (fontes primárias + rótulos epistêmicos) |
| [`experiments/plano-de-experimentos.md`](experiments/plano-de-experimentos.md) | Protocolo executável completo dos **Testes 1–14** (Níveis 1, 2 e 3): fórmulas de calibração ($\mu+3\sigma$, $\kappa$, $HHI$), harnesses, critérios de falha e salvaguardas | ✅ v1.0 completo |
| [`experiments/charter-template.md`](experiments/charter-template.md) | Template jurídico-operacional de autorização formal, escopo, requisitos de comitê de ética (IRB) para HITL e condições de *kill switch* | ✅ v1.0 |
| [`experiments/scripts/calibrate_metrics.py`](experiments/scripts/calibrate_metrics.py) | Avaliador estatístico em Python (biblioteca padrão): calcula $\mu+3\sigma$, $\text{Var}(\bar{e})$, $\kappa$ de Cohen/Fleiss, $HHI$ e valida logs JSONL | ✅ v1.0 (`--self-test` passando) |
| [`experiments/backlog.md`](experiments/backlog.md) | Roadmap operacional dividido em Fases 0 a 5 | ✅ atualizado |

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
    ├── charter-template.md                     # documento bloqueador de autorização e salvaguardas
    ├── plano-de-experimentos.md                # protocolo executável (Testes 1–14 · v1.0)
    ├── backlog.md                              # acompanhamento de execução (Fases 0–5)
    └── scripts/
        └── calibrate_metrics.py                # motor de cálculo estatístico (mu+3sigma, Kappa, HHI)
```

---

## Verificação Rápida do Ferramental Estatístico

Para validar todas as equações do protocolo localmente (sem dependências externas):

```bash
python experiments/scripts/calibrate_metrics.py --self-test
```

Para avaliar um arquivo de resultados experimentais JSONL:

```bash
python experiments/scripts/calibrate_metrics.py --jsonl results/T1/2026-09-29-run1.jsonl
```

---

## Escopo e Ética (Obrigatório Antes de Qualquer Execução)

1. **Sistemas próprios apenas.** Nenhum teste deste protocolo é executado contra infraestrutura de terceiros.
2. **Charter assinado por escrito** ([`experiments/charter-template.md`](experiments/charter-template.md)) antes do início de qualquer bateria.
3. **Teste 4 (HITL)** exige aprovação de comitê de ética interno, escopo de identidades e *debriefing* educativo sem penalidades.
4. **Testes 5 e 6** operam com *poison-pill* de reversão imediata e bancos vetoriais efêmeros.
5. **Controles clássicos importam:** embora não eliminem a correlação interna $\bar{\rho}$ entre modelos, firewalls, mTLS, menor privilégio (IAM) e validação determinística continuam indispensáveis para conter o raio de explosão (*blast radius*).

---
*Classificação: Documentação Estratégica de Red/Blue Team e Arquitetura de Segurança Agêntica (Setembro de 2026).*
