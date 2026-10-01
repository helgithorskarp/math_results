# A local two-star bound without the covered-triangle premise

Actual author: **six-code-3, researcher**, 2026-10-01. The complete raw
carrier is the credited earlier six-code-3 result9045. Its exploratory
inputs and broader carrier observation credit **six-code-1, researcher**.
Two existing seed colorings are reused with exact attribution below.

**Local theorem.** Let F be five-subsets of eighteen points, with distinct
members intersecting in at most two points. Write r_p for the number of
words through p, lambda_pq for the number through p,q, and call a triple
covered when it lies in a word. For distinct x,y,u,v, assume:

1. r_x=r_y=20, lambda_xy=4, lambda_xv=5, and vxy is uncovered.
2. lambda_xu is3 or4; lambda_xp is4 or5 for every p other than x,u.
   In the x-star leave induced on the points p with lambda_xp<5,
   the vertex u is isolated.
3. lambda_yu=lambda_yv=5, and lambda_yp is4 or5 for every p other than y.

Then **|F|<=66**. If lambda_xu=4, then **|F|<=64**.
Neither bound is asserted sharp. The covered-triangle premise4 of9045
is omitted; the conclusion lambda_xu=3 of that earlier theorem is not
claimed here. No hub multiplicity, other point replication, whole-code
automorphism or global replication profile is assumed.

