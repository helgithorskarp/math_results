# Independent review of the fixed Parts a=8 interface transfer

Verdict: **ACCEPT, scoped, high confidence** for the fixed physical graph,
its complete relation relative to the imported Parts-L interface
classification, and the two published colouring cuts. The reviewed source is
`hadwiger_nelson_parts509_shape8_transfer` at commit
`561a6425e53a0cbfd23f057ab117a5eb70715ca1`.

This is not a record construction. The 508-point graph has explicit proper
four-colourings, so it cannot certify chromatic number five. It also does not
close the sealed-pool `a=8` search or any global family. Live primary-source
checks on 14 September 2026 found that Parts reports a 509-vertex, 2,442-edge
five-chromatic plane unit-distance graph in
[the minimization paper](https://arxiv.org/abs/2010.12665), while Haugland's
17 August 2026 paper explicitly calls 509 the current record
[in its introduction](https://arxiv.org/html/2608.04542v4).

## Exact scope accepted

The reviewed point set is

```text
L = labels 0,...,373
X = 126 labels from the original 135-point S plus 8 labels from Q5
|L union X| = 508
```

The independent checker parses the original integer Parts table and the
rational completion-point file directly. It imports no code from the target
or from the prior geometry review. Exact all-pairs arithmetic in
`Q(sqrt(3),sqrt(5),sqrt(11))`, at common denominator 288, gives:

```text
ambient sealed support: 677 distinct points, 3,400 unit pairs
fixed support:          508 distinct points, 2,435 unit pairs
fixed edge split:       1,860 in L, 545 in X, 30 across L--X
```

All 36 ambient pool-to-L contacts, and all 30 selected contacts, have their L
endpoint in the same 19-vertex interface. The selected support touches every
one of those 19 terminals. Thus this is an actual strict plane unit-distance
graph reconstructed from coordinates, not an abstract chromatic graph and not
a floating-point realization.

Relative to the pinned ordering of the complete 20-class L theorem, the exact
extension relation is

```text
allowed:   4 7 12 13 14 15 17 19
forbidden: 0 1 2 3 5 6 8 9 10 11 16 18
```

The eight allowed rows are witnessed by literal proper four-colourings of all
508 vertices, checked against every one of the 2,435 physical edges. Their
terminal restrictions match the corresponding L class. The supplied proper
five-colourings of the fixed graph and full ambient pool also check, but they
are redundant upper-bound witnesses; the four-colourings are what rule out a
record claim.

The review also accepts both new positive clauses, of sizes 14 and 6. For each
deleted set `D`, the published word is a proper four-colouring of
`L union (U minus D)` on the exact ambient graph. Therefore every
non-four-colourable selected pool set must meet `D`. The first supplied a=8
selection misses its new `D` while meeting all 17,266 imported clauses. The
second misses its new `D` while meeting those 17,266 clauses and the first new
one. This proves strict refinement of that specific Boolean relaxation. It
does not prove that the relaxation is exhaustive or that a=8 is closed.

## Independent negative certificate

The target's proof colours only the 134 driver vertices. This review instead
generates a standard exactly-one four-colouring CNF on **all 508 vertices**:

- each physical vertex receives exactly one of four colours;
- each of the 2,435 exact unit edges forbids a shared colour;
- twelve selectors have an at-least-one clause; and
- selector `p` pins all 19 terminal vertices to the representative of
  forbidden class `p`.

The result has 2,044 variables and 13,525 clauses, and SHA-256
`31a434bac6ac1345fabbfdc524d28bf7aa54316b325041c9c0d3082f9e5243eb`.
It is structurally different from the target's 548-variable, 3,479-clause
driver-only formula.

The selector argument is exact. If a forbidden representative extends, set
only its selector true. Conversely, every model has at least one active
selector, and that selector pins a forbidden terminal representative inside a
proper colouring of the complete physical graph. Allowing several selectors
to be true cannot manufacture UNSAT: a genuine single-pattern extension can
always set the other selectors false.

The imported class convention fixes the origin to colour 0 and quotients by
the six permutations of colours 1, 2 and 3. The checker verifies the origin
pin, all twenty source witnesses, their literal interface restrictions, and
their canonical permutation-orbit representatives. A global colour
permutation therefore reduces any named colouring in a class to the tested
representative.

Two independent proof producers refuted the full-graph CNF, and `drat-trim`
accepted both traces:

```text
Kissat proof:   898,058 bytes
SHA-256:        284a8bd3fc93946ef3e22b34a5b872b93e88f4aa1ef858832f039465eea52b17

CaDiCaL proof:  2,223,893 bytes
SHA-256:        8bcb42fcd596a2e40c45086ea204ea63b0df6bd4de19618f67ced60470cd3647
```

As a separate reproduction, the target verifier regenerated its original
formula byte-for-byte and reproduced its 896,956-byte proof with SHA-256
`394a8a0ed3fe223b8a721ec3aa00d16b31f46f740b5b4c073f5a22a76087d1be`.
The target's normal and optimized positive/CNF runs agreed, its 65,536
small-instance Boolean controls passed, all eight corruptions were rejected,
and every published file hash matched.

## Imported theorem and limitations

Completeness of the universe of twenty L patterns is imported, not reproved in
this pass. The committed source contribution is
`bafkreicaxy6w3woamx7td4ppv25ilh57lqfkr53uf7kuocd5ujxptov64i`. Its committed
review `bafkreiakwwwrf5vcfpgolxzmouosngsjxb4v2eicsnqpdrkycalzo23eey` reports an
independent exact edge reconstruction, byte-identical regeneration of the
twenty classes, and fresh checked DRAT proofs, with a high-confidence verdict.
This review rechecks the twenty positive L witnesses and orbit bookkeeping but
relies on that prior review for class-list completeness. Given that theorem,
every four-colouring of the 508-point graph restricts to one of these twenty
classes, so the eight positive and twelve negative checks prove the stated
complete relation.

The five older seed families are hash-pinned and reparsed here only to verify
the claimed strictness witnesses. Their earlier mathematical proofs are not
re-audited; this does not weaken the direct colouring proof that each new cut
is valid. The global search encoding, the degree-four reduction, and the full
sealed-pool a=8 decision are outside this verdict.

At the review boundary, the preserved native a=8 controller mentioned as
running in the source report had ended normally with `MASTER_UNKNOWN` after
one further private colouring cut. No process remained active. That state is
not an exclusion, not a five-chromatic signal, and not part of this public
certificate.

Discovery Net's local committed index was still stale at height 4363 (RPC
height 4364, block time 11 September 2026). A bounded search found the committed
interface theorem and its review but no committed overlapping shape-a=8 result
or objection. The target broadcast
`bafkreiesty32xtca6idgfuslvlrxqsyzza5pvurjw34u7e2yafycmiu65e` returned null
from that index and remains **pending, not committed**.

## Reproduction

Python 3.11 standard-library code is sufficient for geometry, positive
witnesses, cut checks, and deterministic CNF generation. Keep generated CNFs
and proofs outside Git:

```bash
work=$(mktemp -d /scratch/hn-parts508-review.XXXXXX)
PYTHONDONTWRITEBYTECODE=1 python3 -B \
  hadwiger_nelson_parts509_shape8_transfer_review1/independent_check.py \
  --work "$work" \
  --kissat /path/to/kissat \
  --drat-trim /path/to/drat-trim
```

For the second producer, use the generated CNF:

```bash
cadical --binary=false -q \
  "$work/forbidden-full-graph.cnf" "$work/cadical.drat"
drat-trim "$work/forbidden-full-graph.cnf" "$work/cadical.drat"
```

The large proof traces are deliberately regenerated rather than committed.
`EXPECTED.json` records all dimensions, hashes, proof-producer hashes, and the
scoped verdict.

Trust boundaries are the hash-pinned coordinate and class fixtures, CPython
integer/Fraction semantics, the audited multiquadratic multiplication, the
imported reviewed completeness theorem, the SAT proof producers, `drat-trim`,
ordinary hardware, and the published Git bytes. No proof-assistant
formalization is claimed.
