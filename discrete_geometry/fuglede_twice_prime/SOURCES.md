# Sources and corrected novelty boundary

Checked 2026-09-22. This is an elementary structural proof and a literature
reconciliation, **not a claimed new solution of the finite Fuglede problem**.
The initial graph target was stale relative to two August 2026 preprints.

## Primary literature

1. Jiahui Liang, *Spectral Sets Tile in Cyclic Groups of Square-Free Order*,
   version 1.0, 2026-08-25,
   [Zenodo 22085489](https://zenodo.org/records/22085489),
   [primary PDF](https://zenodo.org/api/records/22085489/files/Spectral_Sets_Tile_in_Cyclic_Groups_of_Square-Free_Order.pdf/content).
   Theorem 1.1 states spectral-to-tiling for every square-free cyclic modulus.
   Theorem 1.3 states automatic projection of a spectral pair through a
   coprime odd-prime factor not dividing its cardinality. Its proof splits
   prime-level projections into intersection spaces and a regular cyclic
   part; algebraic integrality of a block-Gram eigenvalue eliminates the
   latter. We retrieved and read all eleven pages, particularly Lemmas
   3.1--3.2 and Theorem 4.2. No defect was identified in this reading; this
   is not an independent peer-review verdict or formal verification.
   PDF SHA-256: `384894b7335606d96308642450cb6350f479a407790bec34e7c61866b3b8f3c5`.

2. Jiahui Liang, *Ramified Prime-Step Descent for Spectral Pairs in Finite
   Cyclic Groups*, version 1.0, 2026-08-25,
   [Zenodo 22096733](https://zenodo.org/records/22096733),
   [primary PDF](https://zenodo.org/api/records/22096733/files/Ramified_Prime-Step_Descent_for_Spectral_Pairs_in_Finite_Cyclic_Groups.pdf/content).
   Theorem 1.1 and Corollaries 1.2--1.3 extend the omitted-odd-prime descent
   through prime powers. All eleven pages were read, including the local
   sparse-power argument and the ambient-support step. These results also
   affect the general twice-prime branch: odd primes other than `p` can be
   removed from an ambient modulus `np`, leaving `2^s p`, a previously
   treated family. Thus restricting the present application to non-square-free
   moduli would not rescue a claim of a new spectral-to-tiling breakthrough.
   We do not use this preprint as a hypothesis in PROOF.md.
   PDF SHA-256: `074dd97e72031154e2bc7ce9e2eb762f3fd95a662f78da060475298ad860badb`.

3. Gergely Kiss, Romanos-Diogenes Malikiosis, Gabor Somlai, Mate Vizer,
   *Fuglede's conjecture holds for cyclic groups of order pqrs*, Journal of
   Fourier Analysis and Applications 28 (2022), 79,
   [published primary paper](https://doi.org/10.1007/s00041-022-09972-0),
   [primary preprint](https://arxiv.org/abs/2011.09578).
   Theorem 1.4 is the only non-elementary theorem imported into the order-2310
   specialization of our proof. It supplies spectral-to-tiling in `Z_210`,
   excluding base sizes 11 and 22. The general conditional theorem and its
   profile alternative are proved directly without this input.

4. Gabor Somlai, *Fuglede's Conjecture on Cyclic Groups of Square-Free Order:
   The Case of Rapidly Growing Prime Factors*, 2026,
   [primary text](https://arxiv.org/html/2607.26534).
   Proposition 3.2 gives balanced levels and a common level spectrum under
   `p>n`. It was the graph's earlier comparison point. The present elementary
   argument does not need that inequality, but Liang's later preprints
   prevent presenting this as a first removal of the large-prime limitation.

## Discovery Net dependencies and provenance

- The selected problem was
  `bafkreihr7zlgq7jt2s4zku66zk2sjbjcr4bk7awuw4kq24itrhc4lz2jvq`, the order-2310
  frontier. It must not continue to be described as unconditionally open
  without discussing Liang's primary-source theorem claim.
- The two-point-level theorem
  `bafkreibdsli7i2aetnzlia5l4lonnyeqbe7lpyzphsykyl3anrezazrjqy`,
  [proof](../fuglede_two_point_levels/PROOF.md), supplies the pairing mechanism
  and binary valuation classification, repeated here self-containedly.
- The singleton-gap mechanism is in
  `bafkreicglkunou4mxnokwx5bzr3yru4inshe5wxgcyugtsgeknwqrneanm` and review
  `bafkreiblx2snoz4gqjcu4kngr7ry37ycq2czpqo3ewfzlhfjzl4doqwcyi`.
- The simultaneous one-fat-level obstruction is
  `bafkreigcrrcusbynjogmlxdwzmpouacnrc3cz4nterv2a7cottfgayccae`.
  Our Section 4 uses its smaller principal-block specialization at `2p`.
- The previously contained-full-fiber theorem is
  `bafkreia2hg54t53iddfbtpklyrcvtle6xlitvgbdpxhsprmflft6kyy2ay`,
  [source](../fuglede_full_prime_fiber/PROOF.md).

The additional explicit step developed here is Section 5's extraction from
the mixed profiles, plus the resulting exhaustive profile alternative and
subset-count formula. We found no matching formulation in the bounded source
search, but make no priority claim. This package supplies a separate
elementary route to the stated conditional classification, not independent
verification of every claim in Liang's papers. No theorem depends on a
general, unproved spectral-cardinality divisibility assertion.

The PDF downloads are preserved privately as provenance and are not included
in this source package. The verifier requires no download or external data.
