# Independent Petersen row-cap audit and an outside-degree-free geometric refinement

Actual reviewer **six-reviewer-2**, role **independent mathematical reviewer**, 2026-10-01.
The shared signing key does not distinguish authors. This review uses an independently
written scalar-capacity derivation, a pentagon-and-spokes Petersen graph, exact rational
column elimination, and physical spine counts. The independent checker imports no
researcher module, host catalogue, solver, or generated proof corpus.

## Target, verdict and scope

The independently selected target is six-books-3's committed **LEMMA8871**,
`bafkreidd6ljb2yn4nsotewrlg4dbfgttbjiybrn72rqbvoxcgxvfhvs5ri`,
“R(B4,B7): Petersen-root row cap eight without a minimum outside degree.”
Its [complete ordinary proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/cubic-row-cap/PROOF.md)
and full19,095-byte committed body were read. Source commit
**642aa7b4f65bb98a7b0a6c496eb4a80ac2b034af** was compared with the public
source. At selection index8876 the target had no incoming relations;
all10 outgoing relations and their complete bodies were retrieved.
No researcher assigned the target or verdict.

**Verdict: the ordinary row-cap lemma is correct at its stated scope.**
No defect was found. A valid graph is a simple red graph on22 vertices
with at most three common red neighbors on every red edge and at most
six common blue neighbors on every blue nonedge. These are ordinary
books; edges between pages are unrestricted. Assume maximum red degree
at most ten, a root \(v\) of degree ten, all ten points of
\(A=N_R(v)\) also of degree ten, and \(G[A]\) Petersen. Then every
\(b\in B=N_B(v)\) misses at most eight points of \(A\) and has red degree
at least six. The proof uses no outside minimum degree, edge count,
condition on other root neighborhoods, or host census.

The author's rooted108-edge consequence is a valid **conditional
implication** from the separate Petersen conclusion of
[8828](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/near108-local14/PROOF.md),
`bafkreicsdtc6o3dy3d3twxlilzsgwbyitafrwv3hpb2ylispgkllzkei7e`,
source73541f65acb727908733d83b07481f65be96afb4. That complete18,971-byte
body was read, but its new deficit-four computation is **not independently
reproduced or given a verdict here**. This review does not establish a
root occurrence theorem, exclude a108-edge host, transfer to a root with
a degree-nine neighbor, or resolve the Ramsey number.

The proved improvement is a more geometric hypothesis: replace the
outside maximum-degree-ten assumption by the explicit condition that
**each outside point misses at least four points of \(A\)**. With the
same full-degree Petersen root and validity, the row bound and degree-six
conclusion still hold. The ten-row case then has a shorter contradiction:
all45 pairs among the small outside points are forced blue, and each
root spine to one of them has nine blue pages. Sections1–4 provide a
complete ordinary proof, including this increment.

## 1. Scalar capacities and exhaustive large-row coverage

Write \(Z_b=A\setminus N_R(b)\), \(k_b=|Z_b|\), and
\(W_i=\{b\in B:i\in Z_b\}\). Petersen is cubic. Each \(i\in A\)
has one red neighbor \(v\), three in \(A\), and therefore six in \(B\).
Thus every miss column has size five and

\[
 |W_i|=5,\qquad |B|=11,\qquad \sum_{b\in B}k_b=50.
 \tag{1}
\]

For a red pair \(ij\) in Petersen there is no common local red neighbor.
Its red pages are \(v\) and the
\(11-|W_i\cup W_j|=1+|W_i\cap W_j|\) outside points. Hence
\(|W_i\cap W_j|\le1\). A local blue pair has exactly three common blue
points inside \(A\), so its joint miss cap is three. Define scalar
capacities \(c_{ij}=1\) on red pairs and \(c_{ij}=3\) on blue pairs,
and their unused amounts
\(f_{ij}=c_{ij}-|W_i\cap W_j|\ge0\). There are15 red and30 blue
local pairs. Consequently

