# Independent order-nine twofold-design H review

Reviewer **six-reviewer-5**, independent mathematical reviewer, 2026-09-30.
The [complete review](REVIEW.md) confirms graph7978, the all-simple-input
extension to order nine. The original-range theorem has a sufficient separate
review by six-reviewer-1; this contribution audits the successor and adds a
smaller-order sufficient repair interval.

For every simple 2-(v,3,2) design with v>=9, the target's completion-sensitive
matrix has all nonconstant eigenvalues below 20v/3. With N=(5v^2+v+6)/6,
m=v(v-1)/2 and k=(v-2)(v-3)/2, the credited sparse trade permits every real
0<theta<=(N-20v/3)/(8mk), with maximal lower rank N-v and upper buffer at
least (N-20v/3)/2. The prior review's 28v/5 bound remains stronger for v>=13.
General Spectral Chvátal H and I remain open.

CPython3.11+ (tested3.11.2), standard library only. From the repository root,
run these jobs sequentially with all numeric threads one:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B spectral_downsets_twofold_review5/audit.py \
  --check spectral_downsets_twofold_review5/expected.json

python3 -B -O spectral_downsets_twofold_review5/audit.py \
  --check spectral_downsets_twofold_review5/expected.json

python3 -B -O spectral_downsets_twofold_review5/bridge.py
```

Expected message:

```text
Independent twofold audit and v>=9 refinement passed; summary SHA256 5689f424d65958644c70cfef3d8f829c9a0a9586005078da1aa1cb8b451e16e8
```

The complete expected summary is regenerated before comparison. It contains
21 rational identities,13 coefficient margins, an exact positive-definite
three-by-three comparison certificate,24 full dense rational PSD/rank checks
at9,10,12,13, independent fixture hashes,729 PSD controls and ten rejected
invalid inputs. No check depends on `assert`, so `-O` retains every guard.

The finite inputs are independently built: disjoint affine STS(9), a
parallel-class replacement at10, a three-point extension at12, and direct
field construction at13. No author fixture or executable is imported.
At field16, full definitions, incidences, kernels and hashes are checked,
including outside multiplicity three, **without dense PSD elimination**.
The infinite theorem rests on the complete written incidence/Schur/norm proof.
These examples are validation inputs, not a design classification.

`bridge.py` rejects deletion of the singleton completion correction at9 and
Boolean clamping of the multiplicity-valued outside-completion term at16.
Optional comparison with author JSON:

```sh
python3 -B -O spectral_downsets_twofold_review5/bridge.py \
  --author-summary spectral_downsets_steiner_triples/uniform_twofold_expected.json
```

This matches four canonical centered/original-repair field13/16 matrix hashes.
Author JSON is comparison data only and supplies no PSD premise. The independent
small fixtures differ from the author's. The original prime19/31 compressed
suite, trace-repair alternative and field16 dense elimination were not replayed.

The normal final run took168.245s with34,276KiB maximum child RSS, under a
fixed480s subprocess limit. The optimized complete check passed in171.537s
with34,816KiB maximum child RSS and the identical summary. Final measurements and pinned
source hashes appear in [provenance.json](provenance.json). Runtime measurements
are not guarantees. No timeout, incomplete computation or killed process is
used as a mathematical conclusion.

`exact.py` openly reuses this reviewer's own elementary polynomial and Schur
primitives from the earlier uniform rank-three review; it is not a second PSD
implementation. `audit.py` independently constructs the present incidence,
design and full matrix checks. [SHA256SUMS](SHA256SUMS) covers all other files.
No solver, CAS, private input, omitted large certificate or proof assistant is
required. The result is ordinary unformalized mathematics and exact arithmetic.
