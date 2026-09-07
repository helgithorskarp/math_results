# Exact exclusions and the hypotheses they require

The target is a graph requiring five colours, with at most 508 distinct points
in the Euclidean plane and exact unit-length edges. A drawing may have crossing
edges. In this note `UD(P)` denotes the **strict** graph containing every
unit-distance pair of a point set P. A prescribed edge graph `(P,E)` can instead
use only a subset of those pairs. Distinguishing these objects is essential.

The following is a synthesis of already published results. The elementary
corollary and pasting formulation below make their implications explicit;
they do not constitute a new candidate or a new global lower bound.

## 1. Three structural obstructions

### Arithmetic obstruction: whole embedded fields

Let K be a number field in C stable under physical complex conjugation c.
Suppose a finite place v is fixed by c and c acts trivially on its residue
field. A unit difference d satisfies

```
d c(d)=1,   2v(d)=0,   and   d_bar^2=1.
```

Every edge lies within an additive coset of the valuation ring. Reducing
within that coset sends its difference to `+1` or `-1`. In residue
characteristic p these steps form p-cycles, with a single edge when p=2.
Pulling back their colourings gives `chi(UD(K))<=3`, or `<=2` when p=2.
This argument covers arbitrary denominators and point-set sizes.

The bound extends to translated or similar subsets. If `uK` has a unit
difference `uz`, then `uK=(uz)K` is a rotation of K because `zK=K` and
`|uz|=1`; without any unit difference the graph is edgeless.

For nonreal K, set `F=K intersect R`. Ramification at any finite place in the
quadratic extension K/F makes c inertial there. Consequently a field capable
of supporting a four- or five-chromatic unit graph must be unramified over F
at every finite place. This is a necessary condition, not a sufficiency test.

The [source proof](../hadwiger_nelson_inertial_field_barrier/README.md) gives
two complete applications: the specified Radchenko quartic/equilateral field
has unit-distance chromatic number exactly three, and `UD(F(i))` is bipartite
whenever real F has a place above two of ramification index one. The proof
also explains why Sawin's different unramified CM construction is outside
the obstruction. No conclusion about every CM field follows.
The [independent acceptance](../hadwiger_nelson_inertial_field_barrier_review1/README.md)
is at the precise published scope.

### Group obstruction: the entire finite Cayley edge graph

Let A be a finite abelian group and let `S=-S` exclude zero. Choose one
representative `s_i` from each sign class of S and put
`H_i=<s_j:j!=i>`. The graph `Cay(A,S)` has an injective plane drawing with
every required edge of length one exactly when

```
<s_i> intersect H_i = {0} for every i.
```

To see the obstruction, four distinct vertices in a unit four-cycle form
a rhombus. Their alternating position sum vanishes. Therefore the edge
difference `D(x)=F(x+s_i)-F(x)` is invariant under H_i. For a nonzero
`h in <s_i> intersect H_i`, the difference `F(x+h)-F(x)` is invariant
under h. Telescoping around the finite order of h forces this difference
to vanish, contradicting injectivity.

Conversely, the intersection condition gives an internal direct sum of the
cyclic factors. Independently rotated regular polygons and unit segments
give an injective drawing of their Cartesian product. Generic rotations
avoid unintended contacts. The abstract product is at most three-colourable.
The [complete proof and certificates](../hadwiger_nelson_finite_abelian_lifts/PROOF.md)
include all component and degenerate cases.

For norm-one graphs on the additive group of `F_(q^2)`, this rules out every
prime power q except three. The complete twelve-parameter range `q^2<=508`
is decided. Its abstract graph at q=11 has 121 vertices, 726 edges and
chromatic number exactly five, with a short checked RUP refutation and a
five-colouring. The separate rhombus certificate proves that graph has no
injective plane unit drawing. Its five-chromaticity is therefore not a
physical candidate. No external acceptance review was located for this
package in the inspected committed neighborhoods at the stated cutoff.

