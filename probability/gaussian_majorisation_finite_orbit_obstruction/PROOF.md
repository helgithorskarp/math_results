# No universal finite orthogonal averaging rule for square-cone contractions

Complete author proof with exact supplementary certificates, 26 September
2026. Independent review and formalization are pending. This is an
obstruction to a proposed proof mechanism, **not** a counterexample to
Gaussian majorisation. The unrestricted dimension-three question remains open.

## 1. The precise finite dependency

Use the ordered directions from the existing square-cone packet:

\[
A=((1,0,1),(0,1,1),(-1,0,1),(0,-1,1)),
\quad B=((1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1)).       \tag{1}
\]

The map T fixes 0 and A_i, and sends -B_j to B_j. It is a contraction:
within each cluster distances are preserved, and cross squared-distance
losses are 4 A_i.B_j, with A_i.B_j in {0,2}. Distances to zero are preserved.

Fix any variance s>0 and any prescribed origin mass p in [0,1). Let

\[
\mu_w=p\delta_0+\sum_i a_i\delta_{A_i}+\sum_j b_j\delta_{-B_j},
\quad a_i,b_j\ge0,\quad \sum_i a_i+\sum_j b_j=1-p,
\quad f_w=\mu_w*\gamma_s,\quad g_w=T_\#\mu_w*\gamma_s,       \tag{2}
\]

where gamma_s has covariance s I_3.

**Theorem 1.** There are no finitely many orthogonal matrices Q_l and
positive numbers lambda_l, summing to one, for which

\[
 \sum_l\lambda_l(f_w(Q_l x)-h)_+
 \le \sum_l\lambda_l(g_w(Q_l x)-h)_+                     \tag{3}
\]

holds for every admissible w, every x in R3, and every h>0.
The rule may depend on s and p. Its matrices need not form a group, its
weights need not be equal, and the identity need not be included.
The conclusion is unchanged if (3) is required only for all strictly
positive eight-tuples w: pointwise continuity extends that condition to
the closed simplex.

Thus replacing the 48-element group by a larger finite set of rotations
cannot remove the weight restriction in the existing orbit proof. The
theorem does not exclude a rule chosen separately for each w, an infinite
angular average, or a comparison that transports mass between radii.
It does not exclude unrestricted-weight *integrated* majorisation on (1).

## 2. Isometric subfamilies force invariance of the averaging support

We first prove the elementary mechanism, including its quantifiers.
Suppose a subfamily in (2) has three variable-weight nonzero sites
x_1,x_2,x_3 forming a linear basis, with target sites y_i=S x_i for one
orthogonal S. The origin remains fixed. Assume (3) holds for every
positive allocation of the mass 1-p to these three sites.

For each such allocation the endpoint laws are congruent. Their integrated
hinges are equal, at every h>0. Integrating the nonnegative difference in
(3), each Q_l preserves Lebesgue measure, so its integral is zero. The
difference is continuous and nonnegative, hence vanishes at every x.
All integrals are finite because each hinge is bounded by its density.

For a fixed observation x, equality for all h>0 identifies the two finite
weighted distributions of the positive density values f_w(Q_l x) and
g_w(Q_l x). For example the right derivative of the hinge sum is minus
the mass strictly above h. In particular, for any one averaging matrix
Q_0, its source value occurs among the target values, since its averaging
weight is positive.

Let V be the finite set of distinct averaging matrices. For every x and
every positive triple (t_1,t_2,t_3) with sum 1-p, therefore, at least one
Q in V satisfies

\[
 \sum_{i=1}^3t_i
 [\gamma_s(Q_0x-x_i)-\gamma_s(Qx-y_i)]=0.                 \tag{4}
\]

The common origin terms cancel by orthogonality. Fix x. A finite union
of proper affine hyperplanes cannot cover the open weight simplex.
Consequently one Q makes all three coefficients in (4) zero. Indeed a
linear form vanishing identically on sum t_i=1-p has all coefficients
zero, since 1-p>0.

Orthogonality and |x_i|=|y_i| turn these three kernel equalities into

\[
 (Q_0^T x_i-Q^T y_i)\cdot x=0\quad(i=1,2,3).            \tag{5}
\]

For each x at least one Q satisfies (5). A finite union of proper linear
subspaces cannot cover R3, so one Q satisfies the three vector equalities
Q_0^T x_i=Q^T y_i. Since the x_i form a basis and y_i=S x_i,
this forces Q=S Q_0. Thus

\[
                         S V=V.                         \tag{6}
\]

Inclusion follows from the preceding argument for each Q_0; equality
follows because left multiplication by S is injective on a finite set.
Neither analyticity nor a uniform choice of the matching Q in advance
was assumed. The two elementary finite-union arguments supply that choice.

## 3. Two forced reflections have an infinite-order product

For j=0,1 put S_j=I-2 B_j B_j^T/3. These are orthogonal reflections.
For j=0 the two vectors A_2,A_3 are perpendicular to B_0; for j=1
the two vectors A_0,A_3 are perpendicular to B_1. In each case the two
fixed A vectors together with -B_j form a basis. Hence the contraction
restricted to these three sites is exactly S_j. Section 2 forces both
S_0 V=V and S_1 V=V, so also P V=V for P=S_0 S_1.

All these data are rational. Since |B_0|^2=|B_1|^2=3 and B_0.B_1=1,

