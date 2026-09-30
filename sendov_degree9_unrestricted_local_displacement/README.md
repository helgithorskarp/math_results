# Unrestricted local degree-nine displacement stability

Actual author **six-sendov-2**, role **researcher**, 2026-09-30.
Ordinary written author proof; independent review pending.

The known displacement direction
`(1,1,1,-1,-1,-1,sqrt(u*),-sqrt(u*))` is a strict local maximum against
every balanced max-normalized eight-vector. Either triple may split
arbitrarily. On an explicit neighborhood, the angular loss is at least
`200 S + 450 (r-u*)^2`, where `S <= 1/100000` is total inward movement
of the six saturated slopes and `2/25 <= r <= 9/100` is the squared
half-difference of the remaining entries. Squared distance of the unit
direction to the optimizer orbit is at most the objective deficit / 90.
The sharp first-order normal-loss coefficient is the credited optimum / 3.

An analytic upper support omits nonnegative inactive spectral weights.
It touches the true grouped objective to fourth order through arbitrary
spectral collisions. Explicit rational contour and Hessian bounds cover
all coordinate changes. The associated complex polynomial phase basin
has the credited leading constant `27.106707 < B* < 27.106708`, now with
no phase-multiplicity condition inside this angular neighborhood.

This is a local result. It does not determine the unrestricted global
optimizer or prove the full first-power endpoint. Read [PROOF.md](PROOF.md)
and [LITERATURE.md](LITERATURE.md) for the hypotheses, dependencies and
trust boundaries.

Python 3.10+ standard library only; author validation uses Python 3.11.2.
Run sequentially from this directory, with one mathematical process:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
```

Each compares the complete compact [expected.json](expected.json).
Expected: PASS, 162 exact checks, six new continuous-domain coefficients,
28 full balanced tangent controls at four exact rational profiles.
Complete canonical record SHA-256:
`48c489f0e8eb748a99cf4184a470a7c98b07a696f0466d4fedd7ca2185cde135`.
No CAS, solver, floating proof input, corpus or campaign module is needed.
The finite algebra checks support the written analytic proof; they do
not alone establish continuum coverage or count as external review.
