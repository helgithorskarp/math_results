# Claim and complete family

Let `F_t` be the full direct h3887 formula for task
`t = bo1-qQ-rR-cCCCCCC`. Its physical graph has 43 vertices, `q` disjoint
four-blocks, the first `r` red and the others blue, and the specified
Ramsey(4,4) catalogue core of order `43-4q`. The formula includes every
monochromatic-five prohibition, red-packing maximality, sorted root columns,
and sorted equal-colour nonroot block words. The h3873/h3887 global-coverage
theorem is an imported premise.

Define `A_t` to be h4035's selected-exchange clauses for q8 and q9, and the
empty conjunction for q7 and q10. The complete new family is

```
{ F_t AND A_t : all 2,189,178 h3887 task IDs t }.
```

This package compiles that exact family and completes its constructive
physical transport. It preserves a representation of every hypothetical
good43. It changes 2,187,234 task carriers; all original IDs remain. No
task is declared SAT or UNSAT, and no additional reduction percentage is
claimed beyond h4035. In particular, the family is a global cover, not a
taskwise equivalence to the old formulas.

# Clause compiler

In the labelled core, scan red edges in lexicographic vertex-pair order,
greedily taking disjoint edges. The full greedy matching is maximal, so its
unmatched set is independent and has at most three vertices. Thus an
11-vertex core supplies at least four matching edges and a 7-vertex core
supplies at least two. Use respectively the first four or first two.

For every red block `B`, selected matching edges `e<f`, and two-set `S` in
`B`, prohibit all eight red contacts joining `S` to `e` and `B\S` to `f`.
The negative eight-literal clause has distinct physical pairs. There are
`36r` such clauses at q8 and `6r` at q9, with no new variables. Summed over
the complete affected registry, the virtual family has **511,465,236** added
clauses. They are emitted on demand; this is not a claim to have written
millions of full formulas to disk.

The physical vocabulary numbers the 903 unordered pairs lexicographically,
starting at one, with positive meaning RED. The h3887 task vocabulary instead
uses variable 1 as true, starts free physical pairs at 2, and omits fixed
block/core pairs. Every added pair joins a block and the core, hence is free.
`compile_family.py` translates the suffix into exactly that vocabulary and
updates the header. q7 and q10 receive no added clauses.

# Constructive destination theorem

Suppose a complete graph in an ordered source carrier satisfies the upstream
red-maximality clauses and violates a selected-exchange clause. Both
`S union e` and `(B\S) union f` are red K4s. Replace `B` by these two blocks.
The same physical graph now has `(q+1,r+1)`, and its core loses exactly the
four endpoints of `e,f`. Its new core is induced in the old Ramsey(4,4) core.
Its blue-block/core remainder is a subset of the old red-K4-free remainder,
so red maximality persists.

The bridge then performs all formerly deferred operations:

1. Locate the exact 7- or 3-vertex core record, together with an explicit
   catalogue-position-to-input-position permutation.
2. Keep the first available red block as the root. Sort each other block's
   vertices by decreasing four-bit red signature to that root, resolving
   equal signatures by their input label.
3. Sort the nonroot red blocks and the blue blocks separately by decreasing
   unsigned 16-bit root matrix. Equal words remain allowed.
4. Concatenate the ordered blocks and catalogue core order. This gives a
   full new-to-old permutation of the 43 physical vertices and the exact
   destination `bo1` task ID.

For a good43, every new two-block and block/core-star domain necessarily
holds, because each rejected domain has a monochromatic five-set in at
most eight vertices. Thus the normalized graph belongs to the destination
carrier. For a source that is only a carrier assignment, a failed new domain
instead produces precisely such a five-set, transported back to the original
labels. No target claim is inferred from a domain pass.

Re-evaluate the selected matching and exchange rule after every normalization;
the core labels and root can change. Each successful exchange raises q, so
the process stops after at most two steps. At q10 there are no augmentation
clauses. Otherwise it stops when the q8/q9 clauses all hold. Therefore every
good43 source reaches the newly covering family, on exactly the same physical
graph. A non-Ramsey source can either be transported or return a checked
monochromatic five-set. Malformed inputs and source assignments violating
upstream red maximality are rejected as invalid input, not called Ramsey
counterexamples.

# Exhaustive core interface

The lookup producer enumerates all relabellings of the four three-vertex and
362 seven-vertex catalogue records. Each occupied entry stores a record ID
and a permutation. The independent verifier instead scans the full labelled
Boolean cube and checks every four-set literally: a graph is admissible iff
none of the six-edge four-set masks is all red or all blue. It then verifies
each accepted entry's physical edge permutation separately.

