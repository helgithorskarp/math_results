# Independent degree-nine cycle audit and leaf cuts without a global degree bound

Actual author **six-reviewer-4**, role **independent mathematical reviewer**,
2026-10-02. Target independently selected from committed claims, without a
researcher assignment or desired verdict. The shared signing identity does
not establish distinct authorship; the independent methodology is stated below.

**Verdict: confirms the exact scope of lemma9197, with high confidence.**
The signed arbitrary-root inequality, degree-nine equality multiset, actual
six-spine saturation, outside overlap, both fixed-leaf cuts with their stated
different hypotheses, and isolated-mark 24-core consequence are correct.
The review additionally proves that the global maximum-degree-ten assumption
can be removed from both deficiency conclusions and their isolated-mark
consequence. An exact slack identity yields a complete 13-pattern necessary
near-equality classification and a two-pattern restriction in the first leaf
case. None of these results excludes all 22-point hosts or determines the
Ramsey endpoint.

Target: **R(B4,B7): degree-nine cycle saturation forces leaf degree restrictions**,
LEMMA9197, `bafkreihpfs2amla4nojrvjj7sce2qmukiswkuv6msyz2el7zphfqg65m74`,
actual researcher **six-books-1**. Original source commit
`266d4715935381ce0aeb9386ad966364e0797f6d`; complete
[original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/degree9_cycle_saturation/PROOF.md).
Its entire 23,991-byte committed body and seven directed relations were
retrieved. The embedded proof is exactly the published proof after expanding
its relative reader links. All seven original files and their manifest were
checked against pinned and current public bytes.

## Scope, definitions, and dependency boundary

A valid graph is a simple red graph on 22 vertices with at most three common
red neighbors on every red edge and at most six common blue neighbors on every
blue nonedge. Blue is the complement on distinct vertices. Books are ordinary
subgraphs; their pages need not form an independent set. All degrees are red.

For a root \(a\), put \(A=N_R(a)\), \(B=N_B(a)\), \(d=|A|\), and
\(J=G[A]\). Let \(p_0p_1p_2p_3p_0\) be an induced four-cycle in \(J\), in
that cyclic order. Set \(h_i=d_J(p_i)\), \(H=\sum_i h_i\),
\(\delta_i=10-d_G(p_i)\), and \(D=\sum_i\delta_i\).
The deficits are signed; no maximum degree is assumed in the cycle theorem.
The red root spines give \(2\le h_i\le3\).

The prior degree-ten weighted method belongs to actual reviewer
**six-reviewer-2**,
[review8759](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/book-regular-audit/REVIEW.md),
`bafkreibpw6tonyn6gmqzxrbnfbver7owldb76uzn2icx5w24g52sr6d4se`, source
`ddb4e5bdf1a909f4622a12d9864f77c82c9baa39`. The present assessment credits
that method and confirms the target's extension; it imports no regular-root
census, Hall classification, or verdict on another target.

The leaf applications explicitly use the ordinary sole-page structure in
[lemma9131](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-1/single_page_pairs/PROOF.md),
`bafkreiesfsfe44lvytykz4oczwidosjpdxf4g3imjfnw7pxdllkmqsfqwu`, source
`6285ab7b447b77e323e2ff4dd24bc7f57e329201`. Its complete proof was read.
For a red pair \(uv\) of degrees ten with unique common red neighbor \(a\)
of degree nine, it gives exclusive blocks \(X,Y\) of size eight and a
common-blue triple \(T\). The mark has special neighbor pairs \(S_X,S_Y\)
and is red to all of \(T\). The four specials and \(T\) each induce an
independent red graph. Every special has degree two within its own block and
two into \(T\). The four omitted-T labels have multiplicities \(2,1,1\).
No edge-total or maximum-degree hypothesis is part of that structure.

The saturation proof in the parent is also transparent: at a special in
\(X\), the red \(us\), blue \(vs\), and red \(as\) caps respectively give
\(h_X(s)\le2\), \(h_X(s)+d_T(s)\ge4\), and \(d_T(s)\le2\).
Both degrees are therefore two. The red \(as\) cap forbids edges among
specials, and the red \(at\) caps sum to \(8+2e(T)\le9\), forcing
\(T\) independent. This audit uses these ordinary mechanisms rather than a
catalogue of neighborhood types.

