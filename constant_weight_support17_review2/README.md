# Independent support-seventeen review

six-reviewer-2, independent mathematical reviewer. The complete assessment
and proofs are in [REVIEW.md](REVIEW.md). The standard-library
[audit.py](audit.py) independently regenerates30 shared-anchor second stars
and16 adjacency second stars by clique enumeration, checks all78 anchor
leaves, and computes sharp adjacency anchor replications15/16.

From the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B constant_weight_support17_review2/audit.py
```

Python3.11.2 or compatible, no third-party dependency. The comparison inputs
are two compact JSON manifests in the sibling
`constant_weight_18_6_5_equality_structure` directory; [INPUT.json](INPUT.json)
pins their source commits and SHA256 values. No researcher code is imported.
For an isolated download use `--target /path/to/manifest-directory`.
Normal and `-O` modes must match [expected.json](expected.json).
`--output PATH` saves the independently regenerated summary locally.
`--generate` explicitly rewrites the reviewer expected file and is intended
only for source maintenance, not the checking command.

Expected status COMPLETE and output SHA256
`80c93b9970bd429127c443bacbb2eaa4574dd1413b12111f159393370cce8477`.
[VALIDATION.json](VALIDATION.json) records normal/optimized and supplementary
author-program reproduction. All searches are single-process, guarded,
and exact. Incomplete runs prove no exclusion. Global69--72 remains open.
