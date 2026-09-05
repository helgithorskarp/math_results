# Independent review of the order-three nine-cycle obstruction

Verdict: **accepted and independently verified**, subject to the dependencies
and software boundaries below.  The reviewed Discovery Net contribution is
`bafkreierr2zz3x2uhbh6nm5qntqjxjypziwucen2rt44g5g5kxvw6wwg54`, from source
commit `1c0c0dd1282c50d7fb6687e4b980040ee7fec916`.

The directly proved new theorem is that a 43-vertex graph with neither a
clique nor an independent set of order five cannot have an automorphism of
cycle type `1^16 3^9`.  Combining this with the previously reviewed
exclusions of one through eight moving cycles shows that every order-three
automorphism moves at least ten 3-cycles, hence at least 30 vertices and fixes
at most 13.  This is an intermediate symmetry restriction on a hypothetical
Ramsey graph.  It is not a 43-vertex graph and does not prove `R(5,5) >= 44`.
The cases with ten through fourteen moving cycles remain open in this chain.

## Mathematical audit

Color edges red and nonedges blue.  The established theorem `R(4,5)=25`
implies that every vertex has between 18 and 24 neighbors of either color.  A
color neighborhood of size 25 would contain either a same-color `K4`, which
extends with its center to a `K5`, or an opposite-color `K5`.

An order-three orbit of size three is a monochromatic triangle.  Fix one such
triangle `C_i`, write `c_i` for its color, `a_i` for its number of fixed
`c_i`-neighbors, and `w_ij` for the number of `c_i`-neighbors in another
moving triangle.  If `m_i` counts blocks with `w_ij=3`, its common
`c_i`-neighborhood and its degree give

```text
a_i + 3m_i <= 4,
2 + a_i + sum_(j != i) w_ij >= 18.
```

The common neighborhood contains no `c_i` edge, since that would extend
`C_i` to a monochromatic `K5`; five vertices in it would therefore form a
`K5` in the opposite color.  With eight other moving triangles, define

```text
delta(w) = 2 - w + 3 [w=3] = 2,1,0,2,
D_i = sum_(j != i) delta(w_ij).
```

Since `sum w_ij = 16 + 3m_i - D_i`, eliminating `a_i` gives the exact interval

```text
max(0, D_i - 3m_i) <= a_i <= 4 - 3m_i.
```

It is nonempty exactly when `D_i<=4` and `m_i<=1`.  Independent exhaustion of
all `4^8` weight vectors and all 17 fixed counts confirms 987 profiles: 635
with no complete block and 352 with one.  The 28 vectors that satisfy the
deficit bound but fail the common-neighborhood bound have exactly two weights
equal to three and six equal to two.

The normalization is exhaustive.  Global color reversal reduces the number
of red moving triangles to zero through four, and triangle permutations put
them first.  Independent phase changes of triangles 1 through 8 rotate each
anchor word to `000`, `100`, `110`, or `111`.  Permuting the sixteen fixed
vertices sorts their nine-bit incidence signatures lexicographically without
affecting the phase normalization.  Equal signatures remain allowed.

There are 381 pair orbits under the prescribed permutation: nine constant
internal triangles, 108 moving-cross variables, 120 fixed-fixed variables,
and 144 fixed-moving variables.  All `binom(43,5)=962598` five-sets are
projected after substituting the constants and identifying orbit literals.
The truth-table gates encode each unary deficit token and complete-block bit
exactly.  The prefix threshold counter is sound by induction, and any input
under its bound extends by assigning each cell the true prefix threshold;
this also covers signed and repeated inputs.  Thus its three repeated block
bits impose `a_i+3m_i<=4`, while its degree instance requires the 16 outside
own-color incidences needed for total degree at least 18.

## Submitted proof reproduction

I ran the complete submitted workflow serially with CPython 3.11.2, GCC
12.2.0, Kissat 4.0.4, and `drat-trim` from commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.  It regenerated every canonical
formula, reconstructed every primary and auxiliary clause in the separate C++
checker, produced a fresh binary DRAT trace, and replayed every trace.

