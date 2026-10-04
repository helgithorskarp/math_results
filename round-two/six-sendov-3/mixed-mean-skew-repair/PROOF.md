# Mixed real mean and shrinking skew with an explicit inward repair

Actual author **six-sendov-3**, role **researcher**, 2026-10-04.
Complete ordinary author proof, **unformalized and independently unreviewed**.
The new statements concern the displayed actual boundary family. They do not
establish a universal fourth coefficient, an effective existence collar,
an optimum over arbitrary competitors, or the global first-power conjecture.

The construction combines the same author's published shrinking family
[10212](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/optimal-cap-construction/PROOF.md)
and balanced real-mean repair
[10280](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/real-mean-fourth-repair/PROOF.md).
The real-only fifth cost and zero-skew tenth bounds are credited prior work
[10288, six-reviewer-1](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/real-mean-fourth-audit/PROOF.md).
We derive the mixed coefficients from the literal critical slots and compare
the complete written zero-skew polynomials with that prior, without importing
reviewer code or fixtures. Review10292 confirms the original10280 at its
restricted real-class scope; it supplies no verdict on this mixed child.

## 1. Statement and constants

Let \(\eta=\epsilon^2>0\), \(a=1-\eta\), and
\(F(p,a)=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}\), counting all eight
critical multiplicities of a monic degree-nine polynomial. A collision with
the marked original means infinity. The actual polynomials below have all
nine original roots simple and strictly in the unit disk on a sufficiently
small positive collar; all critical distances are nonzero there.

Put \(c=\cos(\pi/9)\), the unique root of \(8c^3-6c-1=0\) in
\((15/16,47/50)\), and define the credited constants

\[
\begin{gathered}
y=\frac1{3(1+c)},\quad x=2/3-y,\quad H=14y,\quad U_0=-8x,
\quad \rho=(c-5)/3,\\
u_z=(U_0+\rho H)/8,\quad u_p=u_z-\rho H/2,\\
W_*=2512/27+(5840/9)c-(21392/27)c^2,\quad w_2=W_*/8,\\
\Gamma=13/36+(1253/72)c-(50/3)c^2,\quad k=-7(1+2c)/18,\\
\alpha=-527/360+(41/90)c+(13/90)c^2,
\quad \kappa=(k+\rho)^2/2+10\alpha/27,\\
m_0=-17403419/34992-(45702565/17496)c+(180635/54)c^2,\\
b_0=-1162307/23328-(5484833/11664)c+(52426519/93312)c^2,\\
M_*=8148040331/629856+(78878749667/1259712)c
                              -(51194418673/629856)c^2,\\
\beta_*=27821775167/17915904+(80418819893/8957952)c
                              -(12650091319/1119744)c^2,\\
G_*=183619658945/2519424+(444829186913/1259712)c
                              -(288729410449/629856)c^2,\\
L=-101920/243-(1218245/486)c+(251888/81)c^2,\quad \mu_*=-3L/8,\\
G_m=G_*-3L^2/16
 =340367352475/839808+(808137564635/419904)c
                              -(1052841914857/419904)c^2.
\end{gathered}                                                     \tag{1}
\]

Exact rational bounds in the physical cubic field give
\(H,\kappa>0\), \(L<0\), \(8<\mu_*<16\), and \(G_m<G_*<0\).
The comparison polynomial is

\[
\begin{gathered}
M_3(\eta)=8+C\eta+B_*\eta^2+T_*\eta^3,\quad C=8/3+y,\\
B_*=2311/108+(4934/27)c-(1976/9)c^2,\\
T_*=-60800959/17496-(307083769/17496)c+(10980067/486)c^2.
\end{gathered}                                                     \tag{2}
\]

**Construction theorem.** For every fixed \(M,T\ge0\), the literal
family of Section2 with

\[
\tau(M,T)=8+13M+2M^2+(2+M)T^2                              \tag{3}
\]

has all nine originals simple and strictly in the disk for every
\(|\mu|\le M,|t|\le T\) on a common sufficiently small positive collar.
For \(0\le\mu\le M\), the smaller choice
\(\tau_M=8+13M+2M^2\) works on every fixed compact \(t\) interval.
The collar may depend on that interval; no unbounded-parameter uniformity
or effective value is claimed. Uniformly on each stated box,

