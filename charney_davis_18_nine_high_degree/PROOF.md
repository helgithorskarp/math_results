# Nine vertices of degree fourteen at the eighteen-vertex boundary

Research note, 19 September 2026. This is a human combinatorial proof,
with supplementary exact checks. It has not received independent review.

## Statement and conventions

A generalized homology sphere over a field means a finite pure simplicial
complex for which **every** face link, including the empty-face link, has
the reduced homology of a sphere of the appropriate dimension. All spheres
below are flag. The empty face is included in face polynomials.

**Theorem.** Let Delta be a generalized homology 5-sphere on 18 vertices,
and let H be the complement of its one-skeleton. Then:

1. The minimum degree of H is at most three.
2. If that minimum is three, at least nine vertices of H have degree three.

Equivalently, Delta has a vertex of degree at least fourteen. If its maximum
vertex degree is fourteen, at least nine vertices attain that degree.
The first bound is sharp: the join of three 6-cycles has all vertex degrees
fourteen. We do **not** assert sharpness of the number nine.

**Charney--Davis consequence.** If such a Delta has gamma_3 < 0, its
complement has minimum degree three, at least nine degree-three vertices,
and the link of every degree-three complement vertex is not a suspension.
This is a necessary-condition theorem, not a proof of the eighteen-vertex
Charney--Davis inequality.

Write

    h_Delta(t) = sum_(i=0)^3 gamma_i t^i (1+t)^(6-2i),
    a = gamma_2(Delta),  b = gamma_3(Delta),
    q_v = deg_H(v),  m = |E(H)|,  T = number of unordered H-triangles,
    t_v = |E(H[N_H(v)])|,  L_v = gamma_2(lk_Delta(v)).

Thus t_v counts the triangles of H containing v, and sum_v t_v = 3T.
For an edge uv of Delta, write E_uv = gamma_2(lk_Delta(uv)).
Neighborhoods in H are open neighborhoods throughout.

## External mathematical inputs

We use the following published results and standard consequences.

* Davis--Okun, Theorem 11.2.1, gives gamma_2 >= 0 for flag rational
  homology 3-spheres. Hence E_uv >= 0.
* The vertex-link polynomial identity gives, for a flag homology 4-sphere Y,

      2 gamma_2(Y) = sum_v gamma_2(lk_Y(v)).

  Consequently L_v >= 0. In the convention kappa(X) = F_X(-1/2), the
  equivalent scalar is gamma_2(Y) = 8 sum_v kappa(lk_Y(v)), not 1/8.
* A flag homology (d-1)-sphere has at least 2d vertices. Its links are
  induced flag homology spheres. A vertex with precisely one nonneighbor
  makes the sphere a suspension. These are standard facts also recorded
  in Labbé--Nevo, Lemmas 2.1 and 3.2.
* Labbé--Nevo, Theorem 3.5(i): if v has the minimum antipode number pi > 1
  and lk(v) is a suspension of Gamma, then Delta = Gamma * C_(pi+3).
* Labbé--Nevo, Lemma 2.1(iv), by Alexander duality: deleting an induced
  equator has the homology of S^0. Applied to lk(v), the deletion is the
  disjoint union of v and Delta[N_H(v)]. Thus the latter is connected
  (indeed acyclic).
* Labbé--Nevo, Lemma 3.4(ii), for a vertex with two nonneighbors x,y:

      gamma_Delta(z) = gamma_lk(v)(z) + z gamma_lk(xy)(z).

These inputs apply over an arbitrary coefficient field in the statement.
For the rational input, apply universal coefficients to each finite face
link: vanishing lower homology over the given field implies vanishing lower
integral free ranks. The reduced Euler characteristic then forces top
rational Betti number one. Apply this to all links separately. No assertion
about vanishing integral torsion is needed.

References:

