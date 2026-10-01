# The negative-edge core admits at most one arbitrary extension below tau

Actual author: **six-tammes-2**, role **researcher**, 2026-10-01.
Computer-assisted author proof; independent researcher review pending.
The geometric and differentiation arguments below are unformalized.

Let `I=[14/25,593/1000]`. Let tau be the unique root in I of the credited
incumbent polynomial

`F(t)=13t^5-t^4+6t^3+2t^2-3t-1`.

It lies strictly between
`0.59260590292507377809642492233275` and
`0.59260590292507377809642492233276`. This is prior art, not a new
construction or a proved global fifteen-point optimum.

## Claim and hypotheses

Suppose thirteen unit vectors with labels `0,1,2,4,5,6,7,8,9,10,11,12,13`
have every distinct pair product at most t, where `t in I` and `t<tau`,
and have these 23 prescribed products equal to t:

```
0-5 0-6 0-7 0-11 1-2 1-4 1-10 1-12 2-4 2-8 2-10 2-13
4-8 5-7 5-9 5-11 6-8 6-11 7-12 8-13 9-10 9-11 10-12
```

There do not exist two further unit vectors x,y with
`p_i.x<=t`, `p_i.y<=t` for every thirteen labels and `x.y<=t`.
The added vectors are arbitrary: no contact or incidence pattern is imposed.
This excludes the `(9,13)`-deleted 23-contact core from any improved
fifteen-point packing within this parameter interval.

This is a conditional motif exclusion. It does not prove that an
optimizer contains the motif, settle the full packing domain of the core,
or improve the unconditional global Tammes-15 upper bound. Values
`t<14/25` lie outside the stated theorem.

## Two precise prerequisites

[Lemma8929](../negative-cross-reduction/PROOF.md) classifies every packing
with the displayed contacts on I, up to O(3), as one selected continuous
formal unit model. Its parameter q is the unique simple root
`29/5<q<39/5` of its first quartic factor for orientation `sigma=-1`.
That formal model and all its prescribed identities exist throughout I,
including parameters where some other packing inequalities fail.
The absence of root, chart, rank and denominator exceptions is imported.

[Lemma9003](../negative-core-boundaries/PROOF.md) proves two further facts.
Every actual packing of this core requires `t>=alpha=1/sqrt(3)>577/1000`.
For every actual packing with `t<tau`, the three planes with labels
`1,4,7` have a unique intersection. If it satisfies all thirteen
avoidance inequalities, its norm is strictly less than one. That proof
also treats the equality case and the possible Gram degeneracy.

The two prerequisites remain independently unreviewed author proofs.
[INPUTS.json](INPUTS.json) records their source commits, graph references
and required file hashes. Hashing source identifies a premise; it does
not prove that premise. Their linked reproduction instructions supply
the separate checks needed to audit them.

## Avoidance polytope and the cut

Use anchor coordinates in `(p1,p2,p4)`, with positive definite Gram matrix
`H=(1-t)Id+tJ`. Norms and products below use H. For the selected model
write x046, x047, x147 for the respective intersections of the three
planes `p_i.x=t`. Define

```
n=x046+x047+(4/5)x147,
rho=893/1000, b=rho sqrt(n^T H n),
P={x: p_i^T H x<=t for all thirteen labels},
K=P intersect {x: n^T H x<=b}.
```

The computations establish that all three intersections exist and n is
nonzero on the entire closed rational interval
`J=[577/1000,0.59260590292507377809642492233276]`.
They establish boundedness of P and control every noncritical active
triple of K on that same closed interval. The critical triple uses
lemma9003 only for **actual packings with t<tau**. No claim that every
vertex of K has norm less than one at or above tau is made.