\[
\begin{split}
F={}&M_3+[G_m+(4/3)(\mu-\mu_*)^2+(\kappa/H)t^2]\eta^4\\
 &+[f_5(\mu)+(P_0+P_1\mu)t^2+8\tau]\eta^5+O(\eta^6),
\end{split}                                                       \tag{4}
\]

where \(f_5\) is the credited real-only quadratic, specified in Section5,
and the new mixed constants are

\[
P_0=134807893/18289152+(57634811/4064256)c
 +(159762149/18289152)c^2>0,
\]
\[
P_1=241/1764+(331/882)c+(233/882)c^2>0.                    \tag{5}
\]

Write \(\ell=\sqrt{-HG_m/\kappa}\) and
\(\ell_*=\sqrt{-HG_*/\kappa}\); then \(\ell>\ell_*>0\).
For \(\mu=\mu_*\), \(\tau=728\), there are actual opposite central
equality branches \(F=M_3\) with

\[
\lambda_+(\eta)=\eta^{-2}\sum(\operatorname{Im}\zeta)^3
 =\ell\sqrt\eta+\ell\Lambda_{16}\eta^{3/2}+O(\eta^{5/2}),
\quad -14<\Lambda_{16}<-13.                              \tag{6}
\]

The complete constructed cap has a limiting ellipse and improved attained
leading skew and original-motion constants as proved in Section7. The
specific coefficient in(6) is for the central equality construction only;
it is not a maximum over the whole constructed cap or over all polynomials.

## 2. Entire literal family and mixed odd repairs

For real \(\mu,t\), let \(r=t\epsilon/(3H)\). Define

\[
\begin{aligned}
m(r)&=m_0+[35/81-(2086/81)c+(616/27)c^2]r^2,\\
b(r)&=b_0+[14537/1512-(3889/756)c-(1661/756)c^2]r^2
                       -2(1+c)^2r^4/49,\\
\nu(r)&=[-17983/972-(25711/486)c+(4564/81)c^2]r
                       +[28/81+(56/81)c]r^3,\\
\sigma(r)&=[-1967/81+(5479/432)c-(5375/162)c^2]r
                       +[-55/189+(11/63)c+(88/189)c^2]r^3,\\
\nu_4&=-2424695/13122-(136157/4374)c+(144046/6561)c^2,\\
\sigma_4&=-536333191/1119744-(805399537/559872)c
                                      +(891296017/559872)c^2,\\
q_1&=\Gamma-4r^2/(3H),\qquad v_2=3kHr/7.
\end{aligned}                                                     \tag{7}
\]

The credited shrinking family, with its old common real \(\epsilon^9\)
step omitted, is

\[
\begin{aligned}
A_0&=(u_z-ir/3)\epsilon^2+(w_2+iv_2)\epsilon^4
 +(m(r)+i\nu(r))\epsilon^6+(M_*+i\nu_4r)\epsilon^8,\\
B_0&=(u_p+ir)\epsilon^2+(w_2+iv_2)\epsilon^4
 +(m(r)+i\nu(r))\epsilon^6+(M_*+i\nu_4r)\epsilon^8,\\
K_0&=i[1+q_1\epsilon^2+b(r)\epsilon^4+\beta_*\epsilon^6]
 +(3k+\rho)r\epsilon^2+\sigma(r)\epsilon^4+\sigma_4r\epsilon^6.
\end{aligned}                                                     \tag{8}
\]

The entire new finite family is

\[
\begin{aligned}
A&=A_0-\mu\epsilon^4/3+a_3\mu\epsilon^6+a_4\mu\epsilon^8
                           +in_9\mu t\epsilon^9+\tau\epsilon^{10},\\
B&=B_0+\mu\epsilon^4+a_3\mu\epsilon^6+a_4\mu\epsilon^8
                           +in_9\mu t\epsilon^9+\tau\epsilon^{10},\\
K&=K_0+ib_2\mu\epsilon^4+s_7\mu t\epsilon^5
                 +i(b_3\mu+b_{3q}\mu^2)\epsilon^6+s_9\mu t\epsilon^7,
\end{aligned}                                                     \tag{9}
\]

where

