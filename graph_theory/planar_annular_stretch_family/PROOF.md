# Capped cylinders with stretched or deleted vertical edges

All shortest paths below are taken in the original graph with its specified
edge lengths. Paths may overlap; a single vertex is an allowed path. A
separator is half-balanced when each component after its deletion has mass
at most half the total original vertex mass.

## Graph and statement

For even `m >= 6` and `h >= 2`, let `G(m,h)` have caps `0,1` and vertices

```
v(i,j) = 2 + h*i + j,     0 <= i < m,  0 <= j < h.
```

Column indices are modulo `m`. Its edges are:

- `0--v(i,0)` and `1--v(i,h-1)`;
- `v(i,j)--v(i+1,j)` for every row;
- `v(i,j)--v(i,j+1)` for `j < h-1` (the vertical edges);
- `v(i,j)--v(i+1,j+1)` when `i+j` is even, and
  `v(i+1,j)--v(i,j+1)` when `i+j` is odd, for `j < h-1`.

This is a finite simple planar graph: draw nested cyclic rows on an annulus,
one diagonal inside each quadrilateral, and put a cap in each complementary
disk. Deleting vertical edges preserves planarity.

**Theorem.** Suppose `m` is 6 or 8. Give every vertex an arbitrary
nonnegative real mass. A half-balanced separator consisting of at most two
ambient geodesics exists in either regime:

**A.** Every nonvertical edge has length 1. Each vertical edge independently
is deleted or has an arbitrary real length at least 1.

**B.** All vertical edges are present and have one common real length `t>0`.
Every nonvertical edge has length 1.

Only regime A requires a finite boundary lemma. We prove it explicitly next.

## An anchored two-row lemma

Let `K_m=G(m,2)` with every edge of length 1, for `m=6,8`. Write

```
A_m = {0} union {2+2*i : 0 <= i < m}.
```

The cap `1` will be a proxy for distant vertices. Assume `A_m` carries at
least half of the total mass. Then one of the following three separators is
half-balanced. Each separator is a union of at most two ambient geodesics;
none of the paths uses cap `1` or a vertical edge.

For `m=6`:

| Separator | Paths (vertex order) | Components after deletion |
|---|---|---|
| `S0` | `(8,0,4)` | `{1,2,3,5,6,7,9,10,11,12,13}` |
| `S1` | `(12,2,5,7)`, `(12,10,9,7)` | `{0,4,6,8}`; `{1,3,11,13}` |
| `S2` | `(10,0,6,5)`, `(8,0,2)` | `{1,3,7,9,11,12,13}`; `{4}` |

For `m=8`:

| Separator | Paths (vertex order) | Components after deletion |
|---|---|---|
| `S0` | `(16,2,4)` | `{0,1,3,5,6,7,8,9,10,11,12,13,14,15,17}` |
| `S1` | `(17,2,4,6)`, `(17,14,0,8)` | `{1,3,5,7,9,10,11,12,13,15}`; `{16}` |
| `S2` | `(16,2,5,7)`, `(14,12,10,9)` | `{0,4,6,8}`; `{1,3,11,13,15,17}` |

**Geodesic and component audit.** Every consecutive pair in the table is an
edge from the rule above, and no listed edge is vertical. For endpoints
`v(i,j),v(k,l)` in a unit `G(m,h)`, put

```
delta = min((i-k) mod m, (k-i) mod m),
L = min(max(abs(j-l), delta), j+l+2, 2*h-j-l).
```

A path avoiding both caps has length at least `max(abs(j-l),delta)` since
each edge changes each coordinate by at most 1. A path visiting cap `0`
has length at least `j+l+2`, and one visiting cap `1` has length at least
`2*h-j-l`, by the level function taking values `0,j+1,h+1` on cap `0`, row
`j`, and cap `1`, respectively. These categories cover every path, so `L`
is a lower bound on distance. Each displayed path has length exactly `L`
with `h=2`: the first path in each table has length 2; the other paths have
length 3 except `(8,0,2)`, which has length 2. Thus they are ambient
geodesics. Directly applying the edge rule gives the listed components.
The accompanying checker independently verifies both claims.

**Balance proof.** Call a component heavy if its mass is strictly more
than half the total. Two heavy sets must intersect. A heavy set must also
intersect `A_m`, whose mass is at least half. Suppose all three separators
fail, and let `C0` be the sole residual component for `S0`; it is heavy.

For `m=6`, the component `{1,3,11,13}` of `S1` is disjoint from `A_6`.
Consequently `{0,4,6,8}` must be heavy. At `S2`, the large component is
disjoint from this forced heavy set, while `{4}` is disjoint from `C0`.
Neither can be heavy, a contradiction.

For `m=8`, the component `{16}` of `S1` is disjoint from `C0`, forcing
`C1={1,3,5,7,9,10,11,12,13,15}` to be heavy. At `S2`, `{0,4,6,8}` is
disjoint from `C1`, while `{1,3,11,13,15,17}` is disjoint from `A_8`.
Again neither can be heavy. This proves the lemma, including equality in
the anchor's half-mass assumption.

## Proof of regime A

