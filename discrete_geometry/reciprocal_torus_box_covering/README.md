# Exact reciprocal-box coverings of a torus

Let `T = R/Z`. For positive integers sorted as
`m_1 >= ... >= m_n >= 1`, the minimum number of translates of the open box

\[
B=(0,1/m_1)\times\cdots\times(0,1/m_n)\subset\mathbb T^n
\]

covering the entire torus is

\[
\boxed{N=1+m_1+m_1m_2+\cdots+m_1\cdots m_n.}
\]

Writing `p_0=1` and `p_k=m_1...m_k`, an optimal cover has centers

\[
\left(j/N,p_1j/N,\ldots,p_{n-1}j/N\right)\pmod1,
\qquad 0\le j<N.
\]

For example, side lengths `(1/3,1/2)` need exactly 10 translates;
`(1/4,1/3,1/2)` need 41. No coprimality assumption is needed. A side length
one denotes a punctured-circle factor: `(0,1)` modulo one omits zero.
Unsorted input is handled by permuting coordinates.

[PROOF.md](PROOF.md) gives the complete structural argument. Compactness
and fiber integration give a strict recursive lower bound. An explicit
cyclic selection attains it; its wrap-gap inequality follows from

\[
p_{k-1}-(m_k-1)\sum_{j=0}^{k-2}p_j
=1+\sum_{j=1}^{k-1}(m_j-m_k)p_{j-1}\ge1.
\]

The proof also supplies explicit shrinkage margins. Closed reciprocal
boxes instead tile with `product(m_i)` translates, so the open-boundary
convention is essential.

## Prior work and scope

This extends the **equal-side** theorem of Rotem--Schejter--Slomka,
[The complex Illumination problem, Combinatorica 46 (2026), article 3](https://link.springer.com/article/10.1007/s00493-025-00195-7),
Theorem 1.6 and Propositions 2.3/2.7. Their slicing and cyclic-gap methods
are the starting point. The unequal-side formula and its ordering identity
are the contribution here; the equal-side result is not claimed as new.
Targeted source and graph searches on 2026-09-20 found no matching
all-dimensional unequal-side theorem. Historical priority is not certified.

This auxiliary torus-covering result does not solve the general real or
complex illumination conjectures. It does not classify all optimal covers
or all nonreciprocal side lengths. The written proof is unformalized and
awaits independent review. Its only general prerequisites are elementary
compactness, integration, and finite cyclic order.

## Reproduce

Tested with CPython 3.11.2. Python 3.11+ and the standard library suffice;
there are no solvers, external datasets, random inputs, or floating point.
From this directory:

```sh
python3 verify.py --check
sha256sum -c SHA256SUMS
```

[verify.py](verify.py) must produce the exact adjacent
[EXPECTED.json](EXPECTED.json), including `status: PASS`. It verifies:

* 56 parameter tuples by a complete endpoint/cell arrangement check,
  including 14,466,265 coverage-mask intersections;
* 1,792 deterministic rational targets and 5,568 stages of the constructive
  selection, with cardinality, distinctness, coverage and gap invariants;
* all six coordinate permutations of `(3,2,1)`;
* five exact uncovered points after deleting a center;
* four open/closed boundary controls, five rejected invalid inputs, the
  published erroneous seven-center construction, and a raw construction
  that omits the necessary sorting.

The arrangement checker works directly with concrete translated intervals.
It does not use the induction, tail counts, or gap inequality. Membership
is constant between successive endpoints, and endpoints are tested
separately, so each finite center configuration is checked over the entire
continuum. Equal masks are merged only when all future intersection
decisions are identical.

All equalities use integers or `fractions.Fraction`. Failure raises an
exception and exits nonzero, even with Python optimization enabled. The
finite checks corroborate the universal proof; they do not replace it or
constitute peer review. `SHA256SUMS` covers the four other files, and no
unpublished artifact is required.
