# Independent G20 cut and an explicit rational margin

Actual **six-reviewer-3**, independent mathematical reviewer, 2026-10-03.
This is an ordinary computer-assisted proof, unformalized. The complete
normalization theorem9774 is an explicit import. Its old pruning corpus
is not rerun here. The four literal polynomials in FACTORS.json are credited,
untrusted defining data from six-tammes-2/source27134011; they were not
independently discovered. All identities and signs below are checked anew.

**Refinement.** On the CLOSED interval \(I=[14/25,593/1000]\), every
injective unit packing carrying the original twelve labels
\(0,1,2,4,5,6,7,8,9,10,11,12\) and the twenty equalities

\[
\begin{gathered}
0:5,6,7,11;\quad1:2,4,10,12;\quad2:4,8,10;\quad4:8;\\
5:7,9,11;\quad6:11;\quad7:12;\quad9:10,11;\quad10:12
\end{gathered}
\]

has \(z<1399/1000\) in the entire labelled9774 chart. Extra contacts are
allowed; further packing points are arbitrary. In particular this proves
the target10088 assertion \(z<7/5\). Both statements concern the chart's
upper coordinate. No lower-component or three-addition capacity conclusion
is established. The exact predicate \(1399-1000z>0\) may be appended to
the lossless9912 model, retaining its six addition variables, positive
radical, every packing comparison and exact critical-strip condition.

## Coordinates and positive factors

The imported frame uses \(H=(1-t)I+t\mathbf1\mathbf1^T\), sole feasible
sheet \((\epsilon,\eta)=(-1,+1)\), and \(g>1/2\). Its chart comparison
gives \((1-t)^2z^2\le1\). Thus \(|z|\le1000/407<5/2\). This comparison
is between original labels7 and1; no thirteenth point is required.

Use the following integer expressions, as defined in the full earlier
[9912 proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-2/twelve-core-polynomial-model/PROOF.md):

\[
\begin{gathered}
a=1+t,\ b=1-t,\ c=1+2t,\ D=b^2c,\ C=1+Dz^2,\\
K=t(9t^2-2t-3),\ J=a^2+K,\ h=9t^2-1,\\
S=D(tz^2-2z)+t(2t-1),\ E=C^2-S^2,\\
G=a^4((1-t^2)C^2-S^2)-K^2C^2+2SKta^2C,\\
R=DG,\ w=\sqrt R>0,\ \Omega=hJbca^8CE.
\end{gathered}
\]

