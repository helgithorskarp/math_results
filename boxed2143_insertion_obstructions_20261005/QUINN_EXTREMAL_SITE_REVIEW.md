# Separate internal review of the constant-eight-site obstruction

Reviewer: Theo, literature-researcher-4. Author: Quinn, literature-researcher-3. Verdict: accept the uniform family, exact maximum/minimum site sets, and exclusion of every pointwise positive linear total-site bound, at proof SHA256`d79043597caee092b38617c57ca76d2db0f27f51dbd3d8e7f54618ef37fecbf7`. This reviews the later packet independently of the earlier kernel acceptance. It is partial negative evidence within decision410, not a growth solution, priority claim or external peer review.

For n>=4, p_n=(1,n-1,n-2,...,2,n) cannot contain classical2143. The first selected descent cannot start at its initial1. If it starts in the decreasing middle segment, a later point in that segment is smaller and cannot be the selected largest value. The only larger later point is the final n, which cannot be third because a fourth selected point must follow. This exhausts possibilities and proves avoidance without trusting a checker.

For a new maximum to participate in2143 it must be third. Inserting at gap0 or1 leaves fewer than two preceding entries; gap2 has the increasing initial pair1,n-1; gap n has no succeeding entry. These four gaps cannot create an occurrence. The parent avoids, and a new global maximum lies above every old candidate rectangle, so no old occurrence is created. For every other gap3<=g<=n-1, the one-based quadruple(2,3,g+1,n+1) has values(n-1,n-2,n+1,n). The intervening unselected middle values are all below n-2. The rectangle is empty. Therefore the maximum sites are exactly{0,1,2,n}, including the boundary n=4.

Reverse-complement fixes2143 and transports empty rectangles bijectively. It also fixes p_n. If the parent length is n, the reverse-complement of a maximum insertion at gap n-g is a minimum insertion at gap g into the reverse-complemented parent: the new value n+1 maps to1, while the old values become1 plus their parent complements. Thus min and max legal sites reflect under g->n-g, proving the exact minimum set{0,n-2,n-1,n}. Each set has four distinct members for n>=4. The constant total8 disproves any proposed pointwise lower bound c*n for fixed c>0 at all sufficiently large n, by taking n>8/c.

This proof does not imply that the average total-site count over all avoiders is bounded, nor does it quantify the population of other low-site avoiders. An aggregate or weighted lower-bound route survives. No exponential upper bound or failure of factorial growth follows.

Independent replay uses `check_quinn_extremal_sites.py` and my previously reviewed canonical-rectangle checker, importing no Quinn kernel, author probe or Lyra checker. It reconstructed and compared the parent and every one of the16 supplied n=7 extremal children, including each complete occurrence set. It also checked all286 extremal insertion instances of the family for4<=n<=16, the reflected-child identity, and each stated maximum witness. Finally it exhausted all704 avoiders through n=6 and found minimum total-site counts2,4,6,7,8,8,8. Combined with the n=7 example of total8<9, this independently establishes minimal *length*7 for failure of the proposed n+2 bound. I did not check lexicographic minimality among all size7 permutations; that finer author probe claim is outside this review.

All four separate manifest file hashes/sizes matched and stayed unchanged; manifest SHA256`5883f4c47e2ce3b99c350759e45bfa802375b095af0cc4cb989abc366be5ce14`. The complete finite replay is `quinn-extremal-site-reproduction.json`; CPython3.11.2, standard library, exact integer/permutation operations, about0.39 seconds. Reproduce from this directory:

```sh
python3 -B check_quinn_extremal_sites.py --output quinn-extremal-site-reproduction.json
```

Finite tests verify the indicated implementation/certificate scope. The written arbitrary-n argument is the basis for the uniform conclusion. The complete growth target410 remains unsolved; no completion request or public source claim is justified by this review.
