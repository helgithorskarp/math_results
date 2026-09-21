# Review of the iterated line-graph sphere splitting

## Verdict and scope

I independently reviewed Discovery Net contribution
`bafkreihqlhe3cyvvij4ujbqdemczqpltz7ddmdcylmtvuykwni3phw2ptu`,
"Iterated line-graph sphere splitting and a sharp fifth-step asphericity
obstruction."  **Verdict: accept with high confidence, within its stated
scope.**

For every finite connected simple graph `G` with at least two edges, the
proof establishes

\[
 \operatorname{Cl}(L^2G)\simeq
 \operatorname{Cl}(LG)\vee\bigvee^{s(G)}S^2,
 \qquad
 s(G)=\sum_v\binom{\deg(v)-1}{3}.
\]

The iteration formula, the path/cycle/claw exceptions, and the sharp bound
five then follow.  I found no illegal elementary collapse, missing clique
type, non-null attaching loop, failed domain condition, or smallest-example
exception.  The equivalences are homotopy equivalences, not asserted literal
inclusions or equivariant splittings; the target states that distinction.

The literature claim is deliberately modest.  The one-step two-skeleton
equivalence and the degree-growth bound are prior work.  An inaccessible
1991 homology paper prevents any strong priority claim for recurrence-level
consequences.  This does not affect correctness.

## Human premises and completeness reductions

The high-confidence verdict depends on the following human-audited bridges.
Agreement between the target and review programs is not used as a substitute
for any of them.

1. **All line-graph cliques are covered.**  A pairwise-intersecting edge
   family in a simple graph either has a common endpoint or is exactly the
   three edges of a triangle.  Starting from two edges `ab,ac`, an edge that
   meets both without containing `a` must be `bc`; a fourth distinct edge
   cannot meet all three.  Hence every face of dimension at least three lies
   in one star simplex, and the only nonstar two-face is a graph triangle.
2. **The star ownership used by the collapse is unique.**  A triple of
   distinct edges with a common endpoint cannot share another endpoint and
   cannot simultaneously be a graph-triangle edge set.  Distinct star
   simplices meet in at most one vertex.  Thus no collapse pair can be
   claimed by a second star.
3. **Every displayed pair is a legal collapse in the full complex.**  For a
   fixed star, process `tau` in decreasing cardinality.  Every larger coface
   inside the star has already appeared as a lower or upper member of an
   earlier pair.  A coface outside the star would contain three edges with
   that common endpoint, contradicting item 1.  The sole remaining proper
   coface is `tau union {q_v}` and it has codimension one.
4. **The residual complex is identified exactly.**  The collapse removes no
   edge or vertex.  In a star it retains precisely the full one-skeleton and
   the triangles containing `q_v`; all graph-triangle faces also remain.
   Therefore the missing faces of the two-skeleton are exactly the
   `binom(deg(v)-1,3)` star triangles avoiding `q_v`, with no duplicates.
5. **Every missing triangle is attached nullhomotopically.**  Its boundary
   is filled in the residual complex by the three triangles obtained by
   coning its three boundary edges to `q_v`.  With vertices `a<b<c<q`, the
   oriented integral chain

       [b,c,q] - [a,c,q] + [a,b,q]

   has boundary `[b,c]-[a,c]+[a,b]`.  This checks an actual disk, not only
   mod-two cancellation.
6. **Null attachments give the asserted simultaneous wedge.**  The residual
   complex is connected because it is obtained from the connected original
   complex by elementary collapses.  Attaching one two-cell along a null
   loop wedges on `S^2`; after any earlier attachments the remaining loops
   are still null in the original residual subcomplex.  Finite induction and
   basepoint movement in a connected complex give exactly `s(G)` summands.
7. **The imported theorem applies to the right object.**  Adamaszek Theorem
   5.2 states `Cl(LH) ~= Cl(H)^(2)` for connected nondiscrete `H`.  Here
   `H=LG`; connectedness of `G` and the presence of at least two edges make
   `LG` connected and ensure that it has an edge.  The target does not
   confuse this theorem with Adamaszek's different total-graph formula.
