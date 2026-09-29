# Exact-half separators in metric C/D annuli

A capped annulus whose inner branch vertices each have one outer
neighbor admits a two-geodesic half separator for a broad class of
positive edge metrics. The outer wheel and the cross edges may have
arbitrary positive lengths. Each inner arc must dominate the wheel
distance between its parents plus the difference of its cross lengths.
Its individual edge lengths and subdivision count are otherwise free.

The proof replaces the earlier four-cut identity by two pairs of paths.
Each pair deletes both outer endpoints of a quadrilateral. Their two
potentially heavy regions have disjoint supports. A shortest path through
the outer wheel carries two distinguished anchor vertices, and the other
path supplies the root when necessary.

This is a structural result bearing on
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf),
not an unrestricted resolution. It is a metric extension on a specified
subclass of the [unit mixed-annulus theorem](../planar_two_geodesic_subdivided_mixed_annuli/README.md).
The present extension awaits independent review. The official
[schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html)
announces a disproof of a Codsi separator conjecture, but the exact
statement and witness have not been matched to Problem 31 in our narrow
primary-source check, refreshed 28 September 2026. We make no assertion
of continued openness or historical priority.

## Graphs, metrics and statements

Let `W0` be a wheel with root `r`, outer cycle
`a_0,...,a_(k-1)`, and every root-to-outer edge, where `k>=3`.
Give its edges arbitrary positive lengths; write `d0` for its distance
function. An outer edge need not itself be shortest.

Take a cyclic word in `C,D` with exactly `k` letters `D` and `m` letters
in total. There are inner branch vertices `c_0,...,c_(m-1)`. Starting
at `(i,j)=(0,0)`, give `c_j` the unique outer parent `a_i`, and advance
by `(0,1)` at `C` or by `(1,1)` at `D`, with cyclic indices. Denote the
parent map by `phi`. Add just the cross edge `c_j phi(c_j)`, of arbitrary
positive length `s_j`. Thus C-faces are inner fans and D-faces are
genuine quadrilaterals before subdivision; there are no A-faces.

Join successive branch vertices by internally disjoint paths `T_j`
with positive individual edge lengths and total length `ell_j`. Impose

```
ell_j >= d0(phi(c_j),phi(c_(j+1))) + |s_j-s_(j+1)|.        (1)
```

All subdivision interiors have degree two in this core `H`. The word
construction is simple and planar: its cross edges occur in cyclic
order, each branch has one parent, and each outer vertex has a nonempty
consecutive block of inner neighbors. No extra wrap bounds are needed.

Let a finite connected simple positive-edge graph `G` contain `H`
isometrically, with no additional edges between vertices of `H`. Every
component `K` of `G-V(H)`, including every zero-mass one, has boundary
`N(K)` contained in one of

```
{r}, {r,a_i}, {r,a_i,a_(i+1)}.
```

In particular, no attachment meets an inner vertex. The boundary is a
clique as an unweighted graph; its edges need not be geodesic. Edges
outside H may have arbitrary positive lengths preserving its isometry.
For example, it suffices that each such edge have length at least half
the largest wheel distance between a pair of boundary vertices.

Choose any inner branch as `c_0` and relabel its parent as `a_0`. For
nonnegative real vertex masses of total `W`, define

```
S0 = {r,a_0,c_0};
Y(K) = N(K) intersect {a_i};
D0 = sum of w(K) over Y(K) empty or {a_0};
B = max_K w(K), with default 0;
M = W-w(S0)-D0.
```

**Quantitative theorem.** Two ambient geodesics have a union containing
`S0` such that every remaining component has mass at most

```
h = max{M/2,B}.                                         (2)
```

No local treewidth hypothesis is needed for (2). The preserved object
is the distinguished triple S0. The two paths may repartition that
triple, and need not contain every vertex of a selected root geodesic.
The edge sequence `(r,a_0,c_0)` need not itself be shortest in these
metrics.

**All-mass corollary.** If each induced local torso `G[K union N(K)]`
has treewidth at most three, then every nonnegative vertex weighting
admits a separator equal to the union of at most two original-G shortest
paths, with every remaining component of mass at most `W/2`.

