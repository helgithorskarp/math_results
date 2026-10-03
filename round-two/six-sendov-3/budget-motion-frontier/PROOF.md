# Sharp budget-dependent cubic original-root motion in degree nine

Actual **six-sendov-3**, role **researcher**, 2026-10-03.
Complete ordinary author proof, **UNFORMALIZED and independently UNREVIEWED**.
The small exact certificate corroborates identities and all finite count
cases. Constraint-manifold calculus, compactness, asymptotic uniformity
and the adopted actual-family theorem remain ordinary analytic arguments.

## Definitions and quantified conclusion

Let every original root of a complex degree-nine polynomial lie in the
CLOSED unit disk. Make the polynomial monic and rotate its marked root
to $a=1-\eta>0$. Count ALL eight critical points $\zeta_l$ with
multiplicity, and put $F_p(a)=\sum_l|a-\zeta_l|^{-1}$, with $+\infty$
at a zero denominator. All the constants below are fixed:

\[
\begin{gathered}
c=\cos(\pi/9),\quad y=\frac1{3(1+c)},\quad x=\frac23-y,\quad
H=14y,\quad U_0=-8x,\quad C=\frac83+y,\\
k=-\frac{7(1+2c)}{18},\quad \rho=\frac{c-5}{3},\quad
\alpha=-\frac{527}{360}+\frac{41}{90}c+\frac{13}{90}c^2<0,
\quad \tau=\frac{(k+\rho)^2}{2},\\
B_* =\frac{2311}{108}+\frac{4934}{27}c-\frac{1976}{9}c^2,
\quad K_1=B_*-\frac{\alpha H^2}{2},\\
K_E=\frac{6653}{324}+\frac{23915}{486}c-\frac{15839}{243}c^2,
\quad 9<K_E<10,\\
q^2=\frac{8+25c+20c^2}{162},\quad e=\frac1{56},\\
P(z)=(30\alpha+81\tau)z+(-840\alpha-3024\tau)z^2+28224\tau z^3,
\qquad g(z)=\sqrt z(9-168z),\quad 0\le z\le e.
\end{gathered}                                                    \tag{1}
\]

For every fixed finite real $D>B_*$ define $z_D$ as follows. If $D<K_E$,
it is the UNIQUE $z_D\in(0,e)$ with
\[
H^2P(z_D)=D-B_*;                                               \tag{2}
\]
if $D\ge K_E$, set $z_D=e$. Existence and uniqueness are proved below.
Let $\mathcal P_D(\eta)$ be the class of all actual polynomials above with
\[
F_p(1-\eta)\le8+C\eta+D\eta^2.                                \tag{3}
\]
For sufficiently small $\eta$, the originals have their canonical
labels $Z_j$ near the nine distinct $\omega_j=e^{2\pi ij/9}$, and define
\[
B_j(\eta)=\omega_j+\eta(-\omega_j/3-x-y/\omega_j),\qquad
M_D(\eta)=\sup_{p\in\mathcal P_D(\eta)}
\frac{\max_{0\le j\le8}|Z_j-B_j(\eta)|}{\eta^{3/2}}.            \tag{4}
\]

**Sharp fixed-budget envelope.** For EVERY fixed finite $D>B_*$,
$\mathcal P_D(\eta)$ is nonempty for EVERY sufficiently small $\eta>0$,
and the limit, not just a subsequential upper bound, is
\[
\lim_{\eta\downarrow0} M_D(\eta)=\mathcal A(D)
       :=qH^{3/2}g(z_D).                                     \tag{5}
\]
There are actual families satisfying the EXACT budget (3), with all
nine originals simple and strictly in the disk, whose normalized motion
tends to (5). In particular, the universal coefficient
$\mathsf A=\sqrt{H^3(8+25c+20c^2)/252}$ is reached at $D=K_E$ and on
every larger fixed budget. Each $B_*<D<K_E$ has a strictly smaller
sharp coefficient. Critical collisions, nonconjugate configurations,
and competitors varying arbitrarily with $\eta$ are included.

