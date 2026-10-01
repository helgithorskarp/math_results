# A two-dimensional conditional receiving patch for original J74

**six-rupert-2, researcher; 2026-10-01.** Author-checked exact finite
hypotheses and complete written real-parameter proof. Unformalized and
independently unreviewed. The full Rupert property of J74 remains **OPEN**.

Let `K=conv(V)` be the original unit-edge J74 metabigyrate
rhombicosidodecahedron in [model.py](../model.py). Its exact constructive
named-solid identification is the [original geometry](../PROOF.md), source
`25fc9695745b6832d068d18544452b7852b5847f`, graph
`bafkreig4wvsmlau4koaib63i3cefofih67cczseu3hgdv2r6r54ga572aq`.
All sixty originals, both asymmetric cupola replacements, proper motions
and actual translations are retained. The body is not assumed centrally
symmetric. All originals have norm `R`, with

\[
 R^2=(11+4\sqrt5)/4,\qquad R<9/4.
\]

## 1. Domain, theorem and exact scope

Write `phi=(1+sqrt5)/2` and define

\[
 \begin{split}
 m&=(1,-\phi,-\phi^2)/(2\phi),\\
 d&=((-5+3\sqrt5)/8,(11-3\sqrt5)/8,-1/4),\\
 e&=m\times d=(\sqrt5/4,(-3+\sqrt5)/8,(-9+5\sqrt5)/8),\\
 u(t,s)&=m+td+se,\qquad 3/5\le t\le7/10,
                   \quad |s|\le\varepsilon=1/50000.
 \end{split}                                                     \tag{1}
\]

The raw coordinate `s` is neither a unit-normal chord nor an angle.
Put `P_u=I-uu^T/(u.u)` and `M_u=I-2uu^T/(u.u)`. Let
`G=diag(-1,-1,1)`, `Hx=diag(-1,1,1)`, `Hy=diag(1,-1,1)` and set

\[
       \mathcal S(u)=\{I,G,M_u H_x,M_u H_y\}.                    \tag{2}
\]

All these are proper motions. The checker verifies the full-body
symmetries on all60 original vertices. Every center in(2) has exactly
the receiver shadow, since `P_u M_u=P_u`.

**Theorem.** Take any real `(t,s)` in the closed rectangle(1), any
`S in S(u)`, `Q in SO(3)`, `lambda>=1`, and any physical `b in u-perp`.
Suppose the relative proper motion has the Cayley representation

\[
 QS^T=(I+[c]_\times)(I-[c]_\times)^{-1},
               \qquad \|c\|\le1/14400.                        \tag{3}
\]

Then

\[
 \lambda P_u(QK)+b\subseteq P_uK
       \quad\Longleftrightarrow\quad Q=S,\ \lambda=1,\ b=0.
                                                                    \tag{4}
\]

Thus strict passages are excluded in four **conditional source-motion
neighborhoods** at every receiver of this genuinely two-dimensional
patch. The Cayley norm in(3) is the tangent of half the relative rotation
angle. It is not a bound on every possible source or a receiving radius.
No all-source receiving classification or global non-Rupert theorem
follows. All boundaries and arbitrary scale and physical translation
are included.

Every projective unit normal in(1) is chord **greater than1/3** from
each of the six global minimum axes. Moreover the explicit normal at
`(t,s)=(13/20,1/50000)` is chord **greater than1/200000** from the
entire projective parent arc `s=0`; Section6 proves this.

The direct premise is the [conditional arc proof](../nonlocal_arc_wrench/PROOF.md),
source `03e077716c0a21496133189eee3ba5444cb77555`, graph
`bafkreihs43shk7p73kl327xg73lvh32elxxl5f6qg5o64mzeayyqkgoprm`.
At `s=0` that result has the larger source Cayley radius `1/6000`.
The present patch adds receiving directions while using the smaller
radius in(3); it does not replace the parent's stronger source radius.

## 2. Complete original receiver and parent stress hypotheses

The fixed receiving cycle is

```
17,32,44,8,28,10,46,54,26,23,35,51,15,31,13,49,57,21
```

For an oriented physical edge `v_a->v_b`, put

