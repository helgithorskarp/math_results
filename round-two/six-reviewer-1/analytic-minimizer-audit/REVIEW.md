# Independent exact analytic boundary audit and sharp limiting stability

Actual reviewer **six-reviewer-1**, role **independent mathematical reviewer**.
Target: committed LEMMA8921, **Unique analytic degree-nine first-power boundary
minimizer and sharp small-imaginary stability**, explicitly authored by
researcher six-sendov-3, artifact
`bafkreig4fbumy4uayhto3w7hxj5mmppvn2kuddzmqlnol3leov7ffyq52m`.
Reviewed source commit `ac6099018ea9e0e8e3092122db6ff24d549ebf32`:
[proof](https://github.com/helgithorskarp/math_results/blob/ac6099018ea9e0e8e3092122db6ff24d549ebf32/round-two/six-sendov-3/analytic-boundary/PROOF.md),
[checker](https://github.com/helgithorskarp/math_results/blob/ac6099018ea9e0e8e3092122db6ff24d549ebf32/round-two/six-sendov-3/analytic-boundary/verify.py).

**Verdict: confirmed as an ordinary analytic theorem within its explicitly
inherited concentration and second-optimum premises.** The proof covers all
complex competitors, gives an attained unique radiuswise minimum in an
existential collar, and establishes its analytic coefficients, exact6+2 critical
structure, four active original roots and optimal small-imaginary stability
exponent. The normal inversion, parity division, independent complex slacks,
Hessian continuation, uniform coverage and symmetry bridges were audited; no gap
was found. Analytic arguments remain outside a formal proof kernel.

A proved refinement replaces the published quadratic coefficient1/256 by
**every fixed coefficient strictly below1/2**, and the common radial coefficient
by individual coefficients arbitrarily close from below to **w3/2 and w4/2**.
These limiting coefficients are optimal, with exact feasible witnesses around
the true minimizer. The value1/2 and centered real-splitting mechanism have
prior asymptotic credit in review8883; the refinement here is the error-free
inequality around the exact analytic minimizer, together with sharp individual
radial coefficients. The endpoint1/2 itself is not asserted as a uniform
error-free bound. No new third/fourth/fifth objective coefficient is claimed.

## Definitions and dependencies

Let p be monic of degree9, all nine roots in the closed unit disk, with marked
root a=1-eta>0. Let the eight critical points zeta_j count with multiplicity and
F=sum_j |a-zeta_j|^{-1}; a zero denominator means infinity. The normalization
comes from rotating the marked root and dividing by the leading coefficient.
For arbitrary phase and scalar, the final equality classification is transported
by those operations. Throughout eta>0 tends to0; no effective width is supplied.

Put c=cos(pi/9), the unique root of8c^3-6c-1 in(3/4,1), and

\[
\begin{gathered}
d=2c^2-1,\quad v=2d^2-1,\quad y={1\over3(1+c)},\quad x={2\over3}-y,
\quad H_0=14y,\quad U_0=-8x,\quad b^2=H_0/2,\\
\rho=(c-5)/3,\quad L=-7(2c+1)/18,\quad
u_z=(U_0+\rho H_0)/8,\quad u_p=u_z-\rho H_0/2,\\
w_4={1\over c+d},\quad w_3={2\over3}[7-(1-d)w_4],\quad
C=8/3+y,\\
B_*={2311\over108}+{4934\over27}c-{1976\over9}c^2,
\quad C_3=-{60800959\over17496}-{307083769\over17496}c
              +{10980067\over486}c^2.
\end{gathered}
\]

The essential premises are concentration and conditional coefficient bootstrap
7190, sharp second infimum/profile selection8619 and its independent review8684.
The relevant quantitative bootstrap in8619 and inherited hypotheses in7190 were
read again for this audit:
[7190 refinement](https://github.com/helgithorskarp/math_results/blob/d16c8df095d88b344063fd9c87f39be57e408cd7/sendov_degree9_first_power_boundary_review2/REFINEMENT.md),
[second theorem](https://github.com/helgithorskarp/math_results/blob/f8df996dba7bfec1d05eb6731b3b8e667ca8f860/round-two/six-sendov-3/quartic-boundary/PROOF.md),
[second review](https://github.com/helgithorskarp/math_results/blob/691ea3f4eaa4b06b46ab0aded63903d81d95c668/round-two/six-reviewer-1/quartic-boundary-audit/REVIEW.md).
They are established attributed inputs, not newly re-proved concentration claims.
The third theorem8751 and review8781 identify the existing C3 after the minimum
is proved; they are not necessary to construct it:
[third proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/cubic-boundary/PROOF.md),
[third review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/cubic-boundary-audit/REVIEW.md).
The fourth theorem8841/review8883 and other angular/origin results are context:
[fourth proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/fourth-boundary/PROOF.md),
[fourth review](https://github.com/helgithorskarp/math_results/blob/7bf51b77755026292db72084d8338698e2f43925/round-two/six-reviewer-1/fourth-boundary-audit/REVIEW.md).
No verdict on complementary angular or interior claims is transferred.

## Exact chart and four independent root constraints

Write zeta_j=eta*u_j+i*sqrt(eta)*h_j, with real u,h. Label the two large
imaginary coordinates1,2 and retain the free coordinates
z=(h3,...,h8,u3,...,u8). Their reference is z*=(0^6,u_z^6), and the full
reference is h*=(b,-b,0^6),u*=(u_p,u_p,u_z^6). The following exact chart uses
normal variables U,H,V,M:

\[
\begin{gathered}
m_h=(\eta V-\sum_{j=3}^8h_j)/2,
\quad s_h=\sqrt{(H-\sum_{j=3}^8h_j^2)/2-m_h^2}>0,\\
h_1=m_h+s_h,\quad h_2=m_h-s_h,\qquad
m_u=(U-\sum_{j=3}^8u_j)/2,\\
d_u={M-2m_hm_u-\sum_{j=3}^8h_ju_j\over2s_h},\quad
u_1=m_u+d_u,\quad u_2=m_u-d_u.
\end{gathered}
\]

Thus sumu=U,sumh^2=H,sumh=eta V,h.u=M exactly. All16 coordinates are real
analytic near(eta,U,H,V,M,z)=(0,U0,H0,0,0,z*). At each eta>0 the chart covers
all nearby critical multisets with h1>h2; it requires neither separation among
the six small criticals nor analytic labeling of a competitor.

With epsilon=sqrt(eta), construct p by integrating9 product(z-zeta_j) from
1-eta. Its coefficients are analytic in epsilon and all chart variables,
p(-epsilon)=conjugate p(epsilon), and its epsilon first term vanishes. At
epsilon=0 it is z^9-1. All nine original roots have simple analytic maps in
fixed disjoint neighborhoods of the ninth roots. Shrinking one common chart
neighborhood keeps them simple; they exhaust the roots of the degree9 polynomial.

For k=3,4 let r_k^+,r_k^- be maps near exp(plus/minus2pi i k/9), and put
a_k^s=(|r_k^s|^2-1)/2. These four radials are independent for complex p.
Define

\[
E_k={a_k^++a_k^-\over2\eta},\qquad
O_k={a_k^+-a_k^-\over2\epsilon^3\sin(2\pi k/9)}.
\]

The averages are even analytic functions of epsilon vanishing through order1;
the differences are odd and vanish through order2. Their divided maps are
therefore real analytic in eta and parameters, including eta=0. This follows
from convergent power series and root-map conjugation, not finite jet samples.
The exact identity is a_k^s=eta E_k+s eta^(3/2)sin(theta_k)O_k.

The generic finite jet gives at eta=0

\[
\begin{aligned}
E_k&=-1-A_kU/8+B_kH/14,\\
(A_3,B_3)&=(3/2,3/2),\qquad(A_4,B_4)=(1+c,1-d),\\
O_3&=V/8-M/7,\qquad
O_4=V/8-2cM/7+(1-4c^2)J_3/18,\quad J_3=\sum h_j^3.
\end{aligned}
\]

At the reference, J3 and its four normal derivatives vanish. The even and
odd normal block determinants are3(c+d)/224>0 and(1-2c)/56<0. The full
Jacobian is invertible, so one analytic inverse expresses U,H,V,M in
(eta,E,O,z) on a fixed product neighborhood. At eta=0,E=O=0 it satisfies
sumh=0,sumh^2=H0,sumu=U0,M=LJ3,V=8M/7. The independent checker verifies
both block rows/signs and the mixed relation in one cyclotomic field.

The nonactive branches near k=plus/minus1,plus/minus2 have strictly negative
first radial coefficients at the reference. Continuity keeps those coefficients
negative throughout a fixed small chart neighborhood; uniform Taylor remainders
then put their roots inside for eta sufficiently small. The marked branch is
exactly1-eta. Thus active radials<=0 imply complete disk containment, and E=O=0
gives four boundary roots and five strict interior roots. All are simple.

## Slack elimination and limiting cost

The exact reciprocal sum is analytic in eta,h,u near the reference because
the distance squared is(1-eta(1+u_j))^2+eta h_j^2, close to1. The dual
relations sumwA/8=1,sumwB/14=1/2 give in the inverted chart

\[
\mathcal F=8+\eta(C-w_3E_3-w_4E_4)+\eta^2\widetilde G(\eta,E,O,z),
\]

where Gtilde has bounded derivatives on a smaller fixed product neighborhood.
Consequently, holding z fixed,

\[
{\partial\mathcal F\over\partial a_k^s}
={\mathcal F_{E_k}\over2\eta}
 +s{\mathcal F_{O_k}\over2\eta^{3/2}\sin\theta_k}
=-w_k/2+O(\sqrt\eta)
\]

uniformly there. This derivative bound applies to individual radials; it does
not identify conjugate radials of a complex competitor. Scale all four actual
radials to zero along a straight segment holding z fixed. This scales E,O
inside the product neighborhood and keeps active/nonactive containment. For
any0<alpha_k<w_k/2, integrating the derivative yields

\[
\mathcal F(\eta,E,O,z)-\mathcal F(\eta,0,0,z)
 \ge\sum_{k=3,4}\alpha_k\sum_{s=+,-}(-a_k^s).                 \tag{1}
\]

The published choice alpha_k=min(w3,w4)/4 is valid. The separate near-limit
weights above are the first refinement.

On the zero-slack stratum write F=8+C eta+eta^2 G(eta,z). The exact limiting
cost is

\[
G(0,z)=\mathcal B(h,u)=K_0+\|u\|^2/2+\rho\sum h^2u+\sigma\sum h^4,
\]

with K0=-2609/405-(2000/81)c+(12964/405)c^2 and
sigma=3/8-[(3/2)w3+(1-v)w4]/20. The checker independently builds the generic
fourth Newton/integration jet and the complete affine active second-radial cost.
The odd epsilon^3 root perturbation has no averaged epsilon^4 contribution:
its first radial cancels between branches and its square starts at epsilon^6.
Taking the dual combination of the zero averaged radials gives exactly the
displayed finite cost, with all constant/mixed/fourth-moment coefficients checked.

Review8684's finite global coercivity gives B-B*>=distance to the reference
permutation orbit squared/128 on the exact moment manifold. Restrict to a
neighborhood whose nearest orbit point is the stated reference. The free
coordinates are retained literally, so G(0,z)>=B*+||z-z*||^2/128. Hence
gradientG(0,z*)=0 and Hessian>=I/64. The analytic implicit function theorem
on gradientG gives a unique analytic stationary branch z_eta with z0=z*.
Continuity on a fixed convex ball gives Hessian>=I/128 for small eta; Taylor
integration gives the published1/256. Our full tangent spectrum improves this
step below. No claim that finite jets establish analytic inversion is made.

## Uniform coverage and global uniqueness

This is the essential all-competitor bridge. The attributed second theorem and
review supply an all-disk family for every sufficiently small eta with value
F_upper=8+Ceta+B*eta^2+O(eta^3). Review8684's fixed common-repair2 family
suffices. Fix a finite cubic budget T. A competitor
F<=8+Ceta+B*eta^2+Teta^3 has bounded upper second surplus. The sharp second
infimum supplies its liminf>=B*, while this budget supplies limsup<=B*.
Thus its normalized second surplus tends to B*, and the reviewed selection
theorem gives(h,u)→(h*,u*) after a simultaneous permutation.

The bounded second-budget bootstrap in8619 also gives uniformly
U=U0+O(eta),H=H0+O(eta), bounded h,u, and
V=8M/7+O(sqrt(eta)), with M=h.u. Selection makes M=o(1), hence V=o(1).
The active average radial is O(eta^2) by the bounded-moment fourth jet.
Both actual radials are nonpositive; their average being O(eta^2) then forces
each actual radial to be O(eta^2). Therefore E=O(eta),O=O(sqrt(eta)).
These are precisely the normal variables required by the fixed inverse chart.

The entry into any chosen small product neighborhood/convex z-ball is uniform
for a fixed T: otherwise choose eta_n↓0 and excluded competitors, contradicting
the preceding sequential selection and bounded bootstrap. Critical labels can
be chosen independently at every eta. There is no unproved continuous label
assumption, no assumption that competitors are real, and no reliance on an
attained infimum before the construction.

The stationary polynomial has E=O=0, hence is legal. Apply(1) and the convex
gap to F_upper to see its value m(eta)<=F_upper. Every competitor with
F<=F_upper enters the chart and has F>=m. Those with F>F_upper cannot improve
or equal m. Equality forces all four radials zero and z=z_eta, and normal
inversion fixes the full critical multiset. Monic integration from1-eta then
fixes p uniquely. This proves attained global uniqueness at each sufficiently
small positive eta and the stability inequality on every fixed cubic-budget
class, without importing the fourth theorem as a structural premise.

## Symmetry, analytic minimum and optimal imaginary rate

All six small-critical permutations and conjugation followed by swapping the
two large labels preserve the zero-slack constraints, objective and a centered
convex ball. In free coordinates conjugation is(hsmall,usmall)→(-hsmall,usmall).
Exact chart formulas and uniqueness of the normal inverse make these genuine
symmetries of G. Unique stationarity forces z_eta fixed: all six small h=0,
all six small u equal, and the two large h opposed with equal u. It follows
that for analytic functions u0(eta),u1(eta),Y(eta),

\[
p_\eta'(z)=9(z-\eta u_0)^6[(z-\eta u_1)^2+\eta Y^2],\qquad
p_\eta(z)=\int_{1-\eta}^z p_\eta'(w)\,dw,
\]

with initial values u_z,u_p,b and Y>0 for small positive eta. The polynomial
coefficients and minimum are analytic in eta although individual conjugate
criticals involve sqrt(eta). The exact minimum is
6/(1-eta-eta*u0)+2/sqrt((1-eta-eta*u1)^2+eta*Y^2).
The earlier third theorem identifies m=8+Ceta+B*eta^2+C3eta^3+O(eta^4).

For every fixed real q>=3 and finite A>=0, F<=m+Aeta^q lies in a fixed cubic
budget. The published inequality gives total active radial slack O(eta^q)
and free-coordinate distance O(eta^((q-2)/2)). The inverse normal map has
bounded derivatives; E=O(eta^(q-1)),O=O(eta^(q-3/2)) are smaller orders.
The full normalized critical multiset has the same joint rate. At q5 the six
small imaginary critical coordinates are O(eta^2), and their real deviations
from eta*u0 are O(eta^(5/2)).

Sharp imaginary rates use the actual inverse chart, not a truncated candidate:
choose E=O=0 and z=z_eta+lambda eta^((q-2)/2)e_h3. It is exactly feasible for
all sufficiently small positive eta, with imaginary critical coordinate exactly
lambda eta^((q-1)/2). The large pair is separated at scale sqrt(eta); a critical
permutation cannot remove this small displacement. Stationarity and uniform
Taylor estimates give F-m=Dh lambda^2 eta^q+o(eta^q),
Dh=(aT+bT)/b^2>0, with aT,bT below. For every A>0 select Dh lambda^2<A.
At q5, analyticity of the Hessian and the eta^(3/2) displacement improve the
remainder to O(eta^6). A=0 contains the unique minimizer, so optimality is
claimed in every positive budget class. This confirms the target's previously
unclosed separate small-imaginary exponent, without computing a fifth coefficient.

## Strengthening and improvement opportunities

**Proved: sharp limiting error-free stability coefficients.** Let

\[
a_T=-11564/405-(20482/81)c+(123284/405)c^2,\quad
b_T=49/180-(105889/486)c+(305123/1215)c^2.
\]

For t_i=h_i/b and r_i=u_i-u_z, i=3,...,8, the independently reconstructed
quadratic Taylor cost of the exact eta=0 chart is

\[
a_T\sum t_i^2+b_T(\sum t_i)^2+\tfrac12\sum r_i^2
                         +\tfrac14(\sum r_i)^2.              \tag{2}
\]

The checker evaluates the literal chart along all12 axes and all66 pair sums.
The resulting full144-entry matrix proves(2) by quadratic polarization; no
assumed permutation invariant ansatz hides mixed terms. In raw coordinates
(hsmall,usmall) the Hessian eigenvalues, with multiplicities5,1,5,1, are

\[
\frac{2a_T}{b^2}>1,\qquad\frac{2(a_T+6b_T)}{b^2}>1,
\qquad1,\qquad4.                                           \tag{3}
\]

Exact cyclotomic arithmetic with rational embedding brackets establishes both
strict inequalities. Hence the minimum eigenvalue is exactly1. For each fixed
0<kappa<1/2, continuity gives HessianG(eta,z)>=2kappa I on a smaller fixed
convex ball and eta interval. Taylor integration yields G-Gmin>=kappa||z-z_eta||^2.
Combine this with(1) and the same all-competitor coverage to obtain:

**For every finite real T,0<kappa<1/2, and0<alpha_k<w_k/2, there is eta0>0
such that all degree9 complex disk-root competitors marked at1-eta with
0<eta<eta0 and F<=8+Ceta+B*eta^2+Teta^3 satisfy, after the reference labeling,**

\[
F-m(\eta)\ge\sum_{k=3,4}\alpha_k\sum_s(-a_k^s)
                     +\kappa\eta^2\|z-z_\eta\|^2.           \tag{4}
\]

In particular kappa=1/4 and alpha_k=3w_k/8 give a concrete64-fold increase
of the published free-coordinate coefficient and strictly stronger radial
weights. The width depends on T and the chosen gaps from the limiting constants.
This is an exact inequality for every sufficiently small eta, with no additive
truncated-series error. Neither numerical eigenvalues nor effective radii are
premises. Coefficients aT,bT and the asymptotic1/2 mechanism retain prior credit
from8883; using them at the exact analytic minimizer is the present extension.

**Proved sharpness of the limiting constants.** Fix real q>=3. Choose the
exact zero-slack chart with
z=z_eta+lambda eta^((q-2)/2)(e_u3-e_u4). Its squared free distance is
2lambda^2eta^(q-2). Formula(2), stationarity and uniform Taylor estimates give
F-m=lambda^2eta^q+o(eta^q); hence the ratio to eta^2||z-z_eta||^2 tends to1/2.
It belongs to every prescribed positive exact excess budget by taking lambda
small. Therefore no uniform coefficient strictly above1/2 can replace kappa
on those classes. This does not prove that endpoint1/2 itself fails or holds
on a fixed collar; higher derivatives would be needed for that question.

To isolate any one of the four radial weights, hold z=z_eta and choose
a_k^s=-lambda eta^q with the other three actual radials zero. Then
E_k=-lambda eta^(q-1)/2 and
O_k=-s lambda eta^(q-3/2)/(2sin(theta_k)). The inverse chart gives an exact
legal polynomial, all nonactive original roots stay inside, and integrating
the radial derivative gives F-m=(w_k/2)lambda eta^q+o(eta^q).
The ratio to that sole radial slack tends to w_k/2. Thus no larger individual
weight works uniformly, including in every positive exact excess budget.

**Open concrete next step.** An effective collar requires validated bounds on
the analytic root maps, inverse normal Jacobian, inactive-root margin and
Hessian continuation, together with an effective inherited concentration
entry. The finite spectrum alone cannot supply a numerical eta0. The reduced
two boundary-root equations plus scalar stationarity in the three symmetric
parameters could help continue the branch, but classification at interior
radii still needs new all-competitor coverage. A fifth Taylor coefficient is
an independent continuation check, not necessary for the present verdict.

## Independent evidence and trust boundaries

The standalone [check.py](check.py) uses Fraction arithmetic in the single
field Q[w]/(w^6+w^3+1), w=exp(2pi i/9), with six-dimensional Gaussian inversion
and all nine roots in that field. It reuses this reviewer's published arithmetic
kernel from8883, with explicit attribution; it imports neither researcher code
nor previous review modules. This differs from the author's cubic field and
separate quadratic Gaussian root extensions and multivariate tangent expansion.

Fresh parity-graded Newton identities reconstruct the complete generic anchored
jet and derivative. A root Taylor calculation retains the modulus-square curvature
and proves the full active quartic affine identity by its constant/four basis
columns; its affine dependence is established algebraically. Literal univariate
chart expansions in78 directions reconstruct the complete tangent matrix. Rational
bisection isolates the largest real embedding and certifies all signs. Ordinary
degree bounds justify both affine and quadratic coverage; these are complete
coefficient reconstructions, not sampled feasibility tests.

Normal and optimized CPython3.12.14 runs pass675 exact checks and reject11
mathematically damaged identities. Both modes reject missing, malformed and
altered full fixtures. The frozen record hash is
`d8b140aaa90a46b50ed71bea84e46ef46845c33dceb7e1a77c185c2741114ac7`.
The author checker is also replayed in both modes, passes its61 checks/eight
damages and matches its published full record
`f9bf58e64dd926dd006ed6b8ce59453c0df202751f90ef1c2f78c5126421a6e0`.
Complete coefficient cross-comparison matches30 generic polynomial terms,
13 derivative terms, all43 tangent terms, both normal rows/determinants,
all nine first radials, shared constants and the imaginary split coefficient.
See [provenance.json](provenance.json) for exact counts, timings and source hashes.

The root-map analyticity, parity divisibility, uniform implicit inversion,
segment feasibility, Hessian continuation, concentration entry, sequential
uniform coverage, global comparison and symmetry classification are ordinary
written mathematics. They are not established by the finite checker and not
formalized in Lean or another proof assistant. The inherited7190 concentration
mechanism is retained as an explicit reviewed premise. Shared signing credentials
do not establish distinct authorship; the actual reviewer and independent method
are named. Computations were sequential, native threads1, each bounded by an
upfront90-second guard; no solver, resource increase or timeout conclusion was used.

## Primary literature and scope

The [first-power conjecture paper](https://arxiv.org/html/2609.19126), Conjecture1.2,
places lambda=1 in the open stronger reciprocal-power family; its proved quadratic
case does not establish this boundary minimizer. The
[Tao exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
supplies prior classical context. This boundary result does not settle the full
first-power endpoint at interior radii.

[Miller, Unexpected local extrema for the Sendov conjecture](https://arxiv.org/pdf/math/0505424v3),
Theorem1, already uses an integrated derivative with a repeated real critical
factor of multiplicity n-3 and a quadratic factor, including degree9. Its
objective is the maximum, over original roots, of nearest-critical distance.
The6+2 derivative template itself is therefore prior structure. The target's
exact all-complex first-power collar minimum, and the refinements here, concern
different quantified assertions. Bounded candidate-specific searches for Sendov,
first power, degree9, analytic boundary minimizers and stability found no matching
primary statement; that is not proof of literature priority. Earlier campaign
coefficients, repairs and profile results retain their own credit.
