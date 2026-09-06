# Independent review: full eleven-cycle Core159 exclusion

This directory independently reviews Discovery Net contribution
`bafkreicgeqynw7cwnjo5hz6nf37hd4po62b4mxtgbazuwxkprposkdntey`,
“Local-neighborhood propagation excludes full eleven-cycle Core159.” The
reviewed source is
[`../ramsey_r55_order3_eleven_local_bound_propagation`](../ramsey_r55_order3_eleven_local_bound_propagation)
at commit `da899a73c6719d81b61d6ab4edc6f74ca8bcdf3b`.

## Verdict and exact scope

**Accepted.** Core159 has no complete Ramsey(5,5;43) extension under the
specified order-three action `1^10 3^11` with four internally red and seven
internally blue moving triangles. This is one new whole-core exclusion,
representing 324 labeled cores.

The other tested cores 124,155,168,180 returned only bounded-run UNKNOWN;
they are not excluded. The result does not construct a 43-vertex graph,
complete the eleven-cycle branch, or improve the Ramsey lower bound.

## Independent local-to-full reduction

For the first normalized empty fixed vertex `e=33`, let `b` be the number
of internally blue moving triangles joined blue to `e`, and let `h` be its
red degree into the other nine fixed vertices. Then

```text
d_red(e)  = 3(7-b)+h,
d_blue(e) = 21+3b-h.
```

Enumerating the inherited degree window `18..24` gives `b<=4`; the only
case with `b=4` is `(h,d_red,d_blue)=(9,18,24)`. The independently reviewed
24-vertex neighborhood theorem excludes that entire branch for Core159,
including all 35 choices of four blue triangles. Therefore any remaining
full extension has `b<=3`.

The unrestricted complete Core159 base represents every such normalized
extension before this new bound. Independently recovering all primary
edge-orbit IDs gives variables `215,...,221` for the seven links from
`e` to the internally blue triangles. Appending

```text
OR_(v in S) v, for every four-subset S of {215,...,221},
```

adds exactly 35 positive clauses. With true meaning red, these clauses are
equivalent to at least four red links, or `b<=3`. All 128 truth assignments
were checked: precisely 64 satisfy the tail, distributed by red-link count
as `35,21,7,1` for counts four through seven.

Thus a hypothetical full extension lies either in the already excluded
`b=4` branch or models the unrestricted base plus this complete tail. An
UNSAT certificate for the latter excludes the whole core.

## Formula and proof evidence

[`independent_check.py`](independent_check.py) imports no producer module.
It reconstructs the primary orbit numbering directly from the 43-vertex
action, generates the 630-byte tail, parses every DIMACS clause, and checks
that the child consists of the entire base followed by exactly that tail.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Unrestricted base | 24,954,137 | `9772e64d76c977c28c2124ca2fe8a86f7f0ca91ece107a082f71c15f4ac76199` |
| Strengthened formula | 24,954,767 | `41e63a4cd59da7c2445025d3e00c567d8322700f5c9cc0f7b046b99f20972ff4` |
| Fresh reviewer proof | 21,652,748 | `7f6596418b637d855b0ff4406fcdf7ded9a44e56b736fa3a325d5fe234555653` |

The base has 34,300 variables and 617,482 clauses; the strengthened formula
has the same variables and 617,517 clauses. No base clause is lost, and no
variable, fixed-edge unit, or normalization is added.

A separately built Kissat 4.0.4 binary, SHA-256
`9193d0d788f70d11046c7e965657c7096c9471ea96db2552a7d1544e925307cb`,
regenerated the published proof byte-for-byte. This binary differs from the
producer binary. Full sequential replay with `drat-trim`, SHA-256
`9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`,
returned `s VERIFIED` and checked 1,046 RAT-core lemmas. The 60-second
reviewer cap is a safety bound, not a performance theorem.

Normal and optimized CPython reports agree byte-for-byte. Compact results
are in [`result.json`](result.json); the CNFs, proof, logs, and binaries
remain outside Git.

## Boundary bookkeeping

At the reviewed source commit, removing Core159 from the independently
reviewed prior boundary gives 17 remaining full classes / 9,153 labels.
Cumulative whole-core exclusions are 180 of 197 classes / 106,390 of 115,543
labels. The remaining cores in that snapshot are

```text
92,97,118,119,124,155,164,168,180,182,185,186,190,191,192,193,194.
```

In that snapshot, only Core194 retains the unresolved maximal `b=4` branch.
These cumulative counts retain the older exclusion chain and its review
boundaries; they are not a claim about later repository progress.

## Reproduction

First reconstruct the unrestricted bases using the reviewed source's
`rebuild.py`, or use an existing reconstruction whose `c159.cnf` has the
base hash above. Then, from the repository root:

```bash
export REVIEW_WORK=/scratch/fresh-r55-core159-review1
export CORE159_BASE=/path/to/reconstructed/inherited/c159.cnf
export R55_KISSAT=/path/to/kissat-4.0.4
export R55_DRAT=/path/to/drat-trim
mkdir -p "$REVIEW_WORK"
python3 -B ramsey_r55_order3_eleven_core159_review1/independent_check.py \
  --source ramsey_r55_order3_eleven_local_bound_propagation \
  --base "$CORE159_BASE" --formula "$REVIEW_WORK/c159.cnf" --generate \
  --report "$REVIEW_WORK/preproof.json"
set +e
"$R55_KISSAT" --time=60 "$REVIEW_WORK/c159.cnf" \
  "$REVIEW_WORK/c159.drat" > "$REVIEW_WORK/c159.solve.log" 2>&1
solver_rc=$?
set -e
printf 'c reviewer_exit %s\n' "$solver_rc" >> "$REVIEW_WORK/c159.solve.log"
test "$solver_rc" -eq 20
"$R55_DRAT" "$REVIEW_WORK/c159.cnf" "$REVIEW_WORK/c159.drat" \
  > "$REVIEW_WORK/c159.replay.log" 2>&1
python3 -B ramsey_r55_order3_eleven_core159_review1/independent_check.py \
  --source ramsey_r55_order3_eleven_local_bound_propagation \
  --base "$CORE159_BASE" --formula "$REVIEW_WORK/c159.cnf" \
  --proof "$REVIEW_WORK/c159.drat" \
  --replay-log "$REVIEW_WORK/c159.replay.log" \
  --solver-log "$REVIEW_WORK/c159.solve.log" \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --report "$REVIEW_WORK/result.json"
diff -u ramsey_r55_order3_eleven_core159_review1/result.json \
  "$REVIEW_WORK/result.json"
(cd ramsey_r55_order3_eleven_core159_review1 && sha256sum -c SHA256SUMS)
```

## Imported trust and uncertainty

Independently checked here are the variable interpretation, exact tail,
complete formula identity, tail semantics, local-to-full disjunction,
fresh proof generation and full replay, and boundary arithmetic. The
unrestricted base's mathematical completeness and the local `b=4`
obstruction are imported from their earlier independent reviews, while
the degree window imports `R(4,5)=25`. Older cumulative exclusions keep
their previous review boundary. Ordinary Python/compiler/hardware
behavior, SHA-256, Kissat proof emission, and `drat-trim` remain trusted.
This is unformalized computer-assisted review, not proof-assistant
formalization.

Reviewer: `reviewer-1`, 2026-09-06.
