# The Tammes-15 three-five T/Q branch is empty

Actual author **six-tammes-1**, role **researcher**, 2026-10-01.

[PROOF.md](PROOF.md) excludes three degree-five vertices in a complete
connected fifteen-point contact graph with degrees3/4/5, nine quadrilateral
faces and simple strictly convex hemispherical T/Q sphere cells, for
**1/2<c<3/5**, where c is the cosine of the minimum angular separation.
The new geometric proof covers zero, one and two four-T fives; the
[earlier all-four-T case](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/three-ordinary-fives/PROOF.md)
is an explicit dependency. With the preceding degree bound, **at most two
threes and two fives remain**. The new deficient-five proof is complete
ordinary author mathematics, pending independent review and formalization.
It does not establish a new global separation bound or optimizer coverage.

All nineteen triangle-census cases are covered. Three-neighbor incidence
and actual face links leave only two local patterns, with36 and12 labeled
entries. One forces an impossible ordinary-five/ordinary-four opposite Q
corner equality; the other forces two non-three deficient-four QQ ends
when only one remains. Every unknown point is an original, and neither
role renaming nor link reversal assumes metric symmetry.

The committed21-profile beta catalogue loses all eleven r3 rows, leaving
**10 r2 necessary profiles**. A separate later18-profile public source
leaves **7 r2 profiles**, under its additional hypotheses. These statements
retain their separate provenance. Counts are not realized embedded maps.
[PROFILE_CONTEXT.json](PROFILE_CONTEXT.json) freezes the two prior lists;
[SOURCE_CONTEXT.md](SOURCE_CONTEXT.md) specifies dependencies and source
status. The new geometric exclusion uses neither list nor a beta premise.

From this directory, with CPython3.11+ and its standard library:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
mkdir -p scratch/reproduction
timeout 55s python3 -B check.py > scratch/reproduction/check.json
cmp EXPECTED.json scratch/reproduction/check.json
timeout 55s python3 -B -O check.py > scratch/reproduction/check-O.json
cmp EXPECTED.json scratch/reproduction/check-O.json
timeout 55s python3 -B audit.py > scratch/reproduction/audit.json
cmp AUDIT_EXPECTED.json scratch/reproduction/audit.json
timeout 55s python3 -B -O audit.py > scratch/reproduction/audit-O.json
cmp AUDIT_EXPECTED.json scratch/reproduction/audit-O.json
sha256sum -c SHA256SUMS
```

The primary output SHA256 is
`fc326be148fbfc5b404a1b39280def5ef294ca26a7d84c67b8c1c5046da74451`;
the audit output SHA256 is
`60505ebf7995c7b3b3ece1b5afbe40638ad3fc8bf3d49e52911a356cec47b1ba`.
These are full file hashes including the final newline. Each normal/-O
pair is byte identical. Four sequential runs on CPython3.11.2 took
0.38--1.11seconds, with maximum observed process RSS23,604KiB,
threads one and fixed55-second per-child guards. Measurements need not
reproduce exactly; no operational failure entered the proof.

[check.py](check.py) generates30,451 ordered U-neighbor triples over all
nineteen censuses. [audit.py](audit.py) imports no primary code and uses
supplier subsets, bit incidence and Hamiltonian cyclic links. All nineteen
admitted-row and terminal-row hashes match, as do both families' complete
terminal classifications and prefix hashes. Their raw domains differ:
the audit does not regenerate raw rows violating the initial QQ/common-
contact bounds. It independently audits proper original H-fan aliases,
four F-fan alignments and all possible original fourth neighbors of sealed
links. The continuous sphere/face/link and coverage bridges are written
proofs. These same-author programs are not independent mathematical review.

Nonempty released triangle ceilings, opposite-role tests and QQ budgets
are local surrogate controls, not spherical packings. No floating signs,
solver, CAS, network, coordinate data or large certificate is needed at
runtime. Expected outputs are receipts, not proof inputs. The fixture is
used only to verify the conditional catalogue deletions; the prior list
derivations are imported, not regenerated. Larger faces, lower degrees,
isolated vertices and the remaining r2 branch are unresolved here.
