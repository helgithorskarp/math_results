# Four degree-eight vertices span at least four red edges

Actual author **six-books-1**, role **researcher**, 2026-10-01. The new
blue-pair exclusion below is an ordinary counting proof. Its small exact
controls are validation, with no exhaustive host enumeration as a premise.
The edge-count corollary also uses the previously published, computer-assisted
[root-defect lower bound](degree98_root_four.md). That bound is independently
confirmed in [review8472](../book_ramsey_root_defect8_review4/REVIEW.md), actual
reviewer six-reviewer-4, source commit
`53f585a70892598f863e1cea799afb5cfe50f1e5`. The review also gives a simpler
199-form certificate without active-defect placements; its numerical bound
is unchanged. Independent peer review of the new blue-pair lemma is pending.

**Lemma.** Let a simple graph on 22 vertices avoid an ordinary red \(B_4\)
and an ordinary blue \(B_7\), and have red-degree counts
\((n_8,n_9,n_{10})=(4,16,2)\). Let \(A,B,C\) be these degree classes and put

\[
 F_{ij}=\begin{cases}3-c_R(i,j)&ij\text{ red},\\6-c_B(i,j)&ij\text{ blue},\end{cases}
 \quad F_{ii}=0,\quad f_i=\sum_j F_{ij},\quad q_0=\sum_{i\in A\cup C}f_i.
\]

If the pair in C is blue, then \(q_0\ne8\).

**Corollary, with the cited lower bound \(q_0\ge8\).** If the C-pair is
blue, \(q_0\ge12\). In every graph with the stated histogram,
\(\boxed{e_R(A)\ge4}\), regardless of the C-pair's color. In particular,
when \(q_0=8\), the C-pair is red and A induces either a four-cycle or a
triangle with a pendant vertex. This is a necessary structural reduction;
it does not exclude the whole histogram or determine \(R(B_4,B_7)\).

## Incident, Gram and spine identities

Books are ordinary subgraphs, so extra edges among their pages are allowed.
Their exclusion is exactly \(c_R\le3\) on every red pair and \(c_B\le6\)
on every blue pair. Hence F is nonnegative, symmetric and integral.
For any vertex let \(h_i=|N_R(i)\cap A|\), \(k_i=|N_R(i)\cap C|\).
The histogram has 98 red edges. Triangle counting gives

\[
 f_i=\begin{cases}2(h_i-k_i-1)&i\in A,\\
                  1+2(h_i-k_i)&i\in B,\\
                  2(h_i-k_i+1)&i\in C.
       \end{cases} \tag{1}
\]

Here is a direct derivation, also credited to the earlier
[parity/defect source](parity_square.md). At degree d,
\(f_i=3d+6(21-d)-2(t_R(i)+t_B(i))\), and
\(t_R(i)+t_B(i)=\binom{21-d}{2}-98+\sum_{j\in N_R(i)}d_j\).
Thus \(f_i=196-294+38d-d^2-2\sum_{j\in N_R(i)}d_j\).
Substitution of \(\sum_{j\in N_R(i)}d_j=9d-h_i+k_i\) gives (1).
Since \(\sum_i(h_i-k_i)=4\cdot8-2\cdot10=12\), summing gives

\[
 q_0=-4+4(e_R(A)-e_R(C)),\qquad
 q_0+\sum_{i\in B}(f_i-1)=20. \tag{2}
\]

Label \(A=\{0,1,2,3\}\), \(C=\{4,5\}\). Let \(R_0\) be red adjacency
on these six roots, \(W=(F_{ij})_{i,j<6}\), and M the binary 16-by-6
incidence matrix from B to the roots. Set \(G=M^TM\),
\(s_i=d_i-d_{R_0}(i)\), and \(t=(1,1,1,1,-1,-1)^T\). Pair counting gives

\[
 G_{ii}=s_i,\qquad
 G_{ij}=d_i+d_j-14+(17-d_i-d_j)(R_0)_{ij}
           -(R_0^2)_{ij}-W_{ij}\quad(i\ne j). \tag{3}
\]

For a red root pair its total red codegree is \(3-W_{ij}\). For a blue
root pair use \(c_B=20-d_i-d_j+c_R=6-W_{ij}\). Subtracting common root
neighbors proves (3), including its sign in the blue case.

Assume \(q_0=8\) for the rest of the lemma proof. At a B row x put
\(\delta(x)=h-k=t^Tx\). Equation (1) and integrality imply
\(0\le\delta\le4\), and (2) gives

\[
 \sum_{v\in B}\delta_v=6,\qquad
 \sum_{v\in B}\delta_v^2=t^TGt,\qquad
 \tau=Gt=M^T\delta. \tag{4}
\]

