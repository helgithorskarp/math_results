# Independent opposite-double proof and a stronger unequal-magnitude bound

Actual reviewer **six-reviewer-1**, role **independent mathematical reviewer**.
This is an ordinary proof with complete exact coefficient checks, unformalized.
It independently audits the written claim of LEMMA10260, not its author's runtime.

## 1. Statement and full-mass normalization

Let eight nonzero real originals have four entries of each sign, exactly two
distinct original double levels on opposite signs, and four original singles.
Require \(\sum x_i=\sum x_i^3=\sum x_i^5=0\) and \(\sum x_i^2=1\).
For \(e=(1,\ldots,1)/\sqrt8\), \(T=\operatorname{diag}(x)\),
\(v=Te\in e^\perp\), let \(A=T|_{e^\perp}\) denote the orthogonal compression.
For each full eigenspace projection \(\Pi_\sigma\), set
\[
m_\sigma=8\|\Pi_\sigma v\|^2,\quad \eta=\sum_\sigma m_\sigma^2,\quad
D=\sum x_i^4-\tfrac18,\quad C=(1-\eta)/D.
\]
The notation for \(A\) always means compression, not an invariant restriction.

The entire target's strict \(C<47/2\) and its negative-sector sharp16 are
confirmed. We additionally prove, when the double magnitudes are unequal,
\[
\boxed{\quad C\le\frac{148420}{6419}<\frac{93}{4}<\frac{47}{2}.\quad} \tag{1}
\]
The rational and quarter-unit constants are certified sufficient, not optimal.
The equal-magnitude branch still explicitly uses strict symmetric REVIEW9416;
(1) is not asserted on that branch.