\[
 \Delta_i=v_b-v_a,\qquad
 a_i(u)=\Delta_i\times u,\qquad h_i(u)=a_i(u)\cdot v_a.       \tag{5}
\]

Every `Delta_i` has length one. At all four closed corners of(1), the
checker tests all60 original inequalities
`a_i dot(v_a-v)>=0`, with strict inequality for every original except
the two incident endpoints. All supports are positive. Since these
quantities are affine in `(t,s)`, their signs persist on the whole real
rectangle. Each projected edge has nonzero length because its normal
and support are nonzero. The listed distinct corners and supporting
edges form the complete convex boundary: every listed edge supports all
originals and has exactly its two incident endpoints on its line.
Thus(5) defines the full original shadow, not a selected prototype.

Also `u_z<0` and `||u||<9/8` at all four corners. The first condition
extends affinely and the norm bound extends by norm convexity. Consequently
the physical translation chart below is valid everywhere. The checker
verifies `e perpendicular m,d`, `||m||=1`, and

\[
        0<\|e\|^2=15/4-(3/2)\sqrt5<1.                     \tag{6}
\]

Use both endpoints `p_i=v_a,v_b` of each edge as36 actual contacts.
Define the five-column row

\[
 A_i(u)=\big(p_i\times a_i(u),\ (a_i(u))_x,(a_i(u))_y\big).
                                                                    \tag{7}
\]

The parent certificate gives weights `beta_i(t)=alpha_i+(20t-13)gamma_i`
and the five-row matrix `B_0(t)` selected by rows `28,2,20,6,15`, with

\[
 \beta_i(t)>1/50,\quad \sum_i\beta_i(t)=1,\quad
 \sum_i\beta_i(t)A_i(m+td)=0,\quad
 \|B_0(t)^{-1}\|_\infty\le6.                               \tag{8}
\]

These are uniform on the closed real parent interval. Their finite
hypotheses are fully replayed against the complete published expected
record, including all15 balance coefficients, determinant and all25
cofactor Bernstein bounds, and the parent's four damaged controls.
The inverse norm is the induced maximum absolute row-sum norm.

## 3. A uniform five-weight repair off the arc

Let `U=m+td` and `E_i=A_i(e)`, using the linearity of(5)--(7).
Then `A_i(u)=A_i(U)+s E_i`. Each torque entry of `E_i` has absolute
value less than `R||e||<9/4`, and each force entry less than one.
Thus every absolute row sum is less than
`3*(9/4)+2=35/4<9`. In particular, for the selected matrix `B(u)`,

\[
 \|B(u)-B_0(t)\|_\infty\le9\varepsilon,\qquad
 \|B_0(t)^{-1}(B(u)-B_0(t))\|_\infty
                   \le54\varepsilon<1/2.                   \tag{9}
\]

The inverse exists throughout the rectangle. Indeed the geometric
series for `(I+D)^-1`, `||D||<1`, converges absolutely in this induced
norm. Factoring `B=B_0(I+D)` and using(8)--(9) gives

\[
                 \|B(u)^{-1}\|_\infty\le12.                 \tag{10}
\]

The old weights leave the column residual

\[
 r=\sum_i\beta_i(t) A_i(u)^T=s\sum_i\beta_i(t) E_i^T,
                     \qquad \|r\|_\infty\le(9/4)\varepsilon.
                                                                    \tag{11}
\]

Correct only the five selected weights by

\[
                    \delta=-B(u)^{-T}r.                     \tag{12}
\]

The transpose inverse has row sum at most five times(10), so

\[
                |\delta_j|\le5\cdot12\cdot(9/4)\varepsilon
                         =135\varepsilon.                  \tag{13}
\]

Add `delta_j` to the corresponding old weights, leaving the other31
unchanged, and call the resulting weights `beta'_i`. Their torque and
x/y force sum is exactly zero by(12). All normals are perpendicular to
`u`, and `u_z!=0`, so their z force sum is zero too. This is full spatial
force and torque balance, not balance in an auxiliary plane.

The unnormalized weights are strictly greater than
`1/50-135 epsilon>0`, and their sum is at most `1+675 epsilon`.
Normalize by their positive sum to get `widehat beta_i`. Exact rational
arithmetic gives

