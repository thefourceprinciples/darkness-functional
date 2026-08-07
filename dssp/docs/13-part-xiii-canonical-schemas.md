# Part XIII — Canonical Schemas

## 100. Observation object

```text
observation_id
source_id
instrument_id
timestamp
location_or_reference_frame
raw_data_pointer
normalized_data_pointer
units
calibration_version
environmental_state
selection_function
uncertainty_model
processing_history
data_class
access_status
integrity_hash
```

## 101. Model object

```text
model_id
model_name
model_class
assumptions
parameters
priors
nuisance_parameters
valid_domain
predicted_observables
background_components
falsification_conditions
software_version
source_provenance
integrity_hash
```

## 102. Residual object

```text
residual_id
run_id
observation_id
model_id
model_version
parameter_strategy
parameter_values
nuisance_values
covariance_id
raw_residual
whitened_residual
residual_metrics
feature_vector
topology
artifact_audit_id
background_audit_id
model_comparison_id
replication_links
contradiction_ids
uncertainty_debt_ids
darkness_classification
classification_version
prohibited_claims
next_test_ids
workflow_state
integrity_hash
```

## 103. Claim object

```text
claim_id
version
parent_claim_id
claim_text
claim_type
domain
scope
quantifiers
assumptions
evidence_level
engineering_level
epistemic_status
workflow_state
supporting_evidence_ids
contradicting_evidence_ids
dependency_claim_ids
uncertainty_profile
provenance_id
created_at
updated_at
integrity_hash
```

## 104. Candidate object

```text
candidate_id
candidate_name
candidate_family
ontology_class
theory_version
evidence_maturity
interface_maturity
proposed_mass_or_scale
lifetime
abundance_role
coupling_channels
portal_types
observable_channels
detector_classes
control_variables
predicted_responses
primary_backgrounds
model_dependencies
cross_checks
falsification_conditions
active_constraints
active_anomalies
contradictions
engineering_status
containment_status
stewardship_class
prohibited_claims
next_discriminating_tests
review_date
source_manifest
```

## 105. Experiment object

```text
experiment_id
experiment_type
candidate_id
claim_targets
apparatus_version
protocol_version
preregistration_id
input_channels
output_channels
null_channels
sham_channels
reversal_tests
environmental_monitors
authorized_envelope
current_state
active_stop_conditions
shutdown_plan
release_plan
integrity_hash
```

## 106. Gate object

```text
gate_id
gate_type
target_id
target_version
requested_transition
hard_predicates
soft_indicators
stop_conditions
predicate_results
missing_requirements
decision
restrictions
reviewers
timestamp
recheck_condition
integrity_hash
```

## 107. Stewardship object

```text
stewardship_id
target_object_id
target_version
requested_action
current_SQ_level
requested_SQ_level
non_distortion_status
load_fidelity_status
open_futures_status
clean_handoff_status
reversibility_status
containment_status
auditability_status
proportionality_status
lifecycle_status
dual_use_status
justice_status
release_status
risk_band
active_stop_conditions
restrictions
reviewers
decision
recheck_trigger
expiration
integrity_hash
```

---
