# Full-feedback directional localization: exact small-graph census

## Result

Write \(\zeta_d^*(G)\) for the full-feedback directional localization
number introduced by Jones and Kinnersley.  The following finite theorem was
verified exactly.

> **Theorem.** Every connected simple graph on at most 10 vertices satisfies
> \(\zeta_d^*(G)\leq 2\).  In fact, two cops locate the robber within two
> probing phases.  Every connected cubic simple graph on at most 20 vertices
> also satisfies \(\zeta_d^*(G)\leq 2\), and two cops locate the robber within
> three probing phases.

Here the *two-cop capture rank* is the least number of probing phases needed
from the initial territory \(V(G)\).  A one-vertex graph has rank zero.  The
complete distributions are:

| order | connected graphs | rank 0 | rank 1 | rank 2 |
|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 0 | 0 |
| 2 | 1 | 0 | 1 | 0 |
| 3 | 2 | 0 | 2 | 0 |
| 4 | 6 | 0 | 6 | 0 |
| 5 | 21 | 0 | 21 | 0 |
| 6 | 112 | 0 | 109 | 3 |
| 7 | 853 | 0 | 831 | 22 |
| 8 | 11,117 | 0 | 10,846 | 271 |
| 9 | 261,080 | 0 | 257,192 | 3,888 |
| 10 | 11,716,571 | 0 | 11,634,005 | 82,566 |

| cubic order | connected cubic graphs | rank 1 | rank 2 | rank 3 |
|---:|---:|---:|---:|---:|
| 4 | 1 | 1 | 0 | 0 |
| 6 | 2 | 2 | 0 | 0 |
| 8 | 5 | 5 | 0 | 0 |
| 10 | 19 | 16 | 3 | 0 |
| 12 | 85 | 63 | 22 | 0 |
| 14 | 509 | 251 | 258 | 0 |
| 16 | 4,060 | 1,052 | 3,008 | 0 |
| 18 | 41,301 | 3,750 | 37,548 | 3 |
| 20 | 510,489 | 10,748 | 499,673 | 68 |

The 71 rank-three graph6 records are retained in
[`expected_results.json`](expected_results.json).  The three smallest ones are
also isolated in [`rank3_cubic18.g6`](rank3_cubic18.g6).

This does **not** answer the paper's open question asking whether some graph
has \(\zeta_d^*(G)>2\).  It rules out all connected graphs through order 10
and all connected cubic graphs through order 20 as counterexamples.  No claim
of priority beyond this reproducible artifact is made.

There is also a state-level strengthening.  Every connected graph through
order 10 satisfies the exact **response-fiber descent property** defined and
proved sufficient in [`DESCENT_CRITERION.md`](DESCENT_CRITERION.md).  The
census checks 462,804,261 distinct neighborhood-generated territories.  This
structural certificate gives an alternative proof of the same order-10
conclusion, but the property is only sufficient: the finite census does not
assert that it holds for every graph.

## Exact reduction

For a probe at \(p\) and robber position \(r\), the deterministic full-feedback
reply is

\[
F_p(r)=
\begin{cases}
\{p\},&r=p,\\
\{w\in N(p):d(w,r)=d(p,r)-1\},&r\ne p.
\end{cases}
\]

A simultaneous action \(A\), consisting of at most two distinct probes,
therefore partitions the current robber territory \(B\) by the signature
\((F_p(r))_{p\in A}\).  If the observed cell is \(C\), the cops win immediately
when \(|C|=1\).  Otherwise, after the robber stays or traverses one edge, the
next territory is the closed-neighborhood union
\(N[C]=\bigcup_{v\in C}N[v]\).

Let \(W_0\) be the singleton territories.  Recursively, a territory \(B\) lies
in \(W_t\) if some action \(A\) has the following property for every cell
\(C\) of its response partition: either \(|B\cap C|\leq1\), or
\(N[B\cap C]\in W_{t-1}\).  Induction on \(t\) proves that \(B\in W_t\) exactly
when the cops can guarantee localization within \(t\) phases.  This captures
adaptive strategies because the next action is chosen separately for every
possible response cell.

