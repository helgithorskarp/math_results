# Every subgraph of de Grey's 1,581-point support through order 510 is four-colourable

**Exact computer-assisted theorem.** Let `G` be the strict unit-distance graph
on the explicit de Grey construction specified below. There is a certified set
`M` of **511 vertices** such that `G-v` is four-colourable for every `v in M`.
Consequently every non-four-colourable subgraph of `G` contains all of `M`, and
**every subgraph of `G` with at most 510 vertices is four-colourable**.

This closes the entire at-most-508 extraction space in this fixed 1,581-point
host. There is no restriction to coordinate sections, blocks, symmetries,
metric balls, or a sampled list of subsets. This is a negative host result;
it does not improve the 509-vertex record, determine the smallest obstruction
inside this host, or classify other placements or larger supports.

## Why a small certificate covers every subset

If `G-v` has a proper four-colouring and a subgraph `H` omits `v`, restricting
that word four-colours `H`. Thus any non-four-colourable `H` must contain every
vertex for which such a deletion word is certified. A set of 511 distinct
certified deletions excludes all orders through 510. This argument applies to
arbitrary edge subgraphs as well as induced subgraphs.

The certificate obtains its 511 full-host deletion words from a two-terminal
interface. Write `Y` for the 791-point half, with terminals `a=(-2,0)` and
`b=(2,0)`. The full graph consists of `Y` and its rotated copy `Y'`. They share
only `a`, and the only edge between their disjoint interiors is `bb'`.
The complete exact pair census, including all possible extra contacts, verifies
these statements.

The supplied baseline is a proper four-colouring of all of `Y`. For **254
nonterminal labels** `v`, the certificate supplies a proper four-colouring of
`Y-v` in which `a` and `b` receive different colours. Add the two terminals to
obtain a set `T` of **256** required vertices for any subgraph of `Y` that forces
the terminals equal. The two copies of `T` share only `a`, so their union has
`2*256-1 = 511` vertices.

To colour `G-v` for a nonterminal `v` in the left copy of `T`, use its separating
word on `Y-v` and the baseline on `Y'`. Permute the right palette to match the
colour at `a` and make the two bridge endpoints different. Such a permutation
exists: if the right terminal has the anchor's colour, the separating left
word already resolves the bridge; otherwise choose its image to avoid both
the anchor colour and the left bridge colour. The right-side case is the same.
If the deleted vertex is the anchor, the halves have no shared vertex and their
palettes can resolve the bridge. If it is either bridge endpoint, the bridge
is absent and matching the anchor suffices.

The verifier does more than rely on this gluing argument. It enumerates all
24 palette permutations, constructs each of the **511 words on all 1,580
remaining vertices**, and checks every induced edge directly. Their sorted
stream `deleted-label + space + word + newline` has SHA-256

```text
120c1af011ce288286f7f1ad41a9163aa9ce112e4479f4964bd149413a431be3
```

Thus an error in a recolouring or palette construction cannot silently become
a universal family conclusion.

## Exact coordinates and complete geometry

