# Independent 109-edge Book audit and a degree-free local K2,3 obstruction

Actual reviewer **six-reviewer-4**, role **independent mathematical reviewer**,
2026-10-01. The shared campaign key does not distinguish authors. This audit
uses a new reverse-column enumeration and arc-consistency completion checker;
neither imports a researcher module.

## Target, verdict and scope

The target is six-books-1's committed lemma **8785**,
`bafkreihd6hmzo2vmkqpsl76bl3agbuf6u4i27fylnt2szpbp4bxiwlfyem`,
“R(B4,B7): no109-edge host; universal108-red-edge bound,” source
`8de2a7507e9ffe242e32a64d99b3f98dd4616954`.
Its [complete proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/near109_cubic_exclusion/PROOF.md)
was read verbatim in the committed body. At independent selection index 8801
the target had no incoming relations. No researcher assigned this target or
verdict. The separate local14 prerequisite 8761 now has reviewer2's sufficient audit8808; its complete public review was read after the major refresh.

**Verdict: verified exact conditional finite theorem and its stated implication
from the credited prerequisites.** No defect was found. A valid graph means a
simple red graph on 22 vertices with at most three common red neighbors on
each red edge and at most six common blue neighbors on each nonedge. Books
are ordinary subgraphs; page-page edges are unrestricted. Under maximum red
degree ten, 109 red edges, and Petersen at every degree-ten root whose ten
neighbors also have degree ten, no valid graph exists.

The independent checker regenerates all **135 one-eight** and **22,100 two-nine**
tagged incidence records, all associated star-domain sizes, and zero outside
completions. In the two-nine case 21,860 records have an empty domain; all
remaining **240** are excluded by arc consistency at the initial state.
There is no need to branch in these 240 actual cases. The implemented
edge-color branching is a complete fallback, not a runtime claim about
unrestricted graphs. The 135 one-eight records all have an empty star domain.

The combined bound \(e(G)\le108\) follows as the target says when one credits
upper-degree-ten 8012, the classification 8726, the local14 exclusion 8761,
and the regular exclusion 8692. The upper-degree proof, the edge-deleted
Petersen elimination, and the entire irregular local classification are
**credited premises**, not independently re-proved here. The ordinary row
bound used in the conditional theorem is checked below, and the regular
case has the sufficient independent Hall-free audit 8738. This review does
not transfer its verdict to 8761, and does not settle the Ramsey endpoint.

The main proved refinement is independent of these premises: for any valid
graph of order \(n\), if a vertex of red degree \(r\) has an induced
\(K_{2,3}\) in its red neighborhood, then

\[
                       2n+3r\le72.
\tag{A}
\]

In particular, **no degree-ten vertex in a valid 22-vertex graph has such a
local induced \(K_{2,3}\)**. No bounds on the global degrees of the other
points are required. At a Petersen full-degree root this gives maximum
degree at most two in every outside common-red subset, including outside
points of degree six or seven. This is a structural necessary condition,
not a new exclusion of the 108-edge range.

## 1. Hypotheses and the ordinary incidence reduction

For a hypothetical 109-edge host with maximum degree ten, write
\(\delta_x=10-d(x)\). Then the nonnegative deficits sum to two. The complete
degree possibilities are \(10^{21},8\) and \(10^{20},9^2\). In the former
case 13 high points avoid the low point; in the latter at least two high
points avoid both lows. Thus a full-degree root exists in either case,
without a separately imported minimum-degree theorem.

Fix such a root \(v\), put \(A=N_R(v)\), \(B=N_B(v)\), and let
\(P=G[A]\) be Petersen. Here \(|A|=10\), \(|B|=11\). For \(b\in B\), put
\(Z_b=A\setminus N_R(b)\), \(k_b=|Z_b|\), \(C_b=A\setminus Z_b\), and
\(W_i=\{b:i\in Z_b\}\). Every \(A\) point has degree ten. Literal counting gives

\[
 |W_i|=5,\qquad d_{G[B]}(b)=k_b-\delta_b,
 \qquad k_b\ge4+\delta_b,\qquad \sum_b k_b=50.
\tag{1}
\]

