# Reproduce the sharp one-noncontained-tail boundary

Actual author six-code-2, researcher. See [PROOF.md](PROOF.md) for the exact
theorem and ordinary bridges: for the supplied classicalD and arbitrary F,
t1/R=a+4 has sharp maximum69; every noncontained Q is covered by actual
point maps. There are ten restored canonical69 packings for Q15. This is
author-checked, independently unreviewed, with no global endpoint or
historical novelty claim.

From the repository root, using Python3.11+ standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-code-2/noncontained_tail_boundary/reproduce.py --work scratch/q-boundary-normal
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B round-two/six-code-2/noncontained_tail_boundary/reproduce.py --work scratch/q-boundary-optimized
```

Use fresh output directories. Run the commands sequentially; do not increase
guards after interruption. Child outputs, generated corpora and execution
records stay under the chosen scratch directory. No solver, external
package, private ledger, credentials or external input is needed.

The script checks source/fixture/certificate pins, rebuilds all five stages,
and compares every mathematical byte, positive certificate and complete
generated-artifact hash. Expected whole audit SHA256:

    96d73bf625dcf86a0ddde5e8d18f4fbaebe3639285a8e4573ee06771b8f43d74

Both modes must return4004 full cores,8884 edges,4336 triangles,10
four-cliques, zero five-cliques,2040 actual Q-maps and all10 distinct
normalized69 codes.1573 of2067 prospective caps have no valid core.
The positive four-color certificate is8497 bytes; complete normalized69
codes are5813 bytes. The per-stage initial limits are60seconds and two
million generation/clique states, with one native thread/serial CPU job.

The mathematical result includes full carrier coverage, all graph rows,
every map's whole-D images, every69 code's literal pairs/triples and five
actual damage rejections. Separately implementing the physical checks is
same-author validation, not external review. Hashing is integrity evidence,
not a substitute for the mathematical reduction or completeness checks.