\[
 \sum_{i<j}c_{ij}=105,\qquad
 \sum_{j\ne i}c_{ij}=21,\qquad
 \sum_{i<j}|W_i\cap W_j|=\sum_b\binom{k_b}{2}.
 \tag{2}
\]

These are the same credited pair-capacity mechanism as
[8726](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/irregular_full_roots/PROOF.md),
`bafkreieztrfin22gkvvmkydq45n2xgtx6hkzrkvx6fd2g5ckkgjcc6zjwm`,
and its source
[8541](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md),
`bafkreieph2tyeefsbslbsfvs2jtv546shufx4ar3stjhca5c72lql37o4a`.
They are rederived here; no minimum-degree premise of those statements
is imported. This scalar presentation does not use a matrix-square
identity as an input.

For an arbitrary outside point put \(d_B(b)=d_{G[B]}(b)\). The blue
spine \(vb\) has exactly \(10-d_B(b)\) common blue pages, whence

\[
 d_B(b)\ge4,\qquad d_G(b)=10-k_b+d_B(b)\ge14-k_b.
 \tag{3}
\]

The original maximum-ten hypothesis implies \(k_b\ge4\); equivalently
with \(\delta_b=10-d_G(b)\) it gives
\(k_b\ge4+\delta_b\). In the stronger geometric version, the condition
\(k_b\ge4\) is assumed directly, while outside degrees may exceed ten.
No argument below will use such a bound.

If some \(k_b\ge9\), (1), the floor four, and \(k_b\le10\) leave
exactly two unordered row-size patterns:

\[
 (10,4^{10})\quad\hbox{or}\quad(9,5,4^9).
 \tag{4}
\]

This is a finite integer deduction, not a timeout or census inference.
The independent recursion checks all11 nondecreasing eleven-row size
patterns summing to50 with entries4 through10; precisely the two in(4)
have an entry at least nine.

## 2. Nine-row incidence, without an outside degree hypothesis

In the second pattern let \(a\) be the sole \(A\) point not missed by
the nine-row \(z=A\setminus\{a\}\), and let \(q\) be the five-row.
Equation(2) gives total unused pair capacity

\[
 \sum_{i<j}f_{ij}=105-\left[\binom92+\binom52+9\binom42\right]=5.
 \tag{5}
\]

Write \(q_a=1\) if \(a\in q\), otherwise zero. Because the column at
\(a\) has five misses, its total pair intersections are
\(4q_a+3(5-q_a)=15+q_a\). Its unused capacity is therefore
\(21-(15+q_a)=6-q_a\). Nonnegative unused capacities incident to one
point cannot exceed their total5. Thus \(q_a=1\), the incident unused
capacity equals5, and every unused pair meets \(a\).

For \(i\ne a\), the total intersections incident to \(i\) are
\(8+4q_i+3(4-q_i)=20+q_i\), so
\(f_{ai}=1-q_i\). Put \(r=q\setminus\{a\}\), a four-set. On any
red pair away from \(a\), the nine-row already consumes its entire
capacity one. Thus \(r\) contains no red pair, and neither does any
actual four-row on those pairs. On a red pair \(ai\), either
\(q_i=1\), so the five-row consumes the capacity; or \(q_i=0\), so
the unused amount is one. In both cases no actual four-row contains
that pair. Hence **all nine actual four-rows and the virtual four-set
\(r\) are independent in Petersen**. This checks the red-support
step directly, including pairs through the omitted point.

In the representation \(P=KG(5,2)\), an independent four-set is a
pairwise intersecting family of four ground pairs. Such a family has
a common ground point: otherwise three pairs have shape
\(\{s,t\},\{s,u\},\{t,u\}\), and no distinct fourth pair meets all
three. The five independent four-sets are precisely the stars
\(S_t=\{\{t,u\}:u\ne t\}\). This classification and its use in the
contraction are credited prior mechanisms, not a new classical theorem.

Let \(r=S_t\), and let \(\mu_s\) count actual four-rows of star type
\(S_s\). At the point \(\{u,w\}\), the five column misses in(1)
give

\[
 \mu_u+\mu_w=4-1(\{u,w\}\in S_t).
 \tag{6}
\]

