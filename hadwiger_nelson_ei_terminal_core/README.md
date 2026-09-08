# A 1003-vertex five-chromatic EI spindle

This package gives an exact unit-distance graph in the Euclidean plane with
**1003 vertices, 5241 edges, and chromatic number five**.
It reduces the previously verified
[8,585-point EI composition](../hadwiger_nelson_ei_global_interfaces/README.md),
whose exact construction and proof have received an
[independent acceptance review](../hadwiger_nelson_ei_global_interfaces_review1/README.md),
by extracting a **502-vertex terminal-equality graph** from one
completed physical half. The full new graph is an induced subgraph of that
fixed 8,585-point union. No non-unit triangle or distance-pair premises occur
in the new forcing proof.

This remains larger than the 508-vertex success target. It is not a record
improvement or a smallest-known construction claim. This bounded search does
not establish vertex minimality, minimum support size, or a lower bound for
other supports or constructions.

Saved deletion colourings also prove that **every subgraph of this fixed host
on at most 834 vertices is four-colourable**. Thus this support is closed at
record scale; the original 4,293-point parent and other supports are not covered.

## The exact graph and its chromatic number

Each row `[a,b,c,d]` in [coordinates.json](coordinates.json) denotes

```
((a sqrt(3)+b sqrt(11))/36, (c+d sqrt(33))/36).
```

The rows are distinct integer quadruples in lexicographic order. Let K be the
strict unit-distance graph on them, with every exactly unit-separated pair
included. K has **502 vertices and 2620 edges**. Its marked
vertices are O=`[0,0,0,0]` and V=`[0,0,96,0]`, at distance 8/3.
[certificate.json](certificate.json) contains a directly checked proper
four-colouring of K. A separate checked refutation proves that every proper
four-colouring of K assigns O and V the same colour.

In particular K has chromatic number exactly four. A three-colouring, if one
existed, could be turned into a proper four-colouring with different terminal
colours simply by giving V the unused fourth colour. This contradicts the
terminal theorem.

Rotate an entire copy of K about O through angle theta, where

```
cos(theta) = 119/128,
sin(theta) = 3 sqrt(247)/128.
```

The squared cosine and sine sum to one. Moreover
`2*(8/3)^2*(1-119/128)=1`, so V and its rotated image are adjacent. A proper
four-colouring of the union would give both of them O's colour, a contradiction.
This establishes the lower bound five without any assumption about additional
cross-edges.

The two halves intersect only at O. This follows from independence of
sqrt(247) over Q(sqrt(3),sqrt(11)), and is also checked by exact coordinate
comparison. Therefore the full graph has **2*502-1=1003**
vertices. The supplied proper five-colouring is checked on **all 5241
strict unit edges**, including cross-edges. The full graph consequently has
chromatic number exactly five. There is only one cross-edge between nonshared
vertices: V to RV. Its five-colouring copies the half four-colouring on both
sides and gives RV the fifth colour. Every edge is checked independently.

Full labels first list every unrotated row in its given order. They then list
the rotated rows in the same order with the origin omitted. The integer
coordinate tuples checked by `integer_audit.py` are divided by **4,608** in
physical coordinates. Their basis is

```
1, sqrt(3), sqrt(11), sqrt(33), sqrt(247), sqrt(741), sqrt(2717), sqrt(8151).
```

For a row `[a,b,c,d]`, these integer tuples are

```
unrotated x: (0,128a,128b,0,0,0,0,0)
unrotated y: (128c,0,0,128d,0,0,0,0)
rotated x:   (0,119a,119b,0,-3c,0,0,-3d)
rotated y:   (119c,0,0,119d,0,3a,3b,0).
```

No floating-point equality, clustering or assumed non-coincidence is used.

## Independent geometric verification

[geometry.py](geometry.py) enumerates half edges from the two exact
coefficients of a squared distance. It derives cross-edges from the coefficients
of the squared distance between p and Rq. If
`norm(p)=N0+N1 sqrt(33)`, `norm(q)=M0+M1 sqrt(33)` and
`p dot q=D0+D1 sqrt(33)` in coordinates scaled by 36, a cross-edge requires

```
64*(N0+M0)-119*D0 = 82944,
64*(N1+M1)-119*D1 = 0,
p cross q = 0.
```