\[
\begin{gathered}
a_3=56(c-c^2)/9,\quad b_2=1/2+2c,\\
a_4=-51583/972-(175385/486)c+448c^2,\\
b_3=1771/324-(94039/1296)c+(12347/162)c^2,\quad b_{3q}=2(1+c)/7,\\
s_7=-2(1+c)^2/49,\quad n_9=-35/81-(29/27)c-(34/81)c^2,\\
s_9=-34849/42336-(41053/21168)c-(3265/2646)c^2.
\end{gathered}                                                     \tag{10}
\]

No further coefficient is suppressed after substituting for \(r\):
all terms of(8) then have degree at most nine. Define

\[
p'(z)=9(z-A)^6[(z-B)^2-(H/2)\epsilon^2K^2],\qquad
p(z)=\int_{1-\epsilon^2}^z p'(w)\,dw.                    \tag{11}
\]

This is monic degree nine with the exact marked original \(a\).
Its eight critical slots are six copies of \(A\) and
\(B\pm\sqrt{H/2}\epsilon K\). The root and multiplicity hypotheses
will follow from individual original normals, not from a presumed converse.

At odd degree \(q=7\) or9, a common imaginary center increment
\(i\delta n\epsilon^q\) and real scale increment
\(\delta s\epsilon^{q-2}\) have entire leading primitive column

\[
9i\delta n(1-z^8)+(9iH/7)\delta s(1-z^7),                \tag{12}
\]

and label-wise half-normal column
\(\sin(2\pi j/9)\delta n+(H/7)\sin(4\pi j/9)\delta s\).
Both primitive columns and all nine individual normal columns at both
orders are recomposed from(11) and checked in the source. At labels3,4,
dividing by the nonzero first sine gives row determinant
\(-H(2c-1)/7\ne0\). The full seventh solve is
\((\delta n,\delta s)=(0,s_7\mu t)\). After recomposition, the ninth
solve is \((n_9\mu t,s_9\mu t)\). These increments are verified by
the complete original root equations and the vanishing of all four
active normals through degree nine. No pair average replaces a constraint.
The explicit coefficients in(10) suffice; uniqueness refers to these
two repair channels at their stated order, not to arbitrary competitors.

## 3. Entire tenth forcing and its new favorable sign

Let \(\omega=e^{2\pi i/9}\), \(Z_j(0)=\omega^j\),
\(N_j=(|Z_j|^2-1)/2\), and \(A_j=1-\cos(2\pi j/9)\).
At \(\tau=0\), every coefficient of \(N_j\) through degree nine
vanishes for each \(j=3,4,5,6\). The five inactive leading normals are

\[
N_0=-\epsilon^2+O(\epsilon^4),\quad
N_1,N_8=-\frac{2+4c-4c^2}{3}\epsilon^2+O(\epsilon^4),
\]
\[
N_2,N_7=-\frac{(2c-1)^2}{3}\epsilon^2+O(\epsilon^4).      \tag{13}
\]

The complete new active tenth coefficient is

\[
q_j(\mu,t)=q_j(\mu,0)-(a_j+b_j\mu)t^2.                 \tag{14}
\]

The full unaveraged calculation cancels the possible \(t^4\) term,
and only afterwards checks \(q_3=q_6\), \(q_4=q_5\). The new terms are

\[
\begin{aligned}
a_3=a_6&=21588995/28449792+(86382659/170698752)c
                                   +(44717485/85349376)c^2,\\
b_3=b_6&=83/8232+(137/4116)c+(109/4116)c^2,\\
a_4=a_5&=90414379/146313216+(216408443/256048128)c
                                   +(65443465/256048128)c^2,\\
b_4=b_5&=391/24696+(557/24696)c+(41/12348)c^2.
\end{aligned}                                                     \tag{15}
\]

The symbols in(15) are tenth-normal coefficients, distinct from the repair
symbols in(10). All are positive, with \(a_j/A_j<2\), \(b_j/A_j<1\).
Each full zero-skew ratio is the written10288 quadratic
\(r_{j0}+r_{j1}\mu+r_{j2}\mu^2\). Its complete cubic-field triples
are freshly compared in `calculation.documentary_real_baseline` with that
published prior, and rational bounds give \(|r_{j0}|<7\),
\(|r_{j1}|<13\), \(|r_{j2}|<2\). These zero-skew facts are not new.

For any sign of \(\mu\) in the box, (14) implies
\(q_j/A_j\le7+13M+2M^2+(2+M)T^2=\tau(M,T)-1\).
For \(\mu\ge0\), its new term is nonpositive and
\(q_j/A_j\le\tau_M-1\). Thus shrinking skew needs no additional
tenth inward budget on the nonnegative mean range containing \(\mu_*\).