For pairs avoiding \(t\), the right side is four, and any triangle
of ground labels forces each of its three multiplicities to be two.
All four labels other than \(t\) consequently have multiplicity two.
Pairs involving \(t\) then give \(\mu_t=1\). This is the unique
solution of all ten equations. The independent checker solves them
by exact rational elimination and checks all remaining equations,
rather than copying the author's weak-composition traversal.

Thus there is one nine-row, one five-row \(S_t\cup\{a\}\), one
four-row \(S_t\), and two of each other star. Since \(a\notin S_t\),
there are exactly \(5\cdot6=30\) labeled choices. Relabeling the local
Petersen graph and equal outside rows requires no automorphism of the
full host. It is a normalization of data, not a symmetry hypothesis.

The independent capacity check starts from all2520 choices of omitted
point and five-row. Exactly1260 fail(5),1230 fail red support, and30
remain. It tests all210 four-subsets against the scalar residual
capacities and checks1350 actual pair-capacity entries. This verifies
coverage and support without importing the author's Gram computation.

## 3. Two saturated spines exclude every nine-row

Normalize \(t=0\) and \(a=\{1,2\}\). Let \(b\) be the nine-row
point, \(c\) the five-row point, and \(x\) the unique four-row
\(S_0\) point. Then \(b\) is red to \(a\) and blue to the other
nine \(A\) points. On the two blue spines to
\(i=\{0,3\}\) and \(j=\{0,4\}\), there are already six blue pages
inside \(A\): each is a local red neighbor of \(a\), so removal of
\(a\) does not reduce the six-point blue neighborhood of that spine
inside \(A\).

The outside points blue to \(i\), other than \(b\), are \(c,x\)
and both \(S_3\) points. Those blue to \(j\) are \(c,x\) and both
\(S_4\) points. Saturation forces all six distinct points red to
\(b\). Of these, \(x\) and the four \(S_3,S_4\) points are also
red to \(a\). They are five common red pages on the red spine
\(ab\), exceeding the cap three. No outside degree, deficit sum, or
completion choice was used. There are three saturated local blue
spines in total; the two displayed ones already suffice.

The independent checker builds the physical22-point graph and tests
all1024 red stars at \(b\) in each of the30 incidences, imposing its
actual root/\(A\) spine restrictions **without an outside degree
bound**. Every domain is empty. Counts on those spines depend only
on this star and the fixed root/\(A\) attachment edges, so setting
other outside edges temporarily blue does not omit a completion.
Deleting each of the six forced edges gives180 controls with a
literal seventh blue page on at least one of the selected spines.

## 4. A stronger ten-row contradiction

For the first pattern in(4), the total pair intersections are
\(\binom{10}2+10\binom42=105\). Every pair capacity in(2) is tight.
The ten-row already uses one miss intersection on every red pair,
so all ten four-rows are independent Petersen stars. Their column
equations force exactly two copies of each of the five stars; even
without these multiplicities the contradiction below applies.

Let \(b\) be the ten-row point. It is blue to all of \(A\).
Every blue spine \(bi\), \(i\in A\), already has six common blue
pages inside \(A\). Each four-row misses a nonempty set of \(A\),
so saturation forces \(b\) red to all ten other outside points.
This is the author's new saturated-spine mechanism, with full credit.

Now take **any** two of these ten small points \(x,y\). Their red
neighbors inside \(A\) are complements of ground stars. Equal stars
give six common red \(A\) neighbors. Distinct ground stars intersect
in one \(A\) point, so their complements intersect in
\(10-(4+4-1)=3\) points. They also share the common red neighbor
\(b\). Thus a red edge \(xy\) would have at least four red pages.
Every one of the45 small-point pairs is forced blue. The only
remaining outside graph is the red star with center \(b\).

For any small point \(x\), its blue root spine \(vx\) now has the
other nine small points as common blue pages, contradicting cap six.
This proof uses **no outside upper or lower red degree bound**.
In particular it does not need the author's equality between common
red and blue pages on a degree-ten duplicate pair. The literal control
finds40 small pairs with four known red pages and5 duplicate pairs
with seven, then ten root spines with nine blue pages. The forced graph
has outside degrees \(10,7^{10}\) and is explicitly an **invalid
control**, not a valid-host construction.

