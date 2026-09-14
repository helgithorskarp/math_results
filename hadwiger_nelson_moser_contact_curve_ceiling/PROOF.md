# Contact-polynomial multiplicity in the independent three-Moser sum

## 1. Exact contact equations

Put

\[
 M=\{0,1,\rho,1+\rho,\eta,\eta\rho,\eta(1+\rho)\},
 \quad \rho=(1+i\sqrt3)/2,\quad \eta=(5+i\sqrt{11})/6.
\]

The 343 formal addresses `(i,j,k)` represent

\[
 P_{ijk}=M_i+uM_j+vM_k,\qquad |u|=|v|=1.
\]

For two addresses let

\[
 a=M_i-M_{i'},\quad b=M_j-M_{j'},\quad c=M_k-M_{k'}.
\]

Expanding `|a+ub+vc|^2=1` gives the real Laurent equation

\[
 F_{a,b,c}(u,v)=C+pu+\bar p u^{-1}+qv+\bar qv^{-1}
                    +r u/v+\bar r v/u=0, \tag{1}
\]

where

\[
 C=N(a)+N(b)+N(c)-1,\quad p=b\bar a,\quad q=c\bar a,
 \quad r=b\bar c.
\]

All coefficients lie in
`E=Q(sqrt(33), i sqrt(3))`. Two formal pairs belong to the same contact class
when their seven displayed coefficients are proportional by a nonzero exact
scalar. `model.py` canonicalizes a class by dividing every coefficient by the
first nonzero one. Including the conjugate coefficients makes this equivalent
to real scalar proportionality for these Hermitian equations.

If all cross coefficients vanish, (1) is constant. Exact enumeration separates
1,617 identically zero equations—the Cartesian unit edges—from 1,470 constant
noncontacts. The remaining pairs form 18,828 nonconstant classes. At a phase
on one class, every formal pair counted in that class is a unit edge; other
classes may meet it and add further edges.

## 2. Why every high-multiplicity unit triple is a collision locus

Suppose `a`, `b`, and `c` are all unit vectors. At a phase, set

\[
 x=a,\qquad y=ub,\qquad z=vc.
\]

After rotating so that `x=1`, write `y=e^{iA}` and `z=e^{iB}`. Then

\[
 |x+y+z|^2-1
 =2(1+\cos A+\cos B+\cos(A-B))
 =8\cos(A/2)\cos(B/2)\cos((A-B)/2). \tag{2}
\]

Thus `|x+y+z|=1` forces `x=-y`, `x=-z`, or `y=-z`. In the first case,
for example, `a+ub=0`; using the same third coordinate on the two formal
addresses produces a collision in `M+uM+vM`. The other cases are identical.
Consequently every point of a unit-triple contact class lies on a formal
collision locus. No such class can create an edge in an injective support.

This implication is global and analytic; it is not inferred from sampled
phases or numerical root finding.

## 3. Exact finite census

Among classes with all three differences nonzero but not all three unit, the
exact multiplicity distribution is:

| Formal edge multiplicity | Classes |
|---:|---:|
| 1 | 8,360 |
| 2 | 6,952 |
| 3 | 96 |
| 4 | 1,632 |
| 5 | 144 |
| 6 | 192 |
| 8 | 96 |

There is no class of multiplicity seven or above eight. Therefore eight is the
sharp ceiling for a single non-collision-tautological three-factor contact
class, attained by exactly 96 classes.

The full class inventory is checked by two exact enumerations. The direct
route examines every unordered pair of the 343 addresses. The factorized route
first records every exact one-factor displacement and its ordered endpoint
multiplicity, iterates displacement triples, multiplies their weights, and
divides the final orientation-symmetric counts by two. The resulting class
dictionaries—including exact canonical polynomial keys, multiplicities,
active-factor counts, and unit-triple flags—must be identical. Their canonical
serialization has SHA-256

`6003281b13f03b2cc844384fa8c5da3db8c449bea303458ff68857bec3d4915c`.

Three corruption controls alter a multiplicity, alter a class flag, and break
the global pair partition; all are rejected.

## 4. Scope and construction consequence

The theorem bounds one contact-polynomial class, not the total number of edges
at an intersection of several classes. It does not assert that the whole
independent two-phase family is four-colourable.

For the construction campaign, it gives a precise boundary: no injective
343-point member can gain more than eight formal edges by moving onto only one
genuine three-factor contact equation. A plausible dense candidate must lie at
an intersection of several such equations. The companion discovery pass
therefore exhaustively screened pairwise intersections of the 96 maximal
classes before the architecture pivot; that floating/SAT screen is not part of
this theorem.

Trust remains in the unformalized derivation of (1), the exact Python
enumerations, and the imported exact field implementation. The identity (2)
is ordinary analytic algebra. No floating-point predicate, SAT result, or
abstract graph realization is used in the proof.
