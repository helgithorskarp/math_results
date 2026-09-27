# Uniform signed endpoints on the paired-cubature rational frontier

Complete author proof; independent review pending. This supplies actual
low-threshold signs for **every non-point member** of the existing finite
rational frontier. It does not evaluate the remaining middle interval,
improve the accepted unrestricted bound `D<=7/50`, or settle majorisation.

The low-threshold theorem is R8's existing result. The contribution here
is to discharge its geometric-margin obligation uniformly from the strict
pair-loss floor already built into the rational producer. No new class of
maps, endpoint/middle equivalence, or Kneser--Poulsen result is claimed.

## 1. Explicit endpoints for every input at level k

Use exactly `A_k`, `L=256k^3`, `W=4k A_k`, and the finite rational family
`R^c_k` in [CUBATURE_FRONTIER.md](CUBATURE_FRONTIER.md), Section 5.
Coordinates are integer multiples of `1/L`, both supports lie in `B(0,3k)`,
weights are nonnegative multiples of `1/W`, and distinct labels satisfy

    |x_i-x_j|^2-|y_i-y_j|^2 >= 1/(256k^4).                 (1)

In particular source labels are distinct. Zero weights can be removed;
target sites may coincide. Let `f=sum w_i gamma_1(.-x_i)`,
`g=sum w_i gamma_1(.-y_i)`, `C=(2 pi)^(-3/2)`, and use the adverse convention

    H(u)=H_f(Cu)-H_g(Cu),       J(u)=H(u)/(Cu),     u>0.    (2)

Set the following explicit integers and rational numbers:

    l_W = ceil(log2 W),       delta_k = 1/(12288 k^5),
    B_k = 54k^2+2l_W,
    Q_k = 49152 k^5 B_k = 4 B_k/delta_k,
    e_k = Q_k^2,              tau_k = 2^(-e_k),
    b_k = 1-1/[W^2(1024k^4+1)].                           (3)

**Theorem 1.** If at least two weights are positive, then

    J(u) <= -4 pi delta_k [log(1/u)+1] < 0,
                                      0<u<=tau_k,         (4)
    ||f||_infinity/C <= b_k < 1,
    H(u) <= 0,                         u>=b_k.             (5)

In particular `J(u)<=-6 delta_k(e_k+2)` on the whole low interval. At `u=0`
the hinge difference is zero. With only one positive weight the densities
are translates, and all hinges agree; this branch needs no endpoint bound.

Thus the existing relative-window oracle only needs to sign
`[tau_k,b_k]` for a non-point input. This is an actual, simultaneous sign
certificate on the two complementary threshold ranges, not an assertion
that those endpoint inputs could eventually be found. The middle signs and
the coverage of all configurations remain missing.

## 2. Strict pair loss gives a quantitative mean-support gap

For a finite set `X` define

    hbar(X)=integral_(S^2) max_(x in X) theta.x d sigma(theta),

where `sigma(S^2)=1`. This is half the usual mean width; it is invariant
under translation. Classical mean-width monotonicity says that a labelled
contraction `X -> Z` has `hbar(Z)<=hbar(X)`. We use only this non-strict
theorem, not a quantitative version of its strictness theorem.

**Lemma 2.** Suppose there are at least two distinct positive-mass source
sites, all distinct source pairs have squared-distance loss at least
`ell>0`, and the source diameter is at most `dbar`. Then

    hbar(X)-hbar(Y) >= ell/(8 dbar).                       (6)

Weights affect which sites belong to the supports, but otherwise do not
enter this inequality.

**Proof.** Let `d>0` be the actual source diameter; necessarily `ell<=d^2`.
Put `lambda=1-ell/(2d^2)`, so `1/2<=lambda<1`. For every pair,

    |y_i-y_j|^2 <= |x_i-x_j|^2-ell
      <= (1-ell/d^2)|x_i-x_j|^2
      <= lambda^2 |x_i-x_j|^2.

