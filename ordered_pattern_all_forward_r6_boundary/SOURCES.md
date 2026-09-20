# Sources and status audit

## Primary source

Michael Anastos, Zhihan Jin, Matthew Kwan, and Benny Sudakov,
“Extremal, enumerative and probabilistic results on ordered hypergraph
matchings,” *Forum of Mathematics, Sigma* **13** (2025), e55.

- DOI: <https://doi.org/10.1017/fms.2024.144>
- Open manuscript: <https://arxiv.org/abs/2308.12268>
- Cambridge article page:
  <https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/extremal-enumerative-and-probabilistic-results-on-ordered-hypergraph-matchings/AE2E649A98C610BF71EB90375C4758EE>

Theorem 1.18(1) supplies the standard deletion/blocker construction used for
the upper bound here.  Conjecture 1.20 predicts the full ordered extremal
formula.  Theorem 1.17 proves the matching-size-two case, which includes
`m=2` in the present specialization.

## Search-relative status

The literature status was refreshed on 2026-09-20 UTC.  Searches combined
the phrases “ordered hypergraph matching”, “all-forward”, “6m+2”, “rank
six”, the exact deficit 28, the paper title, its DOI, and citations to
arXiv:2308.12268.  The Cambridge journal record and the arXiv manuscript were
the only directly relevant primary results found.  No later paper resolving
the all-forward `r=6`, `N=6m+2`, `m>=3` specialization was found.

This supports only a search-relative novelty statement.  It is not a claim
of exhaustive bibliographic coverage or historical priority.

## Related source in this repository

The occurrence-cover and repair viewpoint also appears in the independently
published lower-rank specializations:

- <https://github.com/helgithorskarp/math_results/tree/main/ordered_pattern_all_forward_r4_boundary>
- <https://github.com/helgithorskarp/math_results/tree/main/ordered_pattern_all_forward_r5_boundary>

The present proof is self-contained: it reconstructs the four rank-six
occurrence types and proves a new four-band paired-repair lemma rather than
importing either lower-rank theorem.
