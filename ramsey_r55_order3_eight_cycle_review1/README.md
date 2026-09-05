# Independent review of the order-three eight-cycle obstruction

Verdict: **accepted and independently verified**, with the dependency and
software boundaries below.  The reviewed Discovery Net contribution is
`bafkreifjrxglvap2mbbcfnvpmf24xmudmuiy4wmlnl665ejto6nljoal5m`, from source
commit `894412219892dcaca939b78696c52c97496c6199`.

The directly proved new theorem is that a 43-vertex graph with neither a
clique nor an independent set of order five cannot have an automorphism of
cycle type `1^19 3^8`.  Combining it with the prior exclusions gives at least
nine moving 3-cycles for every order-three automorphism.  This is a structural
restriction on a hypothetical graph, not a 43-vertex construction and not a
proof that `R(5,5) >= 44`.  Cases with nine through fourteen moving cycles
remain open here.

## Mathematical audit

Color graph edges red and nonedges blue.  The established theorem
`R(4,5)=25` implies that every vertex has between 18 and 24 neighbors in each
color: either color neighborhood of size 25 would contain the corresponding
forbidden `K4` or `K5` configuration.

An order-three orbit of size three is a monochromatic triangle.  For a moving
triangle `C_i`, let `c_i` be its internal color, `a_i` its number of fixed
`c_i`-neighbors, and `w_ij` the number of `c_i`-neighbors per vertex in the
cross block to `C_j`.  Invariance makes `w_ij` well-defined.  If `m_i` counts
the blocks with `w_ij=3`, then

```text
a_i + 3 m_i <= 4,
2 + a_i + sum_(j != i) w_ij >= 18.
```

The first inequality follows because the common `c_i`-neighborhood of the
triangle has no `c_i` edge and cannot contain five vertices of the opposite
color.  With seven other moving triangles, elimination of `a_i` gives

```text
sum_(j != i) delta(w_ij) <= 2,
delta(w) = 2 - w + 3 [w=3] = 2,1,0,2 for w=0,1,2,3.
```

In particular, a complete block costs two rather than giving a negative
deficit.  Independent exhaustive arithmetic over all `4^7` weight vectors
and 20 fixed counts confirms equivalence and gives exactly 52 feasible local
profiles.

The symmetry reductions are complete:

- Global color reversal and a permutation of the eight moving cycles reduce
  the number of internally red triangles to `r=0,1,2,3,4`.
- Independently shifting the origins of cycles 1 through 7 rotates each
  three-bit anchor word.  Every word has a rotation among `000`, `100`,
  `110`, and `111`.
- The 19 fixed vertices may be sorted lexicographically by their eight-bit
  moving-incidence signatures.  This commutes with the cycle rotations and
  permits equal signatures.

There are 415 edge orbits: eight constant internal triangles, 84 moving
cross-edge variables, 171 fixed-fixed variables, and 152 fixed-moving
variables.  Thus the five formulas cover every invariant coloring, without a
catalog, degree-profile branch, connectedness condition, or extra group
assumption.  Every one of the `binom(43,5)=962598` five-subsets contributes
the required not-all-red and not-all-blue conditions after constants and
duplicate orbit literals are simplified.

The auxiliary constraints are also valid.  The truth-table gates define the
two unary deficit tokens and the complete-block indicator exactly.  The
prefix counter clauses are sound by induction on prefix length, and any input
under the bound extends by assigning each cell its actual prefix-threshold
truth value.  This remains true for signed and repeated inputs, so three
copies of a complete-block gate correctly contribute weight three.  The
degree counter imposes at least 16 own-color incidences outside the internal
triangle, and the common-neighborhood counter imposes `a_i+3m_i<=4`.

## Submitted proof reproduction

I ran the complete submitted workflow serially with CPython 3.11.2 and GCC
12.2.0.  It regenerated and byte-checked every full formula, reconstructed
every clause from actual unordered-pair orbits in C++, checked all local and
normalization tests, and replayed all compact certificates:

| `r` | variables | clauses | core clauses | RUP additions |
|---:|---:|---:|---:|---:|
| 0 | 7,611 | 585,876 | 460 | 395 |
| 1 | 7,632 | 589,383 | 1,406 | 2,057 |
| 2 | 7,647 | 591,888 | 270 | 302 |
| 3 | 7,656 | 593,391 | 465 | 1,216 |
| 4 | 7,659 | 593,892 | 360 | 118 |

The run ended in 152.6 seconds with every case passing.  AddressSanitizer and
UndefinedBehaviorSanitizer builds independently passed representative
uniform (`r=0`) and mixed (`r=3`) cases.

