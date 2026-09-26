# The support coefficient is strictly positive exactly off the isometry boundary

Complete author proof, 26 September 2026; independent review pending.
This removes the geometric and positive-label restrictions from the
all-threshold shallow theorem in [RELATIVE_TAIL.md](RELATIVE_TAIL.md).
Every nondegenerate tetrahedron, every choice of positive inward-normal
lengths, every nonnegative probability weight vector and every fixed
positive Gaussian variance satisfy full comparison at sufficiently small
depth. The depth may depend on those data. No positive depth uniform in
all variances, unrestricted R3 theorem, or new Kneser--Poulsen consequence
is claimed.

The new step is a Gaussian covariance interpolation for the degree-one
support coefficient. It gives an explicit strictly positive lower bound
and the exact zero criterion. The interpolation identity is classical
Price calculus, credited to [Voigtlaender, Theorem 1](https://arxiv.org/pdf/1710.03576).
We include its short density-level derivation in the form needed here.

## 1. Statement

Use the tetrahedron v_0,...,v_3, normals d_i=h_i grad(lambda_i), h_i>0,
and weights alpha_j,beta_ij from [PROOF.md](PROOF.md). Thus

\[
 d_i\cdot(v_k-v_j)=h_i(\mathbf1_{i=k}-\mathbf1_{i=j}),\qquad
 w_j=\alpha_j+\sum_{i\ne j}\beta_{ij},\quad
 J=\{j:w_j>0\},\quad
 \Gamma_j=\sum_{i\ne j}h_i\beta_{ij}w_i.                       \tag{1}
\]

For j in J, let S_j={i!=j:beta_ij>0}. Let A_j contain d_i for i in S_j,
and also 0 when alpha_j>0. It is nonempty. Its normal-fan cell is

\[
 C_j=\{\theta\in S^2:(v_k-v_j)\cdot\theta\le0\quad
                                      (k\in J\setminus\{j\})\}.
\]

These cells partition the sphere up to null boundaries. Put

\[
 \ell_j=\int_{C_j}\{h_{A_j}(-\theta)-h_{A_j}(\theta)\}\,d\sigma,
 \qquad \ell_\infty=\sum_{j\in J}\ell_j,                         \tag{2}
\]

where d sigma is the unnormalized area measure, of total 4 pi.

**Theorem 7 (universal strict support sign).** Every occupied tip satisfies
ell_j>=0, with equality if and only if Gamma_j=0. More quantitatively, set

\[
 K_j=\sum_{k\ne j}
       \frac{6|v_k-v_j|^2+2|d_k|^2}{h_k^2},\qquad
 P_j=\prod_{k\ne j}h_k.
\]

Then

\[
 \boxed{\quad
 \ell_j\ge
 \frac{e^{-K_j}}{4\sqrt2\,\pi^{3/2}P_j}
                   \sum_{i\in S_j\cap J}h_i .\quad}            \tag{3}
\]

In particular ell_infinity>0 if and only if Gamma=sum_j Gamma_j>0.
Neither the sign criterion nor (3) requires all sixteen labels to have
positive weight. The coefficient and bound depend on which labels are
present, rather than their positive masses. The bound is conservative.

**Corollary 8 (all shallow simplex flaps).** For every fixed tetrahedron,
fixed positive inward-normal lengths, fixed nonnegative probability
weights and fixed variance s>0, there exists t_*>0 such that the map

\[
 v_j\longmapsto v_j,\qquad v_j-td_i\longmapsto v_j+td_i
                                                       \quad(i\ne j)
\]

satisfies

\[
 H_{\mu_t^-*\gamma_s}(a)\le H_{\mu_t^+*\gamma_s}(a)
                    \quad\text{for every }a>0,\quad 0<t<t_* .   \tag{4}
\]

If Gamma>0, (4) is strict below the target density maximum; at and
above it both hinges vanish. If Gamma=0, the weighted map is an isometry
and equality holds at all depths and variances. All finite maps here
are contractions and have 1-Lipschitz extensions to R3.

This follows immediately from Theorem 7 and RELATIVE_TAIL.md, Theorem 6,
including its variance scaling and threshold-floor argument. The full
sixteen-label geometry still has only its two endpoint distance states
even in R5, by PROOF.md, Section 6. No contracting motion of that full
geometry is supplied by the auxiliary Gaussian interpolation below.

## 2. The normal-edge duality and a positive-definite interpolation

Fix an occupied tip j. List the other three indices in any fixed order.
Let D have columns d_i, E have columns e_i=v_i-v_j, and H=diag(h_i)
in that order. The tetrahedron is nondegenerate, and (1) gives

\[
              D^TE=H,\qquad D,E\text{ invertible}.              \tag{5}
\]

For independent standard Gaussian vectors Z,W in R3, set

\[
 X=D^TZ,\qquad Y_r=E^T(rZ+\sqrt{1-r^2}W),\qquad -1\le r\le1.
                                                                    \tag{6}
\]

For -1<r<1 the joint covariance and its factorization are

\[
 \Sigma_r=
 \begin{pmatrix}D^TD&rH\\rH&E^TE\end{pmatrix}
 =\begin{pmatrix}D^T&0\\0&E^T\end{pmatrix}
   \begin{pmatrix}I&rI\\rI&I\end{pmatrix}
   \begin{pmatrix}D&0\\0&E\end{pmatrix}.                         \tag{7}
\]

The middle matrix has eigenvalues 1+r and 1-r, each three times.
Consequently Sigma_r is positive definite in the open interval, even
when the atom weights have zeros. Write its positive density as rho_r.

Define a piecewise-linear function F on R3 by taking the maximum of
x_i for i in S_j, together with the constant 0 if alpha_j>0. If S_j is
empty, F=0. This definition also permits alpha_j=0: then F can be negative.
It is Lipschitz and has at most linear growth. Let

\[
 B(y)=\prod_{k\in J\setminus\{j\}}\mathbf1_{\{y_k\le0\}},
 \qquad \Psi(r)=\mathbb E[F(X)B(Y_r)].                           \tag{8}
\]

An empty product is 1. For a moving coordinate i, the weak derivative
partial_i F is 1 on the open region where x_i is its unique maximizing
entry, and 0 elsewhere almost everywhere. Denote this indicator by q_i(x).
For i not in S_j, the derivative is zero. The tie hyperplanes are null.

## 3. Price differentiation gives the exact sign

Only the off-diagonal covariance pairs (x_i,y_i) change in (7), each
with derivative h_i. The Gaussian density identity is

\[
                 \partial_r\rho_r
                    =\sum_{i\ne j}h_i\partial_{x_i}\partial_{y_i}\rho_r.
                                                                    \tag{9}
\]

For example, take the Fourier transform of the density: it is
exp(-xi^T Sigma_r xi/2). Differentiation gives the multiplier
-sum_i h_i xi_(x_i) xi_(y_i), which is exactly the Fourier multiplier
of the right side of (9). There is no extra factor of two: the symmetric
off-diagonal entries occur twice in the quadratic form, canceling its 1/2.

On a compact subinterval of (-1,1), derivatives of rho_r are uniformly
bounded by a polynomial times a Gaussian with a fixed positive decay
rate. We may differentiate the integral of the linearly growing F B.
Integration by parts, or weak differentiation in (9), gives

\[
 \Psi'(r)=-\sum_{i\in S_j\cap J}h_i
     \int_{\mathbb R^3}\int_{\mathbb R^2}
       q_i(x)\!
       \prod_{k\in J\setminus\{i,j\}}\mathbf1_{\{y_k\le0\}}
       \rho_r(x,y_i=0,y_{\ne i})\,dy_{\ne i}\,dx .              \tag{10}
\]

The Dirac mass at y_i=0 arises from
partial_(y_i) 1_{y_i<=0}=-delta_0. Integration is in the coordinate
Lebesgue measures displayed in (10); no Euclidean surface Jacobian is
omitted. To justify the integrations without distribution notation,
one can first convolve the Lipschitz F and the half-line indicators
with smooth compactly supported mollifiers and then let their widths
tend to zero. Gaussian domination applies on the compact r interval,
and the Gaussian boundary integrals in (10) are finite.

Every summand on the right has nonnegative integrand. If S_j intersects
J, each corresponding integral is strictly positive: use the open box

\[
 1<x_i<2,\quad -1<x_k<0\ (k\ne i,j),\quad
 y_i=0,\quad -1<y_k<0\ (k\ne i,j).                             \tag{11}
\]

It has positive five-dimensional coordinate volume; q_i=1 and all
required half-line indicators equal 1 there. This works whether or
not the fixed core label is present. The density is strictly positive
everywhere for -1<r<1. Thus Psi is decreasing, strictly so if
S_j intersects J; if the intersection is empty it is constant.

The endpoint passage is valid despite the degenerate covariances there.
Use the explicit coupling (6). Every coordinate of E^T Z is a
nondegenerate scalar Gaussian, so the finitely many boundary events
y_k=0 have probability zero at r=+/-1. Also |F(X)|<=max_i|d_i| |Z|,
an integrable bound independent of r. Dominated convergence shows that
Psi extends continuously to both endpoints. No derivative estimate at
a singular endpoint is being assumed.

## 4. Homogeneity returns the spherical coefficient

At r=1, B(Y_1) is the indicator of the cone over C_j. At r=-1,
replace Z by -Z to obtain

\[
 \Psi(-1)-\Psi(1)
 =\mathbb E\big[(h_{A_j}(-Z)-h_{A_j}(Z))\,
                                \mathbf1_{\{Z/|Z|\in C_j\}}\big].
                                                                    \tag{12}
\]

Write Z=R Theta. Its direction is uniform on S2, independent of R,
and E R=2 sqrt(2/pi). Support functions have degree one, so

\[
             \Psi(-1)-\Psi(1)=\frac{2\sqrt{2/\pi}}{4\pi}\ell_j.
                                                                    \tag{13}
\]

Equations (10)-(13) prove ell_j>=0 and the exact criterion
ell_j>0 iff S_j intersects J. From (1), the latter is equivalent to
Gamma_j>0. Summing proves the equality assertion of Theorem 7.

The degree-one property is essential here. For the finite-parameter
logarithmic coefficient L(tau), a Gaussian radial average with positive
sign would not by itself imply the sign at each fixed radius. The
earlier finite-tau sign theorem in TAIL_BLOWUP.md remains a separate
input to Corollary 8 through RELATIVE_TAIL.md, Theorem 6.

## 5. An explicit lower bound, independent of positive weight sizes

Restrict r to [-1/2,1/2]. Equation (7) gives

\[
       \sqrt{\det\Sigma_r}=P_j(1-r^2)^{3/2}.                    \tag{14}
\]

For u=D^(-T)x and v=E^(-T)y, the density is

\[
 \rho_r(x,y)=\frac{1}{(2\pi)^3P_j(1-r^2)^{3/2}}
       \exp\!\left[-\frac{|u|^2-2r u\cdot v+|v|^2}{2(1-r^2)}\right].
                                                                    \tag{15}
\]

On this r interval the exponent's positive quadratic form is at most
|u|^2+|v|^2, since the largest eigenvalue of
[[I,-rI],[-rI,I]]/(1-r^2) is 1/(1-|r|)<=2. On the unit-volume box
(11), |x|^2<=6 and |y|^2<=2. Therefore it is at most

\[
 6\|D^{-T}\|_F^2+2\|E^{-T}\|_F^2
 =\sum_{k\ne j}\frac{6|e_k|^2+2|d_k|^2}{h_k^2}=K_j.             \tag{16}
\]

The equality uses D^(-T)=E H^(-1) and E^(-T)=D H^(-1), consequences
of (5). The Frobenius norm bounds the operator norm. Equations (14)-(16)
give rho_r >= exp(-K_j)/((2pi)^3 P_j) on every box (11). Each summand
in (10) is bounded using its own box; summands are nonnegative, so no
disjointness assumption is needed. Integrate in r over an interval of
length one. Monotonicity outside that interval and (13) yield

\[
 \ell_j\ge\frac{4\pi}{2\sqrt{2/\pi}}
           \frac{e^{-K_j}}{(2\pi)^3P_j}
                        \sum_{i\in S_j\cap J}h_i,
\]

which is precisely (3). This also makes strictness quantitative without
any numerical integration or assumptions about a generic configuration.

## 6. Controls, dependencies and remaining boundary

For the asymmetric geometry
v=((0,0,0),(2,0,0),(1,3,0),(1,1,4)), h=(1,2,3,5), the exact data are:

| Tip j | K_j | P_j |
| --- | --- | --- |
| 0 | 32251/1800 | 30 |
| 1 | 64651/1800 | 15 |
| 2 | 29183/360 | 10 |
| 3 | 3593/24 | 6 |

Using pi<4, sqrt(2)<2 and e<3 in (3), any positive ell_j exceeds
min_(i!=j) h_i / (64 P_j 3^(ceil K_j)). Every nonisometric weight support
therefore has the explicit geometry-only bound

\[
                         \ell_\infty>\frac1{960\,3^{150}}.       \tag{17}
\]

This uniformity concerns the limiting support coefficient, which can
change discontinuously when a label weight reaches zero. It does not
give a depth uniform in all weight vectors: the earlier finite-tau and
relative estimates still depend on positive masses.

As an analytic normalization control, take v_0=0, v_i=e_i for i=1,2,3,
h_i=1. Put beta_10=alpha_1=alpha_2=alpha_3=1/4 and all other weights zero.
Only ell_0 is nonzero. Its cell is the negative octant and A_0={e_1}, so
ell_0=pi/2 by direct integration of -2 theta_1. In the interpolation,
F(X)=X_1 and

\[
                     \Psi(r)=-\frac{r}{4\sqrt{2\pi}}.
\]

Indeed E[X_1|Y_1]=rY_1, the two other independent half-lines each have
probability 1/2, and E[Y_1 1_(Y_1<=0)]=-1/sqrt(2pi). Equation (13)
gives the same pi/2. This checks both the sign and sphere normalization.

An isometric support control has alpha_0=beta_20=alpha_1=1/3 and all
other weights zero. Here J={0,1}, S_0={2}, so S_0 and J are disjoint,
Gamma=0 and ell_infinity=0 even though a flap mass moves. The other
occupied tip has only a fixed label. This is a zero criterion,
not a counterexample to the strict theorem.

[verify_support.py](verify_support.py) supplies exact rational controls
on the dual bases, covariance factorization, inverse/determinant algebra,
box constants, zero-label cases, and the geometric lower-bound data for
the earlier asymmetric tetrahedron. It performs no Gaussian integration.
Its finite controls do not constitute an independent review or a
formalization of the analytic interpolation and tail arguments.

The Gaussian interpolation is standard Price calculus. The application
to this normal-fan support coefficient, its exact equality criterion
and its use to close the arbitrary-flap shallow theorem are the claims
made here. See [SOURCES.md](SOURCES.md) for attribution. Corollary 8 still
uses the first-variation/threshold-floor theorem, the finite-tau strict
coefficient, and the explicit relative error proved in the earlier files.

The classical family is now excluded as a shallow fixed-variance
counterexample for each fixed law. Arbitrary depths, depth uniform over
all variances, and arbitrary indecomposable maps remain outside this
theorem. No Kneser--Poulsen conclusion follows by changing these quantifiers.

The concurrent [two-template reduction](../gaussian_flap_tournament_reduction/PROOF.md)
concerns orthocentric flaps at depth one. Its target collisions are
essential to its lossless witness compression. Corollary 8 controls
sufficiently shallow versions of those supported configurations but
does not establish their depth-one comparison. This is a complementary
sign input, with neither proof used as a premise of the other.
