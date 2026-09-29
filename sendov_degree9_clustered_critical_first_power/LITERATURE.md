# Literature, dependencies, and status

Agent: **six-sendov-2**, researcher. Primary sources checked 2026-09-29.

The assigned degree-nine Sendov existence assertion is covered by the
August 2026 all-degree proof reported in
[Tao's primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
and the quantified theorem statements in the
[teorth/sendov source repository](https://github.com/teorth/sendov/blob/master/README.md).
I inspected the statements and reported axiom audit; I did not rebuild the
external Lean development. This is the reason for working on a stronger
nearby endpoint within the assigned family.

[Zhang, arXiv:2609.19126](https://arxiv.org/html/2609.19126) proves the
reciprocal-square Tang–Zhang inequality at every root and explicitly
retains the first-power inequality as a conjectural endpoint. The
reciprocal-square result does not imply the first-power result by
Cauchy–Schwarz. The current artifact proves a local degree-nine
first-power case, including strictness at interior roots, and derives
a uniform boundary annulus by combining it with a teammate result.

[Tang–Zhang, arXiv:2508.10341v3](https://arxiv.org/html/2508.10341v3),
equation (5.1) and Remark 5.1, supplies the classical boundary reciprocal
machinery used in the preceding stability and analytic work. The Schur
coefficient transform, coefficient integration, Taylor theorem, and
elementary symmetric pair bound in the present proof are standard
tools and are not claimed as new.

Earlier local results address the existence of a nearby critical point:
[McCoy's 1998 paper](https://www.tandfonline.com/doi/abs/10.1080/17476939808815077)
states a neighborhood result around `z^n-1` for the original Sendov
assertion. Only its accessible abstract was inspected. A bounded search
also located
[Kasmalkar's 2014 article](https://ajmaa.org/searchroot/files/pdf/v11n1/v11i1p4.pdf),
whose inspected abstract states an explicit polynomial-order annulus for
the original assertion. The present first-power failure hypothesis
allows individual reciprocal terms to exceed one. No priority claim is
made; the stronger local first-power statement was not located in the
primary sources searched.

## Team dependencies

1. [six-sendov-1, first-power polar concentration](https://github.com/helgithorskarp/math_results/tree/728857924504f28020dea5de6590ae3458b7bc90/sendov_degree9_first_power_polar),
   source commit `728857924504f28020dea5de6590ae3458b7bc90`, proof sections
   6-7. This supplies the conditional concentration statement used for
   the annulus corollary. Its central-disk case and boundary equality
   classification are also cited context. Discovery Net lemma:
   `bafkreideaathnoyujdk5pmy4d3qmhu45tyevkegmjmtgmwyvoq2b2pjnue`.
2. [six-sendov-2, degree-nine boundary stability](https://github.com/helgithorskarp/math_results/tree/541c9ff17d23f64f4af9c01c4a49b0fc46bbee8a/sendov_degree9_boundary_stability),
   source commit `541c9ff17d23f64f4af9c01c4a49b0fc46bbee8a`. Its Schur
   lemma and pair-counting coefficient estimates are reproduced
   self-contained in the present proof. Discovery Net lemma:
   `bafkreidafhsoczpgya4mphmniblfg7kx2n4buyfth76mwurmoolpwnoo64`.

The local theorem is independent of the analytic concentration result.
The annulus corollary depends on it. No independent specialist review
or formalization is claimed for either team's ordinary proof.

## The 2017 degree-nine claim

[Meng, arXiv:1705.07235](https://arxiv.org/abs/1705.07235), last arXiv
revision v3 in 2018, continues to state a degree-nine proof claim and
has no journal reference on the inspected arXiv page. The historical
`n<=8` statement in [the supplied later seed](https://arxiv.org/html/2609.20256)
is a status discrepancy, not a refutation of Meng's proof. This bounded
audit did not locate primary evidence settling the acceptance or rejection
of that older claim. No verdict about its correctness is inferred.

## Remaining frontier

The degree-nine first-power conjecture at arbitrary root moduli is not
resolved here. An explicit annulus width, a quantitative concentration
bound, and the gap between that annulus and the analytic central disk
remain concrete frontiers. The source includes compact rational checks,
not exhaustive enumeration or a solver nonexistence claim.
