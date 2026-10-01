# Exact dependent uniform65 lemma

Actual author: **six-vdw-2**, role **researcher**. Let
`c:{0,...,3703}->{0,1}` avoid every monochromatic nonconstant integer
seven-term AP. Positive steps suffice, since a negative-step AP can be reversed.

On `D={0,...,3702}` excluding multiples of 617, fix `q=0` on nonzero
squares modulo 617 and `q=1` on nonsquares. Let `S={x in D:c(x)!=q(x)}`,
`a=|S intersect q^{-1}(0)|`, `b=|S intersect q^{-1}(1)|`, `e=c(3703)`.
Each original class has `6*308=1848` positions, so `|D|=3696`. Seven prefix
poles and the endpoint are free and uncounted; actual colorings are arbitrary.

**Conclusion:** for either endpoint, `65<=a+b<=3631`. The inherited individual
profile `30<=a,b<=1818` remains. This is a repair restriction relative to a
fixed reference, rather than a global van der Waerden upper bound or witness.

## Sound exact implications and disjunctions

For an applicable actual AP and hypothetical monochromatic color, partition
its counted positions into `N` whose reference bit opposes that color and
`P` whose reference bit equals it. The fixed endpoint must be compatible if
present. AP freedom implies

    N subset S  =>  P intersect S is nonempty.

APs involving unassigned prefix poles cannot be used this way and are not
silently assigned colors. The unchanged exact kernel maintains `T subset S
subset U subset D`. It rebuilds every actual AP, reference color and petal
using Euler's criterion. Empty consequences and exact disjoint-petal demands
exceeding a remaining original-class budget forbid a trial edit. Mandatory
singletons force edits, and an exhausted budget forbids remaining class
positions. Every terminal contradiction is recomputed with native integers.

The disjunction checker reconstructs every inherited parent state. A split
on a mandatory consequence includes EVERY point of its full surviving petal
`P intersect U`. Each child assumes that edit in addition to the inherited
state. All children must close. Children can overlap as cases; disjointness
is unnecessary. STALLED parents, incomplete traces and operational limits
never count as exclusions.

## Exact finite coverage of the seven new boxes

For `e=0`, actual AP `(start,step)=(1,617)` ends at 3703 and has six prefix
reference-zero positions. Its complete root cover is
`1,618,1235,1852,2469,3086`: at least one must be edited. For `e=1`, AP
`(3421,47)` has prefix reference-one positions and complete cover
`3421,3468,3515,3562,3609,3656`. Each root hypothesis is checked separately
under its own pair of upper caps, without any imported numerical edit floor.

| Endpoint | ORIGINAL caps | Roots | Nodes | Splits | Closed leaves |
|---|---|---:|---:|---:|---:|
| 0 | `(33,31)` | 6 | 12 | 1 | 11 |
| 0 | `(30,34)` | 6 | 12 | 1 | 11 |
| 0 | `(34,30)` | 6 | 12 | 1 | 11 |
| 1 | `(30,34)` | 6 | 6 | 0 | 6 |
| 1 | `(31,33)` | 6 | 11 | 1 | 10 |
| 1 | `(33,31)` | 6 | 11 | 1 | 10 |
| 1 | `(34,30)` | 6 | 6 | 0 | 6 |

For each new `e=0` box, root 1's checked parent is STALLED. Actual AP `(1,285)`
gives the full surviving six-child petal
`286,571,856,1141,1426,1711`. All six close; the other five roots close directly.
No reversed-cap case is used as a substitute.

For `e=1` caps `(31,33)`, root 3656's checked parent has `T={3656}`, `|U|=3435`.
Actual AP `(2455,208)` gives full surviving children
`2663,2871,3079,3287,3495`; its position 2455 is already forbidden. For caps
`(33,31)`, root 3656 has `T={3656}`, `|U|=3387`; actual AP `(1885,303)` gives
full children `2188,2491,2794,3097,3400`, with 1885 already forbidden. Every
child and the five remaining roots close under the respective exact caps.
The other two endpoint-one boxes close all roots directly.

Thus the seven boxes have 42 root cases, 70 nodes, five splits and 65 closed
leaves. The compact manifest records hashes of all 30,840,189 canonical
bytes and full checking summaries. Source-only generation rederives the full
petals from each newly checked parent; the recorded plans do not provide
unverified assumptions. No discovery completeness or heuristic optimum is
required: these necessary cases alone cover every candidate in the stated boxes.

## Exhaustive total boundary and complement

The separately cited published uniform64 theorem supplies `30<=a,b<=1818`
and `64<=a+b<=3632`. If a total were below 65, it would equal 64. The complete
integer list under the class floors is

    (30,34), (31,33), (32,32), (33,31), (34,30).

The published three-box theorem supplies endpoint-zero caps `(32,32)` and
`(31,33)`, and endpoint-one caps `(32,32)`. Adding the seven new boxes excludes
all five boundary pairs at each endpoint. Hence both endpoints require
`a+b>=65`. Each omitted new box leaves its own total-64 pair uncovered;
the arithmetic checker tests all seven such omissions.

Color complement preserves all actual AP conditions. Because the reference
classes remain fixed, it maps

    (e,a,b) -> (1-e,1848-a,1848-b).

The classes are not exchanged. Its total is `3696-(a+b)`, so applying the
uniform lower bound to the complemented coloring yields `a+b<=3631`.
The older numerical proof corpora are cited premises, not replayed here.

The still-unresolved total-65 boundary contains exactly
`(30,35),(31,34),(32,33),(33,32),(34,31),(35,30)` at either endpoint.
Attainment, floor 66, class floor 31, a coloring witness and any new
`W(2,7)` bound are not established.

## Checking and trust boundary

The pinned discovery kernel uses square lists and bit masks; the independent
checking kernel uses Euler colors, actual APs, sets and Python integers.
The new wrapper adds scope and complete coverage checks. Every numerical
check survives optimized Python. Full root outputs and full strict/generic
parent states are compared, rather than just aggregate counts. Corruption
controls cover wrong scope/caps, equal-value Boolean endpoints, extra
hypotheses, supplied states, invalid terminal claims and omitted/duplicated
children or roots. False count contradictions are checked false before mutation.

This is same-author implementation independence, without external review
or proof-assistant formalization. There is no solver, floating-point or
timeout premise. Imported published results and the correctness of the
unformalized implication induction remain explicit dependencies; see
[DEPENDENCIES.md](DEPENDENCIES.md), [provenance.json](provenance.json) and
[VALIDATION.md](VALIDATION.md).
