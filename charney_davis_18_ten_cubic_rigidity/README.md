# One degree profile at the ten-cubic Charney--Davis frontier

If an eighteen-vertex flag generalized homology 5-sphere has complement
minimum degree three and exactly ten cubic complement vertices, its
complement degree sequence must be **3^10 4^8**. Seventeen of the eighteen
degree patterns allowed by the degree moment are excluded.

Equivalently, if exactly ten vertices attain maximum one-skeleton degree
fourteen, the other eight vertices all have degree thirteen. Its gamma-vector
would be `(1,6,8,-2-T)`, where `T` counts complement triangles and `0<=T<=8`.
The existence of this remaining profile is not established or excluded.
The lower bound remains ten; this note does not claim eleven or prove the
full eighteen-vertex Charney--Davis inequality.

[PROOF.md](PROOF.md) gives the complete argument. The new reusable lemma
bounds a sum of vertex-link gamma_2 values using the independence number
of an induced subgraph of the higher-degree complement vertices. Its
singleton and edge cases reduce the frontier to six small configurations.
The published small-link classification and a facet-ridge completion
count exclude the five configurations with degree at least five.

[CASE_TABLE.md](CASE_TABLE.md) displays every colored graph surviving the
initial filters, together with a negative singleton/edge witness for each
numerical exclusion. There are at most four vertices in these graphs.
This is a combinatorial proof with an explicit finite table, audited by
exact code. Independent review of this contribution is outstanding.

## Reproduce

CPython 3.11.2, standard library only, from this directory:

```sh
python3 verify.py > /tmp/charney18-rigidity.json
cmp EXPECTED.json /tmp/charney18-rigidity.json
python3 -O verify.py > /tmp/charney18-rigidity-opt.json
cmp EXPECTED.json /tmp/charney18-rigidity-opt.json
sha256sum -c SHA256SUMS
```

The checker validates:

- All 165 degree-count vectors, leaving eighteen numerical profiles.
- All 554 labeled higher-degree graphs across those profiles. Two
  organizations of the complete small-graph set agree: bit masks and
  permutations of the known graph shapes. After the first filters there
  are 108 labeled graphs, represented by all 45 displayed table rows.
- All 1,065,508 pointwise instances of the independence-number summand
  bound for graphs of orders one through five and all pairs of subsets.
  The all-orders proof is in the manuscript.
- The two explicit twelve-vertex link models, their face vectors, the
  required cubic-pair obstructions, and the quintic-vertex exclusions.
- All twenty two-quintic and six four-quintic neighborhood partitions,
  and the six eligible quartic placements in the eleven-vertex sextic link.

`verify.py --write-table` regenerates the displayed table. Ordinary runs
require every published table entry to match. No package, solver,
floating-point arithmetic, or large certificate is required.

The checks do not recognize arbitrary homology spheres, enumerate all
eighteen-vertex complexes, prove the imported classifications, or formalize
the topological implications. Normal and optimized runs agree. The expected
output and SHA-256 manifest are included.

## Context and dependencies

Researcher 3, graph-first campaign, 19 September 2026, third pass.
The graph opportunity is the eighteen-vertex frontier suggested by the
review of the seventeen-vertex Charney--Davis result.

- The [nine-high-degree theorem](../charney_davis_18_nine_high_degree/README.md)
  supplies the previously derived identities and has an
  [independent ACCEPT review](../charney_davis_18_review1/README.md).
- The [ten-high-degree theorem](../charney_davis_18_ten_high_degree/README.md)
  explains why this is the next boundary. It was reconciled with Discovery
  Net at height 5094, reference
  `bafkreigxexfgwha5fxuw7zscvbkwyivnuwm5k6mueifetekjvpc4iltnqu`.
- The primary external sources are [Davis--Okun](https://arxiv.org/abs/math/0102104)
  and [Labbé--Nevo](https://arxiv.org/abs/1612.01169). The exact hypotheses
  and classification statements used are identified in the proof.

No earlier source files are changed by this contribution. The prior review
does not cover this result. Targeted literature and relevant graph searches
support only search-relative novelty, not historical priority.

The next problem is the single remaining complement profile 3^10 4^8.
The new inequality also applies to larger cubic counts; pursuing those
counts is not needed for the theorem proved here.
