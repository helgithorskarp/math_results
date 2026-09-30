# Independent review of the 35 ACL69 coordinate cores

Reviewer **six-reviewer-4**, independent mathematical reviewer.

[REVIEW.md](REVIEW.md) confirms the restricted maximum69 theorem and proves
unconditional clique inequalities, trade accounting, and a concrete clique cut
outside the standard triple-packing LP. The unrestricted bounds69--72 are unchanged.

From the repository root, with CPython3.11+ and the standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B constant_weight_acl69_review4/audit.py --expect constant_weight_acl69_review4/expected.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B -O constant_weight_acl69_review4/audit.py --expect constant_weight_acl69_review4/expected.json
```

The checker imports no target code. It reads only the compact, pinned
`coding_theory/a18_6_5_coordinate_cores/acl69.txt` and `certificates.json` inputs.
They total8576bytes and are already public in this repository. To use separately
downloaded copies, pass `--seed PATH --certificate PATH`; hashes must match.

Expected: all8568 masks, all35 cores,4222 outsider occurrences,834 clique classes,
21757 intra-class pairs, and seven rejected malformed certificates. A fractional
witness satisfies all816 triple constraints while violating a verified clique
inequality. The two commands give identical [expected.json](expected.json).
The audit takes under half a second and about21MiB on the campaign machine.

This is a finite computer-assisted review, not a formal proof or a global
determination of A(18,6,5). [provenance.json](provenance.json) records exact inputs
and literature checks. No generator, solver, omitted proof corpus or package
installation is required.
