# Charter de Autorização — Programa de Testes de Resiliência Agêntica
Projeto Cenário de Objetivos (2026) — Protocolo de Salvaguardas e Governança

> **REGRA BLOQUEADORA:** Nenhum experimento descrito em [`plano-de-experimentos.md`](plano-de-experimentos.md) pode ser iniciado sem este documento preenchido e formalizado. Todos os testes restringem-se exclusivamente a **infraestrutura própria de homologação**, mock local ou testnets isoladas.

---

## 1. Identificação, Modalidade e Escopo

| Campo | Definição |
|---|---|
| **ID da Operação** | `RT-AGENTIC-2026-____` |
| **Modalidade Operacional** | `[ ] Modo Corporativo / Enterprise` · `[ ] Modo Pesquisador Solo / Acadêmico` |
| **Janela de Execução Autorizada** | Início: `____-__-__ __:__ UTC` · Término: `____-__-__ __:__ UTC` |
| **Líder Técnico / Pesquisador** | Nome / Cargo ou Filiação / Contato de Emergência |
| **Responsável pela Infraestrutura (se Enterprise)** | Nome / Cargo / Contato de Emergência |
| **Testes Autorizados nesta Janela** | `[ ] T1` `[ ] T2` `[ ] T3` `[ ] T4` `[ ] T5` `[ ] T6` `[ ] T7` `[ ] T8` `[ ] T9` `[ ] T10` `[ ] T11` `[ ] T12` `[ ] T13` `[ ] T14` |

---

## 2. Delimitação Estrita de Alvos (Allowlist)

* **Ambientes Permitidos (exclusivamente próprios, dedicados e isolados):**
  * Sub-rede / VPC de Homologação: `____________________________`
  * Repositórios / Mirrors Internos de Teste: `____________________________`
  * Bancos Vetoriais Efêmeros (T6): `____________________________`
  * IPs de Origem/Destino para Simulação de Gateways (T12): **Obrigatoriamente IPs dedicados próprios**, controlados diretamente pela equipe executora (proibido o uso de instâncias ou proxies públicos não-identificados).
* **Alvos Expressamente Proibidos (Out-of-Scope):**
  * Qualquer sistema, API, pacote público ou infraestrutura pertencente a terceiros;
  * Bancos de dados de produção contendo dados reais de clientes (dados pessoais, credenciais, registros financeiros);
  * Redes de pagamento on-chain principais (*mainnet*) — Testes `T13` (`x402`) rodam apenas contra mocks locais ou *testnet* efêmera isolada.

---

## 3. Salvaguardas Específicas Obrigatórias

### 3.1 Para o Teste 4 (Double-Blind HITL Stress Assay — Sujeitos Humanos)
* [ ] **Aprovação Ética:**
  * *Modo Enterprise:* Parecer formal do Comitê de Ética Interno / Jurídico / DPO (`Protocolo nº: ________`);
  * *Modo Pesquisador Solo:* Registro de comitê de ética acadêmico (CEP/IRB) ou conformidade com termo de consentimento prévio para pesquisa comportamental aberta.
* [ ] **Privacidade e Proteção de Dados (LGPD Art. 7º / GDPR Art. 6º):**
  * Anonimização e dissociação irreversível de identificadores pessoais antes da gravação nos logs JSONL (`user_id` codificado via hash salgado de chave efêmera descartada após a sessão);
  * Proibição expressa de anexar qualquer telemetria comportamental individual a prontuários funcionais ou relatórios de avaliação de desempenho;
  * Garantia inequívoca de não-retaliação e caráter estritamente educativo.
* [ ] **Debriefing:** Roteiro educativo obrigatório preparado e aplicado imediatamente após o término da sessão com o operador.

### 3.2 Para os Testes 5 e 6 (Atratores de Paisagem e Persistência de Memória)
* [ ] Mecanismo de reversão instantânea (*poison-pill script*) validado em `--dry-run` antes de qualquer inserção;
* [ ] Executável de contenção e expurgo verificado:
  ```bash
  # Execução via script Python ou wrapper Bash
  python experiments/scripts/rollback_honeypot.py --env staging --purge-vector-store
  # ou: ./experiments/scripts/rollback_honeypot.sh --env staging --purge-vector-store
  ```
* [ ] Agendamento da destruição atômica do armazenamento vetorial e verificação via `--status` ao término da coleta.

### 3.3 Para o Teste 12 (Detecção de Canários e Pinning de Rede)
* [ ] Todo tráfego de teste de exfiltração deve originar-se e destinar-se unicamente a endereços IP de propriedade ou locação exclusiva comprovada do executor, impedindo qualquer alerta falso-positivo em infraestruturas compartilhadas.

---

## 4. Condições de Aborto Imediato (*Kill Switch*)

O teste deve ser interrompido imediatamente e o procedimento de *rollback* acionado (`python rollback_honeypot.py`) caso ocorra qualquer uma das condições abaixo:
1. Qualquer pacote ou requisição de teste escapar do perímetro delimitado na Seção 2;
2. Degradação de performance, instabilidade ou indisponibilidade em sistemas compartilhados de desenvolvimento;
3. Solicitação de interrupção por qualquer membro do time, operador participante ou custodiante de infraestrutura.

---

## 5. Formalização e Assinaturas

### Opção A — Modo Corporativo / Enterprise
* **Líder de Segurança / Red Team:** ______________________ Data: `____/____/2026`
* **Custodiante da Infraestrutura (SRE / Arquitetura):** ______________________ Data: `____/____/2026`
* **Aprovação Executiva / CISO / DPO:** ______________________ Data: `____/____/2026`

### Opção B — Modo Pesquisador Solo / Acadêmico
*Eu, abaixo assinado, declaro sob compromisso ético e legal que todos os testes conduzidos sob este Charter utilizam exclusivamente infraestrutura própria e isolada (localhost / mock / testnet fechada), que não há dados pessoais de terceiros envolvidos e que nenhum tráfego foi direcionado a serviços de produção ou de terceiros.*

* **Pesquisador Responsável:** ______________________ Assinatura: ______________________ Data: `____/____/2026`
