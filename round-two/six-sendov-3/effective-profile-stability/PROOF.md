# Effective sharp-profile stability for actual degree-nine polynomials

Actual author **six-sendov-3**, role **researcher**, 2026-10-02.
Complete ordinary author proof, **unformalized and independently unreviewed**.
The explicit local energy entry is imported from [9620](../critical-radius-routing/PROOF.md),
itself an ordinary author lemma. The sharp leading coefficient and asymptotic
profile/motion statements are prior [8530](../sharp-boundary-slope/PROOF.md)
and its scoped [8608 audit](../../six-reviewer-3/sendov-boundary-audit/REVIEW.md).
The new content is the effective remainder and pointwise quantitative defects
on a prescribed domain, not a new leading coefficient or profile classification.
The later [8921 exact analytic minimizer](../analytic-boundary/PROOF.md)
and its [8955 review](../../six-reviewer-1/analytic-minimizer-audit/REVIEW.md)
already supply positive actual slack penalties and stronger selected-profile
stability on existential collars and higher-order surplus classes.
Their methods and conclusions are prior credit, not new claims here.
The fresh [9667 independent audit](../../six-reviewer-3/fixed-energy-audit/REVIEW.md)
confirms the9620 input in its exact domain. Its whole ordinary proof was read.
It gives no verdict on the present stability theorem or the optional9629 input.

## 1. Exact domain and statements

Let $p=z^9+\sum_{j=0}^8c_jz^j$ be complex monic, all its original roots in
the closed unit disk, $p(a)=0$, $a=1-\eta$, $0<\eta\le e=2^{-16}$.
Count all eight criticals $\zeta_j$ with algebraic multiplicity, and put
$F=\sum|a-\zeta_j|^{-1}$, $H=\sum|\zeta_j|^2$. Assume $H\le1/512$.
The constant coefficient is constrained only by anchoring. There is no
conjugation, separated-critical, critical-template, smooth-family or
branch-matching premise. Every reciprocal denominator is positive.

Use the exact credited constants

$$
c=\cos(\pi/9),\quad d=2c^2-1,\quad
y=\frac1{3(1+c)},\quad x=\frac23-y,\quad h_0=14y,\quad C=\frac83+y.
$$

**Effective sharp-slope estimate:**

$$
F>8+C\eta-16\eta^{3/2}>8+\frac{111}{40}\eta.             \tag{1}
$$

For the stability statements impose also $F\le8+3\eta$. Write

$$
m=\frac18\sum\zeta_j=M+iD,\quad \nu_j=\zeta_j-m,\quad
V=\sum|\nu_j|^2,\quad T=\sum\nu_j^2,\quad u=a-m,\quad r=|u|,
\quad Q+iJ=T\bar u/u.
$$

Let $Z_k$ be the actual original labeled near $m+u\omega_k$,
$\omega_k=e^{2\pi ik/9}$. These labels exist by the counted-circle
argument in9620, including $V=0$ separately. They do not assert that
opposite labels are conjugates. Define actual paired half-normal slacks

$$
s_k=-\frac12\left(\frac{|Z_k|^2-1}{2}
                       +\frac{|Z_{9-k}|^2-1}{2}\right)\ge0,
\quad k=3,4,
$$

and the positive credited weights

$$
w_4=\frac1{c+d},\qquad
w_3=\frac23\left(7-\frac{1-d}{c+d}\right),\qquad
\Phi=w_3s_3+w_4s_4+\frac{V+Q}{4}\ge0.                 \tag{2}
$$

The effective coercivity inequality is

$$
F-8>C\eta+\Phi-16\eta^{3/2}.                           \tag{3}
$$

If, in addition, $\epsilon\ge0$ and
$F\le8+C\eta+\epsilon\eta$, put
$\Delta=\epsilon\eta+16\eta^{3/2}>0$. Then

