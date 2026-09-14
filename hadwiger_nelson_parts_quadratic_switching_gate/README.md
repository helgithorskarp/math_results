# Quadratic switching cannot improve the Parts vertex record

**Every subgraph on at most 508 points of the exact 644-point support below
is four-colourable.** A graph homomorphism onto the original Parts graph,
together with its checked vertex-deletion colourings, proves this uniformly.
The support has 3024 complete strict unit edges. This closes the proposed
independent quadratic-conjugate switching construction, including choices
that retain points from both conjugates.

This is a restricted construction exclusion, not record progress or a global
lower bound for plane unit-distance graphs. The whole support contains the
published five-chromatic Parts graph on 509 vertices, so its minimum
five-chromatic subgraph order is exactly 509, using that published theorem
for the matching upper bound.

## Physical construction and budget

Let V=L union S be the published Parts coordinates, with labels
L={0,...,373} and S={374,...,508}. Their real coordinates lie in

    K = Q(sqrt(3),sqrt(5),sqrt(11)).

Let sigma be the automorphism fixing sqrt(3) and sqrt(11), and negating
sqrt(5), applied to both Cartesian coordinates. It fixes L pointwise and
fixes no point of S. The frozen envelope is

    H = UD(L union S union sigma(S)).

All 644 points are distinct. The intended capped construction omitted one
label of S and independently chose v or sigma(v) for each remaining label.
Its budget was 374+134=508 actual points. The positive physical inputs were
the two coherent five-chromatic Parts drawings, V and sigma(V). No new
standalone terminal-pair relation was being screened.

The theorem is stronger than the original selection gate: it covers every
at-most-508-point subset of H, even those deleting large-block points or
retaining both v and sigma(v) for some labels. It does not cover other field
automorphisms, new translations, different parents or points outside H.

## Exact retraction and colouring proof

Define pi:H->V by pi(v)=v for v in V and pi(sigma(v))=v for v in S.
Exact reconstruction establishes:

1. L, S and sigma(S) are pairwise disjoint. The two full drawings share
   precisely L.
2. There are **no unit edges between S and sigma(S)**: all 135 squared by
   135 cross pairs are checked exactly.
3. Every edge of H maps under pi to an edge of the original strict unit
   graph G=UD(V).

For edges within V the third assertion is immediate. Edges in sigma(V)
map to old edges because sigma preserves the equation
(x1-x2)^2+(y1-y2)^2=1 and is an involution. The mixed-edge exclusion leaves
no other case. The executable checker also tests the projection on all
3024 physical unit edges directly, rather than relying only on this argument.

Now take any W subset H with |W|<=508. Its image pi(W) omits some original
label m, since V has 509 labels. Let c_m be a proper four-colouring of G-m.
Then

    c(w) = c_m(pi(w)),  w in W,

is proper: a physical unit edge maps to an old unit edge, whose ends have
different c_m colours. The map need not be injective. No symmetry assumption
about W or about its colouring is used.

This is an application of the standard graph-homomorphism colouring argument.
The exact geometry and complete checked collection of c_m are the finite
certificate. It is not an enumeration of switch assignments or a SAT timeout.
No chromatic impossibility premise is needed for the at-most-508 exclusion.

## Reproduction

Use Python 3.11 or later and the standard library, in a full repository
checkout. From this directory run:

```sh
python3 -B verify.py
python3 -O -B verify.py
sha256sum -c SHA256SUMS
```

Expected status:
`QUADRATIC SWITCHING HOST CLOSED THROUGH508 BY EXACT COLOURING RETRACTION`.
The compact exact quantities and canonical hashes are in
[expected.json](expected.json). Inputs are pinned in
[manifest.json](manifest.json): the scale-96 Parts coordinate table and the
published [vertex-deletion colouring certificate](../hadwiger_nelson_parts509_criticality/certificate.json).
No new solver, private trace or omitted proof file is needed.

The checker reconstructs all 207046 unordered point pairs using integer
arithmetic in the mask basis
(1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165)). It checks
all 509 original deletion words on 1238094 retained old edges. It then
explicitly pulls each word back to H with the corresponding whole fibre
deleted, checking another 1533168 retained physical edges. It checks a proper
five-colouring of H by the same map. That positive five-colouring does not
by itself prove a five-chromatic lower bound.

There are 64 basis-product/automorphism controls, four rejected malformed
certificates or support requests, and 138 concrete support-colouring checks.
An author cross-check uses the prior upper-triangular squared-norm routine,
scale 288 and a different point order. The entire coordinate and edge sets
agree after exact relabelling; matching counts alone were not used.
[validation.json](validation.json) records the executed checks and timing.

To obtain an explicit four-colouring of any selected support, provide a JSON
list of at most 508 distinct host indices. Indices 0,...,508 denote V; index
v+135 denotes sigma(v) for 374<=v<=508.

```sh
python3 -B verify.py --support /scratch/selected-indices.json \
  --colouring-out /scratch/selected-colouring.json
```

The output names an omitted original label and lists the pulled-back colour
of every selected point. The checker rejects invalid indices, duplicates,
or a support above the stated cap. Optional `--geometry-out /scratch/host.json`
writes exact coordinates, complete edges and pi outside the repository.

## Sources, trust and stopping decision

The original graph and its published five-chromaticity are from Jaan Parts,
[*Graph minimization, focusing on the example of 5-chromatic unit-distance
graphs in the plane*](https://arxiv.org/abs/2010.12665v2). The imported
non-four-colouring theorem is used only for the statement that H contains a
509-point five-chromatic subgraph. The new exclusion itself rechecks every
positive word it uses and trusts no native solver verdict or negative proof.

Trust remains in the two pinned data files, the ordinary field and
homomorphism arguments, Python integer arithmetic, implementation correctness
and runtime/hardware. This is author validation, not independent external
review or proof-assistant formalization. The word decoder is implemented
locally and does not import the original certificate producer.

The complete switching family is retired at this structural obstruction.
The two conjugate drawings supply no new interaction capable of evading the
old vertex-deletion colourings. No further automorphism, phase, host, seed or
parent variation was launched from this negative result. The separate
point606 critical core remains banked, and the fixed Parts a=8 transfer
decision belongs to its existing researcher.
