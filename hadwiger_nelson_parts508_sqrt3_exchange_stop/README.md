# Fixed Parts triangle-chord distance exchange stops at four colours

The exact support

```
S = { p / sqrt(3) : p is a Parts509 point other than the origin }
```

has **508 distinct physical points and 1,145 complete unit edges**. The
supplied 508-symbol word is a proper four-colouring. This single operation
fails the sub-509 construction gate; it supplies no new non-four signal or
complete-host forcing relation.

The graph has components of orders **337 and 135**, and **36 isolated
vertices**. There are 853 edges among the original large-side labels and
292 among the small-side labels, with no cross-side edges. Its failure is
therefore also structural: the new distance class does not couple the two
parts of the positive parent.

## Construction and exact scope

The starting strict Parts graph is the published five-chromatic 509-point,
2,442-edge graph. Its [existing certificate](../hadwiger_nelson_parts509_criticality/README.md)
checks ordinary five-chromaticity and every one-vertex deletion. This package
uses the exact coordinate rows already published in
`../hadwiger_nelson_parts509_fold264_438_stop/points.tsv`; despite that input
file's directory name, no fold is applied here. The file hash is pinned in
`manifest.json`, and the checker reconstructs the original 2,442 unit pairs.

There is one fixed scale, `1/sqrt(3)`, and one distinguished omitted point,
the origin (source label 0). The remaining labels retain their source order.
The cap is `509-1=508` before any chromatic computation. The map is injective;
no approximate or nonadjacent collision is used to achieve the count.

The construction tests whether directly activating the square-root-three
long diagonals of the parent's unit diamonds can replace its original
unit-distance constraints. Every pair of original squared distance three
becomes a physical unit pair, including pairs without a retained diamond
witness. This is an exact distance-class exchange, not a graph-theoretic
assumption that diamond diagonals already force different colours.

The full parent has 1,175 square-root-three pairs, 30 incident with the
omitted origin. Hence the complete new graph has 1,145 edges. All original
unit distances become `1/sqrt(3)`, so **none of the original unit-edge
constraints survives as a physical edge**. The parent's non-four proof does
not transfer automatically. The ordinary four-word ends the test before
any scale, omitted-point or repair variation.

This result covers only this fixed support and its subgraphs. It is not a
classification of other distance graphs on the parent, arbitrary scales,
other deletions, deformations or plane unit-distance constructions. It does
not strengthen the unrestricted record or prove an exact chromatic lower
bound for the new graph.

## Reproduction

From this directory in a full checkout of the repository:

```sh
python3 verify.py
python3 verify.py --emit /tmp/parts-sqrt3-exchange
```

CPython 3.11 or later and the standard library suffice. The optional argument
writes regenerated geometry outside the repository. No solver, scratch file,
large certificate or floating-point decision is needed to check the result.

Coordinates use the radical basis

```
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

Source coordinates have denominator 96. Multiplying their integer coefficient
vectors by `sqrt(3)` and using denominator 288 exactly implements division
by `sqrt(3)`. The checker expands radical products using
`sqrt(a)*sqrt(b)=gcd(a,b)*sqrt(a*b/gcd(a,b)^2)` with arbitrary-precision integers.
Linear independence of this multiquadratic basis makes coefficient equality
an exact distance predicate. It scans all 129,286 source pairs and 128,778
physical pairs, collision-checks coordinates and compares the complete new
edge stream against the scaled square-root-three source stream. It checks
the literal four-word, the connected components and the absence of cross
contacts. A constant colour-word corruption is rejected, and a separate
one-point distance control verifies the scale.

The producer used subset-mask radical multiplication, wrote the ordinary
four-colour CNF and obtained SAT from CaDiCaL 1.9.5. Its word was checked
directly; geometry and that one SAT decision took about 2.85 seconds. The
public checker uses all ordered radical products through a gcd table and
imports no solver. Its complete coordinate, edge and component streams agree
entry-for-entry with the producer. Normal and optimized execution agree.
These are author-side checks, not independent review. SAT-side proof output
is retained privately and is not a non-four certificate.

## Research boundary

The operation neither preserves the positive parent's obstruction nor
creates a coupled substitute. It is retired without nearby scale, deletion,
shape or repair sweeps. Both reviewed Parts receivers remain banked; no new
receiver, component transplant or teammate-source search was performed.
This failure, following the earlier capped operations, supports reassessing
direct Parts-parent surgery before selecting another operation. It does not
rule out an independently justified future mechanism.

The supported unrestricted record remains
[Parts's 509-point/2,442-edge construction](https://arxiv.org/abs/2010.12665),
also identified as current by [Haugland v4](https://arxiv.org/html/2608.04542v4).
Haugland's 2,131-point construction concerns the restricted spindle-free
problem. Neither that result nor this four-colour stopping example changes
the unrestricted vertex frontier.
