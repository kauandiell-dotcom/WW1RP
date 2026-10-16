# Modernização Integral e Conversão do Mod The Great War RolePlay para HOI4 1.19.3

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Atualizar, estabilizar e converter 100% dos arquivos do mod legado *The Great War RolePlay* (base 2024 / ID 3226668008) para compatibilidade nativa com Hearts of Iron IV versão **1.19.3** (pós-Götterdämmerung/AAT/BBA), eliminando crashes (CTD), corrigindo sintaxe Clausewitz, adaptando designers de equipamento, personagens e otimizando a performance sem perda de conteúdo.

**Architecture:** Abordagem orientada a testes automatizados (TDD Clausewitz). Criação de uma suíte de auditoria contínua (Oráculo Semântico, balanceamento de chaves, integridade de mapa e banco de personagens) que valida cada arquivo antes e depois das transformações, garantindo que o mod mantenha paridade absoluta de conteúdo enquanto adere aos novos padrões da engine.

**Tech Stack:** Paradox Clausewitz Scripting (HOI4 1.19.3), Python 3.11/3.12 (Auditoria AST, Regex, Testes Unitários), Git.

**Spec:** Base do mod em `C:\Users\Usuário\Pictures\Baianagem-WW1-ROLEPLAY`, documentação Paradox Wiki offline em `docs/paradox_wiki/`, Oráculo Semântico Clausewitz 1.19.3.

---

## Global Constraints

- **Zero Perda de Conteúdo**: Nenhuma árvore de foco, evento, decisão ou nação pode ser deletada ou ter suas opções reduzidas.
- **Exit Code 0 Obrigatório**: Nenhuma tarefa é declarada pronta sem passar em 100% dos testes da suíte de validação com código de saída 0.
- **Sintaxe Estrita Clausewitz**: Zero chaves desbalanceadas, zero modificadores inventados, zero triggers em blocos `modifier = { }`.
- **Codificação Binária**: Arquivos `.yml` de localização com UTF-8 BOM único (`\xef\xbb\xbf`); arquivos de script (`.txt`, `.gui`, `.gfx`) em UTF-8 SEM BOM.
- **Isolamento de Diretórios**: Todas as operações e testes devem permanecer 100% contidos no repositório local. Nunca tocar na pasta de download da Steam Workshop (`steamapps/workshop/content/394360/...`).

---

## Review Focus

1. **Triggers Ilegais em Blocos de Modificador**: Blocos `modifier = { is_puppet = yes }` em ideias que geram erro no engine; devem ser convertidos para regras ou triggers válidos.
2. **Crash ao Carregar Estados no Mapa**: Províncias com ID > 13.278 em arquivos de estado que causam CTD instantâneo no carregador do mapa.
3. **MIOs e Projetos Especiais Inexistentes**: Árvores de foco que tentam premiar traits de Organizações Militares ou Projetos Especiais que não estão registrados na nova DLC.
4. **Desconexão de Personagens e Líderes**: Líderes recrutados em `history/countries/` cujos IDs não existem em `common/characters/`.
5. **Degradação de Tick em Multiplayer**: Decisões globais sem cláusula de fast-failing `allowed = { original_tag = TAG }`, causando queda drástica de FPS.

---

## Estrutura de Tarefas de Implementação

### Task 1: Scaffolding da Infraestrutura de Testes e Auditoria Forense
**Files:**
- Create: `scripts/qa_audit_all.py`
- Create: `scripts/hoi4_semantic_oracle.py`
- Create: `data/hoi4_valid_country_modifiers.json`
- Create: `tests/test_roleplay_baseline.py`
- Create: `tests/test_runner.py`

**Interfaces:**
- Consumes: Arquivos brutos do mod em `common/`, `events/`, `history/`, `map/`, `interface/`.
- Produces: Pipeline de validação com 6 camadas (Sintaxe/Chaves, BOM UTF-8, Oráculo Semântico, Mapa, Personagens, Decisões).

- [ ] **Step 1: Escrever os testes unitários da suíte base em `tests/test_roleplay_baseline.py`**
  Definir testes para balanceamento de chaves `{}` em todos os 2.760 arquivos de script e integridade do `default.map`.
- [ ] **Step 2: Executar os testes para registrar a baseline inicial**
  Comando: `python -m unittest tests/test_roleplay_baseline.py`
  Resultado esperado: PASS para chaves (após correções preliminares) e PASS para `default.map`.
- [ ] **Step 3: Instalar a base do Oráculo Semântico Clausewitz 1.19.3 em `data/hoi4_valid_country_modifiers.json`**
  Copiar o banco de dados oficial de modificadores válidos da versão 1.19.3 para referência automática.
