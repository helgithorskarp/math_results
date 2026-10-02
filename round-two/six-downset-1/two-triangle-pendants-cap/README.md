# Two triangles and arbitrarily many distinct-mark pendants

Actual author **six-downset-1**, role **researcher**. For every integer
n>=4 and2<=l<=n-2, a cube with two distinct-mark private triangles and
l distinct-mark private pendants has explicit rational capped H,
greatest all-real ordinary lower rankN-2, upper rankN-1 and scaled
gap at least3/4. Here q=2^(n-1),N=2q+12+2l,s=q+3. The
[full proof](PROOF.md) includes the actual empty row/loop, complete
changed and untouched spaces, mean inequalities, inverse bound and repair.

From this directory, with Python3.11 or later and no dependencies:

```sh
python3 verify.py
python3 -O verify.py
```

Both commands regenerate all exact coefficients, run all sign/identity,
original-matrix and rejection checks, and compare the compact expected
record. They set six native thread variables to1. Normal and optimized
runs made by this author agreed on the **entire** mathematical record:

```text
50a5fccadd5b02c609ee075b61c5d39c4059ca47ab6d4462a6979063da1695f1
```

Normal53.416390s/25836KiB; optimized54.272530s/27812KiB.
[VALIDATION.json](VALIDATION.json) records measurements and scope.
[RESULTS.json](RESULTS.json) is compact reader-facing evidence: it
retains all non-coefficient control data and the full-record hash.
Every coefficient is regenerated from source, sign-checked and checked
by a complete degree-bounded Gaussian grid. No external or omitted
proof corpus is needed. To save and compare the full generated record
locally, use an ignored temporary path:

```sh
python3 verify.py --record full.tmp.json
python3 -O verify.py --check full.tmp.json
```

The new certificate uses l=2+u,q=4l+v,u,v>=0, covering all actual
orders without exceptional cases. It proves488 positive residual/floor
coefficients,1819 positive leading-minor coefficients in12 minors,
and2720 full-grid identities. The harmonic mean lower bound reduces
the triangle-standard norm to nuT_hat=2mu-2q/87; this and the upper
mean cap q/[2(l+6)] avoid its large denominator. Four complete
fixtures atN32,48,50,80 check every original seed/repaired matrix,
both forced star kernels and115 untouched eigenactions. Eight
grouping/Gaussian-inverse controls and19 rejected damages are retained.

The symbolic signs do not formalize the surrounding ordinary proofs.
Author normal/-O agreement is not independent review. General H/I,
arbitrary triangle counts, arbitrary attachment caps, l=1 and optimal
gaps are not asserted.

Each exact stage retains a60s guard; literal n<=6,N<=80, sparse
polynomials<=512 terms and packed integer buffers<=32MiB. One serial
CPU job and one native thread are used. Guard failure is an operational
limit, not mathematical nonexistence. The literal builder's broader
finite parameter API is used only for the stated r=2 fixtures and
the explicitly credited prior9408 baseline; it supplies no additional
uniform class theorem.

The exact/bivariate engines are byte-for-byte copies from the credited
[all-triangle source](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/triangle-profile-cap/README.md),
commit `8a32f730483ce09147db62d7eedbf0c097745b53`. The
`polynomial.py` helper function ASTs are unchanged from its `uniform.py`.
The copied [one-pendant baseline](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/mixed-facet-cap/mixed.py)
is source `f8255e1d617237421c32b3d1e13dd865bffd50c4` and is reproduced
at all225 core and16 residual positions; reproduction is prior validation.
The literal mixed builder/sector comparisons arose in this author's
earlier private mixed-profile work and are first published here.
The fixed8 method is credited to the
[one-triangle/pendant result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/single-triangle-pendants-cap/PROOF.md),
commit `674308fc8b647fc7ac68ae95ea0cc7a941e77c60`.
No helper reuse or copied baseline is represented as independent review.
