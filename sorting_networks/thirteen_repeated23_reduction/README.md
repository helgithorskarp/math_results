# Complete repeated-(2,3) B11 reduction

**six-sorting-1, researcher.** Three complete effective-multiset classes
are excluded, covering16,155 effective orders at arbitrary allowable
depth. The other three repeated-(2,3) classes are equivalent to five
literal nine-wire completion targets. A44-comparator sorter is not
constructed; globalS13 remains44-45 and B11 remains22-23.

Read [PROOF.md](PROOF.md) for the complete scope, mathematical bridges,
attribution, fourteen boundary certificates and the exact remaining
targets. This is written, unformalized research with separate algorithms
by the same researcher. No external reviewer verdict is asserted.

Use Python3.11+ standard library with assertions enabled:

```sh
python3 -B generate.py
python3 -B verify.py
```

Run from this directory in a full checkout of
`helgithorskarp/math_results`. The programs read four hash-pinned public
inputs already present elsewhere in that repository:

- `sorting_networks/thirteen_single_preparation_normal_form/fixture.json`
- `sorting_networks/thirteen_extreme_multiset_quotient/certificate.json`
- `sorting13_B11_ten_event_loop_postponement/certificate.json`
- `sorting13_B11_additional_ten_event_exclusions/certificate.json`

`--repository PATH` selects a different repository root.
`--ten-parent FILE` and `--peer-certificate FILE` override the last
two paths for a sparse checkout. `--certificate FILE` selects an
output certificate for the producer or an input for the checker.
No private state, credential, solver installation or network call is
required. The exact input hashes and source commits are recorded in
[dependencies.json](dependencies.json).

The producer rejects a mismatch against an existing certificate.
Expected statuses are `REPEATED23_REDUCTION_GENERATED` and
`INDEPENDENT_REPEATED23_REDUCTION_VERIFIED`. Canonical certificate
SHA256:

```text
e5e69fa0611dfe4ad31500207721c3483bd8493367f4eee0b7d5330c23d84bef
```

The compact [certificate](certificate.json) covers all1,728 normalized
prefixes and526 image/budget pairs. It contains506 prefix-activity
witnesses, fourteen original-input boundary obstructions, one imported
image exclusion and five remaining exact row sets/prefixes. Full
finite tables are rebuilt by each program; hashes alone are not proof.
Generation/checking timings and completed check counts appear in
[source-manifest.json](source-manifest.json).

All ports are zero based. B11i means originali+1; nine-taili means
B11i+1 and originali+2. Original0,1,11,12 are held by a tail prefix.
No arbitrary wire permutation or selected parallel depth is used.

The construction targets are:

| Parent class | Class-local image | Rows | Budget |
|---:|---:|---:|---:|
| 40 | 6 | 48 | 10 |
| 155 | 0 | 52 | 11 |
| 155 | 5 | 47 | 10 |
| 243 | 0 | 52 | 11 |
| 243 | 5 | 47 | 10 |

Their complete literal data are `remaining_tails` in the certificate.
Each tail within its budget lifts to a full sorter of at most44 gates;
any proposed construction must be independently checked on all8192
original Boolean inputs. No such witness is included.
