# Sources, prior scope and trust

The human-named problem is Aishwarya--Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2),
arXiv:2609.07041v2, Conjecture1.1 in dimension three for bounded laws.
The primary manuscript was checked live on27 September2026. The
unrestricted all-variance question remains open.

The essential accepted input is [the spherical-gap endpoint](../gaussian_majorisation_eventual_endpoint/PROOF.md),
source `48bcea2f85f958f7435aeeb94c2975c4b1e53fc6`, graph6032
`bafkreidhwtkvf5x7vwqont7sizng7wlezmowfgs6kvt4cdkee5yeelkqi4`.
[Its independent review](../gaussian_majorisation_eventual_endpoint_review2/README.md),
source `c750676fd6e164db43c0891c0093ebed2a49c356`, graph6048
`bafkreih6v5ttck5sx6ivw5xrvn7oqzvmuqylrfyohzvpek3k7bm6ohbbli`,
accepts the full endpoint and directly audits both analytic dependencies.

Those dependencies are the [spherical-tail comparison](../gaussian_majorisation_spherical_tail/PROOF.md),
source `740f95368f291816672c96ae1e71a06a9186519d`, graph6002
`bafkreiakfdyplrgs5zveoa2ocaggbrq4ptyrkfdq5efhatguxxntp7u7pi`,
and the [high-noise window](../gaussian_majorisation_high_noise_window/PROOF.md),
source `42fef5f197d9e601db9d1f637b84c4d6215a3039`, graph6008
`bafkreia7jrgymt6rfik4g5kktjinnt5a2dlvpe4y75kwmemx563nssqh7q`.
The new proof imports the accepted all-threshold endpoint; it does not
present another audit of coarea, Abel inversion or the radial tail error.

The endpoint's Corollary3 already gives qualitative eventual majorisation
for finite contracting pairs admitting a martingale witness of convex
order. For such finite pairs, the current work is a uniform effective
subclass of that known sufficient route, not a claim that their eventual
positivity was previously unknown. The new supplied condition is a dilation
margin a>1, yielding one explicit variance bound for arbitrary bounded laws
and a closed-form covariance/damping family. The finite certificate is a
small matrix, with no search over replicas or spherical parameters.

Conditional Jensen, concavity of a fractional power, covariance identities,
and the nonnegative affine product-density construction are elementary
ingredients, not new transport theorems. We construct the coupling directly;
Strassen's theorem or a numerical transport optimizer is not a premise.
The classical Euclidean Kirszbraun extension is used only if the original
contraction is specified on its support. Its existence places the target
in a radius-R ball about T(E X); the checker need not find that anchor.

The handoff uses the accepted [same-pair cubature](../gaussian_prior_localization/CUBATURE_FRONTIER.md),
source `7c5bd936a9f22e1eeb03ac2775ee711295458a8c`, graph6212/6218,
and its [loss-preserving refinement](../gaussian_prior_localization/LOSS_CUBATURE.md),
source `afacddeb257993b31ee118ff92e7360a7870cbc6`, graph6364/6380.
The six consumed source files are content-pinned in [INPUTS.json](INPUTS.json).
Preserving a sufficient guard is different from preserving every hinge.

The earlier [bounded-law stability bridge](../gaussian_majorisation_open_stability/BOUNDED_LAWS.md)
already puts a nonpoint source paired with a point target in the interior
of majorisation at each fixed variance. Its compactness neighborhoods do
not supply the explicit all-law radius/covariance bound proved here. We
do not claim discovery of stability near a point target or of martingale
sufficiency. Historical priority of the assembled quantitative condition
has not been established by the targeted source search.

The current graph/source refresh was inspected: the previous R2 guard6442
is now accepted6448; R3's moving-window defect6450 is accepted6460. R8's
general covariance boundary6454 and R5's complete beta row6452 remain at
their own review status. None is an all-threshold premise here. The new
Coxeter-orbit6462 and screw-motion6456 families use different geometric
hypotheses and are not ingredients of this certificate.
The known rank-six conditional-kernel obstruction is respected: the kernel
here is a probability coupling between endpoint laws, not a purported
nonnegative conditional Gaussian replica kernel.

The finite controls use classical coordinate folds and clipping, including
full paired rank six and a matched map whose dilation expands. These are
already familiar positive geometries, chosen to test the certificate's
logical boundaries. They are not offered as new example classes. Some
controls exceed the worked mean-loss, Q/d and covariance-collapse cutoffs,
but this does not assert they escape every previous sufficient theorem.

The code checks exact finite algebra and supplied records, not the analytic
theorem, historical priority or independent acceptance. No solver, numerical
quadrature, private corpus, floating-point sign or omitted large evidence
is used. All prior artifacts and parked work are preserved.
