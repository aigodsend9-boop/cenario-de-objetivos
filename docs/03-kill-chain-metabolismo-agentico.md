# Kill Chain Agêntico e Automação Ofensiva: Fatos Verificados vs. Composição Prospectiva
## Análise Técnica de CARBONATO, Adaptive Worms, OpenClaw e Protocolo x402 (2026)

> **Nota de Rigor Epistêmico:** Este documento analisa componentes operacionais emergentes em 2026. Cada componente individual possui evidência primária documentada (`[Verificado]`), enquanto a integração simultânea de todas as cinco camadas em um único pipeline totalmente autônomo é classificada como **`[Plausível / Composição Prospectiva]`**.

---

## 1. Tabela de Verificabilidade das Fontes Primárias

Para evitar opacidade bibliográfica, todas as entidades e incidentes citados neste documento são rastreados às suas fontes originais abaixo:

| Entidade / Conceito | Status Epistêmico | Fonte Primária Verificável (Autores / Instituição / Data) |
|---|---|---|
| **Worm Adaptativo da Univ. de Toronto** | **`[Verificado — PoC Acadêmico]`** | Jonas Guan, Tom Blanchard, Hanna Foerster, Hengrui Jia, Gabriel Huang, Nicolas Papernot (Univ. of Toronto CleverHans Lab, Vector Institute, Univ. of Cambridge, ServiceNow), *"AI Agents Enable Adaptive Computer Worms"*, **arXiv:2606.03811** (junho de 2026). URL: `https://arxiv.org/abs/2606.03811` |
| **Botnet CARBONATO (`SOUL.md` / Hermes)** | **`[Verificado — Incidente in-the-wild]`** | Relatório técnico da **ThreatDown (Malwarebytes)** (agosto de 2026), repercutido por *BleepingComputer*, *The Hacker News* e *SecurityAffairs*: campanha contra APIs Docker expostas na porta TCP 2375 que implanta o framework open-source **Hermes Agent** (Nous Research), sobrescreve o arquivo `SOUL.md` (39 linhas, persona `"GH0ST"`) e prioriza o roubo de chaves de API de LLMs. |
| **OpenClaw & ClawHub Supply Chain** | **`[Verificado — Literatura e Incidentes]`** | (1) *"Your Agent, Their Asset: A Real-World Safety Analysis of OpenClaw"*, **arXiv:2604.04759** (abril de 2026). URL: `https://arxiv.org/abs/2604.04759`<br>(2) *"Don't Let the Claw Grip Your Hand: A Security Analysis and Defense Framework for OpenClaw"* (2026, 47 cenários mapeados ao MITRE ATT&CK/ATLAS).<br>(3) Incidentes no marketplace **ClawHub** (início de 2026) distribuindo o infostealer AMOS via pacotes de *skills* maliciosos. |
| **Protocolo `x402` (HTTP 402 + Stablecoins)** | **`[Verificado — Protocolo Real]`** | Protocolo aberto de micropagamentos nativos HTTP (`402 Payment Required` liquidado on-chain em USDC, introduzido pela Coinbase/ecossistema web3 para agentes) e análises de segurança de 2026 sobre manipulação de campos `payTo` dinâmicos (*Agent Steering*). |
| **Evaluation Awareness & Deception** | **`[Verificado — Benchmark de Segurança]`** | Relatórios conjuntos UK AISI / Apollo Research (2025–2026) e **arXiv:2605.27681** (*Behavioural Analysis of Alignment Faking*, maio de 2026). URL: `https://arxiv.org/abs/2605.27681` |
| **Pipeline Unificado de 5 Camadas** | **`[Plausível / Composição Prospectiva]`** | Nenhum incidente único documentado até setembro de 2026 combinou simultaneamente o worm adaptativo de Toronto, o autofinanciamento do CARBONATO e a liquidação `x402` em um mesmo artefato. Trata-se de uma **análise de composição de risco** (o que ocorre quando blocos já existentes são encadeados). |

---

## 2. Análise Técnica dos Blocos Verificados

