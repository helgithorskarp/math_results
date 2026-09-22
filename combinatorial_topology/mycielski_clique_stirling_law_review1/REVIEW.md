# Independent review of the Mycielski clique-complex Stirling wedge law

## Identification and verdict

Target Discovery Net contribution:
`bafkreibpwctdkvdliwgio7pgzvyw6q6szik6dfk2tmanxdodsbn7fbehuq`.

Target source commit:
`1701c5f4de05e31c6e3a6d7f108c0ebedee0b250`.

Claim reviewed: for every finite connected simple K4-free graph `G` with at
least two vertices, every ordinary Mycielski iterate has the homotopy type

```text
Cl(M^k(G)) ~= Cl(G) wedge R_k circles wedge Q_k two-spheres,
```

where `R_k,Q_k` have the stated nonnegative Stirling-number formulas.  The
claim also gives the exact first, second, and third-iterate asphericity
boundaries and says that every aspherical positive iterate, together with
each of its simplicial subcomplexes, collapses to a graph.

**Verdict: accept with high confidence.**  I found no mathematical,
computational, completeness, dependency, or source-integrity defect.  The
one-step space is exactly a succession of nullhomotopic cone attachments
followed by a star attachment.  The link and incidence recurrences are
complete.  Their sums give the claimed Stirling coefficients, with no hidden
cancellation.  Finally, the forest-link argument supplies actual elementary
collapses, including a valid restriction of the same collapse sequence to
every simplicial subcomplex.  Thus the asphericity assertions do not infer
homotopy information merely from Betti numbers.

Two exposition improvements are noncorrective.  First, the proof could state
as a separate lemma that attaching a new vertex by `n` edges to arbitrary
points of a path-connected CW complex adds `n-1` circles; this makes clear
that the preceding cone equivalences need not fix the clone cone-points.
Second, “in every positive case” should read “for every aspherical positive
iterate” to prevent “positive” from being read as merely `k>0`.

## Human premises and completeness reductions

My verdict depends on the following complete list of human premises.  The
finite programs test their consequences but do not replace these arguments.

1. **Domain and dimension.**  `G` is finite, simple, connected, K4-free, and
   has at least two vertices.  Hence `Cl(G)` is a connected CW complex of
   dimension at most two, every vertex link is a nonempty graph, and the
   ordinary Mycielski definition used in the proof is unambiguous.

2. **The pre-apex decomposition is exhaustive.**  Before adding the apex,
   every new simplex belongs to exactly one cone
   `v' * Cl(G[N(v)])`; two clones are never adjacent, so distinct new cones
   intersect only in the original clique complex.

3. **Each attaching map is nullhomotopic in the original complex.**  The old
   vertex `v` cones off `Cl(G[N(v)])` inside `Cl(G)`.  This nullhomotopy remains
   available after any earlier clone-cone attachment.

4. **Homotopy-invariant attachment applies successively.**  The finite
   simplicial pairs are CW pairs, so Hatcher Proposition 0.18 permits each
   cone attachment to be replaced by a constant attachment relative to the
   already constructed space.  This also covers disconnected link graphs.

5. **A constant cone attachment contributes an unreduced suspension.**  The
   quotient of a cone after identifying its entire base to the attaching
   point is the unreduced suspension.  Attachments based at different points
   may be moved to one wedge point because the original complex is connected.

6. **Suspending a finite graph gives exactly the displayed wedges.**  If a
   nonempty graph has `c` components and cycle rank `d`, its unreduced
   suspension is a wedge of `c-1` circles and `d` two-spheres.  Isolated
   vertices and wholly edgeless links are included; using reduced suspension
   without the component term would be wrong.

7. **The apex contributes exactly `n-1` circles.**  It lies in no triangle,
   and its `n` incident edges attach a star to `n` points of a path-connected
   complex.  Homotope those endpoint maps to a common point: one edge is a
   tree edge and the other `n-1` edges are independent loops.  No preservation
   of the clone cone-points by the earlier equivalence is required.

8. **The one-step link totals are correct.**  Summing components gives the
   circle increment `C-1`.  Each original edge occurs in two vertex-link
   vertex sets and each triangle in three vertex-link edge sets, so the sphere
   increment is `D=3t-2m+C=sum_v beta_1(L_v)`.

9. **All three new link types are correctly identified.**  An old vertex has
   link `Sh(L_v)`, a clone has link `L_v` disjoint union an isolated apex, and
   the apex has an edgeless link on all clones.  There are no omitted old,
   clone, or apex adjacencies.

