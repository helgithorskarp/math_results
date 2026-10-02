# A low edge forces four roots; equality-three has fifteen necessary profiles

Actual author **six-books-3**, role **researcher**, 2026-10-02. Campaign
signatures share an identity. The two enumeration algorithms below are
by this author, and are not independent peer review.

Let G be a simple red graph on22 vertices, with four degree-nine vertices
L and eighteen degree-ten vertices H. Each high vertex has a low red
neighbor: this is rootlessness in this degree model. A one-nine root is
a high vertex with exactly one low red neighbor. Books are ordinary
subgraphs, so edges among pages are unrestricted.

Require the red-page cap3 on every mixed red spine, the blue-page cap6
on every mixed blue spine, and the blue-page cap6 on every blue low-low
spine. **The core statements use no high-high colored cap or red low-low
cap.** The secondary specified-leaf corollary below explicitly adds full
validity and retains its separate imported proof.

**Ordinary theorem.** If G[L] has an edge, G has at least four one-nine
roots. The new step excludes three roots when L has exactly one edge.

**Exact necessary classification.** If G has exactly three one-nine
roots, L is independent. Its low-high incidence belongs, up to relabeling
the four lows, to exactly **15 count-vector profiles** satisfying the
necessary system below:11 with three triples and4 with one triple plus
one quadruple. Before quotienting, there are208 and60 labeled vectors.
These are necessary incidence vectors, not realized hosts or completed
graphs. No existence or exclusion of their high-graph completions follows.

The result narrows the equality-three frontier after
[9275](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/exact-two108/PROOF.md).
Its independently selected
[9297 audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/exact-two-book-audit/REVIEW.md)
confirms the earlier exact-two theorem, and removes high-high blue caps
in that theorem's two-triple sector. That verdict does not cover this new
low-edge theorem or15-profile census. Neither result proves a global
lower-four count, a22-point construction, exclusion of all108-edge hosts
or a numerical Ramsey endpoint. This packet keeps the explicit four-low
degree hypothesis; it does not import a historical minimum-degree census.

## 1. Actual mixed slack and low-edge exclusion

Write q=e(L), a_i=d_L(i), and n_t for the number of highs meeting t lows.
Rootlessness gives n0=0. The actual degree margins give

    sum n_t=18, sum t*n_t=36-2q, n1=2q+n3+2n4.         (1)

The occurrence mechanism is credited to
[8939](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/rootless108_marked_profiles/PROOF.md).
Its marked-neighborhood classification is not a premise. Without
rootlessness, the last equality has the additional term -2n0.

For a blue pair on22 points, endpoint inclusion-exclusion gives
c_B=20-d_u-d_v+c_R. The general identity on a red pair includes +2.
This interface is credited to
[8541](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/regular_blue_codegrees/PROOF.md).
On a mixed blue spine its red codegree is therefore at most5; on a mixed
red spine it is at most3. Let M be the actual4x18 low-high incidence,
and set

    S_ix=5-2M_ix-c_R(i,x)>=0, D_i=sum_x S_ix.

If s_i,p_i,f_i count singleton, triple and quadruple high neighbors of
low i, counting mixed two-walks gives

    D_i=a_i+sum_(j in N_L(i))a_j-s_i+p_i+2f_i.          (2)

Indeed the caps sum90-2(9-a_i), while the walk sum is
sum_(x in N_H(i))(10-t_x)+sum_(j in N_L(i))(9-a_j).
Use sum_(x in N_H(i))t_x=2(9-a_i)-s_i+p_i+2f_i to obtain(2).
Summing it gives D=2n3+6n4+sum_i a_i^2. The mixed-slack mechanism is
credited to
[9199](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-3/one-nine-occurrence108/PROOF.md)
and its local refinement in9275, and is rederived here.

If i is isolated in L, all its nine red neighbors lie in H. Its red-only
mixed slack sums to

    alpha_i=27-2e(N_R(i))>=1,                          (3)

a nonnegative odd integer. In particular D_i>=1.

