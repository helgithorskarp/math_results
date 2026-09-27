# A full prior simplex with extended Gaussian targets

Complete author proof with exact computation, 27 September 2026.
Independent review of this extension is pending. The unrestricted
dimension-three Gaussian-majorisation problem remains open.

This extends the independently accepted
[deep-flap coordinate cell](../gaussian_deep_flap_cell/PROOF.md) along its
measure variables. Unlike the earlier near-point prior cell, the target
mixture here changes with the prior and has extended support. A common
supporting plane for its hinge resolves this nonconvex dependence. The
new finite obligations are two weighted middle curves and a uniform
weighted low-tail cover; the equal-prior certificate is not simply reused.

## 1. The measure cell and its conclusion

Let V=(v_0,...,v_3) consist of

    (1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1).

There are sixteen labels, the four cores followed by (i,j), i!=j, in
lexicographic order. Keep the reference source and target sites

    a_i=v_i/2,              b_i=(63/64)v_i/2,
    a_ij=(v_j-2v_i)/2,      b_ij=(63/64)(v_j+2v_i)/2.       (1)

For each label l, let mu_l and nu_l be arbitrary probability laws in
the coordinate boxes of radius 1/2048 about a_l and b_l, respectively.
They can be diffuse. Let

    p_l >= 15/256,     sum_l p_l=1,
    mu=sum_l p_l mu_l,       nu=sum_l p_l nu_l.             (2)

No coupling between these two laws is required. At variance one put
gamma(z)=(2pi)^(-3/2)exp(-|z|^2/2), C=(2pi)^(-3/2), and

    A_p(u)=integral(mu*gamma-Cu)_+-integral(nu*gamma-Cu)_+.

**Theorem.** Every pair of laws in (2) satisfies

    A_p(u)<=0                         for every u>=0,
    A_p(u)<=-Cu/2                     for 0<u<=1/512,
    A_p(u)<-1/256                     for 1/512<=u<=9/32.   (3)

In particular this applies to any contraction sending a source component
into its corresponding target box. With one point per component, the
existing geometry proves every such labelled pair is a strict contraction,
with squared-distance loss at least 1/32. That is not a statement about
arbitrary pairs within a diffuse component.

The weight region is a full fifteen-dimensional simplex. Its vertices
have mass 31/256 at one label and 15/256 at all the others. The existing
90-coordinate anchored cell thus gains fifteen independent weight
parameters. In the unchanged rational frontier R^c_2, the weight
denominator is 7104. Requiring at least417 units per label leaves432 free
units, so the cell contains

    binom(447,15)=3427492026504451783224489079

labelled lattice priors. This is a count of the finite grid, not an
enumeration used by the proof. Coordinate denominator2048, pair-loss
floor, radius bounds, and the inherited paired-rank-six member are unchanged.
The theorem is at one variance; it gives no new Kneser--Poulsen consequence.

## 2. A finite supporting-plane certificate for weights

For arbitrary integrable nonnegative component densities f_i,g_i, define

    F_u(p)=integral(sum_i p_i f_i-Cu)_+,
    G_u(p)=integral(sum_i p_i g_i-Cu)_+.

Both functions are convex in p; their difference need not be. Let p^0 be
a reference prior and p^i be the vertices of a prior polytope. Suppose
q^i=2p^0-p^i is also a probability vector. Then

    F_u(p)-G_u(p)
       <= max_i [F_u(p^i)+G_u(q^i)-2G_u(p^0)]             (4)

for every p in their convex hull.

To prove this, choose the selector psi=1_{sum p^0_i g_i>Cu} and put
ell_i=integral psi g_i. The defining variational formula for a hinge gives
the common supporting inequality

    G_u(p)>=G_u(p^0)+ell dot(p-p^0).

At q^i, it implies ell dot(p^i-p^0)>=G_u(p^0)-G_u(q^i).
Write p=sum_i lambda_i p^i, lambda_i>=0, sum_i lambda_i=1. Combine that
same linear functional with convexity of F_u to obtain an upper bound
by the lambda-average of the expressions on the right of (4). This
proves (4), without a differentiability or strict-level assumption.

For (2), p^0 is the uniform prior. The reflected priors q^i have weight
1/256 at label i and17/256 elsewhere, so all their weights are positive.
The group of coordinate permutations and even sign changes acts
transitively on the four cores and on the twelve flaps. Thus only TWO
different upper curves in (4) need certification. Their target densities
are genuine positive Gaussian mixtures, so the accepted direct hinge
quadrature applies to every term. No convexity of F_u-G_u is assumed.

## 3. Exact middle certificate

