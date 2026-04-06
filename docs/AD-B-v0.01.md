# AD-B-v0.01 — Devil's Advocate Review

**Artefak-ID:** AD-B-v0.01  
**Date:** 2026-04-06 (Den Haag)  
**Baseline:** MP-B-v2.3.0  
**Audience:** Recruiters + synth enthusiasts  
**Scope:** Alignment of SN76489 playable MVP into `midi_chip_platform` (Variant B, single-file baseline)  
**Relevante backlog UUIDs:** [A1B2C3D4](./BACKLOG.txt), [E5F6G7H8](./BACKLOG.txt)  

---

## 1. Purpose (why be adversarial?)

This document intentionally argues against the project’s success.

The goal is not negativity; the goal is to surface the *real* failure modes that a user (or reviewer) will encounter, and to propose mitigations that are cheap and effective.

In audio/MIDI projects, many failures look identical (“silence”), but the root causes differ radically:
- routing vs channel mismatch
- audio backend vs output device
- driver quirks vs code bugs
- OS-level gadget enumeration vs Python MIDI handling

A devil’s advocate review forces clarity:
- what is actually validated
- what is a hypothesis
- what will most likely make a reviewer bounce

---

## 2. Context snapshot (what we are judging)

- Variant B: software chip emulation with Python
- MVP focus: USB MIDI IN → SN76489-style engine → audible output
- Confirmed: MVP runs on macOS; Logic Pro via IAC on channel 3 works
- Pending: Pi Zero 2 USB MIDI gadget verification

This means the core pipeline is proven on macOS, but the “hardware instrument” story is still a risk until verified.

Important: this doc is scoped to the MVP and its presentation to recruiters + synth enthusiasts. It is not attempting to judge the entire long-term product.

---

## 3. Adversarial success criteria (what would make me say “no”)

If I were trying to disqualify this repo as a reviewer, I would look for:

1) **Docs that overclaim** (e.g., implying Pi is validated when it isn’t).
2) **A demo path that depends on hidden knowledge** (unwritten setup steps).
3) **A failure that looks like the project is broken** (hangs, silence, stuck notes) with no guided recovery.
4) **Ambiguous scope** (is this an emulator, a synth, a hardware gadget project, or all of the above?).
5) **Missing evidence discipline** (no results ledger; no record of what passed).

If any of those exist, the project’s technical merit may not matter; the reviewer will churn.

---

## 4. Biggest failure mode: misunderstanding the USB-MIDI device problem

### Critique

The Pi goal can be misunderstood as a Python/MIDI issue (“just open a MIDI port”).

In reality, the Pi appearing as a USB MIDI device is an **OS-level gadget configuration** problem.

If a user expects the Python program to “make the Pi appear,” they will fail and conclude the project is broken.

### Mitigation

- Keep gadget scripts and sanity checks in-repo.
- Put gadget verification steps in the TEST plan.
- In docs, explicitly separate two systems:
  1) gadget enumeration (USB device presence)
  2) synth runtime (MIDI→audio)

### Residual risk

Even perfect scripts cannot fix:
- wrong OTG port
- charge-only cable
- kernel limitations

Therefore, the docs must normalize these failure modes (“this is the usual culprit”).

---

## 5. The “silence problem” is a UX problem, not just a bug problem

### Critique

A reviewer’s first experience is often:
- they run `run`
- they play notes
- nothing happens

At that moment, it does not matter if the code is correct. The project feels broken.

Audio/MIDI tools need a **guided diagnostic flow** baked into the documentation:
- what command to run next
- what evidence to look for
- what conclusion to draw

### Mitigation

- Provide a decision tree for silence triage.
- Teach the layer model explicitly:
  1) audio works (`test basic`)
  2) MIDI arrives (`monitor`)
  3) channel matches
  4) end-to-end sound

### Residual risk

Even with a decision tree:
- DAW routing UIs are confusing
- port names vary across systems

But the goal is not to prevent all failure; the goal is to ensure failures look *understandable*.

---

## 6. Channel mismatch (0..15 vs 1..16) will still bite someone

### Critique