The actual frame has \(g=G/(a^4C^2)>1/2\). The identity
\(G=a^4(1-t^2)E-(KC-Sta^2)^2\) implies \(E>0\). Also
\(J(14/25)=26671/15625>1\) and \(J'=27t^2-2t-1>0\) onI.
Consequently all factors in \(\Omega\) are positive. These statements
are on the feasible domain; positivity ofG on an infeasible rectangle is
never assumed. The metricH is positive definite because \(b,c>0\).

The independent geometry implementation transcribes the written9912
numerators, using ordinary coefficient cross products and
\(L(v)=cv-t(\sum v_i)\mathbf1\). In particular
\[
\begin{gathered}
N_1=a^2e_0,\ N_2=a^2e_1,\ N_4=a^2e_2,\\
N_8=(-a^2,2ta,2ta),\ N_{10}=(2ta,2ta,-a^2),\\
N_{12}=(2t(1+3t),3t^2-2t-1,-2ta),\\
W_n=(Dz^2-1)a^2e_0+2tN_{12}+2bzL(N_{12}\times e_0),\quad W_d=a^2C,\\
V_d=bca^6E,\\
V_n=bca^2[(KC-Sta^2)W_n+C(ta^2C-SK)N_{10}]
       -wL(W_n\times N_{10}),\\
U_n=K(V_dW_n+W_dV_n)-a(3t-1)L(W_n\times V_n),\\
W_l=JV_dW_n,\quad V_l=JW_dV_n.
\end{gathered}
\]
The minus sign inV is the imported original sheet, rather than a fresh
orientation quotient. The twelve numerators are
\[
\begin{gathered}
Y_i=hJCV_dN_i\ (i=1,2,4,8,10,12),\quad
Y_6=hU_n,\ Y_7=hW_l,\ Y_9=hV_l,\\
Y_0=a(2tU_n+2tW_l+bV_l),\\
Y_5=a(bU_n+2tW_l+2tV_l),\quad
Y_{11}=a(2tU_n+bW_l+2tV_l).
\end{gathered}
\]
The points are \(Y_i/\Omega\). Substituting \(k=K/a^2,s=S/C\) and
\(\sqrt{Dg}=w/(a^2C)\) into the originalV formula yields
\(V=V_n/V_d\). Since \(\mu=-abc(3t-1)/J\), the originalU formula gives
\(U=U_n/(JW_dV_d)\). The three reflection formulas then give the displayed
Y values. This audits the packing-to-numerator bridge. Independently,
all twelve unit and twenty required-contact identities are verified as
64 full radical-component zero polynomials.

## Full packing identities

Use \(\langle u,v\rangle_H=(1-t)\sum u_iv_i+t(\sum u_i)(\sum v_i)\).
Define the actual cleared excesses
\(q_5=\langle Y_5,N_{12}\rangle_H-ta^2\Omega\) and
\(q_6=\langle Y_6,N_8\rangle_H-ta^2\Omega\). Their signs are the signs
of the original pair excesses because \(a^2\Omega>0\).
Let
\[
\begin{gathered}
F_5=ta^{10}bc(3t-1),\quad F_6=a^5bc(3t-1)(3t+1),\\
Z=t(3t+1)z-(1+2t),\ M_5=1+2t-t^2-2tbcz,\\
Q=aDz^2-2Dz+2t^2-t+1.
\end{gathered}
\]
BothF factors are strictly positive onI. Whole exact integer division
recovers \(q_i=F_i(A_i+B_iw)\), including every constant and linear
coefficient. With the credited four literal polynomials \(L_5,M_6,H_{10},H_{12}\),
the fresh identity proof establishes
\[
\begin{gathered}
A_5=2D(bz+1)CL_5,\quad B_5=-2(bz+1)CM_5,\quad B_6=2(bz+1)M_6,\\
A_5^2-B_5^2R=32ab^5c^3JC^2(bz+1)^2(1-bz)(bcz+t)ZQ,\\
A_6^2-B_6^2R=4a^2b^4c^3J(bz+1)^2QH_{10}H_{12},\\
aQ=D(az-1)^2+4t^2,\quad M_5(t,1/b)=1-5t^2.
\end{gathered}
\]
The squared identities are also verified in completely uncancelled
q form, retaining \(F_i^2\). Thus a proof using rawq coefficients can
avoid the division step entirely. \(Q>0\) follows from its displayed
square identity. The factorZ is retained even when it changes sign;
no extra5–12 contact or rational-family threshold is imposed.

## Complete closed cover and stronger signs

For either \(r=7/5\) or \(r=1399/1000\), put
\[
\begin{split}
T_0&=[14/25,113/200]\times[r,71/50],\\
T_1&=[113/200,593/1000]\times[r,5/2],\\
T_2&=I\times[71/50,5/2].
\end{split}
\]
They cover \(I\times[r,5/2]\). The independent decoder binds all25
elementary boundary/open cells to containing closed rectangles. Every
cell and seam is included. The strengthened signs are:

| Polynomial | Closed rectangle | Bound supporting its strict sign |
|---|---|---|
|L5|\(I\times[1399/1000,5/2]\)|\(\ge65643155254485131589/38146972656250000000>0\)|
|Z|T1|\(\ge8893/40000000>0\)|
|Z|T2|\(\ge174/15625>0\)|
|M6|T0|\(\ge8238880644523156208257551/1192092895507812500000000>0\)|
|H10|T0|\(\le-109889990082414107919277317/122070312500000000000000000<0\)|
|H12|T0|\(\ge261976057906926985419903000021/7450580596923828125000000000>0\)|

These are rational interval-Horner bounds on the SIX WHOLE closed boxes;
no subdivision is needed. The original7/5 boxes are independently checked
too. Every translated dense coefficient and interval endpoint operation
is exact. RESULTS.json stores all complete records and the hashes of all
six ordered full interval-row arrays for each cut.

OnT0, \(B_6>0\) and \(A_6^2-B_6^2R<0\); hence
\(B_6w>|A_6|\), so \(q_6>0\) contradicts packing. No sign ofA6 is assumed.
OnT1 orT2, \(A_5>0\) andZ>0. The chart gives \(0<bz\le1\).
When \(bz<1\), the first squared identity is strictly positive, so
\(A_5>|B_5|w\), and again \(q_5>0\). At \(bz=1\), retain the actual
boundary: \(M_5=1-5t^2\le-71/125<0\), so \(B_5>0\) and \(q_5>0\)
directly. \(bz>1\) violates the original chart packing inequality.
Since actual \(|z|<5/2\), these cases exclude every actual \(z\ge r\),
including both endpoints ofI and every closed seam. Thus the stronger
strict cut follows, and so does the target assertion.

## Why the identity and sign algorithms are proofs

An integer expression's coefficient-l1 norm is bounded recursively by
\(N(f+g)\le N(f)+N(g)\) and \(N(fg)\le N(f)N(g)\). The compiler also
propagates separate degrees. For a residual choose stride \(s>d_t\) and
integer radix \(B>2N\); evaluate \(f(B,B^s)\) exactly. Distinct t/z
monomials occupy distinct positions. If the image is zero, the least
nonzero coefficient must be divisible byB, impossible because its absolute
value is less thanB. Therefore the residual is identically zero. Balanced
digits recover every coefficient exactly. This proves the ten checked
binding identities and all64 coordinate components without interpolation
or probabilistic testing. Maximum degree bound is(58,12), maximum radix
is \(2^{93}\). Integer division checks every coefficient of all four
scalar quotient polynomials with zero remainder.

For signs, exact binomial translation expresses the polynomial in
\(u=t-t_a\), \(v=z-z_a\). On the closed box, both offsets are nonnegative
bounded intervals. Nested interval Horner uses exact endpoint extrema
under addition and multiplication and therefore encloses every value.
Each required lower bound is positive, or upper bound negative. An
incomplete cover or a non-strict zero cannot supply the contradiction.

The implementation trust is standard-library arbitrary integers,
Fractions, the inspected short arithmetic programs and ordinary algebra.
There is no proof-assistant, CAS, solver or floating-point proof input.
