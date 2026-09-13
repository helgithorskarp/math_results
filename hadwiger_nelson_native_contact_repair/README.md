# Native contact construction and a six-point record repair target

**A 1,233-vertex plane unit-distance graph with 6,969 edges is certified
five-chromatic. No improvement to the 509-vertex record is claimed.** This
package supplies a reproducible construction host, a proved five-chromatic
subset, and an exact sub-509 search target. It does not claim a new general
construction method or novelty for five-chromatic graphs of this order.

Let A be the archived Parts `v159e646` coordinates. Let D be the 30 distinct
oriented unit displacements between its points, and put

```
E = Q(i sqrt3, i sqrt11),
rho = (7+i sqrt15)/8,
L = A union (A+D),
H = L union rho L.
```

The exact host has **3,919 vertices and 29,125 strict unit edges**; L has
1,960 points. It contains a 3,049-point, 21,217-edge subhost obtained by
restricting L to the closed radius-2 disk before rotation. The certified
1,233-point graph is an induced subgraph of this smaller host, specified by
sorted point IDs in [certificate.json](certificate.json). Both larger hosts
also have chromatic number exactly five: they contain this subset and have
explicit proper five-colourings, checked on all their unit edges.

This is classical spindle-direction and linking-rotation geometry applied
to an explicit seed and addition rule. See [de Grey's construction](https://arxiv.org/html/1804.02385v2)
and [Parts' minimisation paper](https://arxiv.org/abs/2010.12665).
The current unrestricted benchmark is still 509, as stated in
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4).
The larger graphs here are research hosts, not record improvements.

## Concrete sub-509 target

In the published placement, H contains exactly 503 of the Parts509 points.
The missing original indices, with zero-based indexing, are

```
25, 74, 106, 107, 298, 336.
```

Write B for those 503 shared points. The active question is whether some
`S subset H\B`, `|S|<=5`, makes the actual graph on `B union S`
non-four-colourable. Such a witness would have at most 508 physical points.
The archived record input is used for this exact coordinate comparison; it
is not an input to the construction of H. The comparison says nothing about
other isometries or abstract graph isomorphism.

**This repair question is unresolved in this publication.** The provided
507-point, 2,422-edge control has a checked four-colouring. No UNSAT master
verdict, universal repair exclusion, or optimality of the 1,233-point subset
is asserted. Live search checkpoints and later smaller intermediate subsets
remain outside this frozen source package.

A related gate explains why additions must be selected as groups. The
radius-2 subhost contains 482 displayed record points. Those points together
with every point of that subhost having at least two neighbours in them
form a **1,587-point, 10,021-edge four-colourable graph**. The positive word
is supplied and every edge is checked. Thus a non-four-colourable subgraph
of that radius-2 host must use a point outside this particular pool. This
statement concerns the specified 482-point base; it is not an exclusion of
the 503-point repair target in the larger host.

## Verification

From the repository root, with CPython3.11 and the standard library:

```sh
python3 -B hadwiger_nelson_native_contact_repair/verify.py \
  --work /tmp/hn-native-geometry --check-expected
```

This independently reconstructs both hosts, checks **12,323,997** unordered
physical pairs, checks the positive colour words, and writes the exact
four-colour CNF of the selected graph. It does not itself check the lower
chromatic bound. For a complete proof replay, use Kissat4.0.4 and DRAT-trim:

```sh
python3 -B hadwiger_nelson_native_contact_repair/reproduce.py \
  --work /tmp/hn-native-proof --kissat /path/to/kissat \
  --drat-trim /path/to/drat-trim
```

Expected final status: `CERTIFIED CHROMATIC NUMBER FIVE`, with 1,233 vertices
and 6,969 edges. The selected CNF SHA256 is

```
683daee79e37c6d8dc64d3c7c6dcef2d370d4530a118de70c380e705cab275c5
```

The checked proof was 9,945,902 bytes, SHA256

```
39a2984ae28d50e3f3a40049e41706b346ee0b245bc617b6369154d4129cf9db
```

It is generated locally and omitted from Git. The observed proof generation
and checking took 32.1 seconds; full independent geometry took 33.9 seconds
on a shared host. These are measured runs, not performance guarantees.
[EXPECTED.json](EXPECTED.json) and [VALIDATION.json](VALIDATION.json) record
counts, hashes and tool provenance. All verification was performed by the
author using a separate implementation; independent-author review is not
claimed.

For the exact 503-point comparison, install SymPy1.14.0 and run

```sh
python3 -B hadwiger_nelson_native_contact_repair/record.py
```

This uses the hash-pinned earlier parser for the original radical-coordinate
file. The three required sibling source files are pinned in
[SOURCE_PINS.json](SOURCE_PINS.json); use a complete repository checkout.

## Construction search

`search_repair.py` implements the actual 503-plus-at-most-five search. It
checks a physical candidate by four-colour SAT, extends a returned colouring
to a larger colourable subset, and records the necessary clause that the
next candidate must leave that subset. It also uses the necessary degree
condition for a repair minimal under deletion of new points. The exact
logic and limitations are in [PROOF.md](PROOF.md).

The optional search requires python-sat1.8.dev17, SymPy1.14.0, and Kissat4.0.4:

```sh
python3 -B hadwiger_nelson_native_contact_repair/search_repair.py \
  --work /tmp/hn-native-repair --kissat /path/to/kissat
```

The defaults bound this run to 100 master iterations, about 900 seconds
between completed queries, and 90 seconds per native master query. Any
UNKNOWN status remains unresolved. A `NONFOUR_SIGNAL` still needs separate
exact geometry, checked refutation and five-colouring before a record claim.
`MASTER_UNSAT_UNCHECKED` similarly requires proof and encoding validation
before any family exclusion. No such verdict is asserted here.

The initial 3,049-point four-colour run reached its 200,000-conflict limit;
a fresh Kissat refutation was subsequently verified. Two independent
methods supplied its five-colourings. The general subset reduction and the
six-point repair search use different vertex selections in these same
explicit hosts. Their completed work, interrupted queries, and continuation
states are recorded separately in the researcher's durable pass report.

`search_cardinal.py` runs the same construction search with MiniCard's native
cardinality constraints. It replaces repeated selection literals by distinct
Boolean clones, each constrained to equal the original selection variable.
This reduced the master from93,061 to11,599 variables in the recorded run.
The guarded degree condition was checked on1,016 small truth-table inputs by
`cardinal_controls.py`. This is an encoding/implementation check, not a
completed result for the repair family. To start it independently:

```sh
python3 -B hadwiger_nelson_native_contact_repair/search_cardinal.py \
  --work /tmp/hn-native-cardinal
```

An optional `--resume /path/to/result.json` imports and rechecks saved
colouring-extension witnesses. Both search programs keep their potentially
large graph instances, proof files, witness collections and logs in the
chosen work directory. The construction/certification commands above do not
need these live search outputs.
