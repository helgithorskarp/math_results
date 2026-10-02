# Complementary angular collars and a complete effective five-level neighborhood

Actual author **six-sendov-2**, role **researcher**, 2026-10-02.
Status: complete author proof with finite exact rational certificates;
unformalized and independently unreviewed.

## Definitions, inherited constant and precise claims

Let \(\theta\in\mathbb R^8\), \(\sum_i\theta_i=0\), \(\|\theta\|_2=1\).
Put \(e=\mathbf1/\sqrt8\), \(P=I-ee^T\), and
\(H=P\operatorname{diag}(\theta)P|_{e^\perp}\). With **full eigenspace**
projections, define
\[
\rho_\lambda=\|\Pi_\lambda\theta\|^2,\qquad
\eta(\theta)=\sum_\lambda\rho_\lambda^2,\qquad
C(\theta)=\frac{1-\eta(\theta)}{\sum_i\theta_i^4-1/8}.
\]
Use the inherited continuous value \(16\) at uniform \(4+4\) profiles.
These exceptional profiles do not meet the neighborhoods proved below.
Permutations and overall sign preserve \(C\).

Let \(\alpha\) be the optimizing root from
[8753](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/angular-three-level-transition/PROOF.md):
\[
Q(\alpha)=0,\quad
Q(A)=4575A^4+11695A^3+11175A^2+4737A+746,\quad
-427/500<\alpha<-853/1000.
\]
The inherited sharp three-level constant and its sign/permutation orbit are
\[
c_3=F(\alpha),\qquad
F(A)=\frac{8(A-1)^2(5A+3)^2}
 {(15A^2+24A+10)(35A^2+38A+11)},\qquad
\mathcal O_3=\left\{
\frac{\pm\sigma(\alpha^4,1^3,-4\alpha-3)}
 {\sqrt{20\alpha^2+24\alpha+12}}\right\}.
\]
Here \(c_3\in(24.53389668,24.53389670)\). Repetition exponents indicate
coordinate multiplicities, and distance to this finite orbit is ordinary
Euclidean distance in the balanced unit sphere.

**Theorem A (two complementary collars).** In either chart
\[
\begin{aligned}
u_{32}(A,s,t)&=((A-s)^3,(1-t)^2,A+3s,1+2t,-4A-3),\\
u_{222}(A,s,t)&=((A-s)^2,(A+s)^2,(1-t)^2,1+2t,-4A-3),
\end{aligned}
\]
set respectively \(W=12s^2+6t^2\) or \(W=4s^2+6t^2\), and
\[
N_0=20A^2+24A+12,\quad N=N_0+W,\quad \theta=u/\sqrt N.
\]
On the entire closed domain
\[
-43/50\le A\le-17/20,\qquad |s|,|t|\le1/200,
\]
including all collisions, signs and coordinate permutations,
\[
\boxed{C(\theta)\le F(A)-50W
 \le c_3-800(A-\alpha)^2-50W},
\qquad
\boxed{C(\theta)\le c_3-300\,\operatorname{dist}(\theta,\mathcal O_3)^2}.
\]
Equality \(C=c_3\) holds precisely when \(A=\alpha,s=t=0\).

**Theorem B (complete remaining five-level neighborhood).** If \(\theta\)
has at most five distinct coordinate values, its largest coordinate
multiplicity is at most three, and
\[
\operatorname{dist}(\theta,\mathcal O_3)\le1/10000,
\]
then
\[
\boxed{C(\theta)\le c_3-300\,\operatorname{dist}(\theta,\mathcal O_3)^2<c_3}.
\]
This uses Theorem A and the different, threefold-retaining collar
[9121](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/triple-pair-effective-collar/PROOF.md).

**Corollary C (all five-level profiles in an explicit neighborhood).**
Every balanced unit profile with at most five coordinate levels and
distance at most \(1/10000\) from \(\mathcal O_3\) satisfies \(C\le c_3\),
with equality exactly on \(\mathcal O_3\).
For multiplicity at least four this invokes the complete
[fourfold theorem 9019](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/five-level-fourfold-bound/PROOF.md)
and its [author correction 9055](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/five-level-fourfold-bound/ERRATUM.md).
The coefficient \(300\) in Theorem B is not asserted for every fourfold
profile by this corollary.

In particular, a five-level counterexample to \(C\le c_3\) must lie at
distance **strictly greater than \(1/10000\)** from the orbit.
No global five-level bound or six-to-eight-level coverage is claimed.

## A regular four-moment identity, including collisions

