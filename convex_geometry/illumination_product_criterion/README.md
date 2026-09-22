# A criterion for multiplying illumination numbers

A convex polytope `P` satisfies

    I(P x K)=I(P)I(K) for every convex body K

if and only if its fractional and ordinary illumination numbers agree:

    I_f(P)=I(P).

The equivalent condition using only powers is `I(P^r)=I(P)^r` for every
positive integer `r`, or even for arbitrarily large `r`. The proof gives

    lim I(P^r)^(1/r)=I_f(P)

and an integer-arithmetic bound that detects a finite strict power whenever
there is a fractional gap. It uses the exact finite family of illuminated
vertex subsets, product certificates, fiber counting, and classical
greedy rounding. The partner in the first assertion may be nonpolytopal.

Product failure and the pentagon example are prior mathematics. Our
rational pentagon is a reproducible version of Baladze--Boltyanski's
five-cycle mechanism: `I(P)=3`, `I_f(P)=5/2`, and `I(P x P)=8`.
The theorem concerns the all-partner criterion, not a new isolated
illumination number or a solution of the general illumination conjecture.
Historical priority of the criterion is unestablished.

Read [PROOF.md](PROOF.md) for the proof and
[SOURCES.md](SOURCES.md) for the attribution and search limits.
[construct.py](construct.py) produces finite product and greedy
certificates; [verify.py](verify.py) checks them from the definitions.

Run from this directory with Python 3.11 or later, standard library only:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py
sha256sum -c SHA256SUMS
```

Both runs must agree with [expected.json](expected.json). The audit checks
all 20 direction strata for the rational pentagon, 100 vertex/direction
incidences, 25 product vertices, matching fractional certificates, eight
deletion holes, all 109 covering set families on three elements, and all
81 ordered products of their nine maximal reductions. Eighty product
pairs have a factor with no fractional gap and attain multiplicativity.
Ten malformed inputs or certificates must be rejected.

Greedy traces through the cube validate the construction only; their
counts are upper bounds. In particular greedy uses nine directions for
the square, whereas the separate optimal certificate uses eight. The
integer bound first detects strictness at exponent 24 for this example;
that is a sufficient bound, while the actual first strict exponent is two.
The audit does not construct the 24th power. The normal run takes about
one second in the development environment. No solver, floating-point
calculation, external dataset, formalization, or independent peer review
is part of the proof claim.
