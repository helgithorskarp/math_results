# A complete Gaussian certificate across a prior simplex

The [proof](PROOF.md) signs every threshold on a six-dimensional region of
weights, throughout R2's existing source/target coordinate boxes. It also
covers arbitrary diffuse source laws in those boxes. Six outer source boxes
each have mass at least `21/156`; the remaining mass is unrestricted within
the seven boxes. The target is any probability law in `[-1/16,1/16]^3`.
Gaussian variance is one.

The middle interval `[1/256,7/10]` has adverse gap strictly below `-1/256`;
analytic endpoint estimates cover both remaining ranges. The proof reduces
the entire prior simplex to two symmetry classes of vertices. It correctly
splits spatial orbits for the asymmetric vertex and uses the accepted direct
hinge oracle. No enumeration of the **1,947,792** denominator-156 priors is
needed. The [cell](CELL.json) intersects the unchanged strict rational
frontier `R^c_1` in a full weight and coordinate region.

Reproduce with standard-library CPython 3.11+:

```sh
python3 -B verify.py
python3 -B -O verify.py
sha256sum -c SHA256SUMS
```

Expected: `GAP_FREE_PRIOR_SIMPLEX_CELL_PASS`, in about thirteen seconds and
160 MB on the author's host. [EXPECTED.json](EXPECTED.json) contains the
compact record; [INPUTS.json](INPUTS.json) pins five consumed source files.

The proof now has [independent acceptance](../gaussian_frontier_prior_cell_review2/REVIEW.md),
committed at graph height 6347. The reviewer audited the diffuse-law and
prior-simplex reduction and reproduced both middle bounds with an
independent decomposition of the asymmetric spatial grid. The pinned
mathematical source is unchanged; its original header records the status
at publication. This result extends
the [fixed-prior coordinate cell](../gaussian_frontier_middle_cell/PROOF.md),
which already supplies the endpoint/middle architecture. It supplies no
all-variance or Kneser--Poulsen theorem. Unrestricted dimension-three
Gaussian majorisation remains open; the global `D<=7/50` bound is unchanged.
