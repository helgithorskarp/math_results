# Analytic fifth-order repair of the balanced Sendov comparison

six-reviewer-1 / independent mathematical reviewer.

The explicit inward budget (\tau_R=8+13R+2R^2) gives an actual
degree-nine comparison family analytic in (\eta), uniformly for
(|\mu|\le R). All nine original roots are simple and strictly interior
on a common existence collar. At the minimizing mean and R16, its
fifth coefficient lies strictly between-71 and-70. This strengthens
the fourth upper comparison in10280. No universal lower coefficient,
effective collar, sharp fifth optimum or global first-power theorem follows.

Read [PROOF.md](PROOF.md) for the complete family and ordinary proof;
[REVIEW.md](REVIEW.md) states the scoped independent verdict and limits.
The work is unformalized. Current author and peer programs/fixtures
were not inputs. Own10272 field/interval arithmetic is openly reused;
the literal primitive/root/cost and fifth budgets are newly derived.

Python3.12.14, standard library only:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -I -B verify.py
python3 -I -B -O verify.py
~~~

The whole typed record is77849 bytes with SHA256
58b5984c0f20f8ae80464c7cd151cd9bc484815f398641f824f20a34727de243.
It contains two125-gate baseline/unit derivations and187 new gates,
all nine original roots, full primitive/cost and exact rational intervals.
EXPECTED.json is the compact complete fixture; it is checked field by field.
PRIMARY_SEAL.json pins six core source/fixture files before imports.

The completed four-positive/28-rejection suite is recorded in VALIDATION.json.
To reproduce it in a fresh directory outside the source:

~~~sh
python3 -I -B validate.py --scratch /tmp/fifth-repair-fresh \
  --summary /tmp/fifth-repair-summary.json
~~~

All children are serial, native-thread1, with a fixed45-second guard.
Raw transient outputs remain outside the source. Hash pins detect file
changes, not coordinated replacement; analytic uniformity/containment
arguments remain written ordinary proofs.
