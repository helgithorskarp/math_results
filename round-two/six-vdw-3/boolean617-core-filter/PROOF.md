# Exact 3703 cap for constant-phase Boolean617 character templates

Actual author: **six-vdw-3**, role **researcher**, 2026-10-02. This is an
author-checked finite structural theorem. The separate exact checkers use
different algorithms from the producers; they are not an independent person,
external review or formal proof.

Let (L:\mathbb F_{617}^{*}\to\{0,1\}) be zero on nonzero squares and one on
nonsquares. Its value at zero is **undefined**. An affine character input is

\[
L(a_i n+b_i),\qquad a_i\ne0,
\]

where integer arguments are reduced modulo617. Take at most three such inputs,
an arbitrary Boolean function of them, and any global color complement. Let

\[
R=\{-b_i/a_i\}
\]

be the union of **all original roots**, including those of ignored inputs.
At every integer position whose residue is in R, the color is arbitrary,
independently of every other position. At every other position the color is the
specified Boolean function of the affine characters. The function and palette
are constant across all rows: there is no row-dependent phase. There are no
additional edited nonroot columns or positions.

**Theorem.** No coloring in this family is seven-term-AP-free on [1,3704].
There is such a coloring on [1,3703]. Thus the largest AP-free interval in this
family has length **3703**.

The attained length3703 is the known Rabung/617 lower bound. This theorem does
not provide a length3704 witness, improve the numerical lower bound, or determine
the unrestricted (W(2,7)\). The scope permits arbitrary truth rules, repeated
inputs, nonsquare affine coefficients, ignored inputs, and independently free
root occurrences; it does not permit an extra edited column or a nonconstant
phase.

## 1. Two forced free columns and a necessary field test

The actual integer progressions

\[
1,618,1235,1852,2469,3086,3703
\]
\[
2,619,1236,1853,2470,3087,3704
\]

have constant residues1 and2. A regular column has one constant color in this
family. Therefore an AP-free coloring must have **1,2 in R**. Families with at
most one distinct original root are immediately excluded. With two roots we
have R={1,2}; with three roots R={1,2,t}, t notin{1,2}.

Any root-avoiding monochromatic nonzero-step field AP can be reversed so its
step is an integer in [1,308]. Choose its first residue as an integer in [1,617],
using617 for residue0. It then lifts to an ordinary AP ending at most

\[
617+6\cdot308=2465.
\]

Every lifted point avoids every original root. Its color is fixed by the same
field rule. An AP-free coloring on [1,3704] must consequently have an AP-free
**regular cyclic617 core**. This necessary test does not assert that a field
completion exists or that affine field maps preserve the whole interval.

## 2. Exact classification of the regular three-root core

On a regular point, multiplicativity gives

\[
L(a_i(n-r_i))=L(a_i)\mathbin{\oplus}L(n-r_i).
\]

The coefficient bits can be absorbed into an arbitrary Boolean function. After
an affine field change of coordinate and root relabeling, three distinct roots
are0,1,t with t in{2,...,616}. A global color complement lets us gauge F(000)=0.
Using argument index b0+2b1+4b2, the complete gauged truth domain is the128 even
words0,2,...,254. All three roots remain free, even if F ignores one or two
inputs.

**Finite core lemma.** For every normalized third root t, the only such truth
words with no regular monochromatic seven-term field AP are

\[
170=\mathtt{0xaa},\quad204=\mathtt{0xcc},\quad240=\mathtt{0xf0}.
\]

These are precisely F(b)=b0,b1,b2. Undoing coefficient absorption and the output
gauge, a regular core that passes the test is a single affine quadratic
character, possibly complemented. The other original roots are still free.

The finite proof has the following exact, reproducible components.

**Root geometry coverage.** The six normalized images of a triple arise by
choosing an ordered pair of its roots to become0,1. In the producer this is the
six root permutations. Independently, the checker closes t under t->1-t and
t->1/t by breadth-first search. The615 third-root values form103 components:
102 of size6 and one harmonic component of size3. We check **all128 rules** at
each geometry representative, including redundant harmonic rules. The tested
canonical domain is therefore **13184 states**, not the smaller joint
root-and-truth quotient13136. Neither count quotients the physical interval.