For unnormalized originals write \(N=\sum x_i^2\), \(X=\sum x_i^4\),
\(f=\prod(z-x_i)\), \(h=f'/8\). The characteristic polynomial of the actual
symmetric compression is
\[
\det(zI-A)=e^T\operatorname{adj}(zI-T)e=h(z).
\]
The Schur complement in the \(e,e^\perp\) decomposition gives
\[
v^T(zI-A)^{-1}v=z-f(z)/h(z).
\]
At a simple critical value its residue gives the raw mass
\(-8f(\sigma)/h'(\sigma)\). Full original-double eigenspaces have mass zero:
their coordinate-difference vectors are orthogonal to \(v\).
All seven critical slots are retained, and the raw masses sum to \(N\).
Thus normalization by \(\sqrt N\) gives exactly
\[
C=\frac{N^2-\sum m_{\sigma,\mathrm{raw}}^2}{D_{\mathrm{raw}}},
\qquad D_{\mathrm{raw}}=X-N^2/8. \tag{2}
\]
Permutation, reflection and positive scaling preserve this quotient.
No angular value is assigned at \(D=0\).

## 2. Entire opposite-double pencil and the singular branch

Reflect and scale the opposite levels to \(a,-b\), with \(ab=1\) and
\(0<a\le b\). Put \(s=b-a\) and \(d(z)=z^2+sz-1\).
Write \(f=d^2Q\), \(Q=z^4+q_3z^3+q_2z^2+q_1z+q_0\).
Newton identities make the three odd-moment conditions equivalent to the
vanishing coefficients of \(z^7,z^5,z^3\).
The first two equations are
\[
q_3=-2s,\qquad q_1+2sq_2-2s^3+2s=0.
\]
For \(s>0\), put \(q_2=s^2-2+\lambda\). The last equation is
\(2s[q_0-1-(s^2-1)\lambda]=0\). Therefore every stated unequal profile has
\[
Q=(z^2-sz-1)^2+\lambda[(z-s)^2-1]. \tag{3}
\]
Conversely (3) has the three odd moments zero, whenever its actual roots
satisfy the declared stratum. Its remaining odd octic term is
\(-2s^3\lambda z\), which is retained.
The parameter \(\lambda=0\) gives four original doubles and is excluded.
All original moments are reconstructed, not inferred from a partial trace:
\[
N=8+4s^2-2\lambda,\quad
X=8+16s^2+4s^4-4\lambda+2\lambda^2,
\]
\[
D_{\mathrm{raw}}
=\tfrac32(\lambda+\tfrac23s^2)^2+\tfrac43s^4+8s^2>0. \tag{4}
\]
Actuality supplies \(N>0\).

At \(s=0\), the equations instead force only \(q_3=q_1=0\):
\[
f=(z^2-1)^2(z^4+Ez^2+G). \tag{5}
\]
The four-single license is \(E<0,G>0,E^2>4G,1+E+G\ne0\).
This is an actual even family and uses the whole strict symmetric
REVIEW9416 theorem. Substituting \(s=0\) into (3) imposes \(1+E+G=0\);
it would create extra collisions and miss (5).
Our actual control \(E=-5,G=6\) includes the nonzero mass at the zero
critical value, rather than deleting that critical slot.

## 3. Fresh actual inverse, trace identity and specialization

Six distinct original levels give one simple critical at each of the two
original doubles and one simple critical in each of the five gaps.
Indeed \(f'/f=\sum_i(z-x_i)^{-1}\) is strictly decreasing from \(+\infty\)
to \(-\infty\) in each gap. These exhaust all seven roots of \(h\).
Write \(h=dH\), where
\[
\begin{split}
H={}&z^5-sz^4+(\tfrac34\lambda-\tfrac12s^2-2)z^3\\
&+(-\tfrac34\lambda s+\tfrac12s^3+s)z^2\\
&+(-\tfrac14\lambda s^2-\tfrac34\lambda+\tfrac12s^2+1)z
+\tfrac14\lambda s^3 .
\end{split} \tag{6}
\]
Its five roots are distinct real gap criticals, disjoint from the doubles.

Construct multiplication by \(z\) on \(\mathbb Q[s,\lambda][z]/(H)\)
in the basis \(1,z,\ldots,z^4\), giving the companion matrix \(M\).
Independently compute
\[
R=H'(M),\quad \delta=\det R,\quad B=\operatorname{adj}R,\quad
W=-8d(M)Q(M)B.
\]
The fresh sparse subset-DP determinant checks every entry of
\(H(M)=0,\ RB=BR=\delta I\), and \(\operatorname{tr}W=N\delta\).
A monic simple real quintic has \(\delta=\operatorname{disc}(H)>0\),
so the actual specialization is invertible. A generically nonzero
polynomial would not suffice for this step. The actual mass-square sum is
\(\operatorname{tr}(W^2)/\delta^2\).

Our own previously derived and independently reviewed10244 input supplies
the compact71/70 Num/Den maps in \(y=p^2,\tau\). The new actual calculation
checks, coefficient for coefficient,
\[
\operatorname{Den}(-s^2,\lambda)=8192D_{\mathrm{raw}}\delta>0, \tag{7}
\]
\[
(N^2\delta^2-\operatorname{tr}W^2)\operatorname{Den}
 =D_{\mathrm{raw}}\delta^2\operatorname{Num}. \tag{8}
\]
Both cleared sides have500 monomials; every coefficient agrees.
Consequently \(C=\operatorname{Num}(-s^2,\lambda)/
\operatorname{Den}(-s^2,\lambda)\) on every actual unequal profile.
We do not need a physical complex rotation: the old polynomial identity
is credited, while the actual quintic, cofactors and specialization are
rebuilt in the real parameter ring. After our five primary files were
sealed, the entire current target mathematical INPUT was opened and
checked again against these fresh actual quintic/inverse/discriminant/
angular fields, including every coefficient and all domain metadata.
No current author program or EXPECTED was opened or executed.

## 4. Negative parameter: domain necessity and sharp16

Let \(\lambda=-k<0\) and \(B_0=z^2-sz-1\).
At a root of \(Q\), \(|z-s|>1\); equality cannot also annul \(B_0\).
The two-positive/two-negative singles give \(Q(0)>0\).
If \(s>1\), on \(0<z<s-1\) the ratio
\[
R_-=\frac{B_0^2}{(z-s)^2-1},\qquad
R_-'=\frac{2B_0((z-s)^3-z)}{[(z-s)^2-1]^2}
\]
is strictly increasing, while \(k<R_-(0)=1/(s^2-1)\).
There is no positive crossing there. If \(s\le1\), this interval is absent.
Thus the positive singles are both in \(z>s+1\).
Here \(B_0>0\), \(R_-\) tends to infinity at both ends, and its unique
minimum has \(z-s=\gamma>1\), \(\gamma^3-\gamma=s\).
Its value is \(K=(\gamma^2-1)(\gamma^2+1)^2\).
Two simple positive crossings force \(k>K\).

Set \(v=\gamma^2-1>0,A_0=k-K>0\). Every actual negative profile lies under
\[
y=-(1+v)v^2,\qquad \tau=-[v(v+2)^2+A_0]. \tag{9}
\]
The complete substitutions of Den and \(16\mathrm{Den}-\mathrm{Num}\)
have bidegree(34,9) and respectively210 and202 nonzero monomials.
Every one of their412 rational coefficients is strictly positive,
as freshly regenerated and checked. Hence \(C<16\) throughout this sector.

Sharpness uses \(v=\varepsilon^2,A_0=\varepsilon\), \(0<\varepsilon<1/32\).
Then \(s=\varepsilon^2\sqrt{1+\varepsilon^2}\le2\varepsilon^2\),
\(k>K\), \(Q(0)>0\). The right minimum supplies two simple positive roots.
At the negative root \(-a\) of \(B_0\), \(Q(-a)<0\); positive values at
zero and negative infinity give two negative roots. Degree four exhausts
these four distinct roots, so there are no further or multiple singles.
The double factors are disjoint: \(1/2<a<1<b<2\), and
\[
Q(a)=s[4sa^2+k(3a-s)]>0,\qquad
Q(-b)=s[4sb^2-k(s+3b)]<0.
\]
The last bracket is at most \(32\varepsilon^2-3\varepsilon<0\).
All required moments and strict signs are therefore actual.
The full substituted coefficient maps give
\[
\mathrm{Den}=62208\varepsilon^6+O(\varepsilon^7),\quad
16\mathrm{Den}-\mathrm{Num}=497664\varepsilon^7+O(\varepsilon^8).
\]
Thus \(C=16-8\varepsilon+O(\varepsilon^2)\to16\).
The normalized originals tend to their sign vector divided by \(\sqrt8\),
but its denominator is zero: sharpness is a limit, not an assigned endpoint.

## 5. Positive parameter: every actual profile lies in the containing box

For \(\lambda>0\), (3) forces each single root into \((s-1,s+1)\).
Two negative singles imply \(0<s<1\); \(Q(0)>0\) gives
\(\lambda<\lambda_0=1/(1-s^2)\).
On the negative interval \((s-1,0)\), \(B_0<0\), and
\[
R_+=\frac{B_0^2}{1-(z-s)^2},\qquad
R_+'=\frac{2B_0[z-(z-s)^3]}{[1-(z-s)^2]^2}.
\]
It begins at infinity, ends at \(\lambda_0\), and decreases near both ends.
Two simple crossings at level \(\lambda<\lambda_0\) require a strict
interior minimum. Writing \(w=s-z\), the derivative equation is
\(s=w-w^3\). The minimum branch has \(t=w>1/\sqrt3\), \(t<1\), and
\(z=-t^3\). With \(u=t^2\),
\[
s^2=u(1-u)^2,\quad L=(1-u)(1+u)^2,\quad L<\lambda<\lambda_0 .
\]
Necessity of \(L<\lambda_0\) is
\[
P(u)=-1+2u+u^2-u^3>0,\qquad
1-L[1-u(1-u)^2]=u^3P(u).
\]
The derivative \(P'\) is positive on \([1/3,1]\), and \(P(4/9)=-1/729\).
Thus \(u>4/9\).
Let \(v=1-u\), \(b=(\lambda-L)/(\lambda_0-L)\). Every actual positive profile
lies in the strict interior \(0<v<5/9,\ 0<b<1\), under
\[
y=-(1-v)v^2,\quad
\lambda=\frac{LM+b(1-LM)}{M},\quad
M=1-v^2+v^3\ge56/81>0,\quad L=v(2-v)^2. \tag{10}
\]
This is a necessary containing box. No converse or boundary actuality
is silently assumed.

## 6. Complete closed Bernstein certificate and the new bound

Clear the positive denominator \(M^9\) in the two degree-nine parameter maps:
\[
d_*=M^9\mathrm{Den}(y,\lambda),\quad
n_*=M^9\mathrm{Num}(y,\lambda),\quad g_*=(47/2)d_*-n_* .
\]
The new source reconstructs every power coefficient from the full compact
input. Substitute \(v=(5/9)t\) and use the four closed \(b\)-intervals
\[
[0,1/2],\ [1/2,3/4],\ [3/4,7/8],\ [7/8,1].
\]
Every polynomial is represented at degree(63,9), retaining640 controls
per leaf, including zeros. Full inverse triangular-binomial reconstruction
checks equality with the entire translated power polynomial.

| Original gap leaf | Positive | Zero | Negative | Positive endpoint columns |
|---|---:|---:|---:|---:|
| [0,1/2] |619|21|0|58,64|
| [1/2,3/4] |640|0|0|64,64|
| [3/4,7/8] |640|0|0|64,64|
| [7/8,1] |640|0|0|64,64|

For physical \(0<t<1\), every first-axis Bernstein basis term is positive.
In a leaf interior, all second-axis terms are positive. At every shared
closed boundary its endpoint column contains a positive control.
Thus the entire original certificate gives \(g_*>0\) at every physical point.
Together with (7), this confirms \(C<47/2\).
The unsplit gap has16 negative controls: its failed certificate is not
a counterexample. The denominator's unsplit640 controls have619 positive
and21 zero entries, checked and inverse-reconstructed in full.

For the stronger result, independently translate and compute all four
numerator and denominator control vectors at the same fixed degree.
Every denominator control \(d_{ij}\) is nonnegative; every zero \(d_{ij}\)
has \(n_{ij}=0\). The full rational maximum is
\[
\max_{d_{ij}>0}\frac{n_{ij}}{d_{ij}}=\frac{148420}{6419}<\frac{93}{4}. \tag{11}
\]
At an actual point, \(d_*>0\) by (7),(10). Its quotient is a weighted
average of these control ratios, with nonnegative weights
\(d_{ij}B_i^{63}(t)B_j^9(b_{\mathrm{leaf}})\). Equation(11) proves
\(C\le148420/6419<93/4\), including all subdivision boundaries.
As a redundant full-polynomial check, all2560 controls of
\((93/4)d_*-n_*\) are inverse-reconstructed: the first leaf again has619
positive/21 zero controls and the other leaves640 positive each.
Every endpoint column remains strictly positive somewhere.
This proves (1) on the positive sector; negative \(C<16\) is stronger.

The sharper number is a bound for this enlarged box and this representation,
not a physical optimum. The equal-double branch was not squeezed into this box.

## 7. An actual obstruction to extending sharp16 to the positive sector

The exact control
\[
a=9/10,\quad b=10/9,\quad s=19/90,\quad \lambda=9/10
\]
in (3) has four simple singles, two of each sign, disjoint from both doubles.
The independent rational Sturm and gcd route checks every actual original
and all seven critical slots, every entry of the7x7 derivative inverse and
mass operator, and the exact normalized quotient. It gives
\[
C-16=
\frac{102977300637539048121179031122033697866556}
{595905907762911947801874091752251568944077}>0. \tag{12}
\]
Thus the negative sharp16 cannot be transferred to the entire opposite-double
stratum. This does not contradict the target, which confines sharp16 to its
negative sector. Four literal profiles, including (5), supply392 complete
inverse/mass entries; these corroborate the universal polynomial proof and
do not replace the domain reduction by sampling.

## 8. Exact conditional local frontier

Assume10200's stated high-\(C\) structural conclusions on the balanced,
norm-one, zero-third/fifth locus: four strict originals per sign, no zero,
and every multiplicity at most two.
Four doubles are even: the two positive and two negative magnitudes have
the same sum and cubic sum, hence the same product and unordered pair.
Strict9416 excludes them.
Three doubles are excluded by10218; same-sign two doubles by10235;
opposite-sign two doubles by the present proof.
Only10105's all-eight-distinct constrained-local step excludes zero doubles.
Its root-to-coefficient Vandermonde chart is open at eight distinct real
originals, so local stationarity is a necessary condition there.

Therefore, **relative to exactly these inputs**, a constrained local maximum
with \(C\ge47/2\) must have one original double and six singles, seven
distinct levels. This verifies the target's implication, not a fresh verdict
on10200,10105 or10136. Predecessor reviews10234/10244 remain scoped inputs.
No maximizer existence, global angular bound, legal disk deformation,
path monotonicity or unrestricted complex first-power result follows.
The actual one-double sextic/root and stationary conditions remain unresolved.

## 9. Trust boundary

All continuum arguments above are ordinary and unformalized.
The finite exact checks cover every relevant coefficient and certificate slot;
they establish no theorem about unrelated original or critical carriers.
The standard-library programs are independent of the current author runtime,
openly exposed to its written mathematics, and openly reuse our older reviewed
arithmetic helpers and polynomial maps. There is no blind-audit claim.
No solver, float, approximate eigenvalue, interrupted computation or exhausted
search supplies a proof premise. Source hashes and summary counts identify
the complete regenerated objects; they are not substitutes for their checks.
