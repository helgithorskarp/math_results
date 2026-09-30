# Independent seventeen-point support audit and sharp adjacent-anchor bound

Reviewer: **six-reviewer-2**, role **independent mathematical reviewer**,
2026-09-30. Target author: **six-code-1**, role **researcher**. Target selection,
implementation and verdict were independent. The shared campaign signing key
does not distinguish authors.

**Verdict: confirmed, high confidence within exact finite computation and
ordinary written mathematics.** The primary target is *At least seventeen
higher-support-degree points in a 72-word A(18,6,5) packing*, committed height
7821, `bafkreidzsavdf7hx6kiemx7t6sui25gbk2zwyumzw427oa66tv2gx62w3y`.
I also independently audit its previously unreviewed adjacency input,
*A(18,6,5): no deficit-two or deficit-three edge between saturated degree-two
points*, height7759,
`bafkreidutgaz5p367nwyzmsl7glsj6i5fwy46kfb6ew5bzgpovuoyy273y`.
No correctness gap was found in either stated local theorem or the
seventeen-point corollary.

The review proves two additional local refinements. The distinct-anchor,
deficit-three adjacency case has **sharp individual anchor replication
bound sixteen**, improving nineteen. The shared-anchor case has replication
at most nineteen without assuming the shared anchor is saturated. A new
ordinary deduction obtains the seventeen-point conclusion without importing
the preceding support-sixteen theorem or its transitive design obstruction.
The global numerical interval remains \(69\le A(18,6,5)\le72\).

## Scope, source and independent method

Let \(F\) be distinct five-subsets of an eighteen-element set, with
\(|B\cap C|\le2\) for different members. This is equivalent to binary
weight-five minimum Hamming distance six. Write \(r_x\) for point replication,
\(d_{xy}\) for pair multiplicity, \(t_{xy}=5-d_{xy}\), and
\(k_x=|\{y:t_{xy}>0\}|\). The asserted global conclusion is
\(|\{x:k_x\ge3\}|\ge17\) at \(|F|=72\).

The new local target forbids five distinct points \(u,v,a,b,c\) with
\(r_u=r_v=r_b=20\), the only positive deficits at \(u\) equal to
\(t_{ua}=3,t_{ub}=2\), and at \(v\) equal to
\(t_{vc}=3,t_{vb}=2\). It has no code-size, replication-at-\(a,c\),
automorphism or incumbent assumption.

For the adjacency input assume \(r_u=r_v=20\), \(k_u=k_v=2\) and
\(t_{uv}=w\in\{2,3\}\). Let \(a,b\) be their other support neighbors.
The source proves: for \(w=2,a\ne b\) no packing exists; for
\(w=2,a=b\), \(r_a\le17\); for \(w=3,a=b\), \(r_a\le18\);
for \(w=3,a\ne b\), \(r_a,r_b\le19\). These are necessary local
restrictions. This review confirms them and improves the last bound.

The [primary target proof](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/SUPPORT17.md)
and its split/uniqueness inputs were read at immutable commit
`f5f4aa8850e4f51def3e654f008430d044c98bbc`.
The [adjacency proof](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/ADJACENT_LOW.md)
has original commit `aa24dfcdc5c3ee2509c5de0584d28f58dd236a59`;
its proof, both executables and manifest are byte-identical at the later
target commit. [INPUT.json](INPUT.json) pins the exact paths and hashes.

The fresh [audit.py](audit.py) imports no researcher executable or external
enumeration. It builds field lines as translates of one-dimensional
subspaces and represents words by integer masks. It independently generates
every candidate quadruple from literal intersections. It enumerates cliques
of the required size in the graph whose vertices are quadruples and whose
edges mean disjoint pair sets. This is a different enumeration from the
author's Algorithm X pair cover and separate relative-plane replay.
The author's two small manifests are untrusted comparison inputs: every
star and obstruction is regenerated. Each comparison input is hash-pinned.
The compact [expected.json](expected.json) contains the regenerated cases
and the new explicit optimal extensions.

## Structural reductions and normalization

The three-point remainders of words on a fixed pair are disjoint, so
\(d_{xy}\le5\). At \(r_x=20\),
\[
\sum_{y\ne x}t_{xy}=85-4r_x=5.
\]
Shortening the twenty words through \(x\) produces twenty four-subsets
of seventeen points, any two intersecting at most once. Their pair leave
has sixteen edges and degree \(1+3t_{xy}\) at \(y\).

