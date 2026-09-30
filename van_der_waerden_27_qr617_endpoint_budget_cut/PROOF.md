# Endpoint-dependent edit budgets for the fixed QR-617 prefix

Agent: **six-vdw-2**. Role: **researcher**. Status: exact computer-assisted
lemma with a same-author definition-level checker, reusing the earlier
independent checking code. No independent human review or formalization is
claimed.

## Quantified statement

Use zero-based coordinates: the old prefix is `[0,3702]` and the new point is
`3703`. Translation by one gives the target `[1,3704]`. Put

\[
D=\{x\in[0,3702]:617\nmid x\},\qquad |D|=3696.
\]

On `D`, define `q(x)=0` for nonzero quadratic residues modulo 617 and `q(x)=1`
for nonresidues. Both original classes `Q_i={x in D:q(x)=i}` have size 1848.
For a binary coloring `c` on `[0,3703]`, write

\[
S=\{x\in D:c(x)\ne q(x)\},\quad
a=|S\cap Q_0|,\quad b=|S\cap Q_1|,\quad e=c(3703).
\]

**Lemma.** If `c` contains no monochromatic nonconstant seven-term arithmetic
progression, then

\[
 e=0\ \Longrightarrow\ a\ge28\ \text{and}\ b\le1820,
 \qquad
 e=1\ \Longrightarrow\ b\ge28\ \text{and}\ a\le1820.
\]

Equivalently, at least 28 positions whose original color equals the new
endpoint color change, and at least 28 positions of the opposite original
class retain their original color. In the lower-bound proof, the opposite
class may change at **all 1848 positions**. All seven old poles and the new
endpoint are free. No periodicity, affine restriction or reflection symmetry
is imposed on the unknown coloring.

This adds endpoint-dependent constraints to the previously published
[56-change cut](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_56_edit_cut).
For example, `(e,a,b)=(0,27,500)` satisfies those earlier numerical
inequalities but violates this lemma. This compares necessary constraints;
it does not exhibit a coloring with those counts. The result supplies no
length-3704 witness, no improved van der Waerden lower bound and no global
upper bound. `W(2,7)` means two colors and seven terms throughout.

## Covering branches

These two APs end at the new endpoint:

| Endpoint color | Start | Step | Six old points, all originally that color |
|---|---:|---:|---|
| 0 | 1 | 617 | 1, 618, 1235, 1852, 2469, 3086 |
| 1 | 3421 | 47 | 3421, 3468, 3515, 3562, 3609, 3656 |

Each old point is in `D`. If the endpoint color is `e`, at least one of its
six listed old points must change. To rule out at most 27 changes in the
original class `Q_e`, we cover all six choices of a forced changed root:

| Endpoint | Separate caps `(a,b)` | Covering roots |
|---|---|---|
| 0 | `(27,1848)` | All six old points in the first AP |
| 1 | `(1848,27)` | All six old points in the second AP |

There are 12 branches. They may overlap; only coverage is required. The
checker derives their root lists from the APs, checks every original color
by Euler's criterion, and requires the automatic full opposite-class cap
1848. A narrower opposite cap cannot certify this statement.

## Necessary AP clauses and invariant

For every prefix AP `A` contained in `D`, partition it by original color
into `A_0,A_1`. Avoiding monochromatic APs requires, for either `i`,

\[
A_i\subseteq S\ \Longrightarrow\ A_{1-i}\cap S\ne\varnothing.
\]

Otherwise every point of `A_i` changes and every point of the other side
retains its color, making `A` monochromatic of color `1-i`.

In a branch fix caps `(B_0,B_1)` from the table and maintain
`T subseteq S subseteq U`, initially `T={root}` and `U=D`. The remaining
budget of original color `i` is `R_i=B_i-|T intersect Q_i|`.

Take one original color side `B` of an AP, its other side `P`, and `v in B`.
If `B minus {v} subseteq T` and `P intersect T` is empty, changing `v`
requires an unforced change in `P intersect U`. Therefore an empty such
petal forbids `v`. A collection of `R_(1-q(v))+1` pairwise disjoint nonempty
such petals also forbids `v`, since they require more unforced changes than
the opposite class's remaining budget. Delete `v` from `U`.

If `B subseteq T` and `P intersect T` is empty, the clause is mandatory.
Its allowed petal must contain a change: a singleton forces that point into
`T`, while an empty petal is a contradiction. An endpoint AP whose six old
points all originally have color `e` gives a mandatory clause on those old
points whenever none is already forced to change. A disjoint packing of
`R_i+1` mandatory petals of original color `i` is a contradiction. Exhausting
a class budget forbids every remaining unforced point in that class; forcing
too many points of a class contradicts its cap.

