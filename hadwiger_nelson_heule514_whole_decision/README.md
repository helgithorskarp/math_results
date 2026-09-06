# Every H514 subgraph on at most 508 vertices is four-colourable

**Computer-assisted theorem.** Every subgraph of the fixed exact H514
unit-distance graph on at most **508 vertices** has a proper four-colouring.
This closes the entire deletion-only family, including edge-deleted
subgraphs. It produces no five-chromatic graph or record improvement.
There is no assertion that H514 contains a five-chromatic 509-vertex graph.

The proof below is a direct certificate on the whole support. It needs
**503 mandatory vertices and only 462 omission patterns**, rather than any
of the earlier 258,914-, 190,536- or 8,974-case residual censuses. Those
censuses explain the discovery route but are not premises of this direct
proof. All colourings and unit edges are checked explicitly.

## Fixed exact support

H514 has 514 distinct points and 2,526 complete unit edges. Its old 510
points are the increasing union labels marked `510` in the
[archived H510 certificate](../hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json).
New indices 510,511,512,513 are the fixed completion centres
170,436,1239,1527 from the
[exact completion table](../hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json).
The induced graph on the four new vertices is the path in that order.

Coordinates lie in the positive squarefree basis
`1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165`, with denominator 96.
The independent geometric checker reconstructs every point and all
131,841 unordered pair norms, so the full unit-edge graph, not a selected
edge list, is checked. The result applies to this support and its common
isometric images. It does not close other centre choices, larger
universes, or arbitrary unit-distance configurations.

## Positive witnesses and mandatory vertices

A positive omission witness consists of a set D and a proper four-colouring
of H514 minus D. It is stored as 514 characters in `0,1,2,3,.`, with dots at
exactly D. If a proposed subgraph omits all of D, restrict this colouring.
For a singleton D={v}, any non-four-colourable subgraph must therefore
contain v.

The checker decodes and directly verifies:

| Source | Positive witnesses | Singleton cuts |
|---|---:|---:|
| [Original H514 library](../hadwiger_nelson_heule514_interface/certificate.json) | 516 | 484 |
| [Frozen-profile pilot](../hadwiger_nelson_heule514_profile_pilot/certificate.json) | 15 | 9 |
| [New whole-family certificate](certificate.json) | 13 | 10 |
| Total | 544 | 503 |

These singleton indices are distinct. The new 13 omission sets are:

| Size | D |
|---:|---|
| 1 | {59}, {236}, {257}, {294}, {313}, {321}, {331}, {398}, {448}, {466} |
| 2 | {214,344}, {344,433}, {433,439} |

The new certificate is **8,006 bytes**. It is obtained by removing
supersets from the 25 newly checked witnesses, not by asserting globally
minimum certificate size. Some positive witnesses need not be used by the
first-eligible covering rule.

After the singleton forcings, the only 11 vertices a non-four-colourable
subgraph could omit are

```text
152,214,344,433,439,497,500,510,511,512,513.
```

The imported witness decoder uses archived positive colourings, including
compressed recipes originally discovered on H517. It does not invoke an
H517 negative theorem or repeat that retired support's geometry/search.
Every expanded H514 witness is checked anew on the exact H514 unit edges.
There are **1,368,406 retained-edge inequalities** across all 544 witnesses.

## Direct proof with 462 cases

Let G be any H514 subgraph on at most 508 vertices. If it misses a mandatory
vertex, its singleton witness already four-colours G. Otherwise it contains
all 503 mandatory vertices and at most five of the 11 free vertices.
Enlarge its vertex set to exactly 508 vertices within H514 and include all
induced unit edges. It suffices to colour each such supergraph.

There are exactly `binomial(11,6)=462` ways to omit six free vertices.
For **458**, an entire positive omission set D is contained in the omitted
set O, so its colouring restricts immediately. The remaining **four** are:

| O |
|---|
| {152,214,433,497,500,512} |
| {152,214,433,497,512,513} |
| {152,433,497,500,510,512} |
| {152,433,497,510,512,513} |

In each of these four induced graphs, vertices **299 and 302** both have
current degree at most three and can be peeled in one simultaneous round.
The remaining graph omits vertex 299, so the archived singleton witness
H514 minus {299}, canonical original-library index 288, colours it.
Restore 302 and then 299, each with at most three already-coloured neighbours,
using an available fourth colour. This colours the original 508-vertex
induced graph.

The checker independently enumerates all 462 omission tuples, tests full
set containment, computes the simultaneous peel, restricts the chosen
colouring and restores the peeled vertices. It checks the final colouring
against every retained unit edge in every case: **1,146,726 target-edge
inequalities**. All original omissions are preserved. Restricting these
colourings handles smaller vertex sets and edge deletions, proving the
theorem.

[direct_certificate.json](direct_certificate.json) records the four cases
and their witness data. The deterministic 462-line first-witness tag stream
has 6,252 bytes, SHA-256

`a8755fe2bac2ff2a13c2e7b19f0d69e3a168baf43ea7c82ad8c7e8116bc5f33c`.

This is a direct finite proof of the full support claim. It needs no
correctness assumption about the prior residual enumerations or their
profile partitions.

## Discovery run and separate historical audit

The standing handoff was the exact
[8,974-core remainder](../hadwiger_nelson_heule514_profile_pilot/README.md),
with 817 cores of order 507 and 8,157 of order 508. Before querying,
[plan.json](plan.json) froze its complete 215,488-byte input, SHA-256

`8f0448c4d9f9cdd0c7f7d1fa1e69aef3ab6d7a368b0cfc6782ea7debedb8a38e`.

