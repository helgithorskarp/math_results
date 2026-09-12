# Literature and claim boundaries

Primary sources checked on 12 September 2026. A search finding no match is
evidence relative to these sources, not a definitive priority clearance.

## Selected question

I. Beaton and B. Cameron, *Vertex-critical graphs in co-gem-free graphs*,
Theoretical Computer Science 1042 (2025), 115234,
[journal](https://doi.org/10.1016/j.tcs.2025.115234),
[author manuscript v2](https://arxiv.org/html/2408.05027v2).
Section 7 asks which five-vertex H yield finiteness of critical co-gem/H-free
graphs for every chromatic number. Its following paragraph suggests bull and
reports equality with the P3+P1-free critical class through k=6.

The all-k equality studied here is our precise extension of that reported
pattern, not the paper's numbered Conjecture 7.1. The k<=6 computation is
imported as a frontier report and is not a premise of our new theorem.

## Inputs and prior results

- T. Karthick, F. Maffray and L. Pastor, *Polynomial Cases for the Vertex
  Coloring Problem*, Algorithmica 81 (2019), 1053–1074,
  [author manuscript v2](https://arxiv.org/pdf/1709.07712v2),
  [journal](https://doi.org/10.1007/s00453-018-0457-y).
  Theorem 5.2 supplies the prime house/bull structural dichotomy; Theorem 4.2
  supplies an analogous house/hammer result. Their complements give the
  hypotheses used in our abstract theorem. The downloaded author PDF has
  SHA-256 `47324bdf900cbccee9a5b068a85adb9a49fc8f0cc3517b6fc442cfee23d3b774`.
- M. Belavadi and C. T. Hoàng, *Structural description of (bull, house)-free
  graphs*, [2026 primary preprint](https://arxiv.org/html/2604.27594v1).
  Theorem 1.2 proves finiteness for critical P5/bull-free graphs for all k.
  Corollary 2.8 gives a stronger prime dichotomy. Section 3 records modular
  decomposition and the critical clique-skeleton reduction. These are prior
  inputs, not new claims. The older KMP theorem suffices for our proof.
- I. Beaton and B. Cameron, *Vertex-critical graphs in subfamilies of
  (P4+ell P1)-free graphs*,
  [2026 primary manuscript](https://arxiv.org/html/2604.06999v1).
  Corollary 3 proves finiteness for all k,ell in the same P5/bull family.
  Our contribution strengthens this to an exact independence-number
  characterization, a sharp bound on that number, and an explicit order bound
  linear in k.
- B. Cameron, C. T. Hoàng and J. Sawada, *Dichotomizing k-vertex-critical
  H-free graphs for H of order four*, Discrete Applied Mathematics 312 (2022),
  106–115, [author PDF](https://www.cis.uoguelph.ca/~sawada/papers/kcritical.pdf).
  Theorem 3.1 gives alpha<=2 and order<=2k-1 for the known P3+P1-free critical
  class. The k=7 census in that paper is prior art and has not been regenerated.
- C. Brause, M. Geißer and I. Schiermeyer, *Homogeneous sets, clique-separators,
  critical graphs, and optimal chi-binding functions*, Discrete Applied
  Mathematics 320 (2022), 211–222,
  [author manuscript v3](https://arxiv.org/pdf/2005.02250v3).
  Theorem 3(i) already gives alpha<=2 for every critical P5/banner-free graph.
  Consequently the banner application in our proof is illustrative, not a
  novelty claim or a numerical improvement.

The general critical-substitution operation used for sharpness is standard.
We supply an explicit pair-palette proof for our exact recursion and use the
family to establish attainment of the new independence bound; we make no
priority claim for the operation itself.

## What is proved and what is open

The new deduction is the exact identity between independence number and the
largest independent set anticomplete to an induced P4, under the abstract
prime-graph hypothesis. This is a short structural corollary of established
decomposition theory; its novelty should be judged accordingly. We found no
statement of this identity or its full sharp bull-family consequence in the
primary sources searched.

At ell=1, it decides the entire **P5-free** co-gem/bull critical class for
every k. It does not exclude P5 in the unrestricted co-gem/bull class. It does
prove that such an exclusion would now imply the exact selected equality,
with no additional D-free classification step. No finite cap on a
P5-containing candidate follows from the theorem.

The graph/repository audit found no overlapping co-gem/bull contribution.
Finite controls are supplied for checking examples and definitions, not as a
substitute for the proof or as independent peer review.
