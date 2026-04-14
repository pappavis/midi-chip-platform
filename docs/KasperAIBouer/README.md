# KasperAIBouer Prompt Pack v0.1

## Doel
Hierdie pakket bevat die volledige OpenClaw-gerigte governance, agentprompts, skills, templates en module-scaffolding vir `KasperAIBouer`.

`KasperAIBouer` is ontwerp as 'n **herbruikbare AI project governance core** vir klein tot medium digitale bouprojekte waar:
- discovery uit rou gesprekke, voice notes, WhatsApps en dokumente kom
- AI-agents gekoördineer moet word
- risiko's en scope creep aktief bestuur moet word
- dokumentasie deur mense gelees en gebruik moet kan word
- die eerste konkrete use case `taxidermy_mvp` is

## Kernbesluite
- Hoofprojek: `KasperAIBouer`
- Werkmodus: `GO V2` / pragmaties, sterk, bruikbaar
- Eerste module: `taxidermy_mvp`
- Governance-erfenis: **verpligtend**. Die stelsel mag nie finale scaffolding finaliseer voordat die huidige `sn76489builder` prompt en relevante governance-bronne opgevra en opgesom is nie.
- Scrum: aparte agent + geïntegreerde governance skill
- Databronne: alle projekbronne woon onder `references/` subdirectories
- Styl: Afrikaans + Engels tegnies gemeng

## Wat in hierdie pakket is
- `agents/` — alle agentdefinisies
- `skills/` — herbruikbare skills
- `prompts/` — master, bootstrap en utility prompts
- `governance/` — roles, gates, artefact policy, handoff policy
- `templates/` — reusable dokumenttemplates
- `modules/taxidermy_mvp/` — eerste module-scaffold
- `references/` — bronbeleid en naming conventions
- `repo/` — repo- en workspace strategy

## Belangrike gebruiksreël
Gebruik hierdie pack nie as “druk knoppie, kry produk” nie. Gebruik dit as:
1. governance core
2. source-ingestion discipline
3. role-based analyse/ontwerp/besluitvorming
4. MVP scope beheer
5. review + QA + release handoff

## Minimum aanbevole eerste gebruiksvolgorde
1. Lees `INSTALL.md`
2. Voer `prompts/bootstrap/first_run_governance_intake.md` uit
3. Versamel huidige `sn76489builder` prompt en governance
4. Laat inheritance summary produseer
5. Voer `prompts/bootstrap/openclaw_bootstrap.md` uit
6. Laat `KasperAIBouer_Master` die eerste module kickoff koördineer
7. Begin met `modules/taxidermy_mvp/` artefakte

## Let wel
Hierdie pakket maak die stelsel **governance-klaar**. Dit bou nie outomaties die hele taxidermy app end-to-end in hierdie weergawe nie. Dit skep die pad, ritme, templates, rolverdeling en eerste module scaffolding om dit beheerbaar te doen.


## v0.2 Highlights
This release tightens governance around:
- decision traceability
- scope boundaries
- demo vs production honesty
- inheritance summary formalization
- open questions and parking-lot discipline

## Recommended first-run sequence in v0.2
1. Run governance inheritance intake.
2. Produce inheritance summary.
3. Bootstrap the structure only after inheritance is accepted.
4. Load current references.
5. Run intake synthesis before business or functional design.
