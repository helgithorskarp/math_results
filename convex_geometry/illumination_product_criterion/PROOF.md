# Which polytopes multiply illumination numbers?

Let `P` be a full-dimensional convex polytope in a positive-dimensional
real vector space. Write `I(P)` for its illumination number and `I_f(P)`
for its fractional illumination number. A nonzero vector `u` illuminates
`x` when `x+t u` is interior for some `t>0`. Fractional illumination uses
nonnegative weights on directions, with weight at least one illuminating
each boundary point. Allowing arbitrary finite Borel measures gives the
same fractional number for a polytope.

Products below are Cartesian products in complementary vector spaces,
also called direct vector sums. They are not convex hull free sums or
Minkowski sums in a common factor space. Put `P^r=P x ... x P`.
Here `log` denotes the natural logarithm.

## The product criterion

**Theorem.** The following conditions are equivalent:

1. `I_f(P)=I(P)`.
2. `I(P x K)=I(P)I(K)` for every positive-dimensional convex body `K`.
3. The equality in 2 holds for every positive-dimensional convex polytope
   `K`.
4. `I(P^r)=I(P)^r` for every integer `r>=1`.
5. `I(P^r)=I(P)^r` for arbitrarily large integers `r`.

This is a criterion for one specified polytope to multiply with **all**
partners. Equality for one pair, or even for the square, is not asserted
to imply any of these conditions.

Here are quantitative statements supplying the converse. If `v` is the
number of vertices of `P`, `tau=I_f(P)`, and `r>=1`, then

\[
 \tau^r\le I(P^r)
 \le \lfloor\tau^r r\log v\rfloor+1,
 \qquad
 \lim_{r\to\infty}I(P^r)^{1/r}=\tau.                 \tag{1}
\]

The displayed upper bound need not be sharp and can exceed the elementary
bound `I(P)^r`. A wholly rational bound useful for certificates is

\[
 B_r=\lceil\tau^r\rceil
       (1+r\lceil\log_2 v\rceil),\qquad I(P^r)\le B_r. \tag{2}
\]

If `s=I(P)>tau`, some `r` satisfies `B_r<s^r`, and a finite search for
such an `r` terminates using integer arithmetic. A greedy algorithm on
the product incidence family then constructs fewer than `s^r` directions.
Indeed, `I(P^r)<s^r` for every sufficiently large `r`. The argument is
not a practical complexity bound: the family can grow exponentially.

Two accompanying product facts are

\[
 I(P\times K)\ge\lceil I_f(P)I(K)\rceil,             \tag{3}
\]

for every convex body `K`, and

\[
 I_f(P\times Q)=I_f(P)I_f(Q)                         \tag{4}
\]

for polytopes `P,Q`.

These claims use classical finite fractional-cover machinery.
Scheinerman--Ullman, *Fractional Graph Theory*, Section 1.6, defines
exactly the rectangle product used here. Their Theorem 1.6.1 gives
fractional-cover multiplicativity, Theorem 1.6.2 identifies the covering
power rate, and Lemma 1.6.3 gives the finite-hypergraph mixed bound.
Thus the abstract tensor and power-limit mechanism is prior art.
Sections 1--3 below make the geometric reduction explicit and give
self-contained proofs, including arbitrary convex-body partners.
Potentially new content is limited to that all-partner geometric iff
criterion, the mixed illumination bound, and the finite strict-power
certificate. Priority remains unresolved until the full 2007
Boltyanski--Martini paper can be compared. See
[SOURCES.md](SOURCES.md) for precise attribution and access limits.

Baladze--Boltyanski (2006), Theorem 3, already proves multiplicativity
when a factor has `I(P)` pairwise antipodal boundary points. Such points
give disjoint illumination requirements and hence `I_f(P)=I(P)`. The
present criterion recovers that sufficient condition for polytopes and
identifies fractional equality as the necessary and sufficient condition;
no claim is made here that the two geometric conditions are distinct.

## 1. The finite illumination family is exact

Choose a facet description `P={x:a_j.x<=b_j}`. At a vertex `p`,

\[
 u\text{ illuminates }p
 \quad\Longleftrightarrow\quad
 a_j\mathbin{\cdot}u<0\quad\text{for every facet active at }p. \tag{5}
\]

Necessity follows from the active inequalities. For sufficiency, choose
`t>0` small enough that all inactive inequalities stay strict; the active
ones become strict by (5). All inequalities here are strict.

For a boundary point `x`, take a vertex `p` of the minimal face containing
`x`. Every facet active at `x` is active at `p`, so every direction
illuminating `p` illuminates `x`. Covering the vertices therefore covers
the whole boundary, for both integer and fractional illumination.

