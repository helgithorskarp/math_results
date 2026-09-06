# H517: the two-large-deletion family is four-colourable

**Every graph obtained from H517 by deleting two large vertices and seven
small vertices is four-colourable.** By restriction, the same holds when
at most 373 large and at most 135 small vertices are retained, or edges
are removed.

Together with the [134-small closure](../hadwiger_nelson_heule517_small134/README.md),
this proves that every non-four-colourable H517 subgraph on at most 508
vertices must have **at least 136 small vertices and at most 372 large
vertices**. It must delete at least three large vertices. The unrestricted
at-most-508 family remains open. No record graph or unconditional lower
bound of 136 small vertices for larger graphs is asserted.

## Exact graph and inherited inputs

G is the fixed [H517 support](../hadwiger_nelson_heule517_family_pilot/README.md),
source `59d634e906f6c6ed5945c0180b5352ba03c3babd`. It consists of the
510 increasing union-certificate labels marked `510`, followed by the
completion-centre indices 327,439,671,1040,1074,1377,1383. G indices
0..509 are those sorted union labels; 510..516 are the seven centres
in that order. They are not the original Heule or Parts indices.

The 517 distinct coordinates have denominator 96 in the positive-radical
basis 1,sqrt(3),sqrt(5),sqrt(15),sqrt(11),sqrt(33),sqrt(55),sqrt(165).
L consists of the points with zero coefficients of sqrt(5),sqrt(15),
sqrt(55),sqrt(165) in both axes; S is its complement. The complete exact
unit graph has |L|=375, |S|=142 and 2555 edges: 1920 in L, 605 in S
and 30 between blocks. [manifest.json](manifest.json) pins the coordinate
inputs, earlier colourings and reused code.

The starting evidence comprises 526 rows of the full H517 pilot and
202 rows of the small134 certificate, source
`adad2a4b42cf76e507ecbe1e8d4ccf23ca231a4d`. Each row supplies a proper
four-colouring of G minus a nonempty set D. A non-four-colourable subgraph
must therefore intersect D. The new theorem checks these positive
witnesses directly, without relying on an earlier negative SAT result.

## Complete family reduction

The 202 small-only cuts force 120 vertices of S. Their other 22 small
vertices are

```
U = [358,359,360,361,362,370,378,379,393,395,399,432,434,
     459,505,510,511,512,513,514,515,516].
```

Of all binomial(22,7)=170544 seven-subsets O of U, exactly 167 avoid
containing a small-only cut D. Any omission set containing a forced
vertex or a cut already has a four-colouring. No symmetry or sampling
is used in this enumeration.

For each of the 167 survivors, inspect every inherited cut D. All such
cuts have at most one large vertex. If its small part is contained in O,
its unique large vertex must be retained by a non-four-colourable graph.
These conditional requirements reduce the possible large omission pairs.
The number of eligible large vertices ranges from zero to 141, and the
total number of pairs across all 167 cases is **870215**.

The pair count concerns candidates not yet covered by the inherited
colourings, not non-four-colourable graphs. In particular the seven
added vertices form one small omission case with zero eligible large
vertices: inherited witnesses already cover every large deletion there.

## New positive certificate and proof

[certificate.json](certificate.json), 48531 bytes, gives 86 proper
four-colourings of G minus D. A row has the increasing G omission list
`D`, a 517-character `colouring` with digits 0..3 and dots exactly at D,
and a `native_index` recording the zero-based original run position.
That last field is provenance; no unpublished run is needed to decode
or verify a public witness.

The new rows have 48 singletons, 27 pairs, nine triples and two four-sets.
They are selected from 143 native witnesses by inclusion: each omitted
native witness has an omitted set containing one of these 86 sets.
The checker tests all 86 full colourings on the exact graph. It then
enumerates every one of the 870215 surviving pairs {a,b}, and verifies
that some new D is contained in O union {a,b}. Restricting the supplied
colouring of G minus D proves that candidate is four-colourable.

This covers all two-large/seven-small deletions: those excluded initially
inherit an old colouring, and all remaining ones inherit a new colouring.
Any graph retaining at most 373 large and at most 135 small vertices can
be enlarged to one of these 508-vertex supports, so it too is colourable.

For the target corollary, let X have at most 508 vertices. If X uses at
most 134 small vertices, the earlier positive eight-omission cover applies.
If X uses exactly 135, it uses at most 373 large vertices and the new
theorem applies. Thus a non-four-colourable X needs at least 136 small
vertices, leaving at most 372 large vertices. The checker also rechecks
all 319770 eight-subsets in the inherited proof, so this corollary needs
only exact coordinates, positive colourings and finite enumeration.

