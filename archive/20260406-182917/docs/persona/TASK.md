# TASK — sn76489builder (governance workflow)

**Baseline:** MP-B-v2.3.0  
**Purpose:** define how work is planned, executed, reviewed, and released.

---

## 1) Default workflow (plan-first)

For any non-trivial change (code, docs, releases), follow this order:

1. **State the goal** in one sentence.
2. **State baseline** (MP-B-v2.3.0) and current confirmed claims.
3. **List impacted files** (exact paths).
4. **List risks** (failure modes + how we’d detect them).
5. **Execution plan** (step-by-step).
6. **Wait for GO**.
7. Implement with minimal changes.
8. Provide **smoke tests**.
9. Append a **devil’s advocate** note.

---

## 2) Traceability rules

### 2.1 Backlog UUID discipline
- Every significant work item links to a backlog UUID (8 chars).
- Docs should reference:
  - `BACKLOG.txt`
  - relevant artifacts (FS/TS/TEST)

### 2.2 Artifact suite discipline
If behavior changes, update:
- FS (what it must do)
- TS (how it does it)
- TEST (how to verify)
- REL/DEPLOY (how to ship)

Avoid “code changed but docs didn’t”.

---

## 3) Validation policy (no overclaim)

### 3.1 Confirmed vs pending
- Confirmed means observed end-to-end and recorded.
- Pending means designed/implemented but not yet verified.

### 3.2 Current allowed confirmed statements
- macOS: `test basic` produces sound.
- Logic Pro → IAC → channel 3 drives the synth.

Everything else must be phrased as pending until verified.

---

## 4) Change safety

- Do not delete user data.
- Prefer reversible changes.
- If archiving, use `git mv` to preserve history.
- Avoid symlinks for release artifacts.

---

## 5) Release workflow (when user says publish)

1) Ensure docs and code are in sync.
2) Ensure TEST ledger reflects what is truly confirmed.
3) Sync to repo workdir (rsync).
4) Commit with clear message.
5) Tag: `FW-B-v0.01`.
6) Create GitHub release using `docs/REL-B-v0.01.md`.

---

## 6) Review checklist (recruiter lens)

Before calling something “ready”:
- Can a reviewer run it in <10 minutes?
- Do we have a clear demo path (Logic/IAC/channel 3)?
- Is the monitor output useful?
- Are risks honest (Pi pending)?
- Are next steps concrete?

---

## 7) Failure recovery protocol

If something breaks:
1) Identify which layer failed: config / MIDI / engine / audio / OS.
2) Use `monitor` to confirm MIDI input.
3) Use `test basic` to isolate audio.
4) Reduce variables (one port, one channel).
5) Roll back the last commit if needed.

---

## 8) Changelog

- 2026-04-06: Created TASK governance workflow aligned to MP-B-v2.3.0, traceability, and release discipline.
