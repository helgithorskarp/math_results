# A complete two-parameter frame for the twelve-point twenty-contact core

Actual author **six-tammes-2**, role **researcher**, 2026-10-02.
Ordinary algebraic reduction plus a complete exact interval certificate.
All 12,091 fixed predicates have actually been replayed under the source
pins in VALIDATION.json. Independent researcher review and formalization
are pending. No fifteen-point global bound or optimizer occurrence is
claimed.

**Theorem.** On the closed interval I=[14/25,593/1000], every injective
twelve-point unit packing with the twenty equalities below is described
by equations(1)--(3) with exactly the branch epsilon=-1,eta=+1. Its
parameter obeys |z|<5/2 and g>1/2. Conversely, equations(1)--(3) on this branch, with t in I, the chart
inequality, g>=0 and all 33 displayed intercluster inequalities, produce
exactly such a packing.
No synthetic or actual point 13 is required. All other orientation branches
and the g<=1/2 portion of the surviving branch are excluded by the fixed
closed-rectangle certificate.

This is a weaker contact hypothesis than the prior thirteen-point G22
frame: one packing point and its two contacts are removed. The present
interval certificate uses only surviving points. In a fifteen-point code
there are now THREE arbitrary added points; their capacity and actual
optimizer occurrence of the core are separate, unresolved obligations.

Let `I=[14/25,593/1000]`. Take twelve unit points with labels
`0,1,2,4,5,6,7,8,9,10,11,12`, every different-point product at most `t in I`,
and these twenty prescribed equalities, allowing additional contacts:

```
0-5 0-6 0-7 0-11 1-2 1-4 1-10 1-12 2-4 2-8 2-10
4-8 5-7 5-9 5-11 6-11 7-12 9-10 9-11 10-12.
```

Before pruning, the complete two-parameter frame `(t,z)` has four formal
choices `(epsilon,eta) in {+1,-1}^2`, `|z|<5/2`, and exactly **33** additional
intercluster packing inequalities. The certificate below then proves the
unique permitted branch and g>1/2. A synthetic point with label 13 supplies
no equality, inequality or distinctness premise.

## Rigid clusters without label 13

Use coefficient basis `Q=[p1 p2 p4]`, metric `H=Q^T Q=(1-t)Id+tJ`,
and coefficient scalar product `<x,y>_H=x^T H y`. Since `t in I`,
`D=det H=(1-t)^2(1+2t)>0`. Set

```
r=2t/(1+t),             k=t(9t^2-2t-3)/(1+t)^2,
gamma=k/(1+k),          den=(2r-1)(r+1)=(9t^2-1)/(1+t)^2,
mu=(t-1)(t+1)(2t+1)(3t-1)/(9t^3-t^2-t+1).
```

For an equilateral unit contact pair, the second unit point at product t
from both endpoints is `r(first+second)-old`. The two solutions are distinct
on I. Reusing the old point violates its product bound `1>t`, so each of
the following six reflections is forced:

```
(new, first, second, old)
(6,0,11,5) (7,0,5,11) (9,5,11,0)
(8,2,4,1) (10,1,2,4) (12,1,10,2).
```

Consequently `B1=e0,B2=e1,B4=e2`,
`B8=r(B2+B4)-B1`, `B10=r(B1+B2)-B4`,
`B12=r(B1+B10)-B2`. These are the entire six-point B cluster.
Put `U=p6,W=p7,V=p9` in coefficient coordinates. Their pair products are k,
as follows, for example, from
`r^2(1+3t)-2r(1+t)+t=k`. Inverting the three A reflections gives

```
p0 =(rU+rW+(1-r)V)/den,
p5 =((1-r)U+rW+rV)/den,
p11=(rU+(1-r)W+rV)/den.                      (1)
```

The reflection determinant is `(2r-1)(r+1)^2>0`. Direct differentiation
gives

