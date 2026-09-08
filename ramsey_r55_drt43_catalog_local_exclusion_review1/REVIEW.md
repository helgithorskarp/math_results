# Review of h3989: exclusion of 2,178 supplied DRT(43) order families

## Verdict and scope

**ACCEPT, subject to the explicit SAT-engine and pinned external-input trust
boundary below.** For every one of the 2,178 records in the file with SHA-256
`fde36db6e2e4e07e9c1ec5df32ffc0eb262705393be686fc41a7f31bdc149d6d`,
and every linear order of its 43 vertices, color a pair red when its
tournament arc points from the earlier to the later vertex.  The resulting
two-coloring contains a red `K5` or a blue `K5`.

This is a terminal exclusion only for the pinned supplied records.  Brendan
McKay's live data page labels the 43-vertex, 2,178-record DRT collection
"incomplete."  The result does not exclude all DRT(43)s, all ordered
tournaments, or all 43-vertex graphs.  It constructs no good43 graph and
does not prove `R(5,5) >= 44`.

Reviewed contribution: Discovery Net h3989,
`bafkreigcszuyvdygn55i5xslewjjnacpr5cnlnnyjzpk5t5qksz5dkyxqu`.
Reviewed source commit:
`93242be92b95d9918582152fdd754014b44010de`.

## Independent reduction

Fix a tournament `T`, a linear order, and its first vertex `r`.  Put
`Q=N_T^+(r)`.  Every pair from `r` to `Q` is red.  Hence a coloring without a
red `K5` can have no forward transitive four-set in the induced order on
`Q`.  A blue `K5` in `Q` is exactly a transitive tournament five-set whose
unique source-to-sink order occurs in reverse.  Thus a good global order
would induce on `Q` an order with neither a forward transitive four-set nor
a backward transitive five-set.

Every audited record is doubly regular of order 43, so every root has exactly
21 outneighbors and each induced `T[Q]` is a regular tournament of order 21.
It is therefore enough to refute the stated local ordering condition for all
`2,178 * 43 = 93,654` rooted outneighborhoods.

For a labeled 21-vertex local tournament, use one Boolean comparison for
each of the 210 unordered pairs.  Two clauses per triple exclude the two
directed comparison cycles.  Since all pair comparisons are present, the
resulting comparison tournament is triangle-free exactly when it is a
linear order.

Each transitive tournament four-set has a unique source-to-sink sequence
`v0,v1,v2,v3`.  The three-literal clause negating
`v0<v1<v2<v3` excludes precisely its forward occurrence.  Similarly, the
four-literal clause negating `v4<v3<v2<v1<v0` excludes precisely the reverse
occurrence of each transitive five-set.  Consecutive comparisons suffice
because the comparison clauses enforce transitivity.

The reviewer formula does not use the source's selector variables.  Instead,
it separately assumes each of the 21 possible first local vertices precedes
the other 20 vertices.  Every linear order has exactly one first vertex, so
UNSAT for all 21 branches proves the unsplit formula UNSAT.  Checking all 43
global roots for every supplied record then proves the exact catalog claim.
Only this necessary local condition is used; no converse from a local order
to a globally good coloring is asserted or required.

## Independent computation

The reviewer C++ checker imports no source implementation.  It uses 64-bit
adjacency masks, rechecks every supplied record's outdegrees and common
outneighbor counts, constructs each 21-vertex local tournament, identifies
transitive subsets from local score sequences, and generates the comparison
clauses directly.  Fixed-width operations shift only by indices 0 through
42, and all global counters are unsigned 64-bit integers.

The full one-process receiving run completed in approximately 3,982 seconds
with these exact totals:

```text
catalog records                  2,178
root formulas                   93,654
first-position branches      1,966,734
reviewer base clauses        508,658,864
source selector clauses       39,428,334
reconstructed source clauses 548,087,198
SAT / UNKNOWN branches                  0
```

The source adds one selector disjunction and 420 selector implications per
root.  Thus its overhead is exactly `93,654 * 421 = 39,428,334`.  The
reviewer checks the resulting clause count against every one of the 2,178
source transcript rows, not merely the grand total.  The 73,058-byte result
receipt has SHA-256
`b70aac40f58e54d5d0995eb015f44be5d73a0cfe04ab7f85e88810f578027402`.
A separate Python receiver rechecks the input DRT identities, both transcript
hashes, all rows, the branch product, and every count relation in normal and
`python3 -O` modes.

The full independent sweep used CaDiCaL 3.0.1 at commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04`, with a fresh generator and
the explicit 21-way first-position exhaustion.  Four spread-out controls
`0:0`, `1:0`, `1089:21`, and `2177:42` were independently encoded without
the case split and solved UNSAT using Kissat 4.0.4 at commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`.  The reviewer code also passed
AddressSanitizer and UndefinedBehaviorSanitizer on all 43 roots of record
zero.  The source package manifest and lightweight audit pass in normal and
optimized Python modes.

Reproduction command:

```sh
python3 -B ramsey_r55_drt43_catalog_local_exclusion_review1/reproduce.py \
  . /scratch/research-team-v2/tmp/reviewer-1/reproduce-h3989 \
  --cadical-dir /path/to/cadical-c607304 \
  --kissat-dir /path/to/kissat-8af8e56
```

Expected status: `REPRODUCED_ACCEPT_REVIEW_H3989`.  The work path must not
already exist.  Expect roughly 70 single-core minutes on hardware comparable
to the review host.

## Imported and residual trust

The source reports that `drat-trim` checked 93,654 transient CaDiCaL proof
streams totaling 2,482,356,972 bytes before deletion.  This review audits
that compact transcript but does not pretend it is a proof certificate: the
proof streams were not retained, regenerated, or independently replayed.
The verdict instead includes a complete fresh decision sweep.  Consequently,
CaDiCaL's correctness remains an explicit trust boundary for the complete
finite UNSAT conclusion; the limited Kissat controls do not remove that
boundary.

The input bytes are pinned and every record is directly audited as a DRT, so
the mathematical claim does not require trusting a catalog classification or
nonisomorphism assertion.  It does require trusting that the pinned bytes are
the intended McKay file; the live source page and fetched SHA agree.  The
page's explicit incompleteness label is essential to the scope.

Residual trust comprises the reduction above, source and reviewer generator
and receiver code, CaDiCaL for the full sweep, Kissat for four controls,
compiler and exact machine-integer semantics, SHA-256, Git archive semantics,
CPython, the operating system, and hardware.  No randomized search,
floating-point predicate, full DRT classification, graph-isomorphism package,
or lower-bound theorem is imported.  Historical novelty is not assessed.
