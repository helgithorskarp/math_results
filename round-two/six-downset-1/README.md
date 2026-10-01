# Capped maximal-rank H for structured Boolean facets

Actual author: **six-downset-1**, role **researcher**, fresh round two,
2026-10-01. The distinct-mark constructions are author-checked and
unformalized, with exact rational validation; independent review is pending.
The arbitrary-petal result8700 has independent review8779. That review
does not cover the distinct-mark extension.
The parent two-facet result8579 and three-petal result8642 have independent
reviews8640 and8682, respectively. Those verdicts do not cover the extension.

[ALL_MARKS.md](ALL_MARKS.md) proves a rational capped H matrix for every
n>=2 Boolean cube with one pendant edge at each of r distinct marked
coordinates, 2<=r<=n. With q=2^(n-1), N=2q+2r and s=q+1, its lower
rank is the universally greatest N-r and its upper rank is N-1.
Every nonunit eigenvalue is at most 1-1/[2(q+2r-1)], and the r marked
stars are exactly the maximum intersecting families. A modified cube
core makes the marked-star vectors orthogonal; a complete decomposition
into one three-dimensional sector, r-1 two-dimensional sectors and
all untouched directions proves the cap. The n=2 boundary is explicit.
A rational mixture restores maximal lower rank. Finite strict-factor
products inherit the credited eligible-cylinder rank/equality rule.
An exact obstruction shows that the previous fixed cube core cannot
admit any three-distinct-mark cap for n>=5; the modified core escapes it.

Run the new replay from the repository root with CPython3.11+ and the
standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-downset-1/verify_all_marks.py --check round-two/six-downset-1/ALL_MARKS_RESULTS.json
```

Expected:15 canonical instances (all n2..6,r2..n), one relabeling,
57 scalar frame fixtures,30 formally reconstructed positive coefficients,
four old-core cases, two products and15 rejection controls. Largest full
matrix order76. Normal and assertion-disabled (`python3 -B -O`) replays
agree; the deterministic [ALL_MARKS_RESULTS.json](ALL_MARKS_RESULTS.json)
SHA256 is
`fa7c8a967ccb516d5a7a205f3e1f6058ecfde99b494a41875ac0d6dbeb27b058`.
The final normal/optimized replays took36.49s/37.72s and
22,420/24,912KiB peak child RSS under CPython3.11.2, serial/thread-one.
The complete written proof supplies unbounded coverage. Repeated or
unequal numbers of leaves at different marks and arbitrary overlapping
facets remain outside this statement; general H/I remain open.

[TWO_MARKED_CUBE.md](TWO_MARKED_CUBE.md) proves a rational capped H matrix
for an n-point Boolean cube, n>=3, with two fresh pendant edges attached
at **distinct** old coordinates. With q=2^(n-1), N=2q+4 and s=q+1, its
lower rank is the universally greatest N-2, its upper rank is N-1, and
every nonunit eigenvalue is at most 1-1/[2(q+3)]. Its two maximum
intersecting families are exactly the marked stars. The three facets
meet in two different singleton intersections, so this class lies beyond
the common-core sunflower scope. The complete centered-frame cap proof
accounts for both changed sectors and both untouched eigenspaces;
an explicit rational trace-bounded mixture removes one extra kernel.

Run the two-marked-cube replay from the repository root with CPython3.11+
and the standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-downset-1/verify_two_marks.py --check round-two/six-downset-1/TWO_MARKED_RESULTS.json
```

Expected: four literal cubes n=3..6 (largest N=68), 24 rational frame
fixtures and ten rejection controls. All original-index PSD/rank/support
conditions and the half-gap are checked exactly. The deterministic
[TWO_MARKED_RESULTS.json](TWO_MARKED_RESULTS.json) SHA256 is
`8c08c7e6ca3d399f99300d740c4ce9b33ed2042180fc17b61382c3442f4903ad`.
Normal and assertion-disabled (`python3 -B -O`) runs match, taking
5.56s/5.94s with22,012/23,208KiB peak child RSS under CPython3.11.2.
The unbounded n>=3 coverage comes from the written complete decomposition
and rank-one inequality. ALL_MARKS.md now handles additional distinct
marked pendants. Arbitrary larger outer petals and general H/I remain open.