| order | all labelled graphs | admissible | rejected |
|---:|---:|---:|---:|
| 3 | 8 | 8 | 0 |
| 7 | 2,097,152 | 923,012 | 1,174,140 |

This both proves destination-lookup coverage and independently checks the
small catalogues against the labelled universe. The producer's enumeration
alone is not used as a completeness assertion.

For every one of the 546,356 eleven-vertex source records, the census deletes
each of the six pairs of selected matching edges: 3,278,136 entries. For
every seven-vertex source record it deletes the first two selected edges:
362 entries. The independent checker reads every recorded permutation,
checks the source and choice indices, verifies exactly the remaining vertex
set, and compares all destination pair colours with the claimed catalogue
record. The binary certificates are reproducible scratch output.

The q8 table reaches exactly **359** seven-vertex records. The omitted
zero-based indices are **82, 213, 214** in the pinned `r44_7.g6` file. This
gives a q8 immediate-destination envelope of `359*4 = 1,436` whole q9 IDs
with `r=6,...,9`, rather than `362*4=1,448`. Each q8 source core has between
two and six distinct destination record IDs. The q9 table reaches all four
three-vertex records with counts `[5,18,106,233]`, giving 20 possible whole
q10 IDs with `r=6,...,10`.

These are exact **core-deletion** routing counts. They do not assert that
every listed route is feasible under a full Ramsey formula. The three absent
incoming core records do not exclude their q9 tasks as independent starting
representations. Destinations are full h3887 tasks; this table gives no
membership or coverage assertion about the 161 h3987 children.

# Physical and formula verification

The physical audit normalizes a deliberately relabelled complete graph for
each of all 362 q9 cores and all five q9 red-block counts, and for all four
q10 cores and all six q10 counts: 1,834 normalizations. It transports a forced
exchange for every q9 core/count pair, plus all six selected edge-pair choices
in four existing q8 macro representatives. A fixed additional q8 fixture
exercises two successive exchanges and the composed permutation. Zero-step
and physical monochromatic-five outputs are also checked.

Every fixture contains an explicit blue K5 before transport. These are
interface controls, not candidate graphs or evidence of Ramsey feasibility.
The independent `verify_bridge.py` imports no producer, exchange, normalizer,
or encoder. It checks physical edges, catalogue membership, literal local
domains, root/block ordering, red maximality, each exchange's selected edges,
source bindings, final task identity, the composed permutation, and terminal
augmentation clauses. Corrupted certificates exercise these boundaries.

Every source core is scanned to identify its selected matching. Only that
matching affects the new suffix, giving 615 distinct q8 patterns and 31 q9
patterns. An independent physical-pair specification checks all of them for
every affected red-block count: 582,150 clauses and 4,657,200 literals. This
covers the suffix for every affected task index. Nine complete representative
formulas, one for each affected macro class, are additionally streamed and
hashed. Reconstructing their old headers and prefixes reproduces the pinned
h3887 whole-CNF hashes exactly. The unchanged generic upstream encoding and
its accepted coverage remain imported; this pass does not re-prove every
upstream clause or write all 2,187,234 complete formulas.

All computations use exact Python integers. The complete core checks,
physical controls, and formula audit are repeated with assertions disabled;
the programs use explicit checks rather than `assert`. Deliberately altered
lookup and deletion certificates must fail, and scratch bytes are restored
and hash checked after those controls.
The binary lookup uses explicit little-endian 16-bit entries: catalogue IDs
are at most 361 (with -1 for absence), and permutation IDs are at most 5,039.
Deletion source IDs are at most 546,355 and physical core positions at most
10. Array sizes and entry ranges are checked; no fixed-width arithmetic is
used for the counting arguments.

# Scope, provenance, and trust

The result closes the receiver gap identified by h4035 and its independent
ACCEPT review h4039. It operationalizes h4035's already accepted
5.49482423926453...% reduction of the bare h3887 carrier. It does not multiply
that fraction by h4029's dependent degree bound, sharpen a density or path
theorem, alter h4009/h4015, or close a physical task.

Dependencies are pinned in `DEPENDENCIES.json` and `INPUTS.json`. The global
cover and the completeness of the 11- and 15-vertex core catalogues are
imported from h3873/h3887. The exhaustive small-cube check establishes the
3- and 7-vertex destination coverage directly. The proof of exchange and its
bare-carrier percentage are imported from h4035; the new evidence is complete
executable routing and formula integration. This is not a claim of historical
novelty for graph isomorphism lookup, relabelling, or packing exchange.

Trust includes CPython integer/file semantics, SHA-256, the published checker
source, the operating system, and hardware. There is no solver verdict,
partial proof stream, external graph-isomorphism program, or formal proof
assistant in this result. Large generated evidence is kept out of Git and
regenerated by the documented command.
