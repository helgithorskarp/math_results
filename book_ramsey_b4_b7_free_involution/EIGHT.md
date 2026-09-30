# Free involutions require nine uniform orbit pairs

Author: **six-books-2**, role **researcher**, 2026-09-30.

**Theorem (computer-assisted).** In every ordinary red-B4/blue-B7-free
coloring of K22, each fixed-point-free color-preserving involution has
at least **nine** uniform unordered pairs of its eleven two-vertex
orbits. Inside colors and matching signs are arbitrary. A uniform pair
has all four cross edges the same color.

The earlier analytic bounds are at least three red and five blue uniform
pairs, from [TWO_RED.md](TWO_RED.md) and [FOUR_BLUE.md](FOUR_BLUE.md).
Consequently exactly nine, if possible, must be **three red/six blue or
four red/five blue**. This theorem excludes exactly eight, whose only
possible color count was three red/five blue. It asserts neither
attainment nor an involution in an arbitrary 22-vertex witness. The
unrestricted located Ramsey interval remains 22..23.

The new global theorem has a **finite computation premise**: an exact,
complete unsigned quotient reduction in Section 3. Two author
implementations with different graph generation and page representations
agree at every survivor and inside-flag entry. Written local arguments
then exclude the survivors without enumerating matching signs.
The stronger local blue-cycle lemma in Section 2 is entirely analytic;
its controls are validation only. Neither new statement has an independent
peer-review verdict or a proof-assistant formalization.

## 1. Definitions and exact page constraints

Label the two vertices of orbit i by i0,i1. For i!=j there are four
involution-invariant cross blocks: red uniform, blue uniform, parallel
red matching, or crossed red matching. Write R, B, M for the first two
and either matching. Let symmetric zero-diagonal W have entries +1 on
R, -1 on B, and 0 on M; S has entries +1/-1 on the parallel/crossed
red matching and 0 on uniform blocks. Let u=W1, and epsilon_i be 1
for a red inside edge and 0 for blue.

For a matching pair ij, its red and blue spines have respectively

    (9+u_i+u_j+(W^2)_ij+S_ij(S^2)_ij)/2,
    (9-u_i-u_j+(W^2)_ij-S_ij(S^2)_ij)/2

common neighbors in their own color. Neither of the two remaining
vertices in orbits i,j contributes. The caps three and six imply

    -3-u_i-u_j+(W^2)_ij <= S_ij(S^2)_ij
                              <= -3-u_i-u_j-(W^2)_ij.          (1)

Thus (W^2)_ij<=0 for matching ij. If that entry is zero, the two
bounds coincide.

For a uniform pair, sum the two spines from endpoint i0 to j0,j1.
The summed page counts are

    R: sum_{k != i,j}(1+W_ik)(1+W_jk)+2(epsilon_i+epsilon_j),
    B: sum_{k != i,j}(1-W_ik)(1-W_jk)+2(2-epsilon_i-epsilon_j). (2)

Their caps are six and twelve. In both colors their difference is
(S^2)_ij. A saturated sum therefore forces that entry to zero.
These identities count ordinary book pages, which need not be independent.
Their derivations also appear in the preceding analytic proofs.

If D is the blue uniform quotient, every red pair ij requires

    |N_D(i) union N_D(j)| >= 3.                              (3)

Indeed, neither endpoint belongs to this union. Each of the nine third
orbits outside it contributes at least one to the red sum in (2),
so 9-|N_D(i) union N_D(j)|+2(epsilon_i+epsilon_j)<=6.

For later use, the graph of orthogonality on six-entry sign rows is
bipartite. If x dot y=0, their Hamming distance is three, so
the product of x's entries is the negative of the product of y's
entries. In particular three such rows cannot be pairwise orthogonal,
and five cannot be successively orthogonal around an odd cycle.

## 2. An analytic local blue-five-cycle obstruction

**Local lemma.** Suppose five orbits 0,...,4 have exactly the blue
uniform pairs

    01,12,23,34,04,

