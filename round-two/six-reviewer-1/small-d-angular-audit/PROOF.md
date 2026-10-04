# Independent proof and larger effective angular collar

Actual author: **six-reviewer-1**, role: **independent mathematical reviewer**, 2026-10-04.
Ordinary proof, unformalized. This independently reconstructs the complete mathematical
claim in LEMMA10290 and proves the additional sufficient cutoff below.

Let \(x\in\mathbb R^8\), with all original coordinate multiplicities retained, satisfy
\[
\mu_1=\mu_3=\mu_5=0,\qquad\mu_2=1,\qquad D=\mu_4-1/8>0.
\]
Set \(e=\mathbf1/\sqrt8\), \(P=I-ee^T\),
\(H=P\operatorname{diag}(x)P|_{e^\perp}\), \(w=x/\sqrt8\).
For each distinct eigenvalue, use the full orthogonal eigenspace projection and put
\[
m_\lambda=8\|\Pi_\lambda w\|^2,\qquad
\eta_{\rm ang}=\sum_{\lambda\ {m distinct}}m_\lambda^2,
\qquad C=(1-\eta_{\rm ang})/D.
\]
The masses are nonnegative and sum to one, because \(w\in e^\perp\) and
\(8\|w\|^2=1\). Repeated eigenspaces are never split into basis-dependent masses.

**Proved refinement.** For every such vector with \(0<D\le1/625\), there are
exactly four positive and four negative coordinates and a simple central
compression eigenvalue \(\sigma\) satisfying
\[
|\sigma|<28D^{3/2}<1/480.
\]
Define
\[
s=\sqrt D,\qquad u(s)=\frac8{1-8s}+125000s^4,\qquad q=s^2u(s).
\]
Then
\[
\boxed{C<\frac{1-(1+q)^{-2}}D
=u(s)\frac{2+s^2u(s)}{(1+s^2u(s))^2}
\le\frac{1721799060000}{73311519121}
=\frac{47}{2}-\frac{2043278687}{146623038242}<\frac{47}{2}.}
\]
The displayed cutoff and root constant are sufficient, not asserted optimal.

## Uniform setup and odd cancellations

Write \(b=1/8\), \(\epsilon_i=x_i^2-b\). The moment equations give
\[
\sum\epsilon_i=0,\quad \sum\epsilon_i^2=D,\quad
|\epsilon_i|\le s,\quad\sum|\epsilon_i|^3\le D^{3/2}.
\]
Put \(m=29/100\), \(B=41/100\), \(r=1/480\). For \(s\le1/25\),
\(b-1/25-m^2=9/10000>0\) and \(B^2-b-1/25=31/10000>0\).
Thus \(m<|x_i|<B\). No coordinate vanishes. If there were at most three
positive coordinates, their sum of magnitudes would be below \(3B\),
while at least five negative coordinates have sum above \(5m\).
Since \(5m-3B=11/50>0\), this contradicts \(\mu_1=0\). Reversing signs
excludes five or more positive coordinates. This pays all sign cases.

The three exact cancellations are
\[
\sum x_i=0,\quad \sum x_i\epsilon_i=\mu_3-b\mu_1=0,\quad
\sum x_i\epsilon_i^2=\mu_5-2b\mu_3+b^2\mu_1=0.
\]
For a nonzero original coordinate,
\[
\frac1x=x(b^{-1}-\epsilon b^{-2}+\epsilon^2b^{-3})
-\frac{\epsilon^3}{b^3x}.
\]
Consequently \(|\sum x_i^{-1}|\le (512/m)D^{3/2}\). This is an exact
identity with a bounded remainder, not a convergent-series assertion.

## Central root and full eigenspace mass