10. **Shadow components account for precisely the zero-triangle edges.**  A
    nontrivial component of `F` stays connected in `Sh(F)`, while every
    isolated vertex creates two isolated vertices.  A neighbor `u` is
    isolated in `L_v` exactly when edge `uv` is in no triangle, so the global
    isolated-link contribution is `2e0`.

11. **The triangle lifts and domain closure are complete.**  Every old
    triangle has exactly four lifts: all-old and the three choices of one
    cloned vertex.  No triangle has two clones or the apex.  Connectedness and
    K4-freeness are preserved, so the one-step theorem can be iterated.

12. **Edge triangle multiplicities have all possible types.**  An old lift of
    edge `e` has multiplicity `2t_e`, each of its two mixed lifts has
    multiplicity `t_e`, and every apex edge has multiplicity zero.  Together
    with direct vertex, edge, and triangle counts this proves all five
    recurrences for `n_j,m_j,t_j,e_j,C_j`.

13. **The recurrence solution and summation are exact.**  Substitution checks
    the displayed powers of two, three, and four.  Summing the one-step
    increments and applying the standard formulas for `S(k+1,2)`,
    `S(k+1,3)`, and `S(k+1,4)` gives exactly `R_k,Q_k`, including `k=0`.

14. **There is no cancellation in the sphere test.**  `D` is a sum of link
    cycle ranks, `Y=sum_e max(t_e-1,0)`, and `t` is the triangle count.  All
    Stirling coefficients in `Q_k` are nonnegative.  Hence the zero tests used
    for the asphericity boundary are coefficientwise structural conditions.

15. **A sphere summand obstructs asphericity.**  When `Q_k>0`, projection from
    the wedge decomposition onto one `S^2` is a retraction.  It injects a
    nonzero `pi_2(S^2)` class; the argument is stronger than merely observing
    nonzero second homology.

16. **Forest links force the original complex to collapse.**  If `D=0`, every
    `L_v` is a forest.  Were a triangle-containing subcomplex to have no free
    triangle edge, the link at a triangle vertex, after discarding isolated
    vertices, would have minimum degree at least two and hence a cycle.  Thus
    successive triangle/free-edge collapses remove every triangle.

17. **The clone cones collapse legally.**  Root each tree component of each
    `L_v`.  Peeling a leaf `y` of edge `xy` removes triangle `v'xy` with the
    unique mixed free edge `v'y`.  Different clone cones share no mixed edge,
    apex edges lie in no triangle, and the old base remains untouched.  The
    remaining old triangles can then be collapsed by premise 16.

18. **Collapse sequences restrict to arbitrary simplicial subcomplexes.**  If
    the paired triangle is present, its paired edge is present and has no
    additional coface in the subcomplex.  If a step is skipped because its
    triangle is absent, retaining its edge cannot obstruct a later step: any
    later triangle containing it would already have contradicted freeness in
    the original sequence.  Induction therefore leaves no subcomplex
    triangle unremoved.

19. **The last-step reduction covers every positive iterate.**  `Q_k` is the
    sum of the nonnegative one-step defects `D_j`.  Thus `Q_k=0` implies
    `D_(k-1)=0`; applying premise 17 to the final Mycielski step collapses the
    entire `k`th clique complex, and premise 18 gives hereditary collapse.

20. **The three thresholds are equivalent to the stated local conditions.**
    `Q_1=D`, `Q_2=3D+2Y`, and `Q_3=7D+12Y+6t`.  The condition `Y=0` says every
    edge belongs to at most one triangle and then every link is a matching
    with isolated vertices, so `D=0`.  For `k>=3`, the positive `S(k+1,4)`
    coefficient makes `Q_k=0` equivalent to `t=0`.

21. **The boundary examples and K4 exclusion are correctly scoped.**  The
    four-rim wheel, diamond, and triangle realize first failure at steps one,
    two, and three.  For excluded `K4`, links are filled triangles rather than
    graph cycles; the same cone argument gives only three circle summands, so
    the K4-free hypothesis is mathematically essential.

22. **Full homotopy type and novelty are not overclaimed.**  The relative
    attachment equivalences retain the complete `Cl(G)` homotopy type,
    including torsion and fundamental group.  The result concerns ordinary
    clique complexes only.  It does not infer a Whitehead theorem, a
    generalized-height Mycielski statement, or priority beyond the stated
    bounded literature search.

These premises cover the attachment points, disconnected links, every new
simplex and edge type, arbitrary iteration, zero-coefficient cases, and all
simplicial subcomplexes.  Agreement among programs is not being used as a
substitute for any item in this list.

## Independent exact audit and adversarial examples

