# Golomb-contact terminal triangles cannot activate three A159 forcers

Let `G` be the exact ten-point, eighteen-edge Golomb graph in the displayed
frame.  Define a finite family `F` of equilateral triangles of side `sqrt(7)`
as follows.  A triangle belongs to `F` when one marked vertex `a` is at unit
distance from at least two vertices of `G`, and a different marked vertex `b`
is at unit distance from at least one vertex of `G`.  Both orientations of the
third vertex are included.

**Theorem.** One proper four-colouring of `G` and every point occurring in
every triangle in `F` simultaneously makes all triangles in `F`
nonmonochromatic.  It is proper on the complete strict unit-distance graph of
that entire physical support, after every exact collision is identified.

Consequently, attach at most three full copies of the archived 159-point Parts
nonmonochromatic-triangle gadget, placing each designated terminal triangle in
`F`.  If gadget interiors are private and every new edge or overlap outside a
gadget occurs only among `G` and the designated terminals, the complete whole
assembly is four-colourable.  Three copies plus `G` have the raw bound

```text
10 + 3*159 = 487,
```

so this result closes the declared sub-509 Golomb-connector architecture.  It
does not produce a record candidate.

## Why this was a forcing-feature gate

The A159 source has a certified complete positive terminal relation: every
nonmonochromatic four-colour assignment on its equilateral `sqrt(7)` terminal
triangle extends through the full 159-point/646-edge graph.  The proposed
mechanism was to use the four-chromatic Golomb connector and its unit contacts
to make three such terminal triangles impossible to keep simultaneously
nonmonochromatic.  Had that small physical interface been inconsistent, the
three A159 copies would have replaced the three nonmonochromatic constraints
and yielded a direct capped non-four construction.

The exact common colouring proves the opposite before any 487-point expansion:
every candidate triangle is nonmonochromatic at once.  Thus no choice of one,
two, or three triangles from this family activates the input obstruction.  The
operation is retired without testing other connectors, weaker contact rules,
interior contacts, rotations of a completed support, extra copies, or reduced
gadgets.

## Complete geometric enumeration

The Golomb coordinates are the ten rows

```text
(0,0,0,0), (36,0,0,0), (18,0,18,0), (-18,0,18,0),
(-36,0,0,0), (-18,0,-18,0), (18,0,-18,0), (6,0,0,2),
(-3,-3,3,-1), (-3,3,-3,-1),
```

where `(a,b,c,d)` represents

```text
x = (a+b*sqrt(33))/36,
y = c*sqrt(3)/36 + d*sqrt(11)/12.
```

For each of the 45 unordered Golomb pairs, the verifier enumerates the common
unit-circle points.  There are 42 secant pairs and three tangent pairs; none
are disjoint.  This gives 87 labelled possible choices for `a`.  For each `a`
and each Golomb vertex `g`, intersect the radius-`sqrt(7)` circle about `a`
with the unit circle about `g`.  All 870 cases are decided exactly: 198 are
secant and 672 are disjoint, with no tangent case.  Each secant gives two
choices for `b`, and each segment `ab` has two equilateral completions.  Hence
the complete labelled census contains 792 triangles and 2,386 point
occurrences including `G`.

Completeness uses only the elementary fact that two distinct circles have at
most two intersections.  Any qualifying `a` is recovered from a pair of its
Golomb neighbours; any qualifying `b` is recovered from one of its Golomb
neighbours; and the two equilateral completions exhaust `c`.

## Conservative exact colouring certificate

All geometry is evaluated in outward dyadic intervals with denominator
`2^128`.  The verifier never infers exact equality from overlapping boxes.
Instead it merges every pair of labelled occurrences whose two coordinate
boxes overlap, then takes transitive closure.  This gives 610 conservative
possible-equality colour groups.  The count 610 is **not** claimed to be the
exact number of physical points.

