# Every anchor in necklaces with short inner arcs

Every branch and either outer parent can be prescribed in a two-geodesic
separator of a necklace whose inner arc totals are **at most** the common
wheel/cross-edge length. There are at least three branches, arbitrary
positive subdivisions, and arbitrary nonnegative vertex masses. The
metric antipode of the chosen branch may lie anywhere inside an arc.

Together with the [previous necklace theorem](../planar_two_geodesic_metric_necklaces/README.md),
this gives the prescribed-anchor bound for **every positive common inner
arc total** on necklaces with at least four branches. No restriction on
the ratio of that total to the wheel-edge length remains in this corollary.

The new step splits the antipodal arc between an anchor path and a root
path. Comparing that pair with a carrier pair gives disjoint potentially
heavy supports. This is a conditional structural result bearing on
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
It does not resolve the unrestricted planar question. The unit-edge
existence cases covered by the earlier mixed-annulus theorem are not new
cases. Independent review of this extension is pending.

## Statement

Let t>=3. A core H has root r, the outer cycle

```
a_0,b_0,a_1,b_1,...,a_(t-1),b_(t-1),a_0,
```

all root-to-outer spokes, and branches c_0,...,c_(t-1). The outer
neighbors of c_j are exactly a_j,b_j. Inner paths T_j join c_j to
c_(j+1), with mutually disjoint degree-two interiors. Indices are cyclic.
Thus the incidence word is `(AD)^t`. Every root, outer and cross edge
has common length lambda>0. Each individual inner edge is positive, and
the total ell_j of each T_j satisfies

```
0 < ell_j <= lambda.                                    (1)
```

A finite connected simple positive-edge graph G contains H induced and
isometrically. Every component K of G-V(H), including zero-mass ones,
has boundary contained in `{r}`, `{r,u}`, or `{r,u,v}` for consecutive
outer vertices u,v. There are no inner attachments. Full-G planarity is
not needed for the conditional statement; H is planar by construction.

Choose any branch and either parent. By rotation and reflection write
the chosen triple as S0={r,a_0,c_0}. For nonnegative real vertex masses
of total W, put

```
Y(K) = N(K) intersect the outer vertices;
D0 = sum w(K) for Y(K) empty or {a_0};
B = max_K w(K), with default zero;
M = W-w(S0)-D0,          h=max{M/2,B}.
```

**Quantitative theorem.** There are at most two shortest paths in the
original G whose union contains S0 and leaves every component of mass
at most h. No maximum-sector selection or treewidth hypothesis is needed
for this bound. The triple is contained collectively; the path
P=(r,a_0,c_0) need not remain one entire selected path.

**Half-balance corollary.** If every induced attachment torso
G[K union N(K)] has treewidth at most three, every nonnegative real
vertex weighting has a separator equal to the union of at most two
original-G geodesics, leaving each component of mass at most W/2. A
heavy-attachment replacement may change the prescribed anchor.

**Arbitrary common-total corollary.** Suppose t>=4 and all inner paths
have one common total rho>0, with arbitrary positive edge divisions on
each path. The same quantitative theorem and half-balance corollary
hold for every branch/either-parent anchor and every ratio rho/lambda>0.
For rho<=lambda use this theorem; for rho>=lambda use the previous
necklace theorem. This does not cover every mixture of totals below and
above lambda.

## Distances in the short-arc region

Write delta(c_i,c_j) for distance on the intrinsic weighted inner cycle.
That cycle need not be isometric in H. The outer wheel is isometric:
an excursion between outer vertices through the inner cycle uses two
cross edges and costs at least 2lambda, at least their wheel distance.
For every i,j,

```
d(r,c_j)=2lambda;
d(c_i,a_j)=d(c_i,b_j)=lambda+min{delta(c_i,c_j),2lambda}.  (2)
```

For the second assertion, consider the first cross exit from an inner
route starting at c_i. Later inner excursions can be replaced by wheel
paths of no greater length. Exiting at c_j gives delta(c_i,c_j)+lambda.
An exit at the neighboring branch relevant to a_j or b_j costs
delta(c_i,c_h)+2lambda. By (1) and the triangle inequality,
delta(c_i,c_j)<=delta(c_i,c_h)+lambda, so that exit gives no improvement.
All other exits cost at least 3lambda. An inner shortest route followed
by a cross edge attains the first bound; a route through r attains the
3lambda bound whenever it is the smaller one. Coincident and neighboring
branches already have smaller inner bounds. This proves (2). The first
assertion follows from one cross edge and one root edge. Core isometry
transfers all distances to G.

Let L_cyc=sum ell_j and delta_j=delta(c_0,c_j). Then
`|delta_(j+1)-delta_j|<=ell_j`. Also, by symmetry of (2),

