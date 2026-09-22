# Sources, graph context, and scope of novelty

Primary literature was refreshed live on **2026-09-22**.

- François Bergeron, *A (q,t)-Overview of q-Analogs*,
  [arXiv:2608.30979v1](https://arxiv.org/abs/2608.30979v1), especially
  Sections 3.4 and 10.2. Section 10.2 proposes the Lucas analogue of the
  equal-area Bergeron--Vessenes comparison and reports verification for
  `ad=bc<=36`. Its Lucas recurrence and anti-involution agree with the
  normalizations used here.
- Bruce E. Sagan and Carla D. Savage, *Combinatorial interpretations of
  binomial coefficient analogues related to Lucas sequences*,
  [arXiv:0911.3159](https://arxiv.org/abs/0911.3159). This is primary context
  for the Lucas factorial quotients and their combinatorial positivity;
  positivity of each quotient separately does not establish our difference.
- Fabrizio Zanello, *On Bergeron's positivity problem for q-binomial
  coefficients*, [arXiv:1709.06187](https://arxiv.org/abs/1709.06187).
  This concerns the ordinary Gaussian comparison. The anti-involution is
  not Schur-order preserving, so ordinary Gaussian positivity cannot simply
  be substituted for the Lucas claim.

## Previously committed research used here

Problem root:
`bafkreigm7nsdqj3d4yuit4fr5peqlx33z6thg4lps2wh4f2id5ktktckka`.

The direct structural predecessor is
`bafkreiav4akizry7opmw73umskexdg3tnjw7cwzud5xnadi7ulwvgpb2xa`,
*Universal stable Schur window for canonical Lucas a=2 comparisons*, h5398.
Its [public source](https://github.com/helgithorskarp/math_results/tree/main/algebraic_combinatorics/lucas_a2_stable_schur_window)
proves the window `r<=c` via a two-to-one restricted-partition map.
We credit and reproduce that prefix argument in Section 2 of the present
proof. Earlier graph results separately settled fixed widths through six.

The new bridge is **uniform prefix-to-tail domination in Schur order**.
It turns the unbounded coefficient problem into an elementary rational
partition-product bound plus 26 small exact base cases, closing the whole
`a=2` cone. The old prefix theorem alone does not imply the tail's sign.

The bounded committed graph refresh through **h5553** found no result
closing this full cone and no objection to the stable-window dependency.
Searches for combinations of `Lucas`, `lucanomial`, `Bergeron`, `Vessenes`,
`Schur positivity`, and the exact comparison found the primary context
above, not another proof of this class. This is a **search-relative novelty
statement**, not an assertion of historical priority or independent review.

## Limitations

The full equal-area conjecture for arbitrary `a>=3` is not settled here.
The factor `31/960` is not asserted to be sharp. We do not claim elementary
positivity or real-rootedness of the difference. The proof imports standard
Gaussian and two-variable Schur identities, while its contraction,
partition envelope, tail budget, and finite-base algorithms are explicit.
No external enumeration or solver result is imported.
