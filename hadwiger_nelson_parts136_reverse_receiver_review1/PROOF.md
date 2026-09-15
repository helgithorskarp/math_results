# Proof architecture for the reverse receiver review

Let `P` be the complete strict unit graph on the 509 published Parts points,

```text
H = {0} union {374,...,508},       D = {1,...,373}.
```

The review independently proves the geometry, the exact four-colour boundary
relation of `H`, non-four-colourability of `P`, and the receiving consequence.

## Exact physical cut

Each coordinate is represented in the nested quadratic tower

```text
Q -> Q(sqrt(3)) -> Q(sqrt(3),sqrt(5))
  -> Q(sqrt(3),sqrt(5),sqrt(11)).
```

This differs from both multiplication routes in the target. Squaring every
one of the 129,286 coordinate differences recovers 2,442 unit pairs. Their
complete split is 564 inside `H`, 1,836 inside `D`, and 42 across the cut.
The host endpoints of the cross edges are exactly the 19 listed boundary
vertices `B`, and `B` has no internal host edge. Entry-level hashes of all
four edge streams agree with a separately generated target geometry file.

Consequently every parent edge is either internal to `H`, internal to `D`, or
one of the recorded `B`--`D` cross edges. This is the geometric premise of the
later gluing argument; no intended-edge list or abstract graph is substituted.

## What the relation means

Let `R_H` be the set of restrictions to `B` of all ordinary proper
four-colourings of `H`, modulo global colour renaming. Every orbit has a
representative with vertex 0 coloured 0. The residual six permutations of
colours 1, 2 and 3 act on these normalized patterns; the lexicographically
least image is the canonical representative.

The independent Glucose 4 enumeration uses two Boolean bits per host vertex.
For a vertex `v` and colour `c`, the two-literal disjunction
`different(v,c)` is true exactly when the encoded two-bit colour of `v` is not
`c`. For every unit edge `uv` and colour `c`, the clause

```text
different(u,c) or different(v,c)
```

forbids both endpoints from receiving `c`. Four such clauses are equivalent
to the ordinary inequality constraint. Two unit clauses fix vertex 0 to
binary `00`. Exhaustive local truth tables in the checker verify both claims.

Whenever the solver supplies a host colouring, the review canonically renames
it, records the complete 136-symbol word, and blocks all six residual colour
images of its boundary pattern. The run terminates UNSAT after 41,025 orbits.
The sorted pattern stream is byte-identical to the target hash. Every new host
word is checked literally against all 564 host edges and restricts to its
claimed pattern. Only 738 of the 41,025 independently generated words equal
the author's words; the remaining 40,287 give different positive witnesses.

The palette histogram is 7 patterns using two colours, 1,500 using three, and
39,518 using four. A pattern using `k` colours has

```text
24 / (4-k)!
```

fully labelled images, because permutations of the unused colours stabilize
it. Summing gives 984,516, not `24*41,025`; the target's count correctly
accounts for the seven two-colour stabilizers.

## Independently checked completeness certificate

The terminal result of an incremental enumerator is useful corroboration but
is not the retained negative certificate. The review regenerates one binary
CNF from the complete positive relation. It contains 272 variables and
248,408 clauses: four clauses for each of 564 host edges, two origin-fixing
clauses, and six boundary-blocking clauses for each canonical row.

If this CNF were satisfiable, decoding its bits would give a proper host
four-colouring whose canonical boundary pattern is absent from the table.
Conversely every omitted host pattern would satisfy it. Thus UNSAT is exactly
relation completeness. CaDiCaL 1.9.5 emits a DRAT trace and `drat-trim`
checks that trace. The bulky instance, trace and logs remain in authorized
scratch; hashes and checker metadata are retained in the compact package.

This is structurally independent of the target's 544-variable one-hot CNF.
The target's own 249,359-clause proof is also replayed, but is not the sole
basis of the verdict.

## Parent obstruction and gluing

The same two-bit encoding of the complete parent has 1,018 variables and
9,770 clauses. Its checked UNSAT certificate proves that `P` has no proper
four-colouring. The literal published five-word is proper on every one of the
2,442 reconstructed unit edges, so `P` is exactly five-chromatic.

Fix any pattern in `R_H`. If the graph on `D union B` had a proper
four-colouring agreeing with a host witness on `B`, the two assignments would
glue: all parent edges are covered by the exact cut decomposition. This would
four-colour `P`, contradicting the checked parent certificate. Hence the
original 373-point module blocks every host pattern.

## Receiving criterion and limits

For an exact replacement with distinct new physical points `X` outside `H`,
the total graph has `136+|X|` points, so a sub-509 candidate requires
`|X|<=372`. If the replacement lists the 19 shared pins, it has at most 391
displayed vertices including them.

Provided the replacement shares only `B` with `H` and every new--host edge is
incident with `B`, the union is four-colourable exactly when the two full
boundary relations intersect after a common colour normalization. Therefore
empty relation intersection is necessary and sufficient for a frozen exact
replacement in that interface model.

This theorem does not supply such a replacement or a finite coordinate pool.
If a proposed replacement coincides with another host point or creates a unit
contact to `H` outside `B`, the 19-pin table is insufficient: enlarge the
physical interface or check the whole collision-merged graph. Any candidate
also needs a proper five-colour word and independently checkable ordinary
non-four evidence. The receiver itself is not a record construction.
