# Regular recovery of the critical coefficient E in the angular stationary system

Actual **six-sendov-2**, role **researcher**. Complete ordinary algebraic
lemma with a small exact certificate; **unformalized and independently
unreviewed**. The stationary reduction and reused arithmetic are explicitly
same-author inputs. Row operations, Sylvester determinants, interpolation,
integer Gauss, and Gram/norm arguments are classical.

## 1. Exact object and claim

Use the entire five residuals of
[LEMMA9550](../degree-five-triangular/PROOF.md), source
**cb4cf7d9d83f3d376d3763b65cbe2fddd50637f4**. Write them as
\(\widehat R(B,E,r,s,t)\) in row order
\((tO_2,tO_1,tO_0,K_1,K_0+4)\). Here E is the coefficient of
\(z^3\) in the monic critical heptic
\(h=z^7-3z^5/8+Bz^4+Ez^3+h_2z^2+h_1z+h_0\). It differs from the physical
critical-energy H in the complementary first-power work.

[LEMMA9695](../nonzero-quartic-mass/PROOF.md), source
**15d70a9cbcc9d49baab803bd94e2d6a2668d90df**, excludes every finite
complex common scalar root of the9550 system at s=0. Its original-root
corollary gives p4!=0 at every covered distinct real stationary profile.
Thus every such profile has the legal coordinates

\[
q=B/s,\qquad x=s^2>0,\qquad u=st=p_4\ne0.                 \tag{1}
\]

The variable u is **signed**. The reflection convention t=p5>0 recovers
\(s=\operatorname{sign}(u)\sqrt x\), \(B=qs\),
\(t=|u|/\sqrt x\). No q!=0 assumption is made. The single q in(1)
is not a reciprocal coordinate of the first-power conjecture.

Multiply the five old rows respectively by \((s^2,s,s^2,s,s^2)\),
and substitute \(B=qs,t=u/s,x=s^2\). Every resulting monomial has
nonnegative even s exponent. This gives the **complete** polynomial vector
\(R(q,E,r,x,u)\in\mathbb Q[q,E,r,x,u]^5\). In the remainder of this
proof R denotes these transformed rows. The source reconstructs every
coefficient from the entire pinned9550 matrix and checks all five exact
inverse pullbacks; no exported CAS polynomial is a premise.

Define the four rows

\[
\begin{split}
F_0&=R_1+\frac{367}{360}R_0,\\
F_1&=R_2-\left(\frac r3+\frac{13}{96}\right)R_0,\\
F_2&=R_3,\\
F_3&=R_4-\frac1{48}R_0.                                  \tag{2}
\end{split}
\]

**Theorem.** These four rows are affine in E,
\(F_i=\alpha_iE+\beta_i\). For **every complex** finite common zero
of all five R, with x!=0 and u!=0,
\(\alpha=(\alpha_0,\ldots,\alpha_3)\ne0\). Consequently, at fixed
\((q,r,x,u)\), there is at most one common complex E. Any such root is
jointly simple in E: the five derivatives \(\partial_E R_i\) do not
all vanish. The proof does not require real h roots, positive masses,
a coefficient corridor, an extremum, or a matrix-rank premise.

**Real recovery and complete reduced predicate.** For real(q,r,x,u)
with x*u!=0, let

\[
S=\alpha\cdot\alpha,\quad T=\alpha\cdot\beta,
\quad U=\beta\cdot\beta,\qquad
R_0=2u^2E^2+\ell_0E+c_0.                                 \tag{3}
\]

There is a common real E **iff**

\[
S>0,\qquad SU-T^2=0,\qquad
2u^2T^2-\ell_0TS+c_0S^2=0.                               \tag{4}
\]

Then E=-T/S. This reconstructs **all five** equations. On the actual
stationary original-root domain one additionally retains x>0,u!=0,
the orientation recovery in(1), seven **simple real** roots of h, and
**strict** p(lambda)>0 at all seven. With the full inherited9550/9496
feasible theorem these conditions give an equivalent reduction to four
real coordinates. Neither the Gram equations nor critical reality alone
certifies feasible original roots. Original collisions remain outside this
interpretation.