The last equation is checked through both its sqrt(3) and sqrt(11)
coefficients. These are the complete four independent coefficient equations
for this rotation, including the shared-origin cases.

[integer_audit.py](integer_audit.py) independently constructs all full-graph
coordinates and checks **502503 vertex pairs** by generic multiplication
in the eight-element radical basis. The rational coefficient is a necessary
filter; every survivor has all seven other coefficients checked too. The two
algorithms agree edge for edge. Linear independence of the basis also makes
the distinct-tuple check an exact distinct-point check.

## A refutation containing only unit-edge constraints

For each vertex v, Boolean variable `4*v+c+1` means colour c. Seven clauses
require exactly one of four colours. Each genuine unit edge contributes four
inequality clauses. Two unit clauses fix O to colour 0 and V to colour 1.
Any proper four-colouring with different terminal colours can be renamed to
these pins. There are **2008 variables and 13996 clauses**;
there are no additional geometric or abstract premises.

Glucose3 generates the final DRAT refutation. DRAT-trim checks it and supplies LRAT
hints. The hash-pinned, standard-library
[positive-hint checker](../hadwiger_nelson_ei_global_interfaces/lrat.py) then
independently verifies every clause addition by the listed unit propagations
under the negated clause, concluding with the empty clause. It accepts no
RAT steps. The final check uses **71096 additions and
6638850 unit-propagation hints**. Neither the solver's result flag nor
the trimmer's success flag is trusted by this final check.

The proof is about the explicit reduced graph's actual unit edges. The old
G40, G49 and T375 forcing theorems are not premises of this new theorem.

## Source provenance and the bounded experiment

The source was the 4,293-point completed half H from the published
8,585-point EI composition. We first enumerated its **29,934 strict unit
edges** and found a proper four-colouring. The word is preserved in
[source_certificate.json](source_certificate.json). Thus H itself is
four-colourable; only its spindle provides the known non-four-colourability
signal for this reduction route.

One core-guided deletion pass tested source vertices in increasing order of
`(original degree, original label)`, protecting O and V. The exactly-one-colour
clauses have vertex selectors guarding only their at-least-one clause.
At-most-one clauses and edge clauses stay present. Inactive vertices can have
all four colour variables false, so the remaining formula is equivalent to
the induced retained graph with the fixed terminal pins.

A deletion is accepted only on UNSAT. An UNSAT assumption core may remove
further vertices at once. SAT and UNKNOWN retain the attempted vertex.
Requested budgets were 200,000 conflicts for the initial gate, 10,000 per
deletion query, and a total deletion allowance of 2,000,000. Backend conflict
counters may exceed an individual requested budget slightly; actual counts
are recorded rather than rounded down.

The bounded pass made **1533 queries**, used **2000001 deletion conflicts**,
and returned **32 UNKNOWN results**. It stopped at its nominal total budget (one backend conflict beyond the requested count), leaving 52 retained nonterminal vertices unattempted.
Afterwards, the deterministic removal of nonterminal vertices of current
degree at most three removed **0 vertices**. This rule preserves terminal
forcing: a four-colouring of the smaller graph with different terminal colours
would extend backwards greedily, since each removed vertex has at most three
coloured neighbours and neither terminal is removed. A fresh proof verifies
the final graph directly; it does not trust the deletion history or peeling.

The source indices are an exact embedding certificate.
[source_audit.py](source_audit.py) reconstructs H in two coordinate
representations, checks all 9,212,778 pairs and its four-colouring, and compares
each selected row with the published reduced coordinates. The provenance audit
is separate from the self-contained graph and chromatic-number proof.

The completed theorem does not say the bounded output is inclusion-minimal.
No UNKNOWN answer is used as evidence of colourability or impossibility.
No second ordering, cap extension, growth pilot, or further extraction from
the final spindle was run.

## Reproduction and trust boundary

