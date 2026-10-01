# Degree-nine first power in a wider complex-center tube

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.

For a disk-root degree-nine polynomial with critical multiplicities
6+1+1 and equal light distances from a marked root a, let q be the
nonzero short center of the two unit light reciprocals after rotating
a positive. The first-power inequality, interior strictness and unique
binomial boundary equality hold when

    |q-1|^2 <= (1-|a|)/40000^2.

There is no heavy-direction or distance-order restriction. This
square-root width strictly enlarges the earlier linear width
(1-|a|)/80000. It is sufficient, not claimed sharp. The unrestricted
6+1+1 and degree-nine first-power questions remain open here.

The [proof](PROOF.md) uses a new antisymmetric double-integral estimate
for the three heavy moments. The phase-dependent norm loss is bounded
by 18000 sqrt(1-b)|q-1|+32000|q-1|^2, preserving half of the credited
reflected-origin surplus. It also corrects an antipodal illustrative
example in the previous source. The previous origin lemma and sector
theorem are unaffected. [Literature and dependencies](LITERATURE.md)
state all imported mathematics and the precise correction.

Reproduce the compact exact evidence using Python 3.11 or later,
standard library only:

```bash
python3 -I -B sendov_degree9_square_root_center_first_power/verify.py
python3 -I -B -O sendov_degree9_square_root_center_first_power/verify.py
```

Both commands reconstruct every stored record in [expected.json](expected.json).
They check the full generic skew/variation coefficient identities,
antisymmetrized weight integrals, sixth-power telescoping identity,
all rational constants, exact Gaussian moment and tube controls, one
actual nonreal disk-root polynomial beyond the old tube and heavy
cone, its complete derivative and marked root, and exact centered
Rouche bounds. A zero-sum pair and an incorrect purported center are
explicitly rejected as mathematical controls. Altered compact records
are rejected through exceptions active under optimization.

This is an ordinary analytic author proof, unformalized and
independently unreviewed. The finite controls are sanity checks;
they do not establish universal estimates. The written analytic proof,
classical complex analysis and the credited reflected-origin/polar
premises remain outside the checker. No large tensor, external data,
solver or floating-point optimum is a premise.
