# Excluding Hall-witness size five at the order-15 frontier

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
d+(x) = 7  and  |S| = 6.
```

The preceding
[`strong_seymour_order15_hall_size4`](../strong_seymour_order15_hall_size4)
theorem proves `|S|` is five or six.  It remains to exclude `|S|=5`.

## Local structure and the D-degree lemma

Assume `|S|=5`, and write

```text
R = Gamma_x(S),   C = A \ S,   D = B \ R.
```

The inherited frontier theorem gives `d+(x)=7`, while ordinaryness gives
`N++(x)=B`.  Minimality of `S` gives `|R|=4`, and every member of `R` has at
least two predecessors in `S`.  Consequently

```text
|C|=2,  |D|=3,  D->S,
```

and every vertex of `D` is reached from at least one member of `C`.

For `v in S`, define

```text
p(v) = d+_{T[S]}(v),       q(v) = |N+(v) intersect R|.
```

The only possible out-neighbors of `v` lie in `(S\{v}) union R union C`.
Since the global minimum out-degree is six and `|C|=2`,

```text
p(v) + q(v) >= 4.                                  (1)
```

There is also a useful constraint on `D`.  Every `d in D` dominates `x` and
all five members of `S`.  If `d+(d)=6`, these are its exact out-neighbors.
It then reaches both members of `C` through `x`, and it reaches every member
of `R` through `S`.  Thus it has at least six exact second out-neighbors and
is ordinary, contradicting the inherited exclusion of ordinary degree-six
vertices.  Therefore

```text
d+(d) >= 7 for every d in D.                        (2)
```

## Two exhaustive branches

Call a member of `S` **tight** when equality holds in (1).

If a tight vertex exists, relabel it as vertex 1.  The other four members of
`S`, and the sets `C`, `R`, and `D`, remain independently relabelable.  This
is the single `tight` SAT case.

Otherwise every member of `S` satisfies

```text
p(v) + q(v) >= 5.                                  (3)
```

Since `q(v)<=4`, (3) gives `p(v)>=1`; hence `T[S]` is a five-vertex
tournament of minimum out-degree at least one.  There are exactly eight such
tournaments up to isomorphism.  To state the representatives, encode the ten
pairs

```text
(01,02,03,04,12,13,14,23,24,34)
```

with `1` meaning that the lower label dominates the higher label.  The
independent orbit-expansion checker gives:

| case | decimal bits | bit word | score sequence | labeled orbit |
|---:|---:|---|---|---:|
| 0 | 2 | `0100000000` | `(1,1,1,3,4)` | 40 |
| 1 | 4 | `0010000000` | `(1,1,2,2,4)` | 120 |
| 2 | 8 | `0001000000` | `(1,1,2,3,3)` | 120 |
| 3 | 10 | `0101000000` | `(1,1,2,3,3)` | 120 |
| 4 | 12 | `0011000000` | `(1,2,2,2,3)` | 120 |
| 5 | 40 | `0001010000` | `(1,2,2,2,3)` | 40 |
| 6 | 41 | `1001010000` | `(1,2,2,2,3)` | 120 |
| 7 | 76 | `0011001000` | `(2,2,2,2,2)` | 24 |

The eight disjoint orbits contain 704 labeled tournaments, exactly the
five-vertex tournaments of minimum out-degree at least one.  Their expanded
union has SHA-256
`d96a749ce921425cf5644e3369b78c8f9828ac9f7ed99b44e3ef173e673bc299`.
Thus the strict branch consists of exactly these eight cases.

## Exact global exclusion

`generate_cases.py` imports the exact all-vertex no-strong encoding from
`strong_seymour_order15/generate_cnf.py`.  In every case it:

1. fixes an ordinary degree-seven root and a normalized minimal Hall set of
   size five;
2. adds the three clauses saying each member of `D` is reached from `C`;
3. adds the three degree-at-least-seven units from (2); and
4. adds one harmless representative arc within each still-symmetric region.

The tight case additionally fixes `p(1)+q(1)=4`.  Each strict case fixes one
of the eight displayed tournaments and enforces (3) at all five vertices.
The normalizations are complete: any tight configuration can move one tight
vertex to label 1, and every strict configuration has exactly one of the
eight displayed `T[S]` isomorphism types.

The tight formula has 20,698 variables and 47,404 clauses.  Each strict
formula has 20,741 variables and 47,509 clauses.  CaDiCaL 3.0.1 proves all
nine formulas UNSAT.  `drat-trim` independently verifies every binary DRAT
trace; every checked core contains zero RAT lemmas.  The traces total
88,525,488 bytes.  Exact per-case formula/proof hashes and core statistics
are in [`EXPECTED.json`](EXPECTED.json); the canonical verification-record
manifest has SHA-256

```text
0358a8f0b7280141575039a7a5b6a6827121695ff242f788300ba44bb9034e13
```

Every hypothetical size-five witness lies in the tight case or one of the
eight strict cases.  Since all nine are impossible, `|S|` cannot be five.
The preceding alternative `{5,6}` therefore reduces to `|S|=6`.

## Scope and trust boundary

This theorem does not settle whether every order-15 tournament has a strong
Seymour vertex.  It shows that any remaining counterexample must have a
size-six minimal deficient Hall witness at every ordinary root.

The two-branch reduction, the `D`-degree lemma, and the eight-type
classification are human-readable above.  `check_tournament_types.py`
independently verifies the finite isomorphism claim by orbit expansion.  The
global exclusion trusts the inspected base generator, PySAT's sequential
cardinality encodings, CaDiCaL, and `drat-trim`; proof checking establishes
UNSAT only for the nine exact hashed formulas.
