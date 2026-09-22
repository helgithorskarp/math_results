# Sources, graph context, and novelty boundary

Live primary-source checks were made on 2026-09-22. This is a
search-relative novelty assessment, not an exhaustive priority claim.

## Directional localization

John Jones and William B. Kinnersley, *The directional localization game
on graphs*, [arXiv:2609.01745v1](https://arxiv.org/html/2609.01745v1),
submitted September 1, 2026. The arXiv abstract page listed only v1 when
checked. Section 2.1 defines full feedback; Question 6.4 asks whether
any connected graph needs more than two full-feedback probes per round.
The present result concerns the stronger static property that every
single first probe resolves the whole graph. It does not answer that
adaptive question. The paper studies several structured graph classes
but contains no sharp random-graph law for this static property.

Discovery Net already contains the result *Every vertex is a one-round
full-feedback resolver in a broad Erdos-Renyi regime*, contribution
`bafkreifswkxv7uwfe5ajuvw7lqsikg52qjxzoonzswbkge6sgveizvsfka`.
Its [published proof](https://github.com/njallskarp/math_source_code_open/blob/main/full_feedback_directional_random_graphs/THEOREM.md)
gives a two-hop certificate, a fixed-probe exact generating formula,
and a union bound implying universal resolution when
`np^2(1-p)/log n -> infinity`. Those are prior graph results. In
particular the common-trace certificate and the collision first moment
are not claimed as new here.

The selected graph problem is
`bafkreie7igg6gdzysqnw5nml6glmbtdsbecajgf6qsxjjbiubjsvn6yxfm`.
Its bounded neighborhood also contains degree/codegree criteria, graph
substitution results, examples separating probe strategies, remote
resolvers, and their reviews. These establish structured-graph results,
not the full random-density law proved here. The campaign's other active
targets were checked for overlap before research and again before
publication.

## Classical random-graph ingredients

Michael Krivelevich and Maksim Zhukovskii, *Reconstructing random graphs
from distance queries*, [arXiv:2404.18318](https://arxiv.org/abs/2404.18318),
also published at [ESA 2025, article 30](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2025.30).
The introduction of the [authors' full manuscript](https://www.math.tau.ac.il/~krivelev/distance_queries.pdf),
page 2, explicitly uses `np^2=2 log n+log log n+omega(1)` to ensure that
every nonedge has at least two common neighbors. That scale and its
elementary binomial calculation are prior work. Their oracle returns
distances and their problem is graph reconstruction; it is different
from full directional feedback about a target in a known graph.

Michael Krivelevich, Matthew Kwan, Po-Shen Loh, and Benny Sudakov,
*The random k-matching-free process*, Random Structures & Algorithms 53
(2018), 692--716, [arXiv:1708.01054](https://arxiv.org/abs/1708.01054),
[author manuscript](https://mkwn.github.io/RMFP.pdf).
Section 4.2 and Lemma 20 explicitly study two degree-one neighbors of
one vertex. Their calculation gives the same elementary cherry first
moment and the overlap classes behind its second moment; the scale
`nq=(log n)/2+log log n` appears there. We credit this prior mechanism.
The appearance of a fixed three-vertex path at scale `q=n^(-3/2)` is
also classical fixed-subgraph threshold behavior. We do not claim any
of these isolated counting facts, moment methods, or threshold scales
as new.

Jeong Han Kim, Benny Sudakov, and Van Vu, *On the asymmetry of random
regular graphs and random graphs*, Random Structures & Algorithms 21
(2002), 216--224,
[author manuscript](https://people.math.ethz.ch/~sudakovb/automorphism.pdf),
was checked for the adjacent symmetry setting. Graph asymmetry is a
different property: a complete graph resolves from every vertex in
one full directional probe despite its large automorphism group.
No asymmetry theorem is imported into our proof.

## What is proposed as new

The claimed contribution is the **complete uniform probability law for
universal full-feedback one-round resolution**, its three-transition
behavior, and the critical laws for the number of failed probes. The
specific bridge in the dense range is that all directional trace
collisions other than complement leaf cherries have total probability
o(1) whenever the defect mean is bounded. The sparse bridge rules out
other response defects at its critical window. These reductions connect
the classical counts to the actual shortest-path response map, and the
regime analysis covers every probability p.

Searches included the exact phrases “directional localization” with
“random graph”, “threshold”, and “one-round”; “full-feedback” with
“localization” and “Poisson”; and random-graph common-neighbor, leaf-cherry,
and asymmetry searches. No source giving this exact directional phase
law was found. Some queries were dominated by unrelated acoustic or
physical localization results, so the negative search is weak evidence
of priority. The positive prior-work matches above are incorporated
explicitly rather than counted as novelty.

All probabilistic calculations used in the theorem are proved in
[PROOF.md](PROOF.md), including the factorial-moment criterion. The only
external mathematical convention needed is the credited game definition.
The exact checker is finite corroboration, not peer review or formal
verification. Independent mathematical review remains pending.
