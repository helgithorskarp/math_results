# Conditional original-J74 rigidity on a two-dimensional receiving patch

**six-rupert-2, researcher; 2026-10-01.** Author-checked exact finite
hypotheses and written continuum proof, unformalized and independently
unreviewed. Global J74 Rupert property **OPEN**.

[PROOF.md](PROOF.md) treats every original receiver
`u=m+t*d+s*(m cross d)`, `3/5<=t<=7/10`, `|s|<=1/50000`.
At each receiver, every closed scale>=1 fit with arbitrary actual
translation and relative Cayley norm<=**1/14400** from one of
`I,Rz(pi),M_u Mx,M_u My` is exactly that center, scale1, translation0.
All centers have the original receiver shadow. This is a conditional
source-motion theorem, not an all-source receiving exclusion.

The entire receiving patch is projective chord>1/3 from all six minimum
axes. Its example `(13/20,1/50000)` is chord>1/200000 from the entire
[parent one-dimensional arc](../nonlocal_arc_wrench/PROOF.md). That arc
retains its stronger source radius1/6000 at `s=0`.

The change is receiving coverage: a five-weight repair preserves exact
positive spatial force and torque balance throughout a real rectangle.
Uniform matrix inverse, positivity and exact Cayley bounds close the
proof. No floating search, sampled balance or improper body motion is
a proof input.

From the repository root, run these commands sequentially:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-rupert-2/nonlocal_receiving_patch/check.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B round-two/six-rupert-2/nonlocal_receiving_patch/check.py
```

The programs compare every field of the frozen [expected.json](expected.json).
Writing a new expected record with `--write-expected` is fixture generation,
not a comparison or independent validation. Explicit exception guards
remain active under optimization. [VALIDATION.md](VALIDATION.md) records
the completed production runs and damaged controls.

[certificate.json](certificate.json) specifies literal domain and theorem
constants. [DEPENDENCIES.json](DEPENDENCIES.json) pins six compact published
inputs. The parent complete finite record is replayed before new checks.
There is no numerical package, solver, remote-service, private scratch,
ledger, credential or omitted large-data dependency. The complete
continuous proof and original-solid identification remain an explicit
unformalized trust boundary. Publication is not independent review.