$$
\begin{gathered}
0\le\Phi<\Delta,\qquad
|M+x\eta|<\tfrac43\Delta,\quad |Q+h_0\eta|<21\Delta,\quad
|V-h_0\eta|<25\Delta,\quad |H-h_0\eta|<26\Delta,\tag{4}\\
\sum(\Re\zeta_j)^2<7\Delta,\qquad
|D|<\sqrt{\eta\Delta}+\Delta+44\eta^2.                \tag{5}
\end{gathered}
$$

All nine actual originals, with $Z_0=a$, obey the pointwise motion bound

$$
\left|Z_k-\left[\omega_k+
 \eta\left(-\omega_k/3-x-y\omega_k^{-1}\right)\right]\right|
 <8\Delta+3\sqrt{\eta\Delta},\qquad 0\le k\le8.        \tag{6}
$$

These are all-profile moment and actual-root estimates. They give no
distance to a selected four-plus-four template, unique critical multiset,
global optimizer or effective concentration into the initial $H$ region.
Rotation applies them to any marked original of modulus $1-\eta$.

## 2. Precisely imported effective entry, and new all-phase motion

On $F\le8+3\eta$,9620 gives

$$
V<6\eta,\quad |M|<4\eta/5,\quad |D|<\eta/3,\quad
|m|<13\eta/15,\quad 1-\eta<r<1+\eta.                  \tag{7}
$$

It also supplies the exact centered anchored polynomial

$$
p(m+w)=w^9-u^9+\sum_{j=1}^7d_j(w^j-u^j),\qquad d_7=-9T/14,
$$

and one counted original in each disjoint circle of radius $V/2$ about
$m+u\omega_k$. All originals are simple, but critical collisions remain.
Write $Z_k=m+u\omega_k+\delta_k$ and
$\delta_{0,k}=-p(m+u\omega_k)/(9u^8\omega_k^8)$.
Here $\delta_{0,k}$ is a linear displacement, not the root indexed zero.

The following extends the cube-only displacement budget to **all nine phases**.
Use $\rho=1/64$, $v_*=1/512$, $a_*=1-e$, $r_-=a_*-\rho$,
$r_+=1+\rho$, $L=1/2$, $s=r_++Lv_*$. Maclaurin, as in9620, gives

$$
|d_j|\le A_j V,\quad
A_7=9/14,\qquad A_j=\frac9{8j}\binom8{9-j}\rho^{7-j}\ (j\le6).
$$

Let $C_d=\sum jA_js^{j-1}$, $N=2\sum A_jr_+^j$,
$B_d=9r_-^8-36s^7Lv_*-C_dv_*$.
The strict exact inequalities $N<B_d/4$ and $N<9r_-^8/4$ give
$|\delta_k|,|\delta_{0,k}|<V/4$. Taylor's complete root equation then gives

$$
|\delta_k-\delta_{0,k}|\le B V^2,\qquad
B=\frac{s^7}{4r_-^8}+\frac{C_d}{36r_-^8}.              \tag{8}
$$

No coefficient or nonlinear term is truncated in this bound. If $V=0$,
all criticals coincide, the centered polynomial is exactly $w^9-u^9$,
and all displacements and errors vanish without division by $V$.

Set $U_3=\sum\nu_j^3$, $\mu_3=\sum|\nu_j|^3$. Complete Newton gives
$d_6=-U_3/2$. For all the remaining lower coefficients use
$|d_j|\le B_jV^2$, $j=1,\ldots,5$, where

$$
B_5=63/32,\quad B_4=(63/32)\rho,\quad B_3=(21/128)v_*,
\quad B_2=(9/128)\rho v_*,\quad B_1=(9/4096)v_*^2.            \tag{9}
$$

In particular the uncanceled $d_3$ at phase four is included.
Exact full-window budgets verify

$$
(1+2\rho)B+1/32+\frac29\sum_{j=1}^5 B_jr_-^{j-7}<9/8,
\qquad B+\frac2{9a_*}\sum_{j=1}^5B_jr_-^{j-7}<1.       \tag{10}
$$

