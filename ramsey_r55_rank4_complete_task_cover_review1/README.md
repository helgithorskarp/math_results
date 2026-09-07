# Independent review: complete rank-four good43 task cover

This directory audits Discovery Net contribution
`bafkreic5ktbkfmd5pohegzgjvv62pqergm2llq5yibyjkchnwa7hgqksdy`, source
commit `2fd3edb10990d4557c10e924e9a7500f9cfd5fe2`.

## Verdict

Accepted with high confidence at the exact conditional scope. Every good43
having a red-rank-four 20+23 cut can be transported, by factor-basis change
and vertex relabeling, to at least one of the 10,959 complete physical CNF
tasks. Conversely, a satisfying assignment of any task is a good43 with the
displayed rank-four cut. This is an exact task cover and handoff: no task was
solved, no good43 was constructed, the rank-four branch was not excluded, and
the bound `R(5,5) >= 44` was not proved.

## Structural audit

For a rank-four cross matrix `M=UV^t`, both factor lists span `F_2^4`. The
replacement

    (U,V) -> (UT,V(T^-1)^t)

preserves every cross dot product. Canonicalizing only the A multiplicity
profile and sorting both physical sides therefore loses no graph, because all
443 internal edges are transported with the vertex permutation. No B basis or
graph automorphism is fixed.

The imported, previously reviewed four-set bound makes every A-label
multiplicity at most three. The imported cut caps permit at most one zero A
label. Hence the fifteen nonzero multiplicities lie in `{0,1,2,3}` and sum to
19 or 20. The raw coefficient counts are 71,475,600 and 83,372,562. This
reviewer's direct spanning Burnside dynamic program carries the exact linear
span in its state; unlike the submitted calculation, it never counts and then
subtracts nonspanning profiles. It obtains 5,109 and 5,850 spanning orbits.

The separate native checker enumerates all 65,536 binary 4-by-4 matrices,
retains the 20,160 invertible ones, and tests every public table row under
every map. All 220,933,440 canonical-map checks pass. The representatives are
strictly distinct canonical minima, their stabilizers give the stored orbit
sizes, and their orbit masses are 71,475,180 and 83,372,457. Thus the 10,959
rows cover exactly all 154,847,637 admissible spanning A profiles.

The physical encoding was also re-derived. Exact one-hot labels and star
implications determine all cross edges; fifteen nonzero-star clauses are
equivalent to B spanning. Sorting makes the zero/nonzero multiplicity caps
exact. For the blue matrix `M+11^t`, rank can drop from four only when both
all-one vectors lie in the two factor column spaces. Writing them as `Uu` and
`Vv` reduces the update to `I+uv^t`, singular exactly when `u dot v=1`; the
eight affine clauses exclude precisely those cases. The full-support guard is
the exact complement of the previously excluded joint one-or-two-multiplicity
sector. Finally, both polarity clauses are emitted for every physical
five-set, with only genuinely constant or duplicate literals simplified.

Direct combinatorial derivation reproduces all four uniform formula shapes:

| Category | Tasks | Variables | Base clauses | Ramsey clauses | Total clauses |
|---|---:|---:|---:|---:|---:|
| affine rows | 5 | 1,157 | 11,258 | 1,925,196 | 1,936,454 |
| known-profile guard | 4 | 1,503 | 12,910 | 1,925,196 | 1,938,106 |
| ordinary | 5,841 | 1,157 | 11,250 | 1,925,196 | 1,936,446 |
| zero row | 5,109 | 1,157 | 11,273 | 1,817,142 | 1,828,415 |

## Reproduction

From the repository root, with a C++17 compiler and CPython 3.11 or later:

```bash
python3 -B ramsey_r55_rank4_complete_task_cover_review1/independent_check.py \
  ramsey_r55_rank4_complete_task_cover \
  --work-root /scratch/research-team-v2/tmp/reviewer-1
python3 -O -B ramsey_r55_rank4_complete_task_cover_review1/independent_check.py \
  ramsey_r55_rank4_complete_task_cover \
  --work-root /scratch/research-team-v2/tmp/reviewer-1
```

The checker imports no submitted module. Expected final status:

    VERIFIED_INDEPENDENT_RANK4_TASK_COVER_REVIEW

Separately, the submitted full replay was run from a detached checkout at the
verified commit:

```bash
python3 -B reproduce.py --work-root /scratch/research-team-v2/tmp/reviewer-1
```

It regenerated the table, checked the two independent submitted orbit
implementations, rejected all six corrupted small certificates, exhausted the
small physical controls, transported all 903 edge coordinates in sixteen
normalizations, and independently read all 7,592,730 Ramsey clauses across
four complete representative CNFs. It returned
`VERIFIED_ALL_PATTERN_RANK4_TASK_HANDOFF` with table SHA-256
`bd1161b4261eb1ee3f8bc2cd0104a062c858bf38d596cf725acbfb195b158bac`
and audit SHA-256
`4ce493a63cf754fc7329d8236820d8cb53e442089b403e5ffa638fb098c44c29`.

## Imported premises and trust boundary

Imported rather than reopened here: the previously accepted cut-rank theorem,
four-set row cap, global zero/column caps, and full-support physical-completion
exclusion. The invalidated h3687 automorphism verifier and the parked B23
projection are not premises. Remaining computational trust includes CPython
integer semantics, the C++ compiler and runtime, SHA-256, the pinned source and
table bytes, this reviewer's implementation, and ordinary hardware. The
algebraic reduction is not proof-assistant formalized. No SAT result, private
checkpoint, or unverified solver transcript is accepted by this review.