No unconditional nonvanishing statement about alpha away from solutions
is asserted. No complete feasible-locus classification, global angular
optimum, original collision extension, or complex first-power resolution
is claimed. The older rank-one substitution for E in
[9602](../regular-linear-pencil/PROOF.md) does not apply to general
rank-two solutions; the newly proved E=-T/S in(4) has separate hypotheses.

## 2. Complete E cancellation and the alleged singular branch

Whole coefficient identities, for arbitrary(q,r,x,u), are

\[
[E^2]R=u^2\left(2,-\frac{367}{180},
\frac{2r}{3}+\frac{13}{48},0,\frac1{24}\right).             \tag{5}
\]

They prove(2) is affine in E. The five-by-five transformation from
R to(R0,F0,F1,F2,F3) has determinant one; no parameter is inverted.
All complete alpha and beta polynomials are regenerated and recorded in
[expected.json](expected.json).

Each alpha_i has an exact factor u. Write

\[
\alpha_i=c_i u A_i,\qquad
(c_0,c_1,c_2,c_3)=
\left(\frac1{16934400},\frac1{4515840},
\frac1{9408},\frac1{2257920}\right),                      \tag{6}
\]

where all A_i are primitive integer polynomials, with the sign retained
by positive rational content. Their whole coefficients, including every
q=0 term, are in the fixture and generated source. In particular,

\[
A_2=7200qu+(31304r+1162x+6165)u-118272.                   \tag{7}
\]

Suppose all alpha_i vanish at a full common zero. Since u!=0, all A_i
vanish. Set v=qu and
\(V=118272-(31304r+1162x+6165)u\). Equation(7) gives
7200v=V. This divides only the nonzero **constant7200**; q is allowed
to vanish.

A0 and A3 are affine in v after replacing qu by v. The expression
u*A1 and the entire beta2 are quadratic in v after that replacement.
All conversions are whole polynomial identities, with no hidden negative
u exponent. If H(v)=h2*v^2+h1*v+h0, define

\[
\operatorname{clr}_v(H)=h_2V^2+7200h_1V+7200^2h_0.
\]

The exact undivided identity is

\[
7200^2H-\operatorname{clr}_v(H)
=(7200v-V)\{h_2(7200v+V)+7200h_1\}.                       \tag{8}
\]

It applies even if either quadratic or linear leading coefficient
vanishes. For the two affine leading rows, the smaller constant-pivot
elimination 7200H-h1*(7200v-V) is used. Normalization gives three
necessary polynomials F,G,J, all affine in u:

\[
\begin{split}
F={}&(-622164480r^2-155391544rx-399486600r
 +584833438x^2-159507315x-59491125)u\\
 &+1719152640r-1926275328x+732326400,\\
G={}&(-1814400r^2+5083304rx-1139400r
 -3260738x^2+1859625x-165375)u+3241728x,\\
J={}&(-55296000r^3+292745728r^2x-55728000r^2
 -203109632rx^2+203291080rx-18225000r\\
 &\qquad-220448x^3-63036010x^2+34741125x-1906875)u\\
 &-458440704rx+404901888x^2-179078400x.                     \tag{9}
\end{split}
\]

The two affine leading eliminations have respective contents4704 and
23520. For u*A1, its entire cleared polynomial is
33868800*u*J. Removing u here is legal by the stated u!=0 branch.
These are complete coefficient identities; neither F's nor G's slope
in u is divided.

The actual lower equation also matters. Since alpha2=0 and F2=R3=0,
one has beta2=0. Applying(8) to its entire quadratic-v form gives
(45/28)N=0, where N=n2*u^2+n1*u+n0 and

\[
\begin{split}
n_2={}&53473280r^3+8414784r^2x+96633600r^2
 +21774144rx^2-32901120rx+43596000r\\
 &+555436x^3+4996740x^2-8541225x+5670000,\\
n_1={}&-252887040r^2-571060224rx-335462400r
 -66189312x^2-10967040x-86400000,\\
n_0={}&1990066176x.                                      \tag{10}
\end{split}
\]

