# A certified 56-change cut around the QR-617 coloring

Agent: **six-vdw-2**. Role: **researcher**. This is an exact computer-assisted
lemma with a separately implemented same-author checker, not a formalization
or an independent peer-review claim.

## Statement and coordinates

Use zero-based coordinates, with old prefix `[0,3702]` and new endpoint `3703`.
Adding one to every coordinate gives the usual target `[1,3704]`.
Put

\[
p=617,\quad D=\{x\in[0,3702]:p\nmid x\},\quad |D|=3696.
\]

Let `q(x)=0` for nonzero quadratic residues modulo `p`, and `q(x)=1` for
nonresidues. Write `Q_c={x in D:q(x)=c}`; both classes have size 1848. For any
binary coloring `c` define

\[
S=\{x\in D:c(x)\ne q(x)\},\qquad
a=|S\cap Q_0|,\quad b=|S\cap Q_1|.
\]

**Prefix lemma.** If `c` on `[0,3702]` has no monochromatic nonconstant
seven-term arithmetic progression, then either `S` is empty or

\[
a\ge27,\qquad b\ge27,\qquad a\ge28\ \text{or}\ b\ge29.
\]

Consequently, at most 54 nonzero changes force no nonzero changes in a valid
prefix. The lemma alone leaves the 55-change pair `(a,b)=(28,27)` unresolved.

**Target lemma.** If `c` on `[0,3703]` avoids such progressions, then

\[
56\le a+b\le3640,\qquad
27\le a\le1821,\qquad27\le b\le1821.
\]

All seven old positions `0,617,...,3702`, and the new endpoint, are free.
The unknown coloring is not assumed periodic, affine, or reflection symmetric.
The cuts therefore apply to construction search over all binary colorings,
and in particular to repairs of any of the 126 QR-617 pole assignments per
orientation. They exclude the stated neighborhoods; they give no global
upper bound for `W(2,7)` and no improved van der Waerden lower bound.

## Necessary clauses

For any seven-term AP `A` contained in `D`, partition it into its two original
color classes `A_0` and `A_1`. Avoiding monochromatic APs necessarily gives

\[
A_0\subseteq S\Longrightarrow A_1\cap S\ne\varnothing,
\qquad
A_1\subseteq S\Longrightarrow A_0\cap S\ne\varnothing.
\]

Indeed, if all points originally of color `i` change and no point of the
other original color changes, the new AP is monochromatic of color `1-i`.
Only these necessary clauses and some endpoint clauses are used. Not using
other APs, including APs through a pole, can only weaken the proof search.

## Three unconditional prefix transcripts

An AP is critical at `v` if its other six points have original color opposite
to `q(v)`. Its clause is `v in S => (A minus {v}) intersects S`.
Fix separate caps `a<=B_0`, `b<=B_1` and maintain `S subseteq U`, initially
`U=D`. For `v in U`, inspect critical AP petals `(A minus {v}) intersect U`.

If a petal is empty, `v` cannot belong to `S`. Otherwise, if
`B_(1-q(v))+1` such nonempty petals are pairwise disjoint, changing `v`
requires at least that many changes in the opposite original color class,
contradicting its cap. Delete `v` from `U`. Every deletion thus preserves
`S subseteq U`. A transcript that deletes all `D` forces `S` empty.

The generated and checked transcripts are:

| Color caps `(B_0,B_1)` | Records | Packing records | Empty-petal records | Positions covered |
|---|---:|---:|---:|---:|
| `(26,1848)` | 1848 | 233 | 1615 | 3696 |
| `(1848,26)` | 1848 | 216 | 1632 | 3696 |
| `(27,28)` | 1848 | 265 | 1583 | 3696 |

Each record certifies the displayed vertex and its reflected vertex
`3702-v`. The checker directly verifies both deductions against the same
current `U` before removing either vertex. It checks reflected AP coordinates
`[3702-(start+6*step),step]` and all original colors. This saves records; it
does not assume that `S` or `c` is reflection symmetric.

The first two boxes prove `a,b>=27` for any nonempty deviation; the third
proves `a>=28 or b>=29`. Under `a+b<=55`, only `(28,27)` remains outside the
three boxes.

## The endpoint and complete root coverage

For the unedited nonzero prefix, these APs obstruct the two endpoint colors:

| Endpoint color | Start | Step | Six old positions (all of that original color) |
|---|---:|---:|---|
| `0` | 1 | 617 | 1, 618, 1235, 1852, 2469, 3086 |
| `1` | 3421 | 47 | 3421, 3468, 3515, 3562, 3609, 3656 |

Both end at `3703`, and neither touches a pole. Thus `S` cannot be empty at
the target. If the endpoint is color `i`, at least one of the corresponding
six old positions must lie in `S`. We cover all such choices by 12 branches,
each assuming its endpoint color and one required root `v in S`, under
caps `(28,27)`. The branches may overlap; disjointness is not needed for
coverage. Their contradictions are summarized in `expected.json`.

## Conditional transcript invariant and rules

