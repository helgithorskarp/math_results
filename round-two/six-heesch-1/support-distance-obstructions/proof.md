# Optimal support-distance covering obstructions

Actual agent **six-heesch-1**, role **researcher**, 2026-10-01.

This note identifies the exact smallest obstruction distance available to
the earlier [linear corona transfer theorem](../linear-corona-bound/proof.md)
for three specific unmarked disc polyominoes. It gives new independently
checked covering certificates, two smaller transferred upper bounds, and
an exact limitation of that theorem. It does not construct five coronas,
compute these tiles' exact Heesch numbers, or claim a height record.

## 1. Definitions and prior theorem

Let S be a finite integer cell set, normalized so both coordinate minima
are zero. Let P be the union of its closed unit squares, and assume P is a
closed topological disc. Write m=|S|, let D4 act by the square symmetries,
and put

\[
 K=\operatorname{conv}\bigcup_{g\in D_4}(gP-gP),\qquad
 A=\operatorname{area}(K),\qquad J(x,y)=(-y,x),
\]
\[
 n(v)=h_K(Jv),\qquad
 d_S(t)=\min_{a\in S}n(t-a),\qquad
 \rho(T,S)=\max_{t\in T}d_S(t).
\]

Here h_K is the support function. K is D4-invariant, so n(v)=h_K(v);
it is a genuine norm. Its vertices are integer vectors, so n and d_S are
integer-valued on the integer lattice. Let

\[
 B_q(S)=\{t\in\mathbb Z^2:d_S(t)\le q\},\qquad q\in\mathbb Z_{\ge0}.
\]

A *rooted grid cover* of a finite target T is a finite packing consisting
of the fixed root P and integer translations of D4 copies of P whose
closed cells cover every cell of T. Interiors of copies are disjoint;
boundary contacts are allowed. Connectivity, layers and disc topology of
the union are not required. Thus these positive witnesses certify cover
feasibility, not multiple coronas.

The previous theorem says that failure of such a grid cover implies
absence of a plane tiling even under arbitrary real rigid motions, and
gives

\[
 H_h(P)\le U_S(\rho(T,S)):=
 \left\lceil\frac{A+2\rho(T,S)}m\right\rceil-2. \tag{1}
\]

The convention is the previous theorem's strict complete coronas: the
successive unions X_k satisfy X_(k-1) contained in int(X_k), each new copy
touches the preceding prefix, and interiors are disjoint. H_h allows
holes/pinches in the final outer prefix; imposing the disc-prefix H_c
condition can only decrease the maximum. The initial motions are arbitrary
real translations, rotations and reflections. Equation (1) inherits the
earlier sector-star alignment, floor-translation and strict segment-area
arguments; those are mathematical dependencies, not newly proved here.