MIDI channel mismatch is the most common “it’s silent” bug.
Even with careful coding, users will still think in 1–16 while libraries use 0–15.

### Mitigation

- Keep CLI/config in 1–16 only.
- Print channel behavior clearly in monitor output.
- Add a troubleshooting checklist that says: “If you see messages on channel 2 but you expect 3, your DAW is sending on 2.”

### Residual risk

DAWs sometimes show “All” or “Omni” settings; users may not realize what they selected.

---

## 7. MIDI port handling: the hang problem and the trust problem

### Critique

Some MIDI ports hang when opened. The user will interpret a hang as “this project is unstable.”

Hangs are worse than clean failures:
- no feedback
- looks like a crash
- forces a hard kill

### Mitigation

- Encourage explicit `--midi-port` usage.
- Print PID on startup.
- Fail fast when a specified port doesn’t exist.
- Provide a “known-good port” example (IAC bus) for macOS.

### Residual risk

The bug may be in driver/OS, not in the code. The best defense is clear guidance and defensive defaults.

---

## 8. Pi Zero 2 performance: the “Python is too slow” narrative

### Critique

Even if the synth works, audio glitches on Pi could create a narrative that “Python can’t do real-time audio.”
That would undercut both enthusiast trust and recruiter interpretation.

### Mitigation

- Keep synthesis simple and vectorized.
- Provide recommended buffer sizes for Pi (“safe mode”).
- Document that stability is prioritized over ultra-low latency.

### Residual risk

Some audio backends are fragile; users may need tuning.
If tuning is not documented, the project feels unreliable.

---

## 9. Chip accuracy expectations: the authenticity trap

### Critique

Chip communities can be strict.
If someone expects register-accurate SN76489 behavior, they may dismiss the MVP as “wrong.”

### Mitigation

- Be explicit: MVP is a playable approximation.
- Put “accuracy mode” on the roadmap.
- Provide a crisp statement: “This project optimizes demoability first; accuracy is a milestone.”

### Residual risk

Some people won’t care. That’s okay. The target audience includes recruiters and synth enthusiasts who value hackability.

---

## 10. Documentation drift: the silent project killer

### Critique

For a project like this, docs are not optional.
If docs and code drift, a reviewer can’t reproduce the demo, and the repo loses credibility.

### Mitigation

- Keep artifact IDs stable.
- Update FS/TS/TEST when behavior changes.
- Use the backlog UUIDs to anchor work.
- Treat the results ledger as part of the definition of done.

### Residual risk

Documentation always lags unless it is treated as part of the deliverable.

---

## 11. Deep-dive risk register (severity × likelihood)

This section is intentionally concrete. It identifies what could go wrong, how it would look to a reviewer, and what the cheapest mitigation is.

### 11.1 R1 — “Silence” with no guidance

- **Severity:** High (instant loss of trust)
- **Likelihood:** High
- **How it presents:** user runs `run`, plays notes, hears nothing, quits
- **Mitigation:** decision tree + explicit monitor workflow (docs)
- **Residual risk:** Medium

### 11.2 R2 — Overclaiming Pi readiness

- **Severity:** High (credibility damage)
- **Likelihood:** Medium
- **How it presents:** README implies Pi works; user cannot enumerate device
- **Mitigation:** explicit “pending verification” labeling everywhere
- **Residual risk:** Low if disciplined

### 11.3 R3 — Stuck notes during demo

- **Severity:** High (demo killer)
- **Likelihood:** Medium
- **How it presents:** note does not stop, user panics
- **Mitigation:** CC123 guidance + optional auto note-off + “panic rehearsal”
- **Residual risk:** Medium

### 11.4 R4 — MIDI port hang

- **Severity:** Medium/High (looks like unstable code)
- **Likelihood:** Medium (depends on devices)
- **How it presents:** CLI freezes while opening ports
- **Mitigation:** explicit `--midi-port`, fail-fast checks, print progress
- **Residual risk:** Medium

### 11.5 R5 — Reviewer cannot map architecture quickly

- **Severity:** Medium (they won’t invest time)
- **Likelihood:** Medium
- **How it presents:** repo has code but unclear architecture story
- **Mitigation:** SKILLS “30-second architecture” + diagrams/flow
- **Residual risk:** Low

