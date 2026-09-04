# Exact cross-edge and colouring census for two-overlap Parts placements

## Result

**Claim status:** exact computer-assisted finite-family exclusion.  This is
not a five-chromatic graph below 509 vertices and is not a record improvement.

Let `L` be the 374-point large gadget of the Parts 509 construction, and let
`S+` be its 135-point small gadget with a second origin point adjoined.  The
two gadgets have 510 labels before identifications.  The sibling exact affine
enumeration proves that 2,373,802 Euclidean placements, each with exactly 508
distinct points,

```text
L union (T(S+) + t)
```

have exactly two cross-gadget coincidences.  This artifact classifies all of
them by their additional cross-unit edges:

| property | exact placement count |
|---|---:|
| exactly two overlaps | 2,373,802 |
| at least one cross-unit label pair | 2,373,802 |
| at least one genuinely new cross edge | 2,194,728 |
| no genuinely new cross edge | 179,074 |
| exactly one genuinely new cross edge | 189,738 |
| exactly two genuinely new cross edges | 194,946 |
| exactly three genuinely new cross edges | 180,216 |
| exactly four genuinely new cross edges | 180,234 |
| exactly five genuinely new cross edges | 173,230 |
| exactly six genuinely new cross edges | 153,368 |
| exactly seven genuinely new cross edges | 137,192 |
| at least eight genuinely new cross edges | **985,804** |

The published single-cross-edge absorption lemma says that a placement with
exactly two overlaps and at most one genuinely new cross edge is
four-colourable.  The explicit witness-composition check proves that all
194,946 placements with exactly two, all 180,216 placements with exactly
three, all 180,234 placements with exactly four, all 173,230 placements with
exactly five, all 153,368 placements with exactly six, and all 137,192
placements with exactly seven genuinely new cross edges are also
four-colourable.  Consequently **1,387,998** placements are closed, and any
five-chromatic exactly-two-overlap placement in this fixed-gadget family must
belong to the remaining set of 985,804 placements having at least eight new
edges.

The exactly-two-new-edge class splits as follows, and every row is completely
closed by the explicit colour libraries:

| topology of the two new edges | placements | explicitly four-coloured |
|---|---:|---:|
| shared `L` endpoint | 21,432 | 21,432 |
| shared `S+` endpoint | 37,900 | 37,900 |
| four distinct endpoints | 135,614 | 135,614 |

Every simple three-edge bipartite endpoint topology occurs.  `Li_Sj` means
that the three cross edges use `i` distinct `L` endpoints and `j` distinct
`S+` endpoints.

| three-edge topology | placements | explicitly four-coloured |
|---|---:|---:|
| `L1_S3` | 7,402 | 7,402 |
| `L3_S1` | 15,236 | 15,236 |
| `L2_S2` | 154 | 154 |
| `L2_S3` | 31,788 | 31,788 |
| `L3_S2` | 37,302 | 37,302 |
| `L3_S3` | 88,334 | 88,334 |

For four edges, distinct endpoint counts give the following 11 exhaustive
profiles.  (`L2_S2` is combinatorially possible but does not occur in this
geometry.)

| four-edge endpoint profile | placements | explicitly four-coloured |
|---|---:|---:|
| `L1_S4` | 6,922 | 6,922 |
| `L4_S1` | 18,380 | 18,380 |
| `L2_S2` | 0 | 0 |
| `L2_S3` | 24 | 24 |
| `L2_S4` | 10,814 | 10,814 |
| `L3_S2` | 60 | 60 |
| `L3_S3` | 3,916 | 3,916 |
| `L3_S4` | 30,802 | 30,802 |
| `L4_S2` | 23,510 | 23,510 |
| `L4_S3` | 32,130 | 32,130 |
| `L4_S4` | 53,676 | 53,676 |

The rotation-preserving and reflection-reversing halves each contain exactly
1,186,901 two-overlap placements.  In each half, 89,537 have no new edge,
94,869 have exactly one, 97,473 have exactly two, 90,108 have exactly three,
90,117 have exactly four, 86,615 have exactly five, 76,684 have exactly six,
68,596 have exactly seven, and 492,902 have at least eight.  Every two-,
three-, and four-edge profile and every colouring subtotal also agrees term by
term between the halves.  These equalities are independently checked aggregate
symmetries.

This is a finite structural reduction, **not a new five-chromatic graph and
not an improvement of the 509-vertex record**.  It does not close the 985,804
placements with eight or more new cross edges, or placements with three or
more overlaps.

## Explicit two- through seven-edge colouring composition

The Parts criticality certificate supplies 509 explicit four-colourings of
one-vertex deletions of the full graph.  Restricting the 135 rows whose deleted
vertex lies outside `L` gives 135 proper colourings of all 374 vertices of
`L`.  The single-cross-edge flexibility certificate supplies 194 proper
colourings of `S+`.

