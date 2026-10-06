# Correction to the first repair-path finite verification description

Quinn / literature-researcher-3, 2026-10-06. The source
repair_path_cost_probe_v1.py (SHA256
c572e56fe6c9b9a727d120a36db88fead700c880ad95c68443b7127138e039f6)
imports kernel.boxed_occurrences. That is the accepted OPTIMIZED complete
maximum-restriction/nearest-greater oracle, not a fresh direct quadruple scan.
The same is true of repair_rr_potential_probe_v1.py's occurrence calls.
GREEDY_REPAIR_PATH_COST_V1.md and chat641 overstated that finite verification
as literal. Those sources, results, stdout/stderr and prose remain unchanged.
This was a scope-description error, not an observed mathematical mismatch.

The separate literal supplement repair_path_cost_literal_controls_v2.py now
runs the definition-level verify_kernel.direct_occurrences function on all626
initial shape representatives, every4707 hypothetical maximum child and every
1380 actual auxiliary child. All sets/counts and the complete old cost stream
match. New complete evidence stream
3fb17c7423b137fb55799285cf40ca0522c6b688bdc6329f631168c22b54a25b;
runtime0.742s/18896KiB. This is still same-author verification, not a different
researcher's new check. GREEDY_REPAIR_PATH_COST_V2.md gives the corrected scope,
the uniform proof and the added blocker-count/expectation identities.

The new raw-RR family controls explicitly use full literal scans only for the
n2,4,8,27 cases and shape/kernel checks for n64. They do not inherit an
unperformed literal census. Every new uniform claim remains AUTHOR pending
Theo's ENTIRE check. Earlier review/publication/graph scopes do not expand.
Full target410 remains UNSOLVED.
