# Exact half-scale two-coincidence classification

Let $B=(b_0,\ldots,b_{25})\subset\mathbb R^2$ be the coordinate set in
`model.py`.  Row `[a,b,c,d]` means

\[
 \left((a\sqrt3+b\sqrt{11})/12,(c+d\sqrt{33})/12\right).
\]

Exoo and Ismailescu give this set as a 26-vertex five-chromatic
`{1,2}`-distance graph.  Exact reconstruction finds 75 pairs at distance 1
and 10 pairs at distance 2.  The verifier also exhausts its four-colour
search and checks an explicit five-colouring.  This source fact motivates the
construction, but the family theorem below only needs the displayed points.

## The classified family

For an orthogonal map $R\in O(2)$ and a translation $t\in\mathbb R^2$, put

\[
 C=\tfrac12 R(B)+t.
\]

The family consists of every such placement satisfying
$|B\cap C|\geq2$.  For each placement, $G(B,C)$ is the **strict**
unit-distance graph on $B\cup C$: two distinct points are adjacent exactly
when their Euclidean distance is 1.

**Theorem.** Every graph $G(B,C)$ in this family is four-colourable.  Up to
equality of the moved point set $C$, there are exactly 1,446 placements.
They arise from 3,348 labeled specifications and have the following complete
census.

| vertices | unit edges | placements |
|---:|---:|---:|
| 49 | 83 | 114 |
| 50 | 84 | 1,122 |
| 50 | 85 | 96 |
| 50 | 86 | 90 |
| 50 | 87 | 24 |

In particular, this family contains no five-chromatic unit-distance graph and
does not improve the 509-vertex record.

## Why the enumeration is complete

Suppose $B\cap C$ contains two distinct points.  Choose their distinct
preimage labels $i,j\in B$, and target labels $p,q\in B$.  Since the copy
is scaled by one half,

\[
 \lVert b_i-b_j\rVert^2=4\lVert b_p-b_q\rVert^2. \tag{1}
\]

`enumerate_placements` checks all 325 unordered source pairs and all 325
unordered target pairs using exact arithmetic, retaining precisely those
satisfying (1).  It then checks both target orders and both choices of
orientation.  Given two nonzero ordered segments of the same length and an
orientation choice, there is exactly one Euclidean isometry taking the first
segment to the second.  `make_placement` writes that isometry as an exact
complex multiplication followed by a translation.  Thus every admissible
placement occurs in the 3,348 labeled list.

Several labeled choices can define the same moved set.  The program sorts all
26 exact moved points and uses that tuple as the canonical key.  Exact
deduplication leaves 1,446 keys.  The descriptor and full point-set stream
hashes in `EXPECTED.json` bind both the representatives and the coordinates.

All calculations take place in
$K=\mathbb Q(\sqrt3,\sqrt{11})$, represented in the basis
$(1,\sqrt3,\sqrt{11},\sqrt{33})$.  Squared norms of source-pair differences
lie in $\mathbb Q(\sqrt{33})$, whose inverse is evaluated symbolically.
Python `Fraction` supplies reduced rational coefficients.  There are no
floating-point comparisons or tolerances.

## Why every strict unit edge is included

Every pair of points in $B\cup C$ is represented in at least one of three
origin cases:

1. Both points come from $B$.  The exact source calculation supplies all 75
   unit pairs.
2. Both points come from $C$.  Since $C$ is a half-scale isometric copy,
   its unit pairs correspond exactly to the 10 source pairs at distance 2.
3. One point comes from each copy.  `unit_graph` tests all 676 labeled cross
   pairs by exact squared norm.

The edge set is deduplicated after coincident points are identified.  This is
the complete strict graph, including incidental cross-copy unit distances.
`controls.py` also compares this origin-case construction with the direct
definition on an orientation-preserving and an orientation-reversing member.
`direct_audit.py` performs that definition-level comparison for all 1,446
members, testing 1,765,764 unordered point pairs in total.

## Four-colour certificate

`certificate.json` contains 1,446 rows in canonical placement order.  Each
row assigns a value in `{0,1,2,3}` to every vertex.  Four two-bit entries are
packed into a byte, rows are zero-padded to 52 positions, and the byte stream
is zlib-compressed and base85-encoded.  The raw SHA-256 digest is pinned in
`EXPECTED.json`.

`verify.py` independently reconstructs every exact placement and strict edge
set, decodes the corresponding row, and tests every edge for unequal endpoint
colours.  Positive colouring witnesses require no SAT-solver trust.  The
producer uses deterministic DSATUR backtracking, but the verifier only relies
on the explicit rows.

## Scope

The theorem covers one fixed copy of $B$ and one half-scale copy with at
least two coincident points, with arbitrary rotation or reflection and
translation.  It does not classify one-coincidence placements, disjoint
placements, other scale factors, or unions of three or more copies.
