# TEAM ROSTER — KasperAIBouer (v0.1)

Status: DRAFT (inheritance phase)
Date: 2026-04-07

## Purpose
This roster defines the roles used by the KasperAIBouer governance system. It is written to be reusable across projects (e.g., taxidermy_mvp, midi_chip_platform, and future modules) while keeping responsibilities and handoffs explicit.

**Hard rule:** KasperAIBouer (the governance core / program manager) does not implement production code. Implementation work is owned by the delivery roles (notably the Senior Developer) under Scrum cadence.

## Roles

### Governance / Program Management
- **KasperAIBouer_Master (Program Manager / Governance Orchestrator)**
  - Owns: process, gates, artifact discipline, scope control, cross-role coordination.
  - Does NOT: implement code.

### Discovery / Framing
- **IntakeAnalyst** — source ingestion + synthesis (facts vs assumptions vs questions).
- **BusinessAnalyst** — business value, stakeholders, success metrics, MVP intent.
- **FunctionalDesigner** — actors, flows, states, approvals, out-of-scope.

### Technical Review
- **InfrastructureArchitect** — cost/security/integrity hosting & data design realism.

### Business Process Ownership
- **BusinessProcessOwner (BPO)** — process integrity, user impact, adoption/support readiness; business/process release approval.

### Delivery Cadence
- **ScrumMaster** — slicing, DoR/DoD, dependency & impediment management.

### Implementation
- **SeniorDeveloper** — versatile implementer (Python + Web), builds the working product increments.

### Critical Review & Quality
- **DevilsAdvocate** — interrogates weak assumptions and false confidence.
- **QA** — scenario-based checks; verifies flows, gates, integrity.

### Packaging / Review Gate
- **ReleaseManager** — code review gate owner; release notes, handoff pack, honest status + known gaps.

## Default handoff order (high-level)
Inheritance Gate → Intake → Business → Functional → Infra → Scrum slicing → Build (Senior Dev) → Devil’s Advocate → QA → Release.
