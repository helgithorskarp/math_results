# Independent audit of the C5 symmetry maximum

Reviewer **six-reviewer-4**, independent mathematical reviewer. See
[REVIEW.md](REVIEW.md) for the exact scope, proof audit and structural refinements.

The maximum size is 68 for length-18, weight-five, distance-six codes with
an automorphism of cycle type `5^3 1^3`. The complete fixed-point reduction
imports Brouwer's historical `A(17,6,4)<=20` theorem. Other automorphism
types and the unrestricted 69–72 gap are outside the claim.

Requirements: CPython 3.11.2 or compatible Python 3, standard library only.
Run sequentially from the repository root:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B constant_weight_c5_review4/audit.py --expect constant_weight_c5_review4/expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -O -B constant_weight_c5_review4/audit.py --expect constant_weight_c5_review4/expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B constant_weight_c5_review4/controls.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -O -B constant_weight_c5_review4/controls.py
```

The public tree and 68-word fixture are read from
`constant_weight_a18_6_5_c5_symmetry`, reviewed source commit
`1bdec881626ddd652b00d5e4f0b69c9322434359`; their hashes are recorded in
[provenance.json](provenance.json). The default auditor pins the certificate.
If those files change, retrieve the reviewed Git blobs and supply their
paths with `--certificate` and `--witness`. No researcher module, generator,
or stored orbit database is imported, and no search engine is needed.

Expected: 1,125 admissible full orbits, all 100 saturated links, all 6,000
normalizer elements, a checked 223-node tree with residual clique number
exactly nine, and the 68-word lower witness. The all-center link graph has
300 vertices, 1,950 edges and no triangles. All eleven semantic corruption
controls reject. The full-domain hashes match the target despite independent
Gosper generation, bit rotations, XOR-distance graph and normalizer methods.

Each audit takes about 1.7 seconds and less than 26 MiB. An interrupted run
is incomplete. [expected.json](expected.json) and
[controls_expected.json](controls_expected.json) contain compact complete
outputs. Generated graphs and execution logs are not publication inputs.
The historical theorem, written unformalized reductions, reviewer code and
Python exact arithmetic remain explicit trust dependencies.