---

## 12. Adversarial questions (what reviewers will ask, even if politely)

### 12.1 “What exactly is validated?”

If the answer is fuzzy, the reviewer assumes the worst.

Required response:
- macOS + Logic via IAC channel 3 is confirmed.
- Pi gadget is pending.
- anything else is unknown unless in the ledger.

### 12.2 “How do I know the MIDI is arriving?”

If the only answer is “it should,” the reviewer loses time.

Required response:
- run `monitor` on the exact port and channel.

### 12.3 “What happens if I pick the wrong port?”

If the answer is “it hangs,” that’s unacceptable.

Required response:
- explicit port selection; clear failure if not found.

### 12.4 “Is this a toy or an engineering artifact?”

Recruiters often use this question to judge maturity.

Signals of maturity:
- explicit scope
- results ledger
- traceability to backlog
- clear runbooks

---

## 13. What I would improve first (highest ROI mitigations)

These are the cheapest improvements that buy the most trust:

1) **Make the diagnostic path first-class:** always teach `test basic` and `monitor`.
2) **Make validation boundaries unavoidable:** “macOS confirmed; Pi pending” in README and release notes.
3) **Make reviewer experience predictable:** copy/paste runbook in SKILLS and DEPLOY.
4) **Provide a release notes template that forbids overclaiming.**

None of these require new synthesis features.

---

## 14. Verdict (devil’s advocate)

The macOS path is strong and already validated.

The biggest risk to a public release is **not** the synth itself; it is the “outer layers”:
- MIDI device variability
- hardware gadget enumeration
- user misunderstanding of routing

Recommendation:
- Do not publish a public release tag until:
  - README and TEST plan are aligned,
  - the macOS demo path is reproducible from scratch,
  - the Pi gadget is either verified or explicitly labeled as pending.

This is not perfectionism; it is credibility management.

---

## 15. Pre-mortem: how this project fails in the wild (story-based)

Imagine it’s a week after you publish.

### Scenario PM-1 — The recruiter tries it in 5 minutes

- They clone the repo.
- They see Python code and a long README.
- They run one command, get silence, and stop.

**Interpretation risk:**
- They conclude it’s “unfinished” even if it works.

**Countermeasure:**
- Make the “three proofs” path unavoidable: `test basic` → `monitor` → `run`.
- Put it at the top of README and SKILLS.

### Scenario PM-2 — The synth enthusiast expects accuracy

- They expect register-level behavior.
- They compare to a tracker or emulator.
- They decide it’s “not real SN76489.”

**Interpretation risk:**
- They dismiss the repo, and their dismissal influences others.

**Countermeasure:**
- Be explicit about the goal: playable approximation.
- Put accuracy mode on roadmap (and label it as future work).

### Scenario PM-3 — The Pi gadget path becomes the headline

- People fixate on “turn a Pi into a USB MIDI device.”
- They hit the OTG/cable/UDC pitfalls.
- They call the project broken.

**Interpretation risk:**
- The project is judged by its hardest, least validated subsystem.

**Countermeasure:**
- Separate “hardware story” docs from “validated MVP demo” docs.
- Use consistent labeling: pending vs confirmed.

---

## 16. Maintainability risks (long-term credibility)

### 16.1 Single-file baseline: strength and trap

Strength:
- reviewers can read everything quickly
- changes are easier to reason about early

Trap:
- as features grow, a single file becomes a dumping ground
- reviewers perceive “spaghetti,” even if the code works

Mitigation:
- keep the single-file baseline for the MVP, but document an exit plan:
  - extract modules only when boundaries are stable
  - keep CLI surface stable

### 16.2 Dependency risk

Python audio/MIDI stacks can be sensitive.
A reviewer might interpret dependency friction as engineering sloppiness.

Mitigations:
- keep deps minimal
- keep install instructions short
- ensure import errors produce clear messages

---

## 17. Security and safety (what could alarm a reviewer)

This project is not security-sensitive by default, but it does:
- open device ports
- run audio callbacks
- (optionally) run `sudo` scripts on a Pi

