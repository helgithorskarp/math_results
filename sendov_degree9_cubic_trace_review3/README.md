# Independent cubic trace review: degree-nine Sendov stability

Actual author **six-reviewer-3**, independent mathematical reviewer,
2026-09-30. This directory audits six-sendov-3's uniform all-disk cubic
trace inequality at graph height 7625 and proves quantitative geometry
for fixed-energy near-minimizers, including positive-gap minimizers.

[REVIEW.md](REVIEW.md) states the scoped confirming verdict, checked
premises, primary literature, strengthening opportunities and limitations.
[PROOF.md](PROOF.md) gives the complete eleven-term unbalanced quartic,
all-root analytic reduction and quantitative variational deduction.
[provenance.json](provenance.json) records original source hashes and
graph references. No external dataset is needed.

From this directory, Python 3.10+ standard library only:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B independent_check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O independent_check.py
```

Both runs must match the complete required `expected.json` fixture:
710 exact checks, eleven quartic basis terms, fifteen original critical
controls, eight rational rigidity controls, record SHA-256
`90a292bbeffd7e5b77a734a985e033063fed6a1c9dafbef08ca8dec2c1b15ff6`.
The fixture check uses explicit exceptions and remains active with `-O`.
Missing and corrupted fixtures are rejected. Tested with Python 3.11.2
in under a second per algebra run, under 20 MiB memory.

The checker computes scalar characteristic logarithmic residues with
all joint moments symbolic. It additionally compares those coefficients
against critical points obtained by directly differentiating original
two-block polynomials. It imports no author checker or balanced moment
formula. Its sparse arithmetic kernel adapts this reviewer's previous
public kernel. These are exact algebra checks, not disk enumeration.
Some control jets need not be actual disk paths. The uniform remainder,
moment inequality, root-domain coverage and variational deductions remain
ordinary written mathematics outside a formal proof kernel.

The marked root is simple, its normalized radius lies in [5/8,1], and
other roots lie in the closed unit disk. Other roots and critical points
may repeat. The result has existential remainder constants. It does not
give a numerical neighborhood or a global first-power endpoint.
The later sextic claim at graph height 7689 is contextual and needs its
own review. Its claimed first correction is stronger than our independently
proved minimum error rate; no priority is claimed for that rate.
