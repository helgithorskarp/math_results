# Independent review of the native Parts136/A159/B214 transfer

## Verdict

**ACCEPT WITH A STRICT FIXED-FRAME LIMITATION.** The source package at commit
`e68a1e0496c9d82da079847cd7675e87136e9f92` correctly reconstructs its one
native-frame plane graph and correctly concludes that it leaves every proper
four-colouring of the 136-point Parts host available.

An independent exact implementation obtains **508 distinct physical points**
and **2,187 complete unit edges**. The edge set decomposes as follows:

| component | unit edges |
|---|---:|
| 136-point Parts host `H` | 564 |
| 159-point source `A` | 646 |
| 214-point source `B` | 977 |
| additional physical contacts | 0 |

`H` and `A` share exactly their origin. `B` is point-disjoint and has no unit
contact with either. All 29 host--new edges are already the edges from the
shared origin inside `A`; the remaining 1,594 edges have both endpoints new.
Thus the graph is the disjoint union of `B` and the one-vertex sum of `H`
with `A`.

Every four-colouring of `H` extends: take one fixed proper four-colouring of
`A`, permute its colour names so its origin agrees with the host origin, and
use any fixed proper four-colouring of the disjoint `B`. Conversely, `H` is an
induced subgraph, so restriction gives the other direction. The unrestricted
four-colour relation projected onto all 136 host vertices is therefore
unchanged. In particular, all 41,025 canonical boundary patterns from the
separately reviewed receiver survive, although this review does not rerun
that earlier exhaustive relation census.

The complete graph is exactly four-chromatic. A fresh proper four-colour word
uses the receiver's second positive host fixture and independently forced
different colours at one private `A` vertex and one `B` vertex. It differs
from the source word in 375 positions: 96 on `H`, 109 on the private `A`
vertices and 170 on `B`. The retained seven-point, 11-edge Moser spindle has
no proper three-colouring under exhaustive checking of all `3^7` assignments.

## Scope

This is an actual strict plane unit-distance graph: exact coordinates are
collision-merged and all 128,778 unordered physical pairs are tested. It is
not an abstract gluing claim.

The conclusion retires only the displayed native placement of complete
`H`, `A` and `B`. It says nothing about rotating or translating a donor,
altering either source, adding contacts, selecting subsets, using a different
host, or constructing an internally coupled replacement. It does not exclude
the Parts136 receiver or arbitrary replacements within its 372-new-point
allowance. There is no five-chromatic graph and no improvement on the
509-vertex record.

## Reproduce

CPython 3.11 or later and the standard library suffice:

```bash
python3 -B verify.py
python3 -O -B verify.py
python3 -B verify.py --controls
sha256sum -c SHA256SUMS
```

The checker imports no target implementation. It uses subset-mask
multiplication in `Q(sqrt(3),sqrt(5),sqrt(11))`, whereas the reviewed public
checker uses squarefree-radicand/gcd products. It verifies byte-identical
provenance copies of all three input tables, reconstructs the graph, compares
the complete target geometry object and directly checks two target words plus
the fresh independent word.

To regenerate the fresh positive word with a DIMACS solver producing standard
`s SATISFIABLE` and `v` lines and exit status 10:

```bash
python3 -B generate.py --solver /path/to/kissat --output /tmp/certificate.json
```

The solver is only a witness producer. No negative solver answer enters the
review proof.

## Sources

- reviewed package (branch path):
  <https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_parts136_mixed_native_transfer_stop>
  The exact reviewed source revision is
  `e68a1e0496c9d82da079847cd7675e87136e9f92`.
- independently reviewed Parts136 receiver:
  [../hadwiger_nelson_parts136_reverse_receiver_review1](../hadwiger_nelson_parts136_reverse_receiver_review1)
- exact A159/B214 coordinate provenance:
  [../hadwiger_nelson_nonmono159_214_lowden2](../hadwiger_nelson_nonmono159_214_lowden2)
- Parts's 509-vertex, 2,442-edge construction:
  <https://arxiv.org/abs/2010.12665>
- Haugland's August 2026 paper, which still identifies 509 as the current
  record: <https://arxiv.org/abs/2608.04542>

See [PROOF.md](PROOF.md), [PROVENANCE.md](PROVENANCE.md), and
[VALIDATION.json](VALIDATION.json) for the finite proof and audit trail.
