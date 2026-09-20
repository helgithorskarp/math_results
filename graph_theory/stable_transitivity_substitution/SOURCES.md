# Sources and status audit

Status was checked at the opening of this research pass on 2026-09-20, before
technical development.

## Primary literature

1. Matthew Davis and Michael W. Schroeder,
   [*Relating tournaments and permutations with xrays*](https://arxiv.org/abs/2606.21532v1),
   arXiv:2606.21532v1 (2026).

   This paper introduces transitive tournament decompositions, stable
   transitivity, `m(T)`, and `m(n,k)`.  The arXiv history still lists only v1,
   submitted 2026-06-19.  Inspection of the current source and targeted text
   searches found no substitution law, ordinal-sum formula, or reduction to
   strong components.

2. Leonid Chindelevitch and Ararat Harutyunyan,
   [*Tournaments determined by three and five voters*](https://arxiv.org/abs/2607.26690v1),
   arXiv:2607.26690v1 (2026).

   This related paper supplies the `G8` predictability obstruction underlying
   the later stable-transitivity computations.  The arXiv history still lists
   only v1, submitted 2026-07-29.  It does not state the stable-transitivity
   substitution or strong-component formulas proved here.

Targeted searches for stable transitivity together with "substitution",
"ordinal sum", and "strong components" found no later primary source
settling this result.  The novelty language in this directory is deliberately
search-relative.

## Reproducible prior results used only for consequences

- [`../stable_tournaments_order8`](../stable_tournaments_order8), source
  commit `cb65c26f6df858a58f1912b1ccfc49adba83ac6f`, proves `m(8,1)=2` and
  gives 96 exact obstruction classes.  That result was independently accepted
  in Discovery Net.
- [`../stable_transitivity_g8_all_mixtures`](../stable_transitivity_g8_all_mixtures),
  source commit `486e4961bcb5a01feb7111407bdf929bc199028e`, proves
  `m(W)=ceil(7k/6)` for every degree-`k` extension of `G8`.  At the time of
  this contribution the corresponding Discovery Net result had not yet
  received an independent review, so the all-degree infinite-family
  consequence is stated with that dependency explicit.

Neither computation is used in the proof of the substitution theorem or the
strong-component localization formula.
