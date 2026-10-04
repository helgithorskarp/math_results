# Independent real-mean construction and sharp repair stability

Actual author **six-reviewer-5**, role **independent mathematical reviewer**.
Target LEMMA10280, actual six-sendov-3/researcher. This is an ordinary,
unformalized proof and audit of the complete explicit construction and its
stated coupled real repair class. It assumes no arbitrary-competitor entry
theorem, universal fourth optimum, or earlier review verdict.

## Domain and explicit constants

A monic polynomial of degree nine is actual if all nine original roots
are in the closed unit disk and the marked root is \(a=1-\eta\).
The objective \(F=\sum_{p'(\zeta)=0}|a-\zeta|^{-1}\) counts all eight
critical multiplicities; a collision gives infinity. The following
families have no such collision for sufficiently small positive \(\eta\).
Set \(c=\cos(\pi/9)\), so \(8c^3-6c-1=0\), and put
\[
\begin{gathered}
y=\frac1{3(1+c)},\quad x=\frac23-y,\quad H=14y,
\quad \rho=(c-5)/3,\\
u_z=(-8x+\rho H)/8,\quad u_p=u_z-\rho H/2,\\
w_2=\frac18\left(\frac{2512}{27}+\frac{5840}{9}c-
\frac{21392}{27}c^2\right),\quad
\Gamma=\frac{13}{36}+\frac{1253}{72}c-\frac{50}{3}c^2,\\
m_0=-\frac{17403419}{34992}-\frac{45702565}{17496}c+
\frac{180635}{54}c^2,\\
b_0=-\frac{1162307}{23328}-\frac{5484833}{11664}c+
\frac{52426519}{93312}c^2,\\
M_0=\frac{8148040331}{629856}+\frac{78878749667}{1259712}c-
\frac{51194418673}{629856}c^2,\\
\beta_0=\frac{27821775167}{17915904}+\frac{80418819893}{8957952}c-
\frac{12650091319}{1119744}c^2.
\end{gathered}
\]
The credited comparison constants, rechecked here by the explicit scalar
formula rather than an inherited lower theorem, are
\[
\begin{gathered}
C=8/3+y,\quad
B_*=\frac{2311}{108}+\frac{4934}{27}c-\frac{1976}{9}c^2,\\
T_*=-\frac{60800959}{17496}-\frac{307083769}{17496}c+
\frac{10980067}{486}c^2,\\
G_* =\frac{183619658945}{2519424}+
\frac{444829186913}{1259712}c-\frac{288729410449}{629856}c^2,\\
M_3(\eta)=8+C\eta+B_*\eta^2+T_*\eta^3.
\end{gathered}
\]
For an unrestricted real parameter \(\mu\), define
\[
\begin{aligned}
m(\mu)&=m_0+\frac{56}{9}(c-c^2)\mu,\\
b(\mu)&=b_0+(1/2+2c)\mu,\\
\widehat M(\mu)&=M_0+
\left(-\frac{51583}{972}-\frac{175385}{486}c+448c^2\right)\mu,\\
\widehat\beta(\mu)&=\beta_0+
\left(\frac{1771}{324}-\frac{94039}{1296}c+
\frac{12347}{162}c^2\right)\mu+
\frac27(1+c)\mu^2.
\end{aligned}
\]
The new family has real centers
\[
\begin{aligned}
A&=u_z\eta+(w_2-\mu/3)\eta^2+m(\mu)\eta^3+
\widehat M(\mu)\eta^4+\eta^{9/2},\\
B&=u_p\eta+(w_2+\mu)\eta^2+m(\mu)\eta^3+
\widehat M(\mu)\eta^4+\eta^{9/2},\\
K_\eta&=i[1+\Gamma\eta+b(\mu)\eta^2+
\widehat\beta(\mu)\eta^3],\\
p'(z)&=9(z-A)^6[(z-B)^2-(H/2)\eta K_\eta^2],\qquad
p(z)=\int_{1-\eta}^{z}p'(w)\,dw.
\end{aligned}
\]
Its critical multiset consists of six copies of \(A\) and the two
opposite imaginary points \(B\pm\sqrt{H/2}\sqrt\eta K_\eta\).
The degree is nine and the primitive is monic with the exact anchor.
The order-two real changes have sum \(6(-\mu/3)+2\mu=0\)
and zero mixed product with the leading opposite imaginary pair.
Those identities alone do not pay the higher normal constraints:
the displayed changes in \(m,b,\widehat M,\widehat\beta\) are essential.

## Independent finite reduction

Write \(\epsilon=\sqrt\eta\), \(W=e^{i\pi/18}\),
\(\omega=W^4\). Our exact coefficient field is
\(\mathbb Q[W]/(W^{12}-W^6+1)\), with all twelve rational
coordinates compared. Here \(i=W^9\),
\(c=(W^2+W^{34})/2\), and conjugation is \(W\mapsto W^{-1}\).
It differs from the author's ninth-cyclotomic representation.

We form the literal degree-eight derivative by multiplying all six
linear factors and the displayed quadratic; integration and subtraction
at the actual anchor give all ten primitive columns. A separate route
uses the eight critical power sums
\[
P_k=6A^k+2\sum_{r=0}^{\lfloor k/2\rfloor}
\binom{k}{2r}B^{k-2r}[(H/2)\eta K_\eta^2]^r
\]
and Newton's recurrence
\(E_n=n^{-1}\sum_{k=1}^n(-1)^{k-1}E_{n-k}P_k\).
All nine derivative columns agree as entire jets.

For each of the nine original labels \(j\), expand at \(o=\omega^j\).
If \(T_m=[u^m]p(o+u)\), the fixed-point coefficient contraction is
\[
d\longmapsto-\frac{o}{9}
\left[T_0+(T_1-9o^8)d+\sum_{m=2}^{5}T_md^m\right].
\]
All perturbations start in degree two. The map raises the error valuation
by at least two, so six iterations determine every coefficient through
\(\epsilon^{10}\). The omitted \(d^6\) starts in degree twelve.
We separately compose the complete primitive with the resulting root
and verify every coefficient of \(p(o+d)=0\). This route differs from
the author's sequential coefficient recursion; no author fixture or
program supplies the answer.

All symbolic comparisons retain the entire polynomial in \(\mu\),
whose degree is at most two in these jets. For the general fourth repairs,
two separate affine coordinates are encoded by formal powers three and
four. Their products first occur in degree sixteen; a mixed mean/repair
term first occurs in degree twelve. Hence these powers cannot alias a
mean monomial or one another through degree ten. This is a proved finite
degree reduction, not sampling real parameter values.

The complete regenerated record includes both ordinary and repaired
families, both primitive routes, all nine complete root/normal jets in
each family, and both actual repair columns at orders three and four at
each original label. [FRESH-BASE.json](FRESH-BASE.json) is our own freshly
generated compact evidence. [verify.py](verify.py) performs the coefficient
checks and compares the entire canonical record; a hash is not used as a
replacement for the mathematical comparisons.

## All nine original-root normals and actual containment

Let \(N_j=(|Z_j|^2-1)/2\), and set
\(A_j=1-\cos(2\pi j/9)\), \(B_j=1-\cos(4\pi j/9)\).
The independent first original displacement is
\(-\omega^j/3-x-y\omega^{-j}\), giving
\[
[\eta]N_j=-\left(1/3+x\cos(2\pi j/9)+y\cos(4\pi j/9)\right).
\]
The active labels are exactly \(3,4,5,6\). The other five first
half-normals are strictly negative, including the actual anchor:
label zero has \(-1\); labels \(1,8\) have
\(-(2+4c-4c^2)/3\); labels \(2,7\) have
\(-(2c-1)^2/3\). All signs are paid on the physical cubic branch.

At each active label separately, every coefficient through
\(\epsilon^8\) is zero and the coefficient in degree nine is \(-A_j\).
Here \(A_3=A_6=3/2\), \(A_4=A_5=1+c\), both positive.
Thus
\[
N_j=-A_j\epsilon^9+O_K(\epsilon^{10})\quad(j=3,4,5,6).
\]
The other five normals have their strict negative degree-two term.
The root at label zero is checked to be the entire exact anchor, rather
than an omitted formal branch.

The polynomial coefficients are polynomial in \(\epsilon,\mu\).
At zero the primitive is \(z^9-1\), with nine distinct simple roots.
Fix disjoint neighborhoods of them. The complex implicit-function theorem
gives nine branches jointly analytic on a common neighborhood of
\(\epsilon=0\) and any fixed compact real \(\mu\) set. One can cover
that set by finitely many parameter neighborhoods and choose the minimum
collar; uniqueness glues the local branches. Uniform Taylor remainders
then make all nine normals negative for small positive \(\eta\).
The branches stay simple and exhaust degree nine. This is a common
existence collar, with no asserted numerical collar or unbounded-parameter
uniformity. Each critical distance tends to one; the pair scale remains
nonzero. Thus all eight critical terms and their multiplicities are paid.

## Full scalar cost and strict improvement

On the same collar \(a-A>0\), and the exact first-power objective is
\[
\frac6{a-A}+\frac2{\sqrt{(a-B)^2+(H/2)\eta|K_\eta|^2}}.
\]
Expanding the two squared distances and the inverse square root gives
\[
F=M_3+G(\mu)\eta^4+8\eta^{9/2}+O_K(\eta^5),
\quad G(\mu)=G_*+L\mu+\frac43\mu^2,
\]
where
\[
L=-\frac{101920}{243}-\frac{1218245}{486}c+
\frac{251888}{81}c^2,
\quad \mu_*=-3L/8.
\]
The complete direct scalar jet, including all zero intermediate
coefficients and the degree-nine coefficient eight, is compared
independently of root recursion. Its positive square-root branch is
analytic near the constant one, so the remainder is compact-uniform.
The cubic imaginary moment is identically zero, with all multiplicities.

The physical cubic has a unique positive root and is bracketed by
\(15/16<c<47/50\). Exact rational bisection and full reconstruction
in the basis \(1,c,c^2\) certify \(L<0\), \(8<\mu_*<16\),
\(G_*<0\), and the strict improvement. Whole cubic reduction gives
\[
\begin{aligned}
G(\mu)&=G_{\rm mean}+\frac43(\mu-\mu_*)^2,\\
G_{\rm mean}&=G_*-\frac3{16}L^2\\
&=\frac{340367352475}{839808}+
\frac{808137564635}{419904}c-
\frac{1052841914857}{419904}c^2<G_*<0.
\end{aligned}
\]
The family at \(\mu_*\) is an actual witness, so for the actual
infimum \(\mathcal I(\eta)\),
\[
\limsup_{\eta\downarrow0}
\frac{\mathcal I(\eta)-M_3(\eta)}{\eta^4}\le G_{\rm mean}.
\]
This is an upper comparison. It excludes the old constructed \(G_*\)
as a prospective universal fourth lower coefficient, but proves no
universal lower coefficient or limit. Since \(C>0\), the constructed
small collar has \(F>8\); no global FIRST conclusion follows.

## Precisely coupled real repair class

Fix real \(\mu,M,\beta\). Replace \(\widehat M\) by \(M\) in both
centers, \(\widehat\beta\) by \(\beta\) in the imaginary bracket,
and allow real \(o(\eta^4)\) center remainders and a real
\(o(\eta^3)\) scale remainder. Keep the lower coefficients above,
including the coupled \(m(\mu),b(\mu)\), fixed as displayed.
Assume actual containment for every sufficiently small positive \(\eta\).
Write \(\delta M=M-\widehat M(\mu)\),
\(\delta\beta=\beta-\widehat\beta(\mu)\).

A common center change \(t\eta^q\) and scale change \(s\eta^{q-1}\)
give the primitive column \(9t(1-z^8)+(9H/7)s(z^7-1)\) at that
order. Composing at all nine \(\omega^j\) gives the half-normal column
\(-A_jt+(H/7)B_js\). Both orders \(q=3,4\) are independently checked.
Consequently the active fourth coefficients are
\[
q_j=-A_j\delta M+(H/7)B_j\delta\beta.
\]
The polynomial remainder is \(o(\eta^4)\); simple-root perturbation
preserves that order even without analytic remainders. Thus actual
containment forces \(q_3,q_4\le0\), and the conjugate labels give the
same two real rows. Their determinant is \(2c-1>0\).

Let
\[
w_4=(c+2c^2-1)^{-1},\quad
w_3=\frac23[7-(2-2c^2)w_4].
\]
Both weights are positive and satisfy \(\sum w_jA_j=8\),
\(\sum w_jB_j=7\). The scalar fourth coefficient is exactly
\[
G_4=G(\mu)+8\delta M-H\delta\beta
=G(\mu)-w_3q_3-w_4q_4\ge G_{\rm mean}.
\]
Equality requires precisely \(\mu=\mu_*\),
\(\delta M=\delta\beta=0\). The displayed inward family belongs
to this class, since \(\eta^{9/2}=o(\eta^4)\), and attains the
coefficient. This proves sharpness in the specified class only.

## Proved sharp mean-gap and repair stability

Put \(a_j=-q_j\ge0\), \(\Delta=G_4-G_{\rm mean}\).
Then the complete gap decomposition is
\[
\Delta=\frac43(\mu-\mu_*)^2+w_3a_3+w_4a_4.
\]
In particular
\[
|\mu-\mu_*|\le\sqrt{3\Delta/4},\qquad
0\le a_j\le\Delta/w_j.
\]
Write \(e=w_3a_3+w_4a_4\le\Delta\), and
\(t=(H/7)\delta\beta\). Inverting the two rows gives
\[
t=\frac{a_4-(2/3)(1+c)a_3}{c+2c^2-1},\qquad
\delta M=2a_3/3+t.
\]
For \(e>0\), \((\delta M,t)/e\) is a convex combination of
\[
v_3=\left(\frac{2(c-1)}{16c-9},-rac1{16c-9}\right),
\qquad v_4=(1,1),
\]
with weights \(w_3a_3/e,w_4a_4/e\). The inverse identities,
unit costs, both vertex deficits, and strict bounds on both coordinates
of \(v_3\) are checked exactly. For \(e=0\) both repairs vanish.
It follows that
\[
|\delta M|\le e\le\Delta,\qquad
\frac H7|\delta\beta|\le e\le\Delta.
\]
These constants and two rates are sharp at coefficient level. The
square-root mean constant is attained with zero repair deficits and
\(\mu=\mu_*\pm\sqrt{3\Delta/4}\), using the actual target family.
The linear repair constants are simultaneously attained on \(v_4\)
with \(\mu=\mu_*\). Adding the same fixed positive degree-nine
inward motion to that real repair ray pays its zero fourth normal;
its other fourth normal is negative. The remaining five first normals
are unchanged. Thus these equality examples are actual small-collar
members of the same class, not merely formal cone points.

No finite-\(\eta\) arbitrary-competitor stability, complete fourth model,
shrinking-skew optimum, or effective collar is implied by these bounds.
All IFT, collar, remainder and decoding arguments are ordinary written
mathematics, outside a formal proof kernel.
