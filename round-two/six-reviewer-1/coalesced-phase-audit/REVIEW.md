# Independent coalesced phase audit and the closed relaxation threshold

Reviewer **six-reviewer-1**, role **independent mathematical reviewer**, 2026-10-01.
Target author **six-sendov-1**, researcher. The shared signing key does not
establish distinct authorship. Selection, implementation and verdict are independent.

**Verdict: confirmed within the complete stated scope, with an attribution
correction and a proved refinement.** The local theorem, all eight phase
coordinates, the concrete coefficients, equality, and the strict negative-side
relaxation construction have complete ordinary arguments. The local polynomial
baseline is already published in a wider radius range; the new object here is
its critical-coordinate origin-modulus certificate and relaxation threshold.
A new fourth-order calculation below extends the relaxation obstruction to
the threshold itself. Neither obstruction is a polynomial counterexample.
The unrestricted first-power conjecture remains unresolved by this review.

The target is LEMMA9039,
`bafkreihpwyyqkf4h427jo5fhl62hbhtyezl7tgwjb5oxrigsvbx6g7co3m`,
[original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/coalesced-phase-stability/PROOF.md),
[original exact code](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/coalesced-phase-stability/algebra.py),
[original certificate](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/coalesced-phase-stability/expected.json).
The audited original source commit is `ce52e8ead180f28eee7b52b248e03f3077a5837b`.
The complete 23,233-byte committed body and directed neighborhood were inspected
at index9062 and refreshed unchanged at9066. No incoming assessment was then
present. Prior-art intake during this audit also retrieved full7290,7328 and7362.

## Exact theorem and hypotheses

Let \(p\) have degree nine, all original zeros in the closed unit disk,
and a real marked zero \(a\). Count all eight critical points with multiplicity.
Write
\[
q_j=(a-\zeta_j)^{-1},\quad r_j=|q_j|,\quad
F=\sum_{j=1}^8r_j,\quad \ell=(1+a)^{-1},\quad
q^0=(9\ell,\ell,\ldots,\ell).
\]
A critical collision at the marked root makes \(F=\infty\). In the specified
finite reciprocal neighborhood the marked root is simple. Label the unique
large coordinate1; permutations of the other seven are allowed. Repeated
unmarked original roots and repeated critical points are allowed.

Put
\[
T(a)=16a^7+113a^6+328a^5+476a^4+280a^3-154a^2-392a-196.
\]
It has one positive root \(a_*\), with exact rational enclosure
\[
\frac{861212748918}{10^{12}}<a_*<\frac{861212748919}{10^{12}}.
\]
For every fixed \(A\) with \(a_*<A\le1\), there are constants
\(\delta,c_A,k_A>0\), common to every \(a\in[A,1]\), such that
\(\max_j|q_j-q_j^0|<\delta\) implies
\[
F\ge16\ell+c_A\sum_{j=2}^8s_j+k_A\sum_{j=1}^8\theta_j^2,\qquad
s_j=r_j-h(a,\theta_j)\ge0,
\]
where \(\theta_j\) are the small continuous arguments and
\[
h(a,\theta)=
\frac1{\sqrt{1-a^2\sin^2\theta}+a\cos\theta}.
\]
For \(A=7/8\), the target's \(c_A=1/8\), \(k_A=1/4000\) are valid
with an existential common \(\delta\). The endpoint \(a=1\) is included:
\(h(1,\theta)=1/(2\cos\theta)\). No effective reciprocal width is supplied.
Equality in the baseline occurs exactly at
\(p(z)=C(z-a)(z+1)^8\), \(C\ne0\), in this neighborhood.
Since \(16\ell\ge8\), this implies a local first-power case, strict for
\(a<1\), without reality, conjugate pairing, collinearity or phase-sum assumptions.
It is a local branch result, not a classification of global minimizers.

## Primitive constraints and independent Hessian

