# Independent nonzero-skew construction and maximal-budget proof

Actual **six-reviewer-5**, role **independent mathematical reviewer**, 2026-10-04.
This is ordinary, unformalized mathematics. The complete written target was
exposed; its native programs and fixtures were never opened or imported.

## 1. Domain and the exact inherited inputs

Let \(\eta>0\), \(a=1-\eta>0\). Let \(p\) be monic complex degree nine,
with every original zero in the closed unit disk and \(p(a)=0\). All eight
critical points are counted with multiplicity. Define
\[
 F=\sum_{l=1}^8|a-\zeta_l|^{-1},\qquad
 T_\eta=(F-8-C\eta-B_*\eta^2)/\eta^3,\qquad
 \lambda_\eta=\eta^{-2}\sum_l(\Im\zeta_l)^3.
\]
Zero reciprocal denominators contribute infinity. This is the first power.
Rotation and nonzero scalar multiplication recover the equivalent marked
modulus statement. No conjugacy or smooth critical labels are assumed.

Use the credited constants
\[
\begin{gathered}
c=\cos(\pi/9),\ s=\sin(\pi/9)>0,\quad y=1/[3(1+c)],\quad x=2/3-y,\quad H=14y,\\
k=-7(1+2c)/18,\quad\rho=(c-5)/3,\quad d=3k+\rho,\\
u_z=-37/36+20c/9-20c^2/9,\quad u_p=u_z-\rho H/2,\\
\alpha=-527/360+41c/90+13c^2/90<0,\quad
\kappa=(k+\rho)^2/2+10\alpha/27>0,\\
W_*=2512/27+5840c/9-21392c^2/27,\quad w_2=W_*/8,\\
D_*=-4270/27-29492c/27+4012c^2/3,\quad
\Gamma=13/36+1253c/72-50c^2/3,\\
C=8/3+y,\quad B_*=2311/108+4934c/27-1976c^2/9,\\
T_*=-60800959/17496-307083769c/17496+10980067c^2/486\in(-19,-18).
\end{gathered}
\]
Set \(\omega_j=e^{2\pi ij/9}\), \(0\le j\le8\), and
\[
 L_j=-\omega_j/3-x-y/\omega_j,\qquad
 W_j=\frac{i}{18}[(3+4c)\omega_j-(1+2c)(1+\omega_j^{-1})-\omega_j^{-2}].
\]
The fixed second drift \(d_j\) is defined in Section 3 below.

We adopt only the following all-actual fixed-cap statements of
[10152](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/third-boundary-optimum/PROOF.md)
and
[10113](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/quadratic-root-motion/PROOF.md).
For every fixed finite cap \(T_\eta\le T\), they give a common collar,
nine simple original branches uniquely labelled near the \(\omega_j\), and
\[
 \lambda_\eta=O_T(1),\quad
 Z_j=\omega_j+\eta L_j+\eta^2(d_j+\lambda_\eta W_j)+O_T(\eta^{5/2}).
\]
Writing \(R_\eta=\eta^{-2}\max_j|Z_j-\omega_j-\eta L_j|\), they give
\[
 R_\eta=\Phi(|\lambda_\eta|)+O_T(\sqrt\eta),\qquad
 \Phi(t)=\sqrt{\mathcal A+\mathcal B t+\mathcal Q t^2},
\]
where
\[
\mathcal A=-13638695/972-16011613c/243+20901119c^2/243>0,
\]
\[
\mathcal B=s(1448+6982c-8224c^2)/243>0,\qquad
\mathcal Q=(8+25c+20c^2)/162>0.
\]
The entire all-real ideal maximum is \(\Phi(|\lambda|)\), attained
uniquely at 7 for positive \(\lambda\), at 2 for negative \(\lambda\),
and at both when zero. Every other label is strictly lower.

