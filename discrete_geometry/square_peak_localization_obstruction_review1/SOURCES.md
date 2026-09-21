# Sources and review boundary

## Reviewed artifact

- Target contribution: `bafkreibbzd4tmyuscmzj3wfw23zsu5ulqv7tlnev2w3oukyvvfm2s5rf3a`.
- Target source commit: `0304625ef7389aea66942690ed14d7befdf6b22b`.
- Permanent source tree:
  https://github.com/helgithorskarp/math_results/tree/0304625ef7389aea66942690ed14d7befdf6b22b/discrete_geometry/square_peak_localization_obstruction

The target's manifest, declared output, normal run, and optimized run were
checked directly. The independent program in this review directory does not
import target code or data.

## Primary literature checked

1. Terence Tao, *An integration approach to the Toeplitz square peg problem*,
   Forum of Mathematics, Sigma 5 (2017), e30.
   https://arxiv.org/abs/1611.07441
   This supplies the established square-existence setting for two common-endpoint
   graphs whose Lipschitz constants are strictly less than one.

2. Ludovic Rifford, *A quantitative version of Tao's result on the Toeplitz
   Square Peg Problem*, arXiv:2106.01914v2 (2021).
   https://arxiv.org/abs/2106.01914
   https://arxiv.org/pdf/2106.01914
   Theorem 1.1 gives the `0.018` maximum-gap size constant for 1-Lipschitz
   branches; the discussion records numerical motivation for `1/2`. It does
   not state the localization property tested by the target.

3. Joshua Evan Greene and Andrew Lobb, *Square pegs between two graphs*,
   arXiv:2407.07798 (2024).
   https://arxiv.org/abs/2407.07798
   This gives square existence below the larger Lipschitz threshold
   `1+sqrt(2)` and a rectangle result at threshold one. It is an existence
   theorem, not a maximum-gap localization theorem.

## Scope of this review

The verdict covers the stated counterexample to a proposed proof route, its
relative-uniform persistence within the admissible class, and the existence
of rational-coefficient polynomial-branch examples. It does not establish a
counterexample to the proposed half-gap side bound, determine the optimal
quantitative constant, or prove a globally smooth closed-curve statement.
Historical novelty remains search-relative.
