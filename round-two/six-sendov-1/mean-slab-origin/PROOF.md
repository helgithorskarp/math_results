# Origin coercivity on a larger real mean interval

Actual author **six-sendov-1**, role **researcher**, 2026-10-01.
Complete ordinary author proof with exact finite checks; unformalized;
independent review of this extension pending.
The radial-defect theorem8656 is an explicit mathematical dependency;
its independent review remains pending. This is a subsequent extension,
not an amendment of the committed mean-tube or weighted-phase statements.

## 1. Statements and notation

Let \(1-10^{-5}\le a<1\), \(q_1,\ldots,q_8\in\mathbb C\),
\(\mu=\frac18\sum|q_j|\le1\), and \(m=\frac18\sum q_j\) with
\(\Re m\ge a\). Put
\[
 R=|m|,\quad \delta=1-a,\quad
 \eta_j=q_j/m-1=u_j+iv_j,\quad
 |u_j|\le h:=1/4,\quad U=\sum u_j^2,\quad V=\sum v_j^2.
\]
The mean is nonzero and \(\sum u_j=\sum v_j=0\). Then
\[
 \boxed{N_a(q):=
 \frac{|9\int_0^1\prod_j(1-atq_j)dt|^2}{\prod_j|q_j|^2}
 \ge1+\delta+\frac1{40}U+\frac1{16}V>1.}                 \tag{1}
\]
There is no imposed bound on the imaginary deviations; the modulus budget
forces the small transverse energy needed below. No polar, individual disk,
second-moment, original-root or multiplicity premise is used in (1).
All coordinates are nonzero since \(1+u_j>0\).

For \(1-5\cdot10^{-6}\le a<1\), the relaxed system
\[
 \sum|q_j|\le8,\quad |C_a(q)|\ge1,\quad N_a(q)\le1,\quad
 2a\Re q_j+(1-a^2)|q_j|^2\ge1\quad(1\le j\le8),          \tag{2}
\]
with \(C_a(q)=\int_0^1\prod_j[a+(1-a^2)tq_j]dt\),
has no eight nonzero complex coordinates. Consequently every degree-nine
disk-root polynomial has strict critical reciprocal sum greater than eight
at each marked root \(1-5\cdot10^{-6}\le|\alpha|<1\).
Critical multiplicities are counted; a collision gives infinity.

The abstract interval theorem enlarges the relative-real-deviation domain
near the boundary. The earlier theorem8591 has the broader a interval and
stronger radial coefficient on its smaller complex tube; both scopes retain
their credit. No optimal interval/annulus, unconditional linear reciprocal
surplus, or full first-power endpoint is asserted.

## 2. The modulus mean forces a small transverse energy

Write \(\rho_j=|1+\eta_j|\) and \(d_j=\rho_j-(1+u_j)\ge0\).
Since \(a\le R\le\mu\le1\) and the real deviations balance,
\[
 D:=\sum d_j=8(\mu/R-1)\le8\delta/a.
\]
The exact identity \(v_j^2=2(1+u_j)d_j+d_j^2\) implies
\[
 V\le2(1+h)D+D^2\le20\delta/a+64\delta^2/a^2.
\]
At \(\gamma=10^{-5}\) this is at most
\(2000044/9999800001<\nu:=1/4000\).
Also \(U\le8h^2=1/2\), \(\max|\eta_j|^2\le h^2+V< H^2\), \(H=1/3\).
For \(z=am\),
\[
 |1-z|^2=1-2a\Re m+a^2R^2\le1-a^2,
 \qquad s_a:=\sqrt{1-a^2}\le s:=1/128.
\]
The last comparison follows from \(2\gamma<s^2\).

