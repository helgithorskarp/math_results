# The cyclic thirteen-vertex core: forced separation, two Gram branches

Authoring agent: **six-tammes-2**, role: **researcher**. Date: 2026-09-30.
Status: complete author-audited hand proof with exact arithmetic checks;
independent mathematical review is pending.

This adds a second forbidden contact motif for a strictly better Tammes-15
packing. Like the [asymmetric core](CONTACT_CORE.md), it needs only thirteen
vertices and twenty-four prescribed contacts. Its arbitrary unit-vector
realizations have **two** labeled Gram matrices. Only one obeys the packing
inequalities. This branch distinction is part of the result; uniqueness
without those inequalities would be false. The global numerical bounds and
optimality of fifteen points remain unchanged.

The incumbent packing, its separation quintic, and its exact construction
are prior work. The contribution is the smaller sufficient cyclic contact
pattern, its two-branch classification, and a compact checkable obstruction.
No historical-priority claim is made.

## Graph and statement

The vertex set is

```
{0,1,2,4,5,6,7,8,9,10,11,12,13}.
```

Begin with complete triangles on `(0,5,11)` and `(1,2,4)`. A tuple
`(n,i,j,o)` adds edges `ni,nj`; the old triangle `(i,j,o)` already has
all three edges.

| Block | Tuples |
|---|---|
| A | `(6,0,11,5) (7,0,5,11) (9,5,11,0) (12,5,7,0) (13,11,9,5)` |
| B | `(8,2,4,1) (10,1,2,4)` |

Add cross edges

```
(6,8) (13,8) (9,10) (12,10).
```

This graph K has 13 vertices and 24 edges: 13 in A, 7 in B, and 4 cross
edges. It is obtained from the known cyclic incumbent contact graph by
removing vertices 3 and 14. The name describes that incumbent and imposes
no symmetry on an input realization.

Put

\[
F(t)=13t^5-t^4+6t^3+2t^2-3t-1,
\]

and let \(t_0\) be its unique root in \((1/2,3/5)\). An exact bracket is

```
0.59260590292507377809642492233275 < t0
t0 < 0.59260590292507377809642492233276.
```

**Theorem.** Suppose thirteen **distinct** unit vectors in \(\mathbb R^3\)
are labeled by K and have inner product t on every prescribed edge, with
\(1/2<t<3/5\). Then \(t=t_0\). There are exactly two possible complete
labeled Gram matrices, up to \(O(3)\), explicitly described below. Both
are realized by distinct unit vectors. One is the incumbent restriction.
In the other, the unprescribed pair \((1,9)\) has inner product greater
than \(49/50\). Thus imposing the packing inequalities
\(p_i\cdot p_j\le t\) for all pairs selects exactly the incumbent Gram
matrix. No symmetry, proximity, or planarity is assumed.

**Tammes-15 consequence.** A packing of fifteen points with strictly larger
minimum geodesic separation than the incumbent cannot contain K in its
contact graph under any injection of the thirteen labels. The other two
points may be arbitrary and additional contacts do not evade the exclusion.
For such a packing with minimum separation d, strict improvement gives
\(\cos d<t_0<3/5\). Fifteen disjoint open caps of radius \(d/2\) give
\(\cos d\ge113/225>1/2\). The theorem would force \(\cos d=t_0\).
There is no assertion that every better packing contains K.

**Packing completion corollary.** Add vertices 3 and 14 with tuples
`(3,1,4,2)` and `(14,0,6,11)` but neither cross edge `(3,7)` nor `(3,14)`.
If all fifteen points obey the packing inequalities as well as these 28
prescribed contacts in the same interval, their full labeled Gram matrix is
the cyclic incumbent's, and both omitted contacts are restored. The core
first selects the incumbent branch; each added point is then a forced
reflection. The packing hypothesis is retained in this corollary.

## Reflection reduction

Let \(H=(1-t)I+tJ\), with positive eigenvalues
\(1-t,1-t,1+2t\). Both anchor triangles are bases. For an equilateral
triangle \((i,j,o)\), its old point is outside
\(\operatorname{span}(p_i,p_j)\), since its Gram determinant is
\((1-t)^2(1+2t)>0\). The unit sphere and the two contact planes have
exactly two intersections. Distinctness forces the new one to be

\[
p_n=\frac{2t}{1+t}(p_i+p_j)-p_o. \tag{1}
\]

Recursively define coefficient vectors \(a_i,b_j\) in the two anchor
bases by (1). Put \(P=(p_0\ p_5\ p_{11})\), so \(P^TP=H\), and
write \(p_i=Pa_i\) in A. The pair \((p_8,p_{10})\), as defined within
B, has inner product

