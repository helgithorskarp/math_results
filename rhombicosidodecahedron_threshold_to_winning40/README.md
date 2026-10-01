# RID threshold sources into winning receivers at 2/5

**six-rupert-3, researcher; 2026-10-01.** Complete written, unformalized,
author-checked intermediate proof. Independently unreviewed. Global RID
Rupertness remains **OPEN**; its proved global cutoff83/200 and
squared-height gap1/28 are unchanged.

For the original standard edge-two rhombicosidodecahedron, write
f(n)=min_original_vertex |v dot n|, with n unit. The new theorem excludes
closed containment of any original threshold signed-region source into
any winning signed-region receiver with f(n)>=2/5, for every proper Q,
full residual roll, physical planar translation t and scale lambda>=1.
Both threshold source classes and the closed cutoff boundary are included.

Together with [graph8487](../rhombicosidodecahedron_winning_to_threshold40/PROOF.md),
[the strict threshold-to-threshold proof](../rhombicosidodecahedron_threshold_band40/PROOF.md)
and the complete original signed-region spectrum, every strict passage
with receiving f(n)>=2/5 would have **both source and receiver winning**.
That remaining branch at2/5 is unproved here. The result generalizes the
ordered mixed branch of [the 21/50 axial-majorization theorem](../rhombicosidodecahedron_mirror_cluster_obstruction/AXIAL_MAJORIZATION_PROOF.md);
its old guard and scalar domain remain unchanged.

The complete [proof](PROOF.md) connects each finite obligation to the
original containment problem. [verify.py](verify.py) checks the fixed
[closed covers](certificates.json) and regenerates every byte of
[expected.json](expected.json). [dependencies.json](dependencies.json)
pins all73 previous mathematical Python/JSON inputs. No private input is
needed; ancestor region enumeration and global proof computations are
not recursively replayed.

The source lower bounds retain all16 original threshold shadow preimages
per class, including eight noncircle originals with their actual signed
heights, and check all4 source polygon corners for the same original on
every leaf. The winning receiving envelope checks all60 originals in
each of12 reference facets, including tied noncorners. Auxiliary adjusted
vectors are bounds rather than substituted original points. The necessary
height polygons have4 source corners and6 receiving corners; no moving
hull combinatorics or small initial full-Q angle is assumed.

From the repository root, Python3.11+ standard library, run separately:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B rhombicosidodecahedron_threshold_to_winning40/verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
 python3 -B -O rhombicosidodecahedron_threshold_to_winning40/verify.py
```

Both regenerate all70878 expected bytes, SHA256
`d84d89512efdf828582ad30c0adf354f52de787097aaa0d0d9776f975333bad0`.
Each source class has26 closed roll leaves, maximum depth3. In total:
52 leaves,208 same-original corner gates,624 positive Bernstein lower
bounds,624 direct planar-vector audits,1536 physical interval triples,
720 whole-original receiving envelopes,4320 receiving corner bounds,
128 signed source adjustments,1920 source hull supports,840 original
polygon height gates and22 validated positive root records. All23
malformed controls reject, including under Python optimization.

The actual raw winning receiver (21/500,2-phi,1) has f between2/5 and83/200;
all60 original signs and exact squared-height inequalities are checked.
It confirms that the new domain extends below the previous global band,
without supplying a passage or global non-Rupert theorem.

Validation uses Python3.11.2, numerical threads1, one mathematical job
at a time and an unchanged55-second deadline. The written continuum
bridges, previously published exact arithmetic kernels and inherited
interfaces remain explicit trust boundaries. Finite vector audits are
author regressions, not independent review. No floating sample, solver
answer, timeout, UNKNOWN or incomplete cover proves nonexistence.
