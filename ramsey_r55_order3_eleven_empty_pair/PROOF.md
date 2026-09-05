# A sharp common-neighbor bound for an empty-signature blue edge

## Standalone lemma

Let a red/blue complete graph have no monochromatic K5. Let C0,C1,C2
be three disjoint red triangles, and let F be an outside set whose
vertices are uniform to each Ci. Write

```text
S(f) = {i : f is red to Ci}.
```

Suppose u,v in F have empty signatures and uv is blue. Put

```text
W = {w in F minus {u,v} : uw and vw are blue}.
```

Then:

1. Every w in W has at least two elements in S(w).
2. W is a blue clique and has at most two vertices.
3. No two vertices of W omit the same minority triangle from their signatures.

These statements require neither a degree bound nor an automorphism.

To prove the first statement, suppose w misses distinct Ci,Cj. There
is a blue edge ab between Ci and Cj: otherwise their union would be a
red K6. The five vertices u,v,w,a,b would be pairwise blue, a
contradiction.

Any two subsets of {0,1,2} of size at least two intersect. Thus any
w,w' in W are both red to some Ci. A red edge ww' would complete a
red K5 with Ci, so ww' is blue. Three vertices of W would consequently
form a blue K5 with u,v. This proves the second statement. If w,w'
both miss Ci, their blue edge, the blue edge uv, and any vertex of Ci
likewise give a blue K5. This proves the third statement.

In addition, if T is any blue triangle disjoint from u,v and uniform
to both, it cannot be blue to both: T together with u,v would be a
blue K5. This elementary consequence will be used for the other moving
triangles in the application.

## Sharpness and the necessary blue-edge hypothesis

Use either of the inherited nine-vertex minority cores:

```text
class 11: red offset words 100,110,110 on pairs 01,02,12;
class 13: red offset words 110,110,101 on pairs 01,02,12.
```

The vertices of triangle i are 3i+s, with s modulo three. Between
triangles i<j the bit in position t-s modulo three specifies the edge
color. Adjoin fixed vertices 9,10,11,12 with signature masks
`0,0,3,5`, where mask bit i means red to Ci. Make every edge among
these four new vertices blue. The literal edge lists `core11.edges`
and `core13.edges` give graphs on 13 vertices with respectively 36 and
39 red edges, no monochromatic K5, and exactly two common blue fixed
neighbors of the empty blue pair 9,10. Thus the bound two is sharp,
even under the order-three action on either residual minority core.

The edge lists are compact certificates. `inspect_fixtures.py` checks
all 1287 five-sets and all 78 action pairs in each, plus their core
words, signatures, uniformity, pair color, and common neighbors.

The blue-edge hypothesis is essential. Starting with class 11, adjoin
five vertices with masks `0,0,3,5,6`. Color the edge between the two
empty-signature vertices red, and all other edges among the five new
vertices blue. The resulting `red_pair14.edges` has 14 vertices, 43
red edges, and no monochromatic K5, but the red empty pair has three
common blue fixed neighbors. Its independent inspector checks all
2002 five-sets and all 91 action pairs. This disproves an extension of
the bound to a red pair. None of these small witnesses is a 43-vertex
Ramsey construction.

## Complete pair-color split in the eleven-cycle application

The independently accepted earlier reduction concerns a hypothetical
Ramsey (5,5;43) graph with action `1^10 3^11`, three internally red and
eight internally blue moving triangles. It leaves classes 11 and 13,
and forces at least two fixed vertices with empty minority signatures.
The parent already sorts complete fixed attachment signatures
lexicographically with minority bits first. Hence vertices u=33,v=34
both have empty signatures. This is inherited ordering, with no new
normalization imposed here.

For each core, uv is either red or blue. These are disjoint and cover
all possibilities, giving exactly four full extension cases. The
color of the pair is not inferred from the local lemma. In particular,
the lemma is used only in the blue branches.

Let e(a,b) be the primary red edge bit between fixed vertices and
l(i,f) the primary red attachment bit between Ci and fixed f. Then
e(33,34)=166 and l(i,f)=211+11*(f-33)+i. Starting from each complete
reviewed many-empty base, append the following primary clauses in the
blue branch:

- `-e(u,v)` (one clause).
- `l(i,u) OR l(i,v)` for the eight blue moving triangles.
- `e(u,f) OR e(v,f) OR l(i,f) OR l(j,f)` for each other fixed f and
  each pair of distinct minority indices (24 clauses).
- For each triple of other fixed vertices, the disjunction of all six
  e(u,f),e(v,f) bits (56 clauses).
- `e(u,f) OR e(v,f) OR e(u,g) OR e(v,g) OR l(i,f) OR l(i,g)` for each
  pair of other fixed vertices and each minority index (84 clauses).

The third family says a common blue neighbor cannot miss two
minorities. The fourth forbids three common blue fixed neighbors.
The fifth forbids two of them missing the same minority. The hand
proof above establishes each family. There are 173 appended clauses
in total, including the pair-color unit, and no auxiliary variables.
The red branch appends only the single unit e(u,v).

## Audited formulas and bounded outcome

Every case retains its complete 34268-variable, 617207-clause
many-empty base. The base itself is regenerated from the accepted
615572-clause parent, including both degree bounds, all projected
five-set conditions, counters and justified normalization, followed by
the accepted core/signature and second-empty-row consequences. The
parent's degree window uses R(4,5)=25. Each intermediate hash matches
the corresponding accepted input. Red branches have 617208 clauses;
blue branches have 617380, all at 34268 variables.

The separate inherited C++ checker reconstructs every parent clause.
`pair_audit.py` recovers all 320 primary variables from actual pair
orbits, independently constructs the new clauses, and compares the
complete original prefix, every appended clause, and EOF. The local
intersection argument and each abstract clause family's truth table
are checked separately. Five malformed formulas and three malformed
fixtures are rejected. Normal and optimized Python controls agree.

All four complete extension tests returned explicit UNKNOWN after
60-second solver limits. Fresh verification regenerates and audits
the entire chain and all four final formulas. **No additional core,
pair color, or full extension is excluded by this pass.** There is no
successful UNSAT trace to replay, and partial UNKNOWN traces are not
certificates or resumable solver states. The new lemma is proved by
the hand argument and its sharpness by the small edge lists, not by
the UNKNOWN computations.

Both residual three-versus-eight cores and the four-versus-seven split
remain open; the minimum moving count remains eleven. No target graph
or Ramsey lower-bound improvement follows. The complete bounded
milestone ends here, before another split or proof phase.
