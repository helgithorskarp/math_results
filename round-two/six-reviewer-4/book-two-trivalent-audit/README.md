# Independent Book quotient audit and a removed equality profile

Actual agent: **six-reviewer-4**, role **independent reviewer**, 2026-10-01.
Campaign signatures share one identity. Independence rests on the independently
selected target, derivation and component-based implementation.

[REVIEW.md](REVIEW.md) confirms the one-trivalent extension of committed
lemma8494, subject to its named inherited premises. It also proves an ordinary
local signed-row consequence and excludes the listed twenty-uniform-pair
degree profile `3^4,2,1^6`. Combining that exclusion with the target leaves
only `3^2,2^5,1^4` and `3^3,2^3,1^5` at equality. Neither remaining profile is
asserted feasible, and this does not determine R(B4,B7).

The original source commit is `cc3e93d253b760355191fd7a2115d0fabd9db088`;
the reviewed snapshot was extracted from repository commit
`6dffbb940c10f415b71e275a45010a7141d1ee4e`.

From the repository root, CPython 3.11+, standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -O -B round-two/six-reviewer-4/book-two-trivalent-audit/audit.py \
  --expected round-two/six-reviewer-4/book-two-trivalent-audit/expected.json
```

Expected: 24 red component forms, 30 inside cases, 121820 unfiltered degree
graphs with no aggregate-page survivor; the author's narrowed domain has
2428 cases (661 at r10, 1767 at r11), with failures R=1913, D=222, M=293.
Our independent record encoding has SHA256
`f8b8d8f351742c984a3f7787cafdde9dfd786fc25569957f38e442a2d6a1e14e`.
Re-encoding those records in the author's format gives
`d019f05fbe99d92d8e0f5a795bb58ef5eeaea04b9d142684f77d16be0d3470e1`.

The checker imports no earlier generator and takes no graph catalogue as input.
It deletes the unique trivalent D vertex, then enumerates paths between
residual degree-one endpoints and cycles on residual degree-two vertices.
Forced sibling edges and weak cross-term clauses are tested after complete
generation. Every unfiltered graph is also tested against the full necessary
page inequalities. Expected data is a redundant output comparison, never a
search input. Mathematical reductions and the universal-sign bridge are written
and unformalized. Interpreter execution and code inspection are trust boundaries.

The stronger equality-profile exclusion is a written capacity proof; its
3072-word degree check is validation, not a finite theorem premise.

Optional entry-level comparison, after generating the original records with its
documented `check_two_trivalent.py --scratch YOUR_SCRATCH` wrapper:

```sh
python3 -B round-two/six-reviewer-4/book-two-trivalent-audit/audit.py \
  --expected round-two/six-reviewer-4/book-two-trivalent-audit/expected.json \
  --author-fixture book_ramsey_b4_b7_free_involution/two_trivalent_expected.json \
  --author-records YOUR_SCRATCH/records.jsonl
```

All 2428 records were compared entry by entry during review. The standalone
default original census entry point has a tuple/list fixture-comparison defect;
its documented wrapper passes. See the precise limitation in REVIEW.md.
Full generated records, logs and author source extracts remain in scratch.
Only this source, compact expectations, validation receipt and review are public.
