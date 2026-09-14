# Exact proof

Write `s=sqrt(3)` and let `y` be the positive root of

```text
y^2 = (4-s)/2.
```

All coordinates lie in the degree-four real field `Q(s,y)`.  Define four cap
points

```text
P0 = (0,0)
P1 = ((1+s)/2,y)
P2 = ((1-s)/2,y)
P3 = (1,0).
```

Every consecutive cap difference has squared norm three.  For
`d=Pi+1-Pi`, define

```text
Xi = (Pi+Pi+1)/2 + (-d_y,d_x)/(2s)
Yi = (Pi+Pi+1)/2 - (-d_y,d_x)/(2s).
```

Since `|d|^2=3`, the perpendicular offset has squared norm `1/4`.
Consequently `Xi` and `Yi` are the two common unit neighbours of `Pi` and
`Pi+1`, and `|Xi-Yi|=1`.  Also `|P0-P3|=1`.

The verifier reconstructs all 45 unordered squared distances rather than
trusting these intended incidences.  It finds ten distinct points and exactly
16 unit edges: five in each of the three diamonds and the closing edge
`P0-P3`.

## Chromatic number

Each diamond is a `K4` minus its cap-cap edge.  In a proper three-colouring,
its adjacent base vertices use two colours, so both caps must use the third.
The three diamonds therefore imply

```text
colour(P0)=colour(P1)=colour(P2)=colour(P3),
```

contradicting the unit edge `P0-P3`.  Thus the graph is not three-colourable.
The checked word in `certificate.json` is a proper four-colouring, proving
that its chromatic number is exactly four.

## Complete terminal relation

Take the ordered terminals

```text
(X0,Y0,X1,Y1,X2,Y2)
```

and write `Ei={colour(Xi),colour(Yi)}`.  Each `Ei` is a two-element subset of
the four-colour palette because `XiYi` is an edge.

Necessity is local.  The shared cap `P1` is adjacent to every endpoint of the
first two terminal edges.  It has an available colour exactly when
`E0 union E1` is not the whole four-colour palette, equivalently when
`E0 intersection E1` is nonempty.  The same argument at `P2` gives
`E1 intersection E2` nonempty.

For sufficiency, put `Ci` equal to the two-colour complement of `Ei`.
The two intersection conditions are equivalent to

```text
C0 intersection C1 is nonempty,
C1 intersection C2 is nonempty.
```

Choose the colour of `P1` in the first intersection and the colour of `P2` in
the second.  Choose colours for `P0` in `C0` and `P3` in `C2` that are
different; this is always possible because both complements have size two.
These choices extend the terminal assignment and satisfy the closing edge.
Hence a proper terminal assignment extends if and only if

```text
E0 intersects E1 and E1 intersects E2.
```

There are 12 named colourings of the middle terminal edge.  For each, 10 of
the 12 named colourings of either adjacent edge have intersecting palettes,
so exactly `12*10*10=1200` of the `12^3=1728` named proper terminal
assignments extend.  Equivalently, 528 named assignments are forbidden.  The
exhaustive computation gives 52 extendible and 22 forbidden patterns among
the 74 equality patterns modulo global colour permutation.

This is a local physical relation theorem, not a five-chromatic construction.
It makes no assertion about a host, a record graph, or any source outside this
fixed support.
