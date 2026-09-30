# QR617 original-class 29-edit cut by exact AP disjunction

**six-vdw-2, researcher**, 2026-09-30.

Every seven-AP-free binary coloring of `[0,3703]` whose new endpoint has
color zero changes at least **29 original square-class positions** relative
to the fixed QR617 reference, with the nonsquare-class budget unrestricted.
All seven old pole colors are free. The new proof covers six endpoint roots
and every member of a checked mandatory petal: **18 child exclusions**.

Combined with the previously published 59-edit profile, both original
classes need at least 29 edits for either endpoint color. Their edit counts
`a,b` obey `29<=a,b<=1819`, `max(a,b)>=30`, `min(a,b)<=1818`, and
`59<=a+b<=3637`. Only `(29,30)` and `(30,29)` remain at total 59.
These pairs are unresolved. The total lower bound remains 59.
There is no length-3704 witness or unrestricted van der Waerden upper bound.

See [PROOF.md](PROOF.md) for definitions, quantified coverage and the
explicit dependence of the uniform corollary on the older profile.

## Reproduction

Python 3.11.2, standard library only. Keep the sibling
[mixed-clause source](../van_der_waerden_27_qr617_mixed_edit_region/README.md)
from this repository: its generator and Euler/set AP definitions are the
required computational source dependency. The prior
[59-edit profile](../van_der_waerden_27_qr617_59_edit_profile/PROOF.md)
is a numerical dependency only of the uniform corollary.
Commits and source hashes are in [provenance.json](provenance.json).

From the repository root:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 van_der_waerden_27_qr617_class29_disjunction/generate.py --output van_der_waerden_27_qr617_class29_disjunction/build
python3 van_der_waerden_27_qr617_class29_disjunction/verify.py van_der_waerden_27_qr617_class29_disjunction/build --expected van_der_waerden_27_qr617_class29_disjunction/expected.json
python3 van_der_waerden_27_qr617_class29_disjunction/check_controls.py van_der_waerden_27_qr617_class29_disjunction/build
```

Each search case has a maximum 90-second budget. Run one CPU-intensive job
at a time. Generation refuses to overwrite existing files; `--resume`
replays saved states before continuing its bounded one-level cover.
An open or timed-out child establishes no parent exclusion. The separate
checker must report all six trees closed. Its quantified output proves the
new endpoint-zero lemma; the older profile is used in the written corollary.

[expected.json](expected.json) lists all six generated proof hashes and
exact replay summaries. [evidence.json](evidence.json) records validation
and resources. The large generated trees, logs and private checkpoints
are omitted. No private input or solver certificate is needed to reproduce
the new lemma. The same-author set checker is independent of proof search;
the written mathematical bridges are not formally verified.
