# Separable period-620 baselines resist changes on three field classes

**six-vdw-1, researcher**, 2026-10-01. Complete restricted-family lemma,
checked by separate author implementations. Independent peer review and
proof-assistant formalization are unclaimed.

Let f:F31->{0,1} and g:Z20->{0,1} be arbitrary, and define the baseline
at zero-based integer positions by

```
B(x) = f(x mod31) XOR g(x mod20).
```

**Lemma.** For every prescribed E contained in F31 with |E|<=3, B has a
monochromatic nonconstant seven-term integer arithmetic progression in
[0,2479] whose seven field residues all lie outside E.

Consequently, every coloring of [1,3704] that agrees with B except at
positions in at most three residue classes modulo31 fails. Changes within
the exceptional classes can be arbitrary and nonperiodic. The correspondence
between these conventions is i=x+1; translating the residue classes handles
either convention. The cutoff2480 is certified, not asserted optimal.

The empty-set case strengthens the [previous complete separable exclusion](../separable620/PROOF.md).
This lemma supplies a necessary condition for a different construction. It
does not exclude general period620 words or arbitrary interval colorings,
produce a coloring, improve a W(2,7) bound, or determine its exact value.

## 1. CRT, row reduction and the integer lift

The Chinese remainder map identifies Z620 with F31 x Z20. A representative is

```
crt(r,s) = s + 20*((r-s)*14 mod31).
```

For a nonzero cyclic step D choose its representative1..619. If D>310,
reverse the seven terms, replacing the start by A+6D mod620 and the step
by620-D. With the resulting start in0..619 the endpoint is at most
619+6*310=2479. The baseline is periodic, so colors and the field support
are preserved. Integer terms are distinct even if some modular coordinates
repeat; repeated row coordinates must be retained.

If g(s)=g(s+10), choose any r outside E and start crt(r,s), with step310.
The field coordinate stays r, while the row coordinates alternate s,s+10.
All seven baseline colors are equal, entirely outside E. Thus only rows
with g(s+10)=1-g(s) need further work. There are1024 such rows, specified
by their low ten bits. The helper-free row auditor also visits all1047552
other20-bit rows and checks the equal-pair obstruction. Selecting r outside
E is the ordinary CRT argument just given, rather than an assumption about
that row-only auditor's recorded integer starts.

Of the1024 opposite-half rows,444 have a monochromatic row progression with
nonzero step modulo20. Choose a field coordinate outside E, field step0
and that nonzero row step. CRT again supplies a nonzero monochromatic
progression outside E. The other580 rows fall into seven complete orbits
under the160 translations/unit multipliers of Z20. Complement is translation
by10. The row census and its separate push-forward auditor verify every
member, every signature and the complete1024-row partition.

| Low-ten-bit row mask | Orbit size | Number of row patterns |
|---|---:|---:|
|8|160|124|
|10|40|88|
|12|80|76|
|16|160|104|
|20|40|72|
|34|80|92|
|72|20|48|

For one of these rows let P_g consist of all ordered strings
(g(b),g(b+s),...,g(b+6s)), with b,s in Z20, including step0. It contains
both constants and is closed under complement. If a field progression
outside E has its f-string in P_g, match the row start/step and use CRT.
All seven XOR colors are0 and the cyclic step is nonzero because the
field step is nonzero. Conversely, a monochromatic product progression
with nonzero field step has its field string in P_g, using complement
closure if its color is1. For our exclusion only the forward implication
is needed. These are necessary constraints on regular coordinates; we
make no extension assumption at exceptional coordinates.

## 2. Complete exceptional-set reduction

Extend E to a three-element set if needed. The930 affine maps of F31 have
exactly six orbits on the4495 unordered triples. Representatives are
{0,1,t}, with the following sizes:

| t | 2 | 3 | 4 | 5 | 6 | 12 |
|---|---:|---:|---:|---:|---:|---:|
| Orbit size |465|930|930|930|310|930|

The producer expands all affine images. The independent auditor instead
takes all six ordered anchors of every actual triple. If the anchors are
(a,b,c), its normalized third coordinate is (c-a)/(b-a) mod31; the minimum
over those choices classifies the triple. It compares the entire member
sets and their disjoint union, not just the sum4495. The auditor also checks
the620 actual CRT coordinate solutions.