Every \(\tau_i\) is a subset sum of the positive \(\delta_v\)'s.
The possible square sums at total six with parts at most four are
\(6,8,10,12,14,18,20\). The maximum 20 occurs only for parts 4,2.
The value 18 has parts 4,1,1 or 3,3; 14 has parts 3,2,1.
These follow by the integer partitions of six with largest part at most
four, or by transferring a unit to a larger part below four. Also

\[
 n_{\text{neither C}}=16-G_{44}-G_{55}+G_{45}\ge n_{\delta=4}, \tag{5}
\]

because a surplus-four word meets all four A roots and neither C root.

Let P be red adjacency on B, and let \(g_j=(F_{vj})_{v\in B}\) be the
outside defect column at root j. Put \(\ell=(3,3,3,3,5,5)^T\),
\(E=\operatorname{diag}(0,0,0,0,1,1)\), and \(W_{\rm out}=(g_0,\ldots,g_5)\).
The red codegree at any B-root pair is \(3-F_{vj}\) for an A root, and
\(5-2M_{vj}-F_{vj}\) for a C root, in either color. Splitting root and
B common neighbors proves

\[
 PM=\mathbf1\ell^T-2ME-MR_0-W_{\rm out}. \tag{6}
\]

Consequently \(Z-M^TW_{\rm out}=M^TPM\) is symmetric, where
\(Z=s\ell^T-G(R_0+2E)\). If \(g_i=0\), then

\[
 (M^Tg_j)_i=Z_{ij}-Z_{ji}. \tag{7}
\]

More generally,
\((M^Tg_j)_i-(M^Tg_i)_j=Z_{ij}-Z_{ji}\).
The sum of \(g_j\) is \(f_j-\sum_i W_{ij}\).
At every even-degree root the red incident defect is even, since
\(\sum_{i\in N_R(j)}F_{ij}=3d_j-2t_R(j)\). These are ordinary identities;
no assumed spectral saturation is used.

## Complete root geometry and attached paths

Suppose the C-pair is blue. Equation (2) makes \(e_R(A)=3\), and (1)
makes the minimum A degree within A at least one. Thus A is a star or
a path. Every A leaf has no red C-neighbor.

The star is impossible throughout this histogram. Its three leaves each
have seven red B-neighbors. Each leaf pair is blue and has red codegree
at most two: \(20-8-8+c_R=c_B\le6\). Their common center already uses
one place, so their B-neighbor sets intersect pairwise in at most one
point. Inclusion-exclusion makes their union at least
\(3\cdot7-3\cdot1=18>|B|=16\).

Label the path by its red edges 03,12,23. Each of its interiors may have
at most one red C-neighbor. Up to path reflection and swapping C, the
A--C red edges are exactly none; 35; 25,35; or 25,34. Relabeling roots
does not assume any automorphism of the whole graph.

| A--C red edges | Root defects \((f_0,\ldots,f_5)\) | Gram diagonal |
|---|---|---|
| none | 0,0,2,2,2,2 | 7,7,6,6,10,10 |
| 35 | 0,0,2,0,2,4 | 7,7,6,5,10,9 |
| 25,35 | 0,0,0,0,2,6 | 7,7,5,5,10,8 |
| 25,34 | 0,0,0,0,4,4 | 7,7,5,5,9,9 |

A root with \(f_i=0\) has its entire F-row zero. In the same-C case
25,35, the only possible nonzero root-pair weight is \(w=W_{45}\le2\).
Equation (3) gives \(t^TGt=26-2w\ge22>20\), impossible.

In the different-C case 25,34, only \(w=W_{45}\le4\) is possible, and
\(t^TGt=28-2w\). Only \(w=4\) reaches the upper bound 20; then there
is a surplus-four row. But (5) is \(4-w=0\), impossible.

For the one-attachment case 35, put
\(x=W_{24},y=W_{25},z=W_{45}\). All these pairs are blue. Root row sums
give \(x+y\le2,x+z\le2,y+z\le4\), while (3) gives
\(t^TGt=24+2(x+y)-2z\le20\). Thus \(z\ge x+y+2\), and the capacities
force \(x=y=0,z=2\). The positive surpluses are then 4,2, but
\(\tau_1=5\) is not one of their subset sums. This excludes all three
attached path shapes.

## No attachment: nine states by integer counting

Now \(R_0\) has only edges 03,12,23. The active root defects are
\(f_2=f_3=f_4=f_5=2\). Put \(a=W_{23},b=W_{45}\) and
\(X=W_{24}+W_{25}+W_{34}+W_{35}\). Every active row of W has sum at most
two. Formula (3) gives the Gram diagonal in the table and

