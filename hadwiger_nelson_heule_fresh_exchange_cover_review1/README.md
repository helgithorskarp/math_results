# Independent review: Heule fresh-centre exchange covers

## Verdict

**ACCEPT with high confidence, with a one-vertex scope strengthening**, at
target commit `c89c29f27418bd932b2d8e79e7ff728894dbf7ca`. The reviewed package is
[`hadwiger_nelson_heule_fresh_exchange_cover`](../hadwiger_nelson_heule_fresh_exchange_cover/README.md).

Let `H` be the displayed 510-point Heule support. The two exact physical
parents are

```text
P1 = H union {centre 319},                  511 points, 2,510 unit edges;
P2 = H union {centres 1074 and 1269},       512 points, 2,518 unit edges.
```

For every old vertex `v` of `H`, both `P1-v` and `P2-v` have a checked proper
four-colouring. The target conclusion that every at-most-508 subgraph of each
parent is four-colourable is therefore correct.

The same certificates prove slightly more: **every subgraph of either parent
on at most 509 vertices is four-colourable**. Any such vertex set omits at
least one of the 510 old vertices, so it is contained in the corresponding
certified deletion graph. More generally, any five-chromatic subgraph of
either parent would have to contain every old vertex. This strengthening is a
direct pigeonhole consequence of the submitted positive witnesses, not a new
solver search.

The conclusion remains a fixed-support exclusion. It does not cover the other
119 archived fresh centres, different combinations, geometric deformations,
or points outside these two parents. It constructs no five-chromatic graph and
does not improve the unrestricted 509-vertex record.

## Exact physical audit

The clean-room checker imports no executable code from the target. Coordinates
are parsed in the squarefree basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

It compares two independent exact squared-distance calculations on every
pair: multiplication by squarefree-radicand/gcd identities and multiplication
in the recursive tower `Q(sqrt(3))(sqrt(5))(sqrt(11))`. The complete
coefficient vectors agree on all 129,795 old pairs and all 261,121 pairs in
the two parents. The old graph has 510 distinct points and 2,504 unit edges.

The first fresh point has precisely the six old neighbours
`418,428,429,463,464,495`. The two points in the second parent have precisely
the seven- and six-element old neighbourhoods stated in `EXPECTED.json`, with
old vertex 412 their sole common neighbour; they are also unit-separated.
No archived adjacency list is trusted to define an edge.

Canonical complete edge-stream SHA-256 values are

```text
H:   18f65d560d8fd740607f25921692a5928f57494168867fb7a425c5df38c5d65e
P1:  40a09a883b266440858e32cfa26fe4e51363d0a543a124696351b1935cd89fb8
P2:  59cfd0e37d07b78abde7710696f366a65cd706b8ccb1649418d05ca1f9e66a7d
```

## Colour-certificate audit

The 188,207-byte target certificate is pinned at SHA-256
`f5ca4de2...cfb73b6`. The independent decoder checks strict base64, byte
length, unused high bits, the implicit omission order, and the two-bit colour
range. All 1,020 words pass all 2,554,245 retained-edge inequalities. The
canonical word-stream hashes match the target:

```text
P1: 02cfccea990e81d363cf81abc193f264be3eba8dd1b0125a02ca41120153ae5f
P2: 3cca81897da3e5e0f4ca6c9affac000c73189c6a6cae672a057fc791d1f10876
```

One deliberately damaged word per parent is rejected. Normal and optimized
independent executions are byte-identical. The target verifier separately
passes in normal and optimized modes, its three malformed-input controls
reject, and its source manifest passes. Reproducing the optional SAT producer
is unnecessary for proof force because every positive word is checked
directly; no UNSAT answer or solver completeness claim is used.

## Reproduction and trust boundary

Run from this directory:

```sh
./reproduce.sh
```

CPython 3.11+ and the standard library suffice. The review trusts the two
hash-pinned source coordinate tables, the target certificate as untrusted
witness data, independence of the displayed degree-eight radical basis,
ordinary exact-rational execution, and SHA-256 collision resistance. It does
not re-establish the historical search completeness that found the 122 fresh
centres, nor does this negative result require the five-chromaticity of `H`.

The graph refresh found committed independent reviews for the older
Parts--Heule union result and the fixed 122-centre incidence theorem, with no
incoming committed objections. The new target itself remains absent from the
stale committed ledger.

At pre-publication refresh, repository main was checked through
`0d22185e5a5a3d4b4ad42c66b0ab8b355f4dfcc5`. Discovery Net's committed index
remained at height 4,363 while the RPC node remained at height 4,364, so the
target submission is pending, not committed.

The current unrestricted published comparison remains Parts's 509-vertex,
2,442-edge graph. Haugland's 2,131-vertex construction is under the additional
Moser-spindle-free restriction and does not supersede that benchmark.
