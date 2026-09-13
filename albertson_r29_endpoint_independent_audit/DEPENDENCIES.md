# Imported theorem and evidence boundary

Primary candidate: Cao and Mehat,
[Albertson's Conjecture for Chromatic Numbers at Most 29, v1](https://arxiv.org/html/2609.04771v1),
submitted 2026-09-04. The reviewed endpoint is its Theorem 7.6 (r=29), not a
claim of a new result by this reviewer. Source archive and exact source/code
hashes are in PROVENANCE.json. Target replay is separate from the independent
proof and arithmetic checks.

| Input | Exact scope used | Source inspected |
|---|---|---|
| Essential immersion | Paths are edge-disjoint, and nonincident target edges have vertex-disjoint paths; cr(target)<=cr(host) | [Oporowski–Zhao, Definition 1.3 and Corollary 2.2](https://arxiv.org/html/math/0501427) (published Discrete Math. 309 (2009), 2948–2951) |
| Critical join decomposition | A critical graph with connected complement has at least 2k-1 vertices; chromatic numbers add across joins | [Stehlík, primary publisher statement](https://www.sciencedirect.com/science/article/pii/S0095895603000698), and [Barát–Tóth, Section 2](https://arxiv.org/html/0909.0413) |
| Critical edge lower bound | 2m >= (r-1)n+(n-r)(2r-n)-2 in r+2<=n<=2r-1 | [Cranston, Lemma B, with Gallai and Kostochka–Stiebitz attribution](https://arxiv.org/html/2512.08020v1); [Barát–Tóth Lemma 4](https://arxiv.org/html/0909.0413) |
| Small-order subdivision | An r-critical graph with n<=r+4 contains a subdivision of Kr | [Barát–Tóth, Corollary 11](https://arxiv.org/html/0909.0413) |
| Complement coloring | For every v of a critical graph with connected complement, G-v has a (k-1)-coloring with all color classes of size at least two | [Stehlík (2003), publisher abstract states the full theorem used](https://www.sciencedirect.com/science/article/pii/S0095895603000698) |
| Triangle-free density | delta(H)>2|H|/5 implies bipartite | [Andrásfai–Erdős–Sós, original paper](https://combinatorica.hu/~p_erdos/1974-18.pdf) |
| Critical regular case | chi<=max{omega,Delta-1,ceil((15+sqrt(48n+73))/4)} | [Rabern, primary abstract](https://arxiv.org/abs/1209.3646v3) |
| Crossing lower bound | cr(F)>=5e(F)-(203/9)(|F|-2), for |F|>=3 | [Büngener–Kaufmann, Theorem 6(b)](https://arxiv.org/html/2409.01733) (JGAA 29 (2025), 143–174) |
| Matching | Hall's saturation criterion and Tutte's odd-component criterion | Classical Hall (1935) and Tutte (1947), in their standard finite-graph forms |
| r=30 additional input | In the Gallai range, excluding the equality family that contains a subdivision raises the right side from -2 to -1 | [Barát–Tóth, Corollary 5](https://arxiv.org/html/0909.0413), applied only at n<=2r-2 |

These imported theorems are not reproved or formally verified by the code.
The primary statements were checked for the hypotheses actually used. The
Stehlík input is checked against its primary publisher statement; this is
not a fresh verification of his full 2003 proof. Cranston's order-range
results and the candidate's separate r<=28 conclusions are not needed by our
independent all-order reconstruction.

The cubic bound in REVIEW.md is derived directly by random sampling from the
listed affine bound, so it does not import a floating-point crossing-lemma
constant. The drawing upper bound Z(r), critical reduction, graph complementation,
ordinary degree counting, and elementary Hall consequences are also reproved
or explicitly explained where used.

Nothing uses cr(K13)=225, cr(K29)=8281, or any inequality-(7) scan.
No catalogue is a computational input to this audit. The published small-order
subdivision theorem uses historical critical-graph enumeration in its proof;
we import the theorem and do not regenerate that enumeration. No solver or
random search occurs in this audit. No computation was restarted in the historical
research-team-v2 workspace.