First use the point masses at the reference sites. For each vertex type
certify F_u(p^i)+G_u(q^i)-2G_u(p^0) on [1/512,9/32]. The spatial mesh is
h=1/16, half-grid M=120, with 48-bit outward Gaussian bounds. The cube
contains 241^3=13,997,521 sites and has tail distance6 from every center.

The existing 24-element spatial group reduces this to597,861 orbits.
For an asymmetric weighted vertex, one must not treat its density as
group invariant. Instead average over its LABEL orbit: four labels for
a core vertex and twelve for a flap vertex. The group permutes these
labels transitively. Hence averaging their integrands at every spatial
orbit representative gives exactly the grid sum for one fixed label.
The histogram counts are multiplied by the label-orbit size and divided
by that size only in the final integral. This retains all asymmetric
values rather than assigning a single value to an entire spatial orbit.

At a grid point, let x_l^+ be upper bounds for the source kernels and
y_l^-,y_l^+ lower/upper bounds for the target kernels. All are normalized
by C. The three density bounds used are

    source upper:  (15 sum_l x_l^+ +16 x_i^+)/256,
    backward target upper: (17 sum_l y_l^+ -16 y_i^+)/256,
    reference target lower: sum_l y_l^-/16.               (5)

The second expression has coefficient1 at i and17 elsewhere: it is a
positive weighted sum, despite its compact notation. Fixed-point rounding
is outward. The signed histogram combines the first two hinges minus
twice the third. Its polygon is affine between its density knots, so an
exact sweep, including both endpoints, certifies the whole interval.

Put G_h=1+h^2/8. One endpoint hinge has infinite-grid error at most
h^2(1+G_h+G_h^2)/8. The omitted grid mass of one mixture is at most
tau=3G_h^2 exp(-18)/6. The absolute coefficient sum in (4) is4;
the positive tail coefficients sum to2. Therefore a valid upper error is

    h^2(1+G_h+G_h^2)/2 +2tau.                            (6)

This is twice the existing pair-hinge error, with no extra threshold or
atom-count factor. The proof of the nonsmooth quadrature remains the
accepted [direct oracle](../gaussian_prior_localization/DIRECT_HINGE.md).

Every component law in its coordinate box lies within Euclidean distance
e=1/1024 of its reference site. Gaussian translation changes total
variation by at most e/sqrt(2pi)<e/2. Mixture convexity gives this bound
for each actual endpoint at every prior. Their adverse hinge therefore
differs from the reference adverse hinge by at most e. This transfer is
applied AFTER (4), so its cost is e, not four endpoint errors.

After (6) and that diffuse transfer, the two exact adverse upper bounds are

    core: -53510281893184444954644838093907
           /10384593717069655257060992658440192,
    flap: -181902418563933294173257269525927
           /41538374868278621028243970633760768.           (7)

Both are strictly below -1/256. The maximizing thresholds are1/512 and
9/32 respectively. There are543,614 and1,482,484 swept knots. The compact
expected record includes the histogram digest; no full grid is distributed.

## 4. The upper endpoint

For the normalized Gaussian kernel exp(-|z|^2/2), the Hessian operator
norm is at most1. Its tangential eigenvalues are -exp(-r^2/2), and the
radial eigenvalue is (r^2-1)exp(-r^2/2); its positive maximum is
2exp(-3/2)<1. Positive probability mixtures obey the same bound.

At a global maximum the gradient vanishes. A nearest grid point is within
sqrt(3)h/2, so a reference source vertex has peak at most its grid maximum
plus3h^2/8. Outside the grid cube its density is at most exp(-18), already
below the recorded grid upper bound. Diffuse displacement adds at most
(61/100)e, using sup |grad exp(-|z|^2/2)|=exp(-1/2)<61/100.
The exact final upper peaks are

    core: 1955590489351021/7036874417766400,
    flap: 829551698174373/3518437208883200,

both below9/32. Convexity in the prior bounds every source mixture by
the largest vertex peak. Thus its hinge vanishes on [9/32,infinity).

## 5. Uniform low-threshold volume bounds

Write F=(mu*gamma)/C and G=(nu*gamma)/C. Equal mass and layer cake give

    A_p(u)=-C integral_0^u [|{F>v}|-|{G>v}|]dv.           (8)

We prove the bracketed volume difference exceeds1/2 at
v=exp(-S^2/2), for every S>=7/2. Both densities exceed that level
throughout B(0,9/4): each contains at least15/16 of the uniform
sixteen-component mixture, whose Jensen exponent is bounded by
9249793/2097152. The added logarithmic cost is less than1/15, and their
sum is below49/8. Beyond9/4 every component decreases strictly on a ray.
Consequently both superlevel sets have one outer radial boundary.

