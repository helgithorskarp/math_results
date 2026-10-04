# Fourth repair and shrinking skew in the exact optimal cap

Actual author **six-sendov-3**, role **researcher**, 2026-10-04.
Complete ordinary author proof, **unformalized and independently unreviewed**.
The finite exact replay is same-author evidence. This proves a better actual
fourth upper construction, a sharp coefficient in a precisely restricted
repair class, and a motion lower bound. It does **not** determine the
universal fourth coefficient or the sharp all-competitor motion correction.

## 1. Definitions, constants and statements

Let \(p\) be monic of degree9 with an actual marked root \(a=1-\eta>0\).
Count all eight critical points with multiplicity, and set
\[
 F(p)=\sum_{l=1}^8|a-\zeta_l|^{-1},\qquad
 T_\eta=(F-8-C\eta-B_*\eta^2)/\eta^3.
\]
A zero denominator is infinity. The exact optimal third cap is
\(\mathcal P_{\eta,T_*}=\{p:\text{all nine roots in }\overline{\mathbb D},
\ a=1-\eta\text{ is a root},\ T_\eta\le T_*\}\).

Use the previously proved constants from
[10152](../third-boundary-optimum/PROOF.md),
[10113](../quadratic-root-motion/PROOF.md) and
[10197](../nonzero-skew-attainment/PROOF.md):
\[
\begin{gathered}
c=\cos(\pi/9),\quad y=[3(1+c)]^{-1},\quad x=2/3-y,
\quad H=14y,\quad U_0=-8x,\quad C=8/3+y,\\
k=-7(1+2c)/18,\quad\rho=(c-5)/3,\quad d=3k+\rho,\\
u_z=-37/36+20c/9-20c^2/9,\quad u_p=u_z-\rho H/2,\\
W_*=2512/27+5840c/9-21392c^2/27,\quad w_2=W_*/8,\\
D_*=-4270/27-29492c/27+4012c^2/3,
\quad\Gamma=13/36+1253c/72-50c^2/3,\\
\alpha=-527/360+41c/90+13c^2/90<0,\quad
\kappa=(k+\rho)^2/2+10\alpha/27>0,\\
B_*=2311/108+4934c/27-1976c^2/9,\\
T_*=-60800959/17496-307083769c/17496+10980067c^2/486.
\end{gathered}                                                    \tag{1}
\]
The two previously attained third repairs are
\[
\mu_0=-17403419/34992-45702565c/17496+180635c^2/54,
\]
\[
\beta_0=-1162307/23328-5484833c/11664+52426519c^2/93312.
                                                               \tag{2}
\]
Our new constants are
\[
\begin{split}
M_*&=8148040331/629856+78878749667c/1259712-51194418673c^2/629856,\\
\beta_*&=27821775167/17915904+80418819893c/8957952-12650091319c^2/1119744,\\
G_*&=183619658945/2519424+444829186913c/1259712-288729410449c^2/629856<0,\\
\nu_*&=-2424695/13122-136157c/4374+144046c^2/6561,\\
\sigma_*&=-536333191/1119744-805399537c/559872+891296017c^2/559872.
\end{split}                                                     \tag{3}
\]
Define
\[
 \ell=\sqrt{-HG_*/\kappa}>0,\qquad
 s_*={\mathcal B\ell\over2\sqrt{\mathcal A}}>0,                  \tag{4}
\]
where the credited motion constants are
\[
\begin{split}
\mathcal A&=-13638695/972-16011613c/243+20901119c^2/243>0,\\
\mathcal B&=\sin(\pi/9)(1448+6982c-8224c^2)/243>0,\\
\mathcal Q&=(8+25c+20c^2)/162>0.
\end{split}                                                     \tag{5}
\]

**Restricted fourth optimum.** In the fixed-third-jet class defined in
section2, the smallest possible fourth coefficient is exactly \(G_*\).
It is attained by actual strictly disk-rooted polynomials, with
\(M=M_*\), \(\beta=\beta_*\) and a higher inward term. This class
fixes the lower jets of both critical centers and of their pair scale;
it does not include arbitrary actual competitors.

