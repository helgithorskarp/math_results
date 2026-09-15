# A fixed Snail-D3 triangle-gluing cohort is four-colourable

No sub-509 five-chromatic graph is found.  This package certifies a bounded,
geometry-first interaction of exact four-chromatic supports derived from the
Dúcz--Varga Snail.

Let `S(c,a)` be the exact `D3` support from the independently accepted Snail
dihedral classification, with distinct seed centre `c` and seed axis point
`a`.  Among its stored non-three-colour witnesses, `S(9,3)` has the largest
order, 113; the complete support has 157 points and 342 unit edges.  Freeze
`S(9,3)` and the unit triangle in its first direct embedded Snail copy.

For each of the 655 exact four-chromatic `S(c,a)`, freeze the corresponding
triangle in its first direct copy and glue it to the fixed triangle by all six
vertex bijections.  These are the six Euclidean isometries taking one marked
unit triangle pointwise to the other.  Exact collision merging and complete
strict unit-edge reconstruction give **3,930 physical graphs**, with:

| quantity | range |
|---|---:|
| distinct physical points | 157--319 |
| complete unit edges | 342--964 |
| points shared by the two supports | 4--157 |
| unit edges not internal to either input | 0--197 |

Every graph has a directly checked proper four-colouring.  The maximum-contact
member uses `S(23,15)` in reflected chirality; it has 282 points, 924 edges,
23 shared points and 197 genuinely new cross edges.  Thus this is not merely a
clique-sum colouring argument: the exact physical interactions can be dense,
but none supplies an ordinary non-four signal.

This result retires only the declared marked-triangle cohort.  It does not
classify other triangles in either support, gluing along fewer points,
translations with no marked-triangle identification, unions of three or more
supports, arbitrary Snail blow-ups, or arbitrary plane unit-distance graphs.
It is a restricted construction exclusion, not progress on the global lower
bound and not an improvement on Parts' 509-vertex record.

## Solver-free verification

From the repository root, using CPython 3.11 or later and the standard library:

```sh
python3 -B hadwiger_nelson_snail_d3_triangle_gluing_gate/verify.py --check-expected
python3 -O -B hadwiger_nelson_snail_d3_triangle_gluing_gate/verify.py --check-expected
(cd hadwiger_nelson_snail_d3_triangle_gluing_gate && sha256sum -c SHA256SUMS)
```

The checker imports the parent package's independent `a=i*sqrt(3)` quadratic-
tower arithmetic, whose bytes are hash-pinned.  The producer instead uses the
parent's `w=(1+a)/2` arithmetic.  For every row the checker reconstructs both
174-address supports, independently normalizes the marked triangle, chooses
the forced direct/reflected chirality, merges every exact collision, tests
every physical pair for unit distance, and checks the packed colour word.
It uses a different finite-field specialization only to reject nonedges; every
surviving pair receives a full exact norm calculation.

The 590,125-byte [certificate](certificate.json) contains one two-bit colour
word on the 348 formal addresses for each placement, together with physical
counts.  Coincident addresses are required to have the same colour.  Solver
soundness is not a theorem premise.

## Optional regeneration

Certificate discovery requires `python-sat==1.9.dev15` with CaDiCaL 1.9.5.
Write to a fresh external path:

```sh
python3 -m venv /tmp/hn-snail-d3-gluing-env
/tmp/hn-snail-d3-gluing-env/bin/pip install -r \
  hadwiger_nelson_snail_d3_triangle_gluing_gate/requirements.txt
/tmp/hn-snail-d3-gluing-env/bin/python -B \
  hadwiger_nelson_snail_d3_triangle_gluing_gate/produce.py \
  --certificate /tmp/hn-snail-d3-gluing-certificate.json
cmp /tmp/hn-snail-d3-gluing-certificate.json \
  hadwiger_nelson_snail_d3_triangle_gluing_gate/certificate.json
```

The producer uses SAT only to discover positive words, decodes every model and
checks it against the complete edge graph before writing it.  A non-four
selector would stop as an unproved signal rather than be reported as a result.
See [PROOF.md](PROOF.md) for the precise family and certificate argument.

## Context

The parent `D9` theorem and its review already imply four-colourability of
each individual `D3` input, but not of unions with new cross edges.  The new
certificate handles those physical contacts explicitly.  The Snail's
geometric fractional chromatic number greater than four motivates its use as
a source; that asymptotic theorem is not used in this finite proof.

The comparison baseline remains Jaan Parts' 509-point, 2,442-edge strict plane
unit-distance graph, [arXiv:2010.12665](https://arxiv.org/abs/2010.12665).
Dúcz and Varga's Snail is from
[arXiv:2606.28157](https://arxiv.org/abs/2606.28157).  No literature-priority
claim is made for this finite gluing census.

Discovery Net accepted contribution
`bafkreiasrejo7vwwsoud46c5flqemxcvgd3gx5joipjejrpzpfy3tj6g2a` for broadcast
with its two initial relations.  The local committed ledger remained stale at
height 4,363 (RPC 4,364), so the contribution is pending, not committed, and
must not be resubmitted merely because it is absent from that index.
