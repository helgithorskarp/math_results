# H7 phase-ten rotation cover

six-vdw-2, researcher. Python3 standard library; tested with Python3.11.2.
See [PROOF.md](PROOF.md) for the complete restricted corollary and scope.
This generates phase representatives and checks their completeness. It does
not generate or solve every corresponding44-variable field model.

From this directory, choose fresh scratch paths outside the repository:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 generate.py --work /tmp/h7-phase10-rotation-cover
python3 check.py --work /tmp/h7-phase10-rotation-cover
python3 -O check.py --work /tmp/h7-phase10-rotation-cover
python3 guards.py --checked-work /tmp/h7-phase10-rotation-cover --work /tmp/h7-phase10-rotation-damage
```

Keep these jobs serial. A55-second guard per stage is sufficient for the
reported run; it is not a mathematical cutoff. EXPECTED.json freezes the
144,603 rooted inputs,127,049 canonical phase classes,29 short-period
classes and corpus hash. Every representative is independently checked
against actual phase positions and Burnside's exact complete class count.
The2.54MB generated corpus and corruption copies are intentionally omitted
from Git. No SAT solver, converter, native library or proof corpus is required
for this new corollary. The cited earlier conditional lemmas remain inputs.
