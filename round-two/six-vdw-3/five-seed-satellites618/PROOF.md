# A five-term field seed must grow into an opposite-color satellite

**six-vdw-3, researcher; 2026-10-02.** Exact computer-assisted lemma,
author checked using separate generator/literal algorithms and strict
positive-RUP replay. No independent-review verdict or formalization is claimed.

Let E be a subset of F103 with at most three points, and let
u:F103\E->{0,1}. Put f(y)=1[y mod6>=3]. Assume the partial cyclic word

    c(t)=u(t mod103) XOR f(t mod6)

has no monochromatic nonzero-step seven-term AP whose field coordinates
all avoid E. Repeated cyclic points are included.

**New lemma.** For every p,r in F103 with r nonzero, if
S=p+r*{0,1,2,3,4} avoids E and has one orientation color, then some
regular point in

    p+r*H,  H={-2,-1,5,6,1/2,3/2,5/2,7/2}

has the other orientation color. All fractions are field fractions.
Equivalently, the regular part of p+r*({0,1,2,3,4} union H) is mixed
whenever its five-term seed avoids E. This is a thirteen-point pattern,
not an assertion that a six-term monochromatic AP must exist.

The [necessary-five-seed lemma](../deleted-cycle-ascent618/PROOF.md),
source **6b8943141b20b4726904e2c027bff62d5870023c**, graph 9170
`bafkreifnbqm6jaxqxrattmsdmjcplw4rn7oloopwiwnrmhhczymkmanbni`,
then guarantees at least one such seed and mixed neighborhood for every
admissible partial baseline. That existence/interval conclusion is an
explicit mathematical input. The new conditional growth proof does not
import the old no-five refutations.

All three-column repairs, general period618 existence and the 3704-point
construction remain unresolved. There is no new W(2,7) bound.

## Local reduction and complete hole geography

An affine field pullback and global color exchange put a chosen seed at
0,...,4 with color zero. They transport holes and all free orientations.
The CRT lift of x->alpha*x+beta uses A mod103=alpha, A mod6=1 and
B mod103=beta, B mod6=0. Then t->A*t+B is an invertible cyclic affine map
fixing f and preserving all nonzero steps. Thus normalization is complete.

In these coordinates write

    A=(-2,-1,5,6)=(101,102,5,6),
    B=(1/2,3/2,5/2,7/2)=(52,53,54,55).

Consider only APs supported in S union A union B, a thirteen-point set.
Every cyclic AP on this set is accounted for. The nonzero field-slope
supports have, up to reversal, exactly these six ordered representatives:

    (0,1,2,3,4,5,6)
    (101,102,0,1,2,3,4)
    (102,0,1,2,3,4,5)
    (3,54,2,53,1,52,0)
    (4,55,3,54,2,53,1)
    (55,3,54,2,53,1,52).

For any outside-hole field AP x_j=a+j*d, cyclic avoidance is exactly
that the four parities u(x_j) XOR u(x_(j+3)), j=0,...,3, are not constant.
The row f and its complements give all sixteen seven-bit orientations
with constant three-place parities. Even phase steps give all period-three
orientations and odd steps all antiperiod-three orientations. Field-slope
zero and nonzero phase steps are mixed. The literal checker reconstructs
this from actual cyclic tuples before making any parity projection.

With the five seed bits zero, the first three representatives require
the one-colored points of A to cover the path

    101 -- 102 -- 5 -- 6.

An edge disappears when either endpoint is a hole. The next two
representatives require each of (52,53,54) and (53,54,55) to be mixed
when its points are regular. The last representative forbids a constant
four-point B and is redundant: if any B point is a hole it disappears;
otherwise the two mixed triples already imply it. Thus this entire
local system separates into a path-cover condition on A and a
no-constant-triple condition on B.

When all regular satellites have color zero, all three path edges must
be hit by holes. The minimum path covers have size two and are exactly
{101,5}, {102,5}, {102,6}. Both B triples must also be hit. With only
one remaining hole that point is 53 or 54. Consequently at most two holes
are impossible, and three holes must be exactly one of

    {5,53,101}, {5,54,101},
    {5,53,102}, {5,54,102},
    {6,53,102}, {6,54,102}.

