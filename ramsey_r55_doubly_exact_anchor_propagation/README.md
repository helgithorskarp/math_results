# Propagation constraints from a doubly exact `R(5,5;43)` anchor

This directory strengthens the companion 21-by-21 cross-matrix normal form.
In the hard branch of the local-deficiency dichotomy, fixing one doubly exact
vertex does not merely fix two `(4,5;21,100)` cores.  The cross matrix also
determines the order and edge count of both color-neighborhoods at every one
of the other 42 vertices.  All 84 of those local graphs must have deficiency
at least seven.  A linear degree-weight test already forces at least 29 of the
42 vertices to have degree 21.  In fact, if the red cross-edge count is `M`,
at least `241-M` of them must reproduce the full doubly exact signature of the
chosen anchor: between 27 and 21 secondary anchors as `M` runs from 214 to
220.  These exact anchors form connected red and blue backbones at `M=214`
and `M=215`.  At `M=216` the red backbone remains connected, while every
possible blue disconnection is reduced to two 13-vertex Ramsey-critical
components at the abstract induced-subgraph level, and global edge accounting
then excludes that exception.  Profile-sensitive excess accounting forces
both colors connected in 348 of the 349 possible degree-count profiles across
all `M=214,...,220`.  Complete order-9 through order-13 `(3,5)` catalogs,
combined with a local `K_4`-cover inequality and its equality case, eliminate
all order-23 disconnections.  The sole remaining abstract escape is the
`M=220` profile with degree multiset `20^1 21^42`, and it can disconnect only
on exactly 22 anchors.  At that order the cover inequality removes the
`9+13` component partition; independent-row capacity and row-completion
constraints eliminate every remaining two-component partition.  Thus any
disconnection is a blue singleton, which forces a nested pair of exact
`(4,5;21,100)` cores.  Deleting that singleton would produce a 42-vertex
Ramsey graph with degree multiset `20^22 21^20`; none of the 656 orientations
of the published known Ramsey-42 catalog has that multiset, and the complete
radius-four transition classification plus a target-specific radius-five
enumeration force its catalog edge distance to be at least six.

This is a necessary pruning theorem for the hard construction branch.  It is
not a 43-vertex Ramsey graph, an enumeration of the local cores, or a solver
feasibility result.

## Setting

Let `G` be a red graph on 43 vertices with no clique or independent set of
size five.  Assume the hard branch: every red or blue color-neighborhood has
deficiency at least seven relative to the exact `(4,5)` extremal edge counts.
Choose one of the doubly exact vertices `v` forced in that branch, and put

```text
A = N_G(v),                  |A|=21,
B = N_complement(G)(v),      |B|=21,
H = G[A],
K = complement(G)[B].
```

Both `H` and `K` are `(4,5;21,100)` graphs.  For `a in A`, `b in B`, let

```text
x_ab = 1 iff ab is red.
```

The prior normal form gives all mixed-`K_5` clauses, 214--220 red cross
edges, and the first-degree row and column bounds.  The formulas below expose
the previously unused second-neighborhood information.

Write `e_L(S)` for the number of edges of graph `L` induced by `S`, and write
`x(S,T)` and `bar_x(S,T)` for the numbers of red and blue cross edges between
`S subseteq A` and `T subseteq B`.

## Exact row formulas

Fix `a in A`.  Define

```text
P_a = N_H(a),                         h_a = |P_a|,
Pbar_a = A minus ({a} union P_a),
R_a = {b in B : x_ab=1},              r_a = |R_a|,
Rbar_a = B minus R_a.
```

Let `d_a` be the red degree of `a`.  Let `t_R(a)` be the number of red edges
inside its red neighborhood, and `t_B(a)` the number of blue edges inside its
blue neighborhood.  Directly partitioning those two neighborhoods gives

```text
d_a = 1 + h_a + r_a,

t_R(a) = h_a
           + e_H(P_a)
           + e_complement(K)(R_a)
           + x(P_a,R_a),                                      (A_R)

t_B(a) = e_complement(H)(Pbar_a)
           + e_K(Rbar_a)
           + bar_x(Pbar_a,Rbar_a).                             (A_B)
```

The first term `h_a` in `(A_R)` counts the red edges from `v` to `P_a`.
There is no corresponding anchor term in `(A_B)`, because `v` is a red
neighbor of `a`.

## Exact column formulas

Fix `b in B`.  Define

```text
Q_b = N_K(b),                         k_b = |Q_b|,
Qbar_b = B minus ({b} union Q_b),
C_b = {a in A : x_ab=1},              c_b = |C_b|,
Cbar_b = A minus C_b.
```

Since red edges inside `B` are the nonedges of `K`, the analogous partition
gives

```text
d_b = 20 - k_b + c_b,

t_R(b) = e_complement(K)(Qbar_b)
           + e_H(C_b)
           + x(C_b,Qbar_b),                                    (B_R)

t_B(b) = k_b
           + e_K(Q_b)
           + e_complement(H)(Cbar_b)
           + bar_x(Cbar_b,Q_b).                                (B_B)
```

Here the term `k_b` counts the blue edges from `v` to `Q_b`.

## Linear degree propagation

Let `M=sum_(a,b) x_ab`, so `214 <= M <= 220`.  Summing the displayed degree
formulas and using

```text
sum_a h_a = 2|E(H)| = 200,
sum_b k_b = 2|E(K)| = 200
```

gives the two exact deviation identities

```text
sum_(a in A) (d_a-21) = M-220,
sum_(b in B) (d_b-21) = M-221.                         (S)
```

Thus the total deviations on the `A` and `B` sides lie in `[-6,0]` and
`[-7,-1]`, respectively.  These equations couple the row and column degree
patterns more sharply than treating their intervals independently.

Define the symmetric degree weight

```text
w(18)=w(24)=21,  w(19)=w(23)=12,
w(20)=w(22)=3,   w(21)=0.
```

The hard-branch deficiency identity from the companion theorem gives

```text
W = sum_(u in A union B) w(d_u)
    in {3,9,15,21,27,33,39}.                            (W39)
```

The omitted anchor `v` has degree 21 and weight zero, so this is exactly the
global weight.  Every non-21 degree costs at least three; consequently at
most 13 of the 42 secondary vertices have noncentral degree, and

```text
at least 29 vertices in A union B have degree 21.        (P29)
```

There is also an `M`-dependent lower bound on the weight.  Pointwise,
`w(d) >= 3|d-21|`; summing and applying `(S)` gives

```text
W >= 3 sum_u |d_u-21|
  >= 3 |sum_u (d_u-21)|
   = 3(441-2M).                                          (WM)
```

Conditions `(S)`, `(W39)`, and `(P29)` use only row and column sums.  They can
therefore reject a cross matrix before the quadratic local counts below are
computed.

Enumerating the nonnegative degree-count vectors on the two labeled sides,
subject only to 21 vertices per side, `(S)`, and `(W39)`, leaves the following
exact numbers of ordered `(A,B)` profile pairs:

```text
M       W=3  W=9  W=15  W=21  W=27  W=33  W=39   total
214       0    0     0     0     0     0     1       1
215       0    0     0     0     0     1     4       5
216       0    0     0     0     1     4    12      17
217       0    0     0     1     4    11    24      40
218       0    0     1     4     9    19    36      69
219       0    1     3     6    13    25    47      95
220       1    2     4     9    17    32    57     122
total     1    3     8    20    44    92   181     349
```

Here a side profile is the seven-tuple of counts of degrees 18 through 24;
vertices within a side are not assigned or labeled.  This is an exact
integer-profile superset, not a claim that any of the 349 pairs is graphical
or compatible with a chosen core.  At the lowest cross total the superset is
a singleton:

```text
M=214:
(x_18,...,x_24 on A) = (0,0,6,15,0,0,0),
(x_18,...,x_24 on B) = (0,0,7,14,0,0,0).
```

Thus a search at `M=214` has no degree-count branching at all; the other six
cross totals together have only 348 possible ordered side-count pairs before
core-specific row and column feasibility is imposed.

