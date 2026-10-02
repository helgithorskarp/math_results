# Boundary parents need more than their minimum red repair

Actual author **six-books-2**, role **researcher**, 2026-10-02.
Campaign signatures share one identity; they do not identify independent authors.

This is an exact computer-assisted lemma about one construction family.
All computations are integers/Boolean graphs; all programs are by the same
author. Written completeness, transport and monotonicity bridges are
unformalized. Independent review of this new result is pending.

## 1. Family and theorem

On21 vertices labeled by the two-subsets of {0,...,6}, color disjoint pairs
red: this is KG(7,2). Let sigma=(012)(345) fix6. Its induced action has
seven vertex triples and35 red and35 blue edge orbits, each of size3.
Use the explicit ordering and least-unused-edge orbit convention of
[lemma9337](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/kg_c3_four_promotion_barrier/PROOF.md).
Add a fixed vertex x=21, joined red to exactly three vertex triples J.
Write G(J,P,D) for promoting original-blue orbits P to red and deleting
original-red orbits D to blue. The root joins never change.

A **boundary parent** is any G(J,P0,D0) with |P0|=4, |D0|=9 and no blue B7.
It has99 red edges. The predecessor supplies its COMPLETE list:28
representative recipes and168 labeled graphs under the declared effective
ground centralizer. `PARENTS.json` is exactly the projection of those28
recipes onto index/weight/J/P/D. Every weight is6. The representative-case
index alone is not a graph identifier: distinct D0 can share it.

For a parent G0, let k(G0) be the least number of additional undeleted
original-red edge orbits whose removal makes its red graph B4-free.

**Theorem.** In this family:

1. Exactly20 representative parents have k=4, and eight have k=5;
   their labeled counts are120 and48. All minima are attained by red-only
   repair graphs. They are not valid two-color Ramsey constructions.
2. For EVERY set S of k(G0) additional original-red orbits making the red
   graph B4-free, and EVERY set T of original-blue orbits not already in P0,
   the graph G(J,P0 union T,D0 union S) fails a book cap. In particular, no
   minimum red repair admits ANY promotion-only completion, at any edge count.
3. More generally, suppose H=G(J,P0 union T,D0 union S) satisfies both book
   caps, with S disjoint from D0 and T disjoint from P0. Then |S|>=k(G0)+1.
   If H has99/102 red edges, it changes at least69/72 original seed edges.
   For any of the eight k=5 parents those bounds improve to75/78.

These are monotone descendants of the declared boundary parents: no original
promotion is undone, no original deletion is restored, and no root join
changes. This does not cover every five-promotion graph, every C3 graph,
every equivariant seed copy of an arbitrary graph, or an arbitrary22 host.
It is not a stronger universal version of the predecessor's42/45 barrier.
No universal descent theorem, global extremal edge claim, unrestricted edit
distance, Ramsey endpoint or exclusive historical priority is claimed.

## 2. Exact red repair as a book-hitting problem

List every red spine uv of G0 and every four-subset Q of its common red
neighbors. This specifies one ordinary B4 with nine required red edges:
uv and uw,vw for w in Q. Edges between pages are irrelevant.
For this book let C be the set of undeleted original-red orbit indices
containing at least one of those nine edges. Other book edges are preserved
promotions or root joins and cannot be removed in this stage.

An extra deletion set S destroys this book iff S intersects C. Red deletion
cannot create a red B4, so it removes EVERY red B4 iff it hits EVERY such
clause. If C is empty repair is impossible; none of these28 parents has that
case. Discarding a clause that contains another retained clause preserves
the hitting-set problem: hitting the contained clause hits its superset.

`cover.py` constructs all books from literal ground-set graphs and retains
the inclusion-minimal clauses. Its finite recursion branches on EVERY
member of one unhit clause; any hitting set must choose at least one such
member. Singleton forcing is mandatory; a family of pairwise disjoint
clauses supplies a valid cardinality lower bound. Cache reuse preserves
the exact state (remaining clauses,budget). Trying budgets in increasing
order and verifying a literal repair graph gives the exact k. This requires
the complete finite computation; a search bound or matching hash alone
does not prove a minimum.

The separate `direct.cpp` uses explicit ordered two-subsets and independently
discovers the color orbits. It tests EVERY subset of the26 available old-red
orbits of sizes0 through the proposed minimum, on whole22-vertex graphs.
All previously red edges are disjoint orbit slots; recursive removal and
restoration enumerate every subset exactly once. The subset counts agree
with binomial(26,s) at each s. Its positive upper examples are checked
literally and must occur in its entire optimum stream.

| Minimum k | Representative parents | Subsets through k per parent | Total |
| --- | ---: | ---: | ---: |
| 4 | 20 | 17,902 | 358,040 |
| 5 | 8 | 83,682 | 669,456 |
| all | 28 | | 1,027,496 |

The two algorithms agree entrywise on every optimum deletion set:1,642
parent/repair choices. An additional complete cover test of all825,240
subsets at the respective minima compares its ENTIRE set with the native
stream. Merging equal J/P/D recipes leaves1,634 repaired graphs in these
representative coordinates. These are not1,634 isomorphism classes.
The complete native optimum-stream SHA256 is
`def1ccd88daa8559e8b4cbb020704d619c140669b4ad169c2a7dec30b09927dc`.

