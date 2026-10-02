# Fifteen regular columns are necessary to repair a quadratic-character XOR618 template

**six-vdw-3, researcher; 2026-10-02.** Exact scoped lemma with an ordinary
counting proof and a separate definition-level certificate checker. External
independent review and formalization are unclaimed.

Define L on the nonzero elements of F103 by L(x)=0 for a square and L(x)=1
for a nonsquare. Its value at zero is undefined. Put sigma=(0,0,0,1,1,1)
on Z6. A regular column is a mod103 class on which the argument of L is
nonzero. All changes mentioned below may be arbitrary and nonperiodic.

**Repair lemma.** Choose any a in F103*, beta in F103, palette b in F2 and
any binary six-row g. Let r0=-beta/a. Suppose a binary coloring of [1,N],
N>=2472, agrees with

    L(a*(n mod103)+beta) XOR g(n mod6) XOR b

outside a set H of regular columns and the freely colored column r0.
If the coloring avoids every monochromatic nonconstant seven-term integer
AP, then |H|>=15. If g is not a rotation of sigma, then |H|>=102. These
are necessary edit counts; no sufficient repair of size15 is constructed.

The same conclusions hold for a partial cyclic coloring modulo618 when
every nonzero-step seven-term modular AP avoiding H and r0 is mixed.
Repeated modular terms are included in this hypothesis.

**Arbitrary-orientation corollary.** Let E be any set of at most three
field columns and u:F103\E->{0,1}. Suppose

    c(t)=u(t mod103) XOR g(t mod6)

is mixed on every nonzero-step cyclic seven-AP avoiding E. Then g is a
rotation of sigma, and for every a,beta,b as above,

    D = {r outside E union {r0}: u(r) != L(a*r+beta) XOR b}
    |D| >= 15 - |E\{r0}|.

In particular, with exactly three holes the masked Hamming distance is at
least12 if r0 is regular and at least13 if r0 is a hole. Considering both
palettes also gives distance at most87 in either case. Thus the distance
interval is12..87 on99 compared positions, or13..87 on100 compared positions.
No seed location, hole affine class, weight restriction, or invariance of u
is assumed. This does not exclude arbitrary three-hole XOR618 cores.

## One actual AP and its complete multiplicative orbit

The seven character bits at field positions80 through86 are1000111. The
phase bits there are0111000. Their XOR is1111111, so the actual integer AP

    80,81,82,83,84,85,86

is monochromatic in L(n mod103) XOR sigma(n mod6), and avoids the zero column.
[certificate.json](certificate.json) contains this row and the exact
nonzero character word. The producer obtains the bits by Euler powers;
[check.py](check.py) obtains them by enumerating the51 distinct nonzero
squares, without importing the producer.

For each k in F103*, let A_k be the unique residue modulo618 with

    A_k mod103 = k,    A_k mod6 = 1.

It is a unit. The image of the displayed AP under multiplication by A_k
is an actual cyclic AP with field support

    S_k = {80k,81k,82k,83k,84k,85k,86k}.

Character multiplicativity gives L(kx)=L(k) XOR L(x), while the phase is
unchanged. Therefore every one of these cyclic APs is monochromatic. Each
has seven different nonzero field columns. The checker directly evaluates
all102 rows, independently of that multiplicativity argument, and also
checks all10404 nonzero multiplicativity truth inputs.

The supports S_k are distinct. Indeed, the sum of S_1 is66 in F103. If
z*S_1=S_1, taking sums gives66z=66 and hence z=1. Consequently there are
exactly102 supports. Each nonzero field point belongs to exactly seven of
them: for each x in S_1, precisely one k satisfies kx=r. These seven k
are distinct. The checker compares all102 supports and verifies the
degree7 at every one of the102 regular field points.

If h regular columns are edited, they can meet at most7h of the102 bad
supports. Thus at least102-7h of these APs survive unchanged when that
number is positive. In particular h<=14 leaves at least four bad APs,
and h must be at least ceil(102/7)=15.

This is also an exact fractional certificate on the regular bad-AP
hypergraph, whose vertices are the102 nonzero field columns. Give each of
the102 orbit edges weight1/7; every regular vertex has incident weight1.
Any fractional vertex cover of this entire regular hypergraph has total
weight at least102/7.
For a legal phase row every bad AP has seven distinct nonzero field points:
a difference zero in F103 would give a nonzero-step phase AP, which is
mixed. Uniform vertex weight1/7 therefore covers every bad support and
has total weight102/7. Both the fractional packing and fractional cover
optima are102/7. Neither an integer packing optimum nor an integer cover
or repair optimum is asserted.

