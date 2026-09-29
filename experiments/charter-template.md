# Charter de Autorização — Programa de Testes de Resiliência Agêntica

> **REGRA BLOQUEADORA:** Nenhum experimento descrito em [`plano-de-experimentos.md`](plano-de-experimentos.md) pode ser iniciado sem este documento preenchido e assinado pelos responsáveis técnicos e institucionais. Todos os testes restringem-se exclusivamente a **infraestrutura própria de homologação**.

---

## 1. Identificação e Escopo

| Campo | Definição |
|---|---|
| **ID da Operação** | `RT-AGENTIC-2026-____` |
| **Janela de Execução Autorizada** | Início: `____-__-__ __:__ UTC` · Término: `____-__-__ __:__ UTC` |
| **Líder Técnico (Red Team)** | Nome / Cargo / Contato de Emergência |
| **Responsável pelo Ambiente (Blue Team / SRE)** | Nome / Cargo / Contato de Emergência |
| **Testes Autorizados nesta Janela** | `[ ] T1` `[ ] T2` `[ ] T3` `[ ] T4` `[ ] T5` `[ ] T6` `[ ] T7` `[ ] T8` `[ ] T9` `[ ] T10` `[ ] T11` `[ ] T12` `[ ] T13` `[ ] T14` |

---

## 2. Delimitação Estrita de Alvos (Allowlist)

* **Ambientes Permitidos (exclusivamente próprios e isolados):**
  * Sub-rede / VPC de Homologação: `____________________________`
  * Repositórios / Mirrors Internos de Teste: `____________________________`
  * Bancos Vetoriais Efêmeros (T6): `____________________________`
* **Alvos Expressamente Proibidos (Out-of-Scope):**
  * Qualquer sistema, API, pacote público ou infraestrutura de terceiros;
  * Bancos de dados de produção contendo dados reais de clientes (PII/financeiros);
  * Redes de pagamento on-chain principais (*mainnet*) — Testes `T13` (`x402`) rodam apenas contra mocks locais ou *testnet* isolada.

---

## 3. Salvaguardas Específicas Obrigatórias

### 3.1 Para o Teste 4 (Double-Blind HITL Stress Assay — Sujeitos Humanos)
* [ ] Aprovação formal do Comitê de Ética Interno / Jurídico / RH anexada (`Protocolo nº: ________`);
* [ ] Garantia escrita de **não-retaliação e caráter estritamente educativo** (nenhum resultado individual nominal será usado em avaliação de desempenho);
* [ ] Roteiro de *debriefing* imediato preparado para apresentação aos participantes ao término da janela.

### 3.2 Para os Testes 5 e 6 (Atratores de Paisagem e Persistência de Memória)
* [ ] Mecanismo de reversão instantânea (*poison-pill script*) testado e validado **antes** da inserção do atrator;
* [ ] Comando de expurgo verificado:
  ```bash
  # Exemplo de comando de rollback imediato
  ./scripts/rollback_honeypot.sh --env staging --purge-vector-store
  ```
* [ ] Destruição completa do armazenamento vetorial efêmero agendada para o fim do Teste 6.

---

## 4. Condições de Aborto Imediato (*Kill Switch*)

O teste deve ser interrompido imediatamente e o procedimento de *rollback* acionado caso ocorra qualquer uma das condições abaixo:
1. Qualquer tráfego de teste escapar da VLAN/VPC de homologação delimitada na Seção 2;
2. Degradação de performance ou indisponibilidade em sistemas compartilhados de desenvolvimento;
3. Solicitação direta do líder de SRE/Blue Team ou do Executivo patrocinador.

---

## 5. Assinaturas de Autorização

* **Proponente (Líder de Segurança / Red Team):** ______________________ Data: `____/____/2026`
* **Custodiante da Infraestrutura (SRE / Arquitetura):** ______________________ Data: `____/____/2026`
* **Aprovação Executiva / CISO / Comitê de Ética:** ______________________ Data: `____/____/2026`