Thus `X -> Y/lambda` is a contraction. Mean-width monotonicity gives
`hbar(Y)<=lambda hbar(X)`. A diameter segment contained in the source hull
has mean support `d/4`: after centering it, integrate `(d/2)|theta.e|`,
using `integral |theta.e| d sigma=1/2` in dimension three. Monotonicity
under inclusion therefore gives `hbar(X)>=d/4`. Consequently

    hbar(X)-hbar(Y) >= (1-lambda)d/4
                     = ell/(8d) >= ell/(8dbar).

The argument also permits a collapsed target. QED.

For clarity about the classical premise, it has the usual Gaussian
interpolation proof. For independent standard Gaussians `G,G'`, put
`A_i=G.x_i`, `B_i=G'.z_i`, and interpolate
`Z_i(t)=sqrt(t) A_i+sqrt(1-t) B_i`. If
`F_beta(t)=E log(sum_i exp(beta Z_i(t)))/beta`, Gaussian integration by
parts gives, for `0<t<1`,

    F_beta'(t)=(beta/4) E sum_(i,j) p_i(t)p_j(t)
                    [|x_i-x_j|^2-|z_i-z_j|^2] >= 0,

with the ordinary softmax probabilities `p_i(t)`. Finite Gaussian moments
justify the identity and endpoint limits, also for singular covariances.
The error between log-sum-exp and the maximum is at most `log(n)/beta`.
Let `beta` increase to infinity, and then use the polar decomposition of
`G`: its expected maximum equals `E|G| hbar(X)`. This proves the required
monotonicity. This standard comparison argument is included to identify
the normalization, not claimed as a new theorem. The primary literature
and historical attribution are recorded in [SOURCES.md](SOURCES.md).

In (1), take `ell=1/(256k^4)` and `dbar=6k`. Equation (6) gives exactly
the value `delta_k` in (3). This remains valid when zero weights are
removed or target sites collide. No covariance, hull rigidity, normal-fan
computation, or lower bound on a target separation is required.

## 3. Consume the existing low-threshold theorem

R8's [low-threshold lemma, Section 2](../gaussian_majorisation_open_stability/PROOF.md)
states the following at variance one, with no clouds. Suppose both finite
supports lie in a radius-`R` ball, each positive support mass is at least
`m`, and their normalized mean-support gap is at least `delta>0`. Put

    B=6R^2+2 log(1/m),            Q=4B/delta.

For every `0<u<=exp(-Q^2/2)`, its actual hinge estimate is

    H_g(Cu)-H_f(Cu) >= 4 pi delta C u [log(1/u)+1].         (7)

Its proof controls the superlevel volumes by radial graphs and integrates
their difference by layer cake. In particular it supplies a sign, not just
a tail asymptotic. We use that proof with the constants displayed there.
Repeated target sites may be aggregated; this increases their masses and
does not change the target support. Distinct source sites have masses at
least `1/W` in the rational family.

Choose `R=3k`, `m=1/W`, `delta=delta_k`. Since
`log W <= ceil(log2 W)=l_W`, the integer `B_k` is an upper bound for `B`.
Hence `Q_k` is a valid larger cutoff radius. The elementary inequalities
`1/2<log 2<1` give

    tau_k=2^(-Q_k^2) <= exp(-Q_k^2/2).

Equation (7) proves (4). Also `log(1/u)>=e_k log 2>e_k/2` for `u<=tau_k`;
using `pi>3` gives the rational margin following (5). This direction of
rounding is essential: a lower cutoff is valid, a larger one need not be.

There is a useful data-dependent version. Given rational finite input,
remove zero weights and merge identical source/image pairs. Require a
strict positive loss between every remaining distinct source pair. Supply
rational bounds `R` for both radii, `dbar` for the source diameter, the
actual minimum pair loss `ell`, and minimum positive weight `m`. Then use

    delta=ell/(8dbar),       l=ceil(log2(1/m)),
    B=6R^2+2l,              Q=4B/delta,
    E=ceil(Q^2),            tau=2^(-E).                    (8)

The same low-tail bound and rational margin hold with `delta,E`. The
producer centers each support at its weighted mean, then uses an L1 norm
as a rational upper bound on Euclidean radius and diameter. This is a
conservative geometric choice, not a fitted or sampled Gaussian estimate.
The conditions do not require the map to be strictly contracting away
from the finite support.

## 4. A uniform source-peak endpoint

