# Business Case — midi_chip_platform (Variant B)

**Artefak-ID:** BC-B-v0.01  
**Datum:** 2026-04-06 (Den Haag)  
**Status:** Draft (content-complete; align README before public release tag)  
**Baseline:** MP-B-v2.3.0  
**Audience:** Recruiters + synth enthusiasts  
**Relevante backlog UUIDs:** [A1B2C3D4](./BACKLOG.txt), [E5F6G7H8](./BACKLOG.txt)  

---

## 1. Purpose (what “business case” means here)

This repo can be viewed through multiple lenses:

- **Portfolio artifact:** demonstrate engineering maturity across MIDI + audio + OS integration.
- **Open-source instrument platform:** a hackable chip-synth toolchain.
- **Potential product seed:** later packaging into a standalone app or plugin wrapper.

This business case does not assume a single destiny. Instead, it clarifies:
- what value exists now,
- what risks remain,
- what a credible path to release looks like,
- what “success” means for each audience.

It is written to be useful in two common real-world contexts:
1) a recruiter skimming quickly, and
2) a synth enthusiast deciding whether to try it.

---

## 2. Executive narrative (what you can say in 30 seconds)

`midi_chip_platform` is a MIDI-controlled retro chip emulation platform. The MVP runs on macOS and can be driven from Logic Pro via an IAC bus on channel 3, producing SN76489-style audio output. The differentiator is not just that it makes chip sounds; it is that it is built like a small platform: single-file baseline for reviewability, clear specs and tests, an explicit backlog, and an honest hardware integration story (Pi Zero 2 USB MIDI gadget scripts) that is documented and traceable.

Validation boundary:
- Confirmed: macOS MVP + Logic/IAC ch3.
- Not claimed: Pi gadget verification.

---

## 3. The “market” context (who would care)

### 3.1 Musicians and producers

They care about:
- quick installation,
- stable routing,
- predictable note-off behavior,
- a sound that is distinct enough to justify the effort.

### 3.2 Makers and chip enthusiasts

They care about:
- authenticity and chip character,
- hackability (being able to see and modify the synthesis logic),
- hardware possibilities (running on a Pi).

### 3.3 Recruiters and engineering reviewers

They care about:
- integration across systems,
- debugging tools and instrumentation,
- clear constraints and trade-offs,
- traceability and documentation discipline.

The project is intentionally positioned at the intersection of these groups.

### 3.4 Primary user journeys (how value is actually experienced)

A business case is more concrete when it describes *how* someone gets value, not just that value exists.

**Journey A — “Hear something now” (confirmed macOS path)**

1) The user clones the repo and installs dependencies.  
2) They run `test basic` and confirm that audio output works at all.  
3) They run `midi list` to discover the OS-visible MIDI input ports.  
4) They run `monitor --midi-port "…" --midi-channel 3` and confirm that MIDI arrives (the routing layer works).  
5) They run `run` and play from a DAW (Logic Pro → IAC bus → channel 3).

Value delivered:
- immediate audible feedback,
- a predictable troubleshooting ladder,
- a demo path that a reviewer can reproduce.

**Journey B — “Tiny external instrument” (Pi path; pending verification)**

1) The user provisions a Pi Zero 2, runs the gadget script, and confirms the sanity script output.  
2) They verify macOS enumerates the Pi as a USB MIDI device.  
3) They route Logic Pro to the Pi destination and confirm MIDI reception (monitor on Pi).  
4) They confirm audio output on the Pi.

Value delivered (when verified):
- a physically separate instrument endpoint,
- a stronger narrative (“the laptop controls a tiny chip synth box”),
- a path toward gig-ready hardware.

Important boundary:
- This journey is intentionally described as *pending* until [E5F6G7H8](./BACKLOG.txt) is verified and recorded.

---

## 4. Value proposition (audience-specific)

### 4.1 Value for recruiters

This project demonstrates:

- **Systems thinking:** event-driven MIDI meets periodic audio callback; careful boundary design.
- **Pragmatic engineering:** build a demoable MVP first; defer accuracy mode.
- **Operational awareness:** monitor mode, PID printing, explicit port selection.
- **Governance:** stable artifact IDs, backlog UUIDs, and a baseline document that constrains the development surface.

In interviews, it supports concrete discussion topics:
- “How do you debug ‘silence’ in a MIDI/audio system?”
- “How do you keep callback workloads stable?”
- “Why single-file baseline, and how do you refactor later?”

