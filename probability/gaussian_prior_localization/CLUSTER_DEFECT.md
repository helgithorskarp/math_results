# Source-cluster certificates for the full Gaussian hinge defect

Complete author proof, with a finite exact certificate producer; independent
review pending. The result combines the existing source-interaction
localization with R8's new small-radius estimate. It supplies a practical
all-threshold upper bound on parts of the unchanged finite frontier,
including source configurations of large total radius. The unrestricted
bound `D<=7/50` and the full open question are unchanged.

No target separation is required: a contraction may merge all the source
clusters. The local component errors and the source classification error
are both retained. The argument does not infer preservation of majorisation
under arbitrary conditioning or mixing.

## 1. A certificate from source balls

Let `gamma_s` be the probability Gaussian of covariance `s I_3`, `s>0`.
For a probability law `mu` and a contraction `T` define

    Delta_s(mu,T)=sup_(a>=0) [H_(mu*gamma_s)(a)
                                -H_((T#mu)*gamma_s)(a)]_+,
    H_f(a)=integral (f-a)_+.

Suppose a bounded law has a finite labelled decomposition

    mu=sum_(i=1)^M p_i mu_i,       p_i>=0, sum p_i=1,
    supp(mu_i) subset B(c_i,r_i),

where the source centers `c_i` are distinct. Zero-mass components can be
discarded. The component measures can be arbitrary Borel probabilities,
including diffuse laws. The balls need not be disjoint. The same map `T`
acts on every component.

Write `d_ij=|c_i-c_j|`. For `t` real put

    psi(t)=1                    if t<0,
           (1/2) exp(-t^2/2)   if t>=0,
    eta_i=min{1, sum_(j!=i) psi((d_ij/2-r_i)/sqrt(s))}.     (1)

Let `E_i` be any valid upper bound for `Delta_s(mu_i,T)`.

**Theorem 1 (weighted cluster bound).** Then

    Delta_s(mu,T) <= min{7/50, sum_i p_i(E_i+eta_i)}.       (2)

Consequently `min{7/50,max_i(E_i+eta_i)}` is valid simultaneously over
every choice of component masses. These are upper bounds, not signs when
the right side is positive.

The input to (2) is only a finite source-ball cover with component masses
and valid local defect estimates. For the concrete producer below use

    E(r,s)=0,                                r=0;
           16k 2^(-5k), k=floor(s/(8r^2)),   k>=2;
           7/50,                            otherwise.   (3)

Equation (3) is exactly the sufficient dyadic bound from R8's
[small-radius theorem](../gaussian_majorisation_high_noise_window/SMALL_RADIUS_DEFECT.md),
not a new proof or a sharper version of it. That theorem now has
[independent acceptance](../gaussian_small_radius_defect_review_frontier/REVIEW.md),
including the required signed-window part of its
[high-noise premise](../gaussian_majorisation_high_noise_window/PROOF.md).
The review does not accept every other result in that high-noise packet.
The radius-zero branch is
equality of translated Gaussians; `k>=2` makes the dyadic bound smaller than
the independently accepted `7/50` cap.

### Proof of the source-interaction estimate

Let `f_i=p_i(mu_i*gamma_s)` and `g_i=p_i((T#mu_i)*gamma_s)`.
The [existing partition inequality](DEFECT_LOCALIZATION.md), Lemma 2,
applies to any measurable partition `V_i` of observation space:

    H_f(a)-H_g(a)
       <=sum_(p_i>0) p_i[H_(f_i/p_i)(a/p_i)
                            -H_(g_i/p_i)(a/p_i)] + Lambda,
    Lambda=sum_i integral_(R3 minus V_i) f_i.              (4)

Its pointwise proof uses nonnegativity of target hinge interaction and
bounds source interaction by the mass outside the selected label. It only
needs a decomposition into nonnegative matched subdensities, so it also
applies to overlapping labelled component measures. In particular it does
not require the label to be a deterministic function of a source point.
The threshold is correctly rescaled by `p_i` before using the local bound.

Choose the ordinary nearest-center Voronoi partition, breaking ties by
index. Distinct-center ties lie in finitely many hyperplanes and have zero
probability after Gaussian smoothing. Conditional on component `i`, write
the observation as `X_i+Z`, where `|X_i-c_i|<=r_i` and
`Z` is `N(0,s I_3)`. If center `j` is at least as close as center `i`,
then for `v=(c_j-c_i)/d_ij`,

    v.Z >= d_ij/2-v.(X_i-c_i) >= d_ij/2-r_i.              (5)

The scalar `v.Z/sqrt(s)` is standard normal. For `t>=0` its upper tail
satisfies

    Pr{N(0,1)>=t}
      = exp(-t^2/2) integral_0^infinity
             exp(-tv) exp(-v^2/2)/sqrt(2pi) dv
      <= (1/2) exp(-t^2/2).                              (6)

For `t<0` use the bound one. The union bound over wrong labels gives the
probability at most `eta_i`. Therefore `Lambda<=sum_i p_i eta_i`.
Taking the supremum in (4) proves (2), including the separate known cap.
This is the earlier localization mechanism with a geometrically certified
error, not cancellation or an assumed sign of the interaction. QED.

Neither (5) nor the error bound contains a target center. For (3), each
restricted map is a contraction on the component support. A finite input
map can be extended by the usual Kirszbraun premise, so the source radius
is also a radius bound for its image after centering at `T(c_i)`. The
executable chooses source-site anchors, so no extension is needed to check
that radius on its finite components.

## 2. A complete parameter region with a small numerical bound

At variance one, take any seven distinct source centers with all pair
distances at least16. Allow **arbitrary** component laws in balls of radius
at most1/8 about those centers, arbitrary probability masses, and every
contraction on the resulting support. Equation (3) gives `E_i<=2^(-33)`.
Equation (5) has normalized margin at least `8-1/8=63/8`, and

    (63/8)^2/2=3969/128>31,
    eta_i <= 6*(1/2) exp(-3969/128) < 3*2^(-31).

Using `e>2` yields the actual all-threshold certificate

    Delta_1(mu,T) <= 13*2^(-33) < 1/500000000.             (7)

No endpoint or middle hinge is numerically evaluated. The assertion covers
every admissible target placement, including merged images, and diffuse
source components. It does not assert `Delta_1=0`.

For a concrete region of the team's existing rational family, use centers

    0, +16e1, -16e1, +16e2, -16e2, +16e3, -16e3.

Every such source lies in `B(0,129/8) subset B(0,24)`, the source-radius
part of `R^c_8`. Thus (7) bounds the defect of all members of `R^c_8` whose
source labels lie in these seven small balls, with every allowed weight
vector and every target satisfying the family constraints. Such members
cannot witness a violation larger than the bound in (7); smaller
violations remain possible. The target-radius and
strict-loss requirements are not removed by this statement. The theorem
also holds beyond those finite constraints.

[CLUSTER_FIXTURE.json](CLUSTER_FIXTURE.json) gives49 labels, seven in each
ball, with the exact `L_8,W_8` grids and strictly contracting targets. Each
seven-label component has paired affine rank six. It tests the original
finite contract and the certificate producer; its full hinge sign is not
asserted. The statement about the whole region follows from the geometric
inequalities above, not from this fixture or a sample search. Checking only
the total source radius would give the previous `7/50` fallback here.

### A tolerance schedule with error tending to zero

For an integer `b>=0` and `M>=2`, put

    k=1+ceil((b+1)/4),          l=ceil(log2(M-1)).

If every `r_i^2/s<=1/(8k)` and every pair has

    d_ij >= 2 max_h r_h + sqrt(2s(b+l)),                  (8)

then (3) and R8's existing tolerance arithmetic give `E_i<=2^(-b-1)`.
Equations (1) and (6) give `eta_i<=2^(-b-1)`, since
`M-1<=2^l` and `e>2`. Hence

    Delta_s(mu,T)<=2^(-b).                               (9)

This is uniform over masses, all source measures in those balls and all
contractions. It gives a decreasing defect estimate for the certified
source geometry; it is **not** a sequence of improved unrestricted global
bounds. For `M=1` only the local radius estimate is needed.

## 3. Exact finite producer and automatic partition selection

`cluster_defect.py` consumes rational finite coordinates, probability weights,
and positive rational variance. It checks every supplied pair contraction,
removes zero-weight labels for the law, and merges identical source/image
pairs. The source distances divided by the variance are exact rationals.
Thus common spatial scaling and variance scaling cancel before any root
enclosure. The target enters validation only; the bound uses source geometry.

Candidate partitions are the connected components of the complete source
distance graph as its edge threshold increases. Equal distances are processed
together. This is a deterministic proposal rule, not a claim that the best
partition must be a single-linkage cut. There are at most `n` distinct
partitions, including all singleton labels and one component. Every candidate
is independently evaluated by (2). The returned bound is the smallest
certified value found, capped by `7/50`.

Within a component the producer selects the member minimizing its maximum
squared distance to the other members. This is an exact source-site anchor
radius, not a minimum enclosing ball. It bounds each normalized radius from
above and each normalized anchor separation from below by rational dyadic
square-root enclosures. If a certified separation becomes zero, or the
resulting margin is negative, it uses error one. Thus ambiguous or overlapping
geometric bounds never create a false sign.

The output precision is an upward dyadic grid `2^(-p)`. For a nonnegative
certified margin `t`, set `q=floor(t^2/2)`. Then

    psi(t) <= 2^(-q-1).

If this is below one output unit, replace it by one unit, not zero.
The local error `16k2^(-5k)` is likewise rounded upward using integer bit
lengths; no huge power is expanded when the exponent is much larger than
the requested precision. Component errors are mass-weighted before a final
upward rounding. The per-candidate rounding overhead is at most
`(M+1)2^(-p)` compared with the exact values of (3) and the already
coarsened probabilities `2^(-q-1)` at the same root enclosures. This
rounding statement excludes the separate losses from the root enclosures
and from replacing the exponential by `2^(-q-1)`. The printed all-masses
bound instead takes the largest rounded component cost. It applies only
to the certified active components (or measures in their displayed
balls); discarded zero-weight sites outside these balls cannot be
activated without checking a new cover.

This is a certificate producer with a small exact proposal search. It never
enumerates `R^c_k`, all possible partitions, Gaussian values, or hinge knots.
The direct implementation uses at most `O(n^3)` rational comparisons and
arithmetic operations for its partition candidates, and `O(n^2)` stored
source distances. Bit costs are not constant. The49-label replay is small;
no claim of feasibility at the worst-case cubature atom budgets is made.

## 4. Reproduction, dependencies and limits

From this directory with standard-library CPython3.11 or later:

    python3 -B cluster_defect.py --check
    python3 -B -O cluster_defect.py --check
    python3 -B cluster_defect.py --input CLUSTER_FIXTURE.json
    sha256sum -c SHA256SUMS

Expected status: `SOURCE_CLUSTER_DEFECT_CERTIFICATES_PASS`.
[CLUSTER_EXPECTED.json](CLUSTER_EXPECTED.json) contains the complete compact
record; [CLUSTER_INPUTS.json](CLUSTER_INPUTS.json) pins the consumed sources.
Controls check the finite mixture inequality directly on small rational
arrays, half-space algebra, root enclosure directions, upward error rounding,
the dyadic schedule, the entire49-label original rational contract, local
paired ranks, rescaling, collisions, zero weights and invalid-map rejection.
The ordinary and optimized runs must agree. Damaging the reported upper bound
must fail the expected-record check.

The new proof rests on the existing localization inequality, elementary
Gaussian tails, R8's now independently accepted local defect theorem and
the previously accepted global cap. Its exponential estimate still rests
on the written analytic high-noise argument audited in that review. The
new cluster composition has not itself been independently reviewed, and
exact arithmetic controls do not formalize its analytic premises.
There is no external numerical
library, floating sign, solver, hidden data or large omitted certificate.

The result provides an all-threshold exclusion budget on actual source
parameter regions. It is complementary to the signed endpoints and relative
window oracle, and it preserves the original localization and rational
budgets. No positive `E` certifies exact majorisation, and the estimate lacks
the threshold-relative small-variance control needed for a new
Kneser--Poulsen conclusion. The full dimension-three conjecture remains open.
