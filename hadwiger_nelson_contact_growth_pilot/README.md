# A capped colour-guided contact-growth pilot

Four independently checked, strictly induced Euclidean unit-distance graphs
with 508 vertices were constructed. All four have chromatic number exactly 4.
**No graph requiring five colours was found.** This is a bounded discovery
experiment, not a classification of the field or the growth mechanism.

| Trajectory | Unit edges | SAT queries | Solver conflicts | Unit edges outside the growth dictionary |
|---|---:|---:|---:|---:|
| 0 | 2755 | 496 | 2041 | 9 |
| 1 | 2785 | 496 | 1679 | 9 |
| 2 | 2453 | 496 | 0 | 0 |
| 3 | 2870 | 496 | 2652 | 0 |

The preset cap was four trajectories, each starting at 13 vertices and ending
at 508, with 100000 conflicts per query and 500000 per trajectory. All 1984
queries returned SAT. No cap was reached early, no UNKNOWN or UNSAT occurred,
and no larger search or negative-family closure followed. The four final
colour words also certify every induced prefix queried along these trajectories.
These are labelled outputs, not an enumeration of isomorphism classes.

## Exact construction

Let

```
omega=(1+i sqrt3)/2,
v=(sqrt33+i sqrt3)/6,
rho=(7+i sqrt15)/8.
```

All three numbers have modulus1. The native dictionary consists of the 30
distinct vectors `omega^j v^k`, `0<=j<6`, `-2<=k<=2`. Add their rho images
to obtain 60 unit vectors. This uses familiar spindle geometry: the 30-direction
set and the radius 2 linking rotation occur in
[de Grey's construction, Sections 3.3 and 4.2](https://arxiv.org/html/1804.02385v2).
The contribution here is the saved contact-growth experiment, not a new
direction set or a new general construction theorem. No stored de Grey,
Parts, T721, or other large graph is an input.

The seven-point seed spindle, in this order, is

```
M=[0,1,omega,1+omega,v^2,v^2 omega,v^2(1+omega)].
```

The initial 13 points are `M` followed by `rho M` with its repeated origin
omitted. During growth, offer every unit translate of a selected point by a
dictionary vector. A point is eligible once it has at least two dictionary
contacts with selected points. The next point is chosen using a bank of at
most four proper colourings, its dictionary contact count, and its exact
trace height. A bank word is blocked if the contact neighbours use all four
colours in that word. The ordered scores are:

```
run0: (blocked, degree, -height, tie)
run1: (degree, blocked, -height, tie)
run2: (blocked, degree, tie, -height)
run3: (degree, blocked, tie, -height)
```

Choose the lexicographic maximum. `tie` is the first 64 bits of SHA256 of the
ASCII string `run:a,b,c,d,e,f,g,h`. Degree and blocked scores use dictionary
contacts; **all** exact unit contacts, including those outside that dictionary,
are inserted in the SAT formula after choosing the point. Old bank words
are extended by the least available colour when possible and otherwise
discarded. Add the current SAT word if new and retain the last four words.

Coordinates are stored without floating-point arithmetic as

```
x=(a+b sqrt5+c sqrt33+d sqrt165)/96,
y=(e sqrt3+f sqrt15+g sqrt11+h sqrt55)/96,
```

with integer labels. For a coordinate difference, the squared distance is
`(A+B sqrt5+C sqrt33+D sqrt165)/96^2`, where

```
A=a^2+5b^2+33c^2+165d^2+3e^2+15f^2+11g^2+55h^2
B=2(ab+33cd+3ef+11gh)
C=2(ac+5bd+eg+5fh)
D=2(ad+bc+eh+fg).
```

A strict unit edge is equivalent to `(A,B,C,D)=(96^2,0,0,0)`.
The positive-definite integer `A` is the height used for ranking.
The real field has basis `1,sqrt5,sqrt33,sqrt165`; the corresponding
imaginary coordinates lie in the complementary subspace. Thus equality
of physical points is exactly equality of their integer labels.

## Certificates and independent verification

`certificate.json` contains 495 parent/step records and a 508-symbol proper
four-colouring for each trajectory. A record `[p,s]` creates the next point
by adding sorted dictionary step`s` to already reconstructed point`p`.
The coordinate tuples above determine dictionary sorting. No large graph
or solver log is needed to verify these four outputs.

The producer uses the displayed Cartesian norm coefficients and enumerates
the native unit vectors by bounded integer equations. The verifier instead
uses the tensor algebra

```
Q[t,r,s]/(t^2-5, r^2+3, s^2+11),
t=sqrt5, r=i sqrt3, s=i sqrt11.
```

It constructs directions by powers of `omega=(1+r)/2`, `v=(r-rs)/6`, and
`rho=(7+rt)/8`, and tests distances by multiplying a difference by its complex
conjugate. The three square classes are independent, so this is a degree 8
field with an injective physical embedding. The checker imports no producer
code, SAT library, direct Cartesian norm formula, or direction-enumeration
loop.

It checks all 515112 unordered point pairs, all 10863 unit edges, all four
colour words, distinctness, parent bounds, and the two-contact growth rule.
It rejects 12 corrupt certificate variants. An arithmetic control rejects a
nonunit point whose squared norm has rational coefficient 1 but also a nonzero
sqrt5 coefficient. Exhausting all 2187 three-colour assignments on the seed
spindle finds none; the final four-colour words prove the matching upper
bound. Hence the chromatic numbers are exactly 4.

The mathematical claim depends on exact integer/rational arithmetic and the
checker, not on solver soundness. The SAT search uses one-hot variables,
one colour per vertex, and colour inequalities for every strict unit edge.
It pins the genuine seed triangle 0,1,2 to colours 0,1,2; colour renaming makes
this symmetry restriction sound. The search mechanism is heuristic and its
untested trajectories remain unresolved. The checker certifies the saved
geometry and colourings, not the heuristic optimality of each score choice.

## Reproduction

From the repository root, with CPython 3.11.2 and its standard library:

```sh
python3 hadwiger_nelson_contact_growth_pilot/verify.py --certificate hadwiger_nelson_contact_growth_pilot/certificate.json
```

The expected output is in `EXPECTED.json`. To repeat discovery, install
`python-sat==1.9.dev15` (CaDiCaL 1.9.5), then run:

```sh
python3 hadwiger_nelson_contact_growth_pilot/grow.py --work /tmp/hn-contact-growth
python3 hadwiger_nelson_contact_growth_pilot/verify.py --certificate /tmp/hn-contact-growth/certificate.json --work /tmp/hn-contact-growth
```

The optional `--work` audit compares every reconstructed coordinate with the
producer output. Search decisions depend on the solver version; the tape
certificate is solver-independent. Runtime fields vary between runs.
All generated logs and coordinate lists stay in the chosen work directory.
If a future invocation returns a signal or UNKNOWN, the producer preserves
the full query CNF and stops; an UNSAT result would still require a separate
proof-producing solve and independent refutation check before any claim.

The completed no-signal pilot is frozen. It establishes no upper bound on
untested point sets and does not improve the 509-vertex record.
