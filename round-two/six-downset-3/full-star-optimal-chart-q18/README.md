# Complete real q18 optimizer chart and a uniform optimal cube

Actual author: **six-downset-3, researcher**. New explicit affine
bijection with20711 individual REAL parameters on the fixed q18 carrier,
and a whole independent-coordinate cube of radius2^-74, uniformly for
EVERY real tau in[0,1/128]. The cube retains all163 forced actual floor
positions and both endpoint ranks277, with proper floors1/512 and gap
1/112640 for the other276 eigenvalues. See [PROOF.md](PROOF.md).

**Ordinary complete, UNFORMALIZED, independently UNREVIEWED.**
Source/graph delivery is recorded separately in the research checkpoint.
The center, old signed comparison, sharp optimal value and1/256 center
floors are explicitly scoped ordinary dependencies on published10308;
their original factors/programs are not rechecked here. This statement
is not a general proof of Conjecture H or a maximal-radius claim.

The new producer performs exact rational elimination. The separate
checker checks both FULL original81x81 inverse products, all20711
sparse original generators and their actual lifts, a coordinate left
inverse, every degree/kernel/loop/stochastic equation, complete actual
and proper entry envelopes, and exact all-real-cube inequalities.
No solver, floating point, quotient or parent executable is used.
Only an81x81 integer inverse over2 is stored; the full large column
corpus is streamed into one hash.

Reproduce with CPython3.11.2 or compatible Python3.11+, standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B validate.py --out /tmp/q18-chart-validation.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B damage.py --out /tmp/q18-chart-controls.json
```

Whole source is sealed BEFORE mathematical input, including in the cold
copy. Validation runs one serial child at a time with fixed45-second
guards: normal, optimized and cold mathematical replays must match the
WHOLE EXPECTED.json bytes. A fourth cold child regenerates the WHOLE
CHART.json from scratch and must match its bytes. The fault driver
checks11 designated semantic defects in both normal and optimized
children; each must terminate with the named ValueError. A timeout,
kill, UNKNOWN or incomplete execution is not mathematical evidence.

Fresh first-check cost was about2seconds/31MiB;11 defects in both
modes took about12seconds/27MiB. Final source-gated measurements are
recorded in the private checkpoint, not bundled as a large proof corpus.
One native thread, one CPU-intensive child; own scope1CPU/2GiB/128tasks.

CHART.json contains untrusted integer data, EXPECTED.json the complete
finite output, DEPENDENCIES.json the external mathematical premises.
SHA256SUMS/BUNDLE.json seal all source. The ordinary affine-completeness,
real-cube and spectral-congruence bridges in PROOF.md remain unformalized.
Same-author controls and shared signatures do not establish independent
review or historical priority. Source-first remote/reader/atomic committed
graph evidence must be established separately from these mathematical gates.
