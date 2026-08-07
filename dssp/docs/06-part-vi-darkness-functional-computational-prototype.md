# Part VI — Darkness Functional Computational Prototype

## 26. Input contracts

Observation package:

observation_id

source_id

dataset_version

data and data class

coordinate system

units

timestamps

detector channels

calibration

environmental records

selection function

missing-data mask

quality flags

preprocessing history

uncertainty sources

integrity hash

Data classes remain visible:

REAL_OBSERVATION

SIMULATED_OBSERVATION

SYNTHETIC_INJECTION

SAFE_ANALOG_OBSERVATION

NULL_DATA

SHAM_DATA

REPLICATION_DATA

Model package:

model identity and version

model class

prediction function

parameters and bounds

nuisance parameters

priors or constraints

valid domain

predicted observables

background components

calibration dependencies

numerical dependencies

falsification conditions

Run manifest:

run identity

observation and model references

covariance strategy

parameter strategy

preprocessing version

software commit

random seed

numerical precision

analyst or agent

execution environment

preregistered hypotheses

execution time

## 27. Covariance architecture

C_total = C_stat + C_det + C_cal + C_env + C_bg + C_model + C_param + C_proc + C_shared

Where:

C_stat = statistical variation

C_det = detector response uncertainty

C_cal = calibration uncertainty

C_env = environmental covariance

C_bg = background uncertainty

C_model = model-form uncertainty

C_param = parameter uncertainty

C_proc = preprocessing uncertainty

C_shared = shared dependence across channels or datasets

The covariance engine tests:

- symmetry;
- dimensional and unit agreement;
- positive semidefiniteness;
- numerical conditioning;
- rank;
- regularization sensitivity;
- resampling stability;
- consistency with known detector behavior.

Critical covariance failures place the residual on HOLD.

## 28. Parameter strategies

Fixed-parameter residual:

r = y - M(theta_fixed, eta_fixed)

Profiled residual:

eta_hat(theta) = argmin_eta L(y | theta, eta)

r_profile(theta) = y - M(theta, eta_hat(theta))

Marginal prediction:

M_bar = Integral M(theta, eta) p(theta, eta | constraints) dtheta deta

The system records how much nuisance fitting absorbs the residual.

## 29. Residual features

Each residual receives a feature vector covering:

- normalized amplitude;
- spatial, spectral, or parameter localization;
- temporal persistence;
- frequency organization;
- cross-channel concordance;
- non-Gaussian or higher-order structure;
- nonstationarity;
- survival under model substitution;
- prospective predictive return;
- response to controlled variation where available.

Residual topology labels may include:

ISOLATED_EVENT

LOCAL_CLUSTER

TEMPORAL_DRIFT

PERIODIC_PATTERN

SPECTRAL_LINE

BROADBAND_EXCESS

SPATIAL_GRADIENT

CHANNEL_COMMON_MODE

BOUNDARY_EFFECT

HEAVY_TAIL

MULTIMODAL_STRUCTURE

UNKNOWN_TOPOLOGY

Topology is descriptive, not causal.

## 30. Artifact and background audit flow

Residual -> instrument audit -> calibration audit -> environmental audit -> preprocessing audit -> selection audit -> background audit -> dependency audit -> model audit -> institutional audit

The engine compares:

raw-domain result

processed-domain result

alternative-processing result

A feature appearing only after one opaque transformation is not robust.

## 31. Model basin

The candidate is evaluated against:

M_null

M_instrument

M_background

M_standard

M_modified

M_candidate_1

M_candidate_2

and other strongest reasonable alternatives.

Permitted tools include likelihood ratios, information criteria, posterior predictive checks, cross-validation, held-out prediction, simulation-based calibration, and residual diagnostics.

No single comparison method receives universal authority.

Prospective prediction receives greater advancement weight than retrospective accommodation.

## 32. Uncertainty debt

When an uncertainty cannot yet be resolved, it is recorded rather than set to zero.

Uncertainty debt contains:

- target object;
- uncertainty class;
- missing information;
- possible effect;
- severity;
- repair test;
- whether it blocks a gate;
- owner and status.

Severity:

LOW

MODERATE

HIGH

CRITICAL

Critical uncertainty debt blocks advancement.

## 33. Classification logic

Primary class and secondary pressures are reported together.

Examples:

D_U with elevated D_B pressure

D_F under model M1, but D_M under alternative model M2

D_A component removed; smaller residual remains D_U

D_N may never be assigned automatically by an opaque classifier.

Machine learning may identify unusual events, clusters, covariance shifts, waveform families, or out-of-distribution data. It cannot independently declare novelty.

## 34. Information efficiency

Early DSSP efficiency means validated information, not extracted power.

eta_I = validated information gain / energy input

A broader research metric is:

eta_R = validated reduction in uncertainty or parameter space / (energy + material burden + detector time + ecological burden + human risk)

This is a prioritization aid, not permission to ignore safety gates.

---