The immutable prior source is commit
`23615d90ae815cc2785d91880f1de77344d70842`,
[proof.md](https://github.com/helgithorskarp/math_results/blob/23615d90ae815cc2785d91880f1de77344d70842/round-two/six-heesch-1/linear-corona-bound/proof.md),
with committed lemma
`bafkreicmouuxtbnucoivi542r53iyj5pzrgmk5ltgpfsc7dxwlu6sgwunq`.

## 2. Complete balls and optimality

**Lemma 1 (finite, complete target ball).** Let L be the larger physical
bounding-box side of P. Then

\[
 n(v)\ge L\|v\|_\infty,
 \qquad B_q(S)=S+\{v\in\mathbb Z^2:n(v)\le q\}. \tag{2}
\]

Consequently B_q is finite, computable by considering only offsets in
[-floor(q/L),floor(q/L)] squared, and contains every finite T with
rho(T,S)<=q.

*Proof.* After a D4 rotation, some difference of points of P has first
coordinate L. Reflecting its second coordinate gives two points (L,y),
(L,-y) in K; their midpoint is (L,0). D4 symmetry supplies the other three
axis points. The diamond with vertices (+/-L,0),(0,+/-L) lies in K, and
its support in Jv is L||v||_infinity. This proves the first inequality.
The definition of d_S proves the sum-set identity and all the conclusions.
Also B_0=S. QED.

**Theorem 2 (global minimum obstruction distance).** Suppose a rooted grid
cover of B_(q-1)(S) is given, and a finite T contained in B_q(S) is proved
not to admit a rooted grid cover. Then

\[
 q=\min\{\rho(R,S):R\subset\mathbb Z^2\text{ finite nonempty and
 not rooted-grid-coverable}\}. \tag{3}
\]

In particular, U_S(q) is the smallest bound obtainable from (1) by choosing
*any* finite integer-cell covering obstruction, including targets outside
the original Chebyshev target or outside the supplied negative core.

*Proof.* Every R with rho(R,S)<=q-1 lies in B_(q-1), so the given packing
covers R. Since rho is integral, no obstruction has rho<q. The supplied T
has rho<=q, hence it has rho=q. This attains the minimum. U_S is monotone
in its argument, so equation (1) has minimum value U_S(q) over all these
obstructions. QED.

Equivalently, if an obstruction exists, the minimum in (3) is the first
integer q for which the *entire* B_q is not rooted-grid-coverable. A positive
ball witness therefore supplies a global lower bound on obstruction
distance. An inclusion-minimal negative subset alone would not do so.
No minimal-cardinality or unique-core assertion is made for the subsets
used below.

**Lemma 3 (standard compactness characterization).** Every B_q is
rooted-grid-coverable if and only if there is a common-grid plane tiling
containing the root P.

*Proof.* A tiling has only finitely many copies meeting any finite B_q;
selecting them and the root gives a cover. Conversely, enumerate all
integer D4 placements disjoint from the root, and associate a Boolean
selection variable to each. Require coverage at every nonroot cell, and
forbid selection of two placements sharing a cell. Each coverage clause
is finite: there are at most 8m possible placements containing a fixed
cell. Collision clauses are also finite. Any finite collection of these
clauses is satisfiable by a packing covering B_q for sufficiently large
q, setting all other placement variables false. Thus the closed cylinder
sets defined by the clauses have the finite intersection property in the
compact countable product {0,1}^N. A common assignment selects disjoint
copies covering all cells, hence a tiling. This is the usual compactness
argument for finite local tiling constraints, not a new compactness
principle. QED.

## 3. Three certified thresholds

The three roots have m=20 and the same difference body:

\[
 K=\operatorname{conv}\{(-6,-4),(-4,-6),(4,-6),(6,-4),
 (6,4),(4,6),(-4,6),(-6,4)\}.
\]

Thus A=136, diagonal support D=h_K(1,1)=10, and

\[
 n(x,y)=6\max(|x|,|y|)+4\min(|x|,|y|). \tag{4}
\]

The exact cells are in [cases.json](cases.json). The case indices are
zero-based positions in the previously published ordered family obtained
by adding three cells to Kaplan's 17-cell seed and quotienting by D4.
The independently regenerated ordered-family SHA256 is
`935192a6bead7d979d7ed60f3907e52278962940d9b3c008d18af94a85fc36ef`.
The shapes and the original covering-radius classifications predate this
note; they are not new tile constructions.

| Family index | Covered ball | Positive copies including root | Negative target cells | Exact minimum rho | Best upper from (1) |
|---:|---:|---:|---:|---:|---:|
| 45 | B_11, 49 cells | 7 | 6 | 12 | 6 |
| 249 | B_21, 95 cells | 11 | 18 | 22 | 7 |
| 701 | B_29, 140 cells | 12 | 26 | 30 | 8 |

The negative targets lie in B_12, B_22 and B_30, respectively. Their
complete encodings have 58/410/660 candidate copies, 1121/8329/13531
variables and 3133/23494/38319 clauses. The published independently checked
RUP traces have 44/246/323 additions and total 77208 bytes. No selected
target is required to be connected or disc-shaped.

For comparison, the preceding radius-r formula used rho=rD: case45 had
published blocking radius 2 and upper 7; case249 had radius 3 and upper 8;
case701 had radius 3 and upper 8. The new upper bounds for the first two are
six and seven. The last remains eight, but its positive B_29 cover now
proves that *no finite target* can lower equation (1) below eight for this
root. This is a limitation of this particular theorem, not a claim that
the tile's actual Heesch number equals eight or exceeds seven.

These three new upper bounds use newly supplied negative certificates;
they do not depend on the old unpublished large proof corpus. The old
radius values are historical comparisons. In fact, the new negative core
for case701 has cell (9,4) outside the old radius 3 target, so it must not
be presented as a replay of that older radius 3 decision.

## 4. Complete covering encoding

[cover.py](cover.py) uses no search cutoff in building the candidate domain.
For each distinct normalized D4 orientation O, each demanded cell t outside
the root, and each a in O, it forms the placement O+(t-a). Placements
overlapping a root cell are excluded, and identical physical cell sets
are deduplicated. Any tile contributing a demanded cell has exactly such
a representation; irrelevant copies in a covering can be removed.
Therefore the candidate domain is complete. There is no bounding-box,
contact-only, layer or symmetry restriction on the physical placements.

One variable x_i selects each candidate. For every physical cell occupied
by any candidate, including cells *outside* the demanded target, impose
at-most-one on its owners. For each demanded nonroot cell impose the
disjunction of all its owners. A satisfying assignment decodes to a
nonoverlapping rooted cover, and every rooted cover gives a satisfying
assignment after removal of irrelevant copies. This proves equivalence
between the finite covering problem and the CNF.

For owners x_1,...,x_n with n>=3, use the standard sequential prefix
encoding with s_1,...,s_(n-1):

\[
 (\neg x_1\lor s_1),\quad (\neg x_n\lor\neg s_{n-1}),
\]
\[
 (\neg x_i\lor s_i),\quad(\neg s_{i-1}\lor s_i),\quad
 (\neg x_i\lor\neg s_{i-1})\qquad(2\le i<n).
\]

If x_i and x_j are true with i<j, the first two kinds of implications
force s_(j-1), while x_j forces its negation. Conversely, when at most
one x_i is true, assign s_i to the disjunction of x_1,...,x_i; every
clause is then satisfied. With two owners use their single pairwise
exclusion; with zero or one owner no exclusion is necessary. This proves
the auxiliary encoding for every owner count.

This is Sinz's established at-most-one sequential encoding, attributed to
[his CP 2005 paper](https://www.carstensinz.de/papers/CP-2005.pdf), Section 2.
Its use and the short completeness proof are not novelty claims.

The reader separately regenerates the placement domain using successive
quarter rotations and full translation rectangles, instead of the
target-minus-cell enumeration. It also regenerates B_q by a full lattice
rectangle and direct D4 widths of the physical cell union, without using
the convex-hull support routine. For a vector v, the direct width is the
anchor-cell projection spread plus |v_x|+|v_y|; maximizing over D4 equals
h_K(v)=n(v). These independent enumerations agree exactly for both balls
and every negative target.

## 5. Independent negative verification

[rup.py](rup.py) is a standard-library forward reverse-unit-propagation
checker. For each proposed clause C it assigns every literal of C false,
includes all current unit clauses, and propagates by examining clauses
whose literals have just become false. It accepts C only when this
produces a conflict. Hence the current formula implies C. By induction
every accepted addition is a consequence of the original CNF. The final
accepted empty clause proves that original CNF unsatisfiable.

Deletion lines are deliberately ignored. Keeping previous entailed clauses
is sound for proving unsatisfiability of the original formula. RAT-only
steps are unsupported and rejected. All three published traces consist
solely of RUP additions and end with the empty clause. Thus neither
Minisat22 nor Glucose4 is in the reader's logical trust boundary.

The optional generator checks the raw Glucose4 trace, records the proved
clauses used by each unit-propagation check, retains their dependency
closure from the final contradiction, and rechecks that trimmed trace
from the original CNF. Trim correctness is therefore checked again and
does not rely on trusting the dependency capture. The final artifacts,
not merely solver statuses or a successful solver run, are checked by the
reader.

CNF and proof hashes, counts, solver provenance, exact coordinates and
positive placements are recorded in cases.json. The reader directly checks
congruence, root inclusion, integer placements, nonoverlap and full lower
ball coverage. It also rejects six malformed proof controls, verifies a
deletion-handling control, and for each root rejects a missing positive
copy and an overlapping duplicate. The six proof controls include a
fabricated empty-clause proof of a satisfiable formula, a nonconsequence,
missing final contradiction, out-of-domain literal, missing terminator
and an internal zero.

## 6. Discovery, reproducibility and limits

The exploratory search used python-sat 1.8.dev24 / Minisat22 with at most
20000 conflicts per query, binary search between zero and the prior rD
distance, then guarded core reduction. It tested seven selected family
members, not all 1233. The 20-cell cases7,6,99,911 have exploratory
thresholds27,36,16,20 in local scratch only; this note publishes no proof
claim about them. No timeout or UNKNOWN was converted into an exclusion.

Fresh ungated negative CNFs for the three published cores were solved
with python-sat 1.8.dev24 / Glucose4 (4.1), with proof logging and a 30000
conflict guard. [PySAT's official solver API](https://pysathq.github.io/docs/html/api/solvers.html)
documents these solver interfaces. There is no external preprocessing,
floating-point arithmetic or multi-threaded solver step. The published
reader uses CPython 3.11.2, standard library only, with explicit checks
that remain enabled under python -O. Threads for numerical libraries are
restricted to one, and only one CPU-intensive job is run at a time.

The mathematical trust boundary is the prior all-motion transfer proof,
the finite-cover encoding proof above, and the correctness of this small
reader. This is reproducible computer-assisted evidence, not formal
proof-assistant verification or an independent reviewer verdict.

## 7. Literature and standing frontier

Kaplan's [2021 paper](https://arxiv.org/abs/2105.09438), published in 2022,
supplies the unmarked-polyform enumeration context and SAT corona method;
his [primary dataset](https://cs.uwaterloo.ca/~csk/heesch/) supplies square,
hexagonal and triangular-grid shapes and the H_c/H_h distinction. Those
are existing methods and results. The earlier round-two linear theorem
and the repository's
[20-cell growth manifest](https://github.com/helgithorskarp/math_results/blob/main/heesch_polyomino_euler_cnf/growth20_manifest.json)
are also prior published work.

The assigned broad unmarked-polyform-five goal was already achieved by
the known Mann fixture's 215-cell polyiamond realization, documented in
the repository before this round. The coordinated remaining square-cell
frontier is a rigorously finite unmarked polyomino with at least five
complete coronas. The broader planar-seven goal also remains outstanding.
Neither is solved here. The seed status was refreshed from the primary
pages on 2026-10-01; the 2025 primary
[historical survey](https://arxiv.org/abs/2509.12216) is context, not a
claim that an older construction is new.

The next useful mathematical step is a lower-corona construction on a
promising square-cell root, or a stronger layer-sensitive obstruction.
Equation (3) proves that further target trimming alone cannot improve
case701's upper bound in this particular transfer theorem.
The separate published
[pair-centered closure reduction](https://github.com/helgithorskarp/math_results/blob/cf3b672f2bf53a076c057b44a6f1a087ef028fcd/round-two/six-heesch-2/proof.md)
tracks interior depth for polyhex contacts. It is complementary context,
not a dependency of these certificates. Transferring that reduction to
all-motion square-cell tiles would require a sound translation-phase
analysis; square-tile axis alignment alone does not supply it.
