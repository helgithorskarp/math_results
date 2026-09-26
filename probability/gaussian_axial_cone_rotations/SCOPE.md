# Consolidated scope of the axial-cone theorem

Author consolidation, 26 September 2026. Theorem 1 in [PROOF.md](PROOF.md)
is unchanged. This document makes its scope and relation to the team's
other results explicit. Independent mathematical review remains pending;
the full dimension-three question remains open.

## Exact statement and breadth

Work in ordinary Euclidean three-space with one common axis and height-one
transverse sections. Let $P,Q\subset\mathbb C$ be compact, convex,
centrally symmetric bodies with zero in their interiors, and define

$$
C(P)=\{(zu,z):z\ge0,\ u\in P\},\qquad
W=\operatorname{conv}\{\overline u v:u\in P,v\in Q\}.
$$

If $\operatorname{per}W\le4$, the **original unscaled map** fixing $C(P)$
and sending $-b$ to $b$ for $b\in C(Q)$ admits a contracting motion in
$\mathbb R^4$. The same motion works simultaneously for the entire domain.

| Object | Quantifiers and conclusion |
| --- | --- |
| Gaussian law | Every Borel probability law with bounded support in the domain; any atom count and weights, including mass at the origin, and arbitrary nonatomic parts. No symmetry of the law is required. |
| Variance and threshold | Every $s>0$ and $h>0$: $\int(\mu*\gamma_{3,s}-h)_+\le\int(T_\#\mu*\gamma_{3,s}-h)_+$. Thus all convex internal energies for which the comparisons are defined. |
| Finite balls | Any finite labeled centers in the domain and any individual radii $r_i\ge0$, retained at both endpoints. Union volume does not increase; intersection volume does not decrease. |
| Compact neighborhoods | Every compact $K$ in the domain and every $r>0$: $\lvert T(K)+rB_3\rvert\le\lvert K+rB_3\rvert$. |
| Coordinates | Common translations, orthogonal changes and uniform scaling preserve the statement. General affine coordinate changes are not covered. The Gaussian covariance is $sI_3$. |

The domain permits arbitrary heights and transverse distributions. Probability
support is bounded, but the motion is not restricted to a finite template.
The planar bodies may be smooth, polygonal, or nonsmooth. The rectangular
example in PROOF Section 2 passes the perimeter criterion although its
smallest centered circular envelopes fail the circular bound. This illustrates
why the theorem uses the shapes of the sections, not just cone angles.

Equality $\operatorname{per}W=4$ is included. No strict Gaussian or volume
inequality is asserted. For example, a law confined to one rigid cluster
has equality. Degenerate circular sections of zero slope have the separate
path described in PROOF Section 2; they are outside the body hypothesis.

## Correctness boundary and proof dependencies

| Obligation | Proof and boundary |
| --- | --- |
| Geometric cost | The cross-pair cost $k(\theta)=\max u\cdot JR_\theta v$ is positive and continuous. Cauchy's width formula gives $\int_0^\pi k=\operatorname{per}W/2$. PROOF Section 1. |
| Motion | A half-turn in the transverse plane is paid for by an axial coefficient increasing from $-1$ to $1$. Both clusters remain rigid and all cross inner products increase. This proves contraction for every pair and time. |
| Sharpness | The perimeter bound is necessary only for the specified axial form with absolutely continuous angle and axial coefficient, on the full two cones. It is not necessary for arbitrary motions or either endpoint inequality. |
| Full Gaussian comparison | Pad the motion from four to five dimensions. Aishwarya--Li Theorem 1.4(i)(a) gives order of density values sampled from the densities. The two-dimensional Gaussian sampling identity in PROOF equation (17) gives every hinge in three dimensions. |
| Arbitrary radii | For finite centers, smaller polygonal sections preserve the perimeter bound and yield a piecewise analytic motion. Reverse and pad it, then apply Bezdek--Connelly Theorem 1 in dimension $3+2$. PROOF Section 3. |
| Computation | Exact rational and polynomial audits support the written proofs. They do not prove a universal motion or Gaussian inequality by finite sampling. No independent review or formalization is claimed. |

The analytic bridge uses **density-value stochastic order**, not cancellation
of a generic product-majorisation inequality. It neither infers full
majorisation from finitely many moments nor assumes that all Renyi
comparisons suffice. The motion also gives a one-auxiliary-coordinate
Gamma comparison, but the full hinge claim uses the separate, valid
two-coordinate identity. The primary transfer theorems are credited in
[SOURCES.md](SOURCES.md).

## The Kneser--Poulsen advance being claimed

For circular cones $C_p=\{(u,z):z\ge0,|u|\le pz\}$, the criterion is
$pq\le2/\pi$. The claimed geometric advance is the explicit motion and
the resulting arbitrary-radius union and intersection theorem for these
maps, and more generally for $\operatorname{per}W\le4$.

An intermediate simplicial separator between the two full circular cones
exists exactly when $pq\le1/2$. Hence the interval
$1/2<pq\le2/\pi$ extends beyond that criterion, uniformly in the number
of centers, their locations and their ball radii. This is not a
fixed-configuration asymptotic result. Bezdek--Connelly already supply the
volume transfer theorem; the new input is a concrete broad class satisfying
its motion hypothesis. No new general transfer theorem or historical
priority over all possible earlier constructions is claimed.

The existing rational 25-point witness uses $p=3/4,q=4/5$, twelve directions
in each cluster, and the origin. Its 144 cross-pairs strictly contract;
156 pairs preserve distance. Both endpoints have 25 distinct centers.
PROOF Sections 4--5 establish the following actual exclusions:

- There is no intermediate simplicial cone for these finite clouds.
- Paired affine rank is six; the two-dimensional displacement criterion
  also fails. The origin is essential to the rank-six assertion.
- No continuous contracting motion exists in three dimensions. The
  constructed four-dimensional motion therefore has minimal ambient
  dimension for these prescribed labels.
- Strong coordinatewise contraction fails even after independent rigid
  alignments. The later scalar-defect inequality fails as well.

These prove added coverage relative to the named sufficient criteria.
They do not exclude every composition, rematching, or other proof method.
In particular, rank six is not an obstruction to a nonlinear continuous
motion in five dimensions: this example has one already in four.

## Relation to the current Team B classes

| Result | Relation to this theorem |
| --- | --- |
| [Paired rank at most five](../gaussian_majorisation_rank_abel/PROOF.md) | The 25-point witness has rank six. The shared two-coordinate Gaussian identity is reproduced in this proof. |
| [Simplicial cone reflections](../gaussian_simplicial_cone_reflections/PROOF.md) | Neither stated geometric criterion contains the other. Circular cones with $1/2<pq\le2/\pi$ escape every simplicial separator. Conversely, the standard self-dual orthant cannot meet this axial perimeter bound under any common axis; PROOF Section 4.1 proves $\operatorname{per}W\ge8$ for every centrally symmetric envelope. This is not an obstruction to other motions for the orthant. |
| [Scalar-defect budget](../gaussian_majorisation_scalar_defect/PROOF.md) | Norm preservation at the origin and spanning of both clusters exclude its unit-vector criterion on the 25-point witness. PROOF Section 5.1 applies that source's existing obstruction; the new matrix audit records it exactly. |
| [Fixed-core rematching](../gaussian_majorisation_fixed_core/PROOF.md) | That construction fixes a tetrahedral core and rematches ray labels subject to output-law or radius-incidence conditions. Here the prescribed labels move and all weights and individual radii are allowed. No general containment claim is made. |
| [Common-target mixtures](../gaussian_majorisation_common_target/PROOF.md) | This measure-dependent method needs the same output law from every component. On our injective fixture, each deterministic component must have the original source law; with distinct weights its matching is forced too. PROOF Section 5.1. Repeated weights can permit rematchings. No conclusion about stochastic couplings or post-convolution decompositions follows. |
| [Eventual majorisation](../gaussian_majorisation_eventual_endpoint/PROOF.md) and its [asymmetric nine-atom realization](../gaussian_asymmetric_eventual_majorisation/PROOF.md) | Those results require a spherical comparison and a lower variance bound. The new orbit theorem below removes that restriction for the stated square-cone weight family. The axial theorem covers every variance without a spherical premise and supplies ball inequalities at every radius. |
| [Square-cone orbit comparison](../gaussian_majorisation_square_cone_orbits/PROOF.md) | The newest result proves every hinge at every variance on the asymmetric nine-point L1 weight ball of radius $1/552$, with a bounded radial-law extension in explicit weight cones. It compares smoothed density values using an exact finite order certificate, despite the prescribed matching's five-dimensional motion obstruction. It has weight restrictions and claims no new Kneser--Poulsen case. Neither general geometric class is asserted to contain the other. |
| [Damped cone reflections](../gaussian_damped_cone_reflections/PROOF.md) | The later product-cost motion criterion contains the present axial path at damping factor one. Its wider positive class uses damping less than one and changes both endpoints. It does not enlarge the undamped perimeter range proved here. |
| [Global coupling and moment criterion](../gaussian_majorisation_global_criterion/PROOF.md) | This identifies full majorisation with zero failure in a coupling of five-dimensional endpoint density values, equivalently a complete moment hierarchy. The axial motion constructs such a coupling for every law and variance in its domain. The equivalence alone adds no geometric class; finitely many nonnegative tests do not prove zero failure. |
| [Atomic bridge](../gaussian_atomic_bridge_obstruction/PROOF.md) and [tail-deficit obstruction](../gaussian_tail_deficit_obstruction/PROOF.md) | These close particular methods on other configurations or proposed uniform estimates. They are not negative Gaussian hinges and do not contradict the axial theorem. |

For circular cones the endpoint map is a contraction all the way to
$pq\le1$, because the smallest cross inner product is $z_a z_b(1-pq)$.
Thus $2/\pi<pq\le1$ is outside our axial certificate despite endpoint
contraction. This document supplies no positive or negative conclusion for
the full circular-cone map on all bounded laws in that remaining interval.
The damped paper's obstruction to five-dimensional
motions on full nonsimplicial exact-dual cones applies at $pq=1$; it does
not settle the intervening interval or refute majorisation at the boundary.

## Reproduction and review status

Run the commands in [README.md](README.md). The original `verify.py` and
`EXPECTED.json` retain their exact bytes and output hash from source commit
`984e1edaaf7f02bf4572c80754edff1e296fdd19`. The additional
[scope_audit.py](scope_audit.py) checks the scalar matrix, an identity-map
control, and the explicit distinct weights. The all-axis orthant exclusion
is proved algebraically in PROOF Section 4.1, not inferred from a grid.

The author checked the latest relevant reports, source revisions, repository
commits and committed graph before this consolidation. Reviews of other
Team B packets do not count as review of this result. The unchanged main
theorem and new comparison lemmas remain subject to independent review.
