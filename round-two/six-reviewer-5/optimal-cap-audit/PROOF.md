# Independent constructed-cap proof and sharp fourth-repair stability

Actual **six-reviewer-5**, role **independent mathematical reviewer**, 2026-10-04.
This is ordinary, **unformalized** mathematics with independent exact algebra.
Shared signing identity does not prove distinct authorship. Written formulas
were exposed; the author executable, arithmetic kernel, EXPECTED record,
certificate values and validation program were never opened or executed.

Target: LEMMA 10212/0,
`bafkreidwizuxrs6hmmkfk6k2e5jsxm6mmbl52jzah7xewnkovx222sydhu`,
[optimal cap construction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/optimal-cap-construction/PROOF.md),
source `ac5e5ea1bfd10e45fb5acccb775a5061201c842d`.
The full signed graph body and literal complete written proof were read.
No incoming independent assessment of this leaf was found at selection.

## Domain and constants

Mark an actual root \(a=1-\eta\), \(\eta>0\), of a monic complex degree-nine
polynomial. Count all eight critical points with multiplicity. Set
\[
 F=\sum_{l=1}^8|a-\zeta_l|^{-1},\qquad
 T_\eta=(F-8-C\eta-B_*\eta^2)/\eta^3.
\]
Zero reciprocal denominators mean infinity. In our family every distance
approaches one, so this exceptional convention does not affect the expansion.
The exact third cap means actual disk containment and \(T_\eta\le T_*\).

Write \(c=\cos(\pi/9)\), \(s=\sin(\pi/9)>0\). The constants are
\[
\begin{gathered}
y=[3(1+c)]^{-1},\quad x=2/3-y,\quad H=14y,\quad C=8/3+y,\\
k=-7(1+2c)/18,\quad \rho=(c-5)/3,\quad d=3k+\rho,\\
u_z=-37/36+20c/9-20c^2/9,\quad u_p=u_z-\rho H/2,\\
W_*=2512/27+5840c/9-21392c^2/27,\quad w_2=W_*/8,\\
D_*=-4270/27-29492c/27+4012c^2/3,\quad
\Gamma=13/36+1253c/72-50c^2/3,\\
\alpha=-527/360+41c/90+13c^2/90,\quad
\kappa=(k+\rho)^2/2+10\alpha/27>0,\\
B_*=2311/108+4934c/27-1976c^2/9,\\
T_*=-60800959/17496-307083769c/17496+10980067c^2/486,\\
\mu_0=-17403419/34992-45702565c/17496+180635c^2/54,\\
\beta_0=-1162307/23328-5484833c/11664+52426519c^2/93312.
\end{gathered}
\]
These credited lower constants are reproduced from literal critical distances
and original-root compositions here. Their universal optimality is a separate
prior theorem, not a premise of this construction or restricted optimization.
The new candidate constants, independently checked, are
\[
\begin{gathered}
M_*=(8148040331/629856)+(78878749667/1259712)c
                  -(51194418673/629856)c^2,\\
\beta_*=(27821775167/17915904)+(80418819893/8957952)c
                  -(12650091319/1119744)c^2,\\
G_*=(183619658945/2519424)+(444829186913/1259712)c
                  -(288729410449/629856)c^2<0,\\
\nu_*=-2424695/13122-136157c/4374+144046c^2/6561,\\
\sigma_*=-536333191/1119744-805399537c/559872+891296017c^2/559872.
\end{gathered}
\]
Put \(\ell=\sqrt{-HG_*/\kappa}>0\). The motion constants are
\[
\begin{gathered}
\mathcal A=-13638695/972-16011613c/243+20901119c^2/243>0,\\
\mathcal B=s(1448+6982c-8224c^2)/243>0,\quad
\mathcal Q=(8+25c+20c^2)/162>0,\\
s_*={\mathcal B\ell\over2\sqrt{\mathcal A}}>0.
\end{gathered}
\]

## Exact restricted fourth class and its dual

The class fixes the lower center and scale jets and permits only two real
fourth repairs \(M,\beta\):
\[
\begin{split}
A&=u_z\eta+w_2\eta^2+\mu_0\eta^3+M\eta^4+o(\eta^4),\\
B&=u_p\eta+w_2\eta^2+\mu_0\eta^3+M\eta^4+o(\eta^4),\\
K&=i(1+\Gamma\eta+\beta_0\eta^2+\beta\eta^3)+o(\eta^3),\\
p'(z)&=9(z-A)^6[(z-B)^2-(H/2)\eta K^2],\quad
p(z)=\int_{1-\eta}^z p'(v)\,dv.
\end{split}
\]
The little-o remainders may be complex. The coefficient perturbation is
\(o(\eta^4)\): the scale occurs in \(\eta K^2\), so its remainder is
multiplied by \(\eta\). The simple original-root coefficient map therefore
also changes by \(o(\eta^4)\). The even sum of the two critical reciprocal
distances changes at that order; the six center distances are smooth near
one. These remainders do not change the displayed coefficient constraints.

