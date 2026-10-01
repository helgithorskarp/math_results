# Capped unions and maximal-rank two-facet certificates

Actual author: **six-downset-1**, role **researcher**, fresh round two,
2026-10-01. Author-checked ordinary proofs with exact finite validation;
unformalized and not independently reviewed.

[PROOF.md](PROOF.md) proves an exact closure rule for spectral Chvatal H.
Given capped H certificates on at least two downsets with disjoint
coordinate supports and the **same largest-star size**, their union
retains the cap after identifying the empty vertices. Its unit eigenvalue
becomes simple, lower-slack nullities add exactly, and a positive explicit
upper spectral gap depends only on component sizes and the common star.
Factors need not be isomorphic, centered, nonsingular or entrywise positive.

[UNEQUAL_FACETS.md](UNEQUAL_FACETS.md) supplies an additional repair for
two Boolean cubes of arbitrary unequal orders. An aligned rational core
has an explicit strict cap margin; a rational mixture removes its excess
lower kernel. Consequently **every downset with exactly two maximal
members**, of any sizes or overlap, has a rational capped H matrix with
universally maximal lower rank. This is an explicit rank construction;
no priority claim for ordinary two-facet H is made.

For r>=2 equal n-point Boolean cubes, n>=2, put s=2^(n-1),
N=r(2s-1)+1 and b=N-s. The complete output spectrum is

| Eigenvalue | Multiplicity |
| --- | ---: |
| 1 | 1 |
| -s/b | rs |
| s/b | r(s-2) |
| 1/b | r-1 |
| [r(s-1)+1]/b | 1 |

The lower rank N-rs is maximal among **all real H certificates**.
Products of these union factors inherit explicit maximal-rank capped
certificates and a precise cylinder classification of maximum intersecting
families. Adding a free c-point core yields unions of overlapping equal
Boolean facets, with maximal lower rank 2^c N-2^(c-1); at c=1 the shared
point star is the unique maximum intersecting family.

The credited core lift and ordinary union/tensor transport are from
[the previous structural proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
graph7578. Classical complementary selectors and switching, the prior
proper-cube argument8020 and its full-cube audit8066 supply the credited
forced-span mechanism. The new cap closure and union spectra do not
resolve general H or I. A signed exact negative witness shows why the
ordinary shifted-core union recipe cannot automatically extend this cap
rule to unequal stars; the witness downset still has a different valid cap.

Reproduce from the repository root with **CPython 3.11.2**, standard library
only (compatible Python3.10+ supports the language features used):

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-downset-1/verify.py --check round-two/six-downset-1/RESULTS.json
```

To regenerate compact results, use `--output /tmp/equal-star-results.json`
instead of `--check`. The same checks run under `python3 -B -O`.
From this directory `sha256sum -c SHA256SUMS` verifies the compact source.
Expected summary: `ok:true`, nine baselines, ten unions, nine unequal-cube
repairs, seven products, largest literal matrix order70, and twelve
rejection controls.
The deterministic [RESULTS.json](RESULTS.json) SHA256 is
`bb547adc6e4e7be1316a1971d7931f9ebfbd075569d34c5a10c095c318484c21`.

[verify.py](verify.py) compares every union entry from the full factor
formula against a separate core lift. It checks support, symmetry,
row sums, actual downsets and largest stars, both complete rational PSD
slacks, their ranks, complete cube spectra, the quantitative gap, mixed
signed/repeated-unit factors, products and common-core facets. It also
constructs all target complementary switches through cube order five and
independently enumerates every maximum cube family through order four.
The shifted unequal-star recipe has scaled upper quadratic form **-37**;
a separate valid capped certificate is verified on that very same family.
The unequal-cube repair attains maximal lower rank there. Every unequal
case checks the full seed and repaired matrices, the exact frame bound,
the shifted trace, and the rational repaired upper gap; the u=1 boundary
and both equal/unequal common-core products are covered.

One normal replay took13.48seconds with21,460KiB peak RSS under the standing
one-process/one-thread scope. Normal and optimized runs produce identical
results. These measurements are local reproduction evidence, not a
performance guarantee. Bitmasks encode coordinates from least significant
bit zero; unions use sequential fresh coordinate blocks and products use
lexicographic factor-index tuples.

The trust boundary is ordinary written mathematics and Python integer/
Fraction semantics. No external solver, floating tolerance, CAS,
classification corpus, private input or large omitted certificate is used.
Finite checks validate the implementation; the written proof supplies
the unbounded statements. The current primary problem remains
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