and their five other pairs 02,24,14,13,03 are each R or M, in any
combination. Suppose every block from these five orbits to the other
six H={5,...,10} is matching. Then a red B4 or blue B7 occurs,
regardless of all inside colors, matching signs, and all fifteen cross
blocks among H. Those H blocks may be R, B or M in any combination.
No prior global uniform-pair minimum is a premise of this local lemma.

Assume the book caps hold. Every red chord has zero contribution in (2)
from the other three core orbits, since at least one incident link is
blue. The six H orbits each contribute one. Thus every red chord is
saturated and both its endpoints have epsilon=0. Put r_i=S_i,H;
each r_i is a six-entry sign row.

The chord graph is itself a five-cycle. Up to a dihedral relabeling
preserving the blue cycle, its red subsets have the following eight
types: empty; one edge; two adjacent or two disjoint edges; three
edges forming P4 or P3+K2; four edges forming P5; or all five edges.
For two edges, adjacency is the only distinction; three-edge types
are obtained by removing two edges from a five-cycle. Four and five
edges have one type each. This proves coverage without a computation.

**Zero or one red chord.** Normalize the possible red chord to 02.
Pair 13 is matching and (W^2)_13=1, from the common blue neighbor 2.
The other products are zero. This contradicts (1).

**Two adjacent red chords.** Normalize them to 02,24. Pair 13 is
still matching with (W^2)_13=1, the same contradiction.

**Two disjoint red chords.** Normalize them to 02,14. The red sums
force epsilon_0=epsilon_1=epsilon_2=epsilon_4=0. At blue34 the
outside sum in (2) is ten: six from H and two each from core orbits
0 and 2. Its full sum is 14-2epsilon_3<=12, hence epsilon_3=1,
and the sum saturates. Blue12 has outside sum eight and inside sum
four; blue23 has outside sum ten and inside sum two. Both saturate.
Therefore (S^2)_12=(S^2)_23=0. Pair 13 is matching, with
u_1=-1,u_3=-2 and (W^2)_13=0: the common-blue contribution at 2
cancels the red/blue contribution at 4. Equation (1) gives
(S^2)_13=0 as well. All core contributions to these three S^2
entries are zero, so r_1,r_2,r_3 are pairwise orthogonal, impossible.

This disjoint-chord case is, up to relabeling, the earlier X core
with arbitrary H blocks, proved independently by
[six-reviewer-4](../book_ramsey_free_involution_review4/REVIEW.md).
It is rederived here for a complete proof and is credited as known
within this campaign; no new priority is claimed for that case.

**Three red chords forming P3+K2.** Normalize them to 02,24,13.
All five core inside colors are blue. At blue04 the six H orbits
give six, core orbits 1 and 3 give two each, and orbit 2 gives zero.
The inside term is four, yielding 14>12, impossible.

**Three red chords forming P4.** Normalize them to 02,24,14.
The red chords force epsilon_0=epsilon_1=epsilon_2=epsilon_4=0.
Red02 and red24 saturate. At blue04 the outside sum is eight,
six from H and two from orbit 3, with inside sum four. Thus blue04
also saturates. All S entries linking core orbit 2 or 4 to another
core orbit are zero. Hence the three zero entries

    (S^2)_02=(S^2)_24=(S^2)_04=0

have no core contributions, and r_0,r_2,r_4 are pairwise orthogonal,
again impossible.

**Four red chords.** Normalize them to 02,24,14,13, leaving 03
matching. Exactly the same saturated triangle 02,24,04 and zero
core contributions apply. The added red13 does not change any
outside sum at those three pairs. The same sign-row contradiction follows.

**Five red chords.** Every red chord saturates, and every S entry
within the core is zero. Thus the five r_i are successively orthogonal
on the red chord cycle 0-2-4-1-3-0. Orthogonality changes the product
of the six entries, so an odd cycle cannot close.

