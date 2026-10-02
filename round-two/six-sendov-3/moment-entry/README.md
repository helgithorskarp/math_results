# Moment-aware entry into degree-nine Sendov stability

Actual author: **six-sendov-3**, researcher. See [PROOF.md](PROOF.md).

For `0<eta<=2^-16`, the proved normalized collar9373 is now entered by
coefficient distance `delta^6 2^-1999 eta^7` (previous power13), by critical
matching energy `delta^2 2^-664 eta^3`, or by the larger eta2 critical-energy
condition with a separately controlled total imaginary trace. The original
matching-energy condition has sufficient power14. All conditions cover
complex polynomials and small critical collisions.

An explicit **feasible inward original-root motion** has both matching
energies of order eta3 while remaining outside the displayed normalized
normal box. Thus power3 is sharp for unweighted critical-energy entry
uniformly as eta tends to zero; constants are not optimized. This is a
local entry theorem and an entry obstruction, not a first-power counterexample
or global concentration/minimum result. The ordinary analytic bridges
remain unformalized and this new result independently unreviewed.

Reproduce with Python3.11+, standard library only, in the authorized
repository with the hash-bound source dependencies present:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-3/moment-entry/verify.py
```

The checker rejects malformed, changed or incomplete inputs, regenerates
the entire compact fixture and replays9373's full80-predicate record.
Use one child at a time with a45-second guard. The new exact budgets,
semantic damage controls, canonical digest and measured cost are recorded
in [VALIDATION.json](VALIDATION.json). No solver search or floating point
output proves the ordinary analytic bridges.
