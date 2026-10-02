# Native 21-gate prefix excluded at size 44

The [P21 six-history theorem](P21.md) excludes every standard completion
of the first **21** ordered native comparators at total size at most44,
with arbitrary suffix order and depth. Three fixed two-high histories fill
the entire ordinary budget after every possible singleton maximum chain;
three further histories contradict that budget for every intervening
preparation word. The alternate direct-merge branch imports P22 below.
P21's minimum total size lies in45..46 and its suffix size in24..25.
The unrestricted thirteen-input44..45 gap remains open.

Author and executing agent: **six-sorting-2**, role **researcher**,
2026-10-02. This is an unformalized author proof with same-author
algorithmic independence, without an external review verdict.

Run p21_generate.py, then the standalone p21_verify.py with Python3.11+
and the standard library. Expected status NATIVE21_SCALAR_CERTIFICATE_VERIFIED.
The [fixture](p21-fixture.json), [certificate](p21-certificate.json)
and [validation](p21-checks.json) are compact; the checker replays624
complete original pair domains and all1277952 free assignments.
[P21.md](P21.md) gives the complete arbitrary-preparation argument,
imported P22 boundary, primary attribution and exact commands.

Earlier P22 result

Author and executing agent: **six-sorting-2**, role **researcher**, 2026-10-01.

The [P22 complete equality cover and exclusion](P22.md) excludes every
standard size-at-most-44 completion of the first **22** native comparators,
at arbitrary subsequent order and depth. All three minimum matchings are
covered; the two new matchings give90 literal roots, each excluded by a
selected nested mass. The479 original domains are reconstructed by a
different scalar algorithm. P22's minimum total size lies in45..46; the
unrestricted thirteen-input44..45 gap remains open.

Run p22_generate.py cover, p22_generate.py roots, p22_verify.py cover and
p22_verify.py roots, in that order, using Python3.11+ and the standard
library. Both check stages return NATIVE22_SCALAR_CERTIFICATE_VERIFIED.
The compact [cover](p22-cover.json), [original-domain fixture](p22-fixture.json)
and [nested certificate](p22-nested.json) contain the complete reproducible
evidence. [P22.md](P22.md) gives the universal coverage argument, dependency
boundaries, checks and exact commands.

The [P23 saturation lift](P23.md) excludes every standard size-at-most-44
completion of the first **23** native comparators, at arbitrary depth.
Its complete two-minimum profile forces the next live event (2,4) to
commute forward, producing the already excluded P24. All 78 standard
last-gate replacements after this fixed P23 are therefore excluded.
Reproduce with p23_generate.py and the standalone p23_verify.py;
expected status is ALL_NATIVE23_SATURATION_CHECKS_PASSED.

The [nested semantic class theorem and certificate](NESTED.md) exclude
every standard size-at-most-44 completion of the literal native 24-gate
prefix, at arbitrary suffix order and depth. The uniform packet checks
all 45 canonical roots in the original complete cover, using 236 selected
original clampings. It closes the fourteen remaining native-prefix cases.
The unrestricted thirteen-input size interval remains 44..45.

Reproduce the current result with Python 3.11+ and the standard library:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 round-two/six-sorting-2/native24-kernel-cover/nested_generate.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 round-two/six-sorting-2/native24-kernel-cover/nested_verify.py
```

Expected status: `ALL_NATIVE24_NESTED_CHECKS_PASSED`, 45 roots, 236
selected domains and zero remaining native-prefix targets. The compact
[certificate](nested-certificate.json) and fixed selected
[fixture](nested-fixture.json) are independently replayed by the standalone
numeric checker. [NESTED.md](NESTED.md) gives the universal proof,
imported-cover boundary, primary attribution and validation details.

The preceding [three-budget normalization and correction refinement](NORMALIZE.md)
excludes ten further original kernels6,7,10,16,18,25,29,30,37,40. Combined
with the credited peer [9/21 exclusion](../../six-sorting-1/joint_extreme_kernel_barrier/PROOF.md),
the native standard size44 question was equivalent to **14 nine-wire
targets at budget12**, with arbitrary order and depth. Exact surviving
IDs and selected original-domain certificates are in
[normalize-certificate.json](normalize-certificate.json). Reproduce with
`normalize_generate.py` and the standalone scalar `normalize_verify.py`.
The new bridge forces `(3,4),(2,3)` to commute to the front in those ten
branches, then proves45-gate lower bounds by a required marked-port
correction. The global13-input44..45 question remains unresolved.

The preceding [paired-touch refinement](TOUCH.md) excluded six initial kernels
3,4,5,12,27,28. Together with six-sorting-1's separately credited
[kernel0 exclusion](../../six-sorting-1/six_extreme_kernel_barrier/PROOF.md),
this gave an equivalent **26-target nine-wire question at budget12**.
The local touch certificate alone certifies the27-target intermediate
refinement. It also proves that wire2 is touched exactly once, by `(2,3)`,
in every completion of the preceding33 targets. Original clamping budgets
are transferred through future moving markers by a fixed carrier
permutation. Reproduce the compact certificate with `touch_generate.py`
and the standalone scalar checker `touch_verify.py`. Earlier pinned
certificates and implementations are unchanged.

The earlier [endpoint-deletion refinement](ENDPOINTS.md) excluded all four
then-remaining eight-wire cases, giving an equivalence with
**33 nine-wire targets at budget12**. Its compact certificate and
standalone scalar checker are `endpoint-certificate.json` and
`endpoint_verify.py`; the original dependency files remain unchanged.

The first [third-minimum refinement](MINIMUM.md) excluded two kernels
and reduced four others to eight wires. Its intermediate disjunction
has **33 nine-wire targets at budget12 and four eight-wire targets at
budget10**. [minimum-certificate.json](minimum-certificate.json) and the
separate producer/checker reproduce this refinement. The original
39-case certificate and proof below remain unchanged as its dependency.

The original result for the literal first 24 gates of Dobbelaere's
`N13L46D9` said that a standard
sorting extension of total size at most 44 exists **iff one of 39 explicit
nine-wire Boolean images has a sorting word of size at most 12**.
No depth restriction is imposed. The global thirteen-input minimum
remains 44..45. Later linked refinements exclude all of those39 targets.

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
