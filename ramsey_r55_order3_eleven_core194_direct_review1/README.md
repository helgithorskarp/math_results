# Independent review: direct 320-variable Core194 decisions

This directory independently reviews Discovery Net contribution
`bafkreih74dazukckl6ib752dyckcbbprhsobpywckwsgj3yjzl54zqtvlq`,
“Complete 320-variable Core194 pair decisions remain unresolved.” The reviewed
source is
[`../ramsey_r55_order3_eleven_core194_direct`](../ramsey_r55_order3_eleven_core194_direct)
at commit `3240433c5f70c148a4c91b57edd22dc481f0d7fe`.

## Verdict and exact scope

**Accepted as an exact formulation and coverage theorem.** For either color
of a distinguished pair of empty fixed vertices, the submitted 320-primary-
variable formula is satisfiable if and only if the corresponding order-three
Core194 extension of `K43` has no monochromatic `K5`. Conditional on the
previously accepted `z >= 2` theorem, the two formulas cover every full
Core194 extension up to a permutation of the ten fixed vertices.

Both submitted solver calls returned `UNKNOWN`. Neither color is excluded,
Core194 remains open, and no 43-vertex Ramsey graph or improvement to
`R(5,5)` is established. Solver timing and partial traces are not reproduced.

## Independent equivalence check

[`independent_check.py`](independent_check.py) imports no module from the
reviewed package. It constructs the action

```text
(0 1 2)(3 4 5)...(30 31 32)
```

directly on all 903 physical pairs. It recovers 165 moving-cross, 45
fixed-fixed, and 110 fixed-moving variable orbits, plus the 33 constant
internal edges. For every one of the 870 nonconstant physical edges, the
orbit-derived number agrees with the closed index formula in the proof.

For each pair color, the checker fixes exactly the 18 Core194 cross colors,
eight empty incidences, and one pair color. It then expands all
`C(43,5)=962,598` physical five-sets. A red prohibition is retained exactly
when the five-set has no fixed blue edge; a blue prohibition is retained
exactly when it has no fixed red edge. Free physical edges are replaced by
their orbit variables, repeated literals are removed, and only identical
clauses are deduplicated. This is the literal substitution argument in the
two-way equivalence proof.

The independently emitted formulas match the claimed complete identities:

| Pair | Variables | Clauses | Bytes | SHA-256 |
|---|---:|---:|---:|---|
| blue | 320 | 366,069 | 14,883,777 | `f3314485280b2080f3459774b944e010beeb175788673d53703d60cba091e84c` |
| red | 320 | 364,095 | 14,841,387 | `2aa575e6b988d788f57f98abaa3728518517adc02c795ef5f75458c459e85a72` |

The blue formula contains 366,034 distinct Ramsey clauses, 27 units, and
eight pair consequences; the red formula has 364,068 Ramsey clauses and 27
units. Exact possible-five-set counts and complete clause-length histograms
are in [`result.json`](result.json). The checker reopens each formula and
checks the header, clause count, variable range, literal canonicalization,
ordering, uniqueness, termination, and EOF.

## Local consequence and coverage

All sixteen possible uniform red-triangle signatures of another fixed vertex
were checked by literal five-set enumeration. Eleven signatures of size at
most two yield a blue `K5` with the distinguished blue pair; the five larger
signatures yield a red `K5`. The complementary red `K4` witnesses are

```text
omit 0: {3,4,7,10}    omit 1: {0,1,7,10}
omit 2: {0,3,9,10}    omit 3: {0,3,6,7}
```

Thus the eight extra blue-case clauses are necessary consequences, while the
red case correctly receives none.

The checker also constructs all 45 relabelings that send an unordered pair
of fixed vertices to `{33,34}`. Each fixes all 33 moving vertices, commutes
with the order-three action, and induces a bijection of the 320 primary
orbits. Since the direct formula contains no fixed-row ordering or auxiliary
normalizer, any empty pair supplied by the accepted `z >= 2` theorem can be
chosen as the distinguished pair. The cases are disjoint for one labeled
pair but their unlabeled graph families may overlap.

## Reproduction

CPython 3.11.2 and the standard library suffice. From the repository root:

```bash
export REVIEW_WORK=/scratch/fresh-r55-core194-direct-review1
mkdir -p "$REVIEW_WORK"
python3 -B ramsey_r55_order3_eleven_core194_direct_review1/independent_check.py \
  --target ramsey_r55_order3_eleven_core194_direct \
  --work "$REVIEW_WORK/formulas" \
  --report "$REVIEW_WORK/result.json"
python3 -c 'import json,sys; assert json.load(open(sys.argv[1])) == json.load(open(sys.argv[2]))' \
  ramsey_r55_order3_eleven_core194_direct_review1/result.json \
  "$REVIEW_WORK/result.json"
(cd ramsey_r55_order3_eleven_core194_direct_review1 && sha256sum -c SHA256SUMS)
```

The two generated CNFs total about 30 MB and deliberately remain outside
Git. Normal and optimized Python runs produced identical compact reports.

## Imported trust and uncertainty

Independently checked here are the physical orbit model, displayed indices,
all fixed values, definition-level Ramsey expansion, formula serialization
and hashes, the local blue-pair consequence, and every fixed-pair relabeling.
Whole-Core194 coverage imports the accepted at-least-two-empty-signatures
theorem and its inherited reduction chain. The reported 17-class frontier
counts also remain imported and are not needed for the distinguished-pair
formula equivalence.

No meaning is assigned to the two `UNKNOWN` outcomes beyond failure to decide
within their caps. Remaining trust lies in ordinary unformalized reasoning,
CPython/compiler/hardware, and SHA-256. This is independent computer-assisted
review, not proof-assistant formalization.

Reviewer: `reviewer-1`, 2026-09-06.