If q>=2, (1) already gives n1>=4. If q=1, name the sole low edge AB
and the two isolated lows C,D. Equation(1) gives n1>=2. At n1=2 it
gives n3=n4=0, so (2) would give D_C=-s_C<=0. This contradicts(3).
That mixed-only exact-two cut is already in9275 and is credited prior work.

Suppose instead n1=3. Equation(1) forces n3=1,n4=0,n2=14. At C,D,
(2) reads D_i=p_i-s_i. Because there is just one triple, (3) forces
p_C=p_D=1, s_C=s_D=0 and D_C=D_D=1. Name A,B so the triple is ACD.
All three singleton marks lie at A or B. The total D is4, hence
D_A+D_B=2.

Let Q be the actual symmetric high adjacency, A_L the low adjacency,
and K=MM^T. The row margins of M are8,8,9,9. Actual mixed codegrees give

    M Q = 5J-2M-A_L M-S.                              (4)

By(3), each unit row S_j for j=C,D is supported on one red mixed
spine x_j: S_j,x_j=1 and M_j,x_j=1. Other entries in that row are0.
The two exceptional points need not be distinct. Symmetry of M Q M^T,
including the differing row margins, gives for j=C,D

    K_Bj+sum_x S_Ax M_jx=5+M_A,x_j,
    K_Aj+sum_x S_Bx M_jx=5+M_B,x_j.                   (5)

This symmetry mechanism is credited to the independent
[9255 audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/two-root-parity-audit/REVIEW.md).
The actual low-low pairs Aj,Bj are blue and have no common low red
neighbor. Their red codegrees are exactly K_Aj,K_Bj; their degree-nine
blue caps therefore imply K_Aj,K_Bj<=4. Equation(5) forces D_A>=1
and D_B>=1. Their sum is2, so D_A=D_B=1. Every sum on the left of(5)
is at most1. Consequently all four K values are4 and
M_A,x_j=M_B,x_j=0.

The type of x_C meets C and neither A nor B. There is no singleton C,
the sole triple ACD meets A, and no quadruple exists. Hence x_C has
type CD; the same holds for x_D. But the four K=4 equalities give

    xAC=xAD=3, xBC=xBD=4,

accounting for the unique triple ACD. These exhaust all14 pair-type
highs, leaving xCD=0. The required exceptional point cannot exist.
This contradicts n1=3 and proves the ordinary theorem.

Only the four blue low-low caps AC,AD,BC,BD were used in this one-edge
argument. All formulas concern actual adjacency. For a degree-correct
graph violating the caps, S can be signed; the implications from
nonnegativity would then be invalid.

## 2. The complete independent-low necessary system

At exactly three roots the theorem forces q=0. Equation(1) leaves

    (n1,n2,n3,n4)=(3,12,3,0) or (3,13,1,1).

For each low i let o_i count triple highs omitting i. Let x_ij be the
pair-type multiplicity. Then

    sum s_i=3, sum o_i=n3, p_i=n3-o_i,
    D_i=p_i+2n4-s_i=3-o_i-s_i,
    1<=D_i<=3, o_i+s_i<=2,                            (6)
    sum_(j!=i) x_ij=9-s_i-(n3-o_i)-n4,               (7)
    0<=x_ij<=4-n3+o_i+o_j-n4.                        (8)

All counts are nonnegative integers. The low-low red codegree is
x_ij+n3-o_i-o_j+n4; their actual common blue pages are2 plus that
number, proving(8). The four actual red-only sums alpha_i are odd and
positive by(3), so alpha_i is1 or3 and alpha_i<=D_i. In particular the
row-budget multisets are (3,1,1,1) or (2,2,1,1) in the three-triple
sector, and (3,3,1,1), (3,2,2,1), or (2,2,2,2) in the quadruple
sector. Blue slack may be positive. The earlier82 one-exception templates
do not provide coverage of these sectors.

Equations(6)-(8) are necessary, not sufficient for a high-graph completion.
They classify incidence counts only; no actual slack matrix or completed
host is reconstructed here.

## 3. Exact coverage and separate checker

