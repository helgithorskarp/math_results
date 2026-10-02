# Complete source exclusion on a closed high-area RID receiving triangle

**six-rupert-3, researcher; 2026-10-02.**

For the standard edge-two rhombicosidodecahedron K, let Delta be the full closed raw receiving triangle

    (9/100,(3+2phi)/100,1), (11/100,(3+2phi)/100,1),
    (1/10,(5+2phi)/100,1), phi=(1+sqrt(5))/2.

For every normalized n from Delta and every actual R in SO(3), original lambda>=1 and physical t in n-perp, a closed fit `lambda P_n R K+t <= P_n K` holds exactly when `lambda=1,t=0,R in G union H_n G`, where G is the actual60-element proper body group and H_n is the proper pi turn about n. Body images and negative normals are included. Every receiver here has physical area>A2, A2^2=960+1536phi. The existing subthird source filter does not supply entry here.

[PROOF.md](PROOF.md) proves the complete reduction and closed coverage. The [8.4KB explicit certificate](certificate.txt) has108 source roots,960 literal bisections and1068 leaves (993 actual-support/75 closest-shadow gauge), with all64080 tensor coefficients>3/5000. Six exact cubic coordinate duals prove the uniform closed local Cayley collar1/25. Global RID remains OPEN; author-checked, unformalized, independently unreviewed.

The mathematical checker requires Python3.11+ and its standard library only. From the repository root, put output under a private scratch directory:

```bash
mkdir -p scratch/rid-high-area-replay
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 timeout 20s python3 round-two/six-rupert-3/rid_high_area_full_source_triangle/verify.py --output scratch/rid-high-area-replay/normal.json
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 timeout 20s python3 -O round-two/six-rupert-3/rid_high_area_full_source_triangle/verify.py --output scratch/rid-high-area-replay/optimized.json
```

Run those commands sequentially. The checker rebuilds named geometry and ALL signs, consumes every closed source subdivision and requires equality with the WHOLE [expected record](expected.json). Expected terminal fields include `tensor_coefficients:64080`, `support:993`, `gauge:75`, `whole_expected_record_match:true`. Normal/optimized CPython3.12.14 replay passed in14.164/12.632s, peak26152/30336KiB. No assert statement controls a proof gate.

Optional discovery regeneration requires NumPy1.24.2 (tested with CPython3.11). It is not needed to verify the theorem:

```bash
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 timeout 20s python3 round-two/six-rupert-3/rid_high_area_full_source_triangle/propose.py --output scratch/rid-high-area-replay/regenerated.txt
cmp round-two/six-rupert-3/rid_high_area_full_source_triangle/certificate.txt scratch/rid-high-area-replay/regenerated.txt
```

The regenerated certificate matched every byte and SHA256 `dd0a0afe62abe6befefe98fd656a715c806cc009755f1ae1f84c8083e1b33b7d`. A soft guard returns INCOMPLETE with pending nodes; it creates no complete text certificate. Floating positivity, lack of a candidate, or a process limit is not a proof. No parallel worker or resource increase is used.

`field.py` is a verbatim pinned copy of the published original RID field module. `geometry.py` freshly checks the actual G/B correspondence and universal Hamilton identity. `domain.py` proves the actual entire closed receiving-triangle supports, physical area and local duals. `forest.py` parses the literal compact tree. `verify.py` independently checks the joint coefficients and six damaged/false controls. `propose.py` is an optional untrusted discovery producer. [DEPENDENCIES.json](DEPENDENCIES.json) records the named input and prior references. Private logs, exploratory data, credentials and node state are absent.
