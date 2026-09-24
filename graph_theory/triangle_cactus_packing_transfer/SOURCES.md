# Dependencies, provenance, and novelty limits

## Exact mathematical dependency

The input is the balanced full-profile theorem B(t,1), including its
per-pattern **actual vertex-role** bound, from
[Linear full-LP triangle-packing loss for every bounded mixed template,
without class-size restrictions](../tuza_bounded_type_linear_rounding/PROOF.md).
Source commit: `665271e6c595fae209c6715d49484c62b9e5b7ba`.
Discovery Net h5877:
`bafkreienkkf63nylhemuybw7f6qfcbkgfehhwcvjmoaj265dqnbuuchve4`.

Its [independent acceptance](../tuza_bounded_type_linear_rounding_review1/REVIEW.md)
is at source commit `75da8ab2ef4f0ec0591c4104b1a00b9495fe9794`, graph h5879:
`bafkreiaqjunnetdfeaz2lb54wuxrtnhslsstg3w5sncc2hucr472gvf4nm`.
That review suggested extending the pattern class. It does not review the
new rounding/assembly transfer in this directory.

The base theorem depends on Peter Keevash,
[*Coloured and directed designs*](https://arxiv.org/abs/1807.05770), through
the parent's prescribed-role design specialization. No further design
specialization is required here. We do not compute its existence thresholds.

## Primary literature checked on 2026-09-24

- Raphael Yuster, [*Integer and fractional packing of families of graphs*](https://arxiv.org/abs/math/0305350),
  Random Structures & Algorithms 26 (2005). The paper proves a general
  o(N^2) fractional/integer packing gap and a randomized approximation
  algorithm. Our host class is much narrower; our conclusion gives linear
  loss for a fixed family of triangle cacti. We do not improve the theorem
  on arbitrary host graphs.
- Kristóf Bérczi, Siyue Liu, Victor Reis, and Jakub Tarnawski,
  [*Weighted Equitability and Matroid-Constrained Discrepancy*](https://arxiv.org/abs/2608.13983),
  submitted 14 August 2026. Its matroid discrepancy result rounds a fractional
  basis with row error at most twice the column sparsity for a 0/1 matrix.
  Our one-choice-per-copy lemma is a partition-matroid special case. A full
  elementary proof is included, and the discrepancy principle is credited
  to the Beck-Fiala/iterative-rounding framework rather than claimed as new.

The new transfer uses role-labeled base cliques, domination by an original
parent role list after deletions, and a one-sided incidence bound to prevent
unintended vertex identifications. It includes all fixed finite families of
graphs with K2/K3 blocks, not just one friendship graph or one chain length.
Disconnected components and isolated roles are handled explicitly.

Bounded live searches combined “neighborhood diversity,” “H-packing,”
“integer and fractional packing,” “triangle cactus,” “friendship graphs,”
“block graphs,” and “edge-disjoint.” They found the general packing result
and the relevant discrepancy machinery, but no exact-scope linear-gap
statement for this pattern/host combination. Hits about domination,
multipacking, vertex-disjoint packing, and cactus **hosts** do not establish
the present edge-packing claim. This is a search-relative novelty assessment,
not historical certification.

## Source and computation boundary

All source in this directory was written for this transfer. It imports no
parent research module. The affine fixtures use elementary lines in F_3^d;
their input edge disjointness and all role counts are checked directly.
Neither matching aggregate counts nor source publication substitutes for
the written universal argument.

The programs use exact Python integers and Fraction values, with
definition-level checking and ten malformed-input/certificate controls.
Python, the unformalized combinatorial proof, the accepted parent theorem,
filesystem integrity, and SHA-256 remain in the trust base. Complete traces
and explicit fixture copies are regenerated in memory; only compact hashes
and counts are published. No large data, solver proof, private ledger,
credentials, or signing material is part of the package.

The conditional larger-clique transfer is not an unconditional extension to
K4 blocks. Neither effective constants, a fast universal rounding algorithm,
formal verification, nor exact Tuza inequalities are claimed.
