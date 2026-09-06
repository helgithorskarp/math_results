# Complete 4-core propagation on the H514 residual family

**68,378 of the 258,914 inherited H514 residual graphs are four-colourable**
by degree-at-most-three peeling and existing positive certificates. No new
SAT or colouring-oracle query is used. Separate queue and simultaneous-round
implementations agree on every core and certificate choice; the independent
checker reconstructs every covered graph colouring and verifies
**168,620,504 retained-edge inequalities**.

The exact remaining family consists of **190,536 distinct 4-cores**:
**6,868 on 507 vertices** and **183,668 on 508 vertices**. Existence of a
non-four-colourable H514 subgraph on at most 508 vertices is equivalent to
existence of a non-four-colourable graph in this specified remaining family.
The surviving cores are **unresolved**, not proved non-four-colourable.
There is no record improvement and no closure of the whole H514 support.

## Fixed inputs

H514 is the [exact mixed-neighbour support](../hadwiger_nelson_heule514_interface/README.md)
with 514 distinct points and 2,526 unit edges. Its first 510 vertices use
the increasing union-certificate labels marked `510`. Added vertices
510..513 are completion centres 170,436,1239,1527. The coordinate basis is
`1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165`.

The parent result supplies 516 positive four-colourings of H514−D. Their
omission sets are an antichain of 484 singletons, 31 pairs and one triple.
It proves an exact target-order reduction to 258,914 induced 508-vertex
graphs whose six-element omission sets avoid all these cuts. The complete
frozen frontier is 6,074,339 bytes with SHA-256

```
6098161a878f17d4eb0f102124e1ea193543d15e4120c1ca0269a28baf0e6c80
```

This pass reads and checks that durable frontier; it does not re-enumerate
the parent six-subset census. The public reproduction command can regenerate
it when the file is unavailable. Both implementations reconstruct the
complete exact graph, decode all 516 published colourings, and directly
check their 1,298,057 retained-edge inequalities before using them. No
colouring-library completeness claim beyond the pinned parent's specified
finite-family theorem is introduced.

The prior [path projection](../hadwiger_nelson_heule514_path_projection/README.md)
remains available. The [complete boundary decision](../hadwiger_nelson_heule514_boundary_decision/README.md)
refuted a universal extension shortcut using only the induced sixteen-vertex
boundary. This pass uses additional whole-graph information: low current
degrees and the existing positive certificates.

## Peeling and positive restoration lemma

For any finite graph G, repeatedly delete a vertex whose current degree is
at most three. Let C be the remaining 4-core. The result is independent of
the deletion order: every induced subgraph of minimum degree at least four
survives each deletion, and the final graph itself has that minimum degree.
It is therefore the unique largest such induced subgraph, possibly empty.

G is four-colourable if and only if C is. Restriction proves one direction.
For the other, restore deleted vertices in reverse order. At its restoration,
a vertex has at most three already-coloured neighbours, so one of four
colours is available.

Apply this to G=H514−O for one frozen six-omission set O. If C omits an
entire known positive omission set D, restrict the checked H514−D colouring
to C and restore all peeled vertices in reverse order. This gives an
explicit four-colouring of G. **All of D must be absent**; one missing
member of a pair or triple is not sufficient.

Every one of the 516 positive cuts is tested, in increasing order of
`(size of D, increasing vertex tuple)`. In this complete run only two
singletons are needed for successful coverage:

| Canonical certificate index | D | Covered graphs using this first eligible certificate |
|---:|---|---:|
| 288 | {299} | 57,586 |
| 370 | {387} | 10,792 |
| Total | | 68,378 |

These are existing colourings, not new solver discoveries.
[`certificate.json`](certificate.json) gives their two full 514-character
witnesses and identifies their original canonical indices. They are
compared with the fully decoded public library and checked on the exact
graph. Each covered target is restored independently using both peeling
orders; the resulting colourings need not be identical.

## Complete native run and independent audit

[`core.cpp`](core.cpp) uses a degree queue. It initializes degrees after the
six omissions and queues all vertices of degree below four. When removing
one, it decrements its retained neighbours and queues any reaching degree
three. It tests every positive cut on the resulting core, uses the first
eligible one, restores all peeled vertices, and checks the complete target
colouring. One bounded run processes exactly all 258,914 input rows.

For each row it writes one 67-byte record: a signed 16-bit little-endian
certificate index (`-1` if uncovered), followed by 65 bytes encoding the
retained core vertices in little-endian bit order. Bits 514..519 are zero.
The file has no header and uses parent-frontier row order. Every record is
checked; the 17,347,238-byte stream remains local. SHA-256:

```
28f84db0f3983524594806c3c08d85a0937f68b96eed0be0225e05e926db1267
```

[`verify.py`](verify.py) imports no queue-peeling or producer code. It uses
the separate published exact geometric checker and the reviewer-owned
compressed-witness decoder, comparing the actual native graph and every
native input witness entry by entry. It computes cores by **simultaneous
rounds** of all eligible vertices. After the initial round, only neighbours
of removed vertices need reconsideration. Initially only original-degree
at-most-nine vertices can fall below four after six deletions; this exact
bound is used only to save checks.

Every one of the 258,914 core bitsets and first-eligible certificate indices
matches the queue result. For every covered graph, the checker independently
restores a colouring from its own round order, preserves exactly the original
omissions, checks the restoration degree bound, and checks every retained
unit edge. It also compares every surviving omission tuple with the native
survivor stream, including order and EOF.

Ten small abstract graph controls exercise cascades, empty and untouched
4-cores, nonempty peeling without coverage, singleton and pair cuts, and
preservation of the original omissions. A third characterization computes
the union of all induced subsets of minimum degree at least four, checking
**2,496 subsets** across these fixtures. All three core descriptions agree,
and all five positive restoration controls pass. The K5-based controls are
abstract test graphs, not claimed Euclidean unit-distance constructions.