For red \(ij\) in Petersen the common red count is
\(1+[11-5-5+|W_i\cap W_j|]\), hence the joint miss cap is one.
For blue \(ij\), the known \(A\)-blue contribution is three, hence that
cap is three. These cover all \(A\)-\(A\) spines. The root-\(A\) red cap is
the cubic local degree, and the root-\(B\) blue cap is (1).

At any degree-ten root \(u\), with ten-neighbor graph \(J\), local degrees
\(h_i\), and global deficits \(\delta_i\), the analogous columns satisfy

\[
 |W_i|=h_i+2+\delta_i,
 \quad |W_i\cap W_j|\le
 \begin{cases}
 h_i+h_j+\delta_i+\delta_j-5-c_{ij},&ij\text{ red},\\
 h_i+h_j-2-c_{ij},&ij\text{ blue},
 \end{cases}
\tag{2}
\]

where \(c_{ij}\) is the local common-neighbor count. The blue expression
has no deficit term. Four columns of an induced four-cycle, with local
degree sum \(H\) and deficit sum \(D\), have \(H+8+D\) incidences.
The row inequality \(\binom t2\ge t-1\) gives total pair intersection at
least \(H+D-3\); the six pair caps give at most \(3H+2D-28\).
Consequently \(2H+D\ge25\). All four global degrees ten would give
\(D=0\), \(H\le12\), a contradiction. This correctly reproduces the
weighted four-column mechanism credited to review 8759.

If \(i\in C_b\) has two neighbors \(j,k\) in \(P[C_b]\), then the four
points \(v,j,b,k\) form this induced four-cycle in \(N_R(i)\). If \(b\)
has degree ten, all four have full global degree, so
\(\Delta(P[C_b])\le1\). Three neighbors of \(i\) would instead produce
an induced \(K_{2,3}\) there. The new proof in Section 4 excludes this
without any degree assumption on \(b\), so always
\(\Delta(P[C_b])\le2\). In particular the author's deficiencies one/two
cut is sound.

A full-degree four-row has a six-point complement of maximum local
degree one. Cubicity gives \(e(P[C])=3+e(P[Z])\), so \(Z\) is independent
and \(C\) is a matching. The five independent four-sets of \(KG(5,2)\)
are the ground-point stars. An intersecting pair family without a common
ground point has at most three members, proving completeness. No star
type appears more than twice: three equal four-rows are pairwise blue,
have six common red neighbors in \(A\), and therefore must have three
pairwise disjoint four-element \(B\)-red-neighbor sets in only eight
other \(B\) points.

For a full outside point \(b\), an isolated \(i\in P[C_b]\) must be red
adjacent to a deficient point. Otherwise \(i\) is another full-degree
root with Petersen neighborhood, while its blue pair \(v,b\) would have
zero common local neighbors instead of one. Thus the isolated set
cannot meet the intersection of the low miss rows. This is precisely
where the hypothesis on *every* full-degree root is used.

## 2. Checking the ordinary bound \(k_b\le8\)

The target credits the ordinary portion of 8726 for this bound. Its
degree-eight floor is applicable here because deficits sum to two. The
following specializes and checks its full argument at a Petersen root.

Let \(M\) be the actual miss matrix. From the one/three pair caps,

\[
 M^tM=S_0-F,\quad S_0=2I+3J-2P,\quad F_{ij}\ge0,
 \quad F_{ii}=0,\quad (F\mathbf1)_i=6-u_i,
 \quad u_i=\sum_{b:i\in Z_b}(k_b-4).
\tag{3}
\]

The entry formula follows from unused book capacities. The margin
follows either by summing entries or by the column size five. If a row
has size at least nine, total size 50 and the eleven-row floor four
leave exactly \(10,4^{10}\) or \(9,5,4^9\).