A cautious reviewer might ask:
- “What does the `sudo` script change?”
- “Can it brick my device?”

Mitigations:
- keep gadget scripts isolated under `scripts/`
- explain that reboot resets gadget state
- ensure docs say “run only on a device you control”

This is not paranoia; it’s reviewer empathy.

---

## 18. Recruiter skepticism checklist (signals they look for)

Recruiters and hiring managers often skim for signals:

Strong signals:
- explicit scope (“what it is” and “what it isn’t”)
- traceability (docs + backlog)
- validation discipline (results ledger)
- operational maturity (runbooks and decision trees)

Weak signals:
- vague claims (“works on Pi”) without evidence
- screenshots without reproduction steps
- missing “how to debug” guidance

If you optimize the repo for these signals, you increase the chance it’s judged fairly.

---

## 19. Devil’s advocate scorecard (quick rubric)

Use this rubric to self-assess before a release:

- **Reproducibility (0–2):**
  - 0: steps ambiguous
  - 1: steps exist but require guessing
  - 2: steps are copy/paste, time-bounded

- **Honesty about validation (0–2):**
  - 0: implied support beyond evidence
  - 1: partially explicit
  - 2: confirmed vs pending clearly separated

- **Diagnosability (0–2):**
  - 0: silence has no path
  - 1: some tips
  - 2: decision tree + tools (`monitor`) make issues isolatable

- **Demo risk (0–2):**
  - 0: hangs/stuck notes likely
  - 1: mitigations exist but unclear
  - 2: panic/recovery runbook exists

Target:
- At least 7/8 before tagging a public release.

---

## 20. Mitigation validation (how to know the mitigations work)

A mitigation is only useful if we can observe its effect.

### 20.1 Mitigation: decision tree for silence triage

Success condition:
- a new user can determine whether the issue is audio vs MIDI vs channel in under 5 minutes.

How to validate:
- ask a fresh reviewer to follow the runbook and report where they got stuck.

### 20.2 Mitigation: explicit “confirmed vs pending” labeling

Success condition:
- a reviewer can answer “Is Pi validated?” correctly without asking you.

How to validate:
- skim test: ask someone to read only README + release notes draft; see what they conclude.

### 20.3 Mitigation: panic/recovery runbook for stuck notes

Success condition:
- during a rehearsal, you can silence audio within 10 seconds.

How to validate:
- rehearse CC123 + restart procedure.

---

## 21. Counter-arguments (why the MVP is still credible)

This devil’s advocate document is adversarial, but it’s also important to state why the MVP is still a strong engineering artifact.

1) **Validated macOS demo path exists.**
   - Many hobby repos never reach an end-to-end proof.

2) **The repo treats docs as deliverables.**
   - Artifact IDs, traceability, and a ledger are uncommon in small projects.

3) **The project optimizes for reviewability.**
   - Single-file baseline and explicit runbooks reduce reviewer effort.

4) **The project is honest about uncertainty.**
   - “Pending” is stated rather than implied.

These points matter because recruiters often judge maturity more than feature count.

---

## 22. Recommended next actions (devil’s advocate backlog mapping)

These are deliberately framed as tasks that reduce *review risk*, not tasks that add features.

- **A (high priority):** keep README, SKILLS, DEPLOY, TEST aligned
- **A:** ensure `monitor` output is easy to interpret (timestamps, channel display)
- **A:** confirm `run` fails fast when a port name is wrong (no silent hangs)
- **B (medium):** one external reviewer run through the demo path
- **B:** Pi gadget verification (only if you want to claim it)
- **C (later):** accuracy milestone and measurements (only after onboarding is robust)

---

## 23. Additional risks worth naming (even if you accept them)

### 23.1 Cross-platform temptation

Risk:
- once people see Python, they assume it works on Windows/Linux automatically.

Why it matters:
- support expectations expand silently.

Mitigation:
- explicitly list validated environments.
- treat additional platforms as backlog items, not implied features.

### 23.2 “Sound quality” subjective critique

Risk:
- synth enthusiasts might critique timbre or aliasing.

