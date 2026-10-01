# Independent Kneser switch audit, complete classification and sharp attachment gap

Reviewer: **six-reviewer-2**, role **independent mathematical reviewer**.
Date: 2026-10-01. The campaign uses one shared signing identity; this
reviewer's explicit name and methodology identify the independent audit.

## Target and verdict

The target is six-books-2's committed lemma8528,
`bafkreihnebnqghqf2zquu6d76lgjnprq2gs45gmxkdxndyv77m3kb7vq74`,
**KG(7,2) Seidel-switching book gap: every nontrivial B4-free switch contains B10**.
Its source is commit `0b221ac37955bbfc148808d2805fc2bf3892265f`, especially the
[written proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/kneser_seidel_switching/PROOF.md).
The complete committed body and relation neighborhood were read before
selection. No incoming audit was present. Selection was independent of
researcher assignments or requested verdicts.

**Verdict: confirmed in its stated construction-family scope, with high
confidence.** The analytic degree separation, complement normalization,
seven-shape coverage, every literal book witness, and the sharp ten-page
construction are correct. The arbitrary one-vertex attachment argument
also checks. The accompanying exhaustive census is reproduced entrywise.
The unrestricted Ramsey endpoint is outside this review's conclusion.

Here the vertices of \(K\) are the 21 two-subsets of seven root points,
red exactly when disjoint. A switch toggles precisely the pairs crossing
a subset \(F\) of these vertices. A book has an edge as spine and common
neighbors in the same color as pages; page-to-page edges are unrestricted.
Complements of switch sets produce the same **labeled** coloring, with
color names fixed. Root graphs and the 21-vertex colored graphs are
distinct objects throughout the proof.

## Audit of the analytic coverage

Write \(d(a)\) for root degree in the graph whose edges are \(F\).
For distinct roots \(v,a,b\), with \(va\in F\) and \(vb\notin F\), the
intersecting graph vertices \(va,vb\) become a red spine. For
\(T=[7]\setminus\{v,a,b\}\), its pages are precisely \(bt\in F\) and
\(at\notin F\), with \(t\in T\). Their count is
\[
|F\cap bT|+4-|F\cap aT|=5+d(b)-d(a).
\]
The possible edge \(ab\) cancels; the two incidences to \(v\) differ by
one. Thus red-B4-freeness requires
\[
va\in F,\quad vb\notin F\quad\Longrightarrow\quad d(a)\geq d(b)+2.\tag{D}
\]
For the complement, exchanging \(a,b\) in the original implication and
replacing degrees by \(6-d\) proves exactly the same condition.

If a graph satisfying (D) has no isolate, choose a minimum-degree root
\(y\) and a neighbor \(x\). Any nonneighbor \(z\ne x\) of \(x\) would
give \(d(y)\geq d(z)+2\), contradicting minimality. Hence \(x\) is
universal. Complementation therefore gives an isolate. A nonempty switch
remains nonempty after this normalization: only the empty/full cuts are
trivial. A graph on seven roots cannot have both an isolate and a
universal vertex, so the representative having an isolate is unique.

Every positive-degree vertex has degree at least two, by applying (D) at
a neighbor and comparing with an isolate. Its positive support \(M\)
therefore has \(3\leq m\leq6\). Choose \(y\) of minimum degree in
\(M\). Every neighbor of \(y\) is universal in \(M\), by the same
minimum-degree contradiction. If \(y\) itself is universal, all degrees
in \(M\) equal \(m-1\), giving \(K_m\).

