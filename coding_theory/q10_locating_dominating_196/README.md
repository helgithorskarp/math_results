# A 196-word locating-dominating code in the binary 10-cube

## Result

The 196 words in `code.txt` form a locating-dominating code in `Q_10`.
Consequently

\[
\gamma^{LD}(Q_{10})\le 196.
\]

Junnila, Laihonen, and Lehtilä proved, for `n >= 10`,

\[
\gamma^{LD}(Q_n)\ge \frac{2^{n+1}}{n+2}.
\]

At `n=10`, taking the integer ceiling gives 171.  The certified interval is
therefore

\[
\boxed{171\le \gamma^{LD}(Q_{10})\le196}.
\]

This improves the published 2021/2022 upper bound of 208 by twelve words.

## Direct certificate

For every non-codeword `v`, both checkers independently construct

\[
I_C(v)=C\cap N[v].
\]

They verify that the 828 signatures are nonempty and pairwise distinct.  The
signature-size distribution is

```text
size 1: 162
size 2: 403
size 3: 201
size 4:  55
size 5:   7
```

The unordered codeword-pair distance distribution is

```text
distance  1:   67
distance  2:  722
distance  3: 2574
distance  4: 3895
distance  5: 4450
distance  6: 4092
distance  7: 2311
distance  8:  781
distance  9:  198
distance 10:   20
```

The 1,826 code/non-code incidences and 67 internal code edges satisfy the
independent boundary identity

\[
1826+196+2\cdot67=11\cdot196=2156.
\]

## Discovery model

Location-domination is represented as a hitting-set problem.  There is a
domination clause `N[v]` for every vertex.  For distinct vertices `u,v`, the
separation clause is

\[
\{u,v\}\cup\bigl(N[u]\mathbin\triangle N[v]\bigr).
\]

Once domination is imposed, pairs at distance at least three have nonempty
signatures in disjoint closed balls and are automatically separated.  The
search code therefore uses only distance-one and distance-two separation
clauses: 29,184 clauses in total.  (The distance-one clauses are themselves
redundant under domination, but retaining them changes only the search
scoring, not the feasible sets.)

The fixed-cardinality min-break/max-make local search found the certificate
with this deterministic command on the discovery host:

```bash
g++ -std=c++20 -O3 -march=native -Wall -Wextra -pedantic \
  search_q10_ld.cpp -o /scratch/search_q10_ld
/scratch/search_q10_ld 196 18000000 22 300000 \
  > /scratch/q10_ld196.out 2> /scratch/q10_ld196.log
```

It reported `FOUND step=15123001 seed=22`.  The exact trajectory of a seeded
C++ random engine is implementation-specific; discovery reproducibility is
not part of the theorem's trust boundary.  Four bounded searches at size 195
using two equivalent clause sets stopped with two uncovered clauses.  Those
timeouts are heuristic only and establish no lower bound.

## Reproduce the theorem

The Python checker generates XOR neighborhoods and intersects sets:

```bash
python3 verify_q10_ld196.py
```

The independently implemented C++ checker instead tests all codeword/vertex
Hamming distances directly:

```bash
g++ -std=c++20 -O2 -Wall -Wextra -pedantic \
  verify_q10_ld196.cpp -o /scratch/verify_q10_ld196
/scratch/verify_q10_ld196 code.txt
```

A fresh run used Python 3.11.2 and GCC 12.2.0.  The C++ checker also passed an
AddressSanitizer/UndefinedBehaviorSanitizer build.  Source SHA-256 hashes are

```text
code.txt                 1a01f85b45699f5d8cb2d6e4269a6bb107997a5c2a49f2187d82631ce0cdeba3
verify_q10_ld196.py      725db86d68094354eeaf18e44effd2f4b3bbc89ff4125b22111116be61276f7c
verify_q10_ld196.cpp     f305b77880f6ea9220690d65aad98fcd5232316da1189d57a0b72f4115a017e2
search_q10_ld.cpp        14158a547490c8e315a07ba6c787cc2815e48625a48b58718abb4bc5cceabf99
```

The discovery log remains under `/scratch`; its SHA-256 is
`47ad6838e2340dbf1782689a092e38e819c78155a84c59e9a650013a7ce574ca`.

## Status, novelty, and trust boundary

The upper bound is a finite construction whose trust boundary is the displayed
196-word input, the two transparent complete enumerations, and ordinary
language/runtime correctness.  No solver status, heuristic claim, random
trajectory, floating-point computation, or external certificate is trusted.
The lower bound is the cited published theorem; the checkers verify only its
arithmetic specialization.

Targeted searches of the primary literature and exact-title/concept searches
through 2026-08-31 found no later binary-Hamming-space upper bound after the
2021/2022 paper.  The 196-word construction is therefore apparently new to
the searched sources; this is not a historical-priority claim.

## Sources

- V. Junnila, T. Laihonen, and T. Lehtilä, "Improved Lower Bound for
  Locating-Dominating Codes in Binary Hamming Spaces," *Designs, Codes and
  Cryptography* 90 (2022), 67--85.
  https://doi.org/10.1007/s10623-021-00963-8
- I. Honkala, T. Laihonen, and S. Ranto, "On Locating-Dominating Codes in
  Binary Hamming Spaces," *Discrete Mathematics & Theoretical Computer
  Science* 6(2) (2004), 265--282.
  https://doi.org/10.46298/dmtcs.322