Mitigation:
- frame the goal as “playable retro flavour,” not “studio-grade production.”
- focus the demo on responsiveness and the MIDI-to-audio pipeline.

### 23.3 Dependency installation friction

Risk:
- if installs fail, a reviewer may not try again.

Mitigation:
- keep install instructions minimal and copy/paste.
- document common install failures.

### 23.4 Audio device exclusivity / backend quirks

Risk:
- some systems can have exclusive mode or device contention.

Mitigation:
- teach the user to validate audio independently (`test basic`).
- keep the troubleshooting tree in docs.

---

## 24. What I would *not* do (scope discipline)

Devil’s advocate advice is often: “add more features.” That’s usually wrong.

Avoid for MVP release readiness:
- adding more synthesis parameters without improving diagnosability
- adding Pi claims without ledger proof
- adding multiple DAW paths before one path is bulletproof

Instead:
- improve the experience of the one validated path
- and make failure modes understandable

---

## 25. Final adversarial summary (one paragraph)

This project succeeds when it is boring to run:
- a reviewer can paste commands, hear sound, and understand what to do when it fails.

It fails when it is surprising:
- silence with no guidance,
- implied Pi support,
- hangs, or
- stuck notes.

The good news is that most mitigations are documentation and operational discipline, not new synthesis features.

---

## 26. Documentation as the user interface (UI)

In a CLI audio tool, docs *are* the UI.

### 26.1 What a reviewer perceives as "quality"

Often it’s not DSP correctness. It’s:
- clear steps
- fast proof of life
- clear failure paths

If docs are confusing, the project feels low-quality even if the engine is solid.

### 26.2 The minimum mental model you must teach

A new user needs exactly this model:

- Audio can work even if MIDI is broken.
- MIDI can work even if audio is broken.
- Channels can silently filter correct MIDI.

If you teach this, users stop blaming the wrong layer.

### 26.3 A practical litmus test

If a reviewer can answer these three questions after reading SKILLS:
1) “How do I prove audio works?”
2) “How do I prove MIDI arrives?”
3) “How do I connect them?”

…then your docs are doing their job.

---

## 27. How to respond to common criticisms (without arguing)

This section is pragmatic: if someone criticizes the project, you want a response that preserves credibility.

### “This is just Python, it can’t do real-time audio.”

Response:
- “Real-time audio is about the callback and buffer strategy. The MVP proves the end-to-end path on macOS. If we want to claim performance, we’ll measure and record it.”

### “It’s not chip accurate.”

Response:
- “Correct. This MVP is about a playable retro flavour and integration reliability. Accuracy is a planned milestone and will be explicitly measured.”

### “The Pi part doesn’t work.”

Response:
- “The gadget path is documented, and it’s explicitly marked as pending verification until it’s recorded in the ledger. The validated demo path is macOS + IAC.”

### “I got silence, so it’s broken.”

Response:
- “Silence has multiple causes; we designed a diagnostic flow: `test basic` proves audio, `monitor` proves MIDI, then `run` connects them.”

These responses keep the conversation factual.

---

## 28. Evidence discipline as a credibility feature

Many repositories fail socially, not technically.

A results ledger does three important things:
- It prevents accidental exaggeration.
- It lets reviewers trust your statements.
- It gives you a stable reference when you update code.

In practice:
- update the ledger after each rehearsal
- keep “pending” items pending until there is evidence

This is the simplest “process” that dramatically improves how the repo is perceived.

---

## 29. Traceability

- Backlog: [BACKLOG.txt](./BACKLOG.txt)
- Test plan: [TEST-B-v0.01](./TEST-B-v0.01.md)
- Deploy plan: [DEPLOY-B-v0.01](./DEPLOY-B-v0.01.md)
- Discovery report: [DR-B-v0.01](./DR-B-v0.01.md)

---

## 16. Credits

- Michiel Erasmus

---

## 17. Changelog (AD-B-v0.01)

### 2026-04-06
- Expanded critique into a structured risk review with mitigations and residual risks
- Added explicit validation boundary (macOS confirmed; Pi pending)
- Added traceability links to backlog and key artifacts
- Pass 2: added a concrete risk register and adversarial reviewer question set
