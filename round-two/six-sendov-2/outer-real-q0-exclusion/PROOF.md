# One-double exclusion through the real-q0 outer boundary

Actual author: **six-sendov-2**, role: **researcher**, 2026-10-04.
Complete ordinary author proof with exact polynomial certificates;
**unformalized and independently unreviewed** at publication. The two arithmetic
implementations are same-author checks. Classical Newton, Rolle, Hermite,
resolvent, Bezout and Bernstein arguments are credited, with no historical
priority claim. This is real angular structure adjacent to the degree-nine
complex first-power problem.

## 1. Claim and the remaining frontier

Let a real eight-vector, with original multiplicities retained, satisfy

\[
\mu_1=\mu_3=\mu_5=0,\qquad\mu_2=1,\qquad
D=\mu_4-1/8>0.
\]

Suppose exactly one original level \(a\) is double and its other six originals
are simple and different from \(a\). Put \(A=a^2\), \(s=A-1/8\), and use
the full grouped spectral masses of [7432](../../../sendov_collapsed_angular_quartic/PROOF.md):
\(C=(1-\eta)/D\).

**Theorem.** Every such actual profile with

\[
\boxed{D-8s^2\ge0}
\]

satisfies \(C<47/2\). The equality boundary is included. The new part is
the entire outer region \(d=D/4-6s^2<0\); the central region and the
impossibility of \(d=0\) are already established in
[10304](../central-one-double-exclusion/PROOF.md).

Consequently every remaining actual exact-one-double profile with \(C\ge47/2\)
has, after reflection so that \(a>0\),

\[
\boxed{1/625<D\le5/141,\qquad D<8s^2,\qquad d<0,\qquad u<0.}       \tag{1}
\]

The lower endpoint is credited to the complete written refinement in
[REVIEW10298](../../six-reviewer-1/small-d-angular-audit/PROOF.md), read in full
before use. That independent verdict concerns its parent10290, not this child.
The full complex first-power inequality and the remaining angular maximum
are not proved here. Sections2 and6 give exact original-root licenses and
additional necessary bounds for the open branch in(1).

## 2. Original model and exact outer reality fiber

The generic chart is prior [10136](../collision-moment-reduction/PROOF.md).
With \(E=3/64-D/8\), define

\[
q_0(t)=t^2+(2A-1/2)t+3A^2-A+2E,
\qquad k_0(t)=t^2+(A-3/8)t+A^2-3A/8+E,
\]
\[
Q_u(z)=(z+a)^2q_0(z^2)+4u,\qquad
f_u(z)=(z-a)^2Q_u(z),\qquad
H_u(z)=z(z+a)k_0(z^2)+u.
\]

