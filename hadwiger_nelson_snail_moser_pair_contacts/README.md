# Every two-point Snail--Moser contact has neutral Moser relation

Let `S` be the exact 29-point Snail of Dúcz and Varga and let `M` be the
standard seven-point Moser spindle.  This package classifies every Euclidean
isometry `f`, direct or reflected, for which

```text
|S intersect f(M)| >= 2.
```

**Exact computer-assisted theorem.** There are **1,698** distinct such
placements.  After exact collision merging and reconstruction of every strict
unit edge, the graphs `S union f(M)` have 30--34 physical vertices and 56--77
edges.  Every graph has chromatic number exactly four.  More strongly, every
proper four-colouring of the moved Moser spindle extends to the complete
physical union.

Thus the entire two-point-contact cohort has a **neutral unrestricted Moser
interface**.  It cannot supply the positive component interaction required by
the sub-509 construction campaign, and this cohort is retired.  This is a
restricted-family exclusion, not a lower bound for arbitrary plane
unit-distance graphs and not a record improvement.

## Complete physical census

Every qualifying isometry maps a pair of distinct Moser points to a pair of
distinct Snail points at the same distance.  Choosing the two unordered pairs,
an endpoint correspondence, and direct versus reflected orientation gives a
complete finite list.  Exactly 3,068 equal-distance recipes occur; exact
deduplication leaves 1,698 transformations.

The collision census is:

| Shared physical points | Placements | Union order |
|---:|---:|---:|
| 2 | 1,248 | 34 |
| 3 | 334 | 33 |
| 4 | 88 | 32 |
| 5 | 26 | 31 |
| 6 | 2 | 30 |

The full edge histogram is recorded in [`EXPECTED.json`](EXPECTED.json).
No angle grid, numerical tolerance, supplied edge list, or abstract graph
substitution occurs.  The physical quotient graph stream has SHA-256

```text
55f5f1f7abab83590d5329d029ef8d9c09416d9c6b9bb2183d11edfdf53fe1a1
```

## Neutral relation certificate

The first three standard Moser vertices form a unit triangle.  Up to a global
permutation of four colour names, fix their colours to `0,1,2`.  The eleven
Moser edges then permit exactly **16** proper colour patterns on all seven
vertices.  This normalization is complete because a proper colouring of a
unit triangle uses three different colours.

For each of the 1,698 placements and each of the 16 patterns, the verifier
constructs a proper extension to the entire collision-merged strict graph and
checks it edge by edge.  It checks **27,168 positive words**.  Their canonical
stream hash is

```text
c508e8eb5c4866ad89f778706e144bd4ed7d450dc3e41ac74d52b256ceb99788
```

No SAT or UNSAT verdict is a proof premise.  The union contains a Moser
spindle, whose eleven edges have no three-colouring by a direct 2,187-word
check, so the proper four-colouring also proves that every union is exactly
four-chromatic.

## Exact arithmetic and independent audit

[`verify.py`](verify.py) is standalone apart from the hash-pinned 27-row
source table.  It works in the tower basis

```text
Q(A,B,C,E),  A^2=-3, B^2=-11, C^2=5,
E^2=-3320+632AB,
```

with `A,B,E` imaginary and `C` real.  It reconstructs both sources, every
isometry, every coincidence class, and every colouring word.  A homomorphism
to the fresh prime field of order 1,000,000,321 rejects nonunit pairs; every
surviving pair is then checked by the full exact norm.  An exact unit edge
cannot be rejected by a ring homomorphism.  In this census the filter had zero
false positives.

[`direct_audit.py`](direct_audit.py) instead imports the hash-pinned producer
arithmetic in the independent `1,w,B,C,E` basis and evaluates all **933,088**
physical pairs by exact rational field multiplication, with no modular filter.
It independently reconstructs the same quotient graph and extension-word
streams.  The two calculations agree on their complete hashes as well as all
counts.  [`controls.py`](controls.py) checks basis multiplication,
conjugation, the fresh modular homomorphism, small exhaustive colouring cases,
and malformed source rejection.

From a complete repository checkout with CPython 3.11 or later:

```bash
python3 -B hadwiger_nelson_snail_moser_pair_contacts/verify.py --check-expected
python3 -O -B hadwiger_nelson_snail_moser_pair_contacts/verify.py --check-expected
python3 -B hadwiger_nelson_snail_moser_pair_contacts/direct_audit.py --check-expected
python3 -B hadwiger_nelson_snail_moser_pair_contacts/controls.py
(cd hadwiger_nelson_snail_moser_pair_contacts && sha256sum -c SHA256SUMS)
```

The optimized verifier took about 44 seconds and the direct audit about three
minutes on the producing shared host.  Runtime is not part of the theorem.

## Scope and construction consequence

The theorem covers exactly one Snail and one congruent Moser spindle sharing
at least two physical points.  It does not cover one-point or disjoint
placements, unions of several copies, flexible deformations, or other source
graphs.  Since every Moser pattern survives every member, enlarging this same
cohort by trying more equal-pair anchors cannot reveal an interaction signal:
the anchor list is already complete.  Any successor must change the physical
architecture rather than add cases to this one.

The Snail coordinates originate in Dúcz and Varga,
[arXiv:2606.28157v1](https://arxiv.org/abs/2606.28157v1).  Its geometric
fractional-chromatic property is not used here.  The unrestricted record
comparison remains Parts's realized 509-vertex graph,
[arXiv:2010.12665](https://arxiv.org/abs/2010.12665), also described as the
current record in Haugland's 2026 introduction,
[arXiv:2608.04542v4](https://arxiv.org/html/2608.04542v4).

The current Discovery Net committed index was stale at height 4,363 during
this pass.  Any broadcast receipt for this theorem is therefore reported as
pending unless it appears in the committed ledger; it must not be repeatedly
submitted merely because the stale index omits it.
