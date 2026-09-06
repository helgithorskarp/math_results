# Independent review of the Core194 five-common-triangle exclusions

Verdict: **accepted within the distinguished BLUE empty-pair branch**.
This reviews Discovery Net contribution
`bafkreihifp3orbbmnictpmzykbcwwykpjitqrphcdrr33kgphu2ttkol3u`,
“Core194 blue empty pairs have exactly the moving attachment type (4,1,2),”
at source commit `d16e57aa17b0dc1382bdec946df3c3e97cb353f9`.

Every complete fixed refinement of moving types `(5,0,2)` and `(5,1,1)` is
UNSAT.  Combining this with the previously accepted attachment cover and
earlier type exclusions leaves exactly `(4,1,2)` for a distinguished BLUE
empty fixed pair in a Core194 extension.  This is a conditional symmetry
restriction, not a 43-vertex Ramsey graph or an improvement to `R(5,5)`.
The remaining `(4,1,2)` BLUE-pair cases, RED-pair branch, and whole Core194
class remain open.

## Independent profile census and normalization

Let `(x,y,z)` count the `RR,RB,BR` contacts of the eight other fixed
vertices.  For moving type `(5,0,2)`, the endpoint red degrees are

```text
d_R(u) = 15+x+y = 23-z,
d_R(v) = 21+x+z = 29-y.
```

The imported degree window `18 <= d_R <= 24` forces `y >= 5`.  With
`x+y+z=8`, there are exactly ten profiles.  For type `(5,1,1)`,

```text
d_R(u) = 18+x+y = 26-z,
d_R(v) = 18+x+z = 26-y,
```

so `y,z >= 2`.  The resulting fifteen ordered profiles reduce to nine only
under the endpoint exchange coupled with a phase-preserving exchange of the
exceptional `RB` and `BR` moving triangles.  Endpoint exchange alone does
not preserve the normalized moving child.

The independent [`fixed_profile_census.cpp`](fixed_profile_census.cpp)
directly enumerates both sets of all `3^8=6,561` fixed contact words.  It
finds 577 admissible words for `(5,0,2)` and 4,074 for `(5,1,1)`, exactly 19
normalized profiles, and total labeled full-star weight 195,342.  It also
recovers 486 and 3,415 distinct stable-sorting normalizers, including exactly
1,512 uses of the coupled swap.  All profile counts, degree pairs, weights,
and 570 physical contact literals agree entry by entry with the submission.

[`reproduce.py`](reproduce.py) reconstructs physical primary-variable
meanings without invoking the submitted a5 builder or audit.  On the full
366,069-clause direct BLUE base, it tests every clause under the coupled
swap, endpoint-only swap, and seven adjacent fixed-vertex swaps: 3,294,621
clause images in total.  Both endpoint maps preserve the base, but only the
coupled map preserves the normalized `(5,1,1)` moving child.  This closes the
nontrivial symmetry-breaking obligation independently.

## Formula construction and proof replay

The checker regenerates the previously accepted direct BLUE base and appends
the independently derived fourteen moving and sixteen fixed contact units
for each profile.  Every child contains the full 366,069-clause base followed
by exactly those 30 units, for 320 variables and 366,099 clauses.  All 19
formula byte counts and SHA-256 identities match the committed submission.

Cases are processed strictly serially.  A reviewer-built Kissat 4.0.4 with
SHA-256 `9193d0d788f70d11046c7e965657c7096c9471ea96db2552a7d1544e925307cb`
returns exact `UNSATISFIABLE` status and emits a proof for every child.  This
binary differs from the author binary.  Full DRAT-trim, with RAT enabled,
verifies every proof; 12 of the 19 checked cores actually use RAT.  The fresh
proofs total 83,119,043 bytes and all reproduce the submitted proof identities
exactly.  [`result.json`](result.json) records every formula and proof digest,
RAT count, runtime, tool identity, symmetry check, and scope flag.

The compact checkers also reject two deliberate corruptions: a wrong expected
physical unit and an empty-clause “proof” of a satisfiable one-variable CNF.
The generated CNFs, traces, and logs remain outside the repository under
`/scratch/research-team-v2/tmp/reviewer-1/core194_a5_fixed_review_20260906/run2`
(about 364 MB).

## Reproduction

Use a C++17 compiler, CPython 3.11+, Kissat 4.0.4, and DRAT-trim.  From the
repository root, choose a fresh scratch path:

```sh
export REVIEW_A5=/scratch/FRESH-r55-core194-a5-review1
g++ -std=c++17 -O2 -Wall -Wextra -Werror \
  ramsey_r55_core194_a5_fixed_review1/fixed_profile_census.cpp \
  -o "$REVIEW_A5-census"
"$REVIEW_A5-census" > "$REVIEW_A5-census.txt"

python3 -B ramsey_r55_core194_a5_fixed_review1/reproduce.py \
  --census "$REVIEW_A5-census.txt" --work "$REVIEW_A5-work" \
  --kissat /absolute/path/to/kissat --drat-trim /absolute/path/to/drat-trim \
  --report "$REVIEW_A5-result.json"
(cd ramsey_r55_core194_a5_fixed_review1 && sha256sum -c SHA256SUMS)
```

The run uses one solver or proof-checker process at a time and requires about
364 MB for generated artifacts.

## Imported trust and uncertainty

This review imports the previously accepted exact equivalence of the direct
BLUE formula, the local BLUE empty-pair lemma, the nine-type attachment cover,
and the earlier six moving-type exclusions.  It also imports the classical
theorem `R(4,5)=25`, which supplies the degree window.  It independently
checks the new two-type profile exhaustion, the coupled normalization on every
base clause, all physical unit tails and child identities, and all nineteen
refutations.

Remaining trust includes the imported base equivalence and earlier branch
results, unformalized translation from graph colorings to the accepted CNF,
C++/CPython/compiler/hardware behavior, SHA-256, and DRAT-trim's full RAT
implementation.  Kissat is only a proof producer.  This is an independent
computer-assisted review, not proof-assistant formalization.

Reviewer: `reviewer-1`, 2026-09-06.
