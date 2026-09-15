# Independent review of the frozen F29/bowtie coupler

Verdict: **accept with a strict local-coupler limitation**.

An independent exact implementation confirms that the proposed support is an
actual **34-point, 82-edge plane unit-distance graph**. The 29-point F29 set
and five-point bowtie set have no point collision, and their only cross edge
is the private-centre contact `0--29`. The complete joint four-colour terminal
relation is exactly

```text
(isolated F29 relation) x (isolated bowtie relation), restricted by P != Q,
```

where `P` is the palette on the fourteen marked F29 neighbours and `Q` is the
palette on the four bowtie leaves. The component projections remain full.

This is a genuine strict relation loss, not a count inferred from an abstract
graph. It is also not a five-chromatic construction: the sole cross edge is a
bridge, a checked proper four-colouring exists, and the complete graph has
chromatic number exactly four. No receiving frame or Parts boundary was
tested.

## Independently recovered quantities

| Quantity | Result |
|---|---:|
| Exact point pairs reconstructed | 561 |
| Physical points / complete unit edges | 34 / 82 |
| F29 / bowtie / cross edges | 75 / 6 / 1 |
| Bare canonical F29 terminal patterns | 6,336 |
| Extending / rejected F29 patterns | 5,109 / 1,227 |
| Isolated bowtie leaf patterns | 120 |
| Surviving / lost joined leaf patterns | 96 / 24 |
| Isolated joint canonical patterns | 613,080 |
| Joined / lost canonical patterns | 490,464 / 122,616 |
| Relative relation loss | 20% |
| Chromatic number | 4 |

The reviewer checker uses direct closed-form squaring in
`Q(sqrt(3),sqrt(11))`, unlike both target radical engines. It enumerates all
`3^13` named F29 terminal words with the first terminal fixed, canonicalizes
the complete proper set, and tests extension with a fixed-order frontier
dynamic program of width four. The target uses domain recursion and a separate
DSATUR producer. The review recovers the target's point, edge, distance and
allowed-pattern hashes entry-for-entry.

The certificate includes a freshly generated proper four-word whose F29
terminal pattern is `01222211102221`; it differs from the target word in 25 of
34 positions. A target conditional five-word is checked only to confirm that
the excluded equal-palette terminal prescription is consistent with five
colours. It is not evidence of ordinary five-chromaticity.

## Reproduction

CPython 3.11 or later; standard library only. From this directory:

```sh
python3 -B verify.py --check-expected
python3 -O -B verify.py --check-expected
python3 -B controls.py
sha256sum -c SHA256SUMS
```

The controls compare the frontier algorithm with direct brute force on all
153,664 combinations of a labelled four-vertex graph and four nonempty
three-colour lists, in three vertex orders (460,992 comparisons). They also
check the quartic square formula on 625 coefficient vectors and reject a
modified coordinate table and three semantic certificate corruptions. See
[PROOF.md](PROOF.md) and [VALIDATION.json](VALIDATION.json).

## Scope and record status

The theorem concerns exactly this fixed support and its eighteen-terminal
interface. It does not show that the relation conflicts with any receiver,
that repeated copies amplify it, or that there is a finite completion to a
non-four-colourable graph. Additional identifications or contacts could make
the local relation useful, but those are new geometries requiring complete
checks. Repeating components using bridge edges alone cannot raise their
ordinary chromatic number.

Accordingly this is local construction evidence, not global Hadwiger--Nelson
progress and not a record candidate. Parts's published 509-vertex, 2,442-edge
five-chromatic construction remains the supported record in the bounded
primary-source check, also identified as current by Haugland's August 2026
paper.

## Sources

- Reviewed package (branch path):
  <https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_frozen_bowtie_palette_coupler>.
  The exact reviewed revision is
  `18b6c94617ca9807f7f9f3da2ba42e10e6780df6`.
- F29 provenance package (branch path):
  <https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_frozen_centre_transfer>.
  The pinned source revision is
  `ef05942eeebba29628dc02f37a5792ac7d4122b8`.
- Parts, [Graph minimization, focusing on the example of 5-chromatic
  unit-distance graphs in the plane](https://arxiv.org/abs/2010.12665).
- Haugland, [A Moser-spindle-free 5-chromatic unit distance graph on 2131
  vertices in the plane](https://arxiv.org/abs/2608.04542).

The requested `math-review` skill was unavailable in this session. Its
independence, scope, geometric-realization, chromatic-certificate,
hidden-assumption and source-integrity criteria were applied directly with the
available exact-computation and GitHub research skills.
