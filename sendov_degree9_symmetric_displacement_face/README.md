# Exact optimization of a degree-nine symmetric displacement face

Author **six-sendov-2**, role **researcher**, 2026-09-30.
Ordinary proof with exact arithmetic certification; independent review
pending. No formalization or historical-priority claim.

For slopes

    (1,1,sqrt(X),sqrt(u),-1,-1,-sqrt(X),-sqrt(u)),  0<=X,u<=1,

the displacement functional J=mu2*K/p0 of the reviewed collapsed angular
quartic is maximized exactly at (X,u)=(1,u*) and (u*,1).
Here u* is the algebraic optimizer already published for the 3+3+1+1
curve, between2/25 and9/100. The additional movable conjugate pair cannot
improve that curve's coefficient. For ordered u<=X,

    J*-J(X,u) >= min(12/7, (1-X)/2 + 450*(u-u*)^2).

The [proof](PROOF.md) derives a rational spectral invariant, covers the
whole face by six exact polynomial certificates, and identifies a false
universal spread-monotonicity route. The prior optimum and actual crossing
are credited in [LITERATURE.md](LITERATURE.md).

From repository root, using Python3.11.2 and only its standard library:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B sendov_degree9_symmetric_displacement_face/verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O sendov_degree9_symmetric_displacement_face/verify.py
```

Both commands print identical results: **807 exact checks**, **380**
Bernstein entries, **seven** rational commutant-projection controls and
**six rejected corrupt manifests**. All checks remain enabled under -O.
Canonical coefficient SHA256:

    92ba3bcafdd62abb39fa968a26f537b26be539d073a09a02f21ced5ff6a2974d

[verify.py](verify.py) reconstructs every polynomial and all Bernstein
coefficients, reverses each full basis conversion, and compares the compact
[expected.json](expected.json) manifest. It imports no other campaign
code, uses no floating point or solver, and needs no external data.
One small CPU process suffices. Matrix profiles are definition-level
author controls, not a universal enumeration or independent review.
The full-domain certificate, physical and spectral bridges, collision
continuity and calculus are described in the proof with their dependencies.

Scope: two saturated conjugate pairs and two movable pairs at the degree-nine
collapsed cutoff. The exact maximum-displacement basin over unrestricted
balanced directions remains unresolved. The stronger first-power endpoint
F>=8 is also outside the claim; this local baseline is128/13>8.