- [ ] **Step 4: Executar a suíte de auditoria completa**
  Comando: `python scripts/qa_audit_all.py`
  Resultado esperado: Auditoria executada gerando relatório de conformidade.
- [ ] **Step 5: Commit do framework de testes**
  `git add scripts/ tests/ data/`
  `git commit -m "chore(infra): establish master QA test runner and Clausewitz 1.19.3 semantic oracle"`

---

### Task 2: Higienização Sintática & Correção de Triggers em Blocos de Modificadores
**Files:**
- Modify: `common/ideas/*.txt`
- Modify: `common/technologies/*.txt`
- Test: `tests/test_semantic_integrity.py`

**Interfaces:**
- Consumes: 46 modificadores identificados como inválidos pelo Oráculo Semântico (ex.: `is_puppet`, `has_tech`, `has_global_flag`, `army_morale`, `MONTHLY_POPULATION`).
- Produces: Ideias e tecnologias 100% limpas sem avisos de sintaxe no `error.log`.

- [ ] **Step 1: Escrever teste unitário `tests/test_semantic_integrity.py`**
  Garantir que nenhum arquivo em `common/ideas/` contenha tokens de condição (`is_puppet`, `has_tech`, `check_variable`) dentro de blocos `modifier = { }`.
- [ ] **Step 2: Executar teste e verificar falhas esperadas**
  Comando: `python -m unittest tests/test_semantic_integrity.py`
  Resultado esperado: FAIL apontando os arquivos com triggers ilegais.
- [ ] **Step 3: Implementar script de refatoração semântica**
  - Converter `army_morale` para `army_org_regain_factor`.
  - Converter `MONTHLY_POPULATION` para `monthly_population`.
  - Mover triggers (`is_puppet`, `has_global_flag`) para o bloco `allowed = { }` ou `targeted_modifier = { }`.
- [ ] **Step 4: Reexecutar o teste unitário**
  Comando: `python -m unittest tests/test_semantic_integrity.py`
  Resultado esperado: PASS (0 triggers em blocos de modificador).
- [ ] **Step 5: Commit das correções semânticas**
  `git add common/ideas/ common/technologies/ tests/`
  `git commit -m "fix(ideas): sanitize invalid triggers in modifier blocks and update obsolete 1.19 tokens"`

---

### Task 3: Unificação do Sistema de Personagens (NSB/BBA/1.19) e Consistência de Liderança
**Files:**
- Modify: `common/characters/*.txt`
- Modify: `history/countries/*.txt`
- Test: `tests/test_characters_consistency.py`

**Interfaces:**
- Consumes: 204 arquivos de personagens e 204 arquivos de histórico de países.
- Produces: 100% dos países utilizando `recruit_character` unificado; eliminação do legado `create_country_leader`.

- [ ] **Step 1: Escrever teste unitário `tests/test_characters_consistency.py`**
  Verificar que todo líder, general ou conselheiro recrutado em `history/countries/` existe com ID idêntico em `common/characters/`.
- [ ] **Step 2: Executar teste e listar discrepâncias**
  Comando: `python -m unittest tests/test_characters_consistency.py`
  Resultado esperado: Identificar líderes dos 7 países legados e IDs órfãos.
- [ ] **Step 3: Migrar os 7 países legados para `common/characters/`**
  Criar declarações de personagens completas com retratos, papéis civis e militares para as tags pendentes.
- [ ] **Step 4: Reexecutar o teste de integridade de personagens**
  Comando: `python -m unittest tests/test_characters_consistency.py`
  Resultado esperado: PASS (0 personagens órfãos, 100% cobertura de recrutamento).
- [ ] **Step 5: Commit da unificação de personagens**
  `git add common/characters/ history/countries/ tests/`
  `git commit -m "feat(characters): unify all 204 country rosters into modern character architecture"`

---

### Task 4: Compatibilização de Designers de Equipamento e MIOs para 1.19.3
**Files:**
- Modify: `common/units/equipment/plane_airframes.txt`
- Modify: `common/units/equipment/tank_chassis.txt`
- Modify: `common/military_industrial_organization/*.txt`
- Create: `common/special_projects/projects/ww1_special_projects.txt`
- Test: `tests/test_equipment_and_mios.py`

**Interfaces:**
- Consumes: Especificações de designers de blindados (NSB), aviões (BBA) e MIOs (AAT).
- Produces: Equipamentos de 1910 a 1920 calibrados com tags de módulo válidas na versão 1.19.3.

- [ ] **Step 1: Escrever teste unitário `tests/test_equipment_and_mios.py`**
  Validar sintaxe de chassis, módulos permitidos e vínculos de MIOs por tipo de equipamento.
- [ ] **Step 2: Executar teste e auditar módulos ausentes**
  Comando: `python -m unittest tests/test_equipment_and_mios.py`
