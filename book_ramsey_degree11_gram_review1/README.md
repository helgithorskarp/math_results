# Independent Book Ramsey degree-eleven audit

Actual agent **six-reviewer-1**, role **independent mathematical reviewer**.

[REVIEW.md](REVIEW.md) verifies the unrestricted degree-eleven exclusion and
proves a stronger finite lemma: every forced matrix in all68,895 reduced
assignments is indefinite, even without entry, row or rank filters. Thus no
real Gram factorization of any rank exists in that integer-budget family.
With credited prior results, every22-vertex ordinary red-B4/blue-B7-free
coloring has red degrees8–10 and97–110 edges. The Ramsey22–23 gap remains open.

CPython3.11+ (tested3.11.2), standard library, from repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B book_ramsey_degree11_gram_review1/audit.py \
  --check book_ramsey_degree11_gram_review1/expected.json
```

The independent checker uses adaptive largest-residual-degree graph branching,
complete explicit orbit partitions, bitset page equations and exact symmetric
integer Schur elimination. Every generated negative vector is checked directly
in its original full matrix. It reads no author code, catalogue or vector pool.
The6551-byte [expected output](expected.json) includes all177 compact core
records and case counts; full labeled domains and matrices are regenerated.
SHA2569d2295127f4c61f0a272a21a5e279b96736320c8e7d388d2766d04213aee4474.
All729 small principal-minor controls and177 literal full-host controls pass;
the latter cover9735 spine equations and are not valid Ramsey witnesses.
Normal25.305s/53128KiB, optimized26.607s/54984KiB, byte-identical output.

Optional reproduction of the author's pinned generator with a passive full
case/matrix observer, separate from the independent proof:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 -B -O book_ramsey_degree11_gram_review1/compare_author.py
```

This optional command requires the11 original files pinned in
[provenance.json](provenance.json) to remain present at their recorded hashes.
It rejects updated inputs; reviewed author source commit is
ce3177a731086284ee89f18a8a3948b672b3c64e. The standalone audit has no such
external input requirement. [author_comparison.json](author_comparison.json)
records the completed comparison. [SHA256SUMS](SHA256SUMS) covers compact
public source. No binary, credential, private ledger or large corpus is included.
The written local reduction and inherited minimum-degree classification boundary
remain explicitly unformalized and credited in the review.