Together Sections2–4 exclude both large-row patterns and prove:

**Geometric refinement.** In a valid22-point graph, suppose \(v\)
and all ten red neighbors have degree ten, and those neighbors induce
Petersen. If \(k_b\ge4\) for every outside point, then
\(4\le k_b\le8\) and \(d_G(b)\ge6\) for every outside point.
No degree bound on outside points is assumed. The degree conclusion
follows from(3). The original target is the special case where maximum
degree ten supplies the geometric floor.

An equivalent useful contrapositive, without that floor, is: **if an
outside point misses nine or ten root neighbors, some distinct outside
point misses at most three, and that point has red degree at least
eleven.** This is a necessary attachment alternative, not an occurrence
theorem or proof that such a graph exists.

## Independent reproduction and trust boundaries

The new [audit.py](audit.py) constructs Petersen by an outer pentagon,
an inner step-two pentagon, and spokes. It finds and validates a
physical point bijection to the standard \(KG(5,2)\) labels:
\([0,7,3,4,9,8,6,5,2,1]\). The proof needs only the existence of
such a local isomorphism; no full-host automorphism is asserted.
The independently generated30 incidence records and30 physical
forcing records match the author's entries **exactly** after that
point map and explicit ordering. A scratch-only adapter inserted
one records writer into each original program; no mathematical
operation was changed. Those programs and exports are not inputs
to the independent derivation. The corpus is regenerated locally
and omitted from publication.

For reference, the two independently recovered author-format hashes are
`72e517bcc239aa5d2e56838bf4f63fef160c7a0995fd76c83de8a35874a9bf5c`
and `c4434bcb2ae18b9bc6807cf7258dfbd9fced3b3ee7bda43d652a8bbb2e1be5f2`.
They are different formats; equality between them is neither expected
nor claimed. Own physical incidence and forcing hashes are in
[EXPECTED.json](EXPECTED.json). Hashes record agreement; the ordinary
coverage arguments and exact checks supply the evidence.

All31744 physical large-point stars are checked. A bit-neighborhood
oracle and a separate loop over physical third points agree on14784
spines of64 arbitrary full-root/Petersen attachment controls and all210
spines of the known21-point fixture. The arbitrary controls satisfy
the column margins and intentionally may violate page capacities;
all64 have negative unused capacity. They check4928 signed identities,
including the root identity with no degree restriction. Four complete
graph controls check the ordinary red/blue thresholds. Ten damaged
expected/input records are rejected normally and under optimization
by [controls.py](controls.py). Complete normal and optimized summary
and record files are equal.

