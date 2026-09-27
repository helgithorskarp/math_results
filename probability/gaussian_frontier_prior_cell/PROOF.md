# All thresholds on a full prior simplex and its measure cell

Complete author proof with an exact finite certificate, 27 September 2026.
Independent review is pending. The full dimension-three Gaussian-majorisation
problem and the unrestricted bound `D<=7/50` remain unchanged.

This extends R2's [coordinate-cell certificate](../gaussian_frontier_middle_cell/PROOF.md)
along the measure and weight variables. That result already signs an entire
coordinate box at one fixed prior. Here a six-dimensional simplex of priors
is certified, along with arbitrary diffuse laws in the same source boxes.
The new finite obligation reduces to two vertex types; their entire middle
intervals are checked. This is a fixed-variance result, not an all-variance
theorem or a new Kneser--Poulsen consequence.

## 1. The measure cell and the rational parameter cell

Let `gamma` be the probability Gaussian with covariance `I_3` and
`C=(2pi)^(-3/2)`. Put

    a=(0,e1,-e1,e2,-e2,e3,-e3),
    Q_i=a_i+[-1/256,1/256]^3,       Q_Y=[-1/16,1/16]^3,
    alpha=21/156=7/52,              beta=30/156=5/26.

The seven closed source boxes are disjoint. Let `mu` be any Borel probability
supported on their union, satisfying

    p_i=mu(Q_i)>=alpha,             i=1,...,6.                 (1)

There is no positive lower bound on `p_0`. Let `nu` be any Borel probability
supported on `Q_Y`. In particular, `nu` may be `T#mu` for a contraction whose
image lies in this box. The comparison below does not require a coupling
between these two laws.

Write `f=mu*gamma`, `g=nu*gamma`, `H_f(t)=integral(f-t)_+`, and use the
adverse sign convention

    A(u)=H_f(Cu)-H_g(Cu).

**Theorem.** Every such pair of laws satisfies

    A(u)<=0                      for all u>=0,
    A(u)<-1/256                   for 1/256<=u<=7/10.           (2)

The laws need not be atomic. Thus (2) is a quantitative measure-cell result,
not an inference from an isolated configuration or a sampled weight list.

For the finite rational frontier, choose one source site `x_i` in each `Q_i`
and seven arbitrary target sites `y_i` in `Q_Y`, all with the same weights
`p` satisfying (1). The coordinate choices vary independently. With

    epsilon=1/128,         r_Y=7/64,

we have `|x_i-a_i|<epsilon`, `|y_i|<r_Y`. Every distinct labelled source pair
has distance at least `1-2epsilon`; every target pair has squared distance
at most `3/64`. Therefore the squared pair loss is at least

    (1-2epsilon)^2-3/64=3777/4096>1/256.                      (3)

This statement concerns one site per source box; it is not a pair-separation
claim for arbitrary points within a diffuse component.

For coordinates in `(1/256)Z^3`, anchor separately at `x_0` and `y_0`.
Translations preserve both hinge profiles and all pair distances. The
anchored radii are at most `1+2epsilon<3` and `2r_Y<3`. Together with (3),
seven labels `<=A_1=39`, and weights of denominator `W_1=156`, these are
exactly members of the existing [paired-cubature family](../gaussian_prior_localization/CUBATURE_FRONTIER.md)
`R^c_1`, with `L_1=256` and no changed constraints.

For denominator 156, put `n_0=156p_0` and `n_i=156p_i-21` for `i>0`.
These are seven nonnegative integers of total 30, so the cell contains

    binom(36,6)=1,947,792                                       (4)

weight vectors. This counts labelled weight vectors, not laws modulo
isometries, collisions or relabellings. No enumeration of them is needed.
The continuous prior region has dimension six. The anchor-zero slice has
36 independent coordinate parameters and six independent weight parameters.

R2's original prior `(24,22,22,22,22,22,22)/156` is an interior point of this
simplex. Its explicit injective paired-rank-six member is retained and
checked in the compact record. It is inherited evidence of nondegeneracy,
not a new construction. Zero central mass and target collisions are allowed.

## 2. The useful extremal reduction is on the source prior

Let `f_p=sum_i p_i gamma(.-a_i)` and let `g_*=gamma`. Because `6alpha+beta=1`,
every admissible prior has the unique form

    p_0=beta lambda_0,
    p_i=alpha+beta lambda_i  (i>0),
    lambda_i>=0, sum_i lambda_i=1.                             (5)

Its seven vertices have reference source densities

    f^(j)=alpha sum_(i=1)^6 gamma(.-a_i)+beta gamma(.-a_j),
                       j=0,...,6.                             (6)