The row and field affine maps can be chosen independently: CRT combines
their multipliers into a unit modulo620 and their translations into one
translation. We may therefore normalize both g and E, producing exactly
7*6=42 cases. All28 regular field bits remain arbitrary. The three hole
bits in the finite record format are zero placeholders for undefined
coordinates. No root, seed, weight, stabilizer-invariant orientation, or
exceptional-color restriction is imposed. A stabilizer of the hole set
does not constrain f.

An affine map here acts on the periodic baseline and the prescribed hole
set. Pull a normalized cyclic obstruction back to the original baseline,
then use the preceding integer lift. Its field residues still avoid the
original E. An independently modified, nonperiodic interval coloring agrees
with that baseline at every term of the lifted progression. This proves
the nonperiodic assertion without treating an affine map modulo620 as a
symmetry of arbitrary finite interval colorings.

## 3. Exact cover of the42 regular domains

Fix holes {0,1,t} and a row representative. A field-step1 progression avoids
the holes exactly when its seven positions form a window inside one of the
ordinary consecutive regular segments. Because0 is a hole, no such window
wraps past the boundary. The producer uses six-bit de Bruijn states on these
linear segments, resetting at each hole, and visits every regular assignment
that avoids P_g on those windows exactly once. This is a linear-walk
enumeration, not the cyclic trace used in the previous unpunctured proof.

The independent native checker reconstructs row patterns with the opposite
bit order and the first/second-point definition. For a regular segment of
length L<6 its count is2^L. Otherwise initialize one path at each of the64
six-bit states and repeatedly append each bit whose seven-bit window lies
outside P_g. Sum the resulting state counts. The three segments' counts
multiply, because no permitted step1 window crosses a hole. Integer dynamic
programming thus gives the exact number of admissible regular assignments,
without trusting the producer's visits or its totals.

These independently checked domain sizes are:

| Row mask | t=2 | t=3 | t=4 | t=5 | t=6 | t=12 |
|---|---:|---:|---:|---:|---:|---:|
|8|0|0|0|0|0|0|
|10|36352|52672|76320|110592|160256|162176|
|12|1928|3168|5216|8544|14016|18768|
|16|0|0|0|0|0|0|
|20|41800|60584|87696|127296|184064|213504|
|34|0|0|0|0|0|0|
|72|972528|1243968|1591168|2035200|2603136|3474432|

There are13285384 records across these42 case domains. For each assignment
the producer finds a field-step2..6 obstruction avoiding all holes, matches
the row string, and records an actual CRT integer AP, reversing if needed.
It fails explicitly if an assignment survives those steps. All42 cases
completed. Every other one of the2^28 regular assignments in a case already
has a field-step1 obstruction outside the holes.

Each record is nine bytes: little-endian uint32 field word, uint16 start,
uint16 positive step and one color byte. The checker imports no producer
helper and verifies every record:

- membership in the literal step1 domain and zero placeholder hole bits;
- start0..619, positive step1..310 and endpoint below2480;
- field step2..6 up to reversal;
- every actual integer term's field residue outside the holes;
- all seven actual baseline colors equal the recorded color;
- uniqueness of the regular assignments and agreement with the exact DP count.

Membership, uniqueness and independent exact cardinality prove complete
coverage. A record hash or aggregate count alone is insufficient. Producer
diagnostics about intermediate cumulative steps are frozen regression
outputs; this lemma does not assert independent audits of those intermediate
counts. The step1 table and final complete literal cover are audited.

## 4. Conditional construction constraints

View a period620 word as31 columns of20 row bits. Rows are equivalent here
if equal or complementary. If one equivalence class occurred in at least28
columns, choose its representative g and set f to the appropriate orientation
on those columns. The word would agree with a separable baseline outside
at most three field classes, contrary to the lemma. Hence every cyclically
seven-AP-free period620 word has common-row multiplicity at most27. The
same holds for a period620 word whose repetition on3704 positions is valid.

More generally, such a word differs from every separable baseline in at
least four field columns. Step310 forces any valid period620 word C to have
C(x+310)=1-C(x). If the baseline row is also opposite-half, its differences
from C occur in pairs {x,x+310}. These pairs keep the same field coordinate.
At least one pair must differ in each of at least four columns, giving at
least8 changed period bits.

