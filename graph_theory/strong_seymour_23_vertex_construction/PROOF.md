# A 23-vertex tournament without a strong Seymour vertex

Let `N++(v)` mean vertices at directed distance **exactly two** from `v`.
A vertex is strong Seymour when the bipartite arc graph from `N+(v)` to
`N++(v)` has a matching covering `N+(v)`; a sink is strong by this definition.
For `S ⊆ N+(v)`, write `Γ_v(S)` for its neighbors in that bipartite graph.
The elementary Hall obstruction `|S| > |Γ_v(S)|` proves that `v` is not strong.

**Theorem.** There is a tournament of order 23 with no strong Seymour vertex.
More generally, the 13-part construction below, with positive integer
parameters `a,b,c`, has no strong vertex whenever

    a < b < 3a,        c > max(3a, a+b).                         (1)

The sufficient statement holds for **arbitrary tournaments within the parts**.
When every part is transitive, (1) is also necessary. The unique parameter
triple of minimum order in this three-parameter class is `(1,2,4)`, of order
`9a+b+3c = 23`. No assertion of unrestricted minimality is made.

## The quotient

Replace vertex `i` of the following tournament `Q` by a part of size `w_i`;
orient all edges between two parts according to `Q`. Indices are zero-based.

| i | name | size | out-neighbors in Q |
|---|---|---|---|
| 0 | A0 | a | 7,9,10,11,12 |
| 1 | A2 | a | 0,7,8,9,10 |
| 2 | B0u | a | 0,1,3,4,7,8 |
| 3 | B0v | a | 0,1,4,7,8,11 |
| 4 | B1 | b | 0,1,5,6,9,10,11 |
| 5 | B2u | a | 0,1,2,3,6,11,12 |
| 6 | B2v | a | 0,1,2,3,7,11,12 |
| 7 | C0p | a | 4,5,8,9 |
| 8 | C0q | c | 0,4,5,6,9,10 |
| 9 | C1q | c | 2,3,5,6,10,11,12 |
| 10 | C1p | a | 2,3,5,6,7,11,12 |
| 11 | C2p | a | 1,2,7,8,12 |
| 12 | C2q | c | 1,2,3,4,7,8 |

This table contains exactly one orientation for each unordered pair. The
literal 23-by-23 matrix uses `(a,b,c)=(1,2,4)` and increasing transitive order
inside each part. Parts are concatenated in the displayed order.

## Thirteen Hall witnesses

For a quotient source set `S_i ⊆ N_Q+(i)`, put

    Γ_i = N_Q+(S_i) ∩ N_Q−(i),       d_i = w(S_i) − w(Γ_i).

Here `N_Q+(S_i)` is the union of the out-neighborhoods of its members.
The following are exact neighbor sets, as checked directly from the quotient.

| i | S_i | Γ_i | d_i |
|---|---|---|---|
| 0 | 9,10 | 2,3,5,6 | c−3a |
| 1 | 7,8 | 4,5,6 | c−a−b |
| 2 | 1,3,4,7,8 | 5,6,9,10,11 | b−a |
| 3 | 1,4,7,8 | 5,6,9,10 | b−a |
| 4 | 0,5,6,9,10 | 2,3,7,12 | a |
| 5 | 2,3,6,11,12 | 4,7,8 | 3a−b |
| 6 | 2,3,11,12 | 4,8 | 3a−b |
| 7 | 8 | 0,6,10 | c−3a |
| 8 | 0,4,5,6,9,10 | 1,2,3,7,11,12 | b−a |
| 9 | 2,3,5,6,10,11,12 | 0,1,4,7,8 | 3a−b |
| 10 | 2,3,5,6,11,12 | 0,1,4,8 | 3a−b |
| 11 | 12 | 3,4 | c−a−b |
| 12 | 1,2,3,4,7,8 | 0,5,6,9,10,11 | b−a |

Fix a vertex `v` in part `i` and take all vertices in the parts `S_i` as
its source set. Every such vertex is an out-neighbor of `v`. Its neighbors
in `N++(v)` are **exactly** the vertices in the parts `Γ_i`:

* A reached external in-part of `i` lies at exact distance two from `v`.
* External out-parts of `i` consist of vertices already in `N+(v)`.
* A source part cannot reach any vertex in part `i`, because all edges go
  from part `i` to that source part.

Thus internal edges in any part cannot alter this Hall obstruction. Under
(1), all thirteen displayed deficiencies are positive. At `(1,2,4)` they
are all exactly one. This proves the existence assertion and its arbitrary
internal-tournament extension, using only the displayed finite tables.

## Exact transitive-part classification

Let `Δ_i` be the maximum **weighted** quotient Hall deficiency, including
the empty source set. For a transitive part, a vertex with `r` later vertices
in its own part has matching deficiency

    |N+(v)| − ν(v) = r + Δ_i.                                (2)

Indeed, its `r` internal out-neighbors have no edges into `N++(v)` and are
isolated on the left of the matching problem. External left vertices in
one part are twins. In maximizing Hall deficiency, include every vertex of
each selected left part, since that does not enlarge its neighbor set.
Unreached external in-parts are isolated on the right and have no effect.
The remaining Hall problem is precisely the weighted quotient problem.
Consequently there is exactly one strong vertex in each part with `Δ_i=0`
and none in the other parts.

