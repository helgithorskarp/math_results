# Exoo `{1,2}` source: half-scale two-coincidence family

This directory gives an exact, complete decision for a candidate-bearing
unit-distance construction family derived from the 26-point `{1,2}` graph of
Geoffrey Exoo and Dan Ismailescu.

Take their exact point set $B$, form any half-scale congruent copy
$C=(1/2)R(B)+t$, and require at least two points of $C$ to coincide with
points of $B$.  The distance-2 edges inside the source copy become genuine
unit edges inside $C$.  If any resulting strict unit-distance graph were
five-chromatic, its order would be at most 50 and would improve the 509-vertex
record by a wide margin.

The complete result is negative: all 1,446 distinct moved point sets are
four-colourable.  They come from 3,348 labeled two-coincidence
specifications.  The graphs have 49 or 50 vertices and 83 through 87 strict
unit edges.  See [PROOF.md](PROOF.md) for the completeness reduction and exact
census.

Public package: <https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_exoo_d2_halfscale>

The source coordinates are from Exoo and Ismailescu,
[The Hadwiger-Nelson problem with two forbidden distances](https://arxiv.org/abs/1805.06055),
arXiv:1805.06055.  Their paper reports 75 unit edges, 10 length-2 edges, and
chromatic number 5.  The code reconstructs the edge counts exactly, checks an
explicit five-colouring, and exhausts a four-colour search.  As a live record
calibration, [Haugland's August 2026 introduction](https://arxiv.org/html/2608.04542v4#S1)
identifies Parts' 509 vertices as the current record; the original record source is Jaan Parts,
[Graph minimization, focusing on the example of 5-chromatic unit-distance
graphs in the plane](https://arxiv.org/abs/2010.12665).

## Reproduce

Python 3.11 or later and its standard library are sufficient.

```bash
python3 verify.py
python3 controls.py
# Optional slower definition-level audit of every point pair:
python3 direct_audit.py
```

`verify.py` rebuilds all geometry over
$\mathbb Q(\sqrt3,\sqrt{11})$, checks the exhaustive placement counts and
hashes, reconstructs every strict unit-distance graph, and checks all 1,446
explicit four-colour rows.  A reference run takes a few minutes on one CPU
core.

The committed certificate can be recreated deterministically:

```bash
python3 produce.py
cmp certificate.generated.json certificate.json
```

`produce.py` uses standard-library DSATUR backtracking.  The verifier does not
trust that search for the family result: it checks each explicit positive
colouring directly.  Source publication proves neither the mathematical
reduction nor the software; the trust boundary is the short exact-arithmetic
model, the exhaustive reduction described in `PROOF.md`, Python's arbitrary
precision integer and `Fraction` implementations, and ordinary code review.

## Files

- `model.py`: exact field arithmetic, isometries, enumeration, and strict
  graph construction.
- `colour.py`: deterministic DSATUR and the compact row codec.
- `produce.py`: certificate producer.
- `verify.py`: independent positive-witness verifier and pinned-output check.
- `controls.py`: field, direct-edge, corruption, and codec controls.
- `direct_audit.py`: exhaustive pairwise edge reconstruction, independent of
  the optimized three-origin edge decomposition.
- `certificate.json`: compact colour rows and provenance-bearing metadata.
- `EXPECTED.json`: pinned exact census and digests.
- `VALIDATION.json`: captured successful verifier output.
- `DIRECT_AUDIT.json`: captured exhaustive definition-level audit output.
- `provenance.json`: primary-source and record-calibration metadata.
- `SHA256SUMS`: manifest for every committed proof or evidence file.
- `PROOF.md`: mathematical completeness and scope.