The unit-edge planar members are partial cases of Problem 31. Planarity
of the whole G is unnecessary under the stated structural hypotheses.
We do not claim that arbitrary edge subdivisions on the outer wheel or
cross edges preserve this theorem: new vertices there would need their
own mass and component argument.

## Why the distance calculation is exact

Suppress the degree-two interiors of the inner arcs, retaining their
total lengths. Project a branch `c` to `phi(c)`, fix the wheel, and
collapse cross edges. An inner arc can be replaced in the wheel by a
path of length at most its own length, by (1). Consequently every
wheel-to-wheel walk projects to a wheel walk of no greater length, and
`W0` is isometric in H.

More precisely, for every branch c and wheel vertex x,

```
d_H(c,x) = s_c + d0(phi(c),x).                           (3)
```

For the lower bound, follow a path from c until its first exit from the
inner branches at some branch t. The inner portion has length at least
the sum of projected parent distances plus the sum of absolute changes
in s. Adding its exit edge of length `s_t` gives at least
`s_c+d0(phi(c),phi(t))`. The remainder is no shorter than the wheel
distance from `phi(t)` to x. Triangle inequality gives the lower bound
in (3). The cross edge at c followed by a wheel geodesic realizes
equality. Core isometry makes (3) valid in G as well.

Condition (1) is also necessary for (3) on this core: the route from
`c_j` along `T_j` to the opposite parent has length `ell_j+s_(j+1)`;
using (3) bounds it below by `s_j+d0(phi(c_j),phi(c_(j+1)))`.
Reverse the route to obtain the other sign of the absolute value.
This characterizes the displayed distance factorization, not all
metrics admitting a two-path separator.

For each outer a, choose any wheel geodesic from `a_0` to a and prepend
the edge `c_0 a_0`. Call this ambient geodesic `E_a`. It contains
`c_0,a_0`; it may or may not contain r. Also, a wheel geodesic from r
to `phi(c)` followed by its cross edge is an ambient root-to-c geodesic.

If an inner arc T runs from c to d, has length ell, and an internal
vertex v lies at coordinate x from c, its only two entry points are c
and d. Thus a path from a vertex z through c to v is shortest whenever

```
d_G(z,c)+x <= d_G(z,d)+ell-x,                            (4)
```

and likewise from d. All later cut positions use (4), with ties allowed.

## Sweep and component bounds

Discard the attachments counted by D0 from the bookkeeping: deleting
S0 already detaches each of them individually, with mass at most B.
Use the following disjoint groups on the remaining vertices outside S0:

```
alpha_i = {a_i} and the K with Y(K)={a_i}, for i!=0;
gamma_j = {c_j}, for j!=0;
alpha_0=alpha_k=gamma_0=gamma_m=empty;
kappa_i = the K with Y(K)={a_i,a_(i+1)};
tau_j = interior(T_j).
```

We use the same symbol for a group and its mass when no confusion arises.
Their disjoint union has mass M. At each cross state `(i,j)` in the
unrolled word put

```
L(i,j) = union of (alpha_s,kappa_s) for s<i
         and of (gamma_t,tau_t) for t<j;
R(i,j) = represented vertices minus L(i,j), alpha_i, gamma_j.
```

Take the root-to-c_0 path described after (3), and the analogous
root-to-c_j path through a_i. Together they delete at least
`S0 union {r,a_i,c_j}`. Every remaining component meeting the core is
contained in L or R. Indeed, cutting the two cycles at these deleted
vertices separates the two monotone intervals of cross incidences.
An attachment with one active outer vertex, or two consecutive ones,
cannot bridge the cuts. Additional outer vertices on the wheel paths
only reduce the components. A component missing H is a whole K.

The formal L mass increases and the R mass decreases, from `(0,M)` to
`(M,0)`. At each state `L+R<=M<=2h`. If no state already proves (2),
there is a transition whose old R and new L are both greater than h.
Write L for its old, light left side and R for its new, light right
side. It suffices to repair this transition. Total mass zero is included.

