# The whole four-double angular class and its displacement basin

Actual author **six-sendov-2**, role **researcher**, 2026-09-30.
Status: complete ordinary written author proof, supplemented by exact
rational certificates. Independent review of this extension is pending.

## 1. Functional, class and result

For a nonzero balanced real eight-vector, use the credited angular
functional
\[
 e=\mathbf1/\sqrt8,\quad P=I-ee^*,\quad
 C=P\operatorname{diag}(\theta)P|_{e^\perp},\quad
 w=\operatorname{diag}(\theta)e,
\]
\[
 \Psi=\sum_{\lambda\text{ distinct}}\|\Pi_\lambda w\|^4,
 \quad\mu_k=\sum\theta_j^k,\quad
 J=122\mu_2+\frac{224\mu_4-5760\Psi}{\mu_2},
 \quad\max_j|\theta_j|=1.                                      \tag{1}
\]
Full spectral projections are used at collisions. This is the
[angular quartic](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md),
with \(K=p_8J/\mu_2\), \(p_8=10985/33554432\), and is not a newly
defined endpoint inequality. Let \(\mathcal D_2\) consist of
the balanced normalized vectors that can be partitioned into four equal
pairs. Pair levels may coincide. Equivalently, every level has even
multiplicity. There is no central symmetry hypothesis.

Define
\[
 h(u)=\frac{532+3120u-3464u^2+3120u^3+532u^4}{(1+u)^3},\quad
 q(u)=381-3292u+3206u^2+532u^3+133u^4.                         \tag{2}
\]
Let \(u_2\) be the unique root of \(q\) in \((1/8,7/50)\), and
\(J_2=h(u_2)\).

**Theorem 1.** The maximum of \(J\) on the whole class \(\mathcal D_2\)
is exactly \(J_2\). Equality holds precisely on the permutation orbit of
\[
 (1,1,-1,-1,\sqrt{u_2},\sqrt{u_2},-\sqrt{u_2},-\sqrt{u_2}).    \tag{3}
\]
In particular,
\[
 614.123304860<J_2<614.123304861<615.                          \tag{4}
\]
This whole cohort is strictly below the credited \(3+3+1+1\) value
\(J_*\ge h_*(1/9)=5472/7\). It cannot contain an unrestricted
displacement maximizer. The two scalar functions \(h\) and \(h_*\)
concern different multiplicities.

There is also a product-preserving, quantitative symmetry restoration.
After a possible sign reflection and ordering, write every vector as
\[
 \theta=(-1,-1,x,x,y,y,z,z),\quad z=1-x-y,
 \quad 1/3\le x\le1,\quad (1-x)/2\le y\le x.                 \tag{5}
\]
Put
\[
 \alpha=1-xy-xz-yz,\quad c=-xyz,\quad
 t=(1-x)(1-y)(1-z)=1-\alpha+c.                               \tag{6}
\]
Here \(t\) is an algebraic asymmetry parameter, not a phase magnitude.
For all of (5), including its collisions,
\[
 \boxed{h(c)-J\ge\frac{211616}{405}t,\qquad
 J_2-J\ge\frac{211616}{405}t+100(c-u_2)^2.}                  \tag{7}
\]
The function \(h(c)\) in this bound is also defined for negative \(c\).
In that case it is an algebraic comparison, not a centrally symmetric
real slope vector. The loss coefficient is a uniform lower bound, not
an asserted sharp normal coefficient. Formula (7) gives optimizer
rigidity: a near-maximal sequence has \(t\to0\), \(c\to u_2\), and its
distance to (3), after permutation, tends to zero.

## 2. Complete coverage and exact active cubic

At least one coordinate has absolute value one. Reflection makes a
saturated pair equal to \(-1\). Sort the three remaining pair levels
\(x\ge y\ge z\). Their sum is one; therefore \(x\ge1/3\),
\(y\ge(1-x)/2\ge0\), and \(z\ge1-2x\ge-1\).
Conversely, all of (5) is balanced and normalized. Thus this includes
every saturation choice and every pair collision. A full rectangular
chart is
\[
 x=(1+2s)/3,\quad y=(1-x)/2+(3x-1)v/2,\quad
 0\le s,v\le1.                                             \tag{8}
\]
The entire edge \(s=0\) maps to the same triple collision.

