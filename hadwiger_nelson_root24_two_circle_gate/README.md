# A two-circle source fails its 377-point virtual-edge bridge

The frozen support

```text
zeta = exp(i*pi/12),    d = zeta + conjugate(zeta) = sqrt(2+sqrt(3)),
S = {0,d} union {zeta^k : 0<=k<24} union {d+zeta^k : 0<=k<24}
```

has **48 distinct plane points, 100 strict unit edges, and chromatic number
three**. Its complete unrestricted four-colour relation on the designated
centres `(0,d)` is neutral: both `00` and `01` extend, hence all 16 named
assignments extend. No physical virtual edge, non-four signal, or sub-509
candidate was obtained. The declared source stops here.

The source was selected together with a real, explicit conditional
composition on at most 377 points. Its intended forcing mechanism was that
a four-chromatic circle interior would prevent the two centres from having
the same colour. Instead, the entire 46-point circle interior is bipartite.
The obstruction is to this fixed construction, not to the Hadwiger–Nelson
record or to arbitrary two-circle supports.

## Exact geometry and a closed-form colouring

List addresses as `0,d`, then the left circle in increasing k, then the
right circle in increasing k. Merge duplicates, retaining their first
occurrence. The only two identifications are

```text
zeta^1  = d+zeta^11,
zeta^23 = d+zeta^13.
```

Thus 50 addresses give 48 distinct physical points. Neither centre lies on
either circumference, and the centres are not unit-separated.

Each centre has its 24 unit spokes. Each circle contributes the 24 edges
between exponents differing by 4 modulo 24. Four additional unit edges join
the two circles:

```text
(left 3, right 7), (left 5, right 9),
(left 19, right 15), (left 21, right 17).
```

There are no others. Exhausting all 1,128 physical pair distances checks
these statements. The 52 interior edges include all contacts; no
Cartesian-product or generic-position assumption is used.

Give both centres colour 0. On **both** circles use

```text
colour(k) = 1 + (floor(k/4) modulo 2).
```

The two identifications have consistent colours. A same-circle unit edge
changes this colour, including wraparound, and so does each of the four
extra contacts. Every spoke avoids colour 0. This proves a proper
three-colouring. The unit triangle `{0,zeta^0,zeta^4}` proves that two
colours do not suffice.

For a different-centre prescription, first give the second centre a fourth
colour; a global colour permutation gives the canonical pins `01`.
[certificate.json](certificate.json) stores both resulting words. The
verifier checks 200 word-edge inequalities and both pin prescriptions.

There is also an elementary consequence for every pair in this support.
In any three-colourable graph, a nonadjacent pair can both be recoloured
with a fourth colour; any distinct pair can be separated by giving one
endpoint the fourth colour. Thus every individual four-colour pair relation
here, and in every retained physical sub-support, is its bare graph
relation. This consequence is a proof by recolouring, not an enumerated
classification of higher-arity interfaces.

## The predeclared conditional physical bridge

The useful virtual-edge length comes from the
[April 30, 2018 Polymath discussion](https://dustingmixon.wordpress.com/2018/04/22/polymath16-second-thread-what-does-it-take-to-be-5-chromatic/).
The following coordinates make its physical budget explicit:

```text
A=(0,0), B=(1,0), C=(1/2,sqrt(3)/2),
D=(-sqrt(3)/2,-1/2), E=(1+sqrt(3)/2,-1/2).
```

The ten pair distances are checked exactly. `AB,AC,BC,AD,BE` have length
one; `AE,BD,CD,CE` have length d; and `DE` has length `1+sqrt(3)`.

**If** the source forced its centres different in every four-colouring,
place four source copies on the ordered pairs `(A,E),(B,D),(C,D),(C,E)`.
For an ordered pair `(p,q)`, the isometry is

```text
x -> p + ((q-p)/d)*x.
```

Its multiplier has norm one. Both centres coincide with the selected
endpoints, so the half has at most `5+4*(48-2)=189` distinct points after
collision merging. All inequalities of `K5` except `DE` would then be
consequences of actual unit edges. Since `A,B,C` have three different
colours, `D,E` would share the fourth.

Put `s=|E-D|^2=4+2*sqrt(3)`. Rotate a second half about D by

```text
v = 1-1/(2*s) + i*sqrt(4*s-1)/(2*s).
```

The radicand is positive, `|v|=1`, and `s*|1-v|^2=1`. The images of E
are therefore distinct and unit-separated. Two equal-terminal halves
would contradict that edge on at most `2*189-1=377` physical points.
Additional coincidences or unit contacts cannot weaken this conditional
non-four argument. No fictitious distance-d edge is counted as a unit edge.

The source's complete relation disproves the required virtual-edge premise.
We therefore did not construct or expand this conditional union. Even if
another source supplied the premise, the actual union would still require
complete exact edge reconstruction, a checked proper five-colouring and
replayable non-four evidence. The argument above alone supplies no
five-colouring upper bound.

## Reproduction and trust

From this directory, use Python 3.11 or later and only its standard library:

```sh
python3 -B verify.py
python3 -O -B verify.py
python3 -B produce.py /tmp/root24-two-circle-certificate.json
cmp certificate.json /tmp/root24-two-circle-certificate.json
sha256sum -c SHA256SUMS
```

[verify.py](verify.py) imports no producer code. It works in the exact
cyclotomic ring `Z[X]/(X^8-X^4+1)`, with `X=zeta`, conjugation
`X -> X^23`, and eight integer coefficients. Irreducibility of the 24th
cyclotomic polynomial makes coefficient equality an exact test for point
equality and unit squared norm. The chosen embedding has `zeta=exp(i*pi/12)`.
It reconstructs every pair, checks the two positive words and the
closed-form colouring, and verifies all ten distances in the conditional
five-point bridge. Five damaged certificates are rejected.

[produce.py](produce.py) uses a separate representation: real Cartesian
coordinates in `Q(sqrt(2),sqrt(3))`, with four integer coefficients on each
axis and scale factor four. It regenerates the two words from the displayed
colour formula. The initial exploratory SAT words were superseded by this
formula; neither solver verdicts nor solver packages are needed for the
published theorem or regeneration.

[EXPECTED.json](EXPECTED.json) records the complete expected output, and
[VALIDATION.json](VALIDATION.json) records versions and author checks.
Normal and optimized replay agree. Author-side comparison also matched every
physical point and all 1,128 squared norms between the radical and
cyclotomic representations, after conversion of their exact bases. The
proof's trust boundary is the elementary geometry and recolouring arguments,
cyclotomic algebra, Python integer arithmetic, finite loops and hardware.
This is author validation, not independent peer review or a formalization.
No large or hidden artifact is needed for proof replay.

## Campaign boundary

This is a new fixed, offset two-circle support, distinct from the retired
100-point VND sum and the banked 11-point Moser relation. It does not use or
expand either source. The neutral relation retires it without new directions,
phases, radii, closure depth, copies, terminal variation or hosts. The
conditional bridge is not a reason to grow a source whose premise failed.

At the 2026-09-14 refresh, the primary record remains
[Parts' 509 vertices and 2,442 edges](https://arxiv.org/abs/2010.12665v2),
also stated by [Haugland](https://arxiv.org/html/2608.04542v4).
This package records a failed construction and makes no record-progress or
priority claim. It does not classify full continuous circles or arbitrary
supports at this centre separation.
