# Finite-atomic inputs and a bounded-law certificate interface

Author derivation, 26 September 2026; independent review is pending. This
makes the existing [finite certificate](BOUNDED_LAWS.md#7-a-finite-positive-certificate-at-one-fixed-variance)
usable as a precise dependency for the finite-atomic lane. It also replaces
its global one-half Holder localization loss by an optional local Lipschitz
loss on a fixed positive threshold interval. No new positive geometric
class, certified unknown Gaussian pair, or full R3 theorem is asserted.

All arguments below are at **one fixed variance**. They require neither a
semigroup comparison nor an optimizer localization, and do not supply those
other lanes' missing signs. [HANDOFF.md](HANDOFF.md) records the class and
quantifier landscape. [certificate_arithmetic.py](certificate_arithmetic.py)
is an exact arithmetic consumer and conformance audit, not a generator of
Gaussian moment enclosures or a verifier of unspecified analytic premises.

## 1. The normalized moment contract

Let f=mu*gamma_s and g=nu*gamma_s, with bounded probability laws on R3 and
covariance s I3, s>0. Put C=(2 pi s)^(-3/2) and

\[
 H(u)=\int(g-Cu)_+-\int(f-Cu)_+,\qquad
 A_m(f)=C\int(f/C)^m=C^{1-m}\int f^m.                    \tag{I1}
\]

Thus A_1=1 and 0<=A_m<=1. A producer supplies **rigorous enclosures** of
A_m(f), A_m(g), for m=2,...,N+2, all for the same laws and variance.
The consumer uses

\[
 a_j=\frac{A_{j+2}(g)-A_{j+2}(f)}{(j+1)(j+2)},\qquad
 b_{N,k}=(N+1){N\choose k}\sum_{l=0}^{N-k}
                (-1)^l{N-k\choose l}a_{k+l}.             \tag{I2}
\]

These are exactly a_j=integral_0^1 u^j H(u)du and
b_(N,k)=E H(V), V~Beta(k+1,N-k+1), from the
[global criterion](../gaussian_majorisation_global_criterion/PROOF.md).
They are dimensionless. In particular the input is not raw integral f^m,
not its difference without the C factor, and not an individual positive
energy gap substituted for the alternating expression in (I2).

For finite atomic mu=sum_i p_i delta_(x_i), completing the square gives

\[
 A_m(f)=m^{-3/2}\sum_{i_1,...,i_m}p_{i_1}\cdots p_{i_m}
 \exp\!\left[-\frac1{2sm}\sum_{a<b}|x_{i_a}-x_{i_b}|^2\right].
                                                               \tag{I3}
\]

The finite-atomic producer owns how this sum is evaluated and enclosed.
Multiplicity compression, interval exponentials, cancellation control and
parameter-box bounds must retain their own proofs. The present consumer
performs signed interval linear arithmetic; it does not turn floating-point
values into certified input. Large alternating coefficients can make loose
independent moment intervals ineffective.

## 2. A source peak bound from the same absolute moments

For every integer m>=2,

\[
 \|f\|_\infty/C\le [m^{3/2}A_m(f)]^{1/m}.                 \tag{I4}
\]

Indeed, for independent samples X_1,...,X_m, the identity

\[
 \sum_a|x-X_a|^2=m|x-\overline X|^2+
                     m^{-1}\sum_{a<b}|X_a-X_b|^2
\]

bounds (f(x)/C)^m by the expectation of the exponential in (I3), which is
m^(3/2) A_m(f). This proof also holds for arbitrary bounded laws by Tonelli;
no atom enumeration is needed for its validity. If U_m>=A_m(f) is a
nonnegative rational upper bound and b>0 is rational, the entirely rational
condition

\[
                  m^3 U_m^2\le b^{2m}                  \tag{I5}
\]

therefore certifies ||f||_infinity/C<=b. Absolute source moments, rather
than only target-minus-source differences, are essential for this input.
The bound converges to the actual normalized peak as m tends to infinity:
||f||_m tends to ||f||_infinity for a bounded probability density, while
the mth roots of m^(3/2) and the fixed normalization factor tend to one.
This is not a practical degree assertion.

An exact Gaussian control for (I4)--(I5) is mu=(delta_(-e1)+delta_(e1))/2,
s=1/(2 log 2). For m=4, the expectation in (I3) is

\[
 2^{-4}\sum_{j=0}^4{4\choose j}2^{-j(4-j)}=27/128,
 \qquad A_4=27/1024.
\]

It certifies a source peak bound b=7/10. The same fourth-moment test fails
for b=2/3, which is only failure of this bound, not a lower bound on the
actual peak. This is a peak-input control, not a Gaussian majorisation
certificate.

## 3. Local threshold control improves the beta error

Suppose the supports fit, after separate translations, in radius-R balls,
and set r=R/sqrt(s). For 0<d<1 define

\[
K_d=\min\!\left\{\frac1d,\frac{\sqrt{2/\pi}}3
               [r+\sqrt{2\log(1/d)}]^3\right\}.        \tag{I6}
\]

**Local modulus.** H is K_d-Lipschitz on [d,1], and its oscillation over
[0,1] is at most one.

For a law in B(0,R), f(x)/C is at most
exp(-((|x|-R)_+)^2/(2s)). Its superlevel volume at Cu is therefore at most
(4 pi/3)[R+sqrt(2s log(1/u))]^3. Layer cake gives, for d<=v<=u<=1,

\[
 H(u)-H(v)=C\int_v^u[V_f(Ct)-V_g(Ct)]\,dt.
\]

Both volumes lie between zero and the same upper bound, so their difference
has absolute value at most that bound, not their sum. Multiplication by C
gives the geometric term in (I6). This proof uses no regular-level assumption. For arbitrary
0<=v<=u<=1, each individual hinge decreases by a number in [0,1]. The
difference of those two decreases lies in [-1,1], proving the oscillation
claim. The alternative bound 1/d needs no support information: probability
normalization gives Cu V_f(Cu)<=1 and Cu V_g(Cu)<=1, so the same layer-cake
identity gives |H(u)-H(v)|<=|u-v|/d on [d,1]. Thus **K=1/d is an exact
automatic choice** for rational d. A rational upper bound for the geometric
term can improve it: r_bar>=r, q>=0 and q^2>=2 log(1/d) give the valid
K=min(1/d,(r_bar+q)^3/3), using pi>2. Only this optional improvement needs
the producer's certified support and scalar bounds.

Fix the endpoint inputs of the old theorem:

\[
 H\ge0\ \hbox{on }[0,\tau],\quad
 \|f\|_\infty/C\le b,\quad 0<d<\tau<b<1.                 \tag{I7}
\]

For one N>=0 put

\[
 h=(N+2)^{-1},\quad t_k=(k+1)/(N+2),\quad
 v_k=t_k(1-t_k)/(N+3),
\]
\[
 J_N=\{k:0\le k\le N,\ \operatorname{dist}(t_k,[\tau,b])\le h\},
\quad
 p_k=\begin{cases}
 1,&t_k\le d,\\
 v_k/[v_k+(t_k-d)^2],&t_k>d.
 \end{cases}                                             \tag{I8}
\]

**Localized finite certificate.** If certified lower bounds ell_k<=b_(N,k)
satisfy

\[
       \ell_k>K\sqrt{v_k+h^2}+p_k\qquad(k\in J_N),       \tag{I9}
\]

then every hinge compares at variance s. As before, all finite endpoint
Hankel matrices on distinct nonnegative integer exponents are positive
definite. Only the moment powers through N+2 enter.

To prove this, first p_k bounds P(V<d). For t_k>d, apply Markov's inequality
to (t_k-V+lambda)^2 on {V<=d}, then choose lambda=v_k/(t_k-d); this gives
the one-sided variance bound in (I8). For t_k<=d use one.
For any u in [tau,b] within h of t_k, use the local modulus on {V>=d} and
the global oscillation bound on its complement. Thus

\[
 |b_{N,k}-H(u)|
 \le K E|V-u|+P(V<d)
 \le K\sqrt{v_k+(t_k-u)^2}+p_k
 \le K\sqrt{v_k+h^2}+p_k.                                \tag{I10}
\]

Every point of [tau,b] has such an index in J_N. Equation (I9) gives
strict positivity on this whole interval. The first endpoint in (I7)
handles the low thresholds; above b the source hinge is zero. A nonzero
polynomial squared integrates positively against H on [tau,b], giving
the Hankel assertion. This is the same endpoint/middle architecture as
Theorem C, with a different rigorously bounded localization error.

For fixed 0<d<tau<b<1 and a fixed valid K, the error is uniformly O(N^(-1/2))
on J_N. In fact once h<=(tau-d)/2,

\[
 p_k\le\frac1{(N+3)(\tau-d)^2},\qquad
 v_k+h^2\le\frac1{4(N+3)}+h^2.                            \tag{I11}
\]

This refines the old global Holder O(N^(-1/4)) rate on a fixed positive
threshold interval. It is not necessarily smaller at each finite N. Either
valid bound can be used, separately at each selected k. For every interior
pair, fix endpoint choices as in BOUNDED_LAWS.md and choose d<tau. With
h_*=min_[tau,b]H>0, the uniform error eventually falls below h_*/2; (I10)
then proves all the tests. Completeness on the interior is preserved. A
tiny certified tau or a small middle margin can still make the required
degree impractical. No useful degree for an unresolved contraction is
claimed by these estimates alone.

If ell_k,K,p_k are rational, (I9) is equivalent to the exact sign checks

\[
 \ell_k-p_k>0,\qquad
 (\ell_k-p_k)^2>K^2(v_k+h^2).                             \tag{I12}
\]

The old Holder test similarly uses ell_k>0 and
ell_k^4>L^4[1/(4(N+3))+h^2]. No rounded root is needed in the consumer.

## 4. The bounded-law transport interface

Suppose atomic reference laws f_0,g_0 have certified beta lower bounds
ell_k and a normalized source peak bound b_0. Let the actual, possibly
nonatomic, endpoint laws have density errors

\[
 \|f-f_0\|_1\le e_f,\quad \|g-g_0\|_1\le e_g,\quad
 \|f-f_0\|_\infty/C\le e_f.                              \tag{I13}
\]

At this same variance, each W_infinity displacement epsilon_f,epsilon_g
supplies e_f=epsilon_f/sqrt(s), e_g=epsilon_g/sqrt(s). Integrate the
Gaussian directional derivative, whose L1 norm is sqrt(2/(pi s)) and
whose supremum is C/sqrt(e s); both are bounded by the displayed coarse
constants. Independent atom-weight changes additionally cost their L1
weight differences in the corresponding e values, provided the tail's
assigned mass floor remains valid.

Since a hinge is 1-Lipschitz in density L1, **every beta average** changes
by at most eta=e_f+e_g. This avoids propagating an error separately through
the large alternating coefficients in (I2). The perturbed peak is at most
C(b_0+e_f). Consequently it suffices to provide, uniformly over the cloud
family:

- b_0+e_f<=b<1;
- the actual signed endpoint H>=0 on [0,tau];
- a local K valid for the actual laws; the automatic K=1/d remains valid
  without any support update;
- ell_k-eta>K sqrt(v_k+h^2)+p_k for all k in J_N.

The conclusion is every hinge for **every** law pair in that family at
this variance. A contraction map is not implied by independent endpoint
clouds, and must be certified separately when a pair is used for the
named problem. An all-variance neighborhood or a small-variance geometric
limit is not supplied.

Here is a fully explicit source for the signed endpoint, using only the
existing [low-threshold lemma](PROOF.md#2-low-thresholds-with-a-positive-geometric-margin).
Let both reference supports have assigned cluster masses at least m>0,
cloud radii at most epsilon, and |X_i|+epsilon,|Y_j|+epsilon<=R. Supply

\[
 \overline h_X-\overline h_Y-2\epsilon\ge\Delta>0,
 \quad B=6R^2+2s\log(1/m),\quad Q=4B/\Delta.
\]

Then any 0<tau<=exp(-Q^2/(2s)) is valid uniformly for those clouds.
Certified upper bounds for log(1/m) and Q, and a certified lower bound for
exp(-Q^2/(2s)), may be used in the indicated directions. The mean-support
comparison is a geometric obligation; it is not inferred from finite
moment positivity. For bounded nonatomic reference laws the finite-net
construction in [BOUNDED_LAWS.md](BOUNDED_LAWS.md#2-finite-support-nets-retain-positive-cluster-masses)
produces positive assigned cell masses and a W_infinity error. Fix the net
before the tail cutoff; its mass floor need not survive arbitrary refinement.

## 5. Exact connection to the unrestricted target

Use the existing [strict rational-witness reduction](../gaussian_majorisation_rank_abel/PROOF.md)
and the [interior/homothety theorem](BOUNDED_LAWS.md#6-the-interior-characterization-and-density).
The following statement is equivalent to the full bounded-law R3 conjecture:

> For every finite rational contraction instance at variance one, with
> positive rational weights, at least two distinct source sites, and every
> pair of distinct source sites strictly contracted, there exists a finite
> certificate of the form (I7)--(I9). Its peak bound can use (I5), and its
> signed endpoint can use the finite-support mean-width lemma in Section 4.

This is a composition of credited results, not a new extremal localization.
Here is both directions with the equality cases retained. If every such
instance has a certificate, no strict rational counterexample can exist.
The rational-witness reduction therefore excludes any bounded-law violation.
A one-point source is a trivial Gaussian-translation equality case.

Conversely suppose the full conjecture holds, and fix one strict finite
instance. Translate its target, which does not change any hinge. If the
target is nonpoint, choose rational c with

\[
 \max_{i\ne j}\frac{|y_i-y_j|}{|x_i-x_j|}<c<1.
\]

The finite map x_i -> y_i/c is still a contraction. Apply the conjecture
to it (using the finite-map extension already used in the rational reduction),
then apply strict target homothety by c. The original pair is in the exact
interior. If the target is a point, the nonpoint source/point target case
of the same interior theorem applies directly. In both cases its mean-width,
peak and middle-hinge gaps are strict. The signed finite-support endpoint
exists; (I4) converges to the source peak; choose b strictly below the target
peak and above a sufficiently sharp finite-moment source bound. Choose
d<tau and apply the completeness following (I11). This supplies the finite
certificate. Increase N if needed to include the power used for the peak.

The order is **for every instance, there exists a finite certificate**.
No universal degree, uniform margin, finite exhaustive list, practical
certificate search or new proof of that universally quantified statement
is supplied. This identifies exactly what a positive finite-atomic mechanism
would have to establish to settle the unrestricted target through this
interface. Its missing sign cannot be replaced by bare finite positivity.

The [eight-lane handoff](../gaussian_majorisation_global_criterion/INTERFACES.md)
also retains the [rigid-mesh reduction](../gaussian_majorisation_extremal_maps/PROOF.md).
Its tight mesh edges and the all-pair strictness used above describe different
test classes. They are not simultaneous hypotheses on one nontrivial mesh.
The equivalence here uses the older strict rational reduction; it neither
constructs a mesh nor localizes an extremal map.

The measure lane's [defect localization](../gaussian_prior_localization/DEFECT_LOCALIZATION.md)
instead bounds the global defect by compact finite maxima D_k with
0<=D-D_k<4/k. Its k controls support radius and atom count; our N controls
moment degree. A certificate for one law pair does not bound D_k uniformly.
Those compact parameter sets include zero weights, repeated sites and
equality pairs, so their compactness alone does not supply a uniform strict
certificate margin or degree from the interior theorem.

## 6. Producer/consumer responsibilities for researcher 2

| Producer evidence | What the functional consumer uses | What remains outside that evidence |
|---|---|---|
| Probability weights, sites, s, law identifiers and rigorous A_m intervals | (I1)--(I2), with exact signed interval arithmetic | A mismatched normalization, variance or law is not repaired by the consumer. |
| An absolute source moment upper bound U_m | Rational peak condition (I5) | Positive target-minus-source moments alone supply no source peak bound. |
| A signed threshold endpoint certificate and tau | Low part of (I7) | An unsigned tail error is insufficient. |
| Rational d<tau; use automatic K=1/d, or certify a better local K | Local modulus and (I8)--(I12) | Only an optional sharper geometric K needs extra support/scalar enclosures. Sampling a peak or hinge is insufficient. |
| Optional transport/weight budgets and uniform cluster data | Direct beta error eta, peak reserve, enlarged support and signed tail | No automatic contraction, optimizer localization or all-variance statement. |
| Certified strict beta margins for every selected index | All thresholds and all energy orders at the fixed variance | Finite bare positivity, missing indices and failed tests do not settle the sign. |

The [finite orthogonal averaging obstruction](../gaussian_majorisation_finite_orbit_obstruction/PROOF.md)
closes a stronger pointwise route for all square-cone weights. It neither
invalidates this integrated certificate nor certifies its missing inputs.
The [all-prior set-transfer criterion](../gaussian_prior_localization/PROOF.md)
has a different all-law quantifier; no atomic optimizer is assumed here.
The [heat-profile work](../gaussian_majorisation_heat_profiles/PROOF.md)
retains its evolution equation and signed forcing obligations. None of
those three routes is reproduced by the fixed-s estimates above.

## 7. Exact controls and trust boundary

From this directory, with standard-library CPython >=3.11:

```sh
python3 certificate_arithmetic.py --check
python3 -O certificate_arithmetic.py --check
sha256sum -c SHA256SUMS
```

[INTERFACE_EXPECTED.json](INTERFACE_EXPECTED.json) records exact checks of
normalization, two independent beta formulas, signed interval extremization,
selected-index coverage, the one-sided beta-tail bound, strict inequalities,
transport margins, and the Gaussian fourth-moment peak control. The improved
local test and the old Holder test are compared on H(u)=u(1-u). That
polynomial is an arithmetic control, **not** an asserted Gaussian hinge gap;
its positive result is not a new Gaussian comparison.

The module exposes arithmetic functions for an enclosing producer to import.
Passing `lipschitz_constant=None` uses the automatic K=1/d; an explicit
smaller constant is an external analytic obligation.
Its self-check cannot attest that a caller's moment intervals or analytic
endpoint/support evidence belong to any Gaussian law. It does not output an
unconditional Gaussian theorem from unaudited scalars. The analytic derivation,
external enclosure validity, finite-net/mean-width bounds and contraction
verification remain distinct trust obligations. The original BOUNDED_LAWS.md,
PROOF.md and all earlier finite certificates are unchanged.
