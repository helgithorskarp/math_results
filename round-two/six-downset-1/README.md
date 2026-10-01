# Equal-star capped unions and Boolean facet spectra

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
Expected summary: `ok:true`, nine baselines, ten unions, five products,
largest literal matrix order70, and twelve rejection controls.
The deterministic [RESULTS.json](RESULTS.json) SHA256 is
`fa6b4b61e27ee716248bc81828f13244f187a94fc3841f7848f70d78f0b83b72`.

[verify.py](verify.py) compares every union entry from the full factor
formula against a separate core lift. It checks support, symmetry,
row sums, actual downsets and largest stars, both complete rational PSD
slacks, their ranks, complete cube spectra, the quantitative gap, mixed
signed/repeated-unit factors, products and common-core facets. It also
constructs all target complementary switches through cube order five and
independently enumerates every maximum cube family through order four.
The shifted unequal-star recipe has scaled upper quadratic form **-37**;
a separate valid capped certificate is verified on that very same family.

One normal replay took3.47seconds with19,944KiB peak RSS under the standing
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