\[
 (G_{01},G_{02},G_{03},G_{12},G_{13},G_{23})
       =(2,1,3,3,1,3-a),\quad
 G_{ic}=4-W_{ic},\quad G_{45}=6-b, \tag{8}
\]

where \(i\in A,c\in C\). Also \(\tau_0=\tau_1=5\) and
\(t^TGt=20-2D\), with \(D=a+b-X\le4\).
The square-sum list in (4) and upper bound 20 force
\(D\in\{0,1,3,4\}\); D=0 is impossible because 4,2 cannot supply subset
sum five. If a=2 or b=2, that pair spends both of its active row capacities,
so all cross weights vanish. If a,b are at most one, their sum is at most
two. These observations prove the following complete list, without an
enumeration premise:

| D | a,b | Cross weights |
|---|---|---|
| 4 | 2,2 | all zero |
| 3 | 1,2 or 2,1 | all zero |
| 1 | 0,1 or 1,0 | all zero |
| 1 | 1,1 | exactly one of the four cross weights is one |

There are nine labeled states. The two endpoint outside columns vanish,
so (7), calculated from (8), reads for \(c=4,5\)

\[
 (M^Tg_c)_0=1-W_{3c},\qquad (M^Tg_c)_1=1-W_{2c}. \tag{9}
\]

When b=2, both C outside columns vanish, but the two right sides in (9)
are one. This excludes (a,b)=(1,2),(2,2).
In each of the four a=b=1/cross-one states, the C root used by the cross
weight has its full defect spent inside the roots. Its outside column
vanishes, whereas (9) requires endpoint moments 0,1 or 1,0. Thus six
states are excluded and three remain.

**State (a,b)=(2,1).** The square sum is 14, so the positive surpluses
are 3,2,1. The weighted moments are
\(\tau=(5,5,3,3,1,1)\). Each C moment one forces the unique surplus-one
row to contain that C root. It therefore contains both C roots and must
contain three A roots. But each endpoint moment five must use the
surplus-three and surplus-two rows, and cannot use the surplus-one row.
That row avoids both A endpoints, leaving only two available A roots.
This is a contradiction. No outside-column placement is needed here.

For the other two states the square sum is 18. Endpoint moment five
excludes the 3,3 partition; the positive surpluses are 4,1,1. The
surplus-four row is necessarily 111100, written in root order 0 through 5.

We will use a simple empty-row identity. For any binary row with h A
bits and k C bits let \(\phi=1+3\binom h2-hk\). A zero-surplus row has
h=k in \(\{0,1,2\}\), so \(\phi\) is one precisely for the empty row,
and zero for every other zero-surplus row. Therefore

\[
 n_{\rm empty}=16+3T_{AA}-T_{AC}-\sum_{\delta_v>0}\phi(v),\quad
 T_{AA}=\sum_{i<j\in A}G_{ij},\quad
 T_{AC}=\sum_{i\in A,c\in C}G_{ic}. \tag{10}
\]

This follows simply by summing \(\phi\) over all rows; it does not
require a binary incidence census.

**State (a,b)=(1,0).** Here \(\tau=(5,5,4,4,0,0)\). All positive rows
avoid C. The surplus-one rows are exactly the singleton A0 and singleton
A1, while the surplus-four row contains all A. From (8),
\(T_{AA}=12,T_{AC}=32\). Their positive \(\phi\)'s are 19,1,1, and (10)
gives \(n_{\rm empty}=16+36-32-21=-1\), impossible.

## The last state (a,b)=(0,1)

Now \(\tau=(5,5,5,5,1,1)\). The two surplus-one rows partition A
membership and also partition C membership. Entries \(G_{02}=G_{13}=1\)
are already used by 111100, so neither surplus-one row may contain pair
02 or 13. Every three-element subset of A contains one of those pairs;
each surplus-one row therefore has at most two A bits. Their total A
membership is four and their total C membership two, so each has exactly
two A bits and one C bit. Formula (10) gives

\[
 T_{AA}=13,\quad T_{AC}=32,\quad
 n_{\rm empty}=16+39-32-(19+2+2)=0. \tag{11}
\]

Consequently every B row has at least one A bit: h=0 together with
\(\delta=h-k\ge0\) would force the absent empty row.

Each outside C column has sum one, because \(f_c=2\) and \(W_{45}=1\).
Thus it is a unit column at some B vertex. By (9) its support contains
A0,A1. There are no red root neighbors of C. The even red incident
defect identity following (7) makes its unit support avoid its own C
root. The C--C symmetry equation is

\[
 (M^Tg_5)_4=(M^Tg_4)_5, \tag{12}
\]

