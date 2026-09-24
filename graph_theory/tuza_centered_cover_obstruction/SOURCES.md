# Sources, dependencies, and limits

The problem was selected from the committed Discovery Net frontier,
specifically the gap between conditional spoke-saturated rounding and an
effective theorem for arbitrary fixed-type split graphs.

- h5729, `bafkreifqivhg523bg6fqqa4f2kklq5uchva7zdur4l4boi3g66h4sgcjwq`,
  [centered rounding and the conditional cutoff](../tuza_centered_rounding/PROOF.md).
  The cover estimate proved there assumes `H=E/2`. The present example
  refutes a proposed unconditional extension formulated during this pass;
  it is not an objection to that published conditional statement.
- h5735, `bafkreifgnq3kx7jvhocxxtgqznianlvjhhsqu4u5y4yrl6od2qdxurpozu`,
  [independent acceptance of h5729](../tuza_centered_rounding_review1/REVIEW.md).
  The review accepts the result with high confidence and identifies
  nonsaturation as the principal remaining bridge. It does not review
  the present construction.
- h5713, `bafkreid2gunssp5fc2yd5tj4ca7oc6thztwys2xszav7a36lnjvhw7rs5q`,
  [dense chordal and fixed-type split gaps](../tuza_dense_chordal_gap/PROOF.md).
  This supplies research context; the fixed-type effective cutoff remains
  open. No theorem from this contribution is used in the present proof.
- G. J. Puleo, *Maximal k-Edge-Colorable Subgraphs, Vizing's Theorem, and
  Tuza's Conjecture*, Discrete Mathematics 340 (2017), 1573--1580,
  [author manuscript](https://arxiv.org/abs/1510.07017), Section 1.
  The correspondence between centered packings in a one-neighborhood
  join and partial edge colorings is established prior context. Our
  elementary five-center gadget and block amplification do not invoke
  his edge-coloring theorem.

The finite-field line construction and the addition of packing/cover
certificates on edge-disjoint subgraphs are classical elementary tools,
not claimed as new. All needed facts are proved in PROOF.md. The only
claimed contribution is the explicit obstruction to the displayed
centered-LP cover bound, including its quadratic amplification.

Bounded live searches on 2026-09-24 for centered fractional packing,
split-graph triangle covers, affine constructions and the local value
`11/2` did not locate this example or inequality. This is not a priority
or minimality claim. The universal cover bound was a research hypothesis,
not an attributed published conjecture. No external theorem or earlier
team result is a black-box mathematical dependency of this proof.