The full actual cost identity is essential, not just its scalar inequality:
\[
 T_\eta=T_*+(\kappa/H)\lambda_\eta^2+S_\eta+O_T(\sqrt\eta),
\]
\[
 S_\eta=-\alpha H\sum_{l=1}^6(t_l+r_\eta/3)^2
 +\tfrac12\|v_\eta-d r_\eta h^*\|^2
 +\sum_{k=3,4}w_k\frac{-\mathcal A_k}{\eta^3}\ge0.
\]
Here \(h^*=(\sqrt{H/2},-\sqrt{H/2},0^6)\),
\(r_\eta=-\sum_l t_l/2\), and
\(\lambda_\eta=3Hr_\eta+O_T(\eta)\). The \(t_l\) and \(v_\eta\)
are the exact normalized transverse and real-profile coordinates of10152,
with simultaneous critical permutations. The positive dual weights are
\(w_4=1/(c+2c^2-1)\),
\(w_3=(2/3)[7-(2-2c^2)w_4]\).
\(N_j=(|Z_j|^2-1)/2\le0\) and
\(\mathcal A_k=(N_k+N_{9-k})/2\le0\).

The prior scoped independent
[10156 review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/quadratic-motion-audit/REVIEW.md)
and
[10182 review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/third-boundary-audit/REVIEW.md)
retain8619's concentration/rate/local-entry premises and10127's precise
fixed-cubic moment frontier/projection. We retain that same boundary.
This is not a new absolute audit of the ancestral concentration chain.
The construction below itself needs no universal concentration theorem.

## 2. The actual unrestricted-parameter family

For a real parameter \(r\), define
\[
\begin{split}
\mu&=\mu_0+\mu_2r^2,\quad
\beta=\beta_0+\beta_2r^2+\beta_4r^4,\\
\nu&=\nu_1r+\nu_3r^3,\quad
\sigma=\sigma_1r+\sigma_3r^3,
\end{split}
\]
with the target's complete written coefficients, independently checked here:
\[
\begin{array}{ll}
\mu_0=-17403419/34992-45702565c/17496+180635c^2/54,&
\mu_2=35/81-2086c/81+616c^2/27,\\
\beta_0=-1162307/23328-5484833c/11664+52426519c^2/93312,&
\beta_2=14537/1512-3889c/756-1661c^2/756,\\
\beta_4=-2/49-4c/49-2c^2/49,&\\
\nu_1=-17983/972-25711c/486+4564c^2/81,&
\nu_3=28/81+56c/81,\\
\sigma_1=-1967/81+5479c/432-5375c^2/162,&
\sigma_3=-55/189+11c/63+88c^2/189.
\end{array}
\]
Put \(\epsilon=\sqrt\eta\), \(b=\sqrt{H/2}\),
\(q_1=\Gamma-4r^2/(3H)\), \(v_2=3kHr/7\), and
\[
\begin{split}
A&=(u_z-ir/3)\eta+(w_2+iv_2)\eta^2+(\mu+i\nu)\eta^3+\epsilon^7,\\
B&=(u_p+ir)\eta+(w_2+iv_2)\eta^2+(\mu+i\nu)\eta^3+\epsilon^7,\\
K&=i(1+q_1\eta+\beta\eta^2)+dr\eta+\sigma\eta^2,\\
p'(z)&=9(z-A)^6[(z-B)^2-b^2\eta K^2],\qquad
p(z)=\int_{1-\eta}^z p'(v)\,dv.
\end{split}
\]
The literal product makes this monic degree nine with exact marked root
\(1-\eta\), six critical copies of \(A\), and the two critical points
\(B\pm b\epsilon K\). These are actual complex critical points,
including a genuinely complex sixfold point for each fixed nonzero \(r\)
and sufficiently small positive \(\eta\).

## 3. Independent algebra and individual containment