| `r` | variables | clauses | solve seconds | replay seconds | RAT core lemmas |
|---:|---:|---:|---:|---:|---:|
| 0 | 8,490 | 609,409 | 3.426 | 4.488 | 30 |
| 1 | 8,514 | 612,097 | 8.091 | 7.070 | 163 |
| 2 | 8,532 | 614,113 | 7.089 | 7.083 | 118 |
| 3 | 8,544 | 615,457 | 9.848 | 9.732 | 245 |
| 4 | 8,550 | 616,129 | 9.346 | 8.608 | 176 |

The 3.1 million complete clauses all passed reconstruction.  Each replay
returned `s VERIFIED`; unlike the previous compact eight-cycle certificates,
these are general DRAT proofs and genuinely use RAT steps.  All fresh proof
hashes matched the reference hashes despite using an independently built
Kissat binary.  The complete workflow took 173.190 seconds.  An
AddressSanitizer/UndefinedBehaviorSanitizer build of the complete-clause
checker also passed the uniform `r=0` and mixed `r=4` cases.

## Reviewer-owned semantic checker

[`independent_check.py`](independent_check.py) imports no module from the
reviewed package.  It obtains every orbit by directly iterating the
permutation on all 903 unordered pairs.  For each of the five cases it then
projects every five-set and independently generates only the phase and
fixed-signature normalizations.  It compares a canonical cryptographic stream
of these semantic primary clauses with the primary-variable clauses parsed
from the full formula.

The exact comparison passed in count and SHA-256 for all five cases, after
checking each full formula and proof against its committed size and hash.  The
checker separately re-derived the 987 profiles, checked the normalization
schemas, and verified the positive fixture.  That fixture has 27 vertices,
177 red edges, the prescribed four-red/five-blue triangle split, no
monochromatic five-set among all 80,730 choices, deficit at most four, and at
most one complete own-color block at every triangle.  It shows that the moving
part alone is feasible; it is not a 43-vertex witness.

Run the audit from the repository root, retaining the roughly 207 MB of
generated formulas and proofs outside Git:

```sh
sh ramsey_r55_order3_nine_cycle_obstruction/verify.sh \
  --work /scratch/r55-order3-k9 \
  --kissat /path/to/kissat \
  --drat-trim /path/to/drat-trim

python3 ramsey_r55_order3_nine_cycle_review1/independent_check.py \
  --target ramsey_r55_order3_nine_cycle_obstruction \
  --work /scratch/r55-order3-k9 \
  --drat-trim /path/to/drat-trim \
  | diff -u ramsey_r55_order3_nine_cycle_review1/EXPECTED_OUTPUT.txt -
```

Exact run metadata is in
[`REPRODUCTION_RESULT.json`](REPRODUCTION_RESULT.json).

## Dependencies, trust boundaries, and uncertainty

The direct nine-cycle exclusion imports only McKay and Radziszowski's
established `R(4,5)=25` theorem.  I retrieved the cited primary paper and
confirmed that statement.  The minimum-ten corollary additionally imports the
one-through-eight exclusions.  The immediately preceding eight-cycle theorem
and its seven-cycle and sparse-motion dependency chain were independently
checked in [`../ramsey_r55_order3_eight_cycle_review1`](../ramsey_r55_order3_eight_cycle_review1).

The graph reduction, normalizations, counter-extension proof, and dependency
composition remain ordinary unformalized mathematics.  The finite part trusts
hardware, CPython exact-integer semantics, GCC, the compact Python/C++
programs, SHA-256 collision resistance for stream comparison, and
`drat-trim`.  The reviewer-owned checker independently reconstructs all
primary semantic clauses; the submitted C++ checker reconstructs every
auxiliary clause, whose schemas were separately audited mathematically.  The
solver is used only to produce traces, not as a trusted UNSAT oracle.  No graph
catalog, external Ramsey dataset, omitted trace, or solver verdict is needed.

Subject to these explicit boundaries, I found no incorrect degree inequality,
missing internal-color case, invalid symmetry quotient, incomplete five-set
projection, unsound auxiliary restriction, clause mismatch, or failed
certificate.  Acceptance of the scoped nine-cycle exclusion and its
minimum-ten corollary is warranted.
