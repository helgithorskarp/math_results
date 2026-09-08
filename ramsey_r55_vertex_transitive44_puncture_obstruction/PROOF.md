# Proof of the vertex-transitive(44) puncture exclusion

Call a graph *good* if it has neither a clique of size five nor an independent
set of size five.  Equivalently, its red/blue edge coloring has no
monochromatic five-set.

## Lemma 1: transitive puncture equivalence

Let `G` be a graph on `n>5` vertices and suppose a group `A <= Aut(G)` acts
transitively on its vertices.  For every vertex `v`, the graph `G-v` is good
if and only if `G` is good.

One direction follows because goodness is hereditary.  Conversely, suppose
`F` is a monochromatic five-set in `G`.  For uniform `a in A`, double counting
the pairs `(a,u)` with `a(u)=v` gives

```text
Pr[v in aF] = |F|/n = 5/n < 1.
```

Thus some automorphic image `aF` avoids `v`.  It has the same color as `F` and
is a monochromatic five-set in `G-v`.  Apply this with `n=44`.

## Lemma 2: the orbital formula is exact

Fix a permutation group `A` on `[44]`.  An `A`-invariant graph is constant on
each `A`-orbit on unordered pairs.  Conversely, every choice of one color for
each unordered-pair orbit defines an `A`-invariant graph.

Give orbit `o` a Boolean variable `x_o`, with one meaning red.  If a physical
five-set `S` meets the orbit set `O(S)`, then `S` is all blue exactly when all
`x_o`, `o in O(S)`, vanish, and it is all red exactly when all those variables
are one.  The clauses

```text
vee_{o in O(S)} x_o,          vee_{o in O(S)} not x_o
```

exclude precisely these two cases.  Taking the clauses over all physical
five-sets is therefore sound and complete for good `A`-invariant graphs.
Any UNSAT subset of these physical clauses is already an exclusion proof.

## Lemma 3: maximal labeled refinements cover the catalog

Let `P` and `Q` be partitions of the same 946 unordered pairs, and suppose
`Q` refines `P`.  A coloring constant on every `P`-cell is constant on every
`Q`-cell.  Hence the invariant-coloring family for `P` is contained in the
family for `Q`.  If the formula for `Q` is UNSAT, so is the family for `P`.

The committed catalog has 2,113 actions and exactly 250 distinct labeled pair
partitions.  Direct comparison leaves 199 partitions that admit no strict
refinement among those 250.  Every one of the 250 is refined by at least one
of these 199.  This is recomputed from the generators by `verify.py`; no group
inclusion or isomorphism heuristic is used.

## Lemma 4: all 199 maximal families are excluded

Catalog entries 1 through 4 have generated group order 44, act transitively on
44 points, and have no nonidentity fixed points.  They are regular actions.
An invariant graph for a regular action is a Cayley graph on the acting group.
The complete Cayley(44) result cited in the README excludes all four groups of
order 44, hence these four maximal families.

For each of the other 195 maximal partitions, `certificates.json` lists actual
five-sets and a color.  The verifier reconstructs the orbit support of every
record and converts it to the corresponding clause from Lemma 2.  Its exact
tuple-clause DPLL returns UNSAT for every core.  There are 15,643 clauses in
total and no unverified solver output.  Therefore all 195 families are empty.

Lemmas 3 and 4 exclude every invariant graph for every catalog action.

## Theorem

There is no good vertex-transitive graph on 44 vertices, and no one-vertex
puncture of a vertex-transitive graph on 44 vertices is good.

If a vertex-transitive graph `G` existed, its transitive automorphism group,
after relabeling, would be one of the degree-44 transitive permutation groups
covered by the TransGrp catalog.  Lemmas 2--4 exclude it.  Lemma 1 then gives
the puncture statement.

The theorem is conditional only on the catalog-completeness trust boundary
stated in the README.  It says nothing about arbitrary 43-vertex graphs and
does not prove `R(5,5) >= 44`.