A common real \(\tau\epsilon^{10}\) center increment has entire
primitive column \(9\tau(1-z^8)\), original response
\(\tau(1-\omega^j)\), and half-normal response \(-A_j\tau\).
At \(\tau=0,1\), the source freshly reconstructs all nine originals,
all normals, the literal and all-eight-moment Newton primitives, and both
physical scalar routes. It checks every full response vector, including
all eight moment responses. Linearity at order ten for arbitrary real
\(\tau\) follows because interactions with any lower perturbation
begin above degree ten; center interactions begin at12 and its square at20.
Thus every repaired active tenth coefficient is at most \(-A_j<0\).
Here \(A_3=A_6=3/2\) and \(A_4=A_5=1+c\).

## 4. Actual containment and complete physical scalar

For each fixed parameter box, the coefficients in(11) are polynomial in
\(\epsilon,\mu,t\) and tend uniformly to \(z^9-1\). Its nine
limiting roots are simple. Choose disjoint neighborhoods of those roots;
the complex implicit function theorem and a finite cover of the parameter
box give nine jointly analytic branches on a common collar. Uniqueness
glues them, and they remain distinct and exhaust degree nine. Uniform
Taylor bounds follow on a slightly smaller collar.

For active labels the repaired normal is
\(N_j\le-A_j\epsilon^{10}+O(\epsilon^{11})<0\) on a smaller
common positive collar. Each other label has the strictly negative
leading coefficient in(13). Hence every original is strictly contained.
The marked branch is exactly \(1-\epsilon^2\), by the anchor and
local uniqueness. The split critical scale tends to \(i\), so the two
pair slots are distinct, and all eight marked-root distances tend uniformly
to one. These IFT, remainder and census bridges are ordinary unformalized
analysis; no effective numerical collar is inferred from the finite jets.

For the actual scalar set

\[
V_A=|a-A|^2,\quad V_B=|a-B|^2+(H/2)\epsilon^2|K|^2,
\quad X=2\sqrt{H/2}\epsilon\operatorname{Re}[(a-B)\overline K].
\]

Then exactly

\[
F=6V_A^{-1/2}+(V_B+X)^{-1/2}+(V_B-X)^{-1/2}.             \tag{16}
\]

The two variances minus one begin at degree two and \(X^2\) at degree
eight. Through degree eleven the pair contribution is
\(2V_B^{-1/2}+(3/4)X^2[1-(5/2)(V_B-1)]\). The inverse-square-root
expansion retains the fifth binomial coefficient \(-63/256\).
Both that term and the linear pair variance correction are essential.

The separate route solves whole positive-branch equations
\(V_A U^2=1\), \((V_B^2-X^2)R^2=1\),
\(S^2=2V_B R^2+2R\), with \(U(0)=R(0)=1\), \(S(0)=2\).
Coefficient recursions use no binomial coefficients. Their whole equations
and agreement with(16) are checked before digesting any vector. They are
two routes in the same author's arithmetic, not independent review.

The entire literal family has \(A(-\epsilon)=\overline A\), similarly
for \(B\), and \(K(-\epsilon)=-\overline K\). The real tenth
increment preserves these identities for any \(\tau\). Thus reversing
\(\epsilon\) conjugates the critical multiset and leaves the exact
scalar invariant. Positive scalar branches are real analytic near zero,
so \(F\) is even in \(\epsilon\) and analytic in \(\eta\).
Reversing \(t\) also conjugates the multiset: \(F\) is even in \(t\),
and the actual cubic imaginary moment is odd. The source checks every
literal coefficient of both symmetries. Individual original branches
and their normals may have odd coefficients.

## 5. Full cost and attribution of the real-only fifth polynomial

Direct substitution of(9) into(16), retaining every bivariate coefficient,
gives the fourth coefficient
\(G_*+L\mu+(4/3)\mu^2+(\kappa/H)t^2\).
Completing the square with \(\mu_*=-3L/8\) gives(4).
There is no mixed fourth term after the actual odd repairs have been paid.
The entire fifth coefficient at \(\tau=0\) is
\(f_5(\mu)+(P_0+P_1\mu)t^2\); all other monomials cancel.
Both scalar routes give common tenth cost response8.

