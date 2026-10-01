# Full fourfold angular-family bound

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Complete ordinary proof with finite exact checks; independent review pending.

[PROOF.md](PROOF.md) proves the sharp bound C<=c3=24.533896688... on
the entire normalized4+2+1+1 family, including all signs and collisions,
with equality precisely at the inherited4+3+1 orbit. It follows for every
at-most-four-level profile containing a block of at least four. An
existential global family quadratic stability bound is also given.

Using the existing3+3+1+1 bound, the remaining genuinely four-level
competitors are3+2+2+1 and2+2+2+2, with four positive/four negative entries.
The unrestricted sphere maximum and degree-nine first-power endpoint are
still open. The sign/heavy-block prerequisite8851 has a complete ordinary
author proof with independent review pending;8753 and8800 are independently
confirmed. [LITERATURE.md](LITERATURE.md) distinguishes these dependencies.

Reproduce using Python3.11+ standard library (tested CPython3.11.2):

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 python3 -I -B verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 python3 -I -B -O verify.py
```

Expected63 recorded items/four mathematical damage controls, record SHA256
`657c42a57af3de781aabbcdf9b50dcd516dd664e39d022ee73faf0525da562ae`.
The checker regenerates the original derivative and full moment/Gram
polynomials. It verifies171 integer17x17 Sylvester determinants under a
degree170 bound, and136/138 integer15x15 minors under degree135/137 bounds.
Newton forward interpolation modulo the quartic proves its forced
collision. Rational Sturm counts and48 positive Bernstein coefficient
intervals exclude every nonquartic stationary branch on its entire
allowed vertical domain. No high-degree lift inversion is required.

`--write-expected` regenerates the compact regression fixture;
`--expected PATH` checks an external fixture; `--progress` prints phase
completion to stderr. Normal/-O tests agree and an altered external
fixture is rejected. Final guarded source wall6.71/6.39sec, peak child22508KiB, native threads1,
serial mathematical jobs and fixed50sec command guards. No CAS or solver
dependency. Written compactness, interlacing and spectral/cofactor/positivity
bridges remain outside a formal kernel. The old incomplete algebraic lifts
are neither needed nor distributed.