**Equality rigidity on smaller budgets and at the threshold.** For
EVERY fixed $B_*<D\le K_E$, if actual polynomials on (3) have
$\eta_n\downarrow0$ and normalized maximum motion tending to $\mathcal
A(D)$, their imaginary critical profile approaches the finite orbit
\[
\begin{split}
\mathcal E(z_D)=\{\ &\text{permutations and overall signs of}\
 &(m,m,m,m,m,m,-3m+r,-3m-r):\quad
 m=\sqrt{Hz_D},\quad r=\sqrt{H/2-12Hz_D}\ \} .
\end{split}                                                     \tag{6}
\]
Moreover, the actual second cost saturates its budget:
\[
\frac{F_{p_n}(1-\eta_n)-8-C\eta_n}{\eta_n^2}\longrightarrow D.  \tag{7}
\]
For $D>K_E$, equality in (5) forces the same $1+7$ endpoint orbit and
only the previously known $\liminf$ cost bound $\ge K_E$; saturation
of an unnecessarily larger budget is not asserted.

**Near-minimum consequence, with the order of limits specified.** Put
\[
\kappa=\tau+\frac{10\alpha}{27}
 =\frac{3053}{1944}+\frac{263}{243}c+\frac{37}{243}c^2>0.
\]
After taking the $\eta\downarrow0$ limit for each fixed budget, one has
\[
\mathcal A(B_*+\delta)
   =q\sqrt{H\delta/\kappa}\,(1+O(\delta))
                                      \quad(\delta\downarrow0). \tag{8}
\]
No joint $D(\eta)\downarrow B_*$ limit, effective numerical collar,
finite-$\eta$ optimizer, or feasibility at the exact cut $D=B_*$ is claimed.

The new application is the COMPLETE sharp fixed-budget motion curve
and its rigidity, including actual attainment under $D=K_E$. The
finite-sample moment methods are classical; no historical priority for
the auxiliary moment frontier is asserted. The canonical motion and
profile cost are prior results. This does not settle the global
FIRST-power Tang--Zhang inequality or the fixed quartic zero-slack
repair question in10028: threshold attainment here uses profiles that
vary with $\eta$, approaching the endpoint from below.

## Precisely adopted prior results and their trust boundary

The required inputs, read in full and source-pinned in
[dependencies.json](dependencies.json), are:

1. [8619, the arbitrary-competitor rate and least-profile cost](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/quartic-boundary/PROOF.md),
   independently assessed in [8684](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/quartic-boundary-audit/REVIEW.md),
   relative to its explicitly inherited concentration and entry inputs.
2. [10060/0, the universal ALL-nine cubic motion theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/sharp-cubic-motion/PROOF.md).
   [Independent review10082](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/cubic-motion-audit/REVIEW.md)
   confirms this universal law relative to its stated inherited inputs;
   its new distance-penalty refinement is not a premise here.
3. [10036, actual uniform realization of the ENTIRE balanced sphere](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/uniform-leading-profiles/PROOF.md).
   [Independent review10070](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/uniform-profile-audit/REVIEW.md)
   confirms this whole-sphere construction. Its lower optimality remains
   relative to8619/8684; its four separately prescribed losses are not
   needed here. Neither review evaluates this new envelope proof.

Here is exactly what is used, rather than treating parent titles as
proofs. For every actual fixed-$D$ arm (3), put
$h_l=\Im\zeta_l/\sqrt\eta$. The profiles are uniformly bounded,
$\sum h_l=O_D(\eta)$ and $\sum h_l^2=H+O_D(\eta)$.
Every convergent ordered subsequence has a limit
\[
v\in\mathcal S:=\{v\in\mathbb R^8:\sum v_l=0,\ \sum v_l^2=H\}.
\]
The necessary second cost obeys
\[
\liminf\frac{F_p(1-\eta)-8-C\eta}{\eta^2}
 \ge \mathcal K(v):=K_1+\alpha J_4(v)+\frac{\tau J_3(v)^2}{H},
\qquad J_r(v)=\sum v_l^r .                                    \tag{9}
\]
This is the full necessary profile cost, not a bound restricted to
analytic critical labels. A nonnegative real-correction squared
residual in8619 can be dropped for (9).

On one collar for each fixed $D$, the10060/0 theorem gives uniformly
over ALL actual competitors and ALL nine original labels
\[
Z_j=B_j(\eta)+\eta^{3/2}J_3(h)W_j+O_D(\eta^2),\qquad
W_j=\frac i{18}[(3+4c)\omega_j-(1+2c)(1+\omega_j^{-1})-
                                             \omega_j^{-2}]. \tag{10}
\]
All originals there are simple. Its exact nine-label norm table gives
$\max_j|W_j|=q$, only at labels2 and7. Thus the actual normalized
motion equals $q|J_3(h)|+O_D(\sqrt\eta)$.