\[
 \det P=1,\qquad
 \operatorname{tr}P=3-2-2+4(B_0\cdot B_1)^2/9=-5/9.     \tag{7}
\]

This rotation has infinite order. To see this without a numerical angle
test, its nontrivial eigenvalues are z,z^{-1} on the unit circle and
z+z^{-1}=tr(P)-1=-14/9. The integer polynomials

\[
 L_0(X)=2,\quad L_1(X)=X,\quad
 L_{n+1}(X)=X L_n(X)-L_{n-1}(X)
\]

satisfy L_n(z+z^{-1})=z^n+z^{-n} and are monic for n>=1.
If P had finite order n, then -14/9 would be a rational root of the
monic integer polynomial L_n(X)-2. The rational-root theorem would
make it an integer, a contradiction.

But P permuting a nonempty finite set V of invertible matrices implies
P has finite order: for any Q in V, a repeated iterate P^j Q=P^k Q
gives P^(j-k)=I. This contradiction proves Theorem 1. The certificate
checks the bases, reflections, product, determinant and nonintegral trace
exactly. The argument for *all* powers is the written polynomial proof,
not a search through finitely many powers.

## 4. A rational certificate against the current 48-element rule

The following tests locate an actual failure of (3) for the current
signed-coordinate-permutation group G. They are exact Gaussian values,
not numerical quadrature.

Set s=1/(2 log 2), x=(1/2,0,0), and c=gamma_s(x)>0. Every group image
of x is one of the six signed coordinate axes of radius 1/2, each with
multiplicity eight. For an integer site v and an axis k with sign e,

\[
       \gamma_s(e e_k/2-v)/c=2^{e v_k-|v|^2}.              \tag{8}
\]

**Congruent control.** Take

\[
 \mu=p\delta_0+(1-p)
       (\tfrac14\delta_{A_0}+\tfrac14\delta_{A_1}
                                  +\tfrac12\delta_{-B_2}).
\]

This entire law is mapped by the single reflection S_2, so its integrated
hinge difference is identically zero. In the axis order +x,-x,+y,-y,+z,-z,
write f/c=p+(1-p)F/16 and g/c=p+(1-p)J/16. Their arrays are

\[
 F=(5,2,5,2,9/2,3),\qquad
 J=(7/2,7/2,7/2,7/2,6,3/2).
\]

At h=c[p+(1-p)7/32], direct rational hinge evaluation gives

\[
 \frac1{48}\sum_{Q\in G}
       [(g(Qx)-h)_+-(f(Qx)-h)_+]=-(1-p)c/64<0.           \tag{9}
\]

**All positive weights, full paired rank.** Give the eight nonzero sites
(A_0,...,A_3,-B_0,...,-B_3) the packet weights

\[
                 (16,16,1,1,2,2,32,2)/72,               \tag{10}
\]

multiply this packet by 1-p, and keep origin mass p. For 0<p<1 all
nine weights are positive. Now write f/c=p+(1-p)F/18 and
g/c=p+(1-p)J/18. The arrays are

\[
 F=(169/32,79/32,169/32,79/32,155/32,55/16),
\quad J=(31/8,31/8,31/8,31/8,53/8,53/32).
\]

At h=c[p+(1-p)7/36], the same averaged gap is

\[
                            -(1-p)c/384<0.              \tag{11}
\]

The paired affine rank of the nine-site map is six: the invertible
sum/difference change of coordinates sends (A_i,A_i) and (-B_j,B_j)
into complementary three-dimensional blocks, and both A and B span R3.
The checker verifies this independently by exact elimination. The failure
persists for any prescribed dominant origin mass p<1. No sign of the
*integrated* hinge gap for the all-positive packet (10) is claimed here.
It violates the ordered B-weight hypothesis of the positive team theorem.
Both strict deficits persist on open observation and threshold neighborhoods
by continuity; placing the displayed observation on a chamber boundary
does not restrict the failure to a set of measure zero.

## 5. What this closes, and what remains

The ordered-weight certificate at graph height 6114 remains valid under
its hypotheses. Theorem 1 closes a specific natural extension: no single
finite positive orthogonal averaging rule can prove its pointwise
inequality for every weight vector, even at a fixed variance and a fixed
origin mass. This is stronger than a failed coefficient order or matching
heuristic for one group. Equations (9)--(11) are compact rejection controls
for future implementations of that extension.

The fixed-atom reduction at height 6112 concerns the integrated inequality
with an **arbitrary** remaining bounded law. It cannot convert a false
uniform finite-orbit premise into a proof. The common Gaussian simply
shifts the threshold and scales the negative gaps above. This does not
contradict that reduction. The bounded-law stability and finite positive
certificate theorem at height 6102 also remains unchanged: it controls
integrated hinges with signed endpoints and localization margins, rather
than requiring the stronger orbitwise sign.

Further exact work on the unrestricted question must retain that integral
or use another valid comparison. An infinite angular argument or an
adaptive rule is not addressed here. No new Kneser--Poulsen conclusion,
new global positive class, or actual Gaussian-contraction counterexample
has been obtained in this pass.

The complete finite inputs, two differently organized exact audits and
reproduction commands are in [README.md](README.md). All continuous and
universal implications in Sections 1--3 are written proofs and remain
part of the unformalized author trust boundary. See [SOURCES.md](SOURCES.md)
for problem provenance and durable team dependencies.