For boundedness use the four normals with labels `7,8,10,11`. Solving
their coordinate relation gives positive weights `w7,w8,w10,w11=1`
with `sum w_i p_i=0`, on each closed cell. Each of the four intersections
of three of these planes has every anchor-coordinate magnitude less
than 10. The four-plane polytope is their tetrahedron. Indeed, if its
slacks are `s_i=t-p_i.x>=0`, then `sum w_i s_i=t sum w_i`, and its
barycentric weights are `w_i s_i/(t sum w_j)`. Consequently every point
of P has all anchor coordinates strictly between -10 and 10. These
positive-weight, nonsingular and coordinate conditions are checked on
every cell, rather than inferred from a floating spanning test.

## Complete finite vertex verification

[PLAN.json](PLAN.json) lists 95 dyadic cells of J by `(depth,index)`.
Their rational endpoints are `L+(R-L)index/2^depth` and
`L+(R-L)(index+1)/2^depth`. The checker verifies their ordering, exact
adjacency and both closed outer endpoints. The maximum depth is eight.
It checks **all** `binom(14,3)=364` active triples on every cell, including
singular interval cases: 34,580 checks, with no inherited parent proofs.

For a triple write its three coefficient rows as A and right sides as z.
Set `D=det(A)` and let C be the Cramer numerator vector. For `D!=0` its
intersection is `x=C/D`. Each triple receives one of these checks:

* **Coordinate exclusion:** for some j, `|C_j|>10|D|` uniformly, so its
  nonsingular intersection cannot lie in the proved coordinate box.
* **Direct norm:** D has strict sign and the outward enclosure of
  `(C/D)^T H (C/D)` has upper endpoint strictly less than one.
* **Homogeneous infeasibility:** for another avoidance row a and right
  side z_a, evaluate `R_a=a.C-z_a D`. A strict positive lower endpoint
  excludes the `D>0` regime; a strict negative upper endpoint excludes
  `D<0`. If the determinant interval crosses zero, both regimes require
  their respective witnesses. No decision is made from a rounded sign.
* **Cut Gram norm:** for unit normals u,v, put `s=u.v`, `a=n.u`, `c=n.v`,
  and `N=n.n`. With `1-s^2>0` and
  `E=N-(a^2+c^2-2sac)/(1-s^2)>0`, the unique intersection with the cut has
  squared norm
  `2t^2/(1+s)+(b-t(a+c)/(1+s))^2/E`.
  This follows by decomposing the intersection into the minimal solution
  `t(u+v)/(1+s)` and the direction perpendicular to u,v. The formula is
  enclosed directly. Prescribed products s=t are used exactly, and
  `n.p4=(14/5)t` follows from the three defining intersections.
* **Critical triple:** only literal labels `1,4,7` may import lemma9003.

The homogeneous calculation is sometimes tightened with the validated
midpoint/derivative enclosures described below. There are exactly three
such witnesses in the final flat certificate; no centered norm witness
is needed there. An interval singularity alone never excludes a vertex.
A triple with actual determinant zero is not independent. Every vertex
of the full-dimensional bounded K has at least one independent active
triple, all of which are checked. Thus singular active sets are not lost.

Zero lies strictly inside every defining halfspace since t,b are positive.
For an actual packing below tau, every feasible vertex of K has norm
strictly less than one, using lemma9003 for the one critical triple.
Every point of a bounded polytope is a convex combination of its
vertices; convexity of the norm then puts all of K strictly inside the
unit ball. A unit point avoiding the core must therefore satisfy `n.x>b`.

## The cap has capacity one

Let `m=n/||n||`. Every unit avoidance point lies in `m.x>rho`.
Two such points have product greater than `2rho^2-1`, by decomposing
along m or by the spherical triangle inequality. The exact rational
margin is

`2(893/1000)^2-1=297449/500000 > 593/1000`,

with difference `949/500000`. Since `t<tau<593/1000`, two avoidance
points cannot also have product at most t. This proves the claim.

## Curve enclosures and square-root branch

[model.py](model.py) uses the pinned 80-bit outward dyadic interval
kernel. For the quartic A(t,q), closed Bernstein signs bracket the
unique selected root on every whole cell and tightly at its midpoint.
Its derivative is `q'=-A_t/A_q`. Exact bivariate Bernstein coefficients
bound these derivatives; every denominator is checked away from zero.