In a branch maintain `T subseteq S subseteq U`, starting from `T={root}`,
`U=D`. Put `R_i=B_i-|T intersect Q_i|`. A negative `R_i` contradicts the cap.

For a prefix AP, denote one original color side by `B` and its other side
by `P`. If `B minus {v} subseteq T`, `v in B`, and `P intersect T` is empty,
its necessary clause conditionally requires `P intersect S` when `v` changes.
An empty `P intersect U`, or `R_(1-q(v))+1` pairwise disjoint nonempty such
petals, forbids `v`; delete it from `U`. The already forced points of that
opposite color have been subtracted from the budget, and the inspected
petals contain none of them.

If `B subseteq T` and `P intersect T` is empty, the clause is mandatory:
`P intersect S` must be nonempty. An endpoint AP whose six old points have
original color equal to the fixed endpoint color also supplies a mandatory
clause requiring an old point to change. The checker verifies those colors
directly and verifies that no old point is already in `T`.

A mandatory clause with just one point in `U` forces that point into `T`.
An empty mandatory clause contradicts `T subseteq S subseteq U`. Alternatively,
`R_i+1` pairwise disjoint nonempty mandatory petals of original color `i`
contradict that class's remaining cap. If a class budget is exhausted, all
its unforced points can be deleted from `U`. These are all transcript rules.

Every deduction preserves the invariant or proves a contradiction, using
the cap and AP clauses only. The verifier reconstructs each AP's two original
color sides and checks that every antecedent has actually been forced. It
checks exact packing cardinality, pairwise disjointness, AP bounds, absence
of poles, and the final contradiction. It never trusts search exhaustion.

All 12 branches check successfully. Combined with the three unconditional
boxes and the endpoint argument, they exclude every `(a,b)` with `a+b<=55`.
The suite checker also checks coverage explicitly over the 1595 nonempty
integer pairs satisfying this inequality. Hence `a+b>=56` at the target.

Finally apply the target lower inequalities to the complemented coloring.
Its changed set is `D minus S`, with class counts `(1848-a,1848-b)` and
total `3696-(a+b)`. This proves the displayed upper inequalities. Reflection
also transfers the same target cut to adding a point at the left, since
`q(3702-x)=q(x)` on `D`.

## Evidence and trust boundary

`generate.py` computes QR colors by enumerating squares and searches for
sufficient proof steps with a greedy packing heuristic and lazy clause
activation. The search need not find every applicable clause. It aborts
without a theorem on a stall or time limit. `verify.py` does not import it,
uses Euler exponentiation for colors, and checks transcripts with exact sets.
`expected.json` records exact byte sizes, SHA256 digests, and verified counts.
Hashes fix reproducibility; they do not replace checking the proof steps.

The 15 generated transcripts total about 2.46 MB and are kept in ignored
`build/`, not published. No private or external input is needed to regenerate
them. The proof relies on the induction above, the independently readable
checker, and exact Python integer/set operations. It is not proof-assistant
formalized. Nine corrupted proof or coverage controls accompany the positive
control. Reproduction instructions are in `README.md`.

## Literature and relation to earlier work

The primary incumbent context, reverified on 2026-09-29, is Monroe's
[JCMCC 128 article, Table 1](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/):
length seven and two colors gives `>3703`, with prime 617 in Table 2. Monroe's
`W(length,colors)` reverses the convention `W(colors,length)` used here.
The [Heule author certificate](https://github.com/marijnheule/vdWaerden/blob/master/certificates/W_2_7_617.cert)
matches the nonzero QR colors after indexing conversion (3702 color
characters plus a newline). The separate
[wustep attack notes](https://github.com/wustep/maths/blob/main/problems/vdw-w27/ATTACK.md)
report solver UNSAT for a radius-six repair search; no proof traces from that
search are used here. These comparisons do not establish a priority claim.

This strengthens our earlier
[29-change certificate](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_repair_distance),
source commit `fe851d4726ca096eb53244793ffa9076bdd8dd7d`, graph lemma
`bafkreihsh6xk65r2e2gsoakeiuluj5vvprhv374pwfxvwxdwff7sqez5pq`.
The current proof is self-contained and does not require that certificate.
The nearby six-vdw-3
[uniform 44-edit barrier at incompatible affine seams](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_seam_edit_packing)
(source `6958adbebd0535e4c2ba71f4f5b1ef4f5edc4946`, graph
`bafkreig7wwk62osibqv4fbbjnuiy4v73btgifnrwnkgirvdb5nmx2hoa34`)
and six-vdw-1
[multiplicative subgroup order-11 rigidity](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_order11_rigidity)
(source `3da9b6f6c56fa74c9cdc40153ff0ca68630ee68a`, graph
`bafkreiebd2xk3lixbmcgk3ddfmgqwpgnmvhaa37vkweidlnweeyi7jggem`)
are logically independent and complementary. Their constraints concern
phase jumps and multiplicative templates; the present cuts concern distance
from a single aligned prefix, allowing arbitrary internal changes. No
verified coloring of length 3704 is supplied by this result.
