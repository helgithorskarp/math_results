# An anchored mixed 505-vertex family is four-colorable at every angle

Let `A` and `V` be the archived Parts 159- and 214-vertex gadgets. Fix

```
t = (5+i sqrt(11))/6
B = A union tA
q = V[0] = 1-sqrt(33)/6
H = V-q.
```

**For every rotation or reflection `g` fixing the origin, the strict
unit-distance graph on `B union g(H)` is four-colorable.** Its order is at
most 505. This excludes the specified inner assembly and anchor at every
angle; it does not exclude other anchors or produce a five-chromatic graph.

The [proof](PROOF.md) separates multipliers in the already four-colored
complex field `E=Q(i sqrt(3),i sqrt(11))` from those outside it. Every
outside-field multiplier with a new cross edge belongs to one of 24,423
irreducible quadratic classes. All 48,846 multipliers are covered by five
component colorings totaling 1,309 bytes, including three reused rows.
No new SAT solve was needed. Reflection adds no point sets because `H` is
invariant under complex conjugation, as checked exactly.

| Exact quantity | Value |
|---|---:|
| Vertices / strict edges of `B` | 292 / 1,251 |
| Vertices / strict edges of `H` | 214 / 977 |
| Nonzero vertex pairs classified | 61,983 |
| Outside-field quadratic classes | 24,423 |
| Outside-field multipliers with a new cross edge | 48,846 |
| Maximum new cross edges outside `E` | 14 |
| Uncovered classes | 0 |

## Reproduce

From this directory in a complete repository checkout, using Python 3.11
or later and only its standard library:

```bash
python3 verify.py > /tmp/mixed505-anchor0.json
cmp expected.json /tmp/mixed505-anchor0.json
python3 audit.py > /tmp/mixed505-anchor0-audit.json
cmp expected_audit.json /tmp/mixed505-anchor0-audit.json
python3 check_example.py > /tmp/mixed505-anchor0-example.json
cmp expected_example.json /tmp/mixed505-anchor0-example.json
sha256sum -c SHA256SUMS
```

On the producing host with CPython 3.11.2, these checks took 21.2, 11.1, and
6.6 seconds respectively; peak RSS was below 44 MiB for each.

`verify.py` rebuilds both components, classifies every nonzero pair, groups
equal monic quadratics, checks the coloring libraries, and constructs a
proper union coloring for every class. It reuses hash-pinned exact routines
from the prior fixed-Moser three-copy census.

`audit.py` uses the separate `E=Q(sqrt(33))+i sqrt(3) Q(sqrt(33))` arithmetic
from the earlier audit and groups by another polynomial normalization. It
checks every pair classification, full edge partition, reflection
permutation, and coloring witness. This is a second implementation check
by the same author, not an independent peer review of the present theorem.

`check_example.py` imports neither census nor field code. It reconstructs
all 127,260 point pairs for each of four labeled realizations of a class
attaining 14 new cross edges, using integer coordinates in
`Q(sqrt(2),sqrt(3),sqrt(11))` at scale 72. Each has 505 vertices and 2,242
strict unit edges; an actual proper coloring is checked.

The canonical edge-partition SHA-256 is
`a45f8d505c1c747626da48e46907a796f51cbf09932abc82c61f787199097ba6`.
Full counts, the histogram, a maximum-contact class, and further hashes are
in `expected.json`.

## Inputs, dependencies, and limits

The coordinate files are reused from
`../hadwiger_nelson_nonmono159_214_lowden2/points159.tsv` and `points214.tsv`;
their [provenance](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md) is
Parts' archived `v159e646` and `v214e977` data. The three 292-vertex colorings
are reused from `../hadwiger_nelson_nonmono159_moser_triple/colors_B.txt`.
The two new 214-vertex rows are in `colors_H.txt`. All input and imported
source files are pinned in `SHA256SUMS`.

The in-field case depends on the published
[four-coloring of the whole restricted complex field](../hadwiger_nelson_nonmono_field_obstruction/PROOF.md).
The algebraic continuous-to-finite reduction remains unformalized. The
finite evidence trusts ordinary exact Python arithmetic and the published
programs and inputs; it requires no approximate distance decision, solver
verdict, or omitted large certificate.

This mixed family differs from the prior 450-vertex three-copy family.
Neither family exclusion is asserted to contain the other. No claim is
made about arbitrary 505-vertex graphs or all mixed gadget constructions.