```
k'(t)=(9t^2-1)(t+3)/(1+t)^3>0 on I.
```

The exact endpoint comparisons k(14/25)>-3/10 and
k(593/1000)<-1/5 give the closed-domain bracket used by the interval
arithmetic. The exact endpoint values and rational identities are
recomputed in [identities.py](identities.py). The k-equilateral Gram
matrix is positive definite. All six A-cluster noncontacts have product
k or `h=4t^2/(1+t)-1`, with

```
k-t=4t(2t+1)(t-1)/(1+t)^2<0,
h-t=(3t+1)(t-1)/(1+t)<0.
```

The six B-cluster noncontacts have products h, k or
`ell=r(h+k)-t`. Specifically h occurs at (1,8),(2,12),(4,10);
k at (4,12),(8,10); ell at (8,12). Since 0<r<1 and h,k<t,
`ell<2rt-t<t`. The same exact checker verifies every cluster unit
identity, all eighteen internal prescribed contacts and these twelve
noncontact identities as rational functions of t. Its computations do
not introduce point 13. These elementary calculations reuse and credit
the [earlier G22 frame](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twenty-two-contact-frame/PROOF.md),
but its old interval pruning is not imported.

Both internal clusters therefore already pack. Each has nine
prescribed contacts. The two remaining equalities are `W.B12=t,V.B10=t`.

## Circle chart and both remaining roots

Let `d=H^-1(B12 cross B1)` and `C=1+D z^2`. The complete unit/contact
circle `W.B12=t`, apart from B1, has rational chart

```
W=tB12+(D z^2-1)/C*(B1-tB12)+2D z/C*d.       (2)
```

Indeed `B1-tB12` and d are orthogonal, with squared norms `1-t^2` and
`(1-t^2)/D`. In coordinates `W=tB12+alpha(B1-tB12)+beta d`, its inverse
is `z=beta/[D(1-alpha)]`; the excluded `alpha=1` is exactly W=B1.
This is forbidden by the surviving constraint `W.B1<=t<1`. The other
projective chart point is present at z=0. Moreover

```
W.B1-t=(1-t)(1+2t)/C*((1-t)^2 z^2-1),
```

so any packing obeys `(1-t)^2 z^2<=1` and
`|z|<=1000/407<5/2`. These statements require no label 13.

Write `s=W.B10` and `g=1-s^2-k^2-t^2+2skt`. The unit equations
`V.W=k,V.B10=t` imply `g>=0`. For a feasible packing, W and B10 are unit, so |s|<=1. On the larger
rectangle k in [-3/10,-1/5],t in I,
`partial_t g=-2t+2sk<=-13/25<0`. For s<=-24/25,
`partial_k g<=-297/625<0`, so the largest value occurs at
k=-3/10,t=14/25 and then s=-24/25: its value is-33/12500<0.
That remaining quadratic is increasing on [-1,-24/25]. For s>=7/10,
`partial_k g>=148/125>0`, so the maximum is at k=-1/5,t=14/25
and then s=7/10: its value is-1/2500<0. The quadratic there is
decreasing on [7/10,1]. Thus, including tangent g=0,

```
g>=0 implies -24/25<s<7/10,    1-s^2>49/625.
```

The exact checker verifies both bounding values; the displayed derivative
signs give the coverage argument, rather than a numerical sample.

All unit solutions are therefore exactly

```
V=((k-st)W+(t-sk)B10
   +epsilon sqrt(Dg) H^-1(W cross B10))/(1-s^2),
U=gamma(W+V)+eta mu H^-1(W cross V).         (3)
```

The metric identity
`||H^-1(x cross y)||_H^2=(||x||_H^2||y||_H^2-<x,y>_H^2)/D`
and orthogonality to x,y prove both equations and completeness. In the
U formula the checked identity is
`mu^2=D(1+2k)/(1+k)^2`, with
`1+2k=(3t-1)^2(2t+1)/(1+t)^2>0`. Thus the U choices are distinct,
including at g=0. At g=0 the two V choices coincide; this locus is retained.
Every denominator is positive, including
`9t^3-t^2-t+1=(1+t)^2(1+k)`. Both anchor handednesses are included by the
two epsilon and eta choices. Equations(1)--(3) prove all twelve unit
identities and all twenty prescribed contacts.