A more precise modulus payment, which does not replace every u by h, is
\[
 d_j=\frac{v_j^2}{\rho_j+1+u_j}
 \ge\frac{v_j^2}{2}-\frac{u_jv_j^2}{2}
                       -\frac{v_j^4}{8(1-h)}.           \tag{3}
\]
Indeed \(\rho_j\le1+u_j+v_j^2/[2(1-h)]\), and convexity of
\(x\mapsto1/x\) gives its tangent lower bound at2. The denominator in
this application is positive. Summing and using
\(\sum u_jv_j^2\le\sqrt U\,V\), \(\sum v_j^4\le V^2\), yields
\[
 1-R\ge R\left(\frac V{16}-\frac{\sqrt U\,V}{16}
                                -\frac{V^2}{64(1-h)}\right). \tag{4}
\]
For \(a\le R\le1\), \(1-R^{18}\ge18a^{17}(1-R)\).
With \(\lambda=(9/8)a^{18}\), (4) therefore gives
\[
 1-R^{18}\ge\lambda\left(V-\sqrt U\,V-\frac{V^2}{3}\right). \tag{5}
\]
If the bracket is negative, (5) follows instead directly from
\(1-R^{18}\ge0\). This avoids multiplying a negative lower bound by a
smaller power of R. Finally
\(\lambda_-\le\lambda\le9/8\), with
\(\lambda_-=(9/8)(1-18\gamma)=449919/400000\).

## 3. Exact origin normalization and the real reference configuration

Let \(e_k\) be elementary symmetric polynomials in eight deviations and
\[
 B_k(z)=9(-1)^k\int_0^z t^k(1-t)^{8-k}dt,\quad
 b_k=B_k(1)=(-1)^k/\binom8k,\quad d_k=b_k-1.
\]
Polynomial primitives are path independent. Let
\(P(\eta)=\prod(1+\eta_j)\), and
\[
 K_z(\eta)=\frac{\sum_{k=0}^8 B_k(z)e_k(\eta)}{P(\eta)}.
\]
Expansion of the eight origin factors gives exactly
\[
 K_z=am^9\,9\int_0^1\prod_j(q_j^{-1}-at)dt,\qquad
 N_a(q)=|K_z|^2/(a^2R^{18}).                            \tag{6}
\]
At \(z=1\), because \(e_1=0\),
\[
 K_1(\eta)=1+\frac{D(\eta)}{P(\eta)},\qquad
 D(\eta)=\sum_{k=2}^8d_ke_k(\eta),\quad d_2=-27/28.
\]
This D is an auxiliary numerator, distinct from the radial Newton defect
\(D_a(r)=2ae_2((1+a)r-1)-e_3((1+a)r-1)\).

Put \(P_0=P(u)\). Concavity of log above the chord on[-h,h], and
\(\sum u_j=0\), gives
\[
 p:=(1-h^2)^4=50625/65536\le P_0\le1.
\]
The real reference radii \(r_j=1+u_j\) have sum8 and minimum3/4.
The radial theorem8656 at a=1 gives
\[
 K_1(u)-1
 =\frac{O_1(r)-P_0}{P_0}
 \ge\frac{5}{256P_0}\left(2-\frac U7\right)U
 \ge\frac3{80}U.                                      \tag{7}
\]
Here \(e_2(2r-1)=28-2U\) and Maclaurin gives the radial defect
at least \(e_2U/14\). The exact scalar comparison is
\(5(2-(1/2)/7)/256=135/3584>3/80\).

Balanced Newton identities and the standard pair-energy bound give
\[
 |e_3(u)|\le hU/3,\quad |e_4(u)|\le(5/4)h^2U,\quad
 |e_k(u)|\le\binom8k h^{k-2}U/8\ (5\le k\le8).
\]
The pair-energy bound follows by bounding each product by h to the remaining
powers times its average pair product, then
\(|x_ix_j|\le(x_i^2+x_j^2)/2\). This argument also applies to subsets and
does not require their balance.
Set
\[
 c=27/56,\quad M=9/8=\max_{2\le k\le8}|d_k|,\quad
 L=h/3+(5/4)h^2+\sum_{k=5}^8\binom8k h^{k-2}/8=28067/98304.
\]
Then, with \(k_0=K_1(u)-1\),
\[
 0\le1-P_0\le M_0U,\quad M_0=1/2+L,
 \qquad0\le k_0\le K_hU,\quad K_h=(c+ML)/p=491381/472500. \tag{8}
\]

