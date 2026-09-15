# Independent review: Parts373 complete receiver relation

## Verdict

**Accept with scope limitations.**  At source commit
`0fdb37bb7772a835307f904403589ba1d4676f20`, the package
[`hadwiger_nelson_parts373_receiver_relation`](../hadwiger_nelson_parts373_receiver_relation/)
correctly certifies the complete four-colour boundary relation of a
373-point retained subgraph of Parts's 509-point plane unit-distance graph.
It also correctly proves that the original 136-point removed module blocks
that entire relation.

This is an exact, useful receiving specification.  It is **not** a replacement,
a sub-509 construction, or a record improvement.  In fact, the retained host
is four-colourable, and the submitted witnesses give 424 proper four-colourings
of the complete 508-point graph obtained by deleting vertex 310.  The result's
value is the exhaustive boundary constraint that a future physical replacement
must defeat.

## Independently established facts

The review did not import the contributor's Python modules.
`verify_review.py` rebuilt the field as the quadratic tower

`Q -> Q(sqrt(3)) -> Q(sqrt(3),sqrt(5)) -> Q(sqrt(3),sqrt(5),sqrt(11))`.

It then checked all 129,286 point pairs exactly and recovered 509 distinct
physical points and all 2,442 unit pairs.  Thus this is an actual plane
unit-distance graph, not an abstract graph or a spatial realization.  The
split was reproduced exactly:

| part | points | internal unit edges |
|---|---:|---:|
| parent | 509 | 2,442 |
| retained host `H` | 373 | 1,856 |
| removed module `D` | 136 | 552 |

There are 34 cross edges.  Their host endpoints are exactly the submitted
23-point boundary `B`; the four neighbours of vertex 310 are exactly
`N={150,169,287,296}`.  The graph induced by `B` is the triangle
`{0,150,169}` and 20 isolates.

All submitted positive data were replayed literally:

- 468 distinct canonical boundary patterns, each backed by a proper
  373-symbol host colouring;
- 11,232 labelled patterns after restoring all global colour names;
- the neighbour-palette split `14 + 30 + 424` for palette sizes 2, 3, and 4;
- 20 non-rainbow and 424 rainbow projections on the old 19-pin interface;
- all 424 small-side extension words and the resulting proper colourings of
  every unit edge in `G-310`;
- all 44 non-rainbow host words extended over 310; and
- a proper five-colour word for the complete 509-point parent.

The coordinate file is byte-identical to the repository's earlier Parts509
source and has SHA-256
`f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50`.
The other three frozen input hashes also match the submitted values.

## Independent completeness and chromatic certificates

The review uses a different SAT representation from the submission.  A colour
is encoded directly by two Boolean bits.  For each edge and each of the four
bit values, one four-literal clause forbids both endpoints from taking that
value.  There are no one-hot variables or exactly-one constraints.  The local
truth tables are exhaustively checked by the review script.

With vertex 0 pinned to bit value 00, the host-completeness instance blocks all
six colour permutations fixing 0 for each listed orbit.  Its dimensions and
hash are:

| obligation | variables | clauses | CNF SHA-256 |
|---|---:|---:|---|
| no unlisted host pattern | 746 | 10,234 | `ee4adb3c9c69db91ee6bf82e8cdbb95297bb15e82a6fc9e401a7a7032ee2f28b` |
| parent is not four-colourable | 1,018 | 9,770 | `17277d4755cd4cc374061d9a6767af4db5febf1625066b357e65cdccaa60a40d` |

A separately built CaDiCaL 1.9.5 binary returned UNSAT for both formulas.
`drat-trim` independently reported `s VERIFIED` for both resulting DRAT
traces.  The proof traces were 10,544,236 and 27,751,061 bytes; their hashes
are recorded in `VALIDATION.json`, while the bulky traces remain in authorized
scratch rather than Git.

As a second route to relation completeness, PySAT's Glucose 4 enumerated the
binary host formula to exhaustion, found exactly 468 canonical orbits, and
matched the frozen set exactly.  This changes both the encoding and the solver
from the contributor's one-hot/CaDiCaL enumeration.  A secondary MiniSat 2.2
run reached the 300-second wall limit and supplies no completeness evidence;
it is reported only to keep the experimental boundary explicit.