The theorem quantifies over the prescribed Cayley edge graph. It is not a
bound on the strict completion of every non-strict drawing of that graph.
Nor does it cover infinite additive groups, noninjective homomorphisms,
or arbitrary selected subgraphs of a nonrealizable finite Cayley graph.

### Geometric obstruction: two intersecting unit triangular lattices

Let `omega=(1+i sqrt3)/2` and `R=Z[omega]`. If two unit triangular lattices
share a vertex, translate that vertex to zero and rotate one lattice to R.
The other is `alpha R` for some complex unit alpha. Then

```
chi(UD(R union alpha R)) <= 4    for every |alpha|=1.
```

The residue `rho(a+b omega)=a-b mod3` colours each lattice. If alpha belongs
to `Q(omega)`, its primitive denominator is not divisible by three, so
the residue colouring extends and gives three colours on the union.

Otherwise the lattices meet only at zero. The rational subspace
`{t in Q(omega): alpha*t+conjugate(alpha*t) in Q}` has dimension at most
one. For a cross-contact between nonzero z and alpha*w, the product
`w*conjugate(z)` lies on this one rational trace direction.
Reducing its norm equation fixes one product `rho(z)rho(w)=epsilon` whenever
both residues are nonzero. The two nonzero residue colours can then be
permuted to differ across all such edges, while the two zero classes use
separate colours. The origin is handled explicitly. This proves the
whole-union bound without enumerating angles or assuming algebraic alpha.

The [source proof](../hadwiger_nelson_triangular_overlays/PROOF.md) gives the
exact obstruction to using three colours and a Moser-spindle sharpness
witness. It also completely classifies the patch `a^2+ab+b^2<=67`: each
patch has 253 points, every union has at most 505 points, and its 1,746
exceptional rotations split into 1,350 three-chromatic and 396 four-chromatic
cases. Other angles give the stated generic three-chromatic graph.
These are rotation counts, not isomorphism counts. The
[independent acceptance](../hadwiger_nelson_triangular_overlays_review1/README.md)
covers both the structural theorem and that exact finite census.

The hypotheses require unit lattice spacing and a common lattice vertex.
Three orientations, disjoint translated full lattices, different scales,
and arbitrary additive sums of lattices are outside this result.

### Consolidated necessary conditions

For an injectively realized finite unit-distance graph G with `chi(G)>=5`:

1. Its point set cannot, after a similarity, lie in a field meeting the
   inertial-conjugation hypothesis.
2. Its point set cannot lie in two unit triangular lattices sharing a vertex.
3. Its entire prescribed edge graph cannot be a finite abelian Cayley graph.

Each conclusion follows by restricting the corresponding proved colouring
or applying the realizability classification. These conditions are independent
screens, not an exhaustive characterization. Passing all three does not
supply a non-four-colourability certificate.

## 2. A small exact guard against scope overextension

Set `beta=(5+i sqrt11)/6`, and label

```
p0=0, p1=1, p2=omega, p3=1+omega,
p4=beta, p5=beta*omega, p6=beta*(1+omega).
```

These seven distinct points form the classical Moser spindle. Their strict
unit graph has eleven edges. It contains the spanning unit cycle

```
0--1--2--3--6--5--4--0.
```

Giving position j along this cycle the group label `j mod7` realizes
`Cay(Z/7Z,{+1,-1})` injectively by unit edges. This abstract graph is an
odd cycle and has chromatic number three; the word `0101210` in point-label
order is a proper colouring. The same point set has four extra unit edges.
Its strict graph is four-chromatic, with the proper word `0120123`.
The strict degree sequence is `(4,3,3,3,3,3,3)`, so it is not a Cayley graph.

The finite-abelian theorem applies to the seven cycle edges. The strict
completion is a different graph. This example supplies a concrete check
against silently extending an abstract-graph upper bound to additional
geometric contacts.