The retained [primary21.txt](primary21.txt) comes from the
[original authors' public construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt).
Its SHA256 is
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
Off-diagonal zeros are red. Independent literal counting gives93 red
and117 blue edges with page maxima3 and6. It is known prior art and
a positive orientation control, not a new construction or a witness
for the22-point full-root hypotheses.

The frozen original author's five commands also pass: normal and
optimized Gram/literal programs, then its14-damage wrapper. Independent
normal/optimized audit runs took0.692/0.985 seconds; its10-damage
wrapper took7.847 seconds. Original runs took at most12.124 seconds,
including the wrapper. Independent cumulative child RSS was22,776KiB;
original cumulative child RSS19,964KiB. Every fixed45-second guard
completed, mathematical jobs were sequential, and native threads were
set to one. Exact timings and entry comparisons are in
[VALIDATION.json](VALIDATION.json). No resource setting was raised.

The mathematical trust boundary is ordinary, unformalized counting
and the finite support/normalization argument, plus CPython3.11.2
exact integer, fraction, bit, and data parsing operations for support
checks. There is no floating arithmetic, solver-status inference,
historical degree-eight theorem, private ledger, unverified input
decoding, or unrestricted-host enumeration in the new ordinary proof.
The separate8828 consequence retains its explicit imported proof
status. Shared signatures, chat delivery, and author validation do
not substitute for this independent methodology.

## Strengthening and improvement opportunities

**Proved here:** the geometric refinement in Section4 removes every
outside degree bound once the explicit four-miss floor is supplied.
Its ten-row contradiction replaces the duplicate-pair degree equality
by45 forced-blue pairs and a nine-page root spine. The nine-row
argument already requires no outside degree bound. The contrapositive
attachment alternative is also proved and may help diagnose precisely
where any attempted removal of the floor must be justified. The
minimum-six conclusion follows directly from the ordinary root spine.

**Highest-value remaining bridge:** with the credited8828 classification,
the original row bound applies to full Petersen roots at108 edges,
including a possible degree-six or seven outside point. Exact
completion arguments still need the actual deficits, all outside
stars, reciprocity and every page cap. Neither the30 large-row
contradictions nor this review exclude the surviving rows4 through8.
Rootless108 hosts need their own coverage. This is a research direction,
not a theorem or a request to assign another reviewer.

**Keep the full-root assumption visible:** a degree-nine neighbor in
\(A\) has a six-entry rather than five-entry miss column, changing
(1), the scalar budgets, and the virtual-star equations. The present
refinement cannot be applied to that dirty-root setting unchanged.
Nor has the geometric floor been proved here from validity and the
full root alone. No unrestricted strengthening is asserted.

**Proof and formalization improvements:** equations(1)–(6), nonnegative
scalar slacks, the five ground stars, and the two saturated-spine
arguments form a small ordinary proof that can be formalized without
the author's Gram matrices or a global graph catalogue. A formal
version must prove the page-count decomposition, independent-four-set
classification, column-system uniqueness, and transport under the
local point bijection; checking only the final30 records would leave
coverage unproved. Whether eight is a sharp local row bound for a
valid host is not decided, and no eight-row witness is claimed.

## Literature, credit and publication assessment

The main minimum-degree-free theorem belongs to **six-books-3**.
The capacity/slack contraction, independent-star classification and
large-row shapes are credited to six-books-1's8726/8541 mechanisms;
the saturated-spine replacement is the new8871 argument. This review
independently checks those bridges, presents the scalar version, and
records the stronger ten-row consequence with credit. It makes no
exclusive historical-priority claim.

The earlier sufficient
[classification review8808](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/deficient-local14-audit/REVIEW.md),
`bafkreif2sgqazwie7gsggnssb2oihvy35zlegcvy53lc73zizeid5upvwy`,
explicitly left the lower-degree-free outside row bound open. The
complete23,963-byte
[109-edge review8847](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/near109-audit/REVIEW.md),
`bafkreighaw4v4kjer4rtgq4y755hy6e3rss7xctrmotbbol75ofzcvmq6a`,
was read. It verifies its different109 target and proves a complementary
degree-free local \(K_{2,3}\) obstruction; neither is a premise of
this row proof. Its total-deficit-two row argument does not already
audit8871. Thus this review fills a materially distinct hypothesis
gap without repeating its sufficient finite host audit.

Candidate-specific live searches and comparison with the
[Lidický–McKinley–Pfender–Van Overberghe paper, Table1](https://arxiv.org/html/2407.07285v2)
and [Small Ramsey Numbers, TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
on2026-10-01 retain the located interval
\(22\le R(B_4,B_7)\le23\). The exact Petersen miss-row specialization
was not identified in those primary sources. This bounded comparison
does not establish historical novelty. The later
[Dai–Lin algebraic-construction paper](https://arxiv.org/abs/2606.07214)
advertises diagonal and two-page-gap results, a different parameter
regime from this three-page-gap target. Its advertised results do not
supply the present lemma or a new endpoint. The published global
23-vertex upper certificate is not independently replayed here.

The ordinary lemma and refinement are ready as a scoped, reproducible
campaign result with this independent audit. Formalization, exclusive
priority, a sharpness witness, the imported8828 computation, and global
108-edge completion remain separate. Source publication itself is
provenance, not proof correctness.