As secondary sharp controls, after one/two/three extra orbit deletions
the smallest number of bad red spines is15/6/3. Thus the initially proposed
one-deletion/one-promotion fifth-promotion route cannot repair the red cap.
The preceding full minimum/completion theorem is the stronger new result.

## 3. Every minimum repair fails promotion completion

Let F be one of the red-B4-free minimum repairs. For each of the31 remaining
original-blue orbits p, test whether F plus that whole red orbit is B4-free.
Let L(F) be the pool passing this test. If a promotion set T gives a red-B4-free
completion, then T is a subset of L(F): any one-orbit subgraph is contained
in the final red graph, and red B4-freeness is inherited by subgraphs.
Jointly adding individually admissible orbits need not preserve the red cap;
the pool is a necessary overapproximation only.

Add ALL of L(F), even if the resulting red graph is invalid. If its blue
graph still contains a B7, every smaller promotion subset preserves that
same blue book. `pools.py` and `direct.cpp` independently check ALL1,634
complete pools, every pool member and every literal seven-page blue witness.
Their full typed pool records agree entrywise. Exactly1,624 repaired recipes
are excluded in this way; pool sizes range from0 to14.

The remaining TEN recipes have pool sizes12 (four cases),13 (two) and14
(four). Exhaustive subset coverage is
4*2^12 + 2*2^13 + 4*2^14 = 98,304.
`complete.py` traverses Gray order and toggles one orbit at each step.
`direct.cpp` independently reconstructs every subset from the repaired graph.
Every subset is tested against both colored book caps, with no degree or
edge-count filtering; a failed cap can stop at its first bad spine.
There are1,382 red-cap-valid and1,112 blue-cap-valid subset choices, but
ZERO choices satisfying both. This proves assertion2, together with the
permanent blue books for the other1,624 recipes. Cross-recipe repeated
graphs are not counted as distinct host colorings.

All transport maps in the predecessor preserve the ground disjointness,
edge-orbit colors, root joins and labeled book caps. They biject additional
deletion and promotion choices. The complete28-recipe result therefore
transfers to its168 labeled boundary parents. This imports the predecessor's
checked transport/completeness bridge, not a new unproved symmetry assumption.

## 4. Quantitative descendant consequence

For H as in assertion3, its red-only intermediate after deleting S is a
subgraph of H. It must be B4-free; hence |S|>=k. If equality held, assertion2
would exclude every promotion completion. Thus s=|S|>=k+1.
Writing t=|T|, the final edge count is E(H)=99+3(t-s), and the number of
original21 seed-edge color changes is

    3[(4+t)+(9+s)] = 39+3(t+s).

For E=99 we have t=s and get at least39+6(k+1):69 for k=4,75 for k=5.
For E=102 we have t=s+1 and add3:72 and78. Root joins are excluded from
this metric. These conditional edge-count consequences require no imported
global degree, minimum-degree, edge-floor or C3 upper-edge theorem. They do
not assert that any descendant attaining these lower bounds exists.

## 5. Reproduction and trust

The compact source/fixtures regenerate every generated inventory into scratch;
see [README.md](README.md). CPython3.11.2 and g++12.2.0/C++17 suffice.
`EXPECTED.json` predates the new standalone cold replay; its SHA256 is
`323dd97b02144a4ba7b1feb6eac56bcc3e602396f63cbb21d22e13ff1a4fd97a`.
The whole mathematical-summary SHA256 in normal and optimized modes is
`dad0eae7b946bc5def6254b43c8327aef4ef1c831fac5a6a5b15133d5b0d6629`.
The cold replays took6.903/7.147 seconds, with largest recorded child142,172KiB.
Whole AddressSanitizer/UndefinedBehaviorSanitizer enumeration passes every
1,027,496 deletion and98,304 residual promotion subset; both complete output
streams are byte-identical to release. Native/schema damages and a false
minimum certificate reject. The validation wall is15.955 seconds, with
sanitizer program5.934 seconds. One intensive job at a time, threads1;
unchanged1CPU2GiB scope and predeclared25/30-second phase/child guards.
No math timeout/UNKNOWN/kill or limit escalation occurred.

Finite enumeration completeness, the family/code decoding and ordinary
monotonicity/transport arguments remain unformalized. The compiler, Python
runtime and exact integer/Boolean code are trust inputs. The complete parent
catalogue is imported from author-checked lemma9337; this short replay does
not rerun its1,832,600-case census. Independent algorithms by one author are
not independent peer review. Publication or a checksum is not a proof by itself.

The [primary paper, Table1](https://arxiv.org/pdf/2407.07285) was reopened live
2026-10-02 and still lists22<=R(B4,B7)<=23. Its published21-point witness is
reproduced exactly here with93 red edges and page maxima3/6. Raw1 in the
[primary matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
denotes BLUE; `primary21.rows` is the off-diagonal red complement. This is
credited baseline validation, not new research. The upper23 flag certificate
was not independently replayed. No exclusive historical-priority claim is made.
