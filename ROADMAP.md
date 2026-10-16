# BAIANAGEM WW1 ROLEPLAY — ROADMAP DE DESENVOLVIMENTO & MODERNIZAÇÃO

> **Status Geral do Projeto:** Modernização para Hearts of Iron IV 1.19.3 Concluída com Sucesso (Exit Code 0 em 100% dos testes e auditorias).

---

## 🎯 MARCO 1: MODERNIZAÇÃO E COMPATIBILIZAÇÃO COM HOI4 1.19.3 (CONCLUÍDO)

### 1. Integridade Sintática e Correção de CTDs (Crash to Desktop)
- [x] **Auditoria Completa de Brackets (3.009 arquivos):**
  - Resolvidos 7 desbalanceamentos críticos de chaves herdados do mod de 2024:
    - `common/countries/cosmetic.txt` (bloco `FORM_AFR` não-fechado)
    - `common/decisions/SOV.txt` (chaves órfãs)
    - `common/scripted_effects/tgwr_peace_deal_scripted_effects.txt` (chaves extras)
    - `events/WW1_Britain.txt` (comentários em linha corrompendo blocos `NOT = {`)
    - `events/WW1_Poland.txt` (comentários em linha corrompendo blocos `NOT = {`)
    - `history/states/865-Calais.txt` (profundidade de estado corrompida)
    - `interface/AGW_core_button.gui` (bloco `guiTypes` desbalanceado)
  - **Evidência Computacional:** Profundidade final = 0 em todos os 3.009 scripts.

### 2. Oráculo Semântico e Sanitização de Modificadores (1.19.3 Engine Standards)
- [x] **Substituição de Modificadores Obsoletos e Erros de Escopo:**
  - `MONTHLY_POPULATION` -> `monthly_population` (`AST.txt`)
  - `recruitable_population` em ideias -> `conscription = 0.01` (`AST.txt`) e `recruitable_population_factor` (`ROM.txt`)
  - `crypto_strength` (legado pré-La Resistance) -> `encryption = -2` (`AUH.txt`)
  - `offence` e `defence` (legados de HOI3) -> `army_attack_factor` e `army_defence_factor` (`BEL.txt`, `GER.txt`, `GRE.txt`, `LUX.txt`, `usa.txt`)
  - `army_morale` -> `army_morale_factor` (`GRE.txt`)
  - Distinção precisa entre blocos de modificadores de país e modificadores de pesos de IA (`ai_will_do`).

### 3. Unificação da Arquitetura de Personagens (Modern Character Roster)
- [x] **Eliminação de 100% dos comandos legados `create_country_leader`:**
  - Migrados todos os 7 países legados para `common/characters/`:
    - `CAT.txt`: Lluís Companys (`CAT_lluis_companys`)
    - `COG.txt`: Spinning Gorilla (`COG_spinning_gorilla`)
    - `HKG.txt`: Governor of Hong Kong (`HKG_governor_of_hong_kong`)
    - `JNC.txt`: Qi Xieyuan (`JNC_qi_xieyuan`)
    - `LAO.txt`: Sisavang Vong (`LAO_sisavang_vong`)
    - `PNG.txt`: Dr. Albert Hahl (`PNG_albert_hahl`)
    - `SIB.txt`: Pyotr Vologodsky e Pyotr Derber (`SIB_pyotr_vologodsky`, `SIB_pyotr_derber`)
  - 100% dos 255 países agora utilizam o padrão unificado `recruit_character`.

### 4. Designers de Equipamentos, MIOs e Suporte a Projetos Especiais (1.15-1.19)
- [x] **Categorias de Equipamento para MIOs:**
  - Criado `common/military_industrial_organization/equipment_categories/00_equipment_categories.txt` resolvendo todas as 15 macros `mio_cat_eq_*`.
- [x] **Arquetipos Base Restaurados:**
  - `mechanized_equipment` registrado em `common/units/equipment/mechanized.txt`.
  - Arquetipos de artilharia de foguetes registrados para compatibilidade com MIOs.
- [x] **Stub de Estabilidade para Special Projects (Götterdämmerung):**
  - Criado `common/special_projects/projects/ww1_special_projects.txt` garantindo inicialização limpa do subsistema da nova DLC.

### 5. Validação da Malha Cartográfica e Ferrovias
- [x] **Auditoria Completa de 13.278 Províncias e 912 Estados:**
  - 0 províncias fora dos limites (`max ID <= 13278`).
  - 0 províncias sobrepostas entre estados.
  - 100% dos nós ferroviários (`railways.txt`) e centros de suprimento (`supply_nodes.txt`) validados sobre províncias terrestres.

### 6. Fast-Failing de Decisões e Otimização de Ticks Diários
- [x] **Injeção de `allowed = { original_tag = TAG }`:**
  - Sanitizadas 27 categorias de decisões nacionais em 9 países (`AUH`, `CHI`, `EGY`, `ENG`, `FRA`, `GER`, `ITA`, `SPR`, `TUR`).
  - Redução drástica de overhead na IA: países sem a tag original ignoram instantaneamente milhares de verificações redundantes por tick diário.

---

## 🚀 PRÓXIMAS FASES: REWORK, CONTEÚDO E BALANCEAMENTO ROLEPLAY

### FASE 2: Rework e Polimento de Árvores de Foco Nacional (1911-1920)
- [ ] Árvore de Foco da Tríplice Entente (França, Reino Unido, Império Russo).
- [ ] Árvore de Foco dos Impérios Centrais (Alemanha, Áustria-Hungria, Império Otomano).
- [ ] Expansão e caminhos alternativos para potências regionais e Neutros (Brasil, Itália, EUA, Balcãs).

### FASE 3: Eventos Narrativos, Notícias e Imersão Histórica
- [ ] Pacing histórico de crises diplomáticas (Agadir, Crise de Julho, Ultimato Austro-Húngaro).
- [ ] Noticiários e jornais de época com formatação bilíngue (EN / PT-BR).

### FASE 4: Pipeline de Gráficos (GFX) e UI
- [ ] Ícones de espírito nacional e metas de foco com shaders de brilho (`shine`).
- [ ] Retratos autênticos em estilo HOI4 para generais e líderes históricos da Grande Guerra.
