# A fixed 508-point coupled-edge exchange of H516 is exactly four-chromatic

The frozen exchange has **508 distinct plane points and 2,506 complete unit
edges**, and its chromatic number is **exactly four**. A literal four-colouring
and an embedded Moser spindle prove this without trusting a solver. This is a
scoped failed construction, not a sub-509 five-chromatic candidate or a closure
of arbitrary multi-point exchanges.

## The one physical exchange

Let B be the certified 516-point/2,538-edge Heule core from committed
[h3441](https://github.com/helgithorskarp/math_results/tree/bff36887d06f5fdbf017380148419da5ce8f0935/hadwiger_nelson_heule560_global_decision).
Its exact coordinate table is pinned by SHA-256
`3f60fe94c7cd3d9c70b7cc52124fa185d4b46d54bb59b21bca0c45d2b181fd51`.
The table's labels are the archived H632 indices. All ten degree-four vertices
are removed:

```text
102 109 293 296 299 302 305 308 569 578
```

Before reconstructing or colouring the resulting graph, `ARCHITECTURE.json`
fixed the additions as the lexicographically first archived H632 unit pair
outside H560 whose two endpoints each have at least three neighbours in the
retained H506. No deletion-set or chromatic pair sweep was performed. Exact
geometry selects **(399,576)**. The point budget is `516-10+2=508`.

The two new coordinates, in the displayed frame, are

```text
399: ((12√5 + 14√33 − 6√165)/96,
      (−28√3 + 42√11 + 6√55)/96)
576: (( 6√5 + 28√33 − 6√165)/96,
      (−14√3 + 42√11 + 12√55)/96).
```

Their distance is one. Their complete retained-host neighbourhoods are
`399: {346,392,421,441}` and `576: {393,421,431}`. Thus seven old–new
contacts and one new–new contact supplement 2,498 retained old edges.
The deletion set is spatially distributed: deleted labels 293 and 299 are
three units apart, so no disk of radius one contains it.

Both added points lie outside B and H560. The complete support is therefore
not contained in B plus one point, and not in the fixed H560 support. The
reviewed [whole-plane one-point closure](https://github.com/helgithorskarp/math_results/tree/4241a558b4f1279e2a8741202cc2bd2c93b3048c/hadwiger_nelson_heule516_all_plane_onepoint_closure)
(h3999/h4003) does not cover this two-point exchange by containment. No claim
about all two-point exchanges follows from this experiment.

## Exact graph and ordinary chromatic decision

Coordinates use denominator 96 and the square-free-radical basis
`(1,√3,√5,√15,√11,√33,√55,√165)`. Every CSV point row contains eight integer
numerators for x followed by eight for y. Distinct rows are distinct physical
points because this is a basis of the degree-eight multiquadratic field.
Final vertices are ordered by increasing original H632 label; the complete
map is in `certificate.json`. Edge indices are zero-based final indices.

The independent verifier tests all **128,778** final point pairs, includes
exactly all pairs at squared distance one, and checks the literal four-word
against every edge. It also rebuilds all 199,396 pairs of archived H632 to
verify the selector, source counts, ten degree-four deletions and all contacts.
It imports neither the producer nor a SAT solver.

The Moser witness has final indices `[0,291,143,162,302,141,160]`, in roles
`[o,t,a,b,s,d,e]`. Its two diamonds force `o=t=s` in any three-colouring,
contradicting the unit edge `t-s`. Together with the four-word this proves
chromatic number exactly four. No ordinary non-four evidence exists for this
frozen graph, and the architecture stops here.

Canonical byte identities:

```text
points.csv 9a68a448527fafd9ea02b31eee6f2b97e2f0430595b29984aa5c79f6ce97c121
edges.csv  c6b4b06b5883d1d8d94693413ff3314148130f3255044f6ecee707ab0fc5d646
```

## Reproduction and trust boundary

The package can be checked in isolation using Python 3's standard library:

```bash
python3 verify.py
python3 -O verify.py
```

Both modes give identical results and reject ten malformed mathematical
certificates. `VERIFY.json` records the output. The producer used ordered
bitmask multiplication; the verifier uses square-free radicands, gcd reduction
and unordered cross terms. Geometry and the word are the mathematical
certificate; the CaDiCaL search and the producer are not trusted by the check.
This author-side checker does not constitute a separate teammate review.

To regenerate the selected graph and obtain a four-word, use a full checkout
of this repository and `python-sat` (tested with 1.8.dev24/CaDiCaL195):

```bash
python3 reproduce.py --output /tmp/h516-exchange-replay
```

`PROVENANCE.json` pins all four archived input files. The H510 coordinate
archive happens to live in a historically named Parts/Heule directory; no
Parts construction or surgery is selected here. `h632.csv` is the compact
self-contained coordinate copy for verification. The original parent's
non-four theorem is prior evidence; the new four-colour theorem follows
directly from this package's exact coordinates and word.

## Campaign scope

This pass tests one physical exchange and retires it on the complete
four-word. It does not authorize another pair, threshold, deletion set,
completion layer or nearby variant. It neither improves the record nor closes
all coordinated H516 exchanges.

The refreshed primary references remain [Parts's 509-point/2,442-edge
construction](https://arxiv.org/abs/2010.12665) and
[Haugland v4](https://arxiv.org/html/2608.04542v4), which explicitly retains
509 as the unrestricted record. Discovery was still indexed at 4363, with RPC
height 4364 and last block 2026-09-11. A subsequent broadcast receipt, if
present, is not evidence of commitment.