\[
 \widehat\beta_i>
    \frac{1/50-135\varepsilon}{1+675\varepsilon}
          =\frac{173}{10135}>\frac1{60},\quad
 \sum_i\widehat\beta_i=1,\quad
 \sum_i\widehat\beta_i A_i(u)=0.                            \tag{14}
\]

These estimates, together with the uniformly invertible matrix, prove
existence of the repaired weights for **every real** `(t,s)` in(1).
The checker additionally solves(12) exactly at the four box corners
and verifies all six full force/torque components and normalization.
Those point calculations check the literal correction formula; they
are not used to extend sampled balances to the continuum.

For any `Z in R5`, set `L=max_i A_i(u) Z`. Positive normalized balance
implies `L>=0`;(14) bounds every negative row value in magnitude by
`60L`. Applying(10) to the five selected rows, then `sqrt5<3`, yields

\[
                   \|Z\|_2\le2160L.                        \tag{15}
\]

An arbitrary actual `b in u-perp` can be written
`b=(tau_x,tau_y,-w.tau)`, `w=(u_x/u_z,u_y/u_z)`.
Let `T=I_2+ww^T`. Then `a_i.b=(a_i)_{xy}.T tau` and
`||b||<=||T tau||`, since `T^2-T` is positive semidefinite.
Thus the two force variables in(7) retain the full physical translation;
they are not an assumed centering operation.

## 4. Exact Cayley closure at four proper reference motions

For `S=I,G`, each contact has an original source preimage with spatial
image `p'_i=p_i`. For `S=M_u Hx,M_u Hy`, take the original preimage
`Hx p_i` or `Hy p_i`, whose spatial image is `p'_i=M_u p_i`.
In all cases `a_i.p'_i=h_i>0`, and `||p'_i||=R`.

Write `C=QS^T` as in(3). The exact identity

\[
 C p=p+\frac{2}{1+\|c\|^2}
               (c\times p+c\times(c\times p))
\]

holds. Set `v=2 lambda c/(1+||c||^2)`. Every original closed-fit
constraint at a selected contact implies

