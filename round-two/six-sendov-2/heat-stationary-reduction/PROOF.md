# Quadratic heat restrictions on all-distinct angular stationary profiles

Actual author **six-sendov-2**, role **researcher**, 2026-10-02.
Complete ordinary author proof with exact finite certificates; unformalized
and independently unreviewed. This is a real degree-eight angular reduction
for the degree-nine first-power research lane. It does not determine the
global angular maximum or prove the complex Tang--Zhang endpoint.

The [constant-term reduction](../constant-term-angular-reduction/PROOF.md),
graph9271, gives six coefficient stationarity equations at distinct original
roots. We use three particular linear combinations, obtained from quadratic
heat variations, to force a high stationary candidate into one explicit
four-negative/four-positive chamber with a dominant central spectral mass.
The [three-level optimum](../angular-three-level-transition/PROOF.md),
graph8753, remains credited. Polynomial heat flow and simple-root dynamics
are classical; see [Tao's 2017 exposition](https://terrytao.wordpress.com/2017/10/17/heat-flow-and-zeroes-of-polynomials/).
The functional identities and quantitative stationary restriction below
are the mathematical addition.

## 1. Statement and domain

Let u1<...<u8 be distinct real numbers with sum ui=0, and put

\[
 f(z)=\prod_{i=1}^8(z-u_i),\qquad h=f'/8,\qquad
 N=\sum_i u_i^2,\quad S_3=\sum_i u_i^3,\quad
 D=\sum_i u_i^4-N^2/8>0.
\]

Write lambda1<...<lambda7 for the critical points; strictly
ui<lambdai<u(i+1). Define

\[
 m_j=-8f(\lambda_j)/h'(\lambda_j)
     =\frac{64}{\sum_i(u_i-\lambda_j)^{-2}}>0,\qquad
 \eta=\sum_jm_j^2,\quad C=(N^2-\eta)/D.                    \tag{1}
\]

Stationarity always means first-order stationarity of C on the balanced
fixed-N original-root manifold. At these distinct roots it is equivalent
to vanishing of all monic coefficient directions of degree<=5.
It is weaker than being a local or global maximum.

**Theorem.** At every such stationary profile, let
M=max_j mj and q=M/N. Then

\[
 4<C<32,\qquad
 \boxed{(768+208C)q^2-(768+48C)q-9C^2+128C>0.}             \tag{2}
\]

In particular, if C>=T=24531/1000, then

\[
 q>81/100,\qquad
 \boxed{\frac D{N^2}<\frac{20273}{1471860}<\frac{69}{5000}.} \tag{3}
\]

For theta= u/sqrt(N), exactly four components are negative and four
positive, and

\[
 \frac3{200}<\theta_i^2<\frac{47}{200},\qquad
 \frac3{25}<|\theta_i|<\frac12.                            \tag{4}
\]

The unique dominant mass is at lambda4 in the central original-root gap:

\[
 m_4>\frac{81}{100}N,\qquad
 |\lambda_4|<\frac2{15}\sqrt N,\qquad
 |u_i-\lambda_4|>\frac9{80}\sqrt N\quad\hbox{for every i}.  \tag{5}
\]

Let O3 be the signed/permuted normalized orbit of the credited
three-level optimizer

\[
 u_\alpha=(\alpha,\alpha,\alpha,\alpha,1,1,1,-4\alpha-3),
\]

where alpha is the unique root in
[-853410556973738/10^15,-853410556973736/10^15] of

\[
 4575t^4+11695t^3+11175t^2+4737t+746=0.
\]

Every stationary profile in (3) also satisfies

\[
                    \operatorname{dist}(\theta,O_3)>1/11000. \tag{6}
\]

This excludes high-valued **all-distinct stationary** profiles from a
neighborhood; it is not an all-profile coercivity estimate there.
The [full-sphere local estimate](../full-sphere-effective-neighborhood/PROOF.md),
graph9211, retains its coefficient300 and closed radius1/250000.

**Conditional global reduction.** Graph8753 proves C extends continuously
to the balanced unit sphere at the equal-magnitude 4+4 orbit, with value16,
and has a finite attained maximum C*>=c3>24.53389668. Thus any all-distinct
global maximizer obeys (2)--(6), as well as the six equations and feasible
centering from9271. A maximizer with repeated original roots remains a
separate possibility. No assertion C*=c3 or complete collision classification
is made.

## 2. Spectral identities and curvature weights

For completeness, let P project onto 1-perp in R8 and
H=P diag(u) P restricted to that seven-dimensional space. At a critical
point lambda, the vector ri=(ui-lambda)^(-1) has sum0 and
H r=lambda r. The critical equation implies
sum_i ui/(ui-lambda)=8. Therefore the squared projection mass of the
balanced vector u onto this eigendirection is exactly64/sum_i ri^2,
which proves (1). The seven distinct eigenvectors are a complete
orthogonal basis. Consequently

\[
 \sum_j m_j=N,\qquad \sum_jm_j\lambda_j=S_3,\qquad
 \sum_jm_j\lambda_j^2=\|Hu\|^2=D.                          \tag{7}
\]

This is the compression framework of
[graph7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and its [independent audit7496](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/PROOF.md).
In the last identity Hu has components ui^2-N/8.
Newton's identities also give sum_j lambda_j=0 and
sum_j lambda_j^2=3N/4.

Define, at each critical point,

\[
 A_j=h''(\lambda_j)/h'(\lambda_j),\qquad
 B_j=A_j^2-h'''(\lambda_j)/h'(\lambda_j).
\]

If s1=sum_(k!=j)(lambdaj-lambdak)^(-1) and
s2=sum_(k!=j)(lambdaj-lambdak)^(-2), differentiating the product for h
gives

\[
 A_j=2s_1,\quad B_j=s_1^2+3s_2>0,\quad
 \boxed{A_j^2/B_j<8/3}.                                  \tag{8}
\]

Indeed s1^2<=6s2, strictly here because the six reciprocals are distinct.
The curvature inequality is valid on any simple seven-node real spectrum.
The **stationary implications** require distinct original roots as well.

## 3. Three feasible infinitesimal heat directions

For w(z)=az^2+bz+c set

\[
 Q_w=w f''-56af-7bf',\qquad R=zf'-8f.                     \tag{9}
\]

The degree8 and degree7 terms cancel in Qw; it is balanced and has degree<=6.
For f+tQw, elementary Newton coefficient differentiation gives

\[
 \dot N=-26aN-112c,\qquad
 \dot D=-44aD-3aN^2-20bS_3-24cN.                         \tag{10}
\]

For example f6=-N/2, f5=-S3/3,
D=3N^2/8-4f4, and [z6]Qw=13aN+56c.
The radial variation R has root velocities -ui, and hence
dot N=-2N, dot D=-4D, dot eta=-4eta and dot C=0.
Thus

\[
 \widehat Q_w=Q_w-(13a+56c/N)R                            \tag{11}
\]

has degree<=5 and fixes N. Every small positive or negative coefficient
step in such a direction has eight simple real roots by the local
implicit-function theorem, because the starting original roots are simple.
No global preservation theorem for heat flow is used.
At a stationary point dot C(Qw)=dot C(Qhatw)=0.

Implicit differentiation of f_t'(lambdaj(t))=0 yields

\[
 \dot\lambda_j=-[w'(\lambda_j)-7b+w(\lambda_j)A_j].
\]

Differentiate the residue -8 f_t(lambdaj(t))/h_t'(lambdaj(t)).
Using f'=0 at the critical point gives

\[
 \boxed{\dot m_j=-64w(\lambda_j)
       +m_j[w(\lambda_j)B_j-w'(\lambda_j)A_j-2a].}         \tag{12}
\]

This includes motion of the critical nodes. Freezing them for
nonconstant directions gives a different and generally wrong derivative.
Summing (12), using (7), (10) and sum lambda_j^2=3N/4, and comparing
the coefficients a,b,c proves the three universal identities

\[
 \sum m_jB_j=336,\quad
 \sum m_j(\lambda_jB_j-A_j)=0,\quad
 \sum m_j(\lambda_j^2B_j-2\lambda_jA_j-2)=22N.             \tag{13}
\]

Define the three squared-mass traces

\[
 M_0=\sum m_j^2B_j,\quad
 M_1=\sum m_j^2(\lambda_jB_j-A_j),\quad
 M_2=\sum m_j^2(\lambda_j^2B_j-2\lambda_jA_j-2).
\]

From (7), (12),
dot eta=-128(aD+bS3+cN)+2(aM2+bM1+cM0).
Differentiating C with (10) then yields

\[
\begin{split}
D\dot C={}&a[(128+44C)D+(3C-52)N^2-2M_2]\\
 &+b[(128+20C)S_3-2M_1]+c[24N(C-4)-2M_0].
\end{split}                                               \tag{14}
\]

At a stationary point all three coefficients vanish:

\[
 \boxed{M_0=12N(C-4),\quad M_1=(64+10C)S_3,\quad
 M_2=(64+22C)D+(3C/2-26)N^2.}                            \tag{15}
\]

Only three combinations of the six stationarity equations are used;
conditions(15) alone are not asserted sufficient for stationarity.
Since B>0 and m>0, M0>0. By(13),
M0<=M sum mB=336M<336N. This proves4<C<32.

## 4. The mass polynomial inequality

Complete the square in M2 using gamma_j=lambda_j-A_j/B_j:

\[
 M_2=\sum m_j^2B_j\gamma_j^2
        -\sum m_j^2(A_j^2/B_j+2).
\]

By(13), sum m_j B_j gamma_j^2=24N+sum m_j A_j^2/B_j.
Use m_j<=M and (8) on the nonnegative factors m_j(M-m_j):

\[
\begin{split}
 M_2&\le24MN+\sum m_j(M-m_j)A_j^2/B_j-2\eta\\
    &\le\frac{80}{3}MN-\frac{14}{3}\eta.                 \tag{16}
\end{split}
\]

Write d=D/N^2. Substitute(15) and eta/N^2=1-Cd into(16):

\[
 (64+52C/3)d+3C/2-64/3\le80q/3.                         \tag{17}
\]

All seven masses are positive, so the squares of the other six masses
have sum strictly smaller than their squared total. Thus

\[
 \eta<M^2+(N-M)^2,\qquad d>2q(1-q)/C.                    \tag{18}
\]

Inserting this strict inequality into(17), whose d coefficient is
positive, and multiplying by6C gives exactly(2).

Let P_C(q) denote its left side. For 0<=q<=1,

\[
 \partial_C P_C(q)=208q^2-48q+128-18C\le288-18C.
\]

For C>=T this is negative. At T the exact values P_T(0) and
P_T(81/100) are both negative; the latter is
-1029981/5000000. Convexity in q therefore makes P_T negative throughout
[0,81/100]. Hence(2) forces q>81/100.
The other six squared masses also have sum at least(N-M)^2/6, so

\[
 d\le\frac{1-q^2-(1-q)^2/6}{C}
   <\frac{1-(81/100)^2-(19/100)^2/6}{T}
   =\frac{20273}{1471860},
\]

because the numerator is strictly decreasing for q>1/7. This proves(3).
All displayed rational comparisons are independently recomputed by
the checker, without a rounded numerical root for P.

## 5. Sign chamber and central critical point

For normalized theta put delta_i=theta_i^2-1/8. Then
sum delta_i=0 and sum delta_i^2=d. Cauchy on the other seven terms yields
delta_i^2<=(7/8)d. Because
(7/8)(69/5000)<(11/100)^2, (3) gives(4), with strict bounds.

Let r=1/sqrt8, let s_i be the sign of theta_i, and put v=theta-rs.
The squared-magnitude bounds imply
r|theta_i|>17/400, since(1/8)(3/200)>(17/400)^2. Therefore

\[
 (|\theta_i|+r)^2>3/200+1/8+34/400=9/40,\quad
 \|v\|^2=\sum_i\frac{(\theta_i^2-1/8)^2}{(|\theta_i|+r)^2}
       <23/375<1/16.                                    \tag{19}
\]

If the signs were unbalanced, |sum s_i|>=2. Projecting rs onto1-perp
and using ||theta||=1 gives theta dot(rs)<=sqrt15/4, and hence
||v||^2>=2-sqrt15/2>1/16. The last inequality follows from
15<(31/8)^2. This contradicts(19), so there are exactly four of each sign.

For the dominant mass at lambda, (7) gives M lambda^2<=D, so
lambda^2<(69/5000)/(81/100) N<4N/225.
Each pole distance in(1) is strictly greater than sqrt(M)/8>
9sqrt(N)/80, because its reciprocal square is strictly smaller than
the sum of all eight positive reciprocal squares.

If lambda were in a noncentral gap, both bounding original roots would
have the same sign. The one closer to zero has magnitude>
3sqrt(N)/25. Because |lambda|<2sqrt(N)/15, its distance to that root
would be less than sqrt(N)/75, contradicting the preceding lower bound.
Thus the dominant mass is at lambda4. It is unique since M>0.81N.
This proves(5).

## 6. Separation from the three-level optimizer

The normalized quartic variance is invariant under sign and permutation.
For the credited algebraic optimizer it is

\[
 d_0=\frac{4\alpha^4+3+(-4\alpha-3)^4}
              {(20\alpha^2+24\alpha+12)^2}-\frac18
       >\frac{707}{50000}.                              \tag{20}
\]

The root interval stated in Section1, certified by a sign change and
Sturm count, gives this strict lower bound by rational interval evaluation.
The full enclosure is in expected.json, approximately
(0.014144512016381738,0.014144512016384530).

On the unit ball the norm of the gradient of sum theta_i^4 is
4sqrt(sum theta_i^6)<=4. The segment between two unit vectors stays in
that ball, so their quartic variances differ by at most four times
their Euclidean distance. For every point psi in O3, (3), (20) give

\[
 4\|\theta-\psi\|\ge d_0-d
       >\frac{707}{50000}-\frac{20273}{1471860}
       >\frac4{11000}.
\]

This proves(6). It is a necessary exclusion of high stationary points;
the sharper local coercive inequality9211 is neither changed nor enlarged.

## 7. Concrete candidate elimination and finite trust boundary

Centering the feasible symmetric primitive from9271 gives

\[
 f_{\rm cen}(z)=(z^2-1)(z^2-9)(z^2-25)(z^2-49)
                         -1294848/280993.
\]

It has eight simple real roots, N=168, and
C=2522064/280993. Its constant-direction derivative is exactly0.
Take the fixed-N tangent

\[
 Q=f_{\rm cen}''-\tfrac13(zf_{\rm cen}'-8f_{\rm cen}).
\]

The exact heat derivative is positive, approximately1.42709481644.
The literal polynomial fcen+Q/1000 still has eight simple real roots
and N=168, with C approximately8.97696759410 instead of8.97554031595.
The exact rational improvement, entire polynomials and independent
Sturm counts are in the fixture. This completes the next candidate
elimination test proposed after9271; it is not evidence that every
feasible centered profile is eliminated.

The integer profile
(-856,-854,-852,-850,412,998,1000,1002) has C>T and maximum mass<0.81N,
but has a nonzero heat gradient. It is a finite negative control against
dropping stationarity, not a counterexample to the theorem.
The double-original profile(-3,-3,-2,-1,1,2,3,3) has seven simple
critical roots, while its positive1/1000 fixed-N heat step loses
real original roots. It demonstrates why simple h alone does not
authorize the two-sided stationary implications at original collisions.

The standalone standard-library checker compares exact trace calculations
in Q[z]/h with independent dual arithmetic in the moving quotient algebra
Q[epsilon]/epsilon^2. All four choices w=1,z,z^2,2z^2-3z+5 are checked
both raw and after fixed-N radial subtraction on five profiles:40
complete derivative comparisons. On three rational distinct-root inputs
it separately isolates all21 critical nodes, derives masses from original
poles, derives A,B from six critical reciprocals, and compares these with
quotient polynomials. It checks(8), (13), (16), every rational constant,
the improving step and the original-double domain failure. Six damaged
mathematical controls must fail. Normal and -O runs compare the entire
fixture, including every rational/interval field.

These finite checks validate identities and explicit certificates, not an
exhaustive enumeration of stationary points. Universal interlacing,
positivity, stationarity, Cauchy, sign and Lipschitz implications are the
ordinary proof above. No proof assistant, external solver, tolerance,
random search, large corpus or inherited review verdict is used.
