# A blue empty pair has precisely the Core194 blue common neighborhood

Use a red/blue complete graph with no monochromatic K5. Let C0,...,C3
be disjoint red triangles whose twelve-vertex induced graph is Core194,
word `100110110110110100` on pair order01,02,03,12,13,23. Let F be
outside vertices uniform to each Ci, and write S(f) for the indices
joined red to f. Suppose u,v in F have empty signatures and uv is blue.

## No common blue fixed neighbor

If a third f in F is blue to both u and v, it cannot miss two of the
red triangles Ck,Cl: there is a blue cross-edge ab between them, since
otherwise their six vertices form a red K6. Then u,v,f,a,b would form
a blue K5. Thus every such f must have |S(f)|>=3.

But each complementary nine-vertex subcore of Core194 has a red K4.
For omitted indices0,1,2,3, literal witnesses are

```
{3,4,7,10}, {0,1,7,10}, {0,3,9,10}, {0,3,6,7}.
```

A vertex red to any three triangles would complete a red K5 with the
corresponding witness. Hence |S(f)|<=2, a contradiction. Therefore

```
{f in F\{u,v}: uf and vf are blue} is empty.
```

This elementary local lemma requires no degree bound, moving blue
triangles, ordering, or additional automorphism. It applies to any
chosen blue pair of empty-signature vertices. The first argument is
the four-triangle counterpart of the earlier three-triangle empty-pair
argument; no priority is claimed for that clique-completion mechanism.

The compact certificate exhausts all sixteen signatures of f. Eleven
signatures of size at most two have an explicit blue K5 on u,v,f and
a blue core edge. The five larger signatures have an explicit red K5
on f and a core K4. Its local labels are core0,...,11, u=12, v=13, f=14.
All colors in each fifteen-vertex obstruction are specified by the core,
the signature and the three blue fixed edges. The independent checker
inspects the ten literal edges of each recorded five-set.

## Feasibility and the blue-edge hypothesis

The blue-pair fourteen-vertex fixture adjoins two empty-signature
vertices to Core194 and joins them blue. It has42 red edges, no
monochromatic K5, and zero common blue fixed neighbors. Thus the
blue-pair hypotheses are consistent locally and the bound zero is sharp.

The red-pair fifteen-vertex fixture adjoins three empty-signature
vertices u,v,w. Set uv red and uw,vw blue. It has43 red edges and no
monochromatic K5, but w is a common blue fixed neighbor of u,v. Thus
the zero bound cannot be imposed on a red empty pair. Both fixtures
preserve the order-three action on the four core triangles. They are
small validation graphs, not43-vertex target graphs.

The two compact edge lists specify the vertex count on the first line
and all red edges as unordered increasing pairs thereafter; every other
pair is blue. The standalone auditor checks all2,002+3,003=5,005
five-sets, exact core colors, empty signatures, the pair color, action
invariance and the stated common-blue fixed-neighbor counts.

## Complete pair split in the full43-vertex extension

The preceding complete multiplicity exclusion shows that Core194 has
at least two empty fixed signatures in any hypothetical full graph
with action `1^10 3^11` and four red/seven blue moving triangles. The
accepted existing full-row order therefore makes u=33,v=34 empty.
No new ordering is imposed. Their edge, primary166, is either red or
blue, giving two disjoint and exhaustive full cases.

For the red case append just the unit166. For the blue case append
-166 and, for each other fixed f=35,...,42, the necessary binary clause

```
x_(33,f) OR x_(34,f).
```

The exact pairs of primary IDs are (167,175),...,(174,182). These eight
clauses express the proved absence of a common blue fixed neighbor.
They are not imposed in the red branch. All remaining fixed edges and
moving incidences remain free subject to the complete inherited base.

Every internally blue moving triangle is uniform to u and v. It cannot
be blue to both when uv is blue, since its three vertices with u,v
would make a blue K5. The seven clauses expressing this are already
in the complete parent:

```
166 OR L(33,i) OR L(34,i),   i=4,...,10,
```

where L(f,i)=211+11*(f-33)+i. The auditor verifies their presence in
the inherited base; no duplicate clauses are appended. Since u,v are
blue to the entire core, the local lemma and these triangle constraints
show that, in the full blue branch, their common blue neighborhood is
**exactly the twelve red-core vertices**.

The local lemma is universal for any blue empty pair. A computational
restriction obtained for just the first ordered pair must not be
silently generalized to the colors of all empty pairs. No arbitrary
pair is moved into the first two rows of an already normalized formula.
Refuting both full color cases would exclude Core194 entirely; refuting
one would restrict only the remaining normalized first-pair branch.

## Entire base, certificates and trust

The base is the entire [multiple-empty Core194 formula](../ramsey_r55_order3_eleven_core194_multiplicity),
with34,320 variables /617,936 clauses,24,968,424 bytes, SHA256
`214cbdad727ec3f48e97e62246134b341719277981119bd6b89baa5475b2dbb4`.
It retains all parent clauses, core units, intrinsic anchors, sharp pair
cuts, both empty prefixes and all350 guarded attachment clauses.
The red child has617,937 clauses; the blue child has617,945 clauses.
Every body byte is retained. No variable or normalizer is added, and
no degree profile or external neighborhood is selected. The previous
UNKNOWN is not a proof premise.

The isolated rebuild regenerates the entire inherited preparation and
multiple formula without rerunning old solver cases. An auditor importing
no producer reconstructs320 primary meanings from physical edge orbits,
checks every base byte, child clause, header and EOF, and locates all
seven inherited moving-cycle clauses. It exhausts131,072 assignments to
the pair edge and sixteen other fixed-edge incidences: all65,536 red-pair
patterns remain allowed, and exactly3^8=6,561 blue-pair patterns remain.
The two cases are disjoint and their union is precisely the new guarded
fixed-incidence condition. Twenty-two malformed local/case/formula inputs
must be rejected under normal and optimized Python, with matching reports.

Any UNSAT exit requires full DRAT checking, including RAT steps, then
a second replay after fresh complete reconstruction. UNKNOWN excludes
nothing; its partial trace is not a refutation or saved solver state.
A SAT target requires a compact edge list and literal five-set checks.

The local lemma and certificate have a standalone solver-free check.
Full exclusions would additionally import the preceding one-empty
closure, its guarded base and their review boundaries. The parent,
core cover, intrinsic anchors, forced-empty theorem and maximal Core194
exclusion have accepted reviews at their stated scopes. The multiplicity
closure and guarded full encoding have author checking. New local and
full claims await independent review. Cumulative counts retain older
empty-signature-specific review gaps. Other trust comprises the imported
R(4,5)=25 degree theorem, unformalized reductions, exact source/runtime/
compiler/hardware, SHA256 and the full DRAT checker. Internal checks are
not peer review or formalization. No new Ramsey lower bound is asserted.