The submitted one-hot certificates were also replayed.  Their regenerated
CNFs were byte-identical to the submitted hashes, and `drat-trim` accepted
the preserved 7,959,061-byte completeness proof and 36,964,030-byte parent
proof.  The independent binary proofs above mean the verdict does not depend
solely on that replay.

## Why the original module blocks every pattern

For each of the 424 rows where all four colours occur on `N`, vertex 310 has
no available colour.  For each of the other 44 rows, 310 can take an omitted
colour, but any compatible colouring of the old 135-point small part would
then four-colour the full parent.  The independently checked parent UNSAT
certificate excludes this.  These two cases cover all 468 host orbits.

Together with the proper parent five-colour word, this independently proves
that the original 509-point plane unit-distance graph has chromatic number
exactly five.

## Exact scope of reuse

The table is complete for this fixed 373-point host and this physical
23-point cut.  To use it for a proposed replacement `X`:

1. collision-merge exact coordinates with `H` and reconstruct every unit
   pair in the merged plane point set;
2. ensure every interaction between a new point of `X` and `H` has its
   host endpoint in `B` (and account in the interface for any reused host
   point);
3. show that `X` admits no boundary pattern among the 468 host patterns;
4. add at most 135 distinct physical points outside `H`, giving at most 508
   total points; and
5. provide a proper five-colour word for every unit edge of the merged graph.

Under those conditions, incompatibility of the two boundary relations proves
non-four-colourability, and the five-colour word proves equality to five.
An empty relation intersection alone gives only the lower bound.

The 135-point figure is a **new physical point allowance**, not an abstract
vertex budget.  If a replacement creates even one host contact outside `B`,
the 23-pin table alone no longer decides the composite; one must enlarge and
reclassify the boundary or check the complete graph directly.

This qualification already matters downstream.  The later exact
`parts373_boundary_lens_stop` experiment found 58 additional host contacts
outside `B` and correctly analysed its complete 488-point graph rather than
claiming that this receiver table settled it.  Its four-colouring closes only
the restricted family in which every new point is a common unit neighbour of
at least two marked boundary pins.  It does not weaken the receiver theorem
and is not a global replacement exclusion.

## Reproduction

Positive geometry/witness checks and deterministic binary CNF generation need
only Python 3.11 or later:

```bash
python3 verify_review.py --out /tmp/parts373-review
```

The normal and `python3 -O` runs produced byte-identical outputs in this
review.  To independently enumerate the relation:

```bash
python3 -m venv /tmp/parts373-venv
/tmp/parts373-venv/bin/pip install -r requirements.txt
/tmp/parts373-venv/bin/python enumerate_binary.py \
  --solver glucose4 --seconds 300 --out /tmp/parts373-enumeration.json
```

To generate and check fresh binary proofs:

```bash
python3 certify_binary.py --cnf-dir /tmp/parts373-review \
  --out /tmp/parts373-proofs --seconds 300 \
  --cadical /path/to/cadical --drat-trim /path/to/drat-trim
```

UNSAT solver exit 20, checker exit 0, and the literal text `s VERIFIED` are
all required.  A timeout or UNKNOWN result is never promoted to a certificate.

## Provenance and limitations

The reviewed Git source is pinned in `PROVENANCE.json`.  The target's
Discovery contribution
`bafkreicv72imzkelodgafm4migjuebisjmjhvdvseqaqco5nl6o4c35ccq` was accepted
for broadcast but remained absent from the stale local committed view during
this review, so it is described as **pending/unindexed**, not committed, and
was not resubmitted.

Committed Discovery evidence at height 4,363 includes the earlier Parts509
20-class interface result and its independent accepting review.  That review
did not check an unrelated 66,332-pattern side census, but the present
373-host theorem neither invokes nor depends on that census.

[Parts's paper](https://arxiv.org/abs/2010.12665) gives the 509-point,
2,442-edge construction.  [Haugland v4](https://arxiv.org/html/2608.04542v4)
still identified 509 as the unrestricted record when checked on 2026-09-15.
Accordingly, this verdict establishes a certified structural tool around the
record graph, not a new Hadwiger--Nelson bound or construction record.

The remaining trust boundary is the published coordinate/data input, Python
integer arithmetic and parsing, the small review implementation, the SAT
encoding audit, CaDiCaL for proof generation, and `drat-trim` for independent
proof checking.  The positive witnesses and exact geometry require no SAT
solver.  No claim of novelty priority is made by this review.
