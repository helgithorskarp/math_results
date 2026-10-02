# Conditional original-tail copy occupancy

six-covering-1, researcher. Under the first720 stage hypotheses in
[proof.md](proof.md), every one of the five free tail copies needs at least
three original classes meeting the actual holes. Two-class copies reduce
to five support shapes, all excluded by compulsory first-stage capacity.
This is a construction restriction, with no new full covering or global
`L_min(8)` bound. Minimum **exactly eight** is the assigned parameter.

The occupancy consequence uses the separately published 99-hole theorem
at [stage720-four-hole-bound](../stage720-four-hole-bound/proof.md),
graph 9329/0. This directory independently computes the new sparse-copy
classification and five compulsory-complement exclusions, without replaying
that prerequisite. `certificate.json` contains every one of the 46 large-union
rows and every first resource-block maximum.

From the repository root, run the following sequentially:

```sh
python3 round-two/six-covering-1/stage720-tail-copy-occupancy/check.py
python3 -O round-two/six-covering-1/stage720-tail-copy-occupancy/check.py
python3 round-two/six-covering-1/stage720-tail-copy-occupancy/audit.py
python3 -O round-two/six-covering-1/stage720-tail-copy-occupancy/audit.py
python3 round-two/six-covering-1/stage720-tail-copy-occupancy/audit.py --sanitizers
```

Expected: 179 productive phase pairs, 46 large unions, 22 surviving tail assignments;
compulsory counts `[420,420,420,420,410]`, capacities
`[404,404,404,404,397]`; eight certificate damages rejected in each Python
mode. The C++ audit compares every tail row and all 73 original first blocks.
Its different modulo 144/modulo 5 core decomposition checks 414720 profile pairs,
whose orbit weights cover 10368000 original phase tuples. Sanitizers check
2160000 left phase-point incidences, 497664 right phase-point incidences,
120 orbit multiplicities. See [manifest.json](manifest.json) for exact
versions, validation commands and hashes.

Requirements: CPython 3.11.2, g++ 12.2.0, C++17, standard libraries only.
All jobs use one thread. Each author's validation had a 20-second outer
guard; the audit has 12-second compilation and 10-second execution guards.
Normal Python takes approximately 2--3 seconds; no large generated data or
solver proof is required. Temporary binaries are confined to ignored build/.
The public certificate is compact exact evidence, not a formal proof object.
Same-author separate-decomposition replay does not constitute independent
peer review. Timeout/incomplete enumeration cannot establish nonexistence.
