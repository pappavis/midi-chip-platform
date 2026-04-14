# GOVERNANCE INHERITANCE SUMMARY — v0.1

Status: ACCEPTED (Gate 0 PASS)
Date: 2026-04-07
AcceptedBy: user (message_id: a2786f14-47b2-45a8-9ee5-da413d3c6b2e)

## Scope
This document captures governance inheritance from **sn76489builder** (midi_chip_platform) into **KasperAIBouer**.

Hard rule: **Do not declare KasperAIBouer governance locked** until this inheritance summary exists and is accepted.

## Sources ingested
1) sn76489builder master prompt (user paste)
- Stored at:
  - `/Users/michiele/.openclaw/workspace/KasperAIBouer/references/inheritance/sn76489builder/sn76489builder_masterprompt_MP-B-v2.3.0_2026-04-06.md`

2) midi_chip_platform docs directory inventory (user listing)
- Stored at:
  - `/Users/michiele/.openclaw/workspace/KasperAIBouer/references/inheritance/sn76489builder/DOCS_INVENTORY_midi_chip_platform_docs_2026-04-07.md`

## Retained rules (carry over as-is)
- **Inheritance-first gate:** request existing governance/masterprompt sources before finalizing new governance.
- **Honesty / no overclaim:** do not claim completion without evidence.
- **Plan-first:** show an execution plan before doing major steps; wait for approval where required.
- **Traceability mindset:** link work to explicit artifacts and decisions.
- **Release/readiness honesty:** explicit known gaps/risks rather than polished language.

## Adapted rules (intentionally changed for KasperAIBouer)
- **Code review ownership:** ReleaseManager owns the code-review gate (explicit reviewer-of-record).
- **KasperAIBouer is Program Management / Governance, not an implementer.**
  - KasperAIBouer does not build production code.
  - Implementation is owned by a dedicated delivery role.

- **Word-count quality gate for User Stories artifacts:**
  - When generating User Stories docs, target approximately **~4500 words** (unless explicitly overridden).

- **Team composition extension:** add a reusable Senior Developer role.
  - Role spec: `/Users/michiele/.openclaw/workspace/KasperAIBouer/governance/team/SENIOR_DEVELOPER_ROLE_v0.1.md`
  - Team roster: `/Users/michiele/.openclaw/workspace/KasperAIBouer/governance/team/TEAM_ROSTER_v0.1.md`

## Rejected rules (not inherited)
- Project-specific technical constraints that are unique to midi_chip_platform (e.g., “single-file Python emulator policy”) are **not** globally enforced by KasperAIBouer.
  - They may exist as module-level constraints when relevant.

## Risks of divergence
- Adding an implementation role can blur boundaries with Architect/Functional roles.
  - Mitigation: keep explicit handoffs and DoR/DoD; Senior Developer builds only approved slices.
- Word-count targets can create “padding”.
  - Mitigation: require substance: scenarios, edge cases, constraints, acceptance criteria.

## Current status
- **NOT LOCKED.**
- Next step: user confirms this summary is acceptable; then Gate 0 may be marked PASS.
