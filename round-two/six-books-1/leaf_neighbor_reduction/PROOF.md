# Thirteen-edge leaf roots force a second deficient neighbor

Actual author **six-books-1**, role **researcher**, 2026-10-01.
Shared campaign signatures do not distinguish actual authors.

A valid graph is a simple red graph on 22 vertices with at most three
common red neighbors on each red edge and at most six common blue
neighbors on each blue nonedge. Books are ordinary subgraphs: edges
between pages are unrestricted. Throughout assume **108 red edges and
maximum red degree at most ten**. A one-nine root has degree ten, one
degree-nine red neighbor, and nine degree-ten red neighbors.

**Lemma.** Suppose a one-nine root u has the following marked red
neighborhood, with its degree-nine neighbor a labeled 0:

```text
0: 1,8,9;  1: 0;  2: 6,7;  3: 4,5;  4: 3,7,9;
5: 3,6,8;  6: 2,5,9;  7: 2,4,8;  8: 0,5,7;  9: 0,4,6.
```

Its lexicographic red-edge bit key is 6790396772737, it has thirteen
edges, and its unique local leaf v is labeled 1. Put B=N_B(u) and
T={b in B: vb is blue}. Then |T|=3 and **e(G[T])<=1**. Moreover,
**v has a deficient red neighbor in B**: v cannot itself be a one-nine
root. Deficient means global red degree below ten. These statements
cover every outside deficit pattern; no rootlessness or outside degree
floor is assumed.

**Counting consequence.** Write H={x:d_G(x)=10}, L=V(G) minus H,
D9={x:d_G(x)=9}, R for the number of one-nine roots, and n_leaf for
the number with the displayed leaf neighborhood up to marked
isomorphism. Then

    n_leaf + R <= e(D9,H)
               = 9|D9| - 2e(G[D9]) - e(D9,L minus D9).       (1)

With the independently confirmed isolated-type exclusion8993, every
one-nine root not counted by n_leaf has a fourteen- or fifteen-edge
neighborhood. In the explicitly **rootless** degree pattern
8,9,9,10^19, if the degree-eight point is red adjacent to both degree-nine
points, at least **four** one-nine roots have fourteen- or fifteen-edge
neighborhoods. This further consequence uses the credited occurrence
bound of review8987, as shown below.

These are necessary structural restrictions. They exclude neither
general leaf completions, all dirty neighborhoods, the independent-four-nine
exception, all 108-edge graphs, nor either Ramsey endpoint.

## Dependencies and scope

The reciprocal-root step imports the complete necessary marked
classification of [8939](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/rootless108_marked_profiles/PROOF.md),
`bafkreie3qf4riaoqbnnzarcfswufog6glhcghahfvaptehf3ia7iis6uji`.
Its fourteen survivors have a unique class containing a local vertex
of degree one: the displayed thirteen-edge leaf graph. The other
thirteen-edge survivor has degrees 0,2,3^8; all eleven fourteen-edge
survivors have degrees 2^2,3^8; the fifteen-edge survivor is Petersen.
[Independent review8987](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/dirty-root-audit/REVIEW.md),
actual six-reviewer-2, confirms that exact conditional classification
and proves the seven-root occurrence refinement used in the last
corollary. No full-root all-five-column restriction is imported here.

Only the identification of nonleaf roots as fourteen/fifteen-edge
types imports [8993](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/dirty13_isolate_exclusion/PROOF.md),
`bafkreibjv6i6monbosb566mqmrkei5fiyvyuopovfbaekihk2uqxrg5eea`.
[Independent review9021](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/isolate-incidence-audit/REVIEW.md),
actual six-reviewer-2, confirms8993 and proves its exact isolated
neighborhood impossible without the edge-count hypothesis. That
stronger review supplies no verdict on this new leaf argument.
The column-degree mechanism retains credit to
[8869](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/rootless108_structure/PROOF.md)
and8939. All maximum-degree and edge-count hypotheses remain explicit.

## 1. Outside equality and the edge cut

Let A=N_R(u), J=G[A], h_i=d_J(i), eta_i=1(i=a),
W_i={b in B:ib is blue}, and delta_b=10-d_G(b). Degrees give

    |W_i|=h_i+2+eta_i,
    k_b=|N_B(b) intersect A|,
    d_(G[B])(b)=k_b-delta_b.                               (2)

There are eleven points in B. The blue spine ub has 10-d_(G[B])(b)
blue pages, so every d_(G[B])(b)>=4. Total deficit is 220-216=4;
the root and its neighborhood account for one, so sum_B delta_b=3.
Since sum_i h_i=26, sum_B k_b=47. Summing (2) yields
sum_B d_(G[B])(b)=44. Thus G[B] is four-regular, with 22 edges.
No lower bound on individual global outside degrees was needed.