Discarding this lower equation would leave additional candidate
coefficient-degeneration points. This proof retains it.

## 3. Three necessary low-degree polynomials

Write F=f1*u+f0, G=g1*u+g0 and J=j1*u+j0. The full identities define
primitive integer P,R,L in QQ[r,x] by

\[
\begin{split}
f_1g_0-g_1f_0&=23040P,\\
g_1j_0-j_1g_0&=30720xR,\\
n_2g_0^2-n_1g_1g_0+n_0g_1^2&=103219200xL.                \tag{11}
\end{split}
\]

Their respective degrees in r are3,3,4 and their respective total
(r,x) degrees are3,3,4. Equations(9)--(11) are complete defining
formulas; [verify.py](verify.py) generates their entire expansions
and the fixture records all coefficients.

F=G=J=0 implies both cross identities vanish. The lower clearing is
necessary from G=N=0 by the whole identity

\[
g_1^2N-(n_2g_0^2-n_1g_1g_0+n_0g_1^2)
=G\{g_1n_2u+g_1n_1-g_0n_2\}.                            \tag{12}
\]

No g1 division occurs. Zero or simultaneous-zero affine slopes,
quadratic degree losses, and identically zero specialized rows remain
in the necessary identities. Since x!=0, an alleged full singular
solution must have P=R=L=0 at the same finite(r,x).

## 4. Fixed determinants and a complete univariate unit

Let Delta1(x) be the fixed6-by6 Sylvester determinant of P,R in r,
and Delta2(x) the fixed7-by7 determinant of P,L. Rows are shifted
P followed by shifted R or L, with shifts in descending order and
columns in descending formal r powers. The formal sizes are never
changed at a parameter specialization.

At any common finite r, the nonzero evaluation column
(r^(m+n-1),...,1) lies in the corresponding matrix kernel.
Consequently P=R=L=0 implies Delta1=Delta2=0, including all
specialized leading losses or identically zero polynomials. This is
an ordinary evaluation-vector argument, not an assumed generic
resultant equivalence.

For Delta1 the rowwise x-degree bound is3*3+3*3=18. For Delta2 it
is4*3+3*4=24. Therefore19 and25 consecutive distinct integer
evaluations determine the **entire** determinants. At every one
of those44 nodes, the checker constructs the full integer matrix,
checks all Bareiss divisions are integral, and separately corroborates
the result by Fraction Gaussian elimination. Complete rational
interpolation yields integer coefficient arrays of degrees9 and12.
Every coefficient and all44 values are recorded. The second algorithm
is same-author corroboration, **not independent review**. Identity
reconstruction under a proved degree bound is not a grid search for
stationary parameters.

Removing only nonzero rational contents gives primitive integer
polynomials D1,D2 of degrees9,12. Their complete reductions modulo
the verified prime257 are the following arrays, in ascending x powers:

```text
D1 = [234,137,182,119,159,129,14,143,246,190]
D2 = [0,0,228,123,0,244,227,63,164,93,101,203,134]
U  = [67,8,222,5,100,142,178,36,246,203,48,134]
V  = [167,102,8,132,57,6,52,62,67]
```

The checker derives the entire multipliers and multiplies every
coefficient of U*D1+V*D2=1 in GF257[x]. Both leading coefficients,
190 and134, are nonzero, so both integer degrees are preserved.

If D1 and D2 had a common complex root, their rational gcd would
have a nonconstant primitive integer factor H. Gauss's lemma makes
H an integer divisor of each primitive polynomial. Its leading
coefficient divides the nonzero-mod257 leading coefficient of D1,
so reduction preserves H's positive degree. Its reduction would
divide both displayed reductions, contrary to the complete unit.
Thus D1,D2 have no common complex root. This is a **univariate
integer** bridge with explicit leading-degree preservation; a
modular multivariate ideal unit would not provide this conclusion.

The necessary Delta1=Delta2=0 is impossible. Hence no full common
zero with x*u!=0 has all alpha_i=0, proving the nonvanishing assertion.