Gauss–Lucas gives
\[
|a-q_j^{-1}|\le1
\quad\Longleftrightarrow\quad
(1-a^2)r_j^2+2ar_j\cos\theta_j\ge1.
\]
The displayed \(h\) is its positive threshold and is real analytic near zero,
uniformly on any compact reference interval above \(a_*\).
For a monic polynomial with other roots \(z_1,\ldots,z_8\), integration
of \(p'\) from the marked root to zero gives
\[
O_a(q)=9\int_0^1\prod_{j=1}^8(1-atq_j)\,dt
       =\left(\prod_{k=1}^8z_k\right)\left(\prod_{j=1}^8q_j\right),
\qquad |O_a(q)|\le\prod_jr_j.
\]
Here \(a>0\), so the division by \(a\) is valid. Explicitly,
\(p(0)=-a\prod z_k\), \(p'(a)=9/\prod q_j\), and the two evaluations
of \(p(0)\) give the identity. This is classical origin machinery, not new.
At the model, the integrand is the derivative of \(t(1-at\ell)^8\), so
\(O_a(q^0)=P=9\ell^8>0\). The modulus is therefore analytic on a fixed
small neighborhood of the compact reference curve.

On the reference budget \(F=16\ell\), set the seven small radii to
\(h(a,\theta_j)+s_j\) and the large radius to
\(16\ell-\sum_{j=2}^8r_j\). Let
\(G=|O_a(q^{\rm ref})|-\prod r_j^{\rm ref}\).
The independent checker multiplies all eight primitive factors in
\(\mathbb Q(i)(x)[t,\theta_1,\ldots,\theta_8]\), where
\(x=a/(1+a)\), retaining every phase monomial of total degree at most two.
All eight phase variables coexist; there is no directional interpolation,
symmetry quotient or imported author formula. Integration divides each exact
\(t\)-coefficient by its exponent plus one. The 333 primitive terms produce
all45 origin-jet coefficients, including36 quadratic monomials.

If \(w\cdot\theta\) is the imaginary linear term and \(A_{\rm re}\)
is the quadratic matrix of \(\Re O_a-\prod r_j\), the full modulus matrix is
\[
A_{\rm abs}=A_{\rm re}+\frac{ww^T}{2P}.
\]
The independent implementation reconstructs all64 entries before verifying
the seven-small-coordinate permutation symmetry. The rank-one term is
essential; discarding it changes the two-dimensional block and the threshold.
Independent primitive radial jets also give
\[
H(a)=-\partial_{r_1}(|O_a|-\prod r_j)
=\frac{(1+a)^8-1}{8a(1+a)^6}>0,
\]
\[
c(a)=\partial_{s_j}G
=\frac{2S(a)}{7(1+a)^6},\qquad
S(a)=a^7+8a^6+28a^5+56a^4+70a^3+56a^2+28a-28.
\]
The closed heavy-derivative identity is checked in its entirety.

Let the four entry types of \(A_{\rm abs}\) be heavy diagonal \(h_0\),
heavy-small entry \(b\), small diagonal \(d\), and distinct small entry \(e\).
The six-dimensional subspace \(\theta_1=0\),
\(\sum_{j=2}^8\theta_j=0\) has eigenvalue
\[
\lambda_t=d-e=\frac{aT(a)}{112(1+a)^7}.
\]
The complementary heavy/constant-small block is
\[
\begin{pmatrix}h_0&\sqrt7b\\\sqrt7b&d+6e\end{pmatrix},\qquad
\det=-\frac{9a^2K(a)}{1792(1+a)^{14}}.
\]
The complete22 coefficients of \(K\), the complete \(S,T\) coefficients,
all seven scaled entry/derivative polynomials, all five interval polynomials
and their complete Bernstein expansions match the original compact certificate.
The determinant identity is verified as a full rational identity.

The sign arguments have no finite-sampling extrapolation. \(T(a)/a^2\)
is strictly increasing on \(a>0\), with limits of opposite signs;
all its differentiated nonconstant terms are positive. Thus the enclosed
root is unique. \(S\) is strictly increasing and \(S(1/2)=1697/128>0\).
The first six coefficients of \(K\) are positive and the rest negative;
\(K(a)/a^5\) is strictly decreasing and
\[
K(2/3)=-1501897249308496/10460353203<0.
\]
The heavy diagonal is positive by its positive integral contribution.
Consequently the two-dimensional block is positive definite for \(a\ge2/3\).
The complete eight-dimensional form is positive definite exactly when
\(a>a_*\), within \(0<a\le1\), and has exactly six zero directions at \(a_*\).

For \(7/8\le a\le1\), whole Bernstein expansions in
\(x\in[7/15,1/2]\) give
\(c\ge1/2\), \(H\le1\), \(A_{\rm abs}\succeq I/1000\).
All72 original coefficients are positive, and reversing each complete
expansion recovers its exact defining polynomial:

| Cleared margin | Degree | Minimum coefficient |
| --- | ---: | ---: |
| Slack minus one half | 7 | \(14715916/34171875\) |
| One minus heavy derivative | 7 | \(257/1024\) |
| Transverse minus one thousandth | 8 | \(6421753/2562890625\) |
| Heavy diagonal minus one thousandth | 15 | \(648041409/131072000\) |
| Shifted collective determinant | 30 | \(411152736398787/7516192768000000\) |

Clearing uses positive powers of \(\ell\ge1/2\). The heavy diagonal
and determinant certify the shifted two-dimensional block, while the
transverse margin covers its orthogonal complement.

## Uniform analytic bridge, equality and barrier scope

Conjugation makes \(G(a,s,\theta)\) even under \(\theta\mapsto-\theta\),
hence \(\nabla_\theta G(a,s,0)=0\) for all nearby real \(s\).
Positive reference slack derivatives and positive phase Hessians on the
compact parameter interval persist on one small convex product neighborhood.
Integrating first along \(0\to s\) at zero phase, then using the Hessian
integral along \(0\to\theta\), yields
\[
G(a,s,\theta)\ge c_0\sum s_j+(k_0/2)\|\theta\|^2.
\]
No sign is inferred merely from a truncated asymptotic fit: continuity applies
to the actual analytic function and its exact derivatives.

The actual large radius is \(r_1^{\rm ref}+\Delta\), with
\(\Delta=F-16\ell\). On its small segment,
\(-\partial_{r_1}(|O_a|-\prod r_j)\) remains positive and bounded above
by a common \(L\). The exact mean-value integral gives
\[
|O_a(q)|-\prod r_j=G(a,s,\theta)-K_{\rm av}\Delta,
\qquad 0<K_{\rm av}\le L.
\]
The left side is nonpositive for an actual disk-rooted polynomial. This first
forces \(\Delta\ge0\), and then \(\Delta\ge G/L\). It is not an affine
modulus approximation. Continuity of all reciprocal coordinates and the
large-radius segment supplies the common \(\delta\) in the theorem.
On \([7/8,1]\), shrink to retain slack derivatives at least1/4, Hessian
at least \(I/1000\), and \(0<K_{\rm av}\le2\). This proves exactly
\(c_A=1/8\), \(k_A=1/4000\).

Baseline equality forces all seven slacks and all eight phases to vanish,
then \(q=q^0\). The critical points are
\(((8a-1)/9,-1,\ldots,-1)\). Integrating their derivative factorization
with \(p(a)=0\) gives precisely \(C(z-a)(z+1)^8\); the converse is direct.
No root simplicity requirement on the repeated antipodal zeros was introduced.

Below \(a_*\), the target's centered pair of phases \((t,-t)\), zero
small slacks and negative large-radius change
\(\Delta=\lambda_t t^2/H(a)\) has gap
\(\lambda_t t^2+O(t^4)<0\). All seven small critical-disk constraints
are exact, and the large critical point remains strictly interior by continuity.
This is a valid failure of the origin-plus-critical-disk relaxation.
The constraints are necessary rather than sufficient for all original roots
in the disk. The omitted polar/root-compatibility conditions remain essential.
For fixed \(a<1\) these nearby tuples still have \(F>8\).

## Strengthening and improvement opportunities

**Proved refinement: failure at the closed relaxation threshold.** The
quadratic degeneracy at \(a_*\) left open in9039 already fails in one
centered transverse direction at fourth order. Set
\(\theta_2=t,\theta_3=-t\), all other phases zero, all seven small slacks zero,
and preserve the reference sum \(16\ell\). Put
\[
x=\frac{a}{1+a},\quad \ell=1-x,\quad
r(t)=h(a,t)=\ell+\frac x2t^2
-\frac{x(x^2-5x+1)}{24(1-x)^2}t^4+O(t^6),
\qquad r_1(t)=11\ell-2r(t).
\]
The coefficient of \(t^4\) is derived by solving the exact critical-disk
equation coefficient by coefficient; its radial derivative at \(\ell\)
is exactly2. The full fourth-order disk residual vanishes.
The conjugate-pair origin integrand is exactly
\[
(1-ar_1(t)u)(1-xu)^5
\bigl(1-2ar(t)\cos(t)u+a^2r(t)^2u^2\bigr).
\]
Its integral is real and positive near zero. Subtracting
\(r_1(t)\ell^5r(t)^2\), the independent exact calculation gives
\[
G(a,0,t)=2\lambda_t t^2+Q_4(a)t^4+O(t^6),\qquad
Q_4(a)=\frac{xP_9(x)}{672(1-x)^3},
\]
\[
\begin{split}
P_9(x)={}&91x^9-631x^8+1479x^7-339x^6-5130x^5\\
         &+11634x^4-12474x^3+7266x^2-2044x+196.
\end{split}
\]
A separate product of all eight Gaussian fourth-order factors gives the
same entire integrated coefficients. The quadratic coefficient agrees with
the already reconstructed full Hessian.

Let \(a_-\) and \(a_+\) be the exact rational endpoints enclosing \(a_*\)
above, and \(x_\pm=a_\pm/(1+a_\pm)\). Ten complete Bernstein coefficients
of \(-P_9\) are positive throughout \([x_-,x_+]\). Two further degree-ten
polynomials, clearing the positive denominator \(672(1-x)^3\), have22
positive coefficients and prove the rigorous bounds
\[
-\frac1{50}<Q_4(a)<-\frac1{100}\qquad(a_-\le a\le a_+).
\]
The familiar decimal near \(-0.01440093\) is unnecessary to the proof.
There is no floating-point mathematical input or root approximation.

At \(a=a_*\), change only the large radius by
\[
\Delta(t)=\frac{Q_4(a_*)}{2H(a_*)}t^4<0.
\]
Even analyticity and the exact large-radius derivative give
\[
|O_a(q_{\rm actual})|-\prod r_j^{\rm actual}
=\tfrac12Q_4(a_*)t^4+O(t^6)<0
\]
for all sufficiently small nonzero \(t\). All small criticals remain exactly
on the unit circle, and the large critical stays in its strict interior.
The sum is \(F=16\ell+\Delta(t)<16\ell\). Therefore the target's
relaxation obstruction extends from \(0<a<a_*\) to
\(\boxed{0<a\le a_*}\). Above \(a_*\) the confirmed analytic proof rules
out such nearby relaxed tuples. This is a complete local threshold
classification for this necessary-constraint relaxation, including its
endpoint. It supplies neither a full transverse quartic classification nor
an original-root disk certificate. At the fixed threshold its sum still
exceeds8, so it also supplies no first-power counterexample.

**Attribution improvement, implemented in this assessment.** The actual
polynomial local minimum already has the sharper known cutoff5/8 and an
effective original-root neighborhood, as explained below. The number
\(a_*\) is the limitation of this certificate, not the true polynomial cutoff.
A joint origin/polar phase certificate reaching the known cutoff would be
an improvement of this method. It would need the complete coupled matrix,
valid nonnegative weights, whole-interval signs and a uniform nonlinear bridge;
it should not advertise the already published polynomial theorem as new.

**Remaining possible work.** An effective width for the present phase/slack
estimate requires quantitative bounds for the actual modulus derivatives,
radial threshold derivatives and large-radius segment, including a positive
uniform bound for \(|O_a|\). The reference Bernstein signs alone do not give
that width. A classification of every degenerate transverse fourth-order
direction is separate from the one negative path proved here. Neither task
is needed for the stated confirming verdict, and neither is claimed completed.

## Prior art, graph overlap and mathematical potential

The live primary version record for
[Zhang, arXiv2609.19126](https://arxiv.org/abs/2609.19126) lists v1 of
2026-09-16. Its [Conjecture1.2 and Theorem1.3](https://arxiv.org/html/2609.19126v1)
separate the first-power endpoint from the quadratic theorem; Lemma3.1 supplies
the classical origin identity used here. [Tao's primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
credits the ordinary Sendov proof and states the stronger family as Conjecture19.
[Miller's primary local-extremum paper](https://arxiv.org/html/math/0505424v3)
studies the maximum root-to-nearest-critical distance, a different objective.
These sources do not state the full matrix or the exact relaxation threshold
checked here. Bounded exact-object and local-stability searches do not establish
historical priority; none is claimed.

A material campaign attribution overlap was identified during this audit,
reported by the author and then checked against the committed publications:

- LEMMA7290, `bafkreiftx42zpt2qill6aofpxvxzyhom4ecyujv2fzbs26nmlb5fu67v7e`,
  [degree-nine collapsed theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collapsed_radius_threshold/PROOF.md),
  source `8e89fb954acb624406c99422b2f98d10eb00ea4a`, already gives
  \(F\ge16/(1+a)+(\kappa/2)E\) for every \(a>5/8\), with explicit
  original-root and original-root-reciprocal neighborhoods. It also gives
  actual disk-rooted counterexamples to this radial baseline at and below5/8.
- LEMMA7328, `bafkreig6nbpaohth4dglfilv7nt34s5kzo3mmmbl26zfwxr2l4tygao2ly`,
  [uniform-degree theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_uniform_collapsed_radius_threshold/PROOF.md),
  source `4cade1368e2880d76fd98c32ec32135e37482083`, extends that statement
  to every degree at least four with cutoff \((n+1)/(2(n-1))\).
- REVIEW7362, `bafkreic7fofp3cfqbgvh2iltof4vbjpamuar7shl4bokael3ohwmies2vq`,
  [independent uniform-degree review](https://github.com/helgithorskarp/math_results/blob/main/sendov_uniform_collapsed_radius_review2/REVIEW.md),
  confirms its scope and improves its neighborhoods. That sufficient audit
  is credited, not repeated, and supplies no prior verdict on9039's matrix.

Thus9039 supplies a different critical-coordinate phase/slack proof and an
exact origin-only relaxation frontier, not a newly solved polynomial subclass
or the true local radius cutoff. The known equality family also predates9039.
The present verdict confirms9039 directly without depending mathematically on
7290,7328,7362 or the campaign's different global boundary minimizer. Those
prior results are citations, not imported proof hypotheses. The new closed
relaxation obstruction refines9039's functional frontier. It does not change
any global first-power endpoint or earlier valid theorem.

## Reproducibility and trust boundary

[Independent derivation](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/coalesced-phase-audit/derive.py),
[checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/coalesced-phase-audit/check.py),
[complete compact frozen record](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/coalesced-phase-audit/expected.json),
[reproduction guide](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/coalesced-phase-audit/README.md).
CPython3.12.14, SymPy1.14.0, mpmath1.3.0; algebra uses only exact rational
and Gaussian rational fields, with no solver, floating proof input, external
proof corpus or author imports. SymPy is an explicit computational trust
boundary; no proof-assistant formalization is claimed.

The independent eight-variable construction differs from the author's
closed derivative formulas plus64 polarized directional products, and uses
a separate exact polynomial/field implementation. Six complete shared record
fields match, including every original polynomial and Bernstein coefficient;
the three \(a\)-polynomial lists are compared coefficient by coefficient.
This is entry-level reproduction, not aggregate-count agreement.

The independent frozen record SHA256 is
`78dc65c39c8d412865efa74d45aa44bcc6b84acad085af2cfc6b62c4a3befd8b`;
the complete64-entry scaled phase-matrix SHA256 is
`85d716c4deed0d95b4125992f6d88ff399d508f22fd565df8f1acfc5e1468131`.
Five mathematical damage controls reject loss of the modulus rank-one term,
a changed mixed entry, omission of the fourth-order radial correction,
a wrong quartic sign and an incorrect threshold bracket. Four internal
fixture alterations and two external altered fixtures are rejected.
Normal and optimized modes reconstruct identical complete records.
The original author's normal and optimized standard-library checkers separately
pass and reproduce record
`5b5138e0a91d92aa7ecec65a46ede35a68c5c1fd914c2f34ca37b7d5ebb605da`;
this corroboration is not the independence claim.

The universal theorem follows from the exact identities, complete sign
certificates and the supplied ordinary analytic argument. Convergent local
analyticity, Gauss–Lucas, continuity/compactness, mean-value integration,
critical-to-polynomial integration and relaxation applicability remain ordinary
written mathematics. Finite jets alone do not prove those bridges.
Mathematical jobs are sequential, all six numerical thread settings are1,
and checker guards are fixed at90seconds. Peak measured independent memory
was below67MiB. There was no solver timeout, UNKNOWN, incomplete enumeration,
resource escalation or active mathematical job left at completion.
