# Exact A159 bridge assemblies in the sqrt(6) extension

**All 51,680 specified 474-point plane assemblies are four-colourable.**
For `u=(sqrt(6)+i sqrt(3))/3`, let `B=A union uA`, where A is the archived
Parts 159-point, 646-edge gadget. Attach a third isometric A by identifying
any oriented unit edge with any of the 20 cross edges between the two
components of B, allowing either chirality. Every resulting complete unit
graph has exactly 474 distinct points and a checked four-colouring.

The stronger certificate covers all attachments along any *one* of those
bridges simultaneously: each complete orbit host has 8,743 points. A
separate two-bridge pilot, for source pairs (70,113) and (111,75), has
17,168 points and 152,201 unit edges and is also four-colourable. All labels
are zero-based original A labels. The assertions also hold for the other
algebraic root `(-sqrt(6)+i sqrt(3))/3`.

This is a restricted construction boundary, not a global vertex bound or
a five-chromatic graph. Unions involving other bridge pairs, other phases,
and other geometries remain outside the claim. This lane retires the
selected phase at this boundary; it does not increment a repair allowance.

A preliminary field gate eliminates 1,260 of the 1,490 archived outside-E
origin-rotation contact quadratics: their *entire* coordinate fields admit
four-colourings by the classical 2-adic residue mechanism. The remaining
230 quadratics belong to seven quadratic extensions over E; passing this
gate is only a necessary condition. The phase used above belongs to the
42-class extension E(sqrt(6)). Six other extensions remain construction
options. See [PROOF.md](PROOF.md) for definitions, argument, and limits.

## Reproduce

From the repository root, using Python 3.11+ and g++ 12.2/C++17:

```sh
python3 -B hadwiger_nelson_ramified_a159_bridge_orbits/verify.py --work /tmp/hn-bridge-orbits --coupled
python3 -B hadwiger_nelson_ramified_a159_bridge_orbits/field_filter.py --work /tmp/hn-bridge-fields
```

The first command regenerates exact points, all required unit pairs and
physical identifications, then verifies positive colourings. It takes
about seven seconds on the author's host. No SAT solver, floating-point
test, or nonstandard Python dependency is needed. `--sanitize` adds C++
undefined-behaviour checks. The expected compact outputs are in
[expected.json](expected.json). Normal and optimized Python runs with
C++ sanitization passed. A separate Cartesian radical calculation agrees
on all 8,649 control pairs, including 118 unit pairs; four malformed words
are rejected. Run it with `python3 -B hadwiger_nelson_ramified_a159_bridge_orbits/controls.py --work /tmp/hn-bridge-controls`.

The two-bridge positive word was found by CaDiCaL153 through python-sat
1.8.dev17 (32,971 conflicts). The public checker independently checks that
word against regenerated complete exact edges; its validity does not
rely on a solver's answer. The 51,680 individual attachments and the 20
single-bridge hosts need no SAT query.

## Provenance and scope

The input point file and field-colouring module are pinned by SHA-256 in
`verify.py`. `field_filter.py` also pins the existing exact contact census.
Sources are the sibling directories
`hadwiger_nelson_nonmono159_214_lowden2`,
`hadwiger_nelson_nonmono_field_obstruction`, and
`hadwiger_nelson_nonmono159_origin_pencil`.

The prior package `hadwiger_nelson_parts159_three_rotations` already closes
three rotations sharing the *published origin*. The current third copy
uses a cross-component unit bridge; its translation is generally nonzero.
It was selected to escape that earlier scope while retaining a sub-509
physical budget. Terminal-only composition results do not account for
these interior contacts. Conditional h4117/h4175/h4177 accounting is unused.

The residue-colouring mechanism is prior work, described by David Speyer
in the April 2018 Polymath16 discussion and proved explicitly in the field
package. No method novelty is claimed. This package applies it to the
contact-quadratic frontier and supplies new exact finite construction
checks. Validation is by the author, not independent-author review or
formalization. Large point/edge dumps, the two 51,680-case exact replay
streams and all exploratory logs remain local; the source regenerates the
mathematically relevant evidence.

The published plane vertex benchmark remains 509 in
[Parts](https://arxiv.org/abs/2010.12665) and the introduction to
[Haugland's August 2026 manuscript](https://arxiv.org/html/2608.04542v1).
No improved witness was found in this pass.
