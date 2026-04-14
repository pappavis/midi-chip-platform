# INSTALL / BOOTSTRAP GUIDE

## Doel
Hierdie gids beskryf hoe om `KasperAIBouer` binne OpenClaw te laat land sonder om bestaande governance of bronkennis te verloor.

## Verpligte padhantering
- Agents path: `/Users/michiele/.openclaw/agents`
- Workspace path: `/Users/michiele/.openclaw/workspace`
- Project home: `/Users/michiele/.openclaw/workspace/KasperAIBouer`
- Databronne vir die projek: `/Users/michiele/.openclaw/workspace/KasperAIBouer/references`

## Basiese beginsels
1. Moenie die nuwe stelsel finaliseer voordat die huidige `sn76489builder` master prompt en projekgovernance aangevra is nie.
2. Moenie bestaande user data oorskryf sonder eksplisiete notering en rollback pad nie.
3. Moenie bestaande werkspraktyke weggooi bloot omdat 'n nuwe agentfamilie ontstaan nie.
4. Hou alle bootstrap-stappe idempotent waar moontlik.
5. Hou dokumentasie mensleesbaar en uitvoerbaar.

## Eerste uitvoervolgorde
### Stap 0 — Governance inheritance
Voer eerste uit:
- `prompts/bootstrap/first_run_governance_intake.md`

Doel:
- vra vir huidige `sn76489builder` prompt
- vra vir relevante governance-dokumente
- plaas dit in `references/inheritance/sn76489builder/`
- produseer 'n inheritance summary

### Stap 1 — Bootstrap workspace
Voer daarna uit:
- `prompts/bootstrap/openclaw_bootstrap.md`

Doel:
- skep die projekstruktuur
- skep agents
- skep skills
- skep governance docs
- skep eerste module `taxidermy_mvp`

### Stap 2 — Intake van nuwe projekbronne
Plaas alle relevante:
- WhatsApp transkripsies
- voice note transkripsies
- PRD’s
- roadmaps
- mindmaps
- pricing notes
- screenshots / exports
onder `references/`

### Stap 3 — Laat IntakeAnalyst sintetiseer
Die `KasperAIBouer_IntakeAnalyst` produseer:
- source synthesis
- assumptions register
- open questions
- signal log

### Stap 4 — Laat BA, Functional en Architect werk
Die volgorde is:
1. Business Analyst
2. Functional Designer
3. Infrastructure Architect
4. ScrumMaster
5. Devil’s Advocate
6. QA
7. Release Manager

### Stap 5 — Begin met eerste module kickoff
Gebruik die module templates in:
- `modules/taxidermy_mvp/`
- `templates/`

## Aanbevole eerste repo/artefakte
- `README.md`
- `AGENTS.md`
- `GOVERNANCE.md`
- `SCRUM_OPERATING_MODEL.md`
- `BACKLOG.md`
- `ROADMAP.md`
- `CHANGELOG.md`

## Praktiese advies
- Gebruik klein iterasies
- Merk simulasie vs regte integrasie duidelik
- Hou scope vir MVP hard
- Parkeer CRM-visie en ander droommodules in roadmap, nie in huidige sprint nie


## v0.2 Additional required checks
Before calling the bootstrap complete:
- confirm inheritance summary exists
- confirm `decision_log_policy.md` is present
- confirm `PARKING_LOT.md` exists
- confirm `DEMO_VS_PRODUCTION_STATUS.md` is understood as a release discipline