Here is the complete formula table. Every row denotes the maximum of its
listed expressions. Terms that are coordinatewise dominated as linear
forms in positive `a,b,c` have been removed.

| i | expressions whose maximum is Δ_i |
|---|---|
| 0 | 0, c−3a, c−2a−b |
| 1,11 | 0, c−a−b |
| 2,3 | 0, b−a, b−c, a−2c |
| 4 | a, 3a−c |
| 5,6 | 0, a−c, 2a−2c, 3a−b, 4a−b−c |
| 7 | 0, b+c−5a, c−3a |
| 8,12 | 0, b−a |
| 9 | 0, a−c, 3a−b |
| 10 | 0, a−c, 3a−b, 4a−b−c |

For completeness, this is a finite symbolic Hall calculation, not an
inference from numerical parameter samples. For each root enumerate every
nonempty subset of its quotient out-neighbors. Replace each source by all
out-neighbors whose in-part neighbors are contained in its neighbor set.
This closure does not change the target and can only increase the source
weight. The complete list comprises 110 nonempty closed rows, obtained from
995 nonempty subsets. `certificate.json` gives every source, target, and
coefficient triple; `verify.py` exhausts the subsets and checks the list and
the displayed coordinatewise maxima with exact integers. Empty sources
supply zero. This argument proves completeness for **all** positive
parameters; the independent finite parameter audit is additional evidence.

If there is no strong vertex, `Δ_8>0` gives `b>a`, and `Δ_1>0` gives
`c>a+b`. In particular `c>a`, so `Δ_9>0` forces `b<3a`. As `b>a`, the
term `c−2a−b` is smaller than `c−3a`, and `Δ_0>0` forces `c>3a`.
These are exactly (1); sufficiency was already proved by the Hall table.

For integer parameters satisfying (1), `b≥a+1` and `c≥3a+1`, whence

    9a+b+3c ≥ 19a+4 ≥ 23.

Equality forces `(a,b,c)=(1,2,4)`, which satisfies (1).

## A certificate-cone minimum with arbitrary part sizes

This additional statement concerns the **selected thirteen Hall rows**,
not all possible Hall witnesses on this quotient. Let `M` be the 13-by-13
matrix whose row `i` is `+1` on `S_i`, `−1` on `Γ_i`, and zero elsewhere.
With unrestricted positive integer part weights `w`, the same certificate
works whenever `Mw≥1` coordinatewise. The exact identity

    (51,31,37,148,162,1,131,1,100,1,132,37,88) M
        = 40 (1,1,1,1,1,1,1,1,1,1,1,1,1)

has positive coefficients summing to 920. Thus `sum(w)≥920/40=23`.
Equality implies every row of `Mw` is one. Since `det(M)=40`, the solution
is unique, namely `(1,1,1,1,2,1,1,1,4,4,1,1,4)`. Both the identity and
the determinant are checked with exact rational arithmetic. This does not
prove that other Hall choices on the quotient, or other tournaments, need
at least 23 vertices.

## Relation to the preceding construction

The starting nine-part quotient is Gibbons's prior `D0`, in the cyclic
labels used by the preceding 24-vertex construction. Its three layers
`A_i,B_i,C_i` each form a directed 3-cycle, with `B→A`, `C_i→A_i`,
`A_i→C_j` for `i≠j`, `B_i→C_i`, and `C_i→B_j` for `i≠j`.

Remove `A1`. Split `B0` and `B2` into two parts in transitive order.
Split `C0` into `(C0p,C0q)`, `C1` into `(C1q,C1p)`, and `C2` into
`(C2p,C2q)`, also in transitive order. In the resulting 13-part quotient,
reverse the five arcs on unordered pairs

    {0,7}, {6,7}, {7,10}, {3,11}, {4,11}.

This gives exactly the quotient above. At the smallest weights these are
six vertex-edge reversals after deleting `A1` from the 24-vertex example;
the pair `{4,11}` accounts for two edges. The resulting example therefore
escapes the unchanged nine-part weight cone whose minimum was 24.
The separate checker constructs the entire family by this surgery rule,
without importing the quotient table or primary constructor.

The original heuristic witness used different internal edges in some
homogeneous parts. The arbitrary-part theorem justifies replacing them
by transitive parts in the canonical literal matrix published here.

Finally, adjoining any number of new vertices in a transitive prefix,
all dominating the construction, gives a no-strong tournament at every
order `n≥23`. Old matching links are unchanged. Each new vertex has a
nonempty out-neighborhood and empty exact second out-neighborhood.

## Scope and trust

The upper bound has the direct Hall proof above. The universal
classification uses the finite symbolic table and Hall's theorem, with
complete exact source attached; it is not formally verified in a proof
assistant. The separate literal check uses exact-distance sets, iterative
augmenting paths, and all 62,464 Hall subsets. It also checks (2) on all
216 triples `1≤a,b,c≤6`, covering 9,828 vertices. These are implementations
by the author, not independent peer review.

Heuristic search and solver outcomes are outside the proof boundary.
The package establishes an upper bound of 23, not nonexistence at 22.
Combined with the separately accepted order-at-most-15 result, the current
graph-supported interval is `16≤m≤23`; that imported lower-bound proof is
not replayed here. This construction is not regular and does not settle
the strong-Seymour question for regular tournaments. Prior sources and
the precise novelty scope are recorded in [SOURCES.md](SOURCES.md).