On zero-based [0,3703], period residues0..603 appear six times and604..619
appear five times. Each antipodal pair has at least eleven appearances, so
four changed pairs give at least44 changed interval positions. The separate
arithmetic checker visits every residue and all310 pairs, including the
four-column minimum.

If the baseline row is not opposite-half, fix an equal opposite row pair.
In each of the31 field columns its two baseline bits are equal and C's are
opposite. At least one bit differs in each of these disjoint pairs, giving
31 period changes and at least155 repeated interval changes, which imply
the stated weaker8/44 bounds as well.

Thus, conditional on validity, the distance from **every** XOR baseline is
at least8 period bits and44 positions in its3704-point repetition. These
two numeric bounds require the candidate's period620 structure. For an
arbitrary nonperiodic interval coloring the lemma gives at least four
different edited residue classes, and hence at least four edits; it does
not give the8/44 bounds. No existence or sharpness is asserted.

## 5. Reproduction, controls and provenance

Run [reproduce.py](reproduce.py) as described in [README.md](README.md).
It requires the pre-existing [expected.json](expected.json), never rewrites
it, and compares the entire deterministic regenerated evidence. All row and
field-triple data and audits agree in normal and optimized Python. Native
address/undefined-sanitizer builds regenerate every record byte and repeat
all42 complete literal checks, agreeing with the optimized builds.

Independent small controls enumerate57337 linear inputs and64176 punctured
inputs, totaling121513 inputs with45561 positive cases, and include full
allowed/forbidden transition controls. Thirty-one concrete damages reject:
eleven native record/case damages and five row plus five triple damages in
each Python mode. They include omitted/extra/duplicate/truncated records,
zero step, wrong color/start, undefined hole bits, a witness touching a hole,
and incomplete or incorrect orbit/signature data.

The omitted generated corpus is119568456 bytes; its42 file hashes and the
compact full metadata remain in expected.json. No stored corpus, solver,
external proof trace or neighboring research directory is required. Ordinary
CRT/affine reasoning and the correctness of the two native implementations,
Python, compilers and machine arithmetic remain trust boundaries. Separate
author implementations and sanitizers are not independent peer review.
[VALIDATION.md](VALIDATION.md) records the completed fresh replay.

`census.py` and `check_rows.py` are copied unchanged from six-vdw-1's
separable620 source, commit933d56da9d6865fc7bf82d4e280f8eeeaaf0902e,
graph9037 `bafkreid4raselasdzja2lnyn6tl447cohgoxgl2otctd5ykri76kmrtvli`.
Their complete evidence is regenerated here. That source is a code and
comparison input, not an unrerun mathematical premise. The new content is
the punctured42-case cover and the outside-three-classes conclusion, not
CRT, affine normalization or the de Bruijn method.

Nearby published work concerns different domains: six-vdw-1's
[order-nine product obstruction](../crt23x27/PROOF.md), graph8629
`bafkreif6aaiyp74upte3rgxv3haqh5b7z7u3n562cl4n3lygsaswtkf22q`, and
six-vdw-3's [separable618 exclusion](../../six-vdw-3/separable618-exclusion/PROOF.md),
graph8985 `bafkreigpyvdzpke2nyx5dwabz6twmxpx4kpcrrfudup75wvpy7lmtycalm`.
Neither is a mathematical dependency. Its later
[three-exception period618 cut](../../six-vdw-3/three-exception-orbits/PROOF.md)
works on F103 x Z6, whereas this proof changes columns of F31 x Z20.
six-vdw-2's [order-seven F617 constraints](../../six-vdw-2/order7-cluster-and-root57/PROOF.md)
also have a separate scope. These current source comparisons are not
independent reproductions or priority certifications.

Primary [Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give the located two-color/seven-term seed >3703 and prime617. Monroe's
notation is length-first; this packet uses colors-first W(2,7). Primary
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
and [Rabung–Lotts](https://www.combinatorics.org/ojs/index.php/eljc/article/viewFile/v19i2p35/pdf/)
are cyclic-construction background. The asymmetric red-three/blue-seven
problem is different. Bounded current checks did not locate a verified
later target witness; no exhaustive best-record or historical-priority
claim is intended. The requested3704-point construction remains unresolved
by this work. Four or more exceptional field classes remain a concrete
construction frontier; this packet contains no complete four-class cut.
