# Independent isolate-incidence audit

Actual author six-reviewer-2, independent mathematical reviewer. The [review](REVIEW.md) confirms committed8993 and proves a more general obstruction: no finite multiset of rows of size at least four realizes the stated column/pair constraints. The row count is forced to11 and tags are row-size excesses. This excludes the specific marked dirty13 graph at any valid22-point/max-degree-ten one-nine root, without an edge-count assumption. The13-type classification corollary retains108 edges and credited8939/8987. Other types, outside completions and the Ramsey endpoint remain open.

Python3.11.2 standard library only. Run jobs sequentially from this directory:

```bash
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
python3 -B audit.py --output /tmp/isolate-incidence-result.json
cmp EXPECTED.json /tmp/isolate-incidence-result.json
python3 -B controls.py --output /tmp/isolate-incidence-controls.json
cmp CONTROLS.json /tmp/isolate-incidence-controls.json
python3 -B -O audit.py --output /tmp/isolate-incidence-optimized.json
cmp EXPECTED.json /tmp/isolate-incidence-optimized.json
python3 -B -O controls.py --output /tmp/isolate-incidence-controls-optimized.json
cmp CONTROLS.json /tmp/isolate-incidence-controls-optimized.json
sha256sum -c SHA256SUMS
```

The six original exact vectors in `CERTIFICATE.json` are untrusted proof inputs, hash `63ba27d0ef4fa100a14f09f902850842aa03e5b3e6ade5ba34ecac6d71bbf839`, from source commit `6fcb099c887612b81c3d4e0689629c9563c171fa`. Every multiplier, score and strict upper bound is checked. No researcher program, optimizer, native trace or graph catalogue is imported.

The third split generator exhausts6561 ternary partial partitions, giving all297 branches:160/128/9 tag pairs00/01/11. Its branch digest is `dd273094b7ce62dd760ee3006d2c9ef78e8b5c12ff15e6f0748096190cfe4541`. Four split vectors cover293/150/21/21 cases, first-use293/2/1/1; two direct vectors give strict upper totals-24/-1. All49740 residual-row scores and560 direct-row scores are computed. Full verification transcript digest is `ad6a82f09acb4c4720cab7a812d71e66be789d4f5f044db400401ae64bca6c10`.

Controls cover235 literal whole-spine cases,13312 full binary-row scalar comparisons,12 corrupted certificates, and the freshly fetched known21-point graph (red93/pages3,6). Original author normal/optimized expected records are separately replayed. Frozen fixture provenance and timings are in `PROVENANCE.json` and `VALIDATION.json`; generating this review's EXPECTED record is distinguished from matching the original frozen record. Ordinary reductions and program correctness remain unformalized.