The native family run took 6.12025 seconds with GCC 12.2.0 and `-O3`.
The independent Python 3.11.2 audit took 67.2969 seconds. Peak memory was not
measured. Both implementations use exact arithmetic; no SAT/QBF result,
floating-point predicate or omitted negative proof is trusted.

## Exact remaining family

The number of peeled vertices over all original candidates is

| Peeled vertices | Input candidates |
|---:|---:|
| 0 | 183,668 |
| 1 | 17,460 |
| 2 | 54,375 |
| 3 | 3,391 |
| 4 | 20 |

After positive-certificate coverage, there remain 190,536 original omission
sets. Their cores are all distinct. Of these, 183,668 have order 508 and
6,868 have order 507. No surviving core is classified as uncolourable.

The original surviving six-omission stream is 4,465,890 bytes, SHA-256

```
7d330bdb94157778eb17f8e467b1a01521ab8bc3da684335394982d96ec48597
```

For further work, [`summarize.py`](summarize.py) converts the fully verified
core stream to a canonical **core-omission frontier**. Each row is the
increasing tuple of all missing H514 indices, of size six or seven, with
comma-separated decimal ASCII and an LF. Rows are ordered by
`(omission count, omission tuple)`. This 4,493,362-byte stream has SHA-256

```
f00bfa52ad63aafb374150cff7917bd7c45716bee19cf416b350b2d0a16d1be2
```

The summary also groups the cores by their order, number of omitted
large-block vertices, and omission mask of added vertices 510..513. There
are **77 nonempty profiles**, with exact counts and one deterministic
representative per profile in [`core_census.json`](core_census.json).
A separate `audit_frontier.py` verifies a bijection between every canonical
core tuple and the surviving native core bitsets, independently recomputes
all 77 profile counts, and checks every representative against its recorded
native row. This is output classification, not another colouring query or
completeness claim about any one representative.

To prove the exact target-order equivalence, first use the parent reduction
to the 258,914 graphs. The 68,378 covered graphs cannot witness a target.
Every remaining graph is four-colourable exactly when its 4-core is, by
peeling and restoration. Conversely each surviving core is itself an induced
unit-distance graph on at most 508 vertices inside H514. Hence a
non-four-colourable target exists in H514 if and only if at least one of the
specified 190,536 cores is non-four-colourable. Edge-deleted graphs are
included through the parent's induced-graph reduction.

## Reproduction

From the repository root, create new temporary directories. If the original
frontier is not already available, regenerate it from its public certificate:

```sh
python3 -B hadwiger_nelson_heule514_interface/verify.py --out /tmp/hn514-frontier
```

Then run:

```sh
python3 -B hadwiger_nelson_heule514_core_propagation/prepare.py --out /tmp/hn514-core --frontier /tmp/hn514-frontier/frontier.txt
c++ -std=c++17 -O3 -Wall -Wextra -Werror hadwiger_nelson_heule514_core_propagation/core.cpp -o /tmp/hn514-core/core
/tmp/hn514-core/core --controls
/tmp/hn514-core/core /tmp/hn514-core/graph.txt /tmp/hn514-core/witnesses.txt /tmp/hn514-frontier/frontier.txt /tmp/hn514-core/cores.bin /tmp/hn514-core/survivors.txt /tmp/hn514-core/summary.json
python3 -B hadwiger_nelson_heule514_core_propagation/verify.py --work /tmp/hn514-core --frontier /tmp/hn514-frontier/frontier.txt --report /tmp/hn514-core/verification.json
python3 -B hadwiger_nelson_heule514_core_propagation/summarize.py --work /tmp/hn514-core --verification /tmp/hn514-core/verification.json
python3 -B hadwiger_nelson_heule514_core_propagation/audit_frontier.py --work /tmp/hn514-core --verification /tmp/hn514-core/verification.json
```

Only Python's standard library and a C++17 compiler are required. The public
files include source, the two compact witnesses, the exact result, core
profiles, validation and verification reports, and input/source hashes.
The full graph/witness packets, 17 MB core records and 4 MB frontier streams
remain local and regenerate. Source hashes are in `SHA256SUMS`; pinned input
hashes are in `manifest.json`.

The trust boundary is the archived exact coordinates, the radical basis,
compressed-witness decoding, finite exhaustive loops, integer arithmetic,
and the unformalized peeling and family-reduction proof. The parent finite
frontier theorem is an explicit inherited premise. New checking is
algorithmically independent and author-run; external review or formalization
of this new family result is not claimed.

## Handoff

This completes the frozen whole-frontier core test. There is no unfinished
proof, background job, or new solver query. The induced-boundary shortcut,
H517/H574 deletion searches, old biased H514 master, and timed-out QBF
configurations remain retired or parked.

The material remaining frontier supports one next bounded candidate decision:
freeze at most **one representative from each of the 77 nonempty core
profiles**, using the verified projected colouring CNF. This spans both core
orders and the observed block/path compositions. SAT results need direct
colouring checks; any UNSAT claim needs a fresh independently checked proof,
exact coordinates and a five-colouring before claiming a record. A complete
positive-cover audit should accompany the fixed pilot before reassessment.
No representative has been queried in this pass, and this proposal does not
assert that 77 samples decide the entire family.

The incremental shared refresh found HN-3's
[three-list connector extension theorem](../hadwiger_nelson_single_contact_extension/README.md),
commit 601ddbe, Discovery Net height 3220. It covers the stated Parts terminal-only assemblies when each
terminal has an available list of at least three colours, with exact private-
interior and contact hypotheses. Those conditions do not supply an H514
premise. The separate geometric lane is not re-enumerated here.
