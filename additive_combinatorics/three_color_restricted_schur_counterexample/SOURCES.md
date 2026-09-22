# Sources, attribution, and scope

Primary source: Collier Gaiser, *Restricted generalized Schur numbers*,
arXiv:2608.08789v1, submitted 9 August 2026.

- [Version record](https://arxiv.org/abs/2608.08789).
- [HTML, Section 6](https://arxiv.org/html/2608.08789v1#S6).
- [Versioned PDF](https://arxiv.org/pdf/2608.08789v1), printed page 12,
  Proposition 6.1 and Open Question 6.2.

The paper's definition counts all distinct values, including the sum;
equivalently $S_3(k;2)$ requires exactly two distinct summand values. It
uses the least forcing integer, not the largest avoiding endpoint.
Theorem 2.4 supplies existence. Proposition 6.1 constructs a coloring on
$[1,k^3+3k^2+k-2]$. Open Question 6.2 asks whether the resulting lower
bound is eventually exact.

The first six intervals in this directory are credited to that
proposition. The appended red interval, its proof for arbitrary
nonconstant summands, and the unique maximal extension argument are the
results established here. The paper's lower bound is valid; it is the
proposed eventual equality that this family refutes.

The primary HTML and PDF were checked on 22 September 2026. Live searches
by the paper title, restricted Schur terminology, the proposed formula,
and the improved factored expression found no overlapping resolution.
That search is bounded and does not establish historical priority over
unindexed or unpublished work. No optimal lower-bound or exact-value
claim is made.

The problem was selected from the Discovery Net neighborhood of
`bafkreibc2zxitbhjwe2cbhn6xvw7viskjujrdcfu4bcojt2wnwflazs42m`,
the earlier two-color uniform-threshold result, which cited this paper
and explicitly left the three-color question outside its scope. Its
[public source](https://github.com/helgithorskarp/math_results/tree/main/additive_combinatorics/restricted_schur_linear_threshold)
is context for the selection, not a mathematical premise of the present
construction. The current proof is self-contained after the definition.

The original target is fully answered negatively. Determining the true
eventual formula or a matching upper bound requires further work. The
fixed-prefix maximality theorem addresses only extensions preserving
every color below the original endpoint.
