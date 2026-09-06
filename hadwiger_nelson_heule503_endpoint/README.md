# The 503-vertex endpoint candidate is four-colourable

The exact induced graph H = G[M union E] has **503 vertices, 2,453 unit edges,
and a proper four-colouring**, where G is the accepted 560-vertex seed, M its
492 mandatory vertices, and

```text
E = {310,358,362,406,409,431,434,530,604,613,615}.
```

The colouring restricted to M lies **outside all 118 templates** of the
preceding complete one-pair Kempe family, even after global palette
permutation. It simultaneously colours all nine supports that fail every
template in that restricted family.

This rules out the chosen 503-vertex candidate and every subgraph of it as a
five-chromatic example. It does not decide H's larger supersets in the
560-vertex seed. No <=508 five-chromatic graph has been found, and the prior
count of **60,151,956,198,234** labelled 508-vertex supports outside the family
certificate is unchanged. The chromatic-number claim here is **at most four**;
we do not claim an exact lower bound of four.

## Selection and exact support

The [parent seed](../hadwiger_nelson_heule632_minimize/README.md) and its
[independent acceptance](../hadwiger_nelson_heule560_family_review1/README.md)
fix G and the M492/U68 partition. The
[complete one-pair Kempe interface](../hadwiger_nelson_heule560_kempe/README.md)
gave nine minimal sets on which none of its 118 mandatory colourings extends:

```text
{362,409,604}
{362,431,604}
{362,434,604}
{362,530,604}
{310,358,406,613}
{310,358,409,613}
{362,406,604,613}
{310,406,613,615}
{310,409,613,615}
```

The endpoint set E is their complete union, so H includes all nine supports
G[M union B]. This canonical union selects one actual graph with order below
509. No greedy augmentation, deletion sweep, additional support, or new Kempe
radius was used. Every displayed label is a host label, not a sparse
fresh-centre identifier. The checker derives E from the pinned previous
certificate and derives the 503 retained labels from M union E.

Coordinates use the same pinned public
[H510 data](../hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json)
and [122 fresh points](../hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json)
as the [632-point parent](../hadwiger_nelson_heule632_pair_pilot/README.md).
The first 510 labels follow the increasing union labels with `510` provenance;
fresh labels follow increasing `centre_index`. The exact coefficient basis is

\[
(1,\sqrt3,\sqrt5,\sqrt{15},\sqrt{11},\sqrt{33},\sqrt{55},\sqrt{165}),
\]

with common denominator 96. Scaled squared distance one is precisely
`(9216,0,0,0,0,0,0,0)`. The producer and independent geometry checker both
exhaust all 199,396 unordered point pairs, verify distinctness of all 632
points, and recover all 3,112 host unit edges. Restriction gives H's 2,453
edges. No approximate distance test is used.

## One exact decision and its certificate

The [frozen plan](plan.json) allowed exactly one native four-colour query on H:
Kissat 4.0.4, seed zero, at most 2,000,000 conflicts and 120 solver seconds,
with an outer 135-second timeout. Native children have address-space and
single-output-file limits of 4 GiB and 512 MiB. UNKNOWN would establish no
negative result. Any UNSAT answer would require a checked DRAT proof and the
inherited five-colouring; that branch did not occur.

For retained vertices in increasing order, variable `4*i+c+1` assigns colour
c to vertex i. The direct one-hot CNF has one at-least-one and six pairwise
at-most-one clauses per vertex, plus four unequal-colour clauses per edge.
Three unit clauses pin the exact triangle (0,143,146) to colours (0,1,2).
A proper four-colouring assigns distinct colours to these three vertices and
can be globally permuted to obey the pins, so they preserve satisfiability.
This gives:

```text
variables: 2012
clauses:   13336 = 503*7 + 2453*4 + 3
CNF bytes: 173474
SHA-256:   3728432dcc928dcccd9741bb5783b636ca0a1f76439043981daf083c7b4a8f1d
```

Two distinct geometry/CNF implementations agree on the exact formula bytes.
Kissat returned SAT with exit code 10 in **0.1176 seconds**; the complete
generation/query/check protocol took about **3.34 seconds**. Its 2,012 signed
model literals satisfy every one of the 13,336 clauses. An independent decoder
obtains exactly the published colour string. A definition-level checker then
verifies the support, colour domain and every one of the 2,453 unit edges.
Thus solver soundness and the CNF encoding are not premises of the positive
mathematical claim: the checked colouring suffices.

[certificate.json](certificate.json) contains the retained labels and a
632-character string, with `.` outside H and digits 0 through 3 on H. It is
**2,888 bytes**, SHA-256
`d44b908f71d87c1a82f06a2dc0a02eef019e3b1b42e8b3827579731bb7fea392`.
It is semantically identical to the native run's JSON result; only JSON
whitespace differs. No second native solver call was made merely to repeat
the SAT result.

## A colouring beyond the finite template family

The earlier family K is defined from one saved colouring of M: choose a
single colour pair, then exchange its colours on any union of the original
two-colour components. Take the union over all six pairs, modulo global
palette permutation. It includes arbitrary component subsets for one pair;
it does not include arbitrary sequences changing the pair or all proper
M colourings.

