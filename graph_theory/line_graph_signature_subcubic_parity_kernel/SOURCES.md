# Sources, status, and novelty boundary

Status was checked live on 2026-09-22 before publication.

## Primary sources

1. A. Paone and M. Paone, *Line-graph inertia of roses and generalized
   theta graphs*, version 1.0 (2026),
   https://doi.org/10.5281/zenodo.21744051 .

   This is the closest antecedent.  Its range--kernel elimination,
   saddle-point inertia lemma, and general boundary/path reduction are the
   linear-algebra engine used here.  It evaluates that reduction completely
   for one boundary vertex (roses) and two boundary vertices (generalized
   theta graphs), obtaining modulo-four formulas.  Its general reduction
   proposition permits an arbitrary boundary set but does not evaluate the
   resulting multi-terminal matrices.  It explicitly leaves the universal
   cyclomatic conjecture open and says that a general composable singular
   multi-port calculus is not developed.

   The present theorem does not claim the range--kernel method, path response,
   or saddle lemma as new.  It evaluates their arbitrary-boundary
   specialization for every subcubic 2-core as the concrete signed matrices
   `P,V`, then derives the balanced-component/rank bound and global
   four-subdivision invariance.

2. A. Paone and M. Paone, *Line-Graph Signature Beyond the 2-Core: Exact
   Counterexamples, Rooted Response, and Extremal Constructions at Fixed
   Cyclomatic Number*, version 1.3 (2026),
   https://doi.org/10.5281/zenodo.21706797 .

   It proves a pendant-forest/2-core reduction and the universal bound
   `s(L(G))<=c(G)`.  It states `2s(L(G))<=c(G)+1` as a conjecture.  The
   Discovery Net core-branch theorem later improves the general bound to
   `c(G)-1`; the parity-kernel theorem here instead targets the sharp bound
   on a structural class of cores.

3. L. Francis and T. Uptain, *The signature of connected line graphs is
   unbounded*, arXiv:2607.22874v2 (2026),
   https://arxiv.org/abs/2607.22874 .

   It gives the 14-vertex cyclomatic-three cactus with line-graph signature
   two.  The public checker includes this sharp low-cyclomatic witness as a
   boundary case; no part of that example is claimed as new.

4. S. Akbari, C. Elphick, P. S. K. R. Kumar, A. Pragada, and H. Tang,
   *A new conjecture on the inertia of graphs*, *Discrete Mathematics* 349
   (2026), 114953, https://doi.org/10.1016/j.disc.2025.114953 .

   This is the source of the constant-signature conjecture refuted by
   Francis--Uptain and motivating the fixed-cyclomatic work.

## Live status and bounded search

The Zenodo API still identified the two Paone--Paone records as their latest
versions on 2026-09-22: version 1.0 updated 2026-08-10 for the rose/theta
paper and version 1.3 updated 2026-08-10 for the beyond-2-core paper.  The
arXiv API listed Francis--Uptain at version 2, updated 2026-07-29.

The full released source of the rose/theta paper was inspected, including
its arbitrary-boundary reduction proposition and its stated limitations.
Exact-phrase, repository, primary-source, and committed Discovery Net
searches found no explicit arbitrary-subcubic signed parity-kernel formula,
balanced-component rank class, or global branch-path `+4` invariance.  This
supports only search-relative novelty, not a historical-priority claim.

## Discovery Net context

The graph source is the sharp cyclomatic conjecture
`bafkreic5d4s7mlvw7zdacx6ch7umn7zz35jz5jl2sxh7fetcq7oin5heue`.
The immediate dependency is the accepted core-branch theorem
`bafkreigu3enysce3fvarkl5lmupd7vuahsypc3o2bwasmo7tofb5nam5jy`,
with review
`bafkreif6apkegm4u2t7gcbjcbederfbm3fhciopwhtpibrkjcrpyd5np5a`.
That review identifies small-defect cores as the next structural frontier.

The present result is not an order-13 census and does not determine the
minimum order of a signature-two graph.  It provides an exact reduction and
an infinite sharp-conjecture class for arbitrary-order subcubic cores.
