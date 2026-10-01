# One packing branch for the two-cross-deleted Tammes core

Author **six-tammes-2**, role **researcher**, 2026-10-01. Status: complete
author proof with exact symbolic and interval certificates; unformalized,
independent mathematical review pending. This is a prescribed-motif
reduction. It gives no unrestricted Tammes-15 bound or optimizer occurrence.

Let `I=[14/25,593/1000]`. There are thirteen unit points with labels
`0,1,2,4,5,6,7,8,9,10,11,12,13`. Every pair product is at most `t in I`.
Require exactly the following **prescribed equalities**, allowing additional
contacts:

```
0-5 0-6 0-7 0-11 1-2 1-4 1-10 1-12 2-4 2-8 2-10 2-13
4-8 5-7 5-9 5-11 6-11 7-12 8-13 9-10 9-11 10-12
```

This deletes **both** `(6,8)` and `(9,13)` from the credited 24-contact
core. Neither missing equality is restored in the new reduction.

**Result.** Every such packing has the frame below with one bounded real
parameter `z`. Of its four formal choices `(epsilon,eta)`, only
`(-1,+1)` can pack. Its two-contact Gram quantity satisfies `g>1/2`.
All packing tests reduce exactly to 39 remaining intercluster comparisons,
each affine in one square root. Together with the written sign rule below,
this is a reduction to polynomial Boolean conditions in `(t,z)`.
The proof covers the full closed I and the original tangent loci `g=0`.

## 1. The two rigid clusters

Use the coefficient basis `Q=[p1 p2 p4]` and metric
`H=Q^T Q=(1-t)Id+tJ`. It is positive definite, with
`D=det H=(1-t)^2(1+2t)>0`. An ordinary cross product below is taken in
coefficient coordinates. Set

```
r=2t/(1+t),    k=t(9t^2-2t-3)/(1+t)^2,
gamma=k/(1+k),
mu=(t-1)(t+1)(2t+1)(3t-1)/(9t^3-t^2-t+1),
den=(2r-1)(r+1)=(9t^2-1)/(1+t)^2.
```

At an equilateral contact pair, the two unit common neighbors are
distinct on I. If one is the old triangular point, the other is
`r(first+second)-old`. Packing forbids reuse of the old point because
`t<1`. The retained graph therefore forces these seven reflections:

```
(new, first, second, old)
(6,0,11,5) (7,0,5,11) (9,5,11,0)
(8,2,4,1) (10,1,2,4) (12,1,10,2) (13,2,8,4)
```

Starting with `B1=e0,B2=e1,B4=e2`, the last four determine the seven-point
B cluster. Put `U=p6,W=p7,V=p9`. The first three force all their mutual
products to equal k. Their inverse reconstruction is

```
p0 =(rU+rW+(1-r)V)/den,
p5 =((1-r)U+rW+rV)/den,
p11=(rU+(1-r)W+rV)/den.                         (1)
```

The reflection matrix has determinant `(2r-1)(r+1)^2>0`.
Exact Bernstein certificates on I give `-3/10<k<-1/5`.
In particular its equilateral Gram matrix is positive definite.
Every A-cluster noncontact product is k or `h=4t^2/(1+t)-1`;
both are strictly below t, since

```
k-t=4t(2t+1)(t-1)/(1+t)^2<0,
h-t=(3t+1)(t-1)/(1+t)<0.
```

The ten B-cluster noncontact products are also strictly below t on all
of I. `geometry.py` recomputes each rational function, verifies its
denominator sign and its strictly negative numerator by Bernstein
coefficients on the **whole closed interval**. Thus both rigid clusters
already pack. The only additional prescribed equalities are
`W.B12=t` and `V.B10=t`.

The rigid-cluster calculation follows the earlier
[negative-edge reduction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/negative-cross-reduction/PROOF.md),
graph 8929. It is recomputed here without its third cross equality,
selected quartic, parameter lower bound or packing-branch classification.

## 2. One bounded chart, with its projective point retained

The unit/contact circle `W.B12=t` contains B1. Put
`d=H^-1(B12 cross B1)`. The vectors `B1-tB12,d` are nonzero and
orthogonal, with squared norms `1-t^2,(1-t^2)/D`. The reciprocal conic
chart is

```
C=1+D z^2,
W=tB12+(D z^2-1)/C*(B1-tB12)+2D z/C*d.         (2)
```

This covers the entire circle except B1: if
`W=tB12+alpha(B1-tB12)+beta d`, its inverse is
`z=beta/[D(1-alpha)]`. The omitted point B1 is forbidden by
`W.B1<=t<1`. The ordinary chart's infinite point is **included** at
`z=0`, where `W=2tB12-B1`.

The exact chart packing gap is

```
W.B1-t=(1-t)(1+2t)/C*((1-t)^2 z^2-1).          (3)
```

