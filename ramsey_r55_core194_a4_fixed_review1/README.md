# Independent review of the complete Core194 BLUE empty-pair closure

Verdict: **accepted**.  This reviews Discovery Net contribution
`bafkreibqknyvdvxopnhcev74n7kur4em4bxwo7r2y2k33qzljblamawgyi`,
“Core194 empty fixed vertices form a red clique of size two to four,” at
source commit `5737e2ee57db6a270602626ec48a9cace8a094c2`.

The new computational result excludes all 27 complete fixed refinements of
the last BLUE empty-pair moving type `(4,1,2)`.  Together with the previously
accepted six-type and a5 exclusions, no BLUE empty fixed pair remains.
Consequently, the empty fixed vertices induce a red clique.  The accepted
multiplicity result supplies at least two such vertices, while five would be
a forbidden red `K_5`; their necessary possible cardinalities are therefore
two, three, or four.

This remains an intermediate Core194 symmetry restriction.  It neither
constructs a 43-vertex Ramsey graph nor excludes Core194 or improves the
lower bound on `R(5,5)`.  In particular, it does not solve the RED-pair
extension branch, and no BLUE-pair contact restriction has been transferred
to that branch.

## Independent cover and normalization audit

For moving contacts `(RR,RB,BR)=(4,1,2)`, let `(x,y,z)` count the contacts of
the eight other fixed vertices.  The endpoint red degrees are

```text
d_R(u) = 15+x+y = 23-z,
d_R(v) = 18+x+z = 26-y.
```

The imported `R(4,5)=25` degree window `18 <= d_R <= 24` is equivalent to

```text
x+y+z=8,  y>=2,  z<=5.
```

There are exactly 27 triples.  The standalone
[`fixed_profile_census.cpp`](fixed_profile_census.cpp) directly enumerates
all `3^8=6,561` fixed-contact words and obtains 5,253 admissible words, 4,019
distinct stable-sorting permutations, and labeled star weight
`210*5,253=1,103,130`.  The factor 210 is 105 placements of the ordered
moving type and two endpoint orientations.  These are star assignments, not
graph realizations.

The C++ census was run under both `-O2` and AddressSanitizer/UBSan with g++
12.2.0; the full outputs agree byte for byte.  Independently, the Python
checker visits all 5,253 admissible words, transports each complete physical
30-contact star, and validates all 4,019 resulting vertex/C3/320-primary
bijections.  It checks 157,590 contact-literal images.  Every submitted
profile count, degree pair, weight, and unit tail agrees entry by entry.

The checker also reconstructs the complete direct BLUE formula and verifies
all 366,069 clauses under seven adjacent fixed-vertex swaps.  Those
2,562,483 clause images establish the sorting symmetry while preserving the
ordered moving child.  As a guard against an unsound extra quotient, all
366,069 clauses are also checked under endpoint exchange: the base is
preserved, but the ordered `(4,1,2)` moving child is not.  No endpoint swap
is used in the cover.

## Independent formula construction and certificate replay

[`reproduce.py`](reproduce.py) does not invoke the submitted a4 builder,
profile audit, runner, or verifier.  It regenerates the previously accepted
direct BLUE base and independently appends the fourteen moving and sixteen
fixed physical contact units for each profile.  Every child has 320 primary
variables and 366,099 clauses.  All 27 complete formula byte counts and
SHA-256 identities match the submission.

Cases are processed strictly serially.  A reviewer-built Kissat 4.0.4 binary
with SHA-256
`9193d0d788f70d11046c7e965657c7096c9471ea96db2552a7d1544e925307cb`,
different from the author binary, returns exact `UNSATISFIABLE` status and
emits a complete proof for each formula.  Full DRAT-trim with RAT enabled
verifies all 27 proofs; 21 checked cores use RAT.  The fresh proofs total
121,167,533 bytes and reproduce every submitted proof identity exactly.
[`result.json`](result.json) records each formula and proof digest, RAT count,
tool identity, runtime, normalization check, and theorem-scope flag.

The compact checkers reject a wrong expected physical unit and an
empty-clause “proof” of a satisfiable one-variable CNF.  Generated formulas,
proofs, and logs remain outside Git under
`/scratch/research-team-v2/tmp/reviewer-1/core194_a4_fixed_review_20260906/run`
(about 514 MB).  No process remains active.

## Reproduction

Use g++ 12+, CPython 3.11+, Kissat 4.0.4, and DRAT-trim.  From the repository
root, choose a fresh scratch path:

```sh
export REVIEW_A4=/scratch/FRESH-r55-core194-a4-review1
g++ -std=c++17 -O2 -Wall -Wextra -Werror \
  ramsey_r55_core194_a4_fixed_review1/fixed_profile_census.cpp \
  -o "$REVIEW_A4-census"
"$REVIEW_A4-census" > "$REVIEW_A4-census.txt"

python3 -B ramsey_r55_core194_a4_fixed_review1/reproduce.py \
  --census "$REVIEW_A4-census.txt" --work "$REVIEW_A4-work" \
  --kissat /absolute/path/to/kissat --drat-trim /absolute/path/to/drat-trim \
  --report "$REVIEW_A4-result.json"
(cd ramsey_r55_core194_a4_fixed_review1 && sha256sum -c SHA256SUMS)
```

The review run uses one solver or proof-checker process at a time.  On this
host, the 27 solves totaled about 33.9 seconds, full replays about 53.8
seconds, and the measured serial proof phase about 90.1 seconds.

## Imported trust and uncertainty

This review imports the independently accepted direct-base equivalence,
BLUE pair theorem, nine-type attachment cover, first five moving-type
exclusions, complete `(6,0,1)` exclusion, complete a5 exclusion, and
one-empty-branch multiplicity theorem.  It also imports the classical theorem
`R(4,5)=25`.  The last a5 gate was independently accepted immediately before
this review.  The present review independently checks the new a4 cover,
physical normalization, complete child identities, and all 27 refutations.

Remaining trust includes the imported graph-to-CNF results and lower-bound
premise, C++/CPython/compiler/hardware behavior, SHA-256, and DRAT-trim's
full-RAT implementation.  Kissat is only a proof producer.  This is an
independent computer-assisted review, not proof-assistant formalization.

Reviewer: `reviewer-1`, 2026-09-06.
