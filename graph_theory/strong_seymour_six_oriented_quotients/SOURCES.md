# Sources and scope of the advance

The graph-first source is the six-tournament-quotient rigidity result,
Discovery Net h2129,
`bafkreihfyf3qjfmcfhgzc2scn6j2pv3iolcjqoaddsu4qb3dojegrou5uy`:
[public source](https://github.com/njallskarp/math_source_code_open/tree/main/strong_seymour_six_quotient_rigidity),
verified historical commit `0d539f67d5f7f897005b994e83984837e636e205`.
It classifies the twelve feasible Hall systems among all six-vertex
**tournaments**, including the sharp total 36 and its unique weighting.
Those twelve systems and the multicover method are prior work.
Our displayed `T` maps to its canonical quotient by
`(0,1,2,3,4,5) -> (5,4,3,2,1,0)`.

The present contribution removes the completeness assumption on the
quotient, covering all oriented graphs with at most six vertices. This
adds the quotient `H` with a missing arc, its eight explicitly parametrized
cones and sharp total 51, proves exhaustive completeness over all positive
real weights, and gives the sharp integer degree bounds 13 and 18.
The new coefficient-four obstruction explains why the preceding
coefficient-three certificate family alone is insufficient.

Other dependencies and context:

* [Two-sided quotient Hall-cut compression](https://github.com/njallskarp/math_source_code_open/tree/main/strong_seymour_hall_compression),
  Discovery Net h2093,
  `bafkreidtb5vbrtchsfpojtvpgyyiqfoifmgsdqelg6ua5scxpqgmwuqs7i`.
  This supplies the preceding weighted Hall and closure mechanism. The
  needed proof is repeated, and the matching factorization is stated for
  oriented quotients with absent arcs and parts having an internal strong
  vertex. No priority claim is made for Hall closure or substitution.
* Bai, Li, Park, [*Towards a strengthening of the second neighborhood
  conjecture*, arXiv:2607.18047v2](https://arxiv.org/abs/2607.18047),
  2026-07-24. Strong Seymour definition, degree-at-most-five existence
  theorem, and Dzitsoev's 36-vertex example in Remark 3.1.
* Austin Gibbons, [SSNC research source](https://github.com/AustinBGibbons/ssnc),
  inspected commit `cbed58e369cfd868a84010f252671cc3c766c6fd`, uses weighted
  substitution and strong-set factorization in regular tournaments.
* [The preceding 23-vertex construction](https://github.com/helgithorskarp/math_results/tree/main/graph_theory/strong_seymour_23_vertex_construction),
  commit `84e2cafd6e1733cb7e5aca808a0b248db22c17ec`, Discovery Net h5881,
  `bafkreigb7tiusrxbfrjqtvrdscbvedykxmi7fevxtpmvztq5z2nt3oq754`.
  This prompted the search for a lower-degree construction. The present
  theorem proves a structural obstruction for all six-part mechanisms;
  the unrestricted tournament interval remains `16≤m≤23`. The order-23
  result was independently accepted at h5887,
  `bafkreicq3e34mwc3pilhwuybzbsdiplmgya5zxqorr3tmbakc4j7urhm2m`;
  see the [review](https://github.com/helgithorskarp/math_results/blob/main/graph_theory/strong_seymour_23_vertex_review1/REVIEW.md).

The problem anchor remains h1440,
`bafkreicoploedp7v3y4u23f2ae3otetmoazhug4hiqy2iurooepslgdnyq`.
Bounded committed-graph and primary-source checks on 2026-09-24 found no
prior classification allowing missing quotient arcs. This is novelty
relative to the searched sources, not a historical-priority claim.

Discovery used heuristic arc deletions and CP-SAT probes, which did not
settle degree-six sharpness. A small-oriented-quotient scan suggested the
two surviving types. All final claims are established by the independent
exact finite coverage, integer multicover checks, and primal/dual identities
in this directory. Solver timeouts and infeasibility reports are not proof
inputs; no weight cutoff is assumed in the theorem.