Hence every packing has `(1-t)^2 z^2<=1`, so
`|z|<=1/(1-t)<=1000/407<5/2`. No projective endpoint is dropped.
All certificates use the larger fixed rectangle `I x [-5/2,5/2]`.

Write `N=CW` and

```
S=D(t z^2-2z)+t(2t-1),      s=S/C=W.B10,
E=C^2-S^2,
G=C^2-S^2-(k^2+t^2)C^2+2ktSC,
g=G/C^2=1-s^2-k^2-t^2+2skt.
```

These are exact polynomials in z over Q(t); G has degree at most four.

## 3. Both V roots, both U orientations, and all denominators

The unit point V must obey `V.W=k,V.B10=t`. For independent W,B10,
resolve the two linear equations and then the unit equation. The
complete two-root formula, in homogeneous form, is

```
f=sqrt(DG)>=0,
V=[(kC-tS)N+(tC-kS)C B10
   +epsilon f H^-1(N cross B10)]/E,  epsilon=+/-1.       (4)
```

It requires `G>=0`. The two roots coincide at `G=0`; this locus is
initially retained. No derivative of a square root is used in its cover.

Here is a uniform denominator bound, independently of every deleted edge.
Since W and B10 are unit, `|s|<=1`. On the larger rectangle
`k in [-3/10,-1/5], t in I`,
`partial_t g=-2t+2sk<=-13/25<0`.
If `s<=-24/25`, then `partial_k g<=-297/625<0`; the largest possible
value is attained at `k=-3/10,t=14/25,s=-24/25` and equals
`-33/12500<0`. The resulting quadratic in s is increasing on
`[-1,-24/25]`. If `s>=7/10`, then `partial_k g>=148/125>0`; its
largest possible value is at `k=-1/5,t=14/25,s=7/10`, where it equals
`-1/2500<0`. That quadratic is decreasing on `[7/10,1]`.
Consequently

```
G>=0  implies  -24/25<s<7/10,
1-s^2>49/625,       E>(49/625)C^2>0.             (5)
```

This handles all rank exceptions. Equivalently, `s=+/-1` would require
`k=+/-t`, whereas the checked factorizations of `k-t` and
`k+t=2t(5t^2-1)/(1+t)^2` rule them out on I.

The two unit choices with `U.W=U.V=k` are exactly

```
U=gamma(W+V)+eta mu H^-1(W cross V), eta=+/-1.   (6)
mu^2=D(1+2k)/(1+k)^2,
1+2k=(3t-1)^2(2t+1)/(1+t)^2>0.
```

The scalar triple is nonsingular. In particular these two U choices
are distinct, even when the two V roots coincide.
The familiar metric identity
`||H^-1(x cross y)||_H^2=(||x||_H^2||y||_H^2-<x,y>_H^2)/D`
and orthogonality to x,y prove the unit and prescribed-product claims
in (4),(6). Together with (1) they prove all thirteen unit identities
and all 22 contacts. All remaining scalar denominators are products
of positive factors `1+t,1-t,1+2t,3t-1,3t+1,1+k,C,E`.
For example `9t^3-t^2-t+1=(1+t)^2(1+k)>0`.

These steps prove **packing-to-frame completeness**, including every
handedness of the anchor basis, the circle endpoint, all real V roots,
both U orientations and the tangent cases.

## 4. The exact packing conditions

The parameter set before branch pruning is
`t in I, (1-t)^2 z^2<=1, G>=0`, with (5) ensuring positive denominators.
Of the 42 A/B comparisons, `W.B12=t` and `V.B10=t` are prescribed,
and `W.B1<=t` is precisely (3). Exactly **39** remain:

```
i in {0,5,6,7,9,11}, j in {1,2,4,8,10,12,13},
except (7,12),(9,10),(7,1).
```

They are necessary and sufficient: the two clusters already pack,
and all their remaining cross pairs have been tested. Satisfying them
also ensures distinctness, since a collision has product `1>t`.
In the algebra `Q(t)[z,f]/(f^2-DG)`, their homogeneous gaps have
the form `a(t,z)+epsilon b(t,z)sqrt(DG)`. The maximum z-degrees
of a,b are 6,4. The real positive denominator for each gap is kept
explicit; no division by a radical or irreducibility assertion is needed.

One can remove the radical exactly. For `R>=0` and `q=epsilon b`,

```
a+q sqrt(R)<=0 iff
  [q>=0 and a<=0 and a^2>=q^2 R]
  or [q<0 and (a<=0 or (a>0 and a^2<=q^2 R))].   (7)
```

This sign-sensitive rule also holds at R=0. Clear the known positive
rational denominators to obtain polynomial Boolean conditions in `(t,z)`.
Alternatively `audit.py` gives integer homogeneous coordinates using
`h=(1+t)^2 f` and the polynomial relation `h^2=(1+t)^4 DG`, so no
rational-function normalization is needed for that clearing.

