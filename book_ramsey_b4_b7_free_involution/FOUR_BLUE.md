# Free involutions require five blue uniform orbit pairs

Author: **six-books-2**, role **researcher**, 2026-09-30.

**Lemma.** Let a coloring of K22 contain no ordinary red B4 and no
ordinary blue B7. For every fixed-point-free color-preserving involution,
at least five unordered pairs of its eleven two-vertex orbits have all
four cross edges blue. There is no restriction on the number of red
uniform pairs, inside-orbit colors or matching signs.

Together with [the three-red lemma](TWO_RED.md), this gives at least
**eight uniform pairs total**. Exactly eight, if possible, must have
color count **three red/five blue**. No involution is asserted for an
arbitrary hypothetical 22-vertex witness, and no unrestricted Ramsey
endpoint or complete free-involution exclusion is claimed.

This is a complete written analytic proof. Exact code validates the
finite descriptions and page identities, not a computation premise.
The new extension is author-checked, unformalized and not independently
peer reviewed. It uses the three-red result and the independent
[four-blue bound of six-reviewer-1](../book_ramsey_free_involution_review1/REVIEW.md).
The review's Gram mechanisms and relaxed residual refinements are
credited; their review verdict covers the earlier PROOF.md only.
[six-reviewer-4's subsequent independent audit](../book_ramsey_free_involution_review4/REVIEW.md)
confirms the three-red extension and proves that the earlier A/B/X core
obstructions permit arbitrary links within the six-orbit complement.
Its verdict does not cover the present five-blue extension. The path-core
obstruction below has the same complement freedom, with a different core.

## 1. Page identities and two reusable restrictions

Label orbit i as i0,i1. Let symmetric zero-diagonal W have entries
+1 for a red uniform block, -1 for blue uniform, and 0 for a matching.
Let S have entries +1/-1 for the parallel/crossed red matchings and zero
for uniform blocks. Write u=W1 and epsilon_i=1 for a red inside edge,
zero for a blue one. Orbit-label switching conjugates S by signs.

The matching-spine page caps, derived in Section 0 of TWO_RED.md, give

    -3-u_i-u_j+(W^2)_ij <= S_ij(S^2)_ij
                              <= -3-u_i-u_j-(W^2)_ij.

In particular, every matching pair satisfies **(W^2)_ij<=0**.
For a uniform pair, the sums of the two spines from a fixed endpoint are

    red:  sum_{k != i,j}(1+W_ik)(1+W_jk)+2(epsilon_i+epsilon_j),
    blue: sum_{k != i,j}(1-W_ik)(1-W_jk)+2(2-epsilon_i-epsilon_j).

Their caps are six and twelve. Their difference in either color is
(S^2)_ij. A saturated sum therefore forces (S^2)_ij=0. These are
literal common-neighbor identities for ordinary books; page vertices
need not be independent in the ambient coloring.

Let D be the graph of blue uniform pairs on the eleven orbits. If ij
is red uniform, put F_ij=N_D(i) union N_D(j). Neither endpoint belongs
to this union, since ij is not blue. Every one of the nine third orbits
outside F_ij contributes at least one red page to the summed spines.
Thus

    9-|F_ij|+2(epsilon_i+epsilon_j)<=6,

and **every red uniform pair has |N_D(i) union N_D(j)|>=3**. This is
only a necessary condition; extra red links can increase that page sum.

**No two blue leaves can share a neighbor.** Suppose two distinct
vertices i,j of D both have blue neighborhood {a}. Their pair is not
blue and cannot be red, because its F union has size one. Hence it is
matching. The summand at a in (W^2)_ij is +1; at every other third
orbit neither endpoint has a blue link, so both W entries are zero or
+1 and their product is nonnegative. Therefore (W^2)_ij>=1, a
contradiction. This restriction permits arbitrary red links and holds
at every blue density, not just the four-edge case below.

## 2. Complete coverage of four blue pairs

The independent review supplies at least four blue uniform pairs. Assume
there are exactly four. The earlier three-red lemma supplies at least
three red uniform pairs. Their number otherwise remains unrestricted.

Up to relabeling, a simple graph with exactly four edges has eleven
forms, with isolated vertices appended to reach eleven. Here P_m is a
path on m vertices, K1,m is a star with m leaves, a fork is the tree
with degree sequence (3,2,1,1,1), and a paw is a triangle with a pendant
edge. A complete list and the exclusion used are:

| Blue form | Exclusion |
| --- | --- |
| 4K2 | No red candidate |
| P3+2K2 | Two blue leaves with a common neighbor |
| 2P3 | Two blue leaves with a common neighbor |
| P4+K2 | Forced matching 02 has (W^2)_02=1 |
| K1,3+K2 | Two blue leaves with a common neighbor |
| K3+K2 | Red endpoints force a blue triangle-pair sum at least fourteen |
| P5 | Three mutually orthogonal six-sign rows |
| K1,4 | Two blue leaves with a common neighbor |
| Fork | Two blue leaves with a common neighbor |
| C4 | No red candidate |
| Paw | Forced matching 03 has (W^2)_03=1 |

To justify the list, disconnected edge-count partitions are 1+1+1+1,
2+1+1, 2+2 and 3+1. A connected two-edge component is P3; a connected
three-edge component is P4, K1,3 or K3. These give six disconnected
forms. A connected four-edge graph has four or five vertices. On four
it is C4 or a paw; on five it is one of the three trees P5, K1,4 or a
fork. This gives the other five forms, with no graph catalogue premise.

Five forms have two degree-one blue vertices with the same neighbor,
so Section 1 already excludes them. The remaining six are handled below.

## 3. Four elementary exclusions

For **4K2**, every nonblue pair has union of blue neighborhoods of size
at most two. It permits no red uniform pair, contradicting at least three.
For **C4**, a nonblue pair among cycle vertices is an opposite pair and
has union of size two. A cycle vertex and an isolated vertex also have
union of size two; two isolated vertices have union zero. Again no red
uniform pair is possible.

For **P4+K2**, normalize the blue pairs to 01,12,23,45. The only
nonblue pairs whose blue-neighborhood union has size at least three are
14,15,24,25. Thus orbit 0 has no red uniform link, and 02 is forced
matching. Its W^2 entry is exactly one from their common blue neighbor
1. Orbit 0 has no other uniform link, so every other summand is zero.
This contradicts the matching restriction.

For a **paw**, normalize blue pairs to 01,02,12,23. The only red
candidates are 2k for k=4,...,10. Orbits 0 and 3 have no red uniform
link, and their pair is matching because its blue-neighborhood union
has size two. Their common blue neighbor 2 gives (W^2)_03=1; the
only other uniform link at 0 is to 1, while 3 has no uniform link
to 1. This is again impossible.

## 4. A blue triangle and edge have incompatible inside colors

Normalize **K3+K2** to blue 01,02,12,34. Put A={0,1,2}, E={3,4}
and H={5,...,10}. The neighborhood-union condition permits red pairs
only between A and E. Indeed an A vertex has two blue neighbors, an E
vertex one, and their neighbor sets are disjoint; every other nonblue
pair has union size at most two. Thus all links involving H are matching.

For any red pair a-e, with a in A and e in E, the other two A orbits
give zero red summed pages because a is blue to them. The other E
orbit gives zero because e is blue to it. The six H orbits each give
one, regardless of all other chosen red pairs. Hence its red sum is

    6+2(epsilon_a+epsilon_e)<=6.

Every endpoint of a red pair therefore has a blue inside edge. There
are at least three red pairs; a single A vertex permits only two, so
at least two distinct A vertices a,b are red endpoints. At their blue
pair, the third A orbit gives four summed blue pages, the six H
orbits give six, and the E contributions are nonnegative. Their inside
sum is four. The total is at least **14>12**, a contradiction.
This covers every subset of the six red candidates, not a fixed red count.

## 5. A blue path leaves an impossible sign-row triangle

Normalize **P5** to blue 01,12,23,34. The only possible red pairs
are 03,13,14: these and only these nonblue pairs have a neighborhood
union of size at least three. At least three red pairs are required,
so all three are red. Every other cross block is matching. Put
H={5,...,10}, and r_i=S_i,H.

At red03 the six H orbits give six summed red pages, and the other
three displayed orbits give zero, since at least one of their two
links is blue. The same holds at red13 and red14. Their sums force
epsilon_0=epsilon_1=epsilon_3=epsilon_4=0 and saturate all three red
pairs. Orbit 2 and all six H inside colors remain arbitrary.

At blue01 the displayed orbit 2 gives two summed blue pages; orbits
3 and 4 give zero. The six H orbits give six, and its inside sum is
four. Thus this pair also saturates its twelve-page summed cap.
The three pairs **01,03,13** consequently have S^2 entry zero.
Every displayed-orbit contribution to these entries vanishes, because
at least one of its two S entries is uniform and therefore zero.
Their only contributions are from H. Thus

    r_0 dot r_1 = r_0 dot r_3 = r_1 dot r_3 = 0.

All three rows have six entries in {-1,+1}. Switch the H labels so
r_0 is all ones. Orthogonality makes r_1 and r_3 balanced, each with
three positive coordinates. Their Hamming distance is even, so their
dot product is 6 minus a multiple of four, hence **2 modulo 4**.
It cannot be zero. This contradiction excludes the last blue form,
at every matching signing and inside-color choice.

**Local path-core lemma, with arbitrary complement.** In any coloring of
K22 with a fixed-point-free color-preserving involution, suppose five
orbits labeled 0,...,4 have exactly blue uniform pairs 01,12,23,34 and
red uniform pairs 03,13,14; their other three cross blocks are matching.
Suppose every block between these five orbits and the other six is
matching. Then the coloring contains a red B4 or a blue B7, regardless
of all inside colors, matching signs, and all fifteen cross blocks among
the other six orbits. Those fifteen blocks may be red uniform, blue
uniform or matching, in any combination.

Indeed, after the displayed core is fixed, the proof in this section
uses only uniform spines within it and the five sign rows to H. None
of the page sums or S^2 entries in the saturated triangle uses a link
between two H orbits. Thus the same contradiction applies with no
restriction on those links. This local lemma requires neither the
three-red minimum nor the four-blue bound.

All eleven four-edge blue forms are excluded. The independent four-blue
lower bound now gives at least five blue pairs. Combining the prior
three-red result gives the stated eight-total bound and the unique
three-red/five-blue color count at exactly eight.

## 6. Exact validation and trust boundary

From the repository root with Python 3.11 standard library:

```sh
python3 book_ramsey_b4_b7_free_involution/check_four_blue.py --scratch /tmp/book-four-blue-check
```

The fast census lists all eleven blue forms, derives every permitted red
candidate and considers all **586** candidate subsets, including **408**
with at least three red pairs. Matching and uniform page relaxations,
with all 2^11 inside flags, leave just the P5 pattern with **128**
inside assignments. These necessary survivors are not valid graphs;
Section 5 excludes them analytically. There is no full matching-sign search.

The separate checker independently generates all four-edge subsets on
eight vertices and canonicalizes connected components, recovering exactly
the eleven forms without importing the author's form list. It derives
two-point page costs from literal neighbor sets, checks each red candidate
by its minimum possible red page sum, uses literal relaxed matching costs
and direct inside-flag branching, and compares every surviving quotient
and flag entry. Both implementations are author checks, not peer review.
Its row and lifted-graph controls are documented in README.md.
The lifted controls include matching, all-red, all-blue and mixed
uniform/matching links within H, to audit the local lemma's broader
complement quantifier; they do not enumerate all such links.

A separate initial diagnostic also covered all **1,353,625** normalized
three-red/four-blue patterns (five red forms times binomial(52,4)). It
left exactly seven labeled copies of the same obstruction, with **896**
inside assignments. This was discovery/validation; the stronger blue-first
proof and its 586-subset audit supersede that diagnostic as the portable
scope. Its adapted C++ source and output remain private, and are not a
computation premise or claim of unrestricted graph enumeration.

The mathematical dependencies are the earlier three-red lemma and the
independent four-blue lemma, plus the literal orbit page identities.
No unrestricted degree/core result, graph catalogue, solver, spectral
classification, numerical eigenvalue or incomplete computation is used.
The proof is ordinary, unformalized mathematics. Its case completeness
and sign-row bridge are written above, rather than assumed from software.
The located unrestricted Ramsey gap remains 22..23; the result leaves
three-red/five-blue and denser uniform patterns unresolved.
