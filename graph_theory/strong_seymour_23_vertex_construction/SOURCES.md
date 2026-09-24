# Sources and contribution scope

Graph-first problem: **Minimum Order of a Tournament Without a Strong
Seymour Vertex**, Discovery Net h1440,
`bafkreicoploedp7v3y4u23f2ae3otetmoazhug4hiqy2iurooepslgdnyq`.

1. Yandong Bai, Binlong Li, Boram Park, *Towards a strengthening of the
   second neighborhood conjecture*,
   [arXiv:2607.18047v2](https://arxiv.org/abs/2607.18047)
   (2026-07-24). Definition of strong Seymour vertices; Remark 3.1
   records Dzitsoev's 36-vertex tournament. Version 1 predates that
   counterexample. This work concerns smaller examples, not the first
   refutation of the unrestricted strengthening.

2. Austin Gibbons, [constant-nine construction](https://github.com/AustinBGibbons/ssnc/blob/main/notes/01_constant_nine_construction.md),
   inspected repository commit `cbed58e369cfd868a84010f252671cc3c766c6fd`.
   His quotient `D0` is the starting nine-part tournament. The cyclic
   label map from `(A0,A1,A2,B0,B1,B2,C0,C1,C2)` to his labels is
   `(6,4,5,0,2,8,7,1,3)`, checked in the preceding package. The present
   13-part quotient changes five arcs after deleting and splitting parts;
   it is not a mere new weighting of the unchanged `D0`.

3. [Preceding 24-vertex construction](https://github.com/helgithorskarp/math_results/tree/main/graph_theory/strong_seymour_24_vertex_construction),
   source commit `68ef11fa9db8888960b769f4647e845f740847ea`, Discovery Net
   h5871, `bafkreigv26yzaxbdb3dinxo2repcikf47w2vlfan3yi2vjacogibejlpqe`.
   Its cyclic weighting `(1,2,5)` supplies the new search seed and the
   explicit surgery interpretation. Its three-parameter and selected-row
   minima are 24. Those minima remain valid for their stated classes.

4. [Exact quotient-weight Hall and cut compression](https://github.com/njallskarp/math_source_code_open/tree/main/strong_seymour_hall_compression),
   Discovery Net h2093,
   `bafkreidtb5vbrtchsfpojtvpgyyiqfoifmgsdqelg6ua5scxpqgmwuqs7i`.
   Prior Hall closure and weighted quotient mechanism. The elementary
   proof needed here is repeated in PROOF.md. Hall obstruction,
   tournament substitution, and closure are not claimed as new methods.

5. [Every tournament of order at most 15 has a strong Seymour vertex](https://github.com/helgithorskarp/math_results/tree/main/graph_theory/strong_seymour_order15_complete),
   Discovery Net h5194,
   `bafkreihvquktzhgyzkw56zsrbiontqntiojahwfqio6ggtghve7r3iqwcm`;
   independent acceptance h5200,
   `bafkreie2rlybzjcuaav3l5f7yab2kia4beta2ak6a6rgsbhinwdxwtemzm`.
   This supplies the imported lower bound `m≥16`, not required to verify
   the new upper bound and not re-proved in this package.

The contribution is the explicit 23-vertex tournament, its 13-part family,
the exact three-parameter chamber, and the selected-certificate minimum.
The graph and targeted primary-literature searches on 2026-09-24 found
no prior 23-vertex example in the searched sources. This is a bounded
novelty check, not a historical-priority claim. None of the new work has
independent reviewer acceptance at source preparation.

Discovery used single-arc heuristic changes of vertex deletions of the
new order-24 construction. A 23-vertex witness was found with PRNG seed
150023 after 2,850,006 moves. Modular compression gave the 13-part
quotient; exact Hall analysis then gave the parameter rule. The published
constructor, proof, and checks reproduce the mathematical result without
replaying the search or depending on its floating-point acceptance rule.
Bounded attempts at order 22 and solver infeasibility reports are not
used to claim a lower bound or an exhaustive quotient classification.
