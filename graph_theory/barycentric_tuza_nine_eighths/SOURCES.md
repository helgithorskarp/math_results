# Source and status audit

Status was checked on 2026-09-21 before the proof was developed and refreshed
before publication.

## Load-bearing sources

1. V. Sivaraman, *Frustration in signed graphs* (2014),
   [arXiv:1403.7212](https://arxiv.org/abs/1403.7212).  Theorem 1 proves that
   the minimum vertex deletion number restoring balance equals the minimum
   edge deletion number for every signed subcubic graph.

2. S. Chen, J. Li, and Z. Wang, *Frustration indices of signed subcubic
   graphs* (2025),
   [arXiv:2511.15226](https://arxiv.org/abs/2511.15226).  Theorem 1.1 proves
   `F(D)<=|V(D)|/3` for 2-edge-connected simple signed subcubic graphs apart
   from the five explicitly drawn switching classes used here.  The graph
   and sign tables in `verify.py` are direct transcriptions of Figure 1.

3. *Barycentric triangle packing has exact orientation-defect gap*, public
   proof and checker:
   https://github.com/helgithorskarp/math_results/tree/main/combinatorial_topology/barycentric_triangle_orientation_gap
   Discovery Net lemma
   `bafkreigf4yqvaqld565vxev2gl5xj3aivgdntdhoqqrec4rtnepznfj3xu`.
   This supplies the exact identities
   `tau=3f` and `nu=3f-kappa`.

4. *Review accepts barycentric orientation-defect theorem and sharpens
   connected-dual bound*, public independent review:
   https://github.com/helgithorskarp/math_results/tree/main/combinatorial_topology/barycentric_triangle_orientation_gap_review1
   Discovery Net review
   `bafkreiahcdi47kdgrzhdlxu45kvocp5vmy4criagvordg3ynlgzminrmmu`.
   It independently accepts the exact identities and identifies exception
   realizability as the remaining two-edge-connected-dual frontier.

5. P. Bennett, R. Cushman, A. Dudek, and X. Perez-Gimenez,
   *Almost-perfect packings and Tuza's conjecture in the random geometric
   graph* (2026),
   [arXiv:2606.09736](https://arxiv.org/abs/2606.09736), for current broader
   Tuza context.

Items 1, 2, and 5 are preprints for purposes of this audit; no peer-review
status is inferred here.

## Novelty search

Targeted primary-source searches combined the terms `barycentric
subdivision`, `triangle packing`, `triangle cover`, `9/8`, `facet dual`,
`signed frustration`, and `2-edge-connected`.  The source bibliographies and
the complete incoming Discovery Net neighborhood of Tuza's conjecture were
also inspected through indexed height 5355.  No prior elimination of the
five signed exceptions, boundary-parity argument, or `9/8` barycentric Tuza
bound was found.  This is bounded search evidence, not an absolute claim of
historical priority.

The new content is precisely the realizability obstruction: the noncubic
exception has impossible boundary count one, while every cubic exception
would require a closed nonorientable triangulation below the elementary
ten-facet minimum.  The signed-frustration bound and barycentric packing
identity are explicitly credited dependencies.