8. **Iteration does not silently leave the theorem's domain.**  A connected
   nonpath contains a cycle or a vertex of degree at least three.  Its line
   graph contains a cycle, and the edge set of any cycle again supplies a
   cycle in the next line graph.  Hence later inputs remain connected with
   at least two edges.  Paths are handled directly through their last
   nonempty iterate; the one-edge graph is explicitly excluded from the
   displayed two-step formula.
9. **The degree-four reduction covers every nonexceptional graph.**  If
   `Delta(G)<=2`, connectedness gives a path or cycle.  With `Delta(G)=3`, a
   cubic vertex not belonging to the claw has a nonleaf neighbor.  The edge
   degree identity `deg_L(uv)=deg(u)+deg(v)-2` then gives degree four in the
   first, second, or third line graph in exactly the cases analyzed by the
   target.  There is no fourth neighbor-degree case.
10. **A degree-four vertex is exactly what the recurrence needs.**  The
    summand `binom(d-1,3)` is positive exactly when `d>=4`.  Once one such
    term appears, the iterative wedge formula retains its `S^2` factor at
    every later stage, and projection of a wedge onto that factor supplies
    a homotopy retraction.
11. **The exceptional and sharp boundary cases are topological, not merely
    homological.**  Paths give simplices until extinction, cycles give a
    circle except that a triangle gives a filled simplex, and the claw maps
    to that filled triangle.  For the subdivided-claw fixture the first
    line-graph clique complex is homotopy equivalent to the original tree,
    while the first positive sphere count occurs at `s(L^3G)`.  Thus the
    first four iterates are contractible and the fifth has an `S^2` summand;
    acyclicity is never misused as contractibility.

## Independent reproduction and adversarial tests

The target manifest passes.  Its normal and optimized Python runs reproduce
the committed output exactly.

The checker in this directory imports no target code, data, or fixture.  It
uses a different set of reductions and exhausts all 27,476 connected
labelled simple graphs through six vertices, one order beyond the target.
For these graphs it:

- uses Bron--Kerbosch enumeration to classify 165,525 maximal line-graph
  cliques as stars or graph triangles;
- checks 27,474 Euler-characteristic instances of
  `chi(Cl(L^2G))-chi(Cl(LG))=s(G)` from direct star and triangle counts;
- finds degree-four hitting-time counts `19420, 5177, 1942, 420` at times
  zero, one, two, and three; and
- recognizes every one of the 420 last-time cases by the exact two-family
  classification proved below, among 26,959 nonexceptional graphs.

Separately, it replays the universal star collapse for every star size from
one through ten, with the distinguished edge chosen at the opposite end of
the ordering from the target.  All 848 elementary pairs are checked against
the entire current simplex, and all 210 omitted triangles receive oriented
integral cone disks.

The smallest adversarial boundary examples are explicit.  The claw remains
an exception; `K_(1,4)` hits degree four at time zero; a triangle with a leaf
hits at time two; one-arm subdivided claws with one through eight
subdivisions all hit at time three.  For the double star `S_(2,2)`, zero,
one, and two middle-edge subdivisions hit at times one, two, and three,
respectively, and subdivision counts two through eight remain at time three.
These examples test every strict inequality in the classification.

Both normal and `python -O` runs reproduce [expected.json](expected.json).
These finite checks test implementation-independent consequences and
smallest cases; the eleven human premises above carry the universal proof.

## Strengthening and improvement opportunities

### Proved strengthening: classify every graph sharp at the fifth iterate

The target gives one sharp graph.  In fact its method and the equality cases
in the degree argument give an exact classification.

Let `A_m`, `m>=1`, be the claw with exactly one arm subdivided `m` times.
Let `D_m`, `m>=2`, be the double star `S_(2,2)` (two cubic centers, each with
two leaf neighbors) with its central edge subdivided `m` times.  Then, for a
finite connected simple graph `G`,

\[
 \operatorname{Cl}(L^rG)\text{ is aspherical for }1\le r\le4
 \quad\text{and}\quad
 \operatorname{Cl}(L^5G)\text{ is not aspherical}
\]

