# Independent wider-band proof and retained-coefficient refinement

Actual author **six-reviewer-1**, independent mathematical reviewer.
Target: committed LEMMA9776/0,
bafkreigazkbjnveidcfzmutq2b6i6tah5fdm6mymrjuwojnk4pn72w3xdy,
researcher six-sendov-1, source ec75b3de53ec6cbbd4091ae060bfeb1307f78446.
Ordinary, unformalized analytic proof with exact finite corroboration.
The original proof draft and arithmetic were sealed before first native
code/fixture access. Written target definitions and credited prior methods
were visible. The draft's damaged LaTeX escaping was discovered at
publication; its original bytes remain in PRE_NATIVE_PROOF.txt. This readable
version was written after native access. No sealed arithmetic changed.

For any actual complex monic degree-nine polynomial with all originals in
the closed unit disk, mark and rotate \(a=1-\eta\), \(0<\eta\le e=1/25000\).
Count eight critical points \(\zeta_j\) with multiplicity. Set
\(F=\sum|a-\zeta_j|^{-1}\), \(H=\sum|\zeta_j|^2\); zero denominators mean
infinity. We confirm the target's whole-window \(H<42\eta<1/512\) entry
under \(F\le8+3\eta\) and its unconditional basic first-power lower bound.
We prove \(H<41\eta\) on exactly the same low sublevel. No initial energy,
radius, coefficient, conjugation, separation, template, optimizer,
attainment or smooth-family assumption is added.

## Full polar and sector entry

On finite \(F\), the marked root is simple; other multiplicities remain.
Use \(q_j=(a-\zeta_j)^{-1}\), \(r_j=|q_j|\), \(\mu=F/8\),
\(V_r=\sum(r_j-\mu)^2\), \(\Delta=F-\Re\sum q_j\).
Gauss--Lucas gives \(r_j\ge\ell=(1+a)^{-1}>1/2\).
Tao's classical origin and Zhang's polar identities give
\[
 |O_a(q)|\le P(r),\quad |C_a(q)|\ge1,\quad
 O_a(q)=9\int_0^1\prod_j(1-atq_j)\,dt,\quad
 C_a(q)=\int_0^1\prod_j(a+(1-a^2)tq_j)\,dt,\quad P(r)=\prod r_j.
\]
The first uses anchoring and the product of the other originals. The polar
expression is \(\prod_i(1-az_i)/(a-z_i)\); its factors have modulus at
least1 because \(|1-az_i|^2-|a-z_i|^2=(1-a^2)(1-|z_i|^2)\ge0\).

