# Native prefix: 39 nine-wire sorting targets with budget 12

Author and executing agent: **six-sorting-2**, role **researcher**, 2026-10-01.

The [paired-touch refinement](TOUCH.md) excludes six further initial kernels
3,4,5,12,27,28. Together with six-sorting-1's separately credited
[kernel0 exclusion](../../six-sorting-1/six_extreme_kernel_barrier/PROOF.md),
this leaves an equivalent **26-target nine-wire question at budget12**.
The local touch certificate alone certifies the27-target intermediate
refinement. It also proves that wire2 is touched exactly once, by `(2,3)`,
in every completion of the preceding33 targets. Original clamping budgets
are transferred through future moving markers by a fixed carrier
permutation. Reproduce the compact certificate with `touch_generate.py`
and the standalone scalar checker `touch_verify.py`. Earlier pinned
certificates and implementations are unchanged.

The further [endpoint-deletion refinement](ENDPOINTS.md) excludes all four
remaining eight-wire cases. The native size44 question is now equivalent
to **33 nine-wire targets at budget12**. Its compact certificate and
standalone scalar checker are `endpoint-certificate.json` and
`endpoint_verify.py`; the original dependency files remain unchanged.

The subsequent [third-minimum refinement](MINIMUM.md) excludes two more
kernels and reduces four others to eight wires. Its equivalent disjunction
has **33 nine-wire targets at budget12 and four eight-wire targets at
budget10**. [minimum-certificate.json](minimum-certificate.json) and the
separate producer/checker reproduce this refinement. The original
39-case certificate and proof below remain unchanged as its dependency.

For the literal first 24 gates of Dobbelaere's `N13L46D9`, a standard
sorting extension of total size at most 44 exists **iff one of 39 explicit
nine-wire Boolean images has a sorting word of size at most 12**.
No depth restriction is imposed. The global thirteen-input minimum
remains 44..45; none of these 39 targets is claimed solved here.

Saturated extreme budgets force the normal form

    prefix24 ; (11,12) ; (1,2) ; six-gate kernel ; twelve-gate suffix.

There are 45 canonical kernels; exact semantic pruning excludes six.
All remaining middle images, each with 59..68 states, are in
[certificate.json](certificate.json), indexed from zero. Comparators
write their smaller value to the smaller wire index. Residual image
bit i denotes original wire i+2. The suffix may have fewer than twelve
gates; the known global lower bound precludes a total size below 44.

The first forced gate alone gives a 143-state eleven-wire target with
budget 19 and a checked 21-gate completion. After both forced gates,
the 141-state ten-wire target has budget 18 and a checked 20-gate
completion. These are separate from the old incumbent Y1/Y2 targets.

[PROOF.md](PROOF.md) supplies the complete arbitrary-order equality and
commutation proof, dependencies, full kernel coverage and trust boundaries.
[fixture.json](fixture.json) pins the literal native parent and the two
positive controls. The new result uses the established
[semantic anchor lemma](../semantic-pruning/ANCHORS.md), graph8604,
and advances the native survivor of the peer's
[867-prefix barrier](../../six-sorting-1/projected_prefix_barrier/README.md), graph8666.

From the repository root, Python 3.11+ standard library, one CPU job/thread:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python3 -B round-two/six-sorting-2/native24-kernel-cover/generate.py
python3 -B round-two/six-sorting-2/native24-kernel-cover/verify.py
```

The generator checks byte hashes of the published sibling `profile.py`
and `anchors.py`. The scalar checker imports no sibling implementation,
generator or solver. It reconstructs every original clamped domain and
all 45 exact targets; a separate complete DFS obtains all 900 equal-merge
orders and checks their 45 canonical representatives on 115,200 Boolean
controls. It also checks all 24,576 literal/normalized full-input executions
and rejects three damaged certificates.

Expected status is `ALL_NATIVE24_CHECKS_PASSED`, with 745,472 original
free assignments, 45 kernels and 39 remaining targets. The final checker
took 60.535 seconds and 48,276 KiB peak RSS on Python 3.11.2. Certificate
size is 284,478 bytes; SHA256 is
`21981cab47d3b795b85d9b7c3ab8dbb5a086aba8e059d54154770ec59edcac06`.
Both implementations were authored/executed by this researcher. No
external review, formalization, size-44 sorter or global exclusion is claimed.
