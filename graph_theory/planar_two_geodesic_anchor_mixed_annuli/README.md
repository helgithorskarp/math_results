# Two-geodesic half separators in mixed annuli with one metric anchor

One suitable anchor extends the two-pair metric argument to mixed
A/C/D annuli, including long outer fans. The resulting quantitative
bound has no fan-mass term: every individual A-step can be repaired
by two shortest paths that retain the anchor's three vertices. We give
an exact local test for the required anchor, allowing arbitrary positive
edge lengths along the inner arcs.

This is a structural result related to
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).
Its unit-edge specialization strengthens the prescribed-triple bound
on the eligible subclass of the earlier
[mixed-annulus result](../planar_two_geodesic_subdivided_mixed_annuli/README.md);
it does not establish a new unrestricted planar half-separator theorem.
The present extension awaits independent review. The official
[schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html)
announces a disproof of a Codsi separator conjecture. Our narrow
primary-source check, refreshed 29 September 2026, has not verified
that talk's exact statement or witness. We assert neither continued
openness of Problem 31 nor historical priority.

## Core, attachments and anchor

Let a cyclic word use steps `A=(1,0)`, `C=(0,1)`, `D=(1,1)`.
Write `k=#A+#D` and `m=#C+#D`. Require `k,m>=3`, every cyclic
pure A-run to have length at most `k-2`, and every cyclic pure C-run
to have length at most `m-2`.

Construct a capped annulus H with root r, outer cycle
`a_0,...,a_(k-1)`, inner branch cycle `c_0,...,c_(m-1)`, and all
root-to-outer edges. Starting from a cross state `(i,j)=(0,0)`, add
the cross edge `a_i c_j` at every visited state and advance by the
word's indicated step, with indices cyclic. Each inner cycle edge
is replaced by an internally disjoint path `T_j` from `c_j` to
`c_(j+1)`. All its interior vertices have degree two in H.

Every root, outer-cycle and cross edge has a common length `lambda>0`.
The edges of each inner arc have arbitrary positive lengths, subject
only to its total `ell_j>=lambda`. The cyclic construction is simple
and planar; before inner subdivision its A/C faces are triangles and
its D faces are quadrilaterals. Let W0 be the outer wheel and d0 its
distance function.

Let G be a finite connected simple graph with positive edge lengths
containing H as an induced isometric subgraph. Every component K of
`G-V(H)`, including every zero-mass component, must have boundary
contained in one of

```
{r}, {r,a_i}, {r,a_i,a_(i+1)}.
```

There are no attachments to the inner arcs or branch vertices.
Edges outside H can have any positive lengths preserving isometry.
The whole graph need not be planar under these hypotheses; restricting
to planar unit-edge members gives instances of the named problem.

Choose a cross state, relabel it `(a_0,c_0)`, and require

```
d_G(c_0,a) = lambda + d0(a_0,a) for every outer vertex a.       (1)
```

Here is an equivalent local condition:

* c_0 has exactly one outer neighbor, a_0.
* For each of the two inner arcs incident with c_0 whose total length
  is strictly less than `2*lambda`, all outer neighbors of its other
  branch endpoint belong to `{a_(k-1),a_0,a_1}`.

In particular, a unique outer neighbor and both incident arc totals
at least `2*lambda` suffice. Equality at the length threshold is allowed.
When `k=3`, every outer vertex is in the displayed set, so uniqueness
of the outer neighbor suffices. This condition characterizes (1), not
the existence of half separators in the whole graph.

## Statements

Give the vertices arbitrary nonnegative real masses with total W.
Put

```
P = (r,a_0,c_0),    S0 = {r,a_0,c_0};
Y(K) = N(K) intersect {a_i};
D0 = sum of w(K) over Y(K) empty or {a_0};
B = max_K w(K), with default 0;
M = W-w(S0)-D0.
```

**Quantitative theorem.** Under (1), there are at most two ambient
geodesics whose union contains S0 and leaves every component of mass
at most

