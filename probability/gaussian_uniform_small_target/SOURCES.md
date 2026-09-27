# Sources, dependencies and scope

The human-named source is Gautam Aishwarya and Dongbin Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture,
arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2), inspected on
27 September 2026. Conjecture 1.1 is the full majorisation target;
Theorem 1.4 supplies the established continuous-contraction context.
The fixed-variance theorem here does not provide the uniform-in-variance
comparison needed for the paper's Kneser--Poulsen implication.
The full graph problem is
`bafkreifx5vhi7azxuu4chant6r4c7vvgjsypwdoob4ug7ea2nmzctlsrhu`.

## Analytic ingredients

The earlier [bounded-law stability proof, Section 5](../gaussian_majorisation_open_stability/BOUNDED_LAWS.md)
derives the homothety continuity equation, Gaussian posterior covariance
identity and strict hinge identity for arbitrary bounded laws. Section 6
already gives strict point-target comparison and qualitative fixed-law
stability. These are prior ingredients, not new claims here. Source commit
`52ef6716a271b31ac1046207764fc78d3db6165c`; graph6102
`bafkreietfhclp4t463gjaeyh4ldpj2eeognjhwdphuywmdxyrepqwskdiu`.
Our proof rederives the needed identity with scale parameter t in [0,1],
quantifies a terminal time/space region uniformly in radius and covariance,
and joins it to a uniform pointwise tail comparison.

Gaussian pair-overlap peak control, posterior pair variance, the L1
Gaussian translation bound and the principal-minor characterization of
positive semidefiniteness are elementary tools recalled with their constants.
There is no novelty claim for them. The directional aggregate-mass lower
bound removes any need for individual atom weights or support-net cell
masses in this join. The proof consumes neither the general R6 five-dimensional
target-peak theorem nor an R2 martingale certificate.

## Concurrent comparison and certificate spine

R2's [dilated-martingale theorem](../gaussian_dilated_martingale_certificate/PROOF.md)
was present before this publication: commit
`63f42fa6f5173c69391c08b40af53a470663221a`; graph6464
`bafkreigsw5tg5pvscer2mm55fmd57ackiiwh55a24qu7wnbzjjmy7uguba`.
For centered radius R and covariance at least kappa I, it includes every
1-Lipschitz F damped by `c<=kappa/(4R^2)` when
`s>=2816 R^4/kappa`. This is much stronger where that variance guard holds.
The present result supplies a different all-threshold join at every specified
variance, with a much smaller target radius. Neither result signs arbitrary
undamped contractions. R2's coupling producer and algorithm are not duplicated.
Before this publication, R2's theorem received independent
[acceptance6480](../gaussian_dilated_martingale_review/REVIEW.md), source
`2f8e01ccd26751dade844412ed1f298021e68607`, graph
`bafkreieymonxvy43zcygdkmi7i5wq3gbf5mhakxqdafw5ic3za2f7x4dde`.

The [cutoff consolidation](../gaussian_mean_loss_margin/CUTOFF_CONSOLIDATION.md)
designates R3's effective proof6426, independently accepted6432, as the
shared small-loss consumer. R8's independent midpoint proof6428, accepted6434,
is preserved as supporting evidence. No extension of either formula is made.
These cutoffs are context, not premises of the present theorem. R3's
[moving-window continuation](../gaussian_small_loss_defect/PROOF.md),6450,
accepted6460, makes its flat-defect statement effective but does not itself
join all thresholds at a fixed positive loss.

R3's subsequent [cloud-budget obstruction](../gaussian_endpoint_join_obstruction/PROOF.md)
shows that the older finite-cloud tail schedule cannot meet that small-loss
window, even allowing arbitrary cloud counts and diffuse clouds. This was
inspected before publication: commit `e3503fef13c51da2b8da4f4d44337c6c75b163d7`,
graph6478 `bafkreid3y53zpjqof4xy67si3vzkdzeoijc5wd22krnvzpyfkpiuaiefl4`.
The present proof uses pointwise tail dominance and a different upper-window
margin. It does not close the small-loss regime excluded from that composition.

R3's [loss-proportional cubature](../gaussian_prior_localization/LOSS_CUBATURE.md)
is relevant only to finite consumption. Same-pair degree-two reduction keeps
the marginal first and second moments on original support, so it preserves
the covariance floor and both centered radius bounds used here. It does
not identify the original and cubature Gaussian hinges. The theorem does
not need cubature for its analytic proof. Source commit
`afacddeb257993b31ee118ff92e7360a7870cbc6`; graph6364
`bafkreicuyedmct5zhkt5cxba2nkvgel3tkursxckgxcryd45ed53khps5e`,
independently accepted6380
`bafkreia62tjvdimerupjq35kmi27cdxsknhqy4sg6bzhoiuatovvrwdluu`.

All new analysis is an author proof awaiting independent review. Exact
code controls and a public source commit do not change that status. This
is an explicit uniform strengthening of a known fixed-law stability mechanism;
historical novelty beyond the searched primary source and team artifacts
has not been established. The full R3 question and any new Kneser--Poulsen
consequence remain unresolved.
