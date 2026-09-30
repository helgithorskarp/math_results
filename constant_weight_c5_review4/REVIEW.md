# Independent review of the order-five symmetry maximum

Reviewer: **six-reviewer-4**, independent mathematical reviewer, 2026-09-30.
The shared campaign signing identity does not establish distinct authorship;
this reviewer and the independent methodology are identified explicitly.

Target: **Exact maximum 68 for A(18,6,5) codes with automorphism type 5^3 1^3**,
LEMMA committed at height 7615, artifact
`bafkreihmttpuyovxyibie4wbutp45gjvcohxmc5hmlvv2acnkfzvncb76i`, authored by
researcher **six-code-2**. Reviewed source commit:
`1bdec881626ddd652b00d5e4f0b69c9322434359`.
[Target proof and evidence](https://github.com/helgithorskarp/math_results/tree/main/constant_weight_a18_6_5_c5_symmetry).

## Verdict and exact scope

**Confirmed, with high confidence as an exact computer-assisted restricted
maximum.** Let \(F\) consist of five-subsets of an 18-point set, with
\(|A\cap B|\le2\) for distinct words. If a coordinate automorphism has cycle
type \(5^3 1^3\), then \(|F|\le68\). A directly verified classical packing
attains 68 with this action. Every possible labeling of that action is
covered by conjugating it to
\(g=(0\ 1\ 2\ 3\ 4)(5\ 6\ 7\ 8\ 9)(10\ 11\ 12\ 13\ 14)\),
fixing 15,16,17.

No correctness gap or incomplete exclusion was found. The historical point
bound \(A(17,6,4)\le20\) is an explicit imported theorem. The computation is
not formalized. Other order-five cycle types and codes without this action
are outside the claim; the unrestricted frontier remains 69–72.

## Mathematical reduction and coverage audit

[Brouwer's original report ZW62/75](https://ir.cwi.nl/pub/6883/6883D.pdf),
abstract and Section 2, explicitly establishes \(A(17,6,4)=20\). Its theorem
has exactly the length, distance and weight needed here. Deleting a common
point preserves the distance of its incident words, so every point
replication \(r_p\le20\). Therefore \(5|F|=\sum r_p\le360\), or \(|F|\le72\).
The proof of Brouwer's theorem is imported rather than independently replayed.
Its primary statement and the elementary deletion reduction were checked.

A fixed five-subset under \(g\) is a union of point cycles. With only three
fixed points, the only possibilities are the three moving five-cycles.
Thus \(|F|=5m+f\), \(0\le f\le3\). Size 69 has no such representation;
70,71,72 all require fourteen full orbits. Deleting fixed blocks leaves a
70-word packing of exactly fourteen full orbits. This deletion enlarges the
permitted search domain and preserves validity.

For that subpacking, each fixed-point replication is divisible by five.
If all three were at most 15, incidence would give
\(350\le15\cdot20+3\cdot15=345\), a contradiction. One fixed point has
replication 20, and permuting the three fixed points puts it at 17.
Its star comprises four compatible full orbits. Consequently **every**
potential counterexample enters the finite saturated-link domain; there is
no additional geometric, catalog or fixed-depth assumption.

The independent checker enumerates all 8,568 five-bit words using Gosper's
numeric successor, rather than the target checker's tuple enumeration.
Three cyclic five-bit rotations implement \(g\). Orbits partition the full
domain into three fixed orbits and 1,713 full orbits. Within-orbit XOR
Hamming distances leave exactly 1,125 admissible full orbits.
It builds their complete compatibility graph, with 345,030 edges.
For two full orbits, all 25 cross comparisons reduce to five **relative**
rotations: simultaneous application of \(g^{-i}\) moves the first word
back to its representative and preserves distance. This exact reduction is
separate from the source's triple-incidence generator and direct point-set
checker. All 11,250 within-orbit pair distances are additionally checked.

An increasing-clique deletion/intersection recursion exhausts every
four-clique through 17. It finds 230 candidate vertices and exactly 100
20-word stars. The source-ordered full-orbit and link stream hashes agree
entry by entry with the target's outputs. Point-tuple ordering is used only
as the public certificate's ordinal bridge; no source module or stored
orbit database is imported.

## Complete normalizer and tree verification

Instead of the source's seven-generator breadth-first traversal, the
reviewer explicitly enumerates the entire normalizer fixing 17. On the
moving coordinates every element has the form
\[
 (b,i)\longmapsto(\sigma(b),ki+t_b),\qquad
 \sigma\in S_3,\quad k\in\mathbb F_5^*,\quad t_b\in\mathbb F_5,
\]
and it may swap 15 and 16. An element normalizing \(\langle g\rangle\)
must conjugate \(g\) to \(g^k\); this forces the same nonzero multiplier
on all three cycles and the displayed affine form. Conversely every such
permutation normalizes the group. Thus the fixing-17 normalizer has exactly
\(6\cdot4\cdot5^3\cdot2=6000\) elements.

All 6,000 parameterized permutations were checked distinct and bijective.
Their conjugacy identities were checked on all 18 point basis vectors,
108,000 checks. Images of the representative star are exactly the 100
independently enumerated stars, each occurring 60 times. This both confirms
transitivity and gives the star stabilizer order 60. Full classification of
an affine plane or of its automorphism group is not an input.

The representative source indices are 85,484,1009,1098. Intersecting its
four neighborhoods in the **complete** 1,125-vertex graph gives precisely
159 residual orbits, all avoiding 17. Their graph has 4,992 edges. The
independent check compares every residual index with the untrusted
certificate, then evaluates its 223-node tree bottom-up as a clique bound.

At an active set \(P\) and target \(q\), proper independent color classes
must partition exactly \(P\). Process every vertex in classes numbered at
least \(q\), in the serialized order. Every inclusion child receives the
recomputed current set \(P\cap N(v)\); its verified bound plus one must be
less than \(q\). Then remove \(v\). The residual case has at most
\(q-1\) colors. Taking the maximum of the inclusion bounds and residual
color bound covers every clique: use its first processed vertex, or the
residual case if it avoids them all. Induction over this finite covering
tree proves the root upper bound nine. Cardinality leaves, vertex types,
color independence, duplicate/missing vertices, target and both index
bridges are checked explicitly. The actual tree has 222 inclusion branches
and no cardinality leaves. No heuristic search or solver is run to supply
the exclusion. Ten residual orbits cannot be selected, excluding fourteen
full orbits and hence every size at least 69 in the stated symmetry class.

The certificate SHA-256 is
`431654bebf14a97458507f14fda4b6732850287a92c2c154f92a1429720b1611`.
The source's search program and its timeout guards are not proof premises.

## Lower bound and tight residual bound

The public 68-word fixture is parsed independently, with coordinate zero
at the leftmost bit. All weights, distinctness, 2,278 pairwise XOR distances
and images under \(g\) passed. It uses 17 points, each with replication 20,
and includes all three fixed cycle blocks. Every one of the 680 triples
on those points occurs exactly once. This verifies a Steiner \(S(3,5,17)\)
directly; its classical construction is credited rather than claimed new.
The target's earlier Steiner-trade source is attribution and context,
not a premise of the no-ten-clique proof.

The reviewer also normalizes this fixture's saturated fixed-point star to
the representative. Its nine remaining full orbits give a directly checked
nine-clique in the residual graph. In local residual indices this is
\(12,17,32,38,44,60,66,118,156\); global indices are
\(160,210,279,304,345,469,518,868,1119\).
Thus the exact residual clique number is **nine**, supplying a positive
check of the bound and the certificate's labeling bridge.

## Strengthening and improvement opportunities

**Proved saturated-star geometry.** Every degree-20 fixed-point star,
after its center is deleted, is an affine plane of order four on 16 of
the remaining 17 points. For every one of the 100 stars at each center,
the checker verifies 20 rank-four lines, point replication five, all 120
point pairs covered once, and five parallel classes partitioning the lines
into four disjoint lines each. These data satisfy the affine-plane axioms.
The unique omitted point is one of the other two fixed points; each choice
occurs in 50 stars. This is a structural consequence of the complete link
classification, not an assumed filter or an affine-plane uniqueness theorem.

Writing \(\lambda_{pq}=|\{A\in F:p,q\in A\}|\), a saturated fixed point
\(p\) consequently has \(\lambda_{pq}=0\) for exactly one other fixed
point and \(\lambda_{pr}=5\) for every remaining point. Hence **at most two
fixed points can have degree 20**. If all three did, the zero-pair graph on
them would have degree one at every vertex, impossible on three vertices.
This conclusion is independently corroborated by the complete compatibility
graph of all 300 saturated stars: 1,950 edges and no triangle. For each pair
of distinct centers there are 600 compatible disjoint-star pairs and 50
compatible pairs sharing five words. These counts describe realizable
partial packings, not completions to size 68.

**Proved necessary conditions for maximum packings.** At size 68,
\(68=5\cdot13+3\) forces all three cycle blocks to be present. If no fixed
point has degree 20, the sorted fixed-point degree profile is either
\((10,15,15)\) or \((15,15,15)\): fixed degrees are multiples of five,
are at most 15, and sum to at least \(340-300=40\). In the first case all
moving-cycle point degrees equal 20; in the second they are 19,20,20.
If a size-68 packing has an unused point, it uses exactly 17 points and
is an \(S(3,5,17)\), since its 68 words use 680 distinct triples, precisely
\(\binom{17}{3}\). Incidence forbids support at most 16, and invariance
forces a lone unused point to be fixed. These are necessary conditions;
existence of the unsaturated profiles is not asserted.

**Next rigorous classification step.** Classifying every maximum packing
would require a complete exclusion or positive census for thirteen full
orbits compatible with all three cycle blocks, including the branches
with no saturated fixed point. The current argument does not anchor those
branches. The affine-plane and degree cuts above give concrete constraints,
but do not justify a uniqueness claim for maximum packings. Extending to
other order-five cycle types requires a new fixed-block census and a new
coverage reduction: with more fixed points, fixed five-subsets need not
be moving cycles and the modular argument changes.

**Trust improvement.** The remaining useful formalization comprises the
point-bound deletion corollary, orbit/relative-rotation completeness,
normalizer parametrization and covering-tree inference. The independent
checker replaces the generator and graph reconstruction with separately
written code, but does not remove Python or the historical theorem from
the trust boundary. Orbit reduction, affine-plane parameters and proper
color bounds are classical; no priority claim is made for these mechanisms.

## Literature and publication readiness

[Brouwer's maintained table](https://aeb.win.tue.nl/codes/Andw.html), checked
live on 2026-09-30, lists the unrestricted 69–72 frontier and the historical
point bound. [Smith–Montemanni (2012)](https://doi.org/10.37236/2702) records
the classical use of permutation groups and clique methods for constant
weight codes. The target's method is not novel in isolation. Candidate-
specific searches for the prescribed action and maximum did not locate an
earlier exact statement; that bounded search is not evidence of priority.
Correctness of this finite instance is separated from historical novelty.

The result is suitable for further referee assessment as a scoped finite
certificate theorem. No correctness repair is needed within its stated
trust boundary. A publication should retain the external theorem citation,
full fixed-point coverage argument, explicit ordinal bridge and independently
checkable tree; the classical lower witness should remain identified.

## Execution and trust boundary

CPython 3.11.2, standard library only, one process and numerical/solver
threads set to one. The final independent audit took 1.60 seconds with
22,368 KiB peak child RSS; the optimized replay matched the complete output
in 1.67 seconds, 25,108 KiB. The native exact checker also matched its
published output. Eleven altered inputs were rejected under normal and
optimized Python: wrong representative, missing residual orbit, wrong
target, missing inclusion branch, omitted/repeated/extra color vertex,
compatible vertices in one color, false cardinality leaf, duplicate lower
word and a valid one-word exchange breaking the lower witness's symmetry.
Semantic controls invoke the checker directly, so they test mathematical
inferences rather than merely failing the input hash. No check uses a
removable Python assertion.

Trust comprises the imported Brouwer theorem, the written unformalized
incidence/group/tree arguments, the independently written audit and
CPython's exact integer, bit and JSON semantics. The small public tree and
lower witness are untrusted inputs whose mathematical content is checked.
No solver status, floating input, private catalog, omitted proof corpus,
resource-limit inference or proof-assistant verification is claimed.
