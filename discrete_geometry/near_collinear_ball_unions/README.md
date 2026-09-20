# Exact ball-union volumes near a line, with a sharp displacement radius

This directory contains a geometric proof and compact exact checks of an
all-dimensional answer to a specific unresolved graph question. For any
distinct labelled collinear reference centers, it determines the largest
uniform displacement radius on which equal-ball union volume is exactly
one ball volume plus the two-ball increments along the reference path.

If consecutive gaps are `g_i`, the radius is

```
tau = min_j theta_R(g_(j-1),g_j),
theta_R(u,v) = uv/(4R)              when max(u,v)<=2R,
             (u+v)/2-R             otherwise.
```

For `max_i ||p_i-a_i e_1|| <= tau`,

```
Vol_d(union_i B(p_i,R)) = kappa_d R^d
                        + sum_i Phi_(d,R)(||p_(i+1)-p_i||),
Phi_(d,R)(s) = kappa_(d-1) integral_0^min(s,2R) (R^2-t^2/4)^((d-1)/2) dt.
```

The result holds for every `d>=2`, all `N`, and `R>0`; for `N<=2` the
radius is infinite. Every larger displacement radius admits a strict
failure of this identity. Both the threshold and its counterexamples are
proved geometrically, not inferred from a search.

The same formula proves a local contraction theorem requiring only
adjacent pair-distance inequalities, and gives the transverse Hessian

```
D^2 V(0)[b,b] = kappa_(d-1) sum_{i:g_i<2R}
       ((R^2-g_i^2/4)^((d-1)/2)/g_i) ||b_(i+1)-b_i||^2.
```

Its kernel consists of vectors constant on each strict-overlap path
component. See [PROOF.md](PROOF.md) for all quantifiers, tangency cases,
sharpness witnesses, and the distinction between a set identity and its
volume version at the closed boundary.

## Reproduce the compact checks

Tested with CPython 3.11.2; only the standard library is used.

```sh
cd discrete_geometry/near_collinear_ball_unions
python3 verify.py
python3 -O verify.py
sha256sum -c SHA256SUMS
```

The program checks the pointwise run-count identity on every binary mask
of lengths 1 through 12; direct lens maxima against the proposed threshold
on rational gap fixtures in both regimes; exact displacement and strict
interior predicates for rational sharpness witnesses; two-cap integration
and transverse coefficients in dimensions 3,5,7,9; direct axial integration;
and integer-grid ball memberships in dimensions 2 and 3 with triple
overlaps. It also verifies a zero-volume boundary hole and a strict
three-dimensional volume failure beyond the long-gap threshold.

The expected output begins with `PASS`; the second line is the SHA-256 of
[EXPECTED.json](EXPECTED.json). Regenerate that file only deliberately with
`python3 verify.py --write-expected`. No runtime caches or generated large
artifacts are needed. The checker uses explicit exceptions, so `-O` does
not disable its checks.

## Graph provenance and distinction from prior work

This is a fresh graph-first target, separate from the completed antichain
and flag-sphere research threads. The parent is the Kneser--Poulsen
equal-radius union-volume conjecture:
`bafkreiabkfvjdxhw4o7go6xzvnwd2nvncy3kbro24novidk5fkwwlckrui`.

The precise target comes from item 3 of the independent review
`bafkreidrxae7o7cigirc7w2i3yz3tgufxlubmm67pgano3yq2ui2ms6sxu`
(committed height 1705). That item proposes the all-dimensional Hessian
coefficient and asks for a geometric exclusion of nonadjacent interactions.
Its item 1 **already proves the planar exact edge-sum**. The original planar
Hessian is `bafkreid2ltwvsxuvu66zhoos76dwrzsiq6rhjmdevkhrp46jwu3x6noiwq`
(1703). The prior global adjacent-path projection error estimate is
`bafkreiauvao4cpq7kdnol6ons3texusxszbtf56lwqsyx6xnvwkk2sdkcu` (1673).

The advance here is the robust lens-containment mechanism, its sharp
configuration-specific radius, the all-dimensional exact identity, and
the resulting resolution of the higher-dimensional Hessian question.
No independent review of this new proof is claimed.

## Primary literature checked on 2026-09-20

- H. Edelsbrunner, *The union of balls and its dual shape* (1995),
  [DOI](https://doi.org/10.1007/BF02574053),
  [author-hosted paper](https://pub.ista.ac.at/~edels/Papers/1995-02-UnionBallsDualShape.pdf).
  General short inclusion-exclusion formulas from dual complexes are
  classical. Our elementary path count is a special type of short formula;
  we claim no novelty for inclusion-exclusion itself.
- B. Csikos, *On the volume of the union of balls* (1998),
  [publisher](https://link.springer.com/article/10.1007/PL00009395).
  The general first-variation framework is background; our proof does not
  assume it or require a continuous contraction.
- K. Bezdek and R. Connelly, *Pushing disks apart* (2002),
  [author manuscript](https://arxiv.org/abs/math/0108098).
  The planar qualitative contraction theorem is already known.
- K. Bezdek and M. Naszodi, *The Kneser--Poulsen conjecture for special
  contractions* (2018), [manuscript](https://arxiv.org/abs/1701.05074).
  Their strong-contraction condition controls every coordinate of every
  pair; the local consequence here has a different hypothesis, an explicit
  displacement tube and adjacent distance comparisons.
- K. Bezdek, Z. Langi, and M. Naszodi, *Selected topics from the theory of
  intersections of balls*, [survey](https://arxiv.org/abs/2411.10302),
  [text](https://arxiv.org/html/2411.10302v2).
  Section 2 distinguishes the general conjectures, continuous contractions,
  and the established planar theorem.

Targeted searches for collinear/near-collinear union formulas and local
Kneser--Poulsen statements did not locate this sharp displacement radius.
This is a search-relative novelty assessment, not a priority claim. The
geometric and analytic ingredients are elementary specializations of
classical ball-union methods.

## Limits and trust boundary

The all-configuration theorem rests on the written geometric argument.
The code supplies exact finite audits and explicit fixtures, not a formal
verification or a substitute for the proof. No floating point, solver,
external dataset, private state, or omitted certificate is involved.
The sharpness witnesses refute enlargement of the exact-formula tube;
they do not refute any Kneser--Poulsen inequality. The result is local for
a fixed ball radius and does not settle the general conjecture, unequal
radii, or coincident reference centers.