\[
\kappa=\frac{t(9t^2-2t-3)}{(1+t)^2}. \tag{2}
\]

The two A pairs \((p_6,p_{13})\) and \((p_9,p_{12})\) have the same
inner product

\[
w=\frac{16t^4-7t^3-5t^2+3t+1}{(1+t)^3}.
\]

The old common unit neighbors of these pairs are respectively \(p_{11}\)
and \(p_5\), with both required inner products t. Each old-neighbor triple
has Gram determinant

\[
E=\frac{16t^2(1-t)^2(2t+1)(t^2-2t-1)^2}{(1+t)^6}>0. \tag{3}
\]

In particular the old neighbor is not in its pair's plane. Moreover

\[
1-w=\frac{8t^2(1-t)(2t+1)}{(1+t)^3}>0,\qquad
1+w=\frac{2Q_4}{(1+t)^3}>0,
\]

where \(Q_4=8t^4-3t^3-t^2+3t+1\). The pairs are independent and
nonantipodal. Their cross contacts, and distinctness from the respective
old neighbors, therefore force

\[
\begin{aligned}
p_8&=Pv_8,&v_8&=\frac{2t}{1+w}(a_6+a_{13})-a_{11},\\
p_{10}&=Pv_{10},&v_{10}&=\frac{2t}{1+w}(a_9+a_{12})-a_5.
\end{aligned} \tag{4}
\]

Both points are fixed in the A anchor frame. This step removes only
coincident-neighbor branches, not a choice of the B anchor orientation.

## Scalar obstruction

Equations (2) and (4) give the necessary condition
\(v_8^THv_{10}-\kappa=0\). Its exact rational-function factorization is

\[
v_8^THv_{10}-\kappa
=\frac{-2t(t-1)(2t+1)C_3(t)F(t)}{(t+1)^2Q_4(t)^2},\qquad
C_3=11t^3-5t^2-11t-3. \tag{5}
\]

Every factor except F is nonzero throughout the closed interval
\([1/2,3/5]\). The checker certifies strict polynomial signs by exact
Bernstein coefficients and audits all geometric divisors before division.
It reconstructs the reflected blocks and the left side of (5) with integer
rational functions, checks the proposed numerator and denominator, and
checks the displayed factorization independently of the CAS generator.
There is no numerical root test, solver verdict, or omitted exceptional
parameter in this inference. Thus \(F(t)=0\).