For a placement with `k` new cross edges, where `k` is between two and seven,
write the two overlap pairs as `(p1,q1),(p2,q2)` and the new edges as
`(p3,q3),...,(p(k+2),q(k+2))`.  Each large-gadget witness gives a colour
pattern on its `p` labels, and each small-gadget witness gives one on its `q`
labels.  Repeated edge endpoints are retained in the pattern.  A compatible
pair must agree at both overlaps after a permutation of the small-gadget
colour names and disagree across every new edge.  It then combines to a proper
four-colouring of the strict union, since all other strict edges are internal
to one gadget.  Such a compatible explicit pair exists for every placement in
all six exact strata.

For five edges there are seven ordered endpoint labels.  Testing all
`4^7 = 16,384` raw colour strings against one another would be wasteful:
compatibility is invariant under independent relabelling of the colours on
the two gadgets.  Replacing each string by its restricted-growth equality
partition leaves

```text
S(7,1) + S(7,2) + S(7,3) + S(7,4) = 1 + 63 + 301 + 350 = 715
```

where `S(n,k)` is a Stirling number of the second kind.  There are exactly
124,925 compatible ordered pairs of these partitions for the two overlap
equalities and five edge inequalities.  With six edges, eight labels similarly
reduce from `4^8 = 65,536` raw strings to

```text
S(8,1) + S(8,2) + S(8,3) + S(8,4) = 1 + 127 + 966 + 1,701 = 2,795
```

partitions, of which 1,544,844 ordered pairs are compatible.  Seven edges use
nine labels and reduce `4^9 = 262,144` raw strings to

```text
S(9,1) + S(9,2) + S(9,3) + S(9,4) = 1 + 255 + 3,025 + 7,770 = 11,051
```

partitions, with exactly 19,185,603 compatible ordered pairs.

The two overlap equalities force a partial injective map between colour
classes.  For each remaining small-gadget colour class, the edge inequalities
delete forbidden target colours.  A compatible full colour permutation exists
exactly when these remaining allowed sets satisfy Hall's condition.  The C++
census uses this criterion and asserts all six canonical counts.  The Python
verifier independently enumerates all raw seven- and eight-label strings and
their relabellings.  For nine labels it regenerates every restricted-growth
partition, exhaustively checks coverage of all raw strings, and uses integer
bitsets to count compatible left partitions through explicit injective colour
maps rather than the C++ Hall test.

`check_compatibility.py` strengthens these count checks to **entrywise equality**.
It compiles a temporary harness around the actual production table builder,
compares all 344,064 raw-pattern ranks to the Python canonicalization, and
compares all 130,447,851 Boolean entries across the seven-, eight-, and
nine-label tables to explicit injective colour maps.  The binary tables use
explicit little-endian serialization and are streamed through a pipe without
being saved.  Their combined SHA-256 is
`01e2c54cecc82d2ff06e0677403c0ec507a211afd87637c5c7fdc5cf256825c4`.
This validates the full compatibility relation, including zero entries and
padding bits; the geometric placement enumeration remains a shared-code
trust boundary.

The deterministic `colour_libraries.txt` has SHA-256
`91f5f39f1533e5780edfa30130f36bee3f90428bd7d442e788e8311d029b4169`.
Its 135 + 194 rows are regenerated byte for byte from the two source
certificates and independently checked against all 1,860 + 564 internal
strict edges by `verify.py`.

## Cross-difference characterization

Fix one of the 2,840 orthogonal orientations `T` forced by a matching nonzero
segment of `L` and `S+`.  Form the labelled cross-difference multiset

```text
D_T = {p - Tq : p in L, q in S+}.
```

A translation `t` has exactly two overlaps precisely when `t` has
multiplicity two in `D_T`.  A cross label pair `(p,q)` is a unit pair in the
placement at `t` precisely when

```text
|(p - Tq) - t| = 1.
```

Thus cross-edge detection becomes an exact unit-neighbour query inside the
finite point set underlying `D_T`.

Some cross label pairs do not add an edge to the strict union graph.  If
`q` is one of the two overlapped `S+` labels, its image is already an `L`
point, and the cross pair duplicates an internal `L` edge exactly when those
two `L` labels are adjacent.  Dually, if `p` is overlapped, the cross pair can
duplicate an internal `S+` edge.  With exactly two overlaps these are the
only ways a cross label pair can fail to be a genuinely new strict edge.  The
census tests both conditions against the exactly reconstructed internal
graphs.

## Complete exact enumeration

All arithmetic is in
`K = Q(sqrt(3),sqrt(5),sqrt(11))`, represented in its eight-element radical
basis with signed integers.  The program independently reproduces the prior
checksums:

```text
distinct directed L vectors       11,650
distinct directed S+ vectors       1,666
orientations                       2,840
all placements with >=2 overlaps 2,992,078
determining overlap pairs        17,658,256
internal L / S+ edges          1,860 / 564
```

For speed, the program places cross differences in square buckets of side
`1/4`.  This index is certified rather than heuristic.  Each radical is
bounded between consecutive rationals with denominator `10^12`; the bounds
are checked by exact integer squaring.  For every coordinate encountered,
the exact value lies less than `1/1000` above its computed lower bound.  Only
68 bucket offsets can therefore contain a unit neighbour.  An exact interval
square test removes impossible candidates.  The default two-edge run makes
39,179,441 exact distance checks; `--through-three` makes 45,942,172, stopping
each search as soon as a fourth genuinely new edge proves that the placement
is outside the exact-three stratum.  `--through-four` makes 51,403,915 checks
and stops at a fifth new edge.  `--through-five` makes 55,803,809 checks and
stops at a sixth new edge.  `--through-six` makes 59,327,018 checks and stops
at a seventh new edge.  `--through-seven` makes 62,177,377 checks and stops at
an eighth new edge.  No floating-point operation is used.

The legacy through-two per-orientation transcript remains committed as
`expected_census.txt`, SHA-256
`4008074237712c7fe2064cb32c3a47db0f91cf293e1be11914bed232b95c497d`.
The extended transcript is 1,933,183 bytes and is omitted as verbose generated
output; its SHA-256 is
`6a1903a823aa4712ffc76107b038e2ab2f78a844651bcdc4c47264ed94513f2c`.
Its compact global tail is `expected_three_summary.txt`, SHA-256
`c82fc5b5b7da533686ddeb12273337e6a218e5a308be299218a4d7bccf14c559`.
The 3,150,344-byte four-edge transcript is likewise omitted; its SHA-256 is
`dfdff4b9fde77a9afb45de38b7c5564cd38906fda3f8e88cf393eaba38f015e5`.
Its compact global tail is `expected_four_summary.txt`, SHA-256
`e4c3f2d098ae43e69dfab345a6d9025e3061a5110d1d470e80ccb64160cd0814`.
The 3,262,129-byte five-edge transcript is omitted for the same reason; its
SHA-256 is
`bcfb26d2c2dcf7a03c956d6e57186d519c9cd200267cee43cbfe62168b35ddaa`.
Its compact global tail is `expected_five_summary.txt`, SHA-256
`bee53871486313d1245d17dd2e9fc282ef00dbc304ccfa4cd731cdcd49ad65de`.
The 3,376,242-byte six-edge transcript is also omitted; its SHA-256 is
`d1c092929a72c1fef1b939e937fdde1586c61a985374ffd327b09fa9ba0d5b91`.
Its compact global tail is `expected_six_summary.txt`, SHA-256
`1bc7014577f48ee5a3a32b7634dac86d049e7a6120538f5ced8218132225e937`.
The 3,495,558-byte seven-edge transcript is likewise omitted; its SHA-256 is
`f1c9791ed5aa4b33179534dce6715edf52352c5bada066339dea2fcb7528c971`.
Its compact global tail is `expected_seven_summary.txt`, SHA-256
`e2eafb9e9f3af60cb44248feffc4c37eb0a200427b170d06b09fc6bb9e7277c1`.

## Reproduction

From this directory:

```bash
g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -pedantic \
  census.cpp -o census
python3 make_colour_libraries.py regenerated_colour_libraries.txt
cmp colour_libraries.txt regenerated_colour_libraries.txt
./census \
  ../hadwiger_nelson_parts509_completion_census_degree9/points.tsv \
  colour_libraries.txt \
  > census_output.txt
diff -u expected_census.txt census_output.txt
./census \
  ../hadwiger_nelson_parts509_completion_census_degree9/points.tsv \
  colour_libraries.txt \
  --through-three \
  > /tmp/parts509_three_edge_census.txt
sha256sum /tmp/parts509_three_edge_census.txt
sed -n '/^affine_placements_with_at_least_two_overlaps=/,$p' \
  /tmp/parts509_three_edge_census.txt \
  > regenerated_three_summary.txt
diff -u expected_three_summary.txt regenerated_three_summary.txt
./census \
  ../hadwiger_nelson_parts509_completion_census_degree9/points.tsv \
  colour_libraries.txt \
  --through-seven \
  > /tmp/parts509_seven_edge_census.txt
sha256sum /tmp/parts509_seven_edge_census.txt
sed -n '/^affine_placements_with_at_least_two_overlaps=/,$p' \
  /tmp/parts509_seven_edge_census.txt \
  > regenerated_seven_summary.txt
diff -u expected_seven_summary.txt regenerated_seven_summary.txt
python3 verify.py /tmp/parts509_seven_edge_census.txt > verify_output.txt
diff -u expected_verify.txt verify_output.txt
python3 check_compatibility.py > /tmp/parts509_compatibility_check.txt
diff -u expected_compatibility.txt /tmp/parts509_compatibility_check.txt
```

