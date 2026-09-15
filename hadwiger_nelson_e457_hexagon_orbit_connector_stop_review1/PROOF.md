# Proof audit

## At most two orbit-to-orbit unit contacts

Put the terminals at `O=(0,0)` and `V=(8/3,0)`. If `X` is on the left unit
circle, `Y` is on the right unit circle, and `XY` is a unit edge, then

```text
V-O = (X-O) + (Y-X) + (V-Y)
```

is a sum of three unit vectors. Their horizontal components sum to `8/3`,
and each is at most one, so every component is at least `8/3-2=2/3`.

In a regular six-point orbit, qualifying directions lie in the arc
`cos(theta)>=2/3`. Its width is `2 arccos(2/3)<120 degrees`, since
`2/3>cos(60 degrees)`. Hence each orbit contributes at most two candidate
directions, and if there are two they are adjacent. Every cross edge is
therefore contained in one `K2,2` whose two vertices on each side are joined
by a rim edge.

Suppose three cross edges exist. Relabel the adjacent pairs so the missing
edge is `L1 R1`. Normalize `L0=0`, `L1=1` and take the left centre to be
`omega=(1+i sqrt(3))/2`; reflection covers the other choice. The point `R0`
is a unit neighbour of both `L0,L1`. The other possible neighbour is the left
centre, but the two radius-one carrier circles are disjoint because their
centres are `8/3>2` apart. Thus `R0=conjugate(omega)`.

Next `R1` is the nondegenerate common unit neighbour of `L0,R0`, so
`R1=-omega`; the other choice is the already used `L1`. Finally the right
centre is the nondegenerate common unit neighbour of `R0,R1`, namely
`-i sqrt(3)`; the other choice is `L0`. Its squared distance from the left
centre is exactly seven, contradicting `64/9`. The review constructs both
reflected chains by the exact equilateral common-neighbour formula. All four
labelled `K2,2` three-edge subsets reduce to this case by independent swaps
of the adjacent pairs. Four cross edges contain such a triple. Therefore the
maximum is two.

The disjoint-circle observation is the needed nondegeneracy condition: without
it the repeated common-neighbour construction also contains points belonging
to the opposite rim.

## Complete abstract colouring relation

There are `1+36+binom(36,2)=667` labelled choices of at most two cross edges
between two labelled six-cycles. The review checks all of them. Its positive
witness bank consists of the four binary phase choices for the two rims and
the words obtained by recolouring at most one vertex with colour two, giving
52 words before case filtering.

Every one of the 667 cases has a proper bank word. Independently, graph
bipartiteness gives 343 bipartite cases and 324 nonbipartite cases. The latter
use a third-colour witness and are therefore exactly three-chromatic. Adding
the two centres and assigning both a fresh fourth colour proves that the
isolated support never forces the terminals different.

## Frozen exact realization

The independent nested-quadratic reconstruction tests all 91 point pairs. It
finds 14 distinct points and 26 unit edges: twelve spokes, twelve rim edges,
and the two contacts `L0 Q0`, `L0 Q5`. Thirteen triangles give a lower bound
of three; the target's three-colour word gives the upper bound. The target's
equal-terminal four-word is also checked directly.

After the quarter-turn the left seed becomes
`(-sqrt(47)/24,23/24)`. If
`sqrt(47)=a sqrt(3)+b sqrt(11)` with rational `a,b`, squaring forces `ab=0`
by independence of `1,sqrt(33)`. The remaining alternatives require either
`a^2=47/3` or `b^2=47/11`, neither a rational square. Thus the point is
outside the reviewed E457 support.

## Complete frozen E457 unions

An ordered pair of distinct plane points has exactly two isometric embeddings
onto another ordered pair, one orientation preserving and one reversing.
`union_check.py` builds both. E457 coordinates are embedded in
`Q(sqrt(3),sqrt(11),sqrt(47))`; the connector is independently rebuilt in the
same ambient field. Exact coordinate equality gives only the two terminal
overlaps. Recomputing every distance gives 2,355 unit edges, exactly the sum
of E457's 2,329 and the connector's 26: there are no incidental contacts.

The pinned E457 word gives both terminals colour three. The connector word
does likewise, and all six permutations of its other three colours remain
proper on the merged complete graph. Hence both frozen 469-point unions are
four-colourable.
