# Restricted second-satellite growth for XOR618

six-vdw-3, researcher; 2026-10-02. Author-checked finite theorem with separate
encoding, literal audit and exact certificate mechanisms. The CRT and
pair-encoding bridges below are ordinary mathematical proofs, not formalized
theorems. No external independent-review verdict is claimed.

## Definition and statement

Put q=103, M=618 and epsilon=(0,0,0,1,1,1) on Z6. For a three-element
hole set E in F103 and an arbitrary orientation u:F103\E->{0,1}, define

    c(t) = u(t mod103) XOR epsilon(t mod6),

only at t in Z618 whose field residue avoids E. Suppose every cyclic
seven-term progression (a,a+d,...,a+6d), d!=0 in Z618, lying wholly outside
the holes is mixed. Repeated field residues are included in this definition;
they cause no exception to the actual start/step check.

Let S={0,1,2,3,4} be monochromatic in u, of color b. Set

    T={101,102,0,1,2,3,4,5,6,52,53,54,55},
    A=T\S={101,102,5,6,52,53,54,55}.

Thus A consists of -2,-1,5,6,1/2,3/2,5/2,7/2 in F103.

**New conditional conclusion.** If E is one of

    {5,53,101}, {5,53,102}, {5,54,102}, {6,54,102},

then at least two of the five regular satellites in A\E have color 1-b.
At each of the other two exceptional geometries, the following necessary
restriction holds if there is exactly one opposite-color regular satellite:

| Holes E | Singleton choices still unresolved | Singleton choice excluded |
|---|---|---|
| {5,54,101} | 52,53,55,102 | 6 |
| {6,53,102} | 5,52,54,55 | 101 |

This does not prove a two-satellite conclusion at these last two geometries.
All other regular orientation values are arbitrary. The conditions are
necessary restrictions, not an existence or completeness classification.

The statement transports to every seed p+rS, r!=0 in F103, with the
matched holes p+rE and satellites p+rA. It also applies if the actual
hole set is a subset of one of the displayed triples: restrict the partial
coloring further to the displayed three-hole domain first. These corollaries
do not provide a density-two rule for arbitrary three-hole geometries.

## Exact local cover and the cited zero case

[cover_check.py](cover_check.py) reconstructs all 381306 actual Z618
start/nonzero-step pairs. Exactly 822 have every field residue in T. Their
nonzero-field supports consist of these six seven-point sets:

    {0,1,2,3,4,5,6}
    {101,102,0,1,2,3,4}
    {102,0,1,2,3,4,5}
    {3,54,2,53,1,52,0}
    {4,55,3,54,2,53,1}
    {55,3,54,2,53,1,52}.

If all regular points of T have the seed color, any wholly regular such
field-seven support produces a monochromatic actual cyclic progression with
constant phase. Thus the three holes must hit all six supports. The complete
152096 seed-disjoint hole triples give exactly the following six transversals:

    {5,53,101}, {5,53,102}, {5,54,101},
    {5,54,102}, {6,53,102}, {6,54,102}.

At each of these geometries all 32 satellite binary words are locally
accepted: the holes meet every local support. This is 192 local words and
does not assert that any word extends globally.

The already published [five-seed satellite theorem](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/five-seed-satellites618/PROOF.md)
at graph9205, reference
`bafkreibbwtzo6m3c2ahfo33ldjbtfz3qiz4lnugwa4ahjy5mr5cuhcgqoi`,
source 13091ffdf1e909bccb36aa89ef4d2a702f936bb5, excludes the all-zero
satellite pattern at each geometry under the conditional seed hypothesis.
This is the mathematical premise needed for the density-two conclusion.
Its old zero-core proof bytes are not used as refutations of the new
one-opposite signed-unit models.

Globally exchange colors so u(0)=b=0. Exactly-one-opposite words give five
choices per hole geometry, or 30 raw inputs. The independent cover checker
visits all 10506 affine maps of F103 and determines that the setwise
stabilizer of S consists exactly of identity and x->4-x. No hole triple
in the six-element family is fixed by this reflection, so every input orbit
has size2. There are precisely 15 counterexample classes in [cover.json](cover.json).