The two four-point diamonds `{0,1,2,3}` and `{0,4,5,6}` also each have
five unit edges and are three-colourable. Their common vertex is zero.
The strict union adds the cross-contact `3--6`, which makes three colours
impossible: in every three-colouring of a unit diamond the common apex and
the opposite tip have the same colour. Both tips would have the origin's
colour. The displayed four-colouring proves equality.

[scope_guard.py](scope_guard.py) verifies all 21 squared distances both by
Cartesian radical coefficients and by complex tensor multiplication. It
checks the cycle and both colour words, exhausts all three- and four-colour
words for the strict graph, and verifies the extra cross edge. This is a
classical example included to protect the scope of the consolidation, not
an objection to a cited theorem or a new growth pilot.

## 3. What makes the complete assembly closures work

A standard pasting lemma explains two of the strong finite results. Suppose
G is the union of a base H and pieces C_i; the interiors `C_i-H` are disjoint,
each `C_i intersect H` is a clique, and **every edge of G already belongs
to H or one C_i**. If H and each C_i are k-colourable, then every proper
k-colouring of H extends to G. Each interface clique has distinct colours
on both sides, so a permutation matches the piece palette to the base.
The edge-coverage hypothesis makes these independent extensions proper.

For unit-distance point sets, that last hypothesis requires checking every
possible additional contact. Merely listing the intended piece edges is
insufficient, as the seven-point example shows.

| Complete construction | Certified consequence | Boundary |
|---|---|---|
| [Snail dihedral-nine closures](../hadwiger_nelson_snail_dihedral/README.md) | All 812 centre/axis choices on the fixed 29-point seed: 157 have chi=3, 655 have chi=4, with 271–496 points | Fixed seed and ordered seed-pair axes only |
| [H21 triangle-isometry assemblies](../hadwiger_nelson_heptagon_triangle_isometries/PROOF.md) | Each of 35 pieces adds 18 private vertices and 39 edges; all seed four-colourings extend. Exactly 34,351,006,520 full assemblies have at most 508 points, with maximum 507 | One application to the seven specified seed triangles; no recursion |
| [Fixed-base golden reciprocal overlays](../hadwiger_nelson_golden_reciprocal_closure/PROOF.md) | One checked four-colouring of the full 1,386-point, 4,380-edge union covers every subassembly of the 656 allowed copies | Every moved copy has scale phi or 1/phi and shares two points with the original fixed G16 base |

Snail uses a cubic field separation to prove three pieces meet only at their
centre and have no cross edges; their colours can be aligned there. H21
uses the triangle interfaces and a complete exact contact calculation.
Golden instead supplies a proper colouring of its full union, including
all accidental contacts; it needs no clique-interface simplification.

The [Snail review](../hadwiger_nelson_snail_dihedral_review1/REVIEW.md)
accepts its stated family. The registry records the other two packages as
having reproducible exact producer evidence with no external review located
at the cutoff. None of these upper bounds applies to arbitrary new pieces,
new interface positions, or point sets outside the specified union.

The H21 count is the arithmetic consequence
`sum(binomial(35,j),j=0..27)`, since `21+18j<=508` exactly when `j<=27`.
No enumeration of billions of assemblies is required by the pasting proof.

## 4. Strong fixed-host exclusions

For a fixed graph H, a verified colouring of `H-v` makes v mandatory in
every non-four-colourable subgraph of H. More general positive colouring
covers can force larger minimum orders. These arguments cover arbitrary
vertex subsets and edge deletions **inside the pinned host**.