### 4.2 Value for synth enthusiasts

- **Immediate sound:** `test basic` gives audible confirmation quickly.
- **DAW integration path:** documented and confirmed on macOS (Logic + IAC + ch3).
- **Hackable core:** single-file makes it easy to tinker.
- **Roadmap:** accuracy mode and additional chips are explicit milestones.

### 4.3 Value for contributors

- The repo is structured for contributions: stories/specs/tests exist.
- Backlog UUIDs give a lightweight but real traceability mechanism.

### 4.4 Value as a “product seed” (what could be monetized later)

This repo is not positioned as a commercial product today, but the business case is clearer if we articulate what *could* become product value later:

- **A reliable external instrument workflow:** “select port, select channel, play; no guessing.”
- **Curated presets/mappings:** chip-appropriate envelopes, noise modes, and DAW templates.
- **Packaged distribution:** a single installer/app reduces time-to-first-sound.

Important boundary:
- these are opportunities, not promises.

---

## 5. Differentiation (why it’s not “yet another emulator”)

### 5.1 DAW-centric design

Many chip emulators are UI-centric (keyboard input, menus). This project is **routing-centric**:
- explicit MIDI ports,
- explicit channels,
- monitor mode as a first-class tool.

### 5.2 Platform orientation

The goal is not “an SN76489 emulator,” but a platform that can host multiple chips and present a stable interface (CLI/config now; potentially plugin later).

### 5.3 Traceability and governed artifacts

A recruiter can map:
- discovery narrative → roadmap → user stories → functional spec → technical spec → test plan.

That is rare in hobby projects and valuable as a hiring signal.

### 5.4 Honest validation boundaries

Overclaiming kills credibility. This repo explicitly records what is confirmed and what is pending.

### 5.5 “Debuggability as UX” (a differentiator that matters)

In this domain, the user experience is dominated by failure recovery:
- why is there no sound?
- why are notes stuck?
- why can’t my DAW see the device?

The differentiator is therefore *not* an additional waveform; it is:
- a stable “triage ladder” (`test basic` → `monitor` → `run`),
- readable logs,
- explicit port selection.

That matters to enthusiasts (less frustration) and to recruiters (operational thinking).

---

## 6. Costs, constraints, and complexity drivers

### 6.1 Engineering complexity drivers

- **Audio callback discipline:** timing stability matters.
- **MIDI device variability:** ports, drivers, naming, virtual routing.
- **Hardware gadget integration:** Pi device enumeration is OS-level.

### 6.2 Direct costs

- Software: open source dependencies.
- Hardware (optional): Raspberry Pi Zero 2 and a correct data cable.

### 6.3 Constraint: MP-B-v2.3.0 single-file baseline

This is a deliberate trade:
- Pros: reviewability, onboarding speed.
- Cons: long-term modularity.

The business case accepts this because early-stage clarity is more valuable than architectural “purity.”

### 6.4 Assumptions and non-goals (business-facing)

The project is easier to evaluate if assumptions are explicit.

Assumptions:
- The MVP can be “instrument-like enough” without hard real-time guarantees.
- macOS remains a credible baseline demo environment because virtual MIDI routing (IAC) is available.
- Users will tolerate a CLI at the current stage if the debug workflow is clear and fast.

Non-goals (for MVP scope):
- competing directly with polished commercial plugins,
- cycle-perfect emulation,
- supporting every OS/device permutation without documented constraints.

### 6.5 Supportability and maintenance cost model (time, not money)

Because this is an open-source/portfolio-oriented project, “cost” is best modeled as *time-to-maintain* rather than dollars.

Main support cost drivers:
- **Environment variance:** different MIDI devices, port naming conventions, and DAW routing habits create a large state space.
- **Audio backend surprises:** default devices, permissions, and sample-rate mismatches can produce silence.
- **Hardware variance (Pi):** gadget mode adds additional failure modes (OTG port, UDC binding, cable quality).

Strategies that keep maintenance cost low:
- publish one **known-good path** (macOS + IAC + ch3) and make it the default demo,
- keep a strict “confirmed vs pending” boundary to prevent support expectations from outrunning reality,
- design tooling (monitor mode) that helps users self-diagnose rather than ask for help.

This is why the business case repeatedly frames debuggability as UX: it directly reduces support cost.

---

## 7. Risks (business-facing)

### 7.1 Risk: “accuracy expectation mismatch”

If a user expects cycle-perfect SN76489 behavior, they may be disappointed.