The first includes the entire $\bar m\delta_0$, nonlinear displacement
and $|\delta|^2/2$ contributions to actual half-normals.
The second proves, for every phase,

$$
\left|\delta_k-\frac{T}{14u}(\omega_k^{-1}-\omega_k)\right|
 <\frac{\mu_3}{9a_*^2}+V^2                           \tag{11}
$$

when $V>0$, with nonstrict zero version at $V=0$.

## 3. Entire actual cube and fourth-phase normals

Let $A_k=1-\cos(2\pi k/9)$, $B_k'=1-\cos(4\pi k/9)$,
and $L_k=-A_kM-B_k'Q/14$. Exact pair-averaging of the base half-normal
gives $(a^2-1)/2-aA_kM+A_k|m|^2$. Exact linear displacement contributes
$-B_k'Q/14$ from $d_7$.
The $d_6$ contribution is

$$
\frac{\cos(6\pi k/9)-1}{18}\Re(U_3\bar u/u^2).
$$

It vanishes at $k=3$ and equals $-\Re(U_3\bar u/u^2)/12$ at $k=4$.
This third moment is retained at the fourth phase, without conjugation or
a zero-third-moment premise. All higher contributions are bounded by(9)-(10).
Thus the **actual**, independently labeled pair means satisfy

$$
-s_k=-\eta+L_k+R_k,
\qquad |R_3|<40\eta^2,
\qquad |R_4|<46\eta^2+\frac{\mu_3}{12a_*}.            \tag{12}
$$

For $k=3$ the9620 error is $|m|V/6+V^2$.
For $k=4$ the new all-phase error is $|m|V/4+(9/8)V^2$.
The residual base terms are $\eta^2/2+A_k\eta M+A_k|m|^2$.
Using(7), $A_3=3/2$, $A_4<2$ gives the complete40/46 budgets in(12).
Every term through the nonlinear root displacement is accounted for;
these are not leading jets used as a completeness premise.

## 4. Complete reciprocal tail and positive physical defect

Centering gives $\sum\nu_j=0$. Cauchy on the other seven coordinates gives
$8|\nu_j|^2\le7V$. Hence

$$
\mu_3\le\sqrt{7V/8}\,V<3\sqrt{21}\,\eta^{3/2}
 <\frac{55}{4}\eta^{3/2},                            \tag{13}
$$

with the zero case understood nonstrictly; $(55/12)^2-21=1/144>0$.
The entire Legendre generating tail from degree three is at most
$\mu_3/[(r-\tau)r^3]$ when $\max|\nu_j|\le\tau<r$.
This follows by $|P_n(t)|\le1$ and summing the geometric majorant
$\sum_j|\nu_j|^3r^{-4}\sum_{l\ge0}(|\nu_j|/r)^l$.
It is an infinite-series argument, not a finite checker identity.
From(7), $\tau=1/96$ is valid, since $6e<(1/96)^2$.
Put $\Lambda=1/[(a_*-1/96)a_*^3]$.

Convexity of $8t^{-1/2}$ at $t=a^2$ gives
$8/r\ge8/a+8M/a^2-4|m|^2/a^3$.
Together with $|r^{-3}-1|<4\eta$, $|Q|\le V$ and(7), this yields

$$
F-8\ge8\eta+8M+(V+3Q)/4-40\eta^2-\Lambda\mu_3.      \tag{14}
$$

The complete dropped costs are bounded by
$[8(4/5)(2-e)/a_*^2+4(169/225)/a_*^3+24]\eta^2<40\eta^2$.
Positive $8/a-(8+8\eta)$ may be discarded.

The credited exact dual identities are

$$
w_3A_3+w_4A_4=8,\qquad w_3B_3'+w_4B_4'=7,
\qquad 8-w_3-w_4=C.                                  \tag{15}
$$

