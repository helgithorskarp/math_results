# Audited joint coercivity and retained constants

Actual six-reviewer-5, independent mathematical reviewer, 2026-10-03.
This is ordinary unformalized mathematics. The precise stationary framework
7432/9496 and the primitive slice certificate 9902/9928 are explicit inputs.
The fresh defining-map and data-only certificate checks are described in
REVIEW.md; a previous input verdict does not establish this leaf.

Let the complete 9550 reconstruction be over
\(\mathbb Q[B,E,r,s,t,t^{-1}]\), with only \(t\ne0\) localized.
The heptic is
\(h=z^7-3z^5/8+Bz^4+Ez^3+F_*z^2+G_*z+J_*\),
and the mass polynomial is
\(p=p_0+p_1z+p_2z^2+rtz^3+stz^4+tz^5\).
Use the full normal-representative remainder \(\rho\) and residue adjoint
\(T\), not a derivation on the quotient. Its ODE/kernel are
\[
 O=ph''+(p'-Q)h'+(64-Q')h,\qquad
 K=-16p-\tfrac14 T^2\rho(p^2)+\tfrac14 T\rho(p(Q-p')).
\]
The fixed pivots \(24t^2,-15t^2/14,-28t\), together with the two
fixed mass pivots, determine every starred coefficient. The entire five-vector
is \(R=(tO_2,tO_1,tO_0,K_1,K_0+4)\). The script implements the complete
written recursion; all five low rows and every quotient reduction remain.

## Quantitative boundary and lawful projection

Put \(\bar R=R(0,E,r,0,t)\) and
\(E_0=-(10976r^2+7344r+1143)/2112\).
The full fourth row is \(\bar R_3=-88t(E-E_0)/7\).
At \(E_0\), the second row is \(-tP/9504\), with
\(P=4934272r^3+4606896r^2+1459368r+157599\).
The first/third rows have forms \(a_2t^2+b_2\) and
\(a_0t^2+b_0\), whose cross is \(5S/1254528\).
Fresh rational Euclid gives \(UP+VS=1\). Hence the full specialized
unit has weights
\[
 W=(-1254528Va_0/5,-9504U/t,1254528Va_2/5,0,0).
\]
For the entire difference quotients
\(\bar R_i-R_i(0,E_0,r,0,t)=(E-E_0)D_i\), set
\(Z_i=W_i\) except \(Z_3=(7/(88t))\sum_iW_iD_i\).
Full multiplication gives \(\sum_iZ_i\bar R_i=1\).
No \(a_0,a_2,r\) or unspecified slope is inverted.

The complete 45 coefficients give summed coefficient norm at most
\(N_Z=202506888\) and absolute Laurent degree 9. All fifteen
\(\partial_B R_i,\partial_E R_i,\partial_s R_i\) have norm at most
\(N_R=16583\), degree at most 9. Also
\(\|\partial_BF_*\|_1=321/140<3\), degree 2. These are whole
polynomial comparisons, not sampled parameter evaluations.

Let \(L\ge1\) bound all five parameter moduli and \(|t^{-1}|\), and
\(m=|B|+|F_*|+\|R\|_\infty\). Complex line segments changing only
\(B,s\) stay in this budget. Coefficient bounds and the unit imply
\[
 1\le N_ZN_RL^{18}(\|R\|_\infty+|B|+|s|).
\]
Define \(a=1/(2N_ZN_R)=1/6716343447408\) and
\(\sigma=aL^{-18}\). If \(m<\sigma\), then \(|s|>\sigma\).
This is the required justification for the later division by \(s\).
Let \(D=3L^2\). Changing \(B\) to zero gives
\(|F_*(0,E,r,s,t)|\le Dm\). The full \(B=0\) E-pivot is
\(-83s/60\), so
\[
 E'=E+60F_*(0,E,r,s,t)/(83s)
\]
makes \(F_*(0,E',r,s,t)=0\). If
\(m<83\sigma/(180L^2)\), the displacement is less than one.
The two complex segments to \((0,E')\) stay within the budget \(2L\).
For \(J=N_R(2L)^9\), every projected full residual is bounded by
\(2J(1+60D/(83\sigma))m\).

On this slice put \(x=s^2,u=st\). Both are nonzero, and
\(|r|,|x|\le L^2\). The five positive primitive contents have inverse
at most \(C_p=1814727936\); the prescribed multipliers are
\(s^2,s,s^2,s,s^2\). Thus
\[
 \|P\|_2\le6C_pL^2J(1+60D/(83\sigma))m.
\]
For completeness the imported minor unit is \(\sum_TU_TD_T=x\).
Its complete 72 credited coefficients, all ten determinants and fifteen
matrix entries are checked separately as data. Their bounds are
\(\sum_T\|U_T\|_1<C_U=10^{-13}\),
\(\sum_{ij}\|M_{ij}\|_1^2=Q=14913669297722925580854623\),
and degrees at most 4 and 5. Complex Cauchy--Binet gives
\(\sigma_1\sigma_2\sigma_3=(\sum_T|D_T|^2)^{1/2}\), while
\(\sigma_1\sigma_2\le\|M\|_F^2/2\). Hence
\[
 \|P\|_2\ge 2|x|\sqrt{1+|u|^2+|u|^4}/(C_UQA^{14})
 \ge2\sigma^2/(C_UQL^{28}),\quad A=L^2.
\]
Combining gives
\[
 m\ge\frac{\sigma^2}{3C_UQC_pN_R2^9L^{39}(1+60D/(83\sigma))}.
\]
Since \(L\ge1\), \(1+(180/(83a))L^{20}\le
(1+180/(83a))L^{20}\). Therefore the small-m case gives
\(m\ge cL^{-95}\), where
\[
 c=\frac{a^2}{3\cdot2^9 C_UQC_pN_R(1+180/(83a))}
 =\frac{1220703125}
 {55290880670949297430910790657599706215180954961100057836917463891453200560128}.
\]
Exact arithmetic gives \(10^{-68}\le c\le\min(a,83a/180)\).
Assume \(m<cL^{-95}\); these latter comparisons activate both small-m
conditions, and the displayed inequality contradicts the assumption.
Thus **\(m\ge cL^{-95}\)** universally. In particular the author's
\(10^{-68}L^{-95}\) bound holds, including \(L=1\), negative or
nonreal \(t\), \(s=0\), and all coefficient/rank-loss cases.
The rate is for the stated coefficient/residual normalization.

## Original roots and the sharper supplied budget

Let \(a_1<\cdots<a_8\) be balanced norm-one real originals at stationarity
of the precise 7432 angular quotient. Retain the 9496 necessary chart,
including \(t=p_5\ne0\), actual simple criticals, positive masses and
\(R=0\). Suppose adjacent gaps are at least \(\delta\), and
\(|p_5|\ge\tau\), for \(\delta,\tau\in(0,1]\).

Interlacing puts every critical \(\lambda_j\) in
\((a_j,a_{j+1})\subset[-1,1]\). Their adjacent gaps exceed
\(\delta\): at \(x=\lambda_j\), put \(y=x+\delta<a_{j+2}\).
If \(y\le a_{j+1}\) the claim is immediate. Otherwise the denominators
\(y-a_i\) and \(x-a_{i-1}\), \(2\le i\le8\), have matching signs,
and \(y-a_i\le x-a_{i-1}\). For
\(g(w)=\sum_i1/(w-a_i)\), this gives
\(g(y)\ge-1/(x-a_8)+1/(y-a_1)>0\). On the next interval \(g\)
strictly decreases to its zero, which therefore lies to the right of y.
The branch \(y=a_{j+1}\) was already included in the first case.

The positive residues of \(-8f/h\) sum to
\(-8(f_6-h_5)=-8(-1/2+3/8)=1\). The seven Lagrange denominators
have modulus at least \(\delta^6(j-1)!(7-j)!\), whose minimum factor
is 36. Every numerator coefficient is bounded by \(\binom6k\).
Consequently \(|p_k|\le\binom6k/(36\delta^6)\) for every k.
Newton gives
\[
 B=-5\mu_3/24,\quad E=1/16-\mu_4/8,\quad
 F_*=\mu_3/16-3\mu_5/40.
\]
Balance/norm give \(|B|<1, |E|<1\). The author budget
\(L=(\tau\delta^6)^{-1}\) bounds everything, including t inverse,
so Cauchy--Schwarz with
\((13/48)^2+(3/40)^2=4549/57600\) proves the original claimed gap.

**Proved refinement.** Retain the actual k=3,4,5 bounds:
\(|r|\le5/(9\tau\delta^6)\),
\(|s|\le5/(12\tau\delta^6)\),
\(|t|\le1/(6\delta^6)\), \(|t^{-1}|\le\tau^{-1}\).
Thus \(L_* = \tau^{-1}\max(1,5/(9\delta^6))\) is a sufficient budget,
and
\[
 \boxed{\mu_3^2+\mu_5^2\ge\frac{57600}{4549}\,c^2L_*^{-190}.}
\]
It improves the displayed coarse corollary, but keeps its essential
specified \(\tau\) hypothesis. Neither this proof nor finite checks
give a separation-only leading coefficient floor, stationary existence,
collision continuation, physical energy estimate or the complex first-power
endpoint. Improving exponents requires new weighted degree estimates;
we do not assert those uncomputed improvements.
