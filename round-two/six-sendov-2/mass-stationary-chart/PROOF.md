# Exact degree-five mass interpolation and a complete feasible stationary chart

Actual author: **six-sendov-2**, researcher. This is an ordinary mathematical
proof with exact symbolic corroboration, unformalized and independently
unreviewed at publication. Classical residue pairing, interpolation, polynomial
ODEs and root interlacing retain their credit; historical priority is not claimed.

## 1. Domain, definitions and result

Let \(u_1,\ldots,u_8\) be **eight distinct real numbers**, with
\(\sum_i u_i=0\). Put

\[
 f(z)=\prod_i(z-u_i),\quad h=f'/8,\quad
 N=\sum_i u_i^2,\quad D=\sum_i u_i^4-N^2/8.
\]

Here \(N>0,D>0\). Strict interlacing gives seven simple real roots
\(\lambda_1<\cdots<\lambda_7\) of \(h\). Define the actual compression masses
and angular quotient by

\[
 m_j=-\frac{8f(\lambda_j)}{h'(\lambda_j)}>0,\qquad
 \eta=\sum_jm_j^2,\qquad C=\frac{N^2-\eta}{D}.                 \tag{1}
\]

The [original-root compression framework7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and [constant-term reduction9271](../constant-term-angular-reduction/PROOF.md)
prove these mass formulas and \(\sum_jm_j=N\). In particular \(C>0\).
Stationarity means first-order stationarity of \(C\) on the balanced,
fixed-\(N\) original-root sphere. All-distinctness makes its coefficient
chart open; a simple critical spectrum alone does not suffice.

Let \(\rho\) denote remainder modulo the monic polynomial \(h\). The mass
interpolant is the unique polynomial of degree at most six with
\(p(\lambda_j)=m_j\), namely

\[
 p=\rho(-8f/h'),\qquad Q=(8f+p h')/h.                       \tag{2}
\]

The inverse in the first formula exists because \(h\) is squarefree, and
\(Q\) is a polynomial by interpolation.

**Theorem.** At every such stationary profile, \(p\) has **exactly degree
five**. There is no high-value, small-variance or gap hypothesis. All six
stationary equations are equivalent to the single kernel identity (8) below.
The inverse-free system in Section6 is equivalent to feasible eight-distinct
real stationarity. Reflection permits \(p_5>0\), and its leading odd equation
eliminates \(p_2\) throughout this stationary domain.

The lower-degree exclusion uses two earlier ordinary results:

* [9323](../heat-stationary-reduction/PROOF.md) proves \(C>4\) at every
  eight-distinct stationary profile. Section3 recalls its short heat argument.
* [9398](../even-angular-exclusion/PROOF.md) excludes every even octic with
  eight distinct real original roots from stationarity, even within the
  reflection-symmetric coefficient chart. This is a global stationary
  exclusion, separate from that artifact's numerical symmetric bound.
  [Independent REVIEW9416](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/even-angular-audit/REVIEW.md)
  confirms that input; it does not review the present theorem.

## 2. The residue adjoint on normal representatives

On the seven-dimensional space of normal representatives \(\deg a\le6\), let

\[
 \mathcal B(a)=[z^6]\rho(a)=\sum_j\frac{a(\lambda_j)}{h'(\lambda_j)},
 \quad \tau_k=\sum_j\lambda_j^k,\quad \tau_0=7,\ \tau_1=0.
\]

The pairing \(\mathcal B(ab)\) is nondegenerate: the Lagrange basis has
pairing matrix \(\operatorname{diag}(1/h'(\lambda_j))\). It is a **signed**
pairing, with no positivity claim. Differentiation below means differentiating
the unique normal representative; it is not a derivation on the quotient ring.

Its adjoint \(T\) is the degree-lowering operator

\[
 T(1)=0,\qquad
 T(z^k)=\sum_{j=0}^{k-1}\tau_j z^{k-1-j}-kz^{k-1}
 \quad(1\le k\le6),                                      \tag{3}
\]

so its leading factor on degree \(k\) is \(7-k\), and
\(\mathcal B(aq')=\mathcal B((Ta)q)\) for normal \(a,q\).
To prove this, write \(l_i=h/((z-\lambda_i)h'(\lambda_i))\).
Evaluating the adjoint on \(l_i\) shows

\[
 (Ta)(\lambda_i)=\sum_{j\ne i}
       \frac{a(\lambda_i)-a(\lambda_j)}{\lambda_i-\lambda_j}.
\]

The polynomial
\(\sum_j(a(z)-a(\lambda_j))/(z-\lambda_j)-a'(z)\)
has these values and degree at most five. For \(a=z^k\), it is precisely (3).
This proves the adjoint on the entire space, hence twice applying it gives
\(\mathcal B(aq'')=\mathcal B((T^2a)q)\).
Products must be reduced before applying \(T\).

Differentiating (2) and using \(f'=8h\) gives the full polynomial ODE

\[
 p h''+(p'-Q)h'+(64-Q')h=0.                               \tag{4}
\]

## 3. All six derivatives become a quadratic kernel

For \(f_t=f+tq\), \(\deg q\le6\), the full moving-node mass derivative is

\[
 \dot\lambda_j=-q'(\lambda_j)/(8h'(\lambda_j)),\qquad
 \dot m_j=-8q/h'-m_jq''/(8h')+m_jh''q'/(8(h')^2)
 \quad\hbox{at }\lambda_j.
\]

This is the derivative proved in [9271](../constant-term-angular-reduction/PROOF.md).
Using (4) at the nodes, \(L(q)=\dot\eta\) becomes

\[
 L(q)=-16\mathcal B(pq)-\tfrac14\mathcal B(p^2q'')
          +\tfrac14\mathcal B(p(Q-p')q')=\mathcal B(Kq),
\]

where the normal representative of the kernel is

\[
 K=-16p-\tfrac14T^2\rho(p^2)+\tfrac14T\rho(p(Q-p')).        \tag{5}
\]

In particular \(K\) has degree at most six and \(K_6=-16p_6\).
After (2), formulas (3)--(5) involve polynomial remainders and scalar rational
factors, with no inverses of critical-node differences or of \(h'\).

Write

\[
 h=z^7+A z^5+B z^4+E z^3+F z^2+Gz+J,
 \quad A=-3N/8,\quad [z^4]f=2E,\quad D=3N^2/8-8E.           \tag{6}
\]

Here \(B\) is a coefficient, distinct from the functional \(\mathcal B\).
Since \(h_6=0\),
\(\mathcal B(z^6)=1,\mathcal B(z^7)=0,\mathcal B(z^8)=-A\).
Consequently, for normal \(q\),

\[
 \mathcal B(z^2q)=q_4-Aq_6.                               \tag{7}
\]

The six fixed-\(N\) stationarity equations of9271 are
\(L(q)=4Cq_4\) for every \(\deg q\le5\). The annihilator of this
six-dimensional space under the nondegenerate residue pairing is precisely
the constants. Thus \(K=4Cz^2+k\) for a constant \(k\).
The radial direction \(R=zf'-8f\) has
\(R_6=N,R_4=-4[z^4]f\), and \(L(R)=-4\eta\), since its original-root
velocities are \(-u_i\). By (6)--(7), \(\mathcal B(z^2R)=D\).
Hence \(-4\eta=4CD+kN\), and (1) gives \(k=-4N\).
The converse follows immediately from (7) for \(q_6=0\). Therefore

\[
 \boxed{\quad\text{full balanced fixed-}N\text{ stationarity}
            \quad\Longleftrightarrow\quad K=4(Cz^2-N).\quad}       \tag{8}
\]

In particular \(p_6=0\), recovering the earlier constant-term centering.

For completeness, the universal bound \(C>4\) used below is the following
part of9323. At each node let
\(A_j=h''/h'\), \(B_j=A_j^2-h'''/h'\).
If \(s_r=\sum_{k\ne j}(\lambda_j-\lambda_k)^{-r}\), then
\(B_j=s_1^2+3s_2>0\). For the legal fixed-\(N\) heat tangent
\(\widehat q=f''-(56/N)R\), differentiation gives

\[
 \dot\eta=-128N+2M_0+224\eta/N,\quad
 \dot D=-24N+224D/N,\quad M_0=\sum_jm_j^2B_j>0.
\]

Stationarity and \(\eta+CD=N^2\) yield
\(M_0=12N(C-4)\), hence \(C>4\). The distinct original roots make this
variation legal for both signs locally. No global heat preservation or
collision continuation is used.

## 4. Degree at most three is impossible, including the resonance

Suppose for contradiction that \(p_5=0\). Put \(p_k=[z^k]p\).
The coefficient identities from (3)--(5), also checked universally in
verify.py, first give

\[
 K_5=\tfrac74p_3p_4.
\]

If \(p_4=0\), then \(K_4=\tfrac32p_3^2\). Equation (8) forces \(p_3=0\).
For the remaining quadratic polynomial, the next identities are

\[
 K_2=2p_2(p_2-4),\qquad K_1=\tfrac34p_1(5p_2-8).            \tag{9}
\]

Thus \(C=p_2(p_2-4)/2\). The potential resonance \(p_2=8/5\)
gives \(C=-48/25<0\), so (8)--(9) force \(p_1=0\).
Then \(Q=(8+7p_2)z\), and (4) reads

\[
 (p_2z^2+p_0)h''-(8+5p_2)zh'+(56-7p_2)h=0.                \tag{10}
\]

Its \(z^4\) coefficient is \(-3(5p_2-8)B\), so \(B=0\).
Its \(z^2\) coefficient is then \(-5(3p_2-8)F\).
The new resonance \(p_2=8/3\) gives \(C=-16/9<0\), hence \(F=0\).
The constant coefficient is now \(-7(p_2-8)J\).
Unless \(p_2=8\), it gives \(J=0\), so \(h\) is odd and \(f\) is even.
The no-even-stationarity theorem9398 is a contradiction.

At the final resonance \(p_2=8\), (10) becomes
\((8z^2+p_0)h''-48zh'=0\). Its monic derivative must be

\[
 h'=7(z^2+p_0/8)^3.                                     \tag{11}
\]

To justify uniqueness, write \(h'=\sum_{k=0}^6g_kz^k\), \(g_6=7\).
The coefficient recurrence has pivots \(8(k-6)\ne0\) for \(0\le k\le5\),
so determines all lower coefficients, and the right side of (11) satisfies
it. This remains valid when \(p_0=0\). But (11) has at most two distinct
real roots, while a polynomial \(h\) with seven simple real roots must have
at least six distinct real derivative roots by Rolle. This excludes the
resonant branch and every polynomial of degree at most three.

## 5. Every quartic branch is impossible

It remains to consider \(t=p_4\ne0\). Since \(K_5=0\), we have \(p_3=0\).
The next two kernel coefficients are

\[
 K_4=t(3p_2-2At-12),\qquad
 K_3=\tfrac34t(5p_1-4Bt).
\]

They force

\[
 p_2=4+2At/3,\qquad p_1=4Bt/5.                            \tag{12}
\]

After this substitution the \(z^5,z^4,z^2\) coefficients of (4) are,
respectively,

\[
 \begin{split}
 O_5&=2(2A^2t-16A-12Et+21p_0),\\
 O_4&=7ABt-36B-25Ft,\\
 O_2&=(-20AFt-3BEt+60Bp_0-100F-105Jt)/5.
 \end{split}                                             \tag{13}
\]

The two remaining nonconstant kernel coefficients are

\[
 K_2=-t(-2A^2t+24A+27p_0)/9,\qquad
 K_1=t(5ABt-36B+25Ft)/20.                                \tag{14}
\]

In particular
\(K_1+tO_4/20=(3/5)tB(At-6)\). Thus the full ODE and (8) force
\(B=0\) or \(At=6\).

If \(B=0\), (12) gives \(p_1=0\), and (13) gives successively
\(F=0,J=0\), since \(t\ne0\). Again \(h\) is odd, \(f\) even,
and9398 excludes stationarity.

In the exceptional branch \(At=6\), (6) gives \(t=-16/N\).
The equation \(O_5=0\) gives

\[
 E=-N^2/128-7Np_0/64.
\]

Set \(d=D/N^2\). Comparing this with \(E=3N^2/64-D/8\) yields
\(p_0/N=8d/7-1/2\). Equations (8) and (14) then imply

\[
 C=96d/7-8.                                              \tag{15}
\]

Since at least two original coordinates are nonzero,
\(\sum_i u_i^4<N^2\), and therefore \(d<7/8\).
Equation (15) implies \(C<4\), contradicting the universal stationary
bound in Section3. All quartic branches are excluded. Since (8) already
forced \(p_6=0\), this proves **exactly** \(\deg p=5\).

## 6. A single rational chart with a reverse feasibility theorem

For degree-five \(p\), the quotient in (2) has the explicit coefficients

\[
 \begin{split}
 Q={}&7p_5z^4+7p_4z^3+(7p_3-2Ap_5)z^2\\
    &+(8+7p_2-2Ap_4-3Bp_5)z\\
    &+7p_1-2Ap_3-3Bp_4+(2A^2-4E)p_5.                    \tag{16}
 \end{split}
\]

The leading odd equation is

\[
 4K_5=7p_2p_5+7p_3p_4-9Ap_4p_5-5Bp_5^2-56p_5=0.
\]

The theorem makes division by \(p_5\) legal everywhere on this stationary
domain, giving

\[
 \boxed{p_2=8+\tfrac97Ap_4+\tfrac57Bp_5-p_3p_4/p_5.}      \tag{17}
\]

Reflection sends \(f(z)\) to \(f(-z)\), \(h(z)\) to \(-h(-z)\),
\(p(z)\) to \(p(-z)\), and \(Q(z)\) to \(-Q(-z)\).
It preserves \(N,C\), reality, positivity and stationarity, and reverses
\(p_5\). Thus \(p_5>0\) may be imposed after choosing orientation.

Here is a full converse, which retains the original-root feasibility.
Choose \(N>0\), a monic real \(h\) as in (6) with \(A=-3N/8\), a real
polynomial \(p\) of degree five with \(p_5\ne0\), and a scalar \(\gamma\).
Form \(Q\) by (16), and \(K\) by (3),(5). Require **all** of:

1. \(h\) has seven simple real roots \(\lambda_1<\cdots<\lambda_7\).
2. \(p(\lambda_j)>0\) for every \(j\).
3. The complete ODE (4) holds as a polynomial identity.
4. \(K=4(\gamma z^2-N)\) as a polynomial identity.

Define

\[
 f=(Qh-p h')/8.                                         \tag{18}
\]

The leading cancellations in (16) make \(f\) monic of degree eight with
\([z^7]f=0\). Differentiating (18) and using (4) gives \(f'=8h\).
It follows that \([z^6]f=4A/3=-N/2\). At the critical nodes,
\(f(\lambda_j)=-p(\lambda_j)h'(\lambda_j)/8\).
Since \(h'(\lambda_j)\) has alternating signs, the odd-index local minima
are strictly negative and the even-index local maxima strictly positive.
The monic even-degree polynomial tends to positive infinity at both ends.
Its eight monotone intervals therefore each contain a root, and these
roots are simple because no critical value vanishes. Thus (18) reconstructs
**eight distinct real original roots**, balanced and of squared norm \(N\).
Their actual masses are exactly \(p(\lambda_j)\).

For this reconstructed feasible profile, the radial identity from Section3
now gives \(-4\eta=4\gamma D-4N^2\). Since \(D>0\),
\(\gamma=(N^2-\eta)/D\) is its actual angular quotient, rather than a free
algebraic value. The kernel identity then gives all six stationary
derivatives. This proves both directions of the claimed equivalence.

One may scale \(N=1\), orient \(p_5>0\), and use (17) to remove \(p_2\).
The remaining full ODE, lower kernel equations, real-root and positivity
conditions must remain in the chart. Positivity with a real critical
spectrum alone does not make an arbitrary pair \((h,p)\) a primitive pair.
This chart need not stay bounded near collisions; interpolation coefficients
can be ill-conditioned even though the actual masses have the continuity
proved in [9440](../spectral-mass-lipschitz/PROOF.md).

## 7. Exact corroboration and remaining frontier

The [standard-library checker](verify.py) works over Fraction polynomials
in independent indeterminates. It verifies all 49 adjoint basis pairs in
Section2, and 22 further universal coefficient identities used in Sections3--6.
No interpolation grid, numerical root rounding or CAS package is a runtime
premise. The entire coefficient-polynomial records are recomputed and hashed.

A separate dual-number companion-matrix computation of the trace of the
squared mass operator checks all seven coefficient derivatives for five
actual real-original controls, totalling 35 full moving-node derivatives.
These include asymmetric profiles, a profile with a zero original, and a
constant-centered asymmetric profile of degree-five interpolation which is
**not** fully stationary. The Hermite control has constant mass interpolant
8 and \(C=8\), but nonzero kernel residual; centering or low interpolation
degree alone is not stationarity. The full radial Euler identity is also
checked in all five controls.

The scalar/domain controls retain both quadratic negative-value resonances,
the exceptional quartic value and its \(d=7/8\) boundary, and all six
nonzero recurrence pivots in (11). A shifted primitive with seven real
simple criticals has only **two** real originals and a negative mass.
A double-original control has seven simple real criticals but only six
distinct original roots; it is outside the stationary domain. A positive
constant interpolant on an unrelated critical polynomial violates the full
ODE. Eight mathematical damages must be rejected, including frozen nodes,
a missing adjoint boundary term, an altered quotient, a squared resonance,
an incorrect quartic exception and removed feasibility/collision conditions.
The whole external [expected record](expected.json) is compared explicitly,
including missing and extra fields; the checks survive Python optimization.

Run either command from the repository root:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-sendov-2/mass-stationary-chart/verify.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O round-two/six-sendov-2/mass-stationary-chart/verify.py

The universal identities are exact polynomial checks. The finite derivative
controls do not enumerate stationary solutions. The ordinary bridges are
interlacing, the residue adjoint proof, the full coefficient-to-root tangent
chart, the imported heat/even stationary exclusions, and the reverse
feasibility argument. None is claimed formally verified by this program.

The new frontier is the full, feasible **degree-five asymmetric system**.
[9353](../heat-tangent-rank/PROOF.md) supplied complementary heat-tangent
charts; (17) now supplies a coefficient elimination valid without its
small-variance hypothesis. [8753](../angular-three-level-transition/PROOF.md)
provides the global-maximization motivation and a high-valued collision
benchmark, without asserting that every maximizer is all-distinct.
No classification or nonexistence of degree-five stationary solutions,
collision-stratum maximum, global angular value, or complex first-power
endpoint is concluded here. The physical coefficient chambers of the other
Sendov researchers have distinct hypotheses; see [the literature record](LITERATURE.md).
