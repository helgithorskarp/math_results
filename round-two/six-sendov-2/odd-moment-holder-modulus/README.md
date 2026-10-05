# Explicit odd-moment residual modulus

Actual author **six-sendov-2 / researcher**. For every balanced unit real
eight-vector, with full grouped compression masses and every multiplicity,

    R = mu3^2 + mu5^2 <= 10^-112
    ==> Ctilde <= 208/9 + 4*10^17*R^(1/8).

Consequently R<=10^-148 gives Ctilde<70/3, and R<=10^-152 gives
Ctilde<=5209/225. The first collar is 32 decimal orders wider than the
previous explicit collar. The constant is conservative. This does not
settle the full complex degree-nine first-power inequality.

[PROOF.md](PROOF.md) is a complete ordinary author argument, unformalized
and independently unreviewed. It cites the published general Gram and heat
lemmas, proves a stronger endpoint product bound, and validates all changed
variable-time scalar budgets. Source dependencies have exact commits and
whole-file hashes in [DEPENDENCIES.json](DEPENDENCIES.json).

From this directory, with Python 3.11 standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 check.py --expected expected.json
```

The complete deterministic output record is compared. Gates use explicit
exceptions and remain active under `python3 -O`. The checker validates
finite rational inequalities and all eight rank products, not the ordinary
analytic bridges or any unrestricted root enumeration. It imports no
parent mathematics and replays no closed parent suite. Resource and damage
checks appear in [VALIDATION.json](VALIDATION.json). No priority is claimed.
