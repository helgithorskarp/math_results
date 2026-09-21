# Sources and provenance

## Reviewed contribution

- Discovery Net CID:
  `bafkreiekhohfsjaoa7casagc6tjdtwtwiy7zzzklpqaiizgpvqnl76do2e`
- Reviewed source at fixed commit:
  [quadratic_universal_dimension_criterion](https://github.com/helgithorskarp/math_results/tree/fb65742ca2280c6da86b04b37bf121d38bb1f0e5/discrete_geometry/quadratic_universal_dimension_criterion)
- Reviewed proof:
  [PROOF.md](https://github.com/helgithorskarp/math_results/blob/fb65742ca2280c6da86b04b37bf121d38bb1f0e5/discrete_geometry/quadratic_universal_dimension_criterion/PROOF.md)

## Primary literature checked

- Kevin Ren and Hong Wang, *Furstenberg sets estimate in the plane*,
  [arXiv:2308.08819v3](https://arxiv.org/html/2308.08819v3), Theorem 1.2.
  This is the deep external input and states exactly the exceptional
  orthogonal-projection bound used in the proof.
- Minh-Quy Pham, *On Falconer type functions and the distance set problem*,
  [arXiv:2510.15118v2](https://arxiv.org/html/2510.15118v2), Theorem 1.4(ii).
  Its displayed compact-product statement motivates the universal-quantifier
  audit; the surrounding text identifies the intended quadratic setting.
- Minh-Quy Pham, *On Hausdorff dimensions of k-point configuration sets and
  Elekes--Rónyai type theorems*,
  [arXiv:2603.03567v1](https://arxiv.org/html/2603.03567), Theorem 1.8 and
  Remark 1.10(i).  This later source requires positive factor dimensions and
  records the `x(y+z)` singleton obstruction.
- Nuno Arala and Sam Chow, *Expansion properties of polynomials over finite
  fields*, [arXiv:2403.03732v1](https://arxiv.org/html/2403.03732),
  Definition 1.1 and Lemma 1.5.  It supplies prior context for the
  coefficient-map rank alternative; the target rederives the needed real
  algebra.

Current version metadata was checked through the official
[arXiv API](https://export.arxiv.org/api/query?id_list=2308.08819,2510.15118,2603.03567,2403.03732).

## Literature-search boundary

The arXiv API was queried for combinations of “quadratic,” “coordinate
line,” “universal quadratic image,” and “Hausdorff dimension.”  No identical
primary coefficient criterion was returned.  This bounded search supports
only the target's search-relative novelty statement and does not establish
historical priority.
