# Primary sources and exact increment

Checked 21 September 2026. This is a scoped structural note, not a new
projection theorem or a solution of the Euclidean distance conjecture.

1. Minh-Quy Pham, *On Falconer type functions and the distance set problem*,
   [arXiv:2510.15118v2](https://arxiv.org/html/2510.15118v2),
   27 February 2026, Theorem 1.4(ii), surrounding paragraph, Theorem 3.1.
   The intended setting is quadratic although the displayed statement
   omits that adjective. It asserts the half-total image dimension bound.
   Our note gives an exact test for making its universal compact-product
   quantifier valid. The all-positive-factor version is credited here,
   not claimed as our new result. The separate
   [journal landing page](https://link.springer.com/article/10.1007/s00208-026-03427-3)
   identifies the publication; the full journal text was unavailable for
   comparison. We make no claim about whether its wording was corrected.

2. Minh-Quy Pham, *On Hausdorff dimensions of k-point configuration sets and
   Elekes-Ronyai type theorems*,
   [arXiv:2603.03567](https://arxiv.org/html/2603.03567),
   Theorem 1.8 and Remark 1.10(i). This later paper explicitly requires
   positive dimensions for each factor and already gives the collapsing
   example Q=x(y+z), A={0}, B=C=[0,1]. Finding this source closed our initial
   new-counterexample route. The example is not new. The later theorem
   concerns a broader analytic class and a different dimension estimate.

3. Kevin Ren and Hong Wang, *Furstenberg sets estimate in the plane*,
   [arXiv:2308.08819v3](https://arxiv.org/html/2308.08819v3),
   Theorem 1.2. This supplies the sharp exceptional projection bound
   max(2u-dim_H K,0). It is the deep external input to our proof of the
   positive-factor case. We do not rely on the endpoint assertion in
   Pham's abstract projection framework; our proof uses strict dimension
   separation and then a supremum for the full image.

4. Nuno Arala and Sam Chow, *Expansion properties of polynomials over finite
   fields*, [arXiv:2403.03732](https://arxiv.org/html/2403.03732),
   Definition 1.1 and Lemma 1.5. The coefficient-map rank alternative for
   nonadditive ternary quadratics is an established ingredient. Their
   stated lemma is over odd finite fields. Our proof includes the short
   real-coefficient calculation and does not transfer finite-field claims
   without justification.

5. Doowon Koh, Thang Pham and Chun-Yen Shen, *Falconer type functions in three
   variables*, [arXiv:2106.01612](https://arxiv.org/abs/2106.01612),
   Journal of Functional Analysis 286 (2024), article 110246. Their
   positive-measure theorem above total factor dimension two is prior
   work. Neither our coordinate-line obstruction nor this criterion
   challenges that theorem.

6. Sung-Yi Liao, Thang Pham and Chun-Yen Shen, *On L2 estimates for quadratic
   images of product Frostman measures*,
   [arXiv:2601.09582v2](https://arxiv.org/html/2601.09582v2),
   3 September 2026, Theorem 1.3. It explicitly attributes the common-set
   half-total bound to Pham. Our criterion is for three arbitrary compact
   factors, including distinct zero-dimensional factors, rather than a
   new common-set bound or a new energy estimate.

The explicit base-27 Cantor construction uses the classical separated-digit
mass-distribution argument, supplied in full in PROOF.md. Inverse-branch
transport of an additive obstruction is standard. Frostman's lemma,
countable stability of Hausdorff dimension, Fubini's theorem and the local
inverse function theorem are additional standard proof inputs.

The precise increment is the equivalence between the universal statement
for every real polynomial of total degree at most two and the two explicit
coefficient conditions (L) and (R), with counterexample mechanisms covering
every failure. This is a modest structural consequence of established
results, not a claimed advance in the sharp Falconer threshold. Targeted
searches for this universal coordinate-line criterion found no identical
statement; that is search-relative novelty, not a historical priority claim.
No independent review or formalization of this note is claimed.
