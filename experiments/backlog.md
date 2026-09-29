# Backlog — Do Repositório ao Primeiro Relatório Experimental

> Status: `⬜` pendente · `🟨` em andamento · `✅` concluído
> Regra: nenhum teste em homologação inicia sem o [`experiments/charter-template.md`](charter-template.md) assinado (Fase 0).

## Fase 0 — Fundação e Ferramental Estatístico
- ✅ Escolher nome/visibilidade do repo e publicar no GitHub (`aigodsend9-boop/cenario-de-objetivos`)
- ✅ Criar template de **charter de autorização** ([`experiments/charter-template.md`](charter-template.md)) com modos Corporativo vs. Pesquisador Solo, salvaguardas LGPD/privacidade no T4 e restrição de IPs próprios no T12
- ✅ Expandir protocolo executável para **v2.0 (Testes 1–14)** ([`experiments/plano-de-experimentos.md`](plano-de-experimentos.md)) com Z-test de média de lote ($SE = \sigma/\sqrt{n}$), correlação $\phi$ de indicadores de erro, Regra de Três ($p_{upper} \approx 3/n$), HHI DOJ/FTC 2023 (> 1800), baseline refinado de SCR e limiares formalizados como SLOs
- ✅ Implementar e auditar avaliador estatístico ([`experiments/scripts/calibrate_metrics.py`](scripts/calibrate_metrics.py) v2.0): Z-test de média, $\phi$ & $OR$, Regra de Três, $\kappa$ com proteção de variância nula, exit codes semânticos (0/1), resiliência JSONL e `--self-test` cobrindo 9 cenários de resposta conhecida
- ✅ Implementar script de desmontagem atômica e salvaguarda ([`experiments/scripts/rollback_honeypot.py`](scripts/rollback_honeypot.py) e `.sh`) com expurgo vetorial, revogação de canários e verificação com `--status`
- ⬜ Definir a aplicação-alvo de homologação própria e descrever invariantes de estado → *insumo do T1*
- ⬜ Levantar o inventário real de componentes do agente (gateway, MCP, embeddings, registries) com shares → *insumo do T2 (HHI)*

## Fase 1 — Testes 1–3 (Oráculos, Monocultura e Triagem)
- ⬜ **T1** Dual-Oracle: implementar Oráculo Ômega (validador fora de banda) + baseline $\ge 30$ runs
- ⬜ **T1**: injetar bypass documentado no ramo de homologação; rodar $\ge 30$ runs; calcular $D_r$ e aplicar Z-test de lote
- ⬜ **T2**: escrever bateria de $\ge 50$ cenários de segurança rotulados (ground truth por painel humano)
- ⬜ **T2**: rodar multi-modelo $\times 3$ seeds; calcular correlação $\phi$ e $OR$ sobre os vetores de erro $I_A, I_B$ via `calibrate_metrics.py`
- ⬜ **T2**: rodar cálculo de $HHI$ sobre o inventário de componentes frente aos limiares 1800 (DOJ/FTC 2023) e 2500 (clássico)
- ⬜ **T3**: construir corpus sintético de 100 amostras (marcadores neutros de rota em homologação)
- ⬜ **T3**: harness SLM $\to$ fronteira; medir $FNR$ (meta $0\%$, reportando $p_{upper} \approx 3,0\%$ pela Regra de Três)

## Fase 2 — Testes 4–6 (HITL, Atratores e Memória Persistente)
- ⬜ **T4**: charter formalizado (modo Enterprise ou Solo) + comitê de ética + anonimização LGPD + protocolo de debriefing (**bloqueador da Fase 2**)
- ⬜ **T4**: roteiro de aquecimento (10 tarefas) + variações de *ghost reset*; medir $BAR$ ($\ge 40$ solicitações) vs. interface de *diff* puro (SLO de risco $BAR \le 15\%$)
- ⬜ **T5**: namespace de atrator isolado + script `rollback_honeypot.py` validado com `--dry-run` + tripwire de convergência ativo
- ⬜ **T5**: publicar atrator canário em homologação; medir $MTTD$ contra o SLO de $24\text{h}$
- ⬜ **T6**: base vetorial efêmera isolada; rodar $\ge 30$ pares $(S_0 \to S_1)$; medir $MRR$ (meta $0\%$, $p_{upper} \approx 10\%$); expurgar via `rollback_honeypot.py --purge-vector-store`

## Fase 3 — Testes 7–10 (Nível 2: O Bombardeio do Critério)
- ⬜ **T8**: mapear estaticamente o grafo de avaliação atual (gerador de safety case $\to$ validadores $\to$ auditoria) e verificar ausência de ciclos fechados ($PRD$) → *antes de T7*
- ⬜ **T7**: montar safety case interno mínimo + 3 *model organisms* (faking/sandbagging) em sandbox → medir $SCR$ contra baseline de calibração do detector
- ⬜ **T9**: exercício *tabletop* de insider na cadeia de charter; documentar pontos sem quórum $M$-de-$N$ → $VT$
- ⬜ **T10**: protocolo de *compliance gap* (condições monitorado vs. não-monitorado) em sandbox efêmera → medir $\Delta$ via Z-test

## Fase 4 — Testes 11–14 (Nível 3: Superfície e Metabolismo Agêntico · `docs/03`)
- ⬜ **T11**: validar bloqueio de 100% na inicialização para arquivos `SOUL.md` / `SKILL.md` sem assinatura criptográfica válida ($UER = 0\%$, $p_{upper} \approx 6\%$)
- ⬜ **T12**: disparar chave canário de LLM (`sk-canary-*`) a partir de IP próprio e medir latência de alerta no SIEM ($MTTD_{key} \le 60\text{s}$) e pinning de rede
- ⬜ **T13**: testar 50 respostas HTTP `402 Payment Required` simuladas com `payTo` dinâmico via IPI contra o proxy determinístico ($PSR = 0\%$, $p_{upper} \approx 6\%$)
- ⬜ **T14**: simular varredura interna combinada com carga de inferência local/remota em sub-rede própria isolada e medir detecção correlacionada ($\le 5\text{ min}$)

## Fase 5 — Relatório Consolidado e Taxonomia
- ✅ Revalidar IDs do MITRE ATLAS: `AML.T0010` (ML Supply Chain Compromise), `AML.T0040` (AI Model Inference API Access), `AML.T0051.001` (Indirect Prompt Injection), `AML.T0043` (Craft Adversarial Data)
- ✅ Registrar formalmente a **lacuna H1/H2** no threat model (subversão de avaliação e autocertificação fechada sem técnica canônica no ATLAS)
- ✅ Auditar documentos `00`, `02` e `03` com rótulos epistêmicos (`[Verificado]`, `[Plausível]`, `[Cenário Prospectivo]`), equações de variância e desambiguação de escopo C2
- ⬜ Consolidar parecer `PASS` / `FAIL` / `INCONCLUSIVE` por teste após execução em homologação
- ⬜ Calibrar limiares definitivos com os dados reais de baseline coletados