To retain correlation, substitute exactly
`t=t0+h, q=q0+c h+z`, with rational c chosen near the midpoint tangent.
A known enclosure Q for q' implies
`|z| <= midpoint_root_error + cell_radius max_{v in Q}|v-c|`.
Two successive Bernstein evaluations on that rectangle tighten Q.
Each uses a previously justified bound, so there is no circular tube
assumption or sample-based root selection.

Each interval dual quantity carries an enclosure of its value, its
derivative along the curve and its midpoint value. Chain-rule operations
propagate all three. The mean value theorem permits intersection with
`midpoint_value + [-r,r] derivative_bound` after each operation.
This narrowing changes no derivative premise. Square roots use integer
floor/ceiling square roots and require strictly positive arguments.
Division requires a denominator enclosure separated from zero.

For stability, V is reconstructed from U and B10 as follows. Put
`s=U.B10`, `D_H=(1-t)^2(1+2t)`, and
`k=t(9t^2-2t-3)/(1+t)^2`. Then

```
g=1-s^2-k^2-t^2+2skt,
V=[(k-st)U+(t-sk)B10+sqrt(D_H g) H^-1(U cross B10)]/(1-s^2).
```

The cover proves g>0 throughout J, from its strictly positive
square-root argument and `D_H>0`. The original linear model of8929,
checked independently at `t=117/200`, has
`V.(H^-1(U cross B10))>0`. Its continuity and the absence of a zero
orientation when g>0 identify this positive square-root branch on all
connected J. The ordinary coordinate cross product is used in that
formula. This branch argument is required; isolated agreement alone
would not justify the replacement formula.

The derivatives of V and W are additionally enclosed by differentiating
their unit equations and their two prescribed products. For example,
V' solves the three independent rows HV, HU, HB10, with right sides
`-V^T H'V/2`, `k'-U'^T HV-U^T H'V`, and
`1-B10'^T HV-B10^T H'V`. Intersecting these linear enclosures with the
chain-rule enclosures is valid. An intersection x of `A x=z` similarly
has derivative solving `A x'=z'-A'x`. All pivots are checked.
The remaining points use the exact reconstruction identities of8929.

## Reproduction, arithmetic audit and scope of trust

[generate.py](generate.py) produces witnesses for every triple of every
cell. [audit.py](audit.py) separately checks each supplied witness without
calling the selectors. It shares the curve model and interval kernel,
so this is a same-author arithmetic audit, not an independent numerical
implementation, a proof-assistant formalization or a researcher review.
The geometric reduction, differentiation and imported classifications
remain explicit mathematical trust boundaries.

Normal and optimized Python runs, the full finite audit and damaged
witness/coverage controls are recorded in [VALIDATION.json](VALIDATION.json).
[EXPECTED.json](EXPECTED.json) contains the exact complete output and
the canonical SHA256 of the generated bulk witnesses. The bulk witnesses
and exploratory tree are omitted from publication. The small plan and
source regenerate them locally with standard-library Python. A guard
failure or unresolved cell is incomplete evidence and is never accepted
as nonexistence. Detailed commands are in [README.md](README.md).

The incumbent and quintic are credited to Buddenhagen's table and
D. A. Kottwitz, [The densest packing of equal circles on a sphere](https://doi.org/10.1107/S0108767390011370);
the [current fifteen-point coordinate table](https://spherical-codes.org/data/3/15)
was refreshed on2026-10-01. Musin and Tarasov's
[arXiv1410.2536](https://arxiv.org/abs/1410.2536) solves N=14.
Earlier core results7246/7288, the opposite-edge deletion8835/review8875,
and the separate incidence exclusions8881/review8953/8975 remain prior
art. The newer [two-ordinary-five exclusion9025](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/two-ordinary-five-branch/PROOF.md)
by six-tammes-1 and [three-five review9043](../../six-reviewer-3/three-five-audit/REVIEW.md)
concern complete contact maps and supply no premise here.
Their review verdicts do not transfer to8929,9003 or this claim.
No historical priority statement follows from the bounded search.
