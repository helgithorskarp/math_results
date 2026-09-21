# Primary sources and contribution boundary

1. Terence Tao, *An integration approach to the Toeplitz square peg problem*,
   Forum of Mathematics, Sigma 5 (2017), e30.
   https://arxiv.org/abs/1611.07441
   Establishes square existence for the union of two graphs with Lipschitz
   constants strictly below 1 and common endpoint values. The two/two
   configuration used here belongs to this established geometric setting.

2. Ludovic Rifford, *A quantitative version of Tao's result on the Toeplitz
   Square Peg Problem*, arXiv:2106.01914v2 (2021), Theorem 1.1 and page 4
   discussion/footnote 5.
   https://arxiv.org/abs/2106.01914
   https://arxiv.org/pdf/2106.01914
   Proves side >=0.018 times the maximum gap for two 1-Lipschitz branches;
   simulations motivate the suggested optimal constant 1/2. The paper does
   not supply or assert the maximum-gap localization property refuted here.

3. Joshua Evan Greene and Andrew Lobb, *Square pegs between two graphs*,
   arXiv:2407.07798 (2024).
   https://arxiv.org/abs/2407.07798
   https://arxiv.org/html/2407.07798
   Gives a stronger rectangle-existence theorem for pairs of graphs under
   larger Lipschitz thresholds, including square existence below 1+sqrt(2).
   This is an existence theorem, distinct from the maximum-gap size target.

4. Prior graph contribution, *Sharp two-thirds square-size bound for two
   Lipschitz graphs with an affine branch*.
   https://github.com/helgithorskarp/math_results/tree/main/discrete_geometry/affine_branch_square_size
   Source commit: 2538cb79365caa81520e3fb7345dc7dc2a16330d.
   Discovery Net: bafkreigr753i3nrnnsnvddpteqv3ddszncrwrx4y23ojwkudrel5rdq2dm.
   Proves the sharp 2M/3 bound when one branch is affine, using a
   maximum-spanning square after rotating that branch to horizontal.
   The present obstruction does not weaken or contradict that theorem.
   The rational elimination/active-set kernel is adapted from its verifier,
   while the present fixtures, two-branch reduction, and assertions are new
   to this source directory. That earlier directory is not needed at runtime.

## What is established here

The new target is the sufficiency strategy of putting a square's entire
horizontal projection across a maximum-gap point. The envelope estimate
would make this a route to side >=M/2. We give an exact counterexample,
prove relative C0 persistence by compactness, and deduce existence for
rational-coefficient polynomial branches by Bernstein approximation.
These are a limitation on that proof route, not a bound improvement,
a counterexample to the half-gap conjecture, or a square-peg solution.

The mathematical tools—Lipschitz envelopes, finite linear incidence systems,
compactness, and Bernstein approximation—are classical. No novelty is
claimed for them. The explicit three-square obstruction and its localization
consequence were not found in the bounded primary-source and graph searches
on 2026-09-21. Historical priority is not established. The search included
square/rectangle results for two graphs, quantitative maximum-gap bounds,
and maximum-gap localization; it is not a survey of all square-peg work.

No source inspected in that search settled the general proposed 1/2 size
constant. This search-relative statement is not proof that no later result
exists. The general Jordan square-peg problem is not needed as a dependency.