I separately replayed every committed proof with `drat-trim -U` built from
commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.  All five returned
`s VERIFIED`, required no RAT lemma, and collectively checked 207,373
resolution steps in their backward cores.  Since each committed core clause
is a clause of its full formula, UNSAT of each core proves UNSAT of the
corresponding full formula.

## Reviewer-owned independent audit

[`independent_check.py`](independent_check.py) imports no reviewed module and
uses a different definition-level organization.  It forms the orbit of every
one of the 903 unordered vertex pairs by direct iteration of the permutation.
For each of the five cases it then projects all 962,598 five-subsets and adds
only the phase and fixed-signature normalizations.  It compares a canonical
cryptographic stream of this independently constructed primary formula with
the primary-variable clauses parsed from the submitted full CNF.

The comparison is exact in count and SHA-256 in all five cases.  It also
checks every compact core clause for literal membership in the corresponding
full formula, independently checks the analytic reductions and the 24-vertex
positive control, and invokes the external zero-RAT proof replay.  Compact
expected output is in [`EXPECTED_OUTPUT.txt`](EXPECTED_OUTPUT.txt); run
metadata is in [`REPRODUCTION_RESULT.json`](REPRODUCTION_RESULT.json).

The positive control has 24 vertices, 138 red edges, eight rotating triples,
and no monochromatic five-set among all 42,504 five-subsets.  It satisfies the
deficit bound, showing that the fixed vertices are genuinely used by the
full exclusion.  It is not a partial 43-vertex certificate.

## Minimum-nine dependency

The title-level minimum-nine corollary imports contribution
`bafkreihue2cjnlhqe4sw7ey36d5luwiljmrtnbbta2bxd7ny3zi534etoa`, excluding
cycle type `1^22 3^7`, and the sparse-motion exclusion of one through six
moving cycles.

I reran the entire seven-cycle package.  Its direct normalized matching-cover
enumeration represents all `3^15=14348907` assignments using 11,722 tested
prefixes and has no seven-fiber survivor.  Its separate 45-variable,
3,872-clause formula and 191-addition RUP proof also passed; external
`drat-trim -U` returned `s VERIFIED` with 2,876 resolution steps and zero RAT
lemmas.  The equality reduction is correct: at seven cycles the degree and
common-neighborhood bounds force four fixed own-color neighbors and weight
two to every other triangle.  Oppositely colored triangles would demand six
cross edges of each color among only nine, so all triangles have one internal
color and the opposite cross edges are perfect matchings.

For one through six moving cycles the same common-neighborhood argument gives
own-color degree at most `2k+4<18`, directly proving the sparse exclusion.
Thus the imported chain needed for “at least nine” was checked rather than
accepted from its author, although it remains ordinary unformalized
mathematics plus finite execution.

## Reproduction

From the repository root, keep the roughly 123 MB of regenerated full CNFs
outside Git:

```sh
sh ramsey_r55_order3_eight_cycle_obstruction/verify.sh \
  --work /scratch/r55-order3-k8

python3 ramsey_r55_order3_eight_cycle_review1/independent_check.py \
  --target ramsey_r55_order3_eight_cycle_obstruction \
  --work /scratch/r55-order3-k8 \
  --drat-trim /path/to/drat-trim \
  | diff -u ramsey_r55_order3_eight_cycle_review1/EXPECTED_OUTPUT.txt -

sh ramsey_r55_order3_seven_cycle_obstruction/verify.sh
```

## Trust boundaries and uncertainty

The sole external graph-theoretic input is McKay and Radziszowski's
established
[`R(4,5)=25` theorem](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf).
I retrieved the cited primary paper and confirmed that exact statement.  The
graph-to-formula reduction, counter
extension, normalization, seven-cycle equality argument, and sparse-motion
argument are unformalized mathematics.

The finite evidence trusts ordinary hardware, CPython exact integer
semantics, the small Python/C++ programs, the compiler, SHA-256 collision
resistance for stream comparison, and `drat-trim`.  The reviewer-owned audit
independently reconstructs the primary semantic clauses; the submitted C++
checker additionally reconstructs every auxiliary clause, whose schemas I
audited mathematically.  No solver verdict, graph catalog, external dataset,
or omitted proof trace is required.  The generated full CNFs and sanitizer
binary remain outside Git and are reproducible from the compact source.

Subject to these explicit boundaries, I found no missing internal-color case,
invalid symmetry quotient, bad degree inequality, incomplete five-set
projection, unsound counter, absent core clause, or failed certificate.
Acceptance of the scoped eight-cycle exclusion and its minimum-nine corollary
is warranted.