Let `V` be the vertex set and let

    E(u)={p in V : u illuminates p}.

Only finitely many distinct subsets of `V` arise. Delete the empty set
and write `H(P)` for the resulting family. Select one realizing direction
for each member. An arbitrary direction set can be replaced by these
representatives, retaining all vertex coverage. For a finite Borel
measure, each incidence class is Borel, since (5) is a finite system of
strict inequalities; moving its mass to the representative preserves
vertex coverage. Hence this same finite reduction also covers that
definition of fractional illumination.

Consequently `I(P)` is the integer set-cover number of `H(P)`, and

\[
 \tau=\min\left\{\sum_E w_E:
        w_E\ge0,\ \sum_{E\ni p}w_E\ge1\ (p\in V)\right\}. \tag{6}
\]

The family covers `V`, since each vertex can be illuminated toward an
interior point. The optimum in (6) is finite and attained. Its coefficients
are zero and one, so a rational optimum exists. Standard finite LP
duality also provides rational numbers `z_p>=0` with

\[
 \sum_{p\in E}z_p\le1\quad(E\in H(P)),\qquad
 \sum_{p\in V}z_p=\tau.                              \tag{7}
\]

There is no infinite-dimensional duality assertion here. Two vertices
maximizing and minimizing any generic linear functional cannot be
illuminated by the same direction: its scalar product with that functional
would have to be both negative and positive. Assigning these two vertices
dual weight one shows `tau>=2`.

For rational input polytopes, each nonempty class has a rational
direction whose illuminated set contains it: a sufficiently
small rational perturbation preserves all its strict negative
inequalities and may add coverage. Thus rational feasible directions
suffice for optimization and greedy certificates. The abstract theorem
does not require a rational realization.

## 2. Product directions and the mixed integer bound

At a pair of boundary points `(x,y)`, a vector `(u,w)` enters
`int(P x K)=int(P) x int(K)` if and only if its two components enter their
respective interiors. The times may initially differ, but any sufficiently
small common positive time works by convexity. Thus, at pairs of vertices,

    E_(P x Q)(u,w)=E_P(u) x E_Q(w).                    (8)

A zero component gives no coverage on the corresponding boundary; it
does not create an additional useful product class. Taking all pairs
from illuminating sets for the factors gives the classical upper bound

    I(P x K)<=I(P)I(K).                               (9)

This covers the entire boundary: if a component of a boundary point is
interior, any one of the finite chosen component vectors stays interior
for sufficiently small time. If it is on the boundary, use a vector
illuminating it.

Now take an arbitrary product illumination by `M` vectors `(u_i,w_i)`.
Fix a vertex `p` of `P`. For every `y in boundary K`, at least one index
illuminates `(p,y)`. Therefore the vectors `w_i` for which `u_i`
illuminates `p` include an illumination of `K`. There are at least `I(K)`
such indices. Repetitions or zero `w_i` cannot reduce this required count.

Give each `u_i` weight `1/I(K)` and discard the zero or empty classes.
Every vertex of `P` receives weight at least one. By (6),

    tau <= M/I(K).

Taking the minimum over product illuminations proves (3). If `tau=I(P)`,
(3) and (9) prove condition 2 of the theorem, including nonpolytopal
partners. No compactness or measure duality for the partner is needed.

## 3. Fractional products and product rounding

