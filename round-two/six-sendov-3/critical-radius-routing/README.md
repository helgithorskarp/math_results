# First-power control from fixed total critical energy

Actual author **six-sendov-3**, role **researcher**, 2026-10-02.
Complete ordinary author proof, **unformalized and independently unreviewed**.

For every monic complex degree-nine polynomial with unit-disk original roots,
p(1-eta)=0, 0<eta<=2^-16, and H=sum|zeta_j|²<=1/512, the reciprocal-distance
sum obeys **F>8+(8/3)eta-(4/3)eta² >=8+(131071/49152)eta >8+(13/5)eta**.
No coefficient cap or critical template is assumed. On F<=8+3eta, the proof
also gives **H<7eta**, |c8|<39eta/5, |c7|<4eta and every |c1..c6|<8eta.
Critical collisions remain included; all originals are proved simple.

Read [PROOF.md](PROOF.md) for all quantifiers, complete inequalities and the
separate total-collision case. The proof centers criticals before original motion,
then uses ACTUAL paired and individual original normals. It does not use the old
cap8 conditional energy estimate to prove coefficient entry. Critical radius
at most1/64 is an included corollary since H<=8/4096. Actual competitors with
H>1/512 remain uncovered by this theorem; the hypothesis permits individual
criticals outside1/64. The source directory retains the original frontier name.

Reproduce with CPython3.11 or later and the standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -B verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1 python3 -I -B -O verify.py
```

Both modes must report PASS with20 whole symbolic identity records,46 strict
whole-domain scalar margins,6 Gaussian-rational critical controls and17 rejected
mathematical changes. The identical entire typed canonical record has SHA256
**b04129905ab1b4992352c925338a6ee29d3540e655563410905f66c7a6442022**.
[VALIDATION.json](VALIDATION.json) records timing/memory and16 external damaged
fixture rejections, each with the intended failure text in normal/optimized modes.

The controls reconstruct full anchored and translated original polynomials and
retain all critical multiplicities. They explicitly do NOT assert original-disk
feasibility for arbitrary generated critical data. One control has a critical
at1/32 and seven atzero: it demonstrates the broader critical-data domain,
not disk feasibility. The written proof uses the
original-disk hypothesis and whole Taylor/Rouche arguments. The finite checker
certifies rational identities and budgets, not infinite-series convergence,
Maclaurin/convexity, analytic root counting or all-parameter completeness.
No solver, CAS, floating-root finder or finite parameter grid is a proof premise.
Kernel reuse is credited in [provenance.json](provenance.json); it is not independent
review. [LITERATURE.md](LITERATURE.md) and [dependencies.json](dependencies.json)
separate self-contained mathematical coverage from prior methods/review scopes
and optional comparison-branch context. Checks precede ordinary source publication;
verified source commit and actual graph commitment are recorded separately in the
original mathematical contribution, without a self-referential source rewrite.
