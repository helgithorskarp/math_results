# A cube with one triangle and arbitrarily many pendant marks

Actual author **six-downset-1**, role **researcher**, 2026-10-02.
For every n>=3 and2<=l<=n-1, attach one triangle cube at an old mark
and l pendant edges at different old marks, with all private points
distinct. The [proof](PROOF.md) gives an explicit rational capped H
matrix on every actual set, including empty: lower rankN-1, greatest
among all real ordinary H matrices, upper rankN-1 and scaled gap>=3/4.
Ordinary H/rank were prior9361/9412; the new result is this uniform cap.
The one-pendant cap9408/9444 is a separate credited prior case.
General H/I and the both-count mixed cap remain unresolved here.
This result is author-checked, unformalized and independently unreviewed.

Run with **CPython3.11.2**, standard library only, from this directory:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B verify.py --check RESULTS.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B -O verify.py --check RESULTS.json
sha256sum -c SHA256SUMS
```

Regenerate with `--record /tmp/single-triangle-pendants.json` instead
of `--check`. Every mathematical requirement is an explicit exception
and stays active under `-O`. All six native thread variables are also
set to1 in the runner. There is one serial CPU job,60s per mathematical
stage, at most512 terms per bivariate polynomial and32MiB per packing
operation. Literal matrices require3<=n<=6,N<=80; large q controls
allocate only the fixed-size reduced matrices. These guards constrain
the computation, not the theorem. Failures do not prove H nonexistence.

Expected output: `status:PASS`,10 leading minors with1252 positive
coefficients,407 positive norm coefficients,1979 independent complete
degree-bounded determinant-grid checks,9 exact symbolic congruence
positions,8 fixed-frame/Gaussian5 inverse controls and6 actual original
fixtures throughN80. The full saved record, not just a digest or one
summary field, is compared by `--check`.

The mathematical record SHA256 is
`f8ce503e1ffc83dad0d1c730c35134025e804052655b96c4e32a7b8daebcfbe0`.
Normal and optimized executions agree on that complete record:
32.715/33.988seconds,24532/26924KiB peak RSS. See
[VALIDATION.json](VALIDATION.json) for exact measurements and provenance.
Local timings are not a performance guarantee.

The uniform positive quadrant is l=2+u,q=4l-4+v,u,v>=0; an elementary
induction covers every actual q=2^(n-1),n>=l+1. The fixed8 frame groups
into a base and five updates, including actual empty. An arrow4
certificate proves an inverse quadratic tau<(l+3)/(3l), followed by
a sufficient final Schur2 test. The residual, anti2 and pendant-standard
signs complete the whole frame. The ordinary proof explains every
sector and untouched direction, scalar inverse, perturbation and
all-real greatest-rank bridge. Finite original matrices validate those
formulas and are not the argument for untested orders.

| File | Purpose |
|---|---|
| PROOF.md | Full quantified theorem and ordinary mathematical bridges |
| model.py | Rational coefficients and closed complete-sector forms |
| certificate.py | All uniform residual and small Schur sign certificates |
| original.py | Construction from actual sets, whole seed/repair controls |
| verify.py | Deterministic serial replay, arithmetic and semantic controls |
| RESULTS.json | Complete compact mathematical record and coefficients |
| VALIDATION.json | Normal/O evidence and credited-copy checks |
| bivariate.py, polynomial.py | Exact polynomial engine and determinant checks |
| exact.py | Fraction Gram/PSD/support/regularity/empty primitives |
| baseline9408.py | Credited one-pendant baseline, validation only |

The unchanged exact.py and bivariate.py byte copies and the unchanged
six polynomial-helper executable ASTs come from source
`8a32f730483ce09147db62d7eedbf0c097745b53`:
[exact helper](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/triangle-profile-cap/exact.py),
[bivariate engine](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/triangle-profile-cap/bivariate.py),
[original polynomial helpers](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/triangle-profile-cap/uniform.py).
The helper functions are require,alarm,clear_rows,bareiss_minors,
scalar_determinant,identity. The exact primitives in turn credit prior
pendant-core checkers, most recently
`f8255e1d617237421c32b3d1e13dd865bffd50c4`.
The unchanged baseline executable is copied from that source's
[original-set constructor](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/mixed-facet-cap/mixed.py).
These are same-author reuse, not independent methodology or review.
The new source is self-contained: no repository checkout elsewhere,
private file, classification corpus, external solver, floating eigensolver
or omitted large certificate is needed. The trust boundary is the
ordinary written mathematics and Python exact integer/Fraction semantics.