### Color-excess and triangle-pair sieve

The hard-branch profiles also give a small color-specific divisibility sieve.
For a global degree-count vector `x_d`, define the baseline local-edge sums

```text
B_R = sum_d x_d (U(d)-7),
B_B = sum_d x_d (U(42-d)-7).
```

For profile weight `W`, let `E=(43-W)/2` be the total excess over deficiency
seven, and split it as `E_R+E_B=E` between the colors.  Triangle incidence
requires

```text
B_R-E_R = 3T_R,
B_B-E_B = 3T_B.                                      (Triangle-divisibility)
```

Enumerating the 349 side profiles and the finitely many nonnegative excess
splits leaves only the following possibilities:

```text
M    number of (T_R,T_B)  range of T_R  range of T_B  exact R sides  exact B sides
214           1             1403          1463             43             41
215           3           1406--1407    1458--1459          38             40
216           8           1410--1412    1452--1455          36             36
217          15           1414--1417    1446--1451          34             32
218          20           1417--1422    1441--1446          29             31
219          27           1421--1427    1435--1442          27             27
220          39           1425--1432    1429--1437          25             23
total        113
```

The last two columns are universal lower bounds.  If the total red excess is
`E_R`, at most `E_R` of the 43 red local sides can have deficiency greater
than seven, and similarly in blue.  Maximizing the permitted color excess
over the profile sieve gives the displayed numbers.

The 113 canonical lines `M T_R T_B`, ordered lexicographically and terminated
by newlines, have SHA-256

```text
ccaf9ccec34aa4633cf2019d3f85f34e714c1f0bb17db444e9f8034c650c936c.
```

This is an exact arithmetic superset.  It provides a compact validation gate
for a candidate coloring, but it does not assert that any listed triangle
pair is realizable.

### Complete red-side exactness at `M=214`

The singleton profile has a further divisibility consequence.  Including the
chosen degree-21 anchor, the global degree counts are

```text
x_20=13,  x_21=30,  and all other x_d=0.
```

Its weight is `W=39`, so `Delta=(1247-39)/2=604`.  There are only two units
of total excess above the hard baseline 602.  Let `E_R` and `E_B` be the sums
of `delta_(u,R)-7` and `delta_(u,B)-7`; then

```text
E_R+E_B=2.
```

Before subtracting these excesses, the red local-edge sum is

```text
13(U(20)-7) + 30(U(21)-7)
    = 13*93 + 30*100 = 4209.
```

The actual red local-edge sum is `4209-E_R=3T_R`, because every red triangle
is counted at its three vertices.  Hence `E_R` is divisible by three.  Since
`0<=E_R<=2`, necessarily

```text
E_R=0,  E_B=2,
T_R=4209/3=1403,
T_B=(13*107+30*100-2)/3=1463.                 (M214)
```

Consequently every red color-neighborhood is exactly seven-deficient: the 13
degree-20 vertices have order-20 red local graphs with 93 edges, and the 30
degree-21 vertices have order-21 red local graphs with 100 edges.  On the blue
side either one local deficiency is nine or two are eight, with every other
blue deficiency seven.  In particular at least 28 of the 30 degree-21
vertices are doubly exact.  This is a necessary branch theorem; it does not
assert that the pinned local graphs exist compatibly.

### Connected exact-anchor backbone at `M=214`

Let `D` be the set of all doubly exact vertices.  The `241-M` theorem gives
at least 27 secondary anchors, while the unique degree profile has only 30
degree-21 vertices.  Therefore

```text
28 <= |D| <= 30.                                         (Backbone-order)
```

The cross total is independent of which `u in D` is selected as anchor:
every such split has 21 incident red edges, 100 red edges in its red core,
110 red edges in its blue-neighbor side, and hence the same
`M=|E(G)|-231=214`.  Apply the side-specific anchor bounds at every `u`.  Its
red-neighbor side contains at least 13 other vertices of `D`, and its
blue-neighbor side contains at least 12.  Thus

```text
minimum degree of G[D]               >= 13,
minimum degree of complement(G)[D]   >= 12.              (Backbone-degree)
```

Both color graphs on `D` are connected.  Indeed, a component of a `K_5`-free
graph with minimum degree 13 has order at least 18: Turan's theorem gives

```text
13s/2 <= ex(s,K_5) <= 3s^2/8.
```

Two such components would require at least 36 vertices.  The blue argument
with minimum degree 12 makes every component have order at least 16, so two
would require at least 32 vertices.  Both contradict `|D|<=30`.

The same argument survives vertex deletions.  If a cut set of size `k` leaves
a component of order `s`, its internal minimum degree is at least `13-k` in
red or `12-k` in blue.  Turan's bound gives the following minimum component
orders:

```text
red:   k=0,1,2,3  ->  s>=18,16,15,14,
blue:  k=0,1      ->  s>=16,15.
```

Two components plus the cut set would require respectively at least
`36,33,32,31` red vertices or `32,31` blue vertices.  Consequently

```text
vertex-connectivity of G[D]              >= 4,
vertex-connectivity of complement(G)[D]  >= 2.          (Backbone-connectivity)
```

Both connected color graphs also have diameter at most five.  A geodesic of
length at least six contains vertices at positions 0, 3, and 6 with pairwise
disjoint closed neighborhoods.  Those neighborhoods would contain at least
`3*(13+1)=42` vertices in red or `3*(12+1)=39` in blue, again exceeding 30.

Consequently every doubly exact anchor can be reached from every other by at
most five red-anchor steps and, independently, by at most five blue-anchor
steps.  A construction or consistency checker can propagate reanchored core
constraints through this connected backbone instead of treating the 28--30
anchors as unrelated splits.

### The `M=215` backbone is also connected in both colors

The next branch retains a weaker but still global reanchoring network.  The
`241-M` theorem and the exact split-profile list give

```text
27 <= |D| <= 33,
minimum degree of G[D]               >= 11,
minimum degree of complement(G)[D]   >= 10.              (M215-backbone)
```

The upper bound is the maximum number of degree-21 vertices among the five
`M=215` split profiles.  Turan's theorem makes every red component have order
at least 15 and every blue component order at least 14.  The exact classical
value `R(5,3)=14` says that a `K_5`-free graph on at least 14 vertices has an
independent triple.  If either color graph on `D` had two components, take an
opposite-color triangle in each; all edges between the components have that
opposite color, producing a forbidden monochromatic clique (indeed a
six-clique).  Thus both color graphs are connected.

After deleting one vertex, a red component still has minimum degree at least
10 and hence order at least 14 by Turan.  The same Ramsey argument rules out
two components, so the red backbone has vertex connectivity at least two.
Finally, disjoint closed-neighborhood packing gives

```text
diameter of G[D]               <= 5,   since 3*(11+1)>33,
diameter of complement(G)[D]   <= 8,   since 4*(10+1)>33.
```

At `M=216` the minimum degrees no longer force every hypothetical component
to reach order 14, so this particular two-component count no longer handles
both colors.  The next argument nevertheless salvages one color sharply.

### Both `M=216` backbones are connected

The profile and propagation bounds at the next cross total are

```text
26 <= |D| <= 36,
minimum degree of G[D]               >= 9,
minimum degree of complement(G)[D]   >= 8.               (M216-backbone)
```

Suppose that the red graph `G[D]` is disconnected.  Every component has at
least ten vertices, since its internal red minimum degree is at least nine.
It is not complete, because it is `K_5`-free, and hence has red independence
number at least two.  Three components would supply a blue six-clique by
taking an independent pair from each.  With two components, their red
independence numbers have sum at most four, or their union supplies a blue
five-clique.  Thus there are exactly two components, each with independence
number two.  The value `R(5,3)=14` bounds both component orders by 13.  Since
`|D|>=26`, both orders are exactly 13 and `|D|=26`.