## 4. Separate real and imaginary perturbation bounds

Let
\[
 P(\eta)=P_0+\alpha+i\beta,\qquad
 D(\eta)=D(u)+\zeta+i\xi,\qquad T=\sum u_jv_j.
\]
The full balanced degree-two/three/four identities are
\[
 \Re e_2=-U/2+V/2,\quad \Im e_2=-T,
\]
\[
 \Re e_3-e_3(u)=-\sum u_jv_j^2,\quad
 \Im e_3=\sum u_j^2v_j-\tfrac13\sum v_j^3,
\]
\[
 \Re e_4-e_4(u)
 =-UV/4+V^2/8-T^2/2+(3/2)\sum u_j^2v_j^2-\tfrac14\sum v_j^4,
\]
\[
 \Im e_4=(U-V)T/2-\sum u_j^3v_j+\sum u_jv_j^3.
\]
The checker reconstructs every coefficient with seven independent u and
seven independent v, and separately checks Newton's identities.
Thus the degree-three real correction is at most \(\sqrt U\,V\),
the degree-four correction at most \(9UV/4+3V^2/8\), and their imaginary
parts at most \(h\sqrt{UV}+V^{3/2}/3\) and
\((5h^2+3\nu/2)\sqrt{UV}\), respectively.

For k>=5, expand \(e_k(u+iv)\) by its number of selected v coordinates.
The quadratic-v real correction is at most
\[
 r_{2,k}UV,\qquad r_{2,k}=(7/12)\binom6{k-2}h^{k-4}.
\]
Use the pair-energy estimate on the six remaining u coordinates and
\(\sum_{i<j}|v_iv_j|\le(7/2)V\).
The real terms with even v-degree p>=4 are at most
\[
 r_{4,k}V^2,\quad
 r_{4,k}=\sum_{\substack{4\le j\le k\\j\ {\rm even}}}
 \frac{\binom8j\binom{8-j}{k-j}}8h^{k-j}\nu^{(j-4)/2}.
\]
The imaginary term of v-degree one is at most
\((8/7)\binom7{k-1}h^{k-2}\sqrt{UV}\).
Use pair energy on the seven remaining u coordinates,
\(\sum|v_j|\le\sqrt{8V}\), and \(\sqrt U\le\sqrt8h\).
The imaginary terms of odd v-degree j>=3 are bounded by the corresponding
sum with factor \(\nu^{(j-3)/2}V^{3/2}\).
These count all disjoint coordinate selections; the finite checker verifies
both binomial counting formulas and independent subset enumeration.

Set \(r_{2,4}=9/4,\ r_{4,4}=3/8\), and
\[
 A_P=\sum_{k=4}^8r_{2,k},\quad B_P=\sum_{k=4}^8r_{4,k},
 \quad A_D=\sum|d_k|r_{2,k},\quad B_D=\sum|d_k|r_{4,k}.
\]
Then
\[
 |\alpha-V/2|\le\sqrt U\,V+A_PUV+B_PV^2,
\quad |\zeta+cV|\le|d_3|\sqrt U\,V+A_DUV+B_DV^2.         \tag{9}
\]
With
\[
 A_I=1+h+5h^2+3\nu/2+\sum_{k=5}^8(8/7)\binom7{k-1}h^{k-2},
\]
\[
 B_I=\tfrac13+
 \sum_{k=5}^8\sum_{\substack{3\le j\le k\\j\ {\rm odd}}}
 \frac{\binom8j\binom{8-j}{k-j}}8h^{k-j}\nu^{(j-3)/2},
\]
we have
\[
 |\beta|\le I:=A_I\sqrt{UV}+B_IV^{3/2},\qquad|\xi|\le MI.
\]
Since \(\sqrt U\le3h\), \(|\alpha|\le C_\alpha V\), where
\(C_\alpha=1/2+3h+A_P/2+B_P\nu\).
The exact comparison \(C_\alpha\nu<p\) ensures
\(\Re P(\eta)>0\); also \(|P(\eta)|\ge P_0\) factor by factor.
Hence \(0<\Re(1/P)\le1/P_0\) and
\(|\Im(1/P)|\le|\beta|/P_0^2\).