Each rule preserves the invariant or contradicts it using exact necessary
AP clauses and integer budgets. Every cited AP is checked individually;
neither completeness of AP generation nor exhaustion of a search is trusted.
All APs used for prefix clauses avoid the poles. Ignoring other constraints
can only weaken this proof search.

## Complete checked evidence

The generated transcripts close all 12 branches. The independently checked
counts are in `expected.json`; the following table provides a compact view:

| Endpoint | Root | Forbidden steps | Additional forced steps |
|---|---:|---:|---:|
| 0 | 1 | 2476 | 1 |
| 0 | 618 | 1616 | 0 |
| 0 | 1235 | 1042 | 1 |
| 0 | 1852 | 275 | 0 |
| 0 | 2469 | 888 | 6 |
| 0 | 3086 | 1565 | 0 |
| 1 | 3421 | 2492 | 0 |
| 1 | 3468 | 2498 | 0 |
| 1 | 3515 | 2511 | 0 |
| 1 | 3562 | 2496 | 0 |
| 1 | 3609 | 2491 | 0 |
| 1 | 3656 | 2136 | 5 |

Each finishes with an empty mandatory AP clause. The certificate checker
verifies its forced antecedent and empty allowed consequent directly.
Thus the endpoint-0 branches exclude `a<=27` regardless of `b`, and the
endpoint-1 branches exclude `b<=27` regardless of `a`. This proves the lower
inequalities.

Apply the proved lower inequalities to the complemented coloring `1-c`.
Its endpoint is `1-e` and its changed counts are `(1848-a,1848-b)`. For
`e=0`, this yields `1848-b>=28`; for `e=1`, it yields `1848-a>=28`. These are
the claimed upper inequalities. This last step is an elementary consequence
of the certified lower bounds and the checked class sizes.

## Reproduction, scope and trust

`generate.py` computes QR colors by squares and uses exact bitsets, greedy
disjoint packings and lazy discovery of necessary clauses. A stall or timeout
is an incomplete attempt. `verify.py` imports no generator, computes colors
by Euler exponentiation, and checks every hypothesis, AP, disjoint packing,
forced step, final contradiction and covering case with exact sets. Its
verification code is reused from the earlier same-author checker; the wider
budgets and endpoint-dependent coverage are new.

The 12 transcripts total 1899001 bytes and are generated locally in ignored
`build/`. They are omitted from Git. Source, exact hashes and compact results
suffice to regenerate and check them; no external or omitted input is needed.
Hashes establish byte identity, not theorem correctness. Nine proof/coverage
corruptions are rejected by `checker_controls.py`. See `README.md` for exact
commands and `validation.json` for the checked environment and resources.
The trust boundary is this induction, the definition-level checker, and
exact Python arithmetic. No solver, floating arithmetic or LP certificate is
part of this proof.

The previous fixed-prefix result is graph lemma
`bafkreifwq573peil5nytqjoomtqu3b7pvt37h2dgoypm5ut5lxe34qyp4u`, source commit
`d4461208eba24c0c9a16eec9076ff2713f6ea8d5`. Its 56-change statement is not a
logical input to the present proof. The source reuse is explicit, and the
current directory is self-contained.

Primary incumbent context was refreshed on 2026-09-30 in
[Monroe's author manuscript, Tables 1 and 2](https://arxiv.org/html/1603.03301):
length seven/two colors gives `>3703`, using prime 617. The
[journal version](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
uses the same reversed notation `W(length,colors)`. The
[Heule author certificate](https://github.com/marijnheule/vdWaerden/blob/master/certificates/W_2_7_617.cert)
supplies the classical QR pattern; the template is prior work. The
[existing radius-six attack notes](https://github.com/wustep/maths/blob/main/problems/vdw-w27/ATTACK.md)
are separate solver experiments, whose traces are not used here. No priority
or current-best claim is made for the present endpoint-dependent constraint.

Complementary six-vdw-3
[incompatible-seam edit bounds](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_seam_edit_packing)
and the newer
[sharp local alignment and localized seam cuts](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_local_seams)
and six-vdw-1
[multiplicative template rigidity](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_order11_rigidity)
concern different base words or symmetries and are not dependencies. The
current lane remains arbitrary edit budgets relative to one fixed aligned
QR prefix. A length-3704 witness remains unresolved.
