# Exact scope of the transversal countermodel

All graphs are finite, simple and labeled. Red means edge and blue means
nonedge. A graph is good if both colors avoid a clique of order five.

## 1. The complete pentagon hypergraph

Let H(G) contain precisely the five-vertex sets inducing C5 in G. An independent
set of this hypergraph is a vertex set inducing a C5-free graph. A transversal
meets every induced pentagon, so its minimum size is n-alpha(H(G)). All these
objects involve every pentagon; none selects a root or assumes an automorphism.

Dyson--McKay's Theorem 1.2 gives N5=21: every graph on 21 vertices has a regular
induced five-set. Its common degree is 0, 2, or 4, giving I5, C5, or K5.
Therefore a hypothetical good43 must satisfy alpha(H(G))<=20, equivalently
transversal number at least 23. This is the external coverage premise from
[arXiv:2604.08215v3](https://arxiv.org/html/2604.08215v3#S1.Thmthm2).
The order-20 computation is not replayed; the reported separate comparison
for that computation reaches order 15. The present certificate proves the
cover for its explicit control without using N5.

## 2. The precise necessary system Q

For a physical pair e, let q_e be its common-neighbor count in its own color,
and let H_e be the graph on those common neighbors. Put

    L(q)=0 for q<=9; L(10)=2, L(11)=4, L(12)=7, L(13)=12.

For each pentagon P and color c, U_c(P) consists of vertices outside P joined
to all of P in c. Let W count seven-sets inducing K2 join C5 or its complement.
The following is the entire system assessed in this pass:

1. G is a physically realized simple graph on 43 vertices; its pentagon and
   joined-edge incidence sets are their full induced sets.
2. Every degree is 18..24, the red edge count is 390..513, and q_e<=13 for
   every physical pair e.
3. Every H_e has at least L(q_e) induced pentagons.
4. For every P and c, |U_c(P)|<=13 and e_c(U_c(P))<=2|U_c(P)|<=26.
5. With sigma=sum_v(d(v)-21)^2, N_i the number of q_e=i pairs, and

       F=2 sum_(e:q_e<=8)(9-q_e) + N_12 + 4N_13,

   sigma is odd and positive, and

       W >= 903+3 sigma+F >= 906,
       W = sum_e p(H_e)
         = sum_P [e_R(U_R(P))+e_B(U_B(P))],
       W <= 2 sum_(P,c)|U_c(P)| <= 52|H(G)|,  |H(G)|>=18.

6. Every 21-vertex set contains a member of H(G).

The degree facts are classical; the 390..513 window is the committed h4009
result accepted at h4017 subject to its stated complete-catalogue boundary.
The pentagon inequalities are h3615, independently accepted at h3619, with
the elementary h3593 input. These are inherited necessary conditions, not new
claims. No source-uncommitted stronger edge window is required.

Q preserves the numerical consequences displayed above of the no-K5 condition.
It does not impose triangle-freeness in every H_e. This missing condition
cannot be silently inferred from a pentagon count or from global coverage.
For any graph, requiring all H_e to be triangle-free in their respective
colors is **exactly equivalent** to avoiding monochromatic K5s: any triangle
in H_e joins e to a K5, and any K5 supplies such a triangle for each of its
pairs. Reintroducing that whole physical condition would restore the original
Ramsey obligation, not close it through this projection.

## 3. The explicit countermodel

The graph is copied byte for byte from the existing pentagon-normal-form
control. [CONTROL_ORIGIN.json](CONTROL_ORIGIN.json) records its public source
and hash. It is not modified, optimized, extended or proposed as a new witness.

Complete literal auditing gives:

- 459 red edges; 28 degrees equal 21 and 15 equal 22;
- q distribution: 7:4, 8:309, 9:214, 10:150, 11:72, 12:119, 13:35;
- 18,535 induced pentagons and W=12,946 under both incidence counts;
- sum_(P,c)|U_c(P)|=35,774; every such set and its same-color edge count
  are at most 5;
- sigma=15, F=893, hence the required W lower bound is 1,841;
- zero failures among all 903 local p(H_e)>=L(q_e) inequalities and all
  37,070 homogeneous-set/edge-cap checks.

`audit.py` scans all 962,598 five-sets. It finds exactly the seven listed
monochromatic five-sets in EXPECTED.json, while collecting the full pentagon
family. It then evaluates every pair and every pentagon in each color.
For example, {0,1,21,22,42} is the red K5. Thus the graph is definitively bad.
The seven defects give 51 distinct anchor pairs whose common-neighbor graphs
violate the missing triangle-free condition. This is a precise omitted
hypothesis, not a new solver residual or an authorization to start gluing.

## 4. Complete certificate for all 21-sets

A proof node has a selected vertex set S and a candidate set C, initially
S empty and C all 43 vertices. S is C5-free, and every vertex in C can
individually be added without creating a pentagon. The state represents
all C5-free sets T with S subset T subset S union C. Excluded vertices are
never silently reinstated.

At a branch on v in C there are two disjoint cases:

- Include v. Set S'=S union {v}. Remove v from C and remove every w for which
  S' union {w} contains a pentagon. Such a pentagon consists of w and four
  selected vertices. These deletions remove no valid extension.
- Exclude v. Keep S and replace C by C minus {v}.

A terminal node partitions C into groups Q_1,...,Q_k. Every two vertices
u,v in the same group must have a pentagon consisting of u,v and three
vertices of S. A valid extension can therefore take at most one vertex
from each group. If |S|+k<21, no 21-set is represented by this node.

The two branch cases exhaust the parent state. The leaf argument is an exact
upper bound, so induction up a complete tree excludes every C5-free set of
size 21. Larger independent sets are excluded because each contains a
21-subset. This is the complete global join **for the supplied control**,
not a proof over all good43 graphs.

### Producer

`cover.cpp` collects all pentagons by induced-degree checks. For every triple
it indexes complementary pairs of vertices completing a pentagon. In a state,
a conflict graph on C joins two candidates when three selected vertices
complete such a pentagon. Adding v removes its existing conflict neighbors;
new selected triples containing v update the conflict graph. Greedy clique
partitions produce possible leaf bounds. A failed bound triggers the complete
binary branch, with no time or node cap.

The output contains branch choices and leaf group masks, not trusted solver
verdicts. Vertex masks use 43 bits in uint64_t; the triple index is at most
C(43,3)-1=12,340. Cycle counts, state counts and edge masks remain within the
declared unsigned domains.

### Separate checker

`check_cover.py` imports no producer. It tests all five-sets against the twelve
explicit labeled cycle edge patterns, rather than the degree criterion.
At inclusion branches it reconstructs forced removals by looking for complete
pentagons with four selected vertices. It does not maintain the producer's
incremental conflict graph or repeat its branch heuristic.

For each leaf it checks a disjoint exact partition of C, the cardinality
bound, and each within-group pair against a literal pentagon whose other
three vertices are selected. Every branch has two checked children. Missing
nodes, trailing nodes, invalid selections, incomplete partitions and false
pair witnesses are rejected.

The exact accepted tree has 408,771 nodes, 204,386 leaves and 688,492 checked
leaf-pair conditions. At most ten selected vertices occur in a node; leaf
bounds certify the rest. This proves all C(43,21)=1,052,049,481,860 required
sets contain a pentagon without enumerating that many sets individually.
The 30,159,116-byte proof is retained outside Git and regenerated exactly.
Its SHA-256 is
94a7e9c0fda102dbb0d811a1108c68cd6646450d28e82be0025a087b5372a3a3.

The same pentagon count is recovered by the producer, checker and physical
audit. A full sanitizer generation matches the proof bytes. A damaged leaf
is rejected, and an empty 43-vertex control produces a C5-free 21-set and a
non-proof status. These are author implementation checks, not peer review
or a proof-assistant formalization.

## 5. Consequence and final research boundary

The exhibited physical graph belongs to Q and has seven Ramsey defects.
Thus Q is consistent, and no sound contradiction can be deduced from Q
alone. In particular, imposing exact global 21-set coverage on the retained
numerical incidence system does not repair its insufficient Ramsey semantics.
This conclusion covers the specified system, not every possible global
pentagon-incidence approach or every later strengthening.

No nonexistence certificate, verified good43, or all-good43 reduction with a
quantitatively finishable residual was obtained. The final trial gate is
missed. The all-pentagon lane is parked and the slot requires reassignment
within R(5,5), with all previous evidence and pending references preserved.
No third pass, stronger-threshold sweep, component extension, physical formula,
carrier queue, moment hierarchy, separator or other parked program is started.
