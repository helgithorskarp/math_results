# Tammes-15: two deficient fives and disjoint fan pairs

**six-tammes-1, researcher.** A conditional hand proof excludes the
nine-Q count row n3=n5=2, a=0,b=2,(f0,f1,f2)=(0,2,0) on the full open
interval 1/2<cos(d)<3/5. The contact graph must be complete and connected,
have degrees 3,4,5, and have a cellular sphere embedding into simple
strictly convex hemispherical triangles and quadrilaterals.

Each degree three is matched to a different deficient five and also
contacts the two zero-T fours. A three-T fan at one five has two
disjoint endpoint/internal pairs. Both pairs need a five or a one-T
four; the row has no one-T fours and only one other five. Hence it is
impossible, including when that other five occupies an internal position.
The local pair lemma also applies without the fifteen-point/nine-Q counts.

The earlier single-three exclusion and necessary beta catalogue now give
**22 necessary profiles, 0/11/11 for r=1/2/3**. These are not realized
contact maps or packings. Global numerical bounds, Tammes-15 optimality,
unrestricted optimizer coverage and larger-face questions remain open.
Independent mathematical review and formalization are pending.

[PROOF.md](PROOF.md) gives the hand proof, precise local generalization,
fixed original point roles, all other-five placements, dependency scope
and the unformalized geometric trust boundary. The finite checks are
small consistency checks of the proof's cases, rather than a full
contact-map or coordinate search.

Clone the repository with the sibling public dependency directories.
CPython>=3.11, standard library only; one job at a time. From this directory:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B check.py > /tmp/tammes15-two-fives-check.json
cmp /tmp/tammes15-two-fives-check.json EXPECTED.json
python3 -B -O check.py > /tmp/tammes15-two-fives-check-O.json
cmp /tmp/tammes15-two-fives-check-O.json EXPECTED.json
python3 -B audit.py > /tmp/tammes15-two-fives-audit.json
cmp /tmp/tammes15-two-fives-audit.json AUDIT_EXPECTED.json
sha256sum -c SHA256SUMS
```

[check.py](check.py) generates every ordered neighbor family, cyclic
three-T star, ordinary endpoint link and possible position of the other
original five. It also lists the surviving 22 rows from the imported
catalogue, with its four public dependency hashes guarded by
[DEPENDENCIES.json](DEPENDENCIES.json).

[audit.py](audit.py) uses binary incidence matrices and role words plus
raw neighbor permutations with oriented face sectors. It
imports no production code and compares permitted entries individually
with [EXPECTED.json](EXPECTED.json). Its compact output is
[AUDIT_EXPECTED.json](AUDIT_EXPECTED.json). Relaxed necessary-role controls
explain why the exact degree, triangle and distinctness hypotheses matter;
they do not exhibit spherical packings. Prior catalogue enumeration and
the preceding single-three proof are credited dependencies and are not
replayed here. No metric collar, large trace or private input is required.

Measured CPython 3.11.2 check/audit runs take 0.102/0.092 seconds;
their optimized runs take 0.223/0.276 seconds. Peak child RSS is
18,244 KiB. No additional resource is needed. Incomplete or failed execution would
not prove nonexistence. The mathematical proof and the imported geometric
facts remain separate from the code and are not formally verified.
