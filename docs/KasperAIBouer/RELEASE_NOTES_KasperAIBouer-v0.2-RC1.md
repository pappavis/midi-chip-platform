# RELEASE NOTES — KasperAIBouer-v0.2-RC1

Status: **Release Candidate** (see Status Assessment)
Date: 2026-04-07

## Release status (required honesty)
- Current status label: **MVP** (governance pack MVP; not production-safe by default)
- Truth statement:
  - This release is a **governance/prompt-pack** milestone. It is designed to be *usable* for structured project work.
  - It is **not** a guarantee of production readiness for any specific software product.
  - Where the pack drives “build” work, those actions remain gated by approvals and role handoffs.

## Scope — what’s included
- KasperAIBouer prompt pack structure (agents/prompts/governance/templates/modules/references/repo).
- Approval gates discipline (Gate 0–9) and artifact-linked readiness expectations.
- Demo vs Production status discipline.
- Handoff policy requiring explicit unknowns and what is real vs simulated.
- Team model with explicit separation of governance vs implementation.
- Senior Developer role + agent exists (implementation role is present but governed).
- BPO agent exists globally and is assigned to KasperAIBouer (business/process lens).

## Scope — what’s NOT included
- No production software system is shipped by this release.
- No guarantee that downstream project modules are complete (taxidermy_mvp remains a module scaffold).
- No claim of security/compliance beyond what is explicitly documented.

## What changed (high level)
- v0.2 adds governance discipline around:
  - parking lot
  - open questions register
  - decision log policy
  - artifact readiness matrix
  - demo vs production honesty
  - stricter first-run sequence (inheritance-first)

(See `CHANGELOG.md` for the detailed list.)

## Known gaps / risks
- Release Candidate does not by itself prove adoption readiness; a short “how to use in 30 minutes” guide may still be needed for new users.
- If roles blur (PM/BA/Functional/Developer), scope creep risk increases.
- If release notes are not used, teams may overclaim “production-ready” behaviour.

## Rollback / escape hatch
- If RC1 causes confusion or workflow friction, revert to the previous pack version and use this RC only as reference.
- Rollback trigger examples:
  - repeated user confusion about which gate to run next
  - significant support load because “demo” is mistaken for “prod”

## Support / escalation
- Governance questions: route to KasperAIBouer_Master.
- Release gate packaging: route to ReleaseManager.
- Business/process readiness: consult BPO.

## Next safe step
- Run an explicit RC review checklist (BPO + ReleaseManager + QA) and record PASS/BLOCKED/CONDITIONAL.
