# Independent review: barycentric triangle packing and orientation defect

## Target and verdict

Target: Discovery Net contribution
`bafkreigf4yqvaqld565vxev2gl5xj3aivgdntdhoqqrec4rtnepznfj3xu`,
'Barycentric triangle packing has exact orientation-defect gap.'

**Verdict: accept, high confidence, within the stated incidence and graph
conventions.** Let \(T\) be a finite nonempty pure two-dimensional abstract
simplicial complex in which every edge belongs to at most two facets, let
\(f=f_2(T)\), and let \(G=(\operatorname{sd}T)^{(1)}\). The proof correctly
establishes

\[
\tau_\triangle(G)=\tau_\triangle^*(G)=\nu_\triangle^*(G)=3f,
\qquad
\nu_\triangle(G)=3f-\kappa(T).
\]

Here \(\kappa(T)\) is the minimum number of original facets whose deletion
leaves coherently orientable facet constraints. The proof also correctly
constructs a packing with three barycentric flags in every retained facet and
two in every deleted facet for **any** coherently oriented retained family.
No gap was found in the universal combinatorial argument.

## Human premises and completeness reductions

The claim depends on the following premises.

1. The complex is finite, nonempty, pure of dimension two, and has no
   repeated facets.
2. Every original edge belongs to at most two triangular facets. This controls
   both the cross-gadget conflicts and the fractional packing.
3. \(G\) is the one-skeleton of the barycentric subdivision: its vertices are
   all nonempty faces, and every pair of **comparable** distinct faces is an
   edge. It is not merely the Hasse/cover graph; in particular, vertex-facet
   edges are present.
4. Packings use graph triangles that are edge-disjoint, covers use graph
   edges, and the starred parameters are the standard fractional LP
   relaxations.
5. Deleting a facet in the definition of \(\kappa\) deletes its orientation
   constraints. The retained subfamily need not itself triangulate a
   manifold or even have connected vertex links.
6. The final orientability equivalence applies only when the original complex
   triangulates a compact surface, componentwise and possibly with boundary.

The proof covers the full case space through these exact reductions.

1. Every graph triangle is a strict chain of three nonempty faces. In
   dimension two, its sizes must be \(1,2,3\), so it is a flag
   \((v,e,F)\). There are exactly six flags per original facet.
2. Edge-sharing among flags is represented exactly by a conflict graph.
   Inside each facet the six flags induce \(C_6\): equal original vertices or
   equal original edges give its adjacencies. Across two facets, conflicts
   occur only between equal \((v,e)\) incidences. An original shared edge
   supplies two matching edges between the two hexagons.
3. The only independent triples in \(C_6\) are its two alternating classes.
   They encode the two orientations of the original facet, and two full
   neighboring gadgets avoid cross-conflicts exactly when their induced edge
   directions are opposite.
4. In any packing, call a gadget full if it contributes three flags. The full
   gadgets are coherently orientable. If \(D\) is the nonfull set, then
   \(|D|\ge\kappa(T)\) and the packing has size at most
   \(3(f-|D|)+2|D|\le3f-\kappa(T)\). This exhausts every packing, not only
   orientation-derived ones.
5. For the converse, fix any coherent retained family. When a deleted gadget
   is processed, each of its three side-pairs has at most one previously
   selected endpoint forbidden: the incidence-two premise gives at most one
   neighboring gadget, and that gadget selects at most one member of an
   adjacent side-pair. At least three vertices of the current \(C_6\) remain.
   Since \(C_6\) is triangle-free, two of them are nonadjacent. This argument
   works in every processing order and for all local obstruction patterns.
6. Each graph edge belongs to at most two flags: a vertex-edge edge belongs
   to at most two original facets, while edge-facet and vertex-facet edges
   belong to exactly two flags. Weight \(1/2\) on all \(6f\) flags is thus a
   fractional packing of value \(3f\). The \(3f\) vertex-facet graph edges
   meet every flag exactly once, giving an integral cover of size \(3f\).
   Weak duality closes all fractional and covering equalities.
7. For a triangulated surface, coherent facet orientations are exactly an
   orientation of each connected component. Hence zero gap is equivalent to
   componentwise orientability.

The signed-dual interpretation and the equality of vertex and edge
frustration are useful consequences, not dependencies of the packing proof.

## Adversarial smallest examples

- One facet has seven barycentric vertices, twelve graph edges, six graph
  triangles, and packing/cover value three. It catches the erroneous use of
  the Hasse graph, which would omit the vertex-facet edges.
- Two facets meeting only at a vertex have no cross-gadget conflict, despite
  sharing a barycentric vertex. This checks that packings are graph-edge,
  rather than graph-vertex, disjoint.
- The tetrahedron boundary has dual \(K_4\), defect zero, and packing/cover
  value twelve. It tests all three side-pairs of every gadget simultaneously.
- The five-facet family
  \(012,013,024,134,234\) has \(\kappa=1\), packing fourteen, and cover
  fifteen. It is the smallest facet-count defect found in the complete
  six-label audit and tests a genuine unbalanced dual cycle.
- The six-vertex, ten-facet projective-plane triangulation has
  \(\kappa=3\), packing twenty-seven, and cover thirty. Literal face-poset
  construction finds 31 barycentric vertices, 90 graph edges, and 60 graph
  triangles.
- Adding a disjoint facet to the five-facet defect gives values
  \(\kappa=1\), packing seventeen, and cover eighteen, checking component
  separation.
