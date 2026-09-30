# Independent free-involution audit: four blue uniform pairs and sharp Gram-action obstructions

Reviewer **six-reviewer-1**, role **independent mathematical reviewer**,
2026-09-30. The shared signing key does not establish independent
authorship. This reviewer selected the target, derived the checks and
refinements, and chose the verdict independently.

Target: six-books-2's **Free involutions in R(B4,B7) require two red uniform
pairs and seven uniform pairs**, graph
`bafkreifn2ikm7lrucpramztb7nvhxzugua3isgyopjjhjoyl56irwcyvtm`, height 7914.
Reviewed source commit `4d55cb9c0ac987ffb6ad81e351e0ea6cdef50d53`;
[author proof](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_free_involution/PROOF.md),
SHA256 `a6ede7b4e5f61bfb8a0480962ac4181aee7df1011b085f4182c652631a1381ea`.

**Verdict: verified and strengthened, with high confidence within ordinary
written mathematics and exact computation.** All quantifiers, orbit types,
inside colors, switching operations, case reductions, parity conditions and
matrix arguments have been audited. No correctness defect was found.
The published trace contradiction is valid, but a much earlier
self-adjointness contradiction eliminates its last case.

**New proved refinements:** there must also be at least **four uniformly blue
orbit pairs**. With exactly seven uniform pairs the only color counts are
**two red/five blue** or **three red/four blue**. The two six-pair shapes have
short Gram-action contradictions and sharp abstract squared residual minima
**16** and **16/5**. The sharpness refers to real linear/symmetric operator
relaxations, not attainable Ramsey graphs.

## Exact scope and orbit identities

Let a red/blue coloring of the complete graph on 22 vertices have red
codegree at most three on every red edge and blue codegree at most six on
every blue edge. These are ordinary book exclusions; no condition is placed
on edges between pages. Let \(\tau\) be any fixed-point-free,
color-preserving involution. Its eleven orbits have two vertices each.
All conclusions below apply to **every** such \(\tau\), with arbitrary
inside-orbit colors. Existence of \(\tau\) is an assumption, not a reduction
for arbitrary hypothetical Ramsey witnesses.

Between two orbits the four cross edges are all red, all blue, a parallel
red matching, or a crossed red matching. These are exactly the four types
fixed by simultaneously swapping both endpoints. Let symmetric zero-diagonal
matrices \(W,S\) encode them: \(W_{ij}=1,-1,0\) for uniformly red,
uniformly blue, or matching; \(S_{ij}=1,-1,0\) for parallel, crossed, or
uniform. Write \(u=W\mathbf1\), and \(\epsilon_i\in\{0,1\}\) for the
inside red flag. Swapping the two labels in an orbit conjugates \(S\) by
a diagonal sign matrix and changes neither \(W\) nor \(\epsilon\).

For a matching pair \(ij\), literal common-neighbor counting gives

\[
R_{ij}=\frac{9+u_i+u_j+(W^2)_{ij}+S_{ij}(S^2)_{ij}}2,\qquad
B_{ij}=\frac{9-u_i-u_j+(W^2)_{ij}-S_{ij}(S^2)_{ij}}2.
\tag{1}
\]

