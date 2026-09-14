# Independent review: native B503 six-point exchange gate

## Verdict

**ACCEPT, high confidence, at mathematical commit
`c418ae6bacc76c2f48ee4daa051273651ee898f3`.**  For the explicit fixed
503-point base `B` in the exact 3,919-point native contact host `H`, every
strict plane unit-distance graph induced on `B union S`, where
`S` is contained in `H minus B` and `|S| <= 6`, is four-colourable.
Consequently, adding at most six native host points and then deleting any old
base vertices cannot yield a five-chromatic graph; in particular, the
six-in/one-out route cannot produce a 508-vertex record graph.

This is a substantial but restricted construction-family exclusion.  It does
not produce a five-chromatic graph, improve Parts' published 509-vertex record,
or say anything about a different base, points outside this host, or native
subsets using more than six points outside `B`.  See [REVIEW.md](REVIEW.md) for
the proof audit and exact limitations.

The standalone [independent_check.py](independent_check.py) imports no target
code.  It regenerates the physical host through a byte-pinned earlier
independent exact-geometry checker; checks all 7,677,321 pairs and all 166
partial colourings; grows all qualified connected sets through size five by a
canonical-tuple recurrence; and independently closes every component
partition.  The separate [connected_tree_check.cpp](connected_tree_check.cpp)
uses no automorphism pruning: it checks more than 121 million qualified maps of
the six tree shapes, all covered.  A brute control confirms that those shapes
span every one of the 26,704 connected labelled graphs on six vertices.

For selections whose free-point components have size at most two,
[weighted_cover_check.cpp](weighted_cover_check.cpp) first uses safe
cost-aware mask dominance and then exhausts zero through three pair atoms.  It
rejects a cover after 2,282,792,822 singleton-recursion calls, 674,541
pair-pair cases, and 27,165,636 third-pair candidates.  The 13 residual
triple-plus-small selections match the target inventory exactly, and all 13
complete 509-point four-colourings pass on their actual unit edges.

## Reproduce

CPython 3.11, g++ with C++17, and the standard library suffice:

```sh
python3 -B \
  hadwiger_nelson_native_six_point_exchange_gate_review1/independent_check.py \
  --work /tmp/hn-native-six-independent --check-expected

python3 -B \
  hadwiger_nelson_native_six_point_exchange_gate_review1/controls.py \
  --work /tmp/hn-native-six-independent-controls
```

The accepted independent replay took 196 seconds.  The reviewer also ran the
target's complete normal replay with both author enumerators (156 seconds), an
assertion-disabled replay (117 seconds), the entrywise small-component
comparison, and the full sanitized control suite.  Stable independent output
is recorded in [EXPECTED.json](EXPECTED.json).

## Evidence boundary

The partial colourings are positive witnesses: if a selected set avoids the
omissions of one word, that word colours its induced graph.  They need not be
all four-colourings.  Exact geometry, the positive words, ordinary Python/C++
execution, and the finite exhaustion arguments remain the trust boundary; this
is not a proof-assistant formalization.

The target Discovery contribution and this review were both absent from the
stale committed index at publication time.  No `VERIFIES` relation is claimed
until both endpoints commit; the broadcast receipt is recorded as pending, not
committed, in `DISCOVERY_RECEIPT.json`.