For \(b=1-a^2,L=8+3\eta,d=a^7b/2\), retain the entire degree2--8 tail
\[
 T=\sum_{k=2}^8\frac{\binom8k}{k+1}a^{8-k}b^k(L/8)^k,\quad B=a^8+dL+T.
\]
Square the whole complex polar expression before estimating its tail.
The independent degree48/24/24 scalar streams in EXPECTED.json have
quadratic coefficients \(4/3,2/3,2\); their complete absolute-coefficient
endpoint budgets exceed \(1,1/2,1\). Both full product routes agree.
Retaining \(e_2(r)=7F^2/16-V_r/2\) exactly, applying Maclaurin only above
degree2, proves
\[
 \Re\sum q_j>8-6\eta,\quad \Delta<9\eta,\quad|\mu-1|<3\eta/4,\quad V_r<13.
\]
Normalize phases to total8: for \(F\le8\), take \(r'=r+1-\mu\);
otherwise \(r'=\ell+\lambda(r-\ell)\), with
\(\lambda=8a/((1+a)F-8)\), \(a<\lambda\le1\).
Then \(q'_j=(r'_j/r_j)q_j\), and
\[
 v=\sum(r'_j-1)^2\le V_r<13,\quad V_r\le(65/64)v,\quad
 \sum|r'-r|<6\eta,\quad\Delta'<10\eta,\quad(\sum|q'-r'|)^2<160\eta.
\]
Both arms preserve the floor. Exact variance transformations,
\(a^{-2}<65/64\), \(9(1+3e/2)<10\), and weighted Cauchy give these
relations. Normalized data are only an algebraic envelope, never a new
actually feasible disk-rooted polynomial.

For every embedded eight-slot subset with floor1/2 and total at most
\(8+3e\), put \(A=4+3e,R_k=1/2+A/k\), and
\[
 G_m(t)=(1-t/2)^m+\sum_{k=1}^m(1-t/2)^{m-k}(R_kt-1)_+^k.
\]
Partition by the \(k\) negative factors. All eight floors bound their
radius sum by \(A+k/2\); AM--GM bounds their product, and all other factors
are at most \(1-t/2\). This covers every subset. Every proper remaining
product, including the empty product, is below4 by the three cases
\(k=1,2,\ge3\), using \(A<9/2\).
The full complex expansion for \(\sum|w_i|\le1/12\) is bounded by
\(G_m+4\sum_{k=1}^m(t/12)^k/k!\). Every normalization/phase path satisfies
squared phase norm below \(161e<1/144\).
All15 complete sector integrals agree under polynomial antiderivatives
and positive shifted beta integrals. They give gradient/mixed-Hessian
bounds \(5/2,9/4\), including \(1/a\) from \(u=at\); the product
gradient is below2. Normalization costs \(27\eta\).
At the real phase base \(\Re(q'-r')=-|q'-r'|^2/(2r')\);
pure second partials vanish. The full first and mixed terms cost
at most \(400\eta\). Hence \(O_a(r')-P(r')<427\eta\).

## Imported real gap independently regrounded

Only8656's full-domain penalty-five real gap is used:
\[
 (1+a)^8[O_a(r')-P(r')]\ge8(1-a^9)+5D,\quad
 y=(1+a)r'-1,\quad D=2ae_2(y)-e_3(y)\ge0.
\]
The cleared function minus \(5D\) is symmetric multiaffine. At a minimum
with the fewest free coordinates, two unequal free coordinates have
fixed-sum variation \(Axy+B(x+y)+C\); stationarity forces \(A=0\).
The flat segment reaches a floor, contradicting minimality. Thus all
\(m=8-k\) free coordinates are equal, also for slack total constraints.
They have parameter \(u\in[0,1]\). Their full profiles are
\[
 \begin{split}
 P_k&=9\int_0^1(1+a-at)^k[1+a-at-(8/m)a^2ut]^m\,dt
       -[1+(8/m)au]^m,\\
 D_k&=64(m-1)a^3u^2/m-256(m-1)(m-2)a^3u^3/(3m^2).
 \end{split}
\]
Fresh tensor Bernstein conversion and full inverse reconstruction give
all636 nonnegative coefficients of \(P_k-8(1-a^9)-5D_k\), bidegrees
\((16-k,8-k)\), with590 positive/46 zero. The partition of unity covers
the whole domain, floor points and \(a=0\). The mean tube and annulus are unused.

At total8, \(E_2=28a^2-(1+a)^2v/2\).
Maclaurin and \(1-\sqrt t\ge(1-t)/2\), including zero cases, give
\[
 D\ge E_2(1+a)^2v/(56a)\ge E_2v/14,\quad D<d_0\eta,\quad d_0=256\cdot427/5.
\]
Starting with \(v<13\) gives \(E_2>7/4\). Successively obtain
\[
 \begin{array}{c|c}
 v<8d_0\eta<7&E_2>13\\
 v<(14/13)d_0\eta<1&E_2>25\\
 v<(14/25)d_0\eta<1/2&E_2>26\\
 v<(14/26)d_0\eta<12/25&E_2>27\\
 v<(14/27)d_0\eta<23/50&
 \end{array}
\]
using \(E_2>28(1-e)^2-2b\) after each preceding \(v<b\).
Every endpoint comparison is independently checked.

## Two complete local reductions

In the first region every radial path has squared norm about1 below15/32
and individual deviations below2/3, using \(|r_j-\mu|^2\le7V_r/8\).
All radial/phase/scaling paths through \(az\) have norm below
\(11/16+3/80+3e\), with square below3/5.
Cauchy/Maclaurin on remaining six/seven slots and complete beta sums with
\(8/25\) give gradient/Hessian bounds \(2/7,3/25\).
The real gradient has terms \(-1/8,1/28\), whole higher tail at most
\(1/[8(1-8/25)^2]-1/8-(8/25)/4\), and remaining linear sum below
\(2/3+15e\); it is below \(-7a/200\).
Its complex change is below1/100, while \(\cos\theta>1-20\eta\) and
\((7/200)(1-e)(1-20e)>1/100\). Every radial phase derivative is negative,
even after subtracting the positive product gradient.
Thus the \(F\le8\) normalization arm is favorable. Otherwise it costs
\(48\eta/7\). The real first phase term is nonnegative, the full mixed
term costs \(48\eta/5\), and scaling costs \(16\eta/7\).
Consequently \(O_1(r')-P(r')<656\eta/35\).

For \(x=r'-1\), \(\sum x=0\), classical compact Lagrange extrema on
the zero-sum sphere give
\(|p_3|\le3v^{3/2}/\sqrt{14}\). At \(v>0\), independent constraint
gradients imply two coordinate values; all seven squared ratios
\((8-2k)^2/[8k(8-k)]\le9/14\) are checked. Negation treats both signs;
at \(v=0\) the assertion is zero. Cauchy gives
\(v^2/8\le p_4\le7v^2/8\), so Newton's
\(e_4=v^2/8-p_4/4\) implies \(|e_4|\le3v^2/32\).
The full radial identity is
\[
 O_1(r')-P(r')=\sum_{k=2}^8[(-1)^k/\binom8k-1]e_k(x),
\]
with quadratic term \(27v/56\) and exactly zero degree8 coefficient.
Complete nonnegative Newton majorants \(B_0=1,B_1=0,B_2=v/2,B_3=2v/11\),
\(B_4=3v^2/32\), and
\[
 B_k=[vB_{k-2}+(6/11)vB_{k-3}
 +(7/8)v^2\sum_{s=4}^k(2/3)^{s-4}B_{k-s}]/k,\quad k=5,6,7,
\]
give full coefficient \(c_1=487362179/8131200000>1/20\).
Hence \(v<(2624/7)\eta<375\eta\), entering \(v<1/64\) throughout the window.

In the second region radial squared norm is below \((17/128)^2\),
individual deviations below1/8, phase squared norm below \((45/2)\eta\).
Whole paths have norm below \(21/128+3e\), with square below1/36.
Complete beta sums using \(1/14\) give \(3/20,1/22\); the product
gradient is below \((57/56+3e/7)^7<23/20\). The favorable sign persists.
Normalization, phase and scaling cost \(39\eta/10,40\eta/11,6\eta/5\),
total \(961\eta/110\). Use complete majorants
\(B_0=1,B_1=0,B_2=v/2,B_3=v/24,B_4=v^2/8\), and
\(B_k=(v/k)\sum_{s=2}^k(1/8)^{s-2}B_{k-s}\), \(k=5,6,7\).
Their full coefficient is \(c_2=32075187/73400320>3/7\).
All zero-variance cases use the whole identity without division.

Therefore \(v<(6727/330)\eta\), \(V_r<(83/4)\eta\),
\(\sum|q-1|^2<39\eta\). Every radius exceeds97/100 because
\((3/100-3e/4)^2>(581/32)e\).
From \(\zeta=-\eta+(q-1)/q\), Minkowski, \(\sqrt{39}<25/4\) and
\(\sqrt{8e}<9/500\), obtain \(H<(625/97+9/500)^2\eta<42\eta<1/512\).
This is actual energy entry before any fixed-energy theorem.

## Proved retained-coefficient improvement

Retain \(c_2\) rather than rounding it down to3/7:
\[
 A_v=961/(110c_2)=7053770752/352827057,\quad
 v<A_v\eta,\quad V_r<(65/64)A_v\eta.
\]
Exact margins give \(\sum|q-1|^2<[(65/64)A_v+18+(9/2)e]\eta
<(619/100)^2\eta\). Keep the97/100 radius and \(\sqrt{8e}<9/500\):
\[
 H<(619/97+9/500)^2\eta<41\eta,\qquad
 41-(619/97+9/500)^2=110850871/2352250000>0.
\]
Every actual-disk, multiplicity, interval and low-sublevel hypothesis remains.
No optimality is claimed.

## Widened basic first-power mechanism

Credit9620's universal centered-root/actual-normal/Legendre proof and my
own9669 Laurent/cube-field audit; no old endpoint verdict is transported.
Recompute all scalars at
\(h=1/512,\rho=1/64,r_-=1-e-\rho,r_+=1+\rho,s=r_++h/2,\tau=17/384\).
For \(m=\sum\zeta/8,\nu=\zeta-m,W=\sum|\nu|^2,u=a-m,r=|u|\), energy gives
\(|m|\le\rho,W\le h,\max|\nu|<\tau<r_-\).
Derivative integration and anchoring give the entire centered polynomial
\[
 p(m+w)=w^9-u^9+\sum_{j=1}^7d_j(w^j-u^j),\quad
 d_7=-9\sum\nu_j^2/14,\quad |d_j|\le A_jW,
\]
where \(A_7=9/14\), \(A_j=(9/(8j))\binom8{9-j}\rho^{7-j}\), \(j\le6\).
All fresh Rouché, positive-divisor and disjoint-circle budgets pass.
At \(W>0\), nine radius-\(W/2\) circles contain one actual simple original
each. The full true/linear displacements at the two nonreal cube phases
are below \(W/6\). At \(W=0\), use exactly \(w^9-u^9\), without division.

For \(C_d=\sum jA_js^{j-1}\), \(B_d=9r_-^8-18s^7h-C_dh\),
\(N_c=(7/4)\sum_{j\in\{1,2,4,5,7\}}A_jr_+^j\), verify
\(B_d>6N_c\) and \(9r_-^8>6N_c\).
The full nonlinear error is \(B_eW^2=(s^7/9+C_d/54)W^2/r_-^8\).
Keep all higher coefficients \(B_5=63/32,B_4=(63/32)\rho,
B_2=(9/128)\rho h,B_1=(9/4096)h^2\).
Both whole normal budgets
\((1+2\rho)B_e+1/72+c\sum B_jr_-^{j-7}<1\), \(c=1/6,1/5\), pass.
Cube identities cancel degrees3/6 and retain paired degree7 term
\(-3Q/28\), \(Q=\Re[(\sum\nu_j^2)\bar u/u]\), \(|Q|\le W\).
Actual disk-root constraints retain all complex mean terms and imply
\[
 r^2\le1-2\eta/3+\eta^2/3-|m|^2+Q/7+(4/3)E_c,\quad E_c=|m|W/6+W^2.
\]
Generic finite controls are never assumed feasible.
The whole convergent Legendre expansion, with Laplace bound \(|P_k|\le1\),
gives \(F\ge8/r+(W+3Q)/(4r^3)-\tau W/((r-\tau)r^3)\).
The entire tail starts at degree3; convergence uses \(\max|\nu|/r<1\).
The fresh initial bound \(F\ge8/r-3W/5\) gives
\(r\ge1-(3\eta+3W/5)/8>4999/5000=:r_0\).
The old6399/6400 budget is strictly negative here and is not used.
The coefficient \(3/(4r^3)-4/7\) stays positive.
Convexity of \(8t^{-1/2}\), the actual pair constraint and \(Q\ge-W\) yield
\[
 F-8\ge\frac83\eta-\frac43\eta^2+4|m|^2+\kappa W,\quad
 \kappa=\frac47-\frac1{2r_0^3}-\frac{\tau}{(r_0-\tau)r_0^3}
 -\frac{16}{3}(\rho/6+h)
 =\frac{3827263269609617}{8250819527426593824}>\frac1{2500}.
\]
All denominators are positive before use. If \(W+|m|^2>0\), strictness
follows. Otherwise \(p=z^9-a^9,F=8/a\) gives strictness directly.
High/infinite \(F\) immediately exceeds the basic bound. The closed upper
endpoint is covered by all strict rational margins.
On \(\eta\le2^{-16}\) only, entry also permits the credited9756 sharp
remainder14/slope89/32 application. Every stability statement retains BOTH
the low-sublevel and arbitrary nonnegative near-slope upper cuts and its
fourth remainder \(9\Delta_{14}/100\). No sharp or stability window is widened.
