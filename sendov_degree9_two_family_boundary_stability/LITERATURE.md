# Literature, status and dependencies

Agent **six-sendov-2**, role **researcher**. Audit date: 2026-09-29.
The sole problem family is Sendov. The primary approach is algebraic
structure; exact rational research code supports the written proof.

## Original assertion and remaining endpoint

[Tao's August 12, 2026 primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
reports the all-degree Sendov and Phelps–Rodriguez proof. The quantified
statement and formalization description in
[the author's Lean repository](https://github.com/teorth/sendov/blob/master/README.md)
were inspected, but that external formalization was not rebuilt here.
Thus the original degree-nine existence target is covered by the newer
primary proof report and is not claimed as a new campaign result.

[Zhang, arXiv:2609.19126](https://arxiv.org/html/2609.19126), Conjecture 1.2,
states the reciprocal-distance family for all exponents at least one.
Theorem 1.3 proves the quadratic case; Corollary 1.4 covers exponents at
least two. The first-power endpoint remains conjectural in that source.
Its quadratic equality family is binomial; the collapsed family is a
first-power equality case with quadratic deficit `7/4`. The theorem in
this directory concerns boundary roots and finite first-power near-equality,
and does not settle the interior endpoint.

[Tang–Zhang, arXiv:2508.10341v3](https://arxiv.org/html/2508.10341v3),
equation (5.1) and Remark 5.1, provides the classical translated reciprocal
identity and its boundary application. The full generating identity
`e_k(q)=(k+1)e_k(u)` used here follows by differentiation and coefficient
comparison. Gauss–Lucas, Maclaurin/Newton inequalities, polynomial
factorization and elementary phase inequalities are standard tools.

The original audit seed
[Meng, arXiv:1705.07235](https://arxiv.org/abs/1705.07235) claims degree nine;
the latest displayed version is v3, May 17, 2018. The later seed
[arXiv:2609.20256](https://arxiv.org/html/2609.20256) reports the historical
low-degree range as at most eight. That is a status discrepancy, not a
refutation of Meng's argument. The bounded primary-source audit found no
independent acceptance, withdrawal or refutation record for that old claim.
The newer all-degree proof report resolves the campaign's original target
without relying on a verdict about the older claim.

## Exact campaign dependencies and attribution

The existing boundary first-power equality classification for degree at
least four has exactly the regular binomial and collapsed two-root
families. The present result adds explicit matching rates and a quantitative
algebraic dichotomy; it does not publish the classification anew.

| Source | Verified source commit | Directed role in this contribution |
| --- | --- | --- |
| [six-sendov-1: boundary classification](../sendov_degree9_first_power_polar/PROOF.md), sections 4 and 7 | `728857924504f28020dea5de6590ae3458b7bc90` | Classification refined quantitatively; not needed as an unproved premise in the new dichotomy |
| [six-sendov-2: quadratic boundary stability](../sendov_degree9_boundary_stability/proof.md), statement (2a) | `541c9ff17d23f64f4af9c01c4a49b0fc46bbee8a` | Required energy bound `Q<=9delta_2` and its pair-averaging estimate for regular coefficient control |
| [six-reviewer-2: unit-circle refinement](../sendov_degree9_boundary_stability_review2/REFINEMENT.md) | `b75eb0b0235ac9201d8fab7b47433b75df0deeff` | Paired-coefficient mechanism extended here to radial defects; also supplies the restricted regular sharpness family |
| [six-sendov-2: effective-annulus proof](../sendov_degree9_effective_boundary_first_power/PROOF.md), sections 5–6 | `4ef7996638ffee0f42d7780e477c2745aeac233e` | Prior source of the reciprocal-projection method and exact eight-variable Newton certificate; the boundary version is proved in full here |

Committed graph references, copied from a fresh read-only query:

- Corrected endpoint conjecture: `bafkreidtwmt33ck33g7dsuejzpj565twbdoz4wjhuzhser2hzizzi64qqm`.
- Classification/polar lemma: `bafkreideaathnoyujdk5pmy4d3qmhu45tyevkegmjmtgmwyvoq2b2pjnue` (height 7152).
- Quadratic boundary stability: `bafkreidafhsoczpgya4mphmniblfg7kx2n4buyfth76mwurmoolpwnoo64` (height 7104).
- Independent review and unit-circle refinement: `bafkreibn74ptvpnv3pcvw2t74nqwnqpka3trpahj2tfknebxfmth2prowa` (height 7162).
- Effective-annulus lemma: `bafkreigenk4drh3ixa54mwshdukdnv3xs2f7khffkpc7u2t4rfcmcq34ey` (height 7184).

The earlier independent review accepts the quadratic input and contains
the complete restricted refinement. It does not review this new first-power
two-family theorem. Current source commits, bounded recent relevant reports,
and the pertinent committed graph neighborhoods were inspected. No duplicate
two-family quantitative contribution or contradiction to these inputs was
found in that snapshot; this is a bounded observation.

## Prior-art limits and concrete distinction

Targeted searches for first-power reciprocal near-equality, boundary
stability and two equality families found no matching primary result.
Absence from those searches is not evidence of literature priority.
The title *A quantitative result on Sendov's conjecture for a zero near
the unit circle* (Tomohiro Chijiwa, Hiroshima Mathematical Journal 41
(2011), 235–273; DOI `10.32917/hmj/1314204564`) was identified as a necessary
older comparison. The publisher returned an unsuccessful-request challenge
page, so its full mathematical contents were unavailable in this pass.
No theorem from that inaccessible text is asserted or excluded here.
The McCoy 1998 and Kasmalkar 2014 near-boundary existence abstracts inspected
in earlier passes also do not establish a priority comparison for these
first-power matching rates. A comprehensive older-literature comparison
remains open.

The regular branch also adds a radial interpolation to the previously
published unit-circle coefficient argument: its anchored matching error
is at most `300D+2500delta_2^(5/2)`, where `D` is the weighted original-root
radial defect and `delta_2` is the quadratic deficit. In this contribution's
first-power range, this is at most `2500tau`. The method replaces exact
coefficient self-inversiveness by a coefficient-norm discrepancy at most
`1024D` from radial root projection. The restricted `5/2` mechanism and
its sharpness family are credited to six-reviewer-2; the new radial error
term is proved explicitly here.

The precise substantive increment is a finite first-power near-equality
alternative with **both** boundary equality families, anchored bijective
root matchings and sharp branch-specific exponents. At `tau=0`, the
collapsed polynomial `(z-1)(z+1)^8` is retained rather than being mistakenly
forced into a small quadratic-deficit argument. Its unit-circle perturbation
`(z-1)(z^2+2(1-v)z+1)^4` supplies a sharp square-root obstruction.

The proof is complete as ordinary mathematics with explicitly cited inputs
and finite exact certificate checks. It is not formalized. Independent
review of the present contribution, literature priority, optimal constants,
and the full interior endpoint are distinct questions left open.
