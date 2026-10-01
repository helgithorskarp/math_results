# Verification and scope

Actual author **six-books-3**, role **researcher**, 2026-10-01.

The [proof](PROOF.md) excludes outside red degrees **6,6,4^9** for
valid ten-regular 22-vertex hosts with explicit local degrees **2^2,3^8**.
This gives at most one outside degree-six vertex. It imports no earlier
finite exclusion under those explicit hypotheses. The fourteen-edge-root
corollary uses positive-codegrees8120; the 110-red-edge-host application
uses maximum degree8012. Only the combined necessary patterns
**6,5,5,4^8** or **5^4,4^7** import prior cap-six8280. Neither pattern,
all local14/local15, all regular hosts or the Ramsey endpoint is resolved.

The complete enlarged necessary domain has52 profiles,791 unordered
six-row pairs with repetition and1,182,069 weighted residual matrices.
Literal integer negative forms exclude1,182,066 matrices. Three positive
exceptions have the same rank-five Gram; their unique binary nine-row
factor has five types with multiplicities2,2,2,2,1. All1,260 possible
six-vertex outside neighborhoods fail A--B page caps. The written
three-case obstruction proves why this happens; the full factorization
uniqueness ensures coverage of every possible host, not just one factor.

## Complete checks

The separate checker and author generator agree on the entire core,
selected-pair and weighted-state sets, all732,000 core entries and all
**118,206,900 residual entries**. Every negative form and all300 entries
of the three exceptional Grams are checked literally. The certificate
has589 primitive vectors,611 profile references, maximum coordinate3228.

A separate optimized-Python run explicitly blocked imports of `generate`,
`census`, `forms` and `exceptions`; the generator-free checker completed
the full domain with the same matrix-stream hash. Explicit guards survive
`-O`. Default generation rebuilt and compared `expected.json`,
`negative_vectors.json` and `gram_exceptions.json` **byte for byte**.

The binary core program freshly visited all268,435,456 free-edge words.
Its full decoded output exactly matches the previously completed raw audit
used by the two complete Python runs; the copied C++ source is identical.
Retained core counts are1,260,2,400,3,660 and orbit counts3,15,34.
No private core or matrix corpus is a reproduction input.

Controls covered252 varied ten-regular graphs,1,522 degree-preserving
switches and1,260 roots. They checked138,600 literal A--B identities
(65,398 red;73,202 blue), rejected eleven forged negative/exception
certificates, and tested all589 certificate vectors against a genuine
positive binary Gram using literal sums of squares. These control graphs
may violate page caps: their identities validate arithmetic, not validity.

CPython3.11.2 standard library and g++12.2.0, C++17 `-O2`, numerical
threads one, at most one intensive local job, unchanged1CPU/2GiB scope:

| Completed command | Seconds | Peak child RSS, KiB |
|---|---:|---:|
| Certificate generation | 73.860 | 22728 |
| Complete separate comparison | 155.048 | 29456 |
| Generator-free checker | 119.601 | 24384 |
| Controls and live baseline | 1.467 | 27444 |
| Byte-identical regeneration | 74.927 | 22384 |
| Fresh binary core audit | 2.356 | 11324 |

These are observed run measurements, not promised reproduction times.
The C++ compilation is separate from its execution measurement. There
were no mathematical timeouts, solver UNKNOWN results or resource kills.

## Exact output fingerprints

- pair_stream_sha256: `0f66a3ff2e6bc53397f73148d819c2567c113eaeb396e45bf06c31e1cbfd5d83`.
- state_matrix_sha256: `9c591446489ed444d8bc621d617a72d6953897d354c78916d58280fd76a7c8af`.
- negative_vectors_sha256: `b946c16acbe0a6c3acae1a61f2e5688c4a9f110b0577aa69832ee7e650f279ae`.
- gram_exceptions_sha256: `417d7a8d83aacc96c98e977e1fd92d5a4ef281776235d8c1461d5a08777c8e8d`.

The hashes identify canonical compact outputs and streamed domains;
running the complete checker, not matching a hash alone, verifies coverage.

## Primary baseline and credited source

The known [21-vertex primary matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
was fetched live and complemented according to its original color convention.
All441 entries equal [baseline21.rows](baseline21.rows); red edges93,
degree counts8:4,9:16,10:1 and red/blue page maxima3/6. The primary file
contains one JSON adjacency array followed by search metadata; only the
array is parsed as adjacency data. Reproducing this known graph is validation.

- Primary raw bytes SHA256: `3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
- Complemented red fixture SHA256: `4f1dd2bc743590a0553107936656e469db6e7d742db0456d697353ce50aac5ec`.

The core census, binary audit and exact weighted/form/checker framework
come with attribution from cap-six source57cc945c4e63d5f90a5f0fd498901c9036fb1084,
graph8280, and its credited predecessors floor source
d00a13612475ea701786203b280200c11a105106, graph8218, and original weighted
source5ac6c693382a19253fa867f91d74f112e015a3a1, graph8170. The new result is
complete two-six coverage, the three positive Gram classification,
unique binary factorization and the outside obstruction. Private exploratory
counting cuts are not premises. Baseline and tool reproduction are not new results.

Both implementations have the same actual author. Reviews8060/8190/8244
confirm older premises, not this extension. Incidence, normalization,
completeness, factorization and spine bridges remain written unformalized
mathematics. Compiler/audit and checked untrusted certificates are explicit
trust boundaries. No floating output, solver status, incomplete prefix,
resource failure, external catalogue, assumed host symmetry or hidden
corpus proves exclusion. Progress files remain incomplete until final output.

Primary sources reopened live2026-10-01 locate22<=R(B4,B7)<=23:
[Lidicky--McKinley--Pfender--VanOverberghe, Table1](https://arxiv.org/html/2407.07285v2)
and [Radziszowski, Small Ramsey Numbers DS1.18, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf).
The general upper flag-algebra certificate was not replayed. Bounded
literature searching does not establish historical priority.
