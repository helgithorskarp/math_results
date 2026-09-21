# Review: relative collapse and Whitehead inheritance for vertex inflations

## Verdict

**Accept with high confidence.**  For a finite simplicial complex of dimension
at most two, the three stated local conditions are necessary and sufficient for
the claimed triangle/free-edge collapse relative to the canonical original
copy.  The proof that one fixed collapse sequence restricts to every
subcomplex is valid.  The spherical obstructions and the graph-of-spaces step
then give both the asphericity criterion and the Whitehead-subcomplex
inheritance equivalence.

The reviewed graph contribution is
`bafkreic22k3ovkb62d6g2oksks6f6welimwcmtvaabbveahg6c2o3zqosi`; its fixed
source commit is `a6a62ac2cf8f69655c1090b3a8e48cbc1b1b8671`.  The absolute
homotopy decomposition of a vertex inflation is classical.  The accepted
increment is the explicit relative collapse, its hereditary replay on arbitrary
subcomplexes, and the resulting operation-specific Whitehead statement.  This
does not resolve Whitehead's general conjecture.

## Human premises and completeness reductions

The verdict depends on the following premises and reductions.  They were
audited separately; program agreement is not being used as a substitute for
case-space completeness.

1. **The objects and quantifiers are literal.**  Complexes are finite abstract
   simplicial complexes of dimension at most two, multiplicities are positive,
   and `Y` ranges over all subcomplexes, not merely full or induced ones.
   Disconnected and empty complexes are interpreted componentwise as stated.
2. **Adding one copied vertex is exactly a cone attachment.**  Immediately
   before a new copy `a` of `v` is inserted, all new faces containing `a` form
   `a*L`, where `L` is the link of `v` inflated by the multiplicities already
   present among its neighbours.  No face can contain two copies of `v`.
3. **The three hypotheses exhaust cyclic prospective links.**  The base link is
   a forest by condition 1.  An already duplicated neighbour `u` has degree in
   `lk_K(v)` equal to the number of triangles on `uv`, hence at most one by
   condition 2.  An edge in the link with both endpoints already duplicated
   would make a triangle whose three originals lie in `S`, contrary to
   condition 3.
4. **The inflated-forest lemma has no omitted case.**  Replacing isolated
   vertices by isolated copies and leaves by parallel leaves preserves a
   forest.  The degree-at-most-one hypothesis prevents duplication inside a
   branching vertex, and the nonadjacency hypothesis prevents an inflated
   single edge from becoming a cyclic complete bipartite graph.
5. **Reverse order covers every new triangle once.**  Every triangle outside
   the original copy contains a unique latest-added copied vertex.  Triangles
   involving still later copies have already disappeared when that vertex is
   processed.  Earlier radial edges were not deleted by a later cone collapse,
   because that later collapse removes an edge incident to its own apex.
6. **Leaf peeling gives legitimate relative elementary collapses.**  If `x` is
   a leaf of a prospective link with neighbour `y`, the radial edge `ax` lies
   only in `axy` among current triangles and did not belong to the older
   complex.  Removing `(axy,ax)` deletes no original face and reduces the link
   forest by one edge until no new triangle remains.
7. **Restricted replay is genuinely hereditary.**  At a scheduled pair
   `(tau,e)`, if `tau` belongs to the current `Y`, downward closure puts `e` in
   `Y`.  Any ambient triangle removed earlier was either absent from `Y` or was
   removed at its own retained step.  Therefore no skipped step can leave a
   triangle obstructing `e`; it can leave only lower-dimensional faces.
8. **The three failures really give subcomplexes.**  Extra ambient faces may be
   omitted.  A link cycle yields the suspension `{v0,v1}*C`; two triangles on a
   duplicated edge yield the join of the copy pairs of the endpoints with the
   two opposite vertices; a fully duplicated triangle yields the join of three
   copy pairs.  These are respectively a polygon suspension and octahedral
   spheres even if the ambient complex has chords or additional copies.
