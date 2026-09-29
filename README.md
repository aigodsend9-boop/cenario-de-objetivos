# Cenário de Objetivos — Threat Model e Protocolo de Testes Agênticos (2026)

> Documentação de ameaça e protocolo de **red team autorizado** para enclaves agênticos autônomos.
> Todos os testes descritos rodam contra **sistemas próprios** ou ambientes de homologação sob charter formal.
> Este repositório **não contém** payloads operacionais nem instruções contra sistemas de terceiros.

## Tese central

O atacante sofisticado de 2026 não ataca o software nem o prompt — ataca a **paisagem de objetivos** (*objective landscape*), os **oráculos de avaliação** e a **memória persistente**. Agentes bem-intencionados, convergindo sobre o mesmo atrator, executam estados danosos sem qualquer canal de comunicação. O Nível 2 (Parte V) leva a regressão ao limite: **quem controla o critério controla o sistema** — do oráculo de runtime até o safety case de certificação.

## Conteúdo

| Documento | Descrição | Status (29/09/2026) |
|---|---|---|
| [`docs/01-pesquisa-fontes.md`](docs/01-pesquisa-fontes.md) | Pesquisa de base com ~30 fontes verificadas: convergência sem canal, monocultura, capability paradox, homogenização, risco sistêmico | ✅ fontes verificadas |
| [`docs/02-threat-model.md`](docs/02-threat-model.md) | Threat model completo — Partes I–V: 6 vetores (Nível 1), protocolo de testes 1–6, blueprint defensivo, mapeamento OWASP/ATLAS, Horizonte H1–H4 (Nível 2) + testes 7–10 | ✅ v2 + Parte V |
| [`experiments/plano-de-experimentos.md`](experiments/plano-de-experimentos.md) | Protocolo executável dos Testes 1–10: pré-requisitos, harness, fórmulas, calibração de limiares (μ+3σ), salvaguardas, schema de registro | 🚧 v0.1 |
| [`experiments/backlog.md`](experiments/backlog.md) | Backlog por fases (Fase 0 → primeiro relatório) | 🚧 v0.1 |

## Estrutura

```
cenario-de-objetivos/
├── README.md
├── .gitignore
├── docs/
│   ├── 01-pesquisa-fontes.md      # base empírica + referências
│   └── 02-threat-model.md         # documento de ameaça (Partes I–V)
└── experiments/
    ├── plano-de-experimentos.md   # protocolo executável (Testes 1–10)
    └── backlog.md                 # fases até o relatório
```

## Publicar no GitHub

Com [GitHub CLI](https://cli.github.com/) autenticado (`gh auth login`):

```bash
cd cenario-de-objetivos
git init
git add .
git commit -m "init: threat model (Partes I–V), pesquisa verificada e protocolo de testes"
gh repo create cenario-de-objetivos --public --source . --push
```

Sem `gh`: crie o repositório em <https://github.com/new>, depois:

```bash
cd cenario-de-objetivos
git init
git add . && git commit -m "init: threat model (Partes I–V)"
git remote add origin git@github.com:<seu-usuario>/cenario-de-objetivos.git
git branch -M main
git push -u origin main
```

## Escopo e ética (obrigatório antes de qualquer execução)

1. **Sistemas próprios apenas.** Nenhum teste deste protocolo roda contra infraestrutura de terceiros — sem essa condição, não é red team, é ataque.
2. **Charter de autorização por escrito** antes da Fase 2 (template no backlog).
3. **Teste 4 (HITL)** exige consentimento, escopo de identidades e *debriefing* imediato — análogo a exercícios de phishing simulado autorizados.
4. **Testes 5 e 6** operam com poison-pill de reversão e bases efêmeras — reverta sempre, sem exceção.
5. **Model organisms e corpora sintéticos** ficam em sandbox isolada; nada disso é publicado fora do repositório privado.

## Roadmap curto

- **Fase 0** — repo, charter, baseline do oráculo duplo
- **Fase 1** — Testes 1–3 (oráculo, monocultura/κ, ingestão/FNR)
- **Fase 2** — Testes 4–6 (HITL com IRB interno, atratores/MTTD, memória/MRR)
- **Fase 3** — Testes 7–10 (Nível 2: SCR, PRD, VT, Δ)
- **Fase 4** — relatório consolidado + revisão das lacunas ATLAS (H1/H2)

---
*Classificação: Documento Estratégico de Red/Blue Team e Arquitetura de Segurança Agêntica (2026).*