## Exact converse and the thirty-three packing tests

Start instead with t in I, finite real z satisfying
`(1-t)^2 z^2<=1,g>=0`, and either choice of epsilon and eta. Construct
all twelve vectors by(1)--(3). The internal Gram identities above establish
their unit norms, internal packing and prescribed contacts. Of the36 A/B
products, `W.B12=t,V.B10=t` are identities and `W.B1<=t` is the chart
constraint. The remaining **33** required comparisons are precisely

```
i in {0,5,6,7,9,11}, j in {1,2,4,8,10,12},
except (7,12),(9,10),(7,1):     Pi.Bj<=t.
```

They are necessary and sufficient for this twelve-point packing. They also
force all twelve names to be distinct since t<1. In particular the frame
is a complete reduction, with no missing rank, tangent or projective case.
The next section supplies the new closed-domain pruning certificate.
The old proof's point 13 packing literals are never applied to this
weaker core.

This frame has twelve actual packing points. Applying it inside a
fifteen-point code leaves **three** arbitrary additional points. The old
thirteen-core two-addition exclusion and equality classification do not
by themselves settle that extension problem or establish occurrence of
the weaker motif in an arbitrary optimizer.

## Fixed closed-domain pruning and its soundness

[PLAN.json](PLAN.json) fixes four prefix trees, on the full closed
rectangle R=I x[-5/2,5/2], in this order:

| target | sign(epsilon,eta) | leaves | prefix nodes | actual ordinal range |
|:---|:---:|---:|---:|:---|
| all feasible parameters |(-1,-1)|7861|15721|[0,7861)|
| all feasible parameters |(+1,-1)|1675|3349|[7861,9536)|
| all feasible parameters |(+1,+1)|1675|3349|[9536,11211)|
| feasible parameters with g<=1/2 |(-1,+1)|880|1759|[11211,12091)|

There are exactly 12,091 leaves and 24,178 prefix nodes. T and Z bisect the
t and z intervals respectively; all child boxes are closed, with a shared
cut boundary. Every other character indexes the fixed 42-element typed
[LITERALS.json](LITERALS.json) table. Only the g-half tree permits its
target-specific outside-target predicate. The strict verifier binds all
twelve labels, exactly 20 contacts, exactly 33 intercluster tests, the literal
table, precision, rectangle and four targets before interpreting a leaf.
It rejects truncated/unused trees, unknown literals, forbidden point 13,
misordered targets, depth>22 or a tree with>20,000 nodes. Exact normalized
leaf areas sum to one for each rooted binary partition; the recursive
closed bisection rule supplies point coverage, including boundaries.
No adaptive selector is needed to check the certificate.

[model.py](model.py) uses 80-bit outward dyadic arithmetic with arbitrary-
precision integers, exact fractions and integer square roots. An interval
[a,b] is stored as integer endpoints over 2^80. Addition and negation are
exact on this lattice; multiplication and division use downward floors
and upward ceilings of all endpoint candidates. Division rejects a zero-
containing denominator. Squaring retains zero when the interval spans it;
square-root endpoints use integer floor roots and an upper correction.
Thus each primitive encloses its real mathematical operation. No ordinary
floating-point sign or solver tolerance enters the certificate.

