Primary-source audit, 11 September 2026. The result proved here is the
exact value g(C3 ⊕ C18)=21. The known lower bound, the complement trick,
and general SAT proof technology are prior work; no novelty is claimed
for them.

- Guillot, Marchan, Ordaz, Schmid and Zerdoum, *On the Harborth constant
  of C3 ⊕ C3p*, Journal de théorie des nombres de Bordeaux 31(3) (2019),
  613–633. [Journal page](https://doi.org/10.5802/jtnb.1097),
  [primary PDF](https://www.numdam.org/article/JTNB_2019__31_3_613_0.pdf).
  Lemma 2.5 is the complement identity; Lemmas 3.2–3.3 give the lower
  construction. Theorem 3.1 treats prime p, including the exceptional
  g(C3 ⊕ C9)=13. Proposition 4.1 gives g(C3 ⊕ C12)=15. The last
  discussion suggests a composite extension, but supplies no n=6 proof.
- The [2018 arXiv version](https://arxiv.org/abs/1808.00722) has C3 ⊕ C3n
  in its title, but its theorem still restricts n to primes. A title
  match alone must not be read as settlement for all composite n.
- Zerdoum's [2021 doctoral thesis](https://pro.univ-lille.fr/fileadmin/user_upload/pages_pros/gautami_bhowmik/Encadrements/Participation/Zerdoum.pdf),
  Chapter III, retains the prime and n=4 results. The
  [authors' code](https://github.com/Zerdoum/Harborth_constant) had head
  `2b7452d9c642ccc82444395c53cf1120171c25c8`, latest reported push
  13 May 2019, when audited. No subsequent C3 ⊕ C18 result was found there.
- Schmid, *Restricted inverse zero-sum problems in groups of rank two*,
  [author manuscript](https://www.math.univ-paris13.fr/~schmid/personal/schmid_31t.pdf),
  [arXiv:1007.0257](https://arxiv.org/abs/1007.0257). Corollary 3.2(2)
  and Theorem 4.1 give the conservative pre-research upper bound 38 by
  specializing to m=3,n=6. That direct specialization is not our result.
- Further checked related primary work includes the
  [2013 rank-two/weighted Harborth paper](https://arxiv.org/abs/1308.3315),
  [2021 barycentric Olson paper](https://doi.org/10.15517/rmta.v28i1.33773),
  [2022 fixed-k variant](https://arxiv.org/abs/2209.14784), and
  [2026 zero-sum triple-partition paper](https://arxiv.org/abs/2606.13764v1).
  Their stated invariants or exact parameter families do not settle this
  exponent-18 distinct-subset instance.
- General restricted-sumset results were checked during the mathematical
  pass. Bajnok–Edwards,
  [*On two questions about restricted sumsets in finite abelian groups*](https://arxiv.org/abs/1607.05718),
  Theorem 2, requires h≥(|G|+|G[2]|)/2−1. Here that threshold is 27,
  so it does not apply at h=18. Chen–Huang,
  [arXiv:2602.10402v1, Lemma 3](https://arxiv.org/html/2602.10402v1),
  quotes the numerical form of Lev's restricted-triple theorem with
  |G|≥312|G[2]|+923. For this group |G[2]|=2 and the required order is
  at least 1547, not 54. Its Theorem A also requires much larger groups
  and subset density above one half. These theorems cannot be applied
  to assert the present endpoint. The original Lev author link exposes a
  DVI file; the explicit numerical form above was read in the cited
  Chen–Huang primary manuscript, not inferred from an abstract.

Targeted exact-parameter and family searches found no later exact value.
The conclusion is that 21 is **new to the searched primary sources**;
there is no claim of exhaustive knowledge of unpublished or concurrent
work. The computational theorem and reproducible certificates stand
independently of that novelty assessment.

Proof infrastructure:

- [Kissat release 4.0.4](https://github.com/arminbiere/kissat/releases/tag/rel-4.0.4),
  upstream tag commit `8af8e56f174b778aef3aa45af9f739b2a5f492c2`.
- [DRAT-trim](https://github.com/marijnheule/drat-trim), pinned commit
  `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

The solver is used to discover refutations. The independent checker
validates those refutations against the generated CNFs. Correctness of
the generator and its link to the theorem is established by the written
reduction, code inspection and semantic controls, not by solver agreement.
