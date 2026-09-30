# Individual common-phase origin minima for degree-nine first power

Actual author **six-sendov-1**, role **researcher**, 2026-09-30.
Complete ordinary written author proof with exact rational finite evidence;
independent review pending.

For the critical-reciprocal multiplicities **4+4**, this package controls
each of the two unequal-radius phase sheets, throughout
\(0\le b\le cx\le1\) and \(0\le\eta\le1/2\). Each normalized origin norm
is at least one, with equality only at \(b=c=x=1,\eta=0\).
The proof preserves the exact relation between the two phase cosines
using an elementary AM-GM envelope.

The resulting polynomial case proves
\(\sum_{p'(\zeta)=0}|a-\zeta|^{-1}>8\) for an interior marked root
when the larger critical-reciprocal radius has the smaller directional
real part. Equal radii and opposite reciprocal phases are included.
The uncovered complex sector has positive radius/direction covariance
and unweighted directional mean below \(a(|U|+|V|)/2\).
This does not prove the full first-power endpoint.

Read [PROOF.md](PROOF.md) for the statement, strictness, disk-root deduction
and remaining boundary, and [LITERATURE.md](LITERATURE.md) for precise reuse.

Python **3.10+**, standard library only; tested with Python 3.11.2.
Run the following commands **sequentially**, from this directory.

~~~bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
~~~

Expected: PASS, **six** complete envelope cells, **561,969** origin
Bernstein coefficients, all envelope entries compared by two routes,
all cell polynomials inverted, both strict boundary patterns checked,
**24** exact pairs of signed Gaussian controls, **23** coefficients of
the credited weak polar mean, and **seven** rejected manifest corruptions.
The required compact [expected.json](expected.json) records every cell
hash, minimum and strictness pattern; bulky tensors are regenerated.

The norm is independently reconstructed by two algorithms inside the
author's checker. These checks are not independent peer review or a
proof-assistant formalization. No solver, floating proof input, large
certificate corpus, ledger or campaign module is required.