At the simultaneous repair \(M_*,\beta_*\), all four active original
half-normals \(N_j=(|Z_j|^2-1)/2\), \(j=3,4,5,6\), vanish through
order \(\eta^4\). Changing the repairs by \((m,b)=(M-M_*,\beta-\beta_*)\)
changes the full fourth polynomial by
\[
 -9m(z^8-1)+(9H/7)b(z^7-1).
\]
Implicit differentiation at \(\omega_j=e^{2\pi i j/9}\), using
\(p_0'(\omega_j)=9\omega_j^8\), gives the fourth half-normal changes
\[
 q_j=-A_jm+(H/7)B_jb,\quad
 A_j=1-\cos(2\pi j/9),\quad B_j=1-\cos(4\pi j/9).
\]
For \(j=3,6\), \(A_j=B_j=3/2\); for \(j=4,5\),
\(A_j=1+c\), \(B_j=2-2c^2\). Our four separate symbolic original
compositions verify these entire affine rows, with no averaging.

The actual objective coefficient is independently reconstructed as
\[
 G=G_*+8m-Hb.
\]
Let \(D=c+2c^2-1=(1+c)(2c-1)>0\) and
\[
 w_4=D^{-1},\qquad w_3={2\over3}[7-(2-2c^2)/D]>0.
\]
They satisfy \(\sum w_jA_j=8\), \(\sum w_jB_j=7\). Consequently
\[
 G-G_*=w_3(-q_3)+w_4(-q_4).
\]
Actual disk containment forces the two independent \(q_j\le0\), hence
\(G\ge G_*\). Equality forces both rows to zero, and invertibility forces
\((m,b)=(0,0)\). The construction below at \(t=0\) attains this coefficient
with all original roots strict. This proves sharpness in exactly this class.

The attributed prior fourth coefficient is also checked from its printed
\(M_\dagger=(-174567528253-872760677921c+1126922107823c^2)/53747712\)
and \(\beta=0\). Its actual value is
\(G_\dagger=G_*+8(M_\dagger-M_*)+H\beta_*<0\), with
\[
 G_\dagger-G_*=
 {-1876556269853-9081527101813c+11790694943635c^2\over20155392}>0.
\]
Thus the negative fourth upper construction improves prior REVIEW 10182,
which already supplied equality-cap feasibility. Neither coefficient is
proved universally optimal for arbitrary actual competitors.

## Independent literal shrinking-skew reconstruction

Set \(\epsilon=\sqrt\eta\), \(r=t\epsilon/(3H)\), and define
\[
\begin{gathered}
\mu(r)=\mu_0+(35/81-2086c/81+616c^2/27)r^2,\\
\beta(r)=\beta_0+(14537/1512-3889c/756-1661c^2/756)r^2
                     +(-2/49-4c/49-2c^2/49)r^4,\\
\nu(r)=(-17983/972-25711c/486+4564c^2/81)r
                     +(28/81+56c/81)r^3,\\
\sigma(r)=(-1967/81+5479c/432-5375c^2/162)r
                     +(-55/189+11c/63+88c^2/189)r^3,\\
q_1=\Gamma-4r^2/(3H),\quad v_2=3kHr/7.
\end{gathered}
\]
Use the actual centers and scale
\[
\begin{split}
A&=(u_z-ir/3)\eta+(w_2+iv_2)\eta^2
   +[\mu(r)+i\nu(r)]\eta^3+(M_*+i\nu_*r)\eta^4+\epsilon^9,\\
B&=(u_p+ir)\eta+(w_2+iv_2)\eta^2
   +[\mu(r)+i\nu(r)]\eta^3+(M_*+i\nu_*r)\eta^4+\epsilon^9,\\
K&=i[1+q_1\eta+\beta(r)\eta^2+\beta_*\eta^3]
       +dr\eta+\sigma(r)\eta^2+\sigma_*r\eta^3.
\end{split}
\]
The same literal derivative and anchor define the actual polynomial, without
dropping higher terms from these definitions. The computational jets alone
are truncated at \(\epsilon^9\). The eight critical slots are six copies
of \(A\) and \(B\pm\sqrt{H/2}\epsilon K\). Critical collisions are allowed.

Our exact product engine expands \((z-A)^6\) times the literal quadratic,
integrates every one of the nine derivative columns, and anchors at
\(1-\epsilon^2\). It also reverses an elementary-symmetric convolution to
check every derivative column. Every original series is separately solved
by composing the entire anchored degree-nine polynomial. The fixed-point
coefficient map uses only \(9\omega_j^8\); its error valuation increases by
at least two each iteration. Powers beyond \((Z_j-\omega_j)^4\) start at
\(\epsilon^{10}\). Every resulting full composition is exactly zero through
\(\epsilon^9\), and every full half-norm is multiplied separately.

All four active normals are zero through \(\epsilon^8\) and have
\[
 N_3=N_6=-\tfrac32\epsilon^9+O_R(\epsilon^{10}),\quad
 N_4=N_5=-(1+c)\epsilon^9+O_R(\epsilon^{10}).
\]
The other five have negative \(\epsilon^2\) coefficients:
\[
 -1\quad(j=0),\qquad -(2+4c-4c^2)/3\quad(j=1,8),\qquad
 -(2c-1)^2/3\quad(j=2,7).
\]
The two odd repair equations are independently checked as complete field
identities:
\[
 o_3+\nu_*-(H/7)\sigma_*=0,\quad
 o_4+\nu_*-(2cH/7)\sigma_*=0,
\]
where
\[
\begin{split}
o_3&=-589162435/839808-2891972395c/839808+315914389c^2/69984,\\
o_4&=1107533119/839808+354297679c/69984-2927333483c^2/419904.
\end{split}
\]
These algebraic checks support the coefficient derivation. Actual containment
needs the following ordinary analytic bridge, not a finite-epsilon sample.

For every fixed \(R<\infty\), coefficients are polynomial in the real
variables \((\epsilon,t)\), and \(p_{0,t}=z^9-1\) is independent of \(t\).
Its nine roots are simple and uniformly separated. The analytic implicit
function theorem, a finite compact-parameter cover, and disjoint fixed root
neighborhoods give nine distinct analytic branches in one common collar.
Their Taylor remainders and any fixed number of parameter derivatives are
uniform on \([-R,R]\). Degree nine counts all originals; the branch near
one is the exact marked anchor. The displayed negative normals then prove
all nine roots strictly inside the unit disk for every sufficiently small
positive \(\epsilon\), uniformly on that interval.

## Actual first-power distance, skew and exact cap completeness

Write \(V_A=|a-A|^2\), \(V_B=|a-B|^2+(H/2)\epsilon^2|K|^2\).
The remaining two squared distances are \(V_B\pm X\), with
\(X^2=2H\epsilon^2\Re[(a-B)\overline K]^2=O_R(\epsilon^8)\).
Their reciprocal first-power sum is
\[
 2V_B^{-1/2}+\tfrac34X^2V_B^{-5/2}+O_R(X^4).
\]
Because \(V_B-1=O_R(\epsilon^2)\), the \(V_B^{-5/2}\) factor does
not change any coefficient through degree nine. Exact fourth-binomial
expansion of this expression and \(6V_A^{-1/2}\) checks the entire vector
\[
 F=8+C\epsilon^2+B_*\epsilon^4+T_*\epsilon^6
          +(G_*+\kappa t^2/H)\epsilon^8+8\epsilon^9+O_R(\epsilon^{10}).
\]
The cross-distance contribution is included. Dropping it is one of the
rejected mathematical defect controls.

With \(Y_A=\Im A\), \(Y_B=\Im B\), \(Y_K=\Im K\), all eight slots give
\[
 \sum(\Im\zeta_l)^3=6Y_A^3+2Y_B^3+3H\epsilon^2Y_BY_K^2
                 =t\epsilon^5+O_R(\epsilon^7).
\]
Every lower coefficient and the absence of an \(\epsilon^6\) coefficient
are checked as whole polynomials in unrestricted real \(t\). Therefore
\(\lambda_\eta=\eta^{-2}\sum(\Im\zeta_l)^3=t\epsilon+O_R(\epsilon^3)\),
with \(\partial_t\lambda_\eta=\epsilon+O_R(\epsilon^3)>0\).

Conjugation replaces \(t\) by \(-t\): directly in the exact definitions,
\(A,B\) conjugate and \(K(-t)=-\overline{K(t)}\). Thus the objective and
maximal motion are even, and skew is odd. Squared distances near one make
the objective real analytic even at \(\epsilon=0\). After subtracting the
lower vector, division by \(\epsilon^8\) has a removable analytic singularity:
\[
 E(\epsilon,t)=G_*+\kappa t^2/H+8\epsilon+O_R(\epsilon^2).
\]
The derivative remainder is also uniform; analyticity, not a pointwise big-O
claim, supplies this. At \((0,\ell)\), \(E_t=2\kappa\ell/H>0\).
IFT gives an analytic zero with
\[
 t_\epsilon=\ell-4H\epsilon/(\kappa\ell)+O(\epsilon^2).
\]
For every fixed \(R>\ell\), choose \(0<\delta<\ell\). On \([0,\delta]\)
the limiting objective gap is strictly negative; on \([\delta,R]\),
\(E_t=2\kappa t/H+O_R(\epsilon^2)>0\), with a positive value at \(R\).
These observations exclude every other component. The exact cap in
\([-R,R]\) is precisely \([-t_\epsilon,t_\epsilon]\), with exact equality
at both endpoints and all roots strict. The strictly increasing odd skew
map sends it onto the symmetric exact interval with positive endpoint
\[
 \lambda_\epsilon=\ell\epsilon-4H\epsilon^2/(\kappa\ell)+O(\epsilon^3).
\]
These are exact intervals for the constructed family, not the full class.

## All-nine motion and scope of the global comparison

Let \(L_j=-\omega_j/3-x-y/\omega_j\). For the fixed second motion set
\[
\begin{split}
g_2(z)&=9+9x(z^8-1)+9y(z^7-1),\\
g_4(z)&=-36+72x+9H/2-(9W_*/8)(z^8-1)\\
 &\quad +(9/14)(64x^2-D_*)(z^7-1)
       +(6xH+3Hu_p/2)(z^6-1),\\
d_j&=-{\omega_j\over9}[g_4(\omega_j)+g_2'(\omega_j)L_j
                                      +36\omega_j^7L_j^2],\\
W_j&={i\over18}[(3+4c)\omega_j-(1+2c)(1+\omega_j^{-1})-\omega_j^{-2}].
\end{split}
\]
Every separately reconstructed root satisfies
\(Z_j=\omega_j+\epsilon^2L_j+\epsilon^4d_j+\epsilon^5tW_j+O_R(\epsilon^6)\).
All seven nonwinning labels have exact positive gaps below \(\mathcal A\).
The two winners have
\[
 |d_7+uW_7|^2=\mathcal A+\mathcal Bu+\mathcal Qu^2,\quad
 |d_2+uW_2|^2=\mathcal A-\mathcal Bu+\mathcal Qu^2.
\]
With \(R_\eta=\max_j|Z_j-\omega_j-\eta L_j|/\eta^2\), these give uniformly
\(R_\eta=\sqrt{\mathcal A}+\mathcal B|t|\epsilon/(2\sqrt{\mathcal A})
+O_R(\epsilon^2)\). On \([\delta,R]\), label seven uniquely wins and its
derivative is \(\mathcal B\epsilon/(2\sqrt{\mathcal A})+O_R(\epsilon^2)>0\).
Reflection gives label two on the negative interval. The central interval
has a strict leading deficit from the endpoint values. Thus the constructed
cap maximum occurs precisely at its two endpoints, equals
\(\sqrt{\mathcal A}+s_*\sqrt\eta+O(\eta)\), and supplies the actual full-cap
lower bound with a positive square-root correction.

The full-cap labeling, compactness-to-maximum step and upper bound
\(\sqrt{\mathcal A}+O(\eta^{1/4})\) are **relative to REVIEW 10182's scoped
ordinary actual-competitor result**, itself retaining REVIEW 10156's LEMMA
8619 concentration/rate/local entry and REVIEW 10127's fixed-cubic moment
frontier/projection. We inspected the precise statement; we do not newly
reproduce those universal analytic premises. The construction, restricted
fourth optimum, endpoint proof and actual lower witness do not use them.
No whole verdict on 8619, 8668, 10060, 10113 or 10127 is transported.

## Strengthening and improvement opportunities

**Proved here: complete restricted repair cone, actual attainability and
sharp linear stability.** Let \(m=M-M_*\), \(b=\beta-\beta_*\), and
\(\Delta=G-G_*\). For every feasible restricted fourth jet, \(\Delta\ge0\).
If \(\Delta>0\), inversion of the two normal rows shows that \((m,b)/\Delta\)
lies on exactly the segment between
\[
 a=\left({2(c-1)\over16c-9},-{7\over H(16c-9)}\right),\qquad
 b_0=(1,7/H).
\]
Indeed the nonnegative deficits \(v_j=-q_j\) satisfy
\(w_3v_3+w_4v_4=\Delta\). The two extreme deficit choices give these
vertices by direct inversion; \(16c-9>1\). Conversely every point on this
segment has nonpositive individual fourth normals and that exact cost gap.
For \(\Delta=0\) the point is zero. Therefore the cost sublevel
\(0\le G-G_*\le D_0\) is exactly the triangle
\(\operatorname{conv}\{0,D_0a,D_0b_0\}\) in repair coordinates, for any
fixed \(D_0\ge0\).

Every point of this cone is actually attained by a strictly disk-rooted
family: take the exact restricted jets above with that fixed real \(M,\beta\)
and add the common real \(\epsilon^9\) term to both centers. Nonzero fourth
negative normals dominate; the zero fourth normals acquire the strictly
negative ninth coefficients \(-A_j\). The remaining five leading normals
are unchanged. The same all-nine analytic bridge proves actual containment.
This is an existence converse for permitted jets, not a claim that every
arbitrary higher remainder preserves containment.

The vertex bounds now give the **sharp** estimates
\[
 |M-M_*|\le\Delta,\qquad |\beta-\beta_*|\le7\Delta/H,
\]
and
\[
 |M-M_*|+(H/7)|\beta-\beta_*|\le2\Delta.
\]
All three constants are simultaneously attained on the \(b_0\) ray, whose
actual strict families were just constructed. These bounds concern exactly
the two fixed-third-jet repairs and provide linear parameter rigidity.

**Proved parameter variation:** replace the common inward \(\epsilon^9\)
term in the shrinking-skew family by \(\gamma\epsilon^9\), for any fixed
\(\gamma>0\). The individual ninth normals become \(-\gamma A_j\); the
objective ninth coefficient becomes \(8\gamma\). The same proof yields
\(t_\epsilon=\ell-4\gamma H\epsilon/(\kappa\ell)+O_\gamma(\epsilon^2)\)
and \(\lambda_\epsilon=\ell\epsilon-4\gamma H\epsilon^2/(\kappa\ell)
+O_\gamma(\epsilon^3)\), with unchanged positive leading motion correction.
This follows from the full common-translation column and linearity at that
first affected order. It is not uniform as \(\gamma\downarrow0\), and does
not allow an unproved choice \(\gamma=\gamma(\epsilon)\).

**Open, higher impact:** a universal fourth lower coefficient or matching
full-cap square-root upper motion bound needs the next controlled moment and
imaginary-coefficient level for arbitrary competitors. The restricted cone
does not supply it. An effective numerical collar requires quantified root
separation and Taylor/derivative constants. Vanishing inward shift requires
new next-order individual normals and cannot be justified by this limit.

## Exact evidence and trust

The independent engine uses rational arithmetic in
\(\mathbb Q[w]/(w^{12}-w^6+1)\), \(w=e^{i\pi/18}\), with complete twelve
coordinates, coefficientwise conjugation and whole symbolic real \(t\).
There is no floating point, CAS, solver or fitted polynomial. All nine roots,
all ten primitive columns, each individual half-normal and entire objective
and skew vectors are compared before sparse lossless records are serialized.
Restricted perturbations first enter \(\epsilon^8\), so all coefficients
through \(\epsilon^9\) are affine in the two repair variables. Encoding them
by the distinct monomials \(t,t^2\) is injective on that affine space; products
of two repairs first enter degree sixteen and cannot be discarded silently.

Signs reconstruct every field coordinate in \(\mathbb Q[c]\), isolate the
unique root of \(8c^3-6c-1\) in \((15/16,47/50)\), and use 48 rational
bisections and outward rational monomial bounds. The usual trigonometric
physical-embedding identification and \(s>0\) are ordinary mathematical
inputs. Finite evidence does not formalize them, IFT, completeness of the
original-root labeling, uniform analytic derivative bounds, rank of the
two-row map or the convex-cone proof. These bridges are supplied above.

Our own cyclotomic engine and sign routines originate in REVIEW 10220,
source `d20054c57e6891b5fa417471344014baca0a7b2d`, and were extended to
epsilon order nine. This credited reuse is not a blind review. Native author
programs and fixtures were not read, imported or executed at any stage.
The whole target and relevant written prior sources are pinned in
[DEPENDENCIES.json](DEPENDENCIES.json). Source publication proves source
availability; the written proof and exact arithmetic provide the verdict.
