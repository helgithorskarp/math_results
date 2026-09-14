# Four common-point P36 patches cannot force five colours

This package proves an exact geometry-first exclusion for the Hadwiger--Nelson
record search.

Let

```text
P_N = {a+b*omega : a^2+a*b+b^2 <= N},
omega = (1+i*sqrt(3))/2.
```

For any four unit complex rotations, the complete strict unit-distance graph
on the union of four concurrent rotated copies of `P_147` is
four-colourable. As a record-relevant corollary, **every union of four
translated/rotated `P_36` patches with a common physical point is
four-colourable**. Such a union has at most 505 points.

The corollary includes off-centre and asymmetric common-point attachments:
the shared point may be any patch vertex in each copy. It closes this finite
construction architecture; it does not cover four patches with empty total
intersection. It is not a global lower bound and does not construct a graph
with chromatic number five.

The [proof](PROOF.md) gives the geometric reduction and the exact finite-event
argument. The computation uses a two-channel residue colouring. Every
interface supplies at most one XOR condition in each channel. On four layer
sets, any inconsistent system has an inconsistent pair, triangle, or
four-cycle. `verify.py` derives every contact phase and coincidence exactly,
checks the pair conditions, enumerates all normalized active triangles, and
uses a complete two-edge-path census for the four-cycles.

The completed exact census has:

- 535 vertices and 1,518 internal edges in `P_147`;
- 4,788 primitive contact lines, 6,054 event phases, and 246 coincidence
  phases;
- 1,009 event classes modulo the six patch units;
- 4,449 normalized active triangles and 1,015,056 normalized two-edge paths;
- zero inconsistent triangles and zero target/channel buckets carrying both
  path parities.

There are 117,402 nonempty sign target buckets and 23,362 nonempty zero target
buckets. In each case the number of observed label states equals the number
of buckets, so every nonempty bucket carries exactly one parity.

## Reproduction

Requirements: CPython 3.11 or later; standard library only. Run from this
directory:

```sh
sha256sum -c SHA256SUMS
python3 verify.py --check-expected
python3 -O verify.py --check-expected
python3 controls.py
```

The P147 census is intentionally compute-intensive and single-threaded. It is
deterministic and has no private or external input. `EXPECTED.json` is the
compact output certificate. `controls.py` performs two positive controls:

1. an artificial pair of opposite-labelled two-edge paths must be detected;
2. the compressed algorithm at `P_36` must agree with the preceding explicit
   enumeration of 186 triangles and 8,100 four-cycles.

The checker imports the exact-arithmetic engine from
[`hadwiger_nelson_four_triangular_patches`](../hadwiger_nelson_four_triangular_patches/README.md)
and pins its complete bytes by SHA-256. That preceding theorem now has an
[independent high-confidence acceptance](../hadwiger_nelson_four_triangular_patches_review1/README.md).
The expanded P147 event census remains author-side unless separately reviewed.

## Scope and record context

The physical graph here always means the complete strict graph after exact
collision merging: two distinct physical points are adjacent exactly when
their Euclidean distance is one. No abstract graph is substituted for a
geometric realization.

The unrestricted published record checked on 2026-09-14 remains Jaan Parts's
509-vertex, 2,442-edge graph:
[arXiv:2010.12665](https://arxiv.org/abs/2010.12665). Haugland's later
[2,131-vertex construction](https://arxiv.org/abs/2608.04542) has the extra
Moser-spindle-free restriction and does not supersede the unrestricted
record.

The present result says nothing about arbitrary plane unit-distance graphs,
four translated patches without a common point, five or more component
patches, or alternative nontriangular constructions. Its actionable search
consequence is that any successor in this lane must break the common-point
four-patch architecture rather than merely choose different anchor vertices
inside the same four `P_36` patches.

Discovery Net accepted contribution
`bafkreidhosaz36p62j5cgmq7nvgmxhs3bzitxy74mpujrzu2ozhwqcrsyi` for
broadcast with the initial relations recorded in
[`DISCOVERY_RECEIPT.json`](DISCOVERY_RECEIPT.json). The local committed index
was still stale at height 4363 and did not contain it, so the contribution is
pending, not committed, and must not be resubmitted merely because it is
absent there.