**Actual shrinking-skew construction.** Section4 gives an explicit family
\(p_{\epsilon,t}\), \(\eta=\epsilon^2\), with all nine original roots
strictly inside the disk for every sufficiently small positive \(\epsilon\),
uniformly on every compact real \(t\)-interval. Its actual skew is
\(\lambda_\eta=\eta^{-2}\sum(\Im\zeta_l)^3\). Uniformly for bounded \(t\),
\[
 \lambda_\eta=t\sqrt\eta+O(\eta^{3/2}),                         \tag{6}
\]
\[
 F=8+C\eta+B_*\eta^2+T_*\eta^3
   +(G_*+\kappa t^2/H)\eta^4+8\eta^{9/2}+O(\eta^5).           \tag{7}
\]
For every fixed \(R>\ell\), its exact cap inside \([-R,R]\) is
\([-t_\epsilon,t_\epsilon]\), where
\[
 t_\epsilon=\ell-{4H\over\kappa\ell}\epsilon+O(\epsilon^2).
                                                               \tag{8}
\]
Both endpoints satisfy the exact equality \(T_\eta=T_*\), while
their original roots remain strictly inside the disk. The exact image
of this constructed cap under the actual skew is a symmetric interval
whose positive endpoint is
\[
 \lambda_\epsilon=\ell\epsilon-{4H\over\kappa\ell}\epsilon^2
                   +O(\epsilon^3).                            \tag{9}
\]
These are intervals for this explicit family, not an exact skew range
for the full class of disk-rooted polynomials.

**Motion.** Put \(\omega_j=e^{2\pi i j/9}\), \(0\le j\le8\), and
\[
 L_j=-\omega_j/3-x-y/\omega_j,
\quad R_\eta(p)=\max_j {|Z_j-\omega_j-\eta L_j|\over\eta^2},
                                                               \tag{10}
\]
with the unique local original-root labels \(Z_j\) near \(\omega_j\).
Within the constructed exact cap the maximum occurs at its two
parameter endpoints, for all sufficiently small positive \(\eta\), and is
\[
 \sqrt{\mathcal A}+s_*\sqrt\eta+O(\eta).                        \tag{11}
\]
Its winning original label is7 at the positive endpoint and2 at the
negative endpoint. In particular the full exact cap satisfies
\[
 \max_{p\in\mathcal P_{\eta,T_*}}R_\eta(p)
 \ \ge\sqrt{\mathcal A}+s_*\sqrt\eta-O(\eta).                  \tag{12}
\]
The previously reviewed upper error remains \(O(\eta^{1/4})\);
we do not claim a matching universal \(O(\sqrt\eta)\) error or an
optimal value of \(s_*\) across all competitors.

## 2. Two actual fourth-normal rows and their positive dual

The restricted class consists of anchored polynomials
\[
 p'(z)=9(z-A)^6[(z-B)^2-(H/2)\eta K^2],\qquad
 p(z)=\int_{1-\eta}^zp'(v)\,dv,                                \tag{13}
\]
where for fixed real \(M,\beta\),
\[
\begin{split}
A&=u_z\eta+w_2\eta^2+\mu_0\eta^3+M\eta^4+o(\eta^4),\\
B&=u_p\eta+w_2\eta^2+\mu_0\eta^3+M\eta^4+o(\eta^4),\\
K&=i(1+\Gamma\eta+\beta_0\eta^2+\beta\eta^3)+o(\eta^3).
\end{split}                                                     \tag{14}
\]
The higher remainders may be complex; their stated orders cannot
alter the displayed fourth polynomial, radial or objective coefficient.
The construction later uses real \(\eta^{9/2}\), which is allowed.
All critical multiplicities are retained: six at \(A\) and the pair
\(B\pm\sqrt{H/2}\sqrt\eta K\). All approach0, so all distances from
the marked root approach1. Original roots are simple near the nine
roots of \(p_0=z^9-1\).

Let \(N_j=(|Z_j|^2-1)/2\). At \(j=3,4,5,6\) their first three
coefficients vanish. Write \(N_j=q_j(M,\beta)\eta^4+o(\eta^4)\),
and set \(A_j=1-\cos(2\pi j/9)\), \(B_j=1-\cos(4\pi j/9)\).
Changing only the two fourth repairs changes the entire fourth
polynomial coefficient by
\[
 -9\,\delta M(z^8-1)+{9H\over7}\,\delta\beta(z^7-1).           \tag{15}
\]
The implicit root derivative is \(-\omega_j\delta p(\omega_j)/9\).
Taking the radial coefficient therefore gives, for every original label,
\[
 \delta q_j=-A_j\delta M+(H/7)B_j\delta\beta.                  \tag{16}
\]
In particular \(A_3=B_3=3/2\), \(A_4=1+c\), \(B_4=2-2c^2\).
The two rows have determinant \(2c-1>0\), so both can be repaired.

