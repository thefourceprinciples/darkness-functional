# Part II — Core Definitions and the Darkness Functional

## 5. Observation, explanation, residual

Observation:
A detector output, astronomical measurement, event record, spectrum, image, field reading, time series, or other registered result with preserved provenance.

Explanation:
A model-generated expectation conditioned on assumptions, physical parameters, nuisance parameters, calibration, backgrounds, selection effects, and valid domain.

Residual:
The difference between an observation and a specified explanatory construction.

r_k = y_obs - M_k(theta, eta)

Where:

- y_obs is the observed data;
- M_k is explanatory model k;
- theta contains physical parameters;
- eta contains nuisance, detector, foreground, calibration, and background parameters.

A residual is always model-indexed.

There is no model-independent residual.

## 6. Darkness Functional

The conceptual form is:

D = Observed - Explained

The operational form is a family of residual and qualification operators.

For covariance C_k:

D_k = C_k^(-1/2) r_k

This is the whitened or covariance-normalized residual.

A compact global burden may be written:

Q_D,k = (r_k^T C_k^(-1) r_k) / nu_k

Where nu_k is the effective number of degrees of freedom.

Neither D_k nor Q_D,k establishes new physics. They quantify disagreement between data and a declared model under a declared uncertainty construction.

The computational Darkness Functional includes:

D_raw = raw observation-model remainder

D_white = covariance-normalized remainder

D_local = localized structure

D_spectral = frequency-domain structure

D_temporal = persistence and nonstationarity

D_cross = cross-channel relation

D_model = survival across a model basin

D_predictive = prospective informational return

## 7. Darkness classes

D_A — Artifact darkness

Residual dominated by instrumentation, software, reconstruction, storage, filtering, or processing.

D_B — Background darkness

Residual produced by a real ordinary physical process that resembles the target.

D_M — Model darkness

Observation remains valid, but the explanatory model is incomplete, rigid, incorrectly parameterized, or used outside its domain.

D_S — Statistical darkness

Residual remains compatible with fluctuation, search multiplicity, sparse samples, selection, or unstable inference.

D_I — Institutional darkness

Evidence is distorted or rendered unrecoverable through hidden exclusions, broken provenance, authority pressure, inaccessible data, publication bias, or undocumented intervention. This is a parallel integrity classification and does not identify the physical source.

D_U — Unresolved darkness

A legitimate remainder exists, but current evidence cannot reliably assign it to another class.

D_F — Fertile darkness

A structured residual survives major removal attempts, recurs, remains coherent under changed conditions, and generates discriminating tests or successful predictions. It is productive unresolved information, not automatically new physics.

D_N — Novelty candidate

A residual has survived qualified replication, strong ordinary alternatives, model-basin comparison, and prospective prediction sufficiently to justify a new physical mechanism as a serious candidate.

D_N != confirmed discovery

## 8. False-darkness decomposition

Conceptually:

D_raw = D_target + D_background + D_artifact + D_model + D_statistical + D_corruption + D_unresolved

The task is not to subtract aggressively until nothing remains. The task is to remove only what can be reproduced and justified while preserving uncertainty and the possibility of mixed causes.

Qualified remainder:

D_qualified = D_raw - reproduced artifacts - qualified backgrounds - corrected model insufficiency - expected statistical variation

What survives may remain D_U, become D_F, or later qualify as D_N.

## 9. Non-promotion laws

NP-1: Residual non-identity

Residual(O, M) does not imply Entity(X).

NP-2: Significance non-causality

Significant(X, Y) does not imply X causes Y.

NP-3: Repetition non-independence

Repeated analyses of one dependency chain are not independent replication.

NP-4: Explanation non-uniqueness

A model that fits does not establish uniqueness.

NP-5: Control non-ontology

Controlling an apparatus response does not establish the preferred interpretation of that response.

NP-6: Function non-safety

A functioning device does not establish containment, safety, or stewardship.

NP-7: Discovery non-ownership

Discovery does not confer unrestricted ownership or extraction rights.

NP-8: Scale non-linearity

Behavior at one scale does not establish behavior at another.

NP-9: Absence non-negation

Failure to detect a candidate in one region does not establish universal absence.

NP-10: Unknown non-zero

Missing uncertainty, background, or risk information does not equal zero uncertainty, zero background, or zero risk.

---