[`dirloc_solver.cpp`](dirloc_solver.cpp) implements this recurrence with exact
64-bit vertex masks.  It uses specialized but equivalent tests for ranks one
and two, followed by bounded memoized recursion for larger requested ranks.
A failure at a requested depth is reported as `UNKNOWN`, never as a losing
graph.  The census driver rejects every `UNKNOWN` or `LOSE` row.

## Exhaustiveness and independent checks

[`run_census.py`](run_census.py) invokes `geng` from nauty/Traces 2.9.3.
For each order it generates one representative of every connected unlabeled
graph; the cubic run additionally imposes minimum and maximum degree three.
Sixteen nauty residue classes partition each enumeration.  Their summed graph
counts must equal constants fixed in the driver before any game result is
accepted.  Since capture rank is invariant under graph isomorphism, checking
these representatives proves the finite theorem, subject to the generator
trust boundary.

Three structurally different checks reduce implementation risk:

1. [`reference_solver.py`](reference_solver.py) constructs the entire
   nonempty belief lattice and computes its least fixed point.  It agrees
   entry by entry with the optimized C++ solver on all 12,113 connected
   unlabeled graphs through order 8 and checks graph6 decoding by round trip.
2. [`verify_rank3.py`](verify_rank3.py) uses arbitrary-precision Python masks
   and an independent bounded recurrence.  It verifies that all 71 stored
   cubic records are connected, cubic, and have exact rank three (failure in
   two phases and success in three).
3. [`verify_descent.py`](verify_descent.py) independently constructs every
   neighborhood-generated territory and checks every response cell of the
   C++ descent certificates.  It agrees entry by entry through order 8
   (238,156 territories over 12,113 connected graphs, including order 1).

An independent reviewer also audited the original census at its immutable
source commit, checked all 71 rank-three witnesses with separately written
code, reproduced the complete order-9 and cubic order-20 censuses, and tested
an order-10 residue class.  The review and retained outputs are in
[`directional_localization_census_review`](../directional_localization_census_review/README.md).

The C++ code was compiled with GCC 12.2.0 using strict conversion and shadow
warnings.  An AddressSanitizer/UndefinedBehaviorSanitizer build also completed
the entire connected order-8 census without a diagnostic.  Remaining trust
boundaries are the correctness of nauty/Traces, the compiler and hardware,
and the mathematical reduction above.

## Reproduction

Obtain and build [nauty/Traces 2.9.3](https://users.cecs.anu.edu.au/~bdm/nauty/),
then set `GENG` to its `geng` executable.  From this directory:

```bash
g++ -std=c++20 -O3 -DNDEBUG \
  -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
  dirloc_solver.cpp -o dirloc_solver

python3 reference_solver.py \
  --compare ./dirloc_solver --geng "$GENG" --max-order 8

python3 verify_rank3.py

python3 verify_descent.py \
  --compare ./dirloc_solver --geng "$GENG" --max-order 8

python3 run_census.py \
  --geng "$GENG" --solver ./dirloc_solver \
  --scope both --partitions 16 --jobs 16 > observed_results.json

diff -u expected_results.json observed_results.json

python3 run_descent_census.py \
  --geng "$GENG" --solver ./dirloc_solver \
  --max-order 10 --partitions 16 --jobs 16 > observed_descent.json

diff -u descent_results.json observed_descent.json
```

The full run processes 12,546,235 graphs.  It uses only the Python standard
library plus a C++20 compiler and the external graph generator.  Changing the
number of residue classes or workers does not change the JSON result.

## Literature target

The motivating source is John Jones and William B. Kinnersley,
[*The Directional Localization Game on Graphs*](https://arxiv.org/abs/2609.01745),
arXiv:2609.01745 (2026).  Its final open question asks whether a graph with
\(\zeta_d^*(G)>2\) exists.