The displayed graph gives |W_a|=6 and |W_v|=3. The red pair av
has its known red page u and no local common red neighbor. Its
outside common red count is

    11-|W_a|-|W_v|+|W_a intersect W_v|=2+|W_a intersect W_v|.

The red page cap forces W_a intersect W_v empty. Put
T=W_v, Y=B minus T, R0=B minus (W_a union T). Their sizes are 3,8,2.
Then N_R(v)={u,a} union Y. In this neighborhood u has local degree
one and a has local degree three, through u and R0. There are no
red u--Y edges. Four-regularity gives

    e(G[Y])=22-12+e(G[T])=10+e(G[T]),
    e(G[N_R(v)])=13+e(G[T]).                              (3)

Each vertex in the ten-point N_R(v) has local degree at most three,
by the red spine from v. Its leaf u has degree one, so the local
degree sum is at most 1+9*3=28. Equation (3) proves e(G[T])<=1.

## 2. A hypothetical reciprocal root forces a four-nine star

Suppose v were also a one-nine root. Its sole deficient neighbor
would be a, since that red edge is present. Thus every Y point has
global degree ten. Classification8939 applies at v under exactly
the current hypotheses. Its neighborhood contains the full leaf u,
so it must be the same displayed thirteen-edge leaf graph. By (3),
T is independent.

Write X=A minus {a,v}. The blue neighborhood of v is X union T,
and the thirteen-edge equality of Section1 applies there too: its
induced red graph is four-regular. For t in T, independence of T
therefore gives d_X(t)=4; original outside four-regularity gives
d_Y(t)=4. Also t is red to a and blue to both roots. These sets
exhaust every other vertex, hence d_G(t)=1+4+4=9. Exactly a and
the three T points have degree nine; every other point has degree
ten. Their induced low graph is the red star centered at a.

Both eight-point blocks X,Y induce the graph F obtained from the
displayed leaf graph by deleting its mark and leaf. Use coordinates
2..9 in each block. The last two, 8 and9, are special: they are red
adjacent to a. The six ordinary points 2..7 induce the cycle

    2-6-5-3-4-7-2.

Within F, points2,3,8,9 have degree two and points4..7 degree three.
Every T point has four red neighbors in each block. A block point
with within-block degree h has T-degree 4-h, because its induced
blue-root outside graph is four-regular. Its degree-ten equation
then gives five red neighbors in the opposite block for an ordinary
point, or four for a special point owing to its extra red edge to a.

## 3. Twelve interfaces and an unavoidable book

For an adjacent ordinary pair in the six-cycle, its two opposite-block
red neighbor sets each have size five in eight points, so their
intersection has size at least two. The pair already shares its
root as a red page. The red page cap three forces their T-neighbor
sets to be disjoint.

Let alpha be the T point omitted by the two-element T-neighbor set
at2. Its neighbors6,7 consequently have singleton T-neighbor alpha.
Similarly let beta be omitted at3; points4,5 have singleton beta.
Edges6-5 and4-7 force alpha!=beta. Let gamma be the remaining T point.
The ordinary-column T-row counts are 3,3,2 for alpha,beta,gamma.
Each T row has total four, so both special columns contain gamma;
one also contains alpha and the other beta. There are exactly twelve
labeled interfaces: six ordered choices of alpha,beta, and two choices
for the special columns. The two nondistinguished T rows are disjoint;
each intersects the gamma row in exactly two block points.

Let gamma_X,gamma_Y be the distinguished actual T points in the two
blocks. If equal, the red spine a--gamma_X has the four special
points as common red pages, a contradiction. If distinct, the blue
spine gamma_X--gamma_Y has common red neighbors a, two points in X,
and two in Y. For a blue pair i,j in order22 the common blue count is
20-d_G(i)-d_G(j)+c_R(i,j). Here it is 20-9-9+5=7, a contradiction.

Every edge incident to these spine endpoints is already specified.
Unknown X--Y edges cannot change either page count. Thus this
exclusion requires no X--Y completion census. The reciprocal-root
assumption was impossible. Since v is full and already red adjacent
to a, it must have an additional deficient red neighbor in B.

## 4. Injective budget and a rootless consequence

Each leaf root u determines its unique full leaf neighbor v and its
degree-nine mark a. By the lemma, v has at least two deficient red
neighbors. The map u to (v,a) is injective. Indeed, if distinct
u,u' gave the same pair, then in N_R(v) each would be a local leaf
with sole local neighbor a. They are blue to one another and to the
other seven members of that ten-point neighborhood. Those seven
already give their blue spine seven pages, impossible.

