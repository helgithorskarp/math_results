# Simplicial-cone reflections and a nine-point obstruction

Author proof, 26 September 2026. Independent mathematical review and
formalization are pending. This proves a full-comparison geometric class
and an obstruction to extending its motion argument. It does not resolve
the unrestricted three-dimensional Gaussian-majorisation conjecture.

## 1. Statements

Let `v1,v2,v3` be a basis of `R^3`, and put

\[
 K=\{\alpha_1v_1+\alpha_2v_2+\alpha_3v_3:\alpha_i\geq0\},
 \qquad K^*=\{a:a\cdot v_i\geq0\ (i=1,2,3)\}.
 \tag{1}
\]

The star denotes the **positive** dual. Define on `D=K* union (-K)`

\[
 T(a)=a\quad(a\in K^*),\qquad T(-b)=b\quad(b\in K).
 \tag{2}
\]

The pieces intersect only at zero: if `a in K*` and `-a in K`, then
`-|a|^2=a dot (-a)>=0`. Thus (2) is unambiguous. It is a contraction:
each piece is mapped isometrically, and a cross-pair has squared-distance
loss `|a+b|^2-|a-b|^2=4 a dot b>=0`.

**Theorem A (explicit lift).** The map (2), on its entire domain, admits
a continuous contracting motion in `R^5` with endpoints in the original
copy of `R^3`. It has smooth trajectories after a time reparametrization,
or two smooth pieces in one degenerate case.

**Theorem B (Gaussian consequence).** For every bounded probability
measure `mu` supported on `D` and every `s>0`, set
`f=mu*gamma_s`, `g=(T#mu)*gamma_s`, where the Gaussian covariance is `s I_3`.
Then

\[
 H_f(a):=\int_{\mathbb R^3}(f-a)_+\,dx
 \ \leq\ H_g(a)\qquad(a>0).
 \tag{3}
\]

Thus `f` is majorised by `g`. The assertion includes nonatomic measures,
arbitrary atom weights, and arbitrary mass at zero. If a global
1-Lipschitz map is desired, (2) has one by Kirszbraun extension; its values
outside the support play no role.

**Theorem C (ball-volume consequence).** For finitely many labeled
`x_i in D`, put `y_i=T(x_i)`. For arbitrary radii `r_i>=0`,

\[
 \left|\bigcup_i B(y_i,r_i)\right|
 \leq\left|\bigcup_i B(x_i,r_i)\right|,
 \qquad
 \left|\bigcap_i B(y_i,r_i)\right|
 \geq\left|\bigcap_i B(x_i,r_i)\right|.
 \tag{4}
\]

These are three-dimensional Lebesgue volumes. There is no restriction
to equal radii, few centers, or small displacements. Translations,
orthogonal changes of coordinates, dilations, and restriction to a subset
preserve the assertions.

The explicit motion is the new geometric ingredient in these statements.
The inference from a five-dimensional motion to (3) or (4) is prior work,
credited in Sections 4 and 5. A concrete seven-point member has paired
affine rank six, so its conclusion does not follow by inserting that rank
into the team's earlier rank-five theorem.

**Theorem D (boundary obstruction).** Define four fixed vectors and four
moving vectors, in the displayed cyclic order, by

\[
\begin{split}
 A={}&((1,0,1),(0,1,1),(-1,0,1),(0,-1,1)),\\
 B={}&((1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1)).
\end{split} \tag{5}
\]

The nine-point map `(0,A,-B) -> (0,A,B)` is a contraction of paired
affine rank six. It admits no continuous contracting motion in `R^5`.
The ordinary leapfrog construction does give a motion in `R^6`, so six
is the least possible ambient motion dimension for this labeled example.
This is an obstruction to the lifting method, not to (3) or (4).

## 2. A rigid three-dimensional cluster moving in five dimensions

Put `H=span(v2,v3)`, and let `P` be orthogonal projection onto `H`.
Choose an isometry `J:H -> R^2`. Since the three vectors are independent,

\[
 h=\frac{|v_1-Pv_1|}{|v_1|}\in(0,1],\qquad
 |Pv_1|^2=(1-h^2)|v_1|^2.
 \tag{6}
\]