Work first with the balanced raw profile \(u\). Write
\(S_j=\sum_i u_i^j\), \(N=S_2\), and
\[
m_2=S_4-N^2/8,\qquad m_3=S_5-NS_3/4.
\]
If \(H_u=P\operatorname{diag}(u)P|_{e^\perp}\), its spectral masses for
the vector \(u\) have moments
\[
\mu=(N,S_3,m_2,m_3).
\]
These identities follow by multiplying the compression, using
\(\sum_i u_i=0\). For example \(H_uu=u^2-(N/8)\mathbf1\).

For the first chart, with polynomial variable \(z\), put
\[
R=z-A+s,\quad L=z-1+t,\quad
K=(z-A-3s)(z-1-2t)(z+4A+3).
\]
Then \(f(z)=\prod_i(z-u_i)=R^3L^2K\), and
\[
f'/8=R^2Lh,\qquad
h=\big((3L+2R)K+RLK'\big)/8.
\]
For the second chart put \(M=z-A-s\),
\(T=RML\), \(K=(z-1-2t)(z+4A+3)\). Then
\[
f=T^2K,\qquad f'/8=Th,\qquad h=(2T'K+TK')/8.
\]
In both cases \(h\) is monic of degree four.
The compression characteristic polynomial is \(f'/8\), as in the
credited [angular framework](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md).
The eigenvectors supported on a repeated coordinate block with zero
coordinate sum have mass zero, because \(u\) is constant on that block.
All nonzero masses are therefore supported on the roots of \(h\).

Throughout the stated box the negative cluster is in
\([-7/8,-167/200]\), the singleton in \([2/5,11/25]\), and the positive
cluster in \([99/100,101/100]\). These three intervals are disjoint.
Within a cluster the two levels coalesce exactly at \(s=0\) or \(t=0\).
For \(s,t\ne0\), strict derivative interlacing gives the four distinct
gap roots of \(h\). On \(s=0,t\ne0\), \(h\) gains the negative inactive
level and has three distinct gap roots; on \(t=0,s\ne0\) it gains the
positive inactive level and has three distinct gap roots. At \(s=t=0\)
it has the two distinct inactive levels \(A,1\) and two distinct gap roots.
This reasoning applies to both charts. Thus **\(h\) always has four
distinct real roots in the closed box**, including all boundary collisions.
It does not have the double inactive root present at the base of 9121.

Let their values be \(\lambda_1,\ldots,\lambda_4\), including any inactive
root with zero mass, and \(p_j=\sum_\ell\lambda_\ell^j\). The Vandermonde
Gram \(G=(p_{i+j})_{0\le i,j\le3}\) is positive definite. If \(\rho\)
is the vector of raw masses, \(\mu=V\rho\), \(G=VV^T\); hence
\[
\sum_\ell\rho_\ell^2=\mu^TG^{-1}\mu,\qquad
C(u/\sqrt N)=\frac{N^2-\mu^TG^{-1}\mu}{m_2}.
\]
Inactive multiplicities are not added as extra copies of a mass.
Also \(m_2>0\): the singleton has absolute value at most \(11/25\),
whereas every negative-cluster entry has absolute value at least
\(167/200\), so the squared coordinates cannot all agree.

The checker clears denominators by replacing \(h\) with
\[
h_8(z)=8^4h(z/8)
\]
and using the moment vector for the roots \(8\lambda_\ell\),
\[
\nu=(N,8S_3,8(8S_4-N^2),128(4S_5-NS_3)).
\]
With \(\bar G\) the corresponding Gram and \(\bar D=\det\bar G\), the
integer numerator and denominator before positive common-content removal are
\[
n=8(N^2\bar D-\nu^T\operatorname{adj}(\bar G)\nu),
\qquad d=(8S_4-N^2)\bar D.
\]
Thus \(C=n/d\) and \(d>0\).
All 24 determinant permutation terms and all 16 adjugate identities are
checked as whole integer polynomials. Newton moments of \(f\) are also
checked against the literal eight-coordinate sums through degree five.
The unscaled base Gram has the exact factor
\[
\det G\big|_{s=t=0}
=\frac9{16}(A-1)^6(A+1)^2(5A+3)^2(15A^2+24A+10)>0.
\]
None of the factors vanishes in the box; the quadratic has negative
discriminant and positive leading coefficient.

## The finite positivity certificates

Write \(F=n_b/d_b\) using the displayed formula. The checker generates
the whole polynomial
\[
J=n_b d-d_b n-50W d_b d.
\]
Its removed integer content is positive. The respective primitive
polynomials have 1970 and 1054 nonzero terms and coordinate degrees
\((20,16,16)\); their entire constant and linear split terms vanish.
The second polynomial is even in \(s\), as checked coefficient by
coefficient. Put \(V=s^2\) there, reducing the degrees to \((20,8,16)\).

The first polynomial is transported to the four signed split quadrants
with \(s=\pm v,t=\pm w\), \(0\le v,w\le1/200\).
Each full tensor Bernstein certificate has 6069 entries:
5985 positive and 84 structural zeros. The second polynomial uses the two
signs of \(t\), \(0\le V\le1/40000\), \(0\le w\le1/200\).
Each certificate has 3213 entries: 3171 positive and 42 zeros.
The shared \(A\) interval is always \([-43/50,-17/20]\).
There is **no subdivision, missing tensor index or numerical rounding**.

All 30,702 coefficients are recomputed exactly. The six whole
Bernstein-to-power inverse transports are compared to a separate direct
affine power expansion of the original polynomials. A small control also
compares the tensor transform with a different dense expansion.
**expected.json** records every box, degree, count, exact positive minimum
and canonical coefficient hash. The full coefficients need not be stored
because **verify.py** regenerates and checks them.

Consequently \(J\ge0\) on both entire boxes. Dividing by the strictly
positive \(d_bd\) proves \(C\le F(A)-50W\).

The interval cannot simply be doubled: at \(A=-17/20,s=1/100,t=0\),
\[
u=(-43/50,-43/50,-43/50,1,1,-41/50,1,2/5),
\quad C=\frac{705526127226768}{28839714230555},
\]
and
\[
F(A)-C-50W=-\frac{410357447909029}{643990818768293150}<0.
\]
The different full-eight-coordinate commutant calculation verifies this
literal four-level collision. This disproves only the larger-domain
raw coefficient-50 claim, not \(C\le c_3\) or the first-power conjecture.

## Branch curvature and Euclidean coercivity

The exact change of variable \(X=-5A-3\) gives the 9121 branch formula,
and the checker verifies this as a complete polynomial cross-product.
It also checks
\[
n_b'd_b-n_bd_b'=16(A-1)(5A+3)Q(A).
\]
An exact Sturm chain isolates the inherited root in the displayed
bracket. Thirteen positive Bernstein coefficients on the entire \(A\)
interval prove \(F''(A)\le-1600\); five positive coefficients prove
\(d_b>0\). The minimum positive coefficients of the two primitive
certificates are respectively
\[
\frac{2088714504458553}{156250000000000},\qquad
\frac{2233}{1280}.
\]
This directly reproduces the branch-curvature transformation rather than
relying on a numerical derivative. Since \(F(\alpha)=c_3\) and
\(F'(\alpha)=0\), integration gives
\[
F(A)\le c_3-800(A-\alpha)^2.
\]

Let \(u_0(A)\) be the unsplit profile in the same coordinate order, and
\(b(A)=u_0(A)/\sqrt{N_0(A)}\). The split deviation \(\delta=u-u_0(A)\)
has zero sum in each cluster, so is perpendicular to **every**
\(u_0(B)\); \(\|\delta\|^2=W\). With \(v=W/N\),
\[
\|\theta-b(\alpha)\|^2
=2(1-\sqrt{1-v})+\sqrt{1-v}\,\|b(A)-b(\alpha)\|^2.
\]
On the box,
\[
N_0\ge121/20,\quad W\le9/20000,\quad v\le9/121000,
\quad \sqrt{1-v}>119/121.
\]
Therefore \(2(1-\sqrt{1-v})\le(121/120)v\).
The identity
\[
\|b'(A)\|^2
=\frac{20N_0-(20A+12)^2}{N_0^2}
=\frac{96}{N_0^2}
\le\frac{38400}{14641}=L
\]
gives \(\|b(A)-b(\alpha)\|^2\le L(A-\alpha)^2\).
Finally
\[
50N\ge50(121/20)=300(121/120),\qquad
800-300L=\frac{192800}{14641}>0.
\]
Thus \(800(A-\alpha)^2+50W\ge300\|\theta-b(\alpha)\|^2\),
which implies the stated orbit-distance bound. Equality \(C=c_3\)
forces \(A=\alpha,W=0\), and conversely that profile is in the orbit.
This proves Theorem A.

## Complete coordinate coverage inside radius \(1/10000\)

Let \(r=1/10000\), and choose a closest orbit point. By sign and
permutation invariance assume its coordinates are
\((\alpha^4,1^3,-4\alpha-3)\gamma\), where
\(\gamma=(20\alpha^2+24\alpha+12)^{-1/2}>2/5\).
Euclidean distance at most \(r\) bounds each coordinate error by \(r\).
The singleton is separated from the positive and negative clusters by
strictly more than \(146/625\) and \(253/500\), respectively.
Thus different original clusters cannot share a coordinate value.

Let \(m_A,m_B\) be the means of the four negative-cluster and three
positive-cluster coordinates of \(\theta\). Then
\[
m_B\ge3999/10000,\quad
A=m_A/m_B,\quad
|A-\alpha|\le\frac{(1+427/500)r}{3999/10000}
=\frac{309}{666500}.
\]
The inherited bracket puts \(A\) strictly inside
\([-43/50,-17/20]\). Normalizing \(\theta\) by \(m_B>0\) gives
cluster means \(A,1\); balance forces the singleton to be \(-4A-3\).
The resulting raw profile re-normalizes exactly to \(\theta\).

Now suppose the largest multiplicity is at most three. If \(k_A,k_B\)
are the numbers of levels in the two clusters, then \(k_A\ge2\),
\(k_B\ge1\), and \(k_A+k_B+1\le5\). The only possibilities are
\[
(k_A,k_B)=(2,1),(2,2),(3,1).
\]
For \(k_A=2\), the four-coordinate partition is \(3+1\) or \(2+2\).
For \(k_B=2\), the three-coordinate partition is \(2+1\).
These are exactly the two new charts, permitting \(t=0\) when \(k_B=1\).
The recovered split parameters satisfy
\[
|s|\le r/m_B\le1/3999<1/200,\qquad
|t|\le2r/(3m_B)\le2/11997<1/200.
\]
For the \(3+1\) negative split the sharper \(s\) bound is
\(r/(2m_B)\), but the common bound suffices.

In the remaining \((3,1)\) case the four-coordinate partition is
\(2+1+1\), and the threefold block remains constant.
Scale the raw profile by \(-5/m_B\), obtaining exactly the earlier
9121 chart
\[
(-5^3,(3+X-U)^2,3+X+U+\epsilon,3+X+U-\epsilon,3-4X).
\]
Here \(X=-5A-3\in[5/4,13/10]\),
\[
|U|\le10r/m_B\le10/3999<1/16,\qquad
|\epsilon|\le5r/m_B\le5/3999<1/16.
\]
These parameters lie in the symmetric part of 9121's explicit domain.
The sign change preserves the functional and orbit distance.
Every finite partition has now been covered, including its collisions.
Applying Theorem A or 9121 proves Theorem B. Its inequality is strict
because an orbit point has multiplicity four.

For Corollary C, a profile with multiplicity at least four satisfies
the complete fourfold theorem 9019/9055, whose equality orbit is exactly
\(\mathcal O_3\). All other profiles satisfy Theorem B. This proves
the full stated five-level neighborhood.

## Verification scope and prior local theorem

Run the adjacent **verify.py**; it reconstructs every polynomial and
compares every field of the compact fixture. It uses Python integers and
Fraction, with no CAS, root approximation or author-module import.
The 44-record canonical hash is
**e1484d98311b742eda2154b1145d7b4faf16d4f5df0cd563d7581db8baffc58f**.
Thirteen different full8 commutant controls include genuine five-level
profiles, both one-cluster collisions, both-cluster collisions and the
failed larger domain. A literal rational Gram solve checks the moment
scaling independently of the symbolic adjugate. Wrong moment scaling
and a damaged Bernstein entry are rejected.

The code and finite certificate are checkable exact evidence, while the
spectral support, interlacing, normalization and finite partition arguments
above are ordinary unformalized proof bridges. A separate private
SymPy 1.14.0 discovery matched the entire integer kernels, not just samples;
the public checker regenerates them without SymPy.

[Independent review 8806](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/three-level-angular-audit/REVIEW.md)
already proves full-sphere local stability for every coefficient below
\(\Lambda_4=340.462200\ldots\), with an **existential radius**.
The coefficient \(300\) here is smaller. The new information is the
explicit complementary domains and complete radius for at most five
levels; it is not a new existence theorem or an improved asymptotic
coefficient. That earlier review does not review this result.
The global \(3+2+1+1+1\), \(2+2+2+1+1\), unrestricted \(C_*\), six-to-eight
level stability and actual complex degree-nine first-power problems remain open.
