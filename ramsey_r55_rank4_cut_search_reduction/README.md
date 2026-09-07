# A 56.0637% reduction of the complete rank-four cut branch

For a fixed 20+23 partition of 43 vertices, consider **every** binary rank-four
cross matrix and **all 443 internal edges**. A complete structural exclusion
removes 56.0636965570% of those cross matrices: the ones having both a zero
row and a zero column. Each such matrix has complement rank five, so this
removes cases passing the prior rank-at-least-four test in both colors.

This also completely excludes the initially selected class in which all
16 row types and all 16 column types occur. No symmetry of the full graph,
fixed internal graph, saved parent, graph catalog or solver is assumed.
The [proof and exact counts](PROOF.md) give the full quantifiers and global
degree argument. The remaining rank-four branch and the good43 target stay
open. No new 43-vertex Ramsey graph or improved bound is claimed.

From this directory, with Python 3.11 and its standard library:

```sh
python3 -B reproduce.py
python3 -B family.py fixture_parameters.json
python3 -B extract.py fixture_graph.json > /tmp/r55-zero-pair-five.json
python3 -B verify.py fixture_graph.json /tmp/r55-zero-pair-five.json
```

The first command verifies the manifest and reproduces every exact audit
output in ordinary and assertion-disabled Python. Expected status:
`REPRODUCED_RANK4_CUT_SEARCH_REDUCTION`. `expected.json` records counts,
controls and the core-witness hash. `VALIDATION.json` records the observed
run cost and interpreter version. There is no missing large proof artifact.

`family.py` accepts two integer label lists of lengths 20 and 23, each
spanning F2^4, and `internal_hex` containing exactly 443 bits in 111 lowercase
hex digits. Integers 0..15 represent four-bit labels. Internal bits enumerate
the within-part unordered pairs in lexicographic physical pair order, first
pair least significant. All cross bits are dot products. The factor map
covers every rank-four matrix, with exactly 20160 parameter representations
per fixed physical cross matrix. It returns a physical graph plus
`EXCLUDED_ZERO_TYPES` or `SURVIVES_ZERO_TYPE_FILTER`. The latter asserts no
Ramsey feasibility. Internal bits remain completely unrestricted.

`extract.py` accepts `n:43`, `red_hex`, a sorted nontrivial `cut`, and `color`
0 or 1 (blue or red). The graph uses 903 bits, lexicographic unordered-pair
order, first pair least significant, in exactly 226 lowercase hex digits.
It recognizes the larger zero-row-and-zero-column family at **any rank and
cut size**, and returns a physical monochromatic five. Outside the family
it returns `OUTSIDE_ZERO_PAIR_FAMILY`, with no feasibility verdict.
`verify.py` independently decodes a dense adjacency matrix, checks the
zero-pair gate, input binding, extraction route and all ten physical pairs.
It imports neither the generator nor Ramsey bounds. The fixture is
intentionally non-Ramsey; it is not a candidate.

The audit checks all 74954 binary matrices of sizes 1..4 by 1..4 against
exact rank and zero-pair counts, all 1470 rank-two factor fibers for a 3x4
matrix, 96 physical certificates including both extraction routes, color
complementation, cut-side reversal and vertex relabeling, and 10836 physical
generator pairs. Malformed inputs and six corrupted certificates are
rejected. The included feasible 32-vertex dot-product core is checked on
all 201376 five-sets and by a separate clique search. It demonstrates why a
local core alone did not decide the 43-vertex class.

The only external mathematical premise is the published R(4,5)<=25 upper
bound; the proof derives R(4,4)<=18 elementarily. No priority claim is made
for the elementary common-neighbor obstruction. The contribution is its
complete global-family application, exact physical reduction, and reusable
candidate filter. Independent external review of this package is pending.
