# Independent review: H630 508-point block-replacement stop

## Verdict

**Accept and strengthen at the one frozen replacement scope.** The published
support consists of 508 distinct exact plane points, its complete strict
unit-distance graph has 2,341 edges, and its chromatic number is exactly four.
It is therefore a valid one-point-below-record geometric construction, but not
a five-chromatic graph and not a record candidate.

The review adds a structural explanation of the lower bound:

- the 418 retained old points alone induce a connected, articulation-free
  2,095-edge graph of chromatic number four;
- that retained graph contains **286 distinct induced Moser spindles** (572
  role embeddings), and every one is wholly old--old;
- the 90 private disk points induce a connected, articulation-free 234-edge
  graph of chromatic number exactly three, with colouring `(m-n) mod 3`; and
- the complete 508-point graph is connected and has no articulation vertex or
  bridge.

Thus the replacement disk does not supply any of the enumerated Moser lower
bounds. This does not say that the disk is irrelevant to four-colourability or
classify other blocks, radii, orientations or hosts.

## Independent exact reconstruction

The checker pins fifteen public files and imports no target executable. It
rebuilds H632 directly from the archived 510-point coordinate table and 122
fresh centres, then deletes labels 399 and 462 and applies the stated whole-
block rule. All 199,396 H632 pairs are checked exactly, reproducing 632 points
and 3,112 edges. The induced H630 seed has 630 vertices and 3,098 edges, in
entry-level agreement with its earlier independent review.

The target producer uses XOR/bitmask multiplication and its verifier uses
sparse square-free-radicand reduction. This review instead represents both
fields as recursive quadratic towers:

```text
Q -> Q(sqrt(p1)) -> Q(sqrt(p1),sqrt(p2))
  -> Q(sqrt(p1),sqrt(p2),sqrt(p3)),
```

using primes `(3,5,11)` for H632 and `(2,3,11)` for the final support. It
constructs the triangular disk from the closed Cartesian formula, proves that
the only retained/disk collision is the origin, sorts the physical union, and
tests all `508 choose 2 = 128,778` pairs.

The resulting canonical identities are

```text
points.csv 0e665d7cf9767d2c0068429e138a686bfdcc8bbc51f310ef27a03763188ac4ee
edges.csv  b5f75973a1319a52ba22dcf1ee256ea075065095637268d0521bb112aafb7fb0
```

and the complete edge split is 2,095 old--old, 12 mixed and 234 private
new--new edges.

## Chromatic certificates

The submitted 508-symbol word is proper on every reconstructed edge. The
submitted seven vertices induce the standard 11-edge Moser spindle, now also
mapped to H632 labels

```text
267, 258, 291, 83, 50, 205, 62.
```

This proves the full graph is not three-colourable without trusting a solver
negative. Enumeration from the complete adjacency relation finds 286 distinct
induced Moser vertex sets. Their canonical final-index stream has SHA-256

```text
7499e526520427c00ceef8063b1090b81e82cd1b9954697232bd484706c5bfc4.
```

All 286 lie in the retained host. Restricting the submitted four-word gives
the retained host a proper four-colouring, so that host is exactly
four-chromatic. On the private disk, `(m-n) mod 3` is proper and vertices
`[0,1,7]` form a triangle, proving chromatic number three there.

## Reproduction

From the repository root, with CPython 3.11 or later and only the standard
library:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B hadwiger_nelson_h630_sqrt2_block_replacement_stop_review1/independent_check.py --check-expected
PYTHONDONTWRITEBYTECODE=1 python3 -O -B hadwiger_nelson_h630_sqrt2_block_replacement_stop_review1/independent_check.py --check-expected
PYTHONDONTWRITEBYTECODE=1 python3 -B hadwiger_nelson_h630_sqrt2_block_replacement_stop_review1/controls.py
cd hadwiger_nelson_h630_sqrt2_block_replacement_stop_review1 && sha256sum -c SHA256SUMS
```

Each full reconstruction takes roughly 30 seconds in the review environment.
Normal and optimized reports must be byte-identical. The trust boundary is
the pinned public bytes, independence of the multiquadratic bases, exact
CPython integer/Fraction semantics, the documented Moser argument, direct
finite enumeration, SHA-256 and ordinary hardware. No SAT status, floating
predicate, target executable, hidden point pool or private data is trusted.

## Scope and record context

Only the named 212-point block, anchors, orientation and radius-five disk are
covered. The review does not classify another H630 replacement, prove a
five-chromatic graph below 509 points, establish minimality, or give a global
sub-509 exclusion. The containment checks only exclude the registered H632,
H560, H516 and H516-plus-one scopes; they are not chromatic evidence.

Parts's [509-point, 2,442-edge construction](https://arxiv.org/abs/2010.12665)
remains the supported unrestricted record. Haugland's
[2026 manuscript](https://arxiv.org/abs/2608.04542) is explicitly non-record.

Reviewed target:
[H630 508-point block replacement](../hadwiger_nelson_h630_sqrt2_block_replacement_stop/README.md),
mathematical commit `53b90e407c24fdd029346f8c9f2de72a51b0d062`.

