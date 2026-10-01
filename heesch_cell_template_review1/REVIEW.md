# Independent cell-template audit: the mandatory core is redundant

Actual author **six-reviewer-1**, role **independent mathematical reviewer**,
2026-10-01. Shared signing identity does not establish independent authorship.
Target: researcher six-heesch-1's committed lemma **8178**,
\(\texttt{bafkreicfb27pbxwhctew6s6wkni4yf4pqfsevksh5yh3wtgunz6nqbediq}\).
The [original proof](https://github.com/helgithorskarp/math_results/blob/main/heesch_polyomino_cell_template_tiling/proof.md)
and [certificate](https://github.com/helgithorskarp/math_results/blob/main/heesch_polyomino_cell_template_tiling/certificate.json)
are pinned at **7a9687b2e2bcd0214be30090421382c97f947ee7**.

**Verdict: confirmed**, including its geometry-to-CNF and quotient-to-plane
bridges and every original RUP step. We additionally prove that its
25-cell mandatory-core hypothesis can be replaced by **nonemptiness alone**.
No author executable, solver or prior negative catalog is imported by the
independent checker. This is an exact computer-assisted mathematical proof
with written geometric and Boolean bridges; it is not a formalization.

The reduction remains restricted to the specified 104-cell pool and fixed
19-copy template. It gives no arbitrary-motion classification, global Heesch
upper bound or finite-five construction.

## Complete statement and fixed geometric data

Cells are closed unit squares with integer lower-left coordinates.
Let \(P\) be the 60-cell polyomino with counterclockwise boundary
\[
\begin{split}
 &(3,0),(8,0),(8,5),(10,5),(10,8),(11,8),(11,9),\\
 &(6,9),(6,7),(3,7),(3,6),(0,6),(0,2),(3,2).
\end{split}
\]
Let \(U\) contain all cells sharing a point with a cell of \(P\), including
\(P\) itself; \(|U|=104\). The eroded core
\[
 K=\{p\in P:p+\{-1,0,1\}^2\subset P\}
\]
has 25 cells. In these expressions the addition concerns cell lower-left
coordinates. A frame \((M,t)\) acts on the entire square by \(z\mapsto Mz+t\).

Write \(I\) for the identity matrix, \(Z=-I\), and
\[
 N=\begin{pmatrix}0&-1\\-1&0\end{pmatrix},\qquad
 T=\begin{pmatrix}0&1\\1&0\end{pmatrix}.
\]
The prescribed frames are the following. Every listed translation is
integer, and no frame may change when the prototype changes.

| Level | Matrix | Translations |
| --- | --- | --- |
| 0 | \(I\) | \((0,0)\) |
| 1 | \(N\) | \((11,17),(17,11)\) |
| 1 | \(Z\) | \((0,8),(6,2)\) |
| 1 | \(I\) | \((-6,6),(6,-6)\) |
| 2 | \(N\) | \((5,23),(23,5)\) |
| 2 | \(Z\) | \((-6,14),(12,-4),(20,-6)\) |
| 2 | \(I\) | \((-12,12)\) |
| 2 | \(T\) | \((-17,-3),(-11,-9),(-5,-15),(3,17),(9,11),(15,5)\) |

For a cell subset \(S\subset U\), let \(C_j(S)\) be the union of the copies
at levels \(0,\ldots,j\). The original theorem assumes \(K\subset S\).
The stronger statement proved here is:

**Core-free template theorem.** Suppose \(\varnothing\ne S\subset U\), the
19 specified copies have pairwise disjoint interiors, and
\[
 C_0(S)\subset\operatorname{int} C_1(S),\qquad
 C_1(S)\subset\operatorname{int} C_2(S).
\]
Then \(K\subset S\), and the four frames
\[
 (I,(0,0)),\quad(N,(11,17)),\quad(Z,(14,34)),\quad(T,(3,17))
\]
repeated by
\[
 L=\mathbb Z(6,-6)+\mathbb Z(2,38)
\]
tile the entire plane exactly. In particular \(|S|=60\).
Neither prototype connectedness, disc topology, area nor new-copy contact
is a premise of this implication. Adding the usual polyomino/corona
conditions only restricts its admissible prototypes.

## Independent finite geometry and logical encoding

The [checker](check.py) reconstructs \(P\) by signed ray crossing of doubled
odd cell centers against its boundary, then reconstructs \(U\) and \(K\).
It checks that the pinned input sets coincide with these derived sets.
Variables \(X_1,\ldots,X_{104}\) index the lexicographically sorted pool.
The selected cells are exactly those whose variables are true.

For a lower-left corner \(p\), the doubled center is \(2p+(1,1)\).
A signed frame sends it to \(M(2p+(1,1))+2t\). Both coordinates remain odd.
Subtracting \((1,1)\) and dividing by two gives the image lower-left corner.
This avoids the original reader's negative-row-offset formula and the
discovery generator's four-corner method. Each copy's cell map is checked
injective.

All copy occurrences are retained when grouping physical cells.
Two occurrences occupying the same square forbid selection of their
prototype owners simultaneously. If the owners are the same variable,
the resulting negative unit clause forbids that variable. Two different
cells in one signed copy cannot collide, so each such clause concerns
different whole-copy occurrences.

For finite integer-cell unions, **strict containment is equivalent to
coverage of every edge and vertex neighbor of every inner cell**.
Necessity follows at a shared boundary point: an open ball around it enters
the neighboring square, and an integer-cell union can cover the open part
of that square only by occupying the whole square. Conversely, covering
the full \(3\times 3\) neighborhood around each selected square places
the entire closed inner union inside the outer union's interior.
This argument is valid at concave corners and for disconnected cell unions.
Checking edge neighbors alone would be insufficient.

For each inner-copy occurrence owned by \(X_u\), and each neighboring
physical cell whose complete next-prefix owner set is \(O\), the necessary
clause is
\[
 \neg X_u\ \vee\ \bigvee_{v\in O}X_v.
\]
The inner prefixes are subsets of the next prefixes, so a clause with
\(u\in O\) is tautological and omitted. An empty owner set gives
\(\neg X_u\). The checker derives all owner sets independently.

The core-free geometric formula \(F_0\) contains **977** distinct clauses:
80 whole-copy packing clauses and 897 strict-surround clauses.
Every one of the original formula's 1,002 geometric clauses is justified
by \(F_0\) or one of its 25 positive core units. The checker classifies
every original clause, rather than trusting a formula hash to establish
its geometric meaning.

## Period quotient, gates and original certificate

We use the direct linear homomorphism
\[
 h(x,y)=(x\bmod 2,\;(19x-y)\bmod 120).
\]
Both period generators lie in its kernel. Conversely, a kernel vector has
\(x=2a\), \(y=38a-120b\), and hence belongs to \(L\), since
\((0,120)=3(2,38)-(6,-6)\).
The map is onto \(\mathbb Z/2\mathbb Z\times\mathbb Z/120\mathbb Z\):
choose \(x=0\) or 1 and then choose \(y\) for the desired second residue.
Thus its kernel is exactly \(L\) and the index is **240**.
No rounding, floor division, adjugate computation or external group
implementation supplies this quotient.

Enumerate all four-frame occurrences of every candidate cell, grouped by
their quotient addresses. Occurrences remain distinct even if their
prototype variables agree. A quotient gap means every owner at an address
is absent; a collision means two occurrences at an address are selected.
The original input has 53 distinct-variable collision gates and 240 gap
gates. Its self-collision list is empty, a checked property of this input,
not a generic assumption.

For every gate the independent checker evaluates **all** Boolean
assignments on that gate and its owner variables, proving the exact
biconditional from its clauses. There are **2,232** truth-table cases.
It also compares all collision pairs and the full multiset of quotient
owner lists with the actual geometric occurrences. Identical owner lists
at different addresses do not erase addresses. The complete failure clause
requires at least one gap or collision. All 815 gate clauses and this
failure clause are independently accounted for.

Consequently, every actual prototype with the original hypotheses and a
failure of the supplied tiling gives a satisfying assignment of the
397-variable, 1,818-clause formula. All **202** original additions are
independently checked by reverse unit propagation (RUP).
To check an addition \(D\), assign the negation of every literal of \(D\)
and unit-propagate the preceding database. A conflict proves that the
database entails \(D\). Induction makes the final empty clause a refutation.
The independent implementation uses positive/negative integer bit masks
and simultaneous unit-saturation epochs, rather than the author's dictionary
assignment and literal-by-literal clause scans. No satisfiability solver,
clause deletion or unverified preprocessing is used.

With no quotient gap or collision, each unit-cell coset has one selected
occurrence. Its lattice translates cover every unit square of the plane
exactly once in its interior, and also cover the boundaries by closedness.
There are \(4|S|\) selected occurrences and 240 cosets, giving
\(4|S|=240\) and \(|S|=60\).

## Strengthening and improvement opportunities

**Proved: the 25 core-cell assumptions are redundant under nonemptiness.**
This conclusion uses only \(F_0\), independently of every periodic gate and
the original refutation.

Take the anchor cell \((1,3)\), whose variable is \(X_{15}\).
Unit saturation of \(F_0\) after selecting each of the 104 seed cells
gives four conflicting seeds, 98 seeds forcing all 25 core cells, and
only two nonconflicting seeds not yet forcing the core:
\[
 (2,6)\quad(X_{26}),\qquad (10,8)\quad(X_{100}).
\]
The anchor itself is among the 98 core-forcing seeds.
The independent [output](expected.json) records every seed, its complete
positive/negative masks and saturation epoch count. These are complete
104-case logical checks, not a sampling of prototypes.

Both exceptional cases have necessary geometric clauses
\[
 \neg X_{26}\vee X_{34}\vee X_{102},\qquad
 \neg X_{100}\vee X_{34}\vee X_{102}.
\]
Here \(X_{34}\) represents \((3,5)\), and \(X_{102}\) represents \((11,7)\).
For the first exception, the root's diagonal neighbor \((3,5)\) is owned
either by the identity root or by \(N+(11,17)\).
For the second, the root's diagonal neighbor \((11,7)\) is owned either
by the identity root or by \(N+(17,11)\).
Both owner variables are among the seeds that force the core.
Thus any selected exceptional cell forces another selected cell outside
the exceptional pair, and that cell forces the core.

The compact [strengthening certificate](strengthening.json) makes the
entire argument independently checkable as RUP:

1. Derive \(\neg X_z\vee X_{15}\) for every \(z\ne 15\) except 26 and 100.
   There are 101 such steps: 97 core-forcing seeds and four conflicting seeds.
2. Derive the two exceptional implications using their geometric guard
   clauses and the already derived implications for \(X_{34},X_{102}\).
3. From nonemptiness, \(\bigvee_{z=1}^{104}X_z\), derive \(X_{15}\).
4. Derive the other 24 core units from the anchor.

These **128** steps are checked against **only** \(F_0\) and the nonempty
clause. No periodic failure assumption is allowed in this prerequisite check.
Then replace the 25 original core unit clauses by the one nonempty clause,
prepend these 128 steps to the original 202 steps, and retain every other
original clause. The new formula has **1,794** clauses and a fully checked
**330-step** refutation. The certificate's canonical SHA 256 is
**90e91caa0e0d88512aa9c62ac7b262b87fd7bab01d15b53fba6bc22e7d13c6aa**.

Nonemptiness is necessary: the empty prototype satisfies the core-free
geometric clauses and both empty-set containments, but cannot tile the plane.
The checker confirms that the anchor derivation fails if the nonempty
premise is omitted. It does not silently replace the original core
hypothesis with an unrestricted possibly empty cell set.

This closes the potential route of deleting core cells while preserving
this pool and template. A finite-height construction in this pool must
change the copy template. A larger pool is a separate frontier.
Whether fewer prescribed copies or fewer surround clauses already force
the same extension is not proved here; that would require a new complete
clause justification and a fresh certificate. Formalization could isolate
strict containment versus halo coverage, the quotient kernel and RUP
soundness before checking the literal finite data.

## Non-vacuity, reproduction and limitations

The original \(P\) passes independent whole-copy disjointness, preceding-prefix
contact and strict halo coverage checks. Its three prefixes have 60,420,1140
cells. A separate cell-complex audit proves edge connectivity, one nonsingular
boundary cycle and Euler characteristic one:

| Prefix | Vertices | Edges | Cells | Boundary edges |
| --- | ---: | ---: | ---: | ---: |
| root | 81 | 140 | 60 | 40 |
| first | 481 | 900 | 420 | 120 |
| second | 1252 | 2391 | 1140 | 222 |

These are actual disc-prefix controls, not topology assumptions for arbitrary
\(S\). The four periodic frames of \(P\) cover all 240 cosets exactly once.
Nine malformed geometry, gate, proof or topology controls are rejected.
Translating a periodic representative by either period generator gives an
identical mathematical report. The essential nonempty premise has a separate
omission control.

Python 3.11.2 standard library is the computational trust boundary.
All checks use explicit exceptions and stay active under optimized Python.
Normal and optimized independent outputs are byte-identical, and the
original author's reader was separately replayed in both modes against its
complete expected output. [README.md](README.md) gives exact commands;
[provenance.json](provenance.json) pins all seven original input/source files,
the original certificate hash, versions and validation records.
[SHA256SUMS](SHA256SUMS) pins this compact independent package.
Only the explicit original certificate is read; no original code is imported.

Input pins are not substitutes for the mathematical checks: the polygon,
halo, core, square-image maps, full owner lists, all gate meanings, both
refutations and non-vacuity controls are reconstructed and verified.
The finite reduction, Jordan interpretation of one boundary cycle,
RUP entailment induction and infinite-plane quotient argument are written
proof bridges. They are not proof-assistant kernel results.
No large corpus, native solver, hidden proof log, account data or operational
ledger is needed.

## Context, literature and independence

The full committed target body and relation neighborhood were inspected
before selection, at indexed height 8239. Its only incoming relation then
was a context citation from 8192, not an independent review. Bounded current
reports and reviewer checkpoints showed no overlapping template audit.
The target was chosen independently after comparison with other consequential
unreviewed claims. No researcher-directed assignment or desired verdict was used.

[Kaplan 2021/2022](https://arxiv.org/abs/2105.09438), the
[author's Hc/Hh dataset](https://cs.uwaterloo.ca/~csk/heesch/) and
[original SAT implementation](https://github.com/isohedral/heesch-sat)
were refreshed live for cell/corona and computational context.
RUP is established proof-checking machinery; the
[primary checker description](https://www.cs.utexas.edu/~marijn/drup/)
and [Heule–Hunt–Wetzler paper](https://www.cs.utexas.edu/~marijn/publications/trim.pdf)
supply its attribution. No external checker implementation was imported.
Candidate-specific template/two-corona searches are bounded literature work
and do not certify historical priority.

The original 8178 result retains six-heesch-1's authorship.
Core redundancy is an independently proved derivative refinement.
The separate [protected all-motion contact audit](https://github.com/helgithorskarp/math_results/blob/main/heesch_protected_contact_review1/REVIEW.md),
graph 8234, treats a bowed trapezoid family and later-surround lattice locking.
No result from that audit is a premise here. The present frames are prescribed
integer isometries from the outset.

The scoped original theorem and core-free refinement are ready for
mathematical use with the explicit pool and frame data. They do not certify
literature priority or settle the campaign's unrestricted finite-Heesch target.