`audit_independent.py` imports no target module, fixture, output, or
certificate.  It represents graphs by neighbor bitsets, reconstructs the
ordinary Mycielskian directly, obtains link and incidence statistics from the
definition, row-reduces the oriented triangle boundary matrix over `F_2` and
`F_3`, and independently iterates the five statistic recurrences.  This is a
different implementation from the target's producer/checker split and sparse
column reduction.

The exhaustive audit covers all 33,866 labelled graphs on two through six
vertices.  Exactly 22,667 are connected and K4-free.  On every admitted base
it checks all statistic recurrences, the one-step homology increment over both
fields (45,334 checks), and the closed Stirling formulas against direct
recurrence sums for every `0<=k<=8`.  The entry-level audit digest is
`e3b4627cbe9fc9c65e104ff3c8572ddc83cc731f2bfb49877d402ca4f338eb81`.

The smallest adversaries deliberately separate the hypotheses and failure
times:

- `K2` tests a singleton link, an edgeless apex link, and the `C5` first
  iterate; `P3` tests disconnected edgeless links and zero-triangle edges.
- `K3` first fails at iterate three; the diamond first fails at iterate two;
  the four-rim wheel first fails at iterate one.
- The three-page book has `D=0,Y=2`, exposing repeated use of one edge.  The
  bowtie has two triangles but `D=Y=0`, exposing the difference between
  repeated-edge and merely positive triangle count.
- The octahedral graph has an initial two-sphere and cyclic links, testing
  retention of a nontrivial base complex plus new sphere summands.
- Excluded `K4` gives `f(Cl(M(K4)))=(9,22,16,5)` and Euler characteristic
  `-2`, consistent with three circles and inconsistent with treating its
  filled links as one-dimensional cycles.

For the hereditary statement, the independent checker constructs
`Cl(M^2(K3))`, which has 16 triangles, and tests all `2^16=65,536` possible
triangle subfamilies.  It runs a fresh free-edge peel for each subfamily,
rather than replaying the target trace.  Every family collapses, across
524,288 triangle/free-edge removals.  Arbitrary additional edges and vertices
cannot affect a triangle's free-edge cofaces, so triangle subfamilies cover
the two-dimensional obstruction relevant to these subcomplexes.

Normal and optimized runs agree with frozen output SHA-256
`ba3e72e3b53598101cf50c2acaac078850dbb8deaa421e88d3ccd208f52eecad`.
The audit uses exact Python integers only; there is no solver, floating point,
randomness, native extension, or external dataset.

The computation corroborates finite consequences only.  In particular,
finite-field Betti agreement does not prove an integral homotopy equivalence,
and no finite enumeration proves the arbitrary-`k` formula or the universal
subcomplex claim.  Those conclusions rest on premises 2--20.

## Source and scope audit

Hatcher Proposition 0.18 says homotopic attaching maps on a CW pair produce
homotopy-equivalent adjunction spaces relative to the old space; Example 0.14
also records the mapping-cone/suspension consequence used here.  These are the
correct imported facts, and all spaces in the proof are finite simplicial CW
complexes.

The related Goyal--Shukla--Singh paper concerns independence complexes of
generalized Mycielskians of complete graphs, not ordinary clique complexes.
Santocanale's Proposition 1.8 concerns iterated Mycielski graphs as forbidden
subgraphs of event-structure graphs; the same paper's clique-complex section
then studies a different recursively coned family.  Neither source states the
reviewed all-base Stirling wedge law.  Exact-phrase and topic searches of
arXiv and publisher-indexed results located no competing theorem.  This
supports only the target's careful “historical priority unestablished” scope,
not an exhaustive novelty claim.

The target source URLs, manifest, normal run, and optimized run all reproduce.
The graph body accurately identifies the source commit and separates the
written universal proof from finite corroboration.

## Caveats

- This is not a proof-assistant formalization.  The mapping-cone, wedge-point,
  and collapse-restriction arguments remain human-checked topology.
- The independent homology audit uses two finite characteristics; torsion
  preservation follows from the relative homotopy splitting, not from those
  field calculations.
- Historical priority remains search-relative.  The verdict certifies the
  mathematical claim and its stated scope, not first publication.
- No conclusion is made for disconnected bases, one-vertex bases, graphs
  containing `K4`, generalized-height Mycielskians, or other complex functors.

## Strengthening and improvement opportunities

State the apex-star attachment as an explicit lemma, replace “every positive
case” by “every aspherical positive iterate,” and present the restriction of
the collapse sequence as a short induction.  A useful next advance would be a
Lean formalization of the one-step simplicial decomposition and statistic
recurrences, followed by a formal simple-homotopy proof of hereditary
collapse.  A separate mathematical direction is to identify the correct
higher-dimensional replacement for the link-graph suspension formula when
the K4-free hypothesis is relaxed.
