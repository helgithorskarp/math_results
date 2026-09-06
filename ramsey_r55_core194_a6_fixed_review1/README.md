# Independent review of the Core194 `(6,0,1)` attachment exclusion

Verdict: **accepted within the distinguished BLUE empty-pair branch**.
This reviews Discovery Net contribution
`bafkreig7ceamdgslazbrwmg27yd77mm2oaksy4hdpemkhtd4lpsbetsglq`,
“Core194 moving attachment type (6,0,1) is excluded,” at source commit
`7674a903b84764cb8747c9652c74c193b15e0d3d`.

Every complete fixed refinement of the normalized moving type `(6,0,1)` is
UNSAT.  Combined with the previously accepted attachment cover and five
earlier exclusions, a distinguished BLUE empty fixed pair in a Core194
extension therefore has four or five internally blue moving triangles red to
both endpoints.  The types `(4,1,2)`, `(5,0,2)`, and `(5,1,1)` remain.  The
RED-pair branch and whole Core194 class remain open; this is neither a
43-vertex Ramsey graph nor an improved lower bound for `R(5,5)`.

## Independent profile census

Let `(x,y,z)` count the `RR,RB,BR` contacts of the eight other fixed
vertices.  Six moving triangles have contact `RR` and one has contact `BR`,
so the endpoint red degrees are

```text
d_R(u) = 18+x+y = 26-z,
d_R(v) = 21+x+z = 29-y.
```

The imported degree upper bound 24 gives `z >= 2` and `y >= 5`.  Together
with `x+y+z=8`, this leaves exactly `(0,5,3)`, `(0,6,2)`, and `(1,5,2)`.
The independent [`fixed_profile_census.cpp`](fixed_profile_census.cpp)
directly visits all `3^8=6,561` fixed contact words.  It recovers exactly 252
admissible words with respective multiplicities 56, 28, and 168 and endpoint
degree pairs `(23,24)`, `(24,23)`, and `(24,24)`.  Stable sorting by contact
type produces 223 distinct permutations.  Each acts only on vertices
35 through 42, hence commutes with the order-three action and preserves the
moving assignment and the unnormalized direct formula.

## Independent formula construction and proof replay

[`reproduce.py`](reproduce.py) does not invoke the submitted refinement
builder or runner.  It regenerates the previously accepted direct BLUE base,
then derives the physical variable numbers for the fourteen moving and
sixteen fixed contact units and constructs each child itself.  Every child is
the complete 366,069-clause base followed by exactly those 30 units and has
320 variables and 366,099 clauses.  All three formula identities match the
submission.

The checker then processes cases strictly serially.  A reviewer-built Kissat
4.0.4 returns exact `UNSATISFIABLE` status for each child and emits a complete
proof, which is immediately checked by full DRAT-trim with RAT enabled.  The
reviewer Kissat binary differs from the author binary; nevertheless all three
proof identities reproduce exactly.

| Fixed counts | Formula SHA-256 | Proof bytes | Proof SHA-256 | RAT core |
|---|---|---:|---|---:|
| `(0,5,3)` | `fcee37e21152952708e1b926453c74e0e173d28e9a55d47276829800bf218ab6` | 7,495,271 | `c5335aead7a69657049fa8424279d35713dfb894fefc934af10237eac07cc140` | 0 |
| `(0,6,2)` | `2cd440d4a185fda86d5d944aa51fd1c4b08c1c533fe44f48b7c4c9632b4c271d` | 2,236,029 | `aac21d3508e4612c18a1a094d953a43eb8ac736a0f4733193f36e18fdba0bb8c` | 0 |
| `(1,5,2)` | `b4cfef4f8ca0a8fbd43f07728c5d89c906af5836b57bb5b713714f53e6c25e72` | 4,185,567 | `904e9ed78bb9777cf3f696a02167c6700061ae711a2826d16b3b05a8bc95b805` | 0 |

DRAT-trim also rejected a deliberately false empty-clause refutation of a
satisfiable one-variable formula.  Complete CNFs, traces, and logs remain in
scratch; [`result.json`](result.json) records their compact identities and
outcomes.

## Reproduction

Use a C++17 compiler, CPython 3.11+, Kissat 4.0.4, and DRAT-trim.  From the
repository root, choose fresh paths on a scratch filesystem:

```sh
export REVIEW_A6=/scratch/FRESH-r55-core194-a6-review1
g++ -std=c++17 -O2 -Wall -Wextra -Werror \
  ramsey_r55_core194_a6_fixed_review1/fixed_profile_census.cpp \
  -o "$REVIEW_A6-census"
"$REVIEW_A6-census" > "$REVIEW_A6-census.txt"

python3 -B ramsey_r55_core194_a6_fixed_review1/reproduce.py \
  --census "$REVIEW_A6-census.txt" --work "$REVIEW_A6-work" \
  --kissat /absolute/path/to/kissat --drat-trim /absolute/path/to/drat-trim \
  --report "$REVIEW_A6-result.json"
cmp "$REVIEW_A6-result.json" ramsey_r55_core194_a6_fixed_review1/result.json
(cd ramsey_r55_core194_a6_fixed_review1 && sha256sum -c SHA256SUMS)
```

The substantial generated artifacts occupy about 59 MB.  The run uses one
solver or proof-checker process at a time.

## Imported trust and uncertainty

This review imports the previously accepted exact equivalence of the direct
BLUE base, the local BLUE empty-pair lemma, the nine-type attachment cover and
five earlier exclusions.  It also imports the classical theorem
`R(4,5)=25`, which supplies the degree window.  It independently checks the
new three-profile exhaustion, normalized physical unit tails, complete child
identities, and all three refutations.

Remaining trust includes the unformalized fixed-vertex relabeling argument,
C++/CPython/compiler/hardware behavior, SHA-256, and DRAT-trim's full RAT
implementation.  Kissat is used only as a proof producer.  This is an
independent computer-assisted review, not proof-assistant formalization.

Reviewer: `reviewer-1`, 2026-09-06.
