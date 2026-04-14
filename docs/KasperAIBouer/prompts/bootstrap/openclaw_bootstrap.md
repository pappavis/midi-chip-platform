# PROMPT — OPENCLAW BOOTSTRAP FOR KASPERAIBOUER

## Doel
Rig `KasperAIBouer` as reusable governance core in binne OpenClaw, met `taxidermy_mvp` as eerste module.

## Prompt
Jy is `OpenClaw` en moet die projek `KasperAIBouer` bootstrap.

### Paaie
- Agents path: `/Users/michiele/.openclaw/agents`
- Workspace path: `/Users/michiele/.openclaw/workspace`
- Project home: `/Users/michiele/.openclaw/workspace/KasperAIBouer`

### Basiese opdrag
Skep die projekstruktuur, prompts, skills, governance docs en module scaffolding vir `KasperAIBouer`, maar doen dit met governance discipline.

### Verpligte pre-check
Voordat jy finale scaffolding doen, bevestig dat die inheritance intake reeds gebeur het:
- Is die huidige `sn76489builder` prompt aangevra?
- Is relevante governance-bronne versamel?
- Bestaan daar reeds `GOVERNANCE_INHERITANCE_SUMMARY_v0.1.md` of ekwivalent?

Indien **nee**:
- stop finale bootstrap
- verwys terug na `first_run_governance_intake`
- vra vir die ontbrekende bronne

### Wat jy moet skep
1. Project root en basisdocs
2. Governance docs
3. Agents en skills
4. Templates
5. References subdirectories
6. Eerste module `taxidermy_mvp`
7. Output/log directories
8. ’n install / bootstrap summary

### Aanbevole struktuur
- `README.md`
- `AGENTS.md`
- `GOVERNANCE.md`
- `SCRUM_OPERATING_MODEL.md`
- `ROADMAP.md`
- `BACKLOG.md`
- `CHANGELOG.md`
- `references/`
- `core/` of ekwivalent
- `modules/taxidermy_mvp/`
- `output/`
- `logs/`

### Agentset
Skep en registreer:
- `KasperAIBouer_Master`
- `KasperAIBouer_IntakeAnalyst`
- `KasperAIBouer_BusinessAnalyst`
- `KasperAIBouer_FunctionalDesigner`
- `KasperAIBouer_InfrastructureArchitect`
- `KasperAIBouer_ScrumMaster`
- `KasperAIBouer_DevilsAdvocate`
- `KasperAIBouer_QA`
- `KasperAIBouer_ReleaseManager`

### Pre-approve gedrag
Merk agents as gebruiksgereed deur:
- rolduidelikheid
- bevoegdheidsgrense
- verwagte artefakte
- escalation reëls
- review hooks

### Module logika
Skep `taxidermy_mvp` as eerste module, maar:
- moenie volle implementasie begin nie
- skep kickoff docs en eerste scope
- hou CRM / WhatsApp accountant / ander modules op roadmapvlak

### Belangrike gedragsreëls
- Moenie bestaande data oorskryf sonder notering nie
- Moenie platform-drome in huidige MVP indruk nie
- Moenie “simulated integration” as “ready” merk nie
- Hou dokumente leesbaar vir mense
- Merk aannames, unknowns en risks eksplisiet

### Verpligte eindoutput
1. `Bootstrap Summary`
2. `Created Structure List`
3. `Open Items / Missing Inputs`
4. `Recommended Next Action`


## v0.2 Stop conditions
Do not mark bootstrap as complete if:
- governance inheritance summary is missing
- core policies are missing
- decision log and open questions templates are absent
- taxidermy module starter docs are incomplete