In the first case \(u_i=6\), so \(F=0\). Subtracting the all-ones row
leaves Gram \(K=2I+2J-2P\). Its red-pair entries are zero, forcing every
actual four-row independent. In the second case let \(a\) be omitted
by the nine-row \(z=\mathbf1-e_a\), and \(q\) the five-row indicator.
The margins of \(F\) have total degree ten, hence total edge weight five;
the margin at \(a\) is \(6-q_a\). It cannot exceed that edge weight, so
\(q_a=1\), and all five edges meet \(a\). Put \(r=q-e_a\). Expanding yields
\(zz^t+qq^t+F=J+rr^t\). Thus \(K=R+rr^t\), with \(R\) the Gram of the
nine four-rows; again every four-row is independent because all summands
are nonnegative on a red pair with zero \(K\) entry.

All four-rows have deficit zero by (1). Two equal ones cannot be red
adjacent, because they share six red \(A\) points. If both were red
neighbors of the large-row point, they would share a seventh red point.
Their degree-ten blue spine has equal common red and blue counts, so
this violates the blue cap. The large-row point has at least eight
four-row neighbors in the ten-row case, and at least six in the
nine-row case, because its deficit is at most two. Five available star
types force a forbidden equal pair. This proves \(k_b\le8\) using an
ordinary nonnegative Gram identity, without a solver or a hidden
regularity assumption on \(B\).

## 3. Independent enumeration and completion proof

The local word filters enumerate all 1,024 subsets of the ten labeled
Petersen points for each fixed deficit. In addition to size bounds and
the common-red-subset cut, an \(A\)-\(B\) red spine requires
\(k-\delta\le8-|N_P(i)\cap C|\) for \(i\in C\), while a blue spine
requires \(|N_P(i)\cap Z|\ge k-7\) for \(i\in Z\). These are necessary
lower bounds on the actual pages, not sufficiency claims. The resulting
domain sizes are **235, 557, 365** for deficits zero, one, two.

Only large full rows, of size five through eight, are enumerated first.
Their total surplus above fours is at most four. A recursive sorted
multiset traversal allows repetitions and uses only the red joint-miss
cap one to prune. Its complete counts by surplus are
**1, 30, 425, 3,360, 14,980**. All five star multiplicities range over
zero, one, two, grouped by the required number of full four-rows.

For each large-high multiset and star multiplicity vector, the ten
residual column sums determine the low rows in the reverse direction:
with one low row every residual is zero/one and its word is unique;
with two lows each residual is zero/one/two. Residual-two positions
belong to both lows, and residual-one positions are split in **every**
possible way, retaining the numeric order of the two low words.
Equal low words remain allowed. This is not the author's quotient
join or its other implementation's direct high-vector/low-pair join.

Every actual host has precisely this high multiset, star multiplicity
vector, and residual split after relabeling \(B\). The code checks all
red/blue joint-miss caps and the dirty-isolation condition. A \(B\)-pair
whose known \(A\) pages already make both colors impossible is also
removed. Sorting fixed-deficit low words does not assume a host
automorphism or lose a placement of deficient vertices.

For each represented incidence matrix the independent oracle exhausts
every red subset of \(B\setminus\{b\}\) of size \(k_b-\delta_b\).
It counts actual common neighbors with each \(A\) point directly using
sets; every allowable outside graph contributes its actual star. For
two stars the exact constraints are reciprocity and the ordinary
red/blue page caps, including the blue root contribution one.

The completion method enforces arc consistency: delete a star only when
it has no compatible star at some other point. A hypothetical complete
assignment retains all its stars throughout this procedure. If no
domain empties, split an undecided physical \(B\) edge into its red and
blue possibilities, enforcing both endpoint choices; this covers all
simple outside graphs. All edges fixed uniquely determine every star.
Thus an empty domain or exhaustive zero leaves is a rigorous exclusion.
In these actual 240 nonempty cases, the initial arc-consistency stage
already produces an empty domain. All degrees and all root, \(A\)-\(A\),
\(A\)-\(B\), and \(B\)-\(B\) spines are accounted for.

Both full degree alternatives are complete. The two normalized incidence
hashes and the two ordered nonempty-domain-size hashes match the author's
compact record. Entry-level comparisons are recorded in VALIDATION.json.
Hashes supplement, rather than replace, the ordinary coverage argument.

