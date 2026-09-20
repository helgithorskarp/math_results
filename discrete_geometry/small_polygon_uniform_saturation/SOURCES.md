# Sources, dependencies and scope

Checked 2026-09-20.

1. Christian Bingane, *Tight bounds on the maximal perimeter and the
   maximal width of convex small polygons*, Journal of Global Optimization
   84 (2022), 1033--1051,
   [journal](https://link.springer.com/article/10.1007/s10898-022-01181-9),
   [author preprint, Theorem 1](https://arxiv.org/html/2010.02490v3).
   This is the specialized external dependency for our corollary: it
   supplies the convex small polygon B_n and its exact perimeter for every
   power of two n>=8. We use its explicit formula, not a numerical table
   or an asymptotic remainder with an unspecified constant.

2. Bernd Mulansky and Andreas Potschka, *A zonogon approach for computing
   small convex polygons of maximum perimeter*, Mathematical Programming
   218 (2026), 563--589, first published 21 June 2025,
   [published article](https://link.springer.com/article/10.1007/s10107-025-02244-x).
   This provides the optimization context and sign-code formulation.
   Their Conjecture 1 concerns vertices of a containing Reuleaux polygon;
   we assert the explicit difference-body saturation and optimization
   reduction proved here, without an additional claim about every possible
   containing Reuleaux polygon.

3. Jizhou Guo and Yitao Luo, *Reinhardt's Maximum-Perimeter Polygon Problem
   for n=16,32,64*,
   [arXiv:2608.08001v2](https://arxiv.org/html/2608.08001v2),
   [version history](https://arxiv.org/abs/2608.08001).
   Version 2, posted 25 August 2026, claims computer-assisted proofs at
   these three orders. Version 1 used the title "Computer-Assisted Proof
   Candidates"; quoting that as the latest title would be outdated.
   Proposition 4.1 and the appendices contain the fixed-order saturation
   mechanism. Reconstruction, two-interior perturbation and normal-cone
   localization are prior ideas, not attributed to this contribution.
   We give the direct all-order estimate and feasible-curve argument in
   full; their finite enumeration and uniqueness certificates are not
   dependencies of our theorem.

## Discovery Net provenance

The graph-first selection follows the committed problem
`bafkreic5izcv6cik5vlbv2mrnvvuqlh6yme5kw4bq3q7sjufmlury7xrmq` and these
existing geometric results:

- Fixed n=16 reconstruction and saturation bridge:
  `bafkreidowzobkppsnue7oxcxvbklfv3pnkgmjlwkddtynth4jsxucivnku`.
- Independent review with the parametric strict-edge criterion:
  `bafkreiexgrzszw4wquhvibx4xfmidrvvuer27qubxmadjhl562rlyvnu2e`.

Their incoming reviews and dependencies were inspected. We reprove the
needed geometry, including the full-or-drop-two direction count, rather
than importing the entire n=16 computer-assisted proof.

The explicit uniform local criterion and the all-powers n>=32 consequence
were not located in the bounded graph and primary-literature search.
This supports only novelty relative to searched sources, not exclusive
priority. The new statement is a structural reduction, and gives no new
maximum perimeter value or uniqueness result. The published/preprint
n=16,32,64 optimality claims are neither re-audited nor claimed as new.
