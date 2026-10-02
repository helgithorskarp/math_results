# Parent4 BASE obstruction

For the literal prefix8:0,9:0,10:1,14:1,12:10, no choice of one phase of
each unused ORIGINAL divisor of2520 at least8 clears all other mod8
parents. This eliminates the parent4-only BASE construction route without
an A4 hypothesis. A full distinct covering with this prefix and moduli
dividing10080 must use a productiveTAIL class outside parent4. There is
no full-prefix exclusion or global numerical \(L_{\min}(8)\) improvement.

Author: six-covering-3, researcher. Exact computation and ordinary proof;
same-author independent algorithm, no external review or formalization.
See [proof.md](proof.md) for the complete reduction and prior-work credit.

Python3.11.2, standard library only. From this directory, run:

```
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B reproduce.py --scratch /absolute/workspace/scratch/parent4-base-check
```

The driver runs only one CPU child at a time. Every child has the unchanged
20-second guard, and the retained frontier is capped at300. Four producer
stages, four independent AP stages in both normal/optimized modes, affine
checks and scope controls are all required. An interrupted, timed-out or
failed run is not mathematical nonexistence. `certificate.json` is compact;
all4644 complete branch rows are regenerated rather than stored publicly.

To inspect one step manually:

```
python3 -B check_affine.py
python3 -B generate.py --stage 1 --output /absolute/workspace/scratch/stage1.json
python3 -B check_stage.py --stage 1
```

Repeat the last two commands for stages2,3,4 and repeat the independent
checker under `-O`. One successful stage alone is insufficient. Expected
retained counts are27,76,60,0. The final conditional maximum is1116<1118;
the universal assertion is at least one outside-parent BASE hole.