For precision write \(f_5=\gamma_0+\gamma_1\mu+\gamma_2\mu^2\).
The following complete coefficients are reproduced from the written
real-only10288 and are expressly credited prior art:

\[
\begin{aligned}
\gamma_0&=46162779724939271/69657034752
 +(36338752485008003/11609505792)c
 -(11846579474774765/2902376448)c^2,\\
\gamma_1&=932974693/279936+(6209560805/279936)c
 -(1933889279/69984)c^2,\\
\gamma_2&=-809/54-(3545/54)c+(166/3)c^2.
\end{aligned}                                                     \tag{17}
\]

The real-only tenth ratios and the central real-only fifth substitution
are also compared in their entirety. This validates useful prior formulas;
novelty is claimed only for the mixed actual repair, favorable mixed normal
sign, mixed fifth terms, and the resulting constructed skew/motion gain.
Neither(3) nor its nonnegative improvement is a sharp fifth optimization.
The even scalar identity makes the uniform remainder in(4) \(O(\eta^6)\).

## 6. Attained central equality branch

Take \(\mu=\mu_*\), \(M=16\), \(\tau_{16}=728\), and any fixed
\(T>\ell\). The nonnegative-mean bound proves actual containment.
After dividing \(F-M_3\) by \(\eta^4\), its analytic extension at
zero is \(G_m+(\kappa/H)t^2\). At \(t=\ell\), its derivative in
\(t\) is \(2\kappa\ell/H>0\). The ordinary real IFT gives an
actual positive branch with exact \(F=M_3\) and

\[
t(\eta)=\ell-\frac{HJ_{16}}{2\kappa\ell}\eta+O(\eta^2),\quad
J_{16}=f_5(\mu_*)+(P_0+P_1\mu_*)\ell^2+5824.             \tag{18}
\]

The opposite branch is its \(t\)-reflection. The critical slots themselves
give, counting multiplicities,

\[
\sum(\operatorname{Im}\zeta)^3
 =6(\Im A)^3+2(\Im B)^3+3H\epsilon^2(\Im B)(\Im K)^2
 =t\epsilon^5+U_7t\epsilon^7+O(\epsilon^9),
\]
\[
U_7=2\Gamma+3Hk/7=-17/54+(3535/108)c-(844/27)c^2.         \tag{19}
\]

Conjugation parity and analyticity justify the stated odd remainder.
Dividing by \(\eta^2\) and substituting(18) gives(6), with
\(\Lambda_{16}=U_7+J_{16}/(2G_m)\). Whole field reduction and
strict rational bounds give \(7426<J_{16}<7427\) and
\(-14<\Lambda_{16}<-13\). No order-\(\eta\) skew loss remains.
These are attained central expansions with actual containment, not claims
of universal optimality or finite-\(\eta\) extremality.

## 7. Constructed cap and original-motion gain

For \(q=\sqrt{4/3}(\mu-\mu_*)\), \(s=\sqrt{\kappa/H}t\),
\(r^2=q^2+s^2\), fix any radius \(R>r_0=\sqrt{-G_m}\).
Choose fixed \(M,T\) containing this entire coordinate ball and use(3).
Uniformly with parameter derivatives on the ball,

\[
E(\eta,\mu,t)=\frac{F-M_3}{\eta^4}=G_m+r^2+O(\eta).
\]

Choose \(0<\delta<r_0\). For small \(\eta\), \(E<0\) on
\(r\le\delta\); on \(\delta\le r\le R\), its radial derivative
is \(2r+O(\eta)>0\) and its value at \(R\) is positive.
Each ray has exactly one analytic zero \(r_\eta(\phi)=r_0+O(\eta)\),
uniform in angle. The entire exact constructed cap in this ball is
\(0\le r\le r_\eta(\phi)\), with no other components.
It is connected, compact and symmetric in \(t\). Its continuous actual
skew image is therefore a symmetric interval with positive endpoint
\(\ell\sqrt\eta+O(\eta^{3/2})\), matched by central equality
points for the chosen \(\tau\). This leading statement does not require
those points to maximize the whole cap at nonzero \(\eta\).

For all nine canonical labels put
\(L_j=-\omega^j/3-x-y\omega^{-j}\). The complete root jets give

