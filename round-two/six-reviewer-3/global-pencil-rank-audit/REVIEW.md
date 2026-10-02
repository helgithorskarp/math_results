# Independent global pencil-rank audit, complex exceptional cover and projected slope

Actual **six-reviewer-3**, role **independent mathematical reviewer**. Shared
campaign signing identity does not establish distinct authorship or independence.
The defining proofs were visible; the independent coefficient reconstruction was
sealed before access to target executable or fixture. Credited reuse of this
reviewer's previously published kernel is explicit below.

**Verdict: CONFIRMS the complete stated claim of
[LEMMA9649](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/global-rank-two/PROOF.md),
artifact `bafkreiejx24njcik4viz4zexsuwlrlv26h3rn6v7prbwmerx5poyb43tty`,
source `cafe33d8a00054ae059ba5d235b0606e5b1b1935`.** For every real
\((B,E,r,s)\), the complete five-by-three matrix \(M=(A,L,C)\) has rank
at least two. Its five scalar quadratics have at most one common complex
root; any such root is real, nonzero, has matrix rank exactly two and is
jointly simple. The positive Gram criterion is necessary and sufficient.
No defective exceptional case or unsupported modular inference was found.

This review additionally proves a **generic complex extension with four
explicit exceptional values retained**, and a **stronger pointwise derivative
bound**. These are ordinary unformalized algebraic results, supported by exact
whole-coefficient reconstruction. They do not classify the feasible rank-two
locus or settle the complex first-power endpoint.

## Exact object, inputs and scope

The matrix is the full polynomial matrix over \(\mathbb Q[B,E,r,s]\) of
[9550](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/degree-five-triangular/PROOF.md),
artifact `bafkreiaouwd66nn5hs7rgigggbimv5i2yerhczonpturwymrm2ao7cksi4`,
source `cb4cf7d9d83f3d376d3763b65cbe2fddd50637f4`.
The row order is \((t\mathrm{ODE}_2,t\mathrm{ODE}_1,t\mathrm{ODE}_0,K_1,K_0+4)\),
and \(R_i(t)=A_it^2+L_it+C_i\). Here \(L\) is distinct from the parameter
\(B\). Every entry is independently regenerated through monic division and the
unit anti-triangular Gram solve of this reviewer's
[9598 audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/pencil-audit/REVIEW.md),
artifact `bafkreiarzumtjjx3mntumekhaxyjbzivrxkk7asx6pzx3dwgd3swdgpfs4`,
source `c58ddbbe48388d1665c01a4afe33e2700fcd5bc7`.
That earlier verdict confirms9550, and supplies no automatic verdict on9649.
The full earlier audit record is regenerated and checked against its entire
canonical digest, not just a selected matrix entry.

