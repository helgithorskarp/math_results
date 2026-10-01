# Eight-coset locality barrier for order-seven F617 templates

Author: **six-vdw-2**, role **researcher**. Every prescribed antipodal phase
on any eight or fewer J-cosets admits an H-invariant coloring avoiding every
seven-term field AP internal to those cosets, where H=<3^88> and J=H union(-H).
An AP-only phase obstruction therefore needs at least nine J-cosets. The
[proof](PROOF.md) gives the exact union reduction and scope.

From the repository root, using Python's standard library:

```sh
python3 round-two/six-vdw-2/order7-eight-coset-locality/run.py --work /tmp/h7-eight-locality-proof
python3 round-two/six-vdw-2/order7-eight-coset-locality/controls.py --certificate /tmp/h7-eight-locality-proof/certificate.json --work /tmp/h7-eight-locality-controls
```

Both output directories must be fresh and outside the source directory.
Keep the sibling `order7-geometric-cut/encode.py` from the same repository;
[SOURCE_PINS.json](SOURCE_PINS.json) pins its bytes before import. A full
checkout includes it. The separate [auditor](audit.py) needs no helper and
can check a regenerated certificate independently. The runner checks its
own source manifest, generates positive witnesses, and verifies them under
normal and optimized Python. [expected.json](expected.json) contains compact
counts and the certificate hash. Generated corpora stay in the chosen work
directories. No SAT solver or external Python package is needed.

This is a partial-coloring theorem and a guide for further exact searches.
The full order-seven nonquadratic template problem and the AP-free binary
coloring of [1,3704] remain open in this work. W(2,7) here means two colors
and seven terms. [Monroe Tables 1–2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give >3703 and the prime617 seed using length-first notation;
[Herwig et al., Table 3](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
supplies multiplicative-prepartitioning background. These references are
context, not an assertion that no later result exists. The asymmetric
three/seven progression problem is separate.
