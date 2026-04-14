# APPROVAL GATES

## Doel
Approval gates keer dat die projek chaoties van idee na implementasie spring.

## Gate 0 — Governance Inheritance Complete
### Vereistes
- huidige `sn76489builder` prompt aangevra
- relevante governance-bronne versamel
- inheritance summary opgestel
- erflike beleidsbesluite aangeteken

### Status
- PASS / BLOCKED

## Gate 1 — Source Intake Complete
### Vereistes
- bronne in `references/` geplaas
- naming standard gevolg
- source log opgestel

## Gate 2 — Source Synthesis Accepted
### Vereistes
- source synthesis
- assumptions register
- open questions
- signal log
deur `IntakeAnalyst` opgestel en deur `Master` aanvaar

## Gate 3 — Business Framing Accepted
### Vereistes
- probleemdefinisie
- stakeholders
- goals
- business value
- MVP intent
vasgelê

## Gate 4 — Functional Scope Locked
### Vereistes
- actors
- user flows
- states/statuses
- approvals
- out-of-scope list
- MVP cut
vasgelê

## Gate 5 — Infra Review Passed
### Vereistes
- database options review
- hosting/cost scenarios
- security minimums
- integration assumptions
- local/self-host reality check

## Gate 6 — Sprint Ready
### Vereistes
- backlog items klein genoeg
- acceptance criteria bestaan
- dependencies gesien
- stories voldoen aan Definition of Ready

## Gate 7 — Devil’s Advocate Reviewed
### Vereistes
- kritieke gate / risks / false confidence areas aangedui
- aanbevelings gelog

## Gate 8 — QA Ready
### Vereistes
- toetsbare scenarios
- integrity checks
- approval-flow checks
- release criteria bestaan

## Gate 9 — Release Candidate Ready
### Vereistes
- artefakte volledig
- scope vir release duidelik
- bekende gaps aangeteken
- handoff notes gereed

## Belangrike reël
Geen agent mag 'n latere gate as “bereik” aanneem as die vereistes nie eksplisiet vasgelê is nie.


## v0.2 refinement — artifact-linked expectation
Each gate should now be read together with `ARTIFACT_READINESS_MATRIX.md` so that gates are not interpreted abstractly.
