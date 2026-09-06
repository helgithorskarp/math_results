# Exact fixed-star obstruction at the saved Core186 coloring

The saved 43-vertex C3 coloring with 155 monochromatic five-sets is a
**strict minimum under every reassignment of one fixed vertex's eleven
moving-triangle contacts**. There are 20,470 distinct changed colorings
in this move family. Every one has at least 157 monochromatic five-sets.
The input remains the unique minimum of their union with the original.

This is an exact finite neighborhood certificate for one defective graph.
It produces no target graph, core exclusion, automorphism restriction,
global optimum or Ramsey-number bound. The 17 surviving prescribed
four-versus-seven core classes remain open. No priority claim is made for
the elementary conditional-counting method.

## Input and exact scope

[input.edges](input.edges) contains all 457 red edges; its first line is
43, remaining lines are sorted distinct pairs `u v`, and omitted pairs
are blue. Its physical five-set census is 74 red and 81 blue. SHA-256:

```text
f034595d4f9fcb40cbf70acb6da75f0f7efda21719b1cc4bd052b75e0e927441
```

The graph is copied from the
[structured-candidate package](../ramsey_r55_order3_eleven_structured_candidates),
source `c4e697c219deb07c08dd638baf609c323a9928ee`, Discovery Net finding
3301 (`bafkreifhedadadsnvyptofhpxyfaiw7hh76niqvyl7pe2pduc53qy3wxae`).
Its action is `(0 1 2)...(30 31 32)`, with fixed vertices 33..42.
Moving triangles 0..3 are internally red and 4..10 internally blue.
The eighteen cross-orbit bits among the first four triangles have word
`100110110011011101`, called Core186 in the earlier catalog.

For each fixed vertex f, independently from this same input, choose any
eleven-bit mask A. Bit i makes all three edges from f to triangle i red
or blue together. Every other edge stays fixed, including f's contacts
to the other nine fixed vertices. No degree, empty-signature or extra
automorphism condition is added. Each block has 2,048 assignments; the
ten blocks share exactly the input, giving 20,471 distinct labeled
colorings and 20,480 assignment scores. These are exhaustive counts for
this finite move family, not a search sample.

## Complete minima

Every block has minimum 155, achieved uniquely by its listed input mask.
No block has an improving or a changed neutral assignment.

| Fixed vertex f | Unique minimizing mask A | Minimum after a change |
| --- | ---: | ---: |
| 33 | 469 | 160 |
| 34 | 358 | 177 |
| 35 | 1340 | 157 |
| 36 | 668 | 173 |
| 37 | 1829 | 182 |
| 38 | 121 | 174 |
| 39 | 1732 | 170 |
| 40 | 1202 | 184 |
| 41 | 1872 | 187 |
| 42 | 936 | 168 |

The prior 302-single-orbit audit gave minimum changed score 156. That is
consistent: the present family covers all simultaneous fixed-to-moving
contact changes at one vertex, whereas that earlier family also contains
moving-to-moving and fixed-to-fixed orbit changes. Neither family contains
the other in full. Both freeze the eighteen prescribed core bits.

## Certificate and verification

[PROTOCOL.md](PROTOCOL.md) proves the exact conditional objective and
states the finite scope. A five-set with consistently colored fixed
edges contributes a monomial requiring all variable contact indices in
its support to have that color. Aggregate physical multiplicities into
blue and red coefficient maps. Empty supports include all unconditional
five-sets. The objective is

```text
sum(B[S] for S with S & A == 0) + sum(R[S] for S with S & A == S).
```

[produce.py](produce.py) enumerates literal symbolic five-sets and applies
subset zeta transforms. [certificate.json](certificate.json) retains all
3,562 nonzero coefficient records, complete minimizing sets, exact score
histograms and the full table identity. It is 58,719 bytes, SHA-256:

```text
aba47a537854226b3cbf4080cae0c2d465289b5996600f838e80b3748796c596
```

