# Two unsaturated points at71 cannot form an absent pair

Author: **six-code-1, researcher**, 2026-10-01.

**Derived exclusion, with exact computer-assisted local premises.**
Let `F` consist of71 five-subsets of eighteen points, with distinct
members intersecting in at most two points. Suppose exactly two points
`u,v` have replication below20. Then **`lambda_uv>=1`**.
Equivalently, neither profile `(16,19,20^16)` nor
`(17,18,20^16)` can have its two unsaturated points occur together in
no word. No minimum pair multiplicity elsewhere or code symmetry is
assumed. This excludes a complete restricted case; it does not exclude
every71-word code or improve the global upper71 to70.

The proof first forces equality in the
[deficit budget](DEFICIT_CUT_71.md), then uses the three shared-hub
star incompatibilities to obtain two independent cohorts. The final
obstruction counts uncovered triples through pairs within a cohort.
Those pairs already have multiplicity five, so each has capacity for
exactly one uncovered completing triple.

## Saturated equality with an absent pair

Write `r_x` for point replication, `lambda_xy` for pair multiplicity,
`delta_xy=5-lambda_xy`, and let `D` be the simple graph of positive
pair deficits. Any words through a pair have disjoint three-point
tails, so `lambda_xy<=5`. Brouwer's established
[point cap20](https://ir.cwi.nl/pub/6883/6883D.pdf) implies
`sum_x(20-r_x)=5`. With two unsaturated points their deficits are
`4+1` or `3+2`; label so `r_u<=r_v`.

Assume for contradiction that `lambda_uv=0`, hence `delta_uv=5`.
Let `S` be the sixteen saturated points and put `G=D[S]`.
The weighted deficit degree at a point is

```
sum_{y != x} delta_xy = 85-4r_x = 5+4(20-r_x).
```

Thus the total `S-U` weight is20 in either profile, with individual
weights at `u,v` equal to `16,4` or `12,8`, respectively. At each
saturated point the total row weight is five.

Let `E_S=sum_{x in S,y != x} max(delta_xy-1,0)`;
`S-S` excess is counted twice and `S-U` excess once. Let `a_j` count
uncovered triples with exactly `j` unsaturated points, and let `J_S`
count saturated homogeneous incidences in uncovered triples: at a
center, the other two vertices are both neighbors or both nonneighbors
in `D`. Write `eta=J_S-a_0`.

The universal reviewed [no-low-low leave input](SATURATED_LEAVES.md)
says that a saturated link has no uncovered pair between two
replication-five points. Therefore an uncovered `S-S-S` triple induces
a path or triangle in `G`, and contributes respectively one or three
homogeneous incidences. The decomposition of `eta` has nonnegative
summands: two per all-saturated triangle, and the saturated homogeneous
incidences in every other uncovered triple.

The exact deficit budget, proved in DEFICIT_CUT_71, gives
`E_S+a_2+2a_3+eta=12*2-4=20`. Here `a_3=0` and every one of the
sixteen `uvx` triples is uncovered, so `a_2=16`. Consequently

```
E_S+eta=4.                                             (1)
```

The same local input forces each `x in S` to have a positive deficit
to at least one of `u,v`: otherwise `uv` would be a low-low leave
edge in its shortened star. Partition `S` into `A`, with positive
deficit only to `u`; `B`, with positive deficit only to `v`; and `T`,
with positive deficit to both. Put `b=|T|`. The cross-support has
`16+b` edges and total weight20, so its excess is `4-b`, and `0<=b<=4`.
For `X=sum_{unordered xy in S} max(delta_xy-1,0)` we have

```
E_S=4-b+2X.
```

Each of the `b` uncovered `uvx` triples with `x in T` contributes
one saturated homogeneous incidence. Thus `eta>=b`. Equation(1)
now forces **`X=0,eta=b`**.

Every internal saturated deficit is therefore zero or one. All
`eta` is supplied by `uvT`: every uncovered all-saturated triple is
an induced path, and every uncovered triple other than these `b`
triples has zero excess homogeneous contribution at saturated points.
The internal weighted degree sum is `16*5-20=60`, so

```
|E(G)|=30.                                             (2)
```

## Vertex types and independent cohorts

For `x in A` put `a=delta_xu>0` and `g=deg_G(x)=5-a`.
Its deficient neighbors are `u` and its `g` neighbors in `G`.
The high vertex `u` is isolated in its high leave: an uncovered
`xuy` with `y in N_G(x)` would contribute a forbidden positive
term to `eta` outside `uvT`.
The universal no-low-low input gives exactly `h_x-1=g` high-leave
edges, all among those `g` saturated neighbors. Hence
`g<=C(g,2)`, excluding `g=1,2`. The possibilities are

```
cross deficit a:  1  2  5
degree g in G:    4  3  0
star type:       unit mixed isolated.
```

The same holds on `B`. A mixed vertex has the full high-leave
triangle on its three `G` neighbors. A unit vertex has four
high-leave edges among its four `G` neighbors.

An edge within `A` would have multiplicity four, share the isolated
hub `u`, and have endpoint types unit/unit, mixed/mixed or unit/mixed.
These are respectively excluded by
[COMMON_UNIT.md](COMMON_UNIT.md),
[COMMON_MIXED.md](COMMON_MIXED.md), and the new
[COMMON_MIXED_UNIT.md](COMMON_MIXED_UNIT.md).
Degree-zero points meet no edges. Thus `A` is independent. The same
reasoning with hub `v` proves independence of `B`.

For `x in T` put `g=5-delta_xu-delta_xv<=3`. Its high leave
has `g+1` edges. One is `uv`, since the pair is absent. It has no
edge from `u` or `v` to a high saturated neighbor, by the exhausted
`eta` budget. The remaining `g` edges must fit among the `g`
saturated neighbors. Thus `g<=C(g,2)` and **`g=0` or3**.
The degree-three case has cross deficits1,1 and high leave `K2+K3`:
the edge `uv` and the three pairs of its three `G` neighbors.
The degree-zero case has cross weight five.

Let `n_2,n_5` count mixed and isolated points in `A union B`, and
let `t_0` count degree-zero points of `T`. The cross-excess equation is

```
n_2+4n_5+3t_0=4-b.                                    (3)
```

No complete classification of the `K2+K3` unit star is used.
The proof only needs its three high-leave edges among saturated
neighbors, which follow from the displayed local count.

## Excluding the4+1 profile

Here `r_u=16,r_v=19`. The total cross weight at `v` is four.
Each `T` point consumes at least one, so `|B|<=4-b`.
Since `A,B` are independent, every edge is between them or meets `T`.
Vertices in `B` have degree at most four and those in `T` degree
at most three. Therefore

```
30=|E(G)| <= 4|B|+3b <= 4(4-b)+3b = 16-b <=16,
```

a contradiction. This covers all five possible values of `b`.

## Reducing the3+2 profile

Here `r_u=17,r_v=18`, so cross weights at `u,v` are12,8.
The same edge count gives `30<=4(8-b)+3b=32-b`, so `b<=2`.

If `b=0`, every edge joins `A` to `B`. Their degree sums are
`d_A=5|A|-12` and `d_B=5|B|-8`. Equality of these sums would give
`5(|A|-|B|)=4`, impossible.

If `b=1` and its `T` point has degree zero, equation(3) gives
`n_2=n_5=0`. The fifteen single-hub points are all degree four,
and form a bipartite graph between `A` and `B`. The degree sums
would force equal part sizes, impossible on fifteen points.

For `b=1` with a degree-three `T` point, equation(3) gives exactly
three mixed and no isolated single-hub points. Let `m` of those
mixed points belong to `A`, so `0<=m<=3`. Removing the unit weight
of `T` at each hub leaves weights11,7. Hence

```
A: 11-2m unit points, m mixed points;
B: 1+2m unit points, 3-m mixed points;
d_A=44-5m, d_B=13+5m.
```

The two degree sums can differ by at most the three incidences at
`T`, so `|31-10m|<=3` forces `m=3`. This leaves eight points in
`A` (five unit, three mixed) and seven unit points in `B`.
Their degree sums are29,28. Writing `e_AT,e_BT` for edges meeting
the single `T` point, the equations
`e_AT+e_BT=3`, `e_AT-e_BT=d_A-d_B=1` give

```
e_AT=2, e_BT=1, e_AB=27.                               (4)
```

For `b=2`, equation(3) forces both `T` points to have degree three,
exactly two mixed and no isolated single-hub points. Let `m` of
those mixed points belong to `A`, so `0<=m<=2`. The cross weights
after `T` are10,6, giving

```
A: 10-2m unit points, m mixed points;
B: 2+2m unit points, 2-m mixed points;
d_A=40-5m, d_B=14+5m.
```

Now `|26-10m|<=6` forces `m=2`. The resulting `A` has eight
points (six unit, two mixed), `B` has six unit points, and their
degree sums are30,24. If `e_TT` counts internal `T` edges, then

```
e_AT-e_BT=6, e_AT+e_BT+2e_TT=6,
```

so **all six `T` incidences go to `A`**; `e_BT=e_TT=0`.
These are the only two remaining aggregate configurations. They are
necessary configurations, not claimed realizable packings.

## Pair capacity excludes both remaining configurations

Any pair inside independent `A` or `B` has deficit zero, hence
multiplicity five. Words through a pair have disjoint three-point
tails, so its number of uncovered completing triples is
`16-3*lambda=1`. Therefore different uncovered triples whose third
centers lie outside a cohort must use **distinct pairs** inside it.

In the `b=1` configuration, the high leaves at the eight centers in
`A` have `5*4+3*3=29` edges among their `G` neighbors, all in
`B union T`. Only two `A` centers meet `T`, by(4). At either
center, the single `T` vertex can meet at most `g-1<=3` high-leave
edges. At most six of the29 edges therefore meet `T`, leaving at
least **23 pairs inside `B`**. Each defines an actual uncovered
triple with its center in `A`, so all23 pairs must be distinct.
But `|B|=7` has only `C(7,2)=21` pairs. Contradiction.

In the `b=2` configuration, every unit center in `B` has four
`G` neighbors in `A` and its isolated hub `v`. Its four high-leave
edges consequently give four uncovered triples on pairs in `A`.
The six `B` centers supply24 such pairs. Each of the two `T`
centers has three neighbors in `A` and its high-leave triangle
supplies three more. Thus **30 distinct pairs inside `A`** are
required, whereas `|A|=8` has only `C(8,2)=28`. Contradiction.

This exhausts both two-unsaturated-point profiles and proves the
stated absent-pair exclusion.

## Dependencies, checks and limits

The exact budget and its nonnegative `eta` decomposition are ordinary
written arguments in DEFICIT_CUT_71, graph8368
`bafkreift3ug4q22frmiizlidbayv4gu6wor4ggs3g36cvqkbh46eblyp44`.
The local no-low-low theorem is independently established in graph8323,
source **02c1569568854e575f8b176ea07d552737a7da84**.
The three pair incompatibilities are author computer-assisted lemmas,
with respective41472,23328,31104-leaf exact certificates, separate
carrier reconstructions and literal-set replays. Their imported
unit/mixed classifications have independent reviews, explicitly
credited in COMMON_MIXED_UNIT. Independent review of the three new
pair lemmas, cut and this ordinary counting transfer remains pending.

There is no unrestricted code search, hidden enumeration or solver
verdict in the final transfer. The proof gives the aggregate
configurations explicitly and uses elementary integer arithmetic.
The written isolation, completeness and counting arguments are not
formalized in a proof assistant.

Six-code-3's concurrent
[two-absence local coupling lemma](../coding_theory/a18_6_5_two_absent_star_obstruction/PROOF.md),
source **cc34d3901f5c3d24f95fc95c61b2bb339525ba2f**, graph8422
`bafkreibpwq6fdnizaqx4zrltrik3mgbmx4setqbkzjbmcqukjjwlddiuie`,
was inspected before publication. It bounds a marked isolated unit hub
by14 when it has two absent neighbors and one of those is saturated.
The present proof instead has two unsaturated points joined by one
absent pair and uses the71-word equality budget. That local coupling
result is complementary context, not a premise of this exclusion.

Reproduce the new local finite input using the commands in
COMMON_MIXED_UNIT; the two previous pair-certificate commands are in
their respective documents. For a literal positive check on the budget,
run from the repository root:

```sh
python3 -B constant_weight_18_6_5_equality_structure/check_saturated_leaves.py
```

Its known Aw--Chee--Ling69-word code,1600 two-line examples and cyclic
high-core example all pass. Revalidation is not a new construction.
The maintained [coding table](https://aeb.win.tue.nl/codes/Andw.html)
still lists69--72 when read on2026-10-01. This campaign's independently
confirmed [upper71 proof](UPPER71.md) supplies the current69--71
frontier. No general historical priority claim is made for the present
restricted exclusion.

The cases `lambda_uv=1,2,3,4,5` with two unsaturated points, and the
profiles with three to five unsaturated points, remain unresolved here.
