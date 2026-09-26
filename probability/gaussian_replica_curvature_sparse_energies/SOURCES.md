# Sources and dependency boundaries

The sole problem source is G. Aishwarya and D. Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
Conjecture*, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2),
13 September 2026. The source was refreshed live on 26 September 2026.
Conjecture 1.1 is the campaign target, restricted to bounded measures in
dimension three. The replica identity, pressure classes, and known
continuous-contraction cases are credited to prior literature.

The two-extra-replica identity was already used in the preceding team
result. The new step here is to average its correction under the
conditionally tilted extra-replica law and then use Jensen. This gives
the optimal `1/12` loss for `B_2 B_4/B_3^2`, all-degree log-convexity of
the normalized gaps at a fixed variance bound, and the sparse-curvature
comparison. Cauchy--Schwarz, Jensen, and the elementary three-moment
representation are not claimed as inventions. Novelty is relative to
the checked primary sources and graph; no historical priority is claimed.

## Mathematical dependencies

| Artifact | Use | Committed graph reference |
| --- | --- | --- |
| [Relative Gaussian moment gaps](../gaussian_contraction_moment_gaps/PROOF.md) | Positive replica formula and monotonicity; preceding two-power and prefix cones | `bafkreibvtztcjy7u65knymr77p6txb2g2cteukcfsb6c5o7yh5lhi4ymna` |
| [High-variance quartics](../gaussian_contraction_high_noise_quartics/PROOF.md) | Two-extra-replica identity and the earlier pointwise radius bound | `bafkreig737fhqpda2iz657ruh6clkymbesvt2a53sw4suywpqb7obwgkay` |
| [Exact Hankel criterion](../gaussian_majorisation_hankel_transport/PROOF.md) | Interpretation of the remaining full hierarchy and finite polynomial witnesses | `bafkreids462diitdof5ijilzcq2xqwftk2bzjr5t2gihnxk327uezbndbm` |

Their verified source commits, respectively:

```text
a0988e688107443394da70b00827d2a52a2179ad
a68f3a7c2d3e1c2141d43d2ea00eca76635ba964
6f51c67737051a61290c070c9fb960e1da83b75b
```

## Current complementary work

Bounded new reports, commits, and relevant graph neighborhoods were
inspected at pass start and before publication. The latter refresh was
indexed at height 5987. The following new work was incorporated as
context, not as a premise of the proof:

- [Instantaneous-lift obstruction](../gaussian_majorisation_local_lift_obstruction/PROOF.md),
  graph `bafkreifseyjs3jimzu7yvo3lpfd3555dmnf5q6hraqdonaldti3nqjgxqy`,
  source `c363e6b2e9db8cdb18b7a6ad787446f305712e92`. This eliminates the
  unrestricted pointwise Hankel route, even for a very strict contraction.
  Its input radius is extremely large relative to the noise, so it does
  not conflict with the radius-controlled result here. Our exploratory
  pointwise branch was closed when this durable result appeared.
- [Symmetric-flap quartics at every scale](../gaussian_symmetric_flap_quartics/PROOF.md),
  graph `bafkreiak3mcoxvlus3otfu53wv2dcu3mdv7vunj32x7hwf4am5jg6kw2he`,
  source `3ac0aff4d05f62405c5a36ee6b039ab002957fad`. That theorem has no
  variance restriction but concerns one symmetric geometric family.
- [Small-mass hinge comparison](../gaussian_majorisation_small_mass/PROOF.md),
  graph `bafkreihtnp3ptickdr4nhikxkarcr3v4uwocvhde5lcj3mx2fhmk7b7jge`,
  source `5f0f1852d71dc61b7edfa1871cbc6a06673a4c27`. That theorem holds
  variance fixed and controls a window of thresholds as moved mass vanishes.

The earlier covariance-free rigidity result was independently audited in
the preceding functional-bridge pass. Its unsigned stability conclusion
is not assumed to supply any sign here. The present sharpness example
uses actual bounded contraction pairs, unlike the earlier obstruction
for arbitrary entropy-ordered densities.

## Reused numerical source

The exact checker pins these unchanged files before use:

| Relative path within `probability` | SHA256 |
| --- | --- |
| `gaussian_majorisation_hankel_transport/bounds.py` | `60ff5166c623797055f37442d5532b1a29c06275b8871fa4fdf34dcd12f54fc7` |
| `gaussian_majorisation_hankel_transport/certify.py` | `71af430dbbecc055471b9f72b288cf4ff4d60ff797aacce8acd08ce7ca14551e` |
| `gaussian_majorisation_hankel_transport/example.json` | `0c96a1d144417e0a4262e7d6d8a5a1d6d206d10679d627a474fcad16c16bc8c9` |
| `gaussian_majorisation_rank_abel/flap_fixture.json` | `2edec28b8738cb0713c0ba70e4e8ec80147857503fbe2d801b43dbef4861ac08` |

The last fixture originates in the paired-rank package, source commit
`f7c122d6a5ade217930d63da27e67f9a9e55a539`, graph
`bafkreidnqtxulerp64z7i2syzjymc3beilgovd4gyfcu5h2mzmim5l5ytu`.
Its classical simplex-flap construction is credited there to
Cheng--Tan--Zheng. Only its rational coordinates and distances are used
in this checker; no nonliftability theorem is required.

All enclosure calculations use rational arithmetic and outward rounding.
Exponential and square-root requests use 70 or 75 decimal digits, with
subsequent products retained at 65 or 60 digits where indicated. Displayed
intervals are rounded outward to 24 or 30 digits. A strict finite sign is
accepted only if the entire enclosure has that sign. The numerical code
is reused with attribution, not represented as independently implemented.
The infinite ranges and optimality quantifier follow from PROOF.md, not
from numerical scans or the single finite `1/13` witness.