Mitigation:
- brand the MVP as a playable approximation,
- add accuracy mode to roadmap,
- document the difference in a future release.

### 7.2 Risk: “hardware story fails in practice”

If the Pi gadget path is unreliable, the “tiny instrument” narrative weakens.

Mitigation:
- keep the Pi story optional for MVP release,
- label the gadget path as pending until verified,
- focus on macOS path as the confirmed demo.

### 7.3 Risk: “silence = frustration”

If a user hits silence with no clue why, they quit.

Mitigation:
- require `test basic` and `monitor` as first-run tools,
- document layered debugging (audio → routing → channel).

### 7.4 Risk: “maintenance drift”

Docs can drift from code.

Mitigation:
- stable artifact suite,
- each behavior change requires doc update,
- keep CLI contract stable.

### 7.5 Risk register (expanded)

This is a more structured view of risks than the narrative above.

- R-BC-01: Dependency friction (audio/MIDI libs) blocks first-time users.
  - Impact: High (kills adoption)
  - Likelihood: Medium
  - Mitigation: keep install steps minimal; document known-good versions when established.

- R-BC-02: Platform variance (different MIDI port names and behaviors) creates support load.
  - Impact: Medium
  - Likelihood: High
  - Mitigation: monitor mode; explicit port selection; do not promise “works everywhere” until proven.

- R-BC-03: Pi gadget integration fails due to cable/OTG/UDC issues.
  - Impact: High
  - Likelihood: High (until verified)
  - Mitigation: keep gadget status pending; ship sanity scripts; treat as optional.
  - Backlog linkage: [E5F6G7H8](./BACKLOG.txt)

- R-BC-04: Users treat the project as a finished instrument and judge it harshly.
  - Impact: Medium
  - Likelihood: Medium
  - Mitigation: scope language; clear “MVP” labeling; honest roadmap.

---

## 8. Success metrics (how we know it’s delivering value)

### 8.1 MVP success metrics (confirmed path)

- A new user can hear sound quickly via `test basic`.
- Logic Pro can send MIDI via IAC on channel 3 and the runtime responds.
- Monitor mode makes routing observable.

### 8.2 Next success metrics (pending)

- Pi enumerates as USB MIDI device on macOS.
- Longer sessions are stable under recommended settings.
- A release tag can be cut with clear scope and known limitations.

### 8.3 Recruiter-facing success metrics

- A reviewer can understand the architecture in < 30 minutes.
- A reviewer can reproduce the demo without special hardware.
- Traceability is visible (backlog UUIDs referenced across docs).

### 8.4 “Time-to-first-sound” as the primary usability metric

This project’s most practical metric is not polyphony count; it is the *time-to-first-sound* for a new user.

What reduces time-to-first-sound:
- a single audible smoke test (`test basic`),
- a clear routing probe (`monitor`),
- a validated DAW path with a deterministic default (channel 3 on macOS IAC).

Important boundary:
- do not claim a numeric value (seconds/minutes) unless actually measured and recorded.

---

## 9. Roadmap section (business case → roadmap alignment)

The business value increases as the project moves from “demo” to “instrument-like reliability.”

- **M1 (macOS MVP)** delivers immediate demo value.
- **M2 (Pi gadget)** unlocks the “hardware instrument” narrative.
- **M3 (stability hardening)** increases trust and reduces support burden.
- **M4 (accuracy mode)** increases credibility in chip communities.
- **M5+ (multi-chip + packaging)** expands audience.

See: [RM-B-v0.01](./RM-B-v0.01.md).

---

## 10. Release and distribution options (what a “product” could become)

This section is intentionally speculative, but grounded.

### 10.1 Open-source instrument CLI

- Keep CLI + docs as primary interface.
- Pros: low maintenance; hacker-friendly.
- Cons: less accessible to non-technical musicians.

### 10.2 Standalone app

- Bundle Python and dependencies.
- Pros: easier install.
- Cons: packaging complexity.

### 10.3 Plugin wrapper (VST3/AU)

- Wrap the engine into a plugin host.
- Pros: best DAW UX.
- Cons: highest complexity; should be later.

The roadmap’s sequencing reflects this: stabilize the engine first.

### 10.4 Licensing and contribution model (practical notes)

Even a “portfolio-first” repo benefits from explicit expectations:
- prefer permissive OSS licensing if the goal is broad adoption,
- include a simple CONTRIBUTING guide if external contributions are desired,
- keep AI assistance disclosure consistent across artifacts.