```
d(a_0,c_j)=lambda+min{delta_j,2lambda}.
d(b_j,c_(j+1))=d(a_(j+1),c_j)
             =lambda+min{ell_j,L_cyc-ell_j}.              (3)
```

In (3), the minimum is at most lambda. Thus the other parent's cross
edge followed by the whole T_j is shortest whenever
ell_j<=L_cyc-ell_j. This always holds if
`|delta_(j+1)-delta_j|=ell_j`: use the triangle inequality in the cycle.
It also holds if either delta_j or delta_(j+1) is at least 2lambda.
Otherwise ell_j>L_cyc-ell_j would put both endpoint distances from c_0
below L_cyc-ell_j<ell_j<=lambda, a contradiction.

For an arc T=(v_0=c,...,v_n=d), use coordinates
`0=z_0<...<z_n=ell`. There are no entries to its interior except c,d.
A shortest path from u to c, avoiding the arc interior, extends
geodesically to v_p exactly when

```
d(u,c)+z_p <= d(u,d)+ell-z_p.                            (4)
```

The analogous reversed inequality controls a suffix. These tests use
non-strict inequalities and allow arbitrary real edge lengths and gaps
between consecutive vertex coordinates.

## Sweep and the mass partition

Let o_(2j)=a_j and o_(2j+1)=b_j. After deleting S0, every K counted in
D0 detaches individually, with mass at most B. Partition the represented
vertices of mass M into the following disjoint groups:

```
alpha_i: o_i and all K with Y(K)={o_i}, for i!=0;
gamma_j: {c_j}, for j!=0;
kappa_i: all K with Y(K)={o_i,o_(i+1)};
tau_j: the interior of T_j.
```

The groups alpha_0 and gamma_0 are empty. At the end of the unrolled
sweep their indices wrap to these empty groups. At state (i,j), define
L(i,j) as the union of alpha_h,kappa_h for h<i and gamma_h,tau_h for
h<j. Let R(i,j) be the represented complement minus alpha_i,gamma_j.

Delete P and the spoke (r,o_i,c_j). Both are geodesics by (2). Every
component meeting H lies in L(i,j) or R(i,j); every other component is
one whole K. To see this, cut the outer and inner cycles at the removed
sites. Cross edges join each branch only to its two consecutive parents,
so they stay in the matching intervals. A K cannot bridge intervals:
its outer sites are at most two consecutive vertices. If all its sites
are removed, it detaches as one whole component. Extra core deletions
only split components. The same interval argument will be used below.

Move through A-steps `(a_j,c_j)->(b_j,c_j)` and D-steps
`(b_j,c_j)->(a_(j+1),c_(j+1))`. The mass of L increases and that of R
decreases from (0,M) to (M,0), with `w(L)+w(R)<=M<=2h`. If a spoke
pair has both sides light, it works. Otherwise take the first transition
whose new L is heavier than h. Its old R is heavy as well; its old L
and new R are light. In the rest of the proof, L and R denote those
old and new light sides at this transition.

For an A-step, deleting S0,a_j,b_j,c_j puts all core components inside
L or R. For a D-step, writing i=2j+1, deleting S0, both outer sites,
and the old branch puts them inside

```
L,              R union gamma_(j+1) union tau_j.          (5)
```

Deleting the new branch instead gives

```
L union gamma_j union tau_j,              R.             (6)
```

Deleting S0, the whole arc including both branches, and only the new
outer site gives

```
L union alpha_i union kappa_i,            R;             (7)
```

deleting only the old outer site instead gives

```
L,              R union alpha_(i+1) union kappa_i.        (8)
```

These are upper bounds, so any additional vertices removed by a path
only help. They include the first and closing D-steps, with the empty
seam groups. Detached K are always bounded individually by B. For
example, kappa_i detaches when both outer sites are removed; when just
one survives it stays on that site's indicated side.

## A-steps and ordinary D-steps

Let I_j be an intrinsic inner shortest route from c_0 to c_j. When
delta_j<=2lambda, I_j followed by either parent is a geodesic by (2).
An A-step has these two paths:

| Case | Pair |
|---|---|
| j=0 | `(r,a_0)` and `(c_0,b_0)` |
| j>0, delta_j<2lambda | I_j followed by b_j, and `(a_0,r,a_j)` |
| delta_j>=2lambda | `(c_0,a_0,r,b_j)` and `(a_j,c_j)` |

The wheel route from a_0 to a_j for j>0 has length 2lambda and is
shortest. In the last row the carrier is shortest by (2); the adjacent
exception b_(t-1) cannot occur because delta_(t-1)<=ell_(t-1)<=lambda.
Every pair contains S0 and removes both parents and their branch, so
the light L,R bounds prove every A-step.

For a D-step across T_j, first suppose one endpoint has delta at least
2lambda. Use the root carrier to its corresponding outer site and the
other outer site's cross edge followed by the whole T_j. Both are
geodesic by (2),(3). The pair removes both outer sites, both branches
and the entire arc, leaving only the light L,R and individual K.

