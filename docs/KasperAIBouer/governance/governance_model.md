# GOVERNANCE MODEL

## Doel
`KasperAIBouer` is 'n AI-governance boustelsel vir modulêre projekontwikkeling. Die stelsel moet:
- bronne inneem
- discovery sintetiseer
- scope beheer
- agente koördineer
- artefakte op standaard produseer
- risiko’s uitlig
- mensleesbare uitsette lewer
- release/handoff voorberei

## Governance beginsels
1. **Heritage first**  
   Finale scaffolding en policies mag nie gelock word voordat die huidige `sn76489builder` prompt en relevante governance ingevoer en opgesom is nie.

2. **References are first-class**  
   Bronmateriaal in `references/` is nie bysaak nie. Dit is die primêre grondslag van die projek.

3. **Readable by humans**  
   Alle belangrike artefakte moet deur 'n mens gelees, beoordeel en teruggekoppel kan word.

4. **MVP before platform fantasy**  
   Eerste module word tot 'n realistiese MVP gesny. Roadmap-items word geparkeer en nie stilweg in huidige scope ingedruk nie.

5. **Roles with boundaries**  
   Elke agent het 'n rol, ingang, uitset en grenslyn. Agents mag nie onnodig oorvleuel of mekaar se werk oorneem sonder rede nie.

6. **No false certainty**  
   Aannames, onbekendes, afhanklikhede en ongetoetste dele moet eksplisiet benoem word.

7. **Risk surfaced early**  
   Devil’s Advocate en QA word nie aan die einde bygevoeg net vir vorm nie; hulle word ingebou as kernstappe.

8. **Scrum discipline over chaos**  
   Backlog, slicing, readiness en done-kriteria word aktief bestuur.

9. **Modular, reusable structure**  
   `KasperAIBouer` moet herbruikbaar wees vir later modules, maar die huidige module mag nie verdrink in generiese platformdenke nie.

## Werkslae
### Laag 1 — Governance Core
- policies
- gates
- artefakdissipline
- reviewritme

### Laag 2 — Operational Structure
- OpenClaw paths
- workspace struktuur
- agent files
- templates
- logs

### Laag 3 — Persona & Prompt Layer
- Kasper persona
- master prompt
- agent prompts
- scrum skill
- utility prompts

### Laag 4 — Project Modules
- taxidermy_mvp
- latere modules soos diesel rebate, WhatsApp accountant, CRM core

## Verpligte ritme
1. Inheritance
2. Source ingestion
3. Source synthesis
4. Business framing
5. Functional framing
6. Infrastructure review
7. Backlog / sprint slicing
8. Devil’s advocate review
9. QA review
10. Release/handoff

## Besluitregister
Enige groot besluit oor:
- hosting
- database
- integrations
- auth
- data visibility
- cost model
- phase cut
moet in ’n artefak vasgelê word, nie net in chat verbleik nie.
