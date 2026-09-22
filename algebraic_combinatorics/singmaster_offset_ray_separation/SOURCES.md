# Sources and literature-status check

Checked 2026-09-22 UTC.

## Primary sources

1. Hacene Belbachir and Laszlo Szalay, *Unimodal Rays in the Ordinary and
   Generalized Pascal Triangles*, **Journal of Integer Sequences 11** (2008),
   Article 08.2.4.
   <https://cs.uwaterloo.ca/journals/JIS/VOL11/Szalay/szalay8.html>

   Their Theorem 4 proves log-concavity of the binomial coefficients on every
   Pascal ray, and Corollary 5 gives unimodality.  The paper does not state
   strict log-concavity for the inward direction used here or formulate the
   proportional fixed-offset-curve separation corollary.  The present proof
   therefore treats their ray theorem as prior art rather than claiming
   general ray log-concavity.

2. Hacene Belbachir and Laszlo Szalay, *Unimodal Rays in the Regular and
   Generalized Pascal Pyramids*, **Electronic Journal of Combinatorics 18**
   (2011), Paper P79.
   <https://www.combinatorics.org/ojs/index.php/eljc/article/view/v18i1p79>

   This extends the ray framework to multinomial Pascal pyramids and recalls
   the ordinary-ray log-concavity theorem.  It does not supply the
   fixed-offset intersection statement proved here.

3. Hugo Jenkins, *Repeated Binomial Coefficients and High-Degree Curves*,
   **Integers 16** (2016), A69; arXiv:1411.4111.
   <https://arxiv.org/abs/1411.4111>

   Jenkins studies `binom(x,y)=binom(x-a,y+b)`, proves finiteness when
   `a!=b`, and explains why bounding common intersections of these curves
   bears on Singmaster's conjecture.  Equal offsets remain outside that
   finiteness theorem.  The present result separates all curves on each
   positive offset ray but does not address nonproportional intersections.

4. Kaisa Matomaki, Maksym Radziwill, Xuancheng Shao, Terence Tao, and Joni
   Teravainen, *Singmaster's conjecture in the interior of Pascal's triangle*,
   **Quarterly Journal of Mathematics 73** (2022), 1137--1177;
   arXiv:2106.03335. <https://arxiv.org/abs/2106.03335>

   This proves bounded multiplicity in a large interior region and records
   the continuing global status.  It does not state a fixed-offset-ray
   separation result.

## Search boundary

Targeted searches used the exact forms `binom(x-ar,y+br)`,
`binom(n-ak,m+bk)`, and `binom(x,y)=binom(x-a,y+b)`, together with the terms
"Pascal ray", "strict log-concavity", "equal offset", "proportional
offset", and Jenkins's exact title.  They located the two Belbachir--Szalay
ray papers, Jenkins, and the 2022 interior theorem.  No primary source found
in that search stated the strict inward-ray theorem together with the
proportional-curve disjointness/sign conclusion.  This is bounded,
search-relative evidence, not an exclusive historical-priority claim.