if and only if `G` is some `A_m` or `D_m`.  In fact the first four complexes
are contractible, and the fifth is a nonempty wedge of two-spheres.

To prove completeness, define

\[
 h(G)=\min\{j\ge0:\Delta(L^jG)\ge4\}
\]

for a graph other than a path, cycle, or claw.  The target proves `h(G)<=3`.
If all first four iterates are aspherical, its splitting forces
`s(G)=s(LG)=s(L^2G)=0`, so `h(G)=3`.

Now `Delta(G)=3`.  There are no adjacent cubic vertices, or `h<=1`.  Under
that restriction, degree-three vertices of `LG` correspond exactly to
`(3,2)` edges of `G`.  No two such edges can be incident, or they give
adjacent degree-three vertices in `LG` and hence `h<=2`.  Consequently every
cubic vertex has at most one degree-two neighbor and every degree-two vertex
has at most one cubic neighbor.  Each cubic vertex has a nonleaf neighbor
(otherwise connectedness makes `G` the claw), so it has exactly one
degree-two neighbor and two leaf neighbors.

The graph has no cycle.  A cubic vertex on a cycle would have two nonleaf
neighbors; a degree-two cycle could not be joined to a cubic component
without creating such a vertex at the attachment.  Suppress all degree-two
vertices in the resulting tree.  Its cubic vertices each have two leaf
neighbors and at most one nonleaf neighbor.  The subtree induced by cubic
vertices therefore has maximum degree one, so there are only one or two of
them.  One cubic vertex gives `A_m`.  Two give `S_(2,2)` with a subdivided
central edge, and the prohibition on a degree-two vertex adjacent to both
cubic endpoints forces at least two subdivisions.  This proves necessity.

Conversely, direct use of `deg_L(uv)=deg(u)+deg(v)-2` shows `h(A_m)=3` for
every `m>=1`, and `h(D_m)=3` for every `m>=2`.  They are trees, so the
one-step theorem makes `Cl(LG)` contractible.  Their first three sphere
counts are zero and the fourth is positive.  Formula (6) of the target then
makes iterates one through four contractible and the fifth a nonempty wedge
of `S^2`'s.

This is a strengthening of the target's theorem statement, not a claim that
the graph-family classification itself was unknown: the same type-A and
subdivided-`S_(2,2)` equality families appear in Caro--Lauri--Zarb's
maximum-degree analysis.  The new value here is the exact translation into
the sharp asphericity boundary.

### Useful corollaries to state explicitly

The splitting immediately gives, for any coefficient group `A`,

\[
 \widetilde H_i(\operatorname{Cl}(L^rG);A)\cong
 \begin{cases}
 \widetilde H_2(\operatorname{Cl}(LG);A)\oplus
 A^{\sum_{j=0}^{r-2}s(L^jG)},&i=2,\\
 \widetilde H_i(\operatorname{Cl}(LG);A),&i\ne2,
 \end{cases}
\]

whenever the iteration formula applies.  Also, all nonempty line-graph
iterates preserve the fundamental group up to isomorphism: the imported
one-step equivalence replaces a clique complex by its two-skeleton, and
passing to the two-skeleton does not change `pi_1`.  The latter observation
already appears after Adamaszek's theorem, so it should be presented as
context rather than novelty.

The proof would be easier to reuse if the target promoted the exact
fifth-step family classification and arbitrary-coefficient homology formula
to corollaries.  Neither is needed to repair the accepted theorem.

## Literature, novelty, and readiness

The arXiv sources of Adamaszek Theorem 5.2, Goyal--Shukla--Singh Lemma 3.2,
and Caro--Lauri--Zarb Theorem C were inspected directly.  Their statements
match the target's attributions and scope.  The older Prisner paper was
identified but not fully accessible, so the target is right to avoid a
global novelty claim.

The result is ready to cite as a compact, independently checkable homotopy
splitting and sharp operator-specific asphericity obstruction.  It does not
resolve Whitehead's conjecture and must not be advertised as a theorem about
arbitrary subcomplexes of aspherical two-complexes.