The10036 construction supplies, for EVERY $v\in\mathcal S$ and EVERY
$0<\eta<\eta_0$, actual monic degree-nine polynomials $p_{v,\eta}$
with ALL originals simple and strictly inside the disk, marked original
$1-\eta$, critical multiplicities included, and
\[
h=v+O(\eta),\qquad
|F_{p_{v,\eta}}(1-\eta)-8-C\eta-\mathcal K(v)\eta^2|
                                                    \le L\eta^3, \tag{11}
\]
where the SAME finite $L$ and positive $\eta_0$ work on the ENTIRE sphere.
Its actual polynomial is $9\int_{1-t^2}^z\prod_l(w-\zeta_l(t))\,dw$
with $t=\sqrt\eta$ and four real controls solved by a uniform analytic
implicit-function chart; the ordinary proof checks all nine disk
constraints. We use this existing actual-family theorem, not formal
moment realizability or a new assertion that a truncated jet is actual.
The uniformity in (11) permits profiles depending on $\eta$.

No reviewer code or fixture is imported. The unchanged exact arithmetic
kernel and optional parent-fixture comparisons are same-author reuse,
not independent validation of these ordinary analytic inputs.

## Exact maximum quartic moment at each fixed cubic moment

First recall the classical skewness bound on $\mathcal S$:
\[
|J_3(v)|^2\le 9H^3/14,                                       \tag{12}
\]
with equality only at the $1+7$ orbit
$\sqrt{H/56}(7,-1,-1,-1,-1,-1,-1,-1)$, allowing permutations and
overall signs. To check every case, the two smooth constraints have
independent gradients $\mathbf1,v$; maximizing $J_3$ forces every
coordinate to solve one quadratic. At two distinct coordinate values
with multiplicities $n,8-n$, direct balance and norm give
\[
J_3^2/H^3=(8-2n)^2/[8n(8-n)]
 =9/14,1/6,1/30,0,1/30,1/6,9/14
\]
for ALL seven $n=1,\ldots,7$. One coordinate value contradicts $H>0$.

Fix now an arbitrary $s\in[-\sqrt{9H^3/14},\sqrt{9H^3/14}]$ and
maximize $J_4$ on $\mathcal S\cap\{J_3=s\}$. This is compact; its
nonemptiness will also follow from the explicit family below.
Suppose a maximum has at least three distinct coordinate values.
The three constraint gradients $\mathbf1,2v,3v^2$ are independent:
the minor at three distinct values is a nonzero Vandermonde determinant.
Consequently there is a smooth constraint manifold near that point,
and Lagrange multipliers give a common cubic equation for EVERY coordinate:
\[
f(u)=4u^3-3\lambda u^2-2\mu u-\nu=0.                         \tag{13}
\]
Thus there are exactly three distinct values $r_1<r_2<r_3$.

The constrained Hessian of $J_4-\lambda J_3-\mu J_2-\nu J_1$ is
the diagonal matrix with entries $f'(v_l)$, and it must be nonpositive
on every constraint tangent direction at a maximum. If $r_1$ occurs
at two indices, the difference of those two coordinate unit vectors
lies in ALL three tangent constraints. Its Hessian value is
\[
2f'(r_1)=8(r_2-r_1)(r_3-r_1)>0,
\]
a contradiction. Repetition of $r_3$ gives the same contradiction
$2f'(r_3)=8(r_3-r_1)(r_3-r_2)>0$. Both outer values therefore occur
once, and the middle value occurs SIX times. This tests genuine tangent
directions of the smooth constraint manifold; it does not assume that
changing only two coordinates exactly preserves all constraints.
There are21 ordered positive multiplicity triples summing to8, and
this argument leaves only $(1,6,1)$.

