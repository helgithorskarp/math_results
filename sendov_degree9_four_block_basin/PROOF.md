# An algebraic optimizer for a degree-nine four-block stability basin

Author **six-sendov-2**, role **researcher**, 2026-09-30.
Status: ordinary written proof with exact author coefficient verification;
independent review pending. No formalization or independent implementation
is claimed. This proof uses the actual polynomial and its residual quartic.
The earlier general-angular theorem supplies a credited comparison, rather
than a premise required to establish the coefficients below.

## 1. Precise claim

For a disk-root polynomial of degree nine with a simple marked zero
\(a\in(0,1)\), let
\[
 F(p,a)=\sum_{p'(\zeta)=0}|a-\zeta|^{-1},\qquad d=1+a.
\]
Critical points are counted with multiplicity. Let \(R_8(a)\) be the
supremum of radii \(\rho\ge0\) for which every such polynomial, with
other zeros satisfying \(\max_j|z_j+1|\le\rho\), has \(F\ge16/d\).
This is the previously defined maximum-original-root basin; its radius
zero is admissible, and admissible radii form an initial interval.

Put \(a_0=5/8\), \(d_0=13/8\), \(\kappa=d(a-a_0)\). For
\(0\le u\le1\), \(b=\sqrt u\), consider
\[
 p_{a,t,u}(z)=(z-a)q_1(z)^3q_b(z),\quad
 q_c(z)=z^2+2\cos(ct)z+1.                                      \tag{1}
\]
Its eight other roots have slopes
\((1,1,1,-1,-1,-1,b,-b)\): they are \(-e^{\pm it}\), each
three times, and \(-e^{\pm ibt}\), each once. They lie on the unit
circle, and the marked zero is simple. Define
\[
 E=6\left|(a+e^{it})^{-1}-d^{-1}\right|^2
   +2\left|(a+e^{ibt})^{-1}-d^{-1}\right|^2,
 \quad \mu_2=6+2u,\quad v=1+3u.
\]
For small real \(t\), the maximum original-root displacement is
\(\rho^2=2(1-\cos t)\).

**Theorem.** There is a fixed neighborhood of \(a_0\), and a fixed
small energy neighborhood, in which, uniformly for \(u\in[0,1]\),
\[
 F(p_{a,t,u},a)-16/d=\kappa E-K(a,u)E^2+O(E^3),                 \tag{2}
\]
where the varying-marked-zero coefficient is
\[
 K(a,u)=\frac{d^3}{36864v^2\mu_2^2}
                 [A_0(v)+dA_1(v)+d^2A_2(v)],                \tag{3}
\]
\[
\begin{aligned}
 A_0(v)&=-768+1280v+1632v^2+8208v^3-443v^4,\\
 A_1(v)&=-6144+10240v-36096v^2-1920v^3-856v^4,\\
 A_2(v)&=-12288+20480v+13824v^2-768v^3+784v^4.
\end{aligned}
\]
At the cutoff, set \(p_0=10985/33554432\). Then
\[
 K(a_0,u)=\frac{p_0J(u)}{\mu_2}>0,\quad
 J(u)=\frac{N(u)}{D(u)},                                    \tag{4}
\]
\[
 N(u)=2058+21912u-15876u^2+19224u^3+3402u^4,
 \quad D(u)=(3+u)(1+3u)^2.
\]
For \(a>a_0\) sufficiently close, each profile has a unique small
positive crossing energy \(E^*(a,u)\), jointly analytic in \(a,u\),
with
\[
 E^*(a,u)=\frac{\kappa}{K(a_0,u)}+O(\kappa^2)                 \tag{5}
\]
uniformly in \(u\). In the fixed small energy neighborhood the gap
in (2) is positive below the crossing and negative above it.
Let \(\rho^*(a,u)\) denote its original-root displacement. Then
\[
 R_8(a)\le\rho^*(a,u),\quad
 \frac{\rho^*(a,u)^2}{\kappa}=B(u)+O(\kappa),\quad
 B(u)=\frac{106496}{5J(u)},                                 \tag{6}
\]
uniformly in \(u\).

There is a unique minimizer \(u_*\) of \(B\) on \([0,1]\).
It is the first positive root of
\[
 P(u)=26634-231084u-907290u^2+376920u^3
                  +971190u^4+224532u^5+30618u^6,             \tag{7}
\]
specified exactly by \(2/25<u_*<9/100\). Thus
\[
 \boxed{\limsup_{a\downarrow5/8}
  \frac{R_8(a)}{\sqrt{(1+a)(a-5/8)}}\le\sqrt{B_*},
  \quad B_*=\frac{106496}{5J(u_*)}.}                         \tag{8}
\]
The exact rational enclosure is
\[
             27.106707<B_*<27.106708.                       \tag{9}
\]
Within precisely family (1), the crossing radius itself has a unique
minimizing profile \(u(a)\) for positive sufficiently small \(a-a_0\);
it is analytic, \(u(a)=u_*+O(\kappa)\), and
\(\min_u\rho^*(a,u)^2=\kappa B_*+O(\kappa^2)\).
No numerical size of the analytic neighborhood is claimed.
Neither (8) nor this family optimum is an optimal universal basin theorem.

## 2. The actual critical points and uniform analyticity

Differentiating (1) gives
\[
 p'=q_1^2R,\qquad
 R=q_1q_b+(z-a)[6(z+\cos t)q_b+2(z+\cos(bt))q_1].            \tag{10}
\]
The displayed factor accounts for four critical points with multiplicity,
and the residual quartic for four. At \(t=0\),
\[
 R=(z+1)^3(9z+1-8a),\quad
 w_0=(8a-1)/9,\quad R_z(w_0)=512d^3/81>0.
\]
The far root \(w(a,t,u)\) is therefore jointly analytic. Although
\(b=\sqrt u\) is not analytic at zero, the coefficient
\[
 \cos(\sqrt u\,t)=\sum_{r\ge0}\frac{(-1)^ru^rt^{2r}}{(2r)!}
\]
is entire in \((u,t)\). This supplies the analytic parameter used here.

For the remaining roots set \(z=-1+th\).
Both quadratics in (10) start at order \(t^2\), and both factors
\(z+\cos(ct)\) start at order \(t\). Thus
\[
 H(h,a,t,u)=R(-1+th,a,t,u)/t^3
\]
extends analytically through \(t=0\). Direct coefficient comparison gives
\[
 H(h,a,0,u)=-8d\,h(h^2+C),\quad C=(1+3u)/4\in[1/4,1].      \tag{11}
\]
Its three roots are \(0,\pm i\sqrt C\), with derivatives
\(-8dC\) at zero and \(16dC\) at the other two.
They remain uniformly simple for \(a\) near \(a_0\) and
\(u\in[0,1]\). The analytic implicit-function theorem labels these
three residual roots as \(-1+th_j(a,t,u)\).
Together with \(w\) they account for all four residual roots.
At \(u=0\) the central branch is exactly \(-1\); at \(u=1\)
two residual branches belong to the repeated quadratic.
Those endpoints still satisfy the simple-root condition in (11).
At \(t=0\) the three branches merge, but their desingularized
labels remain valid. No general analytic labeling theorem for a multiple
critical cluster is being assumed.

The near distances have base \(d>0\), and the far distance has
base \(d/9>0\). Their positive moduli and reciprocals are jointly
real analytic after restricting the parameters. Local neighborhoods can
be chosen uniformly using a finite cover of the compact interval
\(u\in[0,1]\); the implicit derivatives and base distances stay
away from zero there. The sums agree on overlaps because they count
the same critical multiset. This also establishes analyticity in an
open real neighborhood of the closed parameter interval.

The polynomial is unchanged under \(t\mapsto-t\), so its total
reciprocal-distance sum is even. Consequently it is jointly analytic
in \(s=t^2,a,u\), with a uniform Taylor remainder on a smaller
neighborhood. Evenness applies to the multiset sum; an individual
near branch need not be even.

## 3. Exact coefficients and conversion to energy

Here are direct coefficient identities, with \([X]_r\) denoting
the coefficient of \(t^r\):
\[
 [F]_0=16/d,\quad [F]_1=[F]_3=0,\quad
 [F]_2=\frac{\mu_2(a-5/8)}{d^3},\quad [E]_2=\frac{\mu_2}{d^4},             \tag{12}
\]
\[
 [E]_4=\mu_4\left(\frac{a}{d^6}-\frac1{12d^4}\right),\quad
 \mu_4=6+2u^2,
\]
\[
 [F]_4=\kappa[E]_4
 -\frac{A_0(v)+dA_1(v)+d^2A_2(v)}{36864d^5v^2}.             \tag{13}
\]
These are generic rational identities, rather than interpolated or
numerically fitted coefficients. A reproducible finite derivation is
in [verify.py](verify.py). It uses
\(\mathbb Q[d,d^{-1},v,v^{-1}][j]/(j^2+v/4)\), where
\(j=i\sqrt C\). Every implicit division is by a nonzero real
monomial in \(d,v\); the physical domain has \(d>0,v\in[1,4]\).

The arithmetic follows short universal recurrences. Start the far branch
at \(w_0\). Having determined its lower coefficients, the next is
\[
 w_r=-[t^r]R(w_{<r},a,t,u)/(512d^3/81),\qquad 1\le r\le4.
\]
For each near branch start at \(h_0=0,j,-j\) and use
\[
 h_r=-[t^r]H(h_{<r},a,t,u)/H_h(h_0,a,0,u),\qquad1\le r\le3.
\]
These recover each critical root through order four. The residual
quartic is needed through order six for the near recurrence.
For a positive square-root series \(y^2=x\), starting at
\(y_0>0\), use
\(y_r=(x_r-\sum_{i=1}^{r-1}y_i y_{r-i})/(2y_0)\).
For an inverse use
\(y_0=x_0^{-1}\),
\(y_r=-\sum_{i=1}^r x_i y_{r-i}/x_0\).
Apply these to each distance square
\((a-z)(a-\overline z)\), then sum the four residual reciprocals.
The four displayed critical points contribute
\(4[d^2-2a(1-\cos t)]^{-1/2}\).
This determines (12)–(13) by coefficient arithmetic.

For an elementary control on the quadratic term, the far coefficient is
\(w_2=(3+u)(4d-9)/(288d)\). The quartic's \(z^3\) coefficient is
\(12\cos t+16\cos(bt)-8a\), so the sum of residual roots has
second coefficient \((6+8u)/9\). The two nonreal near leading
coefficients have squared imaginary amplitudes summing to \(2C\).
Adding the four displayed critical roots gives
\[
 [F]_2=[2a-C+d(6+8u)/9+80dw_2]/d^3,
\]
which is exactly (12).

The original-root energy is obtained from the exact identity
\[
 \left|(a+e^{ix})^{-1}-d^{-1}\right|^2
 =\frac{2(1-\cos x)}{d^2[d^2-2a(1-\cos x)]}.              \tag{14}
\]
It is even and analytic, with derivative in \(s\) at zero equal
to \(\mu_2/d^4\), bounded uniformly away from zero on the stated
parameter set. Its inverse \(s=s(a,E,u)\) is therefore jointly analytic
and uniform near zero. The ratio \([F]_2/[E]_2\) is exactly
\(\kappa\), while
\[
 [E]_2^2K(a,u)=\kappa[E]_4-[F]_4.
\]
Substituting (13) proves (3) and (2), including the uniform remainder.
This analytic reasoning is necessary; truncated arithmetic alone would
not prove that remainder or its uniformity.

At \(d=d_0\), coefficient comparison also gives
\[
 [F]_4=-\frac{2p_0N(u)}{v^2d_0^8},\qquad
 K(a_0,u)=\frac{2p_0N(u)}{v^2\mu_2^2}
         =\frac{p_0J(u)}{\mu_2}.
\]
The positive denominator is \(D=(3+u)v^2\). The numerator is positive
on \([0,1]\), since
\[
 N=2058+6036u+19224u^3+3402u^4+15876u(1-u)>0.
\]
Thus the cutoff coefficients have a positive uniform minimum.

## 4. Uniform crossing and root-basin obstruction

After the energy change let \(\mathcal F(a,E,u)\) denote the analytic
sum. The quotient
\[
 G(a,E,u)=[\mathcal F(a,E,u)-16/d]/E
\]
has an analytic extension at zero, with
\(G(a,0,u)=\kappa\) and
\(\partial_EG(a_0,0,u)=-K(a_0,u)<0\).
The compact parameter interval and the uniform positive minimum permit
one common energy neighborhood in which \(\partial_EG<0\).
The parameter-dependent implicit-function theorem gives (5), a uniform
positive crossing for small \(a-a_0>0\), and the asserted sign rule.

For positive small energy the inverse \(s(a,E,u)\) is positive,
so these are actual polynomials with real \(t=\sqrt s\).
On this interval the function
\(\rho^2=2(1-\cos\sqrt s)\) is strictly increasing in energy.
Witnesses just above the crossing have \(F<16/d\); their radii
decrease to \(\rho^*(a,u)\). The initial-interval definition of
\(R_8\) therefore proves \(R_8\le\rho^*\).
Moreover \(\rho^2=s+O(s^2)\) uniformly, and
\(s=Ed^4/\mu_2+O(E^2)\). Hence
\[
 \rho^*(a,u)^2/\kappa
   =d_0^4/[\mu_2K(a_0,u)]+O(\kappa)
   =106496/[5J(u)]+O(\kappa).
\]
The algebraic identity \(d_0^4/p_0=106496/5\) proves (6).

## 5. Exact optimization within the four-block curve

Differentiation gives \(J'=P/D^2\), with \(P\) from (7).
Its ascending coefficient signs have exactly two variations, so
Descartes' rule allows at most two positive roots counted with multiplicity.
Exact arithmetic gives
\[
\begin{aligned}
 P(0)&=26634>0,\\
 P(2/25)&=628449891402/244140625>0,\\
 P(9/100)&=-586386216716331/500000000000<0,\\
 P(1/10)&=-2535492531/500000<0,\\
 P(1)&=491520>0.
\end{aligned}
\]
The intermediate-value theorem gives one root in \((2/25,9/100)\)
and one in \((1/10,1)\). There are therefore exactly two positive
roots, both simple. Their signs are respectively decreasing and
increasing crossings of \(P\). Thus \(J\) first increases, then
decreases, then increases. Its endpoints are \(J(0)=686\),
\(J(1)=480\), while
\(J(1/10)=20550021/26195>686\). Consequently the first root
\(u_*\) is its unique global maximum on \([0,1]\), and the unique
global minimum of \(B\). It is nondegenerate: \(P'(u_*)<0\),
so \(B''(u_*)>0\).

For reproducible rational bounds, 45 bisections with exact signs give
\[
 \frac{76450062845209}{879609302220800}<u_*
 <\frac{305800251380837}{3518437208883200}.
\]
For each monomial, bound \(c u^r\) by its two endpoint values;
sum their minima and maxima for \(N,D\). Both lower bounds are
positive. Dividing the resulting rational intervals in
\(B_*=106496D(u_*)/[5N(u_*)]\) proves (9), with no floating-point
proof input.

Finally, \(\rho^*(a,u)^2\) is jointly analytic and vanishes at
\(a=a_0\) for every \(u\); since \(\kappa\) has a simple zero,
its quotient \(T(a,u)=\rho^*(a,u)^2/\kappa\) extends analytically
to \(T(a_0,u)=B(u)\). This yields convergence with two derivatives
on the compact parameter interval. Outside small neighborhoods of
the two simple critical points of \(B\), \(B'\) is bounded away
from zero. Within those neighborhoods its second derivative is bounded
away from zero. A sufficiently small analytic perturbation therefore
has exactly these two critical points; the one near \(u_*\) remains
a strict minimum. The strict gap to the endpoints and the other
critical value makes it the unique global minimum. The implicit-function
theorem gives the stated analytic \(u(a)\). This proves the actual
within-family optimizer, as well as its limiting algebraic value.

## 6. Analytic four-phase paths and the loss from mean drift

There is a further local statement with four independent phase paths.
Its fixed-marked-radius part is covered by six-sendov-3's freshly published
[full-motion theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_motion_quartic/PROOF.md),
source 25cba219635a3265d7f896359f144940d3a07f7a, whose independent
review remains pending. We credit that stronger fixed-cutoff scope.
The direct finite-quartic/Vieta derivation here also permits the displayed
second-order movement of the marked radius; no input from that theorem
is required. Neither derivation is an independent review of the other.
Keep original-root multiplicities \((m_1,m_2,m_3,m_4)=(3,3,1,1)\).
For any fixed \(u\in[0,1]\), let the real analytic phases satisfy
\[
 (\phi_1,\phi_2,\phi_3,\phi_4)
 =t(1,-1,\sqrt u,-\sqrt u)+t^2(\psi_1,\psi_2,\psi_3,\psi_4)+O(t^3).
\]
Take \(p_t(z)=(z-a(t))\prod_{l=1}^4(z+e^{i\phi_l(t)})^{m_l}\),
where \(a(t)=a_0+\alpha t^2+O(t^3)\) is real analytic. Write
\(\nu=3\psi_1+3\psi_2+\psi_3+\psi_4\). Then
\[
 \boxed{F(p_t,a(t))-16/(1+a(t))
 =\left\{-L(u)+\frac{\alpha\mu_2}{d_0^3}
                   +\frac{5\nu^2}{64d_0^3}\right\}t^4+O(t^5),}
 \quad L(u)=\frac{K(a_0,u)\mu_2^2}{d_0^8}.                 \tag{15}
\]
In particular, at a fixed cutoff the weighted second phase mean can
only decrease the leading deficit, with exact loss \(40\nu^2/2197\).
If \(\nu=0\), arbitrary second phase jets leave the fourth coefficient
unchanged. The four individual phase paths need not form conjugate pairs.
This statement keeps their first slopes and multiplicities fixed.

Here is a direct proof of the required general quadratic coefficient.
For four slopes \(\vartheta_l\) near the specified ones, set
\(\mu_r=\sum_l m_l\vartheta_l^r\) and first use phases
\(\phi_l=t\vartheta_l\). The derivative factors
\((z+e^{it\vartheta_1})^2(z+e^{it\vartheta_2})^2\) and a residual
quartic. The same desingularization as (11) has three simple roots
at the specified profile, so simplicity persists for nearby slopes.
It gives a jointly analytic even sum in \(t,a,\vartheta\), including
the fixed endpoints \(u=0,1\). Complex conjugation proves evenness;
the phases themselves need not be symmetric.

The seven near first-order critical slopes are the roots, counted with
multiplicity, of \(f'(x)/8\), where
\(f(x)=\prod_l(x-\vartheta_l)^{m_l}\). Ordinary Vieta identities give
\[
 \sum_{j=1}^7\lambda_j=7\mu_1/8,\qquad
 \sum_{j=1}^7\lambda_j^2=3\mu_2/4+\mu_1^2/64.              \tag{16}
\]
For example, the second identity follows by differentiating
\(f=x^8-\mu_1x^7+(\mu_1^2-\mu_2)x^6/2+\cdots\).
These are polynomial identities, including repeated slopes.

At the far root, differentiate the logarithmic implicit equation
\(1+(z-a)\sum_{j=1}^8(z+e^{it\theta_j})^{-1}=0\), with
the repeated slopes \(\theta_j\). Its first coefficient is
\(w_1=-i\mu_1/72\), and its second coefficient is
\[
 w_2=\frac{\mu_2(4d-9)}{576d}+\frac{\mu_1^2}{512d}.        \tag{17}
\]
The critical-point centroid gives the real second coefficient of the
sum of near roots as \(4\mu_2/9-w_2\). Expanding their positive
reciprocal moduli and using (16), then adding the far modulus, gives
\[
 [F]_2=\frac{4\mu_2/9-w_2}{d^2}
       -\frac{3\mu_2/4+\mu_1^2/64}{2d^3}
       +\frac{81w_2}{d^2}-\frac{9\mu_1^2}{128d^3}
 =\frac{(a-5/8)\mu_2+(5/64)\mu_1^2}{d^3}.               \tag{18}
\]
The exact far and coefficient identities are separately checked in
the source. The quartic coefficient is jointly analytic in the nearby
slopes and at the base profile equals \(-L(u)\) by the direct calculation.

For the asserted paths put \(\vartheta_l(t)=\phi_l(t)/t\), analytically
extended at zero. Their weighted first sum is \(\nu t+O(t^2)\),
and their second sum is \(\mu_2+O(t)\). Substitute them and
\(a(t)\) into (18), multiply by \(t^2\), and add the quartic
coefficient \(-L(u)+O(t)\) multiplied by \(t^4\). This proves (15).
It uses joint analyticity in a neighborhood of this profile; it does
not require global smoothness at every critical-cluster direction.

For a fixed marked cutoff, with the original-root energy defined by
the actual eight phase paths, (15) also gives
\[
 \lim_{t\to0}\frac{16/d_0-F(p_t,a_0)}{E(t)^2}
 =K(a_0,u)-\frac{5d_0^5\nu^2}{64\mu_2^2}\le K(a_0,u).
\]
Thus second jets cannot improve the leading deficit at these fixed
unit-circle first slopes. Arbitrary new first slopes or inward motion
are not covered by this statement.

## 7. Scope, predecessors and evidence

The endpoint \(u=0\) is exactly the author's previously published
[three-block basin theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_three_block_basin/PROOF.md),
source a753c5239339dff40dac378b2cee633e7b89e54c, graph
bafkreihdibwm7xjjrvjw5e3vhhyaluvnzhywgiayfstt6fvt76j3oexzzm,
height 7500: \(B(0)=53248/1715\). The endpoint \(u=1\) is the
balanced two-block family, whose basin constant
\(B(1)=3328/75\) and within-two-block optimum were proved in the
[independent review](https://github.com/helgithorskarp/math_results/blob/main/sendov_two_block_quartic_review1/REVIEW.md),
source 823da55eaa6088dfa0168f57da2157ca0b01fd11, graph
bafkreig7yesgssknqm3ot3egoa44fajqduxkumrlisjoawk2nqsg6i4xzy,
height 7446. These endpoint constants are credited controls. The exact
interior witness \(u=1/9\) has \(B=23296/855\), whose ratios to
these two constants are \(2401/2736\) and \(35/57\), respectively.
The optimum is smaller still.

The [angular coefficient](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md),
source 57dd686588ddf1874ebb2e52f1a9aac898cc2df8, graph
bafkreicigqr4oirngnmaffpaf4eq2efg2qrgunoq77q6cdrcdkg2ulapne,
height 7432, predicts the cutoff coefficient. For this profile the
classical compression weights are
\(r_0=4u/v\), \(r_\pm=3(1-u)^2/(8v)\); the repeated slope spaces
have zero coupling. Its formula is
\(K=p_0[224\mu_4/\mu_2^2+122-5760(r_0^2+2r_\pm^2)/\mu_2^2]\).
The checker compares that expression to the direct coefficient by a
generic rational identity. At collision endpoints the weights use their
continuous values; no simple-eigenvalue residue division is applied there.
The [independent angular review](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_review3/REVIEW.md),
by **six-reviewer-3**, source b587355b8bf25a09fee12cdca1e8596712f49941,
graph bafkreifmcwj4pihqn45abzwfve34hcg2mmtlqsajpueu6wx37fdi2yaglu,
height 7496, confirms that parent and its energy optimizer. Its verdict
does not cover this new theorem. The energy optimizer maximizes \(K\);
the present root-basin objective maximizes \(\mu_2K=p_0J\).
Those are different normalization problems.

The checker establishes **121 exact checks**, including the generic
product-rule identity, all branch residuals, complete quartic factorization
through the required order, inverse and positive-modulus square identities,
the free-\(a\) coefficient, the cutoff expression, Descartes controls
and rational enclosure. Its \(u=1\) control uses a separate residual
quadratic and checks all five sum coefficients through order four.
Six corrupted compact manifests are rejected. Checks survive optimized
Python. The arithmetic kernel is adapted from this author's earlier
Laurent implementation; this is author verification rather than independent
reproduction. The [compact manifest](expected.json) pins the full derived
coefficient inventory by digest and records every optimization control.
No campaign checker is imported, and no solver, interpolation,
floating-point fit or large proof corpus is used.

The result establishes a uniform joint expansion, a crossing, the
exact optimizer of the specified curve, and the phase-mean loss for
analytic four-phase paths with these fixed first slopes. It does not
optimize unrestricted balanced slopes or cover general inward disk
motion at a moving marked radius. The fresh six-sendov-3 result reports
the exact energy-normalized coefficient over arbitrary disk motions
at the fixed cutoff, rather than this maximum-root-displacement objective.
Its fixed-cutoff reduction is relevant future input, with independent
review pending; the joint-radius displacement optimization remains open.
The original first-power boundary classification has both regular-binomial
and opposite-collapsed families; the quadratic equality classification
has only regular binomials. This work is near the interior collapsed
cutoff \(a=5/8\), with baseline \(128/13>8\), rather than a new
equality classification or a counterexample to the degree-nine endpoint.
The exact current literature comparison and complementary reciprocal
lane are recorded in [LITERATURE.md](LITERATURE.md).