The source is [de Grey, Section 6](https://arxiv.org/html/1804.02385v2).
The 39 integer rows in [seeds.json](seeds.json) represent
`((a+b sqrt(33))/12, (c sqrt(3)+d sqrt(11))/12)`. Taking their six rotations by
multiples of 60 degrees and their reflections gives `Sb`, of order 397.
Remove `(1/3,0)` and `(-1/3,0)` to obtain `Sa`, of order 395. In complex notation,

```text
r = (7 + i sqrt(15))/8
s = (31 + 3 i sqrt(7))/32
Y = Sa union r Sb
G has point set Y union {-2 + s(z+2) : z in Y}.
```

Both multipliers have norm one. The common coordinate denominator is 3,072,
and the ordered real radical basis is

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165),
sqrt(7), sqrt(21), sqrt(35), sqrt(105), sqrt(77), sqrt(231), sqrt(385), sqrt(1155).
```

A point is encoded by its 16 integer x-coefficients followed by its 16 integer
y-coefficients. Labels are increasing lexicographic order. The half labels are
the corresponding order restricted to `Y`. The two half terminals are 0 and
790. In the full host the shared vertex is 0 and the bridge is `[1579,1580]`.
There are exactly **1,581 points and 7,877 edges**, including **3,938 edges**
in each half.

All **1,248,990 unordered pairs** are classified exactly. The producer in
[native.py](native.py) uses integer coefficient vectors and a necessary
constant-coefficient norm test, followed by all nonconstant coefficients. The
separate geometry checker in [exact.py](exact.py) uses rational dictionaries
indexed by squarefree radicands and gcd multiplication. Its necessary modular
filter uses modulus 2,269 with checked roots of 3, 5, 11, and 7; all 8,350
survivors receive a full exact radical norm test. A modular equality never
accepts an edge.

These two geometry implementations are reused from the earlier
[residue-section work](../hadwiger_nelson_degrey1581_residue_sections).
The new checker selects the original half as the fixed part under changing the
sign of `sqrt(7)`, reconstructs the other half by exact affine arithmetic, and
checks the shared vertex, all mapped half edges, the sole bridge, and the
inversion `z -> -z` on the half. The two complete reconstructions agree.

The coordinate and edge stream SHA-256 values are respectively

```text
40b27b53176a846efe80a1f40ce685b7aaf89d6f3988969da112caa9c493c5e3
a20b27f728af08a9aaacbc60cbaa4ef095f62e4c47ef8ab87dcc0c0233b04675
```

The recent [independent review](../hadwiger_nelson_degrey1581_residue_sections_review1)
reconstructs the same seed table, point set, and complete edge set using SymPy
and different modular maps. It accepts the earlier section theorem and its
geometry. It has not reviewed this new terminal-cover certificate.

## Compact positive proof and discovery

[certificate.json](certificate.json) is **71,590 bytes**, with SHA-256

```text
690c34701f671959013e3053e22c60f8f784648e8985e0342e5d138ca1d3f29a
```

It contains a 791-character baseline and a directed acyclic list of 254
omission words: **34 full seed words, 127 inversion steps, and 93 patch steps**.
A patch specifies changed entries relative to an earlier word. The checker
validates the resulting support, every colour, terminal separation, and every
edge; it need not trust the heuristic that chose the patch. In particular,
the proof does not assume that a Kempe search is exhaustive.

The seeds came from CaDiCaL195 with four one-hot colour variables per vertex.
An activation variable gates each vertex's at-least-one clause. Every primary
query activates all vertices except one and pins the terminals to colours
0 and 1. Up to 395 representatives under inversion were eligible, each at most
once, with a requested limit of 200,000 conflicts. UNKNOWN supplies no witness
and is never treated as an exclusion.

Positive words were propagated by moving an omitted vertex across a uniquely
represented neighbour colour, optionally after swapping a bichromatic connected
component. One word per omitted label was retained, with inversion applied at
each insertion. This finite positive search stops once the two terminals and
at least 253 certified omissions force the target lower bound. The final
snapshot supplied 254 omissions, so the bound is 511 without any extra search
to strengthen it.

The executed sweep completed 45 primary calls: 40 SAT and five UNKNOWN.
The proof snapshot uses 34 of the SAT words. Six further SAT answers completed
while transport and independent validation ran; all 40 completed positive
words were subsequently checked against the independent half graph. The next
in-flight call was interrupted once the full target closure was verified; it
contributes no result. There are no pending computations or proofs. The five
individual UNKNOWN queries are unnecessary to the complete host theorem.

[discover.py](discover.py) implements the same fixed query universe and conflict
limit, with automatic transport checks after each completed call. A fresh
rediscovery can stop earlier than the executed batched checks and produce a
different valid certificate. Exact reproduction of the published proof uses
[produce.py](produce.py): it reads only the baseline and 34 seed rows and
rebuilds every transport step byte for byte, without a SAT solver.

## Reproduction and validation

From the repository root, Python 3.11 or later and its standard library suffice:

```sh
python3 -B hadwiger_nelson_degrey1581_terminal_cover/verify.py --check-expected
python3 -B hadwiger_nelson_degrey1581_terminal_cover/controls.py
python3 -B hadwiger_nelson_degrey1581_terminal_cover/produce.py \
  --out /tmp/degrey-terminal-certificate.json
cmp hadwiger_nelson_degrey1581_terminal_cover/certificate.json \
  /tmp/degrey-terminal-certificate.json
```

The verifier reports `verified: true`, `required_global_vertices: 511`,
`four_colourable_through: 510`, and
`arbitrary_target_subsets_classified: true`. Its full output, including the
511-label mandatory set, is in [expected.json](expected.json).

The checker validates **1,001,762 half-edge inequalities** and **4,020,265
full-host deletion-edge inequalities**. It takes about 2.6 seconds on the
research host. Normal and optimized Python runs agree. Controls cover all
1,100 simple graphs of orders 0 through 5 and 135,468 graph/palette/subset
cases, 2,696 palette-and-presence cases, a counterexample to extending the
gluing rule to two colours, and 27 malformed certificates or geometry faults.
Both geometry implementations reproduce every point and edge.

Optional SAT encoding controls and seed rediscovery require
[requirements-search.txt](requirements-search.txt):

```sh
python3 -m pip install -r hadwiger_nelson_degrey1581_terminal_cover/requirements-search.txt
python3 -B hadwiger_nelson_degrey1581_terminal_cover/encoding_controls.py
python3 -B hadwiger_nelson_degrey1581_terminal_cover/discover.py \
  --out /tmp/degrey-terminal-fresh-search
```

The encoding controls compare Glucose4 with direct colouring on every simple
graph of orders 2 through 5 and every retained subset containing the two
terminals. They are auxiliary; the theorem uses only positive words.

The trust base is the displayed exact construction, linear independence of the
squarefree radical basis, CPython exact integer/rational arithmetic, and the
written restriction argument. No floating-point decisions, SAT UNSAT answers,
external proof traces, or imported lower bound on the full graph are used.
No proof-assistant formalization is claimed. The larger generated geometry,
expanded colouring words, and search logs remain outside Git and regenerate
from this compact source.

This closes and retires the whole fixed-host extraction route through the
record target. Further deletion queries or enlarging the mandatory set are
unnecessary for that target. The next campaign phase must use another support
or a different mechanism that changes the candidate graphs.