Now
\[
 K_1(\eta)-K_1(u)
   =\frac{(\zeta-k_0\alpha)+i(\xi-k_0\beta)}{P(\eta)}.
\]
Using(8)--(9), \(I^2\le2A_I^2UV+2B_I^2\nu V^2\), and
\(1/P_0-1\le M_0U/p\), gives
\[
 \Re K_1(\eta)\ge K_1(u)-cV-A\sqrt U\,V-BUV-CV^2,       \tag{10}
\]
where
\[
 A=|d_3|/p<2,\quad
 B=\frac{cM_0+A_D+K_hC_\alpha}{p}
              +\frac{2(M+K_h/2)A_I^2}{p^2}<50,
\]
\[
 C=B_D/p+\frac{2(M+K_h/2)B_I^2\nu}{p^2}<30.
\]
Every coefficient here is rational and included in the complete fixture.
This bound keeps the radial real reference intact and puts all mixed error
into \(\sqrt U\,V,\ UV,\ V^2\). It does not bound the error by a multiple
of U+V before paying for transverse deviations.

## 5. Incomplete-beta flatness and coercivity

The polynomial derivatives give
\[
 |B_0(z)-1|\le s_a^9,\quad
 |B_k(z)-b_k|\le t_k=9(1+s)^ks^{9-k}/(9-k).
\]
With H=1/3 and S=U+V, the balanced elementary bounds are
\( |e_2|\le S/2,\ |e_3|\le HS/3,\ |e_4|\le(5/4)H^2S\),
and \(|e_k|\le\binom8k H^{k-2}S/8\) for k>=5.
Writing their respective coefficients as \(\ell_k(H)\), the exact check is
\[
 \frac{\sum_{k=2}^8t_k\ell_k(H)}p
 =808701963469051/44332308831928320000<1/10000.
\]
Therefore \(|K_z-K_1|\le2s_a^9+(U+V)/10000\).
Combining(7),(10) and \(|K_z|^2\ge2\Re K_z-1\) gives
\[
 |K_z|^2\ge1+(3/40-1/5000)U-(27/28+1/5000)V
                 -4\sqrt U\,V-100UV-60V^2-4s_a^9.
\]
Add the payment(5), use \(V\le\nu\), and bound
\[
 (41/8)\sqrt U\,V\le(3/125)U+(210125/768)V^2.
\]
The remaining exact energy coefficients are
\[
 a_U=3/40-1/5000-100\nu-3/125=129/5000>1/40,
\]
\[
 a_V=\lambda_- -27/28-1/5000-(256493/768)\nu
                       =41297341/537600000>1/16.
\]
Consequently
\[
 |K_z|^2\ge R^{18}+U/40+V/16-4s_a^9.
\]
Since \(R^{18}\ge a^{18}\ge1-18\gamma>1/2\), \(a^{-2}<2\),
\(a^{-2}\ge1+2\delta\), and
\(s_a^9\le(2\delta)^4/128=\delta^4/8\), (6) yields
\[
 N_a(q)\ge1+2\delta-2\delta^4+U/40+V/16
               \ge1+\delta+U/40+V/16.
\]
The final comparison uses \(2\gamma^3<1\). This proves(1).

## 6. Joint-channel exclusion on a larger annulus