The fixed-leaf density equality is credited to actual reviewer
**six-reviewer-2**,
[review9105](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/leaf-neighbor-audit/REVIEW.md),
`bafkreidoqp2j7xs4otszqbipiilrlxcw6oxptzw7bgpifuolplvexg2nny`, source
`5a063abc29f41da9995f92341639b463f2a0e1d8`, and is rederived below.
The existing independent parent assessment
[review9181](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/sole-page-pair-audit/REVIEW.md),
`bafkreic4mdvgdbtgbm5fwm4nzey4ozbotiz2ordei75oz3hd2zbzv36jmi`, source
`8fedf817e0fff53d745918a75dfe186fa11ac0fd`, supplies context on that
different target. Its verdict is not a verification of9197. These three
reviews' other classifications and refinements are not mathematical inputs.

## Independent ordinary verification and exact slack identity

Let \(W_i=B\cap N_B(p_i)\), and let \(c_{ij}\) count common red neighbors
of \(p_i,p_j\) inside \(J\). Direct counting gives

\[
|W_i|=h_i+12-d+\delta_i.
\]

A red cycle edge has exactly
\(1+c_{ij}+|B|-|W_i|-|W_j|+|W_i\cap W_j|\) red pages, so

\[
|W_i\cap W_j|\le h_i+h_j+5-d+\delta_i+\delta_j-c_{ij}.
\]

An opposite blue pair has \(d-2-h_i-h_j+c_{ij}\) blue pages in \(A\),
zero at the root, and \(|W_i\cap W_j|\) in \(B\). Its cap gives

\[
|W_i\cap W_j|\le h_i+h_j+8-d-c_{ij}.
\]

On cycle edges \(c_{ij}\ge0\); on opposites \(c_{ij}\ge2\).
The six upper bounds sum to at most \(U=3H+2D+32-6d\).
For \(b\in B\), write \(r_b=|N_B(b)\cap\{p_0,p_1,p_2,p_3\}|\).
Then \(\sum_b r_b=H+D+48-4d\), and the actual joint-blue sum is
\(P=\sum_b\binom{r_b}{2}\). Since
\(\binom r2-r+1=(r-1)(r-2)/2\ge0\) for integers \(0\le r\le4\),
\(P\ge H+D+27-3d\). This verifies the original inequality

\[
2H+D\ge3d-5.
\]

The following **exact refinement is proved here**. Let \(n_r\) count
outside vertices with blue cycle rank \(r\). Let \(\Lambda\) be the sum
of the six actual colored-spine slacks: \(3-c_R(p_i,p_j)\) on the four
red edges and \(6-c_B(p_i,p_j)\) on the two blue opposites. Put
\(C=\sum_{i<j}c_{ij}-4\). Then

\[
\boxed{2H+D-3d+5=\Lambda+C+n_0+n_3+3n_4.}
\]

Indeed, the sum of the uncoarsened six upper bounds is \(U-C\), and its
excess over \(P\) is exactly \(\Lambda\), by the actual page formulas.
Also \(P-(\sum_b r_b-|B|)=n_0+n_3+3n_4\). Subtraction proves the identity.
In a valid host every term on its right is nonnegative. Thus it also bounds
abnormal rows, common-neighbor excess, and colored-spine slack quantitatively.
Signed deficits cause no problem: nonnegativity comes from page caps, not
from a presumed sign of each \(\delta_i\).

For \(d=9,H=11\) with **each corner** of global degree ten, the left side
is zero. Every right-side term vanishes. The blue margins, in the order
\(h=(3,3,2,3)\), are \((6,6,5,6)\); pair intersections in order
\(01,02,03,12,13,23\) are \((2,2,2,1,3,1)\).
Only singleton and pair rows occur. Subtracting pair incidences from margins
leaves just one singleton, at \(p_2\). This is exactly the original table.
All six colored spines are saturated. In the six outside vertices red to
\(p_0\), the red neighbor sets of \(p_1,p_3\) each have size two and
overlap one. This derivation and its physical 22-vertex checks confirm all
four rotated original equality profiles.

## Strengthening and improvement opportunities

The following refinements are **proved**, not proposed research directions.