Now suppose both endpoint deltas are below 2lambda and their difference
has absolute value ell_j. If delta_(j+1)=delta_j+ell_j, an inner shortest
route through c_j,T_j,c_(j+1), followed by a_(j+1), is geodesic; pair it
with `(a_0,r,b_j)`. If delta_j=delta_(j+1)+ell_j, use the reversed
inner route through c_(j+1),T_j,c_j, followed by b_j, and pair it with
`(a_0,r,a_(j+1))`. In these rows the route is chosen through the named
arc even if there is a tie. The first and closing D-steps have simpler
pairs that avoid an adjacent-wheel detour:

```
j=0:    (b_0,c_0,whole T_0 to c_1),    (a_0,r,a_1);
j=t-1:  (r,a_0),    (c_0,whole reversed T_(t-1),b_(t-1)).
```

These seam pairs apply here only when the step is monotone in delta.
They are geodesic by (2),(3). All the displayed pairs remove the whole
current arc and both outer sites; they give the light L,R bounds.

The only remaining case is an arc containing the metric antipode of c_0
strictly in its interior, with both endpoint deltas below 2lambda. If
the antipode is itself a branch, there is no such remaining step.

## The antipodal arc: split it between the two paths

Let the remaining arc be T_j=(v_0=c_j,...,v_n=c_(j+1)), of length ell.
Put x=delta_j and y=delta_(j+1). The forward inner route F from c_0 to
c_j and the reverse inner route Q from c_0 to c_(j+1) have lengths x,y.
Neither uses this arc, and

```
x+ell+y=L_cyc,       |x-y|<ell,       max(x,y)<2lambda.
theta=ell+y-x lies strictly between 0 and 2ell.          (9)
```

By (3),(4), a path starting `(a_0,c_0)` and following F can extend along
T_j through precisely those prefix vertices with `2z_p<=theta`.
Starting at a_0 and following Q in the other direction gives suffix
vertices with `2z_q>=theta`. A root-to-branch path can extend through
a prefix with `2z_p<=ell`, or a suffix with `2z_q>=ell`, because both
branch endpoints have root distance 2lambda.

**Case x<=y.** Consider first the carrier pair

```
F followed by b_j,               (a_0,r,a_(j+1)).        (10)
```

Its paths are shortest and its only possibly heavy core support is
`H1=R union gamma_(j+1) union tau_j`, by (5). The closing step cannot
occur in this case, since there y=0<x; hence the wheel route in (10)
is indeed shortest. All other core components are in the light L.

Choose p last with `2z_p<=theta` and q first with `2z_q>=ell`. Since
theta>=ell, q<=p+1. The split pair is

```
a_0, then F, then v_1,...,v_p;
r,a_(j+1),c_(j+1),v_(n-1),...,v_q.                     (11)
```

Both paths are shortest by (9) and the preceding extension tests. Their
union contains every vertex of the current arc. It contains S0 and the
new outer site, so (7) bounds its only possibly heavy support by
`H2=L union alpha_i union kappa_i`. Its other core components are in R.
H1,H2 are disjoint subsets of the represented mass M. Since M<=2h,
they cannot both have mass greater than h. Thus either (10) or (11)
works, including any whole detached K.

**Case x>y.** Reflect the choice of carrier. Use

```
Q followed by a_(j+1),           (a_0,r,b_j),             (12)
```

except at j=t-1, replace the second path by `(r,b_(t-1))`: the first
already contains a_0. At j=0 we have x=0<y, so the other adjacent-wheel
exception cannot occur. These are geodesics. Their only possibly heavy
support is `H1=L union gamma_j union tau_j`, as in (6).

Choose q first with `2z_q>=theta` and p last with `2z_p<=ell`. Now
theta<ell and again q<=p+1. Use the split pair

```
a_0, then Q, then v_(n-1),...,v_q;
r,b_j,c_j,v_1,...,v_p.                                  (13)
```

It consists of geodesics, covers S0 and the whole arc, and has its only
possibly heavy support inside `H2=R union alpha_(i+1) union kappa_i`,
by (8). This H2 is disjoint from H1; one of (12),(13) therefore works.

The descriptions of F,Q already include their initial c_0 and final
branch; repeated junction vertices are written only once in (11),(13).
The coordinate choices also cover ties, a degree-two vertex at the
antipode, an antipode strictly inside one edge, and an arc longer than
the rest of the inner cycle combined. No assumption that the whole
antipodal arc itself is geodesic was used. This completes the sweep and
the quantitative proof.

## Heavy attachments

