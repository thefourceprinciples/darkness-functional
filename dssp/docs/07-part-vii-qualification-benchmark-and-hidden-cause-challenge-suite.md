# Part VII — Qualification Benchmark and Hidden-Cause Challenge Suite

## 35. Qualification purpose

DSSP must earn the right to classify unknowns by first classifying known hidden causes under blinded conditions.

The benchmark evaluates:

Detection capacity:
Can genuine structure be recovered?

Rejection capacity:
Can artifacts, backgrounds, noise, and corruption be rejected?

Restraint capacity:
Can D_U or D_F be preserved when D_N is not justified?

Recovery capacity:
Can dependent claims roll back when later evidence breaks the story?

The correct answer is the strongest conclusion justified by visible evidence, not the hidden truth known to the benchmark designer.

An accidentally correct but unsupported novelty claim scores worse than a disciplined D_U classification.

## 36. Benchmark governance

Benchmark Architect designs cases.

Truth Custodian maintains the sealed answer key.

Data Fabricator generates synthetic or physical injections.

Analysis Team receives only visible data and metadata.

Adversarial Team attempts to fool the pipeline.

Independent Scoring Team compares submissions with the truth vault.

Stewardship Reviewer evaluates whether recommended actions remain proportionate and safe.

## 37. Ground-truth families

T0 = no injected structure

T1 = statistical fluctuation

T2 = instrument artifact

T3 = calibration failure

T4 = environmental background

T5 = known physical background

T6 = preprocessing artifact

T7 = selection artifact

T8 = model insufficiency

T9 = genuine weak signal

T10 = genuine strong signal

T11 = multiple degenerate causes

T12 = shared-dependency pseudo-replication

T13 = corrupted provenance

T14 = genuine unresolved structure

T15 = safe analog controlled coupling

T16 = controlled ordinary leakage

T17 = prospective prediction success

T18 = prospective prediction failure

T19 = unexplained persistence

T20 = mixed or compound cause

## 38. Challenge families

Family A — Null and statistical controls

Pure noise, correlated noise, heavy tails, look-elsewhere traps, optional stopping, sparse samples.

Family B — Artifact and calibration challenges

Gain drift, cross-talk, timing offset, saturation, dead-channel interpolation, maintenance-state artifact, firmware boundary, calibration contamination, unit mismatch, hidden baseline subtraction.

Family C — Background and environmental challenges

Temperature, RF interference, vibration, radon, cosmic rays, neutrinos, mixed backgrounds, delayed environmental coupling, common-site background, unresolved ordinary source.

Family D — Model and covariance challenges

Missing terms, invalid domain, over-flexible models, prior dominance, singular covariance, missing off-diagonal covariance, excessive uncertainty inflation, nonstationarity, simulation-real mismatch, competing ordinary models.

Family E — Replication and dependency challenges

Duplicate data, shared calibration, shared software, shared site, analyst dependence, partial replication, failed replication, shifted parameters, predicted-channel null, genuine independent replication.

Family F — Hidden signal and fertile-darkness challenges

Weak localized injection, stable periodic signal, multi-channel injection, signal plus artifact, degenerate mechanisms, prospective success or failure, hidden analog coupling, structured mechanismless residual, D_N threshold case.

Family G — Adversarial integrity and stewardship challenges

Mislabeled simulation, deleted null runs, selective covariance, changed hypotheses, fabricated replication, authority pressure, commercial urgency, safety override, hidden biological exposure, concealed dual use.

## 39. Difficulty levels

Level 0 = transparent implementation test

Level 1 = routine diagnostic case

Level 2 = confounded case

Level 3 = adversarial false-discovery bait

Level 4 = deep ambiguity where HOLD is correct

Level 5 = cross-domain synthesis requiring technical and governance integration

## 40. Benchmark outputs

Every case returns:

NO_QUALIFIED_RESIDUAL

D_A

D_B

D_M

D_S

D_I_PARALLEL

D_U

D_F

D_N_CANDIDATE

COMPOUND_CLASSIFICATION

QUARANTINE

and one gate outcome:

PASS

PASS_WITH_RESTRICTIONS

HOLD

FAIL

QUARANTINE

## 41. Scoring

Core scoring vector:

classification quality

claim-scope accuracy

provenance handling

covariance treatment

replication independence

restraint

predictive-test quality

rollback quality

stewardship compliance

report auditability

Recommended scale:

0 = critical failure

1 = major failure

2 = weak

3 = minimum acceptable

4 = strong

5 = exemplary

Critical floors cannot be averaged away.

Catastrophic errors include:

- simulated data declared a physical discovery;
- artifact promoted to novelty after its pathway was available;
- duplicate data counted as independent replication;
- active safety stop ignored;
- unexplained persistence followed by increased power;
- open energy ledger described as generation;
- unauthorized biological exposure;
- deleted nulls omitted after detection;
- D_N converted into discovery or resource language without later gates.

## 42. Qualification bands

Q0 = unqualified

Q1 = schema-qualified

Q2 = residual-qualified

Q3 = adversarially qualified

Q4 = analog-qualified

Q5 = research-qualified

Q6 = interface-support qualified

No qualification band authorizes autonomous discovery or scale decisions.

---
