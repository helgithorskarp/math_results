# Excluding Hall-witness size four at the order-15 frontier

For a vertex `x` in a tournament, put

```text
A = N+(x),  B = N-(x),
Gamma_x(S) = {b in B : s -> b for some s in S}.
```

A vertex is **strong Seymour** when the directed bipartite link from `A` to
`B` has a matching saturating `A`.  It is **ordinary Seymour** when
`|N++(x)| >= |N+(x)|`.

## Theorem

Suppose that a tournament `T` on 15 vertices has no strong Seymour vertex.
If `x` is an ordinary Seymour vertex and `S` is an inclusion-minimal
deficient Hall set at `x`, then

```text
d+(x) = 7  and  |S| is 5 or 6.
```

The preceding
[`strong_seymour_order15_small_hall`](../strong_seymour_order15_small_hall)
theorem already proves `4 <= |S| <= 6`.  It remains to exclude `|S|=4`.

## Local notation and degree bound

Assume `|S|=4`, and write

```text
R = Gamma_x(S),   C = A \ S,   D = B \ R.
```

The earlier frontier theorem gives `d+(x)=7`, while ordinaryness gives
`N++(x)=B`.  Minimality of `S` gives `|R|=3`, and every vertex of `R` is
reached by at least two vertices of `S`.  Thus `|C|=3`, `|D|=4`, and every
arc between `D` and `S` points from `D` to `S`.

For `v in S`, define

```text
p(v) = d+_{T[S]}(v),       q(v) = |N+(v) intersect R|.
```

The only possible out-neighbors of `v` lie in `(S\{v}) union R union C`.
Since the global minimum out-degree is six,

```text
p(v) + q(v) >= 3.                                  (1)
```

If equality holds, then `v` dominates all three vertices of `C` and has
out-degree six.  Since `N++(x)=B` and `S` sends no arc to `D`, every vertex
of `D` is reached from `C`.  Therefore all four vertices of `D` are exact
second out-neighbors of `v`.

## Equality analysis

Assume `p(v)+q(v)=3`.  Four cases are possible.

1. If `q(v)=0`, then `p(v)=3`.  The vertex `v` dominates the other three
   members of `S`.  Double coverage of every member of `R` therefore puts all
   three vertices of `R` at distance two from `v`.  Together with `D`, this
   makes `v` ordinary, contradicting the accepted exclusion of ordinary
   degree-six vertices.

2. If `q(v)=1`, then `p(v)=2`.  The four vertices of `D` and the path through
   the unique dominated Hall neighbor to `x` already give five second
   out-neighbors.  Let `W` be the two out-neighbors of `v` in `S`, and let
   `u` be its remaining in-neighbor in `S`.  If either member of `R\N+(v)` is
   reached from `W`, it is a sixth second out-neighbor.  If neither is, each
   can be reached from at most `u` among the four members of `S`, contradicting
   double coverage.

3. If `q(v)=2`, then `p(v)=1`.  The four vertices of `D` and `x` again give
   five second out-neighbors.  Let `w` be the unique out-neighbor of `v` in
   `S`, let `U` be its two in-neighbors there, and let `r` be the unique Hall
   in-neighbor of `v`.  To avoid a sixth second neighbor one must have
   `r->w`, `U->w`, and `U` dominating the two Hall out-neighbors of `v`.
   Double coverage of `r` then forces `U->r` as well.  Thus `w` has no
   out-neighbor in `S` and at most two in `R`, contradicting (1) at `w`.

4. If `q(v)=3`, then `p(v)=0`.  To prevent any other member of `S` from being
   reached through `R`, all three must dominate every member of `R`.  Hence
   every arc from `S` to `R` points toward `R`.  The vertex `v` is the sink of
   `T[S]`; the remaining three vertices form either a transitive triple or a
   directed triangle.  These are the two surviving equality signatures.

## Ten-orbit classification

If equality never holds in (1), then `p(v)+q(v)>=4` for all `v in S`.
Because `sum p(v)=6`, one has `sum q(v)>=10`.  Hence at most two of the twelve
arcs between `S` and `R` point from `R` to `S`.

There are four tournament types on four vertices, with score sequences

```text
(0,1,2,3), (0,2,2,2), (1,1,1,3), (1,1,2,2).
```

The first two contain a score-zero vertex, so the equality analysis forces
all twelve arcs toward `R`; these give two orbits.  In type `(1,1,1,3)`, only
the score-three vertex can miss a Hall out-neighbor, giving zero, one, or two
misses and three orbits.  In type `(1,1,2,2)`, misses can occur only at the
two score-two vertices and at most once at each.  There is one zero-miss
orbit, two one-miss orbits because the score-two vertices are inequivalent,
and two two-miss orbits according as the missed Hall heads agree or differ.
This gives exactly

```text
2 + 3 + 5 = 10
```

orbits under independent relabeling of `S` and `R`.

The first six bits below encode the arcs `(01,02,03,12,13,23)` in `T[S]`,
with `1` meaning the lower label dominates the higher.  The final twelve bits
encode `s_i -> r_j` in row-major order.

| orbit | representative | labeled size |
|---:|---|---:|
| 0 | `000000111111111111` | 24 |
| 1 | `000010111111111111` | 8 |
| 2 | `001000111111011011` | 72 |
| 3 | `001000111111011101` | 144 |
| 4 | `001000111111011111` | 72 |
| 5 | `001000111111111011` | 72 |
| 6 | `001000111111111111` | 24 |
| 7 | `001001111111001111` | 24 |
| 8 | `001001111111011111` | 24 |
| 9 | `001001111111111111` | 8 |

Their sizes sum to 472.  `enumerate_and_generate.py` obtains the same list by
canonicalizing all 262,144 labeled local patterns.  Of the 22,368 patterns
satisfying double coverage and (1), 21,896 force an ordinary degree-six
vertex.  `check_signatures.py` independently expands the ten displayed
orbits and verifies that their disjoint union is exactly the remaining 472
patterns.

## Exact global exclusion

For each orbit, `enumerate_and_generate.py` imports the exact all-vertex
no-strong encoding from `strong_seymour_order15/generate_cnf.py`.  It fixes
the normalized size-four Hall witness, adds the four clauses saying that the
ordinary root reaches `D` from `C`, fixes the displayed local signature, and
adds one harmless representative arc within each still-symmetric region
`C` and `D`.

Each resulting formula has 20,666 variables and 47,354 clauses.  CaDiCaL
3.0.1 proves all ten UNSAT.  `drat-trim` independently verifies every binary
DRAT trace; the checked cores contain no RAT lemma.  Exact per-case hashes,
sizes, and core statistics are in `EXPECTED.json`.

Every hypothetical size-four witness maps to one of the ten cases by
relabeling `S` and `R`, followed by the harmless relabelings inside `C` and
`D`.  Since all ten cases are impossible, `|S|` cannot be four.  The preceding
bound `4<=|S|<=6` therefore sharpens to `|S| in {5,6}`.

## Scope and trust boundary

This theorem does not settle existence of a strong Seymour vertex in every
order-15 tournament.  It leaves minimal Hall-witness sizes five and six at an
ordinary root.  The local reduction and orbit classification are written
above and checked by two finite standard-library computations.  The global
step trusts the inspected base generator, PySAT's sequential counters,
CaDiCaL, and `drat-trim`; proof checking establishes UNSAT only for the ten
exact hashed formulas.
