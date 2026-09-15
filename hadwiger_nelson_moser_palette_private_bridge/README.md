# Exact heterogeneous relation amplification through private contacts

One explicitly placed Moser11 source and one eight-point palette-intersection
source form a **19-point, 34-edge strict plane unit-distance graph**. Its four
new cross contacts reduce the complete joint four-colour terminal relation
from **12,024 to 11,624** canonical patterns. This removes **9,504 of 288,000**
named assignments admitted by the isolated sources.

The graph has chromatic number **four**. Both a proper four-colouring and a
proper colouring using all five colours are checked on every physical edge.
This meets the campaign's heterogeneous relation-gain milestone; it is **not**
a five-chromatic graph, a record candidate, or a sub-509 record improvement.
No capped composition closing the remaining relation is supplied.

## Frozen physical interaction

Use the published eleven-point Moser source in its original frame, numbered
0--10 with terminals 7,8,9,10. Let

```text
s = sqrt(3), t = sqrt(11), y = sqrt((4-s)/2),
u = -(s+i)/2.
```

In the palette source's original frame its retained caps are
`P1=((1+s)/2,y)` and `P2=((1-s)/2,y)`. Apply the isometry

```text
g(z) = i + u*(z-P1)
```

to its eight points, numbered in the order
`P1,P2,X0,Y0,X1,Y1,X2,Y2`. They become vertices 11--18.
Thus `g(P1)=M0+i` and `g(P2)=M3+i`. The raw budget is exactly 19;
exact collision checking finds all 19 points distinct.

The constituent graphs have 19 and 11 edges. Reconstructing all 171 distances
gives precisely four further unit edges:

```text
(0,11), (1,16), (2,15), (3,12).
```

The first and last were prescribed in the design. The complete graph also
contains the middle two. Every new edge touches a private Moser vertex;
there are no new edges between the ten marked terminals. Their bare graph
is just the three disjoint palette-source terminal edges.

The eight-point core is defined explicitly here and its private colours are
included in the proof. Contacts to its retained caps are not justified merely
by the old six-terminal substitution theorem. Deleted outer caps `P0,P3`
are not included or used as physical contact points.

## Complete relation and a short witness

Terminal order is

```text
M7,M8,M9,M10, X0,Y0,X1,Y1,X2,Y2
```

The isolated relation is exactly the product of

```text
(M7 != M8) or (M9 != M10)
```

and the two palette-intersection conditions

```text
palette(X0,Y0) intersects palette(X1,Y1),
palette(X1,Y1) intersects palette(X2,Y2).
```

Each palette edge must also be properly coloured. Because the components
have no common vertices, this product is the complete relation of the
inherited-edge subgraph, with arbitrary interior recolouring.

| Complete relation | Canonical patterns | Named assignments |
| --- | ---: | ---: |
| Isolated-source product | 12,024 | 288,000 |
| Complete physical graph | 11,624 | 278,496 |
| Newly excluded | 400 | 9,504 |

Both marginal projections remain their full isolated relations: 13 canonical
Moser patterns and 52 palette patterns. The gain is a joint correlation.
Assignments using fewer than four terminal colours are included.

For a concrete newly forbidden word take

```text
(0,0,1,2, 2,3,0,2,0,1).
```

It has a checked full extension in the inherited-edge graph. In the complete
graph, Moser's first diamond avoids colour 0, hence its caps M0 and M3 must
share a colour. M0 also avoids colour 2, leaving only 1 or 3. The three palette
edges force P1 to colour 1 and P2 to colour 3. The edges M0--P1 and M3--P2
exclude both choices, a contradiction. This already proves strict relation
gain using two of the physical cross edges.

The other two contacts matter to the complete answer: retaining just the two
prescribed contacts permits 285,696 named assignments, whereas the complete
graph permits 278,496. Their omission would overstate the relation.

[PROOF.md](PROOF.md) gives the exact field justification, the complete
elimination criterion, and the distinction between this pinned contradiction
and ordinary non-four-colourability.

## Reproduce

Python 3.11 or later, standard library only:

```sh
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
python3 -B controls.py
python3 -B produce.py --out /tmp/fresh-private-bridge.json
cmp certificate.json /tmp/fresh-private-bridge.json
sha256sum -c SHA256SUMS
```

The producer reconstructs the field in a flat monomial basis and directly
searches the whole graph for each canonical terminal pattern. The checker
imports no producer or sibling code: it uses a quadratic tower for geometry,
enumerates all 6,144 named full Moser colourings, and eliminates the two
palette-cap colours for all 288,000 named baseline assignments. Every distance
and the complete canonical truth stream agree. It also checks the explicit
colourings and the short newly forbidden word.

The trust boundary is exact Python arithmetic, the elementary degree-eight
field argument, complete finite loops, and the written elimination proof.
There is no SAT solver, numerical tolerance, hidden input, omitted proof trace,
or external package. The two implementations and controls are author
verification, not independent peer review or proof-assistant formalization.

## Provenance and construction boundary

The inputs are the reviewed
[Moser four-terminal source](../hadwiger_nelson_moser_four_terminal_relation/README.md)
and the reviewed
[eight-point refinement](../hadwiger_nelson_three_diamond_palette_chain_review1/README.md).
Their exact source pins are in [provenance.json](provenance.json). The present
result is self-contained and re-establishes the source relations needed for
its comparison; it does not review or replace either source theorem.

This single frame was frozen before the relation census. It is a private
contact construction, distinct from the retired Moser/palette point-sum and
the unrealizable homogeneous clause cover. No phase, source, or copy-count
sweep was used. No E457 connector or Parts a=8 route was reopened.

A future construction still needs an exact physical mechanism that removes
the remaining joint patterns within 508 points. The relation count alone
does not justify generic repetition or a larger host. No such continuation
is claimed here. [Parts's primary source](https://arxiv.org/abs/2010.12665) and
[Haugland v4](https://arxiv.org/html/2608.04542v4), refreshed on 2026-09-15,
still identify the unrestricted record as 509 points. This four-chromatic
local interaction does not change it.