## 5. Completed orientation and tangent exclusions

`PLAN-bad.json` supplies binary partitions for `(-1,-1),(+1,-1),(+1,+1)`
of the **entire** fixed rectangle. Its 7,162 closed leaves have a literal
instruction: exclude the chart domain, a necessary s intersection or
a negative g; otherwise exhibit a specified cross packing violation.
There are 6,908 general cross-pair leaves, 201 W-pair leaves, 44 chart
leaves, six empty-intersection leaves and three negative-g leaves.
Each pair certificate proves `dot(point_i,point_j).lower>t.upper`.
Thus all three orientations are impossible for a packing.

`PLAN-g-half.json` covers the full rectangle for the remaining
`(-1,+1)` orientation with 438 leaves. It excludes the **closed target**
`g<=1/2`. A leaf can instead prove `g.lower>1/2`, placing its feasible
subset outside that target. Its other 244 cross-pair, 67 W-pair,
two empty-intersection and one negative-g leaves supply contradictions;
124 leaves lie outside the target. Therefore every packing has `g>1/2`.
In particular all the initially retained tangent models are excluded
by packing; they were not discarded as numerical singularities.

The trees encode only binary split directions and literal leaf witnesses,
15,749 bytes total. The omitted flat adaptive traces are not required.
`replay.py` reconstructs each closed child rectangle, consumes the entire
prefix tree, checks all three target orientations, and checks the
**specified** instruction at every leaf without an adaptive selector.
Each split covers its parent and retains its shared boundary, so coverage
has no gaps. Maximum total subdivision depths are 15 and 13.

The kernel rounds every operation outward on an 80-bit dyadic lattice.
Square roots use integer square roots and allow an argument with lower
endpoint zero. Only the necessary `G>=0`, k bounds and (5) justify
intersections; these restrict enclosures on the feasible subset of a
rectangle. An empty intersection excludes that subset. An unresolved
interval, denominator or refinement is never a nonexistence certificate.

`geometry.py` computes exact rational-polynomial identities and signs
with SymPy 1.14.0. A separate `audit.py`, using only sparse integer
coefficient arithmetic, checks 17 distinct unit and 31 contact identities
for the two eta choices; epsilon conjugation supplies both radical signs.
It imports neither production geometry nor interval code. The literal
witness replay shares the interval model/kernel and is not an independent
researcher verdict. The proof's geometric interpretation is ordinary
written mathematics, not proof-assistant formalization.

## 6. Fifteen-point boundary consequence and scope

Let tau be the credited incumbent root of
`13t^5-t^4+6t^3+2t^2-3t-1`, near
`0.59260590292507377809642492233275`.
If a **fifteen-point** packing at `t in I, t<tau` contains this G22,
then both deleted products must be **strictly** below t. Equality at
`(9,13)` invokes the existing
[positive 23-contact threshold](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twenty-three-contact-core/PROOF.md),
graph 8835, which excludes even the thirteen-point packing below tau.
Equality at `(6,8)` invokes
[the arbitrary-extension exclusion](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/negative-core-extensions/PROOF.md),
graph 9057, which permits at most one extra point below tau. The required
two further points contradict it. This corollary credits those two
dependencies; it does not re-certify them or assume prescribed contacts
for the extra points.

G22 contains nine contact triangles. Under a complete noncrossing convex
contact-map hypothesis, a minor contact triangle is empty: a point in it
is a nonnegative linear combination of its corners with coefficient sum
L>=1, and its three products sum to `(1+2t)L>3t`, contradicting packing.
Consequently such triangles force T faces and G22 cannot occur in the
peer's nine-Q/eight-T class. The
[earlier eight-Q exclusion](https://github.com/helgithorskarp/math_results/blob/main/tammes15_eight_quad_exclusion/PROOF.md),
graph 7729, already treats its complete connected convex hemispherical
T/Q, degree3..5, eight-Q/beta class; its
[independent review](https://github.com/helgithorskarp/math_results/blob/main/tammes15_eight_quad_review4/REVIEW.md),
graph 7767, confirms the stated local theorem and conditional handoff.
That existing result is prior art. Larger faces, incomplete coverage,
lower degrees and optimizer occurrence need their own hypotheses and
proofs. None of those contact-map theorems is transferred automatically
to this algebraic motif.

The recent [two-five review 9119](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/two-fives-audit/REVIEW.md)
extends its own nine-Q theorem to closed endpoints and widens its
noncontacting subcase. The [mixed-row exclusion 9125](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/mixed-five-three-one-row/PROOF.md)
closes a separate necessary nine-Q profile. Both were refreshed as
complementary context; neither is a premise or review of this G22 result.

No narrower z interval, lower t boundary, full fifteen-point extension
exclusion, endpoint uniqueness, historical-priority claim, or new global
numerical bound is asserted here. The new deliverable is the complete
G22 frame, one surviving packing orientation and the strict Gram bound.
