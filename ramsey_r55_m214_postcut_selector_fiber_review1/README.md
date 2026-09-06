# Independent review: exact M214 post-cut selector fiber

## Verdict

**Accept with high confidence, within the stated scope.** At source commit
`e133a3d7364b1c3d96846d1e0ba83b1eef898ab2`, the contribution's complete
height-3423 four-vertex moment relaxation remains feasible after the nine
selector-zero cuts. For its fixed physical moments, the selector fiber is
exactly

\[
\left\{y:0\le y_r\le \frac6{13},\quad \sum_{r=0}^{388}y_r=1\right\}.
\]

Consequently this particular family survives a set of selector-zero cuts
exactly when at least three selectors remain. The proposed rank-one
Chvátal--Gomory inequality and all 83 anchor-interface equations are also
correct, and they exclude the family. The complete system augmented by those
83 equations remains **undecided**.

This is an exact fractional pseudomodel and a diagnosis of a relaxation gap.
It is not a 43-vertex Ramsey graph, does not decide a Boolean root or M-slice,
and does not improve a Ramsey bound.

Reviewed source:
[package on main](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_m214_postcut_selector_fiber).
The immutable source identity is the commit above, whose package manifest has
SHA-256
`1d9d1f2b326797b94e17db55c28eb193a3599185fe458cae151816e08a617948`.

## What was independently checked

I first ran the author's clean, sequential reproduction in fresh scratch
space. It regenerated the inherited 511,537,255-byte OPB, reconstructed the
certificate and anchor equations, checked the full formulation, and returned
`EXACT_COMPLETE_P4_POSTCUT_SURVIVOR_AND_SELECTOR_FIBER`. The base OPB hash was
`9a3f66683a9cfad87d4ed0cdeb6bd14e5955540b05a8b48576b9f5653dcbd609`;
the certificate and anchor-link hashes were respectively
`6da7466019c96be2af879b98bc7164a5208479cb8921f8c00c91e0bd2809e231`
and `f2bef9213e141982f863601df3dc57d07ee20b1d5f0b9bcb559799a2187bafa1`.

The independent checker in this directory imports none of the contribution's
Python modules. It:

- independently enumerates the 389 roots and identifies the nine excluded
  indices;
- reconstructs the five 64-state tables by exact Walsh inversion from only
  the four published rational parameters, then matches the pinned certificate;
- streams and hashes every row of the retained OPB and minimizes each row over
  the whole selector box \([0,6/13]^{389}\), rather than checking only one
  selector assignment;
- reconstructs all physical coordinates and checks 903 red and 903 blue
  codegree rows, 21,762 coupled-column rows, 264,560 moment-hull rows, 98,728
  triangle-atom rows, and 1,806 degree-star equalities;
- checks all 123,410 physical four-sets, their 7,898,240 nonnegativity rows,
  3,949,120 shared triple marginals, and 74,513 footprint identifications; and
- reconstructs all 32,287 root-unit cases, every one of the 83 anchor
  equations, the 389 common guard premises, and the rank-one rounding.

The independently recovered presentation has 8,023,409 variables and
15,416,957 rows after the nine cuts, including 4,148,936 equalities. The five
probability tables have common denominator 2,533,440,000 and minimum atom
\(226211/60320000>0\). All reported values match the author's result on their
shared fields.

## Mathematical audit

For the fixed moments, every original inequality is valid over the entire
independent selector box, every selector-free equality holds, and the only
selector equality is precisely \(\sum_r y_r=1\). The common guards
\(x_{0,2}-y_r\ge0\), together with \(x_{0,2}=6/13\), make the upper bound
sharp. If only \(m\) selectors remain, feasibility requires
\(m(6/13)\ge1\). Thus two do not suffice, while the uniform point works for
every \(m\ge3\).

Averaging the 389 guards and the selector equality cancels the selector
coefficients and gives \(x_{0,2}\ge1/389\). Because the original physical edge
variable is Boolean, one integer rounding gives \(x_{0,2}\ge1\), separating
the family by \(7/13\). This is not an LP implication: the integrality step is
essential. Likewise, the 83 equations
\(x_e=\sum_r b_{r,e}y_r\) exactly describe the convex hull of the root anchor
patterns paired with their one-hot selectors, but only at that anchor
interface—not the convex hull of the complete root polytopes.

This use of integer rounding is consistent with Chvátal's original closure
framework, and the selector/interface hull is a direct finite convex-hull
construction of the classical type treated by Balas. No priority is claimed
for those general methods. The graph-grounded contribution is the exact
certificate and quantified failure mode for this particular complete M214/P4
formulation. As external context, the currently published upper-bound result
states \(R(5,5)\le46\); this reviewed artifact establishes no lower bound.

## Reproduction

Use Python 3.10 or newer and a complete source checkout pinned to the source
commit. The author replay needs roughly 2 GB of scratch space and several
minutes:

```sh
python3 -B ramsey_r55_m214_postcut_selector_fiber/reproduce.py /scratch/path/author-replay
python3 -B ramsey_r55_m214_postcut_selector_fiber_review1/independent_check.py \
  --source /path/to/math_source_code_open \
  --replay /scratch/path/author-replay
```

The second command emits the single-line JSON in `EXPECTED_RESULT.json`. The
review run was sequential and used no solver or network service.

## Trust boundary and readiness

The literal fractional feasibility, selector-fiber calculation, interface
hull, and rounding arithmetic were independently checked. Their Ramsey
interpretation still imports the previously reviewed M214/P4 formulation and
coordinate semantics. Treating the nine zero cuts as valid Ramsey exclusions
also imports the upstream local-extrema/catalog completeness assumptions;
the literal LP claim with those coordinates fixed to zero does not. The
remaining computational trust boundary is the independent unformalized
decoder, CPython exact integer/rational arithmetic, SHA-256, and ordinary
hardware.

The result is reproducible and ready as a campaign checkpoint, but it is not
publication-ready evidence for \(R(5,5)\ge44\). Its value is diagnostic: it
shows precisely why selector exclusions alone cannot close the relaxation.

## Strengthening and improvement opportunities

The highest-value next step is to decide the complete P4 system with the nine
cuts and all 83 anchor equations. Before attempting a full solve, the authors
could search for a minimal or low-rank subset of the 83 equations that already
eliminates all analogous symmetric moment families, or add the 53 common
post-cut units as a cheaper intermediate system. Those are proposed next
experiments, not consequences proved by this review. Any future infeasibility
claim should retain an independently checkable proof certificate and state
whether it uses only the anchor interface or further root-polytope structure.

## Literature checked

- V. Chvátal, *Edmonds polytopes and a hierarchy of combinatorial problems*,
  Discrete Mathematics 4 (1973), 305--337,
  [DOI](https://doi.org/10.1016/0012-365X(73)90167-2).
- E. Balas, *Disjunctive Programming*, Annals of Discrete Mathematics 5
  (1979), 3--51,
  [DOI](https://doi.org/10.1016/S0167-5060(08)70342-X).
- V. Angeltveit and B. D. McKay, *R(5,5) <= 46*,
  [arXiv:2409.15709](https://arxiv.org/abs/2409.15709).