All eight cases contradict the caps. Every page or S^2 entry used
has both endpoints in the core; it uses no H-to-H block. This proves
the arbitrary-complement quantifier of the local lemma.

## 3. Complete finite reduction at exactly eight uniform pairs

The preceding analytic minima imply that exactly eight means three R
and five B. We cover every unsigned quotient of this color count,
then all 2^11 inside assignments. All other orbit pairs are M.

**Five-edge blue graph coverage.** The main generator removes a blue
edge conceptually, leaving one of the eleven four-edge forms proved
complete in FOUR_BLUE.md. It adds each of the 55-4=51 nonedges of
each representative, including isolated vertices. Every five-edge
graph is therefore isomorphic to one of the 561 generated graphs.
Exact component canonicalization leaves 26 distinct forms.

The separate checker imports no campaign program and generates those
26 forms differently. Every connected component with at most five edges
has at most six vertices. It enumerates every e-edge subset on n
vertices for 2<=n<=6 and n-1<=e<=min(5,binomial(n,2)), retaining
exactly the connected graphs. The traversed labeled domains are:

| n | e | Edge sets |
| --- | --- | --- |
| 2 | 1 | 1 |
| 3 | 2 | 3 |
| 3 | 3 | 1 |
| 4 | 3 | 20 |
| 4 | 4 | 15 |
| 4 | 5 | 6 |
| 5 | 4 | 210 |
| 5 | 5 | 252 |
| 6 | 5 | 3003 |

These are 3511 labeled edge sets. Canonicalization orders vertices by
degree and minimizes the adjacency integer over all orders within each
equal-degree class. Isomorphisms preserve these classes, so two connected
graphs share the code exactly when isomorphic. The connected catalogs
have 1,1,3,5,12 types at edge counts 1,2,3,4,5. Enumerating every
multiset of these components with total five edges and appending isolates
to reach eleven covers every five-edge graph, independently of the
main augmentation. A five-edge graph has at most ten nonisolated vertices.

**Red coverage.** For each form every nonblue pair satisfying (3) is
a red candidate. Enumerating every three-element subset gives **2696**
quotients. All remaining pairs are matching. The separate checker derives
these same candidates from the literal minimum red summed pages, rather
than a neighborhood-union computation. Candidate positions agree after
canonical relabeling, not merely candidate counts.

**Necessary matching relaxation.** Fix a matching spine pair ij. A
third orbit k has incident block types as in the following table; each
entry lists its possible ordered contributions (red pages, blue pages)
to the red and blue matching spines. Both matching orientations are
allowed at each third orbit.

| Block types to k | Possible contributions |
| --- | --- |
| R,R | (2,0) |
| R,M or M,R | (1,0) |
| B,B | (0,2) |
| B,M or M,B | (0,1) |
| R,B or B,R | (0,0) |
| M,M | (1,0) or (0,1) |

If fixed sums are f_R,f_B and t third orbits have the last type,
some integer a in [0,t] must satisfy f_R+a<=3 and f_B+t-a<=6.
Testing this for every matching pair is a necessary relaxation: actual
globally consistent signs realize one of the allowed choices. It cannot
remove a valid coloring. It leaves **170** of the 2696 quotients.

**Inside and uniform budgets.** For a uniform pair its third-orbit sum
is a*b in red or (2-a)*(2-b) in blue, where a,b are the incident
red degrees 2,1,0 for R,M,B. Add the inside term in (2), and apply
caps six/twelve. An inside red edge has twice the red-uniform quotient
degree as its page count; an inside blue edge has twice the blue-uniform
degree. Check their caps three/six as well. The main carries one bit
for each of all 2048 assignments in a Python integer. The separate
checker branches over all assignments directly and derives third-orbit
costs from literal two-point neighbor sets.

The complete reduction leaves **six quotient patterns and 736 inside
assignments**. Every per-form diagnostic, red-candidate position, survivor
and inside-flag entry agrees. The separate checker additionally searches
all relabelings of the nonisolated blue vertices to verify that every
survivor and its entire inside-flag set belongs to exactly these shapes:

| Shape | R pairs | B pairs | Inside restrictions | Patterns / flags |
| --- | --- | --- | --- | --- |
| Y | 03,13,14 | 01,12,23,34,56 | epsilon_0=epsilon_1=epsilon_3=epsilon_4=0; epsilon_5+epsilon_6>=1; all others arbitrary | 1 / 96 |
| Z | 02,24,14 | 01,12,23,34,04 | epsilon_0=epsilon_1=epsilon_2=epsilon_4=0; all others arbitrary | 5 / 640 |

These counts use one blue representative per isomorphism type, without
quotienting its red choices by all blue automorphisms. The five Z patterns
are isomorphic labeled red choices. Necessary survivors are not graph
witnesses; matching signs have not been enumerated.

For Y, the core 0,...,4 is exactly the local path core of Section 5
of FOUR_BLUE.md. Every core-to-H block is matching; the additional
blue56 lies wholly within H, whose blocks the local lemma permits
arbitrarily. That lemma excludes every sign and inside choice for Y.
For Z, the core is the three-red-P4 case of Section 2, with every
core-to-H block matching, and that local lemma excludes it as well.
Thus all six necessary patterns are impossible. This proves the
computer-assisted nine-uniform-pair theorem.

## 4. Reproduction and trust boundary

Python 3.11 standard library only, tested on Linux with Python 3.11.2.
From the repository root:

```sh
python3 book_ramsey_b4_b7_free_involution/check_eight.py --scratch /tmp/book-eight-check
```

The runner executes one child at a time with thread counts one, a
120-second child timeout, and guards active under Python `-O`. Generated
records and logs remain in scratch. It compares all main diagnostics
with [eight_expected.json](eight_expected.json), then checks every record
with [eight_independent.py](eight_independent.py). A changed inside flag
and a removed survivor must each be rejected for an entry mismatch.

[eight_controls.py](eight_controls.py) checks all 4096 ordered pairs
of six-sign rows, including all 1280 orthogonal pairs and their opposite
entry products, with an order-four positive control. It covers all 32
chord configurations and 32 core inside assignments at four deterministic
matching-sign seeds, giving 4096 literal 22-vertex lifts. The H blocks
are all matching, all red, all blue, or a seeded mixture; outside inside
colors also vary. All 184320 spines among the ten core vertices are
counted against all 22 vertices, and every sample has an actual forbidden
core spine. The same controls compare 10240 matching-pair formulas,
30720 uniform-pair sums and differences, and 20480 inside-spine formulas
against literal neighbor intersections.

These lifted controls sample signs and outside blocks; they do not
exhaust either domain and are not premises of the analytic local lemma.
In contrast, the complete unsigned/inside reduction is a premise of the
global theorem. Its completeness follows from the finite-domain coverage
above and successful exact execution of the published code, with the
Python interpreter, source inspection and independent algorithmic replay
as the computational trust base. No external graph catalog, solver,
floating-point calculation, degree/core theorem or classification result
is a premise. No timeout, UNKNOWN or incomplete search is used to infer
nonexistence. Both implementations belong to the same author; their
agreement does not constitute independent peer review.

The disjoint-two-red local case is credited to six-reviewer-4 above.
The predecessor minima and path lemma are cited precisely; earlier
review verdicts do not extend to this new theorem. The eleven-by-two
representation is the known polycirculant/block-circulant framework,
not a claimed new representation. Primary context is
[Lidicky--McKinley--Pfender--Van Overberghe, Table 1 and Section 3.3](https://arxiv.org/html/2407.07285v2),
[Radziszowski, DS1.18](https://www.cs.rit.edu/~spr/ElJC/sur.pdf), and
[Wesley, Section 3](https://arxiv.org/html/2410.03625v2), rechecked
2026-09-30. No unrestricted Ramsey endpoint is claimed.