First suppose `0<h<1`. For `-1<=t<=1`, set

\[
 a(t)=\frac{t+h}{1+ht},\qquad q(t)=\sqrt{1-t^2},
 \tag{7}
\]

and define a linear map `F_t:R^3 -> R^3 direct-sum R^2` on the basis by

\[
\begin{split}
 F_t(v_1)&=\left(a(t)v_1,\frac{q(t)}{1+ht}J(Pv_1)\right),\\
 F_t(v_j)&=(t v_j,q(t)J(v_j)),\qquad j=2,3.
\end{split} \tag{8}
\]

The denominator is at least `1-h>0`. Both scalar functions `a(t)` and `t`
increase from `-1` to `1`, since

\[
 a'(t)=\frac{1-h^2}{(1+ht)^2}>0.
 \tag{9}
\]

The map `F_t` is an isometric linear embedding. For `i,j in {2,3}` this
follows from `t^2+q^2=1`. The first norm and remaining cross-products
follow, respectively, from the polynomial identities

\[
 (t+h)^2+(1-h^2)(1-t^2)=(1+ht)^2,
 \qquad t(t+h)+(1-t^2)=1+ht.
 \tag{10}
\]

Indeed `Pv1 dot vj=v1 dot vj`. These calculations preserve all nine
entries of the Gram matrix of the three generators; linearity then
preserves the norm and inner product of every pair of vectors in `R^3`.
In particular the moving cluster remains rigid throughout the motion.
The endpoints are `F_-1(b)=(-b,0)` and `F_1(b)=(b,0)`.

One way to find this motion is to preserve the moving Gram matrix while
using original-coordinate coefficients `(a,t,t)`. The remaining Gram
matrix has entries `(1-d_i d_j) v_i dot v_j`. Its Schur complement on
`span(v2,v3)` vanishes exactly when
`(1-a^2)(1-t^2)=(1-h^2)(1-at)^2`. The increasing branch (7) satisfies
this identity. The residual Gram matrix therefore needs only two
dimensions; (8) gives its explicit factor instead of merely invoking
the existence of a continuous matrix factorization.

## 3. Every cross-distance decreases, including the degenerate case

Keep each `a in K*` at `(a,0)`, and move `-b`, for `b in K`, to `F_t(b)`.
Write `b=sum alpha_i v_i`, with `alpha_i>=0`. The cross-distance is

\[
 |(a,0)-F_t(b)|^2
 =|a|^2+|b|^2
 -2\left(\alpha_1a(t)\,a\cdot v_1
             +t\sum_{j=2}^3\alpha_j a\cdot v_j\right).
 \tag{11}
\]

Every coefficient multiplying `a(t)` or `t` is nonnegative by (1), so
(9) proves monotonicity. Distances within either cluster are constant.
The two prescriptions agree at zero. This proves a continuous contraction
on all of `D`. On bounded subsets continuity is joint in position and time.
Putting `t=-cos(pi u)`, `0<=u<=1`, replaces `q` by `sin(pi u)` and gives
smooth trajectories even at the two endpoints.

If `h=1`, then `v1` is perpendicular to `H`. Use two stages in the same
`R^3 direct-sum R^2`:

1. Keep `v2,v3` at their negatives, and send `v1` through
   `(r v1, sqrt(1-r^2)|v1| e)`, where `r` increases from `-1` to `1`
   and `e` is a unit vector of the auxiliary `R^2`.
2. Keep `v1` at `(v1,0)` and send `vj`, `j=2,3`, through
   `(r vj,sqrt(1-r^2)J(vj))`.

At the join all auxiliary coordinates vanish. Orthogonality gives a
linear isometric embedding at every stage. Its three original-coordinate
coefficients are, successively, `(r,-1,-1)` and `(1,r,r)`; they are
nondecreasing. Equation (11) with these coefficients proves contraction.
The cosine reparametrization makes each stage smooth. This also covers
orthogonal cone generators without taking a singular limit in (8).

The same formula in `R^n direct-sum R^(n-1)` works for a simplicial cone
in `R^n`. Only its `n=3` specialization is used for the full Gaussian and
ball-volume conclusions here: it uses exactly two auxiliary dimensions.

## 4. Gaussian majorisation from the motion

