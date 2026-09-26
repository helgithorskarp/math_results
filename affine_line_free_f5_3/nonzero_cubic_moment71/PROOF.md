# The centered cubic moment cannot vanish at 71 points

Polynomial and vector calculations are over \(\mathbb F_5\).
Cardinalities, deficits, and certificate inequalities use ordinary
integers or reals as indicated.

**Theorem.** Let \(S\subseteq\mathbb F_5^3\) have 71 points and contain
no complete affine line. Set
\[
 \mu=\sum_{x\in S}x,\qquad
 T(v)=\sum_{x\in S}\bigl(v\cdot(x-\mu)\bigr)^3.
\]
Then the homogeneous cubic \(T\) is not the zero polynomial.

Since \(71=1\) in the field, \(\mu\) is the barycenter. Under
\(x\mapsto Ax+t\), the centered cubic becomes \(T(A^{\mathsf T}v)\).
Its nonvanishing is an affine invariant. No symmetry of \(S\) is assumed.

**Corollary.** At least 15 projective directions \(v\) satisfy
\(T(v)\ne0\). If there are exactly 15, then \(T\) is a product of three
distinct rational linear forms whose projective zero lines concur.

This computer-assisted necessary condition does not decide whether
71-point sets exist. The exact maximum remains unresolved between
70 and 71.

## 1. Moments and deficit residues

The direct census in `planar_cap.cpp` tests all
\(\binom{25}{17}=1,081,575\) planar 17-subsets against all 30 affine
lines, finding none line-free. Every plane section of \(S\) therefore
has size at most 16 and at least \(71-4\cdot16=7\).

Translate by \(\mu\), so the first moment is zero, and suppose \(T=0\).
Write
\[
 Q(v)=\sum_{x\in S}(v\cdot(x-\mu))^2,\qquad
 U(v)=\sum_{x\in S}(v\cdot(x-\mu))^4.
\]
For a projective normal representative \(v\), set
\[
 m(v,t)=|\{x\in S:v\cdot(x-\mu)=t\}|,\qquad
 \delta(v,t)=16-m(v,t).
\]
The deficits lie in \([0,9]\) and their parallel sum is nine.
Expanding the field-valued indicator \(1-(t-v\cdot(x-\mu))^4\),
using the zero first and third moments, gives
\[
 \delta(v,t)\equiv t^4+t^2Q(v)+U(v)\pmod5. \tag{1}
\]

For \(q=Q(v),u=U(v)\), let
\[
 r_{q,u}(t)=[t^4+qt^2+u]_5\in\{0,1,2,3,4\},
\]
where brackets mean the least nonnegative representative.
Its sum is four modulo five and at most nine. The exact possibilities are
\[
 \begin{array}{c|c}
 q&\text{allowed }u\\ \hline
 0&0,1,4\\
 1,4&0,1,3\\
 2,3&1,2,3
 \end{array}. \tag{2}
\]
For these pairs the residue sum is four or nine. When it is nine,
\(\delta=r\). When it is four, precisely one plane receives an extra five:
\[
 \delta(v,t)=r_{q,u}(t)+5z_{v,t},\qquad
 z_{v,t}\in\{0,1\},\qquad \sum_tz_{v,t}=1. \tag{3}
\]
Directions with residue sum nine have no \(z\) variables.
The verifier independently enumerates all 715 compositions of nine
into five deficits and imposes zero first and third moments.
It obtains the same 39 labeled profiles as (1)--(3).

There is a useful algebraic description of (2). Put \(V=U+2Q^2\).
On \(Q=0\), \(V\) is square-valued. On \(Q\ne0\), either \(V=0\) or
\[
 \chi(V)=-\chi(Q), \tag{4}
\]
where \(\chi\) is the quadratic character. Thus the sextic
\(2Q(U+2Q^2)\) is square-valued at every rational point.
This is a value condition, not an assertion of factorization as a square.
For nonsquare rank-one \(Q\), the translation \(U\mapsto U+2Q^2\)
is a bijection with square-valued ternary quartics. The verifier checks
this identity on the complete two evaluation catalogues.

## 2. A complete quartic cover

A symmetric quadratic form in three variables over \(\mathbb F_5\)
is congruent to one of the diagonal forms
\[
 (0,0,0),\ (1,0,0),\ (2,0,0),\ (1,4,0),\
 (1,2,0),\ (1,1,1),\ (1,1,2). \tag{5}
\]
They represent rank zero, the two rank-one classes, split and
anisotropic rank two, and the two rank-three determinant classes.