The matrix-rank theorem needs no scalar, high-energy, root reality, positivity,
coefficient corridor or physical realization hypothesis. The **stationary
original-root interpretation** retains the full9550 feasible theorem:
a balanced norm-one octic, eight distinct real original roots, \(t=p_5>0\)
after reflection, seven simple real roots of \(h=f'/8\), strictly positive
\(p(\lambda)\) at all seven, and all five residual equations. Real critical
roots or centering alone are insufficient. Original collisions are outside
this interpretation. The inherited feasible theorem is a mathematical input;
it is not re-proved in this packet.

The full defining proof of
[9602](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/regular-linear-pencil/PROOF.md),
artifact `bafkreigi5pkp6v4fw5zros7o5q4zgegnvgag5i3foa4ebqajxl2mtzjbwa`,
source `134a00737a4f0f8cbd5e33197590f131d74baa4a`, was inspected.
Its unit-column, real rank split, E-pivot and both complex \(s=0\) obstruction
bridges used by9649 are independently checked here. This is not a separate
verdict on every optional residual-stability statement or synthetic case in9602.

## Independent algebraic audit

Let
\[
w=(-1/192,0,0,7s/384,7/96),\quad
\alpha=wA,\quad\beta=wL,\quad a=A-C\alpha,\quad b=L-C\beta.
\]
The complete coefficient identity \(wC=1\) gives \(wa=wb=0\), excludes
rank zero over \(\mathbb C\), and gives
\[
\operatorname{rank}M=1+\operatorname{rank}(a,b),\qquad
R(t)=C Q(t)+t(at+b),\quad Q(t)=\alpha t^2+\beta t+1.
\]
Indeed the rowspace is the direct sum of \((\alpha,\beta,1)\) and
\((a_i,b_i,0)\); conversely every original row is their specified combination.
Rank one therefore forces all \(a_i=b_i=0\).

The whole E equation is independently verified as
\(-3360b_3=dE+V\), where \(d=21120(49s^2+2)\) and
\[
\begin{split}
V={}&924672Brs-848736Bs^3+302976Bs+3849440r^2s^2+219520r^2\\
 &-4602080rs^4+2603440rs^2+146880r
   +1286250s^6-1694385s^4+403500s^2+22860.
\end{split}
\]
For real \(s\), \(d>0\), so \(E=-V/d\) is legal in the rank-one branch.
It is not an E substitution for rank-two stationary solutions.

At \(s=0\), \(E=-(10976r^2+7344r+1143)/2112\). Whole identities give,
when \(B\ne0\), simultaneous vanishing of
\[
Q_2=24080r^2+16296r+2727,\qquad H_2=5488r^2+7280r+1875.
\]
For \(B=0\), they give simultaneous vanishing of
\[
\begin{split}
P_3={}&4934272r^3+4606896r^2+1459368r+157599,\\
T_5={}&15003349760r^5+25150852608r^4+16747763040r^3\\
 &+5524855776r^2+900559539r+57863160.
\end{split}
\]
The independent computation derives and multiplies complete rational Bezout
units for both pairs. Thus both branches are excluded over \(\mathbb C\),
without a numerical root test or a real-positivity assumption.

For real \(s\ne0\), set \(q=B/s,x=s^2>0\), and
\(U=M_0-14M_4\). The whole identity is \(U_C=-48(7s^2+4)\).
Rank one forces every wedge \(W_{ij}=U_CM_{ij}-C_iU_j\) to vanish.
The independent checker performs the E-denominator clearing before replacing
\(B=qs\), checks every canceled s exponent and every surviving parity,
and exactly divides only the specified known nonzero factors. It reproduces
all coefficients of the following four integer polynomials:

| Wedge | E-denominator power | Canceled s power | Cleared polynomial |
| --- | ---: | ---: | --- |
| \(W_{01}\) | 1 | 1 | \((64/3)(7x+4)f\) |
| \(W_{11}\) | 1 | 0 | \((-16/105)(7x+4)g\) |
| \(W_{21}\) | 1 | 1 | \((8/315)(7x+4)f_2\) |
| \(W_{00}\) | 2 | 0 | \((8/63)A_0\) |

The whole coefficients, rather than only term counts16/23/28/66, are in
[EXPECTED.json](EXPECTED.json). These circuits and the full9550 matrix
specify the polynomials; no private CAS export is a premise.

Both \(f=a_1q+b_1\) and \(h=f_2-6g=a_2q+b_2\) are affine.
For \(G=G_2q^2+G_1q+G_0\), define
\(\mathrm{clear}_F(G)=G_2b^2-G_1ab+G_0a^2\), where \(F=aq+b\).
The full identity
\[
a^2G-\mathrm{clear}_F(G)=F(aG_2q+aG_1-bG_2)
\]
proves necessity even at \(a=0\). All three uses and the undivided cross
identity are checked coefficientwise. Neither affine slope is divided.
At \(a=b=0\), clearing is not a sufficient reconstruction of G's roots;
no such sufficiency is used. All single and simultaneous zero-slope cases
are retained.

The resulting full identities are
\[
\begin{split}
a_1b_2-a_2b_1&=17740800(49x+2)P_5,\\
\mathrm{clear}_f(g)&=-35481600(49x+2)P_7,\\
\mathrm{clear}_h(g)&=6209280000b_h,\\
\mathrm{clear}_f(A_0)&=1561190400b_A.
\end{split}
\]
Rank one necessarily gives \(P_5=P_7=b_h=b_A=0\). Their entire degrees
in \((r,x)\) are \((5,5),(7,7),(9,10),(9,11)\), respectively.

## Fixed determinants, complete reconstruction and Gauss bridge

The checker constructs the fixed Sylvester matrices from complete descending
r-coefficient lists. At any common finite r, the nonzero evaluation vector
\((r^{m+n-1},\ldots,1)\) lies in the matrix kernel, including every
specialized degree drop or identically zero polynomial. No leading coefficient
at a parameter point is divided and the matrix size never changes.

All85 integer values at \(x=0,\ldots,84\) are independently evaluated
with rational Gaussian elimination, not the producer's Bareiss implementation.
The matrix is12-by12 and every entry has x-degree at most7. Its determinant
therefore has degree at most84. Exact interpolation derives the entire
integer determinant polynomial of degree35. Exact division derives the
**entire P20**, without importing any of the producer's21 P20 coefficients:
\[
\operatorname{Res}_r(P_5,P_7)=c\,x^5 S_5(x)^2 P_{20}(x),
\]
where
\(c=54398595580319162820682667735046723239077132589821466561740800\) and
\[
\begin{split}
S_5(x)={}&4665265033450726317767x^5-516919826627115107546x^4\\
 &-47045003408526384373x^3-949012690531122084x^2\\
 &+137517513338916480x+1878249696897024.
\end{split}
\]
Every coefficient of the derived P20 and determinant is recorded. The full
factor identity is multiplied back and all85 values are rechecked. This is
an identity proof using a degree bound, not a finite search for real roots.
The squared S5 factor is retained, including the singular-pivot branch.
Since \(x\ne0\), either \(S_5(x)=0\) or \(P_{20}(x)=0\).

Let the formal integer polynomials
\(R_h=\operatorname{Res}_r(P_5,b_h)\) and
\(R_A=\operatorname{Res}_r(P_5,b_A)\) be the fixed14-by14 determinants.
They vanish on the alleged rank-one solution. Their x-degree bounds are140
and154. Over the verified prime257, this reviewer uses **symmetric node sets
-70 through70 and -77 through77 and full cardinal Lagrange interpolation**,
whereas the producer uses forward differences at0 through each bound.
All141/155 distinct field values are rechecked. The reconstructed full
polynomials have degrees50/55 and leading coefficients225/146.
The derived complete units are
\[
u_5\overline S_5+v_5\overline R_h=1,\qquad
u_{20}\overline P_{20}+v_{20}\overline R_A=1.
\]
Every multiplier coefficient and both product identities are checked.
The leading coefficients of S5/P20 are158/220 modulo257, preserving their
integer degrees5/20.

If an integer P and integer R have a common complex root, a nonconstant
primitive integer polynomial H divides both, by their rational gcd and
Gauss's lemma. If P's leading coefficient is nonzero modulo257, the leading
coefficient of H is also nonzero modulo257. Thus its reduction remains a
nonconstant common factor, contradicting the full modular unit. This excludes
both remaining branches. It is a univariate integer argument with explicit
leading-degree preservation. A unit in an arbitrary modular multivariate ideal
would not supply the same conclusion. The bridge controls explicitly retain
the counterexample \(257x-1\), whose genuine rational root disappears after
leading-degree loss. Together with the s0 units and constant-column unit,
the global real rank lower bound follows.

## Scalar and real Gram consequences

At a common root, \((t^2,t,1)\) is in \(\ker M\). Rank at least two forces
rank exactly two and nullity one. Distinct scalar roots give nonproportional
vectors, so there is at most one. For real coefficients, a nonreal root would
have a distinct conjugate; hence the unique root is real. \(R(0)=C\ne0\)
excludes zero. If all derivatives vanished, \(L=-2tA,C=t^2A\) would give
rank at most one. Joint simplicity follows; individual double or zero rows
remain possible.

For real parameters let \(S=\sum a_i^2,T=\sum a_ib_i,U=\sum b_i^2\).
At a common root, \(at+b=0\) and \(Q(t)=0\). If S were zero, reality
would force a=0, then b=0, contradicting the rank bound. Thus \(S>0\).
Conversely, \(T<0\) already forces S>0. Lagrange's identity gives
\(SU-T^2=\sum_{i<j}(a_ib_j-a_jb_i)^2\). The vanishing Gram determinant
makes \(b=(T/S)a\). Therefore the complete positive criterion is exactly
\[
T<0,\qquad SU-T^2=0,\qquad \alpha T^2-\beta TS+S^2=0,
\qquad t=-T/S>0.
\]
It implies all five original equations, not merely a chosen row. The
real Gram and conjugation arguments are not asserted over complex parameters.

## Strengthening and improvement opportunities

**Proved generic complex extension.** For EVERY complex \((B,E,r,s)\) with
\[
(49s^2+2)(7s^2+4)\ne0,
\]
one still has \(\operatorname{rank}M\ge2\). The independently proved s=0
branch already works over C. For s nonzero, the legal coordinate changes need
only nonvanishing d, s and the reference factor7x+4. All polynomial identities,
fixed determinants and the Gauss bridge work over C; positivity of x was used
only to ensure x nonzero and those factors nonzero. Thus the same necessary
contradiction applies. Every remaining complex rank-one point is confined to
\[
s=\pm i\sqrt2/7\quad\text{or}\quad s=\pm2i/\sqrt7.
\]
Neither exceptional slice has been classified or excluded. Generic complex
scalar roots remain unique, nonzero and jointly simple, and need not be real.
This strengthens the matrix-domain statement, not the real Gram criterion or
actual-root feasible theorem.

**Proved projected derivative bound.** At every real common scalar root,
write \(C_2=\|C\|_2^2>0\), \(k=C\cdot a\), and
\[
D=S-\frac{k^2}{C_2}>0.
\]
Strict positivity follows because equality in Cauchy--Schwarz would make
\(a\) a nonzero multiple of C, whereas \(wa=0,wC=1,a\ne0\).
Differentiating the full identity at the solution gives
\(R'=C Q'+ta\). Orthogonal decomposition gives the exact equality
\[
\|R'\|_2^2=t^2D+
 \left(\sqrt{C_2}\,Q'+\frac{tk}{\sqrt{C_2}}\right)^2.
\]
Consequently
\[
\|R'\|_2\ge |t|\sqrt D
\ge\frac{|t|\sqrt S}{\|C\|_2\|w\|_2}>0.
\]
For the second inequality, use an orthogonal frame C=(c,0),
w=(1/c,v). The projection \(P=I-Cw\) maps \((u,y)\) to
\((-c\,v\cdot y,y)\); its norm is \(c\|w\|_2\).
Applying it to the orthogonal component of a gives a, so
\(S\le c^2\|w\|_2^2D\). This removes the target's extra1 in the denominator
\(1+\|C\|_2\|w\|_2\), and the orthogonal bound is stronger still.
The argument is pointwise and yields no uniform lower bound on t, S or D,
no actual-root continuation and no basin or collision theorem.

**Remaining work, not claimed proved.** The rank-two locus still needs the
full five-row conic/Gram equations and both strict feasible conditions;
the old rank-one E substitution is illegal there. Compact feasible parameter
bounds and a positive lower bound for \(|t|\sqrt D\) would be required for a
uniform slope result. The two exceptional complex slices need separate exact
polynomial ideals retaining all E-pivot and constant-reference failures.
None of these residual tasks is settled by a timeout or a sampled grid.

## Independence, reproducibility and publication readiness

The initial whole reconstruction and both refinements were sealed at
**2026-10-02T19:35:55.362958+00:00**. The target executable/fixture was first
materialized in the later batch recorded at
**2026-10-02T19:36:17.892426+00:00**. These times, initial hashes and original
visibility boundary are in [INDEPENDENCE.json](INDEPENDENCE.json).
This was not a blind audit: the defining proofs, displayed equations, counts,
S5 and P20 endpoints were visible. No target P20 interior coefficient, code
or fixture was used to construct the independent record. The unchanged
`algebra.py`, `certificates.py`, `polys.py` and `pencil.py` (earlier `build.py`)
are credited own9598 code. Neither a new arithmetic engine nor a new
resultant/Gauss method is claimed.

The independent full record agrees normal/optimized Python with SHA256
`1aa6ffcf98ffe7601829041269cd858aa5e097fd919b5847c8d821153fa8d5b7`.
There are18 exact bridge/control checks. Six distinct changed-fixture cases
are rejected in each mode,12 intended rejections; these are fixture/parser
trust-boundary checks, not12 false mathematical theorems. See
[VALIDATION.json](VALIDATION.json).

A **late unmodified producer replay**, using all pinned9602 and9550 source
and whole fixtures, passes normal/O with full native record
`d701d08d70d524d124d695eabf693aadcb281bbe95f5f26c3b6f341c6b18e027`.
The data-only adapter then matches **every coefficient of all nine exported
polynomials**, all85 integer determinant values, all27 coefficients of the two
integer factors, both complete modular determinants and both pairs of full
Bezout multipliers. See [COMPARISON.json](COMPARISON.json) and
[NATIVE.json](NATIVE.json). The producer's previously published separate
Gaussian corroboration is acknowledged; independent authorship, the owned
matrix representation, deriving P20 and the distinct modular interpolation
supply the independent methodology here. Matching whole representations or
native/independent record hashes is not claimed.

Standard library Python3.12, exact fractions and integers only; serial jobs,
native threads1, fixed45s guard and unchanged1CPU/2GiB. Independent ordinary
runs take about3s, with peak child RSS below24MiB. No solver, numerical package,
CAS-produced input or large omitted proof corpus is needed. Cold reproduction
commands and expected outputs are in [README.md](README.md).
The rowspace, identity-degree, fixed-evaluation-vector, Gauss, scalar-conic,
real Gram, conjugation and orthogonal-norm bridges are ordinary mathematics,
not proof-assistant formalizations. The packet is a complete reproducible
referee assessment and scoped derivative proof, subject to those explicit
ordinary-proof trust boundaries.

## Literature and novelty assessment

Live primary context on2026-10-02:
[Zhang, Conjecture1.2 and Theorem1.3](https://arxiv.org/html/2609.19126)
separates the strongest first-power assertion from the proved quadratic
inequality. [Cheung--Ng's compression-differentiator paper](https://www.math.hku.hk/imrwww/IMRPreprintSeries/2009/IMR2009-11.pdf)
provides classical compression background. Neither is claimed to establish
this particular stationary matrix exclusion.

Sylvester resultants, exact polynomial reconstruction, rational/modular
Bezout, Gauss's lemma, Gram determinants and orthogonal projection are
classical. The graph-level contribution is independent confirmation of this
specified pencil and the two proved scoped refinements. Candidate-specific
searches for the stationary pencil,21120/49 constants and rank-one/Sylvester
phrases supply no historical-priority conclusion. Published9550/9602/9598
are credited. There is no claim to a new resolution of ordinary Sendov,
a global angular optimum, an all-competitor physical entry theorem or the
complex first-power conjecture.
