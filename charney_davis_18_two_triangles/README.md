# Two-triangle bound for the eighteen-vertex Charney--Davis frontier

For a finite flag generalized homology 5-sphere whose one-skeleton
complement has degree sequence `3^10 4^8`, the complement has **at most two
triangles**. Thus its gamma vector must be `(1,6,8,-2-T)` with `T=0,1,2`.
The earlier conditional bound was `T<=8`.

The [proof](PROOF.md) also shows that the subgraph induced by the ten cubic
vertices is triangle-free and has 7--10 edges. At ten edges its only
possibilities are `C10`, `C5 + C5`, and `Theta(1,4,4) + K2`, where plus
denotes disjoint union. At least two of the eight quartic vertices have
suspension links.

These are necessary constraints. No sphere with this degree sequence is
constructed or excluded here; the full eighteen-vertex Charney--Davis
problem remains unresolved. Independent review of this note is outstanding.

The predecessor is the [ten-cubic profile reduction](../charney_davis_18_ten_cubic_rigidity/README.md).
This note assumes its final degree sequence directly, so its proof does not
depend on the predecessor's case table. The older
[independent review](../charney_davis_18_review1/README.md) covers only the
nine-high-degree result, not this note or the intervening extensions.

The main mechanism is an edge-link count: a vertex of degree three in the
cubic subgraph must see its entire component within distance two. Its
second layer is a matching once triangles are excluded. Counting the
resulting branches bounds the cubic edges and leaves too little quartic
link gamma mass for three triangles.

## Reproduction

Python 3.11.2 was used; only the standard library is required. From this
directory:

```sh
python3 verify.py > /tmp/charney18-two-triangles.json
diff -u EXPECTED.json /tmp/charney18-two-triangles.json
python3 -O verify.py > /tmp/charney18-two-triangles-optimized.json
diff -u EXPECTED.json /tmp/charney18-two-triangles-optimized.json
sha256sum -c SHA256SUMS
```

The checker takes about one second on the publication host. It checks:

- 4,687 edge-link identities against direct induced-graph edge counts on
  128 deterministic fixtures with the target degree sequence;
- all 36,396 child graphs in the small rooted configurations after the
  proved radius-two reduction, including the triangle-root case;
- the edge and low-degree bounds on every surviving rooted configuration;
- thirteen numerical cases for cubic edges and the two types of triangles;
- the face vectors and suspension pairs of the two small link models used
  in the zero-gamma suspension consequence.

`EXPECTED.json` contains the compact output. All validation remains active
with `python -O`. The fixture graphs are not claimed to be spheres, and
the rooted check is not a census of spheres. The human proof supplies
the reduction; Davis--Okun and the stated Labbé--Nevo results supply the
topological inputs. No solver, external graph catalogue, or formalization
is required. Exploratory graph generation is not part of the published
evidence.

## Primary sources and status

- [Davis--Okun, Theorem 11.2.1](https://arxiv.org/abs/math/0102104): the
  three-dimensional Charney--Davis input.
- [Labbé--Nevo, arXiv:1612.01169v2](https://arxiv.org/pdf/1612.01169v2):
  antipodes, suspension structure, and the two small-link types.
- [Nevo--Petersen, Section 5](https://pi.math.cornell.edu/~eranevo/homepage/gammakrk11revE.pdf):
  the earlier small-vertex gamma results, checked for overlap.

Literature and the relevant committed Discovery Net neighborhood were
refreshed on 19 September 2026. The thirteen-vertex zero-gamma suspension
lemma is explicitly derived from the cited literature. Novelty of the
conditional eighteen-vertex constraints is search-relative; no global
priority claim is made.

Next mathematical question: can the forced suspension links be compatible
with the cubic component structures and the remaining values `T=0,1,2`?
