# Four-triangle/two-triangle pair of fives

Actual author **six-tammes-1**, role **researcher**, 2026-10-01.

[PROOF.md](PROOF.md) excludes the nine-Q row `r=2,a=2,b=1,f=(1,0,1)`
throughout the full open interval `1/2<c<3/5`. The hypotheses are fifteen
actual distinct unit points and their complete connected degree3..5
contact graph, with a cellular minor-geodesic sphere embedding into
simple strictly convex hemispherical triangle/quadrilateral faces.
The proof closes all twelve ordered three-neighbor pairs and their four
equal-role families. It also supplies a local shared-opposite obstruction,
including the possibility that the ordinary point is a five-fan endpoint.
The geometric and original-face bridges are written proofs; independent
mathematical review and formalization remain pending.

Removing exactly this row from the checked source catalogue gives
**19 beta profiles, split0/8/11 for r=1/2/3**. The preceding20-profile
[source](../tammes15_two_one_triangle_fours_exclusion/PROOF.md), verified
commit `71535b1c836995acfe9b6f6bef3727b97af82c09`, has a rejected original
graph package and is not graph-committed. This directory is a source
publication; no new graph submission or commitment is asserted. The last
actually committed cover remains21 profiles at graph h8360, source
`8e69194e595ae7411d3624537473870f67ff79c8`. The rejected registration is
preserved in the private checkpoint and has not been retried or stripped
of known relations. Global numerical Tammes15 bounds and optimality
remain unchanged.

From this directory, with CPython3.11 or newer and only its standard
library:

```sh
python3 -B check.py > /tmp/tammes15-four-two-check.json
cmp /tmp/tammes15-four-two-check.json EXPECTED.json
python3 -B -O check.py > /tmp/tammes15-four-two-check-O.json
cmp /tmp/tammes15-four-two-check-O.json EXPECTED.json
python3 -B audit.py > /tmp/tammes15-four-two-audit.json
cmp /tmp/tammes15-four-two-audit.json AUDIT_EXPECTED.json
python3 -B -O audit.py > /tmp/tammes15-four-two-audit-O.json
cmp /tmp/tammes15-four-two-audit-O.json AUDIT_EXPECTED.json
sha256sum -c SHA256SUMS
```

[check.py](check.py) uses cyclic neighbor words and actual-original face
sets. [audit.py](audit.py) imports no production code; it rebuilds the
entries using binary vertex/edge incidences, role permutations and
Hamiltonian edge sets. Both compare all entries, rather than only counts.
They cover12 ordered neighbor pairs,24 single-three and12 double-three
G stars,12 F/G shared stars,450 original-alias opposite frames, nine C3
cases, two final five-contact lists at D, and14 C4 endpoint alias entries.
Released-quota/diagonal controls are nonempty abstract necessary
assignments, not spherical packings.

[DEPENDENCIES.json](DEPENDENCIES.json) guards seven previously published
proof/catalogue files by SHA256. The20-profile source catalogue is
imported and exactly one row is removed; it is not regenerated. No private
input, solver, floating-point sign, metric collar or exhaustive packing
corpus is used. [EXPECTED.json](EXPECTED.json) and
[AUDIT_EXPECTED.json](AUDIT_EXPECTED.json) contain the compact outputs.

Recorded CPython3.11.2 checks: production normal/-O 0.073/0.181s,
separate audit normal/-O 0.075/0.18s; maximum child RSS
19724KiB. Each has a45s outer guard.
All four exact outputs agree with their recorded files.

Runs use one local job at a time and one native/BLAS/OpenMP thread, within
the existing1CPU/2GiB researcher scope. These local finite checks support the conditional hand proof.
Unrestricted optimizer occurrence and complete contact-map enumeration
remain open.
The credited classical and prior campaign facts are distinguished from
the new row proof in PROOF.md.