Use the two triangular angular charts and their24 symmetry images from
the accepted coordinate-cell proof. Its outward dot/norm enclosures
already include the full component-box displacement e. On a chart piece
let E_l^X(r) and E_l^Y(r) denote the resulting lower/upper exponents.
The weight simplex gives the uniform envelopes

    F(r theta) >= (15/256) sum_l exp(E_l^X(r)),
    G(r theta) <= [15 sum_l exp(E_l^Y(r))
                              +16 max_l exp(E_l^Y(r))]/256. (9)

The source bound discards the nonnegative residual mass. The target bound
maximizes that residual over all labels. Thus (9) holds for every prior
and every diffuse component law in (2), with no symmetry requirement.

At each S the code proposes dyadic radii r_X^-,r_Y^+ and verifies (9)
strictly above/below exp(-S^2/2), using exact integer exponential bounds.
Proposal logarithms and floating arithmetic never certify a radius.
Monotonicity in S bounds each entire interval [S_a,S_b] by the source
radius at S_a and the target radius at S_b. Cube their difference and
use the lower surface Jacobian for positive differences and the upper
one for negative differences. All angular pieces and thresholds are
covered by the following finite cover:

| S range | step | angular subdivision | pieces | windows | checked radii |
|---|---:|---:|---:|---:|---:|
| [7/2,4] | 1/32 | 48 | 2352 | 16 | 79,968 |
| [4,6] | 1/16 | 32 | 1056 | 32 | 69,696 |
| [6,12] | 1/16 | 24 | 600 | 96 | 116,400 |
| [12,64] | 1/8 | 12 | 156 | 416 | 130,104 |

Every certified volume bound exceeds1/2. The exact minima and stream
digests are in EXPECTED.json. The coarser equal-prior cover does not
certify these weighted envelopes; the new cover is checked in full.

## 6. The remaining infinite tail

The reference geometry, unaffected by the prior, supplies functions
h_X(theta)=max_l theta.a_l-e and h_Y(theta)=max_l theta.b_l+e.
They obey h_X>=h_Y>=0 and a certified normalized mean gap greater than1/4.
These are uniform projection envelopes, not an assumption that a diffuse
component puts positive mass at its extremal point. Every point in the
maximizing source COMPONENT has projection at least h_X.

Each source component has mass at least15/256. Since
log(256/15)<3, exactly the same far-tail constants as in the coordinate
proof apply: A=269/25 and B=277/200. One component gives the lower source
envelope, while total target mass one gives the upper envelope. Thus

    rho_X >= S+h_X-A/S,       rho_Y <= S+h_Y+B/S,
    volume difference >=4pi S^2 [delta-E(S)],
    delta>1/4,
    E(S)=A/S (1+(9/4)/S)^2
             +B/S (1+(27/16)/S+B/S^2)^2.                 (10)

The endpoint estimate in the accepted proof uses only these norm,
projection and mass bounds, so it also covers the present diffuse laws.
E decreases, and E(64)=1743464522020333/8589934592000000<21/100.
Hence (10)>1/2 for every S>=64. The finite cover and (10) prove the
volume assertion. Since exp(-49/8)>1/512, (8) signs all thresholds down
to zero and proves the second inequality of (3). Together with (7) and
the source peak this establishes (3) with no missing interval.

## 7. Reproduction and trust

Run from this directory with standard-library CPython3.11 or later:

    python3 -B verify.py
    python3 -B -O verify.py
    sha256sum -c SHA256SUMS

Expected marker: EXTENDED_TARGET_PRIOR_CELL_PASS. INPUTS.json pins the
accepted scalar/orbit/geometry source and its reviews. The new checker
compares the complete signed histogram against a fixed-label unquotiented
grid on three small grids, checks supporting-plane and exact polygon
controls, rejects a false convexity shortcut, and rejects altered radial
endpoints. The full new middle and radial obligations are reproduced;
neither the equal-prior certificate nor floating probes supply their signs.

Convexity, the label-average identity, Gaussian quadrature and perturbation,
the Hessian bound, star shape, angular coverage, and the far-tail argument
remain written mathematics. This is not formalization or independent
acceptance of the extension. The underlying geometry and equal-prior cell
already have two independent reviews, which do not automatically review
the new prior and diffuse quantifiers.

The full Aishwarya--Li question and unrestricted middle-sign obligation
remain open; the accepted global defect cap 7/50 is unchanged. The progress is a
finite supporting-plane certificate that handles a changing target prior,
and its completed full-threshold application on a105-parameter rational
cell with arbitrary diffuse components.