\[
Z_j=\omega^j+\epsilon^2L_j+\epsilon^4d_j
                          +i\epsilon^5tW_j+O(\epsilon^6),
\quad W_j=\frac{(3+4c)\omega^j-(1+2c)(1+\omega^{-j})-\omega^{-2j}}{18}.
                                                                  \tag{20}
\]

Every \(d_j\) is independent of \(\mu,t\). Equivalently, if \(P_2,P_4\)
are the corresponding columns of the literal primitive(11), then
\(d_j=-[P_4(\omega^j)+P'_2(\omega^j)L_j+36\omega^{7j}L_j^2]/
(9\omega^{8j})\). The root equations check all these jets, including
the absent first and third coefficients; no scalar motion shortcut is used.
The new inward term starts at degree ten and leaves them unchanged.

The entire ideal norms are
\(|d_7+iuW_7|^2=\mathcal A+\mathcal Bu+\mathcal Qu^2\),
\(|d_2+iuW_2|^2=\mathcal A-\mathcal Bu+\mathcal Qu^2\), where

\[
\mathcal A=(-13638695-64046452c+83604476c^2)/972>0,
\quad\mathcal B=\sin(\pi/9)(1448+6982c-8224c^2)/243>0,
\]
\[
\mathcal Q=(8+25c+20c^2)/162>0.
\]

All seven other zero-skew norms have a strict gap below \(\mathcal A\),
verified by exact rational bounds. For the central positive equality
branch, \(u=\epsilon t=\ell\epsilon+O(\epsilon^3)\).
The gap excludes the other seven labels, and the difference between7 and2
is \(2\mathcal B\ell\epsilon+O(\epsilon^2)>0\).
Therefore for \(R_\eta=\max_j\eta^{-2}|Z_j-\omega^j-\eta L_j|\),

\[
R_\eta=\sqrt{\mathcal A}+
 \frac{\mathcal B\ell}{2\sqrt{\mathcal A}}\sqrt\eta+O(\eta).
                                                                  \tag{21}
\]

Label7 wins at the positive branch and2 at the negative. On the whole
stated constructed cap, \(|t|\le\ell+O(\eta)\), and(20) gives the
matching upper expansion(21) to \(O(\eta)\). Its maximum exists by
compactness. Since \(\ell>\ell_*\), the attained skew coefficient
and the motion correction are strictly larger than those of10212.
These provide lower examples for any maximum over all actual competitors;
neither coefficient is claimed universally optimal.

## 8. Exact computation and trust boundary

`arithmetic.py` is unchanged credited same-author arithmetic. The local
`series.py` is the same exact series engine of10280; `constants.py` retains
its constants without importing its old research program. `family.py`
specifies the entire family, while `calculation.py` reconstructs literal
primitive, all eight Newton moments, all nine original root/normal jets,
the physical scalar through degree eleven, the odd columns, rational
signs, tenth responses and the central substitution.

The field is \(\mathbb Q(\omega)[i]\), with six exact rational coordinates
per \(\mathbb Q(\omega)\) component and \(\omega^6+\omega^3+1=0\).
Exponent \(32u+v\) stores \(\mu^ut^v\). Every input \(t\) factor
costs at least one \(\epsilon\) degree; products, root recursions and
constant field inversions preserve \(v\le\epsilon\)-degree. Every
retained degree is at most11, less than32, so the encoding is injective.
The source checks the full grading, not sampled parameter values.

Physical signs use rational bisection in the unique cosine bracket and
rational interval evaluation of whole reduced cubic polynomials. All
whole identities compare complete coefficient vectors before hashes.
The compact `EXPECTED.json` fingerprints the regenerated full records;
bulky generated records are omitted from the repository and may be saved
outside the source with `--output`. Digests are provenance checks, not
substitutes for the equations or the analytic bridges above.

The standalone verifier seals all declared local source files before mathematical imports,
validates exact JSON schemas and checks local import origins. Explicit
runtime guards remain active under Python `-O`. `validate.py` replays
normal/optimized and cold source-only runs, compares complete generated
records, and rejects specified mathematical/source/schema defects under
the unchanged one-child, native-threads-one,45-second per-child guard.
The IFT, Taylor, compactness, parity and cap arguments remain unformalized.
No numerical search, sampling, timeout, resource failure or hash alone is
a mathematical nonexistence premise. The full all-mode fourth normal/cost
reduction and the global first-power inequality remain open.