The x-star leave has an edge pq exactly when xpq is uncovered. Isolation
in assumption2 concerns its deficient induced subgraph; it permits low
leave neighbors of u. This is a local conditional result and changes
neither the campaign unrestricted69--71 interval nor the external
[table's69--72 interval](https://aeb.win.tue.nl/codes/Andw.html).
The ordinary reduction and imported enumeration-completeness arguments
are unformalized; independent review of this new result and historical
priority remain pending.

## Imported raw carrier and its scope

[Earlier local result9045](../good_cohort_z_interfaces/PROOF.md), source
e2f9cc128036b909d4d45a88ba2c5b72f1db8e2d, proves complete raw carrier
coverage **before** applying its triangle filter. Shortening at each
center gives twenty quadruples on seventeen points with pairwise
intersection at most one. The reviewed generic23-class classification
and universal no-low-low leave theorem are explicit dependencies of9045.
The imported coverage argument uses assumptions1--3 above; its separate
covered-triangle premise4 only discards raw positives afterward.

That carrier has14/878 raw first/second marks,2/180 actually checked
subgroup mark orbits, and360 products. Its933120 partial maps represent
5598720 complete relative maps. Separate block-tail and point-DFS
algorithms found exactly34 compatible maps, giving34 distinct labelled
36-word unions in28 products. These are normalized marked interfaces,
not asserted to be34 full isomorphism classes. Every code satisfying
assumptions1--3 relabels to one of those unions. No multiplicity-two
other-uv-tail restriction is in that raw carrier.

[BRIDGE.json](BRIDGE.json) is copied byte-for-byte from9045's public
raw bridge, SHA256
9239f6cfcb413ff8a76eddf172ebd62abdec46aec7c8c87c788c2370e856d1d2.
All34 entries are retained. In particular, all32 entries with an
uncovered common-center multiplicity-four triangle,45 actual witnesses
in total, are included. The two entries without such triangles remain
included. This package does not re-enumerate the360-product carrier;
its completeness is an imported proof dependency, and can be reproduced
using9045's linked source. The current package independently rebuilds
each literal core, all local hypotheses, every residual domain and every
proper-color check from these34 entries.

## Residual color certificates and the ordinary bound

Each core K has36 distinct words,20 through each specified center x,y,
and four through both. In any extension retaining r_x=r_y=20, every
further word avoids both centers. There are exactly C(16,5)=4368 such
five-subsets. A subset is individually admissible precisely when it
shares no triple with K, equivalently when its intersection with every
core word has size at most two.

For every literal K, form a graph whose vertices are all individually
admissible further words; connect two exactly when their intersection
has size at most two. Further words of F form a clique in this graph.
An explicit proper k-coloring bounds that clique by k, giving
|F|<=36+k. This uses only positivity of a finite certificate; no search
failure, numerical optimum or solver exclusion is needed.

[certificates.json](certificates.json) supplies all34 proper colorings.
Residual populations range110--135, totalling4149 vertices and209622
compatible edges over the34 graphs. Proper color counts range25--30.
The complete distribution of certified total bounds is:

| Certified total bound | Interfaces |
| --- | ---: |
| 61 | 2 |
| 62 | 5 |
| 63 | 7 |
| 64 | 15 |
| 65 | 1 |
| 66 | 4 |

Thus every raw interface gives |F|<=66. The complete subset with
lambda_xu=4 consists of eight entries; every one has at most28 colors,
giving the refinement |F|<=64. The other26 entries have lambda_xu=3,
and their maximum certificate uses30 colors. These are actual checked
pair-count subscopes, not a conjectured identification from fixture names.

[verify.py](verify.py) uses literal sets and owned triples to reconstruct
allC(16,5) candidates for every core, verifies local roles and actual
point-map images, then checks every compatible candidate pair against
the supplied color array. It imports no producer, old census helper,
graph module or solver. All source masks, integers, populations,
attributions, color ranges and numerical totals are checked explicitly,
including under Python-O. The ordered candidate-domain hash is
3abef97cddb81b4238f481881bb08d4419e0b38985c38a718435aaaedbf574d4;
the per-interface mathematical record hash is
5ea8cd6745a8bac988fa8f314e2962bff0310db49e90379e66899ca9877a4538.
Hashes use canonical compact JSON without a final newline and corroborate
the actual entrywise checks; hash agreement alone is not the proof.

## Generation, validation and dependencies

[generate.py](generate.py) uses exact bit-mask intersections and greedy
DSATUR to discover positive color arrays. For each of32 new interfaces
it tries an initial fixed priority and at most64 reproducibly seeded
priority permutations, stopping early at28 colors. This heuristic does
not certify optimality. The two previous literal seeds use their
credited25/28 colorings from
[result8967](../two_saturated_seed_interfaces/README.md), source
e26ac0cd59844e9aee9eb8f48e513ffd20910925, copied unchanged as
[seed_certificates.json](seed_certificates.json), SHA256
521f0b322523a340c302fa5f4ea86fd3803a73e3665194e8cff556c0d0635ff6.
Their residual graphs and color checks are freshly rebuilt here.

[controls.py](controls.py) rejects24 semantic damages and transports
all34 literal interfaces and actual color arrays under three point
relabelings fixing normalized x=17,102 transported interfaces. The
complete candidate universes and literal point images are checked in
each transport. [reproduce.py](reproduce.py) regenerates the compact
certificate, compares its whole bytes with the already frozen public
certificate, checks the complete mathematical summary against a
pre-existing [expected.json](expected.json), and runs all controls.
Cold normal and optimized executions agree on every stable record and
actual certificate byte. Details and runtime are in
[VALIDATION.json](VALIDATION.json). These are separate algorithms by the
same author, not a new independent review. Imported9045 is itself
author-checked, with its independent audit pending at this publication.

Reviewed classification8933, source0509c3808f44b45fd3c333a10cf36bd329003450,
[review](../../six-reviewer-5/twenty-star-classification-audit/REVIEW.md),
confirms generic23-class coverage conditional on reviewed universal8323,
[review](../../../constant_weight_upper71_review1/REVIEW.md). The literal
fixture supplier8720, source69f2312bb468eb59b8ab3d8978fe19b3d86cf58a,
[source](../../six-code-2/free_involution_upper68/PROOF.md), is credited
for the generic inputs; its symmetry-specific numerical theorem is
not imported. Exact graph references and input provenance are in
[DEPENDENCIES.json](DEPENDENCIES.json).

The known69 baseline from
[Aw--Chee--Ling2003, Theorem1/AppendixA](https://ymchee66.github.io/home/PDF/6cwc.pdf)
was freshly reproduced this pass:69 five-subsets,690 owned triples and
2346 valid word pairs. Baseline reproduction is validation, not novelty.
This local theorem does not assert an ambient71 profile exclusion or a
new unrestricted numerical bound.
