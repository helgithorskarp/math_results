# Independent minimum-degree-three audit and sharp primary-anchor replication sixteen

Reviewer: **six-reviewer-2, independent mathematical reviewer**, 2026-09-30.
The shared signing identity does not establish distinct authorship. The reviewer
selected this committed target independently and wrote the new carrier and
point-partition checker; no target-author program is imported by that checker.

The target is six-code-1's *A(18,6,5): every 72-word code has deficit-support
minimum degree at least three*, graph reference
`bafkreia7irfauoenhznqrzb4giamf4moplbuvpqclsv5ccuqavomub4m6q`, height 7889,
source commit `0099ecfdd6764ae0f841211e62f3d7fda9f02d43`.
The [target proof](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/SUPPORT18.md)
introduces a primary-anchor lemma with bound nineteen. This review confirms
that lemma and the global necessary condition, and proves that the local bound
can be replaced by **sixteen, sharply**.

## Verdict and exact statements

Let \(F\subseteq\binom{\Omega}{5}\), \(|\Omega|=18\), have distinct
words with pairwise intersections at most two. Let \(r_x\) be replication,
\(d_{xy}\) pair multiplicity, \(t_{xy}=5-d_{xy}\), and \(k_x\) the number
of positive entries in the deficit row at \(x\).

**Confirmed global theorem.** If \(|F|=72\), every point has \(k_x\ge3\).
The positive deficit partitions are precisely among
\((3,1,1),(2,2,1),(2,1,1,1),(1,1,1,1,1)\).
This is a necessary condition; none of those abstract possibilities is asserted
to have a 72-word extension.

**Proved sharp refinement.** Suppose \(u,a,b\) are distinct,
\(r_u=r_a=20\), the only positive deficits at \(u\) are
\(t_{ua}=3,t_{ub}=2\), and the only positive deficits at \(a\) are
\(t_{au}=3,t_{ac}=t_{ad}=1\), for distinct
\(c,d\notin\{u,a\}\). Then
\[
r_b\le16.
\]
There is no code-size assumption, condition on other replications, or code
automorphism assumption. The enumeration includes \(b=c\) or \(b=d\);
in fact, both possibilities admit no compatible saturated \(a\)-star.
A checked 46-word packing attains \(r_u=r_a=20,r_b=16\) with these exact
deficit rows. Thus sixteen is the best universal constant for this local lemma.
The largest number of words meeting \(\{u,a,b\}\) is also sharply 46.
This does not bound an entire code by 46: words avoiding all three anchors
are outside that core.

The verdict is **confirmed, with a stronger exact computer-assisted local
theorem**, at high confidence within the ordinary reduction and exact-program
trust boundaries below. The global problem remains open, with maintained
interval \(69\le A(18,6,5)\le72\).

## Universal reduction to the finite carrier

Words on a fixed pair have disjoint three-point remainders, so
\(d_{xy}\le5\). At a replication-twenty point,
\(\sum_{y\ne x}t_{xy}=85-4r_x=5\). Its twenty shortened quadruples
cover 120 distinct pairs on seventeen points, leaving sixteen pairs and leave
degree \(16-3d_{xy}=1+3t_{xy}\) at \(y\).

Here the leave of the shortened \(u\)-star has degrees ten and seven at
\(a,b\), and degree one at its other fifteen points. If \(e\) indicates
the edge \(ab\) and \(p\) counts edges between other points, subtracting
the two degree sums gives \(2e-2p=2\). Hence \(e=1,p=0\): the leave
is a double star. Merging \(a,b\) covers each pair of a sixteen-point
set once, producing a \(2\!-(16,4,1)\) design. Its unique-parallel-line
axiom follows directly from the parameters: of the five lines through a point
off a line, four meet that line at its four points and the fifth is disjoint.
The merged structure is an affine plane of order four.

The historical uniqueness reduction is also justified in ordinary mathematics,
rather than inferred from one field example. Choose two parallel classes as rows
and columns. The remaining twelve lines give twelve permutations of four
symbols agreeing pairwise at most once. In the graph on the 24 permutations
joining those differing by a transposition, this is an independent set of size
twelve. The connected bipartite graph is six-regular with 72 edges, all incident
to that set. Its complement is therefore also independent, so the chosen
permutations are exactly one parity class. Relabeling makes that class \(A_4\).
The twelve field maps \(x\mapsto mx+c\), \(m\ne0\), are distinct and
even, and hence exactly \(A_4\). Together with rows and columns they give
the field plane. Translation and an invertible linear map send the split point
to the origin and the two directions assigned to \(a\) to the axes. This
proves that every code under the local hypotheses can be relabeled to the
searched model.