```
h = max{M/2,B}.                                             (2)
```

No treewidth hypothesis or upper bound on aggregate fan mass is needed
for (2). In particular, if each individual attachment has mass at most
W/2, the pair half-separates while retaining the chosen triple even
when an entire long fan is heavier than W/2. P is itself geodesic, but
the conclusion preserves its vertices collectively: the pair can
repartition S0, and need not retain P as a whole path.

**All-mass corollary.** If each induced torso `G[K union N(K)]`
has treewidth at most three, every nonnegative vertex weighting admits
a separator equal to the union of at most two original-G shortest paths
with residual components of mass at most W/2. In a heavy-attachment case
the chosen triple need not be preserved. Singleton paths are allowed.

## Metric facts and proof of the local criterion

W0 is isometric in H. Any excursion through the inner part between
two outer vertices uses two cross edges, hence costs at least
`2*lambda`, while their wheel distance is at most `2*lambda`.
Replacing every excursion by a wheel path proves the assertion.
Consequently every inner branch has root distance `2*lambda`.

At a D-step `(a,c)` to `(b,d)`, neither opposite cross edge ad nor bc
exists. The inner neighbors of an outer vertex form one cyclic C-run
interval. An opposite incidence would require at least `m-1`
consecutive C-steps; the stipulated bound excludes it. Since every
inner arc has total at least lambda, the exact distances are

```
d(a,c)=d(b,d)=lambda,    d(a,d)=d(b,c)=2*lambda.             (3)
```

To prove necessity of the local anchor condition, another outer
neighbor of c_0 would have distance lambda, contradicting (1). If an
incident inner arc of total less than `2*lambda` led to a branch
adjacent to a nonneighbor of a_0 on the outer cycle, it would give
a c_0-to-that-vertex route of length less than `3*lambda`, again
contradicting (1).

Conversely, suppose the local condition holds and follow a shortest
path from c_0 to an outer vertex until its first entry into W0.
An exit at c_0 uses its sole cross edge. An exit reached through at
least two whole inner arcs costs at least `3*lambda`, including the
exit edge. The same holds after one arc of total at least `2*lambda`.
The only remaining case uses one shorter arc and exits at a vertex
in `{a_(k-1),a_0,a_1}`. It already costs at least `2*lambda`; reaching
an outer vertex outside that set costs at least lambda more, by wheel
isometry. Thus a_0 has distance lambda, its other outer neighbors
have distance `2*lambda`, and all other outer vertices have distance
`3*lambda`. The routes through a_0 attain these values. This proves
(1) in H, and isometry transfers all these distances to G.

For each outer a_i, use the following explicit geodesic E_i:

```
i=0:                  (c_0,a_0);
i=1 or k-1:           (c_0,a_0,a_i);
all other i:          (c_0,a_0,r,a_i).
```

They contain c_0,a_0. Each follows a shortest a_0-to-a_i route in W0,
so (1) proves shortestness in G. The second path in each repair below
supplies r whenever E_i omits it.

For an arc `T=(v_0=c,...,v_n=d)` of length ell, write
`0=x_0<...<x_n=ell` for its vertex coordinates. Its interior has only
two possible entry points. If a shortest z-to-c path followed by
the prefix ends at v_t, this extension is geodesic when

```
d_G(z,c)+x_t <= d_G(z,d)+ell-x_t.                         (4)
```

The reverse inequality certifies entry through d. In using (4) we
first argue within H; its isometry transfers the result to G.

## Sweep and component bookkeeping

Deleting S0 detaches each K counted by D0 individually, with mass
at most B. Partition the remaining represented vertices into groups

```
alpha_i = {a_i} and all K with Y(K)={a_i}, for i!=0;
gamma_j = {c_j}, for j!=0;
alpha_0=alpha_k=gamma_0=gamma_m=empty;
kappa_i = all K with Y(K)={a_i,a_(i+1)};
tau_j = interior(T_j).
```