If exactly two deficits are positive, fifteen leave vertices have degree
one and the other two have total degree seventeen. Let \(e\in\{0,1\}\)
indicate the edge between those two vertices, and let \(p\) count edges
among the fifteen degree-one vertices. Degree subtraction gives
\(2e-2p=17-15=2\). Thus \(e=1,p=0\): the leave is a double star.
Every ordinary point has one leave edge to one of its two centers, and
no block contains both centers. Merging them covers every pair of sixteen
points exactly once with twenty distinct four-subsets. This is a
\(2\!-(16,4,1)\) design. Every point has five lines; four lines through
a point outside a given line meet its four points, leaving precisely one
parallel line. Hence it is an affine plane of order four. Conversely,
splitting the five lines through one point into two nonempty parts gives
the original links. All thirty proper splits and inverse merges are
directly checked.

The field normal form covers every such plane. Choose two parallel
classes as rows and columns of a four-by-four array. The other twelve
lines are permutation graphs, pairwise agreeing at most once. In the
connected six-regular transposition graph on \(S_4\), they form an
independent set of twelve vertices. All72 edges meet that set, so its
complement is independent too. Connectivity forces one of the parity
parts. A column relabeling makes it \(A_4\), which consists exactly of
the twelve maps \(x\mapsto mx+c\), \(m\ne0\), on \(\mathbb F_4\).
Rows, columns and these graphs are the field plane. The checker verifies
the24 vertices,72 edges, connectivity and the identical field line sets.
The ordinary uniqueness argument supplies the universal quantifier;
the finite checks validate its small model. This is historical mathematics,
also stated as Theorem3.6 in
[Bishnoi's exposition](https://anuragbishnoi.wordpress.com/wp-content/uploads/2014/09/report21.pdf).

For the shared-anchor case, normalize the retained merged origin to
\(a=0\), the two retained origin directions to the axes, and
\(u=17,b=16,v=1=(0,1)\). The forced leave triple \(uvb\) places
\(v\) on a retained direction. Axis exchange and scaling cover every
choice. The six actual maps \((x,y)\mapsto(sx,y)\), \(s\ne0\),
with optional simultaneous Frobenius conjugation, preserve all twenty
first-star words and fix \(u,v,a,b\). Their closure and literal word
transport are checked. Their orbits on possible \(c\) are
\(\{2,3\}\), \(\{4,8,12\}\), \(\{5,9,13\}\), and
\(\{6,7,10,11,14,15\}\). Thus representatives2,4,5,6 cover every case.
These are permissible relabelings of arbitrary codes, not assumptions
that a code has any automorphism.

For distinct-anchor adjacency at \(w=3\), the analogous first-star
normal form is \(u=17,v=0,a=16,b=5=(1,1)\). The two \(v\)-assigned
origin lines are the axes. The forced leave triple \(uvb\) places
\(b\) on another origin direction, with both coordinates nonzero;
independent coordinate scaling sends it to \((1,1)\).

## Fresh finite coverage and the shared-anchor obstruction

In the shared case the five common \(uv\)-words partition the fifteen
points of \(H=V\setminus\{u,v,b\}\) into five triples. One of the
two \(vc\)-words is fixed. If its triple contains \(c\), the tail
of the other \(vc\)-word is any three of the remaining twelve points.
All220 tails per representative are tested. The two \(vc\)-words
determine every leave edge at \(v\): an ordinary point covered with
\(c\) is uncovered with \(b\), and conversely; \(bc\) is uncovered.
Remove those sixteen leave pairs and the36 pairs in the six fixed
shortened words. Exactly84 pairs remain.

Every four-subset avoiding \(u,v\) is tested. It is included precisely
when its six pairs are among those84 and its restored \(v\)-word
meets every first-star word at most twice. A clique of fourteen such
quadruples covers all84 pairs exactly once. Conversely every completed
second star supplies such a clique. No second-plane classification or
symmetry quotient is needed in this enumeration.

The clique routine greedily partitions the active graph into independent
color classes. A clique uses at most one vertex per class. It branches
on vertices in reverse color order, deleting the current vertex after
its branch. Each target clique has a unique last vertex in this order;
induction gives completeness and no duplicates. Color-count pruning
only removes a prefix with fewer classes than the remaining target size.
Each emitted clique and the resulting twenty-word star are checked.

| Primary anchor c | Compatible tails | Complete second stars | Point-capacity cases | Anchor leaves | Fixed-pair conflicts | Missing-pair certificates |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 24 | 0 | 0 | 0 | 0 | 0 |
| 4 | 29 | 8 | 6 | 12 | 4 | 8 |
| 5 | 36 | 12 | 4 | 60 | 26 | 34 |
| 6 | 38 | 10 | 9 | 6 | 3 | 3 |
| Total | 127 | 30 | 19 | 78 | 33 | 45 |

The independent clique census uses18,577 states. Every compatible tail's
candidate rows, candidate columns and number of stars match the source;
all thirty actual second-star word sets match entry by entry.

Each two-star union has35 words and six words through \(b\). Their
\(H\)-tails are six triples covering eighteen distinct pairs. Let
\(I,J\) be the two nine-point tail unions, \(q=|I\cap J|\), and
\(f_x\in\{0,1,2\}\) the tail occurrence count. Any additional
\(b\)-word avoids \(u,v\). A point \(x\) has only
\(14-2f_x\) unused incident \(H\)-pairs, so the number of extra
quadruples is at most
\[
\left\lfloor\frac14\sum_{x\in H}
\left\lfloor\frac{14-2f_x}{3}\right\rfloor\right\rfloor
=\left\lfloor\frac{60-q}{4}\right\rfloor.
\]
This is at most thirteen for \(q\ge5\), excluding saturation.

For \(q=3,4\), saturation at \(b\) leaves one further deficit-one
neighbor \(e\), since the two fixed deficits have sum four. The leave
restricted to \(H\) has three edges and vertex degrees
\(f_x-1+3[x=e]\). The independent checker generates every simple
three-edge graph with this degree vector, without the author's
star/matching templates. It recovers all78 possibilities. Thirty-three
reuse a covered pair. For each other leave, it examines all1365 four-sets
of \(H\), tests their restored words against all35 fixed words, and
requires their pairs to avoid the leave. A required pair is absent from
every eligible quadruple in all45 cases. Every leave, candidate digest,
required-pair digest and literal missing-pair certificate matches the
source. This direct obstruction excludes every remaining saturated anchor.

## Independent adjacency audit and exact anchor optimization

The \(w=2\) distinct-anchor case is an ordinary block contradiction.
The seven leave thirds on \(uv\) contain both anchors; remove them
to leave five points \(D\). The two blocks on \(ua\) partition
\(\{b\}\cup D\) into triples. The block on \(vb\) containing
\(a\) uses two points of \(D\). Avoiding the two points in the
\(ua\)-block through \(b\) forces those two into its other block,
giving an intersection of size three. All100 labeled tail choices
validate this argument.

If \(a=b\), the \(15-3w\) points outside the leave-third set on
\(uv\) have both \(u,v\) as uncovered thirds on their pair with
\(a\). Their multiplicity with \(a\) is at most four. The other
\(3w\) pairs have multiplicity at most five, and
\(d_{au}=d_{av}=w\). Thus
\(4r_a\le60+5w\), giving17 and18 for \(w=2,3\), respectively.
These local proofs use neither Brouwer nor a support-size theorem.

In the remaining \(w=3,a\ne b\) case, the three \(vb\)-words
partition their nine covered thirds into triples. The independent
partition recursion examines all280 unordered partitions. Exactly24
are compatible with the first star. Each fixes five origin triples;
the remaining second star covers precisely90 pairs between them.
The fresh clique census on every eligible four-subset produces all
sixteen second stars, with261,149 states and at most13,298 in any one
case. Every partition and actual star agrees with the source.

Each union has38 words and eight words through \(b\). Every extra
\(b\)-word avoids \(u,v\) and has one of the completely generated
29,30 or34 candidate quadruples on the other fifteen points. The
source's point-capacity bounds9,10,11 are independently verified.
For each of these sixteen small candidate graphs, the same complete
clique routine is run at successive sizes from that bound downward.
No clique exists above the first positive size. Every returned optimum
is directly pair-checked and an attaining full packing is recorded.

| Candidate quadruples | Source extra-word bound | Exact maximum extra words | Exact maximum r_b | Second stars |
|---:|---:|---:|---:|---:|
| 30 | 9 | 7 | 15 | 2 |
| 30 | 10 | 8 | 16 | 4 |
| 29 | 11 | 7 | 15 | 4 |
| 34 | 11 | 8 | 16 | 6 |

These optimizations complete in1,572 additional states. Therefore
\(r_b\le16\) in every distinct-anchor case, and interchanging
\(u,v\) gives \(r_a\le16\). The bound is individually sharp:
the recorded46-word witness has
\((r_u,r_v,r_a,r_b)=(20,20,9,16)\), pair multiplicity
\(d_{uv}=2\), the two prescribed degree-two links, and minimum
distance six. Swapping the endpoints witnesses sharpness for the
other anchor. No simultaneous attainment at both anchors, full-code
maximum46, or density attainment is asserted.

## Strengthening and improvement opportunities

**Proved sharp refinement.** The preceding exact optimization gives
\(r_a,r_b\le16\) for every \(w=3\) distinct-anchor local packing,
without assumptions on other point degrees or code size. The per-star
maxima15 or16 are exact. With Brouwer's degree bound, this carrier
cannot occur at size71 or72: total replication is at most
\(18\cdot20-2(20-16)=352\), hence \(|F|\le70\).
This is a conditional exclusion, not a new unrestricted bound70.

**Proved removal of saturation at the shared anchor.** Assume only
the two saturated links and their distinct primary/shared secondary
anchors in the primary target. Their union fixes six \(b\)-words.
Every extra one avoids \(u,v\); the six tails already cover18 of
the105 pairs on \(H\). Thus at most
\(\lfloor87/6\rfloor=14\) extras are possible, so \(r_b\le20\)
without importing Brouwer. The independently verified exclusion of20
then gives \(r_b\le19\). Sharpness of19 is not established.

**Proved shorter global dependency chain.** At size72 Brouwer forces
all eighteen replications to be20. The separately reviewed absent-
and single-pair results imply \(2\le d_{xy}\le5\), hence
\(0\le t_{xy}\le3\) with row sum five. Every point has
\(k_x\ge2\), and every degree-two point has incident weights3,2.
Two such points cannot be adjacent: their edge would have weight2
or3, forbidden by the adjacency theorem just audited. This proves
independence of the entire degree-two set, with no bound on its size
assumed.

Suppose two remain, \(u,v\), with weight-three anchors \(a,c\)
and weight-two anchors \(b,d\). Independence places all anchors
outside \(\{u,v\}\). The equality \(a=c\) would give a deficit
row at least six. If \(a=d\) or \(b=c\), that anchor's two
incident deficits3,2 exhaust its row, making it degree two adjacent
to another degree-two point, again forbidden. Since \(t_{uv}=0\),
there is exactly one uncovered third on \(uv\):
\(16-3d_{uv}=1\). Each double-star link forces this third into
both \(\{a,b\}\) and \(\{c,d\}\). The only possible intersection
is \(b=d\). The shared-anchor theorem excludes that configuration
because this common anchor also has replication20. Consequently
there is at most one degree-two point and at least seventeen points
of degree at least three.

This derivation uses Brouwer, the two pair bounds and the two local
theorems audited here. It does **not** use SUPPORT16, its earlier
support-size chain, or the Rees--Stinson design nonexistence theorem.
The [existing support-sixteen review](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_support16_review5/REVIEW.md),
`bafkreif2c3tpoeau5zljz35mcz4vkbmfy2c5tqycxbk6zp2vimrsqqtdde`,
is credited for context and the older normal-form audit; its sufficient
enumeration was not repeated or used as a premise of this shorter proof.

**Later work, outside this audit.** During the final refresh a newer
committed claim at height7889 excludes the remaining single degree-two
case: [SUPPORT18.md](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/SUPPORT18.md),
source commit `0099ecfdd6764ae0f841211e62f3d7fda9f02d43`. Its additional
finite obstruction is not reviewed here. It refines the support-seventeen
target and imports the adjacency input; the present assessment supplies
independent evidence for that input. The new
graph reference is `bafkreia7irfauoenhznqrzb4giamf4moplbuvpqclsv5ccuqavomub4m6q`.
Its own stronger global bridge also bypasses the earlier support-size
chain; that concurrent result is credited, with no priority claim for the
idea of removing those dependencies.
No exclusion of the case with eighteen higher-degree points follows from
this audit. That needs a new coupled-star obstruction or complete feasible
leave-cover analysis.
A sharp shared-anchor maximum requires complete packing optimization
and a matching witness. Formalization should prove the split-plane
and parity normal forms, the clique-cover equivalence and colored
recursion, then replay the finite instances inside a trusted kernel.
That is the concrete remaining bridge to a formally checked theorem.

## Reproduction, validation and trust boundaries

Run from a full repository checkout, with the two hash-pinned target
manifests present in the sibling source directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -B constant_weight_support17_review2/audit.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  python3 -O -B constant_weight_support17_review2/audit.py
```

Expected: COMPLETE; shared stars0,8,12,10;78 leaves;16 adjacency stars;
the four-row sharp-extension table above; identical output digest
`80c93b9970bd429127c443bacbb2eaa4574dd1413b12111f159393370cce8477`.
The published expected summary is79,224 bytes. Proof checks use explicit
exceptions and remain active under Python optimization.

The independent routine is compared with brute force on all1,100 simple
graphs through five vertices, for all6,505 target sizes. It accepts the
actual twenty-line affine pair cover. Duplicate/invalid words, self-loop
and asymmetric graph encodings, and both state/time incomplete controls
are rejected. Each census has an unchanged200,000-state/ten-second
guard; no successful run reached a guard. A guard failure raises
INCOMPLETE and proves no exclusion. Every reported case completed.

CPython3.11.2 standard library, one process and numerical threads1.
The final independent normal run took21.894s, optimized20.515s, with
cumulative child peak RSS at most22,288KiB and identical results. Earlier
runs took10.625s/10.119s, with peak22,548KiB; the final source additionally
checks the exact saturated deficit patterns of every relevant witness. As supplementary
reproduction, both original target programs and both original adjacency
programs were run sequentially with complete entrywise comparisons;
all passed, in0.796s,2.033s,0.548s and3.925s. Those are author programs,
clearly distinguished from the fresh independent implementation.
[VALIDATION.json](VALIDATION.json) records the exact results and versions.

This is an exact computer-assisted proof with ordinary completeness
and geometry arguments, not a proof-assistant formalization. The trust
boundary includes Python integer execution, the finite search implementation,
the written reduction/normalization/completeness arguments and ordinary
hardware. Hash agreement authenticates comparisons; it does not establish
enumeration completeness. No solver verdict, floating arithmetic,
unpublished case census or omitted large proof corpus is a premise.

The global consequence imports Brouwer's upper theorem rather than
reproving his scarce-design case analysis, and the two saturated pair
bounds rather than repeating their already sufficient audits. The
[absent-pair review](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_absent_pair_review1/REVIEW.md)
is `bafkreic5krg2bwpfeewirdhqq2vxs76xdkwmx2br7rtolhtb56vr55hsla`.
The [single-pair review](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_single_pair_review2/REVIEW.md)
is `bafkreictwskm2xtw4dmqwekeaz2bhxak5vtjoqvdkr5cigb37aazpzxuai`.
Their underlying committed lemmas are respectively
`bafkreidnkqgqncmmvgx2osdci6hm5oqdjyxume6o7qa4jec6nz6mkr5exa` and
`bafkreiatffk6cdcdpgs2esutx5ixfs4rizcw5hmfb3n3ziav3npv2hzafu`.

## Literature, novelty and publication readiness

Primary literature was refreshed live2026-09-30.
[Brouwer1975](https://ir.cwi.nl/pub/6883/6883D.pdf) proves
\(A(17,6,4)=20\); shortening at a point is exactly that code problem.
[Aw--Chee--Ling2003](https://ymchee66.github.io/home/PDF/6cwc.pdf)
supplies the historical69 lower bound. The
[maintained table](https://aeb.win.tue.nl/codes/Andw.html), distance-six
row18/weight5, retains69--72. Affine-plane uniqueness, coloring bounds
for cliques, and these classical code ingredients are established.

Candidate-specific primary-source and committed-graph searches did not
locate the exact local or sharp-sixteen statements. This does not prove
historical priority. The concrete campaign additions are the independently
validated shared-anchor and adjacency obstructions; this review adds the
sharp local bound and the shorter global proof. No global resolution,
new record code, formal proof or journal acceptance is claimed.
The compact exact evidence and complete ordinary bridges support
publication as scoped computer-assisted results after consolidating the
statement, dependency credit and source. No proof or reproducibility gap
was found within these scopes; wider classification and formalization
remain separate work.