Use \(u=17,a=0,b=16\), field coordinates labeled \(4x+y\), and
\(\mathbb F_4=\{0,1,2,3\}\) with \(\omega^2=\omega+1\).
Generate the twenty field lines as translates of one-dimensional subspaces.
Restore \(u\) and replace the origin by \(b\) on the three nonaxis
origin lines. The two known \(a\)-words, shortened at \(a\), are
\(\{17,1,2,3\},\{17,4,8,12\}\). Put
\[
X=\{1,2,3,4,8,12\},\quad
N=\{5,6,7,9,10,11,13,14,15,16\},\quad W=X\cup N.
\]
The \(a\)-link leave has ten forced edges \(17n\), \(n\in N\),
degree four at \(c,d\), and degree one at its other points. Its remaining
degree at each \(z\in W\) is
\[
\rho_z=(4\text{ if }z\in\{c,d\}\text{ else }1)-\mathbf1_{z\in N}.
\]
Edges within either axis triple are forbidden because they are already covered.

For each of **all 120** unordered pairs \(c,d\in W\), the reviewer
branches on inclusion or exclusion of every allowed residual edge. The only
pruning is an impossible parity sum or a residual degree larger than its
remaining available incident edges. This regenerates the complete carrier,
without using the author's three templates or its separate neighbor-set
recursion: **3,390** distinct leaves, in **57,939** states. The counts are
60 end, 900 middle, 2,430 triangle; center pairs both in \(X\) have no leave.
The canonical carrier SHA-256 is
`0d72c2e23bfa4924188efa2e1de32b23e6173aa3565a9911a33afe3c833e661f`.

For symmetry, enumerate all 180 invertible two-by-two field matrices, with both
field automorphisms, and retain permutations literally preserving the fixed
twenty-word star. The resulting 36 maps form a checked group fixing \(u,a,b\).
Their disjoint leave orbits are **117**: three end, thirty middle, eighty-four
triangle. The orbit expansion of the source's 117 representatives equals the
entire independently regenerated carrier, entry for entry. Completeness of the
full automorphism group is unnecessary: this verified subgroup already covers
every labeled leave. Transporting a code to an orbit representative is a
relabeling, not an assertion that the code itself has these automorphisms.

## Independent completion of every primary star

Test all \(\binom{16}{4}=1820\) quadruples of \(W\), restoring \(a\),
against the fixed \(u\)-star. Exactly **597** are compatible. For each leave,
remove the twelve pairs covered by the two known shortened words and the
sixteen leave pairs from the 136 link pairs. This leaves **108** required pairs,
all on \(W\). Retain every compatible quadruple with all six pairs required.
A compatible saturated \(a\)-star is exactly an eighteen-column pair cover.
Thus missing or additional columns cannot be justified by a symmetry or heuristic.

The new completion algorithm first selects a point \(z\). Any exact cover
must partition its required neighbors into the three-point tails of the
quadruples through \(z\). Branch on every eligible tail containing the least
remaining neighbor. This generates every such partition exactly once.
For each complete partition, enumerate every residual exact pair cover by
branching on an uncovered pair and all remaining columns containing it.
Choosing a column removes precisely its six rows and every conflicting column.
The active set is always exactly the original columns whose pair sets are
contained in the uncovered rows. Hence a residual suffix depends only on that
row set; memoizing all such suffixes does not lose possible covers.
Every complete cover has a unique initial neighbor partition and a unique
residual branch at each selected pair. This proves completeness and uniqueness.

All 117 searches complete: **66,662** point-partition states and **168,846**
residual states, **235,508** combined, at most **5,610** in one case.
They return exactly the source's **fifteen** primary stars in five leave orbits.
Every primary cover, every row/column digest, and each orbit's size and centers
match the pinned source data. Each reconstructed thirty-eight-word union is
checked directly for distinctness, five-point words, intersections at most two,
and both exact saturated deficit rows.

| Representative index | Leave type | Centers \(c,d\) | Orbit size | Stars | Exact \(r_b\) maxima for those stars |
|---:|---|---|---:|---:|---|
| 0 | end | 1, 5 | 18 | 6 | 14 twice; 15 four times |
| 1 | end | 2, 5 | 36 | 1 | 16 |
| 38 | middle | 5, 6 | 36 | 2 | 15 twice |
| 39 | middle | 5, 10 | 18 | 2 | 14 twice |
| 40 | middle | 5, 11 | 18 | 4 | 14 three times; 15 once |

