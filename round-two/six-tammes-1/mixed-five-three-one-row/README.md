# A mixed-five Tammes-15 count row is impossible

Actual author **six-tammes-1**, role **researcher**, 2026-10-01.

[PROOF.md](PROOF.md) excludes the complete convex hemispherical triangle/
quadrilateral contact-map row
`(r,a,b,f0,f1,f2,O)=(2,3,1,1,1,0,7)` on `1/2<cos(d)<3/5`.
There are two threes, one four-triangle five, one three-triangle five,
three one-triangle fours, one zero-triangle four and seven two-triangle
fours. Both contacting and noncontacting fives are covered.
This is an exact computer-assisted author proof; independent researcher
review and formalization are pending. It is a conditional contact-row
exclusion, not an unconditional Tammes-15 numerical bound or optimizer
classification. The geometrical bridges are written in the proof.

Use **CPython3.12.14**, standard library only. Run sequentially, with one
native thread and one mathematical job:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 check.py
python3 -O check.py
python3 audit.py
python3 -O audit.py
python3 controls.py
python3 -O controls.py
```

Each command checks its entire compact expected output and exits nonzero
on a mismatch or uncovered case. No floating arithmetic, solver, external
runtime input, random seed, coordinate table or network is required.
The author used a fixed55-second guard for each run, unchanged one-CPU/
2GiB scope; [VALIDATION.json](VALIDATION.json) records actual costs.
A guard failure is incomplete evidence, never a nonexistence certificate.

[patch.py](patch.py) implements necessary local face/link constraints.
[check.py](check.py) regenerates all covers. [audit.py](audit.py) imports
no primary code and uses bit masks, directed face boundaries and recursive
link walks. It separately regenerates supplier sets and canonical slots,
while sharing the written geometry and forced-face specification.
Both are by the same author. [controls.py](controls.py) supplies positive
partial-incidence fixtures, damaged incidences and a predicate-release
control with exactly two remaining necessary patches; these are not
asserted sphere packings.

The checks retain every original label for every unknown quadrilateral
opposite. Ordinary-role renaming is a naming convention on actual distinct
originals, with an explicit injection proof, never an assumed isometry.
[EXPECTED.json](EXPECTED.json) contains the complete report: 42 necessary
supplier pairs, 5,544 collars, nine paired-fan cases and 20,907 local patch
tests. The two implementations agree on every admission bit and admitted
intermediate tuple. Canonical local-case SHA256:

`edced34501840ef605e136571a0a678174b0b1605c62470b0b61a78131e413bd`.

[CONTROLS_EXPECTED.json](CONTROLS_EXPECTED.json) records the released-rule
result. [DEPENDENCIES.json](DEPENDENCIES.json) records credited geometry,
prior committed sources, qualified catalogue corollaries and review scope.
[SHA256SUMS](SHA256SUMS) identifies the compact source files. Exhaustive
case traces and exploratory data are regenerated locally and omitted.
