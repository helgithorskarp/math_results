# Sources and exact scope

## Mathematical dependencies

The target is Team A researcher 2's complete author proof in
[decision71](../decision71/README.md), initially published at commit
`c358411e750e0cea4dfee77fd7cb13d4d3f7560b`, with documentation clarified at
`0df9ef5a2a1146f48283531290fac6c8c2a1459f`.
The final refresh additionally inspected the preservation supplement at
`134274bb6197b14e4a72480f77189f69e81f1f95` and its [corpus guide](../decision71/CORPUS.md).
It supplies a read-only replay procedure and preserves the original
manifest. It does not assert independent acceptance; its newly added
recheck modules are not imported or assumed by our verifier. The supplement is
`bafkreicqujmxizbnztcjgpimadvn6667hdhftmu2zjyscfssfhaqt4onkm`, height 6084.
Discovery Net reference:
`bafkreic22u2qpq62lbr7vkt743ec37j4gygbnnufblyklm63o7rntyttja`, height 6076.

Our [prior geometric review](../decision71_geometry_audit/REVIEW.md)
accepts the complete finite reduction. Its source snapshot is
`0bd139b2d32f58fcb080b6f90aa42387931d54b6`; its published review commit is
`cd4147d93de941bb2c530c6d055fc7785473cf9a`. Graph reference:
`bafkreiabb3r7ohuclztekpx3tacvwujccityeermnvnaeldrtyzccowube`, height 6064.
Its review included a full replay of the two complete quotient enumerators
and the complete 12,000-map affine audit, but independently compared only
twenty exported formulas and checked no global UNSAT trace. This work
extends those last software checks without repeating the enumerations.

The preferred geometric proof uses researcher 3's
[two-low-plane theorem](../low_pair71/THEOREM.md), graph
`bafkreidy3j3g3qeasqbqxpnzayye526ojhqmes2mvj57glffihpdlf2m3i`, height 5996,
with its [independent review](../low_pair71_review1/README.md), graph
`bafkreibvd76t2o6klwh7lkxwlshvaty2aoyjdpam6ryonzuvdetzretyea`, height 6050.
The fifteen types it supplies lie in the fixed twenty-type proof family.
The earlier 72-point exclusion, affine-symmetry restrictions, local
marginal obstructions, quadratic and cubic moment exclusions, and the
two-six-plane classification are not additional assumptions here.

## Literature and lower bound

Christian Elsholtz, Jakob Führer, Erik Füredi, Benedek Kovács, Péter Pál
Pach, Dániel Gábor Simon, and Nóra Velich,
[*Maximal line-free sets in F_p^n*](https://arxiv.org/abs/2310.03382v2),
Periodica Mathematica Hungarica 90 (2025), 7–21,
[publisher version](https://doi.org/10.1007/s10998-024-00617-x).
This is the source of the 70-point lower bound. The point list in
[known70.json](../known70.json) is checked directly; the review does not
infer line-freeness from its attribution.

A bounded primary-source refresh on 26 September 2026 recovered the
published bounds 70 through 73 and no external exact determination in
the inspected results. This review makes no historical-priority claim.
Its contribution is independent evidence for the team's finite reduction
and certificate boundary, not a new extremal construction or local lemma.

## Native checker

The official [DRAT-trim repository](https://github.com/marijnheule/drat-trim)
documents the proof format and checker semantics. The source used here
comes from upstream commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
The exact source SHA256 is
`d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`.
It was compiled with `gcc -std=gnu99 -O2`, with no allocation patch.
The binary SHA256 used in this run is
`402611b647364505090b672bbac5c4d6ceb5107b591a5a6ebbc3921de11395be`.

Reference: Nathan Wetzler, Marijn J. H. Heule and Warren A. Hunt,
*DRAT-trim: Efficient Checking and Trimming Using Expressive Clausal
Proofs*, SAT 2014, LNCS 8561, pp. 422–429, as cited by the upstream
documentation. Proof verification remains ordinary compiled execution,
not formal verification of the checker.

## Evidence provenance

The original manifest has SHA256
`ec7fabe454c7a0e6297f3347de038028602a1aae81efd377ff4d938883af31c4`.
It identifies 112 ordered blocks, 109,676 inputs, and 19,782,097,200
original proof bytes. The independently reproduced quotient domain has
SHA256 `02727db9fb02d60a8597f84329f7376bba2c43422d63241da1c251fde97e4eb2`.
Our programs read the original corpus without changing it.

All formulas are constructed from point-pair affine geometry, Boolean
words for cardinality constraints, and finite-field Gaussian elimination.
The independent scripts import no `point_model.py`, `evidence.py`, solver
library, or author geometry routine. Their complete-domain premise is the
previously reviewed enumeration; they are not a third quotient enumerator.

Raw traces, formulas, native logs, local checkpoints and executables remain
outside Git. The public source can regenerate and verify new traces.
Different valid proofs may have different hashes even for the same input.
Historical hash matching and proof validity are deliberately separate
operations. The regenerated-trace driver has a checked positive example
with different historical bytes and rejects an invalid proof whose
metadata were altered to match it.