Under(2), the individual disks give \(1/(1+a)\le r_j=|q_j|<9/2\).
Write \(\mu=\frac18\sum r_j\) and \(V_r=\sum(r_j-\mu)^2\).
The mean lemma8533 supplies \(x=\Re m>a+(2/5)\delta/[a(1+a)]\).
Thus, with \(\Delta=\sum(r_j-\Re q_j)\) and
\(\epsilon=\sum|q_j-r_j|\),
\[
 \Delta<32\delta/5,\quad\epsilon^2<512\delta/5,\quad
 \sum|q_j-r_j|^2<288\delta/5.
\]
The finite polar variance derivation in8656, equation(15), retains
\[
 V_r/8\le\frac{1+24\delta+37500\delta^2}{1-30\delta}
 \le\frac{160039}{159952}\qquad(\delta\le\gamma).
\]
The written derivation of that fraction applies for delta<=1/100; its
previous selected gamma was1e-6. Evaluating it at gamma1e-5, the centered
identity now gives
\[
 e_2((1+a)r-1)>
 28(1-3\gamma)^2-16(160039/159952)
 =299650513229811/24992500000000>119/10.
\]
Thus the same inherited Newton argument gives
\(D_a(r)>(17/20)V_r\) when \(V_r>0\), and the radial gap is
\(O_a(r)-\prod r_j>(17/1024)V_r\).

If all \(|\Re(q_j/m-1)|\le1/4\), theorem(1) gives N>1.
Otherwise \(\sum|q_j-m|^2>a^2/16\), while
\(\sum|q_j-m|^2\le2V_r+2\sum|q_j-r_j|^2\).
For \(\delta\le1/200000\),
\[
 V_r>a^2/32-(288/5)\delta
 \ge1/32-(288/5+1/16)\delta
 \ge495387/16000000>0.
\]
Here epsilon<3/125. The adaptive rational phase estimate8707 therefore
has mixed derivative cap \((6/5)/(1-6/125)=150/119\), giving phase loss
at most
\[
 (3/2)\Delta+(75/119)\epsilon^2<(44112/595)\delta.
\]
At the largest allowed delta, the remaining radial gap is
\[
 \Re O_a(q)-\prod r_j>
 \frac{8421579}{16384000000}-\frac{2757}{7437500}
 =\frac{279436893}{1949696000000}>0.
\]
This contradicts N<=1 in the remaining branch. Classical origin/polar
communication identities and Gauss--Lucas give(2) for polynomial
reciprocals under a hypothetical first-power failure, proving the stated
polynomial consequence. These identities are attributed to the primary
Zhang manuscript, Lemma3.1.

## 7. Evidence and trust boundary

The exact checker reconstructs all six real/imaginary component identities
as full sparse polynomials in fourteen independent real variables, then
checks all six Newton components by a separate power-sum route. It rebuilds
all ninety coefficients of the nine B polynomials in two routes, every
one of the forty-two mixed-support counts in an independent subset census,
and twenty-six rational comparisons. Eight Gaussian-rational controls check
direct origin integration against the normalized primitive formula and the
coercive inequality. Four damaged polynomial identities and six damaged
fixtures are rejected in both normal and optimized Python; default runs
change no source or fixture bytes. The control profiles are checks, not the
universal analytic proof.

The controls also include configurations outside the primary centered
argument's second-moment premise. For instance, at a=99999/100000,
m=a+i/2000, and four real deviations1/4 and four-1/4, the modulus mean
is |m|<1 and the real mean is a, but
mean|q|^2=(17/16)|m|^2>1. This is an abstract configuration covered by(1),
not a claim that it is admissible as an original disk-root polynomial.

The product/chord argument, mixed support inequalities,
modulus payment, complex reciprocal denominator, flatness and inherited
radial/communication arguments are ordinary written mathematics.
The finite author checks constitute neither independent review nor
formalization. The checker imports no external source, uses no floating-point
proof input or solver, and omits no computational certificate. The inherited
radial theorem, mean lemma and weighted-phase estimate keep their explicit
source and review status in LITERATURE.md. The global endpoint remains open.
