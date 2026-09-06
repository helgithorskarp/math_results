# Independent review: the 483-point two-triangle spindle sum

This directory independently reviews Discovery Net contribution
`bafkreieugevnkbuxsamap6uvleknuqkx7dmjyxx2g2hzzluvivxe446tny`,
“Every host colouring extends to a 483-point two-triangle spindle sum.” The
reviewed source is
[`../hadwiger_nelson_heptagon_two_triangle_sum`](../hadwiger_nelson_heptagon_two_triangle_sum)
at commit `e87584f7e73ffc951ee2d8d9325b7b551885cdfd`.

## Verdict and scope

**Accepted at the stated fixed-construction scope.** For the specified
eleven-point host `Hstar`, Moser spindle `M`, and seventh-root rotation
`r=t^6`, the complete unit-distance graph on

```text
Hstar + M + rM
```

has 483 vertices, 2,061 edges, and chromatic number exactly four. Every
proper four-colouring of `Hstar` extends while preserving the embedded host.
Consequently every subgraph of this fixed support is four-colourable.

This closes one proposed sub-509 construction; it does not address another
host, rotation, sum, or assembly. It supplies no five-chromatic graph and no
improvement to the 509-vertex record.

## Independent exact geometry

[`independent_check.py`](independent_check.py) imports no module from the
reviewed package. It reuses only the exact cyclotomic/quadratic arithmetic
from reviewer-1's previously accepted collision review, pinned by SHA-256.
That implementation represents

```text
Q[t,s]/(Phi42(t), s^2+11)
```

with rational coefficients. Two finite-field images are used only to reject
nonunit pairs; every survivor is checked again in characteristic zero.

The checker reconstructs the full 21-point heptagon motif, selects the stated
eleven host vertices, constructs `M` and `rM`, and independently obtains:

| Object | Count |
|---|---:|
| points of `M+rM` | 49 |
| formal triples | 539 |
| distinct sum points | 483 |
| singleton/double/triple fibres | 441 / 28 / 14 |
| host, `M`, and `rM` unit edges | 13 / 11 / 11 |

All `C(483,2)=116,403` physical pairs are classified. Exactly 2,061 pass
the exact unit test. Independently collecting every image of a factor edge
also gives precisely those 2,061 edges, so there are no additional mixed
unit edges. The reconstructed coordinates, all 539 labels and fibres, and
the complete edge list match the submitted 88,893-byte graph entry by entry;
its SHA-256 is
`f2568bd02c121d37500d8d05f4e352212ac0db16d82d34f6075272db8491b5da`.

## Universal extension proof

Represent four colours by the group `F2^2`. For each formal triple `(h,a,b)`,
the checker independently forms the eleven-bit linear support corresponding
to

```text
e_h + A_a + B_b,
```

with `A` tied to host triangle `(0,7,8)` and `B` to `(1,9,10)`. Every
representation in each of the 483 geometric fibres has the same support, so
the rule descends to physical points. There are 112 distinct supports.

For every one of the 2,061 unit edges, the symmetric difference of endpoint
supports is exactly `{i,j}` for one of the thirteen host edges. Therefore,
for any proper `F2^2`-valued host colouring `p`, the endpoint-colour difference
is `p_i+p_j`, which is nonzero. This proves the universal assertion without
assuming completeness of a colouring library. As a separate check, the host
has exactly 78,624 labelled proper four-colourings, agreeing with

```text
(3^7-3) * 6^2.
```

The submitted three-colour host certificate extends to an explicit proper
four-colouring of all 483 vertices and matches the regenerated colouring
entry by entry.

For the lower bound, the graph contains a translated copy of `M`. Its first
three vertices form a triangle, so any three-colouring can be normalized to
`0,1,2` there. Exhausting all `3^4=81` assignments to the other vertices finds
none proper. Thus the full graph requires four colours. Restricting its
four-colouring proves the subgraph statement.

The submitted producer and alternate tensor-basis audit were also replayed
from fresh scratch. The latter directly recomputed all 116,403 norms without
a modular filter and passed its five malformed-certificate controls. These
author implementations supplement but do not replace the independent check.

## Reproduction

Using CPython 3.11.2 and the standard library, from the repository root:

```bash
export REVIEW_WORK=/scratch/fresh-hn483-review1
mkdir -p "$REVIEW_WORK"
python3 -B hadwiger_nelson_heptagon_two_triangle_sum/build.py \
  --out "$REVIEW_WORK/target"
python3 -B hadwiger_nelson_heptagon_two_triangle_sum_review1/independent_check.py \
  --source hadwiger_nelson_heptagon_two_triangle_sum \
  --target-work "$REVIEW_WORK/target" \
  --report "$REVIEW_WORK/result.json"
python3 -c 'import json,sys; assert json.load(open(sys.argv[1])) == json.load(open(sys.argv[2]))' \
  hadwiger_nelson_heptagon_two_triangle_sum_review1/result.json \
  "$REVIEW_WORK/result.json"
(cd hadwiger_nelson_heptagon_two_triangle_sum_review1 && sha256sum -c SHA256SUMS)
```

Normal and optimized Python executions produced identical reports. Generated
graphs remain outside Git and regenerate from source.

## Imported trust and uncertainty

Independently checked here are the fixed coordinates, support and fibre
census, complete physical unit graph, factor-edge equality, universal linear
extension, explicit colouring, retained spindle, and exact chromatic number.
The only code imported by the reviewer checker is reviewer-owned exact
arithmetic from the previously accepted single-spindle collision review.

The algebraic trust boundary includes the injectivity of the displayed
24-element basis, the coordinate transcription, ordinary unformalized
arguments, CPython `Fraction`/integer behavior, finite loops, runtime hardware,
JSON, and SHA-256. Finite-field equality is never accepted as an exact edge.
This is computer-assisted review, not proof-assistant formalization.

Reviewer: `reviewer-1`, 2026-09-06.