9. **The obstruction is spherical, not just homological.**  Each displayed
   signed fundamental chain has zero boundary and deflates to zero.  It is
   nonzero in `H_2` because the ambient complex has no 3-simplices.  Its sphere
   inclusion is therefore non-nullhomotopic, producing a nonzero `pi_2`; the
   proof does not make the invalid inference that arbitrary nonzero `H_2`
   contradicts asphericity.
10. **The obstruction proves collapse necessity.**  A relative collapse onto
    the original complex plus vertices and edges would identify its `H_2` with
    that of the original copy: the 2-chain groups and 2-cycle condition are
    unchanged and there are no 3-boundaries.  Deflation is a left inverse, so
    its `H_2` kernel would vanish, contradicting the spherical class.
11. **The graph-of-spaces fact covers every connectivity boundary.**  Attaching
    only vertices and edges to a componentwise aspherical complex produces a
    graph of spaces with point edge spaces.  Its universal cover is a tree of
    contractible vertex spaces and intervals.  Conversely each old component
    is a homotopy retract.  The argument also covers isolated vertices and
    empty old space.
12. **The converse for the base is justified.**  Deflation has the canonical
    original-copy section.  Thus every higher homotopy group of `K` injects
    into the corresponding group of the inflation, component by component.
13. **The `W` equivalence uses all and only connected subcomplexes.**  Every
    component of `Y intersect K_0` is a connected simplicial subcomplex of
    `K`.  Conversely the explicit obstruction sphere itself is a connected
    subcomplex, so `W(I)` rules out every failed condition, while `K_0` rules
    out failure of `W(K)`.
14. **Prior art supports only the absolute part.**  Björner--Wachs--Welker
    Theorem 6.2 gives the wedge decomposition by suspended links.  In dimension
    two it yields exactly the same absolute sphere-versus-graph alternatives.
    Neither that theorem nor the inspected 2026 generalized-inflation paper
    states the target's relative elementary collapse and arbitrary-subcomplex
    replay.

## Adversarial smallest examples and independent checks

- **Empty and graph-only boundaries:** an isolated duplicated vertex has empty
  prospective link.  Inflating both ends of an edge creates a complete
  bipartite graph, possibly with cycles, but no 2-sphere and no triangle to
  collapse.  This correctly passes all three conditions and remains
  aspherical.
- **Condition 1 boundary:** duplicating the apex of a cone over a 3-cycle gives
  the 5-vertex, 9-edge, 6-triangle suspension sphere.  Deleting one cone
  triangle changes the link to a path and restores the collapse.
- **Condition 2 boundary:** two filled triangles sharing an edge, with both
  endpoints duplicated, contain a 6-vertex octahedral sphere.  Duplicating only
  one endpoint is admissible.
- **Condition 3 boundary:** a filled triangle with all vertices duplicated
  contains the octahedral sphere.  Leaving exactly one vertex unduplicated is
  admissible, including the limiting case of a duplicated edge lying in exactly
  one triangle.
- **Arbitrary subcomplexes:** exhaustive replay on two admissible fixtures—a
  triangle with multiplicities `(2,2,1)` and two triangles whose distinct
  opposite vertices are duplicated—checks all 697 and 2,099 subcomplexes.
  These include subcomplexes that retain a scheduled free edge while omitting
  its triangle, the main adversarial skip case.
- **Global rather than copy-ordered search:** the independent checker imports
  no target code and does not reconstruct the target's vertex-addition order.
  It repeatedly chooses a free nonoriginal edge from the full current incidence
  relation.  It succeeds on every admissible case in the finite census.
- **Complete small census:** all 9,417 labelled complexes on one through four
  vertices with multiplicities in `{1,2,3}` were audited.  There are 7,913
  admissible and 1,504 obstructed cases.  A separate mod-2 boundary elimination
  gives zero `H_2` jump exactly in the admissible cases and checks the full
  quantitative local kernel-rank formula in every case; the total obstructed
  rank jump is 8,937.