Use Python 3.11+ for exact checking. Proof generation additionally needs
`python-sat==1.9.dev15` and
[DRAT-trim](https://github.com/marijnheule/drat-trim), built with `make` at source
commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Run from this directory in a
full repository checkout:

```sh
python3 -m pip install -r requirements.txt
python3 -B produce_proof.py --output /tmp/hn-ei-core --drat-trim /path/to/drat-trim
python3 -B verify.py --lrat /tmp/hn-ei-core/reduced.lrat
python3 -O -B verify.py --lrat /tmp/hn-ei-core/reduced.lrat
python3 -B source_audit.py
python3 -B controls.py
sha256sum -c SHA256SUMS
```

[expected.json](expected.json) records the exact point, edge and formula
identities and verification results. [proof_manifest.json](proof_manifest.json)
pins the generated CNF, DRAT and LRAT bytes. The 0.18 MB CNF, 36.00 MB DRAT and 49.26 MB LRAT stay
outside the repository. The compact exact coordinates, colourings and source
code are public.

Optional discovery reproduction, which repeats the longer bounded pass:

```sh
python3 -B search.py --output /tmp/hn-ei-core/search
```

The first CaDiCaL verification trace was rejected at its final empty clause.
It is not used as proof evidence. The unmodified Glucose3 trace passed ordinary
DRAT checking, the independent Python LRAT checker, and a separate compiled C
LRAT checker. The cause of the rejected trace is not diagnosed here. The final
Glucose3 proof files were regenerated byte for byte. The long deletion search
was run once, not repeated as a validation requirement. Source reconstruction
and the final proof are checked separately. Normal and optimized verification
agree. Controls exhaust 544 small named-colour encoding assignments and 512 arbitrary
Boolean assignments, compare 78 geometric fixture pairs, and reject five
malformed colourings. The reused
LRAT checker is hash-pinned to its already tested version.

Remaining trust is exact integer arithmetic and ordinary hardware, the
written correspondence between coordinates, clauses and graph colourings,
the small checker implementations, and the elementary spindle argument.
Source reconstruction additionally trusts the hash-pinned transcription and
geometry inputs; the final graph theorem needs only the explicit coordinates
and independently checked certificate. No proof-assistant formalization,
external-author review, global optimality or record improvement is claimed.

## Exact record-scale obstruction inside the final host

The 416 successful SAT deletion queries already supply local words which,
restricted to K with the attempted vertex omitted, are proper four-colourings
with different terminal colours. No extra solver query is needed for this
consequence. The selected 416 local vertex indices are in
[boundary_certificate.json](boundary_certificate.json).

For each such vertex on either side of the spindle, combine its deletion word
with the other half's fixed four-colouring. Their colours at O match, and the
two V colours differ, giving a proper four-colouring of the full graph with
that vertex omitted. Deleting either V leaves a one-vertex amalgamation that
is coloured by copying the half word. Deleting O leaves the two halves joined
only by the V--RV edge; swap colours 0 and 1 on one half.

[boundary.py](boundary.py) explicitly constructs and checks **835 full-graph
vertex-deletion colourings**: twice 416 nonterminal deletions, both V vertices,
and O. Consequently every non-four-colourable subgraph of this fixed
1,003-vertex host must contain all 835 designated vertices. Thus **every
subgraph with at most 834 vertices is four-colourable**, in particular every
subgraph of target order at most 508. The lower bound 835 is not claimed to be
attained. This obstruction does not cover other subgraphs of the original
4,293-point H, new supports, or arbitrary unit-distance graphs.

The 416 restricted words occupy 214,154 bytes and remain outside the repository;
their hash is in [boundary_expected.json](boundary_expected.json). They are
extracted from the saved output of the same bounded search, rather than obtained
by further queries. After reproducing the optional search above, run:

```sh
python3 -B boundary.py --search /tmp/hn-ei-core/search/reduction.json --words /tmp/hn-ei-core/deletion_words.json
python3 -O -B boundary.py --words /tmp/hn-ei-core/deletion_words.json
python3 -B controls.py --boundary-words /tmp/hn-ei-core/deletion_words.json
```

Main graph verification is independent of these optional boundary witnesses.
Reproducing this additional obstruction requires the generated words. Missing
witnesses are an incomplete boundary verification, not an accepted bound.
Three malformed boundary certificates are rejected by the optional controls.

## Handoff

This completes one material physical-order reduction from the positive EI
source, giving an explicit five-chromatic graph with 1003 vertices.
The source H is four-colourable. The retained K is four-chromatic and forces
its marked terminals equal. The final spindle is five-chromatic.
The fixed final host is now closed at record scale by the 835-vertex
mandatory set. Further progress would require a different support or a
material change to the physical construction. Such a next phase is not started here;
the bounded deletion cap remains closed.