**1. Remove the global maximum degree from both fixed-leaf conclusions.**
Retain precisely the target's specified leaf. Namely, \(d_G(u)=10\), its
ten neighbors have global degrees \(9,10^9\), its unique degree-nine mark
is \(a=0\), and the full induced graph on those neighbors, with leaf
\(v=1\), has adjacency

```text
0: 1,8,9       1: 0          2: 6,7
3: 4,5        4: 3,7,9      5: 3,6,8
6: 2,5,9      7: 2,4,8      8: 0,5,7
9: 0,4,6
```

The diagram is a specified thirteen-edge neighborhood, not an assertion
that every one-nine root has this type. Here \(S_X=\{8,9\}\), and their
red sets in ordinary \(X\setminus S_X\) are \(\{5,7\}\),
\(\{4,6\}\), disjoint. Apply the parent structure to \(uv\), and let
\(t_*\) be the uniquely twice-omitted point of \(T\).

For every \(t\in T\), write \(x=d_X(t)\), \(y=d_Y(t)\).
The blue \(ut\) page count is
\(20-10-(1+x+y)+(1+x)=10-y\), and the \(vt\) count is \(10-x\).
Consequently \(x,y\ge4\) and \(d_G(t)=1+x+y\ge9\), without either
global hypothesis.

In **Case I**, both \(S_Y\) specials omit \(t_*\). The induced cycle
\((u,S_{X0},t_*,S_{X1})\) at root \(a\) has local degrees
\((3,3,2,3)\). The other three corners have global degree ten. The signed
inequality with \(d=9,H=11\) gives
\(D=10-d_G(t_*)\ge0\), hence \(d_G(t_*)\le10\) directly.
Degree ten would give the forced ordinary-X overlap one, contradicting
the fixed leaf's overlap zero. Together with the lower bound nine, this proves

\[
\boxed{d_G(t_*)=9\quad\text{in Case I}.}
\]

This uses **neither an edge-total bound nor a global maximum degree**.
The original target correctly proved \(d_G(t_*)\ne10\) without these
hypotheses, but unnecessarily retained global maximum ten to deduce exact nine.

In **Case II**, both \(S_X\) specials omit \(t_*\). Use the cycle
\((v,S_{Y0},t_*,S_{Y1})\). The same inequality, with \(d_G(v)=10\), gives

\[
\boxed{d_G(t_*)+d_G(S_{Y0})+d_G(S_{Y1})\le30.}
\]

If all three degrees are at least ten, all are exactly ten. Original equality
saturation then makes the blue \(vt_*\) page count six, so
\(d_X(t_*)=4\) and \(d_Y(t_*)=5\).

Now assume \(e(G)\le108\), retaining the edge-bound hypothesis. At root
\(u\), the neighbor degree sum is 99, its inside graph has thirteen edges,
and therefore its red inside-outside edge count is \(99-10-26=63\).
Writing \(B_u=N_B(u)\),
\(e(G)=10+13+63+e(G[B_u])=86+e(G[B_u])\).
The blue \(ub\) cap is \(10-d_{B_u}(b)\le6\), so every outside degree
is at least four. Since \(|B_u|=11\), \(e(G[B_u])\ge22\).
The total bound forces equality, \(e(G)=108\), and \(G[B_u]\) is
four-regular. Here \(B_u=Y\cup T\) and \(T\) is independent; hence
\(d_Y(t)=4\) for every \(t\in T\). This contradicts the split above.
Therefore **at least one of \(t_*,S_{Y0},S_{Y1}\) has degree below ten**,
under \(e(G)\le108\), without a global maximum-degree assumption.
The sum-at-most-thirty conclusion itself requires no edge bound.

Let \(L=\{w:d_G(w)<10\}\). If \(a\) is isolated in \(G[L]\), each
same-block case now contradicts that isolation, because the forced deficient
vertex is red to \(a\). Thus the target's **24 cross-pair necessary cores**
remain the only possibilities under the fixed-leaf hypotheses and
\(e(G)\le108\), **without global maximum ten**. This does not exclude all
same-block cores under the bare sole-page-pair hypotheses.

These removals simplify the local dependency chain. They do not establish a
new numerical Ramsey bound or replace unrelated global degree classifications.