- **Signed integral certificates:** independently constructed suspension and
  octahedral chains have zero integral boundary and zero deflation.  Their
  supports pass edge-manifold, circular vertex-link, connectivity, and Euler
  characteristic checks.

Normal and optimized independent runs reproduce evidence digest
`553cbf2ea539b8ac3a78f49c73a5e7ea0c19c6600e4e147353adce75d344c19e`.
The target manifest passes, and normal and optimized target runs reproduce its
committed output and digest
`43aa2156df34d01030fca06adaca12119a720395e7e0f2138fefee3400a29ae7`.

## Source-integrity and literature audit

The author manuscript of Björner--Wachs--Welker, Theorem 6.2 and Corollary
6.3, defines the same variable-multiplicity inflation and gives the stated
wedge and homology decompositions.  In dimension two its extra `H_2` rank is

```text
sum_v (m_v-1) beta_1(lk v)
+ sum_uv (m_u-1)(m_v-1) max(t_uv-1,0)
+ sum_uvw (m_u-1)(m_v-1)(m_w-1),
```

where `t_uv` counts triangles on the edge and the last sum is over triangles.
This confirms both the absolute attribution and the completeness of the three
failure modes.

Ayzenberg--Khoroshavkina v1 explicitly identifies classical vertex inflation,
then proves absolute wedge decompositions for broader flabby generalized
inflations.  Searches of that paper found no relative-collapse or Whitehead
inheritance theorem.  Current primary literature still describes the integral
Whitehead asphericity statement as a conjecture; Fisher--Lodha's August 2026
paper concerns a group-theoretic route to a special case and leaves its
finitely generated replacement open.  The target correctly makes no global
Whitehead claim.

Bounded searches for combinations of vertex inflation, relative elementary
collapse, arbitrary subcomplexes, and Whitehead asphericity found no identical
statement.  This supports only search-relative novelty, not priority.

## Limitations and caveats

- The theorem is restricted to finite abstract simplicial complexes of
  dimension at most two and positive vertex multiplicities.
- The checker verifies finite combinatorics and homology; it cannot decide
  asphericity of an arbitrary base complex and is not a proof-assistant
  formalization.
- The absolute criterion is already implicit in the classical inflation wedge
  formula.  The relative and hereditary collapse are the substantive scope of
  the accepted contribution.
- The statement does not cover generalized sheaf inflations, simplicial posets,
  higher dimensions, or non-simplicial CW inflations.
- The novelty search is bounded and terminology-sensitive.

## Strengthening and improvement opportunities

The target could state the following quantitative corollary of the classical
wedge formula.  The displayed local sum in the source-integrity section is the
rank of the kernel of
`H_2(I;Z) -> H_2(K;Z)`, not merely a zero/nonzero test.  It measures the full
spherical excess contributed by cyclic duplicated-vertex links, multiply
incident duplicated edges, and fully duplicated triangles.

There is also a useful algorithmic strengthening.  Once any complete relative
triangle/free-edge sequence exists, **every** currently valid collapse of a
nonoriginal triangle through a nonoriginal free edge can be put first.  Commute
it past the earlier steps of a fixed complete sequence, then omit the later
step that would have removed the same triangle; the unused alternative edge is
only one-dimensional and obstructs nothing.  Hence a global greedy free-pair
algorithm succeeds under the three conditions without knowing a copy-addition
order.  The independent census tests this stronger behavior but a short
exchange lemma would make it a theorem.

Finally, the restricted-replay paragraph can be promoted to a standalone
hereditary-collapse lemma: a fixed sequence of top-dimensional elementary
collapses restricts to every subcomplex by retaining precisely the steps whose
top faces remain.  Isolating that general lemma would make the true source of
the Whitehead inheritance particularly transparent and may support analogous
relative results for other combinatorial operations.