There are sum_(v in H, |N_R(v) intersect L|>=2)|N_R(v) intersect D9|
possible image pairs. Of the e(D9,H) red low/high incidences, exactly
R meet a high point whose sole low neighbor has degree nine. High
points with no low neighbor or a single other-degree low neighbor
contribute zero; all other contributing incidences are precisely
the image-pair domain. This proves (1). In particular

    R-n_leaf >= 2R-e(D9,H).                                (4)

For the additional rootless corollary label the low points z,a,b,
of degrees8,9,9. Let e_ij indicate a red low edge, ell_z=e_za+e_zb,
y count high points with low type {a,b}, and t count triple types.
The credited review8987 argument gives

    R=11+ell_z-y,
    y+t+e_za*e_zb<=4-e_ab,
    R>=7+ell_z+e_ab+e_za*e_zb+t.                           (5)

For completeness, exactly 8-ell_z of the nineteen high points meet z;
rootlessness forces each other high point to have type {a}, {b}, or
{a,b}, proving the first identity. The common red neighbors of a,b
number y+t+e_za*e_zb; their red/blue spine caps give the second
inequality and then the last. This is the existing review refinement,
not a new seven-root claim.

If e_za=e_zb=1, then R>=10+e_ab+t and
e(D9,H)=16-2e_ab. Equations (4)--(5) give

    R-n_leaf >=4+4e_ab+2t>=4.

By8939 and8993 these nonleaf one-nine roots have fourteen/fifteen-edge
neighborhoods. The argument retains explicit rootlessness; no
concurrent full-root certificate is required by it.

## 5. Reproduction and remaining trust boundary

[check.py](check.py) decodes the leaf key, deletes its mark and leaf,
and exhausts all 3^8=6561 incidence-column assignments. Independently,
[verify.py](verify.py) starts from the literal ten F edges and chooses
every ordered pair of four-subsets of eight points, 70^2=4900 choices;
the column margins uniquely determine the third T row when possible.
Both complete domains yield the same twelve actual labeled patterns,
also matched entrywise to the hand derivation. All144 pattern pairs
are tested: 48 have the red four-page contradiction and96 the blue
seven-page contradiction. The complete pattern-list SHA256 is

    9b50aaadcd0357d0757e6d9cf6d00959842a51373c9f3d5abf0fe115a5e5e2d3.

The producer uses red-neighborhood bit words; the separate checker
uses a differently numbered 22-point Boolean matrix and literal
third-point loops. Each verifies that all64 unknown cross edges avoid
the selected spine endpoints. All9216 single-edge toggle controls
and144 complete red cross-block controls preserve the pages. This
does not enumerate 2^64 completions: the ordinary endpoint argument
above proves invariance for all of them. The partial frames give the
correct degrees for the two roots, mark and T points, but are not
valid hosts; unspecified cross edges affect the block-point degrees.

The independent checker also reconstructs the seven forced blue pages
in the injectivity argument and rejects eight damaged expected records.
All mathematical checks use exact standard-library integers or literal
colors. Complete records, including all twelve patterns, match
[expected.json](expected.json), not just aggregate counts or hashes.
Normal and Python -O runs agree. Python3.11.2 suffices; no numerical
solver, floating-point certificate, outside catalogue, private corpus,
timeout or resource escalation is a premise.

The ordinary root swap, degree equations, twelve-pattern classification,
page contradictions, injection and dependency bridges are written and
unformalized. Separate algorithms are by the same actual author; new
independent peer review is pending. The small controls do not reprove
the inherited179-class completeness theorem of8939 or its independent
audit8987. [provenance.json](provenance.json) records their exact source
commits and scoped roles; [MANIFEST.json](MANIFEST.json) fixes file hashes.

The located primary interval remains22..23 in
[Lidicky--McKinley--Pfender--Van Overberghe, Table1](https://arxiv.org/pdf/2407.07285)
and [Small Ramsey Numbers, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
reopened2026-10-01. The primary
[21-point matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
was freshly downloaded and exactly reproduced:93 red edges, page maxima3/6.
The compact primary fixture is prior art, not a new construction.
The published upper23 flag certificate was not replayed. Bounded live
literature/graph/source checks do not establish exhaustive priority.
The new increment is the conditional leaf-root reduction and its
injective incidence budget. General leaf completions, the eleven
fourteen-edge types, dirty Petersen completions, and rootless exceptional
high graphs remain concrete open completion frontiers.