For roots r=(0,1,t), a chosen root order pi, and delta=r[pi1]-r[pi0], put

\[
y=(x-r[\pi_0])/\delta,\qquad
u=(r[\pi_2]-r[\pi_0])/\delta.
\]

The normalized character vector satisfies

\[
L(y-s_i)=L(x-r[\pi_i])\mathbin{\oplus}L(\delta),
\quad s=(0,1,u).
\]

Thus root permutations induce coordinate permutations and a common input-bit
complement. The arbitrary truth table is transported as a whole and gauged by
its new value at000. This is a bijection of the128 globally complemented truth
classes and preserves monochromatic root-avoiding APs.

**Complete canonical AP enumeration.** At each representative, enumerate
a=0,...,616 and d=1,...,308: **190036 pairs**. Reversal covers the remaining
nonzero field steps. A seven-term AP meeting a root is discarded for this
necessary test. At each remaining point record the three character bits.
The set of the seven argument labels determines which truth rules are
monochromatic. The producer uses Euler powers and a255-entry label-set mask
library. The independent checker constructs the character by an explicit
square set, then intersects literal truth-bit columns for the seven points.
It reproduces every AP-domain histogram and every ordered per-AP transcript;
it also directly checks all recorded positive witnesses and all1330252
reversal-coordinate identities at every canonical geometry.

Both methods find exactly125 blocked rules and the three projections at
**every** representative. Across103 geometries the checker replays
**19573708** start/step pairs and refutes12875 canonical truth states.

**All raw states.** The independent geometry checker validates1132830 actual
character-coordinate identities and629760 abstract truth entries. It transports
the canonical positive APs back to all615 original normalized triples, reversing
their steps when needed. It literally checks a root-avoiding monochromatic AP
for each of **76875 nonprojection raw states**, totaling538125 witness points.
The remaining **1845 states**, three per third-root value, are exactly the
single-input rules. No absent greedy witness or incomplete solver search is
used in this classification.

The ordered raw positive-witness transcript SHA256 is
`5635e83f766a5b6be13af67c1bdc46a31a53cb367b179514f76b62e757e27eab`.

## 3. Refuting every surviving projection on the actual interval

Return to the physical roots R={1,2,t}, t notin{1,2}. The field lemma permits
only the regular color L(n-r) for r in{1,2,t}, or its global complement. A global
complement bijects completions, so take the uncomplemented color. There are
exactly **615*3=1845** physical projection cases. All20 original-root integer
positions are still arbitrary; no root consistency or reflection invariance
is imposed.

For each case, the source supplies a column q in{1,2}, q different from r.
For **each** of its seven actual points m=q+j*617, it supplies an ordinary
seven-term AP containing m and having six other points outside **all three**
root columns. The six fixed colors are all

\[
1-L(q-r).
\]

Avoiding this AP forces c(m)=L(q-r). The seven demands therefore force all
seven points in column q to the same color, contradicting its vertical AP.
This is an ordinary implication proof with seven positive APs, independent of
the colors assigned to any other original-root position.

The unit producer searches actual interval starts, slots and positive steps;
the independent checker recomputes every color using its own square-set oracle
and checks bounds, nonconstant steps, target-point identity, root avoidance,
the six fixed opposing colors, exact case coverage and the vertical AP.
It refutes **all1845 cases**, using **12915 literal unit APs**,77490 fixed
support points and12915 vertical-AP points. The complete range is split into
contiguous16-third-root batches, with a final9-value batch. Missing certificates
would be explicitly incomplete; there are none.

This part uses the actual positions1,...,3704. No affine field symmetry is
silently applied to the interval or its independent root variables.

The whole interval source-and-checker record commitment is
`d90b74c121549ca480f76e77f5a0841dea42d3e23be2150ed98ce674591623d5`.

## 4. Repeated roots, fewer inputs and attainment

Repeated affine roots give input bits differing only by coefficient constants;
absorbing those constants yields an arbitrary function on the distinct
character inputs, without releasing any original root. At most one distinct
root was excluded by the two vertical APs.

