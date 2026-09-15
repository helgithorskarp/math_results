# Proof and finite completion

## Exact coordinates and independence

Put `s=sqrt3`, `t=sqrt11`, `h=(4-s)/2`, and `y=sqrt(h)`, taking all roots
positive. Coordinates are rational combinations of

```text
1, s, t, st, y, sy, ty, sty.
```

This is a basis of a degree-eight real field. First, 11 is not a square in
`Q(s)`: squaring `a+bs` and comparing coefficients forces `ab=0`, then would
require either 11 or 11/3 to be a rational square. Thus `Q(s,t)` has degree
four. The norm of `h` from `Q(s)` to `Q` is `13/4`; the norm of `h/11` is
`13/484`. Neither is a rational square. Consequently neither `h` nor `h/11`
is a square in `Q(s)`. If `(a+bt)^2=h` in `Q(s,t)`, with `a,b in Q(s)`, its
`t` coefficient forces `ab=0`, contradicting one of those two nonsquareness
facts. Adjoining `y` therefore doubles the degree again.

Coefficient equality in the displayed basis is exact equality of real
coordinates and squared distances. The producer merges coincident coordinates; the
checker independently verifies distinctness. Both reconstruct every pair. For the frozen formula there are no collisions,
and precisely the 34 edges in `certificate.json`. The checker separately
inverts the palette isometry and verifies its ordered common-neighbour
formulas; it does not trust the generator's point table.

The palette construction uses auxiliary centres P0 and P3 to define its six
terminal points. Those centres are not physical vertices in this union.
The actual palette graph has only its retained caps P1,P2 and six terminals.

## Exact elimination criterion for the whole relation

Let `m=(A,B,C,D)` be the four Moser terminal colours, in order 7--10. Define
`S(m)` to be the set of ordered quadruples of colours at Moser vertices
`(0,1,2,3)` appearing in proper four-colourings of the eleven-point source
with terminal word m. The verifier enumerates every such colouring by assigning
all 11 vertices in fixed order, trying each of the four colours and pruning
only an already violated edge. It obtains exactly 6,144 named full words.
Thus the generated sets `S(m)` are complete, not a selected colouring library.

For palette word `p=(x0,y0,x1,y1,x2,y2)`, define

```text
D1 = {0,1,2,3} minus {x0,y0,x1,y1},
D2 = {0,1,2,3} minus {x1,y1,x2,y2}.
```

All three ordered edges must use distinct colours. P1 and P2 are nonadjacent
and have exactly these respective available colour sets in their isolated
source. The four new contacts show that `(m,p)` extends to the complete
physical graph if and only if some `(q0,q1,q2,q3) in S(m)` satisfies

```text
q1 != y1,
q2 != x1,
D1 minus {q0} is nonempty,
D2 minus {q3} is nonempty.
```

Necessity is restriction of any full colouring. For sufficiency choose the
complete Moser word witnessing the selected element of S(m); choose P1 and
P2 independently from the last two nonempty sets; then keep the six prescribed
palette colours. The complete edge reconstruction proves that every edge
has been checked by these conditions. There are no other inter-component
contacts or shared variables.

Without the four contacts the last two sets are simply D1,D2, and the first
two inequalities disappear. Complete enumeration gives the Moser relation
`A!=B or C!=D` on 240 named words and the palette relation on 1,200 named
words. Their product has 288,000 named assignments. Testing the criterion
above on every product member admits 278,496 and rejects 9,504. Quotienting
only by simultaneous global colour permutation gives 12,024 baseline and
11,624 full patterns. The individual projections are still all 13 and 52
canonical source patterns.

The producer uses a different finite decision: it enumerates all 43,947
canonical four-colour patterns on ten pins and solves the full 19-vertex
edge constraints with those pins, using unrestricted interior recolouring.
The resulting baseline/full two-bit truth stream is identical to that
derived from the named elimination calculation. Its SHA-256 is

```text
01a8223e4d37e78eef445f7db05da107015f6da9e54c2d1ae57e314425bc454a
```

The stream order is lexicographic over canonical strings of length ten,
using at most four colours. Each record is `word:bf` followed by a newline,
where b,f are the baseline and full membership bits. The digest is a compact
comparison, not a substitute for either complete computation.

## Strictness and ordinary chromatic number

The word `(0,0,1,2,2,3,0,2,0,1)` is proper on the bare terminal graph and has
a literal baseline extension. Its full nonextension is proved by the
three-colour diamond equality and forced palette-cap colours given in the
README. It is an unrestricted pinned four-colour impossibility statement.
It is not an ordinary non-four-colourability statement about the graph.

The inherited Moser spindle needs four colours: in a three-colouring each
of its two diamonds forces its cap pair equal, contradicting the edge
between the outer caps. The certificate's proper four-colouring proves the
matching upper bound. Its separate five-colouring, using every colour
0 through 4, is also checked on all 34 edges. Hence the strict graph has
chromatic number exactly four and no ordinary non-four signal.

The relation amplification is caused by actual complete-graph contacts on
an already realized 19-point support. The terminal graph is only three
disjoint edges, so no prior non-four terminal graph is assumed. A further
capped forcing composition remains unconstructed.