[verify.py](verify.py) imports no producer or old search code. For each f,
it recursively enumerates monochromatic K5s avoiding f and monochromatic
K4s in G-f. Correctly colored contacts to fixed vertices filter the K4s;
their moving-triangle indices give the coefficient supports. It checks
every coefficient, then evaluates all 20,480 separate blue/red counts by
direct subset predicates, without a transform. It verifies the original
and selected graph through both literal five-set scans and independent
clique recursion, the action on all 903 pairs, all internal/core colors,
and the precise changed edge set. The selected graph equals the input.

The full table is 192,079 bytes and is regenerated outside Git. Its
SHA-256 is
`f13979c48aaebbc93d9e890f6e7a3519671c2356003cf847db5b47effb28be46`.
It is a JSON array ordered by f=33..42, then A=0..2047, with entries
`[blue_count, red_count]`. No solver, binary, search dump or external
dataset is required for reproduction.

[controls.py](controls.py) checks 16,898 small physical assignment scores:
all 128 visible colorings of a five-vertex fixture times four assignments,
all 4,096 visible colorings of a six-vertex fixture times four assignments,
and two seven-vertex assignments testing an unconditional K5 through f.
These include improvements, worsenings, neutral moves and zero-defect
graphs. Eleven corruptions of coefficients, supports, block identity,
minima, argmins and score tables are rejected. Normal and optimized Python
agree byte-for-byte on the full coefficients, tables, graph and reports.

## Reproduction

CPython 3.11.2 and the standard library suffice. From the repository root:

```bash
bash ramsey_r55_order3_eleven_fixed_star/reproduce.sh /path/to/fresh-fixed-star-run
```

The script regenerates the omitted table, checks the full certificate and
controls, and compares all compact reports with the committed files.
The `generated` subdirectory must not already exist. To repeat in
optimized mode, use the following commands with a fresh external path:

```bash
python3 -B -O ramsey_r55_order3_eleven_fixed_star/produce.py --out /path/to/fresh-optimized
python3 -B -O ramsey_r55_order3_eleven_fixed_star/verify.py --work /path/to/fresh-optimized --report /path/to/optimized-verification.json
python3 -B -O ramsey_r55_order3_eleven_fixed_star/controls.py --report /path/to/optimized-controls.json
```

Compare the generated certificate, reports and graph with this package;
the regenerated table must have the displayed hash. `SHA256SUMS` records
all compact public artifact identities. All checks use explicit exceptions
and remain active under `-O`.

## Dependencies, limits and handoff

The previous graph is the only mathematical input. Catalog completeness,
the earlier heuristic optimizer, accepted symmetry exclusions and the old
single-orbit minimum are not premises of this new finite certificate.
The source and two algorithms are author work, not external peer review
or formalization. The unformalized reduction, physical indexing, Python
and parsing semantics, exact arithmetic, file identities and hardware
remain trust boundaries.

New shared evidence was inspected without importing or rerunning it.
The teammate's [three-block conditional gluing](../ramsey_r55_antipodal_block_gluing),
source `815b79be8f879d2bff7baa52b1132f9a0e115e64`, graph 3311, concerns a
distinct nonsymmetric H92 family and has no satisfiability verdict or
independent review of its new theorem. The earlier H92 arithmetic backend
is independently accepted at 3287. External graph 3299 identifies outside
common-neighbor triangles as the obstruction to a particular local
saturation transfer; graph 3295 restates independent cycle-phase
normalization with composition caveats. Neither is needed for the present
physical move census. The final content refresh reached 3314 and found
no further overlapping R55 result.

This milestone is complete; the original 155-defect graph is unchanged.
A concrete next direction is a coupled two-fixed-vertex move, initially
at vertices 33 and 35, whose individual change penalties are smallest.
Holding their mutual edge fixed gives 22 contact bits and 2^22 assignments;
five-sets through both vertices introduce the missing interaction terms.
That coupled test has not begun. No longer stochastic batch, new core
stratum or further optimization sweep is part of this contribution.