With two distinct roots1,2, adjoin the third root0 as an **ignored** character
input and allow its six positions to be freely colored. This enlarges the
completion family. The three-root proof includes t=0 and therefore excludes
the original two-root family as well. No separate assertion about a two-root
physical field quotient is needed.

For attainment at the known endpoint3703, let c(1)=1 and, for n>1, set c(n)=0
if (n-1)%617 is zero or a nonzero square, and c(n)=1 otherwise. This is a
one-input member of the stated family: its original root column1 is free and
is not monochromatic. The seed source independently reconstructs these colors
with Euler powers and a square set. A literal integer checker examines all
**1140833** nonconstant seven-term APs in [1,3703] and finds none monochromatic.
The ASCII bit-string SHA256 is
`8403d5fd5c640f9fab958d78e958194cb69baf62923616a4e6767d574f0e1e8f`.
This reproduces the historical bound, not a new numerical result. Restricting
any longer member of the same template family to [1,3704] preserves its
definition, so the family maximum is exactly3703.

## 5. Reproduction, trust, literature and dependencies

From the repository root, with CPython3.11.2 standard library:

```sh
python3 round-two/six-vdw-3/boolean617-core-filter/reproduce.py --work /tmp/boolean617-fresh
```

Use a new empty work directory. The wrapper verifies [source pins](SOURCE_PINS.json),
rebuilds all certificates, runs every independent checker, compares **whole**
normal/`-O` records, rejects22 witness/domain/coverage damages in each mode, and
checks both complete merges against [expected.json](expected.json). Mathematical
children are serial, numerical threads1, each fixed at20s. Generated full
per-geometry records and unit witnesses are local outputs, omitted from public
source; they are regenerated with no external input.

The compact final record states scope as well as counts. Its status is an exact
cap for this family. It does not encode a conclusion about arbitrary binary
colorings, nonconstant phase words, a fourth character input, or extra edited
columns. The complete canonical source/checker record commitment is
`11f5405456ec1816f1551bcc20d266115977e0aa1e97ec4f383e415583b17e2d`.
Trust includes CPython exact integers, file decoding and the ordinary
unformalized normalization, multiplicativity, reversal, lifting, unit-demand
and restriction arguments. Neither source publication nor a shared signature
is independent review. No native solver, timeout, UNKNOWN or incomplete
enumeration supplies a negative premise.

[Monroe, *New lower bounds for Van der Waerden numbers using distributed computing*](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
gives Table1 length7/two colors >3703, Table2 prime617, and Section2 the
Rabung construction. Its W(7,2) uses length-first order; the campaign W(2,7)
uses color-first order. The present3703 witness is a fresh check of this known
construction. The page was consulted live on2026-10-02; this is not a claim
that no newer unrestricted bound exists. [Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
and [Heule](https://www.cs.cmu.edu/~mheule/publications/JOC_08_03_A01.pdf)
provide power-residue, cyclic-zipper and certificate-symmetry context. The
asymmetric w(3,k) problem is different.

The all-Boolean root/truth transport builds on the method developed in
[our F103 nine-edit lemma9785](../boolean-character-obstruction618/PROOF.md).
[Reviewer4's majority audit9772](../../six-reviewer-4/majority-orbit-audit/REVIEW.md)
is credited for the earlier short-step observation and majority parameter
bookkeeping. Those numerical bounds and that review verdict do **not** transfer
to this F617 theorem. The core classification and physical projection
contradictions here are newly computed and independently checked in source.

[VDW2's H7 exact-ten result9799](../../six-vdw-2/order7-phase-ten-singletons-triple/PROOF.md)
uses an invariant field core and nonconstant phase hypotheses;
[VDW1's F31 phase72 repair result9760](../../six-vdw-1/character-phase72-repair620/PROOF.md)
uses a different prime and phase family. They are complementary lane context,
not numerical premises. This theorem imposes no H7 invariance and does not
exclude their construction families. There is no historical-priority assertion,
external review of this new result, general polynomial-character exclusion,
or new numerical lower bound.
