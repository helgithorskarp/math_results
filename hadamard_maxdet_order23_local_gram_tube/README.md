# A local Gram exclusion tube around the order-23 record

## Result

Let `R0` be the published order-23 sign matrix in `record23.txt`, let

```text
G0 = R0 R0^T,
L  = |det(R0)| = 2779447296000000,
```

and measure the distance between symmetric matrices by the number of
different entries strictly above the diagonal.  The off-diagonal entries of
`G0` consist of 208 copies of `-1` and 45 copies of `3`.

This artifact proves the following finite local exclusion.

> **Lemma.** Let `M` be symmetric of order 23 with diagonal entries 23.
>
> 1. If every off-diagonal entry of `M` is congruent to 3 modulo 4 and has
>    absolute value below 23, and `M` differs from `G0` in at most two
>    off-diagonal positions, then `det(M)` cannot be a square at least `L^2`
>    unless `M=G0`.
> 2. If every off-diagonal entry belongs to `{-1,3}`, the same conclusion
>    holds through distance three.
> 3. The same conclusion holds for matrices obtained by changing at most
>    four of the 45 entries `3` in `G0` to `-1`.

The computation is stronger than a positive-definite candidate search: it
tests all matrices in the stated discrete neighborhoods, whether or not they
are positive definite.  A parity-normalized Gram matrix of a nonsingular
order-23 sign matrix satisfies the entry conditions in part 1, so the lemma
excludes every record-beating sign decomposition in these neighborhoods.

This does **not** determine the maximal determinant in order 23.  Candidate
Gram matrices farther from `G0`, including other graph-Gram matrices and
matrices containing larger inner products, remain untreated.

## Exact census

The four searches cover 6,006,451 matrices:

| neighborhood | matrices | square-determinant survivors | largest square root |
|---|---:|---:|---:|
| exactly one arbitrary legal edit | 2,530 | 0 | — |
| exactly two arbitrary legal edits | 3,187,800 | 756 | 2,743,271,424,000,000 |
| exactly three `-1`/`3` toggles | 2,667,126 | 24 | 2,740,715,520,000,000 |
| exactly four deletions of existing `3`-edges | 148,995 | 0 | — |

All 780 survivors are evaluated by direct exact integer determinants.  Their
complete determinant/multiplicity census is in `certificate.json`; every
square root is strictly below `L`.  The nearest one is about 1.30% below the
record.

## Reproduction

Only Python 3.10 or later and a C++20 compiler are required.

```bash
g++ -std=c++20 -O3 -Wall -Wextra -Wconversion -Wshadow -pedantic \
  enumerate.cpp -o enumerate
./enumerate record23.txt > result.json
python3 verify.py result.json
```

The terminal output ends with

```text
modular local Gram exclusion verified
exact local Gram exclusion certificate verified
```

`enumerate.cpp` checks all 6,006,451 matrices and assigns every nonsquare a
quadratic-nonresidue witness among 48 explicitly checked primes.  It emits
the 780 cases that survive those tests.  `verify.py` independently rebuilds
`G0`, checks `det(G0)=L^2` by fraction-free Bareiss elimination, recomputes
the scaled inverse, validates the survivor encodings, and evaluates every
survivor determinant directly with Python integers.

On the research host, GCC 12.2.0 completed the enumeration in 16.7 seconds
on one core with peak resident memory about 10.2 MiB.  The Python checker
took 2.9 seconds with peak resident memory about 12.3 MiB.  The full C++ run
also passed AddressSanitizer and UndefinedBehaviorSanitizer using `-O1 -g`,
`-fsanitize=address,undefined`, and `-fno-omit-frame-pointer`.

## Known frontier and sources

Orrick, Solomon, Dowdeswell, and Smith published the matrix and determinant
record in [*New lower bounds for the maximal determinant
problem*](https://arxiv.org/abs/math/0304410).  Exhaustive candidate-Gram
generation and decomposition are the standard route to exact odd-order
results; the relevant definitions and algorithms are given by
[Orrick](https://arxiv.org/abs/math/0401179) and by
[Brent--Orrick--Osborn--Zimmermann](https://arxiv.org/abs/1112.4160).

At least 14 inequivalent order-23 matrices attaining the same record were
already known by 2005; see Orrick's
[*On the enumeration of some D-optimal
designs*](https://arxiv.org/abs/math/0511141).  This artifact is anchored to
the particular published matrix `R0`.  It does not assert that the Gram
neighborhoods of the other record designs are equivalent to this one.

The present result is a local certificate around the order-23 record.  No
claim is made that the local neighborhood had previously been studied, or
that this replaces global candidate-Gram enumeration.

## Trust boundary

The proof trusts the matrix determinant lemma, elementary finite-field
arithmetic, and the fact that an integer square is a quadratic residue or
zero modulo every prime.  All listed primes are checked by trial division at
runtime.  Products modulo primes are bounded below `10^18`, and the raw
scaled-update entries are below `2*10^9`, so signed 64-bit arithmetic is
safe.  The C++ enumerator is the exhaustive coverage component; the Python
program is an independent exact checker for its compact survivor list.