These are disjoint and have total mass M. Symbols below denote either
sets or their masses. Unroll the cyclic word at the chosen state and
define at each state (i,j)

```
L(i,j) = union of (alpha_s,kappa_s) for s<i
         and of (gamma_t,tau_t) for t<j;
R(i,j) = represented vertices minus L(i,j), alpha_i, gamma_j.
```

**Cut-containment lemma.** Deleting `S0 union {a_i,c_j}` leaves
each component meeting H inside L(i,j) or R(i,j). At an A-step
`(a,c)` to `(b,c)`, deleting `S0 union {a,b,c}` leaves such components
inside the old L or new R. At a D-step `(a,c)` to `(b,d)`, deleting
S0, a,b and the arc suffix `v_q,...,v_n=d` leaves them inside
`L_old union gamma_c union {v_1,...,v_(q-1)}` or R_new.
The reflected prefix deletion leaves them inside L_old or
`R_new union gamma_d union {v_(p+1),...,v_(n-1)}`.
All components missing H are individual K. Further deletions confined
to H preserve these containments.

To prove the lemma, cut the outer and inner cycles at S0 and the
listed vertices. The surviving outer vertices before a and inner
vertices before c lie on the old side; those after b and d lie on the
new side. The monotone word puts every remaining cross incidence on
one side. In the D-suffix case, c and the remaining initial arc segment
can join only the old side: incidences at c precede the D-step and
the opposite cross edge bc is absent. Reflect for the prefix case.
The A deletion removes the shared inner endpoint, cutting its entire
fan between a and b. The state case cuts at one endpoint on each
cycle. At seams, the omitted a_0,c_0 already belong to S0. An attachment
has at most two consecutive active outer vertices, so it joins only
one surviving interval; if all its boundary vertices are deleted,
it detaches as one whole K. No vertex of K is deleted. This proves
every asserted containment, including when extra core vertices are
removed.

P and `(r,a_i,c_j)` are ambient geodesics, so the state case of the
lemma applies to their union. The arc-prefix/suffix versions for a
C-step follow by the same interval cut at its common outer vertex.

L is nondecreasing and R nonincreasing, from `(0,M)` to `(M,0)`;
`L+R<=M<=2h`. If no displayed spoke pair already works, take the
transition where L first becomes greater than h. Its old R exceeds h
and its new R is at most h. Write L for the old light left side and
R for the new light right side. There are only three step types.
The case h=0 is included: every represented or detached mass is zero.

## A-step: remove the outer edge's endpoints

Suppose the transition is `(a,c)` to `(b,c)`. Take the carrier E_a
and the path

```
(b,c)       if E_a contains r;
(r,b,c)     otherwise.
```

The second path has length lambda or `2*lambda`, hence is geodesic
by the root-distance calculation. Together the paths delete
`S0 union {a,b,c}`. Each remaining core component is contained in
the old L or the new R. The attachments on the sector ab and those
whose only active outer vertex was a or b detach individually; their
separate masses are at most B. The cyclic intervals on both boundaries
are now cut at a,b and c, so no further component can join the sides.
This proves (2) at every A-step, including each step in a long A-run.
There is no aggregate fan-mass inequality and no fan centroid argument.

## C-step: one midpoint threshold

Let the transition be `(a,c)` to `(a,d)` across T. Let p be the last
index with `2*x_p<=ell`, and q the first with `2*x_q>=ell`. Keep P,
and choose either

```
U = (r,a,v_0,...,v_p),
V = (r,a,v_n,...,v_q).
```

Both are shortest by (4), because both branch endpoints have root
distance `2*lambda`. The first retains the old light left side and
the second the new light right side. Let L_old,R_old,L_new,R_new
be the formal sides at the two states. The other possible supports are

```
R_old minus {v_1,...,v_p},
L_new minus {v_q,...,v_(n-1)}.
```

