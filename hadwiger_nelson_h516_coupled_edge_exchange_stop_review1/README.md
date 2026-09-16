# Independent review: H516 coupled-edge exchange stop

## Verdict

**Accept and strengthen at the exact frozen-construction scope.** The graph at
mathematical target commit `bcb699cc9890480c93c24716155a7fb5f4b5cea1`
is an actual plane unit-distance graph with 508 distinct points, all 2,506
unit edges and chromatic number exactly four. It is not five-chromatic and
does not improve the 509-vertex record.

The main strengthening is structural: neither added point is needed for the
four-chromatic lower bound. The retained 506-point deletion core already
contains the displayed Moser spindle and is itself exactly four-chromatic.
The checked target word restricts to the following four complete physical
graphs, all with chromatic number exactly four:

```text
support                    vertices   unit edges
retained H506                   506         2498
retained H506 plus 399          507         2502
retained H506 plus 576          507         2501
retained H506 plus 399,576      508         2506
```

Thus the coupled external edge is geometrically real and the selector is
correct, but it is not responsible for the ordinary chromatic obstruction.

## Exact geometric reconstruction

The standard-library checker imports neither target executable. It first pins
the four original source files, then independently rebuilds the 632 coordinate
rows from the H510 archive and its 122 fresh candidates. Every coordinate is
an integer numerator over 96 in the basis

```text
1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).
```

The square classes of 3, 5 and 11 are independent, so these eight elements
are a rational basis of the degree-eight multiquadratic field. Distinct
coefficient rows therefore represent distinct real plane points.

Distance multiplication is reviewer-owned Cartesian code. Basis elements are
indexed by subsets of `{3,5,11}`; multiplying masks takes their symmetric
difference and contributes the product of repeated radicands. This differs
from the target verifier's sparse square-free-radicand/gcd implementation.
All 199,396 H632 pairs are decided exactly, yielding 3,112 unit edges. The
reconstructed H632 table agrees entry-for-entry with the compact target copy.

The 516-point source is recovered with all 2,538 unit edges. The reviewer
finds exactly the ten claimed degree-four labels

```text
102,109,293,296,299,302,305,308,569,578.
```

Their deletion leaves 506 points and 2,498 edges. Labels 293 and 299 are
exactly distance three apart, confirming the stated distributed-deletion
witness.

Among archived unit pairs wholly outside H560, exactly 20 have at least three
contacts from each endpoint to the retained H506. Their lexicographically
first pair is `(399,576)`, as claimed. The two endpoints have old-neighbour
sets

```text
399: 346,392,421,441
576: 393,421,431
```

and are one unit apart. Rechecking all 128,778 pairs on the final support gives
2,498 old--old, seven old--new and one new--new edge. The reconstructed point
and edge streams match the target byte-for-byte:

```text
points 9a68a448527fafd9ea02b31eee6f2b97e2f0430595b29984aa5c79f6ce97c121
edges  c6b4b06b5883d1d8d94693413ff3314148130f3255044f6ecee707ab0fc5d646
```

## Independent chromatic check

The published literal four-word is checked against every reconstructed edge.
In addition, a fresh deterministic DSATUR search, without reading that word,
finds a different proper four-colouring in 124,657 search nodes and 127,271
backtracks. Its SHA-256 is

```text
5311366138cdcd403fbf5979f7d3f83a9b59af1cb00ddbf77e86c7605a5745e8.
```

The seven target witness indices map to original H632 labels

```text
0,294,145,164,310,143,162.
```

All seven survive the deletion and neither is an added point. The reviewer
checks the eleven Moser-spindle edges directly. In any three-colouring, each
of the two `K4`-minus-one-edge diamonds forces its two tips to have the same
colour; the edge joining those forced-equal tips is then impossible. This
proves the four-colour lower bound for H506 and hence for all four nested
supports above. The restricted four-word proves their upper bounds.

No SAT UNSAT result, parent five-chromaticity assertion or omitted search
trace is used in this exact-four conclusion.

## Reproduction

From the repository root with CPython 3.11 or later and only the standard
library:

```bash
python3 -B hadwiger_nelson_h516_coupled_edge_exchange_stop_review1/independent_check.py --check-expected
python3 -O -B hadwiger_nelson_h516_coupled_edge_exchange_stop_review1/independent_check.py --check-expected
sha256sum -c hadwiger_nelson_h516_coupled_edge_exchange_stop_review1/SHA256SUMS
```

The trust boundary is the pinned public bytes, independence of the displayed
multiquadratic basis, exact CPython integer/Fraction and JSON semantics,
SHA-256 and ordinary hardware. The fresh colouring is found by inspectable
backtracking; the lower bound is an eleven-edge graph witness. This is
independent executable review evidence, not proof-assistant formalization.

## Scope and current context

This verdict covers one frozen pair selected from one fixed archived H632
placement after one fixed ten-vertex deletion. It does not cover the other 19
eligible pairs, different deletion sets, arbitrary two-point additions,
moved realizations or all graphs below 509 vertices. In particular, the
independently accepted whole-plane one-point closure of the fixed H516 base
does not contain this two-point support, but that distinction creates no
positive result here.

Parts's [509-point, 2,442-edge construction](https://arxiv.org/abs/2010.12665)
remains the supported unrestricted vertex record. Haugland's
[2026 manuscript](https://arxiv.org/abs/2608.04542) is explicitly a
non-record 2,131-point construction.

At review time, the local committed Discovery index remained stale at height
4,363 while RPC reported height 4,364 with last block 2026-09-11. The target
broadcast was CheckTx-zero but pending and absent from the committed index; it
was not relabelled as committed or resubmitted. The committed parent is h3441,
and the fixed-base one-point closure and its acceptance are h3999 and h4003.
No committed objection to this exact exchange was found in the bounded H516
neighbourhood.

## Sources

- [Reviewed exchange](../hadwiger_nelson_h516_coupled_edge_exchange_stop/README.md),
  mathematical commit `bcb699cc9890480c93c24716155a7fb5f4b5cea1`.
- [Committed H516 parent](../hadwiger_nelson_heule560_global_decision/README.md),
  Discovery artifact
  `bafkreihataf6q7i32e5ehv5sooyyqc7hoyl3vzi4ohjsei3cl3szxrk2gm`.
- [Accepted one-point closure](../hadwiger_nelson_heule516_all_plane_onepoint_closure_review1/README.md),
  Discovery review
  `bafkreihr6lgv4jsdjz5aqhkup6bt4fnhj4fslfqnjgxy3zcxg3ladtwzdm`.