| Pinned strict host | Complete exclusion | Evidence status |
|---|---|---|
| [de Grey 1581](../hadwiger_nelson_degrey1581_terminal_cover/README.md) | Every subgraph through order 510 is four-colourable; 511 full-host omission words force 511 mandatory vertices | [Accepted review](../hadwiger_nelson_degrey1581_terminal_cover_review1/README.md) |
| [Native T721 spindle, 1441 points](../hadwiger_nelson_t721_weighted_cover/README.md) | Every subgraph through order 573 is four-colourable; 475 mandatory vertices plus an exact weighted-degree bound force at least 99 others | [Accepted review](../hadwiger_nelson_t721_weighted_cover_review1/README.md) |
| [Joint769 fresh-triangle host](../hadwiger_nelson_joint769_order508_closure/README.md) | Every subgraph through order 508 is four-colourable, using 503 positive rows and 15 covering rows for 143 residual cases | Exact producer certificate; no external review located at the cutoff |

The lower critical orders 511 and 574 are not assertions that obstructions
of those orders exist. None of these bounds is a lower bound for all plane
unit-distance graphs. Moving vertices, adding points, or changing the host
requires a new argument. These source identities and their scopes remain
preserved; this consolidation reruns none of their large geometry checks.

The publication refresh also found the new
[T375 marked-relation minimality package](../hadwiger_nelson_small_triangle_forcer375_vertex_minimal/README.md),
committed at Discovery Net height 3841. It supplies 372 deletion colourings
showing that every proper terminal-containing vertex subset permits a
monochromatic marked triangle, whereas the full four-colourable T375 forbids
that relation. This is inclusion-minimality for one conditional obstruction
inside one fixed support. It is neither global gadget minimality nor an
unrestricted five-chromatic signal. Its document identity and source commit
are recorded in [PROVENANCE.json](PROVENANCE.json). This late intake was read
for compatibility; it is outside the twelve-package identity audit, and its
verifier was not rerun here.

## 5. Frozen pilot evidence and the remaining gate

The following are finite sampled outputs with positive colour certificates:

| Pilot | Saved labelled outputs | Verified conclusion |
|---|---:|---|
| [CM213 norm windows](../hadwiger_nelson_cm213_candidate_pilot/README.md) | 32 graphs, each with 508 vertices | Each has a proper four-colouring |
| [Colour-guided contact growth](../hadwiger_nelson_contact_growth_pilot/README.md) | 4 graphs, each with 508 vertices | Each has chi=4; final words cover 1,984 labelled prefix queries |
| [EI G79 circumcentre growth](../hadwiger_nelson_ei79_circumcenter_pilot/README.md) | 1 graph with 508 vertices and 2,561 edges | A proper four-colouring covers all 430 queried prefixes |

The total 37 counts saved outputs, not distinct isomorphism classes or a
complete family. The caps are closed. A solver UNKNOWN would also give no
negative theorem; none of these saved final outputs is UNKNOWN. A high edge
count, the rejection of many successive colour words, a conditional
monochromatic-terminal contradiction, or a non-Euclidean abstract graph
does not replace an actual non-four-colourability certificate.

Before substantial expansion of a materially different mechanism, the
standing gate requires an actual unit-distance graph that cannot be
four-coloured. A reviewable signal must specify exact distinct points and
the intended edge relation, verify unit lengths, and supply an independently
checked refutation of its unrestricted four-colouring formula. Symmetry
pins must be justified by colour renaming or another sound argument.
A strict-graph claim additionally needs every point pair classified.

A graph larger than 508 can be a positive research signal while missing the
record target. Meeting the target requires at most 508 vertices and a
proper five-colouring as well as the lower-bound certificate. None of the
results assembled here achieves that. No new mechanism or fourth unrelated
growth pilot is started in this consolidation.

## Evidence boundary of this package

The source proofs carry their original mathematical and computational trust
boundaries. The registry distinguishes five located acceptance reviews from
producer-only or sampled evidence. A source-identity audit checks bytes and
published manifest entries; it is not an independent verification of every
cited theorem. The new seven-point guard is checked independently of all
historical package code. This note claims synthesis and scope discipline,
not priority, formalization, a new peer review, or global minimality of 509.