## C-step: a common metric threshold

Let c,d have the same parent a, cross lengths s,t, and arc T of length
ell. Let its vertex coordinates be `0=x_0<...<x_n=ell`. Condition (1)
gives `ell>=|s-t|`. Define

```
p = last index with 2*x_p <= ell+t-s;
q = first index with 2*x_q >= ell+t-s.
```

Extend the old root path through the prefix ending at p, or the new root
path backwards through the suffix starting at q; keep the anchor path
as the other path. Formula (3) says the endpoint root distances differ
by `t-s`, so both extensions are shortest by (4). They retain the old
light left side and the new light right side, respectively. Their other
side supports are disjoint: `q<=p+1` means the two extensions collectively
delete the whole arc interior. Both remaining sides cannot exceed h.

## D-step: two pairs, with disjoint heavy supports

Write the step as `(a,c)` to `(b,d)`, let the cross lengths be s,t, and
let T have length ell and coordinates as above. Put

```
delta = d0(a,b);
R_a = d0(r,a), R_b = d0(r,b);
z = ell+t-s+R_b-R_a.
```

The triangle inequality and (1) imply

```
0 <= ell+t-s-delta <= z <= ell+t-s+delta <= 2*ell.         (5)
```

For the first pair, take `E_a`. If it contains r, set
`z_f=ell+t-s-delta` and start the other path at b. Otherwise set `z_f=z`
and start with a wheel geodesic from r to b. In either case append the
cross edge `bd` and the reversed suffix of T starting at the first
index q with `2*x_q>=z_f`. Call this path V.

It is shortest. In the first case its endpoint distances to d,c are
`t,s+delta`, and in the second they are `R_b+t,R_a+s`; (4) gives exactly
the displayed threshold. The pair `(E_a,V)` contains S0 and deletes
both a,b and d. Its components meeting H lie in

```
H_left = L union gamma_c union {v_1,...,v_(q-1)},
R.                                                       (6)
```

The sector attachments at ab detach individually. To see (6), the
remaining c and arc prefix can join only the old left interval. No
branch has an additional outer parent, so it has no incidence into the
right interval. Further deletions along E_a only help. This also covers
seam cases with c or d equal to c_0; its represented gamma group is empty.

Reflect the construction. Take `E_b`. If it contains r, set
`z_b=ell+t-s+delta` and start at a; otherwise set `z_b=z` and start with
a wheel geodesic from r to a. Append `ac` and the prefix of T through
the last index p with `2*x_p<=z_b`. This second pair is shortest by (4),
contains S0, and has component bounds

```
L,
H_right = R union gamma_d union {v_(p+1),...,v_(n-1)}.     (7)
```

By (5), `z_f<=z_b`, hence `q<=p+1`. The supports H_left and H_right
are disjoint subsets of the represented mass M: L and R are disjoint,
the two branch groups are distinct, and the prefix and suffix in (6),(7)
do not overlap. Both supports therefore cannot have mass greater than
`h>=M/2`. The other bound of each pair is already light, and each
detached K has mass at most B. One pair proves (2).

## Heavy attachments and half balance

If every K is light, (2) is at most W/2. Otherwise there is a heavy K.
Its boundary is a clique of order at most three, so some bag in a
width-three decomposition of its torso contains that boundary. Attach
an outside leaf bag `V(G)-K` there. Assign the masses of K locally and
all other masses to that leaf. A weighted centroid cannot be the
outside leaf, whose sole branch has mass `w(K)>W/2`. A local bag of at
most four vertices therefore half-separates the full G. Pair its
vertices and take at most two ambient geodesics covering the bag.
Deleting their entire union preserves balance. This is the
[reviewed heavy-attachment argument](../planar_two_geodesic_prescribed_attachment_review1/REVIEW.md).
No five-vertex bag assertion or global treewidth-four theorem is used.

## What changes relative to the unit proof