In either component `C`, let `L=complement(G[C])`.  The graph `L` is
triangle-free because `alpha(G[C])=2`, and it has maximum degree at most
`13-1-9=3`.  Brooks' theorem makes `L` 3-colorable: its only complete-graph
exception is excluded by triangle-freeness, and its odd-cycle exception is
still 3-colorable.  One color class has at least `ceil(13/3)=5` vertices.
That class is independent in `L`, hence a red five-clique in `G[C]`, a
contradiction.  Therefore `G[D]` is connected.  Closed-neighborhood packing
also gives

```text
diameter of G[D] <= 8,   since a length-9 geodesic gives 4*(9+1)>36.
```

The corresponding argument also classifies every possible blue
disconnection.  Each blue component has at least nine vertices and blue
independence number at least two.  Avoiding a red five-clique permits exactly
two components, both with independence number two; `R(5,3)=14` and
`|D|>=26` then force two components of order 13 and `|D|=26`.  In the red
complement `H_i` of either blue component, triangle-freeness and the blue
minimum degree give `Delta(H_i)<=4`.  Also `delta(H_i)>=4`: otherwise a
vertex with at least nine nonneighbors has, by `R(3,4)=9`, four mutually
nonadjacent vertices in its nonneighborhood, and those four together with
the vertex are an independent five-set of `H_i`, hence a blue five-clique.
Thus every exceptional `H_i` is a 4-regular `(3,5;13)` Ramsey graph.

This exceptional shape is attainable under the displayed abstract backbone
bounds.  Let `H` be the circulant graph on `Z/13Z` with differences
`+/-1,+/-5`; direct enumeration verifies that `H` is 4-regular,
triangle-free, and has independence number four.  On two copies of its
vertex set, color all cross edges red and use `H` for the red edges inside
each copy.  The red clique number is `2+2=4`.  The blue graph is two
disconnected copies of `complement(H)`, also with clique number four, and
has minimum blue degree `12-4=8` (while the red minimum degree is 17).
Consequently the `M=216` order and degree bounds alone cannot force the blue
backbone to be connected.  This 26-vertex auxiliary coloring is not asserted
to extend to a full 43-vertex candidate—and in fact global edge accounting
now rules out every such extension.

Indeed, the same component argument shows that a disconnected color on any
`D` of order 26 has two order-13 components of independence number two.  In
the opposite color, all `13*13=169` cross-component edges are present.  The
opposite-color graph inside each component is triangle-free with independence
number at most four; `R(3,4)=9` gives minimum degree at least four, hence at
least 26 edges.  Thus the opposite color has at least

```text
169+26+26=221
```

edges inside `D`.  If its global edge count is `T`, balanced degree 21 on `D`
leaves exactly `T+221-21*26` edges on the 17 outside vertices.  Here every
global color total is at least 445, so this is at least 120, contradicting
`ex(17,K_5)=108`.  Therefore neither color can be disconnected when
`|D|=26`, and both `M=216` backbones are connected.

### A profile-level connectivity sieve through `M=220`

The component argument has a useful profile-sensitive form.  For a split
profile of weight `W`, let `n_21` be the total number of degree-21 vertices,
including the chosen anchor.  There are only

```text
E=(43-W)/2
```

units of deficiency excess.  Every degree-21 vertex outside `D` consumes at
least one such unit, so the profile itself certifies

```text
|D| >= L := n_21-E.                                  (Profile-D)
```

There is an `M`-independent connectivity threshold.  Put `d=|D|`.  Every
vertex of `D` has 21 neighbors of each color in the full graph, while only
`43-d` vertices lie outside `D`.  Consequently both induced color degrees
are at least

```text
21-(43-d)=d-22.                                      (D-internal)
```

If `d>=27`, every component of either color has at least six vertices.  It
cannot be complete because it is `K_5`-free, so it contains an independent
pair in that color.  Avoiding an opposite-color five-clique then forces
exactly two components, each with independence number two and hence, by
`R(5,3)=14`, order at most 13.  This would give `d<=26`, a contradiction.
Thus every profile with `L>=27` forces both backbone colors connected.  The
order-26 edge obstruction above improves this to `L>=26` for every `M`.

There is one further order-25 improvement in the `M=217,218` branches, where
both side-specific backbone minimum degrees are at least four.  A
disconnection then has two independence-two components of orders 12 and 13.
Their opposite-color complements have minimum degrees at least three and
four by `R(3,4)=9`, so the opposite color has at least

```text
12*13 + 12*3/2 + 13*4/2 = 200
```

edges inside `D`.  The least relevant global color total is 448, leaving at
least `448+200-21*25=123` edges on the 18 outside vertices.  This contradicts
`ex(18,K_5)=121`.  Hence `L>=25` also forces both colors connected at
`M=217,218`.

### The last `M=218` escape is also connected

There is only one `M=218` profile not covered above:

```text
W=15, L=24,
A counts in degrees 18,...,24 = (0,0,2,19,0,0,0),
B counts in degrees 18,...,24 = (0,0,3,18,0,0,0).
```

Including the anchor, its global degree multiset is `20^5,21^38`.  Its 14
units of local-side excess have possible color splits and triangle counts

```text
(E_R,E_B,T_R,T_B) =
(2,12,1421,1441), (5,9,1420,1442), (8,6,1419,1443),
(11,3,1418,1444), (14,0,1417,1445).
```

If either backbone color were disconnected, the lower bound `L=24` and the
preceding `d=25` obstruction would force `|D|=24`.  Thus there is zero slack:
the 14 nonexact degree-21 vertices consume exactly one excess unit each, and
all five degree-20 vertices have both local sides exactly seven-deficient.

The side-specific backbone degree bounds at `M=218` are five in red and four
in blue.  A disconnected color therefore has exactly two components, each
with independence number two.  Each component has order at most 13 by
`R(5,3)=14`, so their orders are `11+13` or `12+12`.  Inside these components,
the opposite color consists of `(3,5)` Ramsey graphs.  The complete small
catalogs have exact minimum edge counts

```text
e(3,5,11)=15,  e(3,5,12)=20,  e(3,5,13)=26.
```

Both component partitions consequently put at least

```text
11*13+15+26 = 184,  or  12*12+20+20 = 184
```

opposite-color edges inside `D`.

