# Twenty global interfaces and an 8,585-point EI composition

The exact Exoo–Ismailescu composition can be recompiled using **20 small-triangle
restrictions per half**, yielding a specified non-four-colourable plane
unit-distance graph on **8,585 distinct points**. The previous measured
[minimum-premise assembly](../hadwiger_nelson_ei_physical_order/README.md) has
48,365 points. The reduction uses all actual unit edges between overlapping
G49 copies when proving the outer endpoint implication.

The 20 selected restrictions are **inclusion-minimal on the fixed 1,167-point
intermediate half**: each single deletion has a checked four-colouring with
different outer endpoint colours. No minimum-cardinality claim over all
possible supports is made. The completed graph's exact chromatic number has
not been computed. This is not a graph on at most 508 vertices or a record
improvement; no smallest-known composition claim is made.

## Precise intermediate graph and theorem

The source is Exoo and Ismailescu,
[The chromatic number of the plane is at least 5 — a new proof](https://arxiv.org/abs/1805.00157v1).
The numeric G40 and G49 tables, attachment convention, and the mask 1682
selection are hash-pinned from the
[local interface package](../hadwiger_nelson_ei_interface_minima/README.md).
Coordinates have the paper convention

```
[a,b,c,d] = ((a sqrt(3)+b sqrt(11))/36, (c+d sqrt(33))/36).
```

Take G40 and attach the orientation-preserving labelled G49 copy to each of
the 53 selected distance-sqrt(11/3) pairs. Deduplicate all points and use **every
actual unit-distance edge**, including edges between copies. This gives a
graph J with 1,167 vertices and 6,472 edges. Sort its integer quadruples
lexicographically for zero-based labels. Its outer endpoints are
O = `[0,0,0,0]`, label 804, and V = `[0,0,96,0]`, label 820.
They are distance 8/3 apart.

The eight previously required small triangles in each G49 placement give
321 distinct physical target triangles in J. The 20 sorted triples in
[certificate.json](certificate.json) form a subset S of these targets.
Each is equilateral of side 1/sqrt(3). The proved statement is:

> Every proper four-colouring of J in which every triangle in S is
> nonmonochromatic assigns the same colour to O and V.

For each t in S the certificate also supplies a proper four-colouring of
all J, with O coloured 0 and V coloured 1, which makes exactly t monochromatic
among S. Thus no proper subset of this particular S proves the implication.
These witnesses do not certify the necessity of any triangle among all 321
possible choices, nor the necessity of physical T375 copies after additional
cross-edges have been introduced.

## Finite proof and independent checks

The Boolean variable `4*v+c+1` says vertex v has colour c. Seven clauses per
vertex impose exactly one of four colours; four clauses per unit edge impose
different endpoint colours; four clauses per selected triple exclude its
being monochromatic. Two unit clauses pin O to colour 0 and V to colour 1.
Any proper colouring with distinct endpoint colours can be globally renamed
to these pins. The resulting formula has **4,668 variables and 34,139 clauses**.
The triangle clauses are logical premises, not invented unit edges.

CaDiCaL produces a refutation and DRAT-trim checks it and supplies LRAT hints.
The separate standard-library [lrat.py](lrat.py) then checks every addition
using only the original clauses and explicitly listed unit propagations.
For an added clause C it assumes the negation of C, checks that each indicated
clause is unit or conflicting under the current partial assignment, and
requires a conflict. Thus each addition follows from the current database.
Deletions preserve satisfiability. The final empty clause proves UNSAT.
The checker rejects RAT hints, missing clauses, non-unit hints, and incomplete
proofs. It checks **22,714 clause additions and 1,188,643 hint steps**.
Neither the solver's UNSAT flag nor the trimmer's success flag is trusted by
this final check.

[geometry.py](geometry.py) uses generic exact arithmetic in the bit-indexed
basis for Q(sqrt(3),sqrt(11),sqrt(247)). For its unit-edge enumeration an exact
homomorphism modulo 1021 is only a necessary filter; every survivor is checked
over the original field. [audit.py](audit.py) instead derives the isometries
directly in the four-coordinate convention and checks all **680,361 point
pairs** by the formula

```
1296 * squared_distance =
3 da^2 + 11 db^2 + dc^2 + 33 dd^2 + 2(da db + dc dd) sqrt(33).
```

The two implementations agree point by point, edge by edge, and triangle by
triangle. All 20 deletion colourings are checked directly. The controls cover
1,056 complete named-colour assignments in small encoding instances, two valid
RUP fixtures including derived nonempty clauses, and 16 malformed proof or
witness cases. Normal and optimized Python verification agree.

## Physical construction and exact order

For each of the 20 selected triangles, attach one isometric copy of the
[T375 terminal gadget](../hadwiger_nelson_small_triangle_forcer375/README.md).
Order the target triangle by J's labels. Use the map taking the first two
marked terminals to the first two targets, reflecting if needed to match the
third. These choices are fully specified by `completed_half()`.

The verifier reconstructs the T375 support from its orbit representatives,
checks its 1,661 unit edges and supplied proper four-colouring, and replays
its exhaustive monochromatic-terminal obstruction: **735 nodes, 367 conflicts**.
Each frame is an injective isometry with all three terminal matches verified.
Therefore any proper four-colouring of the completed half H satisfies the
20 triangle premises on J, and hence gives O and V the same colour.

Both independent coordinate implementations give **4,293 distinct points**
in H. Rotate H about O through the angle with cosine 119/128 and sine
3 sqrt(247)/128. The rotation preserves distance, and

```
2 * (8/3)^2 * (1 - 119/128) = 1.
```

Thus V and its rotated image are adjacent. In a hypothetical four-colouring
both would have O's colour, which is impossible.

All points of H lie in Q(sqrt(3),sqrt(11))^2. Since sqrt(247) is independent
of that field, a nonzero point of H cannot have its rotated image in that
same plane over the field: the sqrt(247) coefficients in the two coordinates
would force both original coordinates to be zero. The halves consequently
intersect only at O. Exact tuple intersection independently confirms this, so
the full physical order is **2*4,293-1 = 8,585**.

The graph is the strict unit-distance graph on this point union. Its full
edge set need not be enumerated for the non-four-colourability proof: every
edge used in a component remains a genuine unit edge, and additional edges
can only strengthen the contradiction. The point-set hashes are in
[expected.json](expected.json). No floating-point equality is used.

The second half rotates the entire first completed half, including its
chosen T375 placements. We do not claim this union is an induced subgraph of
the earlier 48,365-point canonical realization. The earlier 755-point bound
for the staged full-G49 architecture remains valid. Its direct-overlap lane
is not reopened here.

## Reproduction

Use Python 3.11 and the standard library for checking. Generating the omitted
proof additionally uses `python-sat==1.9.dev15` with CaDiCaL 1.9.5 and
[DRAT-trim](https://github.com/marijnheule/drat-trim). The tested trimmer source
commit is `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`; build it with `make`.
The trimmer's output is independently checked, rather than trusted.

From this package directory in a full repository checkout, with the trimmer
available at `/path/to/drat-trim`, run:

```sh
python3 -m pip install -r requirements.txt
python3 -B produce_proof.py --output /tmp/hn-ei-global --drat-trim /path/to/drat-trim
python3 -B verify.py --lrat /tmp/hn-ei-global/half.lrat
python3 -O -B verify.py --lrat /tmp/hn-ei-global/half.lrat
python3 -B controls.py
sha256sum -c SHA256SUMS
```

The proof generator checks the pinned byte identities in
[proof_manifest.json](proof_manifest.json). The 0.47 MB CNF, 6.43 MB DRAT, and
9.70 MB LRAT are generated outside the repository; they are not committed.
The source and compact 20-word certificate are sufficient to regenerate them.
The final formula solved in 2.57 seconds with 20,873 conflicts on the recorded
machine; DRAT verification took 1.81 seconds. Timings are observations, not
resource guarantees. The full independent verification also reconstructs
geometry and replays T375.

Optional discovery reproduction:

```sh
python3 -B search.py --output /tmp/hn-ei-global/reproduced_certificate.json
```

This is one deterministic descending deletion pass with core restriction,
20,000 conflicts per deletion query and 1,000,000 total deletion conflicts
available. It completed all 154 necessary queries in 89,383 conflicts with no
UNKNOWN outcomes, reproducing the certificate byte for byte. It did not prove
cardinality optimality. The initial conditional gate used 2,649 conflicts.

Remaining trust is the mathematical encoding and isometry argument, source
transcriptions and pinned inputs, the small checker implementations, CPython
exact arithmetic, the finite T375 search and its documented colour-symmetry
argument, and ordinary hardware. There is no proof-assistant formalization
or external-author review claim.

## Durable handoff

This is the physical-order milestone following the EI handoff and the
755-point overlap obstruction. The result replaces 642 distinct triangle
obligations by 40 placed forcing copies in a new exact compilation.
The next reduction would need to use the completed physical graph's additional
constraints or change the implication mechanism. The 20 deletion words forbid
further pure deletion of these logical premises on J with this proof format.
No such next phase has been run here. No cap, geometry-growth family, or retired
support is extended.