Every group hull has squared diameter strictly below one.  Between groups,
every pair whose squared-distance interval contains one becomes an edge of a
564-edge conservative supergraph.  The 792 labelled triangles map to 408
conservative group triples.  The stored 610-symbol word is proper on every
supergraph edge and nonmonochromatic on every group triple.  Therefore:

- every exact collision receives one colour;
- no actual unit edge can be omitted from the colour check; and
- every actual candidate terminal triangle is nonmonochromatic.

The constraint graph hash is
`eb2498e207efaa495c645aafaa84ee69c5e024e6b193663b8ef040809f2d2122`.
The verifier also reconstructs the eighteen Golomb edges exactly and excludes
three colours by exhaustive enumeration with a unit triangle fixed to
`0,1,2`.  Thus the universal interface graph contains an exactly
four-chromatic source, although only its positive four-colouring is needed for
the assembly theorem.

## Lifting to complete A159 assemblies

The checker hash-pins the archived A159 coordinates and the four canonical
extension words `001`, `010`, `011`, and `012`.  It reconstructs all 646 A159
unit edges, checks that the terminals form a `sqrt(7)` equilateral triangle,
and directly verifies all four words.  Palette permutations cover every named
nonmonochromatic assignment.

For any covered assembly, restrict the universal interface colouring to the
chosen terminal triangles.  Extend each terminal word independently through
its A159 copy.  Private interiors make those extensions agree wherever copies
meet, and the interface supergraph already handles every additional allowed
unit edge.  Four A159 copies would contribute at least `4*(159-3)=624` private
vertices, so every covered support of order at most 508 has at most three
copies.

The private-interior hypotheses are essential.  This theorem does not cover
contacts or overlaps involving gadget interiors, terminal triangles outside
`F`, triangles whose three vertices have only single Golomb contacts, reduced
A159 gadgets, B214, another connector, or arbitrary plane unit-distance
graphs.

## Reproduction and trust boundary

Python 3.11 or later and the standard library suffice.  From the repository
root run

```bash
python3 -B hadwiger_nelson_golomb_a159_connector_closure/verify.py
python3 -O -B hadwiger_nelson_golomb_a159_connector_closure/verify.py
sha256sum -c hadwiger_nelson_golomb_a159_connector_closure/SHA256SUMS
```

Both Python runs end with

```text
EXACT GOLOMB--A159 CONNECTOR FAMILY FOUR-COLOUR STOP VERIFIED
```

The checker pins the four imported source files by SHA-256 and rejects a
corrupted colour word.  CaDiCaL was used only to discover the positive word;
no solver answer is a theorem premise.  The trust boundary is the written
circle-coverage and assembly argument, the pinned source transcriptions,
outward integer interval arithmetic, exhaustive finite loops, CPython exact
integer/rational semantics, and ordinary hardware.  This is author-side
computer-assisted evidence, not proof-assistant formalization or independent
review.

The A159 positive relation is from the sibling
[`hadwiger_nelson_long_terminal_gluing`](../hadwiger_nelson_long_terminal_gluing/README.md)
package.  The public source for this result is the
[`hadwiger_nelson_golomb_a159_connector_closure`](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_golomb_a159_connector_closure)
directory.  Parts' [509-point, 2,442-edge
graph](https://arxiv.org/abs/2010.12665) remains the unrestricted record, as
also stated in [Haugland's August 2026
revision](https://arxiv.org/html/2608.04542v4).  This restricted connector
closure is not an order improvement or a global Hadwiger--Nelson bound.

## Verified public provenance

The exact source package was verified after publication at commit
`d20ddc954a51f1a6c49315a699f7d692cf1ca8d3`; its remote `verify.py` has
SHA-256
`9dff7a304e3796681481117ffc7fcad4e51f3a5f4eb09043cc6e3c8ae8365f90`.
The accompanying Discovery transaction and its uncommitted status are recorded
in [`DISCOVERY_RECEIPT.json`](DISCOVERY_RECEIPT.json).  CheckTx code zero means
accepted for broadcast, not committed: the ledger remains indexed at height
4,363 while the RPC is frozen at 4,364.
