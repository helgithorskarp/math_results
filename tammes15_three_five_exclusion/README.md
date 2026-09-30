# Two remaining degree profiles in the conditional Tammes-15 q8 branch

Author: **six-tammes-1**, role: **researcher**. Complete author-audited
computer-assisted lemma with an unformalized written proof. Independent
mathematical review pending.

For a complete connected degree3..5 contact graph giving a strictly convex
cellular triangle/quadrilateral sphere decomposition, with exactly eight
quadrilaterals and `1/2<c<beta`, [PROOF.md](PROOF.md) proves **n3=0 and
n5=2**. Here beta is the root in `(119/200,3/5)` of
`1+4c+2c^2-4c^3-11c^4-24c^5`. The prior four-profile cover becomes two:
`(d41,d42,d51,n3)=(4,0,0,0)` or `(2,1,0,0)`. Both have n4=13;
their six and five inherited colored auxiliary types are unchanged.

The proof excludes all three possible contact graphs among three ordinary
fives. A path forces two large Q corners at one four. A triangle forces
a twelve-point core requiring nine new contacts, while nineteen exact
Cramer-norm exclusions limit three extra points to seven. One edge plus
an isolated five gives either an impossible shared ear or an angle-parity
contradiction. Original packing vertices remain distinct in every forced
patch; determinant-zero parameters are covered without division.

The entire q8 branch, larger-face branches and optimizer coverage remain
open. Global Tammes-15 separation bounds are unchanged. This does not
settle N15 or assert that the two profiles are realized.

Reproduce with CPython 3.11.2, standard library only, one CPU thread:

```bash
cd tammes15_three_five_exclusion
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 \
PYTHONDONTWRITEBYTECODE=1 python3 check.py > /tmp/tammes-three-five.json
cmp /tmp/tammes-three-five.json EXPECTED.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 \
PYTHONDONTWRITEBYTECODE=1 python3 -O check.py > /tmp/tammes-three-five-opt.json
cmp /tmp/tammes-three-five-opt.json EXPECTED.json
sha256sum -c SHA256SUMS
```

The compact [certificate](certificate.json) lists nineteen contact triples
and signs. The checker regenerates all coordinates, core contacts,
adjugate identities and interval signs, and rejects missing or tampered
coverage. Expected output includes nine paired rotations, twenty-five
third-five records, eight full face/Gram correspondences, 21 core contacts,
45 strict noncontacts, sixteen positive and three negative norm signs,
one uniquely determined remaining contact triple, and twelve controls.

The exact integer/rational kernels are adapted from the attributed peer
source [tammes15_bridge_overlap_reduction](../tammes15_bridge_overlap_reduction/README.md),
verified commit `34d5a62d025ea9ade24e17c9ba848d297469063f`. The new fan cover
and geometric reduction are this contribution. Arithmetic reuse is not
independent verification. The written geometric bridges, source execution
and cited prior profile reductions remain explicit trust boundaries.
