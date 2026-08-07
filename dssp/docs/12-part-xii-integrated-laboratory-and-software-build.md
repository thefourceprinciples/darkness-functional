# Part XII — Integrated Laboratory and Software Build

## 95. Functional laboratory architecture

A future DSSP laboratory contains:

Zone A — Source and Calibration Vault

Zone B — Clean Assembly and Materials Screening

Zone C — Safe Analog Test Hall

Zone D — Low-Background Detector Hall

Zone E — Modular Candidate Interface Chamber

Zone F — Independent Null Channel

Zone G — Control and Observation Room

Zone H — Shutdown and Recovery System

Zone I — Immutable Data Mirror and Provenance Archive

Zone J — Stewardship Review Chamber

The central apparatus is called an interface chamber, not a containment vessel, unless containment has actually been demonstrated.

## 96. Minimum experimental packet

No physical DSSP experiment begins without:

1. Claim card.
2. Candidate interface card.
3. Apparatus diagram.
4. Input-output ledger.
5. Background model.
6. Null design.
7. Sham design.
8. Reversal test.
9. Randomization protocol.
10. Blinding protocol.
11. Environmental monitor list.
12. Calibration plan.
13. Shutdown and persistence test.
14. Exposure envelope.
15. Containment assessment.
16. Lifecycle and waste plan.
17. Dual-use assessment.
18. Independent replication package.
19. DMRC review packet.
20. Phase V stewardship review.
21. Phase VI release plan.

## 97. Consolidated repository

```text
 dark-sector-stewardship/
 |
 |-- README.md
 |-- DSSP_MASTER_PACKET_v1.0.md
 |-- STEWARDSHIP_CONSTITUTION.md
 |-- CLAIM_LABELS.md
 |
 |-- core/
 |   |-- identifiers.py
 |   |-- claims.py
 |   |-- evidence.py
 |   |-- relations.py
 |   |-- observations.py
 |   |-- models.py
 |   |-- residuals.py
 |   |-- uncertainty.py
 |   |-- provenance.py
 |   |-- contradictions.py
 |   |-- states.py
 |   |-- transitions.py
 |   `-- advancement.py
 |
 |-- darkness_functional/
 |   |-- intake.py
 |   |-- normalization.py
 |   |-- parameters.py
 |   |-- covariance.py
 |   |-- whitening.py
 |   |-- features.py
 |   |-- topology.py
 |   |-- classification.py
 |   `-- reporting.py
 |
 |-- gates/
 |   |-- provenance_gate.py
 |   |-- observation_gate.py
 |   |-- residual_gate.py
 |   |-- replication_gate.py
 |   |-- mechanism_gate.py
 |   |-- interface_gate.py
 |   |-- coupling_gate.py
 |   |-- reversibility_gate.py
 |   |-- accounting_gate.py
 |   |-- containment_gate.py
 |   |-- stewardship_gate.py
 |   |-- application_gate.py
 |   |-- scale_gate.py
 |   `-- release_gate.py
 |
 |-- model_basin/
 |   |-- null_models/
 |   |-- background_models/
 |   |-- standard_models/
 |   |-- cosmology/
 |   |-- particle_candidates/
 |   |-- hidden_sectors/
 |   `-- modified_gravity/
 |
 |-- atlas/
 |   |-- candidates/
 |   |-- interfaces/
 |   |-- detectors/
 |   |-- backgrounds/
 |   |-- hazards/
 |   `-- falsification_tests/
 |
 |-- false_darkness/
 |   |-- taxonomy/
 |   |-- diagnostics/
 |   |-- counterfeit/
 |   |-- repair/
 |   `-- regression/
 |
 |-- benchmarks/
 |   |-- generators/
 |   |-- suites/
 |   |-- truth_vault/
 |   |-- blind/
 |   |-- scoring/
 |   `-- reports/
 |
 |-- safe_analog_lab/
 |   |-- apparatus/
 |   |-- hidden_states/
 |   |-- control/
 |   |-- accounting/
 |   |-- blind/
 |   |-- qualification/
 |   `-- reports/
 |
 |-- stewardship/
 |   |-- integrity/
 |   |-- load/
 |   |-- risk/
 |   |-- governance/
 |   |-- futures/
 |   |-- handoff/
 |   `-- release/
 |
 |-- dmrc/
 |   |-- packets/
 |   |-- anonymous_reviews/
 |   |-- minority_reports/
 |   |-- disagreements/
 |   `-- decisions/
 |
 |-- data/
 |   |-- raw/
 |   |-- normalized/
 |   |-- public/
 |   |-- synthetic/
 |   `-- manifests/
 |
 `-- ui/
     |-- residual_map/
     |-- candidate_atlas/
     |-- claim_ledger/
     |-- contradiction_view/
     |-- stewardship_gate/
     `-- release_dashboard/
```

## 98. Minimum viable software build

The first executable system must support:

- typed claims and versioning;
- evidence attachment;
- support, rebuttal, undercutting, refinement, and dependency relations;
- evidence and engineering coordinates;
- workflow-state transitions;
- gate evaluation;
- PASS, HOLD, FAIL, and QUARANTINE;
- contradiction logging;
- dependency rollback;
- stop-condition enforcement;
- append-only event history;
- observation and model packages;
- covariance validation;
- residual construction and whitening;
- artifact and background checklists;
- model-basin comparison;
- D_A through D_F classification;
- D_N lockout until qualification conditions are supplied;
- benchmark generation and blind submission lock;
- stewardship restrictions;
- exportable DMRC and release packets.

## 99. Integrated build sequence

Phase 0 — Packet and schema foundation

- finalize master packet;
- implement identifiers, objects, states, and manifests;
- create claim, residual, candidate, experiment, gate, and stewardship schemas.

Phase 1 — Linear residual engine

- simple known models;
- covariance validation;
- raw and whitened residuals;
- deterministic reports.

Phase 2 — Time-series and multi-channel engine

- drift;
- periodicity;
- colored noise;
- nonstationarity;
- common-mode dependence;
- cross-channel analysis.

Phase 3 — False-darkness and benchmark suite

- artifact generators;
- background generators;
- corruption cases;
- blind truth vault;
- scoring and rollback tests.

Phase 4 — Safe Analog Laboratory

- oscillator bench;
- resonator bench;
- thermal-memory bench;
- distributed-sensor bench;
- AQ0-AQ5 qualification.

Phase 5 — Candidate Interface Atlas

- first fifty candidate cards;
- cross-interface maps;
- falsification routes;
- current evidence and interface coordinates;
- stewardship restrictions.

Phase 6 — DMRC and Stewardship Engine

- anonymous review packets;
- minority reports;
- restrictions;
- incident records;
- handoff and release objects.

Phase 7 — Qualified public-data demonstrations

- select public datasets;
- preregister model basin;
- publish complete residual and contradiction reports;
- no physical novelty claim unless gates independently pass.

---