* [Davis--Okun, Vanishing theorems and conjectures for the l2-homology of
  right-angled Coxeter groups](https://arxiv.org/abs/math/0102104).
* [Labbé--Nevo, Bounds for entries of gamma-vectors of flag homology
  spheres](https://arxiv.org/abs/1612.01169), especially Lemmas 2.1, 2.2,
  3.2, 3.4 and Theorem 3.5.
* [Gal, Real Root Conjecture fails for five and higher dimensional
  spheres](https://arxiv.org/abs/math/0501046), Section 2.2, for the
  low-dimensional context. Real-rootedness is not needed in this proof.

## Counting identities

For a (d-1)-sphere with n vertices and e edges, coefficient extraction gives

    gamma_2 = e - (2d-3)n + 2d(d-2).

Counting independent triples of H by inclusion--exclusion gives

    f_2(Delta) = choose(18,3) - 16m + sum_v choose(q_v,2) - T.

Extracting the third gamma coefficient and using the vertex-link identity
sum_v h_lk(v) = 6h + (1-t)h' yields

    a = 39-m,
    b = 230 + (1/2) sum_v q_v(q_v-11) - T,
    S := sum_v L_v = 3b+4a
       = 846 + (1/2) sum_v q_v(3q_v-37) - 3T.                 (1)

In particular S >= 0. The minimum-vertex bound on four-dimensional links
gives q_v <= 7. No vertex has q_v = 0, since flagness would make Delta a
cone.

For the individual link, let B = V(H) minus ({v} union N_H(v)). Removing
the incident edges gives

    |E(H[B])| = m - sum_(u in N_H(v)) q_u + t_v.

Since |B|=17-q_v, the same low-coefficient formula gives

    L_v = a+8 + q_v(q_v-19)/2
          + sum_(u in N_H(v)) q_u - t_v.                    (2)

We will use a two-vertex version. Suppose uv is a nonedge of H and
N_H(u) and N_H(v) are disjoint. Let z_uv count H-edges between these two
neighborhoods. Then

    E_uv = L_u + L_v - a + (q_u-1)(q_v-1) - z_uv.           (3)

To prove (3), remove {u,v} and their two disjoint neighborhoods. The
remaining set B has 16-q_u-q_v vertices and

    |E(H[B])| = m - sum_(x in N_H(u)) q_x
                 - sum_(x in N_H(v)) q_x + t_u+t_v+z_uv.

Substitute this expression into
E_uv = choose(|B|,2) - |E(H[B])| - 5|B| + 16, and use (2).
Flagness identifies the induced complex on B with the edge link.
More generally, identity (3) is valid in every dimension where the
corresponding gamma_2 coefficients are defined, with a, L and E referring
to the ambient complex and its vertex and edge links.

## First reduction and the three boundary profiles

If all q_v >= 4, then for 4 <= q <= 7,

    q(3q-37)/2 <= -50.

Equation (1) would give S <= 846-18*50 = -54. Thus pi := min q_v <= 3.

Assume pi=3 and let n_j count vertices of complement degree j. Equation
(1) becomes

    S = 90 - 8n_4 - 13n_5 - 15n_6 - 14n_7 - 3T >= 0.     (4)

Put r=n_4+n_5+n_6+n_7. If r>=12 the subtracted weight exceeds 90.
If r=11, its minimum is 88, but the degree sum must be even. Upgrading
eleven degree-four vertices enough to correct its odd excess requires
a degree-five or degree-seven vertex, increasing the weight by at least
five. Hence r<=10, or n_3>=8.

Suppose n_3=8. Then r=10, and parity and (4) give

    n_5+n_7 is even,
    5n_5+7n_6+6n_7+3T <= 10.

There are exactly the following possibilities. Exponents denote vertex
multiplicities, not powers of graphs.

| Complement degree multiset | a | b | possible T |
| --- | ---: | ---: | --- |
| 3^8 4^8 5^2 | 6 | -8 | 0 |
| 3^8 4^9 6^1 | 6 | -7-T | 0,1 |
| 3^8 4^10 | 7 | -6-T | 0,1,2,3 |

In particular, **each boundary profile has b<0**, without assuming that
at the outset.

Whenever pi=3 and b<0, every link at a degree-three complement vertex is
not a suspension. Otherwise Labbé--Nevo's join theorem gives
Delta = Gamma * C_6 with Gamma a flag homology 3-sphere, and therefore
b = 2 gamma_2(Gamma) >= 0, a contradiction. This observation will be
used only in the last profile.

## Elimination of 3^8 4^9 6^1

At the unique degree-six vertex, (2) reads

    L_v = -25 + sum_(u in N_H(v)) q_u - t_v.

All six neighbors have degree at most four, so L_v <= -1. This contradicts
L_v >= 0.

## Elimination of 3^8 4^8 5^2

Here T=0. Let r,s be the two degree-five vertices. At r, (2) reads

    L_r = -21 + sum_(u in N_H(r)) q_u.

The sum is at most 5+4*4=21. Nonnegativity forces r adjacent to s and four
degree-four vertices. The same holds at s. Triangle-freeness makes their
four-element sets disjoint, partitioning the eight quartic vertices into
U and W. Both U and W are independent in H.

Every quartic vertex consequently has exactly one degree-five neighbor.
Equation (2) requires its neighbor-degree sum to be at least sixteen, so
at most one of its other three neighbors is cubic. A cubic vertex has no
degree-five neighbor, and (2) gives L_v=k_v-1, where k_v is its number of
quartic neighbors. Hence it has at least one quartic neighbor. There are
eight cubic and eight quartic vertices, so these cross edges form a
perfect matching. Each quartic vertex has two quartic neighbors, both in
the opposite part U or W. All vertex-link values L_v are zero.

Choose a cubic vertex v matched to w in W, where N_H(r)={s} union U.
The two neighborhoods N_H(r) and N_H(v) are disjoint: the latter consists
of w and two cubic vertices. At least three edges cross between them:
the edge sw and the two edges from w to U. Thus (3) gives

    E_rv = 0+0-6+(5-1)(3-1)-z_rv = 2-z_rv <= -1.

This contradicts the nonnegativity of edge-link gamma_2.

## Elimination of 3^8 4^10

Let C be the eight cubic vertices, Q the ten quartic vertices, and
J=H[C]. Write k_v=|N_H(v) intersect Q| for v in C and
c_h=|N_H(h) intersect C| for h in Q. Equation (2) gives

    L_v = k_v-t_v = 3-deg_J(v)-t_v,       v in C,
    L_h = 1-c_h-t_h,                    h in Q.             (5)

Therefore c_h<=1, and if c_h=1 then t_h=L_h=0. In particular, there is
no mixed triangle between C and Q. Also x=|E_H(C,Q)|<=10, whence

    |E(J)| = (24-x)/2 >= 7.                                (6)

If J has a triangle, each of its vertices must have k_v>=1 by (5).
The triangle already uses two of its three edges, so k_v=1, t_v=1 and
L_v=0. This triangle is a component of J. By (6), another component
contains an edge; choose a nonisolated vertex w there. Then L_w<=2.
For a vertex u in the triangle, the H-neighborhoods of u and w are
disjoint: no cubic neighbor is shared across J-components, and no
quartic vertex has two cubic neighbors. They are nonadjacent in H.
Equation (3) now gives E_uw <= 0+2-7+4 = -1. Thus J is triangle-free,
and t_v=0 for every v in C.

J is also C_4-free. Indeed, opposite vertices u,v of a four-cycle in J
would be nonadjacent (J has no triangles) and share at least two H-neighbors.
In the complement graph of lk_Delta(v), the degree of u would be
3-|N_H(u) intersect N_H(v)| <= 1. Degree zero makes that link a cone;
degree one makes it a suspension. Both are impossible, the latter by
the nonsuspension observation above. Hence J has girth at least five.

We next rule out a degree-three vertex v in J. Such v has no quartic
neighbors and L_v=0. Suppose a quartic vertex h is attached to a cubic
vertex u outside N_J(v). Then L_h=0, v and h are nonadjacent in H, and
their H-neighborhoods are disjoint. Equation (3) gives

    E_vh = 0+0-7+(3-1)(4-1)-z_vh = -1-z_vh < 0.

Consequently every C--Q edge must meet N_J(v). All four vertices of
R=C minus ({v} union N_J(v)) therefore have degree three in J. But
C_4-freeness allows each vertex of R at most one neighbor in N_J(v),
and J[R] has at most three edges (a four-vertex graph of girth at least
five is a forest). Counting degrees on R gives the contradiction

    12 = 2|E(J[R])| + |E_J(R,N_J(v))| <= 6+4 = 10.

Thus J has maximum degree two. Together with eight vertices, girth at
least five and (6), this leaves precisely

    P_8, C_8, C_7 disjoint union K_1,
    C_6 disjoint union P_2, C_5 disjoint union P_3.

Every one contains two degree-two vertices u,v at distance at least three
or in different components. They have L_u=L_v=1. Their H-neighborhoods
are disjoint: no cubic neighbor is shared at that distance, and no
quartic vertex has two cubic neighbors. Again (3) gives

    E_uv = 1+1-7+(3-1)(3-1)-z_uv = -1-z_uv < 0.

This eliminates the last profile and proves n_3>=9.

## Charney--Davis scope and remaining frontier

If pi=1, Delta is a suspension and b=0. If pi=2, the two-antipode
decomposition quoted above gives b=gamma_2(lk(xy))>=0. Thus a negative
example must have pi=3; the theorem and the nonsuspension observation
give the stated consequence.

No existence of a negative example, or classification at n_3>=9, is
asserted. The next concrete frontier is the remaining degree profiles
with nine cubic complement vertices, where the clean ten-quartic
attachment argument no longer applies verbatim.

The graph source was the accepted seventeen-vertex proof and its review,
whose suggested frontier was eighteen vertices. The normalization repair
in that neighborhood was incorporated. The new argument does not assume
the seventeen-vertex theorem. Targeted searches of the primary sources
above and the committed Discovery Net neighborhood did not locate this
nine-vertex refinement; this is search-relative novelty, not a priority
claim. The general conjecture remains unresolved here.

## Computational trust boundary

`verify.py` independently counts faces and induced links to check (1)--(3),
checks the boundary-profile list, verifies the final degree-two component
list, and checks the explicit join examples. These are supplementary
checks, not an enumeration of all eighteen-vertex spheres or a homology
verification. The theorem rests on the argument above and its named
literature inputs. There is no solver verdict, external graph census,
floating-point computation, or proof-assistant formalization in that proof.
