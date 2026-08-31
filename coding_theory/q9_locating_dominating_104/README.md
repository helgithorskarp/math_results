# A 104-word locating-dominating code in the binary 9-cube

## Result

The 104 words hard-coded in both verifiers form a locating-dominating code
in `Q_9`.  Consequently

\[
\gamma^{LD}(Q_9)\le 104.
\]

The Honkala--Laihonen--Ranto lower bound specializes to

\[
\left\lceil
\frac{9^2 2^{10}}{9^3+2\cdot9^2+3\cdot9-2}
\right\rceil
=\left\lceil\frac{82944}{916}\right\rceil=91,
\]

so the certified interval is

\[
91\le\gamma^{LD}(Q_9)\le104.
\]

The 2021/2022 literature table gives the preceding upper bound 112, obtained
from an identifying code.  Thus this construction improves that bound by
eight words.  It is apparently new relative to the primary-source searches
described below; this is not a historical-priority claim.

## Direct certificate

For every non-codeword `v`, both checkers independently form

\[
I_C(v)=C\cap N[v].
\]

They verify that the 408 resulting signatures are nonempty and pairwise
distinct.  The exact signature-size distribution is

```text
size 1:  87
size 2: 196
size 3: 110
size 4:  10
size 5:   3
size 6:   2
```

The unordered codeword-pair distance distribution is

```text
distance 1:   30
distance 2:  332
distance 3: 1033
distance 4: 1287
distance 5: 1237
distance 6:  961
distance 7:  386
distance 8:   72
distance 9:   18
```

These counts sum to `5356 = binom(104,2)`.  The 876 code/non-code
incidences and 30 internal code edges satisfy the independent boundary check

\[
876+104+2\cdot30=10\cdot104=1040.
\]

## Exact local-clause reduction used for discovery

Location-domination can be written as a hitting-set problem.  The domination
clause for `v` is `N[v]`.  For distinct `u,v`, separation is the clause

\[
\{u,v\}\cup\bigl(N[u]\mathbin{\triangle}N[v]\bigr).
\]

If the code hits all domination clauses and `d(u,v)>=3`, then `N[u]` and
`N[v]` are disjoint while both signatures are nonempty.  Their signatures
are therefore automatically different.  It is enough to include separation
clauses for distance-one and distance-two pairs.  In `Q_9` this gives exactly

\[
512+\frac{512\cdot9}{2}
+\frac{512\binom{9}{2}}{2}
=512+2304+9216=12032
\]

clauses, rather than one clause for every pair of vertices.  This is an exact
model reduction, not a heuristic relaxation.  The search program maintains a
fixed-size set and performs min-break/max-make swaps on this reduced model.

Starting from the preserved 105-word code, the deterministic command

```bash
g++ -std=c++20 -O3 -march=native -Wall -Wextra -pedantic \
  search_q9_ld.cpp -o /scratch/search_q9_ld
/scratch/search_q9_ld 104 3000000 28 100000 q9_ld105_seed20.txt
```

finds the displayed 104-word certificate at step 51,645 with libstdc++ and
GCC 12.2.0 on the discovery host.  The exact output of a seeded C++ random
engine is implementation-specific; discovery reproducibility is not needed
for verification.  Four five-million-step seeded searches at size 103 stayed
at two uncovered clauses.  Those timeouts are heuristic and establish no
lower bound.

## Reproduce the theorem

The Python checker uses explicit XOR neighborhoods and set intersection:

```bash
python3 verify_q9_ld104.py
```

The independently implemented C++ checker uses direct Hamming-distance
comparisons:

```bash
g++ -std=c++20 -O2 -Wall -Wextra -pedantic \
  verify_q9_ld104.cpp -o /scratch/verify_q9_ld104
/scratch/verify_q9_ld104
```

Both print the distributions and interval above.  Successful runs used
Python 3.11.2 and GCC 12.2.0.  All decisive operations are exact.  The
theorem's trust boundary is the displayed finite input, the two transparent
complete enumerations, and ordinary Python/C++ runtime and compiler
correctness.  No solver status, proof log, stochastic-search claim, or
floating-point result is trusted.

## Status and sources

The graph's preceding 56-word `Q_8` code lifts trivially to a 112-word `Q_9`
code, matching the published 112 upper bound, but the 104-word code here is
verified directly and does not depend on a lift.  Targeted searches through
2026-08-31 found no later primary-source table or smaller explicit `Q_9`
locating-dominating code.

- I. Honkala, T. Laihonen, and S. Ranto, "On Locating-Dominating Codes in
  Binary Hamming Spaces," *Discrete Mathematics & Theoretical Computer
  Science* 6(2), 2004, 265--282.
  https://doi.org/10.46298/dmtcs.322
- V. Junnila, T. Laihonen, and T. Lehtila, "Improved Lower Bound for
  Locating-Dominating Codes in Binary Hamming Spaces," *Designs, Codes and
  Cryptography* 90, 2022, 67--85.
  https://doi.org/10.1007/s10623-021-00963-8
