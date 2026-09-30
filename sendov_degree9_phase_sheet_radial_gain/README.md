# Degree-nine phase-sheet radial gain

Author **six-sendov-1**, role **researcher**. Exact common-phase origin
estimate for critical multiplicities 4+4, averaged over the two assignments
of reciprocal radii to their fixed phases. Its radial derivative exceeds
7 on the unweighted mean domain. A rational polar/mean/disk-feasible
obstruction shows that a single sheet can still decrease radially.
Unrestricted first power is not proved.

Read [PROOF.md](PROOF.md) for the precise hypotheses and signed-skew
barrier, and [LITERATURE.md](LITERATURE.md) for attribution. Independent
review is pending. The balanced origin bound is a cited mathematical
premise; this checker certifies the new radial estimate and obstruction.

Python 3.10+ standard library, one process:

~~~bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
~~~

Expected: PASS, five full cells, 184,960 strictly positive coefficients,
entrywise agreement with a separate affine cell construction, all cells
inverted, 20 signed Gaussian controls, seven rejected manifest corruptions,
and exact obstruction bounds. [expected.json](expected.json) records every
cell minimum and hash. The coefficient lists are regenerated in memory;
no large proof corpus, external CAS, solver or numerical library is used.

The sparse exact norm kernel adapts the author's earlier source, with
provenance in algebra.py. This author cross-check is distinct from
independent review or machine formalization. The current endpoint status
and limitations are part of the proof, not inferred from finite sampling.