Write the resulting profile as six copies of $m$ and a pair $-3m\pm r$.
Balance and norm give $r^2=H/2-12m^2$. The middle-order condition is
$r>4|m|$ for three distinct values, equivalent to $0\le z=m^2/H<e$.
Direct summation of all eight powers gives
\[
\begin{gathered}
J_3=168m^3-9Hm,\qquad J_4=H^2/2+30Hm^2-840m^4,\\
J_3^2/H^3=z(9-168z)^2=g(z)^2,\qquad
J_4/H^2=Q(z):=1/2+30z-840z^2.                                \tag{14}
\end{gathered}
On $(0,e)$,
\[
g'(z)=\frac{9(1-56z)}{2\sqrt z}>0,\qquad
g(0)=0,\quad g(e)=\sqrt{9/14}.                               \tag{15}
\]
Hence EVERY cubic level in (12) is realized by this family, and its
parameter $z\in[0,e]$ is unique for each $|s|$; the sign of $m$ chooses
the opposite sign of $s$. At $s=0$, $m=0$ and the profile is an opposed
pair with six zeros. At $z=e$, an outer and middle coordinate merge,
giving exactly the already classified $1+7$ endpoint.

It remains essential to handle singular maxima with only two distinct
values, since the three-gradient argument does not apply to them.
For such values $u_1,u_2$, the coordinate identity
$v_l^2=(u_1+u_2)v_l-u_1u_2$ and balance give $-u_1u_2=H/8$;
then $J_3=(u_1+u_2)H$ and
\[
J_4/H^2=1/8+J_3^2/H^3.                                     \tag{16}
\]
At the SAME cubic moment, the candidate (14) exceeds this by the exact
factor
\[
Q(z)-[1/8+g(z)^2]=(1-56z)^2(3/8-9z)>0\quad(0\le z<e).       \tag{17}
\]
The last factor is positive even at $e$. At the sole endpoint $e$,
(12) already forces $1+7$. All singular cases are therefore covered.
Compactness, (13)--(17) prove the GLOBAL statement, including equality:
\[
J_4(v)\le H^2Q(z),\quad
J_3(v)^2/H^3=g(z)^2,quad 0\le z\le e,                       \tag{18}
\]
with equality exactly at the orbit $\mathcal E(z)$ in (6).

This is a self-contained ordinary proof of the needed finite-population
moment frontier. The credited Sharma--Bhandari upper bound specializes
to $J_4/H^2\le1/2+(5/12)J_3^2/H^3$ for eight coordinates. Its excess
over our exact candidate is
\[
1/2+(5/12)g(z)^2-Q(z)=(15/4)z(1-56z)^2,
\]
strictly positive in the interior. This comparison shows why that
general classical bound alone does not determine our sharp cost curve;
it is not a historical-priority assertion. See [LITERATURE.md](LITERATURE.md).

## Exact scalar cost curve and actual attainment under the exact cut

Since $\alpha<0$, (9) and (18) imply for EVERY $v\in\mathcal S$
\[
\mathcal K(v)\ge B_*+H^2P(z),\qquad
J_3(v)^2/H^3=g(z)^2,                                        \tag{19}
\]
with equality exactly at $\mathcal E(z)$. Substitution of (14) proves
the polynomial $P$ in (1), without any asymptotic truncation in $z$.
The exact derivative and endpoint are
\[
P'(z)=(1-56z)(30\alpha+81\tau-1512\tau z),\qquad
B_*+H^2P(e)=K_E.                                            \tag{20}
\]
Here $\tau>0$, and for $0\le z\le e$ the second factor is at least
\[
30\alpha+54\tau=421/6+63c+(29/3)c^2>0.                       \tag{21}
\]
Thus $P$ is strictly increasing on $[0,e]$, despite its derivative
vanishing at the RIGHT endpoint. This proves (2), and (19) translates
every cost cut $\mathcal K(v)\le D$ to $|J_3(v)|\le H^{3/2}g(z_D)$.

For actual attainment when $B_*<D\le K_E$, set, for all sufficiently
small $\eta$,
\[
\epsilon_\eta=\eta^{1/4},\quad z_\eta=z_D-\epsilon_\eta>0,
\qquad v_\eta\in\mathcal E(z_\eta).
\]
Use the SAME uniform actual construction (11) at these moving profiles.
Integrating (20)--(21) over $[z_D-\epsilon_\eta,z_D]$ gives the useful
bound at both interior and endpoint budgets:
\[
\begin{split}
D-\mathcal K(v_\eta)
 &=H^2[P(z_D)-P(z_D-\epsilon_\eta)]\\
 &\ge H^2(30\alpha+54\tau)
       [(1-56z_D)\epsilon_\eta+28\epsilon_\eta^2]\\
 &\ge28H^2(30\alpha+54\tau)\eta^{1/2}.                       \tag{22}
\end{split}
\]
The positive right side dominates $L\eta$, the error in (11) after
division by $\eta^2$. Consequently these are ACTUAL polynomials
satisfying the EXACT cut (3) for EVERY sufficiently small positive
$\eta$, including $D=K_E$. Every original is strict and simple by (11).
Their profiles converge to $\mathcal E(z_D)$, and (10) yields normalized
motion tending to $qH^{3/2}g(z_D)$.

For $D>K_E$, simply choose a FIXED endpoint profile in (11).
The fixed positive budget margin $D-K_E$ dominates the same $L\eta$,
and (10) again gives (5). We have not assumed that an actual family with
the fixed endpoint profile has cost $\le K_E$; the moving profiles in
(22) are what establish the exact threshold statement.

All constants above are on the physical real embedding of the ninth
cyclotomic field. The rational bracket $15/16<c<47/50$ follows from
$8c^3-6c-1=0$, strict monotonicity on $(1/2,1)$ and the endpoint signs;
$\cos(\pi/9)>1/2$ identifies that root. It proves $-1<\alpha<0$ and
$\tau>3$ by substitution, and the decreasing quadratic $K_E(c)$ is
between9 and10 on this bracket. The certificate checks every rational
endpoint inequality and the entire field identities, not floating-point
estimates or a choice of a different algebraic embedding.

## Upper envelope, equality and the near-minimum limit

Fix $D>B_*$. The preceding families make (4) meaningful for every
sufficiently small $\eta$. The10060/0 uniform law bounds $M_D$.
Choose any sequence $\eta_n\downarrow0$ and competitors within
$1/n$ of their normalized supremum. From the bounded profiles, take
a subsequence converging to $v\in\mathcal S$. By (3) and (9),
$\mathcal K(v)\le D$. Equations (19)--(21), or simply (12) when
$D\ge K_E$, give $|J_3(v)|\le H^{3/2}g(z_D)$. The uniform law (10)
then bounds that subsequence's normalized motion by (5). A hypothetical
larger $\limsup$ would yield precisely such a contradictory subsequence.
The actual families in (22), or the fixed endpoint families for larger
budgets, give the matching $\liminf$. Thus the full limit exists and
equals (5).

For equality rigidity, take a sequence in the statement and ANY
convergent profile subsequence. When $D\le K_E$, (10) forces
$|J_3(v)|=H^{3/2}g(z_D)$. At this cubic level, (19) gives
$\mathcal K(v)\ge D$, whereas (9) and the actual cut give
$\mathcal K(v)\le D$. Equality in (18)--(19) therefore forces
$v\in\mathcal E(z_D)$, and (9) together with the upper cut gives
(7) along that subsequence. If either convergence to the orbit or (7)
failed for the original sequence, boundedness would yield a contradicting
convergent profile subsequence. This proves both full-sequence assertions.
For $D>K_E$, equality forces the maximum of (12), the endpoint orbit;
(9) then gives the prior $\liminf$ cost $\ge K_E$.

Finally $P'(0)=30\alpha+81\tau=81\kappa>0$. The ordinary analytic
inverse at zero gives $z_{B_*+\delta}=\delta/(81\kappa H^2)+O(\delta^2)$,
and $g(z)=9\sqrt z(1+O(z))$. Substitution into (5) proves (8).
This is a second limit in the budget parameter after the fixed-$D$
polynomial limit; no exchange or simultaneous limit is assumed.

## Exact corroboration and unresolved scope

[curve.py](curve.py) expands all eight candidate moments directly,
compares every rational polynomial coefficient, checks the three-gradient
minor, the two repeated-outer Hessian signs, ALL21 ordered three-value
count cases and ALL seven two-value cases. It verifies the entire cost
derivative, endpoint and quadratic-gap factor, the nine inherited
harmonic maps, all physical-embedding sign bounds and the coefficient
in (22). [verify.py](verify.py) checks the entire typed record and source
manifest; [validate.py](validate.py) also rejects mathematical, fixture
and source damage in normal, optimized and cold source-only runs.

Optional source-pinned baseline comparison reads the entire parent
fixtures and compares EVERY coefficient of ALL nine10060/0 harmonic
maps and the ENTIRE10036 least-profile cost polynomial. This is useful
reproduction only, not new research or an independent parent-theorem replay.
The ordinary proof depends on (9)--(11), whose exact scope and review
status are stated above. Finite identity checks are not a formal proof
of the calculus or actual-family bridges. No global FIRST-power proof,
effective collar, finite-$\eta$ optimizer, simultaneous shrinking-budget
law, exact minimum-budget existence, or fixed zero-slack endpoint repair
is asserted.
