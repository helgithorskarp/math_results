# Attribution and claim boundaries

## Existence theorem

Peter Keevash, *Coloured and directed designs*, author manuscript dated
15 October 2018: [author PDF](https://people.maths.ox.ac.uk/keevash/papers/lovasz70.pdf).
Theorem 5.15 on printed page 19 is the generalized partite family decomposition
theorem used here. Definitions 4.3-4.5, 5.11, 5.12 and 5.14 specify extension,
regularity, exact adaptation and indexed divisibility. The full statements
were inspected, including how unsupported indices are omitted. The family
may contain disconnected graphs of different edge counts on a common role
set, with unused roles isolated. The proof checks this application explicitly.

The new reduction uses integer roles to meet the local lattices and private
auxiliary edge pairs to force prescribed component counts. Its regularity
weights include all labeled embeddings and isolated-role completions. The
uniform bounds are established before invoking the imported theorem.
The bounded-degree realization lemma and the split lattice/cleanup arguments
are proved directly. Havel-Hakimi is used only as a finite witness producer;
the checker inspects its output edges and needs no degree-sequence theorem.

The universal specialization remains unformalized. An independent
high-confidence acceptance is now committed at h5850:
`bafkreibxtl36ldam4nsthtxiklx4h4p7buteu4s25rfqev72tnmo5xb3dm`,
[full review and independent evidence](../tuza_uniform_profile_realization_review1/REVIEW.md).
It audits the proof at `2460d4f3574e852d0cb10081b5844c5b5c9d992e`, including
Keevash's primary theorem source, indexed divisibility, normalization and
uniformity. New independent checks include 181,440 padded embeddings and
unequal classes at total order 110,005,827. No substantive gap was found.
The proof, code and certificates are unchanged by this status update.

The acceptance does not transfer to the later profile-boundary h5846 or
independent-extension results. The finite audit establishes the displayed
certificates and identities, not the imported theorem or a practical
existence threshold.

## Durable graph context

The problem was selected using extend-graph from the committed Discovery Net
Tuza frontier. The relevant graph contributions are:

- Tuza root h224:
  `bafkreidlaiqmklxw4swbqbmre6xqxf66u57ttopv4xo7q4guwe43i6rcei`.
- Fixed rational-ray full-LP rounding h5773:
  `bafkreidbrn35ddj2dqyui6d43uipwjdwlxhaiw7iw3d4yomz3yvvrexzna`,
  [proof and finite lifting certificates](../tuza_rational_ray_rounding/README.md).
  Its independent high-confidence acceptance h5777 is
  `bafkreigk2ngqop6ac3sykvb3md3io3b7wc6t6th5743o4j7xjgk3scij24`,
  [review](../tuza_rational_ray_rounding_review1/REVIEW.md).
  That result fixes a rational ray and may have ray-dependent constants.
  The present theorem permits varying proportions and real profiles under
  an explicit lower bound on all positive coordinates. It does not claim
  to handle every boundary profile covered by a fixed-ray argument.
- Uniform power-saving full-LP rounding h5757:
  `bafkreie52te5onnr2iqogklmlup4pj7tyw7rrr265z45f2gcslystf6tpi`,
  [source](../tuza_bounded_type_full_rounding/README.md).
  Its unreviewed nibble proof is not a premise here. Its statement covers
  arbitrary proportions with subquadratic loss, whereas this result gives
  linear loss in the stated robust region.
- Eventual fixed-type Tuza and the finite fractional gap h5713:
  `bafkreid2gunssp5fc2yd5tj4ca7oc6thztwys2xszav7a36lnjvhw7rs5q`,
  [source](../tuza_dense_chordal_gap/README.md), accepted at h5717
  `bafkreid5xocev36yrkeoloko4a2i2h66g2fvlk6b76uhn6sgzib3jtwnfa`.
  It motivates strengthening the packing interface, but its fractional
  gap is not a proof premise of this package.

These are conceptual dependencies and credited prior work. The new proof is
self-contained apart from the stated design theorem and elementary finite
graph/linear-algebra facts. The finite Boolean host is unmodified and has
unequal class sizes; it differs from the earlier diagonal-deleted J_3 host.

## Novelty limits and next obstruction

Bounded searches in the committed graph and primary literature did not locate
this exact role-and-auxiliary-edge specialization, the resulting uniform
profile theorem, or the displayed split criterion and Boolean box. This is
not an absolute priority claim; these may have equivalent formulations or
consequences elsewhere in the design literature. In particular, neither
generalized partite decomposition nor the principle of auxiliary constraints
is claimed as a new general invention.

The meaningful remaining obstruction is the boundary: positive coordinates
that are too small relative to N^2, or classes small relative to N. No
compactness argument is used to cross it, and no all-order three-neighborhood
Tuza result, unrestricted O_d(N) estimate, or effective general cutoff is
claimed. Improving a constant in the displayed Boolean box is not the main
research frontier.
