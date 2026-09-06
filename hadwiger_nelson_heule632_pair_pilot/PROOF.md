# Exact five-chromatic seed certificate

Let P be the ordered 632-point set defined in the README, and let
G be its full unit-distance graph after deleting labels 399 and 462.
The claim is `|V(G)| = 630`, `|E(G)| = 3098`, and `chi(G) = 5`.

## Geometry

The square classes of 3, 5 and 11 are independent over the rationals.
Consequently the eight squarefree radicals indexed by subsets of these
three primes form a basis of `Q(sqrt(3),sqrt(5),sqrt(11))`.
For integer coefficient vectors A and B representing coordinates scaled by
96, squared Euclidean distance is computed in that basis without rounding.
For squarefree r and s,

```
sqrt(r) sqrt(s) = gcd(r,s) sqrt(rs/gcd(r,s)^2).
```

Thus distance is exactly one if and only if its scaled squared-distance
vector is `(9216,0,0,0,0,0,0,0)`. Distinct coefficient pairs give distinct
Euclidean points. Both implementations enumerate every unordered point
pair, confirm 632 distinct points and 3,112 edges, and restrict the complete
edge list after the two deletions. This yields exactly 630 vertices and
3,098 unit edges. Missing geometric incidences are excluded by the complete
enumeration, although only verified unit edges would be necessary for the
chromatic lower bound.

## CNF equivalence

For each retained vertex v and colour c in `{0,...,k-1}`, introduce a Boolean
variable `x(v,c)`. Add one clause requiring at least one colour and all
pairwise clauses forbidding two colours at the same vertex. For every unit
edge uv and every c, add `not x(u,c) or not x(v,c)`.

These clauses are satisfiable exactly when G has a proper k-colouring:
a satisfying assignment chooses exactly one colour per vertex and gives
different colours to every adjacent pair; conversely, any proper colouring
defines such an assignment.

The lexicographically first retained triangle is `(0,143,146)`.
Pin its vertices to colours 0, 1 and 2 respectively. For k at least three,
these three vertices receive distinct colours in any proper colouring,
and a global permutation of the palette realizes the pins. The pins
therefore preserve satisfiability. This permutation argument is essential
for concluding unpinned non-four-colourability from the pinned refutation.

For k = 4 the formula has

```
4*630 = 2520 variables,
630*(1+6) + 4*3098 + 3 = 16805 clauses.
```

The direct verifier reconstructs this exact formula independently and checks
the binary DRAT proof against it. `drat-trim` returns exit code zero and the
exact line `s VERIFIED`; the checker-completeness flag is not inferred from
a substring or the solver status. By soundness of checked DRAT refutations,
the formula is unsatisfiable. The encoding equivalence gives `chi(G) >= 5`.

## Upper bound

The `five_colouring` field of `certificate.json` gives one symbol at every
host position, using digits 0 through 4 and dots exactly at positions 399
and 462. The verifier checks length, alphabet, exact omission set, and
distinct colours on all 3,098 retained edges. It is therefore a proper
five-colouring of G, proving `chi(G) <= 5`. Combining the bounds proves
`chi(G) = 5`.

## Experiment scope

The five earlier SAT models prove only the four-colourability of their
stated pair-deleted supports. The selection of 24 pairs is a frozen heuristic
sample from 118,828 remaining old pairs. It is not an enumeration modulo
automorphisms, and the 18 unattempted cases carry no verdict.

No conclusion about a 508-vertex subgraph follows from the 630-vertex
refutation. Any subsequent lower-bound claim on a smaller graph requires a
new checked refutation for that graph. A five-colouring can be restricted
from this certificate to prove its upper bound.