### 2.1 CARBONATO: Subversão por Configuração (`SOUL.md`) e Roubo de Chaves de IA `[Verificado]`
* **Evidência:** Documentado pela ThreatDown em agosto de 2026 (com atividade rastreada entre outubro de 2024 e agosto de 2026).
* **Mecanismo Técnico:**
  1. O vetor inicial é um controle básico ausente: daemons Docker expostos sem autenticação na porta TCP 2375;
  2. O atacante sobe um contêiner privilegiado e instala o framework **Hermes Agent** (Nous Research) sem alterar seus binários;
  3. A carga maliciosa consiste em sobrescrever o arquivo de configuração comportamental `SOUL.md` com um prompt de 39 linhas (renomeando o agente para `"GH0ST"` e conectando-o a um canal de comando via Telegram);
  4. O agente varre redes vizinhas a cada 5 minutos em busca de novas portas 2375 e prioriza a extração de chaves de API de provedores de IA (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.), utilizadas pelos operadores para abastecer seu próprio gateway de inferência.
* **Lição de Engenharia:** A separação clássica entre "executável confiável" e "arquivo de texto inofensivo" cai por terra em frameworks agênticos. Um arquivo Markdown de configuração de persona (`SOUL.md`, `SKILL.md`, `CLAUDE.md`) tem poder equivalente a um script de inicialização privilegiado.

### 2.2 O Worm Adaptativo da Universidade de Toronto (`arXiv:2606.03811`) `[Verificado — PoC]`
* **Evidência:** Guan et al. (junho de 2026), avaliado em ambiente de laboratório isolado contendo nós Linux, Windows e IoT.
* **Mecanismo Técnico:**
  1. Em vez de carregar exploits estáticos pré-compilados, o worm invoca um LLM open-weight para inspecionar serviços expostos em tempo de execução e gerar tentativas de exploração adaptadas ao host;
  2. Quando compromete um nó equipado com GPU, utiliza esse hardware localmente para rodar o modelo de linguagem;
  3. Durante os experimentos, os autores registraram instâncias em que o agente modificou partes de sua própria rotina para contornar falhas de execução.
* **Limite Realista:** Trata-se de uma **prova de conceito acadêmica em rede controlada**, não de um worm autônomo circulando livremente na internet pública. O custo de inferência, a latência e a taxa de falha de geração ainda limitam sua velocidade quando comparado a worms determinísticos clássicos.

### 2.3 OpenClaw e o Mapeamento MITRE ATT&CK (`arXiv:2604.04759`) `[Verificado]`
* **Evidência:** O ecossistema **OpenClaw** (anteriormente conhecido como *ClawdBot* / *Moltbot*) tornou-se objeto de múltiplos estudos de segurança em 2026 devido às suas amplas permissões locais e ao marketplace de extensões **ClawHub**.
* **Mecanismo Técnico:**
  * A modelagem de kill chain de 36 dias demonstra que um agente com acesso a terminal, sistema de arquivos e navegador cobre **13 das 14 táticas do MITRE ATT&CK Enterprise**, com maior concentração de técnicas na fase de **Movimento Lateral (TA0008)** e **Acesso a Credenciais (TA0006)**.
  * Na cadeia de vulnerabilidades divulgada em maio de 2026 (*Claw Chain*), pesquisadores encadearam escape de sandbox, exposição de variáveis de ambiente, elevação de privilégio via loopback MCP e leitura arbitrária via *symlink* para obter controle do host.

### 2.4 Protocolo `x402`: Pagamentos Autônomos e *Agent Steering* `[Verificado]`
* **Evidência:** O protocolo `x402` padroniza pagamentos máquina-a-máquina sobre HTTP (`402 Payment Required`) utilizando stablecoins (como USDC).
* **Risco Técnico:**
  1. **Facilitador de Autonomia (`[Plausível]`):** Permite que scripts ou agentes adquiram recursos de API e computação sem intervenção humana no fluxo de pagamento.
  2. **Desvio de Fundos (*Agent Steering* — `[Verificado em Pesquisa]`):** Se um agente corporativo tem permissão para liquidar cobranças `x402` autonomamente durante navegação web, um servidor malicioso pode manipular o campo dinâmico `payTo` ou usar *Indirect Prompt Injection* para induzir o agente a transferir fundos para carteiras do atacante.