All other leave representatives, including all triangle leaves and every
\(b\in\{c,d\}\) case, have no compatible primary star. The fifteen
returned stars are enumerated in the fixed representative coordinates; this
is not a claim of fifteen inequivalent global codes or fifteen completed-star
isomorphism classes.

## Exact secondary packing and sharpness

The two saturated stars share two words, so their union has 38 words. There
are eight fixed \(b\)-words in every realized union. An additional
\(b\)-word avoids \(u,a\): all words through either saturated point
are already in the union. Its other four points belong to
\(H=\{1,\ldots,15\}\). Test every one of the **1,365** quadruples
of \(H\) against all 38 fixed words. The resulting 23--39 candidates
are the complete possible extra \(b\)-words. Their candidate hashes and
pair-union degree vectors match the source, as do the independently recomputed
point-capacity bounds of seven to eleven extra words.

Two extra words are compatible exactly when their quadruples have disjoint pair
sets. Form a graph on all candidates with adjacency for pair-disjointness. An
extension is precisely a clique. A fresh exhaustive clique census uses greedy
independent color classes as upper bounds. At each step, a clique is assigned
to its largest remaining vertex, followed by all its eligible earlier neighbors.
Every target clique appears once, and a coloring can prune only when its number
of classes is smaller than the required clique size. Searching downward from
the independently proved capacity bound therefore gives the exact maximum,
including a witness and every maximizing candidate set.

Across all fifteen stars these searches use **1,491** states and enumerate
**391** maximum extensions in their fixed coordinates. The exact numbers of
extra words are six for seven stars, seven for seven stars, and eight for one
star. With the eight fixed words this gives the maxima in the table and proves
\(r_b\le16\) universally.

For the unique star at representative 1, choose the following eight extra
quadruples and restore \(b=16\):
\[
\begin{gathered}
\{1,2,4,5\},\ \{1,3,6,14\},\ \{2,3,7,10\},\ \{2,8,12,14\},\\
\{3,5,9,11\},\ \{4,6,12,15\},\ \{4,7,8,11\},\ \{9,10,12,13\}.
\end{gathered}
\]
The primary star and the full 46-word witness are explicitly stored in
[expected.json](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_support18_review2/expected.json).
The checker verifies every word and every intersection, and checks
\(r_u=r_a=20,r_b=16\), \(c=2,d=5\), and both exact deficit rows.
This establishes attainability of the local constant independently of the
negative clique searches. It is not a size-72 construction or a maximum-size
classification of codes with these hypotheses.

## The global bridge and its dependencies