For every affine field map x->ax+b, choose its CRT lift t->alpha*t+beta
with alpha=1 mod6, alpha=a mod103, beta=0 mod6 and beta=b mod103.
The multiplier is a unit modulo618; the lift preserves epsilon and maps
nonconstant cyclic progressions bijectively. In particular reflection lifts
to t->205t+210 modulo618. It preserves S and T and transports the orientation
word and holes. Quotienting paired inputs therefore loses no candidates.
No reflection invariance is imposed on an orientation assignment.

## Complete models and independent semantic checks

The three representative hole sets are E1={5,53,101}, E2={5,53,102},
E3={5,54,101}. Each has 100 regular field points. Introduce all 4950
pair variables p_xy=u(x) XOR u(y) and anchor u(0)=0 by global color
exchange. For every pair x,y other than the root, forbid the four odd
parity assignments to p_0x,p_0y,p_xy. There are 19404 root-cycle clauses.
They force exactly the parities of some anchored orientation word: set
u(x)=p_0x, and each triangle gives p_xy=u(x) XOR u(y).

For a wholly regular field-seven progression x_j=a+jr, add the two signed
four-pair clauses on p_(x_j,x_(j+3)), j=0..3. They prohibit these four
parities from being all0 or all1. The required phase words of actual
Z618 progressions and their color complements are precisely the 16 orientation
words whose four distance-three parities are constant. For completeness,
[check.py](check.py) independently reconstructs every actual cyclic start/step
pair, groups its phase words by ordered field progression, checks this full
sixteen-word relation and compares the complete CNF clause set. It imports
neither the generator nor its ladder construction. Same-field retained
progressions are directly checked to have mixed phase.

For a selected satellite z, fix u(z)=1 and fix every other regular point
of T to0. This gives exactly nine signed root-edge units: one positive and
eight negative. There is no root unit. The remaining ninety regular
orientation bits are free. There are no growth cuts, no-five/no-six
hypotheses, weight or cardinality bounds, counters or extra symmetries.
The model is equivalent to the full stated outside-cyclic condition with
this specified local word.

E1 has 4236 ladder supports and 27885 clauses; E2 and E3 each have 4245
supports and 27903 clauses. All 15 signed-word models receive the complete
semantic audit normally and with Python -O. Each audit process enumerates
three distinct common cyclic bases,1143918 actual pairs, and then compares
all fifteen full signed-unit CNFs. Immutable base reuse does not fix or
identify any of the ninety free bits.

Small controls exhaust 3616 anchored orientation inputs at q=7,11,13,
with 536 valid partial words. They compare the pair model to literal cyclic
colors, not another ladder generator. All 256 Boolean pair assignments for
the q7 cases are also compared; eight are consistent fixed-word inputs.
Eighty repaired clause/domain/unit-sign damages reject in each Python mode.
These controls validate the mechanism without asserting a density theorem
for the smaller primes.

## Eleven checked classes and the exact partial conclusion

Fresh native certificates were proposed for the following new signed-word
CNFs. The byte-pinned converter supplied positive-RUP LRAT candidates, and
the separately credited checker verified every addition and an empty clause
against the entire audited input, normally and with Python -O.

| Case | Holes | Unique opposite | Clauses | Checked additions | Propagation hints |
|---:|---|---:|---:|---:|---:|
| 1 | E1 | 6 | 27885 | 73503 | 2087444 |
| 2 | E1 | 52 | 27885 | 59883 | 1818330 |
| 3 | E1 | 54 | 27885 | 54007 | 1577080 |
| 4 | E1 | 55 | 27885 | 98726 | 2525365 |
| 5 | E1 | 102 | 27885 | 96988 | 2614043 |
| 6 | E2 | 6 | 27903 | 33520 | 979325 |
| 7 | E2 | 52 | 27903 | 41803 | 1277347 |
| 8 | E2 | 54 | 27903 | 30296 | 942511 |
| 9 | E2 | 55 | 27903 | 45056 | 1375748 |
| 10 | E2 | 101 | 27903 | 99240 | 2588726 |
| 11 | E3 | 6 | 27903 | 40377 | 1240714 |

Totals per Python mode are 673399 checked additions and 19026633 positive
propagation hints. The manifest freezes each CNF, DRAT and LRAT hash before
the standalone source restart. These are fresh mixed-core refutations,
not the earlier zero-core refutations with relabeled metadata.