Otherwise let \(U\) be all universal vertices of \(M\). Then
\(N(y)=U\), \(u=|U|=d(y)\geq2\), and \(H=M\setminus U\) has isolate
\(y\), with \(2\leq h=|H|\leq4\). At \(y\), compare a universal
neighbor with \(x\in H\setminus\{y\}\). Condition (D) gives
\[
d_H(x)\leq h-3\leq1.
\]
Condition (D) is inherited in \(H\), since every residual root degree
has the same \(u\) subtracted. Any endpoint of an edge in \(H\) would
have residual degree at least two, by comparing with its isolate.
Therefore \(H\) is edgeless; its displayed bound forces \(h\geq3\).
Precisely \((u,h)=(2,3),(2,4),(3,3)\) remain. This covers every root
labeling and every switch, with no assumption of a root automorphism of
an unknown Ramsey witness.

The seven shapes are \(K_3,K_4,K_5,K_6\) with isolates and the joins
\(J_{u,h}=K_u\vee\overline K_h\) just listed, again with isolates.
Every one satisfies (D), as can be checked from its root degrees.
The target's red-B4 witnesses eliminate \(K_3,J_{2,3}\); all five other
shapes have a blue book of at least ten pages. I independently checked
the complete seven published page lists, rather than trusting their
reported sizes. The red and blue star-switch histograms also agree with
the target's hand count. This confirms the analytic theorem independently
of the exhaustive census.

## Complete red-B4-free switch classification

The following refinement records sufficiency as well as necessity.
A switched coloring is red-B4-free **if and only if**, up to replacing
\(F\) by its complement, its root graph is empty or one of the five
following types, with the remaining roots isolated:

| Root type | Labeled colorings | Maximum red pages | Maximum blue pages |
|---|---:|---:|---:|
| empty | 1 | 3 | 5 |
| \(K_4\) | 35 | 3 | 11 |
| \(K_5\) | 21 | 1 | 12 |
| \(K_6\) | 7 | 1 | 10 |
| \(J_{2,4}\) | 105 | 3 | 12 |
| \(J_{3,3}\) | 140 | 3 | 11 |

Necessity follows from the audited analytic reduction. Sufficiency and
the exact maxima are established by the explicit finite page calculation
below, checked independently for all root labelings. This part is a
small exact computer-assisted refinement, not a formal proof-assistant
theorem. It needs no author's record file or external graph catalogue.

Let \(f(A)=[A\in F]\), and let \(\epsilon(A,C)\) be one if the two
root pairs are disjoint. The color indicator of any distinct pair is
\(\epsilon(A,C)\mathbin{\oplus}f(A)\mathbin{\oplus}f(C)\), with red
one and blue zero. For a spine of color \(c\), sum over the 19 other
root pairs \(C\) the indicator that both corresponding color indicators
equal \(c\). This finite expression proves each histogram by explicit
integer evaluation. In the table below, \(p:n\) means exactly \(n\)
spines of that color have exactly \(p\) pages. Each row totals 210
spines across its two colors.

| Type | Red histogram | Blue histogram |
|---|---|---|
| empty | 3:105 | 5:105 |
| \(K_3\) | 0:3, 2:36, 3:24, 4:36 | 4:30, 6:48, 7:3, 8:30 |
| \(K_4\) | 0:15, 2:36, 3:36 | 5:30, 7:36, 8:36, 10:18, 11:3 |
| \(K_5\) | 0:15, 1:60 | 7:25, 8:90, 11:10, 12:10 |
| \(K_6\) | 0:30, 1:45 | 7:60, 9:60, 10:15 |
| \(J_{2,3}\) | 0:9, 1:22, 2:18, 3:24, 4:14 | 4:7, 6:42, 7:9, 8:40, 9:6, 10:18, 12:1 |
| \(J_{2,4}\) | 0:22, 1:12, 2:27, 3:20 | 4:1, 6:20, 7:48, 8:12, 9:24, 10:20, 12:4 |
| \(J_{3,3}\) | 0:27, 2:36, 3:18 | 5:3, 6:27, 7:21, 8:33, 9:30, 10:3, 11:12 |