The checker rebuilds that entire family using the preceding independent
union-find implementation. It enumerates all **246** component-switch slots
before deduplication, obtaining **118** canonical M colourings. Their canonical
stream hash is
`faad386a59949ff5b2c22cf2b8615cf1cccd777126e09342169299c0a801c3da`.
Canonicalization orders colour classes by their first occurrence on increasing
M labels, identifying exactly global palette permutations.

The new restriction to M has canonical 632-character-string SHA-256
`4d7f9437b5f817e7a147295cebd9bef77a71dfeebf28947ba7d6b07603371625`
(dots outside M, no final newline). It is compared directly, as a string, with
every template and matches none. Hash inequality alone is not used as the
membership test. This proves that the finite one-pair restriction omits a
proper mandatory colouring useful for all nine residual sets simultaneously.
It does not prove that the new colouring belongs to a different full Kempe
equivalence class.

Restricting the new colouring gives:

| Optional set B | Vertices of G[M union B] | Unit edges |
| --- | ---: | ---: |
| 362,409,604 | 495 | 2,405 |
| 362,431,604 | 495 | 2,405 |
| 362,434,604 | 495 | 2,405 |
| 362,530,604 | 495 | 2,407 |
| 310,358,406,613 | 496 | 2,413 |
| 310,358,409,613 | 496 | 2,414 |
| 362,406,604,613 | 496 | 2,409 |
| 310,406,613,615 | 496 | 2,413 |
| 310,409,613,615 | 496 | 2,413 |

The checker directly verifies all nine restrictions, totalling 21,684 edge
inequalities. More generally every one of the 2^11 = **2,048** supports
G[M union T], T subset E, is four-colourable by restriction. Arbitrary
subgraphs of H are also four-colourable. This is compatible with the previous
template classification: its nine failures concerned the finite K, not graph
four-colourability under arbitrary M recolourings.

## Reproduce and trust boundary

The public checker needs only Python 3.11 or later and the standard library.
From this directory in a clone, with new output directories:

```sh
sha256sum -c SHA256SUMS
python3 -B verify.py --out /tmp/hn503-check
python3 -B -O verify.py --out /tmp/hn503-check-optimized
```

It imports no producing graph/CNF module or native runner. It reuses the
preceding independent checker for exact sparse-radicand geometry and complete
template reconstruction. The producer uses ordered XOR-convolution geometry.
These are author-run independent computational paths, not external review of
this new result or proof-assistant formalization.

To regenerate the native decision, build Kissat 4.0.4 at source revision
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and provide the proof checker
reserved for the conditional UNSAT branch:

```sh
python3 -B run.py --out /tmp/hn503-native \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
python3 -B verify.py --archive /tmp/hn503-native \
  --certificate /tmp/hn503-native/certificate.json --out /tmp/hn503-native-check
```

The runner enforces the executable hashes in plan.json. Recorded SHA-256 values:

```text
Kissat:    2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45
drat-trim: bc7543a99da8521ddb09af442698956054f11e10d198bd482ac756535244c021
```

The public certificate verifies without either executable. The CNF, native
model transcript and unused SAT-run proof output remain local; none is required
for checking the positive result. The optional archive audit checks every
native clause and compares the independently decoded model with its certificate.

Five damaged certificates are rejected: truncated colour string, missing
endpoint, monochromatic unit edge, wrong endpoint union and false record flag.
Normal and optimized standalone verification agree except for timing.
[expected.json](expected.json) records the exact checks;
[result.json](result.json) records the bounded native outcome;
[validation.json](validation.json) records timings and dependencies.

Trust remains in the pinned coordinate inputs, the radical basis, exact
Python integer/Fraction arithmetic, support reconstruction and direct colouring
checks. Template membership additionally uses complete component enumeration
and the palette normalization argument. No UNSAT assertion or DRAT checker
is a premise of this SAT result, and no lower chromatic bound is asserted.

## Campaign boundary

This completes the one planned candidate decision. It supplies a proper M
colouring outside the restricted family and disproves any interpretation of
the nine template failures as unconditional graph obstructions. It does not
contradict the correctly scoped preceding theorem.

The 503-point support and all its subgraphs are closed for the five-colour
target. There is no warranted increase in the previous **95.9068%** coverage
of labelled 508-point supports: a colouring of H does not automatically extend
to additional optional vertices. No such augmentation, new template projection,
further Kempe radius or additional native query was started.

The next approach needs a whole-family mechanism allowing unrestricted M
recolouring. A bounded analysis of separators and the number of boundary colour
states is a possible feasibility test before another solver campaign. This
single SAT witness does not by itself justify resuming an isolated-cut or
successive-augmentation ladder. No background computation remains.

At startup we inspected the new
[independent acceptance of the earlier three-pair interface](../hadwiger_nelson_heule560_interface_review1/README.md).
It reviews that fixed-c theorem, not automatically the subsequent Kempe family
or this candidate decision. No new overlapping teammate construction was
re-enumerated. No priority or record claim is made.
