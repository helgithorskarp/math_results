# Explicit approximate-odd-moment angular collar

**six-sendov-2 / researcher**, 2026-10-05.
Ordinary author proof; unformalized and independently unreviewed.

For every balanced unit real original vector of length eight, with all
original and compression multiplicities and full grouped masses,

\[
 \mu_3^2+\mu_5^2\le10^{-180}\quad\Longrightarrow\quad
 \widetilde C\le70/3=47/2-1/6.
\]

[PROOF.md](PROOF.md) makes a legal exact-locus comparison: backward heat
separates actual roots; eight sign intervals license the heated polynomial
after the two residual coefficients are erased. Its general three-row
Gram changes by a controlled amount and retains an explicit positive
determinant. A closed-collar heat approximation completes collisions.
The collar is extremely conservative; it is an explicit quantitative
existence result, not an estimate of the largest useful collar.

This builds on the credited exact-locus sharp polynomial, parity
continuation, universal real localization and full-mass continuity. It
does not solve the unrestricted complex first-power inequality or the
whole balanced real angular sphere. See [DEPENDENCIES.json](DEPENDENCIES.json)
and [LITERATURE.md](LITERATURE.md) for scope and attribution.

From the repository root, with Python3.10+ standard library:

    python3 -I -B round-two/six-sendov-2/explicit-odd-moment-collar/check.py
    python3 -I -B -O round-two/six-sendov-2/explicit-odd-moment-collar/check.py

Set OMP_NUM_THREADS, OPENBLAS_NUM_THREADS, MKL_NUM_THREADS,
VECLIB_MAXIMUM_THREADS, NUMEXPR_NUM_THREADS and BLIS_NUM_THREADS to1.
The entire finite record is [expected.json](expected.json); commands,
hashes and targeted rejection evidence are in [VALIDATION.json](VALIDATION.json).
The code uses no solver, float predicates, external generated proof corpus
or parent mathematical executable. The written heat-gap/sign argument,
least squares and collision completion remain ordinary proof boundaries.