The driver processes every row in canonical `(omission count, tuple)` order,
skipping only if a previously checked positive omission set is contained
in that row. Otherwise it uses the pinned
[optional-P4 projected formula](../hadwiger_nelson_heule514_path_projection/README.md),
with 2,052 variables, fixed origin colour zero and no additional symmetry
breaking. It calls a fresh CaDiCaL 1.9.5 worker through python-sat 1.8.dev24,
with defaults, no assumptions or retained learned clauses. The limits were
100,000 conflicts and 60 seconds per candidate, 4 GiB worker address space,
1,800 seconds for the finite traversal, at most 8,974 target calls, and no
retries. The worker is the unchanged previously controlled implementation.
No new abstract solver-control calls were needed.

The run completed with **25 SAT calls and 8,949 positively covered rows**.
There was no UNKNOWN, UNSAT, unqueried case, worker failure or limit
extension. Greedy restoration of omitted vertices gave 25 new witnesses,
then 13 witnesses after inclusion minimization. All 8,974 cases are covered.
The canonical first-certificate tag stream has 17,952 bytes and SHA-256

`d92ebfdb65f17d2c970385cfd05a2206bc0b8733f7c2e1496b5d15741839d5c9`.

The survivor stream is empty. The native search used 28,885 conflicts in
total, maximum 4,473 in one call. Summed native solve time was 1.4078 seconds,
and total traversal time 5.6720 seconds. Maximum worker RSS was 27,920 KiB.
These figures describe this run and are not bounds for other supports.

The independent optional historical audit imports no driver, projected
compiler, path dynamic program or solver. It verifies every chronological
skip against the already available witness prefix, all 25 actual formula
byte streams and all Boolean models (**260,736 clauses**). It independently
enumerates path-colour assignments, checks 124,746 raw candidate/restored
edge inequalities and all 109 restoration steps, and matches each public
new witness to its native source row. It separately reconstructs and checks
all **8,974 full core colourings**, with **22,202,318 edge inequalities**.
The full historical audit and direct proof agree.

[cases.json](cases.json) records the 25 actual queries and formula hashes;
[result.json](result.json) records the complete finite traversal. Raw models,
CNFs, logs, chronological rows and generated tag streams remain local and
regenerate. Their absence from the repository does not affect the direct
positive theorem.

## Reproduction

With Python 3.11.2 and its standard library, from the repository root:

```sh
python3 -B hadwiger_nelson_heule514_whole_decision/verify.py --out /tmp/hn514-whole-check
```

This is sufficient for the whole theorem. It requires neither a solver nor
any residual-frontier file. It reconstructs exact geometry, expands the
archived witnesses, proves all 503 singleton forcings, and checks every
one of the 462 possible induced 508-vertex supergraphs. The measured run
took about 1.5 seconds. Three malformed-colouring controls are rejected.

To reproduce the discovery route, first obtain the checked 8,974-row
frontier and exact graph packet by following the
[profile-pilot README](../hadwiger_nelson_heule514_profile_pilot/README.md).
With those artifacts at the example paths below and an interpreter with
python-sat 1.8.dev24:

```sh
/path/to/pysat-python -B hadwiger_nelson_heule514_whole_decision/run.py --frontier /tmp/hn514-profile-run/survivors.txt --graph /tmp/hn514-core/graph.txt --out /tmp/hn514-whole-run
python3 -B hadwiger_nelson_heule514_whole_decision/verify.py --out /tmp/hn514-whole-audit --frontier /tmp/hn514-profile-run/survivors.txt --run /tmp/hn514-whole-run
```

The driver's output directory must be new. Optional archive auditing
expects the recorded mathematical outcomes and deterministic colour
choices; different solver builds can find different valid witnesses.
Timing fields are not reproduction invariants. Including the full
historical audit took about 7.2 seconds in the recorded run.

[manifest.json](manifest.json) pins imported input and method files;
[SHA256SUMS](SHA256SUMS) pins this package. [verification.json](verification.json)
and [validation.json](validation.json) preserve the actual checks and
versions. No compiled binary, full search dump, private state or solver
proof trace is required for the public positive theorem.

The trust boundary is exact coordinate transcription and squarefree-basis
independence, faithful archived positive-witness decoding, Python integer
and file semantics, complete finite loops and the elementary containment,
forcing and greedy-restoration argument. All mathematical inequalities
used for edges are exact. SAT solver soundness, floating-point predicates,
negative H517 results, and earlier residual-census completeness are not
premises of the direct proof. Separate author-run implementations are not
presented as external acceptance or formalization of this new theorem.

## Decision and shared handoff

H514 is closed for the at-most-508 target. Do not continue deleting or
sampling vertices of this support. No unfinished proof or background job
remains, and this pass yields before opening another support or phase.

A concrete next direction is an exact simultaneous mutual-incidence
analysis of the fixed 122 archived external completion centres, using
their existing coordinates instead of re-enumerating their source triples.
It can identify coupled added-point supports outside H514, particularly
interactions among points whose old-neighbour sets lie in different
blocks. At least one of the other 118 centres must occur to leave H514.
No H514 singleton forcing may be transferred to a larger support unless
its positive colouring is extended and checked there. This next analysis
and any new native graph queries are **unstarted**. It is not a sequence
of isolated one-point augmentation closures.

The incremental refresh read HN-3's
[terminal-coincidence theorem](../hadwiger_nelson_moser_terminal_coincidences/README.md),
which closes all terminal-only fixed Moser/full-Parts assemblies below 509
with private interiors, including coincident terminals. Its different
geometric mechanism supplies no H514 premise and was not duplicated. The
new coincidence strengthening's external review remains pending. No new
overlapping objection appeared in the inspected H514 relation neighbourhoods.
The retired H517/H574 supports and parked HN-1 census also remain closed
or parked under their exact prior scopes.
