# Gaussian set transfer and measure localization

The new [threshold-relative certificate](RELATIVE_HINGE.md) bounds the error
in a hinge divided by its threshold. It certifies entire positive threshold
windows directly, including exponentially small levels. An exact known-positive
Gaussian control has upper adverse relative gap below -30 throughout
`[2^-26,2^-24]`, where the old absolute error divided by the threshold exceeds
one million. The replay takes about nine seconds. This is a sign-certificate
method control; no unknown contraction or full configuration cover is signed.
Independent review is pending, and the global `D<=7/50` bound is unchanged.

Run `python3 -B relative_hinge.py --check` and
`python3 -B -O relative_hinge.py --check`. Expected status:
`RELATIVE_HINGE_WINDOW_CERTIFICATES_PASS`. The [proof](RELATIVE_HINGE.md)
states the link to R8's existing signed-endpoint/middle certificate and the
remaining coverage obligation. [RELATIVE_EXPECTED.json](RELATIVE_EXPECTED.json)
records the exact bounds; [RELATIVE_INPUTS.json](RELATIVE_INPUTS.json) pins inputs.

The latest [direct hinge certificate](DIRECT_HINGE.md) evaluates the maximum
defect over **all thresholds** on an existing finite input, with rigorous
second-order spatial quadrature and an exact sweep of the density-value knots.
It avoids high-degree moment expansion and supplies converging lower/upper
defect bounds. On a rank-six member of the rational frontier, grid refinement
gives upper bounds below 0.194, 0.048 and 0.012; that known-positive map is a
control, not a new subclass. No entire configuration family is enumerated,
and the universal D<=7/50 bound is unchanged. Independent review of this new
oracle is pending.