We reproduce the entire defining-factor primitive and all nine original
jets through order4. At \(M=100,\beta=0\) this gives the reviewed
[10182 baseline](../../six-reviewer-4/third-boundary-audit/PROOF.md),
\[
\begin{split}
q_3=q_6&=(77000544293+371513219527c-483693373045c^2)/6718464,\\
q_4=q_5&=(-17159240005-90073161839c+112464832314c^2)/13436928.
\end{split}                                                     \tag{17}
\]
Equations(16)–(17) determine all four active fourth coefficients
without guessing or pair averaging a complex family's constraints.
Solving the two independent rows gives precisely \(M_*,\beta_*\)
in(3); all four individual fourth normals then vanish.

The positive dual is
\[
 w_4=(c+2c^2-1)^{-1},\quad
 w_3=\tfrac23[7-(2-2c^2)w_4],\quad
 \sum_{j=3,4}w_jA_j=8,\quad\sum_{j=3,4}w_jB_j=7.              \tag{18}
\]
Both weights are positive in the physical embedding. The actual fourth
first-power coefficient is affine with slopes8 and \(-H\):
\[
 G(M,\beta)=G_*+8(M-M_*)-H(\beta-\beta_*)
           =G_*+w_3(-q_3)+w_4(-q_4).                         \tag{19}
\]
For completeness this scalar follows directly from the actual distances.
Put \(a_z=1+u_z\), \(a_p=1+u_p\), and
\[
\begin{split}
Q_1&=-2a_p+H/2,\quad Q_2=a_p^2-2w_2+H\Gamma,\\
Q_3&=2a_pw_2-2\mu_0+(H/2)(\Gamma^2+2\beta_0),\\
Q_4&=2a_p\mu_0+w_2^2-2M+H(\Gamma\beta_0+\beta).
\end{split}
\]
The fourth coefficient of
\(6/(1-\eta-A)+2[(1-\eta-B)^2+(H/2)\eta(1+\Gamma\eta+
\beta_0\eta^2+\beta\eta^3)^2]^{-1/2}\) is
\[
 6(M+2a_z\mu_0+w_2^2+3a_z^2w_2+a_z^4)-Q_4
 +\tfrac34(2Q_1Q_3+Q_2^2)-\tfrac{15}8Q_1^2Q_2
 +\tfrac{35}{64}Q_1^4.                                      \tag{20}
\]
Reduction by \(8c^3-6c-1=0\) gives \(G_*\) at the joint repair.
The generic single-distance fourth scalar, also checked as a whole
rational polynomial, is
\[
 (1+u)^4-5(1+u)^3h^2+\tfrac{45}8(1+u)^2h^4
 -\tfrac{35}{16}(1+u)h^6+\tfrac{35}{128}h^8.                  \tag{21}
\]
Actual disk containment in class(14) forces each active \(q_j\le0\).
Thus(19) proves \(G\ge G_*\), and equality forces both independent
rows to vanish, hence \(M=M_*\), \(\beta=\beta_*\). The inward
construction at \(t=0\) below attains that coefficient with all nine
roots strict. This proves the restricted optimum, including necessity
and physical attainment. It is not a universal optimization argument.

## 3. Exact baseline and improvement over the reviewed upper construction

Reviewer six-reviewer-4's complete
[REVIEW10182 proof](../../six-reviewer-4/third-boundary-audit/PROOF.md)
already proved exact-cap feasibility. Its construction changes only
\(M\), retaining \(\beta=0\), and has
\[
\begin{split}
\theta&=-232825395763/40310784-572817768121c/20155392
                          +46344688537c^2/1259712,\\
G(\theta,0)&=(-407598998293-1964260111205c+2551353809267c^2)/10077696,\\
M_\dagger&=(-174567528253-872760677921c+1126922107823c^2)/53747712,
\end{split}                                                     \tag{22}
\]
with \(G(M_\dagger,0)=G(\theta,0)/2<0\).
We reconstruct this entire second polynomial independently from the
literal factor, checking all nine full fourth root/radial jets and
all first-power coefficients through order4. No reviewer code,
arithmetic, EXPECTED fixture or damage control is imported.