## Bounded full-graph discovery

The [frozen plan](plan.json) allowed at most 256 native queries, each
with 100000 conflicts and 4 GiB address space. The producer cycles through
the lexicographic small omission cases, choosing the lexicographically
first uncovered large pair in each. It stops on complete coverage, a
certified target, UNKNOWN, or the query limit. No limit was extended.

Each query uses the full H517 colouring formula with all 517 activation
values specified. There are four colour variables per vertex and one
activation variable per vertex. The clauses are guarded at-least-one
colour constraints, four inequalities per unit edge, and a guarded
origin-colour normalization. There are 2585 variables and 10738 clauses.
Inactive vertices can have every colour variable false. At-most-one
clauses are unnecessary: adjacent true-colour sets are disjoint and
choosing one true colour at each active vertex produces a colouring.
The origin normalization applies only when that vertex is present.

The candidate colouring is checked directly, then greedily extended over
omitted large vertices followed by omitted small vertices. The result
is checked again. Every family member avoiding its residual D is removed.
The full graph oracle admits all compatible colourings after large
deletions; it does not assume the 20 intact-L patterns remain complete.

Coverage finished after **143 queries, all SAT**, touching 90 of the
167 small omission cases. Other cases were covered by colourings found
elsewhere. There were no UNKNOWN answers, negative targets or proof traces.
The native run took 17.7183 seconds with peak RSS 118848 KiB. Its full
143 witness rows remain local; the 86 retained rows replace them in the
public proof. [run_summary.json](run_summary.json) records the result.

The [producer](run.py) includes a bounded fresh Kissat/DRAT/five-colouring
branch for a negative target. That branch was not exercised. No negative
native answer is a premise of this theorem.

## Reproduction and independent checking

In a full repository checkout, from this directory:

```bash
python3 -B verify.py --report /scratch/heule517-large2-check.json
sha256sum -c SHA256SUMS
```

Python 3.11.2 and the standard library suffice. Expected output includes
`large_pairs_checked=870215`, `remaining_pairs=0` and
`small_vertices_needed_by_any_at_most508_nonfour_subgraph_at_least=136`.

[verify.py](verify.py) imports the hash-pinned independent monomial
geometry routine, not the producer or a SAT solver. It reconstructs all
133386 pair distances, checks the 526 earlier full witnesses (1336627
edge inequalities), the 202 earlier small witnesses (513249), and the
86 new witnesses (218392). It then performs the complete seven-omission
enumeration, conditional large-pair reduction and 870215-case cover,
as well as the inherited eight-omission proof.

The additional author-run `--work /path/to/native-run` audit compared
all 143 native witnesses (362434 edge inequalities), their public subset,
the entire round-robin transcript, every removal count and the actual
activated CNF entry by entry. It took 17.1014 seconds, including 3.7982
seconds for the coupled cover. [verification.json](verification.json)
records that audit. The public-only checker verifies the same theorem
without native files. The checker is independently implemented and
author-run; no separate-author review or formalization is claimed.

Discovery used python-sat 1.8.dev24 and CaDiCaL 1.9.5. To reproduce the
frozen run in a fresh external directory:

```bash
python3 -B run.py --work /scratch/heule517-large2-fresh \
  --kissat /path/to/kissat --drat /path/to/drat-trim
```

Kissat 4.0.4 and drat-trim would be invoked only for a negative target.
The actual activated CNF SHA256 is
`21fcfe71a6162a4ac3577456d50e607479dd2358001991e814e49aa95ff29a9f`.
Native formulas, logs and checkpoints are external. Exact coordinate
data, Python integer arithmetic, witness decoding and the complete
finite cover are the proof boundary; floating-point approximations,
negative solver trust and an omitted large proof are unnecessary.

## Decision and next boundary

This whole family is closed; extending its query budget is unnecessary.
The next proposed bounded target family deletes three large vertices
and six small vertices, retaining 372+136=508. It can reuse every
published positive colouring. That new level has not started. The
unrestricted H517 family and the <=508 record objective remain open.

HN-3's separate unit-spindle contact closure was inspected at source
`bed7c367371df2024cb5e9428885333b1d85760c`, Discovery Net height 3114.
It colours 126 elimination supergraphs and leaves only the unenumerated
both-nonunit contact family, bounded by 960 rotation classes. Its result
supplies no premise here. No background job or unfinished proof remains.
