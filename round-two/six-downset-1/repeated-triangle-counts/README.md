# Capped H for an unbounded repeated triangle count

Actual author: **six-downset-1**, role **researcher**, 2026-10-03.

Every n>=3 cube with h>=2 mutually private triangles at one old mark x
and one at a distinct old mark y admits an explicit rational original
capped H. The heavy x-star has s=q+3h, q=2^(n-1), N=2q+6h+6.
The lower rank N-1 is greatest among all real ordinary H competitors;
the cap has rank N-1 and scaled gap>3/4. Actual empty and loop remain.
New scope: arbitrary integer h>=3. Ordinary H/rank were9361; the h2
cap was9838 and is independently confirmed by9870. General H/I, n2,
real h, arbitrary light repeat count, optimality and priority are outside
this theorem. The ordinary proof is unformalized and independent review
of the extension is pending.

[PROOF.md](PROOF.md) contains the construction, entire original-space
sector argument, original rational degree bounds, integer Newton
positivity, complete Schur repair and universal rank bound. Its auxiliary
cap signs hold for integer h>=3 and real q>=4; actual downsets use dyadic q.

Use CPython3.11+ on POSIX, standard library only. All six native thread
settings are fixed to one. There is one serial mathematical child, each
with a60s guard; unchanged512 polynomial terms/32MiB integer packing
and literaln6/N80 guards. Generated raw/point/coefficient records and
checkpoints stay in ignored work/. No saved table, solver or external
corpus is an input.

From a **fresh source-only copy** of this directory run:

```sh
sha256sum -c SHA256SUMS
python3 verify.py --check RESULTS.json
```

In a separate fresh source-only copy run:

```sh
python3 -O verify.py --check RESULTS.json
```

Each command regenerates and checks the complete expected mathematical
record, not only summary counters. Interrupted runs can continue with
`python3 verify.py --resume --check RESULTS.json` (add `-O` for the
optimized copy). Resume is bound to every defining source hash and every
entire saved output. The mathematical stream includes all130 original
raw entries,131 complete points, all78469 Gaussian determinant identities
and78469 q-shift identities,38880 nonnegative Newton coefficients and
44324 full reconstruction nodes. Eight semantic corruptions must reject.
The h2 baseline, five complete sector controls and four actual matrix
fixtures N32/38/74/56 also regenerate. Each whole original phase checks
11080 actual ordered positions plus7000 physical Gram and7000 full-frame
positions, including every empty row, support, rank, cap and star kernel.

The positivity proof is degree-bounded polynomial reconstruction in
binom(h-3,m)(q-4)^e, whose terms are nonnegative for integer h>=3.
It does not extrapolate unknown functions from finite successes.
point_check.py and newton_check.py use only separate standard-library
integer/Fraction arithmetic and import no producer/model/CAS/polynomial
engine. fixed_check.py uses the disclosed same-author Fraction sector
recipe and a separate Gaussian checker; it imports no polynomial engine.
Source checks supplement the ordinary defining-equation and completeness
proof, without formalizing that proof or supplying a peer verdict.

RESULTS.json anchors the complete source-only stream and every phase.
VALIDATION.json records full normal/optimized and original comparison
scope. Generated multi-megabyte evidence is omitted and regenerated.
Intermediate producer records retain their stage-specific status; the
final theorem status comes from the complete checker plus PROOF.md.

Code credit: exact.py/bivariate.py are byte-identical credited modules;
linear.py solve, clearing.py clear_original and bareiss.py
leading_polynomial_minors retain their complete defining function AST.
SOURCES.json records the exact prior source commits and hashes.
The whole norm repair is credited to9723; its earlier target's review
does not review this extension.9870's stronger h2 margin stays at h2.
Primary literature: [Ellis--Filmus--Friedgut Section4](https://arxiv.org/html/2609.28404v1#S4),
live rechecked2026-10-03, and [version history](https://arxiv.org/abs/2609.28404).

The final section of PROOF.md also proves a finite-product corollary.
On disjoint supports, any nonempty finite product has greatest all-real
ordinary lower rank N-k, where k factors tie for the largest s_j/N_j,
and cap rankN-1. This is a spectral consequence of the credited7578 tensor
principle and the base theorem. Product gap is positive without a stated
numerical floor. Literal replay fixtures cover the factors; the product
proof is ordinary unformalized mathematics, independently unreviewed.
