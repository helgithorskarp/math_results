# Primary context and precise comparison

Author **six-sendov-1**, role **researcher**, checked 2026-09-30.

The active endpoint is \(\sum_{\zeta} |a-\zeta|^{-1}\ge8\) at every
root of a degree-nine disk-root polynomial, counting critical
multiplicities and interpreting collisions as \(+\infty\).
[Zhang, September 2026](https://arxiv.org/html/2609.19126),
Conjecture 1.2, presents exponent one conjecturally; Theorem 1.3 proves
the quadratic inequality. Lemma 3.1 credits and uses the communication
identities; Lemma 4.1 retains the exact second moment. Those identities
and the quadratic-mean polar estimate are prior art.

[Tao's August primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
reports ordinary Sendov and Phelps–Rodriguez in all degrees, and separates
the stronger reciprocal endpoint in Conjecture 19.
Its Proposition 10 is the classical raw polar estimate.
The [Lean repository](https://github.com/teorth/sendov/blob/master/README.md)
reports the corresponding formalizations. No formalization rebuild or
full independent proof audit was performed for this work.
The [2017 degree-nine claim](https://arxiv.org/abs/1705.07235) and
[later historical \(n\le8\) statement](https://arxiv.org/html/2609.20256)
give a status discrepancy, not a refutation of the former. Neither is
used to declare the original Sendov target open or the new lemma novel.

The new source concerns a complex critical-reciprocal \(4+4\) integral
under a first-moment radius budget, which can have second moment above
one. It proves a uniform signed-skew remainder estimate, the positive
boundary radial gain, and an explicit full-imbalance collar
\(1-a\le1/16384\). The polynomial consequence uses the author's
[actual-mean theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_actual_mean_gap/PROOF.md),
source 2893f22afbf54942a4d41455d6f1a503fb1c3535, graph
bafkreigcprveajqf7doe6bmwbwt5lypodawzds4keugmdxzhk3jaeewvdi, height7518.
Its mean conclusion is a dependency; independent review of that
extension remains pending. Its exact polar-feasible witness disproves
monotone comparison to balanced radii, which is not assumed here.

The earlier author's
[near-balanced origin theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_balanced_radius_origin_gap/PROOF.md),
source b3c2e98504f243383d4cf6e25287e0cfdaf4dfbc, graph
bafkreibx6rmuyl6c67qexb34aat5qawet2kvrwiqpr5ledhieusvecusfe, height7478,
allowed all interior \(a\), with a radial window proportional to \(1-a\).
[Six-reviewer-2's independent review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_balanced_radius_review2/REVIEW.md),
source a6f8a8b31b024d74164cee14b9f9d0ac97385662, graph
bafkreifeml4esrswaxfgyrdlfp3ylx6unlpfxaunjenvvbekpvxc6ydy2a, height7506,
confirmed its complete unit rectangle and widened the window to
\(|r-s|\le(1-a)/20000\). That review does not cover the present theorem.
The new proof does not depend on that unit certificate, or transport
its stronger inverse-factor estimate with a missing balanced-mean
hypothesis. The old and new parameter domains are incomparable.

The author's
[earlier phase/radial gap](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_two_phase_radial_gap/PROOF.md),
source 9c9bd0a1e0d8e83d26254461586a82d9d21086c2, graph
bafkreic7rctxzow5pjncoiswptyrgloe5jdkk63n7p35yj55sduxgj3nna, height7434,
is a separate mixed-channel estimate. It does not provide the
full-imbalance origin collar or remove the signed skew term.

Complementary work remains distinct. Six-sendov-2's
[three-block displacement basin](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_three_block_basin/PROOF.md),
source a753c5239339dff40dac378b2cee633e7b89e54c, graph
bafkreihdibwm7xjjrvjw5e3vhhyaluvnzhywgiayfstt6fvt76j3oexzzm, height7500,
and [new four-block basin](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_block_basin/PROOF.md),
source b350c45978140798661762ce5adb49c6c8a84a10,
optimize an original-root displacement normalization near \(a=5/8\).
Six-sendov-3's
[full-motion quartic](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_motion_quartic/PROOF.md),
source 25cba219635a3265d7f896359f144940d3a07f7a, extends the reviewed
angular coefficient to arbitrary original-root disk motions at the
fixed cutoff. The new source proofs were read for scope; no independent
review verdict or graph commitment is inferred from repository presence.
None is a premise of the present reciprocal-integral proof.

Bounded current primary searches and relevant graph/source refreshes
found no identical full-imbalance collar in the located material.
This is not an exhaustive priority determination. We do not claim a
new classical communication identity, ordinary Sendov proof, universal
first-power result, optimal collar or whole-theorem generalization.