Let \(\Phi(z)=\sum_i(z-x_i)^{-1}\), with no poles on \([-r,r]\).
On the entire central gap between the negative and positive coordinates,
\(\Phi'=-S_2<0\), where \(S_2(z)=\sum_i(x_i-z)^{-2}\).
Cauchy--Schwarz on the eight original positions gives
\[
64=\left(\sum_i\frac{x_i-z}{x_i-z}\right)^2
\le S_2(z)\sum_i(x_i-z)^2=S_2(z)(1+8z^2).
\]
The last equality uses both \(\mu_1=0\) and \(\mu_2=1\).
Hence, for \(|z|\le r\),
\[
S_2(z)\ge A:=\frac{64}{1+8r^2}=\frac{1843200}{28801}.
\]
For \(\delta=28D^{3/2}\),
\[
\delta\le28/15625<r,\qquad
28A-512/m=22067200/835229>0.
\]
Integration bounds \(\Phi(-\delta)>0>\Phi(\delta)\).
The intermediate value theorem and strict decrease therefore give the unique
central root \(\sigma\in(-\delta,\delta)\). Since \(f'/f=\Phi\) off the
originals for \(f(z)=\prod_i(z-x_i)\), it is also a critical root of the
literal octic, with its original multiplicities retained.

The vector \(v_i=(\sigma-x_i)^{-1}/\sqrt{S_2(\sigma)}\) is unit and lies in
\(e^\perp\). The identity \(x_i/(\sigma-x_i)=\sigma/(\sigma-x_i)-1\)
gives \(Hv=\sigma v\). Any other vector \(y\in e^\perp\) in this
eigenspace has \((\sigma I-\operatorname{diag}(x))y\) proportional to
\(e\). All diagonal entries are invertible because \(|\sigma|<r<m\),
so \(y\) is proportional to \(v\). Thus the eigenspace is one-dimensional
and the entire mass, without any choice of basis, is
\[
w^Tv=-\sqrt8/\sqrt{S_2(\sigma)},\qquad m_\sigma=64/S_2(\sigma).
\]
In particular \(\eta_{\rm ang}\ge m_\sigma^2\), including arbitrary
collisions of the other original or compression eigenvalues.

## All eight inverse-square Taylor remainders

The exact inverse-square decomposition gives
\[
S_2(0)=64+64\sum_i\frac{\epsilon_i^2}{b+\epsilon_i}
\le64+\frac{64D}{b-s}.
\]
For \(t=\epsilon/b\),
\[
(1+t)^{-2}-(1-2t+3t^2)=-t^3\frac{4+3t}{(1+t)^2}.
\]
Multiply by \(xb^{-2}\) to obtain \(x^{-3}\); its polynomial part sums
to zero by the three odd cancellations. The ratio
\(T(t)=(4+3t)/(1+t)^2\) has derivative
\((-5-3t)/(1+t)^3<0\) throughout \([-8/25,8/25]\), where it is positive.
Thus \(T(t)\le1900/289\) and
\[
|S_3(0)|:=\left|\sum_i x_i^{-3}\right|
\le A_3D^{3/2},\qquad A_3=Bb^{-5}(1900/289).
\]
For each of the eight functions \(g_i(z)=(x_i-z)^{-2}\), Taylor's theorem
has linear term \(2\sigma x_i^{-3}\) and second derivative
\(6(x_i-z)^{-4}\). Every intermediate point lies in \([-r,r]\), with
\(|x_i-z|>m-r\). The sum of **all eight** half-second-derivative
remainders is bounded by \(24\sigma^2/(m-r)^4\). Hence
\[
S_2(\sigma)\le64+\frac{64D}{b-s}
+\left(56A_3+\frac{24\cdot28^2}{(m-r)^4}\right)D^3.
\]
The entire constant equals
\[
\frac{506316387394134474752}{65888562449329}<8000000,
\]
with strict difference \(20792112200497525248/65888562449329\).
As \(D>0\), this yields the strict inequality
\[
S_2(\sigma)<64\left(1+\frac D{b-s}+125000D^3\right)=64(1+q).
\]
It follows that \(\eta_{\rm ang}>(1+q)^{-2}\), proving the nonlinear
upper bound for \(C\). Strictness does not assume any other mass is positive.

## Uniform endpoint payment for the new collar

Let \(F(s)=u(s)(2+s^2u(s))/(1+s^2u(s))^2\). Direct differentiation gives
\[
F'(s)=\frac{2[u'(s)-su(s)^2(3+s^2u(s))]}{(1+s^2u(s))^3}.
\]
For \(0<s\le1/25\), \(u\) is increasing,
\(u\le u(1/25)=5136/425<13\), \(s^2u<13/625<1\), and \(u'\ge64\).
Therefore
\[
su^2(3+s^2u)<676/25<64\le u',
\]
so \(F\) is strictly increasing on this entire interval. At the endpoint,
\(q=5136/265625\), and direct exact evaluation gives the displayed
\(1721799060000/73311519121\) and its positive strict gap below \(47/2\).
This finishes the refinement for every real vector satisfying the hypotheses.

## Complete reconstruction of the original 10290 constants

For the original interval \(s\le1/27\), the same magnitude and odd-sum
arguments apply. The author's weaker slope estimate is also valid:
\[
S_2(z)\ge8/(B+r)^2=46080000/978121=:A_0\quad(|z|\le r).
\]
With \(L=40\), \(40/19683<r\) and \(LA_0>512/m\), the same bracket and
full-eigenspace argument give \(|\sigma|<40D^{3/2}\) and \(m_\sigma=64/S_2\).
Now \(T(t)\le T(-8/27)=2268/361\). Put \(A_{3,0}=Bb^{-5}(2268/361)\).
The complete Taylor loss is
\[
80A_{3,0}+24\cdot40^2/(m-r)^4
=5078352912883209732096/411518530176605<12500000.
\]
With \(q_0=D/(b-s)+(12500000/64)D^3>0\), one has
\(\eta_{\rm ang}>(1+q_0)^{-2}\). The exact positive difference
\[
2q_0(1+q_0)^2-[(1+q_0)^2-1]=3q_0^2+2q_0^3>0
\]
then yields precisely
\[
C<16/(1-8\sqrt D)+390625D^2.
\]
This expression increases on the full original interval. At \(D=1/729\)
it is \(237004387/10097379=47/2-568039/20194758\).
Thus the complete original strict inequality and constants are confirmed,
independently of the stronger new derivation.

## Necessary bands, including repeated originals

For arbitrary \(D>0\) under the moment hypotheses, \(H\) has dimension
seven, so at most seven positive full masses sum to one. Cauchy--Schwarz
gives \(\eta_{\rm ang}\ge1/7\) and \(C\le6/(7D)\).
Combining with the new collar proves
\[
C\ge47/2\quad\Longrightarrow\quad 1/625<D\le12/329.
\]
If an original value \(a\) has multiplicity at least two, its original
block of vectors with zero sum is an eigenspace of \(H\) at \(a\),
orthogonal to \(w\). It is the **entire** eigenspace: the eigen-equation
\((\operatorname{diag}(x)-aI)y\) proportional to \(e\) forces that
proportionality constant to zero at an original-a coordinate. All other
coordinates of \(y\) then vanish, and \(y\in e^\perp\) has block sum zero.
An eigenvalue off the originals is simple by the inverse-diagonal argument.
Thus at least one dimension is fully inactive, leaving at most six positive
full masses. Consequently \(\eta_{\rm ang}\ge1/6\), \(C\le5/(6D)\), and
\[
C\ge47/2,\quad\hbox{an original coordinate repeated}
\quad\Longrightarrow\quad 1/625<D\le5/141.
\]
This argument also works for repeated zero coordinates outside the collar.
It needs neither original simplicity, attainment of an optimizer, nor
coverage by a stationary central chart. Replacing the new cutoff by
\(1/729\) reconstructs both corollaries of10290 exactly.

## Literal even calibration and prior credit

Let \(0<D<1/16\), \(b=1/8\), and
\[
f_D(z)=(z^2-b)^2[(z^2-b)^2-D/4].
\]
Its actual eight real roots are \(\pm\sqrt b\) each twice and
\(\pm\sqrt{b-\sqrt D/2}\), \(\pm\sqrt{b+\sqrt D/2}\) each once.
All squared levels are positive. Paired odd moments vanish,
\(\mu_2=2[2b+(b-\sqrt D/2)+(b+\sqrt D/2)]=1\), and
\(\mu_4=b+D\). The central root is zero and the same full mass argument gives
\[
S_2(0)=64(1-8D)/(1-16D),\quad
m_0=(1-16D)/(1-8D),\quad p=1-m_0=8D/(1-8D).
\]
The other full masses are nonnegative and sum to \(p\); their squared sum
lies in \([0,p^2]\). Hence
\[
\frac{16(1-16D)}{(1-8D)^2}\le C(f_D)
\le\frac{16(1-12D)}{(1-8D)^2}.
\]
Both bounds tend to16. This confirms10290's calibration and shows that a
uniform leading constant below16 cannot work. The family and limit are
already published mathematics:8753, independent8806 and symmetric9416.
Their full-sphere/symmetric scopes remain prior art, not new claims here.

## Proof and computation boundary

The universal proof is the written argument above. It includes the real
spectral theorem, inverse-diagonal eigenspace dimension, IVT, differentiation,
Taylor's theorem, Cauchy--Schwarz and passage to a squeezed limit. None is
checked in a formal proof kernel. The standard-library checker independently
pays all scalar identities and rational constants, the entire calibration
octic and its moment lists, the full new nonlinear derivative identity,
and two literal normalized eight-coordinate controls with repeated originals.
Each control uses \(a=(1,-1,1,-1,1+t,-1-t,1-t,-1+t)\), \(t=1/100,1/50\),
\(x=a/\sqrt{\sum a_i^2}\), and exact rational projectors. The two controls are
symmetric; coverage of asymmetric profiles comes from the universal proof,
not from finite sampling. No diagonalization, floating-point root search,
resource-limited enumeration or solver nonexistence inference is used.
