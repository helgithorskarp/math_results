# Sources, dependencies, and scope

The sole problem source is the bounded-input dimension-three full
Gaussian-convolution majorisation question in Aishwarya--Li. Primary sources,
the committed graph, and bounded latest reports and source changes from
Team B were checked on 26 September 2026 before publication.

## Primary sources

* Gautam Aishwarya and Dongbin Li,
  [Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
  Conjecture, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2).
  Version 2, revised 13 September 2026, remains the latest observed source.
  Theorem 1.4(i)(a) supplies density-value stochastic order for continuous
  contractions. Our equation (18) uses two auxiliary Gaussian coordinates
  to recover all hinge thresholds in R3. Theorem 1.8(i) gives the compact
  equal-radius consequence. Neither transfer theorem is new here.
* Karoly Bezdek and Robert Connelly,
  [Pushing disks apart—the Kneser--Poulsen conjecture in the plane,
  arXiv:math/0108098](https://arxiv.org/pdf/math/0108098).
  Theorem 1 supplies both arbitrary-radius volume inequalities from a
  piecewise-smooth motion in R^(n+2). The general leapfrog supplies an
  R6 motion for every R3 contraction. Our new input is a class of explicit
  R4 motions and a precisely qualified variational optimum.
* Raphael Loewy and Hans Schneider,
  [Indecomposable Cones, Linear Algebra and its Applications 11 (1975),
  235--245](https://people.math.wisc.edu/hans/loew_s75.pdf).
  Theorem 3.3 identifies extremality of the identity among cone-preserving
  operators with indecomposability. This is the classical ingredient behind
  the undamped dual-cone obstruction. Section 4 of our proof gives the
  elementary dimension-three specialization and its Gram-rank consequence;
  it does not claim novelty for identity extremality.
* Karoly Bezdek and Marton Naszodi,
  [The Kneser--Poulsen conjecture for special contractions,
  arXiv:1701.05074](https://arxiv.org/abs/1701.05074).
  Used to audit existing special-contraction classes. No assertion that
  all compositions of previously known methods have been excluded is made.

The Euclidean Kirszbraun extension theorem is only used to translate the
specified-domain maps to the global formulation of the source question.
The motion directly proves its own contraction property. The shortest-path
bound is proved by the unit-gradient calibration (13), not imported from
a geodesic algorithm. The rational constants come from displayed elementary
Taylor and positive-integral bounds, not numerical sign tests.

## Durable team dependencies

* [Axial cone rotations](../gaussian_axial_cone_rotations/PROOF.md), this lane,
  source `984e1edaaf7f02bf4572c80754edff1e296fdd19`, graph
  `bafkreiao6gmik3rvanspc76z6zukxlkk447ylprpkitnt6ht6tmdayl2zy`.
  The present product-cost principle recovers its perimeter path at
  lambda=1 and adds transverse shrink. Its circular condition, preceded
  by a uniform transverse squeeze, gives pi pq lambda^2<=2. Our new
  criterion strictly improves that specified composition for all pq>2/pi.
  The initial R5 operator-path continuation gave only a small angle
  improvement, which is not claimed or published in this packet.
* [Paired-rank reduction and Gaussian cancellation](../gaussian_majorisation_rank_abel/PROOF.md),
  source `f7c122d6a5ade217930d63da27e67f9a9e55a539`, graph
  `bafkreidnqtxulerp64z7i2syzjymc3beilgovd4gyfcu5h2mzmim5l5ytu`.
  The two-coordinate sampling calculation is reproduced in our proof.
  The finite fixture has paired affine rank six and is not covered by the
  rank-five sufficient condition.
* [Simplicial cone reflections](../gaussian_simplicial_cone_reflections/PROOF.md),
  researcher 7, source `a792a1a8601d347e6e45a00bf9a3fc849d91f4b7`, graph
  `bafkreidbsexp7txezqi7745mb5d57ztkzptjrfas4gvwf6ujqakiyjzusy`.
  Supplies the simplicial half of the undamped dual-cone classification and
  the square-cone model for its nonsimplicial half. The R4 damped theorem
  does not depend on that classification.
* [Scalar-defect criterion](../gaussian_majorisation_scalar_defect/PROOF.md),
  researcher 5, source `a8c8a21bde0eb356cf1fc302e3f9b13f1e9b113e`, graph
  `bafkreidpgtehewdn2wn72hfi4c6aoq5bohkdss6dv36o37rjyxg6ndzxlq`.
  Its full proof was read at this pass start. It gives R5 motions when one
  pair of scalar coordinates fits inside every squared-distance deficit.
  Section 4 excludes that certificate on our open two-cone pieces for
  every positive lambda; Section 5 gives a finite exact exclusion at 4/5.
* [Asymmetric atomic bridge obstruction](../gaussian_atomic_bridge_obstruction/PROOF.md),
  researcher 7, source `d05dd54b551a5a14329cfbe31f8b66c13cc0e217`, graph
  `bafkreihqcqwjylfikk74mclhloshmpkpap7xdr233z6bu2rw7wryagqx2i`.
  Its nine-point law rules out specific martingale and common-target
  certificates. The fresh
  [independent review](../gaussian_atomic_bridge_obstruction_review1/README.md),
  source `b89f9f31a95637f92f7235a5693d2edbc5e530f6`, accepts that result
  with high confidence. That review does not review this new packet.

## New work inspected during the publication refresh

* Researcher 5's
  [asymmetric eventual-majorisation theorem](../gaussian_asymmetric_eventual_majorisation/PROOF.md),
  source `733f2f1ffeec6a97089fbdaa5bd89aa997da2240`, was read in full.
  It proves every hinge for the undamped nine-point square-cone law at
  variance at least 13200, and at least 16896 throughout an L1 weight ball
  of radius 1/25000. Its validated sphere cubature proves a uniform spherical
  gap; the smaller-variance regime remains open. It does not imply a new
  ball-volume result. Our theorem instead changes the endpoint by a uniform
  damping and handles all variances, all weights, and arbitrary ball radii.
* Researcher 8's
  [tail-deficit obstruction](../gaussian_tail_deficit_obstruction/README.md),
  source `54372e691479d94f8c4a6ee9a7c3a7ab4ffdac3d`, was inspected at the
  same refresh. Actual two-atom contractions show that no vanishing modulus
  of mean distance deficit or entropy gap can uniformly bound the normalized
  spherical-tail approximation error. A signed next correction gives a
  separate possible route at zeros of the spherical gap. Those two-atom
  examples are positive for majorisation. This closes an approximation
  shortcut, not the present exact motion.
* Researcher 8's
  [common-target theorem](../gaussian_majorisation_common_target/PROOF.md),
  source `3ad6ed0be174d1292b250efcad734d03eed01af5`, graph
  `bafkreiefowbrpgnu2cjyyuyig4y2gzk5zdchubp3xqpcgu2rzzpy5fe25m`, and its
  [independent review](../gaussian_majorisation_common_target_review2/README.md)
  had already been read. Its all-variance uniform-flap result closes the
  prior continuation of this lane's fixed-core work. That route remains
  parked. The new cone theorem uses the original labels and arbitrary weights.

The tail, endpoint, and common-target results are coordination context,
not unacknowledged premises in the positive proof.
Researcher 7's latest durable pass report additionally records positive
degree-32 polynomial tests at five variances and no certified negative
hinge. Those finite audits were retained privately; they are not premises
of this packet and are not interpreted as a full comparison. Their lane
retains direct asymmetric counterexample searches, while this lane owns
the geometric class and nonsimplicial motion mechanism.

## Novelty and trust boundary

Bounded live searches covered damped/scaled cone reflections, contracting
motions, Kneser--Poulsen special contractions, and positive operators on
indecomposable cones. They located the classical identity-extremality result,
which is explicitly credited, but no identical product-cost criterion or
damped tangent-arc construction. This does not establish historical priority.

The scope advance is the variational geometric principle and its uniform
all-variance, arbitrary-radius consequences. The optimum is for (6), not
for all possible motions. The new rational example rules out the two
specific certificates stated in the proof. It does not exclude every prior
geometric factorization, prove the undamped dual-cone Gaussian comparison,
or solve the unrestricted dimension-three problem.
