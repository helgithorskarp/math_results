# Review verdict and limitations

## Explicit verdict

`ACCEPT_AND_STRENGTHEN_H630_508_BLOCK_REPLACEMENT_STOP`

The target's exact theorem is supported. One fixed whole-block replacement of
the reviewed H630 seed gives 508 distinct plane points whose complete strict
unit-distance graph has 2,341 edges and chromatic number exactly four.

The review strengthens the target by enumerating 286 induced Moser spindles,
all wholly inside the 418-point retained host, proving that host itself is
four-chromatic. The 90 private disk points instead induce a three-chromatic
graph. All three relevant graphs are connected and have no articulation
vertex or bridge.

## Checks passed

- Fifteen public source, target and dependency files pinned by SHA-256.
- H632 reconstructed from its three original archives, not from target code.
- All 199,396 H632 pairs and 128,778 final pairs tested exactly.
- Physical collision and outside-field claims proved coefficientwise.
- Canonical final point and complete edge files reproduced byte-for-byte.
- Every edge split and all twelve mixed contacts reconstructed.
- Four-word checked on every complete-graph edge.
- Moser lower bound checked and exhaustively strengthened.
- Private disk three-colouring and triangle checked.
- Connectivity, articulation and bridge claims independently traversed.
- Source-box and three disjoint ten-unit-pair containment argument checked.
- Eight malformed certificates rejected; field and graph controls passed.
- Normal and optimized reports byte-identical.

## Limitations

- Only one frozen 212-point block, anchor pair, orientation and radius-five
  disk are covered.
- The result is four-chromatic and therefore is not a five-chromatic record,
  despite its physical order 508 being below the current 509 record.
- No conclusion is made about another replacement, deletion, radius, angle,
  host, point pool or later closure.
- The 286-spindle census concerns induced Moser subgraphs of this fixed
  complete graph. It is not a classification of all four-critical subgraphs.
- Registered-containment exclusions are not global geometric exclusions.
- The proof is computer-assisted. Residual trust is in the pinned public
  bytes, square-class independence, exact CPython integer/Fraction semantics,
  the documented finite reductions, SHA-256 and correct hardware execution.

