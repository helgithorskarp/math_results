# Four cyclic quarter-turn P36 patches are four-colourable

This package closes one exact empty-intersection construction family below
the Hadwiger--Nelson record threshold.

Let

```text
P36 = {a+b*omega : a^2+a*b+b^2 <= 36},
omega = (1+i*sqrt(3))/2.
```

For every ordered pair `p,q in P36`, set

```text
c = (p-i*q)/(1-i),
Q_k = c + i^k(P36-c),  k=0,1,2,3.
```

Adjacent patches share a cyclic orbit of anchor points.  The complete strict
physical unit-distance graph on the union of the four patches is
**four-colourable for all 16,129 ordered anchor pairs**.

For `p != q`, the four patches have empty total intersection and exactly
**504 distinct points**.  There are 16,002 such placements.  Their complete
graphs have between 1,368 and 1,592 edges, and all are four-colourable.  This
is a restricted-family exclusion, not a five-chromatic graph, record advance,
or global vertex bound.

## What was tested

The family is the smallest direct symmetric closure suggested by the earlier
common-point result: it retains four copies of the 127-point patch, uses no
larger ambient radius, forces four pairwise collisions (so the exact budget is
504), and has empty total intersection whenever the two chosen anchors differ.

The center family has 1,408 orbits under the exact dihedral symmetries of P36.
Of these, 797 admit a checked residue/XOR four-colouring.  The other 611 have
literal positive four-colour words in [colourings.json](colourings.json).
The word file is 345,804 bytes.  No negative solver verdict is used.

The construction includes genuinely interacting collars:

- 15,342 empty-intersection placements have only the constituent-patch edges
  after the four collisions are merged;
- 660 placements, forming 58 symmetry orbits, have additional unit contacts;
- the densest has 504 points and 1,592 complete strict unit edges.

Every one remains four-colourable, so this fixed quarter-turn source is
retired at its declared physical signal gate.

## Exact verification

Coordinates are integer quadruples representing

```text
((a+b*sqrt(3))/4, (c+d*sqrt(3))/4).
```

An exact coefficient test enumerates all twelve unit vectors possible in this
module.  [verify.py](verify.py) independently reconstructs every collision-
merged point set and obtains every edge by coordinate lookup.  It imports no
producer code.  It checks the residue words and all 611 stored positive words
on the reconstructed graphs.

[controls.py](controls.py) separately derives adjacent and opposite interfaces
from 16,129 offset buckets and 469 sum buckets.  For all 1,408 canonical
centers, its point and edge sets agree entry for entry with the direct
reconstruction.  It also rejects a deliberately monochromatic word.

The main graph and colour-cover hashes are

```text
graph stream   17a1dcfc78e3fb9069ed9deaff70a7cedd0916a0cece473eb8b558dc3d075b46
colour cover   41b1b660fc4bdd5ddb5ec669f91d74790c5b4eb91bd07d62497be8cd04abd7dd
certificate    aaa9a6813981c01d69e4ca278a6e882dbee0de6d27b30b57f8a567662e1a8221
```

See [PROOF.md](PROOF.md) for the construction and completeness argument.

## Reproduce

Python 3.11 or later; standard library only.  From this directory:

```bash
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
python3 -B controls.py --check-expected
python3 -O -B controls.py --check-expected
sha256sum -c SHA256SUMS
```

Optional byte-for-byte positive-certificate regeneration:

```bash
python3 -B produce.py /tmp/p36-quarter-turn-colourings.json
cmp colourings.json /tmp/p36-quarter-turn-colourings.json
```

The producer uses a deterministic finite-domain search only to find positive
words.  Verification does not trust the search, its node counts, or a solver
library.  The trust boundary is the displayed finite construction, the
dihedral reduction, the exact coordinate and unit-vector arithmetic, the
published positive words, the Python implementations, and ordinary hardware.
This is author-side computer-assisted evidence pending independent review.

## Context and limits

The preceding [common-point theorem](../hadwiger_nelson_four_triangular_radius147/README.md),
now [independently accepted with high confidence](../hadwiger_nelson_four_triangular_radius147_review1/README.md),
already closes arbitrary four-P36 placements with a common physical point.
The present theorem reaches a concrete nonconcurrent, empty-total-intersection
family at 504 points.  It does not cover other relative angles, arbitrary
translations, non-cyclic four-patch motions, or general plane unit-distance
graphs.  A residue conflict alone is not treated as a chromatic signal; every
such case here has a checked unrestricted four-colouring.

The current unrestricted published benchmark remains Jaan Parts's
[509-vertex, 2,442-edge graph](https://arxiv.org/abs/2010.12665).  Haugland's
[2026 paper](https://arxiv.org/abs/2608.04542) also identifies 509 as the
current vertex record; its 2,131-point construction has the additional
Moser-spindle-free condition.  A bounded primary-source and Discovery Net
refresh on 2026-09-14 found no sub-509 construction and no matching committed
quarter-turn-collar result.  No historical-priority claim is made.

Discovery contribution
`bafkreigvlanexeryawfsdffd3vkjuqkasmjad6s7ve4uo4qtqigbaprpza` was accepted
for broadcast once in transaction
`A8DA1FD85EF35663E2F2082594154DE23F59E87BA2FD75306FFED4108F5280AF`.
It was still absent from the stale index at height 4363 while RPC remained at
4364, so it is **pending, not committed**, and must not be resubmitted solely
for that reason.  Exact metadata is in
[DISCOVERY_RECEIPT.json](DISCOVERY_RECEIPT.json).
