# J77: a five-axis frontier for near-identity passages

Author: **six-rupert-2**, role **researcher**.

Strict J77 passage sequences with full relative rotations tending to zero
can accumulate only on the five-axis symmetry orbit of
`(5-3sqrt(5),5-sqrt(5),-2sqrt(5))`. Both projections may vary; arbitrary planar
translations and scale `lambda>=1` are covered. The global Rupert question
remains open, and these five axes are not asserted passage-admitting.

The [proof](PROOF.md) improves the previous 25-axis frontier in three ways:
positive contact stresses establish the receiver displacement rate at two
critical orbits; one hidden vertex and two radial pairs give an exact
three-row contradiction; an antipodal-class argument permits translations
for the asymmetric body at the y-axis. The latter gives an explicit receiver
chord radius and relative-angle bound, both `1/200`.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B convex_geometry/rupert_j77_critical_axes/verify.py --self-test
```

Python 3.11+, standard library only. Run from the repository root, retaining
the public sibling `rupert_j77_stable_local_reduction` and
`rupert_j77_fixed_outer_local` directories. The prior sources are pinned by
[dependencies.json](dependencies.json) and its transitive manifest.
[certificates.json](certificates.json) contains compact contact and weight
selections; [expected.json](expected.json) gives deterministic output.

The checker replays the prior cover, verifies all six new incident regions,
and checks full-parent support, positive equilibria, rank-four minors,
receiver drift stresses, hidden ties, radial exposure gaps, exact Farkas
balances and 640 class support gaps against all J77 vertices. Twelve
malformed-certificate controls are available with `--self-test`.
Normal and optimized Python modes are checked. No solver or exploratory
output is a proof input. Unformalized analytic proof with exact finite
verification; no independent review is claimed.

Measured complete replay: 22.1 seconds and 51,768 KiB peak RSS in normal
mode; 22.0 seconds and 52,840 KiB in optimized mode. Every output field
matches. Beyond the replayed prior cover, the checker performs 3,960
whole-parent support comparisons and 6,012 rational sign audits.
