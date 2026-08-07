# Part IV — Claim Calculus and State Machines

## 13. Core object classes

SRC = source or provenance object

OBS = observation object

MOD = explanatory model object

RES = residual object

CLM = claim object

EVD = evidence object

CND = candidate mechanism or interface object

EXP = experiment object

GAT = gate evaluation object

REV = review object

STW = stewardship object

DEC = decision object

REL = typed relation between objects

Every object receives:

- immutable identifier;
- type;
- creation time;
- creator or generating process;
- version and parent version;
- workflow state;
- provenance pointer;
- integrity hash;
- access class;
- append-only change history.

## 14. Claim structure

A claim contains:

claim_id

proposition

claim_type

domain

scope

quantifiers and tolerances

assumptions

supporting evidence

contradicting or undercutting evidence

uncertainty profile

evidence level

engineering level

workflow state

version

Claims should be atomic.

Invalid compound claim:

The detector observed dark matter, demonstrated a new force, and can generate unlimited clean energy.

Required decomposition:

1. An unusual detector event occurred.
2. The event remains after qualified background subtraction.
3. A defined mechanism explains it.
4. Deliberate intervention controls it.
5. Energy conversion occurs with closed accounting.
6. The device performs a useful function.
7. The device is safe and fit to scale.

Each proposition requires a separate claim object and evidence path.

## 15. Claim types

CLM-OBS = observation claim

CLM-MET = calibrated measurement claim

CLM-RES = residual claim

CLM-SYS = systematic or artifact claim

CLM-REP = replication claim

CLM-HYP = hypothesis claim

CLM-MOD = model claim

CLM-MEC = mechanism claim

CLM-INT = interface claim

CLM-CTL = controlled-coupling claim

CLM-TRN = transduction claim

CLM-CON = containment claim

CLM-APP = application claim

CLM-SAFE = safety claim

CLM-STEW = stewardship claim

CLM-GOV = governance claim

No CLM-HYP or CLM-MOD may be represented as CLM-MEC without mechanism qualification.

No CLM-MEC may become CLM-CTL without intervention evidence.

No CLM-CTL may become CLM-TRN without closed accounting.

No CLM-APP may be represented as safe merely because it functions.

## 16. Typed relations

Supports:

e supports claim c

Rebuts:

e supports the material falsity of c

Undercuts:

e weakens the inference by challenging an assumption, calibration, model, or method

Refines:

claim c2 narrows c1

Generalizes:

claim c2 extends c1 and requires new evidence

Predicts:

model m predicts observation o

Causally produces:

controlled intervention x produces response y under a qualified design

Supersedes:

claim c2 replaces c1 for active use while preserving c1 historically

Depends on:

claim c1 loses active qualification if prerequisite c2 fails

## 17. Epistemic and workflow states

Epistemic states:

UNASSESSED

SUPPORTED

PROVISIONAL

CONTESTED

UNDERCUT

REFUTED

SUPERSEDED

UNRESOLVED

Workflow states:

DRAFT

REGISTERED

PROVENANCE_CHECK

QUALIFICATION

ACTIVE_REVIEW

GATE_HOLD

GATE_PASSED

QUARANTINED

ROLLED_BACK

RETIRED

ARCHIVED

Truth status and workflow state remain separate.

A claim may be supported yet remain on gate hold because safety, replication, or stewardship is incomplete.

## 18. Candidate state coordinates

Every candidate has two independent coordinates:

Evidence coordinate E:

E0 = raw signal

E1 = validated observation

E2 = reproducible residual

E3 = cross-channel structure

E4 = candidate mechanism

E5 = source-backed physical claim

E6 = strong physical fact

Engineering coordinate X:

X0 = observation only

X1 = correlated response

X2 = controlled coupling

X3 = reversible coupling

X4 = transduction

X5 = containment

X6 = qualified application

X7 = stewardship-qualified scaling

Example:

(E4, X0) means a scientifically credible mechanism with no controlled interface.

(E2, X2) means a controllable laboratory response whose ontology remains unresolved.

The second state demands special restraint.

Control does not settle interpretation.

## 19. Experiment lifecycle

CONCEPT

DESIGN

SIMULATION

ANALOG_QUALIFICATION

PRE_REGISTRATION

SAFETY_REVIEW

APPARATUS_QUALIFICATION

CALIBRATION

BLINDED_RUN

UNBLINDING

ANALYSIS

REPLICATION

CONTAINMENT_TEST

APPLICATION_TEST

SCALE_REVIEW

RELEASE

DECOMMISSIONED

Exceptional states:

HOLD

FAILED

QUARANTINED

ABORTED

ROLLED_BACK

INCIDENT_REVIEW

## 20. Event-sourced audit law

Every material action creates an append-only event:

OBJECT_CREATED

VERSION_CREATED

SOURCE_ATTACHED

EVIDENCE_ATTACHED

CONTRADICTION_ADDED

STATE_CHANGE_REQUESTED

GATE_EVALUATED

ADVANCEMENT_APPROVED

ADVANCEMENT_DENIED

ROLLBACK_TRIGGERED

QUARANTINE_TRIGGERED

QUARANTINE_LIFTED

CLAIM_REFINED

CLAIM_REFUTED

EXPERIMENT_ABORTED

RELEASE_COMPLETED

Current state is reconstructed from event history.

No material state change occurs through silent overwrite.

---
