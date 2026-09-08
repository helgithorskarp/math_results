# Every good43 has between 390 and 513 edges

A graph is good if it contains neither a clique nor an independent set of
order five. We prove that every good graph G on 43 vertices satisfies

    390 <= e(G) <= 513.

The complete excluded family consists of all 43-vertex graphs with at most
389 edges in either color. Its members have arbitrary individual degrees,
internal structure and labels. No regularity, automorphism, packing, fixed
neighborhood or selected physical witness is assumed.

We import the classical R(3,5)<=14 and R(4,5)<=25, the exact local extremum
U(18)=85 for (4,5;18) graphs, and completeness of the 352,366-record
(4,5;24) catalog. The last two are the same premises used in the accepted
h3959 regular18/24 exclusion. The new result strengthens that exclusion to
seven additional irregular degree multisets in each color.

## 1. A robust consequence of the complete dense-neighborhood catalog

Let X be a hypothetical good43 graph, and set

    delta(w) = 24 - d_X(w) >= 0.

Consider an X-edge uv whose endpoints both have degree 24. Suppose the two
actual neighborhood graphs H_u=X[N_X(u)] and H_v=X[N_X(v)] each have at
least 128 edges. Put

    C=N_X(u) intersect N_X(v),  c=|C|,
    T=V(X) - (N_X(u) union N_X(v)),  |T|=c-5,
    e=e(X[C]),  d_w=d_{X[C]}(w),  d_max=max_w d_w.

The common graph C is triangle-free, since a triangle with u and v would
be a K5. For i in {u,v}, define the quantities obtainable from its rooted
neighborhood:

    D_i(w) = degree of w in H_i,
    L_i(wz) = common-neighbor count of w,z in H_i,
    P_i = sum_(w in C) D_i(w),
    Q_i = sum_(w in C) d_w D_i(w) - sum_(wz in E(C)) L_i(wz).

Write delta_C=sum_(w in C) delta(w). The number r_w of X-neighbors of w
inside T is exactly

    r_w = 24 - delta(w) - D_u(w) - D_v(w) + d_w.

Summing r_w<=c-5 gives

    P_u+P_v+delta_C >= c(29-c)+2e.                         (1)

For any edge wz of C, its full common-neighbor count is
L_u(wz)+L_v(wz)+|N_T(w) intersect N_T(z)|. There is no double-counted
common vertex inside C, because C is triangle-free. Its common-neighbor
count is at most 13 by R(3,5)<=14. Using
|N_T(w) intersect N_T(z)| >= r_w+r_z-|T| and summing gives

    Q_u+Q_v+sum_(w in C) d_w delta(w)
        >= sum_(w in C) d_w^2 + (40-c)e.                   (2)

In particular, if delta_C<=2, the respective extra terms in (1) and (2)
are at most 2 and 2*d_max. Nonnegativity of every delta(w) is essential.

The complete catalog has exactly 1,027 graphs with at least 128 edges.
Rooting all of them at all 24 vertices gives 24,648 rooted graphs. Their
common-graph order, sorted common-graph degree sequence and (P,Q) values
give 39 bins and 527 distinct profiles. As in h3959, matching by degree
sequence admits all genuine common-graph identifications and possibly
extra ones; this enlargement is safe for exclusion.

The new finite certificate tests all 6,669 unordered profile pairs,
including equal pairs, with the extra slack just described. Exactly
5,708 fail (1) even with an added 2. The remaining 961 fail (2) even with
an added 2*d_max. Therefore:

**Robust overlap lemma.** No such edge uv can have delta_C<=2.

This lemma allows arbitrary deficits and edges away from the two roots;
it does not assert that X is regular. `produce.py` computes the robust
test from the hash-pinned accepted parent table. The separate `verify.py`
scans the full catalog, compares every retained graph, reconstructs every
root profile from Boolean adjacency matrices and a literal edge-sum for Q,
then verifies every new pair decision. The finite test is not a SAT solve.

## 2. Global weighted incidence forces many dense neighborhoods

Suppose Y is good43 with m<=389 edges. The classical degree window gives
18<=d_Y(v)<=24, so m>=387. Define

    delta(v)=d_Y(v)-18,  D=sum_v delta(v)=2m-774.

Thus D is 0, 2 or 4. Let X be the complement of Y. Its degree is
d_X(v)=24-delta(v), matching the notation above. Let

    Z={v:delta(v)>0},  z=|Z|,  F=V(Y)-Z,  f=43-z,
    s_v=sum_(w in N_Y(v)) delta(w)  for v in F.

