# Primary literature and claim boundary

Checked 11–12 September 2026, including a live recheck during the
mathematical pass on 12 September.

**Stijn Cambie, Jun Gao, Younjin Kim and Hong Liu**, *The Erdős distinct
subset sums problem in a modular setting*, Acta Arithmetica **217**
(2025), 295–307.

- [Publisher/DOI](https://doi.org/10.4064/aa231107-13-9).
- [Open manuscript, arXiv:2308.03748v1](https://arxiv.org/abs/2308.03748),
  7 August 2023; the arXiv record lists only this version.
- [Author's publication list](https://jungao0211.github.io/).
- [Author's computational repository](https://github.com/StijnCambie/ErdosSumSet),
  inspected at commit `ab4e935712db698dfbd1fedeaad81e3c23c150ea`.
  Its two scripts support Appendix B rather than a classification at
  excess five.

The full open manuscript was read. The publisher confirms online
publication on 6 February 2025, but a journal-PDF download redirected to
a home page; the journal typesetting was not compared. The specific
structural/open statements below are attributed to the author manuscript.

Theorems 1.4–1.7 classify maximal sum-distinct sets modulo 2^n+t for
0 <= t <= 3. Lemmas 2.1–2.2 discuss unit dilation and sign changes.
Lemma 5.2 already shows that, for odd excess, the missing subset sums
consist of the center and opposite pairs. Section 7 asks for an eventual
perturbation classification and for O_t(N^(2+v_2(t))) sets. The
introduction states an O(N^((3+t)/2)) estimate for odd t, giving O(N^4)
at excess five.

Proposition A.1 supplies the perturbation constructions. At t=5 its
three types are exactly B0, B1 and B2 in this package. Appendix A says
that the indicated examples appear exhaustive for t=5,7; no necessity
proof there is supplied. Their existence and the symmetry of missing
sums are therefore not claimed as new results here.

This package proves necessity for every set containing a signed unit
doubling chain of length n-2, uniformly for n >= 5, and counts that
entire subclass. It also gives unrestricted divisor and path constraints.
It does not force such a chain in every set. The complete n=5,6
censuses are exact controls; no standalone novelty is claimed for those
small computations.

Searches by the exact title, author names, “sumset-distinct”,
“classification”, “five”, “doubling chain” and 2^n+5 found no primary
source settling the adopted unrestricted classification or stating
this complete conditional case. This is search-relative evidence,
not a priority guarantee. The result is an elementary extension of the
published constructions and is presented as progress toward the
unrestricted problem, not its solution.

The reconstruction theorem of Glaudo and Kravitz,
*Reconstructing a Set from its Subset Sums: 2-Torsion-Free Groups*,
Discrete Analysis 2024:14,
[DOI](https://doi.org/10.19086/da.125856),
[arXiv:2305.11062v2](https://arxiv.org/abs/2305.11062),
includes moves arising from embedded odd cyclic subgroups. None of its
uniqueness claims or reconstruction machinery is needed for this proof.