They are disjoint subsets of the represented vertices: `q<=p+1`
means that the prefix and suffix together delete the whole interior.
Both supports cannot exceed `h>=M/2`. All detached K are bounded by B,
so one choice works.

## D-step: two reflected pairs

Write the transition as `(a,c)` to `(b,d)` across T. For the first
pair use E_a. If it contains r, take the first q with
`2*x_q>=ell-lambda` and use `(b,d,v_(n-1),...,v_q)` as the other path.
If it omits r, take the first q with `2*x_q>=ell` and prepend r to
that other path. Equations (3),(4) and the root distances certify
shortestness in the two cases. The pair contains S0, deletes a,b,d,
and has component bounds

```
H_left = L union gamma_c union {v_1,...,v_(q-1)},    R.     (5)
```

For the reflected pair use E_b. If it contains r, take the last p
with `2*x_p<=ell+lambda` and use `(a,c,v_1,...,v_p)` as the other path.
If it omits r, take the last p with `2*x_p<=ell` and prepend r to
that path. This pair is also shortest, contains S0, and has bounds

```
L,    H_right = R union gamma_d union {v_(p+1),...,v_(n-1)}.  (6)
```

Here an empty prefix or suffix is interpreted in the evident way.
Since `ell>=lambda`, all thresholds lie in `[0,2*ell]`, including
the possible choices q=0 or p=n.

For (5), the surviving c and initial arc segment can connect only
to the old left interval: the D-step has no opposite cross edge bc,
and its other incidences precede the step. Deleting a,b isolates every
attachment on their sector individually. The remainder belongs to
the new right interval. The reflected argument proves (6). Extra
vertices on the carriers only reduce the residual components. Seam
cases use the empty group for c_0 and a_0.

The first threshold is at most ell and the second at least ell,
so `q<=p+1`. Therefore H_left and H_right are disjoint subsets of
the represented mass M. At least one is at most h; its paired other
side is already light, and detached K have mass at most B. This repairs
the D-step and completes the proof of (2).

## Heavy attachments

If every K has mass at most W/2, then (2) gives the all-mass corollary.
Otherwise a heavy K has a width-three torso decomposition. Its clique
boundary is contained in a bag. Attach the bag `V(G)-K` as an outside
leaf there, producing a tree decomposition of G. Assign K's vertex
masses locally and all other masses to the leaf. A weighted centroid
cannot be the outside leaf, whose only branch has mass greater than
W/2. Its local bag has at most four vertices and half-separates G.
Pair those vertices and choose at most two ambient geodesics covering
the bag. Deleting more vertices preserves the balance.

This is the existing
[reviewed heavy-attachment reduction](../planar_two_geodesic_prescribed_attachment_review1/REVIEW.md).
No long-fan replacement is used in either part of the theorem.

## Scope and small controls

The previous [unit mixed theorem](../planar_two_geodesic_subdivided_mixed_annuli/README.md)
allowed all valid words without condition (1). Its quantitative bound
included Fmax, the maximum long-fan region mass; heavy fans required
a centroid replacement that could change the anchor. The present result
removes that term and proves the specified-triple bound under an exact
anchor condition, including arbitrary positive inner-edge prices. We do
not count the previously established unit all-mass cases as new cases.

The previous [metric C/D theorem](../planar_two_geodesic_metric_cd_annuli/README.md)
allowed arbitrary wheel and cross prices satisfying its arc inequalities,
but excluded A-steps. Here their prices share one scale; A-steps are
allowed. Neither theorem contains the other in all its hypotheses.
The C/D theorem has since received a
[confirming independent review](../planar_two_geodesic_metric_cd_annuli_review1/REVIEW.md),
which proposes admitting A-steps and requests an explicit component
lemma. The cut-containment lemma above isolates that topological step.
That review does not independently verify the present mixed extension.
Outer/cross subdivisions carrying new vertex mass, inner attachments,
and arbitrary nonisometric cores remain outside the statement.

