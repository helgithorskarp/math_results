# Both central-root neighborhood densities are realizable

There are explicit20-vertex graphs with no red K4 or blue K5, containing
the literal critical eight-vertex core and the required marked pair,
at **both92 and93 red edges**. Thus this central-neighborhood necessary
condition does not exclude either density. The two small graphs provide
concrete inputs for a future22-vertex opposite-side and cross-edge test.

This is **not** a43-vertex Ramsey graph, an extension certificate, a
hard-profile/470-case survivor, or a Ramsey-bound improvement. No claim
of novelty for small Ramsey graphs, SAT, or neighborhood gluing is made.
The contribution is this exact guarded feasibility checkpoint and its
fully specified extension margins, not a census of all such graphs.

## Literal local statement

Use local labels0,...,19. The marked vertices0,1 have a blue mutual edge.
Let W={2,...,9}. In lexicographic order of the28 pairs of W, the BLUE-edge
bit mask is5388912. All other W pairs are red. Equivalently the eight-bit
red adjacency rows inside W are(30,45,115,179,205,206,180,120).
Both marked vertices are blue to every vertex of W.

Their complete red neighborhoods in the20-vertex graph are

```
N_R(0) = {10,11,12,13,18,19}
N_R(1) = {14,15,16,17,18,19}.
```

They have red degrees6 and6, with exactly two common red neighbors.
The remaining ten vertices have marked red patterns1,2,3 with sizes4,4,2.
Exactly65 pairs are fixed, of which30 are red:18 within W and12 between
the marked pair and the ten remaining vertices. The other125 pairs
(80 W/remaining and45 remaining/remaining) are unrestricted before the
Ramsey and edge-count conditions. No ordering, automorphism, catalog,
distinct-footprint or other local-degree assumption is used.

[H92.json](H92.json) and [H93.json](H93.json) give the two sorted red-edge
lists. An omitted pair is blue. The density92 graph has104 red triangles
and72 blue K4s; the density93 graph has105 red triangles and68 blue K4s.
Neither has a red K4 or blue K5. Adding a new vertex20 red to all twenty
vertices gives a full Ramsey(5,5;21) graph, with112/113 red edges; these
cones are checked directly but are not stored separately or advertised
as new Ramsey bounds.

## Transfer from the43-vertex guard

This scope comes from the literal core/cell model in the
[joint-three-outside artifact](../ramsey_r55_critical_path_joint3_realization),
source9cd9cc7f8b23008f7081f8d3028325e57b32b0de. In its original labels,
the three degree20 vertices are0,1,2 and all other vertices have degree21.
Original vertex0 is red to1,...,10, the edge12 is blue, and1,2 are blue
to3,...,10. The BLUE core on3,...,10 has mask5388912. Outside root-signature
groups2,3,4,5,6,7 have sizes9,4,9,4,4,2 on their displayed labels. A
signature bit i means red adjacency to root i.

Suppose a full Ramsey(5,5;43) graph realizes this guard and the selected
central root caps t_R(0)<=93 and t_B(0)<=107. These caps are hypotheses,
not new unconditional bounds proved by this package. Its red neighborhood
H=G[N_R(0)] consists of original labels

```
1,2,3,4,5,6,7,8,9,10,20,21,22,23,33,34,35,36,41,42.
```

This list is the map from local H labels0,...,19 to original labels.
A red K4 in H would join original0 to make a red K5; a blue K5 in H is
already forbidden globally. The signature cells give exactly the
marked6/6/common2 interface above. Hence a full target necessarily
contains some H of the displayed kind, although not necessarily either
particular exhibited H.

Let m=e_R(H), O be the22 vertices blue to original0, and C=e_R(H,O).
The degree profile gives450 total red edges. The sum of prescribed global
degrees on H is2*20+18*21=418. Its20 red edges to original0 yield

```
C = 418 - 20 - 2m = 398 - 2m,
e_R(O) = 450 - 20 - m - C = 32 + m,
e_B(O) = 231 - e_R(O) = 199 - m.
```

Thus the selected caps imply92<=m<=93. The two witnesses prove both
values survive this NECESSARY local graph test; they do not establish
the converse extension implication. This derivation needs no external
small-Ramsey-number value or enumeration-completeness premise.

## Exact future extension interface

For each local H vertex v, its required red degree into O is
19-d_H(v) for v=0,1 and20-d_H(v) otherwise. The complete20-entry rows and
original labels are in [verification.json](verification.json), independently
matched by the bit checker.

| H density | Red H/O edges | Red edges in O | Blue edges in O |
|---|---:|---:|---:|
|92|214|124|107|
|93|212|125|106|

O has original labels11..19,24..32,37..40. Its marked red patterns are
1 on the first9,2 on the next9,3 on the last4. This fixes each marked
vertex's13 required red cross edges. Each O vertex would have total
red degree21, all O/center edges are blue, and O must have no red K5 or
blue K4. The latter follows by joining any blue K4 to the center.
These requirements do not include all mixed K5 prohibitions, other local
caps or the3,140 global root-union inequalities. Full gluing must retain
the appropriate constraints and audit its quantifiers.

No O graph, cross-edge realization or full43-vertex extension is claimed
or searched in this package. Refuting the extensions of these TWO chosen
H graphs would not exclude all possible central neighborhoods. A local
feasible graph is not a valid global hard-profile witness by itself.

## Verification and reproducibility

Use CPython3.11.2 and the standard library. From the repository root,
using fresh report paths outside Git:

