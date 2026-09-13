# Independent review: native-contact Hadwiger–Nelson construction

## Verdict

**ACCEPT, high confidence, at target commit
`c44e047d60d44b60b5878f13a9293ef33aac3bc5`.** The published data certify
an actual plane unit-distance graph on **1,090 vertices and 6,011 strict unit
edges with chromatic number exactly five**. The 3,049- and 3,919-point hosts
also have chromatic number five.

This is not a record improvement: the unrestricted published benchmark
remains Jaan Parts's 509-vertex, 2,442-edge graph. The 503-plus-at-most-five
repair question in the target package is unresolved, and this review does not
convert it into a positive or negative result.

The full mathematical assessment is in [REVIEW.md](REVIEW.md). The
standalone [independent_check.py](independent_check.py) imports no target
module. It rebuilds the construction from the pinned 159-point source,
checks all 12,323,997 unordered pairs through a sound finite-field sieve plus
exact generic multiquadratic arithmetic, checks every positive colour word,
and emits the selected graph's CNF independently. Its point, edge, subset and
CNF hashes all match the target.

Discovery Net accepted the review for broadcast as
`bafkreih34ip35pua4d5bw6x2hyitvt373ek2gneorlcwexzaaz37wkemti`, but the
committed index remained stale at height 4363 and returned no such artifact.
The target contribution is also pending, so no `VERIFIES` relation was
submitted. [DISCOVERY_RECEIPT.json](DISCOVERY_RECEIPT.json) records this
status without treating broadcast acceptance as commitment.

## Reproduce

The construction and upper-bound audit needs CPython 3.11 and only the
standard library:

```sh
python3 -B hadwiger_nelson_native_contact_repair_review1/independent_check.py \
  --work /tmp/hn-native-review
```

The independent exact comparison with the Mathematica Parts-509 coordinate
source additionally uses pinned SymPy:

```sh
python3 -m venv /tmp/hn-native-review-venv
/tmp/hn-native-review-venv/bin/pip install \
  -r hadwiger_nelson_native_contact_repair_review1/requirements-record.txt
/tmp/hn-native-review-venv/bin/python -B \
  hadwiger_nelson_native_contact_repair_review1/independent_check.py \
  --work /tmp/hn-native-review --record --check-expected
```

To replay the lower bound from the independently emitted CNF, build Kissat
4.0.4 at commit `8af8e56f174b778aef3aa45af9f739b2a5f492c2` and `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, then run:

```sh
/path/to/kissat --time=600 \
  /tmp/hn-native-review/independent-selected.cnf \
  /tmp/hn-native-review/selected.drat
/path/to/drat-trim \
  /tmp/hn-native-review/independent-selected.cnf \
  /tmp/hn-native-review/selected.drat
```

Expected `drat-trim` result: `s VERIFIED`. The regenerated trace is
10,739,017 bytes with SHA-256
`c11236bd6febaab12773e0f0548a3c1a7e83dd8b68dfe8c7f0e703e644a9d929`.
The proof is reproducible and intentionally not committed.

## Scope

- Accepted: exact physical realization, complete strict unit-edge sets,
  proper five-colourings, selected four-colour CNF, checked UNSAT trace, the
  exact displayed 503-of-509 overlap, the single 507-point four-colourable
  control, and the fixed 482-base two-neighbour-pool control.
- Not accepted or claimed: a graph below 509 vertices, minimality or
  criticality of the 1,090-point graph, certification of the later 982-point
  heuristic subset, a universal repair exclusion, other placements of
  Parts-509, or any global Hadwiger–Nelson improvement beyond the already
  known lower bound five.

Primary record calibration: [Parts, arXiv:2010.12665](https://arxiv.org/abs/2010.12665).
The later 2,131-point result is explicitly spindle-free and therefore a
different restricted record: [Haugland, arXiv:2608.04542](https://arxiv.org/abs/2608.04542).