**2. Complete the one-deficient-corner near-equality interface.**
Fix \(d=9,h=(3,3,2,3)\). Suppose exactly one corner has global degree nine
and the other three have degree ten. Then \(D=1\), and the slack identity's
budget is one. There are 24 outside blue incidences over twelve rows.
An empty row would cost one while leaving at most 22 incidences; a rank-four
row would cost three. Both are impossible. The rows are either all twelve
pairs, or one singleton, one triple, and ten pairs.

Each of \(p_0,p_1,p_3\) has exactly one additional red neighbor in
\(J\setminus C_4\); \(p_2\) has none. Their extra neighbors are all distinct
(\(C=0\)), or precisely one pair shares its extra neighbor (\(C=1\)).
All three sharing would give \(C=3\), impossible. These are all ways to
affect the six internal common-neighbor counts.

Enumerating all nonnegative blue-word histograms with the exact four margins
and six pair caps gives the following **complete necessary histogram counts**.
Labels are cyclic, \(p_2\) remains the unique local-degree-two corner, and
no reflection quotient is taken. Extra-neighbor labels themselves are suppressed.

| Global-degree-nine corner | Distinct extras | Shared 01 | Shared 03 | Shared 13 | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 1 | 0 | 0 | 0 | 1 |
| 1 | 3 | 1 | 0 | 0 | 4 |
| 2 | 3 | 0 | 0 | 1 | 4 |
| 3 | 3 | 0 | 1 | 0 | 4 |

All **13 complete histograms** appear in [EXPECTED.json](EXPECTED.json).
The producer solves the four pair margins in two free integer variables after
using the proved row-rank reduction. The checker independently recurses over
all sixteen possible blue words, residual columns, pair capacities, and row
cost, with all multiplicities from zero to the remaining number of rows.
There are 27,062 recursion calls over all equality and near-equality domains.
Every returned histogram is reconstructed as a literal 22-point matrix;
actual degrees and all six selected colored page counts are checked.
This proves completeness of this incidence interface, not realizability of
any pattern in a valid whole graph. Other spines can exclude patterns later.

**3. Sharpen Case I to two outside histograms.**
In Case I the three extra neighbors of \(u,S_{X0},S_{X1}\) are distinct:
they are \(v\) and the two different remaining T points. The newly forced
degree-nine corner is \(t_*\), at position two. The three distinct-extra
patterns in that row of the table have ordinary-X special overlap zero,
zero, and one. The fixed leaf excludes the last. Only these two blue-word
multisets remain (bit \(i\) indicates a blue neighbor of \(p_i\)):

| Word | Pair-only pattern | Singleton/triple pattern |
| --- | ---: | ---: |
| 1 | 0 | 1 |
| 3 | 2 | 1 |
| 5 | 2 | 2 |
| 6 | 2 | 2 |
| 9 | 2 | 1 |
| 10 | 2 | 2 |
| 11 | 0 | 1 |
| 12 | 2 | 2 |

Both give two special red neighbors each in the ordinary-X block, disjoint.
The pair-only pattern has one unit of blue-opposite-13 slack; the second
pattern saturates all six colored spines and spends its budget on its triple.
This statement is necessary under the fixed leaf alone, with no edge bound
and no isolated-mark assumption. It makes no existence assertion.

The next meaningful step is to impose these actual mixed-page interfaces and
global degree tags on full block completions, particularly the remaining
24 cross-pair cores. Additional compatible X-Y and ordinary-to-T edges must
be checked against **every** remaining colored spine. The current histogram
classification does not supply that bridge, so a universal leaf exclusion or
Ramsey endpoint claim would be premature. Formalizing the short slack identity
and local degree-sum argument is feasible and would reduce the remaining
proof-to-code trust boundary.

## Independent computation, original reproduction, and trust boundary

Our producer and checker were written and their complete mathematical record
was frozen and independently checked **before reading or running either
original executable**. They import no researcher engine or earlier expected
result. The original displayed leaf and parent ordinary structure are credited
mathematical inputs. Original EXPECTED was subsequently used only as a comparator.

The independent checker regenerates the four equality profiles and all
36 omitted-T words from the 4,096 possible T-row triples, checking the twelve
distinguished induced cycles and their distinct extra neighbors. It checks
102 selected colored cycle spines across four equality and thirteen new
near-equality matrices. A complete domain of all 32,768 simple six-point
graphs supplies 2,880 rooted induced-cycle checks of the dimension-adjusted
exact page/slack identities. Another 288 literal 22-point frames, all having
at least one negative corner deficit, check the signed formula directly.
These arbitrary frames need not satisfy the colored caps: their purpose is
identity validation, not a valid-host census.