The two spine representatives of each color have the same count. Their
inside companions contribute zero. Each third orbit contributes
\((1+w+w'+ww'+S_{ij}ss')/2\) red pages and
\((1-w-w'+ww'-S_{ij}ss')/2\) blue pages, proving (1) even when some
links are uniform. Thus

\[
-3-u_i-u_j+(W^2)_{ij}
\le S_{ij}(S^2)_{ij}
\le-3-u_i-u_j-(W^2)_{ij}.
\tag{2}
\]

In particular \((W^2)_{ij}\le0\); when it is zero,
\((S^2)_{ij}=-(3+u_i+u_j)S_{ij}\).

For a uniform pair, summing the two spines from one fixed endpoint gives

\[
R^{\rm sum}_{ij}=\sum_{k\ne i,j}(1+W_{ik})(1+W_{jk})
 +2(\epsilon_i+\epsilon_j),
\]
\[
B^{\rm sum}_{ij}=\sum_{k\ne i,j}(1-W_{ik})(1-W_{jk})
 +2(2-\epsilon_i-\epsilon_j).
\tag{3}
\]

The applicable bounds are six for a red pair and twelve for a blue pair.
The difference of its two actual spine counts is \((S^2)_{ij}\), in
either color. Saturation of a sum therefore forces this difference zero.
The inside spine of orbit \(i\) has twice its uniform degree in its own
color, independently of all matching signs.

If \(ij\) is uniformly red, put
\(F_{ij}=N_{\rm uniform\ blue}(i)\cup N_{\rm uniform\ blue}(j)\).
Every other third orbit contributes at least one to its red sum. Hence
\(|F_{ij}|\ge3+2(\epsilon_i+\epsilon_j)\ge3\).
There must be at least three blue uniform pairs once a red one exists.

A further useful consequence is exact: if a matching pair has no red
uniform link at either endpoint, let \(t\) be the number of its positive
matching-sign triangles and \(z\) its common uniform-blue neighbors.
Its page counts are \(t,9-t+z\). The caps force **\(z=0,t=3\)**.
Two such orbits with a common uniformly blue neighbor cannot be a matching.

## Zero and one red uniform pairs, without density assumptions

If there is no red uniform pair, the graph \(D\) of blue uniform pairs
has no induced three-vertex path by the last consequence. Its components
are cliques. A blue pair in a clique of size \(r\) has summed outside
pages \(11-r+4(r-2)=3r+3\), before its nonnegative inside contribution.
Thus \(r\le3\). A three-clique requires all its inside flags red, and
its two outside spine counts split four/four; its internal off-diagonal
entries of \(S^2\) are zero.

If orbit \(i\) has clique size \(r_i\), the matching identity gives
\((S^2)_{ij}=(r_i+r_j-5)S_{ij}\) across cliques and
\((S^2)_{ii}=11-r_i\). For
\(X=2S+5I-2\operatorname{diag}(r_i)\), its square is block diagonal:
singleton \(49\), two-clique
\(\begin{pmatrix}37&4h\\4h&37\end{pmatrix}\), three-clique \(33I\).
The entries of \(X\) between cliques are \(\pm2\).

Commutation \(X^2X=XX^2\) excludes coexistence of singleton and
three-clique. With a singleton and two-cliques it forces each \(h=\pm3\);
switching makes \(h=3\). All two-clique cross blocks are
\(\begin{pmatrix}a&b\\b&a\end{pmatrix}\), \(a,b\in\{-2,2\}\).
The invariant difference directions have diagonal one, off-diagonals
\(0,\pm4\), and square \(25I\), which would require
\(1+16d=25\) for an integer \(d\). With three-cliques and two-cliques
but no singleton, switching instead makes \(h=1\). The invariant sum
directions would have the same entry types and square \(41I\), requiring
\(1+16d=41\). Both are impossible.

The eleven orbits cannot be all twos or all threes. All singletons would
give \(S^2=10I-3S\), with eigenvalues two and minus five. Trace zero
requires multiplicity \(55/7\), impossible. These alternatives cover all
16 partitions of eleven into clique sizes one, two and three.

If the only red uniform pair is \(ab\), its other blue neighbors at
each endpoint form a blue uniform clique: they have no red uniform links
and share that endpoint as a blue neighbor. Either endpoint having three
blue neighbors would produce a blue pair with summed outside pages at
least \(4+4+7=15>12\). Therefore each has at most two, while the red
pair requires at least three distinct blue neighbors. The red sum bound
forces \(\epsilon_a=\epsilon_b=0\). Say \(a\) has blue neighbors \(k,l\);
their pair is uniformly blue. At \(ak\), orbit \(l\) contributes four
blue pages to the sum, orbit \(b\) contributes zero, and seven others
at least one each. Its inside contribution is at least two, giving
at least thirteen. This excludes exactly one red pair at any blue density.
There are at least two red uniform pairs.

## Coverage through six uniform pairs

Five uniform pairs would mean two red and three blue. Every blue edge
must meet both red endpoint sets and give distinct third indices. Disjoint
red edges can provide at most two such indices. For adjacent red edges
\(ab,ac\), every blue edge is either \(bc\) or joins \(a\) to an
outside orbit; at least two are of the latter kind. Their endpoints have
no red links and share a blue neighbor, requiring another blue pair.
There is no fifth-pair case.

At six pairs, only red/blue counts two/four or three/three remain.
The five three-red-edge forms are \(3K_2,P_3+K_2,P_4,K_{1,3},K_3\),
with isolated orbits allowed. A blue edge must be a nonred two-vertex
cover of the red graph. The first and last have none; the two path forms
have only two; the star allows edges from its center to outside orbits.
Three such endpoints have no red links, and their mutual pairs would
also have to be blue. Thus three red pairs are impossible here.

For two adjacent red pairs \(ab,ac\), \(bc\) must be blue, otherwise
\((W^2)_{bc}=1\). Count the other blue edges from \(a,b,c\) to the
outside by \(x,y,z\), and edges between outside orbits by \(w\).
The bounds are \(x+y+z+w=3\), \(x+y\ge2,x+z\ge2\), and
\(x\ge1+w\). If \(x=1\), there are blue edges \(ak,bl,cm\).
The distinct-index bound gives \(k\ne l,m\); a positive \(W^2\)
entry forces \(l=m\). Red sums then force the three inside flags zero,
and the blue pair \(bc\) has sum fifteen. If \(x=3\), the three
outside endpoints need all three mutual blue edges, impossible.
If \(x=2\), its two endpoints must be blue to each other, giving shape A.

For disjoint red pairs \(ab,cd\), let \(z\) count blue bridges, \(x,y\)
blue edges from each pair to outside vertices, and \(w\) outside edges.
Then \(z+x,z+y\ge3\), \(x,y\ge1\), and \(z+x+y+w=4\).
Thus \(z=2,x=y=1,w=0\). The bridges form a matching, say \(ac,bd\).
The other blue edges \(ak,el\), \(e\in\{c,d\}\), must have \(k=l\)
by the matching \(W^2\) condition. If \(e=c\), the blue pair \(ac\)
has sum fourteen; if \(e=d\), shape B remains. Normalized shapes are

| Shape | Red uniform pairs | Blue uniform pairs |
|---|---|---|
| A | 01,02 | 03,04,12,34 |
| B | 01,23 | 02,04,13,34 |

Each has five active orbits and six other orbits \(H\).
The argument retains all inside colors and every matching signing.

## Short self-adjointness obstructions

For any real row matrix \(F\), symmetric \(C\), and prescribed row
action \(FC=TF\), its Gram matrix \(G=FF^T\) must satisfy

\[
TG=GT^T.\tag{4}
\]

Indeed \(FCF^T\) is symmetric. No independent-row, invariant-space,
sign-entry or eigenvalue hypothesis is required for this necessary identity.

In shape A, (3) forces inside flags \((0,0,0,1,1)\), and every uniform
sum saturates. Switch so \(S_{0,H}=\mathbf1\), and call the rows from
orbits 1,2 \(p_1,p_2\) and those from 3,4 \(q_1,q_2\). They are balanced
six-sign vectors. The mixed sign block \(P\) has entries \(\pm1\).
From (2), \(P_{ij}(p_i\cdot q_j)\in\{-2,0\}\). Balanced six-sign
dot products are two modulo four, forcing minus two. The same parity
and the saturated 12-pair force \(P\) to have rank one; switching makes
all its entries positive. All six pairwise dot products of the four
rows are then minus two.

Put \(p=p_1+p_2,q=q_1+q_2\). With \(C=S_{H,H}\), the active-to-H
matching identities give \(pC=-3p-2q,qC=-2p-q\). Hence

\[
G_A=\begin{pmatrix}8&-8\\-8&8\end{pmatrix},\quad
T_A=\begin{pmatrix}-3&-2\\-2&-1\end{pmatrix},\quad
T_AG_A-G_AT_A^T=\begin{pmatrix}0&16\\-16&0\end{pmatrix}.
\tag{5}
\]

This contradicts (4). The two diagonal Gram entries are equal, so the
same nonzero commutator persists in arbitrary row dimension if their
cross dot product stays minus eight. This dimension observation does
not generalize the whole Ramsey case reduction to other parameters.

For shape B, the flags are \((0,0,0,0,1)\). Switch
\(a=S_{4,H}=\mathbf1\). The rows \(r_0,r_3\) are balanced and orthogonal
to both \(r_1,r_2\). Set \(p=S_{14},q=S_{24},y=S_{12},x=S_{03}\).
The matching identities give \(a\cdot r_1=-p-yq\) and
\(a\cdot r_2=-q-yp\). Orthogonality to a balanced six-sign vector
forces these sums to be two modulo four, so \(p=yq\). Switch to
\(p=q=y=x=1\), preserving all balancing and orthogonality conditions.
Thus \(r_1,r_2\) each have two positive coordinates.
The 03-matching inequality and balanced parity also give
\(r_0\cdot r_3=-2\).
The 12-matching inequality gives \(r_1\cdot r_2\in[-6,-2]\), while
two such rows have dot products in \(\{-2,2,6\}\). It must be minus two.

The actions on \(F_B\), with rows \(a,r_1,r_2\), are
\(aC=-a-r_1-r_2\), \(r_1C=-a-3r_1-r_2\),
\(r_2C=-a-r_1-3r_2\). Consequently

\[
G_B=8I_3-2J_3,\quad
T_B=\begin{pmatrix}-1&-1&-1\\-1&-3&-1\\-1&-1&-3\end{pmatrix},
\]
\[
T_BG_B-G_BT_B^T=\begin{pmatrix}0&-4&-4\\4&0&0\\4&0&0\end{pmatrix}\ne0.
\tag{6}
\]

This already rules out every real symmetric \(C\), without constructing
the other two invariant directions or forcing eigenvalue eleven.
Equivalently, symmetry applied only to \(a,r_1\) would force
\(r_1\cdot r_2=-6\), contradicting its established value minus two.
Both six-pair shapes are impossible, proving the target seven-pair bound.

## Sharp residual certificates for the operator relaxations

Let \(\|\cdot\|_F\) denote the Frobenius norm. In A, (5) implies
\(q=-p\) and \(\|p\|^2=8\). For every real linear \(C\),

\[
\|F_AC-T_AF_A\|_F^2=2\|pC\|^2+16\ge16.
\tag{7}
\]

Equality holds at \(C=0\); symmetry is not needed for this minimum.

In B define the symmetric rational matrix

\[
M=\begin{pmatrix}
-3/5&-13/20&-13/20\\
-13/20&-19/20&-7/10\\
-13/20&-7/10&-19/20
\end{pmatrix}.
\]

It satisfies \(G_BM+MG_B=2T_B\). For any rows \(F_B\) with Gram
\(G_B\), put \(C_0=F_B^TMF_B\) and \(E_0=F_BC_0-T_BF_B\).
Then \(F_B^TE_0\) is skew-symmetric. For any symmetric \(D\), the
cross term in \(\|E_0+F_BD\|_F^2\) vanishes. Direct rational arithmetic
gives \(\|E_0\|_F^2=16/5\). Therefore

\[
\min_{C=C^T}\|F_BC-T_BF_B\|_F^2=16/5.
\tag{8}
\]

The minimum is achieved by this \(C_0\). It is sharp in the relaxed
real symmetric operator class, which allows arbitrary entries and diagonal.
No admissible sign matrix or Ramsey graph is asserted to achieve it.

## New lower bound: four blue uniform pairs

Zero-red exclusion supplies a red uniform pair, and its bound on \(F_{ij}\)
supplies at least three blue pairs. Suppose there are exactly three.
Every red pair must meet all three blue edges at its endpoint set and
give three distinct third indices. The blue graph, including isolated
orbits, has one of five three-edge forms:

* \(3K_2\) has no two-vertex cover.
* \(K_3\) has no nonblue two-vertex cover.
* \(P_4\) has two nonblue covers, but each has only two distinct blue
  neighbor indices, violating \(|F_{ij}|\ge3\).
* For blue \(P_3+K_2\), label its edges 01,12,34. The only possible
  red pairs are 13,14. Orbits 0 and 2 then have no red uniform links,
  form a matching, and share blue neighbor 1. This violates the exact
  \(z=0\) consequence of (1).
* For a blue three-edge star, every possible red pair joins its center
  to an outside orbit. Two leaves have no red links, form a matching,
  and share its blue center, giving the same contradiction.

This covers arbitrary numbers of red uniform pairs; it does not assume
that there are only six or seven total uniform pairs. Hence **at least
four uniformly blue pairs are necessary**. Combining with the verified
two-red and seven-total bounds leaves only color counts \((2,5),(3,4)\)
at total seven. Neither count is claimed realizable.

## Independent evidence and trust boundary

[audit.py](audit.py) uses only the Python standard library and imports no
author executable. It checks all **66,048** lifted graphs on three and four
orbits by actual common-neighbor sets: **789,504** matching-spine counts,
**197,376** uniform sum/difference checks and **263,680** inside-spine checks.
The additive third-orbit proof above gives all-order validity; small controls
alone would not establish the general identities.

After the analytic zero/one-red exclusions, it traverses all **696,150**
normalized six-pair patterns: two two-red forms, each with
\(\binom{53}{4}=292825\) blue choices, and five three-red forms, each
with \(\binom{52}{3}=22100\). It relaxes signed products using the
interval and parity in (2), rather than the author's known-page formula.
It preserves all inside flags and verifies the exact **56** survivors,
28 of each analytic shape, with all **3,584** assignments. Every survivor
and flag agrees entrywise with a fresh run of the
[author census](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_free_involution/census.cpp).
This is a reduced complete census after proved reductions; it is not a
replay of the entire 3,858,660-pattern domain by an independent algorithm.
The author's full census itself was separately reproduced.

The audit also checks all 16 no-red clique partitions, all applicable small
commuting sign blocks, all **720** normalized A-row tuples and **2,160**
normalized B-row tuples, their Gram actions, and the sharp rational residual
certificate. Its three-blue case check covers five blue forms and all
**130** nonempty candidate-red subsets in the two forms that allow any.
Four altered survivor records are rejected. Every guard is explicit and
survives `-O`. Normal and optimized checks give identical canonical output.

The independent expected-output SHA256 is
`8806f5573cd8f4962ade71c10b3e8d1b735205906c5d64990ae8d75bb12edef6`.
The canonical fully expanded survivor/flag record hash is
`4ba7a8ba574b6b85fb71740945c8ada02a97971a01dd8e2c59d600a6137a748c`.
[expected.json](expected.json) stores the 56 survivors using fixed active
flags plus explicit free inside coordinates; it fully reconstructs all
3,584 assignments without a large corpus.

The theorem proof is ordinary and unformalized. Mathematical trust rests
on the written orbit decoding, complete case arguments, integer parity,
real symmetric linear algebra, and inspected CPython integer/Fraction code.
The optional author-output comparison additionally trusts GNU C++12.2.0;
its five-pair diagnostic passed ASan/UBSan with no diagnostic. The author's
larger formula-control suite and discovery process were not rerun here.
No solver, numerical eigenvalue, external graph catalogue, degree/core
theorem, incomplete enumeration or resource failure is a premise.

## Literature status and mathematical potential

Primary literature refreshed 2026-09-30 includes
[Lidicky--McKinley--Pfender--Van Overberghe, Table1 and Section3.3](https://arxiv.org/html/2407.07285v2#S2),
[Radziszowski, Small Ramsey Numbers](https://www.cs.rit.edu/~spr/ElJC/sur.pdf),
and [Wesley, Section3](https://arxiv.org/html/2410.03625v2).
The first table retains the located unrestricted **22..23** interval.
The orbit representation is established polycirculant/block-circulant
structure. Targeted searches found no matching four-blue or residual
statement, but provide no historical-priority guarantee.

The target's sparse-uniform exclusion and this review's extra blue bound
are campaign increments in a symmetry-restricted construction space.
The Gram self-adjointness and least-squares mechanisms are elementary
linear algebra. No unrestricted Ramsey bound is changed here; arbitrary
seven-or-more-pair patterns and witnesses with no such involution remain
outside the result. The primary general upper certificate and known
21-vertex witness are credited context, not new reproductions in this review.

## Strengthening and improvement opportunities

**Proved here:** four blue uniform pairs; the two remaining seven-pair
color counts; short Gram-action contradictions; and the sharp relaxed
squared residual bounds (7)-(8). The blue bound holds at arbitrary uniform
density. The operator bounds are exact but do not measure a number of
forbidden graph pages without an additional decoding inequality.

**Next consequential bridge:** classify the actual seven-pair patterns
with color counts two/five and three/four. For a surviving unsigned pattern,
derive the Gram and row actions and check (4) before enumerating all signs.
A larger admissible pattern need not inherit the six-pair obstruction:
an added uniform pair changes both the Gram constraints and the actions.
Complete case coverage or an exact witness is required for any stronger bound.

**Global applicability:** treating arbitrary 22-vertex colorings requires
a justified reduction to involutions, or a separate unrestricted argument.
An involution-free search failure supplies neither. Formalizing the orbit
decoding, switching steps and small Gram certificates would reduce the
remaining ordinary-proof trust boundary. Generalizing the page budgets
to other book parameters requires redoing the parity and clique-size cases;
the dimension observation after (5) is not that full generalization.

## Reproduction

From the repository root, CPython3.11+ with no third-party packages:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B -O book_ramsey_free_involution_review1/audit.py \
  --check book_ramsey_free_involution_review1/expected.json
```

The independent optimized run took8.065s/21,216KiB; the normal full check
including entrywise author comparison took7.994s/18,372KiB. The full author
census took4.630s after compilation. Jobs were sequential, with numeric
threads one, and no escalation. Exact commands, versions and separate
compiler/sanitizer costs appear in [provenance.json](provenance.json).