The separate audit includes a concrete long-fan check. Use word
`AAAAADDDDD`, common wheel/cross length four, and put an individual
attachment K_i in each outer sector, adjacent to r,a_i,a_(i+1) by
length-four edges. Take T_0 lengths `(3,2,3)`; for all other T_j use
`[4], [3,5], [1,2,1], [1,8,2]` according to j modulo four. Give unit
mass to a_1,...,a_4 and K_0,...,K_4, and zero elsewhere. The long-fan
region has all mass nine and each K has mass at most one. With anchor
`{r,a_7,c_2}`, the two geodesics

```
(c_2,a_7,r,a_2),    (a_3,c_0)
```

leave largest component mass three. The new bound is 9/2; the old
fan term was nine. This demonstrates the sharper bound and the direct
A-step mechanism, not failure of other possible separator constructions.

Two further controls distinguish the anchor condition from the target.
In word `AADDDD`, take anchor `(a_3,c_1)` and T_0 of total length seven
or eight, with common scale four and the remaining arcs as above.
Its distance to a_0 is respectively eleven or twelve; the criterion
fails in the first case and holds at equality in the second. In words
`(AD)^5` and `(AC)^5`, every inner branch has multiple outer neighbors,
so none satisfies (1). These are failures of this anchor method, not
counterexamples to two-path half balance.

For comparison with prior sufficient mechanisms, the all-D 18-vertex
control already audited in the metric C/D source is also an eligible
member here (all incident cross endpoints near the chosen anchor).
That source verifies a core minor of treewidth at least four and no
half-separating face for its weighting. We reuse that scope comparison;
we have not produced a new separation from those mechanisms or from all
known positive classes. The general treewidth-three and facial methods
in [Diot--Gavoille](https://emilie-diot.eu/Article/DG10a) are prior art.

## Reproduction and trust boundary

Run from the repository root, with Python 3.11+ and its standard library
(the recorded run used 3.11.2), with assertions enabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_anchor_mixed_annuli/verify.py --check
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_anchor_mixed_annuli/audit.py
```

The first output must match [expected.json](expected.json). It uses exact
Fraction arithmetic and six attachment fixtures, every eligible anchor,
and 80 further seeded core words. Seed: `2026092918`. It checks original-G
shortestness, spherical rotations, core isometry, exact anchor criteria,
mass partitions, actual component containments and final balance.
Profiles include zero, uniform, singleton, heavy/equality attachments,
random integer masses, inner-arc concentration and entire long fans.
Totals: 347 systems, 13,031 component cuts, 4,956 quantitative checks,
1,761 heavy-attachment cases and 3,195 light-attachment half checks;
360 of the last group have a heavy long fan and use no fan replacement.
These counts overlap across coordinate systems; they are not distinct
graphs or an exhaustive weight census. The checker imports the prior
graph, mass-choice and heavy-attachment helpers in this repository.

The separate [audit.py](audit.py) imports no research code. It directly
constructs every labelled A/C/D word of lengths three through seven
containing A and satisfying the run bounds, with one specified integer
metric and singleton sector attachments: 2,292 models. Floyd--Warshall
distances independently check the local criterion and every A-step
pair at every eligible anchor. It also checks the explicit controls.
It is an audit of the new local criterion and A repair; the C/D repairs
are covered by the written proof and the main checker. Expected line:

```text
A_component_pairs=7513 A_other_root=4511 A_root_carrier=3002 anchor_threshold_controls=2 criterion_states=15323 eligible_states=4744 heavy_fan_control_mass=9 heavy_fan_control_residual=3 models=2292 no_anchor_controls=2 PASS
```

The universal claim rests on the written distance, component, threshold
and centroid proofs. Finite regression is not a proof for every real
metric or mass. A separate implementation by the same researcher is not
independent peer review. No solver, proof assistant or external dataset
is required. The reused all-embedding scope comparison uses Whitney
uniqueness as explicitly recorded in its original source; the present
separator proof does not need it.