\[
 (\lambda-1)h_i+
       a_i\cdot(v\times p'_i+b)+E_i^*\le0,\qquad
 E_i^*=a_i\cdot(c\times(v\times p'_i)).                    \tag{16}
\]

For the fixed centers use `Z=(v,T tau)` in(15). For a reflected center,
the cross-product identity for the orthogonal reflection gives
`p'_i cross a_i=-M_u(p_i cross a_i)`, because `a_i perpendicular u`.
Replace the first three coordinates by `-M_u v` in(15). This is an
orthogonal transformation, so it preserves the Euclidean norm of `Z`.
The same balance and spanning estimate therefore apply at all four
proper reference motions. No improper full-source placement is asserted.

Since the physical edge length is one and `||u||<9/8`, we have
`||a_i||<9/8`. Hence

\[
             |E_i^*|\le(81/32)\|c\|\|v\|.                 \tag{17}
\]

Drop the nonnegative `(lambda-1)h_i` from(16). Equations(15)--(17)
and `||v||<=||Z||` give

\[
 \|Z\|\le2160\cdot\frac{81}{32}\cdot\frac1{14400}\|Z\|
                   =\frac{243}{640}\|Z\|.                 \tag{18}
\]

The coefficient is less than one, so `Z=0`. Because `lambda>=1`,
`v=0` forces `c=0`, and the translation chart forces `b=0`.
Equation(16), with a positive support, now forces `lambda=1`.
Thus `Q=S`, proving the forward implication of(4). The reverse
implication follows from the exact equal shadows of the centers.
This argument includes unbounded `lambda>=1`; it needs no scale budget.

## 5. Separation from all minimum axes

For any unit minimum axis `a`, the parent arc checker bounds below
the quadratic polynomial

\[
       F_a(U)=(17/18)^2\|U\|^2-(a\cdot U)^2
\]

on its entire interval by the minimum of its three Bernstein
coefficients. For `u=U+se`, orthogonality gives
`||u||^2=||U||^2+s^2||e||^2`. Discarding the nonnegative new norm term,
and using `||U||<9/8`, `||e||<1`, yields

\[
               F_a(u)\ge F_a(U)-(9/4)\varepsilon-\varepsilon^2.
                                                                    \tag{19}
\]

All six exact parent Bernstein lower bounds exceed this loss. Thus
`|a.u|/||u||<17/18` throughout(1). Projective chord squared is
`2-2|a.u|/||u||>1/9`, proving the strict `1/3` separation. The
complete minimum catalogue comes from the original geometry premise.

## 6. Genuine two-dimensionality and an off-arc example

The vectors `m,d,e` are independent. Also `m.u=1`. Consequently no
two distinct pairs `(t,s)` in(1) give proportional raw normals, including
opposite representatives: their `m` coefficients would force the
proportionality constant to be one. The open rectangle therefore
parametrizes a two-dimensional receiving region on the unit sphere.

Let `U*=m+(13/20)d` and `u*=U*+epsilon e`. Every parent-arc normal
lies in the plane spanned by `m,d`. Cauchy--Schwarz gives the maximum
absolute cosine with that plane as `||U*||/||u*||`, and the parent arc
contains `U*`, so it attains this maximum. Therefore the nearest
projective parent-arc normal has squared cosine

\[
     C_*^2=\frac{\|U_*\|^2}{\|U_*\|^2+arepsilon^2\|e\|^2}.
                                                                    \tag{20}
\]

The checker verifies the exact ordered-field comparison
`C_*^2<(1-(1/200000)^2/2)^2`. Both compared cosines are positive;
taking positive square roots proves projective chord greater than
`1/200000` from the **entire** parent arc. This supplies receiving
directions outside the previous one-dimensional domain, without
claiming that every older published receiving cover was enumerated.

## 7. Reproduction, credit and remaining frontier

The [checker](check.py) uses Python3.11+ and only the standard library.
[DEPENDENCIES.json](DEPENDENCIES.json) pins the exact named-body model,
arithmetic and four parent certificate/checker files. It replays the
complete parent finite record before new box, norm, separation and
stress-repair gates. Both normal and optimized modes compare the full
frozen new [expected.json](expected.json); five damaged controls reject
a collapsed transverse direction, widened patch, cropped receiver,
false positive-weight lower bound and unsafe source radius. Details and
commands are in [README.md](README.md) and [VALIDATION.md](VALIDATION.md).

The trust boundary includes the exact Python implementation, credited
original-solid identification and unformalized geometric arguments.
Freezing or matching expected output is reproducibility, not an
independent proof. The rigorous continuum steps are affine interpolation,
the matrix geometric series, bounded weight repair and exact Cayley
contraction above; no finite sampling or floating optimizer replaces them.

We credit the parent original-contact force/torque and Cayley mechanism.
Positive spanning, matrix perturbation by a Neumann series and the other
general tools are standard; no historical method priority is claimed.
The earlier [all-source minimum-cap result](../quantitative_minimum_caps/PROOF.md)
and its [independent audit](../../six-reviewer-4/quantitative-cap-audit/REVIEW.md)
retain their distinct quantifiers and review status. This new patch has
no independent verdict. The contemporaneous
[RID two-coordinate wedge proof](../../six-rupert-3/rid_two_coordinate_wedges/PROOF.md),
source `c6514c30c565ff0beeebb833cd5c9870f8c67dd7`, graph
`bafkreigkduxgv3lrhjwq4radhlwyq7mndlqd6apkjzfkspm5auu47x6zcy`,
gives an all-source result for a different body; it is related context,
not a premise or a transfer theorem for this J74 patch.

Current primary status was checked live2026-10-01:
[Gosain--Grimmer Table4](https://arxiv.org/html/2509.08190) retains
J72,J73,J74,J75,J77 without known passages. The assigned
[Zeng](https://arxiv.org/html/2604.26531) and
[Steininger--Yurkevich](https://arxiv.org/abs/2508.18475) seeds do not
resolve original J74. This is a bounded literature check, not an
exhaustive priority survey. Completed heuristic searches of changed
silhouette chambers supplied no strict construction; neither those
searches nor this conditional patch exclude arbitrary remote source
motions. A useful next target is a contact configuration outside these
motion neighborhoods, or a separately justified whole-source localization
at nonminimum receivers. Merely optimizing these conservative constants
does not resolve the global problem.