Run `python3 -B direct_hinge.py --check` and
`python3 -B -O direct_hinge.py --check`. Expected status:
`DIRECT_HINGE_CERTIFICATES_PASS`. The full exact replay takes about 12 seconds
and 31 MB on the author's host. [DIRECT_EXPECTED.json](DIRECT_EXPECTED.json)
records the bounds and stream hashes; [DIRECT_FIXTURES.json](DIRECT_FIXTURES.json)
contains the rational controls. `direct_hinge.py --budget k` gives a uniform
per-input enclosure width below 21/(100k) on the unchanged rational family.
The global coverage obligation and a parameter-cell error budget are explicit
in [the consumer contract](DIRECT_HINGE.md#5-uniform-consumer-contract-on-the-unchanged-rational-family).

The earlier [square-root threshold budget](SQUARE_ROOT_BUDGET.md) lowers the
required largest moment power from 65536 k^8 to **2048 k^5-1** on the same
finite rational configurations. It combines a geometric superlevel-volume
bound with total probability mass and a classical positive kernel. The
resulting unrestricted rational beta error is <973/(256k). The
[exact controls](weighted_degree.py) check the kernel, constants and consumer
budgets; they supply no unknown Gaussian sign. A subsequent
[independent review](../gaussian_square_root_budget_review2/REVIEW.md) accepts
this degree reduction and its stated error compositions.

Run `python3 -B weighted_degree.py --check` and
`python3 -B -O weighted_degree.py --check`. Expected status:
`SQUARE_ROOT_DEGREE_BUDGET_CONTROLS_PASS`. The [expected record](WEIGHTED_EXPECTED.json)
and [pinned sources](WEIGHTED_INPUTS.json) are compact and use only standard
library Python. The existing paired rational producer is unchanged.

The [paired-cubature frontier](CUBATURE_FRONTIER.md) reduces the
previous k^6 atom bound to O(k^3(1+log k)^(3/2)), with explicit integer
budgets. Matching both latent coordinate-moment lists on shared actual
sites preserves the contraction. Its compact error is <11/(4k); the
updated finite rational beta error was <3107/(768k) using the credited
row N=2^16 k^8-2; the new degree supplement improves that testing budget.
The paired-cubature reduction now has
[independent acceptance](../gaussian_paired_cubature_review2/REVIEW.md), graph
height 6218; the full question remains open. This does not numerically improve the separate
D<=7/50 bound without additional signed estimates.

Run `python3 -B paired_cubature.py --check` and
`python3 -B -O paired_cubature.py --check` from this directory. The expected
status is `PAIRED_CUBATURE_FRONTIER_CONTROLS_PASS`; the exact
[record](CUBATURE_EXPECTED.json) and [pinned inputs](CUBATURE_INPUTS.json)
cover finite cubature and rounding controls, not Gaussian signs. The new
`round_instance` in [paired_cubature.py](paired_cubature.py) uses W=4kA_k;
the earlier producer keeps its original interface and fixtures.


This packet proves measure-side reductions of the dimension-three
Gaussian-majorisation question and identifies limits on exact localization.
It does **not** settle the open conjecture or add a Kneser--Poulsen class.
Complete author proof; independent review pending.

The [uniform defect localization](DEFECT_LOCALIZATION.md) proves that
the worst possible Gaussian hinge defect D satisfies

    0 <= D-D_k < 4/k,

where D_k is an attained maximum over at most k^6 matched atoms, both
supports in B(0,2k), at variance one. Consequently any violation of size
delta>0 has a witness retaining at least delta/2 with k=ceil(8/delta).
The bounds do not depend on the original support extent. A randomly
shifted cube partition controls source overlap by Gaussian boundary
crossing; target overlap has a favorable sign. Quantizing one conditioned
cube then preserves the original pairwise contraction.

This is a uniform finite-dimensional frontier with an error bound, not a
computed sign or an exact finite-support optimizer theorem. Its atom bounds
are large. Conditioning need not preserve a prescribed dominant atom, and
unprotected independent rounding of input and output sites is not valid.

The [effective rational interface](RATIONAL_INTERFACE.md) now supplies that
missing rounding guarantee. For R8's moment budget and R2's exact producer,
it gives at most k^6 labels, radius 3k, coordinate denominator 256k^3,
weight denominator 4k^7 and integer-verifiable positive pair margins.
With R8's existing largest power 2^16 k^8, the maximum beta defect F_k
over this explicit finite integer family satisfies

    0 <= D-F_k < 4067/(768k) < 16/(3k).

The interface specifies the complete input schema, conditional detection
at a prescribed gap, a uniform absolute-error certificate obligation,
configuration counts and a moment-precision budget. It also supplies an
exact pair-distance-loss floor for non-point laws. Its new content is
effectivity of the existing compact frontier. No global enumeration,
Gaussian moment, unknown sign, or efficient exhaustive procedure is claimed.
The proof and the [exact rational producer](rational_frontier.py) cover
collisions and zero weights by merging before expansion and rounding.

The [shift-averaging boundary](SHIFT_AVERAGING_BOUNDARY.md) shows why one
proposed cancellation of the partition error fails. For eight equally
weighted sites, a strict contraction with paired affine rank six has
**decreasing mean hinge interaction** under random shifts of a cubic
source partition. An exact small-cube expansion gives the negative sign.
The same sites admit a straight contracting motion, so full Gaussian
majorisation remains true. This rules out a proposed interaction inequality;
it does not refute a zero-error inequality for positive defects or settle
the main question. The localization proof and its bounds are unchanged.

For a compact support K, continuous map T, Gaussian variance s, and a set A
of finite positive volume v, define

    m(A) = min_mu [ sup_{|B|=v} integral_B (T#mu)*gamma_s
                                      - integral_A mu*gamma_s ].

The [proof](PROOF.md) establishes:

- An ordinary set B of volume v attains the equivalent max-min problem
  simultaneously over every centre in K. It is a superlevel set of a
  minimizing target Gaussian mixture. The minimizing measure is supported
  on the contact set of the resulting Gaussian mass potential.
- All-law Gaussian majorisation is exactly m(A)>=0 for every A. The
  [dominant fixed-atom reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md)
  has an explicit version retaining compensation by the fixed atom.
- On a sphere under x -> cx, 0<c<=1, the corresponding minimizer for a
  centred-ball test is uniquely uniform surface measure, provided
  (cR)^2<=3s. This remains true with any fixed positive rare mass beside a
  dominant atom at zero. No finite prior attains the optimum; every fixed
  atom bound has a strictly positive optimization error.
- A delta-net still approximates the value within
  (1+Lip(T))delta/sqrt(2 pi s), multiplied by the rare mass in the anchored
  version. Strict negative witnesses remain finitely approximable.

The obstruction is to **exact optimizer localization**. It neither refutes
finite counterexample witnesses nor provides a counterexample to Gaussian
majorisation. The common-set inequality remains unproved for arbitrary
contractions. The sphere example already has a classical contracting motion.

Reproduce the compact algebra controls with standard-library Python 3.11+:

```sh
python3 verify.py --check
python3 -O verify.py --check
python3 localization_audit.py --check
python3 -O localization_audit.py --check
python3 interaction_audit.py --check
python3 -O interaction_audit.py --check
python3 -B rational_frontier.py --check
python3 -B -O rational_frontier.py --check
sha256sum -c SHA256SUMS
```

[EXPECTED.json](EXPECTED.json) contains exact rational checks of the
hyperbolic-series identity, the positive exponential-kernel tensor identity,
and finite-cell saddle controls. Finite-cell data are explicitly not Gaussian
contraction examples; their ties explain why the analytic no-plateau step
in the proof is needed. The universal result relies on the written proof,
standard minimax and analytic facts, not numerical integration or a solver.

[LOCALIZATION_EXPECTED.json](LOCALIZATION_EXPECTED.json) records the new
partition controls at every finite-model breakpoint, exact shifted-grid
crossing controls, a failure of independent endpoint rounding, and the
rational constant check. Its finite cells are not Gaussian counterexamples.
The reported k^6 frontiers are symbolic sizes; none was enumerated.

[INTERACTION_EXPECTED.json](INTERACTION_EXPECTED.json) records all eight
cube partitions, Walsh orthogonality, all 28 pair types, rational motion
controls and the exact radical sign margin. There is no quadrature or
claim that the audited rational parameters lie in the asymptotic sign
range. Existence of that range follows from the written analytic proof.

[RATIONAL_EXPECTED.json](RATIONAL_EXPECTED.json) records six producer
controls, including near-colliding isometries, zero weights, target
coincidences, point laws and a rounding failure when merging is omitted.
The audit checks exact integer constraints and rational budgets, four
malformed-input rejections and 91 coefficient-norm controls. Its expected
SHA256 is `22f543a40f8a2a1298ce2ff933bb78422f57528b032db957b5d481725d1d227c`.
The universal denominator and error bounds rely on the written proof;
finite controls do not establish an all-configuration beta sign.

See [SOURCES.md](SOURCES.md) for mathematical attribution, team dependencies,
the literature boundary, and the distinction from existing per-law endpoint
couplings and finite strict rational-witness reductions.