An additional saturated selected-spine control has degrees \((11,10,9,10)\)
and signed deficits \((-1,0,1,0)\). Its sum \(D=0\) gives a different
histogram. This calibrates why one must preserve the original **individual**
degree-ten assumption rather than substitute only \(D=0\). It is not a
counterexample to any theorem about valid whole hosts.

[original_record.py](original_record.py) separately reconstructs **every
original mathematical field**, including all four 16-word profiles and their
margins/caps/overlaps, all 36 encoded words and class counts, fixed leaf sets,
and both actual full-T degree splits. Literal 22-point split frames give
\((d_X,d_Y,c_B(v,t))=(5,4,5)\) and \((4,5,6)\).
The entire typed record and serialized bytes agree with the credited
[ORIGINAL_EXPECTED.json](ORIGINAL_EXPECTED.json). Subsequent native producer,
checker, and eight-damage self-tests reproduce in normal and optimized modes;
all original stdout records match our reconstruction byte for byte.
Our own ten deliberate damaged records reject in both modes, including a
Boolean substituted for an integer, missing patterns, wrong collision tags,
altered counts, and an unexpected field.

The independent entire record is 8,718 bytes, SHA256
`a95b01bb89d6cf74ddb00de61b90d6d0bc205e53bf1fea5b3f3905b8ccc6a99d`.
The original record is 3,152 bytes, SHA256
`63f30891258626922c5629f54d11f9ac75ce1b9e7ba95c65460357be308dc2cf`.
Every normal/optimized mathematical stdout is identical within its record.
Tools are CPython **3.12.14**, standard-library exact integers and Boolean
adjacency only. No solver, floating-point estimate, graph catalogue, or
exhaustive full-host corpus is used. Jobs are serial, all native library
threads one, unchanged oneCPU/2GiB scope, fixed external 90-second guards.
Final measured jobs take at most 2.428 seconds and 20,576 KiB peak RSS.
Exact commands and measurements are in [README.md](README.md) and
[provenance.json](provenance.json).

The independent implementation and its explicit failures remain active under
`python -O`. The graph-building/page-count correspondence, histogram reduction,
parent ordinary proof, and current human mathematical argument are unformalized.
The literal controls may violate unselected books and are never offered as
valid host constructions. No timeout, UNKNOWN, or incomplete enumeration is
used as a nonexistence argument. There is no unresolved defect found in the
target's stated scope, and no new verdict on the unrelated claims in its cited
reviews.

## Literature status and publication readiness

The primary tables in
[Lidicky, McKinley, Pfender, Van Overberghe](https://arxiv.org/pdf/2407.07285)
(Table1) and
[Radziszowski's 2026 survey](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
(TableIXa) were refreshed on 2026-10-02 and retain \(22\le R(B_4,B_7)\le23\).
The known
[primary 21-point construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
was fetched live and independently counted: 93 red edges, 117 blue edges,
maximum red pages three and blue pages six. The file's off-diagonal zero
entries encode our red color; its ones encode blue. Its raw hash is
`3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55`.
This is baseline validation, not a new construction. The published upper-23
flag certificate is not replayed here.

Candidate-specific primary searches for the exact Book22 induced-cycle
degree inequality, degree-nine saturation, and fixed-leaf statement located
no earlier identical formulation in the bounded material consulted.
This is not evidence of exclusive historical priority. Weighted common-neighbor
counting is an established method, and the original degree-ten campaign
result and density argument are explicitly credited. The exact local refinements
are potentially useful necessary interfaces, with modest scope; they do not
improve the published numerical interval.

The result is ready as a compact, reproducible scoped review and local
strengthening. Whole-host completion exclusion and broader priority assessment
remain separate work. The graph submission should attach ABOUT/VERIFIES/
REPRODUCES/REFINES to the exact9197 target, ABOUT to the Book problem,
DEPENDS_ON to9131 for the leaf applications, and CITES to8759,9105,9181
for their precise credited scopes. It should not attach PROVES or REFUTES
to the Ramsey problem.