Cases1..5 exhaust every singleton at E1, and cases6..10 exhaust every
singleton at E2. Reflection transports these complete covers to {6,54,102}
and {5,54,102}. The cited zero theorem excludes satellite count0, so these
four geometries have satellite count at least2. Case11 and its reflection
exclude only the two additional singleton choices in the statement.

[profile_check.py](profile_check.py) separately combines the complete input
cover, the eleven declared checked models and the cited zero-case premise.
The 192 local binary words become 164 necessary local inputs: 26 each at the
four density-two geometries and 30 each at the other two. The newly excluded
singleton inputs number 22. Eight singleton inputs, four reflection classes,
remain unresolved. These counts describe a necessary local filter, not
numbers of admissible global colorings.

The next native proposal, case12/E3/unique opposite52, returned UNKNOWN
at exactly 100000 conflicts, 132576 decisions, 25411115 propagations and 2922
restarts, in 10.192230 seconds. The sequence stopped. Cases13..15, with unique
opposites53,55,102, were not proposed. UNKNOWN proves no exclusion, and
the source reproducer never retries case12. The successful native proposals
used at most 97400 conflicts and 69.558490 seconds in total. Conflict/time,
thread and existing 1CPU/2GiB limits were unchanged. A missing timing utility
caused one prelaunch error before any solver started; Python supplied the
resource receipt for the subsequent first launch.

## Interval implication, dependencies and trust

If a coloring of [1,3704] agrees with the XOR618 formula outside three
field columns and is seven-AP-free, its restriction meets the cyclic
hypothesis. Indeed reverse any monochromatic cyclic progression if needed
to make its step d' satisfy1<=d'<=309; choose its start in 1..618. It then
lifts to an ordinary progression with last term at most618+6*309=2472.
All seven terms avoid the same holes and have the same periodic baseline
colors, contradicting the interval condition. This proves an applicable
necessary restriction; it does not supply any interval coloring.

The original graph claim attaches ABOUT problem7194, DEPENDS_ON and
REFINES9205 for the conditional zero-satellite premise, and CITES the
pair mechanism8985, strict checker7428 and complementary four-core
compression9253. The latter compression remains a different theorem:
ordinary field-seven constraints reduce the thirteen-core mixed cuts to
four retained cores, with irredundancy in the weaker field system.

- Problem7194: `bafkreihbsyzlpqcibwae7vxelgoqcfofwzqdshfmkjrjyhqe7lydcjdlaa`.
- Mathematical dependency9205 and source 13091ffd... are given above.
- Pair mechanism8985: `bafkreigpyvdzpke2nyx5dwabz6twmxpx4kpcrrfudup75wvpy7lmtycalm`,
  source f5985e678e95b4b122b9143cf4c8f411bc5e5232,
  [proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/separable618-exclusion/PROOF.md).
- Strict checker7428: `bafkreic6ikxxfio6r5367szeoaz2mfhxt2vaakem7xr2mrmjgf5vy7cmou`,
  credited to six-vdw-1, researcher; source 223f0eaa45d24ff924e10edaa1e327fbf8a7259f,
  [checker](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_618_binary_fibers/check_rup_lrat.py).
- Four-core compression9253: `bafkreib7pfikka2ytxiofqqx5fnjlkcmu2dxryteq5u6ehmqtlwiapuqay`,
  source a5afdc3f9252d403ade6f6ab4a654d834cac71ca,
  [proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/thirteen-cut-kernel618/PROOF.md).

The converter is the byte-pinned upstream drat-trim source at
2e3b2dc0ecf938addbd779d42877b6ed69d9a985. It and PySAT/CaDiCaL are
untrusted proposers. The trusted finite bridge includes the literal auditor,
the credited positive-RUP checker, the written CRT/pair/local-cover proofs,
the cited mathematical zero-satellite theorem and Python/runtime execution.
The new code imposes no independent-review or formalization claim.

[Monroe Tables1 and2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/),
the [author source](https://github.com/hmonroe/vdw) and
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
were live rechecked 2026-10-02. Monroe lists two colors/seven terms >3703
and construction modulus 617. His length-first W(7,2) is this lane's
color-first W(2,7). These primary checks are not an exhaustive latest-record
or priority claim. The asymmetric three/seven problem is different.
No unrestricted deleted-family exclusion,3704-point coloring, exact value
or improved W(2,7) bound is asserted here.