[ALL_PETALS.md](ALL_PETALS.md) now proves a rational capped H certificate
with greatest possible lower rank for **every Boolean sunflower**, with
arbitrary petal count and sizes. For disjoint nonempty petals, r>=2,
largest cube star t, largest-order multiplicity k and total size N, the
lower rank is N-kt and the unit endpoint is simple (upper rank N-1).
The new opposite-pair frame attachments extend the credited two- and
three-petal seeds to any number of smaller petals; equal-star gluing
then handles repeated largest petals. A common c-point core, c>=1,
gives both ranks N-2^(c-1), with exact maximum-family cylinder equality.
Finite strict-factor products retain the credited eligible-factor
rank/equality description. General overlapping facets remain outside
the result, and general H/I remain open.

Run the arbitrary-petal replay from the repository root with CPython3.11+ and
the standard library only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-downset-1/verify_all_petals.py --check round-two/six-downset-1/ALL_PETALS_RESULTS.json
```

Expected: `ok:true`, all35 sorted four-petal order1..4 tuples plus15
additional union fixtures, three products, four common-core products,
largest full matrix71, largest petal count15, and12 rejection controls.
The fixtures cover every leading attachment regime. The checker also
reconstructs the credited263 positive sign coefficients. Normal and
optimized (`python3 -B -O`) runs match. The deterministic
[ALL_PETALS_RESULTS.json](ALL_PETALS_RESULTS.json) SHA256 is
`3f1b9bd966a3ba795892e80152927935ccb6967407d75c2849c3021d17cf0a68`.
The unbounded extension uses the written exact pair norm budgets and
kernel/transport arguments, with the existing sign certificate for
leading triples. Finite matrix fixtures alone do not prove it.
The final normal replay took23.68seconds/25,608KiB peak child RSS;
the optimized replay took21.16seconds/26,920KiB with CPython3.11.2.
There was one mathematical job at a time, with every configured numerical
thread count one. These are local reproduction measurements.

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

[MULTI_FACETS.md](MULTI_FACETS.md) is the preceding repair for **every three-petal
Boolean sunflower**, allowing unequal petal orders. On disjoint petals,
let r be their number, t the largest cube star and k the number attaining
t. The same construction and the credited equal-star union also cover
every r<=3k: lower rank N-kt is universally maximal and the upper rank
is N-1. A nonempty common c-point core gives lower and upper rank
N-2^(c-1). The new mechanism is a small fixed-diagonal Gram LMI;
three explicit Gram choices and an exact polynomial sign certificate
cover every dyadic ordering. General overlapping three-facet families
and unrestricted unequal-star cap closure remain outside the claim.

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

Reproduce the new multi-facet result with Python3.11+, standard library
and the local parent verify.py only:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B round-two/six-downset-1/verify_multi.py --check round-two/six-downset-1/MULTI_RESULTS.json --coefficients round-two/six-downset-1/MARGIN_COEFFICIENTS.json
```

Expected: `ok:true`, all20 sorted order1..4 triples plus four further
triples, five packet assemblies, four products, four common-core
sunflowers, largest matrix order74, and16 rejection controls. Every
coefficient of three margin polynomials is reconstructed and checked:
34,219,10 positive integer coefficients, respectively. The infinite
wide-gap step uses this263-coefficient exact certificate rather than
finite matrix sampling. Normal and optimized replays agree.
[MULTI_RESULTS.json](MULTI_RESULTS.json) SHA256 is
`e2bffb13274445cded7b3b808cd0e9ec6389613d4de88d71664bdfc4dc808d0d`;
[MARGIN_COEFFICIENTS.json](MARGIN_COEFFICIENTS.json) SHA256 is
`892ff3f9611aa4632fd67936d630eff35c52960098016c404323c9446dc5ddbb`.
A normal new replay took12.64seconds and25,128KiB peak child RSS with
CPython3.11.2. The finite literal constructor refuses matrix order>80;
this resource guard does not restrict the mathematical theorem.

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
Finite matrix checks validate the implementation; the written proof and,
for the wide-gap multi-facet step, its exact coefficient certificate
supply the unbounded statements. The current primary problem remains
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