Convexity of the scalar hinge, applied pointwise and integrated, gives

    H_(f_p)(Cu)-H_(g_*)(Cu)
       <=sum_j lambda_j[H_(f^(j))(Cu)-H_(g_*)(Cu)]
       <=max_j [H_(f^(j))(Cu)-H_(g_*)(Cu)].                    (7)

The point-target reference in (7) is independent of the prior. We do not
assume that a difference of two weight-dependent convex hinges is convex.
The actual target law is treated by a uniform error below.

Signed coordinate permutations identify the six outer vertices for their
integrated hinges. Thus the complete prior simplex requires only two
reference calculations: the central vertex with masses
`(30,21,21,21,21,21,21)/156`, and one outer vertex with masses
`(0,51,21,21,21,21,21)/156`.

For equal-mass densities, each hinge is 1-Lipschitz in total variation:

    |H_q(t)-H_r(t)|<=TV(q,r)=||q-r||_1/2.                      (8)

Couple every point of `Q_i` to `a_i`. The usual translated-Gaussian bound
`TV(gamma(.-v),gamma)<=|v|/sqrt(2pi)<|v|/2` gives, even for diffuse `mu`,

    TV(f,f_p)<=epsilon/2.                                     (9)

For the target let `m=E Y`. Translation leaves its hinge unchanged.
Taylor's formula around the mean, cancellation of `E(Y-m)` and
`||partial_ee gamma||_1=4phi(1)<1` yield

    TV(g(.+m),gamma)<=E|Y-m|^2/4<=3/1024.                     (10)

For clarity, the Taylor remainder for a centered shift `v` is
`integral_0^1(1-t) v^T D^2 gamma(z-tv) v dt`. Its integrated absolute value
is at most `|v|^2/2`, and total variation contributes another factor one half.
The variance is at most `E|Y|^2<=3/256`. Bounded supports justify integration
of this estimate against any Borel law. These are the same transport/Taylor
bounds used by R2's coordinate cell, now applied uniformly in the prior.

Combining (7)--(10), at every threshold,

    A(u)<=max_j [H_(f^(j))(Cu)-H_gamma(Cu)]+eta,
    eta=epsilon/2+3/1024=7/1024.                              (11)

This is the measure-side reduction that makes a finite calculation cover
all the weights and all the diffuse components simultaneously.

## 3. A common signed low interval

Put `F=f/C`, `G=g/C` and `r=|z|`. The six outer mass floors give

    f_p(z)/C >=2alpha exp(-r^2/2-1/2) sum_(k=1)^3 cosh(z_k)
              >=3alpha exp(-r^2/2-1/2+r/sqrt(3)).              (12)

The second inequality uses convexity of `t -> cosh(sqrt(t))`, then
`cosh(v)>=exp(v)/2`. Displacing any latent source by at most epsilon changes
its normalized kernel by a factor at least
`exp[-epsilon(r+1)-epsilon^2/2]`. Integration over arbitrary components gives

    F(z)>=3alpha exp[-r^2/2+(4/7-epsilon)r
                                  -1/2-epsilon-epsilon^2/2], (13)

where `1/sqrt(3)>4/7` is used in a safe direction. For `r>=r_Y`, the target
support bound gives `G(z)<=exp[-(r-r_Y)^2/2]`.

Take `rho=25/8` and `tau=1/256`. The logarithmic slope of the lower ratio
in (13) to this target upper envelope is

    4/7-epsilon-r_Y=407/896>0.

At `r=rho` its exponent is `q=210485/229376`. Exact enclosures certify

    exp(-q) <=56218989677313/140737488355328 <21/52=3alpha.    (14)

It follows that `F(z)>G(z)` for every `r>=rho`.

Inside this ball the quadratic exponent in (13) is concave in `r`, so its
minimum on `[0,rho]` occurs at an endpoint. This observation replaces the
fixed-prior mean estimate, which would not be uniform on the new simplex.
The scalar enclosures give

    F(z)>=78418785823455/7318349394477056 > tau,
    G(z)>=752996687755/140737488355328 > tau,    r<=rho.        (15)

For the second inequality use `G(z)>=exp[-(rho+r_Y)^2/2]`. For the first,
evaluate (13) at zero and rho and take the smaller lower bound.

For `0<u<=tau`, both clipped densities `min(F,u)` and `min(G,u)` equal u
inside the ball, while `min(F,u)>=min(G,u)` outside. Equal total masses give

    A(u)=C integral[min(G,u)-min(F,u)]<=0.                    (16)

The clipped integrals are finite. At u=0 both hinges equal one. Thus the low
interval is actually signed; it is not covered by an unsigned error bound.

## 4. A common signed upper interval

