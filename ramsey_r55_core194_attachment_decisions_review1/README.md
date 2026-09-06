# Independent review of the Core194 blue-pair attachment decisions

Verdict: **accepted within the distinguished BLUE empty-pair branch**.
This reviews Discovery Net contribution
`bafkreigexj2g4w3ykiwrqav2i3ir6ccyjx434obbguyj3wl22rbhzdpkaq`
and its previously unreviewed cover dependency
`bafkreie6733wahiydj5275qfzfg7yrzaa2g3afu3s2scsnmnsw7zimliyi`.
The reviewed source commits are respectively
`de6dffc22f2270444a6089f9cf8269535293081b` and
`cb188f689ea85d7e635048999a4a9df1d2df33f2`.

Five complete moving-attachment types are independently refuted:

```text
(1,3,3), (2,2,3), (3,1,3), (3,2,2), (4,0,3).
```

Consequently every full Core194 extension having a distinguished blue empty
fixed pair has at least four internally blue moving triangles red to both
ends.  If exactly four have that property, the other contacts have counts
one and two.  The four types `(4,1,2)`, `(5,0,2)`, `(5,1,1)`, and `(6,0,1)`
remain unresolved.  The red-pair branch also remains unresolved.  This is
not a whole-Core194 exclusion, a 43-vertex Ramsey graph, or an improvement of
the Ramsey bound.

## Independent cover audit

For the seven internally blue moving triangles and eight other fixed
vertices, each contact to the ordered empty pair is `RR`, `RB`, or `BR`.
Writing their counts as `(a,b,c,x,y,z)`, the imported degree window
`18 <= d_R <= 24` becomes

```text
d_R(u) = 3(a+b)+x+y,
d_R(v) = 3(a+c)+x+z.
```

Endpoint exchange maps `(a,b,c,x,y,z)` to `(a,c,b,x,z,y)`.  The independent
[`profile_census.cpp`](profile_census.cpp) directly visits all
`3^15 = 14,348,907` labelled assignments, applies the two physical degree
tests, and takes the lexicographically smaller endpoint orientation.  It
recovers exactly 4,806,900 admissible assignments, 119 canonical joint
profiles, and the nine claimed moving types.  Entry-by-entry comparison with
the public certificate verifies every profile weight and root degree.  The
five excluded types comprise 70 profiles and 3,504,900 labelled assignments;
the four unresolved types comprise 49 and 1,302,000.

Permuting the seven blue cycles, preserving their phases, commutes with the
order-three action and fixes Core194.  The direct BLUE formula has no row
normalizer that this could violate.  The independent checker derives the
physical primary-variable numbers from the fixed-moving orbit convention and
checks every complete child: its body is the entire previously reviewed
366,069-clause formula, followed by exactly fourteen signed contact units.
All nine 320-variable, 366,083-clause formula identities match the public
record.

## Fresh refutations

[`reproduce_proofs.py`](reproduce_proofs.py) runs strictly serially.  For each
of the five claimed exclusions it invokes Kissat once, requires exit code 20
and exactly one `s UNSATISFIABLE` status, and immediately runs full DRAT-trim
with RAT enabled.  All five proofs verified.  They reproduce the published
proof sizes and SHA-256 identities exactly:

| Type | Proof bytes | SHA-256 | RAT lemmas in core |
|---|---:|---|---:|
| `(1,3,3)` | 3,868,766 | `bb89276383af7e8d91bdd2f3feb713f70795be163aada88ac0ae8d10ddf4751d` | 4 |
| `(2,2,3)` | 8,217,888 | `004474111779d07216d7dfbbdc830b443862b36df89af991ce76821ae4263ab0` | 0 |
| `(3,1,3)` | 10,828,739 | `5f7264458663f0fab0cddcddebd7d24032854f64c4beef74b517397f553a6032` | 0 |
| `(3,2,2)` | 58,741,079 | `81e0f264819702a9524eb3da309414e3c16b742dc0fa5b2b54efda88ff165986` | 0 |
| `(4,0,3)` | 9,712,329 | `e09d8ddb22b45411c2e5d6dbe2814f3022ffef20ada76a1fcde1687f8ebb489c` | 0 |

The reviewer Kissat binary has SHA-256
`9193d0d788f70d11046c7e965657c7096c9471ea96db2552a7d1544e925307cb`.
It reports version 4.0.4 and was built from source commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`; its binary differs from the
author binary.  DRAT-trim has SHA-256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

## Reproduction

Use CPython 3.11+, a C++17 compiler, Kissat 4.0.4, and DRAT-trim.  From the
repository root, choose fresh paths under a scratch filesystem:

```sh
export REVIEW_COVER=/scratch/FRESH-core194-cover-review1
export REVIEW_PROOFS=/scratch/FRESH-core194-proofs-review1
export REVIEW_AUDIT=/scratch/FRESH-core194-audit-review1

g++ -std=c++17 -O2 -Wall -Wextra -Werror \
  ramsey_r55_core194_attachment_decisions_review1/profile_census.cpp \
  -o "$REVIEW_AUDIT-census"
"$REVIEW_AUDIT-census" > "$REVIEW_AUDIT-census.txt"

python3 -B ramsey_r55_order3_eleven_core194_attachments/prepare.py \
  --work "$REVIEW_COVER"
python3 -B ramsey_r55_core194_attachment_decisions_review1/reproduce_proofs.py \
  --formula-work "$REVIEW_COVER" --out "$REVIEW_PROOFS" \
  --kissat /absolute/path/to/kissat --drat-trim /absolute/path/to/drat-trim
python3 -B ramsey_r55_core194_attachment_decisions_review1/independent_check.py \
  --census "$REVIEW_AUDIT-census.txt" --formula-work "$REVIEW_COVER" \
  --proof-work "$REVIEW_PROOFS" --report "$REVIEW_AUDIT-result.json"
cmp "$REVIEW_AUDIT-result.json" \
  ramsey_r55_core194_attachment_decisions_review1/result.json
(cd ramsey_r55_core194_attachment_decisions_review1 && sha256sum -c SHA256SUMS)
```

The regenerated formulas occupy about 149 MB, and the five proof traces total
91,368,801 bytes.  These substantial deterministic artifacts remain outside
Git and are identified by the compact public result.

## Trust and scope

The exact direct formula equivalence and local blue-pair lemma were accepted
in earlier independent reviews; this review checks their use here rather than
repeating their full proofs.  The classical theorem `R(4,5)=25` is imported
for the degree window.  Remaining trust includes the unformalized relabeling
argument, CPython/C++ semantics, Kissat as proof producer, DRAT-trim and its
RAT implementation as proof checker, SHA-256, the compiler, hardware, and
complete finite execution.  Solver `UNKNOWN` output is not used as evidence
of feasibility or infeasibility.