Apply [Aishwarya--Li, Theorem 1.4(i)(a)](https://arxiv.org/html/2609.07041v2)
to the embedded bounded law and Theorem A's motion in `R^5`. The Gaussian
density sampled from itself at the initial endpoint is stochastically
dominated by its counterpart at the final endpoint.

At the two endpoints the densities factor as `f(x) gamma_s^(2)(z)` and
`g(x) gamma_s^(2)(z)`. Write `C2=(2 pi s)^(-1)`. For `Z` sampled from
`gamma_s^(2)`, the variable `|Z|^2/(2s)` is exponential with mean one.
Therefore, if `X` is sampled from `f`,

\[
 \Pr\{ f(X)\gamma_s^{(2)}(Z)>aC_2\}
 =\int f(x)\left(1-\frac a{f(x)}\right)_+dx
 =H_f(a).
 \tag{12}
\]

The endpoint stochastic order gives (3). This is the same two-auxiliary-
coordinate cancellation used in the team's
[paired-rank argument](../gaussian_majorisation_rank_abel/PROOF.md),
Section 3. Here its input is the explicit motion (8), not a paired-rank
bound. Neither Aishwarya--Li's theorem nor this cancellation is claimed new.

## 5. Kneser--Poulsen consequence and relation to known classes

Reverse the motion in Theorem A. It is a piecewise-smooth expansion
in `R^(3+2)`, with both endpoints in the same `R^3`. Theorem 1 of
[Bezdek--Connelly, Pushing disks apart](https://arxiv.org/pdf/math/0108098)
gives both inequalities (4), with their indicated directions. Zero radii
follow by continuity, or have zero contribution to an intersection volume.

Thus the new geometric assertion is a concrete class of motions to which
their existing theorem applies. It is not a new proof of their theorem.
Unlike the general six-point consequence, the number of points in either
cone is unrestricted. Unlike their two-dimensional-displacement
criterion, the moving differences can span all three original dimensions.

For example choose the rational unit vectors

\[
 v_1=(3/13,4/13,12/13),\quad v_2=(1,0,0),\quad
 v_3=(3/5,4/5,0),
 \tag{13}
\]

and their dual basis

\[
 a_1=(0,0,13/12),\quad a_2=(1,-3/4,0),\quad
 a_3=(0,5/4,-5/12),\qquad a_i\cdot v_j=\delta_{ij}.
 \tag{14}
\]

The seven points `(0,a1,a2,a3,-v1,-v2,-v3)` map to
`(0,a1,a2,a3,v1,v2,v3)`. Their paired span is
`span{(ai,ai),(-vi,vi)}=R^6`. The displacement span has dimension three.
All off-diagonal cross-pair distances are unchanged, while the three
matched squared distances decrease by four. Equations (8)-(11) prove
every hinge inequality for every choice of positive weights on these labels.

This example is not a strong (coordinatewise) contraction in any common
orthonormal coordinate system. To see this, such a coordinate system
would require `(ai)_k (vj)_k>=0` for every `i,j,k`. Since both lists are
bases, in each coordinate they can all be made nonnegative by a common
sign change. Their duality then forces the two nonnegative inverse
matrices to be monomial. An elementary way to see that last step is to
use `ai dot vj=0` for `i!=j`: nonnegative coordinate products must vanish
separately, so every coordinate can support only one matched basis pair;
invertibility uses all three. Thus the `vi` would be mutually orthogonal,
contrary to (13). The definition and the prior volume theorem for strong
contractions are from
[Bezdek--Naszodi](https://arxiv.org/abs/1701.05074).

These comparisons identify distinctions from specific established
sufficient classes. They do not prove historical priority over every
possible construction or every composition of known motions. The primary
literature search and its limitations are recorded in [SOURCES.md](SOURCES.md).

## 6. An exact nine-point obstruction beyond simplicial separation

Use (5), and include the origin. Every `a_i dot b_j` is zero or two,
so the map in Theorem D is a contraction. Both lists span `R^3`.
As in Section 5, the paired affine rank is six.

Suppose a continuous contracting motion in `R^5` existed. Any pair whose
initial and final distances agree must preserve its distance at every
time. In particular all distances inside the anchored cloud `{0} union A`
are fixed, all distances inside `{0} union (-B)` are fixed, and every
zero-dot cross-pair in (5) remains a zero-dot pair relative to the moving
origin. Translate that origin to zero at each time.

Let `U_t` be the three-dimensional span of the anchored cloud. Identify
it isometrically with the original `R^3` using its labeled Gram matrix.
Write `z_j(t)` for the moving image of `-b_j`, and let `p_j(t)` be its
orthogonal projection into `U_t`, under this identification. Two independent
facet normals in `A` are perpendicular to each `b_j`; their preserved
zero products force

\[
 p_j(t)=\lambda_j(t)b_j.
 \tag{15}
\]

The four vectors `b_j` have precisely the one-dimensional relation space
generated by

\[
 b_1-b_2+b_3-b_4=0.
 \tag{16}
\]

Preservation of the Gram matrix of the moving vectors implies the same
relation among the `z_j(t)`: the squared norm of that linear combination
remains zero. Projecting it into `U_t` and using the uniqueness of (16)
shows

\[
 \lambda_1(t)=\lambda_2(t)=\lambda_3(t)=\lambda_4(t)=:\lambda(t).
 \tag{17}
\]

These coefficients can be expressed using inner products with three
anchored basis vectors and their fixed inverse Gram matrix, so they are
continuous without needing to choose a moving orthonormal frame.
They start at `-1` and finish at `1`. At some time `lambda=0`, all four
moving vectors lie in `U_t`'s orthogonal complement. Their fixed Gram
matrix has rank three, but this complement in `R^5` has dimension two.
This is a contradiction.

More explicitly, at any time their residual Gram matrix is
`(1-lambda^2) G_B`; at an intermediate value of `lambda` its rank is
three. This also explains why the ordinary six-dimensional leapfrog
motion can work. The proof concerns arbitrary continuous motions, not
merely linear Gram interpolation or the formula from Section 2.

The origin is essential to this proof. Deleting it leaves eight output
points in the plane `z=1`, and their paired affine rank is five. That
eight-point contraction is already safe by the earlier rank theorem.
No statement that nine is the smallest possible obstruction is made.

There is also a simple way to rule out deterministic relabelling for a
specific law on these points. Number the nine displayed labels from zero
to eight and give them weights `2^j/511`. All target sites are distinct.
A deterministic map with this target law must send some subset of input
atoms to the target of mass `2^j/511`. Uniqueness of binary expansion
forces this subset to be exactly label `j`. Hence the prescribed map is
the only deterministic realization of these two laws, and its
five-dimensional obstruction cannot be removed by changing the matching.
This binary-weight device follows the team's
[earlier matching argument](../gaussian_majorisation_nested_hulls/PROOF.md);
the new part here is its nine-point geometric obstruction. It imposes no
restriction on nondeterministic couplings or on other proof methods.

## 7. What this changes for counterexample exploration

All dual-basis flips are in Theorem A: take `K=cone(v1,v2,v3)` and fixed
points in its positive dual. They can no longer be used to search for
an asymmetric-weight or arbitrarily high-degree Gaussian counterexample.
The exclusion is universal and follows from the motion, not from positive
numerical experiments. More generally it excludes any two-cluster central
reflection for which one can place the moving positive cluster in a
simplicial cone whose positive dual contains the fixed cluster.

For the square fixture, `cone(B)` is exactly

\[
 \{(x,y,z):z\geq|x|,\ z\geq|y|\}
 =\{b:a_i\cdot b\geq0\text{ for every }a_i\in A\}.
 \tag{18}
\]

It has four extreme rays. A cone lying between `cone(B)` and the
right side of (18) must equal this cone; it cannot be simplicial. Thus
Theorem A cannot be applied by simply selecting a better enclosing
simplicial cone. Theorem D independently rules out every other
five-dimensional continuous motion of the prescribed labels.

This nine-point contraction is therefore a concrete next target for
asymmetric weights and higher-order witnesses. It is outside the motion
class proved here. Its Gaussian-majorisation and arbitrary-radius volume
questions remain open in this note. Nonliftability alone supplies no
negative Gaussian hinge or volume inequality. The familiar sixteen-label
simplex-flap obstruction remains a separate, valid target.