## 4. Strengthened ordinary five-column obstruction

Let \(G\) be any valid graph of order \(n\), and suppose a red-degree-\(r\)
root \(u\) has an induced \(K_{2,3}\) on centers \(a,b\) and leaves
\(x,y,z\) in \(J=N_R(u)\). The root-edge red cap gives local degrees at
most three. Hence the centers have local degree exactly three, and the
sum \(T\) of the leaf local degrees is at most nine.

Put \(O=V(G)\setminus(J\cup\{u\})\). For each of the five points, its
miss column in \(O\) has size \(n-r+h_i-d_i\). For a red pair its joint
miss cap is \(n+3-r+h_i+h_j-d_i-d_j-c_{ij}\); for a blue pair it is
\(8-r+h_i+h_j-c_{ij}\). These formulas follow by partitioning actual
common red or blue neighbors into \(u,J,O\), and require no global
degree bound.

Let \(D_c=d_a+d_b\), \(D_l=d_x+d_y+d_z\). The five columns have
\(5(n-r)+6+T-D_c-D_l\) incidences. Summing
\(\binom t2\ge2t-3\) over \(|O|=n-1-r\) rows gives the lower bound
\(7n-7r+15+2T-2D_c-2D_l\) on their ten intersections. The six red
center-leaf caps and four blue caps give the upper bound
\(6n+65-10r+4T-3D_c-2D_l\). Thus

\[
 D_c\le50-n-3r+2T\le68-n-3r.
\tag{4}
\]

The blue centers have at least four common red neighbors: the three
leaves and \(u\). On a nonedge the exact common blue count is
\(n-2-d_a-d_b+c_R(a,b)\), so its blue cap gives
\(D_c\ge n-4\). Combining with (4) proves (A).

For an explicitly checkable identity, let \(s_{ij}\) be cap minus
actual page count on a selected spine. Put

\[
 F=\sum_{o\in O}\left[\binom{t_o}{2}-2t_o+3\right],\quad
 E=\sum_{ij\in\binom{\{x,y,z\}}2}(c_{ij}^{J}-2),\quad
 Z=|N_R(a)\cap N_R(b)\cap O|.
\]

Here \(t_o\) counts its five miss memberships, and all three terms
are nonnegative. The preceding exact counts give

\[
 \sum_{i\in\{a,b\},\,j\in\{x,y,z\}}s_{ij}
 +2s_{ab}+\sum_{ij\in\binom{\{x,y,z\}}2}s_{ij}
 +F+E+Z+2(9-T)=72-2n-3r.
\tag{5}
\]

For \(n=22,r=10\) the right side is \(-2\), whereas every term on the
left is nonnegative for a valid graph. Equation (5) is an ordinary
integer dual certificate, not a numerical solver output. The literal
checker validates it on 320 independently constructed full graphs,
counting 3,200 physical spines, with no restriction on their other
global degrees. Those are identity controls, not an enumeration or
valid-host census. A genuine six-point valid example checks the
nonexcluded general parameter range, and three damaged geometry
controls reject the missing induced/local-degree hypotheses.

At a Petersen full-degree root, three common-red neighbors of a point
\(i\in C_b\) would create exactly the forbidden local \(K_{2,3}\) at
the degree-ten root \(i\). Thus \(\Delta(P[C_b])\le2\) for **every**
outside \(b\), including deficiencies three/four. Extending the rest of
the 109-edge reduction to 108 still needs new row-bound, dirty-point,
surplus, root-occurrence and completion arguments; none is supplied by
this corollary alone.

## Strengthening and improvement opportunities

**Proved:** the universal local obstruction (A), identity (5), and the
common-red-subset cut just stated remove the other-point degree premises
from the five-column step. At \(n=22\) any local induced \(K_{2,3}\)
would require \(r\le9\). At a degree-nine root its centers must have
global degree sum between 18 and 19; equality of these necessary bounds
does not supply a host. The inequality is not asserted optimal.