Using(12), $8M+Q/2=-w_3L_3-w_4L_4$, so(14) gives

$$
F-8\ge C\eta+\Phi
 -(40+40w_3+46w_4)\eta^2
 -\left(\Lambda+\frac{w_4}{12a_*}\right)\mu_3.
$$

Here $V+Q=2\sum[\Re(\nu_j\bar u/r)]^2\ge0$.
The identity $8c^3-6c-1=0$ follows from $\cos(3\pi/9)=1/2$.
Here $c\in(\sqrt3/2,1)$ since $\pi/9<\pi/6$. On this interval the
cubic is strictly increasing, so the two rational endpoint signs select
$c\in(15/16,47/50)$. They imply
$4<w_3<23/5$, $1/2<w_4<3/5$, so the quadratic cost is less than252.
The strict rational endpoint budget

$$
252/256+\frac{55}{4}\left(\Lambda+\frac{3}{60a_*}\right)<16
$$

proves(3), hence(1) on the low sublevel. If $F>8+3\eta$,(1) is immediate
because $C<3$. Finally $c<47/50$ gives $C>826/291$ and
$826/291-1/16>111/40$. The exact numerical window is retained throughout.

## 5. Quantitative complex moment stability

The added near-slope upper bound and(3) give $\Phi<\Delta$.
Thus $s_3<\Delta/4$, $s_4<2\Delta$, $V+Q<4\Delta$.
Using(12)-(13), $\eta\le e$ and $\Delta\ge16\eta^{3/2}$ gives
$|R_3|<\Delta/100$, $|R_4|<\Delta/12$. Therefore

$$
|L_3-\eta|<13\Delta/50,\qquad |L_4-\eta|<25\Delta/12.  \tag{16}
$$

The exact optimal pair satisfies $A_kx+B_k'y=1$, $k=3,4$.
The positive absolute determinant is $3(c+d)/2>651/256$.
Cramer's rule with $B_4'<31/128$, $A_4<97/50$ gives

$$
|M+x\eta|<\left[(62/651)(13/50)+(128/217)(25/12)\right]\Delta
 <4\Delta/3,
$$

and

$$
|-Q/14-y\eta|
 <\left[(24832/32550)(13/50)+(128/217)(25/12)\right]\Delta
 <3\Delta/2.
$$

This proves the $Q,V$ bounds in(4); adding $8|m|^2<8(169/225)\eta^2$
proves the $H$ bound. No determinant vanishes on the stated interval.

Cauchy gives $J^2\le(V+Q)(V-Q)<48\eta\Delta$.
The two individual actual cube normals from9620 give
$|aD-J/14|\le(2/\sqrt3)(s_3+E_3)$, where
$E_3=|m|V/6+V^2<37\eta^2$.
Indeed their difference errors have modulus at most $E_3$ after averaging;
the two originals are not declared conjugate.
Using $2/\sqrt3<7/6$ and the positive $a_*$ lower bound gives

$$
|D|<\frac{2\sqrt3}{7a_*}\sqrt{\eta\Delta}
       +\frac7{24a_*}\Delta+\frac{259}{6a_*}\eta^2.
$$

The three coefficients are respectively less than $1,1,44$.
For the first, $2\sqrt3/7<1/2$ because $48<49$; the other two comparisons
are strict rational endpoint budgets. This proves(5)'s $D$ bound.

Set $\nu'_j=\nu_j\bar u/r$. Then $\sum(\Re\nu'_j)^2=(V+Q)/2<2\Delta$.
Since $\Re u=a-M>0$, $|u/r-1|^2\le2D^2/r^2$.
The inequality $(b_1+b_2+b_3)^2\le3\sum b_i^2$, applied to
$\Re\zeta_j=M+\Re\nu'_j+\Re[\nu'_j(u/r-1)]$, gives

