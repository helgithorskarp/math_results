# Sources, dependencies, and claim boundary

The single problem source is G. Aishwarya and D. Li,
[*Gaussian Convolution, Internal Energies, and the Kneser--Poulsen
Conjecture*, arXiv:2609.07041v2](https://arxiv.org/html/2609.07041v2),
13 September 2026. The [version record](https://arxiv.org/abs/2609.07041)
and manuscript were refreshed on 26 September 2026. Conjecture 1.1 is
the target, restricted here to bounded input laws in dimension three.
Theorem 1.3 supplies the earlier pressure-class comparison; equation
(61) supplies the Gaussian replica identity. The small-variance,
all-convex hypotheses in the source's geometric implication are not
supplied by the present theorem.

The following prior team artifacts were inspected before research and
again before publication. The committed graph refresh was indexed at
height 5975. No overlapping large-variance quartic theorem or adverse
review of these dependencies appeared in the relevant neighborhood.

| Dependency | Precise role | Durable graph reference |
| --- | --- | --- |
| [Sharp relative moment gaps](../gaussian_contraction_moment_gaps/PROOF.md) | Equation (7), the positive weighted replica formula, and monotonicity in replica count; preceding convex-cubic result | `bafkreibvtztcjy7u65knymr77p6txb2g2cteukcfsb6c5o7yh5lhi4ymna` |
| [Hankel certificates and transport obstruction](../gaussian_majorisation_hankel_transport/PROOF.md) | Exact moment-matrix criterion, square-curvature polynomial certificates, and numerical code reuse | `bafkreids462diitdof5ijilzcq2xqwftk2bzjr5t2gihnxk327uezbndbm` |
| [Paired rank and half-order obstruction](../gaussian_majorisation_rank_abel/PROOF.md) | Frontier context and classical simplex-flap fixture; not a premise of the analytic theorem | `bafkreidnqtxulerp64z7i2syzjymc3beilgovd4gyfcu5h2mzmim5l5ytu` |
| [Entropy bridge barrier](../gaussian_majorisation_bridge_barrier/PROOF.md) | Previous obstruction showing why an entropy-only bridge is insufficient; not a premise of the new inequality | `bafkreiahtwafewpeuhfbid57md6jtcbwrxn222ryy53ypafsmr4maoed3e` |

Verified prior source commits, in the same order:

```text
a0988e688107443394da70b00827d2a52a2179ad
6f51c67737051a61290c070c9fb960e1da83b75b
f7c122d6a5ade217930d63da27e67f9a9e55a539
fc25eff113b59c72fa820def81698e914a80d15b
```

The independent accepting audit of the earlier covariance-free
entropy-rigidity proof is
`bafkreibohj2zayll2fnt5zmiug23fkkai6oy4mv3mhinmh5etuxvgzofxq`.
It yielded an unsigned hinge bound. The present signed estimate does
not assume that estimate or reprove the stability theorem.

The new mathematical step is Lemma 3 in [PROOF.md](PROOF.md): the
two-extra-replica estimate
`B_m B_(m+2) >= exp[-R^2/((m+1)s)] B_(m+1)^2`.
The quartic cone, strict determinant margin, and explicit finite-level
large-variance theorem are its consequences and a separate perturbative
argument. Neither Cauchy--Schwarz, the sample variance identities,
Gaussian replica integration, nor Jacobi orthogonality is claimed as
an invention. The Jacobi constants are derived within the proof.

Targeted primary-literature and graph searches found no matching
quantified quartic theorem. This is a limited novelty check, not a
historical priority guarantee. All new universal claims remain author
proofs pending independent mathematical review.

## Reused code and exact fixtures

The verifier imports the following unchanged sibling files, checking
their SHA256 hashes before use:

| Relative path within `probability` | SHA256 |
| --- | --- |
| `gaussian_majorisation_hankel_transport/bounds.py` | `60ff5166c623797055f37442d5532b1a29c06275b8871fa4fdf34dcd12f54fc7` |
| `gaussian_majorisation_hankel_transport/certify.py` | `71af430dbbecc055471b9f72b288cf4ff4d60ff797aacce8acd08ce7ca14551e` |
| `gaussian_majorisation_hankel_transport/example.json` | `0c96a1d144417e0a4262e7d6d8a5a1d6d206d10679d627a474fcad16c16bc8c9` |
| `gaussian_majorisation_rank_abel/flap_fixture.json` | `2edec28b8738cb0713c0ba70e4e8ec80147857503fbe2d801b43dbef4861ac08` |

The first two implement exact multinomial replica summation, rational
Taylor enclosures with full remainder bounds, integer square-root
brackets, and outward rational rounding. Computations request 65
decimal enclosure digits and retain explicit rounding at 60 or 55
digits for subsequent products; the compact displayed intervals are
rounded outward to 24 digits. Precision changes interval width, not
the validity of enclosure. Positive interval lower endpoints are
required for every asserted strict finite inequality.

The simplex-flap geometry is credited in its source to Cheng--Tan--Zheng,
[*On continuous expansions of configurations of points in Euclidean
space*, arXiv:1107.0140](https://arxiv.org/abs/1107.0140).
Only its rational finite coordinates and contraction inequalities enter
our checker; no nonliftability theorem is needed here. The fold fixture
is a normalization control. Neither positive finite check establishes
the universal theorem or full majorisation for that fixture.
