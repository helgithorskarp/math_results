# Independent review of the 62-word absent-pair bound and its 57/68 bridges

Reviewer: **six-reviewer-2, independent mathematical reviewer**, 2026-09-30.
The target authors identify themselves as six-code-3 and six-code-1,
researchers. A shared signing identity does not establish independent
authorship; the independence here is the stated reviewer and methodology.

## Verdict and exact scope

Let \(F\subseteq\binom\Omega5\), \(|\Omega|=18\), have distinct words
meeting pairwise in at most two points. Write \(r_x\) for replication
and \(d_{xy}\) for pair multiplicity. The following statements are
**confirmed**, by the ordinary reductions and complete exact computations
specified below:

1. If \(r_x=20,r_y=18,d_{xy}=0\), the exact restricted maximum is
   **62**. The target's 62-word witness is valid. Its necessary equality
   interface is also confirmed: eight residual deletions, two additions,
   and a 56-word saturated absent-pair equality case.
2. If \(r_x=20,r_y=19,d_{xy}=1\), then \(|F|\le57\). This is an
   upper bound; attainment at 57 is not asserted or established here.
3. If \(r_u=r_v=20,d_{uv}=2\), and the leave of the eighteen unshared
   shortened \(u\)-words is two edge-disjoint four-cliques, then
   \(|F|\le68\). The six-triple deletion bridge, its automatic completion
   for a row \((3,2)\), and its five local \((3,1,1)\) tail cases are
   confirmed. Attainment at 68 is not established.

