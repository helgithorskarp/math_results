# A Ramsey bottleneck in a two-interval Schur construction

The proposed six-colour construction at 537 is **unresolved**. This note
explains why its large prescribed colour class makes it an unexpectedly
strong target: a completion would also give a five-colour triangle-free
edge colouring of **K216**, hence **R_5(3) >= 217**. The April 2026 survey
still gives **162 <= R_5(3) <= 307**. This is a conditional consequence,
not a new bound, an impossibility proof, or evidence that S(6)=536.

The underlying difference-colouring implication is classical. We claim
no novelty for it. The useful information here is its exact application
to this proposed interval family, including a converse, a sharp auxiliary
independence calculation, and the screening of 46 smaller supports. A
generalization then selects a different support at 537 with auxiliary
independence number 156; its completion remains open.

## Exact correspondence

Fix integers q>=1 and k>=1, put N=5q+2, and reserve colour k+1 for

    T = [q+1,2q] union [4q+2,5q+2].

All intervals here are intervals of integers. T is sum-free, with 2q+1
elements. Its complement is

    M = [1,q] union [2q+1,4q+1].

A k-colouring c of M completes a Schur (k+1)-colouring of [1,N] exactly
when it avoids monochromatic Schur triples wholly in M. This includes
x=y. Writing u[d]=c(d) and w[i]=c(2q+1+i), the remaining conditions are:

1. u is a Schur k-colouring of [1,q].
2. For 1<=d<=q and 0<=i<=2q-d, w[i], w[i+d], u[d] are not all equal.

Indeed, two low summands with a sum outside the low interval land in T;
two high summands land in T or above N. The other triples are precisely
the displayed low/high conditions.

Now use the following 2q+2 vertices:

    A = [0,q] union [3q+1,4q+1].

Their positive differences are **exactly M**. Give the edge xy, x<y,
colour c(y-x). Each triangle x<y<z has differences
(y-x)+(z-y)=z-x, so a Schur colouring of M gives a triangle-free edge
colouring of K_(2q+2) in k colours.

Conversely, every Schur triple in M occurs as the differences of one of
these triangles. A low triple a+b=z<=q is represented by 0,a,z in the
first block. For a mixed triple d+h=h+d with 1<=d<=q and
2q+1<=h<h+d<=4q+1, put

    x = max(0,3q+1-h-d),  y=x+d,  z=x+h+d.

Then x,y lie in [0,q] and z lies in [3q+1,4q+1], and the triangle has
differences d,h,h+d. No other triples occur in M. Thus the two problems
are equivalent, provided the graph edge colours depend only on the
integer difference in this specified vertex placement. This requirement
is stronger than an arbitrary k-colouring of the complete graph.

At q=107 the full interval is [1,537], |T|=215, |M|=322, and the graph
has 216 vertices. Its 1,656,360 triangles project onto exactly 20,089
distinct Schur triples: 2,862 low triples and 17,227 mixed triples.
A completion would therefore imply R_5(3)>=217. The known upper bound
307 does **not** exclude it. The consequence changes the construction's
priority; it does not establish nonexistence.

## The auxiliary independence bound is sharp

Let G_T have vertex set [0,N], with an edge when the positive difference
of two vertices belongs to T. Then

    alpha(G_T) = 2q+2.

The set A above attains the bound. For the upper bound, start with the
smallest vertex a in an independent set. All vertices within distance
2q of a must lie in [a,a+q], since [q+1,2q] is forbidden. Remove that
cluster and repeat. A second cluster starts at least 2q+1 later. A third
would start at least 4q+2 after a; its distance from a would then belong
to [4q+2,N], which is forbidden. There are at most two clusters, each
containing at most q+1 integers.

This is an exact graph calculation for the specified T, **not** an
upper bound for unrestricted Schur colourings.

## Smaller two-interval supports still have a Ramsey cost

Earlier pilots reserved

    T(a,b) = [a,a+b-1] union [N+1-a,N-a+b] union {N},

with N=537, b=80, and 81<=a<=126. Each such support is sum-free and has
161 points. Set

    r = min(a, floor((N-2a-b+2)/2)),
    A(a,b) = [0,r-1] union [a+b+r-1,a+b+2r-2].

The within-block differences are below a; the cross-block differences
lie between a+b and N-a. Consequently every positive difference avoids
T(a,b). A five-colouring of its complement would colour K_(2r) without
a monochromatic triangle, giving R_5(3)>=2r+1.

For these 46 supports, 2r ranges from 162 to 228: it is 2a for a<=114,
and 458-2a for a>=115. Thus even supports with only 161 reserved points
can force a much larger Ramsey graph. This is a lower bound on their
auxiliary independence numbers; exact optimality is not claimed here.

The resulting design criterion is to examine difference-avoiding sets
before investing in a prescribed-colour completion. Maximizing the
number of reserved points alone can silently impose a much stronger
Ramsey construction. This does not justify imposing 161 as a universal
upper bound on colour-class sizes or on auxiliary independence numbers.

## A replacement chosen by the exact independence number

