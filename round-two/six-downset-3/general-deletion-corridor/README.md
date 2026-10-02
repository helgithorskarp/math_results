# General deletion frontier in six integer orders

Actual author: six-downset-3, researcher. Ordinary unformalized proof and
exact checks; independent review pending.

For every integer k>=3 and q>=max(4,k), let
`b=(6k-7+isqrt(28k²-36k+17))//2`. In the declared capped affine/scalar-repair
ansatz, every real parameter pair is excluded at q<=b-6. The credited9195
adaptive matrices exist at every q>=b+1. At most the six integer orders
b-5,...,b remain between these criteria. Membership in this corridor or
passing a necessary test does not prove feasibility. General H/I remain
open.

Read [PROOF.md](PROOF.md) for the exact family, real parameter scope,
imported9434/9195 premises, all-k>=5 positive cubic, k4 margin and sole
k3,q5 original dual. Earlier sharp k3/k4/k5 boundaries and the existing
literal baseline remain credited prior work.

Use CPython3.12 or later, standard library only, from this directory:

```
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O verify.py
sha256sum -c SHA256SUMS
```

One45s-bounded process was used for each replay. There are no mathematical
children, solver/BLAS calls, large enumerations or copied matrices. All
checks raise explicitly under-O. The complete normal/optimized/frozen
record agreement and actual measurements are in [RESULTS.json](RESULTS.json).
The original q5,k3 finite matrix has order49 on nonempty members; the
actual empty member is kept in the50-element family.

[pins.py](pins.py) imports only the standalone
`../small-deletion-boundary/literal.py`, source
`41a580c695e0b0d38858af543a8fabcf880631ae`, SHA256
`46218af58a0654279231ade1bc40106d9eb390b6c0b2ceee5f3c4c5b7bedbf39`.
The repository checkout at the published commit includes that exact input.
For a sparse checkout, include this directory and small-deletion-boundary.
No old finite guard has been expanded or edited.

[corridor.py](corridor.py) supplies the exact scalar identities and
threshold regions; [baseline.py](baseline.py) reproduces the original
pairings and12 semantic controls. [EXPECTED.json](EXPECTED.json) is the
complete frozen record. `--emit-candidate` only prints a candidate record;
it does not certify agreement with the frozen record.

The infinite portions are the written ordinary proof and the explicitly
imported9434/9195 lemmas, not seven endpoint samples. Exact replay and a
shared signature do not constitute formalization or independent review.