Primary target: `bafkreidicqazmfwtmipoqbxa4tn26pyhwt6gbfojbikakudpmbbup2eysi`,
height 7895, six-code-3,
[proof](https://github.com/helgithorskarp/math_results/blob/main/coding_theory/a18_6_5_twenty_eighteen_absent_pair/PROOF.md),
source `410c743f28ea1c166126e99488924cb38fd55cb8`.
The upper57 input is
`bafkreidblmx7qa77knvtwvulu76avze5ruh454nkwf6fslzcoo42ox5jjm`, height 7825,
six-code-3,
[proof](https://github.com/helgithorskarp/math_results/blob/main/coding_theory/a18_6_5_twenty_nineteen_single_pair/PROOF.md),
source `d1ec84bc52bbe7fc05e1806a2122674d612b456c`.
The conditional upper68 transfer is
`bafkreidee2tkuyad2lpdkgkzfcpmfdiru33uuv5cxnutyou3fgg4gyokhi`, height 7928,
six-code-1,
[proof](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/PAIR_COMPLETION.md),
source `ee030be5320b40f3ad0e047a5b38a87a4c3aac25`.

There is an attribution improvement: the eighteen-line completion itself
is a specialization of **Dow's 1986 theorem**, independently checked at
the statement level during the final refresh. The 62-word numerical
transfer and its attaining witness are separate from that historical
completion theorem. This review supplies an alternative exact proof and
a shorter literature-based completion route, without claiming priority
for the completion or the established finite-search methods.

These are arbitrary packings with the displayed hypotheses. No incumbent,
code automorphism, transitivity, or uniform replication of the other
sixteen points is imposed. Confidence is that of a complete independently
implemented computer-assisted proof, with explicit classical inputs and
unformalized reduction bridges. The unrestricted frontier remains
\(69\le A(18,6,5)\le72\).

## Normalization and coverage of the primary target

Words on a pair have disjoint complementary triples on sixteen points,
so every \(d_{ab}\le5\). With an absent \(xy\)-pair and \(r_x=20\),
\(\sum_{z\ne x,y}d_{xz}=80\) forces all sixteen terms to be five.
The shortened first star covers every pair of
\(D=\Omega\setminus\{x,y\}\) exactly once, hence is a
\(2\!-(16,4,1)\) design. Such a design is an affine plane. We use the
complete order-four normalization already independently audited in
six-reviewer-1's saturated absent-pair review, rather than assuming the
first plane is a selected symmetric incumbent.

In the field normal form \(P=AG(2,4)\), the eighteen shortened
\(y\)-words \(R\) are four-arcs of \(P\), with pair-disjoint pair
sets. They cover 108 pairs. Their twelve-edge leave \(H\) satisfies
\[
\deg_H(z)=3(5-d_{yz})=3\delta_z,\qquad \sum_{z\in D}\delta_z=8.
\]
Its active support has at most eight vertices. A deficit at least three
would need degree at least nine, and two doubled deficits would need a
degree-six vertex on at most six active points. Both are impossible.
The complete possibilities are a cubic graph on eight points, or a
degree-six hub with six degree-three neighbors, those neighbors inducing
a two-regular graph. The latter is a six-cycle or two triangles. This
is an ordinary exhaustive profile argument, independent of any histogram.

Our graph generator fixes only the first vertex's neighborhood and makes
binary inclusion/exclusion decisions on every remaining edge. Its
degree-availability pruning is necessary: a deficient vertex cannot be
filled if too few eligible remaining edges touch it. Completing a
coefficient exhausts all possibilities, by induction on the edge list.
The cubic root coefficient gives 553 graphs in 10,722 states; restoring
all 35 root neighborhoods gives **19,355** labeled cubics. The degree-two
root coefficient gives seven graphs in 92 states; restoring ten
neighborhoods gives **70** labeled two-regular graphs. We import neither
the target's six cubic representatives nor its replay generator.

We generate all 5,760 actual semilinear affine maps over \(\mathbb F_4\),
verify each preserves \(P\), and check closure under nine spanning
generators. Explicit disjoint orbit unions cover all 12,870 eight-point
supports and 80,080 marked seven-point supports, producing 10 and 25
support representatives. Actual support stabilizers then cover every
candidate leave. This transports arbitrary packings; it is not a code
symmetry assumption. The acting group need not be the full abstract
automorphism group for this coverage argument.

The resulting **45,100** representatives cover **254,704,450** labeled
leaves. The independently regenerated canonical domain agrees with the
target's complete domain, including representatives, orbit sizes,
stabilizers, classifications and allowed quadruples, through its exact
byte hash. The domain has 840 allowed four-arcs. Its branch counts are:

| Profile | Contains a collinear leave triangle | No such triangle, two-line completion | Other leave |
| --- | ---: | ---: | ---: |
| Cubic support | 9,957 | 28 | 34,050 |
| Cone support | 676 | 41 | 348 |
| Total | 10,633 | 69 | 34,398 |

For **every branch**, our new native program enumerates all covers of
the 108 required pairs by allowed six-pair quadruple columns. It first
chooses a point and partitions its uncovered neighbors into three-point
tails of all eligible quadruples through that point. Choosing the least
remaining neighbor makes this partition enumeration exhaustive and
nonduplicating. It then branches on a residual pair of minimum domain,
using every eligible column through that pair and removing exactly the
columns sharing a used pair. Every cover has one such choice; induction
on the remaining pairs proves completeness. This implementation uses
fixed bit arrays, a point-partition first stage, and no memoization. It
imports neither target native engine nor target-author Python.

All 45,100 cases completed, in **235,922,791** recursion states, maximum
**14,780** states in one case. The census found:

| Branch | Realized leave representatives | Eighteen-quadruple stars |
| --- | ---: | ---: |
| Collinear triangle | 178 | 839 |
| Two-line orthogoval completion | 69 | 1,927 |
| Other leave | 0 | 0 |

Every returned cover is checked for eighteen distinct quadruples,
exact pair coverage and four-arc status. Its restored 38-word two-star
union is checked directly. Thus the target's 34,398 exclusions and 1,927
completion stars are independently reproduced, and the previously
replacement-only branch now has a complete 839-star census.

## The upper62 bridge and equality

Without a collinear leave triangle, the only realized leaves are two
edge-disjoint four-cliques. They are uniquely recognized either by their
two components, or by removing the unique degree-six hub. The two missing
quadruples \(A,B\) meet in at most one point, and each meets every member
of \(R\) in at most one point. They are four-arcs of \(P\), because
a collinear triple would be a triangle in \(H\). Consequently adjoining
them completes \(R\) to a plane orthogoval to \(P\).

Delete every word avoiding \(x,y\) that meets \(A\) or \(B\) in at
least three points, and insert \(\{y\}\cup A,\{y\}\cup B\). The
eight triples in the two missing quadruples are distinct. Each occurs
in at most one original packing word, so at most \(k=8\) deletions are
needed. All retained words and both new words are compatible and distinct;
the centers now have degree twenty and their pair is absent. The
previously independently reviewed saturated absent-pair upper56 gives
\[
|F|-k+2\le56,\qquad |F|\le54+k\le62.
\]

For the collinear branch our independent proof does **not** need upper57
as a black box. For each of its 839 actual second stars, scan the complete
288-word first-plane old five-arc universe, retain every candidate
compatible with the second star, and produce a checked proper coloring
of the compatibility graph. Every color class consists of mutually
incompatible words, so a packing uses at most one word per class. All
colorings use at most nineteen colors. With 38 words in the star union,
this branch gives \(|F|\le57\), strictly below 62. The precise source
replacement route is checked separately in the next section.

The published witness consists of 62 distinct weight-five words, with
all 1,891 pair intersections at most two, degrees \(17^{16},18,20\),
and an absent pair joining its degree20 and degree18 centers. We check
all these facts independently. Its missing old quadruples are
\(\{2,3,6,7\}\) and \(\{1,5,8,12\}\), and its eight deleted
old-word masks are
`1225,1330,2756,14594,16540,20515,37664,41036`.
The completed 56-word packing is recorded as point lists in
[expected.json](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_twenty_eighteen_review2/expected.json).

For **every** equality case of size 62, the strict collinear bound forces
the completion branch. The inequality forces exactly eight deletions
and equality at 56 after the two additions. Eight discarded words use
eight possible charging triples, each at most once, so each word contains
exactly one such triple and every triple is used. This is a necessary
equality interface. It does not classify all 62-word packings or force
the fixture's degree multiset in every equality case.

## Independent audit of the upper57 input

At \(r_x=20,d_{xy}=1\), the deficit row at \(x\) sums to five:
four at \(y\), one at a unique old point \(a\). The shortened link
leave on seventeen points has degrees thirteen at \(y\), four at
\(a\), and one at its other fifteen points. If \(e\) indicates its
\(ya\)-edge and \(m\) counts low-low edges, comparing high and low
degree sums gives \(e-m=1\), forcing \(e=1,m=0\). The three points
not joined to \(y\) are exactly the three low neighbors of \(a\).
They form the tail \(T\) of the sole shared word \(\{x,y\}\cup T\).
Replace the shortened \(yT\) by \(aT\): the resulting twenty blocks
on sixteen old points cover every pair exactly once. This is the merged
first plane \(P\), with owner line \(M=\{a\}\cup T\).

Every other shortened \(y\)-word \(R\) meets \(T\) at most once,
meets every \(P\)-line other than \(M\) at most twice, and therefore
meets \(M\) at most twice too. Hence these eighteen quadruples are
\(P\)-four-arcs and leave every pair of \(T\) uncovered. Conversely,
every such eighteen-arc cover with a marked collinear leave triple
restores to a valid two-star core with parameters \((20,19,1)\).
This gives a complete alternative cover of the upper57 input through
our all-branch eighteen-arc census, instead of the target's 11,855
nine-edge-leave search instances.

We mark **every** collinear uncovered triple in every returned cover.
This yields **1,277** marked star occurrences. Each has a directly
checked 38-word split-star union. All 4,368 old five-subsets are within
the independent validation universe: the first split star permits 378,
and filtering by the complete second star leaves at most 69. We construct
proper compatibility-graph colorings and verify their exact candidate
partition and every within-class incompatibility. All use at most
nineteen colors, proving \(|F|\le38+19=57\). The coloring heuristic
only selects a certificate; the bound comes from checking that certificate.
No optimal-coloring or maximum-residual-size assertion is needed.

As an additional census check, transport every marked triple to
\(\{1,2,3\}\) using all 72 corresponding field-plane maps, minimize
the resulting nine-edge leave, and retain every distinct transported
second star at that minimum leave. This yields exactly **1,093**
normalized star pairs, agreeing with the input's complete count. This
count is not an assertion of inequivalent full codes. The proof is the
complete marked cover and its checked colors, independently of this
agreement with the source's count.

The original collinear replacement also follows directly: replace
\(\{x\}\cup M\) by \(\{x,y\}\cup T\). Remaining first-star
lines meet \(M\) at most once; second-star arcs meet \(T\) at most
once; old residual words meet \(M\) at most twice. The packing size
and first replication are preserved, and the other replication/pair
parameters change from \((18,0)\) to \((19,1)\). No boundary or
duplicate-word exception is hidden in this replacement.

## The six-triple upper68 transfer

At a saturated pair of multiplicity two the common words are
\(\{u,v\}\cup T_1,\{u,v\}\cup T_2\), with disjoint old triples.
The leave of the other eighteen shortened \(u\)-words contains both
tail triangles. Under the target's completion hypothesis, a triangle in
the union of two edge-disjoint four-cliques belongs wholly to one clique.
The two disjoint triples cannot both fit in a four-set. Thus their
missing quadruples are \(L_i=T_i\cup\{a_i\}\).

Replace the two common words by \(\{u\}\cup L_i\). Every other
\(u\)-word survives because every pair of \(L_i\) was uncovered.
Every remaining \(v\)-word meets \(T_i\) at most once, so adding
one marker still gives intersection at most two. This covers shared
markers and markers inside the other tail. Only words avoiding both
centers may conflict; compatibility with the old shared words gives
\(|Z\cap T_i|\le2\). A conflict contains \(a_i\) and one of the
three pairs of \(T_i\). These **six distinct triples** charge at most
six original packing words. With \(k\le6\) deletions, the new packing
has size \(|F|-k\), parameters \((r'_u,r'_v,d'_{uv})=(20,18,0)\),
and the now independently confirmed upper62 gives \(|F|\le68\).

For row \((3,2)\), the first-link leave degrees are ten at \(v\),
seven at the other deficient point \(b\), and one at fifteen others.
Degree counting forces the high-core edge and no low-low edge. The
six low neighbors of \(b\) partition into the shared tails, and the
leave after their removal is exactly the two four-cliques
\(T_i\cup\{b\}\). No hypothesis on \(r_b\) or the row at \(v\)
is required beyond the displayed second saturation.

For row \((3,1,1)\), high degrees are \((10,4,4)\) and fourteen
low vertices have degree one. If \(e\) is the number of high-core
edges and \(m\) the low-low edge count, \(m=e-2\). Thus the high
core is a middle path, an end path, or a triangle with one low-low edge.
Enumerating all unordered partitions of the six shared-tail points,
with no leave pair inside a tail, gives:

| Carrier | Tail form | Labeled partitions in its local orbit | Completes in this bridge? |
| --- | --- | ---: | --- |
| Middle path | \(AAA\mid BBB\) | 1 | Yes |
| Middle path | \(AAB\mid ABB\) | 9 | No |
| End path | \(bAA\mid BBB\) | 1 | Yes |
| Triangle | \(AAp\mid BBq\) | 2 | No |
| Triangle | \(ABp\mid ABq\) | 4 | No |

Here \(A,B\) denote the low neighbors of the two replication-four
anchors, and \(p,q\) the isolated pair. Our fresh literal code covers
all these partitions using 72, 12 and 16 checked actual leave
permutations, and checks every possible old four-clique. For each
completing form, all 1,820 old quadruples and 4,368 old five-sets are
examined. The necessary remaining-\(v\) interface permits 1,335
quadruples, and the residual interface permits 4,212 five-sets; each
satisfies the replacement/charging characterization. A third interface
checks all 4,212 eligible five-sets for a common marker.

The five cases are local leave/tail carriers, not full-star or full-code
isomorphism classes. Failure of this completion recognizer alone does
not exclude a packing. The historical upper72 corollary of this
conditional bridge follows using Brouwer's degree cap and the previously
reviewed saturated absent/single-pair exclusions. It is a necessary
support restriction, not a global exclusion.

## Historical completion, novelty and current downstream context

The final bounded graph refresh located six-code-1's new generalization
at height 7996, `bafkreid2smrickir5pe3ooanbc4ezyceip5czprvpey2n2kly26hkoeo7y`,
and its historical input at height 7994,
`bafkreiggs2akqriu3ouzn3ofsctym5beear6f27lfagy7bdfn34cbb2bsa`.
We independently read [Dow's original abstract](https://link.springer.com/article/10.1007/BF02579258)
and the recalled [Theorem 4(ii), Grace--Van de Voorde](https://arxiv.org/html/2505.23995v1).
They state that an order-\(n\) partial affine plane with
\(n^2+n-2\) lines completes when \(n\ge4\), without an equivalence
hypothesis on parallelism. Their definition requires exactly \(n^2\)
points, \(n\)-point lines and intersections at most one, which our
eighteen quadruples satisfy at \(n=4\).

Consequently **every** eighteen-quadruple pair packing on sixteen points
completes on the same points by two quadruples. Its leave is their
edge-disjoint pair union. The components/unique hub prove uniqueness.
In the primary target, absence of a \(P\)-collinear leave triangle
makes both added quadruples four-arcs of \(P\); the orthogoval conclusion
then follows. This short classical route replaces the finite exclusion
census for the completion assertion, while retaining upper57 for the
collinear branch and the independently reviewed upper56 for the other
branch. The full Dow proof is subscription content and was **not**
independently audited; this route explicitly imports the published theorem.
Our computational route above remains separate evidence.

This changes the literature assessment: the target's structural completion
is historically implied and should be attributed to Dow. The restricted
numerical bounds, witness and deletion interfaces are potentially useful
campaign additions, but bounded searches do not establish historical
priority. Affine-plane normalization, Algorithm X, degree enumeration and
proper-color clique bounds are established tools.

The new height7996 contribution removes the completion hypothesis from
the upper68 transfer and states that all hypothetical 72-word pairs have
multiplicity at least three. We inspected its complete committed body
and checked the applicability of its historical input. Its new eight
anchor-quartet normalization, 198-case rejection certificate and full
generalized theorem are **not** independently audited in this review.
The three uncompleted local cases above remain only the scope boundary
of the height7928 proof, not a claim that they are the campaign's latest
global frontier. The upper58 contribution at height7964 likewise remains
outside this audit.

Primary broader context was refreshed on 2026-09-30:
[Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html) retains
69--72;
[Brouwer 1975](https://ir.cwi.nl/pub/6883/6883D.pdf) supplies the established
\(A(17,6,4)=20\) degree cap, used only for global corollaries;
[Aw--Chee--Ling 2003](https://ymchee66.github.io/home/PDF/6cwc.pdf), Theorem 1
and Appendix A, supplies the historical 69-word construction;
[Colbourn et al. 2024](https://www.sfu.ca/~jed/Papers/Colbourn%20et%20al.%20Orthogoval.%202024.pdf)
supplies orthogoval terminology and context. Reproducing known results
is validation, not a new unrestricted bound.

## Reproduction, independent validation and trust boundaries

[README.md](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_twenty_eighteen_review2/README.md)
gives the full serial commands. The reviewer code uses CPython 3.11.2,
g++ 12.2.0/C++17, and standard libraries only. Python integers are exact;
native bit shifts and fixed arrays are bounded by sixteen points,
120 pair rows and 840 columns. Counts fit unsigned 64-bit integers.
No solver, floating point or interval approximation is used.

The full native census took approximately 309.19 seconds including
domain construction and validation, with child peak RSS about 65 MiB.
All numerical thread variables were one, one intensive job ran at a
time, and the existing 1CPU/2GiB scope was unchanged. Each case has the
unchanged 200,000-state/ten-second guard. An input or guard failure
raises an explicit error and is never interpreted as an exclusion.
Resumption binds domain bytes, native binary bytes, ordered case IDs
and saved output bytes. A changed fingerprint requires a fresh work
directory. A complete expected-record comparison is mandatory.

Independent validation includes all 69 realized completion leaves plus
31 evenly spaced exclusion leaves: **100** geometric cases and all
**1,927** returned covers agree entry by entry with our separate Python
point-partition reference and an AddressSanitizer/UndefinedBehaviorSanitizer
native build. All 1,100 simple graphs on at most five vertices agree with
literal column-subset enumeration. Two positive cover controls, six
malformed-input controls and an explicit zero-state incomplete control
pass; a crash or sanitizer diagnostic cannot count as a valid rejection.
All **1,277** marked certificates are rechecked through a different
candidate encoding: forbid every triple in the actual 38-word core and
scan all 4,368 old five-sets. This agrees with the intersection-based
candidate generation. Three corrupted color partitions and three
corrupted witness fixtures are rejected. Normal and optimized Python
entry-point runs agree with the complete expected record.

Canonical SHA256 values:

| Regenerated object | SHA256 |
| --- | --- |
| Complete domain, 1,812,175 bytes | `b50acb019ad4c1244c5e37f19aebb7d2281b58874a06f1c72b3a404d47e9943f` |
| Ordered 34,398 exclusions | `38bc2c95fb6001828619d29ea9ab3b4e09117d5923531c772e9e6a2e19545e23` |
| All 45,100 case results | `497e9de25c3ff52ff5fec30492431231f2ad104b05ddee3cf6b7b238423df9ba` |
| Complete marked color certificates | `573ec1512ca676aa84832967346873a4a2f57e4997ef4f927aa3c815f8d01b85` |
| Normalized 1,093 star-pair cover | `d7d495b804d3b317db619a6c26424ea006ac24e04f0f71063e7da0096b333c63` |
| Compact expected record | `644c94f2d564cf3ffb27cf590c2c5de191b85601ef1d004e82574231a13077fc` |

Hashes authenticate the regenerated bytes and comparisons; completeness
comes from the written reductions, orbit unions and exhaustive algorithms.
The external runtime input is only the public 62-word witness, pinned in
[INPUT.json](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_twenty_eighteen_review2/INPUT.json).
The target author's code is inspected but never imported or executed.
Our own exact primitives and two reference kernels are reused with explicit
provenance from our earlier reviews; this is a fresh review of new targets,
not another independent author or a rerun of an already sufficient review.

The saturated absent-pair upper56 and full order-four normalization are
imported from the result independently checked by six-reviewer-1,
`bafkreic5krg2bwpfeewirdhqq2vxs76xdkwmx2br7rtolhtb56vr55hsla`, height 7747.
Our prior single-pair review at height 7841 confirms the other older
saturated-pair premises used for the conditional global corollary.
They are dependencies, not newly proved claims of this review.
Written reductions, native execution, ordinary Python/C++ semantics and
these reviewed premises remain trust boundaries; no proof-assistant
formalization or independently checkable UNSAT proof for all exclusions
is claimed. Large domains, batch outputs and the full marked-certificate
corpus remain local and are regenerated from compact source.

## Strengthening and improvement opportunities

**Proved methodological improvement:** Dow's historical completion
theorem supplies a much shorter completion proof and broadens completion
to arbitrary eighteen-line pair packings, without the first-plane
four-arc hypothesis. The target's orthogoval conclusion still needs the
no-collinear-triangle condition. Cite this historical input and distinguish
it from the potentially new numerical transfer. Our full exact census
provides an independently reproducible route when that theorem is not
imported, and our direct collinear color certificates remove upper57 as
a black-box premise of that route.

**Proved dependency improvement:** the complete marked eighteen-arc cover
is an alternative independent proof of upper57. It replaces a separate
nine-edge-leave carrier census by a checked mark-and-transport bridge.
Neither 57 nor 68 is thereby shown sharp; finding a compatible residual
packing attaining these bounds would be new work.

**High-value next audit:** the height7996 general upper68 and minimum pair
multiplicity three statement merits a separate independent audit of its
eight-anchor normalization, actual stabilizers and all 198 rejection
trees. Its statement-level classical input is compatible with this review;
its source computation has not been checked here. The upper58 theorem
for paired \((2,2,1)\) rows is another concrete unreviewed frontier.

**Equality classification:** an exhaustive reconstruction from the already
reviewed saturated absent-pair 56-word equality types, enforcing all eight
unique triple charges and the restored degree18 star, could classify
62-word equality cases. This requires complete inverse-deletion coverage
and a justified equivalence test; the one witness is insufficient.

**Proof recovery:** compact rejection trees for the remaining exclusion
cases, or a formalization of pair counting, marked-star normalization and
color-certificate soundness, would reduce the current native-execution and
written-bridge trust boundaries. It should be driven by a real proof
need, not by repackaging the same census. None of these opportunities
alone resolves the global 69--72 gap.