Strictly positive Bernstein coefficients of \(F'\), opposite endpoint
signs, and opposite signs at the stated rational bracket show that the only
possibility is \(t=t_0\).

## Exactly two labeled Gram matrices

At \(t_0\), fix the A anchor basis P. The [parent exact
certificate](certificate.json) supplies the cyclic incumbent with B anchor
basis \(Q_0\) satisfying

\[
Q_0=P H^{-1}M,\qquad
M=\begin{pmatrix}a&b&c\\c&a&b\\b&c&a\end{pmatrix},
\]

where

\[
\begin{aligned}
a&=(117t^4-48t^3+70t^2-6t-27)/2,\\
b&=(195t^4-106t^3+136t^2-38t-31)/4,\\
c&=(-429t^4+202t^3-276t^2+42t+81)/4.
\end{aligned}
\]

All quantities in this section are evaluated at \(t_0\). The parent
checker verifies \(M^TH^{-1}M=H\), exact unit norms, all 30 contacts and
strict noncontact separation for the incumbent. The new checker also
verifies \(Q_0b_8=Pv_8\) and \(Q_0b_{10}=Pv_{10}\) modulo F.

For any input B anchor basis Q, the linear map \(Q Q_0^{-1}\) is
orthogonal since both anchor Gram matrices are H. It fixes the two vectors
in (4). They span a plane because \(1-\kappa^2>0\). An orthogonal map
fixing that plane pointwise is either the identity or the reflection T in
that plane: its action on the one-dimensional perpendicular space is +1
or -1. These exhaust every remaining branch.

Let \(X=(v_8\ v_{10})\) and
\(G=\begin{pmatrix}1&\kappa\\\kappa&1\end{pmatrix}\). The two
complete labeled configurations have A coefficient vectors \(a_i\), and
respectively B coefficient vectors

\[
x_j=H^{-1}Mb_j,\qquad
x'_j=Sx_j,\qquad S=2XG^{-1}X^TH-I. \tag{6}
\]

This S is the coefficient matrix of T. In scalar form its projection
coefficients are

\[
q_8=\frac{x\cdot_H v_8-\kappa x\cdot_H v_{10}}{1-\kappa^2},\qquad
q_{10}=\frac{x\cdot_H v_{10}-\kappa x\cdot_H v_8}{1-\kappa^2},
\quad Sx=2(q_8v_8+q_{10}v_{10})-x.
\]

Equation (6) describes every Gram entry: within A use \(a_i^THa_k\);
within B use \(b_j^THb_l\); across the blocks use either
\(a_i^TMb_j\) or \(a_i^THS H^{-1}Mb_j\).

The checker verifies all unit norms and all 24 prescribed contacts for
both branches, and preservation of the B Gram matrix under S, modulo F.
Within-block distinctness follows from the parent realization and the
orthogonal reflection. For every reflected cross-block pair it certifies
\(1-a_i^THx'_j>0\) by exact rational interval evaluation over the root
bracket. Hence the reflected configuration really consists of thirteen
distinct points. It is not discarded as an unproved coincidence case.

The same exact interval evaluation proves

\[
p'_1\cdot p_9>49/50. \tag{7}
\]

The incumbent has this unprescribed pair below \(17/40\). Thus the two
Gram matrices differ, and (7) excludes the reflected branch under the
packing inequalities, since \(t_0<3/5<49/50\). All other potential pairs
need not be checked for that exclusion. The incumbent branch satisfies
every packing inequality by its checked exact construction.

## Reproduction and trust boundary

With Python 3.11 or later, from the repository root:

```sh
python3 -B tammes15_contact_pattern_obstruction/verify_cyclic_contact_core.py --selftest
python3 -B -O tammes15_contact_pattern_obstruction/verify_cyclic_contact_core.py --selftest
```

The [321-byte certificate](certificate_cyclic_contact_core.json) contains the
scalar residual numerator/denominator and a pair/bound witnessing the packing
violation. The self-test corrupts a residual coefficient and substitutes a
prescribed contact for the packing witness; both must be rejected. It also
checks root identity and nonidentity controls. Mathematical checks use
explicit exceptions and survive optimized Python.

Optional regeneration, with SymPy 1.14.0:

```sh
python3 -B tammes15_contact_pattern_obstruction/generate_cyclic_contact_core_certificate.py
python3 -B tammes15_contact_pattern_obstruction/verify_cyclic_contact_core.py --selftest
```

The generator proposes the residual coefficients without reading the
certificate. The checker uses standard-library integer polynomial arithmetic
and rational interval evaluation; it does not require SymPy. Regeneration is
byte-identical. The certificate SHA-256 is

```
f9529c639d6d2d12df3a59b3182cb9ed2e47cf98c8db31da47eade3acd773cda
```

All library thread counts are one and the small jobs run sequentially.
The source includes the geometric reduction, the exact rational-function
helper, the polynomial helper, and the parent existence certificate. The
new necessary direction does not assume the old full-contact classification;
that certificate identifies the explicit incumbent for the branch analysis.
No optimizer, tolerance, external coordinate file, private proof corpus, or
large generated artifact is needed. This is a written proof with exact
arithmetic checks, not a proof-assistant formalization.

## Prior work and complementary scope

The incumbent and F are recorded in [Cohn's
table](https://spherical-codes.org/) and the
[fifteen-point coordinate file](https://spherical-codes.org/data/3/15).
Its optimality is not marked proved. Primary construction references are
Kottwitz (1991), DOI `10.1107/S0108767390011370`, and
Buddenhagen–Kottwitz, Section 4, pp. 7–11 of the archived construction
manuscript linked in the parent README. Their symmetric eighteen-point
antecedent is not an assumption about an input to this theorem.
[Musin–Tarasov, arXiv:1410.2536](https://arxiv.org/abs/1410.2536) settles
fourteen points. Hars's *Numerical Solutions of the Tammes Problem*, Section
10.15, computes the incumbent distance assuming its displayed full graph;
the smaller arbitrary core theorem is not in the inspected section.
Targeted primary searches are bounded evidence and establish no priority.

The sibling [asymmetric core theorem](CONTACT_CORE.md), source commit
`c25479d5c21ac31ef1b64eb5619dd5cda18619ec`, has one arbitrary labeled
Gram branch. The cyclic core has two and needs the packing inequalities to
select one. The two motifs can both be used as necessary exclusions in a
justified contact-graph cover of strictly better fifteen-point packings.

The complementary [eight-quadrilateral refinement by
six-tammes-1](https://github.com/helgithorskarp/math_results/blob/main/tammes15_eight_quad_reduction/TWO_FIVES.md),
source commit `a6d0b907b54f897ea358043bf2e44fe5ca0c37a3`, leaves 29
necessary degree/deficit profiles and 17 auxiliary types under its stated
complete connected convex triangle/quadrilateral cellular hypotheses and
degrees 3–5. Those structures are not asserted realizable. Its geometry is
cited rather than assumed here. Neither result supplies a complete global
contact-graph enumeration.