since \(Z_{45}=Z_{54}\).

A zero-surplus row containing both A endpoints would also contain both C
roots, violating this parity restriction. Therefore the support of each
C unit column is either the surplus-four row x=111100 or a surplus-one
row containing A0,A1 and the other C root. A mixed choice makes the two
bits in (12) different. Two surplus-one choices require distinct A0,A1
rows, but their A memberships partition A. Both columns must consequently
be supported on x.

The red degree of x within B is \(9-4=5\). Its C-root equations (6)
require exactly four red B-neighbors meeting each C root, because each
of its two C defects equals one. Among its five B-neighbors at least
three meet both C roots. Those have at least two A bits by
\(h\ge k\). Every other neighbor has at least one A bit by (11).
Thus their total A incidence is at least
\(3\cdot2+2\cdot1=8\). But its four A-root equations (6) give the
neighbor counts

\[
 (2,2,1-(g_2)_x,1-(g_3)_x),
\]

whose sum is at most six. This contradiction excludes the ninth state,
and completes the ordinary blue-C lemma.

Finally, the cited root-defect theorem gives \(q_0\ge8\). Equation (2)
makes \(q_0\) a multiple of four. If C is blue the new lemma raises its
lower bound to 12 and gives \(e_R(A)\ge4\). If C is red, (2) and
\(q_0\ge8\) also give \(e_R(A)\ge4\). At \(q_0=8\), C is red and A
has exactly four edges; the two possible four-vertex graphs are a
four-cycle and a triangle with a pendant vertex. This proves the stated
corollary with precisely the imported lower-bound premise.

## Reproduction and evidence boundary

Use CPython 3.11 standard-library exact integers and fractions, one thread:

```sh
python3 -O degree98_root_eight_blue_check.py --records /tmp/book-root-eight-blue-records.json
python3 -O degree98_root_eight_blue_independent.py --records /tmp/book-root-eight-blue-records.json --report /tmp/book-root-eight-blue-audit.json
```

The [primary control](degree98_root_eight_blue_check.py),
[separate control](degree98_root_eight_blue_independent.py), and
[compact expected output](degree98_root_eight_blue_expected.json) are
standalone source. The expected file compares outputs; it supplies no
missing mathematical object. Generated records remain outside the source
directory and are regenerated completely. Their canonical JSON SHA-256 is
`2b6793d306d23a87d24508afb9c5618d0d5772752e8dd0ea91e5939a7014b1f7`.

The controls reproduce the 124 labeled root geometries and the 78 complete
root-pair capacity states (56,14,3,5). They agree on all nine necessary
moment states. They separately check 7,098 coefficient entries, the five
positive patterns in the final three states, and all 256 multiplicity
entries of the four final incidences. The primary code uses matrix
coefficients, product domains and a zero-row decoder. The separate code
uses literal red/blue root quotas, recursive remaining capacities and
integer partitions, and generic rational elimination on all 22 incidence
feature equations. Its grouped literal red/blue stars cover 12,012 labeled
five-neighbor subsets: 1,000 satisfy the C equations, all have A-incidence
at least eight, and none satisfies the A equations. These are checks of
the written counting argument, not indispensable finite classification
premises. Explicit checks remain active under `-O`.

Cold optimized control runs completed in 0.802/0.602 seconds wall time,
0.614/0.466 CPU seconds, and peak child RSS 25,276/25,092 KiB, primary
and separate respectively. The jobs ran sequentially with one numerical
thread and did not reach an operational guard.

There are also 32 signed controls with the exact degree histogram and
15,488 F entries checked by literal intersections. They verify the incident,
Gram, spine, symmetric-column and red parity identities even when defects
are negative. The deterministic control generator is reproduced from
[the earlier source](degree98_root_four_check.py). These graphs are
identity controls, not Ramsey constructions.

The [known 21-vertex fixture](baseline21.rows) was freshly matched in all
441 entries against the off-diagonal complement of the authors'
[primary construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt):
93 red edges and red/blue page maxima 3/6. This reproduces prior work.
The [primary paper, Table 1](https://arxiv.org/html/2407.07285v2) and
[*Small Ramsey Numbers*, Table IXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
reopened live on 2026-10-01, retain the located interval
\(22\le R(B_4,B_7)\le23\). The upper-bound certificate was not rerun.

The new lemma's proof consists of the written integer counting, root
classification, Gram and spine identities, parity and neighbor inequalities
above. The source checks strengthen validation but are not its logical
premises. The corollary additionally inherits the stated computational
trust boundary of the cited root-defect lower bound. No proof assistant,
independent peer review of the new work, historical priority classification,
or resolution of the Ramsey endpoint is asserted.
