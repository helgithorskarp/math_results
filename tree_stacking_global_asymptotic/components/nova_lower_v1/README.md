# Statement B: eventual all-order lower component

Nova / studio-researcher-3, researcher, 2026-10-05. Shared task17.
Author component for Rowan's independent internal check. This directory is
reproducible source, presently a private exact-version handoff. Publication
and the combined global theorem await the team's accepted frozen inputs.

PROOF.md audits the inherited R construction and supplies the explicit
lower bound log2 M(n)>=(5/36)n^2-(5/4)n for every integer n>=37.
It uses primary tree-stacking/score theorems and reconstructs the sufficient
redistribution construction. The converse equality classification is a
separate inherited obligation for the global upper bound. The R-family,
parameters and restricted leading exponent are prior art and stably cited.

Reproduce the bounded exact controls with CPython3.11 or later, stdlib only:

    PYTHONDONTWRITEBYTECODE=1 python3 check_lower.py > RESULT.rerun.json

The mathematical record is identified by deterministic_record_sha256;
timing/platform fields may differ. RESULT.json is the author's completed
run, not an internal-check report. All eighteen order residues are tested
for five finite parameter values, with six extra boundary/eligibility
controls. The infinite range follows from the ordinary proof and exact
identities, not from these finite samples. Inputs/source hashes and exact
primary import scopes are recorded in INPUTS.json and PROOF.md.

No solver, NetworkX dependency, random search, expanded census or predecessor
module/output import is required. The runtime uses one process and exact
integer/Fraction decisions; timing is separate. Code does not decide
arbitrary pebbling reachability by raw move enumeration. Rowan should
independently reconstruct the relevant proof, inputs and any exact controls
used in the check, and state the actual accepted scope and defects.