No other holes, including holes elsewhere in the field, can escape
this local cover under the three-hole limit.

The seed reflection x->4-x exchanges the endpoints of both A and B.
It pairs these six triples, leaving representatives

    E1={5,53,101}, E2={5,53,102}, E3={5,54,101}.

It transports every free orientation; no orientation reflection symmetry
is imposed. The complete affine stabilizer of S consists only of the
identity and this reflection: the mean is2, and its centered second
moment is10, so a preserving affine map has multiplier squared equal
to1. Both5 and10 are invertible in F103.

For context, a normalized seed leaves 98 possible hole positions, giving
C(98,3)=152096 hole triples. None is fixed by the reflection: its unique
fixed point 2 is in the seed, and an invariant odd set would need a fixed
point. Hence there are 76048 seed-hole reflection classes. This is a
normalized seed/hole domain, not a count of admissible colorings.

## Exact local profiles and useful density bounds

There are 93 satellite hole subsets of size at most three, or 49 reflection
classes. Enumerating the remaining binary satellite bits gives 4864 local
inputs and 2802 accepted inputs before the three global refutations below.
These are partial local patterns; global extendability is not claimed.

For a given local hole set, the generating polynomial for the number
of opposite-colored regular satellites factors into the path-cover
polynomial on A and the mixed-triple polynomial on B. With no local holes
these are

    (3z^2+4z^3+z^4)(2z+6z^2+2z^3)
       =6z^3+26z^4+32z^5+14z^6+2z^7.

Thus a seed with no satellite holes forces at least three opposite-color
points and at least one additional seed-color point in this neighborhood.
For all seed-disjoint three-hole triples, the purely local minimum
opposite-color counts have the exact geography:

| Local minimum | Hole triples |
|---:|---:|
| 0 | 6 |
| 1 | 1030 |
| 2 | 25570 |
| 3 | 125490 |

The six zero-minimum rows are precisely the exceptional triples above.
The three checked global refutations eliminate their zero-color local
patterns, giving a uniform minimum of at least one. The local geography
still supplies stronger two/three-point bounds for its other cohorts.
The six removed patterns leave 2796 necessary local patterns; neither
attainment of a bound nor extension of these patterns is asserted.

The generator obtains these profiles from the graph conditions. A
separate checker imports neither the graph predicate nor the generator.
It visits all381306 actual cyclic start/nonzero-step pairs, keeps the 822
supported on the thirteen-point set, and projects both monochromatic
colors to literal forbidden satellite terms. There are nine such terms,
including the two redundant constant-B terms. It checks every one of 4864
ternary local inputs, each component polynomial, all 93 profiles and 49
classes, and every one of 152096 literal seed-disjoint hole triples.
The complete local truth table has SHA256
`1e9c02da5f4142860c91769721192911c2bc44a5529f3039372d99486e539fad`.

## Three global refutations

For each Ei, all ten regular points of the thirteen-point neighborhood
are fixed to the seed color. The other 90 regular orientation bits are
unrestricted. This is the exact hypothesis still needed after the local
cover, without a no-five/no-six assumption, weight bound or counter.

Use 4950 pair variables p_xy=u(x) XOR u(y) on the 100 regular points, rooted
at0. Four clauses for each odd truth row enforce
p_0x XOR p_0y XOR p_xy=0. These 19404 cycle clauses extend every rooted
word uniquely. Conversely u(0)=0,u(x)=p_0x reconstruct the word;
the alternative root color is global color exchange.

Every outside-hole seven-field AP receives both signed four-pair ladder
clauses. Nine negative units fix its other regular core points to0.
No arbitrary opposite-color anchor or stabilizer invariance is imposed.

| Case | Seven ladders | Clauses | Checked RUP additions | Propagation hints |
|---|---:|---:|---:|---:|
| E1 | 4236 | 27885 | 45365 | 1464548 |
| E2 | 4245 | 27903 | 56052 | 1776553 |
| E3 | 4245 | 27903 | 35733 | 1011088 |
| Total | | | 137150 | 4252189 |

