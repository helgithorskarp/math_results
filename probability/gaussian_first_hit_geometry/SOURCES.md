# Sources, dependencies and limits

The sole campaign target remains full Gaussian-convolution majorisation in
dimension three under arbitrary 1-Lipschitz maps, as posed in Conjecture1.1
of Gautam Aishwarya and Dongbin Li,
[Gaussian Convolution, Internal Energies, and the Kneser--Poulsen Conjecture](https://arxiv.org/html/2609.07041v2).
The present source does not settle it or enlarge the known map classes.

The event specifications being tested come from the team's
[prior-stationary contact and Brownian witness author proof](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_prior_stationary_contacts/PROOF.md),
source commit `4e1899ea00cd49e86c365604e2b4cbbe2016fbfb`, graph6323
`bafkreicfifksgqojo563256s2vm23c3ekcbuftk33lfuw4cahx3xobmnxa`.
Its independent review was still pending at this pass's initial graph6383.
The earlier [contact reduction](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_majorisation_heat_profiles/CONTACT_REDUCTION.md)
was accepted at review6166, target6140
`bafkreibrti7gur7ddhxqck2kq7lco2x6lmosmorbytzjfzb26qufiasy3m`.
Their mathematical files are preserved unchanged. The example here is
proved directly and does not rely on the global reduction being correct.

The earlier Brownian source already warned that balanced terminal variables
alone need not have favorable noise-energy covariance. Its scalar signed
control was not a Gaussian contraction/contact. The present distinction is
an actual Gaussian equality contact with four affinely independent sites,
all-prior equality, the true top set, and the precise event probability
budgets. It also compares two valid noise couplings of the same experiment.
The strictness and transverse-crossing hypotheses are explicitly absent.
No claim is made to have found a counterexample to those stronger hypotheses.

The proof uses only direct Gaussian densities, conditional expectation,
Brownian symmetry and continuity, a second-moment Markov bound, elementary
Gaussian level-set inclusions, and pi<22/7. These are classical tools, not novelty
claims. A short positive-series bound verifies the exponential constant.
No theorem about independent Brownian outputs is assumed; the required
estimates use their individual marginal laws.

The new team inputs were inspected before the attempt. In particular,
[R5's replica interaction](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_replica_interaction/PROOF.md)
(source `49a7d4c0828418b342e209b91c8753173a51ed3b`, graph6362
`bafkreicp5fr5uoquxbrunjvq7idskx5rg47hsxedl4qnastmppakpngaba`)
and [R8's relative spherical transfer](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_relative_spherical_transfer/PROOF.md)
(source `e949d9f482f3bb61b19f6d8ecc205561eaed0a80`, graph6376
`bafkreibblggn3ysibhslp7rdh5websr6jdcaiduc4omw4p5ud7uul45hsi`)
do not supply a signed, top-set-conditioned first-hit comparison. They are
context, not premises of this example. No conditional version of their
averaging or approximation results is imported.

This is a bounded checkpoint closing an event-only detection attempt.
The signed covariance at a strict adverse first contact remains the
unresolved obligation. The source supplies neither an equivalent sufficient
inequality nor a general impossibility theorem for probabilistic methods.
Independent review is pending. The exact checker covers finite rational
constants only; the continuum argument is written mathematics, with no
proof-assistant formalization, simulation, or omitted external artifact.
