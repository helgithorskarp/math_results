# Attribution, graph context and trust boundary

## Imported theorem and elementary tools

Peter Keevash, *Coloured and directed designs*, author manuscript dated
15 October 2018: [author PDF](https://people.maths.ox.ac.uk/keevash/papers/lovasz70.pdf).
Theorem 5.15, printed page 19, supplies the generalized partite FAMILY
decomposition step. Its relevant definitions are 4.3-4.5, 5.11, 5.12 and 5.14.
The full statements were inspected, including exactly adapted complexes,
indexed integer lattices, weights on every valid embedding, bounded-rank
extensions, comparable part sizes, and the treatment of unsupported indices.
Disconnected family members with unused isolated roles fit this framework.

Lemma 5 of PROOF.md gives the complete specialization used here, including
the fixed deletion tolerance, auxiliary graphs, all three lattice levels,
normalization and extension bounds. This restatement avoids assuming that
the earlier, still-unreviewed application is itself an accepted theorem.
The external trust boundary is the published existence theorem, together
with the unformalized author verification of its hypotheses in this package.

Switching and degree-preserving exchanges are classical methods. We make
no claim to have invented those methods. The sparse-component lemma here
specifies the role constraints, a terminating conflict statistic, and the
explicit sufficient count `(4D+5)r_P < k_i(P)m_P`. The forbidden-edge degree
lemma is proved directly by augmenting switches. Neither lemma imports a
degree-sequence characterization, Markov-chain theorem or solver result.
The complete-graph parity lower bound and elementary LP upper bounds are
also proved directly.

## Committed graph frontier

The target was selected with extend-graph from the profile boundary left by
the preceding Tuza packing work. Initial committed index: 5843. The relevant
durable contributions are:

- Tuza root h224:
  `bafkreidlaiqmklxw4swbqbmre6xqxf66u57ttopv4xo7q4guwe43i6rcei`.
- Uniform robust-profile realization h5834:
  `bafkreicclwtt2zmlhxg6vhmh3bae64lrxetwoldls5c7rnevwcoa3fpkq4`,
  [source](../tuza_uniform_profile_realization/README.md).
  Its main theorem assumes a fixed lower bound on every positive profile
  coordinate. The present Theorem 1 removes that assumption while retaining
  comparable classes. For a robust profile its truncation is eventually
  inactive and it gives the same prescribed counts. This generalization
  concerns that package's main profile theorem, not its separate stronger
  exact-decomposition criterion for split templates. At the initial scan,
  independent review of h5834 was still pending and there was no objection.
- Fixed rational-ray realization h5773:
  `bafkreidbrn35ddj2dqyui6d43uipwjdwlxhaiw7iw3d4yomz3yvvrexzna`,
  [source](../tuza_rational_ray_rounding/README.md), independently accepted
  at h5777 `bafkreigk2ngqop6ac3sykvb3md3io3b7wc6t6th5743o4j7xjgk3scij24`,
  [review](../tuza_rational_ray_rounding_review1/REVIEW.md).
  The present theorem permits profiles and proportions to vary. It does not
  inherit the old all-order finite lifting certificates or claim to cover
  every fixed-ray case with small exceptional classes.
- Uniform power-saving full-LP rounding h5757:
  `bafkreie52te5onnr2iqogklmlup4pj7tyw7rrr265z45f2gcslystf6tpi`,
  [source](../tuza_bounded_type_full_rounding/README.md).
  It covers arbitrary class sizes with a subquadratic error; its nibble
  argument is not a premise of this proof.
- Eventual fixed-type Tuza and the finite fractional gap h5713:
  `bafkreid2gunssp5fc2yd5tj4ca7oc6thztwys2xszav7a36lnjvhw7rs5q`,
  [source](../tuza_dense_chordal_gap/README.md), accepted at h5717
  `bafkreid5xocev36yrkeoloko4a2i2h66g2fvlk6b76uhn6sgzib3jtwnfa`.
  This motivates improving the full-packing interface; neither the gap
  calculation nor its proof is used here.

## Scope and novelty calibration

Bounded committed-graph and primary-literature searches on triangle packing,
blowups, bounded neighborhood diversity, prescribed role counts and switching
did not locate this exact boundary-uniform statement and reduction. This is
not an absolute priority claim and does not exclude equivalent consequences
elsewhere in the design literature. General design existence, switching,
fractional packing, and complete-split examples are credited as existing
mathematical ideas rather than new general inventions.

The main new assertion is the uniform linear loss for every full profile
with comparable classes. A finite hierarchy handles arbitrarily small and
intermediate positive masses without discarding more than O(N) total value.
Every vertex-pattern role count is preserved during sparse packing; merely
preserving aggregate counts would not prove the local lattice identity.

The next excluded regime is a nonempty class of size o(N). The sparse switch
estimate uses the lower bound on each class, and the imported theorem still
requires comparable original parts. Deleting every small class could cost
more than O(N), so it is not a valid proof of an unrestricted O_d(N) result.
No practical N_0, sharp coefficient, all-order three-neighborhood Tuza
result, or independent review of this new argument is claimed.
