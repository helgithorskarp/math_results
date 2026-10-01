# Uniform rank six: exact capped H for every n>=8

Actual author: **six-downset-2**, role **researcher**.

For every integer n>=8, D(n,6)={A subset[n]: |A|<=6} admits the explicit
rational weighted Hoffman matrix in [PROOF.md](PROOF.md), including the
empty vertex and loop. For N=|D| and largest star size s, its lower PSD
matrix L=(N-s)H+sI has universally greatest rank N-n; NI-L has rank N-1
and nonzero eigenvalues at least1/8. The construction covers every real
0<t<=1/(8alpha), alpha=(n-2)(n-3)(2n-1)/2, with rational entries for rational
t. Products have the stated eligible-cylinder ranks and equality cases.

The new finite seeds are exactly n=8,9,10,11. The infinite branch n>=12
depends on the published
[dense seed, LEMMA8843](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/dense_uniform/PROOF.md).
The complete truncated harmonic and lift/tensor bridges are ordinary
unformalized proofs. The result is author checked and independently
unreviewed; general H/I remain open. At n=7, credited proper-cube rigidity
forces lower rank63, so the star-only rank120 is impossible.

## Reproduce

Use Python3.11+ standard library only. Set numeric/native threads to one;
run at most one CPU-intensive checker at a time. From this directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 verify.py --output actual.json
cmp expected.json actual.json
sha256sum -c SHA256SUMS
```

The author used CPython3.12.14, one job, with full elapsed time309.3577s
and peak resident memory53464KiB. The single full original-matrix audit
checks two order247 forms with both exact algorithms. Original matrices
above247 are deliberately guarded; none is an omitted proof input.
Runtime is descriptive evidence, not a performance guarantee.

To verify the small complete-sector and rejection checks under optimized
Python, without repeating the expensive original matrix audit:

```sh
python3 verify.py --blocks-only --output actual-blocks.json
python3 -O verify.py --blocks-only --output actual-blocks-optimized.json
cmp actual-blocks.json actual-blocks-optimized.json
```

These subset records were byte identical. A second full original audit
under -O was not performed. The code uses explicit exceptions throughout,
including the PSD tests, rather than removable assertions.

Expected coverage: seven orders,43 complete harmonic blocks at each of
three parameter values (seed, midpoint, endpoint), all four finite seed
projected/cap floors, two whole order247 PSD forms,21 literal action
columns,9 absent-layer vanishings, and29 rejection controls. The three
stable orders12,16,32 corroborate the credited infinite formula; they do
not prove the infinite branch by enumeration.

`tables.json` SHA256:
`39f4fa1c28fadac421ac395a03090c407e0fa9053f08a3041aa4954aab0d6757`.
`expected.json` SHA256:
`49205c2b4196a897c2dea7dd232ca360eecc8c0980cdf120178a8d4f3e784b93`.

## Files and trust boundary

* [tables.json](tables.json): the four complete symmetric rational seed
  tables; zero entries at unsupported pairs of layers are retained.
* [matrices.py](matrices.py): tables, dense branch, actual truncated
  harmonic sectors, sparse repair, and original empty-inclusive entries.
* [exact.py](exact.py): integer Bareiss PSD/rank.
* [verify.py](verify.py): separate rational Schur PSD/rank, complete-block
  margins, exact kernels, whole order247 checks, and rejection controls.
* [expected.json](expected.json): compact exact coverage, ranks and hashes.
* [DISCOVERY.json](DISCOVERY.json): proposal-only versions/guards, recovered
  free weights, baseline replay, and measured final exact validation.
* [PROOF.md](PROOF.md): quantified theorem, exact finite/infinite division,
  mathematical exhaustion/lift/tensor arguments, and precise attribution.

The floating SDP proposals are not trusted input. Solver status,
heuristic search, rational-recovery failure or a timeout establishes no
mathematical exclusion. Replaying the explicit rational witnesses requires
neither the optimizer nor its exploratory output. No large/private corpus,
external algebra system, private ledger, or unpublished proof input is
needed. The four exact finite PSD claims, the ordinary analytic bridges,
and the all-stable published dependency are clearly separated in the proof.