Set
\[
 g(\lambda)=(\lambda+1)(\lambda-x)(\lambda-y)(\lambda-z)
 =\lambda^4+e_2\lambda^2-e_3\lambda+e_4,
\]
\[
 e_2=xy+xz+yz-1=-\alpha,\quad
 e_3=xyz-xy-xz-yz=-t,\quad e_4=c,
\]
\[
 Q=g'=4\lambda^3+2e_2\lambda-e_3,
 \quad \Delta=\operatorname{Disc}(Q)=-128e_2^3-432e_3^2.     \tag{9}
\]
The eight-slope polynomial is \(H=g^2\), so \(H'=2gQ\).
Equal-coordinate difference modes have zero \(w\)-weight. The three
possible positive-weight compression modes are the roots of \(Q\).
For a simple root \(\lambda\) of \(Q\), the secular residue gives
\[
 r_\lambda=\|\Pi_\lambda w\|^2
 =-\frac{8H(\lambda)}{H''(\lambda)}
 =-\frac{4g(\lambda)}{Q'(\lambda)}.                         \tag{10}
\]
At a coincident slope and simple \(Q\)-root, the last expression is zero:
the whole mode has zero weight. The first fraction in (10) is then
understood through the last expression, not evaluated as \(0/0\).

There is exactly one zero-discriminant profile. The standalone checker
substitutes (8), factors \(\Delta=s^2D(s,v)\), and reconstructs all
**35** tensor Bernstein coefficients of \(D\) on the unit square.
Their minimum is exactly \(1024/9>0\). Hence \(\Delta>0\) for every
\(s>0\), including all other pair collisions. At \(s=0\),
\(\theta=(-1)^2,(1/3)^6\); this case is evaluated directly below.

For \(\Delta>0\), cubic radicals can be avoided entirely. Multiplication
by \(\lambda\) in \(\mathbb Q[e_2,e_3,e_4][\lambda]/(Q)\) has matrix
\[
 M=\begin{pmatrix}0&0&e_3/4\\1&0&-e_2/2\\0&1&0\end{pmatrix},
 \quad Y=12M^2+2e_2I,\quad \det Y=-\Delta/4.
\]
Modulo \(Q\),
\(-4g=f=-2e_2\lambda^2+3e_3\lambda-4e_4\). Therefore
\[
 \Psi=\operatorname{tr}(f(M)^2Y^{-2})=\frac{N_\Psi}{\Delta},
\]
\[
 N_\Psi=-16e_2^5+128e_2^3e_4-36e_2^2e_3^2
                   -768e_2e_4^2+864e_3^2e_4.                \tag{11}
\]
The checker derives \(16\operatorname{tr}(f(M)^2\operatorname{adj}(Y)^2)\),
divides it by \(\Delta\), and checks the full multiplication back.
There are no root-finding or floating inputs to this identity.
Newton identities give
\(\mu_2=4\alpha\), \(\mu_4=4\alpha^2-8c\).

## 3. Product-preserving symmetry restoration

An especially useful simplification of (11) is
\[
 \Psi=\frac{\alpha^2}{8}-c+\frac{6c^2}{\alpha^2}
       +\frac{18e_3^2(\alpha^2+12c)^2}{\alpha^2\Delta}.
\]
Thus the **exact** angular objective is
\[
 \boxed{J=F(\alpha,c)
       -\frac{25920t^2(\alpha^2+12c)^2}{\alpha^3\Delta},
 \quad F(\alpha,c)=532\alpha+\frac{992c}{\alpha}
                                  -\frac{8640c^2}{\alpha^3}.} \tag{12}
\]
This identity concerns the present equal-pair class. It does not assert
a symmetry-restoration shortcut in the previously studied asymmetric
\(3+3+1+1\) class, where a different proposed comparison fails.

We have \(\alpha\ge2/3\) by Cauchy--Schwarz on \(x+y+z=1\), and
\(t\ge0\) because all levels are at most one. Also
\(-1/27\le c\le1\): when \(z\ge0\), AM--GM bounds
\(xyz\le1/27\); when \(z<0\), all absolute values are at most one.
In particular, \(1+c=\alpha+t>0\). For every fixed real \(c\) and
positive \(\alpha\), put \(w=c/\alpha^2\). Then
\[
 \partial_\alpha F=532-992w+25920w^2
 =\frac{211616}{405}+25920\left(w-\frac{31}{1620}\right)^2.
                                                                  \tag{13}
\]
The last term in (12) is nonnegative. Integrating (13) from
\(\alpha\) to \(1+c\) proves
\[
 J\le F(\alpha,c)\le F(1+c,c)-\frac{211616}{405}t
                    =h(c)-\frac{211616}{405}t.               \tag{14}
\]
For \(c\ge0\), the comparison \(h(c)\) is attained by the actual
centrally symmetric pair levels \((-1,1,\sqrt c,-\sqrt c)\).
For \(c<0\), each nonconstant term in
\[
 h(c)=532(1+c)+\frac{992c}{1+c}-\frac{8640c^2}{(1+c)^3}
\]
is nonpositive relative to 532, so \(h(c)<532\).

At the only excluded discriminant corner, the compression has just one
positive-weight eigenvalue \(-2/3\). Its weight is
\(\|w\|^2=\mu_2/8=1/3\). Hence
\[
 \Psi=1/9,\quad J=2336/9,\quad c=-1/27,\quad t=8/27.
\]
There is no division by \(\Delta\). Direct rational calculation gives
\[
 h(-1/27)-2336/9=11941760/59319
                  >1692928/10935=(211616/405)(8/27).
\]
Consequently (14) holds on the whole class, including the singularity.

## 4. Scalar maximum and quantitative rigidity

Differentiating the whole symmetric curve gives
\[
 h'(u)=\frac{4q(u)}{(1+u)^4}.                                \tag{15}
\]
The coefficient signs of \(q\) have two variations. Descartes' rule
allows at most two positive roots, counted with multiplicity. Exact
signs are positive at \(1/8\), negative at \(7/50\) and \(3/4\), and
positive at one. There is therefore exactly one simple root in each of
\((1/8,7/50)\) and \((3/4,1)\), and no other positive roots.
The first is a local maximum and the second a local minimum.
Since \(h(1/8)>600\), \(h(0)=532\), and \(h(1)=480\), the first is
the unique global maximizer on \([0,1]\). Negative \(c\) cannot compete.
Together with (14), this proves the maximum assertion.

The exact checker also constructs the divided-difference polynomial
\(L(r,u)\) satisfying
\[
 h_N(r)(1+u)^3-h_N(u)(1+r)^3
  =(u-r)^2L(r,u)-4q(r)(1+r)^2(u-r),                          \tag{16}
\]
where \(h_N\) is the numerator in (2). All **24** tensor Bernstein
coefficients of
\(L(r,u)-100(1+r)^3(1+u)^3\) are strictly positive on
\([1/8,7/50]\times[0,1]\); the minimum is
\(67837093119/78125000\). At \(r=u_2\), (16) yields
\[
 J_2-h(u)\ge100(u-u_2)^2\quad(0\le u\le1).                 \tag{17}
\]
For \(-1/27\le c<0\), we instead use
\[
 J_2-h(c)>600-532>100(1/27+7/50)^2
                             \ge100(c-u_2)^2.
\]
Combining with (14) proves both parts of (7).
Equality in the maximum requires \(t=0\) and \(c=u_2\).
Since the levels are ordered, \(t=0\) means \(x=1\);
then \(z=-y\) and \(c=y^2\). This is exactly (3).
The same argument plus compactness proves the stated orbit rigidity.

The decimal bounds (4), and the basin bounds below, follow from forty
exact rational bisections of the isolated quartic root and rational
Horner interval evaluation. The complete bounds appear in expected.json.
They are not a floating optimization claim.

## 5. Complex paired-phase displacement basin

Let
\[
 p(z)=b(z-a)\prod_{j=1}^8(z-z_j),\quad b\ne0,\quad
 0<a<1,\quad |z_j|\le1,
\]
with simple marked root \(a\). Repeated other roots are allowed.
Count critical points with algebraic multiplicity and put
\[
 F_a=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\quad
 G_a=F_a-\frac{16}{1+a},\quad \rho=\max_j|z_j+1|,\quad
 \kappa=(1+a)(a-5/8),\quad d_0=13/8.
\]
For \(\rho\le1/2\), write uniquely
\(z_j=-(1-\tau_j)e^{i\phi_j}\), with \(\tau_j\ge0\) and small
real principal phases. Define the **paired-phase class** by requiring
the eight phases to be partitionable into four equal pairs, allowing
collisions and the case all phases are equal. Inward depths may be
independent; the polynomial need not have real coefficients. Centering
the phases preserves this pairing condition.

Define \(R_{2^4}(a)\) as the supremum of admissible radii
\(r\in[0,1/2]\): for every polynomial in this class with
\(\rho\le r\), require \(G_a\ge0\). Radius zero is admissible.
Endpoint admissibility is not assumed.

**Corollary 2.** For this whole complex phase class,
\[
 \boxed{\lim_{a\downarrow5/8}\frac{R_{2^4}(a)^2}{\kappa}
        =B_2=\frac{106496}{5J_2},\qquad
 34.682285839<B_2<34.682285840.}                             \tag{18}
\]
For every \(\varepsilon>0\), sufficiently small positive \(a-5/8\)
and \(\rho^2\le\kappa d_0^4/(p_8J_2+\varepsilon)\) imply
\(G_a\ge0\), where \(p_8=10985/33554432\).
Near-sharp negative-gap sequences in this class have negligible inward
depth and squared mean phase relative to squared reciprocal energy;
their max-normalized centered directions approach (3), and \(G_a/E_a^2\to0\).

This corollary specializes the credited
[all-disk displacement reduction](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_displacement_variational_basin/PROOF.md)
and its
[joint expansion](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_sharp_energy_basin/PROOF.md).
For clarity, their uniform negative-gap bootstrap gives, with
\(T=\sum\tau_j\), \(M=\sum\phi_j\),
\(s_0=\|\phi-(M/8)\mathbf1\|\), and unit centered direction \(\eta\),
\[
 T=O(s_0^4),\quad M^2=O(s_0^4),\quad \kappa=O(s_0^2),
\]
\[
 G_a=\kappa E_a+\frac{128}{169}T+\frac{40}{2197}M^2
                  -K(\eta)E_a^2+o(E_a^2),
 \quad \rho^2/E_a=d_0^4q_\infty(\eta)+o(1),                \tag{19}
\]
where \(E_a=\sum|(a-z_j)^{-1}-(1+a)^{-1}|^2\) and
\(q_\infty=\max\eta_j^2\). Negative gap forces \(s_0>0\).
Max-normalize \(\eta\) to obtain a direction in \(\mathcal D_2\);
then \(K(\eta)/q_\infty(\eta)=p_8J\le p_8J_2\).
Equation (19) rules out every failure strictly below the claimed scale,
exactly as in the cited reduction.

For the matching upper family, take (3), divide it by \(\sqrt{\mu_2}\)
to get \(\eta_2\), fix \(\lambda>1\), and use actual disk polynomials
\[
 s_0^2=\lambda\kappa d_0^4/K(\eta_2),\qquad
 p_a(z)=(z-a)\prod_j(z+e^{is_0\eta_{2,j}}).
\]
They have paired phases, \(T=M=0\), and a simple marked root.
Equation (19) gives \(G_a<0\) and
\(\rho^2=\lambda\kappa d_0^4/(p_8J_2)+O(\kappa^2)\).
Taking \(\lambda\downarrow1\) proves (18), since
\(d_0^4/p_8=106496/5\). The same equality-chain argument in (19)
forces \(J\to J_2\), negligible positive penalties, and the stated
direction rigidity via (7).

The quantifier “sufficiently small” has no effective numerical cutoff
here. No finite-radius first-crossing uniqueness is claimed. At the
collapsed cutoff the comparison is \(128/13>8\); a negative \(G_a\)
is not a first-power counterexample. The unrestricted angular maximum,
unrestricted complex displacement basin, and full degree-nine first-power
Tang--Zhang endpoint remain open in this work.

## 6. Verification and trust boundary

The standalone checker uses only Python 3.11 standard-library rational
arithmetic. It checks the exact companion trace, complete cancellation,
the restoration square, whole-chart identities, the 35 discriminant
and 24 curvature coefficients with inverse basis reconstruction, scalar
root signs, root/value enclosures, and 14 full eight-coordinate rational
compression controls. The latter compute the Frobenius projection of
\(ww^*\) onto the symmetric commutant, a different route from cubic
residues. They include all corner types and the singular triple collision.

These are author checks, not independent review or formalization. The
coverage argument, spectral identification, Descartes principle,
integration, and cited analytic expansion are written mathematics.
The manifest is a complete regression record, not an imported proof
oracle. Verification rejects absent or changed manifests even under
Python optimization. Exploratory meshes played no role in this proof.
