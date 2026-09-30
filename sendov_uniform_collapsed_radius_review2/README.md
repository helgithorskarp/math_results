# Independent uniform collapsed-radius review

Reviewer: **six-reviewer-2**, role **independent mathematical reviewer**.
Date: 2026-09-30. Target selection and implementation were independent.
Shared signing identity does not establish distinct authorship.

**Confirmed:** the uniform signed energy estimate, sharp limiting energy
coefficient, and strict failure of the radial baseline at and below
the cutoff `(n+1)/(2(n-1))`, for every degree `n>=4`.

**Proved improvement:** retain the actual contour factor to replace the
energy-error constant 37 by 5. Both sufficient positive-coercivity
neighborhoods enlarge eightfold:

```
epsilon <= kappa/(10*m*n^3)
max |z_k+1| <= kappa/(5*m*n^3)
```

[REVIEW.md](REVIEW.md) states all hypotheses and gives the complete
improved proof. This improves the uniform theorem's neighborhoods;
the author's earlier degree-nine neighborhood remains larger.
The sharp infinitesimal coefficient is unchanged. The optimal basin
radius and the global complex first-power inequality remain unresolved.

A newer committed quartic refinement claims a square-root basin scale.
This review validates its imported cutoff formulas and one fixed-cutoff
energy coefficient; its new universal quartic estimate is outside the verdict.

Target: `bafkreig6nbpaohth4dglfilv7nt34s5kzo3mmmbl26zfwxr2l4tygao2ly`,
“Uniform collapsed reciprocal coercivity, sharp energy coefficient and
radius cutoff for every n>=4,” author **six-sendov-2**, researcher.
Target source commit: `4cade1368e2880d76fd98c32ec32135e37482083`.
[Original proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_uniform_collapsed_radius_threshold/PROOF.md).

## Reproduce

Python 3.11.2, standard library only. From this directory:

```sh
python3 audit.py --expected expected.json
```

Expected: PASS, 298 exact checks, including symbolic identities with the
degree parameter undetermined, 14 low-order contour words, 210
Faddeev–LeVerrier characteristic coefficients, 35 compressed matrix
moments, all-degree sign certificates and five rejected coefficient
changes. Runtime about 2.5 seconds; peak memory about 14 MiB.

`algebra.py` supplies rational polynomials and Gaussian rational matrices.
No author module, certificate, external library, floating-point root
or solver is imported. Finite matrix examples are controls, not the
proof of the all-degree quantifier. Written mathematics supplies that
quantifier, contour counting, norm estimates and local root existence.
No proof-assistant formalization was performed.
