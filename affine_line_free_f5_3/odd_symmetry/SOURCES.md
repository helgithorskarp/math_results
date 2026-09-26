# Sources and dependencies

1. C. Elsholtz, J. Führer, E. Füredi, B. Kovács, P. P. Pach, D. G. Simon,
   and N. Velich, *Maximal line-free sets in F_p^n*, Periodica Mathematica
   Hungarica **90** (2025), 7–21.
   [arXiv:2310.03382v2](https://arxiv.org/html/2310.03382v2),
   [journal DOI](https://doi.org/10.1007/s10998-024-00617-x).
   Theorem 1.5 gives the published upper bound 73; Figure 4 gives the
   70-point construction used by this repository as a comparison control.
   The paper recalls the planar bound $(p-1)^2$, attributed to Jamison
   and Brouwer–Schrijver. In this finite setting the repository also gives
   a complete [planar verification](../plane_caps.cpp) of the bound 16.

2. Campaign [upper bound 72](../upper_bound72.md), Discovery Net artifact
   `bafkreigdcleaywkrwivj7mewtq4lir55ort2jlkblt6a72m5j5bskscdjq`.
   This is context for the exact target. Neither the sharp order-three
   obstruction nor the conditional automorphism-group theorem uses the
   global upper bound as a proof premise.

3. Campaign [global low-plane theorem](../low_planes72/README.md),
   Discovery Net artifact
   `bafkreifb7i4346rrz2c5ch5vhs4odx3n57xijazwl6jrgjhdmmijzthaqy`.
   Used only in excluding central inversion at size 72: there are at
   least five planes whose sections have size at most nine.

4. Campaign [two-eight-plane exclusion](../two_eight_planes72/THEOREM.md),
   Discovery Net artifact
   `bafkreidboslmutvk646hvk6d7kjyvqopa3ks6znrczmmwnyqpdirzoqwwu`.
   Used in the same central-inversion argument: at most one plane
   section has size eight. Its 164 solver exclusions have separately
   checked proofs; the current verifier does not replay those proofs.

The finite order-three obstruction and group-theoretic deductions are
the claims of this contribution. Theorem 1 has no dependency on items
2–4. The 2-group conclusion in Theorem 2 needs Theorem 1 and the planar
bound. The exclusion of central inversion at 72 and the resulting
order bound 32 additionally use items 3–4.

Primary-source and graph searches on 26 September 2026 found no matching
order-three or all-odd-order obstruction. This is novelty relative to the
searched sources, not an exhaustive priority claim. The extra 70-point
seed is proved affinely distinct from the specific Figure 4 control;
no claim is made that its affine orbit was previously unknown.