```sh
python3 -B ramsey_r55_critical_path_central_neighborhood/verify.py --report FRESH_LITERAL.json
python3 -B ramsey_r55_critical_path_central_neighborhood/bitcheck.py --report FRESH_BIT.json
python3 -B ramsey_r55_critical_path_central_neighborhood/crosscheck.py --report FRESH_CROSS.json
```

`verify.py` checks literal pairs and every4-/5-set; `bitcheck.py` uses
bit-intersection clique recursion and a separate literal W-row encoding.
Neither imports the producer, encoder or solver. Both check the exact
marked/core interface, density, absence of the forbidden cliques, cones,
and degree-algebra margins. The literal checker inspects4,845 H four-sets,
15,504 H five-sets and20,349 cone five-sets per graph.

`crosscheck.py` compares all report fields and every actual red-triangle
and blue-K4 mask, not only their counts:209 red triangles and140 blue K4s
across the two graphs. It tests12 malformed graphs per density, each
rejected by both checkers. These include a balanced free-pair mutation
preserving the fixed interface and density while creating a red K4.
They are checker controls, not local-descent searches.

Normal and optimized Python yield byte-identical reports. Fresh generation
from the self-contained public source reproduces both formulas, graphs
and SAT traces byte for byte. `run.json` preserves compact initial/replay
observations; its nested pending-audit status names the generator stage,
completed by the separate graph audits. The mathematical certificates
are the small graphs, not the SAT output or discovery encoding.

Graph SHA256 identities:

```
H92 926c18173764c02a45d6e6d46dc001eddff6a161570bdc3b1efcd8a24539f466
H93 2e33d5c585ef3af1beff09dfd76cfc7484f8ea1ea1dfadcc957923ec033cda74
```

For optional discovery of both cases, use a fresh external work directory:

```sh
python3 -B ramsey_r55_critical_path_central_neighborhood/generate.py --work FRESH_WORK --kissat /absolute/path/to/kissat --seconds 90
```

The generator simplifies every red-K4/blue-K5 restriction against the65
fixed pairs and obtains5,458 base clauses (2,140 possible red K4s and
3,318 possible blue K5s). It then enforces exactly62/63 red free pairs.
It verifies a complete SAT assignment against every clause before decoding.
There is no symmetry break. `encoding.py` copies the joint3 threshold
primitive, SHA256902f06f7bd3ec062aaa717743bd972ab0f3fcaaff43d3ade2197b4252820dbcd;
the unused lex routine remains for exact source identity. No ancestor
graph or negative solver conclusion is imported.

Density92 CNF:6,047 variables,28,960 clauses,530,459 bytes,
SHA256e04c4201f7a18087e86d8a11c822b5fbbe1c4eb3c77101500419d4731a97f6b6.
Density93 CNF:6,109 variables,29,207 clauses,534,456 bytes,
SHA256433ed52f8882ff09975146d4a3372caadaf0e5638974f40978df35c82988ddf6.
Each case had a90-second cap and solved in approximately0.215 seconds
in both initial and public-source runs; each build took about0.108 seconds.
Peak solver RSS ranged21,284..26,036 KiB. These are observations, not
performance guarantees. Kissat4.0.4 source
8af8e56f174b778aef3aa45af9f739b2a5f492c2, binary SHA256
2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45.
CNFs, SAT traces, logs and binaries are outside Git. SAT traces are not
refutations or restart states; no DRAT refutation replay is claimed.

## Scope, coordination and stopping boundary

This is author-written exact verification using two implementations,
not independent peer review or formalization. The positive graph claims
do not trust a solver or cardinality encoding. Ordinary finite reasoning,
exact Python/hardware and file identities remain trusted. No independent
whole-formulation audit or classification of all125-bit assignments is
claimed or needed for the two witnesses.

The preceding full joint-four-outside model was checkpointed locally with
UNKNOWN at180 seconds; it is not retried. This local H test is necessary
for the full target, not equivalent to that relaxation: its blue-K5
conditions include some pure-five-outside sets absent from joint4. It is
also not the older fixed-H20 marked7/5 disjoint-neighborhood family.
All older fixed-tail closures, order-five and degree19-W conclusions,
global66/271 counts and470 filters retain their previous scope.

The initial incremental graph scan through3189 found independent acceptance
of the teammate's Core194 blue-pair lemma at3182, source
d59a572af02f942157d741ce1ae4be948e3b1e2e. Its new complete320-primary pair
models at3186, source3240433c5f70c148a4c91b57edd22dc481f0d7fe, both remain
UNKNOWN and were then unreviewed. The external3188 complementary-K4 criterion
generalizes that symmetry-local argument under uniform triangle incidence;
it does not apply automatically to this non-symmetric core. Bodies and the
new teammate README were read, not replayed/imported. The symmetry lane
and its17/9,153 residual boundary remain separate.

The final incremental refresh through3191 found acceptance of the new
direct Core194 equivalence and coverage at3190, review source
f36e1aa39de45e209b174a81cd765deaa04d6d47. That review explicitly establishes
no solver verdict; both colors remain open. Its body was read, not replayed
or imported. No new feedback on the joint3/six-support ancestors was found.

This bounded two-density local milestone is complete. The next distinct
phase may test the opposite22-vertex graph and mixed constraints, while
keeping the chosen-H versus whole-family distinction explicit. Neither
that phase, another density/core nor a longer global solve has begun.
No background computation remains; the controller pass yields here.