Let the total mass be `W`. If `W=0`, the empty separator works. If either
cap has mass at least `W/2`, deleting that cap works. Hence assume both cap
masses are strictly less than `W/2`.

Choose the smallest row `j` such that cap `0` together with rows `0,...,j`
carries at least `W/2`. This row exists since cap `1` has less than half the
mass. The mass strictly above row `j` is less than `W/2`, and the mass
strictly below it is at most `W/2`, with the appropriate cap included.

If `1 <= j <= h-2`, split the row cycle into its two half-arcs. Each has
length `m/2 <= 4`. A path between their antipodal endpoints avoiding caps
requires at least `m/2` steps in the cyclic column coordinate. Every edge
costs at least 1. A path visiting cap `0` costs at least `2*(j+1) >= 4`,
and one visiting cap `1` costs at least `2*(h-j) >= 4`, by the same level
bound. Therefore both half-arcs are ambient geodesics. Deleting their union
deletes the row; no edge skips a row, so all residual components lie above
or below it and are half-balanced.

Suppose instead `j=0`. Define a map `phi` to `K_m` that keeps cap `0` and
rows `0,1` with their matching column labels, and sends all other vertices
(including cap `1`) to the proxy cap `1`. Every original edge maps either
to a kernel edge or to one vertex. The length of a noncollapsed kernel
edge is 1, no greater than that of the original edge. Thus

```
d_K(phi(x), phi(y)) <= d_G(x,y).
```

Put on each kernel vertex the sum of masses in its inverse image. The
anchor `A_m` has at least half the mass. Choose a balanced separator from
the boundary lemma. Its paths avoid the proxy and all vertical edges.
Each such path therefore lifts, vertex for vertex, to an existing unit-edge
path in `G`, with exactly the same length. The displayed distance inequality
proves that its lift is ambient shortest.

Every deleted kernel vertex has a singleton inverse image. A component
remaining in `G` maps to a connected set in the kernel after the certified
separator is deleted, hence lies over a single residual kernel component.
Its mass cannot exceed that component's aggregated mass, which is at most
`W/2`. This proves balance. This argument also applies when `h=2`; then
the map is simply the identity on the vertex labels, and any removed
vertical edges only improve its distance inequality.

Finally, if `j=h-1`, cap `1` together with its boundary row has more than
half the mass. Reverse the cylinder, interchanging caps and sending

```
(i,j) -> ((i+s) mod m, h-1-j),
s = 0 if h is odd, and 1 if h is even.
```

This preserves the alternating diagonal rule. A square with indices `(i,j)`
maps to one with indices `(i+s,h-2-j)`, whose index sum has opposite parity
because `s+h` is odd; reduction modulo even `m` preserves that parity.
Reversing the rows also reverses its diagonal orientation. The map thus
preserves each edge class, while permuting the
arbitrary vertical lengths and deletions. The preceding boundary argument
therefore applies from the other end. These cases exhaust regime A.

## Proof of regime B

For `t>=1`, use regime A. For `0<t<=1`, define a potential by

```
f(0)=0,  f(v(i,j))=1+j*t,  f(1)=2+(h-1)*t.
```

Every edge has length at least its absolute potential change: this is
equality on cap and vertical edges, and follows from `t<=1` on diagonals.
Every full vertical meridian from cap `0` to cap `1` attains the potential
difference and is consequently an ambient geodesic.

Let `a_i` be the total mass in column `i`, and `A=sum_i a_i`. If
`2*a_0>=A`, delete the zeroth meridian; all remaining mass is at most
`A/2<=W/2`. Otherwise choose the first `k` in `1,...,m-1` with
`2*(a_0+...+a_k)>=A`, and delete meridians `0,k`. Every remaining
component is contained in one of the two open angular sectors: edges
change columns only by one, and both caps have been deleted. The first
sector has mass less than `A/2` by the minimality of `k`; the second has
mass at most `A/2`. Both are at most `W/2`. This proves regime B.

## A precise limit of the boundary reduction

For any even `m>=10`, the same two-row kernel with proxy cap `1` cannot
satisfy the anchored lemma if both geodesics must avoid that proxy, even
if vertical edges are permitted on those paths.

Indeed, in the unit graph `G(m,2)` any two vertices are at distance at
most 3. Two grid vertices in the same row connect through their adjacent
cap in two steps; for opposite rows one can use the first row's cap and
one vertical edge in three steps. Distances involving caps also have this
bound. Thus two ambient geodesics together contain at most eight vertices.

Assign mass 1 to every first-row vertex, mass `m` to the proxy cap `1`,
and zero elsewhere. The total is `2m`, with exactly half in the anchor.
If the proxy survives, deleting at most eight vertices leaves at least
one of the `m` disjoint column pairs `{v(i,0),v(i,1)}` intact. That pair
connects its positive-mass first-row vertex to the proxy, whose component
then has mass at least `m+1`, exceeding half.

This is not a counterexample to the original separator question: deleting
the proxy alone is a half-balanced geodesic separator of this finite graph.
It is forbidden only in the lifting argument, because an aggregated proxy
has no single vertex to which it can lift. Larger circumferences therefore
require a different or deeper boundary reduction, or another construction
argument.
