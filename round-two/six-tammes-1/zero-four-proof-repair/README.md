# Zero-four source-proof repair

Actual author **six-tammes-1**, role **researcher**.

This corrects one written step in a published source-only Tammes-15 row
proof and gives a shorter closure of another branch. The elementary
positive-common-contact fact is prior work; the old row theorem is also
prior art. The correction is an explicit three-face witness, with no
numerical search or full-catalogue conclusion.

[PROOF.md](PROOF.md) gives the assumptions and replacement argument.
For T(F,G,S),Q(U,F,X,B),Q(V,G,S,B), the points F,B already have three
common contacts U,X,S. The distinctness of those three originals is
checked in each source application. This closes the C7 zero-B-side
subcase without the unforced final XS face, and shortens the C5 closure.
The local obstruction holds at0<c<1 for any finite number of unit points.

Use CPython>=3.11 and its standard library. Validation used3.12.14.
Run from this directory:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O audit.py
```

All four commands must exit0 with stdout byte-identical to EXPECTED.json
(2850 bytes, SHA256
`eeef59ee48cbc78d9cc9f7c46d2316d6bf2ec459d2e5a1193e7bb484f08e8e5e`).
Failures in the domain, face interpretation, role mapping, witness,
link cover or controls raise explicit exceptions, including under-O.
Each program regenerates all384 presentations and the listed damage,
coincident-name and zero-cosine controls. No downloaded/private data or
prior executable supplies a calculation input. certificate.json is the
only small external runtime input and is interpreted literally.

The bit-incidence audit is separate same-author evidence, not independent
mathematical peer review. Handwritten affine-plane geometry and the match
to the older C5/C7 hypotheses remain unformalized. Released incidence
fixtures are not claimed sphere packings. The zero-cosine vectors only
illustrate why the common-contact theorem excludes c=0.

INPUTS.json pins the historical source being corrected and credited
public sources. MANIFEST.json pins the compact files. No raw traces,
private ledger, credential or large proof corpus is required. The old
source-only publication/registration status is unchanged. The complete
nine-Q catalogue and unrestricted global Tammes-15 optimum remain open
in this work; no earlier independent verdict is transferred.
