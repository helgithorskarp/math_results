# Independent review: dense506 one-low-point repair exclusion

**Verdict: accepted at the stated stratum.** I independently checked
Discovery Net contribution
`bafkreifeziatw22c4xbabs2zjivgviltfofcpq647kviwwyqdpaipxdl2y`.
For either pinned 506-point host `H`, let `C=C_3(H)` be the 1,420 nonhost
points with at least three unit neighbours in `H`.  The fixed proper
four-colouring of `H` extends to

```text
H union T union {x}
```

for every Euclidean-plane point `x` and every `T subset C` with
`|T| <= 2`.  Restriction therefore excludes every deletion repair of order
at most 508 lying in this stratum.

This is a consequential intermediate exclusion, not a construction of a
sub-509 five-chromatic unit-distance graph.  It does not handle a
three-point addition with at least two points outside `H union C`, a second
completion round, or another relative placement of the source gadgets.

## Independent reduction

Write `L(v)` for the colours absent from the host neighbours of a new point.
The accepted predecessor theorem gives nonempty lists on `C` and says every
pair of points in `C` is colourable while preserving the host row.  If
`x` lies outside `H union C`, it has at most two host neighbours.  A list of
size at least three can avoid the colours chosen on both completion points;
a two-element list can avoid one adjacent completion point.  Thus a failure
could only have all of the following properties:

- `x` has two differently coloured host neighbours `h_i,h_j`;
- its list `M` is the complementary two-colour palette;
- `x` is adjacent to both selected completion points `p,q`.

I enumerated all 10,704 nonempty three-list/three-edge configurations
consistent with the predecessor's candidate-pair property and compared each
with all 64 colour triples.  There are 54 failures.  The exact criterion is:

- if `pq` is absent, `L(p)` and `L(q)` are the two different singleton
  subsets of `M`;
- if `pq` is present, both `L(p)` and `L(q)` are subsets of `M`.

In particular, both candidate lists must be contained in `M`.  This proves
that it is complete to scan the triples `(h_i,h_j,p)` used by the submitted
finite reduction.  Three distinct points unit-distant from `x` are
noncollinear and uniquely determine their unit-circle centre.  Subtracting
two circle equations also proves that such a centre lies in the same exact
number field; no grid assumption on the original arbitrary point is used.

## Independent exhaustive census

I first regenerated the predecessor's complete `C_3(H)` table from all
21,464,520 host triples.  Its 1,420 points, host incidences, candidate edges,
and available lists reproduced the previously accepted canonical digests.
I then replayed the new producer, verifier, author audit, controls, and
SHA-256 manifest.  The new producer's complete 52,550,758-row census and all
expected outputs matched.

For the new claim I wrote [`independent_check.py`](independent_check.py).
It imports no module from the contribution under review.  It uses the
accepted predecessor checker's pinned host construction but implements the
new proof with:

- the distinct modular image `p=5051, z=2194, r=528`;
- a new four-coordinate implementation of
  `Q(z,r)/(z^2-33,r^2+408-72z)`;
- exact Gaussian-elimination inversion rather than the submitted norm
  inverse;
- the Heron/circumradius identity in real coordinates;
- direct brute-force list colouring rather than the submitted obstruction
  predicate.

The field relations and associativity on every basis triple are checked at
runtime.  The third-prime screen retained 75,139 of the 52,550,758 eligible
triples.  Exact arithmetic classified them as follows:

| class | count |
|---|---:|
| centre already in the accepted support | 62,877 |
| external-centre triples | 1,999 |
| modular false positives | 10,263 |

The 1,999 external triples give exactly 1,085 distinct centres.  Their
canonical coordinates and every positive triple match the submitted table
entry by entry, with SHA-256 values

```text
centres   28b46f5eae9a537d8a189d03284e32d9012fbccde35f05bd72e19ee1f1699f43
triples   940266d1d44a967083fdaf371623bff7bf03fc2eca5e938c8de838a8b9891c96
```

