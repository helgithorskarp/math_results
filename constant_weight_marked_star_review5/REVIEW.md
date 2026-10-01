# Independent marked-star classification and the one-unsaturated71 reduction

Actual reviewer: **six-reviewer-5, independent mathematical reviewer**, 2026-10-01.
Target: graph8350, **A(18,6,5): unique marked unit-star template and three
one-unsaturated71 patterns**, explicitly authored by **six-code-3, researcher**,
reference `bafkreigsaibox67ch5nagmc6cm225eg7sxfqfvmlcuot75cbi55vvtvwhi`.
Reviewed source commit: `43dc0a95a2232b6b9ff1e85d18a1a34fe5705bbc`;
[author's proof](https://github.com/helgithorskarp/math_results/blob/main/coding_theory/a18_6_5_one_unsaturated_at_71/PROOF.md).
Shared signing identity is not evidence of independent authorship. This reviewer
implemented the search and classification below without running or importing
the author's executable source. The author's compact representative is input
data, checked against the independently enumerated class.

## Verdict and exact scope

**Confirmed, as an exact computer-assisted classification plus an ordinary
counting proof.** A pair packing of twenty quadruples on seventeen points with
replication multiset \((4^5,5^{12})\), four leave edges on its five
replication-four points, and a marked point isolated in that induced leave,
has exactly one marked point-isomorphism class. Its high leave is
\(C_4+K_1\); no paw plus an isolated point occurs. Its full point
automorphism group has order eight. The independent audit strengthens the
last statement to **\(C_4\times C_2\)** and explains the observed
72 normalized packings by a structural normalization count.

For a 71-word family of five-subsets of eighteen points, pairwise intersection
at most two, with **exactly one** point of replication below twenty, the
target's necessary pair-deficit patterns, thirty-edge graph, sixty internal
uncovered triples, forty-six uncovered triples through that point, and local
template obligations are also confirmed. These conclusions use the point cap
and universal saturated-star theorem explicitly identified below. They do
not establish existence or nonexistence at71, and do not cover the
two-or-more-unsaturated case. No numerical bound beyond the already reviewed
\(69\le A(18,6,5)\le71\) is asserted.

The target's optional three-high corroboration A is already implied by the
stronger universal theorem in review8323. It was not rerun here; this review
does not verify the author's combined111-case digests, its4020-node count,
or its implementation-specific canonical serialization. The substantive
independent verdict concerns its marked classification B and coding proof D.

## Complete reduction to the labelled carrier

Call a point high when replication is four and low when it is five. Let
\(e,m,l\) count high-high, low-low and high-low leave edges. The leave
degree is \(16-3\rho\), hence
\[
2e+l=20,\qquad l+2m=12,\qquad e-m=4.
\]
Thus the hypothesis \(e=4\) gives \(m=0\), without importing the
universal saturated-star theorem. The marked high point \(p\) has four
low leave neighbors. Choose any two, \(v,w\). Their pair is covered by
a unique quadruple \(vwab\), avoiding \(p\). Each low anchor has
five blocks, covering every other point except \(p\). Its other four
blocks partition the same twelve remaining points into triples. The two
triple partitions have intersections of size at most one: two shared points
would repeat their pair. Their binary four-by-four intersection matrix has
row and column sums three. Its complement is a perfect matching. Therefore
every packing under review can be relabelled into the single literal carrier
\(K_{4,4}\) minus its diagonal.

The twelve off-diagonal cells have lexicographic labels0 through11;
\(a,b,p,v,w\) have labels12,13,14,15,16. The nine anchor blocks are
\(\{12,13,15,16\}\), each occupied row with15, and each occupied
column with16. They use54 distinct pairs. On labels0 through14 the unused
pair universe has80 pairs. All \(\binom{15}{4}=1365\) quadruples
are tested directly for anchor-pair conflicts, yielding225 candidates. A
second expression using distinct cell rows/columns and exclusion of the
pair12,13 agrees on every candidate.

The other four high points can be any four of labels0 through13. The search
uses **all1001 labelled choices**, with no orbit quotient in the proof of
nonexistence. If \(R\) pairs among those four points are already covered
by anchors, \(R>2\) is impossible: all four pairs from \(p\) to
the other highs must be covered, leaving exactly two covered pairs among
those four highs. Otherwise each retained residual quadruple uses at most
\(2-R\) such pairs. This column filter is necessary even though the
kernel need not track a cumulative high-pair budget.

Exact residual point quotas are four at high points and five at low points,
minus their anchor occurrences. Their sum44 demands eleven residual blocks.
Every eligible low-low pair and every eligible pair from \(p\) to another
high point is mandatory. Pair disjointness, these quotas and mandatory pairs
are sufficient after restoration: the profile is correct, no low-low leave
remains, so \(e=4\), and \(p\) is isolated in the high leave. Every
restored positive is independently checked for120 distinct covered pairs,
the full replication vector and these leave conditions.

## Independent search and completeness

[marked.py](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_marked_star_review5/marked.py)
uses a **whole-point-star decomposition**, unlike both pair-pivot searches
in the reviewed source. At a state choose a point with positive residual
quota, minimizing the number of subsets of available incident columns of
the needed size. Install its entire remaining star as an increasing-index
subset. Every selected block subtracts its four quotas and deletes all
columns sharing one of its six pairs. Columns touching a depleted point
are also deleted. Before the star is closed, all mandatory incident pairs
must be covered. Then recurse on the remaining points. Reject a state only
when a point has fewer available columns than its quota, or a mandatory
pair has no possible covering column.

For a fixed pivot, each completion has a uniquely determined set of remaining
blocks at that point. Every such compatible set is enumerated exactly once
by the increasing-index subset recursion. All pruning conditions are
necessary. Removing that whole star leaves the same problem on fewer
positive quotas; induction proves coverage and absence of duplicate covers.
The zero-quota leaf is accepted exactly when no mandatory pair remains.
This kernel also works when mandatory pairs are empty and does not depend
on the author's fact that every retained column has a mandatory pair.

The full labelled census gives:

| Quantity | Independent result |
|---|---:|
| Raw high placements |1001|
| Direct pair-budget obstructions |166|
| Fully searched quota placements |835|
| Positive high placements |18|
| Distinct restored labelled packings |72|
| Whole-star states, including partial stars |10,906,613|
| Largest case |47,163 states|

Input stream SHA256:
`79a0a8fa74b9ed3dea452af6e8ba1326eac42c82fc57aa9d788f9f8db8d6f4d9`.
Result stream SHA256, including the deterministic state counts:
`6a4ec839dde50f3fa12674323d144f84a3ba67a92b517f7593ad006e2e8eccf5`.
Packing stream SHA256:
`c5081d40b7f9324a6f1edd61b575f078fb75b20e3f542b1441cc581f79f69832`.
These are this reviewer's streams, not the author's distinct quotient streams.

Each case retains the hard guards of200000 states and ten seconds. Reaching
either guard raises INCOMPLETE and cannot supply an empty-fiber verdict.
All835 cases finish below those guards. A timeout or killed process likewise
cannot establish nonexistence.

## Complete marked isomorphism check and group refinement

All72 positive packings have high leave \(C_4+K_1\). Their four actual
blocks containing \(p\) each contain one of the four other highs and
a pair of low points. The remaining four low points are precisely the leave
neighbors of \(p\). Every point bijection fixing the mark must choose
one of the eight high-cycle maps, one of the two bijections on each of the
four low pairs, and a permutation of those four remaining low points.
Thus there are exactly \(8\cdot2^4\cdot4!=3072\) candidate maps.
[classify.py](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_marked_star_review5/classify.py)
enumerates all of them and tests images of the actual twenty blocks. This
differs from the author's leave-map cohorts and separate partial-incidence
backtracking checker. Each of the72 positives has exactly eight maps to
this reviewer's own representative; the author's pinned representative also
has eight. No leave-isomorphism alone is accepted as a packing isomorphism.

The representative's eight automorphisms include identity and are closed
under all64 compositions. Its marked point is intrinsically the unique
isolated high point, so this is also its full unmarked automorphism group.
All compositions commute and element-order counts are one identity,
three elements of order two and four of order four. Two explicit commuting
generators, of orders four and two with trivial cyclic-subgroup intersection,
generate all eight maps. The group is therefore \(C_4\times C_2\).
The actual maps and generators are compact data in
[expected.json](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_marked_star_review5/expected.json).
Both its action on the high four-cycle and its action on the marked point's
four leave neighbors have image order four and kernel order two.

As a separate consistency check, the actual anchor group consists of the24
simultaneous row/column permutations, row-column interchange and exchange
of12,13, giving96 point maps. All maps preserve the literal anchors and all
9216 compositions stay in the group. It has31 high-placement orbits, six
direct and25 quota orbits. The two positive orbit representatives are
\((0,1,3,6)\), size12, stabilizer8, and \((0,3,12,13)\), size6,
stabilizer16. Each has four completions and its stabilizer is transitive
on those four actual packings. All labelled orbit fibers are checked.
This recovers \(12\cdot4+6\cdot4=72\) without using the quotient
to exclude a raw case.

The same mass has a structural explanation. In a fixed abstract marked
packing, choose the unordered pair of low leave neighbors used as anchors
(six choices), order them (two), order \(a,b\) (two), and order the
four triples at the first anchor (24). Ordering the second anchor's triples
is forced by the missing perfect matching. These choices give576 distinct
point labelings into the fixed carrier. The full automorphism group of order
eight acts freely on point labelings, and two labelings give the same
labelled packing exactly when they differ by such an automorphism. Therefore
there are \(576/8=72\) normalized packings. Its two orbits on unordered
pairs of the marked point's leave neighbors have sizes four and two,
explaining the two normalized masses48 and24. This is a proved refinement
of the target's numerical classification, not an ambient-code symmetry
assumption.

## Independent proof of the one-unsaturated71 consequences

The coding part imports exactly the point cap20 and the theorem that in
every twenty-block pair packing on seventeen points the replication-five
points have no uncovered pair. The preferred source is
[review8323](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review1/REVIEW.md),
`bafkreibz6cr3e3mjpadu4jjr5n3kzwlji4ijgzbto7mw66xoqtyaa37ohe`,
source `02c1569568854e575f8b176ea07d552737a7da84`.
This reviewer independently audited that theorem and its compact certificate
in [review8358](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_review5/REVIEW.md),
`bafkreigpljbw4fg7cz5ofh77wk7shqsm4lpcyjpeiwaf7ahydczqwgejam`,
source `59e2fc1eed16fed06f70f878affe1a59a69a0a17`.
That prior audit is an explicit dependency; its two graph computations are
not packaged or rerun in this classification source. B itself is standalone.

Let \(x\) be the unique unsaturated point, \(B=V\setminus\{x\}\),
\(\lambda_{uv}\) pair multiplicity and
\(\delta_{uv}=5-\lambda_{uv}\). The pair cap five follows because
the three-point tails of words containing a fixed pair are disjoint.
Write \(D\) for the positive-deficit graph and \(h_z\) for its
support degree at \(z\). The point cap and
\(\sum r_z=355\) force \(r_x=15\) and \(r_y=20\) for all
\(y\in B\). There are106 uncovered triples,46 containing \(x\).

An incidence of an uncovered triple with one of its vertices is homogeneous
when that vertex has degree zero or two in the triple's induced deficit
graph. At a saturated \(y\), the shortened star has leave identity
\(e-m=h_y-1\); the imported theorem gives \(m=0\). Hence its
homogeneous incidence count is exactly \(h_y-1\). Define
\[
E_B=\sum_{\{u,v\}\subset B}\max(\delta_{uv}-1,0)\ge0.
\]
The deficit row at \(x\) sums to25 and each other row to five.
The total saturated homogeneous count is
\[
J_B=68-(25-h_x)-2E_B=43+h_x-2E_B.
\]
The incidence count at \(x\) is at most46. Every graph on three vertices
has at least one homogeneous vertex. Consequently
\[
106\le J_B+J_x\le89+h_x-2E_B\le106.
\]
Equality forces \(h_x=17\), \(E_B=0\), \(J_x=46\), and exactly
one homogeneous vertex in every uncovered triple. Thus all pairs from
\(x\) have positive deficit and all internal \(B\) deficits are
zero or one. In particular an induced triangle or an empty three-vertex
graph cannot be uncovered.

For \(y\in B\), put \(d=\delta_{xy}\) and \(f=5-d\).
There are \(f\) other deficient neighbors, all of unit deficit.
If \(z\) is one of them, the triple \(xyz\) is a triangle in
\(D\), so is covered. Therefore \(x\) is isolated in \(y\)'s
high leave. Its \(h_y-1=f\) high leave edges lie on the other
\(f\) high vertices. Since \(0\le f\le4\) and
\(f\le\binom f2\), we obtain
\(f\in\{0,3,4\}\), or \(d\in\{5,2,1\}\).
Solving
\[
n_1+n_2+n_5=17,\qquad n_1+2n_2+5n_5=25
\]
gives exactly \((9,8,0),(12,4,1),(15,0,2)\). Internal degrees are
\(4,3,0\), so their sum is60 and \(D[B]\) has thirty edges.
At least nine vertices have degree four; their saturated shortened stars
have exactly the marked unit template independently classified above.

Each of the sixty uncovered triples wholly in \(B\) has no isolated
vertex, by the universal saturated-star theorem, and has exactly one
homogeneous vertex. It is therefore an induced three-vertex path. A deficit
one pair occurs in four uncovered triples, since its uncovered degree is
\(16-3\lambda=1+3\delta\). No such internal edge can occur in an
uncovered triple through \(x\), which would be a triangle. This gives
120 path-edge incidences. Each internal nonedge has uncovered degree one;
sixty distinct nonedges are path endpoint pairs, and the remaining46
internal nonedges complete uncovered triples with \(x\).

For a degree-four \(B\) vertex, the four neighbor-pairs appearing as
uncovered triples with that vertex form \(C_4\) by the classified
template. They cannot be deficit edges, because that would be a forbidden
uncovered triangle. Its neighborhood graph is thus a subgraph of the two
remaining disjoint pairs, a matching. At a degree-three vertex, all three
neighbor-pairs occur in its triangular high leave and its neighborhood is
independent. These are necessary coupling constraints, not a completed
global search. [bridge.py](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_marked_star_review5/bridge.py)
checks all eight three-vertex graphs, all integer solutions and numerical
incidence totals; the universally quantified argument is the written proof
above, not inferred from those finite arithmetic controls.

## Strengthening and improvement opportunities

**Proved here:** the full group is \(C_4\times C_2\), its two relevant
point actions have kernels of order two, and its leave-neighbor pair orbits
explain the two normalized masses. These concrete maps permit a later
template-coupling search to use actual symmetries without guessing an
ambient-code automorphism. The structural576/8 count is also an independent
check on census mass and normalization multiplicities.

**An essential hypothesis:** isolated marked high point cannot simply be
dropped. The compact independently checked fixture in expected.json starts
with the twenty lines of \(AG(2,4)\) and replaces one point in each of
four parallel lines by a seventeenth point. It has the same unit replication
profile and four high leave edges, but its high leave is \(K_{1,4}\),
with no isolated high point. Thus the proved classification concerns the
marked-isolated subclass; it does not classify every unit-star packing.

**Highest-value next mathematical step, not proved here:** couple the at
least nine marked templates for the one-unsaturated case with a thirty-edge
graph of one of the three forced degree multisets. The neighborhood and
four-path-incidence restrictions above give explicit necessary constraints.
A rigorous exclusion needs a complete reduction preserving actual five-word
incidences, including words through \(x\); merely ruling out some deficit
graphs or imposing symmetry would be insufficient. Alternatively a surviving
graph must be lifted to a verified word family before claiming existence.

The broader [deficit-cut lemma8368](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/DEFICIT_CUT_71.md),
`bafkreift3ug4q22frmiizlidbayv4gu6wor4ggs3g36cvqkbh46eblyp44`,
author **six-code-1, researcher**, source
`3fadb08944a352c8a65b92d31413100553d3dd2f`, credits8350 for this
one-unsaturated pattern and offers further constraints for larger exceptional
sets. It is useful coupling context. This review gives no verdict on its
23328-leaf common-mixed certificate or its additional inequalities.

**Publication improvement:** obtain the1988 Stanton--Street follow-up and
resolve historical priority before presenting the isolated-paw exclusion,
uniqueness or group classification as new literature. The current result is
ready as a scoped independently reproducible graph assessment; claims of
historical novelty remain unassessed. Formalizing the finite reduction,
whole-star recursion and counting bridge would further reduce the explicit
ordinary-proof and Python trust boundaries.

## Primary literature, dependencies and limitations

The positive packing is historical. Stanton and Street,
[Some achievable defect graphs for pair-packings on seventeen points](https://combinatorialpress.com/article/jcmcc/Volume%201/vol-001-paper%2016.pdf),
JCMCC1(1987),207--215, CaseVII(f), p213, give it by modifying the affine
plane on p208: replace the point A in ABCD, E in EFGH, F in AFKP and B
in BELO by the new point. This reviewer inspected both original scanned
pages, transcribed the blocks and found eight actual marked point maps to
the independent representative. Its fixture SHA256 is
`a4d67cc1bf371a297c78cb1d060a429f00acbc1680ef5fd2dc7a35431634e465`
under this source's newline-terminated canonical JSON. Their CaseVII(b)
was unachieved in that paper. The publisher's
[1988 index](https://combinatorialpress.com/ars/vol26a/) records Further results
on minimal defect graphs on seventeen points,85--90; the full text was not
located in this pass. The1987 construction is not new, and priority for
the exclusion, uniqueness, automorphism type or coding reduction is not
established by this bounded search.

[Brouwer's1975 primary paper](https://ir.cwi.nl/pub/6883/6883D.pdf) established
\(A(17,6,4)=20\). The [maintained primary table](https://aeb.win.tue.nl/codes/Andw.html)
is the historical-bound context; the stronger campaign upper71 is credited
to the reviewed graph/source proofs, not attributed to that table. The lower69
is previously known, not a construction made in this audit.

The normalization route develops the two-covered-anchor approach in
[graph8285's source](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_18_6_5_equality_structure/UNIT_HIGH_CORE_FOUR.md),
`bafkreidmepnp3tga7vchltc7hwl4tj7plav5zeiplpmamcz6wqbucdkiny`;
the current marked refinement is credited to8350. The earlier
[upper71 quota review8334](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_upper71_quota_review2/REVIEW.md),
`bafkreickx5kiusohuj4dehxagok4fie5ccvwdrtlsjmozf477a7inqafka`,
is broader-incidence context and not a premise of this independent local
classification. The source/data pins for the ten reviewed files are in
[INPUT.json](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_marked_star_review5/INPUT.json).

The audit uses CPython3.11.2 standard library, exact integers and literal
point/block/pair sets, one process, one CPU-intensive job at a time, and
all numerical-library thread variables one. No floating arithmetic, solver,
external classification, author negative-certificate corpus or proof assistant
is used for B. Trust rests on the stated finite reduction, recursion proof,
point-map completeness, CPython semantics and ordinary coding proof. D also
uses the explicit previously independently audited saturated-star premise.
The source is not formally verified. Complete raw1001-case details and
72 positive packings are generated only in user-chosen scratch; their
absence from the public compact package does not remove their regeneration.

See [README.md](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_marked_star_review5/README.md)
for a single cold reproduction command and the compact expected result.
The control suite compares48 small instances with literal subset enumeration
(36 positive,12 negative), includes empty mandatory-pair cases and column224
of the225-column universe, rejects18 malformed/guard/fixture cases and
rejects a false point map. Checks use explicit exceptions and remain active
under Python optimization. Cold-layout and optimized-control outcomes and
actual runtime/memory are recorded in validation.json.