The calculation extends to

    T(N,a) = [a,2a-2] union [N+1-a,N],
    a>=2, N>=5a-4.

These hypotheses make T(N,a) sum-free. Write D=N-a. For the graph on
[0,N] with edges at differences in T(N,a), the exact independence number is

    max over 1<=j<=1+floor(D/(2a-1)) of
        min(j*a, D+1-(j-1)*(2a-2)).

Proof: any independent set has diameter at most D, by the upper forbidden
interval. Greedily group its points into clusters whose span is at most
a-1, starting each cluster at the next ungrouped point. The next cluster
starts at least 2a-1 after the preceding cluster's first point. Its
distance from the preceding cluster's last point is therefore at least a;
the lower forbidden interval forces that distance to be at least 2a-1.
Thus j clusters contain at most ja points, and their j-1 intervening gaps
omit at least (j-1)(2a-2) integers from a span containing at most D+1
integers. Even j singleton clusters need span at least (j-1)(2a-1), which
gives the stated range of j.

Conversely, for each j in that range take
B=min(ja,D+1-(j-1)(2a-2)). There are j positive integers at most a whose
sum is B. Use them as the lengths of consecutive interval clusters,
separated by gaps of exactly 2a-2 missing integers. The total span is
B-1+(j-1)(2a-2)<=D. All internal differences are below a, and all
differences between clusters are at least 2a-1 and at most D, so the
resulting B-point set is independent. This proves equality.

For N=537, exact evaluation over all 107 permitted integers 2<=a<=108
has the **unique minimum 156 at a=78**. The replacement support is

    T = [78,154] union [460,537],     |T|=155,
    M = [1,77] union [155,459],       |M|=382.

An attaining independent set is [0,77] union [232,309]. The j=1,2,3
terms of the formula are 78,156,152. This support therefore avoids the
forced new R_5(3) bound identified above; that does not establish its
five-colourability. All 382 complement positions can be coloured
independently, so there is no restriction to old-colour images or fibres.
Unlike the original q=107 reduction, the high interval now contains
Schur triples wholly within itself. These additional constraints must be
included in any completion search.

A bounded joint pilot was inconclusive at 100,000 CaDiCaL conflicts. No
full 537 word, certified negative result, or feasibility inference follows
from choosing the minimum of this auxiliary parameter.

The optional `complete.py` runner supplies the full construction instance:

    python3 -m pip install -r requirements.txt
    python3 -B complete.py --budget 100000 --word /tmp/schur-interval-word.txt

It uses 1,910 Boolean variables and 144,050 clauses. Each of the 382
positions has exactly one of five colours. Every Schur triple wholly in
M forbids each common colour, and colour names are ordered by their first
appearance. This last condition loses no colouring because all five
names are interchangeable. There are no other symmetry restrictions.
The 27,664 remaining triples include 1,482 low, 20,482 mixed, and 5,700
wholly high triples. The runner checks a satisfying complete word against
all integer Schur triples before writing it. UNSAT output would remain
an uncertified solver observation; the runner emits no proof trace.

## Reproduction and trust boundary

Run from this directory, using Python 3.10 or newer:

    python3 -B verify.py > /tmp/schur-interval-check.json
    diff -u expected.json /tmp/schur-interval-check.json
    sha256sum -c SHA256SUMS

The verifier uses only the standard library and was run with Python
3.11.2. It compares integer Schur rows with directly enumerated graph
triangles, including the full q=107 case. It independently enumerates
62,485 small complete assignments (7,270 valid), checks all 270,592
subsets for the auxiliary graphs q=1,2,3, verifies all 46 smaller support
witnesses, and checks a complete positive 32-point four-colouring. Nine
further small graphs test the general formula against all 1,775,744
subsets, and exact integer evaluation checks the 107-case replacement
screen and its attaining set.
The optional SAT encoder is also checked against 2,940 complete small
assignments, including its colour symmetry, and its target row set is
compared with a separate literal traversal. The mathematical verifier
does not import PySAT or invoke a solver.

These finite audits check the construction and implementation. The
general claims are proved above, without a solver or an enumeration
assumption. This is not an independent peer review, and no UNSAT claim
at 537 or new lower bound is made.

## Sources and relationship to prior work

- Fredricksen and Sweet, [Symmetric Sum-Free Partitions and Lower Bounds
  for Schur Numbers](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v7i1r32/pdf/),
  2000, for the classical endpoint convention and the construction at 536.
- Radziszowski, [Small Ramsey Numbers, revision 18](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
  April 24, 2026, section 6.1.1, for the current R_5(3) bounds.
- Our earlier [bounded additive pullback note](../schur_additive_pullback_search/README.md)
  proves a different restriction, |T|<=m+1 for exact integer maps of
  height m. The interval family escaped that restriction; the present
  Ramsey consequence applies to arbitrary complement colourings.

Prepared 2026-09-28. The standalone 537 construction remains the research
target; the oversized interval supports are deprioritized in favour of
the a=78 model. None of these supports is claimed impossible.