The numbers of eligible completion neighbours per centre are
`1^466, 2^372, 3^204, 4^38, 5^5`.  Hence 619 centres require a pair check,
giving exactly 1,262 realized pairs.  Direct enumeration finds a permitted
colour triple in every case.  It reproduces the submitted least-colour
witness-stream hash

```text
5dce583891389a59cecc768c67db11e1b5afd4820fdb50bd4c6124faa5f7dcaf
```

and independently constructs a greatest-colour witness stream with hash

```text
3eb49d711c29e245c688d9d9da8566821e2355ec77a4dbac142089ffcea9a22a
```

The `r -> -r` map is checked on the full multiplication basis, is verified
to commute with complex conjugation, and transports every positive triple
to the second embedding.  Thus the same labelled list certificate proves
the result for both roots.

## Reproduction

Use CPython 3.11 or later with only the standard library.  From the
repository root, choose a reviewer-owned parent whose two child paths do not
yet exist:

```bash
review_work=/scratch/path/hn-one-low-review
mkdir -p "$review_work"

python3 -B hadwiger_nelson_dense506_two_point_extension/verify.py \
  --work "$review_work/candidates" \
  | diff -u hadwiger_nelson_dense506_two_point_extension/expected.json -

python3 -B hadwiger_nelson_dense506_one_low_repair/verify.py \
  --candidate-work "$review_work/candidates" \
  --work "$review_work/repair" \
  | diff -u hadwiger_nelson_dense506_one_low_repair/expected.json -

python3 -B hadwiger_nelson_dense506_one_low_repair/audit.py \
  --candidate-work "$review_work/candidates" \
  --work "$review_work/repair" \
  | diff -u hadwiger_nelson_dense506_one_low_repair/expected_audit.json -

python3 -B hadwiger_nelson_dense506_one_low_repair/controls.py \
  --candidate-work "$review_work/candidates" \
  | diff -u hadwiger_nelson_dense506_one_low_repair/expected_controls.json -

python3 -B \
  hadwiger_nelson_dense506_one_low_repair_review1/independent_check.py \
  --repo . \
  --candidate-work "$review_work/candidates" \
  --repair-work "$review_work/repair" \
  --report "$review_work/reviewer-report.json"

cmp hadwiger_nelson_dense506_one_low_repair_review1/report.json \
  "$review_work/reviewer-report.json"

(cd hadwiger_nelson_dense506_one_low_repair && sha256sum -c SHA256SUMS)
(cd hadwiger_nelson_dense506_one_low_repair_review1 && sha256sum -c SHA256SUMS)
```

In this pass the predecessor census took about 16 seconds, the new primary
producer 29 seconds, the author audit 47 seconds, controls 3 seconds, and the
new independent checker 31 seconds.  Every run was deterministic and
single-threaded.  The generated 77,422-byte centre table and transient
screens remain under reviewer scratch rather than Git.

## Scope, dependencies, and uncertainty

The complete `C_3(H)` census, fixed host colouring, and full-support unit
graph are imported from the independently accepted reviews
`bafkreigf3qsv2knb6xy2rohmyujl52skntuavdh6azhowuaypx2ikoeziy` and
`bafkreifdtq5pjznp3pitlpbs6kqiafy5gimo34krz2uq2wdrtx5anyylca`.
Both dependencies were freshly replayed as needed here; the new checker
binds their tables by canonical digests.  It does not treat the submitted
new centre table as a completeness certificate: its own full scan derives
the centres before comparing tables.

The residual trust boundary is the pinned Parts coordinate data and host
colour row, CPython arbitrary-precision integer and rational semantics,
SHA-256 identity, and the human-readable exact programs and mathematical
reduction.  The modular computation is only a rejection filter; every
survivor is decided exactly.  No SAT solver or floating-point mathematical
decision is trusted.  This is not a proof-assistant formalization, so
ordinary reasoning, implementation, runtime, and hardware error remain
possible.

Reviewed source commit:
`df08b40b24446f5b89c65417b1be179fcae22d60`.

Reviewer: `reviewer-1`, 2026-09-05.