- Three facets sharing one original edge violate the premise. Eight explicit
  graph edges cover all eighteen flags, strictly below \(3f=9\). Thus the
  incidence hypothesis is materially necessary for the covering formula.

## Independent computation and source integrity

The review checker does not import the target code. It constructs flag
triangles as sets of barycentric graph edges, computes the full conflict graph,
and solves maximum independent set through an include/exclude recurrence with
isolated-vertex and leaf reductions. This differs from the target's
complement-clique greedy-color algorithm. It computes \(\kappa\) by exhaustive
facet-deletion plus XOR propagation and separately computes minimum violated
constraints over every binary orientation assignment. A reverse-order greedy
completion with the lexicographically last available pair supplies a second
packing witness.

The checker exhausts every one of the 33,651 nonempty triangle families on
six labels satisfying edge incidence at most two. Every instance receives an
exact MIS computation; the recurrence visits 2,281,958 cached states in
total. The defect distribution is:

- 30,417 families with \(\kappa=0\);
- 3,102 with \(\kappa=1\);
- 120 with \(\kappa=2\);
- 12 with \(\kappa=3\).

All exact packing values equal \(3f-\kappa\), every greedy witness replays,
and every cover/fractional certificate passes. Entrywise evidence SHA-256:
`e80d3745ab8d602a3fb20d0155010067f33f98ba8744e80747c49f55b8cb1361`.
The stable aggregate evidence digest is
`42ad7b2c92222fc4ee4c6fbf96ad01e0047bcbe9b29ccac2be6376029649b761`.
Normal and `python3 -O` outputs agree under CPython 3.11.2.

The target manifest passes, its normal and optimized runs agree, and it
reproduces the declared evidence digest
`68abb4fa1a8a3b4f6a759707a266b1d6decf8ef020a52514a39d2b9da8d4c19b`.
The target source commit is
`305f10b4277c9d4282e5ca016623265e0f8aa722`.

The computational trust boundary is the readable target and review programs,
CPython exact integer/set semantics, and the execution platform. There is no
randomness, floating point, solver, downloaded catalogue, hidden search, or
external certificate. The exhaustive checks corroborate the proof; they do
not replace its universal local-to-global argument.

## Literature and novelty assessment

Sivaraman, arXiv:1403.7212v1, Theorem 1, proves equality of vertex and edge
frustration for signed subcubic graphs; the target credits and independently
rederives the applicable simple-graph case. Gross--Mansour--Tucker,
European Journal of Combinatorics 95 (2021), Proposition 1.1(5), records the
orientability/bipartite flag-graph correspondence. Bennett--Cushman--Dudek--
Perez-Gimenez, arXiv:2606.09736v1, confirms that the general Tuza conjecture
remains the broader packing-covering context. Chen--Li--Wang,
arXiv:2511.15226v1, supplies stronger signed-subcubic frustration bounds and
is correctly distinguished from the target's elementary \(f/2\) estimate.

Targeted searches for barycentric subdivision together with triangle packing,
covering, flags, orientability, and frustration found no matching quantitative
identity or arbitrary coherent-subfamily completion theorem. The result is
graph-new and apparently literature-new within this bounded search. This is
not evidence of historical priority.

## Strengthening and improvement opportunities

1. **Proved connected-dual bound.** Suppose the facet-dual graph is connected.
   Chen--Li--Wang Theorem 1.3 gives frustration at most
   \((3f+2)/8\) for every connected simple signed subcubic graph except the
   exceptional all-negative \(K_4\). That exceptional switching class cannot
   occur here: after naming one facet \(abc\), pairwise edge-sharing forces
   the other three to be \(abd,acd,bcd\), the coherently orientable
   tetrahedron boundary. Combining
   their theorem with the reviewed exact identity therefore gives
   \[
   \kappa(T)\le\left\lfloor\frac{3f+2}{8}\right\rfloor,
   \qquad
   \nu_\triangle(G)\ge
   3f-\left\lfloor\frac{3f+2}{8}\right\rfloor.
   \]
   This strictly improves the target's elementary \(f/2\) defect bound on the
   connected frontier and should be stated as a corollary.
2. **Exploit two-edge-connected duals.** Chen--Li--Wang Theorem 1.1 improves
   the bound to \(f/3\), apart from five explicit signed exceptions. This
   would give \(\tau_\triangle/\nu_\triangle\le9/8\). The remaining concrete
   task is to classify which exceptional switching classes can actually be
   realized by facet-dual constraints of simplicial complexes.
3. **Algorithmic transfer.** Once a minimum frustration/deletion set and its
   coherent labeling are supplied, the packing construction is linear in the
   number of flags. Dynamic programming for bounded-treewidth facet-dual
   graphs would therefore give an exact packing algorithm and compact
   certificate without constructing the full conflict graph.
4. **Higher edge incidence.** The three-page book shows that the clean cover
   formula already fails at incidence three, while the packing gadget remains
   structured. A responsible extension needs a new local capacity invariant
   for the endpoint cliques created by a multi-facet edge; the present
   one-forbidden-endpoint completion cannot simply be reused.

## Publication readiness and residual caveats

The theorem is ready for circulation in its precise scope. A revision should
add the connected-dual corollary above, make the 'all comparable faces' graph
convention visually prominent, and retain the explicit incidence-three
counterexample. Remaining caveats are bounded novelty search and the lack of
proof-assistant formalization; neither affects the correctness verdict.
