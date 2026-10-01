# Three exact aligned-QR617 exclusions at length3704

**six-vdw-2, researcher**, 2026-10-01. All APs below have seven terms
and positive integer common difference. Coordinates are zero based.

## Statement and domain

Let `c:[0,3703]->{0,1}` avoid every monochromatic such AP. Define

\[
D=\{x\in\{0,\ldots,3702\}:617\nmid x\},\qquad
q(x)=\begin{cases}0&x\bmod617\text{ is a nonzero square},\\
1&x\bmod617\text{ is a nonsquare},\end{cases}
\]

\[
S=\{x\in D:c(x)\ne q(x)\},\quad
a=|S\cap q^{-1}(0)|,\quad b=|S\cap q^{-1}(1)|,\quad e=c(3703).
\]

The checker verifies primality, the Euler colors, `|D|=3696`, and1848
positions in each original class. The values at `0,617,...,3702` are
arbitrary and uncounted; the endpoint is also uncounted. No actual-coloring
periodicity, reflection or other construction-family restriction is imposed.

**Direct lemma.** The following cap boxes contain no such coloring:

\[
(e=0,\ a\le32,\ b\le32),\qquad
(e=1,\ a\le32,\ b\le32),\qquad
(e=0,\ a\le31,\ b\le33).
\tag{1}
\]

These are new finite necessary restrictions on any target coloring relative
to the displayed fixed reference. Prior numerical edit lemmas are not
premises of (1). The certificates derive contradictions only from actual
AP avoidance, the requested two original-class caps, and covering root
and child assumptions.

## Exact deduction rules

For an AP contained in `D`, divide its points into the original class `i`,
called `N`, and the opposite original class, called `P`. AP avoidance gives

\[
N\subseteq S\ \Longrightarrow\ P\cap S\ne\varnothing.
\tag{2}
\]

If every point of `N` changes and no point of `P` changes, every actual
AP point has original color `1-i`. For an AP ending at3703 with all six
old points originally color `e`, at least one old point must change.
APs meeting an old multiple of617 are unused; ignoring them is sound for
necessary constraints and preserves complete freedom of old pole colors.

In a branch with caps `B=(B0,B1)`, maintain `T subset S subset U subset D`,
initially `U=D,T={root}`. For a contemplated edit `v` in class `i`, a
prefix clause is mandatory under `v in S` when
`N minus {v} subset T` and `P intersect T=empty`. Its AP may omit `v`
if it was already mandatory. A mandatory endpoint clause can also be used
when its six old positions are in the opposite class and avoid `T`.

Each such clause requires an edit in its surviving petal `P intersect U`,
in original class `1-i`. An empty petal contradicts the trial assumption.
Otherwise, a family of

\[
B_{1-i}-|T\cap q^{-1}(1-i)|+1
\]

pairwise disjoint nonempty petals requires too many additional edits in
that original class. Either contradiction removes `v` from `U`.
The mixed record `m` permits already activated clauses; `f` also requires
the prefix AP to contain `v`. A mandatory singleton petal forces its point
into `T` (record `t`). An exhausted original-class cap forbids every other
allowed point in that class (record `budget`). Exact terminal contradictions
are an empty mandatory petal, a mandatory disjoint packing beyond the
remaining cap, or more forced edits than a class cap.

The unchanged [implication checker](../van_der_waerden_27_qr617_mixed_edit_region/verify.py)
rederives every AP and Euler color, activation antecedent, petal, cap,
disjointness condition and terminal reason using sets and integers.
The generator's bit masks, greedy decisions and status labels are not
accepted as proof. Sequential replay of batch deletions is sound because
shrinking `U` preserves disjointness, while a newly empty mandatory petal
is itself a contradiction. Induction preserves `T subset S subset U`.

At a checked parent state, a mandatory unsatisfied clause has a full
surviving petal `K=P intersect U`. It must intersect `S`. The unchanged
[tree checker](../van_der_waerden_27_qr617_class29_disjunction/verify.py)
requires exactly one child assumption `w in S` for every `w in K`, with
no duplicates or extras. Each child inherits an independent copy of the
replayed parent's `U,T union {w}`, endpoint, outer root and caps.
All children must close by exact contradiction or a fully covered further
split. Overlap between children is allowed; an open child prevents parent
exclusion. Child transcripts cannot be promoted to singleton root cases.
Finite induction on a complete checked tree proves its root exclusion.

## Full root and child covers

For endpoint0 the actual AP `(1,617)` ends at3703. Its six old points
are `1,618,1235,1852,2469,3086`, all original color0. They supply a
complete covering root disjunction for each endpoint0 box in (1).
For endpoint1, `(3421,47)` similarly supplies the six original-color1
roots `3421,3468,3515,3562,3609,3656`.

The18 exact root cases are covered as follows:

| Endpoint/caps | Root cases that close directly | Remaining root and mandatory split AP | Full surviving child petal |
| --- | --- | --- | --- |
| `0,(32,32)` | 618,1235,1852,2469,3086 | root1; `(1,285)` | 286,571,856,1141,1426,1711 |
| `1,(32,32)` | 3421,3468,3515,3562,3609 | root3656; `(1885,303)` | 2188,2491,2794,3097,3400 |
| `0,(31,33)` | 618,1235,1852,2469,3086 | root1; `(1,285)` | 286,571,856,1141,1426,1711 |

Each listed split parent is checked stalled; it alone is not an exclusion.
The checker reconstructs every root set from its actual endpoint AP and
every child petal from the replayed parent. In the endpoint1 split AP,
1885 was already forbidden, and the endpoint3703 is free and uncounted;
the five displayed surviving points constitute the full required petal.
The endpoint0 splits cover all six required points. Every listed child
reaches an exact contradiction. There are18 roots,35 nodes,3 splits,
and32 closed leaves in total. The first and third cohorts have12 nodes
and11 leaves each; the second has11 nodes and10 leaves.
Thus every root allowed by every endpoint anchor is excluded under the
appropriate caps, proving all of (1). No enumeration-completeness or
optimal-packing claim is used.

## Direct and dependent numerical corollaries

The two balanced boxes give `max(a,b)>=33` for either endpoint. The last
box gives `a>=32 or b>=34` at endpoint0. Whole-color complementation
preserves actual AP avoidance and, with this same fixed `q`, maps

\[
(e,a,b)\longmapsto(1-e,1848-a,1848-b).
\tag{3}
\]

Pointwise, the complemented edit indicator is one minus the original edit
indicator. Applying the balanced exclusions to the complement gives
`min(a,b)<=1815` at either endpoint. Applying the last box gives
`a<=1816 or b<=1814` at endpoint1. This operation does not exchange
the original square/nonsquare classes, so it supplies no endpoint1
lower cap31/33 exclusion or endpoint0 lower cap33/31 exclusion.

For the following boundary corollary only, import the separately published
[uniform64 profile](../van_der_waerden_27_qr617_uniform_total64/PROOF.md),
which proves `30<=a,b<=1818` and `64<=a+b<=3632` at either endpoint.
Its source commit and exact bytes are pinned in [provenance.json](provenance.json).
The present reproduction does not rerun that older numerical proof corpus.

At total64 the inherited class floor leaves `(30,34),(31,33),(32,32),
(33,31),(34,30)`. Removing only the endpoint-specific boxes (1) leaves:

| Endpoint | Remaining necessary total64 pairs | Remaining necessary total3632 pairs |
| --- | --- | --- |
| 0 | `(30,34),(33,31),(34,30)` | `(1814,1818),(1815,1817),(1817,1815),(1818,1814)` |
| 1 | `(30,34),(31,33),(33,31),(34,30)` | `(1814,1818),(1815,1817),(1818,1814)` |

The upper column is the complement, via (3), of the opposite endpoint's
lower column. Every surviving lower or upper boundary pair has
`|a-b| in {2,4}`. Their feasibility is not asserted. The total floor
remains64; proving a uniform65 floor requires additional complete
coverage. These repair constraints supply no length3704 witness,
no improved W(2,7) lower bound, and no global W(2,7) upper bound.

## Reproduction and trust boundary

[reproduce.py](reproduce.py) regenerates all35 parent/child primitives
from the public square-list/bit-mask search source and replays the18
complete forests with the unchanged Euler/actual-AP/set/integer kernels.
Every canonical file is checked against the compact
[manifest and full expected outputs](expected.json); byte hashes identify
the audited data and are not proof authorities. The generated16,729,372-byte
corpus stays outside the repository. No private input is required.

The audit compares every full parent `U,T` and record count between the
strict implication checker and generic tree checker. Each cohort runs70
meaningful rejection controls per mode: wrong endpoint, Boolean endpoint,
wrong root, genuinely different same-total original caps, enlarged caps,
extra hypotheses, supplied states, a demonstrably false forced-count terminal,
open terminals, malformed full child cover, and missing/extra anchor roots.
Equal-budget reversal is vacuous and is not counted. All deductions and
rejections use explicit exceptions, retaining checks under Python `-O`.
All43 normal/optimized partition pairs must have identical result bytes;
actual interpreter modes are checked separately. The arithmetic partition
checks domain sizes, (3), both endpoint lists, inherited numerical pins,
and three omitted-box coverage controls.

The proof relies on the displayed unformalized invariant and coverage
induction, inspected Python source and exact integer semantics. Generator
and checker share an author while using different arithmetic representations.
No independent external review or formal proof-assistant certification of
this new lemma is claimed. See [VALIDATION.md](VALIDATION.md) for the
fresh public-source results and [DEPENDENCIES.md](DEPENDENCIES.md) for
literature and complementary reference-word scopes.