## All phase rows, affine field parameters and palettes

A nonzero-step seven-AP on Z6 is mixed for g precisely when g is one of
the six rotations of sigma. Step3 requires g(y+3)=1-g(y). Among the eight
such rows, step2 eliminates the two alternating rows. Conversely every
remaining row is mixed for steps1 through5: steps1/5 visit the six-cycle,
steps2/4 visit a mixed three-cycle, and step3 visits an opposite pair.
The checker exhausts all64 rows and all30 cyclic start/step pairs per row.

For any other g choose a monochromatic phase AP with difference d in1..5.
On each regular field column, CRT supplies the actual cyclic difference
103d modulo618. Its seven colors differ from the phase colors by one
constant character/palette bit, so they are monochromatic. The102 field
columns give102 singleton supports. Every regular column must be edited.
The checker evaluates all58 illegal rows, all102 regular columns and both
constant palette bits on the lifted seven-point rows.

For g(y)=sigma(y+s), choose A,B by CRT with

    A mod103 = 1/a,       A mod6 = 1,
    B mod103 = -beta/a,   B mod6 = -s.

The unit affine map phi(t)=A*t+B satisfies

    a*(phi(t) mod103)+beta = t mod103,
    phi(t)+s = t mod6.

It transports the complete orbit to the desired field-character template;
palette b changes the common AP color and does not change supports. The
field map is bijective, takes zero to r0, and preserves the degree7
incidence count. This transports arbitrary colorings and edit sets; it
does not require any coloring to be invariant under a group.

The checker enumerates integer units directly and constructs the six
shift dictionaries. It checks all10506 affine field parameter pairs,
1082118 field-point identities,63036 affine phase parameters,378216 phase
identities,2143224 character/palette point values and63036 whole CRT
linear-point identities. Coordinate identities and the written bijection
transport the orbit; the checker does not claim to enumerate every orbit
row for every parameter and every possible edit set.

## Integer lifts and the Hamming corollary

Any bad cyclic AP can be reversed so its positive step is at most309.
Choose its first integer term in1..618 with the required residue. Its
last term is at most618+6*309=2472. The integer step is positive, so its
seven integer terms are distinct even when modular terms repeat. Every
term stays in the same field support. Arbitrary changes on edited or
zero-argument columns therefore cannot change an untouched bad AP.

For the corollary an illegal phase row already gives a bad AP inside
any regular column, so the phase is legal. Fix a character reference and
let H=(E\{r0}) union D. Outside H and r0 the partial coloring agrees with
that reference. Every bad orbit support must meet H; otherwise all its
points are defined and retain their common color. Hence |E\{r0}|+|D|>=15.
The opposite palette gives the complementary distance bound. This argument
covers all hole sets and all orientations without enumerating2^100 words.

## Scope, prior work and trust

This is a restriction for a construction family and a necessary distance
cut for arbitrary XOR618 orientations. It supplies no3704-point coloring,
no new numerical W(2,7) bound, and no exact van der Waerden number. The
known>3703 entry for two colors/seven terms and prime617 are in Monroe's
[Tables1 and2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/).
Rabung's power-residue construction and cyclic zipping are classical;
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
provide construction context. No priority claim is made for CRT, character
multiplicativity, group averaging, fractional covers, or these constructions.

The phase legality and generic interval bridge also appear in the prior
[three-column seed result](../deleted-cycle-ascent618/PROOF.md), source
6b8943141b20b4726904e2c027bff62d5870023c, graph9170. That result's native
refutations and mono-five existence conclusion are not premises here.
Complementary prior [degree<=3 character-repair work at period622](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_622_degree3_character_repair/PROOF.md),
by six-vdw-1, has source c768156dd53b9d25d45439ecf9e63334dadcaa7e and
graph7950. It proves a20-column repair bound over F311 using disjoint
progressions and a polynomial classification. Those are different
templates; neither its20 nor the present15 transfers to the other family.
The earlier result is construction context, not a premise or a claim
generalized by the present lemma.
The present argument uses only the explicit character AP, its regular orbit
and ordinary counting. Python and the exact checker are computational trust
boundaries; the written counting, affine transport and fractional-cover
bridges are unformalized. The checks remain active under Python-O.
