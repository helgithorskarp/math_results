# Quartic phase-kernel F3 completion is exactly three-chromatic

This package freezes and exactly decides one plane-native Hadwiger--Nelson
construction.  Start from the 74-point quartic paired-circle kernel in the
accepted phase-obstruction realization.  For every unit two-path `p-r-q` in
that kernel, form the opposite rhombus corner

```text
p + q - r.
```

Among genuinely new physical points, retain every point having at least three
distinct unit neighbours in the original kernel.  Add all retained points
simultaneously, collision-merge exact coordinates, and reconstruct the
complete strict unit-distance graph from all physical pairs.

The result has **206 points and 834 unit edges**.  A literal proper
three-colouring and an embedded unit triangle prove that its chromatic number
is exactly **three**.  The triangle already lies in the original 74-point
kernel, so this also sharpens that source's previously published positive
four-colouring to an exact three-colouring.

This is a scoped construction stop, not a five-chromatic graph or progress
below Parts's 509-point record.  The result separates the source's genuine
owner-palette/list obstruction from ordinary chromatic forcing: even a dense,
nonlocal first completion round does not activate it.  The frozen architecture
is retired without changing the contact threshold, taking another round,
varying the quartic parameter, or testing another paired-circle placement.

## Exact construction and counts

Let `eta > 0` satisfy `eta^4=12`, and use the exact quartic realization from
[`hadwiger_nelson_realized_phase_obstruction`](../hadwiger_nelson_realized_phase_obstruction/README.md).
The source coordinates are reconstructed from the displayed formulas rather
than imported as a graph.  All arithmetic is in `Q(eta)+i Q(eta)`.

The 198 source edges give 1,442 unordered unit two-paths.  Their opposite
corners collision-merge to 506 genuinely new points.  Counting unit contacts
back to the complete source gives:

| old-kernel contacts | new physical points |
|---:|---:|
| 2 | 374 |
| 3 | 100 |
| 4 | 22 |
| 5 | 10 |

Thus the declared threshold retains `100+22+10=132` points, for a total of
206.  The verifier then discards the generating routes as an adjacency
description and checks all `binom(206,2)=21,115` pairs exactly, obtaining 834
edges.  In particular, all incidental new--new and old--new unit contacts are
included.

The canonical graph hashes are:

```text
points 19001684386ee2397e2e8d062c195ee4efdc9b42b9df3748aeed74f6cf6187ac
edges  593393352586c6817c4dbfff87712ed203511af64a686054a966cba6ed3aae52
```

## Reproduce

CPython 3.11 or later and the standard library suffice.  From the repository
root:

```sh
tmp=$(mktemp)
python3 -B hadwiger_nelson_quartic_phase_kernel_f3_stop/produce.py --out "$tmp"
cmp "$tmp" hadwiger_nelson_quartic_phase_kernel_f3_stop/certificate.json
rm "$tmp"
python3 -B hadwiger_nelson_quartic_phase_kernel_f3_stop/verify.py
python3 -O -B hadwiger_nelson_quartic_phase_kernel_f3_stop/verify.py
(cd hadwiger_nelson_quartic_phase_kernel_f3_stop && sha256sum -c SHA256SUMS)
```

The producer represents the field as `Q[T]/(T^4-12)` and uses deterministic
DSATUR only to discover the saved three-colour word.  The verifier imports no
producer or parent code: it reconstructs the same coordinates in the quadratic
tower `Q(sqrt(3))[eta]/(eta^2-2sqrt(3))`, rebuilds every route, collision,
contact and physical edge, and directly checks the word and source triangle.
Seven malformed certificates are rejected.  No floating-point predicate,
solver verdict, omitted graph stream or external data is a premise.

These are author-side exact computations, not independent review or a
proof-assistant formalization.  The parent realization is pinned at commit
`8c671c68a26488bbd551e46a6054a762cbb210da`; its list obstruction remains
valid.  This package changes only the ordinary finite-graph conclusion for
the displayed source and its one declared completion.