The only intersections with fixed necessary intervals are k in [-3/10,-1/5],
s in [-24/25,7/10], and1-s^2 in [49/625,1]. Their validity for every feasible
packing was proved above. Before taking sqrt(Dg), g is intersected with
[0,+infinity); g=0 is retained. These operations may discard infeasible
parameters but enclose every feasible parameter in a leaf box. An empty
necessary intersection therefore excludes its entire feasible subset.
For interval rectangles containing infeasible parameters, clipped values
need not represent those parameters; they are only necessary enclosures
on the feasible subset. This is the precise domain of the interval proof.
All divisions in the frame have a positive mathematical denominator. An
interval division that cannot certify this is a failed predicate, not an
exclusion. The pair-witness path catches ArithmeticError and returns False.

A successful leaf has one of the following meanings:

- chart: a strict positive lower bound for (1-t)^2z^2-1, contradicting the
  chart packing constraint;
- empty-necessary-intersection: a necessary k or s interval is empty;
- no-real-V: the entire g enclosure is strictly negative;
- W-pair: a strict positive lower bound for one prescribed surviving
  comparison W.Bj-t, j in {1,2,4,8,10};
- pair: a strict lower bound for Pi.Bj above the upper endpoint of t,
  with (i,j) in the complete 33-test list;
- outside-target-g-half: a strict lower bound g>1/2, only in the tree
  whose target includes g<=1/2.

For each of the first three trees, every leaf excludes feasible packing
parameters. For the fourth, every leaf excludes feasible parameters with
g<=1/2, either by a packing contradiction or its target-specific predicate.
The four full closed partitions therefore exclude all three unwanted
branches and prove g>1/2 on the remaining one. Combined with the complete
packing-to-frame and converse proof, this proves the theorem.

[replay.py](replay.py) checks at most 2500 explicit ordinal predicates per
invocation, with 50 slogical/55 shard guards. The five ACTUAL disjoint runs
[0,2500),[2500,5000),[5000,7500),[7500,10000),[10000,12091) all passed under
identical four-file source pins, with every requested predicate executed.
No cursor or hash supplied execution evidence for another slice.
[VALIDATION.json](VALIDATION.json) records the complete actual cover,
source pins, counts and measured costs. [controls.py](controls.py) provides
adversarial structural and arithmetic boundary controls. The exact
cluster identities are checked separately by [identities.py](identities.py).
These are author checks; publication, identical outputs and different
internal representations do not provide independent researcher review.

## Interface with actual contact faces

For an actual spherical packing containing this injective twelve-point core,
the following eight unordered triples are actual small triangular faces of
the complete contact drawing:

```
{0,5,11} {0,6,11} {0,5,7} {5,9,11}
{1,2,4}  {1,2,10} {1,10,12} {2,4,8}.
```

This applies the classical empty-contact-triangle argument explicitly given
in [the triangle-support proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/disconnected-core-obstruction/PROOF.md).
Each triple has all three products equal to t, so its Gram matrix is H.
Any point z in its small spherical triangle is a normalized nonnegative
combination `z=s/||s||`, where `s=sum lambda_i Vi`, `sum lambda_i=1`.
For a different packing point z, all `z.Vi<=t` would imply `||s||<=t`.
But

```
||s||^2=t+(1-t)*sum lambda_i^2 >= (1+2t)/3 > t^2,
```

where the last gap is `(1-t)(1+3t)/3>0`. Thus no other packing point can
lie in that small closed triangle. Equal-length minor contact arcs cannot
cross, and no third packing point can lie inside a contact arc. Hence no
other graph edge enters the triangle interior either; it is an actual face.
The eight vertex sets are distinct because the twelve core names are
distinct actual points. The same reasoning holds with additional packing
points present.

These eight triangles supply the eighteen internal-cluster edges. Together
with the required cross edges7-12 and9-10, an injective occurrence in an
actual contact map supplies precisely the twenty equalities of this frame.
This is a concrete interface for a map-occurrence search, rather than a
total face profile. The status and interior angles of the pentagon cycle
12-10-9-5-7 require a separate check. No such pentagon-face hypothesis is
used in the frame, and no occurrence theorem for an arbitrary optimizer
is inferred from this classical triangle observation.
