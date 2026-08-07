# Part V — Gate Logic

## 21. Universal gate rule

A gate passes only when all mandatory predicates pass, no critical stop condition is active, and integrity remains valid.

PASS = all hard predicates true and no stop active

HOLD = information incomplete or materially unresolved

FAIL = one or more required propositions tested false

QUARANTINE = integrity, safety, provenance, or category failure requires restricted handling

PASS WITH RESTRICTIONS = mandatory predicates pass inside a narrower envelope than requested

Unknown defaults to HOLD, not PASS.

## 22. Scientific and engineering gates

G0 — Identity and provenance

Requires unique identity, source, version, creation process, processing history, integrity, access limitations, and conflict disclosure.

G1 — Observation integrity

Requires known instrument state, valid calibration, timing, units, reference frame, environmental record, acquisition history, selection rules, and preserved raw data.

G2 — Residual qualification

Requires a valid observation, specified model, valid domain, declared parameters and priors, nuisance treatment, covariance, background model, reproducible computation, and bounded residual language.

G3 — Replication

Requires materially independent data or apparatus, declared shared dependencies, independent analysis, predefined compatibility, inclusion of failed replications, and no exclusive dependence on the originating team.

G4 — Mechanism qualification

Requires a mathematically or causally specified mechanism, compatibility with established constraints, explanation of the residual, prospective prediction, mapped degeneracies, strong ordinary alternatives, and explicit falsification.

G5 — Interface qualification

Requires defined input, output, mediator or transfer relation, scaling law, backgrounds, null behavior, reversal or modulation behavior, detector sensitivity, and ordinary leakage pathways.

G6 — Controlled coupling

Requires deliberate intervention, randomized or blinded design where practical, negative null and sham channels, predicted scaling, reversal behavior, environmental and instrumental separation, repeated cycles, and independent replication path.

G7 — Reversibility

Requires defined start and stop conditions, measured shutdown and recovery, repeated start-stop cycles, hysteresis and delayed-effect assessment, stored-energy accounting, baseline restoration, independent shutdown, and no unexplained persistence.

G8 — Accounting closure

Requires electrical, magnetic, thermal, mechanical, chemical, radiation, cryogenic, material, momentum, and uncertainty accounting. Data-processing gain must not be represented as physical gain.

Accounting residual:

epsilon_E = E_out - E_in - E_stored + E_loss

An anomalous energy claim requires epsilon_E to remain inconsistent with zero after complete pathway and uncertainty accounting.

G9 — Containment

Requires spatial, temporal, energetic, exposure, propagation, shielding, failure-mode, shutdown, persistence, recovery, and monitoring boundaries.

G10 — Stewardship

Requires Non-Distortion, proportionality, lifecycle accounting, biological and environmental restraint, dual-use analysis, independent oversight, clean handoff, open futures, and release planning.

G11 — Application

Requires a defined function, performance metric, comparison baseline, measured benefit, known failure behavior, operator requirements, maintenance, calibration stability, safety, and containment during use.

G12 — Scale

Requires earlier gates to remain valid at proposed scale, empirically qualified scaling law, nonlinear transition assessment, supply-chain and waste review, governance, rollback, and monitoring that scales with deployment.

G13 — Release and decommissioning

Requires safe shutdown, stored-energy disposition, hazardous-material resolution, bounded persistence, raw-data archive, corrected claims, assigned responsibility, documented hardware disposition, knowledge handoff, and long-term monitoring where needed.

## 23. Automatic rollback

If a prerequisite claim becomes REFUTED, QUARANTINED, or materially UNDERCUT, every dependent object enters REVIEW_REQUIRED.

Example:

Calibration fails -> measurement reviewed -> residual reviewed -> mechanism reviewed -> interface and application claims reviewed

Downstream claims are not necessarily universally refuted. They lose active qualification until rebuilt from valid evidence.

## 24. Contradiction ledger

Contradictions are recorded as:

DIRECT_REBUTTAL

ASSUMPTION_CONFLICT

PARAMETER_CONFLICT

SCOPE_CONFLICT

CALIBRATION_CONFLICT

MODEL_DEGENERACY

REPLICATION_FAILURE

SAFETY_CONFLICT

GOVERNANCE_CONFLICT

APPARENT_ONLY

Contradictions are not averaged away.

The system asks:

- Can both claims hold under different scopes?
- Does one depend on a failed assumption?
- Are the datasets independent?
- Is one claim more precisely bounded?
- What experiment discriminates between them?
- Must both remain unresolved?

## 25. Quarantine classes

Integrity quarantine:
Broken provenance, fabricated or duplicated evidence, undocumented modification, hidden exclusion, or inaccessible critical source.

Epistemic quarantine:
Simulation presented as observation, analogy as discovery, residual as identified matter, correlation as control, or control as transduction without accounting.

Experimental quarantine:
Unexplained persistence, uncontrolled propagation, unauthorized parameter increase, failed independent shutdown, unexpected biological or environmental response, or open critical accounting.

Governance quarantine:
Suppressed adverse findings, bypassed review, concealed dual use, unauthorized commercialization, or scale beyond the approved envelope.

Quarantined objects are preserved, not deleted.

---
