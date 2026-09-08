# Proof of the catalog exclusion

## Ordered tournament colorings

Let `T` be a tournament and let `<` be a linear order of its vertices.  Define
an undirected graph `G(T,<)` by declaring `{u,v}` red exactly when the arc of
`T` points from the earlier vertex to the later vertex.  Blue pairs are the
nonedges of `G`.

Fix the first vertex `r` and put `Q=N_T^+(r)`.  Every pair `{r,q}` with
`q in Q` is red.  If `G(T,<)` has no red `K5`, then `G[Q]` has no red `K4`.
If `G` has no blue `K5`, then `G[Q]` has no blue `K5`.  Thus the following is
a necessary condition for an ordered tournament coloring to be good:

> `P(T,r)`: the 21-vertex tournament `T[Q]` has a linear order whose forward
> graph contains no `K4` and whose backward graph contains no `K5`.

Consequently, proving `not P(T,r)` for every vertex `r` proves that no order
of `T` produces a good coloring.

## Exact CNF for `P(T,r)`

Number the vertices of `Q` from 0 to 20.  For each pair `i<j`, the variable
`x_ij` says `i<j`; a signed helper literal represents either comparison.
For every triple `a<b<c`, the two clauses

```text
not(a<b) or not(b<c) or (a<c)
(a<b) or (b<c) or not(a<c)
```

forbid both directed comparison cycles.  Since one Boolean comparison is
present for every pair, these clauses encode exactly the linear orders.

A four-set can be a red clique only when its subtournament is transitive.  If
its unique source-to-sink order is `v0,v1,v2,v3`, it is a red clique exactly
when the three consecutive comparisons point forward.  The certifier adds

```text
not(v0<v1) or not(v1<v2) or not(v2<v3).
```

Likewise, a five-set can be all blue only when its subtournament is
transitive.  It is blue exactly when the vertex order reverses its unique
tournament order, so the certifier forbids the four consecutive reverse
comparisons.  These clauses are necessary and sufficient because transitive
tournament arcs between nonconsecutive vertices follow from the chain.

Finally, selector `y_f` implies that local vertex `f` precedes every other
vertex, and one selector must hold.  Every linear order has a unique first
vertex, so selectors preserve satisfiability while exposing 21 complete
branches.

## Checked finite conclusion

For each of the 2,178 input tournaments and each of its 43 possible first
vertices, `certify.cpp` constructs that CNF.  It checks all 21 assumptions
`y_f` incrementally.  After an UNSAT result, CaDiCaL's `conclude()` operation
emits the negated failed-assumption core as a derived clause.  Once all
selectors have failed, the selector disjunction yields the final empty
clause.  Every assumption solve and the final solve has a separate fixed cap
of 100,000 conflicts; the completed run encountered no `SAT` and no
`UNKNOWN` result.

The program writes the original CNF and the binary DRAT stream to temporary
files.  `drat-trim` independently returned `s VERIFIED` on every one of the
93,654 streams.  Only then did the program count the instance as UNSAT and
delete its temporary files.  `RESULT.tsv` records 43 checked UNSAT formulas
for every input record.

It follows that `P(T,r)` fails for every root of every supplied tournament.
For any order, take its first vertex `r`: `G[Q]` contains either a red `K4`,
which joins `r` to form a red `K5`, or a blue `K5` already.  Hence no ordering
of any supplied tournament gives a Ramsey(5,5) graph.