Our new arithmetic is \(\mathbb Q[w]/(w^{12}-w^6+1)\),
\(w=e^{i\pi/18}\). Thus \(i=w^9\),
\(c=(w^2+w^{-2})/2\), \(s=(w^2-w^{-2})/(2i)\),
\(\omega_j=w^{4j}\). All coefficients are exact rational vectors;
the parameter \(r\) remains a whole polynomial. The physical cosine is
the unique root of \(8c^3-6c-1\) between \(15/16\) and \(47/50\).
Monotonicity above \(1/2\), the triple-angle identity and
\(0<\pi/9<\pi/3\) identify this embedding. Forty-eight rational
bisections and outward polynomial bounds establish every used strict sign.

Omit only the common \(\epsilon^7\) shift during integer \(\eta\) jets.
We multiply the seven literal factors, integrate each complete z column,
and substitute the full anchor \(1-\eta\). This differs from the target's
Newton/power-sum construction. We obtain all ten columns through order3,
including every parameter coefficient. The first two are
\[
g_2=9+9x(z^8-1)+9y(z^7-1),\qquad
g_4^r=g_4^0+3HrQ(z),
\]
\[
Q(z)=\frac{i}{2}[(1+2c)(z^8+z^7-2)+(z^6-1)],
\]
\[
\begin{split}
g_4^0={}&-36+72x+9H/2-(9W_*/8)(z^8-1)\\
&+(9/14)(64x^2-D_*)(z^7-1)
 +(6xH+3Hu_p/2)(z^6-1).
\end{split}
\]
The fifth column is zero exactly. Define
\[
d_j=-[g_4^0(\omega_j)+g_2'(\omega_j)L_j+36\omega_j^7L_j^2]/(9\omega_j^8).
\]
For each of the nine labels we compose the entire polynomial with a root
jet and solve its next coefficient using the fixed nonzero derivative
\(9\omega_j^8\). Every coefficient equation through order3 is checked.
The resulting first and second jets are \(L_j\) and
\(d_j+3HrW_j\). We reconstruct the complete
\((Z_j\overline{Z_j}-1)/2\) from these jets. All four individual active
normals, labels3,4,5,6, have zero coefficients at orders1,2,3 for every
real \(r\). No pair average replaces this assertion.

Differentiating the defining factors at order3 also gives all four rows in
the independent variables \((\mu,\beta,\nu,\sigma)\):
\[
(\cos\theta_j-1,\ H(1-\cos2\theta_j)/7,
\sin\theta_j,\ H\sin2\theta_j/7),\quad\theta_j=2\pi j/9.
\]
The pair sum and sine-normalized difference blocks have determinants
\(2c-1>0\) and \(-H(2c-1)/7\ne0\). Hence these are the unique
four defining-variable repairs, with both odd rows essential.

Now restore the shift. Translating all eight critical factors by
\(\delta=\epsilon^7\) changes the limiting derivative \(9z^8\) by
\(-72\delta z^7\), so the anchored primitive changes by
\(-9\delta(z^8-1)\). Its first root response is \(1-\omega_j\),
and its half-normal response is \(\cos\theta_j-1\). Thus
\[
 N_3=N_6=-\tfrac32\epsilon^7+O_R(\epsilon^8),\qquad
 N_4=N_5=-(1+c)\epsilon^7+O_R(\epsilon^8).
\]
The other first normals are
\[
N_{0,2}=-1,\quad
N_{1,2}=N_{8,2}=-(2+4c-4c^2)/3<0,\quad
N_{2,2}=N_{7,2}=-(2c-1)^2/3<0.
\]

Here is the ordinary uniformity argument, separately from the finite record.
On every compact \(|r|\le R\), the literal coefficients are polynomial
in \((\epsilon,r)\) and converge uniformly to \(z^9-1\).
Choose nine disjoint small circles around its roots. For all sufficiently
small \(\epsilon\), uniform coefficient closeness and Rouche's theorem
give precisely one root within each circle, counting multiplicity.
Hence those nine roots exhaust the degree and are simple. The implicit
root maps in one common coefficient neighborhood are analytic; on a
slightly smaller compact parameter collar their derivatives through order8
are uniformly bounded. Taylor's theorem now supplies the stated uniform
remainders. All nine strict leading signs imply actual strict disk
containment for every small positive \(\epsilon\), uniformly in \(r\).
No numerical root sample, critical separation or containment of a real-part
polynomial is needed.

## 4. The direct first-power cost

Without the common shift, define the exact squared distances
\[
 D_A=|1-\eta-A|^2,\quad
 V=|1-\eta-B|^2+b^2\eta|K|^2,\quad
 X=-2b\sqrt\eta\Re[(1-\eta-B)\overline K].
\]
The two pair distances squared are \(V\pm X\); in particular
\[
 X^2=2Hr^2(d-1)^2\eta^3+O_R(\eta^4).
\]
We multiply these squared-distance jets directly, retaining all r powers.
For a jet with unit constant, use
\((1+u)^{-1/2}=1-u/2+3u^2/8-5u^3/16+O(u^4)\).
The pair sum is
\(2V^{-1/2}+3X^2/4+O_R(\eta^4)\).
Adding six copies of \(D_A^{-1/2}\) gives the whole identity
\[
 F^0=8+C\eta+B_*\eta^2+[T_*+9H\kappa r^2]\eta^3+O_R(\eta^4).
\]
This checks the r-fourth cancellation and the correct two-branch split
payment; it is not a small-skew fit or a squared-reciprocal objective.

Each critical reciprocal has derivative with respect to a common real
translation equal to1 at the limiting configuration \(a=1,\zeta=0\).
Thus the shift adds \((6+2)\epsilon^7=8\epsilon^7\) at first order.
All distances are uniformly bounded away from zero; the inverse square
root and the two-branch expression are smooth there. Uniform Taylor
estimates therefore give
\[
 F=8+C\eta+B_*\eta^2+[T_*+9H\kappa r^2]\eta^3
                       +8\eta^{7/2}+O_R(\eta^4).
\]
Directly cubing the imaginary critical components gives
\[
6(\Im A)^3+2(\Im B)^3+6b^2\eta(\Im B)(\Im K)^2
      =3Hr\eta^2+O_R(\eta^3),
\]
so \(\lambda_\eta=3Hr+O_R(\eta)\).
The root jets give
\(Z_j=\omega_j+\eta L_j+\eta^2(d_j+3HrW_j)+O_R(\eta^3)\).
For any fixed real \(\lambda\), take \(r=\lambda/(3H)\).
This is actual attainment of \(T_*+(\kappa/H)\lambda^2\).

## 5. The exact fixed cap, both endpoints and the maximum

Fix \(T>T_*\), \(\gamma=\kappa/H\), and
\(\Lambda=\sqrt{(T-T_*)/\gamma}>0\). In the exact cap \(T_\eta\le T\),
the inherited cost inequality gives
\(|\lambda_\eta|\le\Lambda+O_T(\sqrt\eta)\), with a uniform error
because \(\Lambda\) is a fixed positive number. The inherited motion
law and bounded derivative of \(\Phi\) imply
\(R_\eta\le\Phi(\Lambda)+O_T(\sqrt\eta)\).

Every fixed \(|\lambda|<\Lambda\) is attained within the exact cap
for all sufficiently small positive \(\eta\), using the strict limiting
cost gap. Constant endpoint r would pay the positive shift cost, so use
\[
D=8H/(\kappa\Lambda),\qquad
r_\eta^\pm=\pm(\Lambda-D\sqrt\eta)/(3H).
\]
These parameters stay in a fixed compact interval. Section4 then gives
\[
T_\eta=T_*+\gamma(\Lambda-D\sqrt\eta)^2+8\sqrt\eta+O_T(\eta)
       =T-8\sqrt\eta+O_T(\eta)<T.
\]
The endpoints are therefore realized in the exact cap for every
sufficiently small positive \(\eta\), with limiting skew \(\pm\Lambda\)
and motion \(\Phi(\Lambda)+O_T(\sqrt\eta)\).
The complete set of limiting skews is exactly \([-\Lambda,\Lambda]\).

For fixed \(\eta\), the coefficient set of monic disk-rooted polynomials
with the marked root is compact: it is the image of a closed subset of
the compact labelled original-root disk product. The critical multiset
depends continuously on coefficients. The extended reciprocal sum is
lower semicontinuous, including collisions of a critical point with the
marked root. Its finite sublevel is closed and nonempty by the endpoint
family. In the sufficiently small common collar, the canonical simple
original-root maps are continuous on this entire sublevel, so \(R_\eta\)
attains a maximum. Combining the two bounds proves
\[
\max_{T_\eta\le T} R_\eta=\Phi(\Lambda)+O_T(\sqrt\eta).
\]
No exact finite-eta skew interval or identity for this maximum is implied.

## 6. Proved quantitative strengthening for near-maximizers

For each fixed \(T>T_*\), there are constants \(K_T,\eta_T>0\) such
that every actual cap competitor with
\[
 R_\eta\ge\Phi(\Lambda)-\delta,\quad 0\le\delta\le1,
 \qquad E=\delta+\sqrt\eta,
\]
satisfies
\[
 \big||\lambda_\eta|-\Lambda\big|+|T_\eta-T|\le K_TE,
\]
\[
 \left(\sum_l(t_l+r_\eta/3)^2\right)^{1/2}
 +\|v_\eta-d r_\eta h^*\|\le K_T\sqrt E,
 \qquad |N_j|\le K_T\eta^3E\quad(j=3,4,5,6).
\]
For \(E\) sufficiently small, let
\(\sigma_\eta=\operatorname{sign}(\lambda_\eta)\in\{-1,1\}\).
Then also
\[
\eta^{-2}\max_j|Z_j-\omega_j-\eta L_j
                    -\eta^2(d_j+\sigma_\eta\Lambda W_j)|\le K_TE.
\]

Proof: in one fixed compact scalar interval containing every competitor,
\(\Phi'(t)=(\mathcal B+2\mathcal Q t)/(2\Phi(t))\) has a positive
lower bound. The motion law, the assumed lower motion, and the upper
skew bound therefore imply
\(\big||\lambda_\eta|-\Lambda\big|\le K_TE\).
Using the full nonnegative cost identity,
\[
 0\le S_\eta\le\gamma(\Lambda^2-\lambda_\eta^2)+O_T(\sqrt\eta)
                    \le K_TE.
\]
This bounds each separate positive payment. The same identity gives
\(0\le T-T_\eta\le K_TE\).
Individual nonpositivity gives \(|N_j|\le2|\mathcal A_k|\),
which proves all four individual bounds. The all-nine drift estimate
gives the final inequality. For small E the skew stays away from zero;
the strict ideal gap thus supplies the target's unique actual winner,
label7 for positive skew and label2 for negative skew.

For actual exact maximizers, Section5 implies \(\delta=O_T(\sqrt\eta)\).
Consequently the endpoint skew and all-nine scaled drift errors are
\(O_T(\sqrt\eta)\), the transverse/real tangent errors are
\(O_T(\eta^{1/4})\), and each active half-normal is
\(O_T(\eta^{7/2})\). The target's qualitative maximizing-sequence
rigidity follows as well. These constants are ineffective and depend
on the fixed positive gap \(T-T_*\); there is no claim of uniformity
as that gap vanishes or of optimal rates.

## 7. Trust boundary and excluded claims

The literal construction, whole parameter algebra, physical signs and all
nine root jets are independently checked. The exact finite record does
not formalize analytic root/Taylor maps, compactness or the inherited
all-competitor entry and projection premises. These are the ordinary
written arguments and the precise relative boundary in Section1.
Zero-skew third repairs, all lower coefficients, the fixed drifts and
ideal maximum retain their prior credit. Reviewer10182's equality-cap
feasibility and quantitative minimizing rigidity are also prior results.
New child10212's fourth construction concerns a different exact optimal
cap regime; it has no verdict from this review. No universal fourth
optimum, effective collar, exact finite-size skew range, unrestricted
first-power endpoint or historical priority is asserted.