If B<=W/2, then h<=W/2 and the quantitative theorem suffices. Otherwise
there is a unique heavy K. Its boundary is a clique of size at most
three, hence occurs in a bag of a width-three torso decomposition.
Attach an outside leaf bag V(G)-K at that bag. Assign outside mass to
the leaf and K's mass to local bags. A weighted centroid cannot be the
outside leaf, whose only branch contains more than half the mass.
Its local bag has at most four vertices and half-separates G. Pair its
vertices and choose at most two ambient geodesics covering the bag;
deleting more vertices only shrinks components. This is the existing
[reviewed heavy-attachment reduction](../planar_two_geodesic_prescribed_attachment_review1/REVIEW.md).
It proves the half-balance corollary, while allowing the anchor to change.

## Literal controls and scope

Take t=3, lambda=4, and one singleton K_i in each root triangle
`r,o_i,o_(i+1)`. Give K_1,K_5 mass three each, one specified inner
vertex mass four, and every other vertex mass zero. Total mass is ten,
the bound h is five, and the anchor is {r,a_0,c_0}.

| Control | Inner edge lengths | Mass-four vertex | Carrier residual | Split residual |
|---|---|---|---|---|
| x=y | T_0=(2), T_1=(1,1), T_2=(2) | v_1 in T_1 | 7 | 3 |
| x>y | T_0=(3), T_1=(1,1,1), T_2=(2) | v_1 in T_1 | 7 | 3 |

For the first row, the split pair is `(a_0,c_0,c_1,v_1)` and
`(r,a_2,c_2,v_1)`. For the second it is
`(a_0,c_0,c_2,v_2,v_1)` and `(r,b_1,c_1,v_1)`. These exact full-component
checks show why the additional pair matters; they are positive examples,
not counterexamples to two-geodesic separation.

A separate method control uses totals (3,1,1), with T_0 divided (1,1,1).
The whole-arc path b_0,c_0,T_0,c_1 has length seven, while
b_0,c_0,c_2,c_1 has length six. Thus blindly using the whole antipodal
arc fails. The split proof handles it. The closing wheel route
a_0,r,b_(t-1) is also correctly rejected: its endpoints are adjacent.

This theorem covers all short totals, not only symmetric or equal ones,
and it covers t=3. Its common-total corollary uses t>=4 because the
previous long-total result has that restriction. Subdivisions of outer
or cross edges carrying new mass and arbitrary mixtures straddling
lambda are outside the stated conclusions. No separation from every
known sufficient graph class or historical novelty is claimed.

The [official workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html)
announces a Codsi separator-conjecture disproof. Its exact statement and
witness remain unmatched in our bounded primary-source audit, refreshed
29 September 2026. No author was contacted. Neither continued openness
nor historical priority follows from the posted problem list or the
targeted searches.

## Reproduction and trust boundary

From the repository root, Python 3.11+ with the standard library and
assertions enabled (recorded version 3.11.2):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_short_necklaces/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_short_necklaces/audit.py
```

The main result matches [expected.json](expected.json). Eight attachment
fixtures have 74 anchor orientations; 60 further seeded core metrics
have two tested orientations each (`2026092921`). Exact Fraction
arithmetic checks ambient shortestness, all stated component bounds,
disjoint supports, core isometry, spherical rotations, local torso
decompositions and actual residual masses. It imports prior graph,
mass-choice and heavy-torso helpers. Recorded totals are 194 systems,
5,132 component cuts and 17,136 quantitative mass checks, including
6,778 heavy repairs and 10,358 light-half checks. All four antipodal
carrier/split choices occur in the mass tests. These are finite controls,
not distinct-graph counts or an exhaustive census of metrics and masses.

The separate [audit.py](audit.py) imports no research code. It constructs
named graphs with singleton cap attachments and computes integer Floyd
distances. For 240 oriented models with t=3 through 8 (`2026092922`),
it exhausts endpoints in the local candidate bank, filters paths by
direct shortestness, and derives the possibly heavy supports from actual
components. It then checks for one empty support or two disjoint supports.
It uses no production coordinate-threshold formula. This supplies
definition-level checks of 2,640 A/D steps, including 122 requiring two
candidates in that bank. The literal controls are checked separately.
Expected output:

```json
{
  "A_steps": 1320,
  "D_steps": 1320,
  "closing_wheel_detour_failure": 1,
  "dominant_arc_old_path_failure": 1,
  "left_control_old_residual": 7,
  "left_control_split_residual": 3,
  "models": 240,
  "right_control_old_residual": 7,
  "right_control_split_residual": 3,
  "single_pair_steps": 2518,
  "two_pair_steps": 122,
  "valid_path_pairs": 5330
}
```

The final line is `PASS`. This is a separate implementation by the same
researcher, not independent peer review. The arbitrary-order, real-metric
and real-mass statements rest on the written proof, not finite enumeration.
No proof assistant, solver, external dataset or omitted large artifact
is required. The common-total corollary additionally depends on the
previous necklace proof in the complementary region.
