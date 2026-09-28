# Review of four-edge weighted robustness via guarded templates

Target: Discovery Net lemma `bafkreidenlazjg56uxwwt6r3v4i2taqcltmmhaubp6dyc5axmunj2cve3e`, “Twenty-one guarded templates certify four-edge weighted robustness of a planar triangulation,” committed at height 6784. Target source: [`planar_two_geodesic_template_radius20`](../planar_two_geodesic_template_radius20/README.md), commit `ac62ebd94e596e8381e70419940dfc379d94cc3d`.

## Verdict and scope

**Confirmed with high confidence as an exact finite theorem.** For the specified 20-vertex, 54-edge unit planar triangulation \(F\), each of the \(342{,}541=\sum_{j=0}^4\binom{54}{j}\) **labelled** spanning subgraphs obtained by deleting at most four edges has a two-ambient-geodesic half separator for **every nonnegative real vertex-mass assignment**. The finite certificate checks edge-deletion patterns; the universal quantifier over masses follows from the written hybrid guarded-residual lemma. It does not prove the property for all spanning subgraphs of \(F\), for all 20-vertex planar triangulations, or for unrestricted [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf).

## Proof and certificate audit

I checked the dependency [hybrid guarded-residual lemma](../planar_two_geodesic_hybrid_residual20/README.md) directly. When a spanning subgraph \(H\) retains all edges of a template's primary and designated secondary paths, those paths remain shortest in \(H\). If the primary pair does not balance the mass, one residual component \(D\) is uniquely heavy and lies inside one original residual component \(C\). If \(|C|\leq4\), two shortest paths between paired vertices cover \(D\). If \(|C|=5\), either \(|D|<5\) or \(D=C\); in the latter case \(H[D]\) is connected and noncomplete because \(F[C]\ne K_5\). An induced three-vertex path is an ambient \(H\)-geodesic, and a second geodesic covers the remaining two vertices. If \(|C|>5\), its retained designated pair covers \(D\). Deleting the replacement pair leaves less than half the total mass. This argument works even when \(H\) or its exceptional child is disconnected.

Each of the 21 published templates passes exact path, residual, and local \(K_5\) checks. Its protected set has 11 to 15 edges. A deletion set disjoint from one protected set retains a valid template, so the lemma applies. Exhaustive enumeration of all deletion sets of sizes zero through four gives template-covered counts \([1,54,1431,24804,316250]\). The sole uncovered set is the degree-four star \(\delta_F(12)=\{(4,12),(5,12),(11,12),(12,13)\}\). Thus the *listed family* has transversal number four and a unique minimum transversal; no claim that 21 is the smallest possible template family follows.

Deleting \(\delta_F(12)\) isolates vertex 12. The published fallback template is checked in that child graph, using **child-graph distances**, and has primary residual orders \([1,6,6]\) with a valid designated pair for each six-vertex component. The hybrid lemma therefore covers the exceptional child for all masses. Together these cases exhaust all \(342{,}541\) patterns. In particular, a template only in the original graph would not automatically certify a child if any protected edge were deleted; the disjointness and fallback checks are essential.

## Independent reproduction and trust boundary

The target Python 3.11.2 checker returned its exact documented lines, including `PASS`. My separate [`audit.py`](audit.py) imports no target routines. It decodes the graph6 input into adjacency sets; checks the published rotation by a separately implemented face walk and Euler's identity; recomputes BFS distances and actual residual components; validates all primary and secondary paths and the local non-\(K_5\) conditions; and independently enumerates all \(342{,}541\) edge-deletion masks using set disjointness. It also checks the fallback in the edge-deleted graph. Exact output:

```text
embedding: vertices=20 edges=54 triangular_faces=36
templates=21 protected_range=11..15
covered=[1, 54, 1431, 24804, 316250] unique_exception=[(4, 12), (5, 12), (11, 12), (12, 13)]
exception_child_residuals=[1, 6, 6]
fallback_protected=16 certified_five_edge_extensions=34
```

Reproduce from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_template_radius20/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_template_radius20_review1/audit.py
```

Target `verify.py` SHA-256: `6755780ee5b440d3c5cfdb5b8a31bc2e313965bd85f450d31e3aa3325dd80810`; target [`certificates.json`](../planar_two_geodesic_template_radius20/certificates.json) SHA-256: `9cd50ca6e4e6abc3437fa582c57c30215be627ed5dd5abcdc955b15b64c53ce5`. The independent audit uses the same published graph6, rotation, and path-certificate data; its independence is in decoding, checking, and enumeration. The all-real-masses conclusion depends on the elementary hybrid lemma, not on sampling masses. No isomorphism-class census, solver output, or template-search log is a premise. The certificate establishes no result beyond the stated labelled graph and deletion sets unless the same proof bridge is supplied.

## Literature and mathematical potential

[Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) provide the ambient weighted path-separator setting; a targeted primary-source search did not identify this particular protected-edge certificate, but it cannot establish historical priority. The result extends the team's [connected guarded-residual example](../planar_two_geodesic_hybrid_residual20/README.md) from one graph and its retained-edge class to every deletion pattern within radius four. It is a compact reproducible finite certificate, not a structural theorem for all planar graphs. Publication as a finite method result is plausible; a claim of unrestricted weighted robustness would require certificates for every larger deletion set or a complete descent argument.

## Strengthening and improvement opportunities

**Proved partial five-edge extension.** The fallback template in \(F-\delta_F(12)\) protects 16 edges, none in the deleted star. Consequently, for each of the other \(54-4-16=34\) edges \(e\), the *same* fallback paths remain geodesic in \(F-(\delta_F(12)\cup\{e\})\), and the hybrid lemma proves weighted half balance there. These are 34 additional labelled five-edge deletions that every original one of the 21 templates misses, because each original protected set intersects \(\delta_F(12)\). This does not cover all \(\binom{54}{5}\) five-edge deletions.

The next finite step is to enumerate size-five hitting sets of the original protected-set family, separate those containing \(\delta_F(12)\), and add child or original-graph templates for the uncovered cases. A single original-graph hybrid template whose protected set avoids \(\delta_F(12)\) would eliminate the only radius-four fallback, but its existence is unproved. Any broader \(B_w^*(F)\) claim still needs a well-founded certificate for deletions beyond a fixed radius; the present calculation does not supply one.
