# RID closed rigidity across a Cauchy-area sign transition

six-rupert-3, researcher. [PROOF.md](PROOF.md) proves that every closed
scale-at-least-one fit at receivers in S=W union P is congruent, with
zero physical translation. W is the pinned prior receiving wedge set;
P contains all proper body images of normalized(s,t,1) and(t,s,1),
0<=s<=1/20,abs(t)<=s/2, with both signs and all boundaries. Arbitrary
source orientation and full proper planar roll are included. The x-major
cone crosses the actual Cauchy kink abs(t)/s=2-phi. Its seed
normalized(1/20,1/40,1) is outside all proper images of W.

The global standard rhombicosidodecahedron Rupert problem remains open.
Status: complete written intermediate proof with exact finite checks;
author-checked, unformalized, independently unreviewed. No priority claim.

Python3.11+ standard library, from repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-rupert-3/rid_cauchy_transition_cones/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B round-two/six-rupert-3/rid_cauchy_transition_cones/check.py
```

Both outputs must match the entire compact [expected.json](expected.json).
[DEPENDENCIES.json](DEPENDENCIES.json) pins the published prior W files.
The complete prior wedge, source filter, fivefold and brightness records
are replayed with all transitive source hashes before new comparisons.
The original facets, exact kink, receiving area/width budgets, actual
matching and exposed-face budgets, two minor-row refinement factors,
unsquared branch selection and separate source-area bounds are rechecked.
Eight new damaged controls reject. Affine and analytic estimates in the
written proof establish the continuum; no sampled search does so.

The only generated public evidence is a small deterministic exact record.
No external solver, numerical library, private ledger, key, raw corpus,
floating-search output or proof-assistant formalization is required.
