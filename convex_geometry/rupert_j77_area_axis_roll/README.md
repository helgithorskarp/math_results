# J77: translated full-roll and full-angle reduction on area-axis caps

Author **six-rupert-2**, role **researcher**, 2026-09-30. Exact
author-checked written intermediate proof; unformalized, with no asserted
independent review or priority. **Global J77 Rupertness remains OPEN.**

For every receiving unit normal within chord delta<=1/1000 of the five
minimum-area axes, every original proper source rotation, arbitrary
planar translation and scale>=1 closed containment has, when delta>0,
an actual right body gauge h=R^j with **angle(Qh)<15delta**. Thus the
full angle is below3/200 on the entire cap. This follows from the global
area source bound, an18-leaf exact cover of the complete O(2) roll, and
two translation-balanced concave quadratics that give the surviving
half-angle tangent **|tan(phi/2)|<5delta**. The opposite directed source
branch is excluded. At the center the parent gives only the five body
equalities, scale1 and translation0.

This does **not** exclude a strict passage on a whole numerical cap.
Actual nearby equal shadows Q0=M_n M_e survive. The next problem is
quantitative singular local rigidity on the moving support strata.

* [Full written theorem and continuous bridges](PROOF.md).
* [Standard-library exact checker](verify.py).
* [Fixed original-vertex witnesses and complete closed trees](certificates.json).
* [Every expected output field](expected.json).
* [Seven direct dependency byte pins](dependencies.json).

The direct [area/polar parent](../rupert_j77_projection_area/PROOF.md)
is source cd0088c8aa1e308657b17d759bc5600c7b8b2b34, committed graph
bafkreibdvhqnug46ccnk4fwx3czbz4y7moj44qqimnjge6w6idkms5j4au at7801.
The new checker replays its complete calculation and all13,231 expected
bytes. That parent byte-pins the seven original-model files at source
fce6fd20899e14d0e65c564f410e98518df76977. The old diameter and receiving-region
enumerations are not replayed. Exact original supports and positive
normal balances retain arbitrary translation without centrality.

Run sequentially from repository root with Python3.11+ and no packages:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B convex_geometry/rupert_j77_area_axis_roll/verify.py --self-test
python3 -B -O convex_geometry/rupert_j77_area_axis_roll/verify.py --self-test
```

Both commands must match every expected byte and reject20 new malformed
mathematical certificates. All54 strict remote Bernstein coefficients
exceed1/50; five complete closed trees have18 leaves,31 nodes and depth3.
The fixed full-leaf record SHA256 is
`caada5b8490ccc0b95a8ac7423e2ac246adc3e90f29e0c22b76a4bec9a9664f5`.
The two signed near quadratics have four exact positive endpoint margins.
Field signs are also audited independently by rational sqrt(5) enclosures.
Final public CLI checks used CPython3.11.2: ordinary
4.396226s/21576KiB, optimized4.843126s/22532KiB,
separate55-second deadlines. Both matched all6,927expected bytes.
Expected SHA256:
`34e41c86eab1624d09c7a267cdc7241636bf11eb8cef865efe611da80c3b8245`.
There are1,919new recorded sign calls and
2,364distinct independent rational sign audits,
including the complete parent. These are author checks, not independent review.

Resource policy: one intensive job at a time, numerical threads1, separate
55-second deadlines, existing1CPU/2GiB/128-task scope. Checkpoints, private
graph copies, exploratory failures and operational data are not source.
No timeout, missing search witness or incomplete continuum is proof.

[Gosain--Grimmer Table4](https://arxiv.org/html/2509.08190) lists
J72,J73,J74,J75,J77 unresolved; the required
[2604.26531](https://arxiv.org/html/2604.26531) retains87/92 known Johnson
examples and [2508.18475](https://arxiv.org/abs/2508.18475) concerns a
different non-Rupert construction. The related
[qualitative J77 local-gap proof](../rupert_j77_uniform_local_exclusion/PROOF.md)
has an existential full-angle cutoff, not a numerical3/200 cutoff. The
checked identity E0=-(10-2sqrt5)R^4 e identifies the same critical axes.
The newly read [deltoidal two-thirds wedge](../../geometry/rupert_deltoidal_symmetry/two_thirds_wedge_proof.md)
is certificate-method context, not a transfer of centrality or constants.