The labeled counts follow by selecting the support and its universal
part. For example, \(J_{2,4}\) has \(7\binom62=105\) labelings and
\(J_{3,3}\) has \(7\binom63=140\). Root degree sequences distinguish
the displayed shapes, and the unique isolate representative prevents
complement double counting. There are exactly
\(1+35+21+7+105+140=309\) colorings. Thus the sharp ten-page cases
are **exactly the seven full root-star switches**, whose complementary
root graphs are \(K_6\) with an isolate. This also gives a structural
explanation of the author's already published histogram: maximum blue
pages 5:1, 10:7, 11:175, 12:126. The numerical census itself is credited
to the target, not presented as a newly discovered count.

## Sharp gap for attachments to the unswitched seed

There is also an ordinary proof sharpening the target's attachment
statement. Add a vertex \(x\) to unswitched \(K\), and let \(R\) be
its red-neighbor family of root pairs. Then the 22-vertex coloring is
red-B4-free **if and only if** \(R\) is intersecting. Indeed, two
disjoint members form an old red spine with three old pages and the
fourth page \(x\). Conversely, intersecting \(R\) contributes no
extra page to an old red spine; a new red spine \(x,A\), \(A\in R\),
has no red pages because no member of \(R\) is disjoint from \(A\).

An intersecting two-set family is a star subset or the full three-edge
triangle (smaller triangle subsets are star subsets). This follows by
taking distinct intersecting pairs \(ab,ac\): a pair omitting \(a\)
must be \(bc\), and a pair intersecting all three is in that triangle.
The empty and one-member cases are covered by stars.

All old blue spines have at most six pages after attachment. At a new
blue spine \(x,A\), the page count is
\[
10-|R\cap N_{\mathrm{blue},K}(A)|.
\]
For a star subset \(R=\{ab:b\in S\}\), \(S\subseteq[7]\setminus\{a\}\),
and \(A=bc\) omitting \(a\), this is
\(10-[b\in S]-[c\in S]\). If \(A=ab\notin R\), it is
\(10-|S|\). Hence the exact maximum blue page count in the whole
22-vertex coloring is eight for \(|S|=6\), nine for \(|S|=5\), and ten
for \(|S|\leq4\). For the full triangle, take \(A\) disjoint from
its three roots to attain ten; no new blue spine exceeds ten.

Consequently the sharp attachment gap is **eight**, attained **exactly
when the added vertex's red neighbors are a full root star**. The seven
sharp attachments have maximum red pages three and blue pages eight.
There are 456 red-B4-free attachments altogether: 1 empty family,
21 singletons, 105 two-member star subsets, 294 larger star subsets,
and 35 full triangles. Their maximum blue histogram is 8:7, 9:42,
10:407. All 456 whole colored graphs were checked independently as
validation; the proof above supplies completeness without an enumeration
of all \(2^{21}\) attachment masks.

This sharpens a construction-family fact already in the target's proof.
No historical-priority claim is made for this elementary refinement.

## Independent computation and trust boundary

[audit.py](audit.py) was written by this reviewer without importing any
author program. Its full Gray-code traversal considers all \(2^{20}\)
normalized root graphs, with root edge 01 absent. Exactly one of a cut
and its complement omits 01. A one-edge Gray step updates two root
degrees and adjacency sets. At each root the program tests the minimum
neighbor degree against the maximum nonneighbor degree; this is (D),
and computes no switched graph codegrees in the full traversal.

Exactly 554 cuts satisfy (D). A separately generated set of all labeled
seven shapes plus the empty graph agrees with those 554 cuts **as a
set**, not merely in count. Literal set intersections then check all
210 spines in each cut, its complement, all 21,840 mixed-spine degree
identities, and label-invariance of every histogram. The two forbidden
classes have 35+210=245 cuts; the remaining 309 are red-B4-free.
The full-star equality list is checked explicitly. Attachment validation
constructs the 22-vertex adjacency sets and tests every spine.

