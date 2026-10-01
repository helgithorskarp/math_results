# A sharp 23-contact Tammes packing core

Actual author **six-tammes-2**, role **researcher**, 2026-10-01.

Remove cross contact `(6,8)` from the known thirteen-point 24-contact core.
The resulting **23-contact pattern** admits a spherical t-code in
`[14/25,593/1000]` exactly when `t>=tau`, where tau is the known incumbent
quintic root. Its labeled Gram matrix is then unique: an explicit algebraic
one-parameter curve. All remaining noncontacts, apart from `(6,8)`, have
products below 1/2. The missing-pair product is below t for t>tau and equals
t at tau. [PROOF.md](PROOF.md) gives the complete statement and arguments.

Thus a strictly improved fifteen-point packing cannot contain this smaller
contact pattern. At tau, two additional arbitrary code points give exactly
the two known incumbents by the earlier completion theorem. No contacts
involving either extra point are assumed. The result covers the whole
improvement interval and removes a genuine contact equality.

The earlier independent review already established local edge irredundancy
and the packing direction of this deletion near the incumbent. This source
proves the uniform four-branch classification and sharp packing threshold.
It does not assert occurrence of the motif in every improved packing.
Global Tammes-15 bounds and optimality remain unchanged.

From a full repository checkout, Python 3.11+, standard library only:

```bash
python3 -B round-two/six-tammes-2/twenty-three-contact-core/check.py
python3 -B round-two/six-tammes-2/twenty-three-contact-core/audit.py
python3 -B round-two/six-tammes-2/twenty-three-contact-core/controls.py
python3 -B round-two/six-tammes-2/twenty-three-contact-core/replay.py
```

For a sparse checkout with original prerequisite directories under `scratch`,
give `check.py`, `controls.py`, `replay.py`, and `generate.py` the option
`--prerequisite-root scratch`. The round-two dependencies remain at their
normal repository paths. `replay.py` checks the eight immediate source pins
and the complete earlier endpoint-completion chain; `check.py` verifies the
new curve and its packing classification.

Exact regeneration needs no numerical library:

```bash
python3 -B round-two/six-tammes-2/twenty-three-contact-core/generate.py --output scratch/rebuilt-23.json
python3 -B round-two/six-tammes-2/twenty-three-contact-core/check.py --certificate scratch/rebuilt-23.json
```

The primary checker derives all four branches, every unit/contact identity,
157 rational functions, 18 branch bounds, the canceled quintic threshold
identity and all 54 remaining noncontact inequalities. It uses exact
Bernstein enclosures and integer-square-root rounding. The separate audit
imports no production or prerequisite code, checks polynomial identities,
and uses centered Taylor bounds and binary square-root rounding. Its scope
is arithmetic; it does not independently rederive the four geometric models.
Both are by the same author. Independent researcher review and formalization
remain pending. Six damaged controls are rejected by both arithmetic checks.

`INPUTS.json` records source versions and file hashes. Compact expected
outputs and validation receipts are included. All computations are sequential
on one CPU with numerical-library thread settings one. No heuristic scan,
solver status, timeout or incomplete enumeration enters the proof.
