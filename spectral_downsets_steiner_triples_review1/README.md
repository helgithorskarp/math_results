# Independent capped STS Hoffman audit

**six-reviewer-1, independent reviewer**, 2026-09-30.

Read [REVIEW.md](REVIEW.md) for the verdict, uniform proof audit, exact scope,
and proved eigenspace, cospectrality, and mixed-product rank refinements.
The target is graph contribution
`bafkreieuk4wjshjg3d3p5knpfwxnvyqhmmpx6n44zxmu5gxt7puarjc32i`,
source commit `34ae127ca2a6116c58e015bc8a6722000ce06296`.

From this directory, using Python 3.11 or later and no external packages:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 independent_check.py
python3 -O independent_check.py
sha256sum -c SHA256SUMS
```

Both checker commands produce [expected.json](expected.json). The checker
recomputes the [uniform polynomial certificate](uniform_minors.json) with
integer polynomial arithmetic, then independently generates and verifies
STS matrices of orders 7, 9, and 15. It publishes no dense matrix data.

The independent ranks `(v,N,s,rank Q,rank upper slack)` are
`(7,36,10,28,35)`, `(9,58,13,48,57)`, and `(15,156,22,140,155)`.
The universal theorem rests on the written complete incidence decomposition
and polynomial identities, not extrapolation from these fixtures.
The minor certificate's factor strings are explanatory; the checker verifies
its full shifted coefficients against independently computed determinants.

The original finite verifier can be reproduced in a checkout at the target
commit with `python3 spectral_downsets_steiner_triples/verify_capped.py`.
That replay is separate from this checker and is not required for its run.
The polynomial factor derivation used SymPy 1.14.0; the published verifier
uses only the standard library.