This business case does not choose a license; it notes that license clarity increases trust.

---

## 11. Traceability (backlog and artifacts)

### 11.1 Backlog items
- [A1B2C3D4](./BACKLOG.txt) — SN76489 MVP: MIDI→Audio
- [E5F6G7H8](./BACKLOG.txt) — Pi Zero 2 USB-MIDI gadget

### 11.2 Artifact suite

- Discovery: [DR-B-v0.01](./DR-B-v0.01.md)
- User stories: [US-B-v0.01](./US-B-v0.01.md)
- Functional spec: [FS-B-v0.01](./FS-B-v0.01.md)
- Technical spec: [TS-B-v0.01](./TS-B-v0.01.md)
- Test plan: [TEST-B-v0.01](./TEST-B-v0.01.md)
- Release plan: [REL-B-v0.01](./REL-B-v0.01.md)
- Deploy plan: [DEPLOY-B-v0.01](./DEPLOY-B-v0.01.md)

---

## 12. Appendix: recruiter-friendly “talk track”

If asked “why did you build this?”

- “It’s a cross-domain systems project that is also musical. It proves MIDI routing, real-time-ish audio streaming, and disciplined docs.”

If asked “what’s the hardest part?”

- “Not the waveform; it’s the integration: MIDI ports, channel mapping, audio callback timing, and OS-level gadget configuration.”

If asked “what’s next?”

- “Verify the Pi gadget path, then harden stability and add accuracy mode.”

### 12.1 Alternate talk track (more product/UX oriented)

- “It’s a chip-synth tool that treats debugging as user experience. The first priority is: no mystery silence. The second is: chip character. The third is: optional accuracy.”

This helps a recruiter see the product mindset without pretending the repo is already a product.

---

## 13. Objections and responses (decision-ready business case)

This section is written as if a skeptical stakeholder is reviewing the project. It is useful both for “portfolio defense” and for deciding whether to invest further time.

### 13.1 Objection: “This is a toy; chip synths already exist.”

Response:
- The goal is not to compete with polished commercial plugins on features.
- The goal is to demonstrate *systems integration* and *debuggability* in a domain that is fun and demoable.
- Many existing tools hide the pipeline; this repo makes the pipeline explicit and traceable.

### 13.2 Objection: “Python can’t do real-time audio.”

Response:
- The MVP does not promise hard real-time guarantees.
- It uses buffering via an audio callback and keeps DSP simple and vectorized.
- The roadmap includes stability hardening before expanding features.

### 13.3 Objection: “If it isn’t chip-accurate, it’s pointless.”

Response:
- Musical value exists before perfect fidelity.
- Accuracy mode is explicitly planned as a milestone.
- The MVP is clearly labeled as a playable approximation.

### 13.4 Objection: “The hardware story will be fragile.”

Response:
- The Pi gadget path is treated as OS integration and documented as such.
- It is optional for the macOS MVP release path.
- Verification is pending and is clearly labeled to avoid credibility loss.

---

## 14. Alternatives and positioning (how this compares)

This section does not claim superiority; it clarifies trade-offs.

### 14.1 Alternative: commercial chip-synth plugins

Pros:
- best DAW UX
- stable distribution

Cons:
- not hackable
- less “engineering story” for recruiters

### 14.2 Alternative: classic emulators (game/console emulators)

Pros:
- potentially high fidelity

Cons:
- often not designed for DAW routing
- difficult automation/instrumentation

### 14.3 Alternative: hardware chip modules

Pros:
- authentic sound

Cons:
- hardware friction
- cost
- less accessible to casual users

Positioning:
- `midi_chip_platform` sits between these: approachable and hackable, with a credible integration story.

---

## 15. Roadmap section (value curve)

A useful way to judge the roadmap is to ask: “where does value increase sharply?”

- **M1 (confirmed):** immediate demo value on macOS.
- **M2 (pending):** major narrative uplift (“tiny external instrument”).
- **M3:** trust and usability (less friction, fewer failure modes).
- **M4:** credibility with chip accuracy expectations.
- **M5+:** broader musical usefulness and potential packaging.

This business case supports prioritizing M2/M3 before chasing new chips.

---

## 16. Go/No-go criteria (when to invest more time)

### Go criteria

- The macOS demo path remains reproducible.
- Docs stay aligned as code evolves.
- The Pi gadget path is either verified or clearly marked as experimental/pending.

### No-go criteria