The generator enumerates half field slopes. The independent auditor
visits every actual cyclic tuple, checks each full sixteen-word relation,
reconstructs the cycle truth clauses and explicit seed units, and compares
the entire DIMACS domain and clause set. The tests remain active under -O.

Every case ends in a strictly checked positive-RUP empty clause, normally
and under optimized Python. CaDiCaL195 and drat-trim are untrusted proposers.
The credited strict checker is pinned to six-vdw-1's source
**223f0eaa45d24ff924e10edaa1e327fbf8a7259f**, graph 7428
`bafkreic6ikxxfio6r5367szeoaz2mfhxt2vaakem7xr2mrmjgf5vy7cmou`.
Its [reader-facing source](../../../van_der_waerden_618_binary_fibers/check_rup_lrat.py)
and converter pins are in [expected.json](expected.json). The pair-parity
and ascent mechanism is credited to [separable618](../separable618-exclusion/PROOF.md),
source f5985e678e95b4b122b9143cf4c8f411bc5e5232, graph 8985
`bafkreigpyvdzpke2nyx5dwabz6twmxpx4kpcrrfudup75wvpy7lmtycalm`.
Its intact-carrier refutations are not mathematical premises here.

## Interval interpretation, validation and limits

The prior necessary-five-seed lemma applies to every binary coloring of
[1,3704] agreeing outside at most three mod103 classes with an arbitrary
XOR618 baseline. It forces the six-bit row to be a rotation of000111 and
supplies a field-five seed avoiding the edited classes. A phase translation
with zero field shift fixes that row without changing u. The present lemma
adds an opposite-color regular satellite around each such seed, even if
edits inside the exceptional classes are nonperiodic.

The elementary lift behind this interval interpretation reverses any bad
cyclic AP to step at most 309 and takes its first term in[1,618]. Its endpoint
is at most 2472. A carrier avoiding edited columns survives all those edits.
Illegal six-bit rows already fail within any regular column, by the steps
309/206 forcing opposite halves and mixed parity triples. The same necessary
growth statement therefore holds for a seven-AP-free prefix of length2472.

The complete standalone restart regenerated every model, repeated all
literal local/coverage/small controls and strictly replayed all three
candidate traces normally/-O. The candidates were untrusted trace bytes,
not cached verdicts. The frozen fixture existed before that validation.
The runner also rejects eight local-artifact damages, 28 small-model damages,
eight generic malformed proofs, two damages of each selected production
proof, and a changed checker pin. It checks 1808 small anchored orientations,
including 265 positive partial colorings, and 128 complete q7 pair assignments.
No general-prime version of the F103 lemma is claimed.

All native proposals used 100000 conflicts/35 external seconds, maximum 60927
conflicts and 14.609 seconds summed native time. Conversion limits stayed 25
internal/30 external seconds; strict replay stayed 50 seconds per child.
Jobs were serial, all threads one, under the existing 1CPU/2GiB scope.
Exact validation provenance is in [verification.json](verification.json).
Large generated models/traces/binaries stay outside Git.

A separate harmonic no-six pilot reached 100002 actual conflicts at a
configured 100000 cap and returned UNKNOWN. It establishes no six-seed
exclusion and is not a premise. The original unrestricted harmonic
proposal also remains UNKNOWN. Neither incomplete instance was repeated
or given larger caps. The new three seeded models follow the different,
complete six-hole local reduction.

[Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
were rechecked 2026-10-02: the inspected symmetric two-color/seven-term seed
is >3703 and its construction modulus617. Monroe puts length before colors;
here W(2,7) puts colors first. [Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
provides primary cyclic-construction context. The asymmetric three/seven
parameter is different. Bounded lane/source/graph and narrow literature
comparison did not reveal this deleted-seed cut; no exhaustive priority or
current-record assertion is made.

The new result is a conditional seed-growth restriction plus exact local
hole profiles. It can be installed as a valid mixed-thirteen-point cut in
the outside-carrier search. The mathematical five-seed input is needed
only to assert existence of a seed in every admissible baseline. Remaining
trust includes that cited input, written CRT/affine/cover bridges, exact
source/checker and Python/compiler runtimes. Full three-column robustness,
general period618/620 colorings and unrestricted W(2,7) remain open.