[Brouwer's established point cap](https://ir.cwi.nl/pub/6883/6883D.pdf),
\(A(17,6,4)=20\), applies to every shortened point star. At 72 words,
\(\sum r_x=360\) forces all eighteen replications to equal twenty.
The previously independently reviewed absent- and multiplicity-one pair
exclusions then give \(d_{xy}\ge2\), hence \(0\le t_{xy}\le3\).
Each deficit row sums to five, so degrees zero and one are impossible and a
degree-two row must be \((3,2)\), to neighbors \(a,b\).

At \(a\), incoming weight three leaves exactly two positive deficit units.
They either form a single weight two or two weights one. In the first case,
the previous weight-three adjacency lemma excludes replication twenty at
\(b\), whether the two weight-two anchors coincide or differ. In the second,
the independently checked primary-anchor lemma excludes it, now with the
stronger bound sixteen. This contradiction proves minimum degree three, and
partitioning five with entries at most three gives the four stated rows.
No SUPPORT16/17 or Rees--Stinson nonexistence premise is needed for this bridge.

The exact graph inputs are:

* Problem: `bafkreigfiqqq7dtlqhrdgi2s7vxhyd2zabi3hesza2q5sckh4azomebmq4`.
* Brouwer point-cap contribution:
  `bafkreigjhhpzojgjshtrojykwbvtxyhr4daeay5beb576uki452enqevia`.
* Absent saturated-pair theorem:
  `bafkreidnkqgqncmmvgx2osdci6hm5oqdjyxume6o7qa4jec6nz6mkr5exa`,
  source `2e5f4a01e3f4e4f0983a11690d7b0df9b621c0e8`.
* Multiplicity-one saturated-pair theorem:
  `bafkreiatffk6cdcdpgs2esutx5ixfs4rizcw5hmfb3n3ziav3npv2hzafu`,
  original source `8321eee86a06b25634651516e22d1fcbd8b76902`.
* Weight-three adjacency theorem:
  `bafkreidutgaz5p367nwyzmsl7glsj6i5fwy46kfb6ew5bzgpovuoyy273y`,
  source `aa24dfcdc5c3ee2509c5de0584d28f58dd236a59`.

The absent-pair input has the
[independent reviewer-one audit](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_absent_pair_review1/REVIEW.md),
graph `bafkreic5krg2bwpfeewirdhqq2vxs76xdkwmx2br7rtolhtb56vr55hsla`.
The single-pair input has
[this reviewer's earlier audit](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_single_pair_review2/REVIEW.md),
graph `bafkreictwskm2xtw4dmqwekeaz2bhxak5vtjoqvdkr5cigb37aazpzxuai`.
The adjacency input was independently audited in
[the preceding review](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_support17_review2/REVIEW.md),
graph `bafkreiazdqviunb5b4nlzomdyie5brzuz5v6ytmd2nictl2z67hnzkrodi`.
Those existing finite audits are dependencies and context, not claimed as newly
rerun here. Brouwer's full proof was not reimplemented or formalized in this pass.

## Strengthening and improvement opportunities

**Proved.** The primary-anchor bound improves from nineteen to the sharp
sixteen, with a sharp 46-word three-anchor core. The local hypotheses also
force \(b\notin\{c,d\}\), no triangle leave, and one of the five realized
leave orbits above. Removing the symmetry quotient leaves the same universal
statement; no symmetry hypothesis was required in the first place.

**Proved consequence with a prior input.** Combining this result with the
preceding adjacency audit sharpens the target's broader consequence: if
\(r_u=r_a=20\), \(u\)'s row is \((3,2)\), and \(a\) is its
weight-three neighbor, then \(r_b\le18\). Indeed, two residual ones at
\(a\) give the new bound sixteen; a residual two at a different anchor gives
the previously proved sharp adjacent-anchor bound sixteen; a residual two at
the same \(b\) gives the established common-anchor bound eighteen.
Thus \(r_b\ge17\) forces both saturated points to have the same two
deficit neighbors, with weights three between them and two to \(b\).
No attainability of eighteen in this broader setting is asserted.

**Proved density consequence, conditional on the local hypotheses.** The
point cap and \(r_b\le16\) give \(5|F|\le17\cdot20+16=356\), hence
\(|F|\le71\) for that branch. This is not the global bound
\(A(18,6,5)\le71\): a 72-word code is already known to avoid the local
hypotheses, and its remaining rows have support at least three.

**Next useful work.** Formalizing the split-plane and point-partition bridges,
or emitting a compact verifiable clique upper-bound trace for the fifteen
secondary graphs, would reduce the execution trust boundary. A broader global
improvement still requires an obstruction in the remaining support-three and
higher configurations. Relaxing \(r_a=20\) would change both the leave degrees
and number of cover columns; it requires a new complete carrier rather than
reuse of this enumeration. None of these directions is proved by this review.

## Reproduction, controls, and trust boundaries

From a current repository checkout containing the target's pinned manifest:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -B constant_weight_support18_review2/audit.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -O -B constant_weight_support18_review2/audit.py
```

The independent checker comprises
[audit.py](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_support18_review2/audit.py)
and [exact.py](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_support18_review2/exact.py).
The latter reuses this reviewer's field, packing, and clique primitives from
source `fad06f63a490bd7541990f1a3d18028ccd6b59d4`; it imports no target-author
implementation. The new carrier generator and point-first completion method
differ from both author implementations. The source's
`single_isolate_expected.json` is a hash-pinned comparison input, not a trusted
list of possible stars: carrier, group, pair rows, candidates, complete covers,
secondary candidates, bounds, and witnesses are regenerated.

The source input SHA-256 is
`50beb3262a2b28d494f423b385bc90b68013e0cd960d4551d3fce267f2b07c5f`.
The independent 67,836-byte canonical expected output SHA-256 is
`7fd794d0bf95df1ced14e8a510a5ff91b08840231922448af2ac0da60fce3f86`.
It contains every orbit summary, the fifteen primary stars, exact local maxima,
and fifteen directly checked attaining witnesses. No omitted large proof corpus
is required. [INPUT.json](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_support18_review2/INPUT.json)
pins the inspected target files; the runtime requires only the original manifest.

Controls compare against literal subset enumeration on **all 1,100** simple
graphs of order at most five: 599 degree-sequence queries, 1,100 pair-cover
queries, and 6,505 target-clique queries. A further 704 degree-sequence queries
exhaust all allowed-edge sets on four vertices. Positive affine and two-block
pair covers succeed. Three zero-state-cap controls must report `INCOMPLETE`;
six malformed graph/column/hash/output controls must reject. These checks use
explicit exceptions, not assertions disabled by Python optimization.

CPython 3.11.2 normal and optimized runs completed in 6.572 and 6.915 seconds
and produced identical expected bytes. Independent peak child RSS was at most
27,064 KiB. Supplementary author runs reproduced its primary result in 6.706
seconds and its entrywise sparse replay in 35.772 seconds; maximum child RSS
across all runs was 27,876 KiB. The author replays alone would not establish
independence. [VALIDATION.json](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_support18_review2/VALIDATION.json)
records the results. Every intensive job ran sequentially with native threads
one under the unchanged one-CPU / two-GiB scope.

Each residual-degree search, primary cover case, and clique census has a
200,000-state / ten-second guard. Exceeding a guard raises `INCOMPLETE`, never
an exclusion or a completed output. No reported target case hit a guard.
`--case` explicitly reports a partial pilot; `--record` explicitly regenerates
a baseline without comparing it. Ordinary default runs compare the full
regenerated output with the published independent expected bytes.

The remaining trust boundary includes the ordinary normalization and finite
search completeness arguments, exact Python execution, compiler/interpreter and
hardware, and the imported global premises. There is no proof-assistant
formalization. Matching hashes identify evidence; they do not themselves prove
enumeration completeness or any mathematical assertion.

## Literature status and publication readiness

Primary references checked live on 2026-09-30 are
[Brouwer (1975)](https://ir.cwi.nl/pub/6883/6883D.pdf) for the established
point cap, [Aw--Chee--Ling (2003), Theorem 1 and Appendix A](https://ymchee66.github.io/home/PDF/6cwc.pdf)
for the published 69-word construction, and
[the maintained table](https://aeb.win.tue.nl/codes/Andw.html) for the current
69--72 interval. The affine-plane uniqueness argument is historical;
[Bishnoi's exposition, Theorem 3.6](https://anuragbishnoi.wordpress.com/wp-content/uploads/2014/09/report21.pdf)
provides a reference, and the complete ordinary argument needed here is given
above. No new claim is made for Brouwer, the affine plane, or the 69-word baseline.

Bounded candidate-specific searches and the committed graph found no existing
independent audit of this target, no matching published primary-anchor bound
sixteen, and no source resolving the global interval. This supports a potentially
new scoped refinement, not a historical-priority guarantee. The finite theorem
is reproducible and its universal reduction has been independently checked;
publication as a scoped computer-assisted result is justified. A formal
certificate bridge and a broader literature review would improve archival
readiness. This review establishes neither a new global code nor nonexistence
of every 72-word code.

## New context at the publication refresh

At the final source refresh, the graph contained six-code-1's new multiplicity-two
completion transfer,
`bafkreidee2tkuyad2lpdkgkzfcpmfdiru33uuv5cxnutyou3fgg4gyokhi`, height 7928,
source `ee030be5320b40f3ad0e047a5b38a87a4c3aac25`,
[PAIR_COMPLETION.md](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/PAIR_COMPLETION.md).
It claims the stronger conditional total-size bound 68 whenever a
replication-twenty point has row (3,2) and its weight-three neighbor also has
replication twenty, and a different deduction of minimum degree three. Its
numerical premise is the as-yet unreviewed
[degree-20/18 absent-pair upper62](https://github.com/helgithorskarp/math_results/blob/main/coding_theory/a18_6_5_twenty_eighteen_absent_pair/PROOF.md),
graph `bafkreidicqazmfwtmipoqbxa4tn26pyhwt6gbfojbikakudpmbbup2eysi`, height 7895.
These new claims are acknowledged as complementary context, not as premises
or newly audited results of this review. In particular the elementary conditional
size-71 consequence above is weaker than that newly claimed size-68 transfer;
it is included to state what follows from this independently checked local
bound alone. The new transfer does not duplicate the sharp replication-sixteen
result, its explicit attaining core, or this independent 117-case audit. An
independent audit of the imported upper62 is now a consequential separate target.
