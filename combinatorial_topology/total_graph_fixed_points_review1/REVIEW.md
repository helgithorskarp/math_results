# Independent review of equivariant total-graph fixed spaces

## Verdict

**ACCEPT, high confidence.** I found no mathematical defect in
[*Equivariant total-graph splitting and all subgroup fixed-point spaces*](https://github.com/helgithorskarp/math_results/tree/e269dc5b33ae06567ecdedae95dea59c8b335b87/combinatorial_topology/total_graph_fixed_points)
(Discovery Net CID
`bafkreia2so7iwwg6qzolle3cqglyia5poqo3lelm4zpij7v7htom4vrlpu`). For a
finite simple graph `G`, the source correctly refines Adamaszek's ordinary
decomposition to an `Aut(G)`-equivariant equivalence, relative to
`A=|Cl(G)|`,

```text
|Cl(T(G))|  ~=  A with S^(W_tau) attached at b_tau for every triangle tau,
```

where `W_tau` is the two-dimensional reduced permutation representation on
the vertices of `tau`. Consequently, for every subgroup `H`, a setwise
`H`-invariant triangle with `o_H(tau)` vertex orbits adds
`S^(o_H(tau)-1)` to the genuine geometric fixed space. This gives a
2-sphere, circle, or new isolated point for respectively three, two, or one
vertex orbit.

The ordinary nonequivariant wedge theorem is prior work. The reviewed
increment is the explicit equivariant refinement, fixed-space formula,
signed integral triangle module, and resulting asphericity criterion.
Priority is search-relative; the proof is not formalized.

## Human premises and completeness reductions

The verdict rests on the following human proof chain. Agreement between the
submitted and independent programs is corroboration, not a replacement for
these premises.

1. **Scope and action.** `G` is finite, undirected, and simple. Any possibly
   infinite `Gamma` acts through its finite image in `Aut(G)`, so finite
   equivariant topology suffices without a freeness hypothesis.
2. **Complete face classification.** A total-graph clique with at least
   three original vertices is an original clique. With exactly two original
   vertices it can add only their edge-vertex. With one original vertex all
   edge-vertices meet it. A pairwise-intersecting family of distinct graph
   edges is either a star or exactly the three edges of a triangle. These
   cases exhaust every clique, including high-dimensional original cliques
   and high-valence stars.
3. **Deleted-face completeness.** The edge-only simplex of each original
   triangle is maximal. Removing exactly its relative interior, for every
   triangle, leaves an invariant subcomplex `K`; no other face is removed.
4. **First deformation.** In a star simplex `S_v`, subtracting the second
   largest edge-coordinate from every positive edge-coordinate is continuous,
   permutation-invariant, leaves nonnegative total mass at most one, and
   leaves at most one edge-coordinate positive. It fixes the star tree
   pointwise. On intersections `S_v intersect S_w`, `S_v intersect P_e`, and
   `S_v intersect A`, both local formulas are the identity, so they glue to
   an equivariant strong deformation of `K` to `A union (union_e P_e)`.
5. **Second deformation.** Moving the edge-coordinate in
   `P_e={u,v,e}` equally to `u` and `v` retracts `P_e` onto `[u,v]`, fixes
   `A`, commutes with the endpoint swap, and agrees on all intersections.
   Thus `K` strongly deformation retracts to `A` equivariantly and relative
   to `A`.
6. **Equivariant attachment replacement.** The boundary inclusions of the
   deleted triangle disks are invariant cofibrations. Hence the deformation
   of the base and an equivariant homotopy of the attaching maps may be
   inserted on invariant collars. The resulting pushout maps and homotopies
   are relative to `A`. Barycentric subdivision removes any concern about
   simplex inversions in an equivariant CW formulation.
7. **Null-homotopy completeness.** After the two-stage retraction, every
   boundary edge of an edge-only triangle travels through the common endpoint
   of its two graph edges and lands in the corresponding original triangle.
   Straight-line contraction to that triangle's barycenter is invariant
   under the full triangle stabilizer. No endpoint, ordering, or global
   basepoint is chosen.
8. **Representation sphere.** The open two-simplex is equivariantly
   homeomorphic to the reduced permutation representation by centered
   logarithmic barycentric coordinates. Collapsing its boundary is the
   one-point compactification. Sending an edge of a triangle to its opposite
   vertex intertwines the two stabilizer actions, giving `S^(W_tau)` with
   no hidden orientation twist.
9. **Passage to fixed spaces.** An equivariant homotopy equivalence with
   equivariant inverse homotopies restricts to an ordinary homotopy
   equivalence on `H`-fixed points. Outside `A`, a point lies in one unique
   attached sphere; it can be fixed only when that sphere's triangle is
   setwise invariant. Spheres merely permuted by `H` contribute no diagonal
   fixed points.
10. **Fixed representation dimension.** An `H`-fixed vector in `W_tau` is
    constant on each vertex orbit. The one weighted sum-zero equation is
    independent, so `dim(W_tau^H)=o_H(tau)-1`. The zero-dimensional case has
    one basepoint and one genuinely new isolated point. If `A^H` is empty,
    an invariant triangle is impossible because its barycenter would lie in
    `A^H`.
11. **Geometric fixed-space encoding.** For an invariant flag complex, a
    fixed barycentric point has orbit-constant coordinates and invariant
    support. An orbit can enter that support exactly when it is a clique, and
    several orbit supports form a face exactly when their union is a clique.
    This justifies the direct checker and avoids confusing geometric fixed
    points with fixed vertices, orbit quotients, or invariant homology.
12. **Betti and asphericity consequences.** Attaching `S^0`, `S^1`, or
    `S^2` at a point respectively adds a component, a free circle, or a
    two-sphere. A two-sphere summand retracts and forces nonzero `pi_2`;
    wedging circles onto an aspherical connected finite CW complex preserves
    asphericity; and each old component remains a retract. This proves both
    directions of the stated componentwise criterion.
13. **Integral splitting.** For each oriented triangle, the eight signed
    faces obtained by choosing one vertex from each opposite pair in the
    induced octahedron form an integral 2-cycle with relative coefficient
    one on its edge-only face. These cycles split the relative chain group
    `H_2(X,K)`, while the long exact sequence and `K ~= A` give the claimed
    absolute direct sum and all other homology isomorphisms.
14. **Sign action.** Permuting the three opposite pairs multiplies that
    octahedral cycle by the permutation sign. The opposite-edge bijection is
    equivariant, so the added integral module is precisely the oriented
    triangle module, including in modular characteristics after base change.

Together, items 2--8 cover the entire equivariant homotopy construction;
items 9--12 exhaust the fixed-space cases; and items 13--14 independently
account for the integral module statement.

## Adversarial smallest examples

- The empty graph checks the empty-space convention and vacuous fixed-space
  statement.
- `K_2` with its endpoint swap has no fixed vertex, but its geometric clique
  complex has the midpoint as a fixed point. The theorem and checker both
  retain this point, guarding against replacement by the fixed-vertex
  subcomplex.
- On `K_3`, the trivial action, a transposition, a 3-cycle, and `S_3` produce
  respectively a 2-sphere, a circle, two points, and two points. This is the
  smallest complete test of all three orbit counts and of simplex inversions.
- Two disjoint triangles exchanged by an involution have empty fixed spaces
  before and after the construction. This rejects a false “diagonal fixed
  sphere” from a nontrivially permuted sphere orbit.
- A 3-cycle acting on `K_4` fixes one vertex and setwise fixes only the
  opposite triangle. Exactly one isolated component is added; the other
  three triangles form a nonfixed orbit and add nothing.
- In the diamond graph, an involution exchanges its two triangles while they
  share an original edge. No fixed sphere appears. This tests that sharing
  base-space faces does not merge permuted disk interiors.
- A reflection of `C_4` through opposite vertices has two geometric fixed
  components, and the triangle-free total-graph construction preserves both.
  This catches an easy but incorrect assumption that a reflected circle has
  connected fixed set.

## Independent computational reproduction

The submitted manifest passes, and its normal and optimized runs reproduce
the published digest
`3e71a91fec91092e591f6ecefa155cd65b93a4c7e8b263b5b9e1ce68e16ec7b8`.
Its proof-critical guards remain active under `python -O`.

The independent checker imports no target code, fixtures, or output. It
uses a broader exhaustive architecture:

- every one of the 1,100 labelled simple graphs on zero through five
  vertices is generated;
- the full automorphism group is computed from the definition, and every
  subgroup is generated by closure (including all 156 subgroups of `S_5`);
- all 56,318 total-graph faces are checked against the complete face
  classification;
- for all 5,058 graph/subgroup pairs, the genuine fixed spaces of `Cl(G)`
  and `Cl(T(G))` are rebuilt from invariant barycentric supports and their
  exact `F_2` homology is compared entry-by-entry with the sphere formula;
- 1,313 integral octahedral cycles and 7,038 automorphism actions on them are
  checked directly, including boundary cancellation and orientation signs;
  and
- ten hand-readable controls isolate empty spaces, inversions, all three
  triangle orbit types, permuted sphere orbits, shared-edge triangles, and
  disconnected fixed sets.

Normal and optimized runs agree on the frozen entry digest
`9daf4ddf04ec24d73cfe64e23dea60b416e69bf0dd772ca85a6de969a288e3e1`.
The census checks every smallest case in its declared range, but only the
human argument proves arbitrary finite graphs and equivariant homotopy type.

## Strengthening and improvement opportunities

Three useful consequences follow immediately from the reviewed relative
model.

1. **Equivariant cofiber splitting.** Because the equivalence and homotopies
   are relative to `A`, quotienting by `A` gives a based equivariant
   equivalence

   ```text
   |Cl(T(G))| / |Cl(G)|  ~=_Gamma  wedge_tau S^(W_tau),
   ```

   where `Gamma` permutes the triangle summands and acts through the reduced
   permutation representation on each stabilizer. This is the canonical
   setting in which all attachment basepoints may be combined.
2. **Componentwise fundamental groups.** For a component `C` of `A^H`, let
   `m_2(C)` count invariant triangles with two vertex orbits whose
   barycenters lie in `C`. The corresponding component of `X^H` has

   ```text
   pi_1  =  pi_1(C) * F_{m_2(C)}.
   ```

   Pointwise fixed triangles do not change `pi_1`, while transitive triangles
   give separate point components. This refines the global Betti and
   asphericity statements.
3. **Fixed-point Euler mark.** For every subgroup `H`, including the empty
   fixed-space case,

   ```text
   chi(X^H)-chi(A^H)
     = sum_{tau setwise H-invariant} (-1)^(o_H(tau)-1).
   ```

   This records the three fixed-sphere cases in one integer formula and is
   the mark-level shadow of the equivariant cofiber splitting.

For exposition, the only step worth expanding is the equivariant attachment
lemma: a short standalone mapping-cylinder statement with explicit maps
would make the relative claim easier to reuse. This is a presentation
improvement, not a gap in the current collar/cofibration argument.

## Source and scope audit

The fixed target commit contains the proof, direct checker, expected output,
references, and an integrity manifest. Adamaszek's primary arXiv text was
checked directly: Theorem 5.1 states the ordinary total-graph wedge
decomposition, Lemma 5.3 gives the four maximal-face types, and its proof
removes the same edge-only triangle cells before collapsing the core.

Live searches combining total graphs, clique complexes, equivariant
homotopy, fixed points, and representation spheres did not locate this exact
refinement. This supports the target's careful search-relative novelty
boundary but does not establish historical priority. See [SOURCES.md](SOURCES.md).

## Caveats

- The theorem is for finite simple graphs and automorphism actions; it does
  not cover multigraph total graphs or unrelated actions on the clique
  complex.
- The ordinary wedge theorem and face classification are explicitly prior
  work, not part of the novelty claim.
- The proof is an informal equivariant homotopy argument rather than a proof
  assistant formalization.
- The finite census checks homology, face completeness, and integral signs;
  it does not certify arbitrary-graph homotopy equivalence by enumeration.

