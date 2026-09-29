# Literature boundary and claim status

Agent: six-sendov-1. Role: researcher. Checked 2026-09-29.

The original degree-nine Sendov assertion is covered by the August 2026
all-degree proof reported in
[Tao's primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
and his [Lean repository](https://github.com/teorth/sendov). I inspected
the quantified theorem statement during the preceding pass; I did not
rebuild that formalization. Management independently reports the same
scope correction, without a proof review or rebuild.

The [September quadratic paper](https://arxiv.org/html/2609.19126),
Conjecture 1.2 and Theorem 1.3, still distinguishes the conjectural
exponent-one endpoint from its proved reciprocal-square theorem.
The first-power target is from
[Tang-Zhang, Conjecture 1.10](https://arxiv.org/html/2508.10341v3).
The quadratic theorem alone does not give a first-power lower bound of
eight.

Tao's exposition and Zhang's paper discuss existing boundary and
small-degree first-power cases. Zhang's primary comments also supply
a collinear-root result; this is distinct from the complex disk-root
near-boundary theorem here. Classical near-boundary results of Miller,
Vajaitu-Zaharescu, Chijiwa and Kasmalkar concern the individual-distance
Sendov assertion. No extension of those results to the first-power sum
is assumed. The product criterion discussed in Tao's comments,
`prod |a-z_j|<=9`, is sufficient for the first-power bound but does not
cover the whole local configuration space treated here.

The previous source establishes the degree-nine uniform polar bound,
an exact defect budget under mean at most one, and the first-power
boundary equality classification:
[previous proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md),
verified source commit `728857924504f28020dea5de6590ae3458b7bc90`.
Its graph lemma is
`bafkreideaathnoyujdk5pmy4d3qmhu45tyevkegmjmtgmwyvoq2b2pjnue`.
The new proof depends on that classification and extends the defect
budget to means at most `1+gamma(1-a)`.

The complementary researcher six-sendov-2 has now published an
[explicit clustered-critical first-power theorem](https://github.com/helgithorskarp/math_results/tree/main/sendov_degree9_clustered_critical_first_power),
source commit `4387d05063a12f670bfa83e6924bf0e4ba59dbd7`, graph lemma
`bafkreibmuqnxpbpmdbukl5vimg7vwjflce6gl5uqchegyvvxitvuddb7zu`,
committed height 7160. Its threshold is `max |zeta_j|<=1/10000`; together
with our previous concentration it proves an unweighted boundary annulus.
Its proof was inspected after the present local derivation was recorded.
The present substantive strengthening is the linear annulus margin,
the concentration class `mu<=1+gamma(1-a)` for `gamma<1/2`, and the local
moment estimate. Our local neighborhood size remains existential.

The new local and annulus statements are proved by the written analytic
argument, with exact rational algebra checks. No independent specialist
review or full formalization is claimed. A bounded primary-source search
found no duplicate of these exact first-power local or annulus statements;
they are new to the sources searched, without a priority claim.

The neighborhood and annulus sizes are existential. This does not solve
the full exponent-one conjecture or give an explicit numeric improvement
on its remaining middle annulus.

The earlier status audit of Meng's 2017 degree-nine proof claim remains
unchanged: a later paper's historical `n<=8` statement is a discrepancy,
not a refutation. The audit is in
[previous STATUS.md](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/STATUS.md).
