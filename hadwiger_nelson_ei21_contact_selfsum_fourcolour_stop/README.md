# Exact EI21 self-contact and commutative self-sum stop

This package certifies one fresh, plane-native use of the flexible 21-point
Exoo--Ismailescu (`EI21`) unit-distance framework.  It has two parts.

1. The framework is flexed to an isolated exact realization at which the
   previously nonadjacent vertices `0` and `14` become unit distance.  The
   resulting complete strict graph has 21 distinct points and exactly 39 unit
   edges.  It is four-chromatic, has no bridge or articulation vertex, and the
   new physical contact blocks an explicit complete colouring of the original
   38-edge source while another complete colouring survives.
2. The sole declared capped continuation is the commutative self-sum
   `P+P={p_i+p_j: 0<=i<=j<21}`.  It has 231 formal addresses and between 210
   and 231 distinct physical points.  An exact conservative reconstruction
   produces 210 possible-equality clusters and 731 possible unit edges.  The
   supplied proper four-colour word colours this conservative supergraph and
   therefore the complete actual strict unit graph.  Since `p_0+P` is an
   isometric copy of the four-chromatic contact graph, `P+P` has chromatic
   number exactly four.

This is a scoped stopping result, not a five-chromatic graph and not progress
on the 509-vertex record.  The selected contact/self-sum architecture is
retired.  The package does not classify other EI21 flex parameters, other
self-contacts, or other operations.

## Reproduce the proof

The theorem verifier uses only the Python standard library:

```bash
python3 verify.py
python3 -O verify.py
python3 controls.py
```

The normal and optimized verifier outputs must equal `EXPECTED.json`, and all
seven corrupted-certificate controls must be rejected.

Optional byte-for-byte certificate regeneration uses the pinned dependencies:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-producer.txt
.venv/bin/python build_certificate.py /tmp/geometry_certificate.json
.venv/bin/python produce_selfsum.py /tmp/selfsum_certificate.json
cmp geometry_certificate.json /tmp/geometry_certificate.json
cmp selfsum_certificate.json /tmp/selfsum_certificate.json
```

`build_certificate.py` is an untrusted numerical producer.  `produce_selfsum.py`
uses a SAT solver only to obtain a positive colouring word.  Neither numerical
root finding nor a solver verdict is trusted by `verify.py`.

## Files

- `geometry_certificate.json`: rational midpoint, approximate inverse, source
  edges, and explicit blocked/surviving colour words.
- `selfsum_certificate.json`: conservative-graph digest, counts, and the
  positive four-colour word.
- `verify.py`: exact contraction, complete-edge, chromatic, connectivity, and
  self-sum replay.
- `controls.py`: seven semantic corruption tests.
- `PROOF.md`: proof details and scope.
- `PROVENANCE.md`: primary source, teammate boundary, and evidence refresh.
- `SHIBUYA_LICENSE.txt`: MIT licence for the adapted parametrisation.

## Result boundary

The source contact meets the campaign's strengthened intake gate: it removes
a complete colouring through a genuine nonseparable physical contact and has
a finite continuation of at most 231 points.  The continuation then hits the
mandated stop because its complete graph has a rigorous global four-colouring.
No adjacent contact, parameter, sum, difference, phase, or copy sweep follows.
