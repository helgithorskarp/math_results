# One reflection round preserves the paired-circle centre relation

Start with the exact 39-point paired-circle patch `S0` from the sibling
[`paired_circle_obstruction_realizability`](../hadwiger_nelson_paired_circle_obstruction_realizability/README.md)
package.  It has four marked centres, paired into two unit edges, and one
point adjacent to all four centres.  On a four-colouring of the bare terminal
graph the canonical pattern `0123` is feasible, but that common neighbour
forbids it on `S0`.  All other six feasible canonical patterns extend, so
`S0` has a verified nontrivial complete unrestricted centre relation.

For every unit two-path `p-r-q` in `S0`, simultaneously adjoin

```text
p + q - r.
```

After exact collision merging, reconstruct every unit edge on the resulting
support `S1`.

**Exact result.** `S1` has 139 distinct physical points and 492 strict unit
edges.  It has chromatic number exactly three, and its complete four-colour
relation on the four original centres is identical to that of `S0`.  Thus the
first complete capped interaction does not strengthen the input forcing
feature and is retired.  This is not a five-chromatic graph, a record
candidate, or a theorem about later reflection rounds or other sources.

## Why this was a forcing-feature gate

The source restriction is physical and unrestricted: the common unit
neighbour rules out four pairwise-distinct centre colours, while the six
positive source words show that no other pattern is lost.  It is not a
failure of an auxiliary list, phase prescription, or abstract quotient.

The declared operation completes every unit rhombus based at every unit
two-path of the source.  It was selected to couple this no-rainbow feature
through all source incidences and any incidental contacts among the new
points.  A direct non-four graph would have met the record-facing signal gate;
a strictly smaller centre relation would have justified only a separately
budgeted completion.  Instead the relation is unchanged, and a literal
three-colouring supplies the mandated immediate stop.  No second round,
partial-round selection, alternate paired-circle placement, deformation,
extra orbit, or host was tested.

## Exact geometry and complete relation

Coordinates lie in `Q(sqrt(3),i)`, represented in the linearly independent
basis

```text
1, sqrt(3), i, i*sqrt(3).
```

The checker reconstructs the paired-circle witness directly from

```text
omega = (1+i*sqrt(3))/2
```

and its two exact direction orbits.  It recovers 39 source points and all 102
source unit edges, matching the published point and edge identities.  The
source has 556 labelled unit two-path routes.  Their opposite-corner formulas
add 100 distinct points.  The checker discards the routes as an adjacency
description and tests all `binom(139,2)=9,591` physical pairs from scratch,
obtaining 492 unit edges.  Every generating route's two promised contacts are
then checked against that complete edge set.

Canonical terminal strings are restricted-growth words in centre order.
The bare graph consists of the two unit edges `(0,1)` and `(2,3)`, so its full
relation is

```text
0101, 0102, 0110, 0112, 0120, 0121, 0123.
```

The exact point `-i` is adjacent to all four centres.  It excludes `0123` in
every proper four-colouring of both `S0` and `S1`.  The certificate supplies a
proper 139-symbol word for each of the other six patterns.  Restricting those
words to `S0` proves positive extension there; checking them on all 492 edges
proves positive extension through `S1`.  Since `S0` is an induced physical
subsupport of `S1`, no pattern absent from `S0` can reappear.  Therefore both
complete unrestricted relations are exactly the same six-element set.

The certificate also contains a proper three-colouring of all 492 edges.
The common neighbour `-i` and the first paired centres form a unit triangle,
so two colours do not suffice.  Hence `chi(S1)=3` exactly, not merely at most
four.

Canonical hashes are:

```text
closure points  6bb06ff2fb651b605079ca7d8593ed5802ba774d850511444361c99e577e1e6b
closure edges   5cb394d5fb599ad14964f7d3b70e1e5878c026b0f18d84a48d30905235b8a85e
labelled routes 5e7bb9748b133de6cfa26eeba1b4026b472816f07c18e906c627514a2f138082
```

## Reproduction and trust boundary

CPython 3.11 or later and the standard library suffice.  From the repository
root run:

```bash
python3 -B hadwiger_nelson_paired_circle_reflection_neutrality/verify.py
python3 -O -B hadwiger_nelson_paired_circle_reflection_neutrality/verify.py
sha256sum -c hadwiger_nelson_paired_circle_reflection_neutrality/SHA256SUMS
```

Both Python invocations end with

```text
EXACT PAIRED-CIRCLE REFLECTION RELATION NEUTRALITY VERIFIED
```

The verifier imports no producer, sibling arithmetic, floating-point package,
or solver.  It reconstructs the source, closure, collisions, complete edges,
terminal relation and chromatic witnesses from the displayed exact formulas.
Three malformed certificates are rejected.  CaDiCaL was used only to discover
the positive words; the published checker validates every symbol directly, so
solver soundness is not a theorem premise.

The trust boundary is the stated reflection-completeness definition, the
elementary common-neighbour relation argument, the faithful
`Q(sqrt(3),i)` basis, Python rational arithmetic, exhaustive finite loops and
ordinary hardware.  This is author-side computer-assisted evidence, not an
independent review or proof-assistant formalization.

The result leaves arbitrary later reflection points and other source supports
unclassified.  It also says nothing about the infinite four-circle support;
only this exact finite patch and its one simultaneous reflection round are
decided.  Parts's [509-point, 2,442-edge
construction](https://arxiv.org/abs/2010.12665) remains the supported
unrestricted record, as also stated in [Haugland's August 2026
revision](https://arxiv.org/html/2608.04542v4).

## Verified public provenance

The exact source was verified after publication at commit
`494327c9962ae280c87ebbff567e2b0261f3e85b`; its remote `verify.py` has
SHA-256
`eb90cb78f2de35720bc0a25dab83f554b16d8975b0563d641c7e250dcffd85b0`.
The Discovery transaction and its uncommitted status are recorded in
[`DISCOVERY_RECEIPT.json`](DISCOVERY_RECEIPT.json).  CheckTx zero means
accepted for broadcast, not committed: the ledger remains indexed at height
4,363 and the RPC remains frozen at 4,364.
