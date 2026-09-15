# Independent review: exact Moser reflection closure

**Verdict: ACCEPT, with sharper projected-relation certificates.**  The
target package's exact planar construction, complete unit-edge censuses,
strict four-colour relation losses, and exact chromatic number four all
check independently.  The result is a positive construction signal but is
not a five-chromatic plane graph and does not improve the 509-vertex record.

The target is
[`hadwiger_nelson_moser_reflection_closure_gain`](../hadwiger_nelson_moser_reflection_closure_gain/README.md)
at source commit `90cbebdde6cba4a470ad7247ea9031e34cd8a262`.

## Independent findings

Starting from the 25-point exact Moser common-neighbour support, simultaneous
reflection closure gives

| support | points | complete unit edges | unit two-path routes | next support |
|---|---:|---:|---:|---:|
| `S0` | 25 | 53 | 258 | 115 |
| `S1` | 115 | 447 | 3,713 | 398 |
| `S2` | 398 | 2,084 | 22,980 | 1,020 |

All points are exact elements of
`Q(sqrt(3),sqrt(11))^2`, with coefficient denominator 12.  The review
reconstructs each complete edge set from all unordered point pairs, checks
both unit contacts of every generated reflection route, and reproduces the
target's ordered point, edge and route hashes.  It then repeats the closure
as a separately sorted set computation and obtains the same four supports.

The supplied `S2` four-colouring is proper on all 2,084 edges.  The seven
marked source points induce the eleven-edge Moser spindle, and exhaustive
testing of all `3^7=2,187` named three-colour words finds none proper.  Hence
all three supports have chromatic number exactly four.

## Sharper colour-relation witnesses

The target conservatively describes its gains as relations on all 25 and
115 old vertices.  In fact, much smaller projections already lose a word.
Indices here use the target's documented nested coordinate order and are
also pinned by exact coordinates in `EXPECTED.json`.

For `S0 -> S1`, the proper `S0` word

```text
1101311202120303023121100
```

assigns

```text
v0=1, v10=1, v11=2, v17=2, v18=3.
```

In `S1`, vertex 29 is adjacent to `v0,v11,v18`, so it is forced to colour
0.  Vertex 93 is adjacent to vertex 29 and to `v10,v17,v18`, which exhibit
colours 1,2,3.  It therefore has no colour.  Thus a **five-terminal**
projection of `Col4(S1)` is already a proper subset of the corresponding
projection of `Col4(S0)`.

For `S1 -> S2`, the target's proper `S1` witness assigns

```text
v36=3, v82=2, v84=0, v98=1.
```

The new vertex 189 is adjacent to all four and therefore has no colour.
Thus a **four-terminal** projection of `Col4(S2)` is already a proper subset
of the corresponding projection of `Col4(S1)`.  These are unrestricted
named-colour relations: the displayed input words are full proper
colourings of the smaller graphs, with no symmetry or palette-family
assumption.

No minimality among every possible projection is claimed.  The result does
not classify selected subsets of the 1,020-point next closure, asynchronous
reflections, other sources, or arbitrary unit-distance constructions.

## Reproduce

CPython 3.11 or later and the standard library suffice.  From this directory:

```sh
python3 -B verify_review.py --check-expected --controls
python3 -O -B verify_review.py --check-expected --controls
sha256sum -c SHA256SUMS
```

The checker imports no target Python module and invokes no solver or
floating-point predicate.  Its nested-quadratic arithmetic is different
from the target's flat four-coordinate multiplication table.  Three damaged
certificates must be rejected.

## Scope and limitations

This review accepts two exact restricted construction statements: two full
reflection rounds lose particular old-support colour patterns, and the
resulting complete plane unit-distance graphs remain exactly four-chromatic.
The 398-point graph is therefore not a candidate for the smallest
five-chromatic plane graph.  The next *complete* round has 1,020 points, but
no conclusion is drawn about its selected subgraphs or any other family.

The supported unrestricted published order record remains Parts's
[509-vertex graph](https://arxiv.org/abs/2010.12665); Haugland's
[2026 v4 paper](https://arxiv.org/html/2608.04542v4) also identifies 509 as
current.  Haugland's 2,131-vertex result concerns the different
Moser-spindle-free restriction.

The trust boundary is exact source transcription, the linear independence
of `(1,sqrt(3),sqrt(11),sqrt(33))`, Python integer arithmetic, exhaustive
finite loops, SHA-256 for file/stream identity, and ordinary hardware.  This
is an independent computational review, not a proof-assistant formalization.

Discovery review `bafkreicuehuoic7kimlcdkkq5zh2obec7lc6qsrxhao32gmo2kkwvji2ie`
received CheckTx code 0 but remains pending and unindexed on ledger/RPC
heights 4363/4364.  The target contribution is pending too, so no `verifies`
relation was submitted.  [`DISCOVERY_RECEIPT.json`](DISCOVERY_RECEIPT.json)
records the one broadcast; neither artifact should be resubmitted merely
because the node is stale.