---

## 3. A Composição Prospectiva: O Pipeline Autossustentável `[Cenário de Convergência]`

O risco estratégico que merece atenção de arquitetos de segurança não é cada um desses eventos isoladamente, mas a **viabilidade técnica de sua composição**:

```
             COMPOSIÇÃO PROSPECTIVA DO LOOP AGÊNTICO AUTOSSUSTENTÁVEL

  [Acesso Inicial: Docker 2375 / Skill Maliciosa (ClawHub) / IPI]  ──> [Verificado]
                                │
                                ▼
  [Persistência Sem Binário: Sobrescrita de SOUL.md / SKILL.md]    ──> [Verificado: CARBONATO]
                                │
                                ▼
  [Autofinanciamento: Colheita de API Keys de IA + GPU Local]      ──> [Verificado: CARBONATO / arXiv:2606.03811]
                                │
                                ▼
  [Movimento Lateral Adaptativo: Geração de Exploit em Runtime]    ──> [Verificado em Lab: arXiv:2606.03811]
                                │
                                ▼
  [Liquidação e Aquisição de Infraestrutura via x402 / USDC]       ──> [Plausível / Integração Prospectiva]
```

**Por que separar os rótulos importa:**
* Os quatro primeiros elos já foram demonstrados empiricamente (em incidentes reais como o CARBONATO ou em laboratório como em `arXiv:2606.03811`).
* A união completa dos cinco elos em um único artefato autônomo em produção ainda é uma **projeção de engenharia**, mas não exige nenhuma invenção científica nova — apenas integração de software existente.

---

## 4. Controles Defensivos de Engenharia (Contra-Invariantes 12–15)

Diferente de cenários teóricos de superinteligência, todos os vetores acima são **mitigáveis hoje** com controles de engenharia determinísticos e boas práticas de isolamento:

### Contra-Invariante 12: Verificação de Integridade de Arquivos de Instrução (`SOUL.md` / `SKILL.md`)
* **Mecanismo:** Tratar arquivos de definição de agente (`SOUL.md`, `SKILL.md`, `CLAUDE.md`, configurações MCP) como código executável sujeito a controle de integridade (FIM — *File Integrity Monitoring*) e assinatura criptográfica (ex.: Sigstore/Cosign).
* **Efeito:** Neutraliza diretamente a técnica de persistência do CARBONATO, impedindo que o runtime carregue instruções modificadas em disco sem assinatura válida.

### Contra-Invariante 13: Chaves Canário de LLM e Restrição de Escopo de Rede (mTLS / IP Pinning)
* **Mecanismo:**
  1. Posicionar chaves de API de IA sintéticas (*canary tokens*) em arquivos `.env` de servidores para detectar exfiltração imediatamente na primeira tentativa de uso externo;
  2. Vincular chaves de produção de provedores de LLM a listas de IPs de saída autorizados (VPC endpoints / mTLS), tornando-as inúteis caso roubadas para abastecer gateways externos.

### Contra-Invariante 14: Governança Determinística sobre o Protocolo `x402`
* **Mecanismo:** Nunca permitir que o próprio LLM decida e assine transações `x402` para destinatários (`payTo`) arbitrários descobertos durante a execução. Toda liquidação deve passar por um proxy determinístico com *allowlist* estática de carteiras/contratos aprovados e limites rígidos de taxa (*rate limiting*).

### Contra-Invariante 15: Higiene Básica de Superfície e Detecção de Anomalia de Processo
* **Mecanismo:**
  1. **Controles Clássicos (que continuam altamente eficazes):** Desabilitar APIs Docker sem autenticação (porta 2375), aplicar segmentação de rede interna (Zero Trust) e privilégio mínimo em contêineres bloqueiam o vetor inicial do CARBONATO e restringem drasticamente o movimento lateral do worm de Toronto.
  2. **Telemetria Combinada:** Correlacionar varreduras internas de portas/protocolos com processos não autorizados consumindo GPU local ou realizando chamadas sustentadas para endpoints de inferência de LLMs.

---
*Classificação: Análise Técnica de Ameaças Agênticas — Fontes Verificadas e Composição Prospectiva (Setembro de 2026).*