Suppose first that red is disconnected.  The blue graph has 454 edges, so
the outside 19-set `O` has at least `454+184-21*24=134` blue edges and at
most 37 red edges.  [Brouwer's exact extension of Turan's theorem](https://ir.cwi.nl/pub/6791/6791D.pdf)
says that an `n`-vertex graph with independence number at most `t` and at
most

```text
T(n,t)+floor(n/t)-2
```

edges is a union of `t` cliques, where `T(n,t)` is the minimum from Turan's
theorem.  Here `T(19,4)=36`, so the threshold is 38.  The red graph on `O`
would be a union of four cliques; one has at least five vertices, contrary to
the absence of a red `K_5`.  Thus red cannot be disconnected.

For the other color we use the following small edge lemma.

```text
Every (5,5;19) graph has at least 43 edges.              (R5519-edge)
```

To prove it, suppose `F` has at most 42 edges.  If a vertex has degree
`d<=3`, the complement of `F` on its `18-d` nonneighbors is a `(4,5)` Ramsey
graph.  The exact values

```text
E(4,5,15)=66, E(4,5,16)=72, E(4,5,17)=79, E(4,5,18)=85
```

give respective lower bounds `42,50,58,68` on `e(F)` as `d=3,2,1,0`.
Equality for `d=3` leaves the three neighbors mutually nonadjacent and
anticomplete to the other 15 vertices, yielding an independent five-set.
Hence `delta(F)>=4`; averaging supplies a degree-four vertex `v`.

Let `N` be its four neighbors and `S` its 14 nonneighbors.  The complement
of `F[S]` is a `(4,5;14)` graph, so `e(F[S])>=31`.  Put
`a=e(F[N])`, `b=e_F(N,S)`, and `z=a+b`.  Since `N` is `K_4`-free, `a<=5`;
the minimum-degree bound gives `2a+b>=12`.  If `e(F[S])>=32`, then `z<=6`
and `2a+b=a+z<=11`, a contradiction.  Therefore `e(F[S])=31`, and the
same inequalities force `a=5`, `b=2`, `z=7`.  The complement of `F[S]` is
the unique 60-edge `(4,5;14)` graph.  Its 80 triangles have vertex
transversal number four, as the verifier checks directly from the catalog's
graph6 representative.  The missing edge `xy` of `F[N]` has at most two
neighbors in `S`, so some independent triple of `F[S]` avoids all of them.
Together with `x,y` it is an independent five-set, proving `(R5519-edge)`.

Finally, if blue were disconnected on `D`, the red graph would have at least
184 edges there.  This leaves at least `449+184-21*24=129` red edges, hence
at most 42 blue edges, on `O`, contradicting `(R5519-edge)`.  The last
`M=218` profile therefore has both backbone colors connected.

### All order-24 and order-25 escape backbones are connected

The same argument closes every remaining profile with `L>=24`, including the
`M=219,220` cases.  If a disconnected color on `D` has a component with
independence number one, that component is a clique.  At `|D|=25`, the
universal internal minimum degree `|D|-22=3` makes it a `K_4`; each of its
vertices must then see all 18 outside vertices in the same color, immediately
forming a `K_5`.  At `|D|=24`, a complete component is a `K_3` or `K_4`.  A
`K_4` has a common outside neighbor, while every outside vertex sees all of a
`K_3`; an outside edge then completes a `K_5`.  Such an edge must exist because
the outside color graph has independence number at most four.

Thus every component has independence number at least two.  The opposite
color is complete between components, so their independence numbers sum to
at most four.  There are exactly two components, both with independence
number two and order at most 13.  The only partitions and the exact minimum
numbers of opposite-color edges on `D` are

```text
|D|=24:  11+13 or 12+12,  at least 184 edges;
|D|=25:  12+13,           at least 12*13+20+26 = 202 edges.
```

Brouwer's theorem also gives `e(5,5,18)>=35`: here `T(18,4)=32`, and every
graph through 34 edges with independence number at most four is a union of
four cliques, which cannot cover 18 vertices without a `K_5`.  By complement
symmetry, the maximum `(5,5)` edge counts at orders 18 and 19 are therefore
118 and 128.  For `M=219,220`, edge accounting in each color and at each
backbone order gives

| `M` | `d` | disconnected color | opposite edges forced on outside | allowed maximum |
|---:|---:|:---:|---:|---:|
| 219 | 24 | red | 133 | 128 |
| 219 | 24 | blue | 130 | 128 |
| 219 | 25 | red | 130 | 118 |
| 219 | 25 | blue | 127 | 118 |
| 220 | 24 | red | 132 | 128 |
| 220 | 24 | blue | 131 | 128 |
| 220 | 25 | red | 129 | 118 |
| 220 | 25 | blue | 128 | 118 |

Every case is impossible.  Hence any surviving disconnected profile must
have `|D|<=23`.

Exact enumeration of all 349 ordered split profiles now gives

| `M` | all | proved connected | diameter <=8 (`L>=29`) | diameter <=5 (`L>=32`) | escapes |
|---:|---:|---:|---:|---:|---:|
| 214 | 1 | 1 | 0 | 0 | 0 |
| 215 | 5 | 5 | 2 | 0 | 0 |
| 216 | 17 | 17 | 11 | 5 | 0 |
| 217 | 40 | 40 | 30 | 16 | 0 |
| 218 | 69 | 69 | 52 | 28 | 0 |
| 219 | 95 | 95 | 70 | 37 | 0 |
| 220 | 122 | 121 | 88 | 49 | 1 |

The threshold is deletion-stable.  If a set `S` of `k<=d-27` anchors is
removed, the remaining order is at least 27 and the same global degree count
gives internal minimum degree

```text
21-(43-d+k)=d-k-22 >= 5.
```

The component argument therefore applies again.  Neither color can be
disconnected after deleting at most `d-27` vertices, so

```text
vertex-connectivity of each color on D >= d-26 >= L-26.   (Profile-kappa)
```

In total, 348 of the 349 profiles force both color backbones connected.  The
numbers of profiles certifying vertex connectivity at least
`k=1,2,...,11` in each color are respectively

```text
348, 291, 253, 231, 193, 135, 128, 97, 22, 22, 20.
```

The same internal-degree bound also controls diameters.  A color geodesic
of length at least nine gives four disjoint closed neighborhoods, whereas a
geodesic of length at least six gives three.  Since every such neighborhood
has at least `d-21` vertices, `d>=29` forces diameter at most eight and
`d>=32` forces diameter at most five.  Thus the profile lower bound alone
certifies both-color diameter at most eight in 253 profiles and at most five
in 135 profiles.  (The earlier `M=214,215` arguments certify some stronger
bounds outside these two generic counts.)

The sole surviving connectivity escape has lower-bound multiplicity

```text
M=220: L=22       -> 1.
```

The complete machine-readable list is
[`BACKBONE_ESCAPE_PROFILES.txt`](BACKBONE_ESCAPE_PROFILES.txt).  Its one
canonical data line has SHA-256
`d2af6208594ffb7e20180e4a79e46025c637bccfe7222f815521fdd73a8cf694`,
and the verifier regenerates it exactly.  A disconnected realization has
`|D|=L=22`.  The number of excess units not forced to serve distinct nonexact
degree-21 vertices is exactly

```text
E-(n_21-|D|)=|D|-L = 0.
```

Thus every excess unit lies on a different nonexact degree-21 vertex, with no
repeated excess and no excess on a noncentral local side.  These are direct
cardinality and excess-budget constraints for a construction or local-repair
search; they do not discard the last escape profile without further
compatibility information.

## Exact normal forms for the preliminary residual profiles

Let `D` be the full set of doubly exact vertices and put `d=|D|`.  The previous
profile bound first leaves the following four candidates at the listed
orders.  The order-23 support obstruction below subsequently eliminates three
of them and the order-23 realization of `M220-W3`.  The table and excess file
are retained as an exact audit trail of that reduction.  Here `L` is the
certified lower bound for `d`.

| profile | global red-degree multiset | possible `d` | slack `d-L` | excess/triangle splits |
|:---|:---:|:---:|:---:|---:|
| `M219-W9` | `20^3 21^40` | 23 | 0 | 6 |
| `M220-W3` | `20^1 21^42` | 22 or 23 | 0 or 1 | 7 |
| `M220-W9-A21` | `20^2 21^40 22^1` | 23 | 0 | 6 |
| `M220-W9-mixed` | `20^2 21^40 22^1` | 23 | 0 | 6 |

The two `W=9` profiles at `M=220` have the same global degree multiset but
different distributions between the original anchor sides.  Every exact
quadruple `(E_R,E_B,T_R,T_B)`, repeated for each possible `d` and accompanied
by its exact slack, is in
[`RESIDUAL_EXCESS_SPLITS.tsv`](RESIDUAL_EXCESS_SPLITS.tsv).  Its 32 data rows
have SHA-256
`2bb0a8f67e346f1066a9cf2d8219ef89e97480bcf973372fe59040bacefed857`.

### Two sparse diagonal edge bounds

The order-19 lemma above admits a useful elementary bootstrap:

```text
e(5,5,20) >= 50,        e(5,5,21) >= 56.              (Sparse-20/21)
```

For the first bound, suppose an order-20 Ramsey graph `F` has at most 49
edges and choose a minimum-degree vertex `v`, of degree `r<=4`.  If `r<=3`,
the complement on the `19-r` nonneighbors of `v` is a `(4,5)` graph.  The
exact extremal values at orders 19, 18, 17, and 16 give respective lower
bounds

```text
r=0,1,2,3:       e(F) >= 79,69,59,51,
```

all impossible.  Thus `r=4`.  Let `N` be the four neighbors, `S` the 15
nonneighbors, `a=e(F[N])`, and `b=e_F(N,S)`.  Since the complement of `F[S]`
is a `(4,5;15)` graph, `e(F[S])>=105-66=39`, and hence `a+b<=6`.  Summing
the degrees of `N` and using the minimality of `r` gives `2a+b>=12`, so
`a>=6`.  But `F[N]` is `K_4`-free and therefore `a<=5`, a contradiction.

For an order-21 Ramsey graph, apply the order-20 bound to all 21 one-vertex
deletions.  Every edge survives in 19 of them, so

```text
19e >= 21*50,       hence e >= 56.
```

Complementation bounds the maximum edge counts at orders 20 and 21 by 140
and 154.  These are the outside-edge caps used below.

### Components at order 23

Fix a disconnected backbone color `Q`.  Its induced minimum degree on `D` is
`d-22=1`.  A component with `Q`-independence number one would therefore be
`K_2`, `K_3`, or `K_4`.  At `d=23`, the vertices of those cliques have,
respectively, 20, 19, or 18 `Q`-neighbors in the outside 20-set.  Their common
outside neighborhoods have orders at least 20, 17, or 12.  The first contains
a `Q`-triangle by `R(3,5)=14`, the second contains a `Q`-edge because the
whole graph has `Q`-independence number at most four, and the third is
nonempty.  Each alternative completes a `Q`-colored `K_5`.

Thus each component has independence number at least two.  Since the opposite
color is complete between components and has no `K_5`, there are exactly two
components, each of independence number two.  Their orders are therefore

```text
10+13 or 11+12.
```

Inside either component, the opposite-color graph is a `(3,5)` Ramsey graph.
For an order pair `(a,b)`, if those two catalog graphs have `e_a,e_b` edges,
the number of opposite-color edges on `D` is exactly

```text
s = ab + e_a + e_b.                                  (Component-s)
```

There is a further cover constraint that uses exactness vertex by vertex.  If
`H` is the opposite-color graph on a `Q`-component `C`, every outside vertex's
opposite-color neighbors in `C` must hit every independent four-set of `H`.
Otherwise, the corresponding `Q`-colored `K_4` together with the outside
vertex is a `Q`-colored `K_5`.  Write `tau_4(H)` for the minimum size of such a
transversal.  If `|C|=a`, its other component has order `b`, and the outside
has order `o`, exact degree 21 on `C` gives the necessary inequality

```text
a(21-b)-2e(H) >= o*tau_4(H).                           (K4-cover)
```

Indeed, the left side is exactly the number of opposite-color edges from `C`
to the outside: the sum of the opposite degrees on `C` is `21a`, while the
opposite graph inside `D` contributes `ab+2e(H)` incidences.

The complete catalog has the following `tau_4` spectra, written
`transversal size : number of isomorphism types`:

```text
order  9:  1:26, 2:263, 3:1
order 10:  2:197, 3:116
order 11:  3:105
order 12:  4:12
order 13:  5:1.
```

In the `10+13` case at `d=23`, the unique order-13 type has `e=26` and
`tau_4=5`.  Its left side in `(K4-cover)` is 91, whereas the 20 outside
vertices require at least 100 edges.  Thus this entire component partition is
impossible.  In the surviving `11+12` case, `(K4-cover)` forces the order-12
type to have exactly 20 edges (there is one such type) and the order-11 type
to have at most 19 edges.  Combining this with `(Component-s)` and
`(Sparse-20/21)` gives the exact finite menu:

| `M` | disconnected color | cap on `s` | `10+13` types | `11+12` types | total |
|---:|:---:|---:|---:|---:|---:|
| 219 | red  | 170 | 0 | 57 | 57 |
| 219 | blue | 173 | 0 | 87 | 87 |
| 220 | red  | 171 | 0 | 87 | 87 |
| 220 | blue | 172 | 0 | 87 | 87 |

For example, a red disconnection at `M=219` makes the opposite blue outside
edge count `s-30`; the order-20 maximum 140 gives `s<=170`.  The other three
rows follow from the same exact identity, followed by `(K4-cover)`.  This menu
is only preliminary: equality in `(K4-cover)` supplies a final obstruction.

Call the order-12 opposite-color graph `H_12`.  Its cover inequality is the
equality

```text
12(21-11)-2*20 = 80 = 20*tau_4(H_12).
```

Consequently every outside vertex has exactly four opposite-color neighbors
in this component, and those four vertices form a minimum transversal.  The
unique 20-edge order-12 catalog graph has 16 minimum four-transversals: 12
span three `H_12` edges and four span four edges.  In particular, every one
contains an edge.

Now call the other component graph `H_11`.  If an outside vertex's
opposite-color neighbors in `H_11` also contained an edge, that edge, an edge
from its `H_12` transversal, the complete opposite-color join between the
components, and the outside vertex would form an opposite-color `K_5`.
Therefore its `H_11` neighbor set is independent.  It must simultaneously
hit every independent four-set of `H_11`, so it is an independent
transversal of order three or four.

The cover inequality already restricts `H_11` to at most 19 edges.  For each
of the 87 eligible order-11 catalog graphs, take the union of all vertices
that occur in an independent transversal of order three or four.  The exact
histogram below is indexed by `e(H_11)` and the size of that union:

| `e(H_11)` | support 0 | support 4 | support 5 | support 6 | support 7 |
|---:|---:|---:|---:|---:|---:|
| 15 | 1 | 0 | 0 | 0 | 0 |
| 16 | 5 | 1 | 0 | 0 | 0 |
| 17 | 15 | 3 | 1 | 0 | 0 |
| 18 | 20 | 6 | 3 | 1 | 1 |
| 19 | 23 | 4 | 2 | 1 | 0 |

No support has all 11 vertices.  Yet every vertex of `H_11` has at least

```text
21-12-deg_H11(v) = 9-deg_H11(v) >= 5
```

opposite-color neighbors outside: triangle-freeness makes every neighborhood
independent, so `Delta(H_11)<=alpha(H_11)<=4`.  Every vertex would therefore
have to appear in one of the independent transversals, contradicting the
catalog support bound of seven.  This eliminates every `d=23` disconnection,
in both colors and for both `M=219,220`.

### Components and the asymmetric singleton at order 22

At `d=22`, the same common-neighborhood calculation excludes every
nonsingleton component of independence number one: the common outside sets
for `K_2,K_3,K_4` have orders at least 19, 15, and 9.  Consequently either

```text
two alpha-two components have orders 9+13, 10+12, or 11+11,
```

or there is one singleton and one order-21 component of independence number
three.  Other component patterns violate the total independence budget four
and the order-13 bound supplied by `R(3,5)=14`.

For the two-component case, `(K4-cover)` eliminates `9+13` outright: the
order-13 component supplies only 104 opposite-color outside edges, one short
of the required `21*5=105`.  In `10+12`, it retains every order-10 type with
`tau_4=2` but only the edge-10 through edge-13 types with `tau_4=3`.  All
`11+11` pairs pass the cover inequality.  Combining that filter with the edge
caps gives the preliminary cover-only menu

| disconnected color | cap on `s` | `9+13` types | `10+12` types | `11+11` types | total |
|:---:|---:|---:|---:|---:|---:|
| red  | 164 | 0 | 2,676 | 5,564 | 8,240 |
| blue | 165 | 0 | 2,676 | 5,565 | 8,241 |

The simultaneous outside rows impose a much sharper capacity condition.  For
a component graph `H` of order `a`, define `iota(H)` to be the maximum number
of independent transversals of its independent four-sets that can be packed
as a multiset while using each vertex `v` at most

```text
a-1-deg_H(v)
```

times.  This is exactly the opposite-color degree available from `v` to the
21 outside vertices when `d=22`.  For each outside vertex, its neighbor set
in both components is a transversal.  At least one of the two sets must be
independent: if both contained an edge, those edges, the complete join between
components, and the outside vertex would give an opposite-color `K_5`.
Therefore every surviving pair satisfies

```text
iota(H_1)+iota(H_2) >= 21.                            (Row-capacity)
```

An exact memoized packing computation on the complete catalogs gives the
following capacity spectra among cover-feasible types with positive capacity:

```text
order 10:  6:79, 7:37, 8:11, 9:1, 10:3, 12:27, 13:8, 18:1
order 11:  7:23, 8:2, 14:1
order 12:  8:1.
```

For `10+12`, the displayed order-12 type is the only one with positive
capacity, so `(Row-capacity)` requires an order-10 capacity of at least 13.
Exactly nine order-10 types qualify.  For `11+11`, one component must be the
unique capacity-14 type, while the other can be any of the 26 positive-
capacity types.  Thus the relaxed two-component menu is

| disconnected color | `10+12` types | `11+11` types | total |
|:---:|---:|---:|---:|
| red  | 9 | 26 | 35 |
| blue | 9 | 26 | 35 |

One more necessary condition remembers that the unselected rows still have to
be transversals.  Suppose `k` independent rows use vertex `v` exactly `y_v`
times, and put `q=21-k`.  The remaining column demand is
`r_v-y_v`, where `r_v=a-1-deg_H(v)`.  Necessarily

```text
0 <= r_v-y_v <= q,
sum_{v in I} (r_v-y_v) >= q  for every independent four-set I.
```

The second inequality holds because each of the remaining `q` rows must meet
`I`.  Define the *extendable capacity* by maximizing `k` over multisets of
independent transversals subject to these residual conditions.  Exact state
enumeration on the 36 relaxed survivors gives maximum extendable capacities

```text
order 10: 10,       order 11: 6,       order 12: 3.
```

But the outside-row argument still requires the two component capacities to
sum to at least 21.  The largest possible sums are only `10+3=13` for
`10+12` and `6+6=12` for `11+11`.  Therefore every two-component
disconnection at `d=22` is impossible.

The exact 36 graph6 representatives from the intermediate sieve, with edge
count, `tau_4`, relaxed and extendable capacity, and their forced role, are
listed in
[`D22_CAPACITY_TYPES.tsv`](D22_CAPACITY_TYPES.tsv).  This makes the sieve
independently auditable and records precisely how the preliminary 35-pair
menu collapses.

There is a sharper conclusion for a singleton.  The only order-22 profile is
`M220-W3`, with 451 red edges and degree multiset `20^1 21^42`.  Suppose an
exact vertex `u` is isolated in the red backbone.  Its red neighborhood is the
outside 21-set `O`, and its blue neighborhood is the other 21 anchors `C`.
Exactness forces 100 red edges on `O` and 100 blue, hence 110 red, edges on
`C`.  Global edge accounting gives 220 red `C--O` edges.  But the red degree
sum on `O` is `20+20*21=440`; subtracting its 200 internal incidences and the
21 edges to `u` gives only 219 red `C--O` edges.  Therefore a red singleton is
impossible.

If `u` is instead isolated in blue, the two counts agree at 220.  Moreover,
its red neighborhood `C` and blue neighborhood `O` are necessarily exact
`(4,5;21,100)` cores.  Thus the sole singleton escape is not generic: it is a
second doubly exact anchoring of the original `M=220` profile, with all other
21 exact anchors on the red side and none on the blue side.

Since the two-component alternatives have now been eliminated, this blue
singleton is the only possible disconnected-backbone normal form left by the
entire argument.

### Bridge to the known Ramsey-42 catalog

Delete the isolated-blue exact vertex `u` from the singleton normal form.
Each of the 21 vertices in `C` loses its red edge to `u`, so its red degree
drops from 21 to 20.  No vertex in `O` loses a red edge: its unique degree-20
vertex remains degree 20 and the other 20 vertices remain degree 21.  Thus the
resulting Ramsey graph on 42 vertices necessarily has degree multiset

```text
20^22 21^20.                                             (Singleton-delete)
```

The companion radius-three artifact contains 328 known Ramsey-42 graphs and
uses complement symmetry to represent 656 color orientations.  The independent
[`verify_known_r42_bridge.py`](verify_known_r42_bridge.py) audit pins that
catalog by SHA-256 and finds zero orientations with `(Singleton-delete)`.  In
fact, the label-independent lower bound obtained by matching sorted degree
sequences shows that every graph with `(Singleton-delete)` is at least four
edge edits from every known orientation.  The full lower-bound histogram is

```text
edge edits at least   4  5   6    7    8    9   10  11  12
known orientations    1 17  72  146  187  152  67  13   1.
```

The unique closest orientation is base catalog index 93 (zero-based), with
degree multiset `19^4 20^20 21^16 22^2`.  The companion
[`ramsey_r55_catalog_edge_radius4_classification`](../ramsey_r55_catalog_edge_radius4_classification)
exhaustively lists all 8,408 Ramsey-preserving exactly-four flips from the 328
stored parents and proves, using complement symmetry, that every
Ramsey-preserving graph within four edits of any of the 656 orientations is
again in the known catalog.  Since the target degree multiset occurs nowhere
in that catalog, the singleton deletion has edge-edit distance at least five
from every known orientation.  The bridge verifier additionally pins and
scans the complete radius-four map, finding neither the target multiset nor
its color complement among its 8,408 records.

The degree signature makes radius five much cheaper than a generic
classification.  Of the 656 catalog orientations, only 18 have the
degree-sequence edit lower bound at most five.  Six have the wrong edge-count
parity for exactly five flips, leaving 12 orientations.  On each remaining
orientation, equality in the degree-edit bound forces every flip endpoint to
move monotonically toward degree 20 or 21: additions join only rising
vertices and deletions join only falling vertices.  The endpoint changes are
at most two.  The independent
[`verify_known_r42_radius5.py`](verify_known_r42_radius5.py) audit enumerates
all small degree-realizing addition/deletion graphs, deduplicates the flip
sets, explicitly checks the target degree multiset, and searches both colors
for a 5-clique.  Exactly 230,503 flip sets survive the degree constraints and
none preserves the Ramsey property.  Therefore the singleton deletion is at
edge-edit distance at least six from every known catalog orientation.

Consequently, any hard-branch graph realizing the last disconnected normal
form must delete to a Ramsey-42 graph outside the published known catalog and
outside its radius-five neighborhood.  This is a relative catalog exclusion,
not a completeness claim for Ramsey graphs on 42 vertices.

### Exact local profile inside the singleton normal form

The singleton structure also determines every remaining unit of local
deficiency.  Let `z in O` be the unique red-degree-20 vertex.  The 22
vertices `u union C` are doubly exact, so each has local pair
`(t_R,t_B)=(100,100)`.  The hard-branch excess identity for `M220-W3` leaves
20 units above the baseline deficiency seven.  Every one of the 20
degree-21 vertices in `O minus {z}` is outside the exact-anchor set and hence
uses at least one unit.  Therefore each uses exactly one, while `z` uses
none:

```text
z:                  (d,t_R,t_B) = (20,93,107),
o in O minus {z}:   (d,t_R,t_B) = (21,99,100) or (21,100,99).
```

If `x` vertices have the first exceptional type, triangle-incidence
divisibility gives

```text
x in {0,3,6,9,12,15,18},
(T_R,T_B) = (1431-x/3, 1429+x/3).                       (Singleton-local)
```

Thus the seven `M220-W3` rows in `RESIDUAL_EXCESS_SPLITS.tsv` have a direct
vertex-level interpretation, not merely a global excess interpretation.

### A complete SAT dichotomy for the residual singleton

There is a useful exact test that avoids enumerating either order-21 core.
Delete `u`, label `C=0,...,20`, label `O=21,...,41`, and choose `z=21`.
For each pair `i<j<42`, let the Boolean variable `x_ij` mean that `ij` is
red in `F=G-u`.  Impose:

1. neither color has a `K_5` on any five vertices of `F`;
2. `C` has no red `K_4` and `O` has no blue `K_4`;
3. the red degrees in `F` are 20 on `C union {z}` and 21 on
   `O minus {z}`; and
4. `G[C]` has 100 red edges and `G[O]` has 110 red edges (equivalently,
   100 blue edges).

These conditions are a relaxation of the singleton normal form because they
omit `(Singleton-local)` and all other local-triangle equations.  Nevertheless
they have a sharp two-sided interpretation.  If the CNF is UNSAT, then the
singleton normal form is impossible.  If it is SAT, extend the model by
making all `u-C` edges red and all `u-O` edges blue.  A monochromatic `K_5`
not using `u` is forbidden by condition 1.  One using `u` would be a red
`K_4` in `C` or a blue `K_4` in `O`, forbidden by condition 2.  Hence every
SAT model is already a certified order-43 Ramsey graph and proves
`R(5,5)>=44`.

[`singleton_sat.py`](singleton_sat.py) emits this formula deterministically
using Sinz sequential counters and independently checks any SAT model by
exhausting all `binom(43,5)=962598` five-sets.  Its pure-Python self-test
exhausts the sequential-counter encoding through five input literals and the
independent balanced-binary-adder encoding through six.  The base DIMACS has

```text
157521 variables
2028680 clauses
SHA-256 3eb71332561297639e6798fd5e1d495437181d4c62193a0cc57cabf24b742bca.
```

Reproduce the encoding (the DIMACS itself is intentionally not committed):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 singleton_sat.py self-test
PYTHONDONTWRITEBYTECODE=1 python3 singleton_sat.py generate singleton.cnf \
  | cmp - EXPECTED_SINGLETON_SAT.txt
```

The optional local-profile strengthening introduces one exact indicator for
each color of each triangle in `F`, reuses those indicators at their three
vertices, and encodes the displayed local counts with balanced binary
population-count circuits.  It enforces `(100,100)` on all vertices of `C`,
`(93,107)` on `z`, and total 199 on each other vertex of `O`.  The last
condition is equivalent to the two displayed alternatives because each
order-21 local `(4,5)` graph has at most 100 edges.  This strengthened DIMACS
has

```text
458257 variables
3784316 clauses
SHA-256 63efa37992e27fe12a668f7c7c8c917871d35938b6f0c003f6078731b9dc31fa.
```

Generate it with:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 singleton_sat.py generate \
  singleton-local.cnf --local-profile | cmp - EXPECTED_SINGLETON_LOCAL_SAT.txt
```

Finally, the seven values of `x` in `(Singleton-local)` give seven exhaustive
typed branches.  In a typed branch the script uses a selector for each vertex
of `O minus {z}`, separately fixes its local pair to `(99,100)` or
`(100,99)`, and fixes the selector sum to `x`.  Each branch has 458107
variables and 3782794 clauses.  All seven deterministic hashes are recorded
in [`SINGLETON_TYPED_BRANCHES.tsv`](SINGLETON_TYPED_BRANCHES.tsv).  For
example:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 singleton_sat.py generate \
  singleton-x0.cnf --local-profile --red-exceptional 0
```

UNSAT certificates for all seven rows would eliminate the singleton normal
form; a SAT model in any row would be the desired order-43 witness.

For a solver transcript containing a `s SATISFIABLE` line and standard `v`
model lines, independently verify and export the red graph in graph6 format:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 singleton_sat.py check-model solver.log \
  --require-local-profile --write-graph singleton-witness.g6
```

The complete edge-resolved catalog menu is
[`RESIDUAL_COMPONENT_MENUS.tsv`](RESIDUAL_COMPONENT_MENUS.tsv).  Its empty
data section certifies that no two-component catalog pair survives; the
header records the schema used by the preceding intermediate sieves.  Its
SHA-256 is
`b471f2d664cc156e89ff951287e1f739c6747e4d1f0c63969b298609675f10f2`.
The verifier regenerates both residual files exactly.  This is a finite
necessary-condition menu, not an assertion that any listed pair extends to a
43-vertex coloring.

## Hard-branch propagation theorem

For `18 <= q <= 24`, the exact maximum edge counts in an order-`q`
`(4,5)` graph are

```text
q       18  19  20  21  22  23  24
U(q)    85  92 100 107 114 122 132.
```

Every row and column profile computed above must satisfy

```text
18 <= d_u <= 24,
t_R(u) <= U(d_u)-7,
t_B(u) <= U(42-d_u)-7.                                (D7)
```

Indeed, `t_R(u)` and `t_B(u)` are exactly the edge counts of the two local
`(4,5)` graphs at `u`; `(D7)` is precisely the definition of the hard branch.
This supplies 84 exact local inequalities in addition to the mixed-clique
clauses.  The left sides are explicit quadratic functions of the cross bits,
or can be maintained as local-repair scores under a single-bit flip.

There is also a much stronger global propagation condition:

```text
at least 241-M vertices u in A union B satisfy
       (d_u, t_R(u), t_B(u)) = (21,100,100).             (PM)
```

To prove `(PM)`, the exact deficiency identity gives

```text
Delta = (1247-W)/2.
```

The 86 local sides have baseline deficiency `86*7=602`, so at most

```text
E = Delta-602 = (43-W)/2
```

of them can have deficiency greater than seven.  Meanwhile, at most `W/3`
vertices have nonzero degree weight, hence at least `42-W/3` secondary
vertices have degree 21.  A degree-21 vertex can fail to be doubly exact only
if at least one of its two local sides is among those `E` exceptional sides.
Therefore the number of secondary doubly exact vertices is at least

```text
42 - W/3 - (43-W)/2 = (123+W)/6
                          >= 241-M,
```

where the last step is `(WM)`.  A vertex is doubly exact exactly when its
displayed triple is `(21,100,100)`: red degree 21 makes both local orders 21,
and the two local edge counts are then seven below `U(21)=107`.  Thus `(PM)`
does not choose or label the secondary anchors in advance.

There are also side-specific guarantees.  Write `s=220-M` and split
`W=W_A+W_B` over the two sides.  Equation `(S)` and the pointwise weight
bound give `W_A>=3s` and `W_B>=3(s+1)`.  Subtracting the same exceptional-side
budget `E` separately from the degree-21 population on either side yields

```text
exact vertices in A >= 21-W_A/3-E
                    = -1/2+W_A/6+W_B/2 >= 2s+1,
exact vertices in B >= 21-W_B/3-E
                    = -1/2+W_A/2+W_B/6 >= 2s,

number of doubly exact vertices in A >= 2s+1 = 441-2M,
number of doubly exact vertices in B >= 2s   = 440-2M.   (PM_side)
```

The total guarantee `(PM)` is stronger than adding these two separate bounds,
because the exceptional sides cannot simultaneously be spent twice.  The
three guarantees specialize as follows:

```text
M                             214 215 216 217 218 219 220
forced exact vertices in A     13  11   9   7   5   3   1
forced exact vertices in B     12  10   8   6   4   2   0
forced exact vertices in A+B   27  26  25  24  23  22  21
```

For a hard-branch cross search, `(D7)` and `(PM)` are lossless.  A general
construction search must retain the complementary branch in which some
local deficiency is at most six.

## Exact single-cross-flip update

The propagated scores also admit a simple local-repair rule.  Toggle one
cross edge `ab`, and put

```text
sigma = +1 for blue-to-red,  -1 for red-to-blue,
c_R(a,b) = |N_G(a) intersect N_G(b)|,
c_B(a,b) = |N_complement(G)(a) intersect N_complement(G)(b)|.
```

The common-neighbor counts exclude `a,b` and do not depend on the color of
`ab`.  At each endpoint `u in {a,b}`, the profile changes by

```text
(d_u, t_R(u), t_B(u))
    -> (d_u + sigma,
        t_R(u) + sigma*c_R(a,b),
        t_B(u) - sigma*c_B(a,b)).                       (F_end)
```

For a third vertex `u`, its degree is unchanged.  Its red-local count changes
by `sigma` exactly when both `ua` and `ub` are red; its blue-local count
changes by `-sigma` exactly when both are blue.  Otherwise neither changes.
The chosen anchor `v` always sees one red and one blue edge to `a,b`, so its
profile remains `(21,100,100)`.

This follows because only the membership of one endpoint in the other
endpoint's color-neighborhood changes, while at a third vertex only the
color of the single internal edge `ab` changes.  Thus a local-repair program
can update all 42 propagated profiles in one linear scan after a cross flip;
it need not rebuild the 43-vertex graph or rescan five-sets.

## Definition-level audit

`verify_anchor_propagation.py` uses the same embedded `(4,5;21,100)` sample
core as the cross-normal-form artifact, with a nontrivial deterministic
relabeling on the blue side.  It builds seven deterministic
21-by-21 matrices with 214 through 220 red entries.  For every matrix and all
42 non-anchor vertices, it compares `(A_R)`--`(B_B)` against a direct scan of
the resulting labeled 43-vertex coloring.  It also audits `(F_end)` and the
third-vertex rule on 14 toggles, once in each direction for every matrix.

All seven matrices satisfy the earlier cardinality and row/column degree
bounds, but have degree weights from 99 through 111, only 17 through 21
degree-21 vertices, no secondary doubly exact vertex, and violations of
`(D7)`.  They are deliberately not claimed to satisfy the mixed-`K_5`
clauses.  Their role is a regression witness that the new tests contain
information absent from the earlier independent cardinality/degree intervals,
not evidence about feasibility.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_anchor_propagation.py \
  | cmp - EXPECTED_OUTPUT.txt
```

Expected output is

```text
PASS exact row/column formulas on 7 matrices and 294 vertex profiles
PASS exact one-cross-flip updates on 14 flips and 588 vertex profiles
PASS all test matrices satisfy cross cardinality and first-degree bounds
PASS split degree deviations equal M-220 and M-221
PASS first-degree-feasible test weights=99,...,111 exceed hard limit 39
PASS hard split degree-profile counts=1,5,17,40,69,95,122 total=349
PASS triangle-pair counts=1,3,8,15,20,27,39 total=113 sha256=ccaf9ccec34aa4633cf2019d3f85f34e714c1f0bb17db444e9f8034c650c936c
PASS exact local-side minima red=43,38,36,34,29,27,25 blue=41,40,36,32,31,27,23
PASS M=214 forces degrees 20^13,21^30 and excess split red=0 blue=2
PASS M=214 forces monochromatic triangle counts red=1403 blue=1463
PASS M=214 exact-anchor backbone order=28,...,30 min degrees red=13 blue=12
PASS backbone vertex connectivity is at least red=4 blue=2
PASS both backbone colors have diameter at most 5
PASS M=215 exact-anchor backbone order=27,...,33 min degrees red=11 blue=10
PASS M=215 backbones connected; red connectivity>=2 diameters red<=5 blue<=8
PASS M=216 red backbone order=26,...,36 is connected with diameter<=8
PASS M=216 blue disconnection forces two 13-vertex critical components
PASS C13(1,5) gives a sharp disconnected-blue abstract backbone
PASS outside-edge obstructions eliminate d=26 and M217/218 d=25 cuts
PASS small R(3,5) catalog counts at orders 9,...,13 are 290,313,105,12,1
PASS every R(5,5;19) graph has at least 43 edges
PASS diagonal edge minima at orders 20,21 are at least 50,56
PASS the unique M=218 profile has both backbone colors connected
PASS d=24/25 cuts are impossible in the M=219/220 escape profiles
PASS both-color connectivity profiles M214..220=1/1,5/5,17/17,40/40,69/69,95/95,121/122
PASS backbone escape profiles=0,0,0,0,0,0,1 total=1 sha256=d2af6208594ffb7e20180e4a79e46025c637bccfe7222f815521fdd73a8cf694
PASS residual excess split counts=6,7,6,6 rows=32 sha256=2bb0a8f67e346f1066a9cf2d8219ef89e97480bcf973372fe59040bacefed857
PASS independent-four cover sieve removes d=23 10+13 and d=22 9+13
PASS pre-support d=23 component-pair menus M219 red/blue=57/87 M220 red/blue=87/87
PASS d=23 independent-transversal support eliminates all four menus
PASS pre-capacity d=22 two-component menus red/blue=8240/8241
PASS d=22 independent-row capacity leaves red/blue=35/35 type pairs
PASS d=22 extendable-row capacity eliminates every two-component pair
PASS d=22 red singleton impossible; blue singleton reanchors two R(4,5;21,100) cores
PASS residual component menu rows=0 sha256=b471f2d664cc156e89ff951287e1f739c6747e4d1f0c63969b298609675f10f2
PASS profile diameter bounds <=8 for 253 profiles and <=5 for 135
PASS profile vertex-connectivity counts k=1,...,11 are 348,291,253,231,193,135,128,97,22,22,20
PASS first-degree-feasible tests have 0 secondary exact anchors
PASS side anchor minima A=13,11,9,7,5,3,1 B=12,10,8,6,4,2,0
PASS hard branch forces secondary exact anchors=27,26,25,24,23,22,21
```

The main audit uses CPython 3.11 or later, the standard library, exact integer
arithmetic, and no solver, randomness, floating point, or network.  It embeds
the one small graph6 representative needed for the order-19 lemma and took
about 2.1 seconds under CPython 3.11.2 on the research host.  The separate
provenance audit fetches the pinned official catalog files and checks their
SHA-256 digests, counts, Ramsey properties, edge histograms, and the extremal
singleton.  It then computes every independent-four transversal number and
checks the order-12 minimum-cover edge distribution and the order-11
independent-cover support obstruction.  It also recomputes every order-22
independent-row capacity by exact memoized integer packing, checks the
row-completion inequalities, and reproduces the 36 graph6 representatives in
the capacity-type list.  Finally, it certifies that no order-22 two-component
menu row survives, independently of the joint-invariant product routine in
the main verifier:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_catalog_inputs.py
```

It uses only the standard library and network access; its dominant input is
the approximately 91 MB compressed edge-extremal `(4,5)` archive.

The catalog bridge is a fast local check against the pinned Ramsey-42 file
already committed by the companion radius-three artifact:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_known_r42_bridge.py \
  | cmp - EXPECTED_R42_BRIDGE.txt
PYTHONDONTWRITEBYTECODE=1 python3 verify_known_r42_radius5.py \
  | cmp - EXPECTED_R42_RADIUS5.txt
```

The radius-five audit uses only the Python standard library and took about 33
seconds on the research host.  Its trust boundary is the pinned known catalog;
unlike the radius-four bridge, it does not invoke or trust a SAT solver.

## Scope, provenance, and trust boundary

The formulas are elementary partitions and are checked independently against
the definition of a local color-neighborhood.  The `241-M` secondary-anchor
count imports the companion
[`ramsey_r55_local_extremal_deficiency`](../ramsey_r55_local_extremal_deficiency)
theorem, including its stated trust in the completeness of the pinned McKay
`(4,5)` extremal catalogs.  The backbone connectivity corollaries additionally
use the classical exact values `R(5,3)=14` and `R(3,4)=9`, and the `M=216`
red result uses Brooks' theorem.  The `M=218` closure and the residual
component menus additionally trust
[McKay's complete small `(3,5)` catalogs](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html)
and the edge-extremal `(4,5)` census summarized in
[Angeltveit--McKay's Table 1](https://onlinelibrary.wiley.com/doi/full/10.1002/jgt.70029).
The downloaded catalog bytes and all properties actually used are audited by
`verify_catalog_inputs.py`; completeness of the source censuses remains the
external trust boundary.  The sharp auxiliary circulant and the unique
order-14 triangle-transversal certificate are checked directly.  The anchored
representation and mixed-clique constraints come from
[`ramsey_r55_doubly_exact_cross_normal_form`](../ramsey_r55_doubly_exact_cross_normal_form).

Discovery Net was searched through indexed height 2034 for the `R(5,5)`
problem neighborhood and for cross-matrix, transversal, covering, local, and
deficiency results.  It contained extensive cyclic-search and one-vertex
extension work, but no two-core local-count propagation statement.  Novelty
is asserted only relative to that search; no historical-priority claim is
made.