The new strict improvement is the exact physical sign
\[
 G(M_\dagger,0)-G_*
 ={ -1876556269853-9081527101813c+11790694943635c^2\over20155392}>0.
                                                               \tag{23}
\]
Both(22)'s negative upper construction and its original equality-cap
feasibility are reviewer credit. Reproducing them is validation, not
new research. The new information is the simultaneous repair,
restricted optimality, its smaller fourth coefficient, and the
shrinking-skew realization below.

## 4. Literal shrinking-skew family and its two actual odd repairs

Use the closed previously attained repairs from10197, with
\[
\begin{split}
\mu(r)&=\mu_0+\mu_2r^2,&
\mu_2&=35/81-2086c/81+616c^2/27,\\
\beta(r)&=\beta_0+\beta_2r^2+\beta_4r^4,&
\beta_2&=14537/1512-3889c/756-1661c^2/756,\\
&&\beta_4&=-2/49-4c/49-2c^2/49,\\
\nu(r)&=\nu_1r+\nu_3r^3,&
\nu_1&=-17983/972-25711c/486+4564c^2/81,\\
&&\nu_3&=28/81+56c/81,\\
\sigma(r)&=\sigma_1r+\sigma_3r^3,&
\sigma_1&=-1967/81+5479c/432-5375c^2/162,\\
&&\sigma_3&=-55/189+11c/63+88c^2/189.
\end{split}                                                     \tag{24}
\]
Set \(\epsilon=\sqrt\eta\), \(r=t\epsilon/(3H)\),
\(q_1=\Gamma-4r^2/(3H)\), and \(v_2=3kHr/7\). In(13) take
the following **actual** centers and pair scale, with no omitted terms:
\[
\begin{split}
A={}&(u_z-ir/3)\eta+(w_2+iv_2)\eta^2
 +[\mu(r)+i\nu(r)]\eta^3+(M_*+i\nu_*r)\eta^4+\eta^{9/2},\\
B={}&(u_p+ir)\eta+(w_2+iv_2)\eta^2
 +[\mu(r)+i\nu(r)]\eta^3+(M_*+i\nu_*r)\eta^4+\eta^{9/2},\\
K={}&i[1+q_1\eta+\beta(r)\eta^2+\beta_*\eta^3]
       +dr\eta+\sigma(r)\eta^2+\sigma_*r\eta^3.
\end{split}                                                     \tag{25}
\]
Its eight critical points are \(A\) six times and
\(B\pm\sqrt{H/2}\epsilon K\). This need not be a conjugate critical
set when \(t\ne0\). Conjugating the whole polynomial corresponds
to replacing \(t\) by \(-t\): \(A,B\) conjugate and
\(K(-t)=-\overline{K(t)}\). Consequently \(F\) and \(R_\eta\)
are even in \(t\), and the actual cubic skew is odd.

To derive, rather than guess, the new odd repairs, first omit
\(i\nu_*r\eta^4\), \(\sigma_*r\eta^3\), and the final common
\(\eta^{9/2}\). Substitute \(r=t\epsilon/(3H)\) before truncation.
Complete original-root composition gives all four individual normals
zero through \(\epsilon^8\). Their ninth coefficients at \(j=3,4\)
are \(t\sin(2\pi j/9)o_j/(3H)\), where
\[
\begin{split}
o_3&=-589162435/839808-2891972395c/839808+315914389c^2/69984,\\
o_4&=1107533119/839808+354297679c/69984-2927333483c^2/419904.
\end{split}                                                     \tag{26}
\]
There is no unaccounted cubic or higher polynomial in \(t\) at this
order; the entire coefficient maps, not a numerical fit, are checked.
Common imaginary fourth and real third pair-scale changes supply
the individual radial columns \(\sin(2\pi j/9)\) and
\((H/7)\sin(4\pi j/9)\). After dividing by the nonzero first sine,
the two actual equations are
\[
 o_3+\nu_*-(H/7)\sigma_*=0,\qquad
 o_4+\nu_*-(2cH/7)\sigma_*=0.                                \tag{27}
\]
Their determinant is \(-H(2c-1)/7\ne0\). Solving gives the two
closed constants in(3). Recomposition of the whole actual factor now
checks all four individual normals; no conjugate-pair average is used
as a surrogate for an individual complex-root constraint.

