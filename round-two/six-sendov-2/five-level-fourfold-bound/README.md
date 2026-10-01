# Fourfold original-root angular bound

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.

The complete genuine five-level 4+1+1+1+1 family satisfies **C<c3**, with
sharp supremum c3=24.53389668... inherited from the three-level optimizer.
Combined with8957, the sharp inequality C<=c3 holds whenever there are
at most four original levels or an original-coordinate block of size at
least four; equality is exactly the known4+3+1 orbit.

The new proof uses three compression moments, a17/19-term rational Bessel
upper bound, two classical quartic moment constraints and two complete
tensor Bernstein boxes. All120+105 coefficients are strictly positive.
An exact genuine-five-level path establishes sharpness at the collision.

- [PROOF.md](PROOF.md): full argument, equality, sharpness, scope and the
  failed coefficient-convexity shortcut.
- [verify.py](verify.py): standalone Fraction checker, no CAS or floats.
- [expected.json](expected.json): compact regenerated exact evidence.
- [LITERATURE.md](LITERATURE.md): current primary status and attribution.

From this directory, with CPython3.11.2 (used here):

```bash
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
```

Expected: PASS,76 recorded checks,225 positive Bernstein coefficients,
six full eight-coordinate commutant controls and four mathematical damage
controls. Normal and optimized modes regenerate exactly the same fixture.
The record hash is **0a2fac690549342c195009f62019922fc1088306b460a829ea6ec37045cf4dc5**. The decisive checker uses only
Python's standard library; SymPy1.14.0 was a discovery aid.
Each mathematical run used a fixed50-second guard and one native thread.
The final measured runtime and memory are recorded separately in publication
receipts; no timeout or incomplete search is used as a mathematical exclusion.

To regenerate the full mathematical record after performing all proof checks,
use `python3 -I -B verify.py --emit`. To check a separately supplied fixture,
use `--expected PATH`; a changed fixture is rejected even with `python -O`.

This is an author-checked ordinary proof, unformalized and independently
unreviewed at publication. Standard spectral projection and interlacing,
the real-root moment enclosure, Bessel's inequality and the application of
the credited three/four-level theorems remain ordinary proof bridges.
It does not establish the other two five-level patterns, the global sphere
constant Cstar, or the complex first-power Tang--Zhang endpoint.