- Frequent “silence” failures without diagnosable steps.
- A backlog that grows without being actionable.
- Overclaiming results (credibility damage).

### 16.1 Acceptance criteria (business-case-level)

These acceptance criteria help decide whether the project is ready for “public portfolio visibility” (e.g., sharing a link) *without* implying that everything is production-grade.

- AC-BC-01: The README, discovery report, and test plan agree on what is confirmed vs pending.
- AC-BC-02: A reviewer can follow a single path to reproduce sound on macOS.
- AC-BC-03: The CLI contract is documented and consistent across artifacts.
- AC-BC-04: Pi gadget support is clearly labeled as pending until verified (no ambiguous wording).
- AC-BC-05: Backlog UUIDs appear in artifacts and resolve to entries in [BACKLOG.txt](./BACKLOG.txt).

---

## 17. Appendix: portfolio framing (what to highlight)

If using this project in a CV/interview:

- Emphasize integration: MIDI routing + audio callback + OS gadget scripts.
- Emphasize observability: monitor mode, explicit port selection, reproducible tests.
- Emphasize governance: MP-B-v2.3.0 baseline, artifact suite, backlog UUIDs.
- Be explicit about what is confirmed vs pending.

### 17.1 FAQ (business case)

**Q: Is the Pi required to get value from the repo?**  
A: No. The confirmed macOS path is the primary demo. Pi is an optional lane.

**Q: Is this intended to become a plugin?**  
A: Not in the MVP. A plugin wrapper is a later distribution option after stability hardening.

**Q: Who is the “customer” right now?**  
A: Recruiters/reviewers and synth enthusiasts. The repo is optimized for learnability, demoability, and hackability.

**Q: What would make this a credible v1 release?**  
A: Stability hardening, documentation alignment, and a clearly scoped release note that does not overclaim.

### 17.2 Glossary (business framing)

- **Business case (here):** a reasoned argument for continued investment (time), not a revenue forecast.
- **Portfolio artifact:** a repo that demonstrates engineering behavior, not just a demo.
- **Instrument-like reliability:** predictable behavior under typical use, with documented failure recovery.

### 17.3 Example “first-run” script (macOS, confirmed path)

This is an *example command sequence* that illustrates the intended user experience. It is not a benchmark, and it does not claim Pi support.

1) Verify audio works:

- `python src/midi_platform.py test basic`

If this is silent, stop and fix the audio layer first (device selection, permissions, sample-rate issues).

2) Discover MIDI ports:

- `python src/midi_platform.py midi list`

3) Probe routing (observe MIDI arrival):

- `python src/midi_platform.py monitor --midi-port "<IAC bus name>" --midi-channel 3`

At this stage you should see readable messages. If you do not, the problem is routing, not synthesis.

4) Play:

- `python src/midi_platform.py run --midi-port "<IAC bus name>" --midi-channel 3`

This sequence is valuable in a business case because it operationalizes the “time-to-first-sound” goal.

### 17.4 Interview prompts (how this project becomes a conversation)

If you are presenting this as a portfolio artifact, useful prompts include:
- “Explain the layered debugging strategy for silence.”
- “Where would you add instrumentation to detect underruns without overengineering?”
- “How do you keep the CLI stable while refactoring the synth core?”
- “What are the risks of claiming hardware support too early, and how do you avoid it?”

These prompts connect directly to the repo’s differentiators: integration, observability, and honest boundaries.

### 17.5 Conservative release-note skeleton (scope-first)

If/when a public tag is cut, the release note should be short and honest:
- What is confirmed (macOS demo path, Logic/IAC ch3)
- What is explicitly pending (Pi gadget verification)
- What is intentionally out of scope (cycle-perfect emulation, plugin delivery)
- What changed since the previous tag (CLI flags, defaults, or behavior)

This avoids the most common portfolio/open-source failure mode: implied promises that turn into support obligations.

---

## 18. Credits

- Michiel Erasmus
- OSS libraries: `mido`, `python-rtmidi`, `numpy`, `sounddevice`
- Built with AI assistance as implementation support (not human authorship)

---

## 19. Changelog (BC-B-v0.01)

### 2026-04-06
- Expanded business framing, risk model, success metrics, and distribution options
- Added roadmap alignment section and recruiter talk track
- Added product-seed framing, explicit assumptions, structured risk register, and business-case acceptance criteria
- Preserved explicit validation boundary (macOS confirmed; Pi pending)
- Preserved artifact ID/version and backlog traceability links