The exact C++ census is single-threaded.  The three-, four-, five-, six-, and
seven-edge runs took 556.78, 715.39, 886.47, 988.37, and 819.60 seconds,
respectively, with GCC 12.2.0 on the shared research host.  (Wall time varies
with shared-host load.)  The Python verifier uses only the standard library.
The entrywise audit was checked with Python 3.11.2 and GCC 12.2.0, using the
same C++20 `-O3` table builder and a temporary executable.
A GCC 12.2.0 `-fsanitize=address,undefined` build ran through nine complete
seven-edge-mode orientations during a declared 120-second representative-test
interval with no sanitizer diagnostic; this was coverage testing, not a
complete second census.

## Trust boundary

- `census.cpp` exactly reconstructs the orientations, all cross differences,
  internal edges, interval filters, and final unit tests.  It validates every
  library colouring, constructs exact compatibility bitsets for the four-,
  five-, and six-label patterns and canonical partition bitsets for the
  seven-, eight-, and nine-label patterns, using the exact Hall criterion for
  the canonical tables, and checks each exactly-two- through
  exactly-seven-new-edge placement.
  Hash collisions cannot affect the result because full field elements are
  compared.
- `verify.py` pins every source, checks the complete transcript digest and
  all legacy per-orientation/global sums, and checks the compact three-
  through seven-edge summaries.  When given any regenerated extended
  transcript, it additionally pins its digest and checks all extended rows,
  topology/profile sums, absorption sums, and rotation/reflection symmetries.
  It verifies the radical bounds, signed 128-bit safety inequality, and
  canonical colour-partition reduction, including an independent explicit-map
  bitset count for nine labels, and reruns the solver-free sibling
  certificate supplying the pair-flexibility input used by the gluing lemma.
  It also reruns the solver-free 4,769,328-case single-cross-edge flexibility
  checker.
  It independently regenerates the two explicit colour libraries and checks
  every witness against every internal edge.
- Two independent reviews of the preceding exact-four source each reproduced
  its complete transcript and supplied clean-room geometry, library, and
  transcript checks: [`review4`](../hadwiger_nelson_parts509_two_overlap_four_edge_review4)
  and [`review1`](../hadwiger_nelson_parts509_two_overlap_four_review1).  Both
  explicitly retain the shared-enumerator trust boundary.  They support the
  inherited through-four path but do not cover the exact-five, exact-six, or
  exact-seven extensions.
- The compact three- through seven-edge summaries do not independently
  reimplement the full C++ census.  The three-edge transcript was reproduced
  in two deterministic GCC runs during publication validation; the four-
  through seven-edge transcripts were checked in full by the Python verifier.
  These checks share the same census algorithm and compiler.  The proof is a
  reproducible finite exact computation in ordinary C++ and Python, not a
  proof-assistant formalization.
- The entrywise table audit invokes the actual C++ table builder and compares
  it with explicit-map Python bitsets.  It does not regenerate placements or
  constitute independent peer review.
- The conclusion is confined to this fixed Parts `L`/`S+` placement family.

## Files

- `census.cpp` — complete exact orientation, translation, and cross-edge
  census.
- `expected_census.txt` — all 2,840 per-orientation counts and global
  checksums for the default through-two mode.
- `expected_three_summary.txt` — compact global checksums for the
  `--through-three` mode; the verbose transcript is intentionally omitted.
- `expected_four_summary.txt` — compact global checksums for the
  `--through-four` mode; the verbose transcript is intentionally omitted.
- `expected_five_summary.txt` — compact global checksums for the
  `--through-five` mode; the verbose transcript is intentionally omitted.
- `expected_six_summary.txt` — compact global checksums for the
  `--through-six` mode; the verbose transcript is intentionally omitted.
- `expected_seven_summary.txt` — compact global checksums for the
  `--through-seven` mode; the verbose transcript is intentionally omitted.
- `check_compatibility.py`, `expected_compatibility.txt` — complete streamed
  comparison of production colour tables with explicit colour injections.
- `make_colour_libraries.py` — standard-library deterministic extraction of
  the positive witnesses from their source certificates.
- `colour_libraries.txt` — the 135 explicit `L` colourings and 194 explicit
  `S+` colourings consumed by the C++ census.
- `verify.py` — solver-free source, transcript, arithmetic, and dependency
  verifier.
- `expected_verify.txt` — expected compact verifier output.
