# Dense inner-gadget attachment exclusion

Let A be Parts' archived 159-point gadget, V his archived 214-point gadget,
and

```
B = A union (conjugate(A) + (5+sqrt(33)+5i sqrt(3)-i sqrt(11))/12).
```

**Every Euclidean isometry g with 0 in g(V) gives a four-colourable strict
unit-distance graph on B union g(V).** The union has at most 506 vertices.
This covers all angles, reflections and all 214 source attachment vertices,
at the one specified B origin. It does not cover disjoint placements,
other B attachment vertices or graph completion by new points.

The inner B has 293 vertices and 1,389 strict edges. It was selected from
the existing A159 overlap catalogue for its maximal recorded edge count
among the 6,435 entries small enough to accompany V within 508 vertices.
It has 138 more edges than the previously studied 292-vertex inner gadget.
That extra internal density still does not obstruct this attachment family.
There is no five-chromatic record improvement.

[PROOF.md](PROOF.md) gives the universal angular reduction, exact scope and
trust boundaries. The finite certificate has 303,730 irreducible quadratic
classes and 5,189,194 nonempty anchor/class cases, all covered by 4,480 bytes
of explicit component colourings. An independent rational census matches
the classification and complete edge groups; a separate direct permutation
audit matches the coverage. Two explicit algebraic realizations attain the
maximum 23 new cross edges, producing 506-vertex, 2,389-edge graphs.

## Reproduce

From this directory in a complete repository checkout, with Python 3.11
or later and the standard library:

```bash
python3 verify.py > /tmp/hn-dense506.json
cmp expected.json /tmp/hn-dense506.json
python3 audit.py > /tmp/hn-dense506-audit.json
cmp expected_audit.json /tmp/hn-dense506-audit.json
python3 controls.py > /tmp/hn-dense506-controls.json
cmp expected_controls.json /tmp/hn-dense506-controls.json
python3 catalogue.py > /tmp/hn-dense506-catalogue.json
cmp expected_catalogue.json /tmp/hn-dense506-catalogue.json
sha256sum -c SHA256SUMS
```

`verify.py --anchors /tmp/hn-dense506-anchors.tsv` optionally writes all 214
anchor histograms; their canonical hash is pinned in `expected.json`.
`audit.py` is slower because it constructs irreducible monic polynomials
with exact rational field arithmetic. Allow several minutes and about
1 GiB RAM. `validation.json` records measured execution costs on the
producing CPython 3.11.2 host.

The verifier's lazy colour search was compared with the complete inherited
bitmask implementation: the entire selected-witness hash and every anchor
histogram agree. The rational audit tests permutations directly. The direct
control uses integer coordinates in a separate eight-dimensional algebra
and checks every unordered physical point pair for both roots. It checks
full colourings and rejects a monochromatic-edge mutation.

## Optional positive-witness regeneration

The proof replay needs no solver. To reproduce the four discovery calls,
use a separate environment with `python-sat==1.9.dev15` and a new work
directory:

```bash
python3 generate.py --work /tmp/hn-dense506-regenerate
```

The generator uses CaDiCaL195 and limits each call to one million conflicts.
It starts from the first B row and first ten V rows in the published library,
reconstructs all 1,309 uncovered cases, and selects the case with the largest
cross-edge count, then smallest anchor and canonical class index. It saves
four further rows per component and verifies they equal the published rows.
All four discovery calls returned directly checked satisfying assignments.
Their instance hashes, constraints and timings are in `solver_provenance.json`.
A solver failure or a library miss is never treated as a non-four-colourability
certificate.

## Dependencies and research consequence

Source coordinates and arithmetic are imported from the existing
[A159/V214 artifact](../hadwiger_nelson_nonmono159_214_lowden2/README.md),
[all-anchor reduction](../hadwiger_nelson_mixed505_all_gadget_anchors/README.md)
and its rational field dependencies. The separate
[whole-field four-colouring](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md)
settles in-field multipliers. All imported files and the optional existing
compressed catalogue inputs are pinned by SHA-256. No new large output,
archive, binary or solver trace is committed. Local census dictionaries
are dispensable and can be regenerated.

This closes the selected origin-attachment milestone. A concrete next
construction question is whether one or two exact geometric completion
points can obstruct four-colourability of the explicit 506-vertex maximum
contact examples. No such completion has been tested in this artifact.

Primary context: [Parts' graph-minimization paper](https://arxiv.org/abs/2010.12665)
reports the 509-vertex graph; the introduction of
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4) still names
509 as the unrestricted record, checked on 5 September 2026. This artifact
claims a specific family exclusion, not a new record or historical priority.