`quadratic.py` supplies and checks an invertible basis change for
each of the \(5^6=15,625\) symmetric matrices. It diagonalizes using
a nonisotropic vector, scales each nonzero entry to 1 or 2, and
replaces each pair \((2,2)\) by \((1,1)\) using
\(\begin{pmatrix}2&2\\2&3\end{pmatrix}\).
A final scaling gives the chosen split representative \((1,4,0)\).
The resulting congruence is checked entry by entry. The zero form
is included.

Fix one representative \(Q\). Evaluate the 15 degree-four monomials
at the 31 projective representatives whose first nonzero coordinate
is one. An exactly checked invertible 15-row minor shows that a
quartic is uniquely determined by its 15 information values.
Each value has three choices in (2).
The native enumerator visits all \(3^{15}=14,348,907\) information
words for each of the seven forms and checks all 31 coordinates.
There is no symmetry quotient at this stage.

Two integer identities discard many quartics. There are 155 planes,
31 through a point, and six through two distinct points. Therefore
\[
 \sum_Hm_H=2201,\qquad
 \sum_Hm_H^2=31\cdot71+6\cdot71\cdot70=32021,
\]
and
\[
 \sum_H\delta_H^2=1269. \tag{6}
\]
Writing \(\epsilon=1_{\{\mu\in S\}}\), the 31 central planes satisfy
\[
 \sum_{H\ni\mu}\delta_H=70-25\epsilon. \tag{7}
\]

For each direction, list the allowed pairs
\((\sum_t\delta(v,t)^2,\delta(v,0))\) from (3).
An exact dynamic program adds these pairs across all 31 directions
and retains a quartic only if it reaches \((1269,70-25\epsilon)\).
Intermediate sums are nonnegative, so pruning sums above the target
bounds is sound. The statistics for \(q=1,4\) agree, as do those for
\(q=2,3\), by rescaling the normal. No arc, conic, seven-plane bound,
or earlier moment theorem is used.

| Diagonal \(Q\) | Locally allowed quartics | After (6),(7) | Subgroup orbits | \(\epsilon\)-cases |
|---|---:|---:|---:|---:|
| \(0,0,0\) | 10603 | 930 | 1 | 2 |
| \(1,0,0\) | 7843 | 91 | 3 | 5 |
| \(2,0,0\) | 10603 | 31 | 2 | 2 |
| \(1,4,0\) | 7097 | 308 | 14 | 17 |
| \(1,2,0\) | 6495 | 78 | 2 | 4 |
| \(1,1,1\) | 4839 | 192 | 4 | 4 |
| \(1,1,2\) | 6285 | 51 | 3 | 3 |
| **Total** | **53765** | **1681** | **29** | **37** |

The orbit reduction uses verified isometries of \(Q\). For \(Q(a)\ne0\),
\[
 v\longmapsto v-\frac{2\,v^{\mathsf T}Da}{a^{\mathsf T}Da}\,a
\]
preserves the diagonal matrix \(D\). Additional explicit generators
act invertibly on the radical; three elementary linear maps are used
when \(Q=0\). Every generator satisfies the checked identity
\(g^{\mathsf T}Dg=D\). Any such subgroup suffices; completeness of
the full isometry group is not assumed.

The change \(U\mapsto U\circ g\) corresponds to \(S\mapsto g^{\mathsf T}S\).
It preserves line-freeness, \(Q\), zero cubic moment, and origin membership.
It does not assume that the original set has this symmetry.
Every one of the 1,681 surviving words belongs to exactly one of
the 29 subgroup orbits. An independently evaluated matrix transport
is checked for every word, using the original quartic monomials
on transformed vectors instead of composing projective permutations.
The permitted origin-membership values yield precisely 37 cases.

## 3. Global point and line inequalities

Fix one \(Q,U,\epsilon\). Index the 155 planes by the projective normal
and then by \(t=0,1,2,3,4\). Let \(r_H\) be their residues.
The variables \(z\) from (3) are nonnegative and have sum one within
each eligible parallel class.

Write \(P_yz=\sum_{H\ni y}z_H\) and
\(L_\ell z=\sum_{H\supset\ell}z_H\), interpreting absent variables as zero.
The exact point-star identity is
\[
 \sum_{H\ni y}\delta_H=70-25\,1_S(y).
\]
With \(K_y=(70-\sum_{H\ni y}r_H)/5\), this gives
\(P_yz+5\,1_S(y)=K_y\), hence
\[
 P_yz\le K_y,\qquad -P_yz\le5-K_y. \tag{8}
\]