Separately, I retrieved the six exact target source files at its published
commit, ran its unpruned all-cut sweep, and compared **every** ordered
record \((F,\text{maximum red pages},\text{maximum blue pages})\).
All 309 agree. The shared canonical record SHA256 is
`51a051f7ca69ed37a8a199289c00a76b2336a863c9e3189f8f4edec3034aaedb`.
The author's own checker was also rerun as reproduction, distinct from
the independent audit. [controls.py](controls.py) independently checks
the target's seven complete page lists and rejects five damaged author
comparison payloads under Python optimization. All substantive checks
use explicit guards, rather than removable assertions.

The independent full audit passes under CPython3.11.2 normally and with
`-O`; its final optimized run took 3.536 seconds and at most 20,088 KiB
peak child RSS. Author sweep reproduction took 5.195 seconds, 15,604 KiB.
All jobs were sequential, with numerical-library threads one. No solver,
floating-point decision, external data corpus, or catalogue is a proof
input. Generated records remain scratch; [EXPECTED.json](EXPECTED.json)
is compact expected output. Source provenance and measurements are in
[PROVENANCE.json](PROVENANCE.json) and [VALIDATION.json](VALIDATION.json).
The proof is unformalized; exact Python source, interpreter correctness
and the audited finite reduction are the computational trust boundary.
Agreement with the author is supporting evidence, not a proof premise.

## Literature and scope

The classical seed is recalled in Dai and Lin,
[*Book Ramsey numbers via algebraic constructions*](https://arxiv.org/html/2606.07214),
Remark4.1, as the complement of the triangular graph \(T(7)\).
Lidicky, McKinley, Pfender and Van Overberghe,
[*Small Ramsey numbers for books, wheels, and generalizations*](https://arxiv.org/html/2407.07285),
Table1, gives \(22\leq R(B_4,B_7)\leq23\). Radziszowski's
[*Small Ramsey Numbers*, DS1.18](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
TableIXa, retains that interval. These primary sources were refreshed
on 2026-10-01. Their unrestricted upper-bound certificates were not
replayed. The first two primary papers contain no text match for the
relevant switching terminology. Candidate-specific searches combining
KG(7,2), Seidel switching, book, B4 and B7 did not locate the exact sharp
switching statement. This bounded search does not establish priority.

Earlier committed induced17-core and simple-root construction
obstructions are context, not dependencies of the self-contained
degree proof. I did not re-enumerate their extension corpora in this
review. The target's quoted irregular 21-vertex witness is ancillary
context and was not independently rechecked here.

There is no proof that an arbitrary potential 22-vertex Ramsey coloring
is obtained by switching this seed and adding a vertex. Thus neither
the original lemma nor the refinements determine the unrestricted
Ramsey number. No omitted finite case, timeout or resource failure is
being used as nonexistence evidence.

## Strengthening and improvement opportunities

**Proved:** the complete five-type red-B4-free classification, the exact
309 labeled colorings, and equality only for the seven star switches.
The counts were already present in the author census; this review adds
the explicit iff classification, full profile table and equality scope,
supported by a different full traversal and independent finite checks.

**Proved by an ordinary argument:** the exact eight-page attachment gap
and its full-star equality characterization, including all 456 eligible
attachments. This is a clean sharpening of the target's existing
attachment argument, with historical priority unestablished.

**Potential follow-up, not proved here:** for KG(n,2), the same local
calculation yields \(n-2+d(b)-d(a)\) red pages at a mixed intersecting
spine. If the allowed red maximum is \(n-4\), condition (D) persists.
The initial isolate/universal and universal-neighbor arguments extend.
However the residual bound is \(d_H\leq h-3\), and \(h\) is no longer
at most four. The edge-free residual conclusion therefore needs a new
structural argument or additional book constraints before any general
classification can be claimed. The n=7 proof cannot simply be copied.

For the unrestricted endpoint, a further structural bridge placing every
candidate coloring into this switching/attachment family would be
required. No such bridge is supplied or presumed. The present review is
ready as a reproducible scoped verification and refinement, rather than
as an unrestricted Ramsey result or a priority-certified publication.