- [ ] **Step 3: Atualizar tags de chassis e criar stubs seguros de Projetos Especiais**
  Adicionar declarações de compatibilidade para evitar que o motor de 1.19 reclame de ausência do sistema de cientistas/projetos especiais da nova DLC.
- [ ] **Step 4: Reexecutar os testes de equipamentos**
  Comando: `python -m unittest tests/test_equipment_and_mios.py`
  Resultado esperado: PASS.
- [ ] **Step 5: Commit de designers e MIOs**
  `git add common/units/ common/military_industrial_organization/ common/special_projects/ tests/`
  `git commit -m "feat(equipment): modernize air/armor designers and integrate WW1 special projects stub"`

---

### Task 5: Auditoria e Validação da Malha de Mapa (13.278 Províncias e 912 Estados)
**Files:**
- Modify: `map/railways.txt`
- Modify: `map/supply_nodes.txt`
- Modify: `history/states/*.txt`
- Test: `tests/test_map_and_states.py`

**Interfaces:**
- Consumes: `map/definition.csv` (13.278 províncias), `history/states/` (912 estados), `map/provinces.bmp`.
- Produces: Mapa livre de províncias órfãs, nós de suprimento flutuantes ou conexões marítimas inválidas.

- [ ] **Step 1: Escrever teste unitário `tests/test_map_and_states.py`**
  - Auditar que nenhuma província referenciada nos 912 estados exceda o ID máximo 13.278.
  - Verificar se todos os nós de ferrovia e supply hubs estão ancorados em províncias terrestres válidas.
- [ ] **Step 2: Executar teste e mapear províncias órfãs**
  Comando: `python -m unittest tests/test_map_and_states.py`
- [ ] **Step 3: Corrigir províncias mal mapeadas ou estações ferroviárias flutuantes**
  Ajustar arquivos de estado e `map/railways.txt` com coordenadas terrestres precisas.
- [ ] **Step 4: Reexecutar o teste de mapa**
  Comando: `python -m unittest tests/test_map_and_states.py`
  Resultado esperado: PASS (100% províncias cobertas, 0 erros de nós).
- [ ] **Step 5: Commit da malha de mapa**
  `git add map/ history/states/ tests/`
  `git commit -m "fix(map): reconcile 13278 provinces, state assignments, and railway infrastructure"`

---

### Task 6: Otimização de Performance e Decisões Fast-Failing (Padrão Roleplay Fluído)
**Files:**
- Modify: `common/decisions/*.txt`
- Modify: `common/decisions/categories/*.txt`
- Modify: `common/on_actions/*.txt`
- Test: `tests/test_performance_and_fastfailing.py`

**Interfaces:**
- Consumes: Decisões genéricas e nacionais de 43 países.
- Produces: 100% das decisões com `allowed = { original_tag = TAG }`, eliminando checks inúteis de IA e acelerando o tick diário.

- [ ] **Step 1: Escrever teste unitário `tests/test_performance_and_fastfailing.py`**
  Garantir que nenhuma categoria de decisão de país específico execute sem a cláusula de restrição de tag original.
- [ ] **Step 2: Executar teste e listar decisões lentas**
  Comando: `python -m unittest tests/test_performance_and_fastfailing.py`
- [ ] **Step 3: Injetar cláusula de fast-failing em todas as categorias de decisão**
  Inserir `allowed = { original_tag = TAG }` sistematicamente.
- [ ] **Step 4: Reexecutar o teste de performance**
  Comando: `python -m unittest tests/test_performance_and_fastfailing.py`
  Resultado esperado: PASS.
- [ ] **Step 5: Commit das otimizações de performance**
  `git add common/decisions/ common/on_actions/ tests/`
  `git commit -m "perf(decisions): enforce fast-failing allowed tags across all decision categories"`

---

### Task 7: Auditoria Final Master & Verificação E2E
**Files:**
- Modify: `descriptor.mod`
- Modify: `ROADMAP.md`
- Test: `scripts/qa_audit_all.py`

**Interfaces:**
- Consumes: Repositório completamente modernizado.
- Produces: Relatório final de pré-voo com Exit Code 0 em todas as 6 camadas de auditoria.

- [ ] **Step 1: Executar a suíte de auditoria completa master**
  Comando: `python scripts/qa_audit_all.py`
  Resultado esperado: Exit Code 0 em todas as camadas.
- [ ] **Step 2: Atualizar documentação de tracking em `ROADMAP.md`**
  Registrar a compatibilização para 1.19.3 concluída e pronta para as fatias de rework de conteúdo.
- [ ] **Step 3: Commit final do marco de modernização**
  `git add .`
  `git commit -m "chore(release): complete full modernization of Baianagem-WW1-ROLEPLAY for HOI4 1.19.3"`
