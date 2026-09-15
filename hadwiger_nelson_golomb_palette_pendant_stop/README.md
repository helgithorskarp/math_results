# Joint relation loss from a universally extendible Golomb attachment

One exact diamond attachment of the reviewed eight-point palette chain to
Golomb's ten-point graph gives **14 distinct points and 24 complete unit
edges**. Its joint 12-terminal relation shrinks from **5,700 to 2,916
canonical patterns**, while both input projections remain full.

The decisive construction result is a **stop**. The complete graph is exactly
Golomb with two triangles attached at single vertices. **Every full Golomb
four-colouring extends in exactly 36 ways.** The graph has chromatic number
four, and this operation supplies no constraint back to its Golomb input.
The joint relation loss does not provide a record candidate, a receiver
obstruction or a finishing construction. The fixed attachment is retired
without alternate diamonds, orientations, copies, hosts or added layers.

## Frozen physical construction

Put `s=sqrt(3)`, `t=sqrt(11)` and `y=sqrt((4-s)/2)`, all positive. In complex
coordinates let Golomb's first seven points be

```text
G0=0, G1=1, G2=(1+i*s)/2, G3=(-1+i*s)/2,
G4=-1, G5=(-1-i*s)/2, G6=(1-i*s)/2.
```

Let `q=(1+i*t)/6` and `w=(-1+i*s)/2`; the remaining points are
`G7=q, G8=w*q, G9=w*w*q`.

For the original three-diamond chain, the four cap positions are

```text
P0=(0,0), P1=((1+s)/2,y), P2=((1-s)/2,y), P3=(1,0).
```

Its terminal edge `Xi Yi` is the pair of common unit neighbours of
`Pi,P(i+1)`. Keep the eight-point graph
`P1,P2,X0,Y0,X1,Y1,X2,Y2`; **P0 and P3 are absent**. Apply the one fixed
isometry `(x,z) -> (z-y+1/2,1/2-x)`. This identifies

```text
P1=G6, P2=G2, X1=G0, Y1=G1,
X0=10, Y0=11, X2=12, Y2=13.
```

There are no further collisions. All 91 physical pairs are evaluated exactly
in the degree-eight real field `Q(s,t,y)`. The Golomb graph contributes 18
edges and the chain 11, with five shared diamond edges and no incidental
edges, giving 24. The only old--new contacts are

```text
G2--12, G2--13, G6--10, G6--11.
```

The new--new edges are `10--11` and `12--13`. This makes the two pendant
triangles explicit. The chain's retained private caps are deliberately shared
and their complete colour options are recomputed; no ten-to-eight-point
substitution theorem is assumed for an enlarged interface or for contacts
with deleted caps.

## Complete joint relation

In Golomb, hide vertices 2 and 6 and mark
`T_G=(0,1,3,4,5,7,8,9)`. In the chain, mark its six original edge endpoints.
The common visible pins are 0 and 1. The union interface, in order, is

```text
T=(0,1,3,4,5,7,8,9,10,11,12,13).
```

The baseline consists of compatible pairs of **projected isolated input
relations**, agreeing at 0 and 1; it does not already identify the hidden
colour choices at the two private caps. On that baseline a joint word extends
exactly when both conditions hold:

```text
|palette(0,1,3,12,13)| <= 3,
|palette(0,1,5,10,11)| <= 3.
```

These are the complete private neighbourhoods. Vertices 2 and 6 are
nonadjacent, so their nonempty available-colour lists can be chosen
independently. Sharing each private cap intersects two lists that were
individually nonempty in the isolated inputs. This accounts for every lost
pattern; there are no unaccounted geometric contacts.

Normalize colours at the unit edge `0--1` to `0,1`. Direct enumeration gives:

| relation/count | edge-pinned named count |
|---|---:|
| Golomb full words | 190 |
| Golomb eight-terminal words | 114 |
| chain six-terminal words | 100 |
| compatible input product | 11,400 |
| full composite terminal relation | 5,832 |
| lost terminal words | 5,568 |
| composite full words | 6,840 |

The selected Golomb eight-terminal projection is itself neutral: every
proper word on its induced terminal graph extends. The chain supplies the
already known palette-intersection relation. Neither this neutrality nor
Golomb's ordinary four-chromaticity is disguised as a new input restriction.

Each joint terminal word uses at least three colours because vertices 7,8,9
form a triangle. The two residual colour permutations act freely, so the
canonical counts are 5,700 before, 2,916 after and 2,784 lost. The unrestricted
labelled counts are 136,800, 69,984 and 66,816. Each private-cap condition
rejects 3,280 edge-pinned words; 992 fail both.

The fixture `011230210201` extends to each isolated input but fails on the
union. A directly checked proper five-word realizes the same terminal
prescription. This is a conditional four-colour failure, not ordinary
five-chromaticity. Both source projections remain full. More strongly, every
one of the 190 pinned full Golomb words has exactly 36 full extensions, as
both the graph decomposition and the exhaustive census show.

## Reproduction and proof boundary

CPython 3.11 or later, standard library only. From this directory:

```sh
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
python3 -B produce.py --compare EXPECTED.json
python3 -B controls.py
sha256sum -c SHA256SUMS
```

The verifier constructs the four added points from direct closed formulas,
uses a nested tower of quadratic extensions, enumerates the isolated inputs
by named-colour assignments, and tries all 16 hidden-cap assignments for
**every** input-product word. It verifies the exact available-list formula,
the full relation counts and hashes, every fibre of the projection onto
Golomb, literal proper four/five words and Golomb's non-three-colourability.

The independent producer constructs and transforms the original chain,
uses flat basis multiplication and a complete full-graph DSATUR enumeration.
Its geometry and all three relation hashes agree with the verifier. No
solver status, floating incidence, omitted table or sibling code is used.
Controls accept the valid package first and then reject three semantic
corruptions. These are author-side checks, not independent peer review.
See [EXPECTED.json](EXPECTED.json), [certificate.json](certificate.json)
and [VALIDATION.json](VALIDATION.json).

For the arithmetic, `Q(s,t)` has basis `1,s,t,st`. The element
`a=(4-s)/2` has norm `13/4` to Q. If a were a square in `Q(s,t)`, either a
or a/11 would be a square in `Q(s)`. Their rational norms, `13/4` and
`13/484`, are not rational squares. Thus adjoining y is genuinely quadratic
and the eight coefficient positions are independent. Exact coefficient
tests therefore decide every collision and unit distance.

For universal extension, each new triangle has one old cap of colour c.
Its two ordered new vertices can take any two distinct colours among the
other three: six choices. The triangles have no further contacts, so all
36 combinations work for every full Golomb word. A proper four-word is
checked; exhaustive three-colour testing of the retained Golomb graph gives
the lower bound four. No negative ordinary four-colour claim is made.

## Attribution and stopping scope

The inputs are prior physical graphs, described in the
[Golomb source package](../hadwiger_nelson_golomb_rotation_sum/README.md) and
[the independent eight-point chain refinement](../hadwiger_nelson_three_diamond_palette_chain_review1/README.md).
This package claims neither a new atom nor priority for intersecting available
colour lists. [PROVENANCE.json](PROVENANCE.json) records the exact source
revisions and verified remote identities.

The loss on an expanded joint interface does not imply that any old input
colouring is eliminated. Here the complete graph proves the contrary by an
elementary extension formula. Neither Parts receiver was selected, and no
receiver pattern was tested or excluded. The result retires this one framed
attachment; it does not exclude other Golomb supports, arbitrary palette
compositions or the Hadwiger--Nelson objective.
