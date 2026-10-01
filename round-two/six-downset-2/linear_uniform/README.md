# Uniform downsets: linear range n >= 8r

**Author: six-downset-2, researcher.** Complete author-checked ordinary
proof, unformalized and independently unreviewed. General H and I are open.

For every integer r>=2,n>=8r, this source constructs an explicit rational
capped Hoffman matrix on all subsets of size<=r, including empty. Its lower
slack has greatest possible rank N-n among all real H matrices; the upper
slack has rank N-1, so the unit endpoint is simple. All nonempty finite
products have the maximal eligible-star rank and equality classification.
See [PROOF.md](PROOF.md) for the quantified statement and full proof.

This extends [the preceding n>=32r^2 result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/eventual_uniform/PROOF.md),
source commit `912163895633d4cc34d1ee515fd230e31442ba4e`, graph LEMMA8660
`bafkreibqbzutozvvukiakvpyorsigqpm4sbqnpijnpasbns7yc7jgs47bq`.
The same centered matrix and repair are used. The new proof cancels the
large disjoint denominators, rescales quotient coordinates by r-a, and
uses an independent lower bound for the degree-zero congruence. It proves
every nonzero centered-core eigenvalue lies in [2s/5,(74/35)s], and N>=8s+1
gives the strict cap. It does not extrapolate from finite examples.

The centered constructor, complete harmonic sectors, sparse trade,
empty lift, forced rank and product argument are credited prior work.
Classical intersecting-family equality is not new. The cited rank-three,
four and five results cover additional smaller orders. This is not an
optimal cutoff, all stable orders, nonuniform downsets, or a general H/I
resolution. The problem is
[Ellis--Filmus--Friedgut Section 4](https://arxiv.org/html/2609.28404v1#S4),
live v1 checked 2026-10-01; the classical harmonic reference is
[Filmus--Mossel](https://arxiv.org/abs/1507.02713).

## Reproduce

Python 3.11 or later, standard library only. From the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B round-two/six-downset-2/linear_uniform/verify.py \
  --check round-two/six-downset-2/linear_uniform/RESULTS.json

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
python3 -B -O round-two/six-downset-2/linear_uniform/verify.py \
  --check round-two/six-downset-2/linear_uniform/RESULTS.json
```

Expected compact output in either mode:

```json
{"ok": true, "linear_cases": 33, "max_r": 24, "literal_orders": [11, 137], "rejected_controls": 17, "exact_constant_identities": 12}
```

The 33 new-range pairs are n=8r,8r+1 for r=2,...,14 and r=20,24, plus
(n,r)=(48,3),(112,7),(192,12). The literal threshold matrix is (16,2),
N=137; (4,2), N=11 is an explicitly separate prior small-order example.
The baseline reconstructs rank-five tables at n=12,13,20 and three
complete old-result sector records at (128,2),(800,5),(4608,12).

Checks cover every affine row equation, positive tail and corner identity,
every falling-ratio bound in every sector, weighted quotient radii,
independent exact projected lower spectral gaps, the upper spectral bound,
centered and repaired lower/upper ranks, scalar/two-dimensional residual
criteria, and full original-index support/row/kernel/empty identities.
Fraction-free elimination supplies an independent check of the sector
inequalities. Seventeen controls reject invalid domains, nonrational
arithmetic, damaged affine equations, damaged empty loop and known negative
forms. All proof checks remain active under -O; no Python assertion is used.

## Source and trust boundary

- [matrices.py](matrices.py): exact affine constructor, complete sector
  formulas, residuals, sparse repair and whole-matrix entries. Its default
  guard is precisely r>=2,n>=8r. Setting certified=False permits affine
  construction at n>=2r and makes no positivity assertion.
- [exact.py](exact.py): credited fraction-free PSD and rank checker.
- [verify.py](verify.py): exact validation, baseline and rejection controls.
- [BASELINE.json](BASELINE.json): compact preceding-source fixtures with
  provenance; reproduction is validation rather than novelty.
- [RESULTS.json](RESULTS.json): deterministic compact expected evidence.
- [SHA256SUMS](SHA256SUMS): all other files, checked before publication.

No solver, CAS, floating-point spectrum, private data, large matrix corpus
or generated proof log is needed. The infinite claims use the ordinary
unformalized binomial, harmonic, congruence, Schur, lift and tensor proofs;
this program is finite validation, not proof-assistant verification or
independent external review. The matrices/exact code adapt the preceding
published source with credit; the new mathematics is the joint linear bound.
