# Backlog — Do Repositório ao Primeiro Relatório Experimental

> Status: `⬜` pendente · `🟨` em andamento · `✅` concluído
> Regra: nenhum teste em homologação inicia sem o [`experiments/charter-template.md`](charter-template.md) assinado (Fase 0).

## Fase 0 — Fundação e Ferramental Estatístico
- ✅ Escolher nome/visibilidade do repo e publicar no GitHub (`aigodsend9-boop/cenario-de-objetivos`)
- ✅ Criar template de **charter de autorização** ([`experiments/charter-template.md`](charter-template.md)) com salvaguardas éticas, escopo e *kill switch*
- ✅ Expandir protocolo executável para **v1.0 (Testes 1–14)** ([`experiments/plano-de-experimentos.md`](plano-de-experimentos.md))
- ✅ Implementar e verificar avaliador estatístico ([`experiments/scripts/calibrate_metrics.py`](scripts/calibrate_metrics.py): $\mu+3\sigma$, $\text{Var}(\bar{e})$, $\kappa$ de Cohen/Fleiss, $HHI$)
- ⬜ Definir a aplicação-alvo de homologação própria e descrever invariantes de estado → *insumo do T1*
- ⬜ Levantar o inventário real de componentes do agente (gateway, MCP, embeddings, registries) com shares → *insumo do T2 (HHI)*

## Fase 1 — Testes 1–3 (Oráculos, Monocultura e Triagem)
- ⬜ **T1** Dual-Oracle: implementar Oráculo Ômega (validador fora de banda) + baseline $\ge 30$ runs
- ⬜ **T1**: injetar bypass documentado no ramo de homologação; rodar $\ge 30$ runs; calcular $D_r$
- ⬜ **T2**: escrever bateria de $\ge 50$ cenários de segurança rotulados (ground truth por painel humano)
- ⬜ **T2**: rodar multi-modelo $\times 3$ seeds; calcular $\kappa$ (Cohen/Fleiss) sobre erros via `calibrate_metrics.py`
- ⬜ **T2**: rodar cálculo de $HHI$ sobre o inventário de componentes
- ⬜ **T3**: construir corpus sintético de 100 amostras (marcadores neutros de rota em homologação)
- ⬜ **T3**: harness SLM $\to$ fronteira; medir $FNR$; configurar gate de regressão

## Fase 2 — Testes 4–6 (HITL, Atratores e Memória Persistente)
- ⬜ **T4**: charter assinado + IRB interno + lista de participantes + protocolo de debriefing (**bloqueador da Fase 2**)
- ⬜ **T4**: roteiro de aquecimento (10 tarefas) + variações de *ghost reset*; medir $BAR$ ($\ge 40$ solicitações) vs. interface de *diff* puro
- ⬜ **T5**: namespace de atrator isolado + *poison-pill* testado + tripwire de convergência ativo
- ⬜ **T5**: publicar atrator canário em homologação; medir $MTTD$
- ⬜ **T6**: base vetorial efêmera isolada; rodar $\ge 30$ pares $(S_0 \to S_1)$; medir $MRR$; destruir base ao final

## Fase 3 — Testes 7–10 (Nível 2: O Bombardeio do Critério)
- ⬜ **T8**: mapear estaticamente o grafo de avaliação atual (gerador de safety case $\to$ validadores $\to$ auditoria) e verificar ausência de ciclos fechados ($PRD$) → *antes de T7*
- ⬜ **T7**: montar safety case interno mínimo + 3 *model organisms* (faking/sandbagging) em sandbox → medir $SCR$
- ⬜ **T9**: exercício *tabletop* de insider na cadeia de charter; documentar pontos sem quórum $M$-de-$N$ → $VT$
- ⬜ **T10**: protocolo de *compliance gap* (condições monitorado vs. não-monitorado) em sandbox efêmera → $\Delta$

## Fase 4 — Testes 11–14 (Nível 3: Superfície e Metabolismo Agêntico · `docs/03`)
- ⬜ **T11**: validar bloqueio de 100% na inicialização para arquivos `SOUL.md` / `SKILL.md` sem assinatura criptográfica válida ($UER = 0\%$)
- ⬜ **T12**: disparar chave canário de LLM (`sk-canary-*`) em homologação e medir latência de alerta ($MTTD_{key} \le 60\text{s}$) e bloqueio mTLS/IP
- ⬜ **T13**: testar 50 respostas HTTP `402 Payment Required` simuladas com `payTo` dinâmico via IPI contra o proxy determinístico ($PSR = 0\%$)
- ⬜ **T14**: simular varredura interna combinada com carga de inferência local/remota em sub-rede isolada e medir detecção correlacionada ($\le 5\text{ min}$)

## Fase 5 — Relatório Consolidado e Taxonomia
- ✅ Revalidar IDs do MITRE ATLAS no Navigator vigente (`AML.T0080` e `AML.T0110` consolidados sob `AML.T0051.001`, `AML.T0043` e `AML.T0020`)
- ✅ Registrar formalmente a **lacuna H1/H2** no threat model (captura de critério e autocertificação não têm técnica canônica no ATLAS)
- ✅ Auditar documentos `00` e `03` com rótulos epistêmicos (`[Verificado]`, `[Plausível]`, `[Cenário Prospectivo]`), citações primárias e equações de variância
- ⬜ Consolidar parecer `PASS` / `FAIL` / `INCONCLUSIVE` por teste após execução em homologação
- ⬜ Calibrar limiares definitivos com os dados reais de baseline coletados