For a line \(\ell\) containing \(k_\ell\) selected points, its six
incident planes have total section size \(71+5k_\ell\). Therefore
\[
 \sum_{H\supset\ell}\delta_H=25-5k_\ell.
\]
Line-freeness gives \(k_\ell\le4\), so
\[
 -L_\ell z\le\frac{\sum_{H\supset\ell}r_H}{5}-1. \tag{9}
\]
All divisions by five in (8),(9) are exact; the verifier checks this.
Their divisibility also follows by restricting the homogeneous
residue polynomial to a projective line or by summing degree-four
monomials on a projective plane.

At the origin we impose
\[
 P_0z=K_0-5\epsilon. \tag{10}
\]
Since actual \(z_H\) are zero or one, the energy identity (6) is
\[
 \sum_H(25+10r_H)z_H=1269-\sum_Hr_H^2. \tag{11}
\]
It is sound to relax \(z\) to nonnegative reals while retaining
(8)--(11) and the parallel-class equalities.
Every actual set yields a feasible vector. No converse or sufficiency
of local plane data is assumed.

## 4. Thirty-seven exact contradictions

Let \(Cz\le d\) contain the 1,029 inequalities, in this row order:

1. 125 upper point inequalities \(P_yz\le K_y\);
2. 125 lower point inequalities \(-P_yz\le5-K_y\);
3. 775 line inequalities (9);
4. both signs of (10);
5. both signs of (11).

Let \(Dz=\mathbf1\) be the parallel-class equalities.
All matrices and right-hand sides are regenerated from the definitions.
For each case, [certificates.json](certificates.json) gives integer
vectors \(\lambda,y\) with
\[
 \lambda\ge0,\qquad C^{\mathsf T}\lambda+D^{\mathsf T}y\ge0,\qquad
 d^{\mathsf T}\lambda+\mathbf1^{\mathsf T}y<0. \tag{12}
\]
A feasible \(z\ge0\) would imply
\[
 0\le(C^{\mathsf T}\lambda+D^{\mathsf T}y)^{\mathsf T}z
 \le d^{\mathsf T}\lambda+\mathbf1^{\mathsf T}y<0,
\]
a contradiction.

The verifier checks all 4,180 column inequalities with arbitrary-precision
integers. The 37 certificates contain 1,050 nonzero multipliers in total,
all of absolute value at most 155. Each right-hand side in (12) is
at most \(-50\) and is recomputed exactly.
Missing cases, incorrect multiplier signs, and changed contradictions
are rejected. An optimizer is needed only for optional rediscovery;
its output is accepted only after the integer conditions (12) pass.

Every possible \(Q,U,\epsilon\) under \(T=0\) is excluded.
This proves the theorem.

## 5. Directional consequence

A nonzero ternary cubic has at most 16 rational projective zeros.
Without a rational linear factor, its restriction to each rational
line has at most three zeros. Counting through one zero gives at most
\(1+6\cdot2=13\); if there are no zeros the bound is immediate.

With a rational linear factor, the remaining quadratic has a
nonsingular conic, an isolated point, a repeated line, or two lines
as its rational zero set. The only way to reach 16 distinct zeros
is three distinct concurrent rational lines, giving \(6+5+5=16\).
Three nonconcurrent lines give 15; all other cases give fewer.
This proves the corollary and its equality statement.

In tensor coordinates, the ten symmetric degree-three moments of
\(x-\mu\) cannot all vanish. The multinomial coefficients \(1,3,6\)
are nonzero in characteristic five, so this is equivalent to the
polynomial statement.

## Scope and trust boundary

The proof is self-contained after the locally rechecked planar cap.
It assumes no 72-point SAT exclusion, two-low-plane certificate,
nonzero quadratic-moment theorem, conic inequality, or affine
asymmetry theorem. All candidate data are regenerated from small-field
polynomials and incidence geometry.

Trust remains in the written reduction, exact Python/C++ implementations,
and compiler execution. This is not a proof-assistant formalization.
Replay uses no optimizer, floating-point inference, external classification,
or opaque solver trace. The full quartic catalogues are regenerated
locally and are not repository artifacts.

A nonzero cubic still leaves many possible 71-point candidates.
This contribution does not settle the campaign's exact-value target.