The uniform six-site reference mixture has normalized peak at most
`exp(-1/2)`, since `cosh(t)<=exp(t^2/2)`. The residual mass beta in (6)
has normalized peak at most beta, independently of its location. Therefore
every prior in (5) has reference peak at most `6alpha exp(-1/2)+beta`.
The normalized Gaussian gradient has norm at most `1/sqrt(e)<1`, so the
source displacement contributes at most epsilon, also for diffuse laws.
Using the elementary `exp(-1/2)<61/100`,

    ||F||_infinity<=6alpha(61/100)+beta+epsilon
                   =2217/3200 <7/10=b.                     (17)

Hence `H_f(Cu)=0` for `u>=b`, and `A(u)<=0` on that whole interval.

## 5. Two exact middle certificates

Only `[tau,b]=[1/256,7/10]` remains. The computation uses the accepted
[absolute hinge quadrature](../gaussian_prior_localization/DIRECT_HINGE.md)
on the two reference sources and a point target. It takes

    h=1/16, M=112, R=1, T=Mh-R=6, Q=2^48.

The uniform reference error is

    E_quad=(h^2/4)(1+G_h+G_h^2),  G_h=1+h^2/8,
    E_tail=(3G_h^2/T) exp(-T^2/2).                            (18)

Here R bounds the reference supports. The actual source perturbations have
already been charged in (11). No inappropriate smooth-function quadrature
claim is made for a nonsmooth hinge: the needed theorem was independently
reviewed in the original oracle packet.

The grid has `225^3=11,390,625` sites per vertex. For a representative
`0<=i<=j<=k<=112`, its signed-permutation orbit has size

    m=2^(number of nonzero coordinates) 3!/product_v m_v!.

The central reference source is invariant on that orbit. The outer-heavy
reference is not. To integrate it correctly, split the orbit according to
its first coordinate. If a value v occurs `c_v` times in the multiset
`{i,-i,j,-j,k,-k}`, precisely `m c_v/6` orbit points have first coordinate v.
Every count is integral, including repeated coordinates and zero.

The symmetric part of (6) is constant on an orbit. Its extra outer kernel
is `gamma(z-e1)`, so only this distinguished coordinate is additionally
needed. This splitting covers the entire asymmetric reference source;
applying the central symmetry quotient without the split would be invalid.
All 246,905 orbit representatives are processed.

Positive products of pinned exponential enclosures yield upper source
densities and lower point-target densities with denominator Q. Their upper
adverse lattice profile is affine between successive density-value knots.
The exact sweep includes every knot and both rational window endpoints;
in particular `7Q/10` is retained as a rational, not rounded to a grid value.
Negative sums are multiplied by the lower positive enclosure for C to get
an upper bound. There is no sampled-threshold or floating-sign premise.

After quadrature, tail and the perturbation error eta, the exact results are:

| Vertex type | Upper adverse gap on the entire middle interval |
| --- | --- |
| Central residual | `-381118184370125770791542443287977 / 83076749736557242056487941267521536` |
| Outer residual, all six choices | `-265378122392705868839843704354167 / 41538374868278621028243970633760768` |

Both are less than `-1/256`. Equation (11) proves this same uniform middle
margin on the entire prior simplex and measure cell. Equations (16),(17)
join it to both infinite endpoint ranges without a gap, proving (2).

## 6. Validation and limits

Run in this directory with standard-library CPython 3.11 or later:

    python3 -B verify.py
    python3 -B -O verify.py
    sha256sum -c SHA256SUMS

Expected status: `GAP_FREE_PRIOR_SIMPLEX_CELL_PASS`. The compact record pins
the cell, five source dependencies, all scalar bounds, both complete middle
sweeps, the orbit stream and the inherited rank-six member. No large grid
dump, solver, external numerical library or hidden dataset is needed.

Every histogram entry from both vertex types is compared against the
general unquotiented density routine on three small grids (1,197 sites per
type). Definition-level knot checks include rational boundaries and negative
maxima. Exact controls also check barycentric reconstruction, hinge convexity,
the stars-and-bars count, malformed inputs and corrupted expected records.
The author replay takes about thirteen seconds and 160 MB; a coarser grid was
insufficient because its error exceeded the available margin, so the final
calculation uses the stated finer step. Optimization changes the evaluation
cost, not the exhaustive grid/threshold or prior coverage.

The universal measure-cell reduction and Gaussian estimates remain written
mathematics. The executable certifies their exact constants and the finite
middle calculation, subject to inspection of the source and Python integer
semantics. It is not independent review or formalization. Convexity, total
variation, Taylor expansion, group multiplicities and knot sweeps are standard;
no historical priority claim is made for them.

This certificate enlarges one actual positive part of the existing rational
frontier. It does not sign the rest of `R^c_1`, any whole later frontier,
all later beta rows, or all variances for a fixed measure
and map. The full conjecture and the global `D<=7/50` bound remain unchanged.