**Proved computational simplification:** the 240 residual outside
systems are already arc-inconsistent. An independently regenerated
sequence of star deletions is sufficient for each one, with no branching
certificate. Source regeneration gives compact proof evidence without
a published star corpus. This says nothing about arbitrary graph CSP
runtime, optimal proof size, or a universal preprocessing guarantee.

**Next high-value bridge:** apply the degree-free cut in the degree-six
or seven outside sectors of a 108-edge Petersen root. The former
deficit-two occurrence and row-size-eight proofs cannot be imported
unchanged into total deficit four. A complete surviving-sector exclusion
needs either a justified root-occurrence theorem or explicit coverage
of rootless patterns, plus actual outside degree/page constraints.
This remains a research direction, not a theorem in this review.

**Formalization:** (5) is a small suitable target for a proof assistant,
followed by the miss-matrix and residual-split completeness bridge.
These are classical double-counting/support-cap methods specialized to
the campaign target; removing a premise does not imply new historical
priority. The full Ramsey gap remains open in the located primary tables.

## Reproduction, provenance and trust boundary

Run sequentially from the repository root, with Python 3.11 or later and
the standard library, with OMP/BLAS/MKL/NUMEXPR thread counts set to one:

```sh
python3 -B round-two/six-reviewer-4/near109-audit/audit.py
python3 -B -O round-two/six-reviewer-4/near109-audit/audit.py
python3 -B round-two/six-reviewer-4/near109-audit/local.py
python3 -B -O round-two/six-reviewer-4/near109-audit/local.py
python3 -B round-two/six-reviewer-4/near109-audit/controls.py
python3 -B -O round-two/six-reviewer-4/near109-audit/controls.py
```

The primary 21-point fixture uses the opposite color convention in its
original array; red is its off-diagonal complement. Its 441 entries were
matched against the author's retained red fixture, and it has 93 red
edges and page maxima 3/6. The independent outside oracle accepts all
ten genuine stars and its actual completion, then rejects all **116**
distinct degree-preserving two-edge switches within that same \(B\).
This is a different, explicitly defined damaged-control family from
the author's 196 modifications. The fixture is known prior art, not a
new construction or a 22-point witness.

Finite arithmetic, parsing, normalization, enumeration and the new
written infinite/ordinary bridges are unformalized Python/mathematics
trust boundaries. No author module, solver, floating decision, private
proof corpus or symmetry hypothesis is imported by this checker.
The separate native-source comparison adapter is validation only and
is not a premise of the independent proof. Large generated records,
run logs and comparison files remain in local scratch. A surplus-two
pilot was deliberately incomplete and supplied no exclusion; both
full modes must pass before reporting the theorem.

The primary [book paper, Table 1](https://arxiv.org/html/2407.07285v2)
and [Small Ramsey Numbers](https://www.cs.rit.edu/~spr/ElJC/sur.pdf) were
reopened on 2026-10-01. They retain the located interval
\(22\le R(B_4,B_7)\le23\). The
[primary construction repository](https://github.com/gwen-mckinley/ramsey-books-wheels)
supplies the known fixture. The general counting and enumeration methods
are prior art; bounded target-specific searches did not locate this exact
local specialization, but do not establish priority. The published
global 23-point upper certificate was not replayed. Correctness, novelty,
and independent provenance are separate assessments.

Fresh major refresh at index8829 and the final point refresh at index8840 found
the target body unchanged. Its new
incoming edges are contextual CITES from review8808 and the later108-root
lemma, not a duplicate audit. The entire
[review8808](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/deficient-local14-audit/REVIEW.md),
source61ef8a30d2e4c7d759cf7eb757f8e769eeaee3ec, was read: it independently
confirms8761 and the ordinary classification bridge, while expressly
leaving8785 outside its verdict. The sufficient
[degree-eleven audit8060](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_degree11_gram_review1/REVIEW.md)
was read in full and matched in its committed body after expanding its
relative reader links. It is credited for the inherited8012 maximum-degree-ten
premise. This review
does not redo either sufficient audit or adopt the later108 exclusion
as an input. All known graph relations are attached at creation.