The whole identity \(f_u'=8(z-a)H_u\) and all three zero odd moments,
the norm and fourth excess follow by exact Newton identities. Original
feasibility means **six simple real zeros of \(Q_u\)** and
\(Q_u(a)=4(u-Ad)\ne0\). Reality of \(H_u\) alone is insufficient.

Write \(b=2A-1/2,c=3A^2-A+2E\). The derivative is independent of \(u\):

\[
Q_u'(z)=2(z+a)T_4(z),\qquad
T_4=3z^4+2az^3+2bz^2+abz+c,\qquad T_4(-a)=-d.          \tag{2}
\]

Six simple real originals force five distinct simple real derivative zeros
by Rolle and the degree count. Hence \(T_4\) has four distinct real roots,
none equal to \(-a\). In particular \(d\ne0\). If \(d<0\), \(-a\)
is a strict minimum of \(Q_0\), since \(Q_0''(-a)=-2d>0\).

Here is an explicit finite real-root test. Let \(p_j\) be the power sums of
the roots of the monic quartic \(T_4/3\), counting multiplicities, with
\(p_0=4\). Newton recurrence determines \(p_1,\ldots,p_6\) exactly.
The four leading principal minors of \((p_{i+j})_{0\le i,j\le3}\) are

\[
4,\quad\frac{9-56s}{6},\quad
\frac{-504Ds+81D+3136s^3-392s^2-34s+2}{162},\quad
\frac{F(s,D)}{46656},                                  \tag{3}
\]
where the entire polynomial is

\[
\begin{split}
F={}&-6912D^3+173376D^2s^2-2736D^2s+117D^2\\
&-1455104Ds^4+30464Ds^3+3888Ds^2-752Ds+32D\\
&+4214784s^6-150528s^5-20160s^4+4224s^3-192s^2.
\end{split}                                             \tag{4}
\]

All four are strictly positive **if and only if** the quartic has four
simple real roots. For real distinct roots the matrix is a Vandermonde
Gram matrix and is positive definite. Conversely its determinant excludes
repeated roots; for any nonreal conjugate pair, interpolation gives a real
polynomial of degree at most three taking values \(i,-i\) at that pair
and zero at the other roots. Its quadratic form is \(-2\), contradicting
positive definiteness. Sylvester's criterion pays the stated equivalence.
Both implementations reconstruct every coefficient of all four minors;
the converse is an ordinary written argument, not a formal kernel result.

On \(d<0\), suppose(3) holds and order the five fixed derivative zeros
as \(\gamma_1<\cdots<\gamma_5\). Their types alternate: minima at
indices1,3,5, maxima at2,4. Define

\[
L=\max_{j=2,4}[-Q_0(\gamma_j)/4],\qquad
U=\min_{j=1,3,5}[-Q_0(\gamma_j)/4].                    \tag{5}
\]

Then \(Q_u\) has six simple real roots **if and only if** \(L<u<U\).
Necessity follows from strict alternating extrema of a monic sextic.
For sufficiency these signs give one crossing in each of the six intervals
cut out by the five extrema, including both unbounded intervals; degree
six rules out additional roots or multiplicity. Because \(-a\) is one of
the minima and \(Q_0(-a)=0\), always \(U\le0\). An empty interval pays
infeasibility; no numerical nonexistence inference is used. Excluding
\(u=Ad\) additionally pays separation from the selected original double.
The same extremum argument proves \(u<0\) on every actual outer fiber.

## 3. A cubic outer cap when q0 has real roots

Only the range \(1/625<D\le5/141\) needs the new certificate. Smaller
\(D\) is excluded by10298. Larger \(D\) is excluded by the six-positive-mass
Cauchy bound \(\eta\ge1/6\), hence \(C\le5/(6D)<47/2\). This uses the
entire inactive eigenspace at the original double, not a split mass.

Assume \(d<0,D-8s^2\ge0\). Set \(h=|s|>0,H=-d>0\). Then

\[
0<H\le4h^2,\qquad h\le\sqrt{D/8}<3/40,\qquad
q_0(A)=H.
\]

The two squared roots of \(q_0\), possibly equal, are positive. Indeed they
are \(1/8-s\pm\tfrac12\sqrt{D-8s^2}\), and
\(s+\tfrac12\sqrt{D-8s^2}\le\sqrt{3D/8}<1/8\), by Cauchy--Schwarz
on \((s,\sqrt{D-8s^2})\) with the matching weights; \(D<1/24\).
Both roots lie on the same side of \(A\). The closer root has distance

\[
\beta=2h-\sqrt{4h^2-H}>0,\qquad
\beta^2-4h\beta+H=0,\qquad0<\beta\le2h.
\]

Between \(-a\) and this closer negative root, \(Q_0>0\), with zero values
at both endpoints and exactly one strict maximum. To justify uniqueness
also at equality \(D-8s^2=0\): \(Q_0\) then has three distinct double
roots; their three minima and two intervening Rolle maxima exhaust degree
five. For strict discriminant, the double at \(-a\), the two minima
between the two negative and two positive simple roots, and the two Rolle
maxima again exhaust degree five. The closer negative gap is one of those
maxima. Its maximum threshold is an upper bound for the feasible \(-u\).

At a point of this gap let \(x=|z^2-A|\in(0,\beta)\). Then

\[
Q_0(z)=\frac{x^2(H-4hx+x^2)}{(\sqrt{z^2}+a)^2}.
\]

Put \(k=4hx/H,y=x^2/H\). We have \(0<k<2\), \(y\le k^2/4\), and
\(1-k+y>0\). The two whole identities

\[
k^2(2-k)^2-4k^2(1-k+y)=k^2(k^2-4y)\ge0,
\]
\[
1-k^2(2-k)^2=(k-1)^2(1+2k-k^2)\ge0
\]

give the uniform coupled numerator bound

\[
\boxed{x^2(H-4hx+x^2)\le H^3/(64h^2).}                \tag{6}
\]

The second nonnegative factor follows from \(1+2k-k^2=1+k(2-k)\ge1\).
No stationary sampling or series truncation is involved.

If \(s<0\), the closer squared root lies above \(A\), so every interior
gap denominator is strictly greater than \(4A\). If \(s>0\), that root
is \(t_+\ge1/8-h>A/4\); the last strict inequality is equivalent to
\(h<3/40\). Hence its denominator is strictly greater than \(9A/4\).
Taking the maximum on the compact gap, whose maximizing point is interior,
pays

\[
\boxed{
0<-u<\frac{H^3}{\kappa A h^2},\qquad
\kappa=1024\ (s<0),\quad\kappa=576\ (s>0).
}                                                        \tag{7}
\]

The strictness in(7) includes \(D-8s^2=0\); equality in the numerator
estimate does not remove the strict denominator improvement. The exact
fiber for this real-q0 case is \(-\min[Q_0(\text{two maxima})]/4<u<0\),
because all three minimum values are nonpositive and one is zero.

## 4. The whole angular numerator

The original double is a full inactive compression eigenspace. The six
other compression roots \(\sigma_i\) are distinct real gap roots of
\(H_u\), by the logarithmic derivative and Rolle. At each one the full
positive gap mass is

\[
m_i=-8(\sigma_i-a)Q_u(\sigma_i)/H_u'(\sigma_i).
\]

Let \(r=8zH_u-8(z-a)Q_u\). It has degree five and leading coefficient
one. Define the six-by-six Bezout matrix by

\[
\frac{H_u(x)g(y)-H_u(y)g(x)}{x-y}
=\sum_{i,j=0}^5B(H_u,g)_{ij}x^iy^j.
\]

Evaluation at the six simple roots gives diagonal entries
\(H_u'(\sigma_i)g(\sigma_i)\). Therefore

\[
\det B(H_u,H_u'+wr)=\Delta\prod_i(1+wm_i),\qquad
\Delta=\operatorname{disc}(H_u)>0.
\]

The coefficient of \(w\) equals \(\Delta\); the coefficient of \(w^2\),
denoted \(N\), equals \(\Delta(1-\eta)/2\). Thus

\[
C=2N/(D\Delta),\qquad
P=47D\Delta-4N>0\quad\Longrightarrow\quad C<47/2.       \tag{8}
\]

Both source implementations derive this **entire** determinant from the
original model, and check full reflection parity before converting to
\(\mathbb Q[A,D,u]\). There are166,227,228 nonzero terms in
\(\Delta,N,P\), each with complete \(u\)-degree five. The degree-two
determinant jet in \(w\) is exact for those coefficients; it truncates no
dependence on \(A,D,u\). This generic mass identity is prior10136, not
a new formula claimed here.

## 5. Complete sign certificate and combination of ranges

Set \(q=\sqrt{D/24}>0,t=s/q\). The actual real-q0 outer chart satisfies
\(1<|t|\le\sqrt3\). In(7) put

\[
A=1/8+qt,\quad D=24q^2,\quad
u=-\frac{216v q^4(t^2-1)^3}{\kappa A t^2},\qquad0<v<1.
\]

The complete cleared polynomial identity is

\[
(\kappa A t^2)^5P\left(A,D,-\frac{216v q^4(t^2-1)^3}{\kappa A t^2}\right)
=q^{10}(t^2-1)^2S_\kappa(q,t,v).                        \tag{9}
\]

Every cleared denominator and removed factor is strictly positive on the
actual chart. The complete reduced tensor degrees are \((12,28,5)\).
The three closed rational boxes below cover a superset of the entire needed
actual chart; \(1/123<\sqrt{(1/625)/24}\),
\(1/26>\sqrt{(5/141)/24}\), and \(7/4>\sqrt3\).

|Box|\(\kappa\)|\(q\)|\(t\)|\(v\)|Minimum of all2262 controls|
|---|---:|---|---|---|---|
|negative|1024|\([1/123,1/26]\)|\([-7/4,-1]\)|\([0,1]\)|\(37725215322714843119616/1792160394037\)|
|positive-left|576|\([1/123,149/6396]\)|\([1,7/4]\)|\([0,1]\)|\(28090220358923189203046560727198822280054/40437393667554291532315824798997\)|
|positive-right|576|\([149/6396,1/26]\)|\([1,7/4]\)|\([0,1]\)|\(472115081689901544567668295283515/3839339858408590549723567\)|

For each tensor axis the exact coefficient conversion is
\(b_k=\sum_{i\le k}c_i\binom{k}{i}/\binom{n}{i}\). Every one of the
6786 controls is strictly positive. Every full reverse basis identity is
checked. Bernstein basis functions are nonnegative and sum to one, so
the whole polynomial on each closed box is strictly positive. The extra
points with \(|t|>\sqrt3\) are only a rational enlargement for the polynomial
test, not claimed actual profiles. The faces \(|t|=1\) are similarly
harmless polynomial tests; actual \(d=0\) was excluded by Rolle.

The native engine uses Fraction/integer Berkowitz recursion, independent
binomial cap expansion and de Casteljau subdivision. The CAS engine uses
SymPy1.14.0 exact rings, a subset determinant, direct composition, and a
separate direct affine computation of each final box. They share only
serialization/strict coverage checks. Neither reads a predecessor's
coefficient corpus, peer/reviewer executable, fixture or private data.

Equations(8)-(9) prove the complete new outer exclusion in the middle band.
For \(d>0\),10304 gives the entire central exclusion because
\(D\le5/141<1/24\). For \(d=0\), \(Q_u'\) would have a repeated root
at \(-a\), contradicting the degree-five Rolle count. The small band is
covered by10298 and the upper band by six-full-mass Cauchy--Schwarz.
This proves the theorem for every \(D>0\) at its stated real-q0 scope.

## 6. A necessary strip for the remaining positive-q0 branch

This section provides ordinary necessary conditions, **not an exclusion**
of the surviving branch. Apply(1) and the strict sign/nonzero consequence
of [10200](../quartet-triple-rigidity/PROOF.md), which ensures four originals
of each sign. The double may therefore be reflected to \(a>0\). Put

\[
B=1/4-A,\quad h=|A-1/8|>0,\quad
e=2h^2-D/4>0,\quad q_0(t)=(t-B)^2+e,\quad K=-4u>0.
\]

First \(B>0\). There are two positive simple zeros of \(Q_u\), so
Rolle supplies a positive root of \(T_4\). If \(A\ge1/4\), all its
coefficients in(2) are nonnegative and its constant is \(B^2+e>0\),
which prevents a positive root. Thus \(0<A<1/4\).

Now \(b=-2B,c=B^2+e>0\). Descartes' rule gives at most two positive
and at most two negative roots of \(T_4\). The actual four real simple
roots therefore comprise exactly two of each sign. The two negative
roots lie strictly between \(-a\) and \(-\sqrt B\): outside this interval
the two terms \(q_0(z^2)>0\) and
\(2z(z+a)(z^2-B)\) in \(T_4\) are nonnegative. Their closer-to-\(-a\)
extremum is a maximum of \(Q_0\).

At that maximum, \(x=|z^2-A|\in(0,2h)\) and

\[
Q_0(z)=\frac{x^2[(2h-x)^2+e]}{(\sqrt{z^2}+a)^2},\qquad
x^2(2h-x)^2\le h^4,\quad e x^2<4h^2e.
\]

The numerator estimate follows from
\(h^2-x(2h-x)=(h-x)^2\ge0\); the whole difference of squares is
checked exactly. Define

\[
M_- =\begin{cases}(\sqrt A+\sqrt B)^2,&s>0,\\4A,&s<0,\end{cases}
\qquad M_+=(\sqrt A+\sqrt{B/3})^2.
\]

The negative maximum denominator is strictly greater than \(M_-\).
For the larger positive critical root \(\gamma\), which is a minimum,
we have \(\gamma>\sqrt{B/3}\). Indeed

\[
T_4'(z)=4z(3z^2-2B)+2a(3z^2-B)<0
\quad(0<z^2\le B/3),
\]

while the larger of two positive simple quartic roots crosses from negative
to positive, so its derivative is positive. Hence
\(Q_0(\gamma)>eM_+\). The exact sextic alternating-extrema conditions(5)
now give the useful two-sided necessary bound

\[
\boxed{eM_+<K<\frac{h^4+4h^2e}{M_-}.}                \tag{10}
\]

Whenever \(J=M_-M_+-4h^2>0\), this implies

\[
\boxed{0<e<h^4/J.}                                    \tag{11}
\]

On \(s>0\), \(A>B>0\), so \(J>0\) automatically: each square-root
cross term is positive and

\[
(A+B)(A+B/3)-(A-B)^2=\tfrac23B(5A-B)>0,
\qquad4h^2=(A-B)^2.
\]

On \(s<0\) we retain the explicit condition \(J>0\) rather than assume
it; (10) remains valid without it. These bounds use the **original**
extrema and all needed sign/root-count licenses. They do not assert that
the interval is nonempty, rule out high angular values there, or imply
any stationary-system nonexistence. Extending the sign certificate into
this remaining strip is the concrete next frontier.

## 7. Reproduction, trust boundaries and prior work

[README.md](README.md) gives exact commands. [EXPECTED.json](EXPECTED.json)
commits the complete generated mathematical record by hash and all three
box minima. [VALIDATION.json](VALIDATION.json) records four complete
local/cold normal/optimized replays and seven intended source damages.
The entire1643743-byte mathematical record is identical between both
engines, SHA256
`12b0ed927868bc6bb04d9d9cfce17c77089d22af34637a64d7d277936cc64234`.
The bulky record is omitted from the repository; both small sources regenerate
it from definitions. No finite sample, floating-point root search or
resource-limited enumeration is a universal premise.

Original-root hyperbolicity, resolvent/full spectral masses, IVT/Rolle,
Hermite's real-root converse, Bernstein convexity and Descartes' rule remain
ordinary unformalized bridges. Source hashes do not formalize those bridges.
Neither same-author source validation nor a cited parent's independent
review is an independent review of this child.

The prior chart10136, central lemma10304, collision/sign lemma10200 and
reviewer's quantitative cutoff10298 are applied at their exact scopes.
The cutoff is a newly adopted published input, not a new theorem here.
The leading16 limit and compact attainment8753/8806 and symmetric9416 are
already prior mathematics and need not be rerun for this argument.
[LITERATURE.md](LITERATURE.md) keeps the stronger first-power endpoint
distinct from the reported ordinary/quadratic results. No global angular
47/2 theorem, classification of its optimizers or complex disk-path transfer
is asserted.