The common final inward step changes the ninth normal by \(-A_j\).
The full result is
\[
 N_3=N_6=-\tfrac32\epsilon^9+O_R(\epsilon^{10}),\quad
 N_4=N_5=-(1+c)\epsilon^9+O_R(\epsilon^{10}).                  \tag{28}
\]
All five remaining labels already have negative leading coefficients:
\[
\begin{split}
N_0&=-\epsilon^2+O_R(\epsilon^4),\\
N_1=N_8&=-(2+4c-4c^2)\epsilon^2/3+O_R(\epsilon^4),\\
N_2=N_7&=-(2c-1)^2\epsilon^2/3+O_R(\epsilon^4).
\end{split}                                                     \tag{29}
\]
The equalities in(29) refer to the displayed leading coefficient;
the full skew polynomial's reflected normals need not be identical.

All coefficients of(25)'s anchored polynomial are real analytic in
\((\epsilon,t)\), with \(p_{0,t}=z^9-1\) independently of \(t\).
The simple-root implicit theorem at each of the nine \(\omega_j\),
followed by a finite cover of \([-R,R]\), supplies nine distinct
branches in one common collar and uniform Taylor remainders. Degree9
means these are all original roots; there are no additional uncounted
roots. Negative leading normals(28)–(29) then prove strict disk
containment for every sufficiently small positive \(\epsilon\),
uniformly on the compact parameter interval. The branch near1 is
exactly the prescribed root \(1-\epsilon^2\).

For clarity, the finite derivation uses every critical power sum:
\[
 P_l=6A^l+2\sum_{\substack{0\le j\le l\\j\text{ even}}}
 {l\choose j}B^{l-j}[(H/2)\epsilon^2K^2]^{j/2},\quad1\le l\le8,
\]
\[
 e_0=1,\quad le_l=\sum_{j=1}^l(-1)^{j-1}e_{l-j}P_j,
 \qquad p'=9\sum_{l=0}^8(-1)^le_lz^{8-l}.                    \tag{30}
\]
Integration and anchoring of(30) agree with the literal factor in all
ten polynomial columns through \(\epsilon^9\). Each original-root
series is separately composed with that entire polynomial, coefficient
by coefficient, and its full half-norm is separately multiplied out.

## 5. Actual first-power cost, skew and exact constructed cap

The six equal critical distances have square \(V_A=|a-A|^2\).
The two remaining squared distances are \(V_B\pm X\), with
\[
 V_B=|a-B|^2+(H/2)\epsilon^2|K|^2,
\quad X^2=2H\epsilon^2\Re[(a-B)\overline K]^2.
\]
For(25), \(X^2=O_R(\epsilon^8)\). Hence their first-power sum is
\[
 2V_B^{-1/2}+\tfrac34X^2+O_R(\epsilon^{10}).                  \tag{31}
\]
Indeed the exact even expansion is
\(2V_B^{-1/2}+(3/4)X^2V_B^{-5/2}+O(X^4)\), and
\(V_B-1=O_R(\epsilon^2)\). Expanding \(6V_A^{-1/2}\) and(31)
through the fourth binomial power gives the entire vector(7), including
the physically necessary cross-distance contribution and the positive
common-shift coefficient8. This also verifies that substituting shrinking
skew in a fixed-skew third-cost formula has not silently discarded a
fourth-order term.

Write \(Y_A=\Im A\), \(Y_B=\Im B\), \(Y_K=\Im K\). Directly from
all eight actual critical multiplicities,
\[
 \sum(\Im\zeta_l)^3
 =6Y_A^3+2Y_B^3+3H\epsilon^2Y_BY_K^2
 =t\epsilon^5+O_R(\epsilon^7),                              \tag{32}
\]
with no sixth coefficient. Division by \(\eta^2=\epsilon^4\)
proves(6). The analytic uniform remainder also controls its first
parameter derivative, so \(\partial_t\lambda_\eta
=\epsilon+O_R(\epsilon^3)>0\) in a small common collar.

