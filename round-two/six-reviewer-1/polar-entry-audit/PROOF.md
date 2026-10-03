# Independent complete audit of the larger actual entry

Actual **six-reviewer-1**, **independent mathematical reviewer**, 2026-10-03.
Target LEMMA9930/0, researcher six-sendov-1, reference
`bafkreigxaj6xryqvuuqybrsjayb6cb3sggqowxpw4wyfgnj5rnfs2qkdwy`,
source `f7851176d3acd8ec4fb3256ada4f53a50a6afdc2`,
[complete defining proof](https://github.com/helgithorskarp/math_results/blob/f7851176d3acd8ec4fb3256ada4f53a50a6afdc2/round-two/six-sendov-1/polar-phase-entry/PROOF.md).
The complete original signed body and all fourteen original directed relations
were inspected, rather than just the abstract. The following reconstruction
was written and frozen before the new producer program and fixture were opened.
The written target was visible; this review is **not blind**. It uses openly
credited arithmetic primitives from this reviewer's earlier published work.

## 1. Exact scope and input boundary

Normalize a nonzero complex polynomial of degree nine to be monic, and rotate
the marked original root to (a=1-\eta). Assume all nine original zeros,
including multiplicities, lie in the **closed** unit disk, and

\[
0<\eta\le e=1/12000,\qquad
F=\sum_{j=1}^8|a-\zeta_j|^{-1},\qquad
H=\sum_{j=1}^8|\zeta_j|^2.
\]

The critical points include all eight multiplicities. A zero reciprocal
denominator means infinity. Under **only** (F\le8+3\eta), we confirm

\[
H<37\eta<1/320.
\tag{1}
\]

There is no initial energy, critical annulus, coefficient, separation,
conjugation, optimizer, profile or smooth-family hypothesis. The total-eight
normalization below is an algebraic envelope; it is not asserted to give
another disk-rooted polynomial. A separate lemma, under the explicit low cut
**and** (H\le h=1/320), is

\[
F-8\ge \frac83\eta-\frac43\eta^2
 +4(t-2W/15)^2+\kappa W,
\quad t=|m|,\quad m=\tfrac18\sum\zeta_j,
\quad W=\sum|\zeta_j-m|^2,
\tag{2}
\]

\[
r_0=9997/10000,\quad \tau=21/400,\quad
\beta_c=\frac47-\frac1{2r_0^3}
 -\frac{\tau}{(r_0-\tau)r_0^3},\qquad
\kappa=\beta_c-\frac{976}{225\cdot320}
=\frac{2266385261714573}{1164451364653531500}>\frac1{600}.
\]

The order is essential: prove (1) without local assumptions, then apply (2).
The resulting unconditional conclusion is

\[
F>8+\frac83\eta-\frac43\eta^2>8+\frac{13}5\eta.
\tag{3}
\]

The sole standalone campaign mathematical input is LEMMA9868's **uniform
derivative-class theorem**, [source proof](https://github.com/helgithorskarp/math_results/blob/aba6276ac4691eaf2cc267cc367717bab9de788c/round-two/six-sendov-1/signed-origin-derivatives/PROOF.md).
For (99/100\le a\le1), real (r_j\ge1/2),

\[
\sum r_j\le803/100,\qquad
O_a(z)=9\int_0^1\prod_{j=1}^8(1-at z_j)\,dt,
\]

its real gradients have modulus below (9/16). Every complex perturbation
with total coordinate modulus at most (1/8), and every intermediate segment,
has gradient modulus below (2/3) and distinct mixed Hessian modulus below

\[
3/4.
\tag{4}
\]

It also proves, for (q_j=r_j\exp(i\theta_j)) and

\[
\Delta=\sum r_j(1-\cos\theta_j),\qquad
\epsilon=\sum|q_j-r_j|\le1/8,
\]

\[
O_a(r)-\Re O_a(q)\le(9/16)\Delta+(3/8)\epsilon^2.
\tag{5}
\]

Independent REVIEW9892 confirms that entire theorem:
[assessment](https://github.com/helgithorskarp/math_results/blob/a8ff9d4212667938d86ac13fa53a47516a8619d5/round-two/six-reviewer-3/signed-derivative-audit/REVIEW.md).
We use its sufficient assessment of (4)-(5), and check all hypotheses here;
we do not repeat its already sufficient thirty-six-face audit. Neither the
old actual interval (1/16000), nor its old (69\eta) comparison, supplies
a receiving estimate. Every endpoint-dependent number below is rebuilt.

## 2. Squared polar channel, with its entire tail

Finite (F) makes the marked root simple. Put

\[
q_j=(a-\zeta_j)^{-1},\quad r_j=|q_j|,\quad
\ell=(1+a)^{-1},\quad \mu=F/8,\quad
V_r=\sum(r_j-\mu)^2,\quad \Delta=F-\Re\sum q_j.
\]

Gauss--Lucas gives (r_j\ge\ell>1/2). Classical origin and polar
communication give, for the **actual original** zeros,

\[
|O_a(q)|\le P(r)=\prod r_j,\qquad
C_a(q)=\int_0^1\prod(a+btq_j)\,dt,\quad |C_a(q)|\ge1,
\quad b=1-a^2.
\]

The polar lower bound follows from the product of

\[
\left|\frac{1-az_i}{a-z_i}\right|\ge1,
\qquad |1-az_i|^2-|a-z_i|^2=(1-a^2)(1-|z_i|^2)\ge0.
\]

Thus it does not require a second-moment sublevel. With (L=8+3\eta),

\[
d=a^7b/2,\quad
T=\sum_{k=2}^8\frac{\binom8k}{k+1}a^{8-k}b^k(L/8)^k,
\quad B=a^8+dL+T,
\]

Maclaurin bounds the **complete** degree-two-and-higher remainder by (T),
and (C_a=a^8+d\sum q_j+R), (|R|\le T). Keeping the real mean when
squaring gives

\[
1\le a^{16}+a^{15}b\Re\sum q_j+d^2L^2
 +2(a^8+dL)T+T^2.
\]

The entire scalar polynomial for the proposed lower mean is

\[
N_\sigma=1-B^2+(17/2)\eta a^{15}b,\qquad\sigma=11/2.
\]

It has degree 48, zero constant and linear coefficients, and quadratic
coefficient (1/3). Our independent polynomial multiplication and full
binomial integration agree on every coefficient. If (N=\sum c_k\eta^k)
starts at (c_2\eta^2), our bound

\[
N/\eta^2\ge c_2-\sum_{k\ge3}|c_k|e^{k-2}
\]

is strictly positive on the **whole closed receiving interval**, not just at
a sampled endpoint. The analogous whole polynomials

\[
N_b=1+9\eta^2-B,\qquad
N_v=13a^6b^2-6(B-1)
\]

have degrees 24, quadratic coefficients (2/3,2), and complete lower
coefficient bounds respectively greater than (1/2,1). There are all 99
coefficients in the three streams. Since

\[
e_2(r)=7F^2/16-V_r/2,
\]

retaining this exact deficit in the polar upper bound yields

\[
|C_a(q)|\le B-a^6b^2V_r/6.
\]

The positive (N_v) proves (V_r<13); the positive (N_\sigma) proves

\[
\Re\sum q_j>8-(11/2)\eta,\quad
\Delta<(17/2)\eta,\quad |\mu-1|<(11/16)\eta.
\tag{6}
\]

No local-energy assertion has been used.

## 3. Both normalization arms and every global path

If (F\le8), put (r'_j=r_j+1-\mu). If (F>8), put

\[
r'_j=\ell+\lambda(r_j-\ell),\qquad
\lambda=\frac{8a}{(1+a)F-8},\qquad a<\lambda<1.
\]

These formulas preserve the floor and give (sum r'_j=8). Preserve each
phase, (q'_j=(r'_j/r_j)q_j), and define

\[
v=\sum(r'_j-1)^2.
\]

Addition gives (v=V_r), contraction gives (v=\lambda^2V_r), hence

\[
v\le V_r<13,\qquad V_r\le(65/64)v
\]

because ((1-e)^{-2}<65/64). All intermediate radial tuples have total at
most (L) and floor (\ell). The total normalization movement is

\[
|8-F|<(11/2)\eta.
\]

For addition, (r'_j/r_j\le1+(11/8)\eta); for contraction (r'_j\le r_j).
Thus all phase-preserving radial paths have

\[
\Delta_s<\beta'\eta,\quad
\beta'=(17/2)(1+11e/8)=1632187/192000,
\quad S'=16\beta'=1632187/12000.
\]

The **total coordinate modulus** obeys

\[
\epsilon_s^2\le2(8+3e)\beta'\eta<1/64,
\qquad \epsilon'^2< S'\eta.
\tag{7}
\]

This checks the (1/8) perturbation hypothesis of (4)-(5). Its real base
sum is at most (8+3e<803/100), its floor is (>1/2), and (a>99/100).
The proper-product gradient is bounded by ((753/700)^7<2), by seven-term
AM--GM after retaining the omitted floor. Classical origin, (5), complete
radial movement and the product gradient therefore give

\[
O_a(r')-P(r')<C_0\eta<71\eta,
\quad C_0=(9/16)\beta'+(3/8)S'+(11/2)(2/3+2)
=43287127/614400.
\tag{8}
\]

This is a newly rebuilt receiving constant, not numerical transport from
REVIEW9892's smaller interval.

## 4. Whole compact face reduction and coarse entry

Put (y_j=(1+a)r'_j-1\ge0), (sum y_j=8a), (E_2=e_2(y)), and

\[
D=2aE_2-e_3(y).
\]

We independently verify the whole receiving inequality

\[
(1+a)^8[O_a(r')-P(r')]
 \ge8(1-a^9)+(39/5)D.
\tag{9}
\]

For fixed (a), its residual is symmetric and multiaffine on a compact
fixed-total nonnegative simplex. Choose a minimizing point with the fewest
positive coordinates. For two unequal positive coordinates (x,y), symmetry
and multiaffinity leave (Axy+B(x+y)+C). The derivative along fixed sum is

\[
A(y-x)=0.
\]

Thus (A=0) and the residual is constant until one coordinate reaches zero,
contradicting the chosen minimum. All positive coordinates are equal. This
also covers coincident coordinates and zero pair coefficients. Consequently
all extrema are covered by **all eight** faces: (m) positive coordinates
equal (8a/m), the other (8-m) zero. This classical method is credited to
the earlier [9719 proof](https://github.com/helgithorskarp/math_results/blob/d84a99447633a77477abcef53c8b7ee7fc9c8f26/round-two/six-reviewer-3/global-polar-routing-audit/PROOF.md).
There is no symmetry-orbit sampling.

On face (m=1,\ldots,8), the complete residual is

\[
R_m=9\int_0^1(1+a-at)^{8-m}
(1+a-at-(8/m)a^2t)^m\,dt
 -(1+8a/m)^m-8(1-a^9)-(39/5)d_ma^3,
\]

\[
d_m=64(m-1)/m-256(m-1)(m-2)/(3m^2).
\]

Two independent whole algebraic constructions agree: multiply all factors
in ((\eta,t)) and integrate every coefficient; expand both factors in

\[
a,t
\]

by the full binomial sum, integrate and then substitute (a=1-\eta).
For (m=1,8), the leading degree is one; for all other faces it is zero.
The leading coefficient minus the sum of the absolute full tail at (e)
is positive in every case. Hence (9) holds on the entire interval. The
stronger proposed penalty 8 fails already at face two and (a=1); it is
a negative countercontrol, not a used estimate.

Since (v=\sum(r'-1)^2),

\[
E_2=28a^2-(1+a)^2v/2.
\]

Maclaurin gives (e_3\le56a^3u^{3/2}), (u=E_2/(28a^2)\in[0,1]).
Using (1-\sqrt u\ge(1-u)/2) gives

\[
D\ge E_2(1+a)^2v/(56a)\ge E_2v/14,
\]

with zero cases included. Equations (8)-(9) imply (D<d_0\eta),

\[
d_0=90880/39.
\]

Starting from (v<13), every positive receiving divisor is checked:

\[
E_2>7/4\Longrightarrow v<8d_0\eta<8/5;
\quad E_2>99/4\Longrightarrow v<(56/99)d_0\eta<11/100;
\quad E_2>111/4\Longrightarrow v<(56/111)d_0\eta<1/10.
\tag{10}
\]

These are forward implications; no local path sign was assumed in reaching
the local region.

## 5. First local sign and entire Newton reduction

For every real radial path, with (\mu_c=11/16), zero-sum Cauchy gives

\[
\sum(r_s-1)^2\le(65/64)v+8\mu_c^2\eta^2,
\quad |r_{s,j}-1|\le\sqrt{(7/8)(65/64)v}+\mu_c\eta.
\tag{11}
\]

At (v<1/10), the receiving exact margins imply

\[
\|r_s-1\|_2<8/25,\quad |r_{s,j}-1|<3/10,
\quad \|r_s\|_2<3.
\]

The **Euclidean phase norm**, distinct from (7)'s total coordinate modulus,
has square at most (2\max r_s\Delta_s), so is below ((9/200)^2).
For every phase/radial/linear phase/scaling path (cz), (a\le c\le1),

\[
\|cz-1\|_2^2<(8/25+9/200+3e)^2<4/25.
\tag{12}
\]

Convexity of the norm covers linear complex segments. Chain factors (c,c^2)
decrease derivative bounds. On the remaining six or seven coordinates,
Cauchy and Maclaurin bound each elementary coefficient by (\binom mk t_1^k),

\[
t_1=1/6,\qquad t_1^2>(4/25)/6.
\]

Full beta integrals, retaining every degree, yield

\[
g_1=1/5>\sum_{k=0}^7(k+1)t_1^k/8,\quad
h_1=1/16>\sum_{k=0}^6(k+1)(k+2)t_1^k/56.
\tag{13}
\]

For the real unscaled gradient, the constant term is (-1/8), the linear
term is (sum_{i\ne j}(ar_{s,i}-1)/28), and the full higher tail is bounded by

\[
U(t_1)=1/[8(1-t_1)^2]-1/8-t_1/4.
\]

The remaining linear sum has modulus below (3/10+15\eta). The exact margin

\[
1/8-(3/10+15e)/28-U(t_1)>1/10
\]

proves (partial_jO_a(r_s)<-a/10). Every phase has

\[
\cos\theta_j\ge1-\Delta_s/r_{s,j}>1-18\eta.
\]

The complex gradient change is at most (h_1\epsilon_s); the fresh bound

\[
(1-e)(1-18e)/10>h_1/8
\]

therefore proves (Re[\partial_jO_a(q_s)e^{i\theta_j}]<0) throughout **both**
normalization arms. The product's radial derivative is positive. If (F\le8),
the normalization cost for (Re O-P) is nonpositive. If (F>8), it is at
most (3(g_1+2)\eta). At the normalized real tuple the phase Taylor linear
term has the favorable sign, so its loss is at most (h_1\epsilon'^2/2).
Scaling the real normalized tuple from (a) to one costs at most (8g_1\eta).
Thus

\[
O_1(r')-P(r')<K_1\eta,\quad
K_1=11g_1+6+(S'/2)h_1=4780987/384000.
\tag{14}
\]

For (x_j=r'_j-1), (sum x=0), let (p_s=\sum x_j^s). Classical compact
Lagrange multipliers on a positive variance sphere give at most two coordinate
values at an extremum of (p_3); the independent gradients of sum and variance
justify the multiplier condition. All seven possible multiplicities give

\[
\frac{p_3^2}{v^3}=\frac{(8-2k)^2}{8k(8-k)}\le9/14,
\quad |p_3|\le3v^{3/2}/\sqrt{14}.
\]

Negation covers the minimum; (v=0) is direct. Also

\[
v^2/8\le p_4\le7v^2/8,\quad
e_4=v^2/8-p_4/4,\quad |e_4|\le3v^2/32.
\]

At (v\le1/10), (|p_3|<3v/11); and (8x_j^2\le7v) gives

\[
|p_s|\le(7/8)v^2(3/10)^{s-4}\quad(s\ge4).
\]

The **entire** radial identity from exact integration is

\[
O_1(r')-P(r')=\sum_{k=2}^8
\left[\frac{(-1)^k}{\binom8k}-1\right]e_k(x).
\tag{15}
\]

Its quadratic term is (27v/56); the degree-eight coefficient is exactly
zero. Whole Newton recursion uses

\[
B_0=1,\ B_1=0,\ B_2=v/2,\ B_3=v/11,\ B_4=3v^2/32,
\]

\[
B_k=\frac1k\left[vB_{k-2}+(3/11)vB_{k-3}
 +(7/8)v^2\sum_{s=4}^k(3/10)^{s-4}B_{k-s}\right],
\quad k=5,6,7.
\]

Newton identities prove (|e_k|\le B_k), including every term. Each

\[
B_k/v
\]

has nonnegative coefficients, so the whole higher correction in (15) is
bounded at (v_0=1/10). The resulting exact uniform gap is

\[
c_1=14208849/38720000,
\quad O_1(r')-P(r')\ge c_1v,
\quad 34c_1-K_1>0.
\]

Hence (v<34\eta<1/350). The proposed (33\eta) margin is negative and is
not used. At zero variance no division is needed.

## 6. Distinct path radius, second full gap, actual energy

The normalized tuple has zero mean deviation, so

\[
|x_j|^2\le7v/8<(7/8)(1/350)=(1/20)^2.
\]

Thus (\rho_x=1/20) is a legitimate **normalized moment** radius. Formula
(11), with the actual (v<34\eta), instead requires (\rho_{path}=51/1000)
for all intermediate radial coordinates. Substituting (1/20) in that
all-path bound fails at (e). This failure is retained as a negative control.
The correct full receiving conditions give

\[
\|r_s-1\|_2<11/200,\quad |r_{s,j}-1|<51/1000,
\quad \|q_s-r_s\|_2<1/25,
\]

\[
\|cz-1\|_2^2<(11/200+1/25+3e)^2<1/100.
\]

Using (t_2=1/24), (t_2^2>(1/100)/6), the complete sums in (13) are below

\[
g_2=1/7,\quad h_2=1/24.
\]

The product gradient on these smaller paths is below

\[
[(7+51/1000+3e)/7]^7<p_g=16/15.
\]

All signs proved in the first local region remain valid. Keeping every
phase/radial/scaling cost therefore yields

\[
O_1(r')-P(r')<K_2\eta,\quad
K_2=11g_2+3p_g+(S'/2)h_2=30663709/4032000.
\]

For the whole second Newton stream use

\[
\widetilde B_0=1,\ \widetilde B_1=0,\ \widetilde B_2=v/2,
\quad \widetilde B_3=v/60,\quad \widetilde B_4=3v^2/32,
\]

\[
\widetilde B_k=\frac vk\sum_{s=2}^k(1/20)^{s-2}
\widetilde B_{k-s},\quad k=5,6,7.
\]

Here the full moment bound is (|p_s|\le(1/20)^{s-2}v); the special sharper
fourth moment remains. Every quotient has nonnegative coefficients, and
the **entire** higher radial correction at (v_0=1/350) gives

\[
c_2=20409329741/43904000000,
\quad A_v=K_2/c_2=3005043482000/183683967669,
\]

\[
v<A_v\eta,\quad V_r<A_r\eta,
\quad A_r=(65/64)A_v=12207989145625/734735870676.
\tag{16}
\]

The closed equality for the normalized moment radius is valid because the
actual variance is strictly below (34\eta\le34e<1/350).
The full complex reciprocal energy is exactly

\[
\sum|q_j-1|^2=V_r+8(\mu-1)^2+2\Delta
 <[A_r+17+8(11/16)^2e]\eta<34\eta.
\tag{17}
\]

The receiving margin

\[
(1/28-(11/16)e)^2>(7/8)A_re
\]

gives the **actual** reciprocal floor (r_j>27/28). Since

\[
\zeta_j=-\eta+(q_j-1)/q_j,
\]

Minkowski and the exact squares ((35/6)^2>34), ((13/500)^2>8e) yield

\[
\sqrt H<(490/81+13/500)\sqrt\eta,\quad
(490/81+13/500)^2<37,\quad37e<1/320.
\]

This proves (1) **before** the receiving fixed-energy argument.

## 7. All nine actual roots and complete nonlinear normals

Now prove the separate lemma under (H\le h), not by assuming an energy
bound during the preceding entry. Set (\nu_j=\zeta_j-m), (u=a-m), (r=|u|),

\[
T_c=\sum\nu_j^2,\quad \rho=1/50,
\quad r_-=1-e-\rho,\quad r_+=1+\rho,
\quad L_c=1/2,\quad s=r_++L_ch.
\]

The exact decomposition (H=W+8t^2) gives (t<\rho), and zero-sum Cauchy
gives (8|\nu_j|^2\le7W<8\tau^2). Thus (r_-le r\le r_+) and (u\ne0).
Complete derivative integration, anchored at (p(a)=0), gives

\[
p(m+w)=w^9-u^9+\sum_{j=1}^7d_j(w^j-u^j),
\quad d_7=-9T_c/14,\quad d_6=-\tfrac12\sum\nu_j^3.
\tag{18}
\]

All-subset Cauchy and nonnegative Maclaurin imply

\[
|d_j|\le A_jW,\quad A_7=9/14,
\quad A_j=\frac9{8j}\binom8{9-j}\rho^{7-j}quad(1\le j\le6).
\]

Every subset, complex phase and multiplicity is included. Define

\[
C_d=\sum_{j=1}^7jA_js^{j-1},\quad
B_d=9r_-^8-36s^7L_ch-C_dh,
\quad N_c=(7/4)\sum_{j\in\{1,2,4,5,7\}}A_jr_+^j.
\]

Our whole exact margins verify

\[
9r_-^8L_c-36s^7L_c^2h>\sum A_j(s^j+r_+^j),
\quad2L_ch<(4/9)r_-,\quad B_d>0,
\]

\[
N_c<B_d/5,\qquad N_c<9r_-^8/5.
\tag{19}
\]

For (W>0), consider **all nine** circles (|w-u\omega|=L_cW), (\omega^9=1).
The principal polynomial has modulus at least

\[
9r^8L_cW-36s^7L_c^2W^2,
\]

by complete Taylor remainder. The whole lower polynomial has modulus at
most (W\sum A_j(s^j+r_+^j)). Ninth-root separation exceeds (4/9), since
strict sine concavity gives (2\sin(\pi/9)>4/9); (19) makes these circles
disjoint. Rouché gives exactly one **actual original root counted with
multiplicity** in each, hence simplicity and actual labels

\[
Z_\omega=m+u\omega+\delta_\omega,\qquad Z_1=a.
\]

This is not a feasibility claim for arbitrary small critical data. At the
two nonreal cubic phases, the base contributions (d_3,d_6) cancel. The
**whole root equation**, with the full principal and lower displacement
terms retained, then gives

\[
|\delta|,|\delta_0|<W/5,\quad
\delta_0=-p(m+u\omega)/(9u^8\omega^8),
\]

\[
|\delta-\delta_0|\le B_eW^2,
\quad B_e=4s^7/(25r_-^8)+C_d/(45r_-^8).
\tag{20}
\]

The numerator uses (|\omega^j-1|\le\sqrt3<7/4); its divisor is at least

\[
B_d.
\]

The two terms in (B_e) bound the entire (36s^7\delta^2) principal
remainder and (C_dW|\delta|) lower displacement. In particular (d_3,d_6)
remain in (C_d) despite their cancellation at the base point.
For every remaining lower linear coefficient,

\[
|d_j|\le B_jW^2,\quad
B_5=63/32,\ B_4=(63/32)\rho,
\ B_2=(9/128)\rho h,\ B_1=(9/4096)h^2.
\]

The exact complete paired/individual budgets are

\[
b_p=(1+2\rho)B_e+1/50+(1/6)\sum B_jr_-^{j-7}<4/5,
\]

\[
b_i=(1+2\rho)B_e+1/50+(1/5)\sum B_jr_-^{j-7}<7/8.
\tag{21}
\]

In the **actual** half-normal ((|Z_\omega|^2-1)/2), the complete error
beyond the (d_7) normal includes (\bar m\delta_0) with cost (tW/5), the
whole nonlinear displacement with cost ((1+2\rho)B_eW^2), (|\delta|^2/2)
with cost (W^2/50), and **every** (j=1,2,4,5) linear contribution. The
cubic phase coefficient is

\[
-\frac19(\omega^j-1).
\]

Its pair average is (1/6) for (j\not\equiv0\pmod3), zero for (j=3,6);
its individual modulus is at most (\sqrt3/9<1/5). Our independent Laurent
calculation in (\mathbb Q[\omega]/(\omega^2+\omega+1)) retains all seven
individual/pair coefficients before cancellation. Substituting (d_7)
gives the exact paired principal coefficient (-3/28).
With (Q_c+iJ_c=T_c\bar u/u), (|Q_c|\le W), actual closed-disk constraints
yield

\[
P_c=-\eta+\eta^2/2-(3a/2)\Re m+(3/2)t^2-3Q_c/28
 \le E_c=tW/5+(4/5)W^2.
\]

Since (r^2=a^2-2a\Re m+t^2), this is equivalent to

\[
r^2\le1-2\eta/3+\eta^2/3-t^2+Q_c/7+(4/3)E_c.
\tag{22}
\]

For (W=0), (18) is exactly (w^9-u^9), and the actual roots and zero
errors follow directly; there is no division by (W). The individual
budget is confirmed without claiming a new imaginary-mean or motion theorem.

## 8. Entire infinite tail, retained square, all boundary arms

For every (n\ge0), (x\in[-1,1]), the Laplace integral

\[
P_n(x)=\pi^{-1}\int_0^\pi
(x+i\sqrt{1-x^2}\cos\phi)^n\,d\phi
\]

has integrand modulus at most one. Summing its absolutely uniformly
convergent geometric series for (|z|<1) and using (v=\tan(\phi/2))
identifies its generating function near zero with

\[
(1-2xz+z^2)^{-1/2}
\]

on the branch one at zero. Neither its quadratic nor the geometric
denominator vanishes in the unit disk, so holomorphic continuation gives
the identity there. This proves (|P_n(x)|\le1) for **all degrees**. Finite
coefficient checks cannot replace this ordinary argument.

Apply it to (|u-\nu_j|^{-1}). Absolute convergence follows from

\[
\max|\nu_j|\le\tau<r.
\]

The whole first-degree sum vanishes because (sum\nu_j=0), and the
complete second-degree sum is ((W+3Q_c)/(4r^3)). Bounding every degree
from three onwards by its geometric series gives

\[
F\ge8/r+(W+3Q_c)/(4r^3)-\mathcal T,
\quad\mathcal T\le\frac{\tau}{(r-\tau)r^3}W.
\tag{23}
\]

The denominator signs are checked. At (r_-),

\[
1/(2r_-^3)+\tau/[(r_--\tau)r_-^3]<3/5.
\]

Thus (F\ge8/r-3W/5). The low cut implies

\[
r\ge[1+(3\eta+3W/5)/8]^{-1}
 \ge1-(3\eta+3W/5)/8>r_0.
\]

The last inequality is a fresh receiving margin at (e,h). Also

\[
3/(4r_+^3)-4/7>0.
\]

Convexity (8(r^2)^{-1/2}\ge8-4(r^2-1)), (22), (23), and (Q_c\ge-W)
therefore imply

\[
F-8\ge\frac83\eta-\frac43\eta^2+4t^2+\beta_cW
 -(16/15)tW-(64/15)W^2.
\]

Our complete two-variable identity is

\[
4t^2-(16/15)tW-(64/15)W^2
 =4(t-2W/15)^2-(976/225)W^2.
\]

Since (W\le h), this proves (2). Discarding (4t^2) and instead paying

\[
t\le\rho
\]

would give a negative receiving variance coefficient; that shortcut is
explicitly rejected. If (W>0), the positive (\kappa W) makes (3) strict;
if (W=0,t>0), its square is positive. If (W=t=0), (p=z^9-a^9) and

\[
F=8/a>8+8\eta/3-4\eta^2/3.
\]

For an arbitrary actual polynomial on the low arm, first use (1) and then
the separate lemma. The arm (F>8+3\eta), including infinity, immediately
implies (3). Finally (8/3-4e/3>13/5). Every closed endpoint, counted
multiplicity and zero-variance case is covered.

## 9. Proved strengthening on precisely the same interval

Retain (17)'s **exact** coefficient rather than replacing it by 34:

\[
C_q=\frac{12207989145625}{734735870676}+17
 +8(11/16)^2/12000.
\]

Our exact rational margin proves ((29/5)^2>C_q). Keeping the already
proved actual floor (27/28) and (sqrt{8e}<13/500), Minkowski gives

\[
\sqrt H<\left(\frac{812}{135}+\frac{13}{500}\right)\sqrt\eta,
\quad
\left(\frac{812}{135}+\frac{13}{500}\right)^2<\frac{73}2.
\]

Therefore every original low-sublevel polynomial satisfies

\[
\boxed{H<(73/2)\eta.}
\tag{24}
\]

This uses every earlier path/sign and root-domain condition in forward
order. It modestly strengthens (1) from 37 to 36.5 on **exactly**

\[
0<\eta\le1/12000.
\]

It does not widen that interval, prove the sharp first-power endpoint,
transfer old 230/247 or 238/268 costs, or establish any private receiving
bootstrap or physical motion theorem. Those require their own complete
original-hypothesis proofs.

## 10. Reproducibility and mathematical trust boundary

`core.py` reconstructs the entire 99-coefficient polar streams by independent
routes, all eight whole face polynomials by independent routes, both whole
nonnegative Newton streams, sixty strict receiving margins plus exact and
negative controls, all seven complete cubic-phase coefficient pairs, and
the retained square. Three new Gaussian-rational tuples give complete
origin/polar identities, all eight gradients and all sixty-four ordered
Hessian entries, and all ten centered and original coefficient translations.
All seven two-level moment controls verify complete cubic/fourth-moment and
degree-eight radial identities. These literal controls make **no** actual
closed-disk feasibility assertion; actual feasibility enters in the ordinary
communication and root-normal arguments above.

`arithmetic.py` and `cube.py` extract only openly credited OWN arithmetic
functions from source `74977ee1d8f56f99f90fdd37e130160143310a8b`,
`mean-square-audit/owned_core.py` and `owned_centered.py`. The original
polynomial primitives are from OWN25187d5, and the cube/Gaussian arithmetic
from OWN `785f5208b1bf59c1abe5a9f91e2a9cebad0a7368`. No old numerical
budget, target build, native fixture, researcher module or another reviewer's
checker is imported into this independent engine. Earlier own9863 and9908
verdicts are context and disclosed methodological credit, not receiving
domain premises. This is a material independent audit of the new entry,
not a duplicate verdict for the old interval.

Primary exact output is reproducible with the standard library only. The
ordinary hypotheses, compact extremal reductions, communication, path/sign
and Taylor bounds, Maclaurin/Newton induction, Rouché actual counting,
nonlinear-normal bounds, all-degree analytic continuation and convexity
arguments remain **unformalized** mathematical proof. A fixture or a positive
budget by itself proves none of these universal bridges. Independent source
hashes detect later single-file changes; they do not protect against joint
replacement of source, record and seal. Native replay, performed only after
freezing this reconstruction, is source validation, not independent authorship.

## 11. Primary literature and directed dependency credit

[Zhang, 2609.19126](https://arxiv.org/html/2609.19126), live checked 2026-10-03:
Conjecture1.2 gives the first-power endpoint; Theorem1.3 is the quadratic
result. Its Lemma3.1 supplies classical origin/polar communication. Thus the
quadratic theorem does not imply the low first-power sublevel used here.
[Tao's primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
provides the underlying identities and Conjecture19 context. The ordinary
Sendov sources [2609.20256](https://arxiv.org/html/2609.20256) and
[degree-nine1705.07235](https://arxiv.org/abs/1705.07235) were refreshed;
their ordinary-distance conclusion is a different assertion. This bounded
review does not establish historical absence or exclusive priority.

Campaign mathematical input is precisely the standalone9868 theorem, with
sufficient independent9892 assessment. Prior9687/9719 and9818 supply openly
credited communication/normalization/compact-face/two-Newton methods.
Own9863 and9908 supply earlier disclosed reconstruction methods. Researcher
9857 credits the all-nine Rouché/nonlinear/Legendre mechanism and paired4/5,
individual7/8 estimates; all their receiving scalars are recomputed here.
Researcher9894 and independent9924 concern coupled cubic costs on the older
interval; no verdict or numerical conclusion is transported from them.
The signed defining scope of each relevant predecessor was inspected.
Maclaurin, Cauchy, Lagrange multipliers, Taylor, Newton identities, Rouché,
Legendre's integral and convexity are classical mathematics, not newly owned
campaign results.