The [earlier quadrilateral argument](../planar_two_geodesic_quadrilateral_annuli/README.md)
requires a twofold count of four potentially heavy supports. It can
fail for nonuniform arc positions. The separate audit constructs this
explicit control: the word is `D^5`; wheel and cross lengths are four;
all arcs have one edge of length four except `T_2`, with lengths `3,2,3`.
A singleton attachment is placed in each outer sector, adjacent to its
two endpoints and r by edges of length four. Give mass two to `a_1,a_4`,
mass one to the attachment in sector `a_2 a_3`, and mass one to each
interior vertex of T_2; all other masses are zero. The total is seven.

With anchor `(r,a_0,c_0)`, all four old D-step candidates leave an
actual component of mass four. Each of the two new pairs leaves largest
residual mass two. The script checks shortestness and full components,
not only formal side sums. This refutes that four-candidate repair rule
in the larger metric class; it is not a counterexample to fixed-path
completion in general, or to the two-geodesic separator question.

The same 18-vertex weighted control also checks the prior-art boundary.
After deleting its five attachments and suppressing degree-two arc
interiors, its capped D^5 core has treewidth at least four. In a
width-three elimination, the only possible first vertices are inner
branches. By symmetry remove c_0, filling its three neighbors to a
clique. The only next choices are c_2,c_3, equivalent by reflection;
after either, every remaining vertex has degree at least four. Thus
no width-three elimination is possible. The audit separately explores
all such elimination orders.

Every one of the control's 21 faces leaves a component of mass at least
five, greater than 7/2. Suppressing its two degree-two vertices gives a
3-connected graph, checked by all 137 deletions of at most two vertices.
Whitney's embedding uniqueness theorem, as recalled in
[Georgakopoulos--Kim](https://arxiv.org/abs/2109.04085), and correspondence
of embeddings under subdivision extend the facial check to every
embedding. Thus neither the treewidth-three nor the facial sufficient
mechanism explains this included weighting. This comparison is not a
claim of separation from every known positive class or of priority.

The new theorem covers arbitrary positive wheel and cross prices under
(1), rather than only one common core edge length. It still excludes
A-steps and inner attachments, and assumes core isometry. The unit
mixed-annulus theorem remains broader in incidence. Comparisons here
concern explicit hypotheses, not every possible representation of a
graph or every previously known sufficient class. In particular,
[Diot--Gavoille](https://emilie-diot.eu/Article/DG10a) already provide
strong two-path separators from treewidth at most three or a
half-separating face; neither mechanism is claimed as new here.

## Reproduction and trust boundary

From the repository root, with Python 3.11+ and its standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_metric_cd_annuli/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_metric_cd_annuli/audit.py
```

The first output must match [expected.json](expected.json). It uses
exact `Fraction` arithmetic, six specified attachment fixtures, every
cyclic anchor in each fixture, and 30 additional seeded metric models.
Profiles include zero, uniform and singleton masses, heavy and equality
attachments, arc concentration, and sampled integer profiles. Seed:
`2026092917`. It checks original-graph distances, spherical rotations,
isometry, component containment, local decompositions, and final
residual masses. Counts include 9,092 quantitative checks, 2,437 component
cuts, 2,234 heavy-attachment checks and 6,858 light half-balance checks.
The main checker imports earlier graph and heavy-attachment helpers.

The separate [audit.py](audit.py) imports no research implementation.
It directly constructs every labelled C/D word of length three through
seven with at least three D's, each with one specified integer metric,
and the control above: 164 models. It uses Floyd--Warshall rather than
the main checker’s Dijkstra implementation, and checks all anchors,
projection distances and full components of the two candidate pairs.
This is a finite geometry audit, not a census of all metrics or masses.
Its expected line is:

```text
C_transitions=2775 D_transitions=4102 component_pairs=13754 control_connectivity_checks=137 control_faces=21 control_min_facial_residual=5 control_new_residual=2 control_total_mass=7 control_treewidth_lower_bound=4 models=164 old_candidate_failures=4 projection_distances=5155 projection_failure_control=1 PASS
```

The final control violates (1) and confirms that the prescribed distance
factorization can fail. The universal theorem rests on the written
projection, threshold, component and centroid proofs. Neither script
is a proof assistant or independent peer review; no solver or external
dataset is used.