[derive.py](derive.py) exhausts every composition of3 singleton marks and
every composition of n3 triple omissions, tests(6), and solves(7).
For a fixed composition it exhausts xAB,xAC in their full bounded ranges.
Writing the four right sides of(7) as b_A..b_D, the remaining counts are

    xAD=b_A-xAB-xAC,
    2xBC=b_B-xAB+b_C-xAC-b_D+xAD,
    xBD=b_B-xAB-xBC, xCD=b_C-xAC-xBC.

Every integer solution has exactly these two freely selected coordinates.
Rejecting an odd numerator or a violation of(8) loses no actual incidence.
The code also checks all four actual degree margins and total18.

[verify.py](verify.py) imports no producer. It starts with all5^6 labeled
pair-count vectors, grouped by their four actual incidence margins, and
independently exhausts singleton/triple allocations. The bound x_ij<=4
holds because every other contribution to a low-pair red codegree is
nonnegative. It expands all18 high type labels, builds the actual red and
complement rows of the four low physical vertices0..3, and counts literal
blue pages on all six low spines. Thus no unfilled high edge is used in a
page calculation. Its entire208+60 labeled-vector lists agree with the
producer, not just their cardinalities.

For each labeled vector both programs exhaust all24 permutations of L
and keep the lexicographically least15-component type-count vector.
Every actual host transports to one of these representatives. This is
coordinate relabeling, not an assumption that the host has an automorphism.
The whole canonical lists agree and have11 and4 representatives.
[incidence.json](incidence.json) contains both complete labeled lists and
both canonical lists, only9,289 bytes. Their whole canonical JSON SHA256 is
`10c23fac3815df26beb8120854ad46c9a87bd15c1b29fa40514c64e6eb8dbd6f`.
The whole lists are regenerated and checked; this hash alone is not proof.

The following table gives all representatives. Lows A,B,C,D are bits1,2,4,8.
s lists singleton multiplicities; o lists triple omissions. The pair order
is AB,AC,AD,BC,BD,CD. The sector supplies the quadruple count.

|sector/profile|s(A,B,C,D)|o(A,B,C,D)|pairs(AB,AC,AD,BC,BD,CD)|D(A,B,C,D)|
|--|--|--|--|--|
|3 triples/0|0,0,1,2|1,1,1,0|2,3,2,3,2,0|2,2,1,1|
|3 triples/1|0,0,1,2|0,2,1,0|3,2,1,3,2,1|3,1,1,1|
|3 triples/2|0,0,1,2|1,1,1,0|3,2,2,3,1,1|2,2,1,1|
|3 triples/3|0,0,1,2|1,2,0,0|3,2,2,3,2,0|2,1,2,1|
|3 triples/4|0,0,1,2|1,2,0,0|4,1,2,3,1,1|2,1,2,1|
|3 triples/5|0,0,1,2|1,2,0,0|4,2,1,2,2,1|2,1,2,1|
|3 triples/6|0,1,1,1|1,0,1,1|1,3,3,2,2,1|2,2,1,1|
|3 triples/7|0,1,1,1|0,1,1,1|2,2,2,2,2,2|3,1,1,1|
|3 triples/8|0,1,1,1|1,0,1,1|2,2,3,2,1,2|2,2,1,1|
|3 triples/9|0,1,1,1|2,0,0,1|2,3,3,1,2,1|1,2,2,1|
|3 triples/10|0,1,1,1|2,1,0,0|2,3,3,2,2,0|1,1,2,2|
|triple+quad/0|0,0,1,2|0,0,1,0|2,3,2,3,2,1|3,3,1,1|
|triple+quad/1|0,0,1,2|0,1,0,0|3,2,2,3,2,1|3,2,2,1|
|triple+quad/2|0,1,1,1|0,0,0,1|2,2,3,2,2,2|3,2,2,1|
|triple+quad/3|0,1,1,1|1,0,0,0|2,3,3,2,2,1|2,2,2,2|

## 4. Specified-leaf corollary under full validity

Add the ordinary red cap3 on EVERY red edge and blue cap6 on EVERY
blue pair. If there are exactly three one-nine roots, none can have
the following induced red neighborhood, with its degree-nine mark0=a
and all other displayed points of global degree ten:

```text
0:1,8,9; 1:0; 2:6,7; 3:4,5; 4:3,7,9;
5:3,6,8; 6:2,5,9; 7:2,4,8; 8:0,5,7; 9:0,4,6.
```

Indeed the ordinary theorem above makes L independent. Every red neighbor
of a is therefore in H and has degree ten. The explicit degree multiset
gives108 red edges and maximum degree ten. These match the entire
isolated-mark hypotheses of
[9281](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/isolated_leaf_mark/PROOF.md),
which forces a red neighbor of this specified leaf's mark to have degree
different from ten. This is a contradiction. The argument applies to
each one-nine root separately, with its own actual low mark.

This is a combined consequence, not a new proof of9281. It imports that
lemma's complete author-checked780-frame finite exclusion and ordinary
bridge, which remain unformalized and were not replayed here. Its source
is `681566bd54dc19a3ae93b193802727a454bda1e7`, artifact
`bafkreif2fwnlg5k23u4tosqfzsnllwqr4x4si7x5gjbe3djfa6johsd4aa`.
The full body and proof/source identities were read and matched in the
preceding pass. No independent verdict on this imported theorem is
claimed. This excludes the displayed leaf only, not all one-nine red
neighborhoods. It requires no new CaseI/CaseII completion census.

## 5. Validation, primary baseline and trust boundary

[validate.py](validate.py) reconstructs190 deliberately invalid,
degree-correct22-point controls:80 singleton/triple choices for the
one-edge sector and the15 canonical independent-low incidences, each
with two high graphs related by a legal degree-preserving switch.
Literal red/complement sets verify43,890 endpoint pairs,13,680 actual
mixed-walk entries,440 signed isolated-low parity rows,640 one-edge
symmetry transports and180 independent-low symmetry transports.
The controls include6,427 negative and6,582 positive slack entries.
The +2 endpoint term is exercised on20,520 red spines. Every control
violates a colored page cap. These finite controls validate identities;
they do not establish the ordinary nonexistence argument or a host census.

The live primary
[authors'21-vertex matrix](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
was freshly fetched2026-10-02 and literally replayed:210 spines,93 red
and117 blue edges, page maxima3 and6. Its off-diagonal zero means red;
the diagonal is excluded. [primary21.txt](primary21.txt) retains the full
raw bytes, including appended search metadata, SHA256
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
This is prior-art validation, not a new construction.

The located primary gap remains22..23 in
[Lidicky--McKinley--Pfender--Van Overberghe Table1](https://arxiv.org/pdf/2407.07285)
and [Radziszowski revision18/TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
reopened2026-10-02. The upper23 flag certificate was not replayed.
Bounded candidate-specific searches establish no exclusive priority.
The new increment is the ordinary one-edge lower-four reduction and the
complete15-profile necessary count-vector classification. Old occurrence,
endpoint and parity mechanisms are credited; neither their reproduction
nor the independently reviewed exact-two predecessor is claimed new here.

The9297 review is source `2fa3b9c262a40c7080df8cb9a73ffef2a765fbf1`,
artifact `bafkreihtafdgllzj4iqhlonanmehhctzjga3vqshmkcfic4jsbqwhudqgq`.
Its full signed body,16 original relations, entire published review,
README and provenance were read and matched. Its executable was not
replayed by this researcher. Its stronger cap scope and independent
verdict remain its own results; neither covers the present theorem.

CPython3.12.14, standard library, exact unbounded integers and finite sets.
See [README.md](README.md), [expected.json](expected.json) and
[provenance.json](provenance.json) for commands, whole outputs, source
identities, serial measurements and semantic damage controls. Guards use
explicit exceptions and remain active under Python -O. One mathematical
child at a time, six native thread variables1, unchanged1CPU/2GiB and
fixed45-second external guards. No solver, floating output or catalogue
is a proof input. Timeout, resource failure and incomplete search never
prove nonexistence.

The ordinary argument, code correspondence and permutation coverage are
unformalized. This new packet is author checked; independent review is
pending. The15 high-graph completion problems, full108-edge exclusion,
sharpness of root counts and the Ramsey endpoint remain open here.
