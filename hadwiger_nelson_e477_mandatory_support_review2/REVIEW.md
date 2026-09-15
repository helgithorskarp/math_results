# Review verdict

## Target

The unpublished target checker claimed:

- 477 distinct E477 points and 2,458 complete unit edges;
- 253 valid deletion colourings separating the marked terminals;
- a 255-point mandatory core with 659 complete unit edges;
- a proper unequal-terminal four-colouring of that core;
- hence forcing-half order at least 256 and sole-bridge non-four order at
  least 511.

Its reported script SHA-256 is
`9a9a957d9bcf2fada8e8bd0247846f6b0316f58ae36c990a1c0fe5749993fe65`
and result SHA-256 is
`065ccebfb569d7c179dbd5c42c853fedfa5c23d7524246f74cf3f40d53eb75e4`.

## Verdict

**Accept and strengthen.**  Normal and optimized replay of the target were
byte-identical to its reported result.  The source census, all 253 deletion
words, the mandatory-core census, and its positive four-colouring are valid.
The mandatory-set inference and the `2m-1` sole-cross-edge inference are
sound under the already certified geometry.

An independent radical-field reconstruction and a new positive-colouring
bank strengthen `m>=256` to `m>=258`.  All 222 singleton and 24,531 pair
extensions of the mandatory core are explicitly covered.  The consequent
family floor is therefore 515, not merely 511.

## Limitations

- The 515 bound is restricted to subgraphs of fixed E477 in the previously
  classified one-overlap, sole-cross-edge two-half frames.
- It is not global Hadwiger--Nelson progress and produces no sub-509 graph.
- It does not assert sharpness, a 258-point forcing half, or a 515-point
  five-chromatic realization.
- Placements with extra cross contacts, different source graphs, and larger
  assemblies remain outside scope.
- E477's equality-forcing property and the 16-frame physical geometry are
  imported from, and freshly replayed against, the prior independent review.
