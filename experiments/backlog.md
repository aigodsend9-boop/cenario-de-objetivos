# Backlog — do repositório ao primeiro relatório

> Status: `⬜` pendente · `🟨` em andamento · `✅` concluído
> Regra: nenhum teste inicia sem charter assinado (Fase 0).

## Fase 0 — Fundação
- ⬜ Escolher nome/visibilidade do repo e publicar (comandos no README)
- ⬜ Template de **charter de autorização** (escopo, alvos próprios, janelas, owner, rollback)
- ⬜ Definir a aplicação-alvo de homologação (nossa) e descrever invariantes de estado → *insumo do T1*
- ⬜ Inventário de componentes do agente (gateway, MCP, embeddings, registries) com shares → *insumo do T2 (HHI)*
- ⬜ Instalar/definir stack de métricas: coletor JSONL + script de baseline (μ, σ) + gerador de gráficos

## Fase 1 — Testes 1–3
- ⬜ **T1** Dual-Oracle: implementar Oráculo Ômega (validador fora de banda) + baseline ≥ 30 runs
- ⬜ **T1**: injetar bypass documentado no ramo de homologação; rodar ≥ 30 runs; calcular Dr
- ⬜ **T2**: escrever bateria de ≥ 50 cenários de segurança rotulados (ground truth por painel humano)
- ⬜ **T2**: rodar multi-modelo × 3 seeds; calcular κ (Cohen/Fleiss) sobre erros
- ⬜ **T2**: script de HHI sobre o inventário de componentes
- ⬜ **T3**: construir corpus sintético de 100 amostras (marcadores neutros, sem payload real)
- ⬜ **T3**: harness SLM→fronteira; baseline de FNR; gate de regressão configurado

## Fase 2 — Testes 4–6
- ⬜ **T4**: charter + IRB interno + lista de participantes + protocolo de debriefing (**bloqueador para tudo da Fase 2**)
- ⬜ **T4**: roteiro de aquecimento (10 tarefas) + variações de ghost reset; baseline de BAR (≥ 40 solicitações)
- ⬜ **T5**: namespace de atrator isolado + poison-pill testado + tripwire de convergência ativo
- ⬜ **T5**: publicar atrator; observar por janela (7 dias); registrar MTTD
- ⬜ **T6**: base vetorial efêmera isolada; pares S0→S1 (≥ 30); medir MRR; destruir base ao final

## Fase 3 — Testes 7–10 (Nível 2)
- ⬜ **T8**: desenhar o grafo de avaliação atual (gerador de safety case → validadores → auditoria) e identificar o nó de fundo → *antes de T7*
- ⬜ **T7**: montar safety case interno mínimo + 3 model organisms (faking/sandbagging) em sandbox → medir SCR
- ⬜ **T9**: tabletop de insider da cadeia de charter; documentar pontos de veto ausentes → VT
- ⬜ **T10**: protocolo de compliance gap (condições monitorado/não-monitorado) em sandbox efêmera → Δ

## Fase 4 — Relatório e taxonomia
- ⬜ Consolidar PASS/FAIL/INCONCLUSIVE por teste + limitações
- ✅ Revalidar IDs do MITRE ATLAS no Navigator vigente (AML.T0080 e AML.T0110 consolidados sob AML.T0051.001, AML.T0043 e AML.T0020)
- ✅ Registrar formalmente a **lacuna H1/H2** no threat model (captura de critério e autocertificação não têm técnica canônica no ATLAS)
- ⬜ Retrospectiva: calibrar limiares com os dados reais de baseline (substituir 15% / 0.8 orientativos)

## Fase 5 — Expansão opcional (próximo ciclo)
- ⬜ Demo multi-agêntica da tese de convergência (enxame local, medir convergência sem canal)
- ⬜ Guia defensivo V5 para mantenedores open-source (proveniência, sigstore, canários de registry)
- ⬜ Instrumentar MTTD contínuo em produção (não só na janela do T5)