Subtract the first four objective coefficients and divide by
\(\epsilon^8\). The resulting function extends real analytically:
\[
 E(\epsilon,t)=G_*+\kappa t^2/H+8\epsilon+O_R(\epsilon^2).
                                                               \tag{33}
\]
It is even in \(t\). At \((0,\ell)\), its \(t\)-derivative is
\(2\kappa\ell/H>0\). The implicit theorem gives the unique nearby
zero \(t_\epsilon\), with derivative
\(-8/(2\kappa\ell/H)=-4H/(\kappa\ell)\), proving(8).

There are no other cap components within any fixed \([-R,R]\),
\(R>\ell\). Choose \(0<\delta<\ell\). On \([0,\delta]\),
\(E<0\) uniformly for small \(\epsilon\). On \([\delta,R]\),
\(\partial_tE=2\kappa t/H+O_R(\epsilon^2)>0\), so its unique
zero divides exactly the feasible and infeasible parameters. Evenness
gives the negative endpoint. All these family members already satisfy
strict original-root containment. Thus equality at the two endpoints
is an actual equality in the exact third cap, not a formal jet equality.
Monotonicity and oddness of(32) give the exact constructed skew interval
and its expansion(9).

## 6. All-nine finer motion and the constructed maximum

For a self-contained description of \(d_j\), put
\[
 g_2(z)=9+9x(z^8-1)+9y(z^7-1),
\]
\[
\begin{split}
g_4^*(z)={}&-36-9U_0+9H/2-9W_*(z^8-1)/8\\
 &+9(U_0^2-D_*)(z^7-1)/14
   +(-3U_0H/4+3Hu_p/2)(z^6-1),\\
d_j={}&-{\omega_j\over9}
 [g_4^*(\omega_j)+g_2'(\omega_j)L_j+36\omega_j^7L_j^2].
\end{split}                                                     \tag{34}
\]
These are the full credited canonical second-order original motions.
The literal construction, checked for all nine labels, gives
\[
 Z_j=\omega_j+\epsilon^2L_j+\epsilon^4d_j
       +\epsilon^5tW_j+O_R(\epsilon^6),
\]
\[
 W_j={i\over18}[(3+4c)\omega_j-(1+2c)(1+\omega_j^{-1})
                      -\omega_j^{-2}].                       \tag{35}
\]
This is a stronger family-specific remainder than importing a general
\(O(\eta^{5/2})\) cap map: that general error alone could obscure
the new \(\eta^{5/2}\) original motion.

The exact all-nine algebra gives
\[
 |d_7+uW_7|^2=\mathcal A+\mathcal Bu+\mathcal Qu^2,
\quad |d_2+uW_2|^2=\mathcal A-\mathcal Bu+\mathcal Qu^2.        \tag{36}
\]
Every other label has \(|d_j|^2<\mathcal A\); all seven strict
zero-skew gaps are checked in the physical field. Thus, uniformly on
bounded \(t\), (35)–(36) give
\[
 R_\eta(p_{\epsilon,t})
 =\sqrt{\mathcal A}+{\mathcal B\over2\sqrt{\mathcal A}}
                  |t|\epsilon+O_R(\epsilon^2).              \tag{37}
\]
For \(t\in[\delta,R]\), label7 uniquely wins: the other seven
have a fixed leading gap, while the label7/2 gap is positive of order
\(t\epsilon\), larger than the \(O_R(\epsilon^2)\) remainder.
Its motion is differentiable there and has positive derivative
\(\mathcal B\epsilon/(2\sqrt{\mathcal A})+O_R(\epsilon^2)\).
The same follows at negative \(t\) by reflection, with label2.

Choosing any \(0<\delta<\ell\), the central interval's upper
value in(37) is strictly below the endpoint value for small
\(\epsilon\). The winning motion is strictly increasing on
\([\delta,t_\epsilon]\). Consequently the constructed exact cap's
global maximum is attained precisely at its two parameter endpoints.
Substitution of(8) into(37) proves(11), with positive coefficient(4).
This establishes a sharp motion correction for this constructed cap,
with no optimality claim across all possible polynomial families.

## 7. Global comparison and its retained trust boundary

The constructed family alone proves the actual lower bound(12).
For the full cap's compactness, local all-nine labeling, and its
known uniform upper bound, we retain exactly the actual-competitor
scope of
[REVIEW10182](../../six-reviewer-4/third-boundary-audit/PROOF.md),
itself relative to
[REVIEW10156](../../six-reviewer-4/quadratic-motion-audit/PROOF.md)'s
precisely scoped8619 concentration/rate/local entry and10127 fixed-cubic
moment frontier/projection. No complete8668 or10127 ancestor verdict
is transported to this leaf. Our constructive and restricted-class
arguments do not use a universal concentration theorem.

Monic disk-rooted coefficients with the fixed marked root form a compact
set; the finite objective cap is closed by continuity of critical
multisets and lower semicontinuity of extended reciprocal distances.
The retained cap labeling makes \(R_\eta\) continuous there, so its
maximum exists. REVIEW10182's equality-cap drift bound then gives
\[
 \sqrt{\mathcal A}+s_*\sqrt\eta-O(\eta)
 \le\max_{p\in\mathcal P_{\eta,T_*}}R_\eta(p)
 \le\sqrt{\mathcal A}+O(\eta^{1/4}).                           \tag{38}
\]
In particular the normalized lower excess has liminf at least \(s_*>0\).
The exponents and constants on the two sides are not matched. A universal
fourth lower expansion and an improved all-competitor skew/motion rate
remain substantive analytic obligations. Exact equality-cap feasibility
was already established by the reviewer and is not counted as new here.

## 8. Reproduction, attribution and exact limitations

The standard-library source
[cap.py](cap.py) reconstructs the literal factors and ALL8 Newton moments,
all ten anchored columns, all nine full original jets and half-normals,
the actual first-power distances, cubic skew and both winning quadratics.
[EXPECTED.json](EXPECTED.json) records the entire compact typed output.
There are416 whole field-polynomial identities, one whole generic
rational identity, and35 physical rational sign bounds. The unchanged
same-author arithmetic kernel is pinned separately; it is not an
independent reviewer or formal proof assistant.

Signs use exact rational Horner evaluation on an isolating interval for
the unique root of \(8c^3-6c-1\) in \((15/16,47/50)\), narrowed
by48 monotone rational bisections. No floating-point sign, fitted
coefficient, incomplete enumeration, timeout or solver verdict is used.
Coefficient identities are checked as entire maps before their hashes
are stored. The canonical record SHA256 is
`d6925c6515ee6ad211c51a2fa9ad68124b3dee5a41b3aca3ea48dda49a647769`.

[dependencies.json](dependencies.json) pins complete source files.
The useful baseline compares all50 primitive columns, all45 root and
all45 half-normal coefficients through order4, and all four first-power
coefficients through order3 with10152's entire pinned record. It also
compares all four complete symbolic repairs and all27 zero-parameter
root coefficients through order2 with10197. Reviewer10182's entire
ordinary PROOF/REVIEW is read and attributed, while its executable and
fixtures remain unimported. These are same-author validation checks,
not a new independent review of those prior analytic theorems.

Run from this directory, Python3.12.14 observed, standard library only:
```
python3 -I -B verify.py
python3 -I -B -O verify.py
python3 -I -B verify.py --baseline-root ../../..
python3 -I -B validate.py --baseline-root ../../.. --output /tmp/sendov-fourth-cap-validation.json
```
The bounded serial validator performs four local/optimized/cold
positive replays, nine distinct mathematical damages in normal and
optimized modes, seventeen typed/whole external-record rejections and
one source-byte rejection. Every mathematical child has a fixed45-second
guard, one native thread and the existing1CPU/2GiB scope. A guard failure
is operational incompleteness, never mathematical nonexistence.

The analytic implicit maps, uniform Taylor/derivative remainders,
all-root containment, IFT cap endpoints and maximal-motion transfer are
complete written ordinary arguments, not formalized by the finite
record. The new leaf is independently unreviewed. The global stronger
degree-nine first-power endpoint, effective numerical collar, universal
fourth coefficient and universal sharp motion correction remain open.
Classical Newton/binomial/implicit-function and positive-dual methods
are credited; historical priority is not asserted.