## 5. Recovery, simplicity, and a pointwise derivative bound

Two distinct common E values at fixed(q,r,x,u) would make
alpha_i*(E1-E2)=0 for all four rows, contradicting their proved
nonvanishing at either solution. Thus E is unique over C. If all
five E derivatives vanished at a common root, differentiating(2)
would give alpha=0. This proves joint simplicity in E. It does not
assert full parameter-Jacobian rank two: the E and t derivative
directions can require a further independence argument.

For real parameters, the nonzero alpha gives S>0. The complete
Lagrange identity

\[
SU-T^2=\sum_{i<j}(\alpha_i\beta_j-\alpha_j\beta_i)^2        \tag{13}
\]

shows that equality implies beta=(T/S)*alpha. Consequently the
four affine rows vanish exactly at E=-T/S. The last equation of(4)
is S^2*R0(-T/S)=0. The invertible row operation(2) then supplies
all five original transformed equations. Conversely, any common
root satisfies all conditions in(4). The fixture/source retains
complete alpha,beta,ell0,c0 definitions; the norm identities are
ordinary real algebra and are checked in universal small variables.
Over C a nonzero vector can have zero sum of squares, so neither
S>0 nor this Gram recovery is transferred to complex tuples.

Let Trow be the four-by-five row map in(2). After column ordering
it is (c,I4), with
c=(367/360,-r/3-13/96,0,-1/48). Therefore
Trow*Trow^T=I4+c*c^T and its real Euclidean operator norm is
sqrt(1+||c||^2). Since Trow*(partial_E R)=alpha, at every real
common root

\[
\|\partial_E R\|_2\ge
\frac{\sqrt S}{\sqrt{1+(367/360)^2+(r/3+13/96)^2+1/2304}}>0.\tag{14}
\]

This concerns the five **scaled** rows R. It is pointwise;
no uniform lower bound for S or upper bound for r is supplied.
It is a coefficient-residual statement. Quantitative original-root
continuation requires further control of the remaining equations,
critical separation and strict mass margins. No actual nonlinear
basin or angular Hessian theorem is asserted.

## 6. Inputs, proof status, and remaining frontier

The new source byte-pins both9695 files, regenerates its **entire**
typed record, and checks its canonical digest. Its inherited9550
source, entire typed fixture, full matrix and record digest are
likewise regenerated. All parent arithmetic and mathematical
premises are explicitly same-author reuse. No private chart export
or CAS result is a runtime input. Original feasible interpretation
retains the premises of
[9496](../mass-stationary-chart/PROOF.md) and
[7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
through9550/9695.

[REVIEW9598](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/pencil-audit/REVIEW.md)
confirms9550. The actual independent
[REVIEW9691](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/global-pencil-rank-audit/REVIEW.md)
confirms[9649](../global-rank-two/PROOF.md), supplies its generic
complex extension and strengthens its pointwise t derivative bound.
None supplies a verdict on this new E theorem or on9695. Those
pointwise scalar statements and the new E statement retain their
separate domains. The new exclusion does not use either rank-one
E formula or9649 as a proof premise.

The meaningful change is a legal **E elimination across every
covered actual stationary profile**, including B=0, either sign of
p4, all vanishing individual E slopes and every row degree loss.
The four-real-coordinate predicate(4) still requires both strict
feasible conditions. A useful next step is to combine it with the
credited9598 actual corridor9/448+sigmaM/32<E<3/64 and the full
rank-two conic conditions, looking for one small sign/root
incompatibility. Uniform E-slope or original-root stability needs
additional quantitative bounds. Neither algebraic uniqueness nor
a timeout on a larger ideal supplies stationary nonexistence.

Reproduction, full typed fixture, meaningful degeneracy controls and
explicit proof trust boundaries are in[README.md](README.md).
Current primary status and classical-method attribution are recorded
in[LITERATURE.md](LITERATURE.md). The strongest first-power question
remains distinct from the reported resolved ordinary Sendov theorem
and proved quadratic Tang--Zhang inequality.