$$
\sum(\Re\zeta_j)^2
 <6\Delta+(384/25)\eta^2+4\eta^3/a_*^2<7\Delta.
$$

All scalar margins, including the square-root coefficient bounds, are exact.

## 6. All nine actual original-root motions

The exact $T$ displacement in(11) uses
$T/u=(Q+iJ)/\bar u$. Thus

$$
\left|\frac{T}{14u}+y\eta\right|
 <\frac{21\Delta+4\sqrt{3\eta\Delta}}{14a_*}
   +\frac{28y}{15a_*}\eta^2,                          \tag{17}
$$

because $|u-1|\le\eta+|m|<28\eta/15$.
Also $|m+x\eta|<7\Delta/3+\sqrt{\eta\Delta}+44\eta^2$.
Use $x+y=2/3$ to compare
$m+(a-m)\omega_k+[T/(14u)](\omega_k^{-1}-\omega_k)$
with the expression in(6). Equations(11),(13),(17) give the full error

$$
\left(14/3+3/a_*\right)\Delta
 +\left(2+4\sqrt3/(7a_*)\right)\sqrt{\eta\Delta}
 +125\eta^2+\frac{55}{36a_*^2}\eta^{3/2}.
$$

The125 coefficient uses $y<16/93$, proved from $c>15/16$.
Exact budgets give $2+4\sqrt3/(7a_*)<3$ and

$$
14/3+3/a_*+\frac{125/256+55/(36a_*^2)}{16}<8.
$$

This proves(6) for all phases, including the marked root and total collision.
The argument is pointwise in each polynomial; no differentiability through
a critical collision or analytic path is required.

## 7. Coverage and evidence boundaries

The leading coefficient, two dual angles/weights, limiting moment relations,
balanced-sphere profile set and limiting root motion are already8530/8608.
Their universal concentration radii are existential. This proof gives explicit
finite remainders, positive actual slack/real-energy coercivity, and effective
complex moment/root bounds on the numerical region supplied by9620.
It does not make an existential annulus constant numerical.
The stronger8921/8955 exact-minimizer classification and error-free
slack/profile gaps retain their prior credit; their collars and coverage of
fixed cubic-surplus classes are existential. The present leading-surplus
estimates use an explicit full window and all critical profiles in the
specified energy region. No new uniqueness or selected-profile gap follows.

**Credited optional union corollary.** The actual wider-collar energy lemma
[9629 by six-sendov-1](../../six-sendov-1/paired-cube-energy/PROOF.md)
states that $\max_j|\zeta_j|\le1/25$ and $F\le8+3\eta$ imply $H<25\eta$.
Its complete published ordinary proof and complete signed defining body were
read and aligned; no checker replay or review verdict is asserted here.
9620 is now independently confirmed by9667;9629 remains independently
unreviewed. No parent verdict transfers to the present theorem.
Since $25\eta\le25/65536<1/512$ (gap $103/65536$), apply the core theorem
only after this credited entry. Hence(1) holds on the union

$$
H\le1/512\quad\hbox{or}\quad \max_j|\zeta_j|\le1/25.
$$

For the collar's $F>8+3\eta$ case,(1) is immediate because $C<3$.
The additional low-sublevel stability statements(2)-(6) also hold on that
union, with the same actual counted labels. This optional enlargement
imports9629; the core proof above imports only9620.
The global arm with both $H>1/512$ and $\max_j|\zeta_j|>1/25$ remains open.
No selected critical template or angular stationary classification follows.

Finite exact coefficient maps, the entire phase table, dual identities and
rational budgets corroborate the written proof. Root counting, all nonlinear
norm bounds, nonnegative Maclaurin/Cauchy, full infinite-series convergence,
convexity and all-parameter coverage remain ordinary unformalized bridges.
All roles and pinned sources are explicit; author code reuse is not review.
The current primary first-power Conjecture1.2 remains distinct from quadratic
Theorem1.3. No global first-power resolution or historical priority is claimed.
