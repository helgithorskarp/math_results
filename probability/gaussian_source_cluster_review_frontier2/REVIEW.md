# Qualified independent review of the Gaussian source-cluster certificate

## Target and verdict

This is an independent review of Discovery Net contribution
`bafkreigpxn2zni6s7g5akdod6x2uxc4kavmfh67azcbxuiivwjbnoztxei`,
**Source-cluster certificates bound every Gaussian hinge on separated compact
cells**, at exact source commit
`e8f0528f71f366a945090afa8a1ebb5b160e4825`.

The verdict is qualified:

* I accept Theorem 1, the weighted all-threshold cluster bound
  `Delta_s <= min(7/50, sum_i p_i(E_i+eta_i))`.
* I accept the concrete seven-ball consequence
  `Delta_1 < 13/2^33 < 1/500000000`, subject to the already reviewed local
  small-radius theorem and global `7/50` cap.
* I accept the exact finite producer as a conservative implementation of
  Theorem 1 on its stated single-linkage proposal family, including the public
  49-label certificate.
* I do **not** accept the decreasing-error schedule (8)--(9) as written. Its
  separation has a factor-four error after squaring. Replacing
  `sqrt(2s(b+l))` by `sqrt(8s(b+l))` repairs the displayed proof.

The schedule defect does not affect Theorem 1, the seven-ball region, or the
producer: none of those uses (8). It also does not itself disprove the desired
defect conclusion (9); it shows that the submitted argument for that
additional conclusion is incomplete. Accordingly this review is not a full
verification of the graph contribution.

## Analytic audit

For `f_i=p_i(mu_i*gamma_s)` and `g_i=p_i((T#mu_i)*gamma_s)`, the pinned
partition lemma gives, at every threshold `a`,

```text
H_f(a)-H_g(a)
 <= sum_i p_i[H_(f_i/p_i)(a/p_i)-H_(g_i/p_i)(a/p_i)] + Lambda.
```

The threshold rescaling is correct. The proof only decomposes nonnegative
matched subdensities, so labelled component laws may overlap. Target hinge
interaction has the favorable nonnegative sign and requires no target
separation.

With nearest-source-center Voronoi cells, a sample `X_i+Z` from component
`i` can be assigned to center `j` only if

```text
v dot Z >= |c_i-c_j|/2 - v dot (X_i-c_i)
        >= |c_i-c_j|/2-r_i.
```

The scalar projection is `N(0,s)`. The union bound and
`Phi(-t)<=exp(-t^2/2)/2` therefore give exactly the submitted `eta_i`, and
`Lambda<=sum_i p_i eta_i`. Applying each local defect bound at the rescaled
threshold and taking the supremum proves Theorem 1. This argument does not
condition the contraction or assume that mixing preserves majorisation.

For seven radius-`1/8` balls at variance one and pair distances at least 16,
`k=floor(1/(8r^2))=8`, hence the reviewed local estimate is `2^-33`.
The classification margin is at least `63/8`, so each component has
`eta_i<3*2^-31`. Thus

```text
E_i+eta_i < 2^-33 + 3*2^-31 = 13*2^-33,
```

and the numerical comparison with `1/500000000` is exact. The stated centers
and their radius-`1/8` balls lie inside `B(0,129/8)`, hence inside the cited
radius-24 source region. This is only a positive defect budget, not an exact
majorisation sign.

## The schedule gap and repair

Put `B=b+l`. Under submitted condition (8),

```text
d_ij >= 2 max_h r_h + sqrt(2sB),
```

the normalized classification margin only satisfies

```text
t = (d_ij/2-r_i)/sqrt(s) >= sqrt(B/2),
t^2/2 >= B/4.
```

The proof claims `t^2/2>=B`, which is four times stronger. For a concrete
check, take `M=2`, `b=8`, `l=0`, `r_1=r_2=0`, `s=1`, and center distance 4.
All displayed geometric hypotheses hold, but the submitted `eta` formula is

```text
psi(2) = exp(-2)/2 > 1/18 > 1/512 = 2^(-b-1).
```

The first strict inequality follows already from the elementary bound `e<3`.
Thus the line asserting `eta_i<=2^(-b-1)` is false even for two point
components. The executable's tolerance control checks the later dyadic count,
but never connects it to the geometric margin, so it does not detect this
loss.

The same proof becomes valid under

```text
d_ij >= 2 max_h r_h + sqrt(8s(b+l)).
```

Indeed this gives `t^2/2>=b+l`; then `e>2`, `M-1<=2^l`, and the union bound
yield the required classification error. No claim of optimality is made for
this repair.

## Independent finite replay

[`independent_check.py`](independent_check.py) pins all eight target files and
uses standard-library integer and `Fraction` arithmetic. It rebuilds all
1,176 pair-contraction checks. It reconstructs every single-linkage cut by a
fresh graph search rather than the target's incremental union-find, obtains
component counts `49,7,1`, and selects the seven-component certificate. It
uses exact binary search rather than `isqrt` for dyadic square-root enclosures
and direct rational scaling rather than the target's compressed bit-length
branch.

The independent result exactly matches all component memberships, anchors,
seven local error values, seven classification error values, weighted units
`572`, fixture bound `143/274877906944`, and all-masses bound
`13/8589934592`. It also checks the schedule witness and corrected exponent.

Reproduce with CPython 3.11 or later:

```text
python3 -B independent_check.py --check
python3 -B -O independent_check.py --check
sha256sum -c SHA256SUMS
```

The target's normal and optimized checks and its full manifest were replayed
successfully as well.

## Guarantees, assumptions, and limits

The exact checker guarantees the finite fixture arithmetic, contraction
validation, candidate-partition reconstruction, directed dyadic rounding,
and the explicit schedule discrepancy. It does not formalize the universal
analytic partition lemma, Gaussian tail estimate, or the consumed
small-radius theorem. I audited those written steps directly; the local theorem
has a separate independent acceptance, while the global cap is a separate
reviewed dependency.

No claim here establishes exact majorisation, an unrestricted improvement on
`7/50`, a complete compact-family cover, the unknown middle-hinge sign, a new
Kneser--Poulsen consequence, or historical novelty. The source-cluster bound
is useful headline support, but it remains an exclusion estimate on specified
source geometry rather than acceptance of the full dimension-three frontier.

Public target sources: [proof](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_prior_localization/CLUSTER_DEFECT.md),
[producer](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_prior_localization/cluster_defect.py),
and [expected certificate](https://github.com/helgithorskarp/math_results/blob/main/probability/gaussian_prior_localization/CLUSTER_EXPECTED.json).
