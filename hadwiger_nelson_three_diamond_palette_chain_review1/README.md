# Independent review and eight-point refinement of the three-diamond chain

This reviews
[`hadwiger_nelson_three_diamond_palette_chain`](../hadwiger_nelson_three_diamond_palette_chain)
at its immutable mathematical source commit
`38094e405f1bf389eb7b0f363a241ce11f0263b8`.

## Verdict

**ACCEPT with high confidence, and refine the relation source from ten points
to eight.**  I found no concrete defect in the target theorem.  The displayed
ten distinct plane points induce exactly 16 unit edges and form a
four-chromatic graph.  For ordered terminal edges `E0,E1,E2`, its complete
unrestricted four-colour relation is exactly

```text
palette(E0) intersects palette(E1)
and
palette(E1) intersects palette(E2).
```

The bare three-edge terminal graph has 74 proper equality patterns modulo
global colour permutation.  Exactly 52 extend and 22 fail; in named colours
the corresponding counts are 1,200 and 528 out of 1,728.

The target did not claim interior minimality, and it is not minimal as a
relation source.  Delete outer caps `P0,P3` and retain

```text
P1, P2, X0, Y0, X1, Y1, X2, Y2.
```

These eight inherited physical points induce exactly 11 unit edges and have
chromatic number three, yet their complete six-terminal four-colour relation
is identical to the ten-point relation.  The two retained interior vertices
`P1,P2` are relation-essential inside this fixed support: deleting `P1` leaves
only the `E1`--`E2` intersection condition, and deleting `P2` leaves only the
`E0`--`E1` condition.  No global smallest-gadget claim is made.

This refinement matters only when the source is used through its six marked
terminals.  A construction that also needs contacts to `P0` or `P3`, or needs
the source itself to remain four-chromatic, cannot silently substitute the
eight-point core.

## Independent mathematical audit

Put `s=sqrt(3)` and take the positive real root

```text
y = sqrt((4-s)/2).
```

The checker constructs all points directly from the radical formulas in
SymPy's exact degree-four algebraic number field `Q(s,y)`.  It then separately
parses the target's coefficient rows in basis `1,s,y,s*y` and proves equality
in the field.  Exhausting all 45 pairs recovers ten distinct points and the
complete 16-edge graph, including three `K4`-minus-cap-edge diamonds and the
closing edge `P0P3`.  The target point and edge hashes match.  No approximate
coordinate comparison is used.

The colouring audit generates restricted-growth strings, i.e. canonical set
partitions, rather than invoking the target's per-assignment backtracker.  It
finds no colouring with at most three colours and 208 canonical proper
four-colourings, representing 4,992 named full colourings.  Their terminal
restrictions give precisely the target relation and match independently
computed canonical, named, and extension-multiplicity hashes.  Only after the
exhaustive relation calculation does it inspect the 52 supplied witnesses;
all are proper and correctly indexed, but they are not proof premises.

The eight-point induced subgraph is checked by the same exact all-pairs graph.
It has four canonical proper three-colourings and none with at most two
colours.  Exhaustion with an unrestricted four-colour palette yields 72
canonical full colourings and exactly the same 52 canonical / 1,200 named
terminal assignments as the ten-point source.

There is also a short proof of the refinement.  `P1` is adjacent to all four
endpoints of `E0,E1`, so it has an available colour exactly when those two
two-colour palettes do not cover all four colours, equivalently when they
intersect.  The same argument at `P2` gives the second intersection.  The
complete edge census shows `P1P2` is not an edge and that there are no other
contacts, so the two choices are independent.  Conversely, deleting either
shared cap removes exactly its associated condition.  Outer caps `P0,P3` and
their closing edge serve only the separate four-chromaticity proof.

## Scope and construction status

Both the ten-point source and eight-point core are actual strict plane
unit-distance graphs, not abstract chromatic graphs.  The result remains only
a local relation theorem.  Repeating intersection constraints permits a
constant two-colour palette, so neither graph is a five-chromatic construction
or an at-most-508 candidate.  Any composition must specify compatible exact
incidences, merge collisions, reconstruct every unit edge, and certify
ordinary non-four-colourability.  No such host is supplied here.

At the 2026-09-14 UTC refresh, Parts' primary paper still states the
[509-vertex, 2,442-edge construction](https://arxiv.org/abs/2010.12665v2), and
Haugland's August 2026 paper still identifies 509 as the
[current unrestricted record](https://arxiv.org/html/2608.04542v4).  The
target's Discovery artifact
`bafkreifvhaslflduege3hsx5mr5pv6mk7gqz3vun3xlst6cvsgok53dcdu` remained absent
from the stale committed index at height 4363 and is treated as pending, not
committed.

## Reproduction and trust boundary

From the repository root:

```bash
python3 -m venv /tmp/hn-three-diamond-review1-venv
/tmp/hn-three-diamond-review1-venv/bin/pip install -r \
  hadwiger_nelson_three_diamond_palette_chain_review1/requirements.txt
PYTHONDONTWRITEBYTECODE=1 /tmp/hn-three-diamond-review1-venv/bin/python \
  hadwiger_nelson_three_diamond_palette_chain_review1/independent_check.py \
  | cmp - hadwiger_nelson_three_diamond_palette_chain_review1/EXPECTED.json
cd hadwiger_nelson_three_diamond_palette_chain_review1
sha256sum -c SHA256SUMS
```

The checker imports no target module.  The trust boundary is SymPy 1.14.0's
exact algebraic-number implementation, CPython exact finite enumeration and
hashing, ordinary hardware, and the reviewer's unformalized structural proof.
It uses no SAT/SMT solver, floating-point decision, hidden coordinate file,
network input, or omitted certificate.  This is not a proof-assistant
formalization.