This uses the standard pair-overlap peak bound, also used by R2 in
[peak pruning, Lemma 2](../gaussian_beta_peak_pruning/PROOF.md). For
`F=f/C`, Gaussian multiplication gives, at every `z`,

    F(z)^2 <= sum_(i,j) w_i w_j exp(-|x_i-x_j|^2/4).

Choose any distinct positive pair. If each of its weights is at least
`m` and its squared source separation is at least `ell`, then

    F(z)^2 <= 1-2m^2[1-exp(-ell/4)]
            <= 1-2m^2 ell/(4+ell).

Here `exp(-t)<=1/(1+t)` for `t>=0`. Since
`sqrt(1-2v)<=1-v` for `0<=2v<=1`, this proves

    ||f||_infinity/C <= b=1-m^2 ell/(4+ell).               (9)

The requirement `2v<=1` follows from `m<=1/2` and `ell/(4+ell)<1`.
In the rational family use `m=1/W` and `ell=1/(256k^4)`, obtaining `b_k`.
This is a source-only bound. The target may have peak one, for example
when all its sites coincide. For every `u>=b` the source hinge is zero,
so the adverse difference is nonpositive. No target-peak gap is needed.

## 5. What the certificate does and does not make effective

The output [SIGNED_ENDPOINT_EXPECTED.json](SIGNED_ENDPOINT_EXPECTED.json)
stores `tau` as the pair `(base=2, negative_exponent=E)`. It never expands
the integer `2^E`. The exponent and the upper endpoint are exact, small
descriptions even when writing the full dyadic denominator would be
impractical. The value `2 ceil(Q)` is a certified upper bound for
`sqrt(2 log(1/tau))`, so a subsequent relative-window computation has an
explicit logarithmic radius. This does **not** mean its large precision,
spatial grid or complete parameter coverage has been computed.

At fixed `k` this certificate signs both endpoints for the entire finite
input family. The remaining interval is explicit and bounded away from
zero. On any supplied input, a gap-free cover of that interval by valid
[relative-window certificates](RELATIVE_HINGE.md) with nonpositive adverse
upper bounds finishes all thresholds, by R8's existing
[endpoint/middle architecture](../gaussian_majorisation_open_stability/CERTIFICATE_INTERFACE.md).
There is no promise that such a cover exists for an unresolved input.

The analytic endpoint is useful to both direct-hinge and beta consumers;
it does not require either oracle's implementation as a theorem premise.
It does not sign a whole beta average whose support extends into the
unknown middle. In particular it does not bypass R2's new all-order
conditional-kernel obstruction or settle the first unsigned beta entry.

The uniform radius `Q_k` is very conservative. As `A_k=O(k^3 log^(3/2) k)`,
`Q_k=O(k^7)` and `e_k=O(k^14)`. These are explicit bounds for a **signed**
endpoint, not a new atom/degree reduction, a practical exhaustive-search
proposal, or an improvement of the global defect constant. No new
Kneser--Poulsen consequence or unrestricted theorem follows here.

## 6. Reproduction and trust boundary

With standard-library CPython 3.11 or later, from this directory:

    python3 -B signed_endpoints.py --check
    python3 -B -O signed_endpoints.py --check
    python3 -B signed_endpoints.py --budget 64
    sha256sum -c SHA256SUMS

Expected status: `SIGNED_FRONTIER_ENDPOINTS_PASS`. An optional `--instance`
accepts the source/target/weights/variance-one rational schema used by the
hinge oracle and emits a data-dependent endpoint certificate. The normal
`--check` path compares the complete expected record and all pinned
dependencies, rejecting a changed cutoff, peak bound or claimed margin.

The exact controls exercise the contraction-to-homothety inequality,
collinear mean-support normalization, source-peak inequalities, the existing
rational-family budgets, translation and signed-permutation invariance,
zero weights, source collisions, target collisions, and the point branch.
They also reject malformed or ineligible non-strict inputs. No Gaussian
integral, mean-width quadrature, floating optimization, or large enumeration
is used. The written mean-width argument and R8's analytic low-tail lemma
remain unformalized premises; arithmetic controls do not replace their
proofs or independent mathematical review. Pinning a source records the
dependency being consumed, not acceptance of every result in its directory.