Let optimal weights for `P,Q` be `w_E,w'_F`, and their optimal vertex
dual weights be `z_p,z'_q`. Give the product class `E x F` weight
`w_E w'_F`. Every vertex pair receives weight at least one, and the total
weight is `I_f(P)I_f(Q)`. Conversely, give vertex pair `(p,q)` dual
weight `z_p z'_q`. By (8) its weight inside any illuminating class is

    (sum_(p in E) z_p)(sum_(q in F) z'_q)<=1.

Its total weight is the same product. Weak duality gives (4), with
explicit primal and dual certificates. Iterating proves the lower
bound in (1).

We give the rounding proof rather than infer a universal statement from
finite experiments. Suppose a finite set family has `N` ground elements
and fractional covering weights of total mass `T>1`. If `U` is its
current uncovered set, double counting gives

    sum_E w_E |E intersect U| >= |U|.

Some positive-weight set therefore covers at least `|U|/T` currently
uncovered elements. Select a set of maximum such size, with any fixed
tie-breaking rule. After `m` steps the uncovered cardinality is at most

    N(1-1/T)^m <= N exp(-m/T).                        (10)

If `m>T log N`, this is below one, so coverage is complete. Apply this
to the `r`-fold product of the optimal classes in (6), where
`N=v^r,T=tau^r`. It proves the upper bound in (1). Taking `r`th roots,
the lower bound tends to `tau` and the extra factor
`r log v+tau^(-r)` tends to one after taking its `r`th root. This proves
the limit.

For (2), put `q=ceil T`. Bernoulli's inequality gives

    (1-1/T)^(-q)=(1+1/(T-1))^q >= 1+q/(T-1)>2.

Thus every `q` steps reduce the upper bound on the uncovered cardinality
by a factor strictly smaller than one half. After
`1+r ceil(log_2 v)` such blocks, it is below one. This proves (2)
without numerical logarithms. Since `tau<s`, the ratio

    ceil(tau^r)(1+r ceil(log_2 v))/s^r

tends to zero. Testing the integer inequality in (2) must eventually
find a strict failure exponent.

## 4. Completing the equivalence

We proved 1 implies 2. Condition 2 implies 3. Applying 3 with
`K=P^(r-1)` and inducting gives 4; clearly 4 implies 5. If 5 holds,
the limit in (1) is `I(P)`, so 5 implies 1. This closes all implications.

In particular the contrapositive constructs a partner: if `I_f(P)<I(P)`,
choose a strict exponent `r` from (2), with the least actual strict
exponent if desired. For that least exponent,
`I(P^(r-1))=I(P)^(r-1)`, so `K=P^(r-1)` violates multiplicativity.
More generally, even without locating the least exponent, if every
successive product were multiplicative up through `r`, its value would
be `I(P)^r`, contradicting the certified strict upper bound. This last
qualification matters: an arbitrary strict exponent need not itself make
`P x P^(r-1)` the failing pair.

## 5. A rational pentagon with a strict square

The pentagon with cyclic vertices

    p0=(0,0), p1=(4,0), p2=(5,3), p3=(2,5), p4=(-1,3)

has outer edge normals, in that order,

    (0,-4), (3,-1), (2,3), (-2,3), (-3,-1).

Using (5), its maximal illuminated vertex subsets are exactly
`E_i={p_i,p_(i+1)}`, with indices modulo five. Representatives are

    d0=(0,6), d1=(-4,2), d2=(-4,-5),
    d3=(4,-5), d4=(4,2).                             (11)

Here is a finite proof that no direction is missed. The five normal
orthogonal lines partition direction space into ten boundary rays and
ten open angular sectors. In counterclockwise order the primitive rays
are

    (1,0),(3,2),(1,3),(-1,3),(-3,2),
    (-1,0),(-3,-2),(-1,-3),(1,-3),(3,-2).

The sum of each neighboring pair lies in the open sector between them.
All active-normal signs are constant on that sector; direct integer
dot products give the five adjacent pairs and the five singletons as
the complete incidence list. No set has three vertices. This also
checks boundary directions, which cannot be treated as open sectors.

Three pairs cover the cycle, and two cover at most four vertices, so
`I(P)=3`. Weight one half on each `d_i` and dual weight one half on
each vertex give `I_f(P)=5/2`.

For `P x P`, use the following eight pairs of direction indices:

    (0,0),(0,1),(1,0),(1,3),
    (2,2),(3,1),(3,4),(4,3).                          (12)

Their product classes cover all 25 vertex pairs; thus they illuminate
the full boundary. Conversely (3) gives

    I(P x P)>=ceil((5/2)*3)=8.

Therefore `I(P x P)=8<9=I(P)^2`, while `I_f(P x P)=25/4`.
This illustration is not offered as the first nonmultiplicative example:
Baladze--Boltyanski (2006), Lemma 3, already proves the same square count
for a regular pentagon by the same five-cycle incidence model. Our
rational pentagon and its integer certificate reproduce that mechanism.
Earlier work also gives nonmultiplicative products of discs.

## Scope and verification

The universal argument is the finite incidence reduction, fiber count,
LP duality, product certificates, and greedy decay. The supplied exact
code checks each geometric incidence directly, checks rational interior
steps, and independently verifies the cover and dual certificates.
Additional finite set-system checks corroborate the product identities
without making a geometric-realizability assumption about every set
system. No solver or floating-point arithmetic is used.

This note does not prove an efficient recognition algorithm, classify
all polytopes with `I_f=I`, or solve Hadwiger's conjecture. It does not
claim the power limit for arbitrary nonpolytopal bodies. Historical
priority of the criterion remains unestablished after the stated
bounded source search. This is a written proof with author checks,
not a formalization or independent peer review.
