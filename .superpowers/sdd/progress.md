# SDD ledger - plan: docs/superpowers/plans/2026-10-16-modernization-and-conversion-to-hoi4-1-19.md

## Pre-flight Scan
| Task Pair | Produces / Consumes | Conflict Status |
| :--- | :--- | :--- |
| Task 1 -> Task 2 | Test runner & semantic oracle -> Sanitize modifiers | Clean (Task 1 installs oracle; Task 2 audits and fixes ideas) |
| Task 2 -> Task 3 | Clean modifiers & ideas -> Unified characters | Clean (Characters use valid country ideas/roles) |
| Task 3 -> Task 4 | Unified characters -> Equipment designers & MIOs | Clean (Designers reference valid traits/tags) |
| Task 4 -> Task 5 | Designers & stubs -> Map & states | Clean (States reference valid provinces and buildings) |
| Task 5 -> Task 6 | Map & states -> Performance fast-failing | Clean (Decisions target valid states and tags) |
| Task 6 -> Task 7 | Performance decisions -> Master E2E audit | Clean (Full 6-tier pre-flight audit pass) |

---

## Tasks Status
- [x] **Task 1: Scaffolding da Infraestrutura de Testes e Auditoria Forense**
  - Unit tests: 	ests/test_roleplay_baseline.py (PASS, 4 tests)
  - Test runner: 	ests/test_runner.py (PASS)
  - 6-Tier Master QA: scripts/qa_audit_all.py (Brackets 2999 files PASS, BOM 202 files PASS, Map 912 states PASS)
  - Semantic Oracle: scripts/hoi4_semantic_oracle.py + data/hoi4_valid_country_modifiers.json
- [ ] **Task 2: Higienizacao Sintatica & Correcao de Triggers em Blocos de Modificadores**
- [ ] **Task 3: Unificacao do Sistema de Personagens (NSB/BBA/1.19) e Consistencia de Lideranca**
- [ ] **Task 4: Compatibilizacao de Designers de Equipamento e MIOs para 1.19.3**
- [ ] **Task 5: Auditoria e Validacao da Malha de Mapa (13.278 Provincias e 912 Estados)**
- [ ] **Task 6: Otimizacao de Performance e Decisoes Fast-Failing**
- [ ] **Task 7: Auditoria Final Master & Verificacao E2E**