For a vertex v in F, its Y-neighborhood A has 18 vertices and its
Y-nonneighborhood B has 24. Let a=e(Y[A]) and b=e(X[B]). Counting Y-edges
between A and B from both sides gives

    a+b = 213+s_v-D/2.

For completeness, the two counts are 306+s_v-2a and
2b-120+(D-s_v), respectively. Since Y[A] is (4,5;18), a<=85, and hence

    b >= 128+s_v-D/2.                                    (3)

When D>0, call v in F qualifying if s_v>=D/2, and write H for the set of
qualifying vertices. Its members have X-degree 24, and (3) puts each of
their X-neighborhoods in the complete dense catalog used in the lemma.

Double-counting weighted Y-edges between Z and F gives

    S=sum_(v in F) s_v = sum_(w in Z) delta(w) d_{Y[F]}(w).

There are at most z-1 neighbors of w inside Z. Consequently

    d_{Y[F]}(w) >= 19+delta(w)-z,
    S >= (19-z)D + sum_(w in Z) delta(w)^2.                (4)

Put k=D/2 and h=|H|. Every s_v is at most D, and each nonqualifying s_v
is at most k-1 because it is an integer. Thus

    S <= hD+(43-z-h)(k-1).                               (5)

All positive-excess multisets are listed below. Omitted vertices have
excess zero, or Y-degree 18. Inequalities (4) and (5) give:

| D | positive excesses | lower bound on S | lower bound on h |
|---|---|---:|---:|
| 2 | 1,1 | 36 | 18 |
| 2 | 2 | 40 | 20 |
| 4 | 1,1,1,1 | 64 | 9 |
| 4 | 1,1,2 | 70 | 10 |
| 4 | 1,3 | 78 | 13 |
| 4 | 2,2 | 76 | 12 |
| 4 | 4 | 88 | 16 |

In every case h>=5. The table is an exhaustive integer partition of D,
not a sample of degree profiles. The independent checker also enumerates
all 80 possible graphs on the exceptional vertices for these seven
multisets, and obtains the same minimum S directly by subtracting their
weighted internal edge sums from sum_w delta(w)(18+delta(w)). These small
graphs need not extend to good43; admitting all of them is conservative.

## 3. The qualifying set forces the contradiction

Suppose u,v in H were adjacent in X. Their neighborhoods meet all premises
of the robust overlap lemma. Moreover C is disjoint from N_Y(u), so

    delta_C <= D-s_u <= D/2 <= 2.

The lemma forbids this edge. Thus H is independent in X, or a clique in Y.
Since |H|>=5, Y is not good, a contradiction.

If D=0, all 43 vertices have X-degree 24 and (3) gives b>=128 everywhere.
Every edge would have delta_C=0 and is forbidden by the same lemma. An
X-graph of degree 24 cannot have no edges. This recovers the accepted
regular18 case without assuming it as an additional premise.

Therefore m>=390. Applying the result to the other color, whose edge
count is 903-m, proves m<=513. This establishes the complete family gate.

## Scope and trust

The bound is universal over all complete physical 43-vertex graphs. It
provides the direct necessary inequality 390<=sum_(i<j) x_ij<=513 for red
edge bits. It makes no inference about the existence of graphs at either
endpoint. A graph passing this bound need not be good. No historical
priority, sharpness, formal proof-assistant check or external review of
this new strengthening is claimed.

The imported catalog completeness and U(18)=85 are essential. The parent
theorem was independently accepted at h3965 with these boundaries. Exact
source and graph references are in `DEPENDENCIES.json`; source commits
are recorded separately in `README.md`. Remaining trust is the displayed
unformalized argument, exact Python semantics, catalog decoding, SHA-256,
the two implementations and ordinary hardware.

The 72 whole-graph overlap controls check both identities by their physical
residuals: missing C-to-T edges for (1), and the sum of 13 minus actual
edge codegree plus common nonneighbors in T for (2). The 96 other whole
graphs check the irregular density identity directly. The controls allow
signed deficits to exercise the algebra, and are expressly non-Ramsey
fixtures. Nonnegative deficits and the Ramsey caps are used only in the
proof of the inequalities, not assumed to hold in random controls.

This excludes seven new irregular degree multisets per color, alongside
the two previously excluded regular classes. The h3987 degree20/22 q10
children have 430 or 473 edges and receive no new decision from this
bound. The 99 closed / 161 open ledger, 518 closed / 122 open q7-r5 tasks,
and 2,188,660 remaining whole h3887 tasks are unchanged. No saved witness,
old proof trace, fixed H92/H93 subsystem, tail ladder or symmetry source
is used in this result. No good43 or Ramsey lower-bound improvement is
established.
