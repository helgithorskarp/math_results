# The fixed fish–spindle sum has no nontrivial two-terminal relation

The exact support in this package has **157 distinct plane points and 535
strict unit edges**. Every distinct pair permits different colours in some
proper four-colouring. Every nonunit pair also permits the same colour in some
proper four-colouring. Thus its complete unrestricted relation on each
**two-terminal set** is exactly the relation of the bare terminal graph.

This closes one concrete attempt to obtain a small forced-equal half for a
five-chromatic spindle. Before reconstruction the source had a 161-point
bound, allowing a two-copy construction on at most 321 points. Its exact order
would improve that budget to 313. **The required forced-equal pair does not
exist**, even after taking any retained induced physical subgraph. No
five-chromatic graph, sub-509 candidate, or qualifying physical signal is
obtained. Relations on larger terminal sets and arbitrary rotated unions are
not classified. The declared source is retired without phase or host expansion.

## Fixed physical source

Let `F=(f_0,...,f_22)` be the symmetric Hochberg–O'Donnell fish realization
specified by [geometry_certificate.json](geometry_certificate.json). Its
fixed vertices are

```
f_0=(0,0), f_1=(1,0), f_2=(0,1), f_5=(1,1).
```

The remaining 38 real coordinates are the unique solution in the listed
rational box to the 38 non-square squared-unit-edge equations. The midpoint
has denominator `10^50` and the box radius is `10^-25`. Together with the four
square edges, these define the fish's 42 unit edges. The checker proves root
existence and uniqueness, excludes every point collision and every unlisted
fish contact, and does not treat the midpoint as the exact realization.

This is the known fish graph, with labels `(A,B,p0,...,p10,q0,...,q4,r0,...,r4)`
in [Parcly Taxel's Shibuya construction](https://github.com/Parcly-Taxel/Shibuya/blob/master/shibuya/graphs/pegg.py),
with its symmetry parameter set to zero. The original construction is due to
Hochberg and O'Donnell, *Some 4-Chromatic Unit-Distance Graphs without Small
Cycles*, Geombinatorics 5 (1996), 137–141; see also
[Taxel's construction discussion](https://math.stackexchange.com/questions/3958839/are-4-chromatic-3-connected-unit-distance-graphs-always-rigid).
The fish graph and the Moser spindle are prior art; no new atom or priority
claim is made. The exact support here is defined by the included isolating
certificate, so reproduction needs no external numerical input.

In complex notation put

```
rho = (1+i*sqrt(3))/2,
r   = (5+i*sqrt(11))/6,
M   = (0,1,rho,1+rho,r,r*rho,r*(1+rho)).
```

Freeze the single aligned support `S=F+M`. Neither an orientation parameter nor
a family of fish flexes is varied. A formal address `(i,j)` names `f_i+m_j` and
has integer label `7*i+j`. Among 161 addresses the only collision classes of
size greater than one are

```
(1,7), (3,9), (15,35), (17,37).
```

They are exact consequences of the fixed square and `m_1-m_0=m_3-m_2=1`.
Physical labels are assigned in order of first occurrence. The remaining
classes are singletons, giving 157 points.

After these identifications, **every physical unit edge is inherited from a
factor**: either a fish edge at fixed Moser index or a Moser edge at fixed fish
index. There are no additional unit contacts. This last statement is checked
on all 12,246 physical pairs, including the 11,711 nonedges; it is not an
assumption that the graph is a Cartesian product. A quotient of a product can
have different colouring properties, so proper colourings of this particular
quotient are still checked explicitly.

## Exact realization certificate

[model.py](model.py) uses only Python integers and `fractions.Fraction`.
Let `P(x)` be the 38 non-square squared-distance equations minus one, `J` its
Jacobian, `m` the rational midpoint, `r_box=10^-25`, and `A` the rational
approximate inverse matrix supplied in the certificate. The checker computes

```
beta  = ||I-A J(m)||_infinity,
eta   = beta + 16*r_box*||A||_infinity,
delta = ||A P(m)||_infinity + eta*r_box.
```

It verifies `beta<1`, `eta<1`, and `delta<r_box` exactly. Each Jacobian row
changes by at most `16*r_box` in row-sum norm throughout the box. Hence
`x -> x-A P(x)` is a contraction mapping the box strictly into itself.
Its unique fixed point exists and is a zero of `P`, since `beta<1` also proves
that the square matrix `A` is nonsingular. This gives exact real coordinates
without needing a radical expression for them.

The Moser coordinates and unit edges are checked in the exact field
`Q(sqrt(3),sqrt(11))`, using the basis `(1,sqrt(3),sqrt(11),sqrt(33))`. For
noncontact bounds, integer square roots give rational enclosures of each
positive radical. A coordinate of a sum point differs from its computed
rational midpoint by at most `R=r_box+2/10^50`. A midpoint difference `(dx,dy)`
therefore has squared-distance error at most

```
4*R*(abs(dx)+abs(dy)) + 8*R^2.
```

This excludes all unlisted collisions and contacts. The actual bounds are
recorded as exact fractions in [EXPECTED.json](EXPECTED.json); physical squared
separations exceed `0.0004` and nonedge squared-unit gaps exceed `0.00018`.
Listed edges follow exactly from the factor equations and translations.
No floating-point edge decision enters verification.

The optional numerical search that found the box is not a proof dependency.
The rational midpoint, equations, inverse certificate and isolating radius are
the complete input specifying the exact source.

## Complete two-terminal relation

[relation_certificate.json](relation_certificate.json) contains **92** proper
four-colour words of length 157. [verify.py](verify.py) first reconstructs the
physical graph, then directly checks all 49,220 word–edge inequalities.
For every physical pair it records whether the words exhibit equal colours,
different colours, or both. The result is:

| Pair type | Pairs | Feasible canonical patterns |
|---|---:|---|
| Unit | 535 | `01` |
| Nonunit | 11,711 | `00`, `01` |
| All distinct pairs | 12,246 | Every pair permits `01` |

There are exactly 23,957 feasible pair-pattern requests. Colour renaming makes
`00` representative of every equal-colour assignment and `01` representative
of every unequal-colour assignment. This proves the full relation for each
pair, not just that there is no forced-equal pair. It does **not** classify
simultaneous prescriptions on several pairs or the full relation on all 157
vertices treated as terminals.

The source contains the physical fibre `f_0+M`. The checker exhausts all
`3^7=2187` Moser colour assignments and finds no three-colouring. The positive
words above therefore prove that the full support is exactly four-chromatic.

Every retained induced physical subgraph inherits the positive colour words.
In particular, no internal-vertex deletion can create a forced-equal pair, or a
forced-unequal pair at nonunit distance. The lack of a small core follows by
restriction; it is not based on a heuristic minimizer.

## Connection to the record objective

If a four-colourable physical source of order `n` had terminals `a,b` forced to
have equal colours, with `d=|a-b|>=1/2`, identify `a` in two rotated copies and
choose the relative rotation so the two images of `b` are unit distance apart.
The required rotation has

```
cos(theta) = 1 - 1/(2*d^2).
```

Any four-colouring of the union would force those adjacent images to have the
colour of the shared vertex, a contradiction. Its order is at most `2*n-1`.
Here that would be at most 313, comfortably below 509. A real candidate would
still require complete contact reconstruction, a proper five-colouring and a
replayable four-colour refutation. Our source fails the intrinsic relation
premise, so no such union is proposed or generated.

This is a scoped construction failure, not a theorem about arbitrary two-copy
unions: extra cross-contacts between copies could create other obstructions.
It also supplies no lower bound for the order of general five-chromatic plane
graphs. The fixed aligned source and this equality-half mechanism are retired.

## Reproduction and validation

Use Python 3.11 or later, standard library only, from this directory:

```bash
python3 -B verify.py
python3 -B direct_audit.py
python3 -B controls.py
python3 -O -B verify.py
sha256sum -c SHA256SUMS
```

Expected relation status: `EVERY TWO-TERMINAL RELATION IS NEUTRAL`.
See [EXPECTED.json](EXPECTED.json) and [VALIDATION.json](VALIDATION.json).

The alternate [direct_audit.py](direct_audit.py) uses rational interval products
on all **12,880 formal address pairs**, with radical enclosures of denominator
`10^40`. It obtains four collision pairs, 593 unit pairs and 12,283 nonunit
pairs before quotienting. Its transposed colour-bitset check reproduces the
complete physical pair relation. It shares the root proof and atom definition
with the main checker; this is an alternate author-side check, not independent
peer review. Eight mathematical corruptions are rejected without relying on
file hashes. Normal and assertion-disabled main outputs agree.

Optional positive-certificate regeneration uses the pinned
[python-sat dependency](requirements-discovery.txt) and CaDiCaL195:

```bash
python3 -B produce.py /tmp/fish-spindle-relations.json
cmp relation_certificate.json /tmp/fish-spindle-relations.json
```

The SAT encoding has exactly one colour per vertex and one unequal-colour
clause per physical edge and colour. Equal and unequal pin requests are
normalized to `00` and `01`; there are no other base pins or symmetry clauses.
All returned models are decoded and checked on the original graph. Every
required answer is positive. No SAT UNSAT verdict is a verification premise;
a future negative response makes regeneration stop for separate certification.
The author obtained byte-identical regeneration.

Certificate hashes:

- Geometry: `3bd20da06a912e5274e99db2e17f09c89e5761bc0ab209f84b6b24403b28b566`
- Pair relations: `e37d67ac5702629e67d54b64f04515540c397d738b42e2dbbe985cd264ffabfa`
- Colour-word stream: `9b79e15cb22fedc55d29519a73d8aabfde3cb1060b8fdbd183d3b4b50c233fe9`
- Complete physical graph: `76b3316f71fac45faa0dd13a76711003b9763731ff4f67daa82ce6391cc3397e`

The geometry certificate is 27,453 bytes and the relation certificate is
14,868 bytes. No large artifact or external numerical input is omitted from
the verification boundary. Trust rests on the elementary contraction and
coverage arguments, input transcription, the checkers, Python exact arithmetic
and ordinary hardware; there is no proof-assistant formalization or external-
author acceptance.

The 2026-09-14 bounded primary-source refresh retained the published 509-point,
2,442-edge record from [Parts](https://arxiv.org/abs/2010.12665v2), also identified
as the current vertex record by
[Haugland](https://arxiv.org/html/2608.04542v4). The newer
[2,259-edge repository claim](https://github.com/md-amer/hadwiger-nelson-e5)
uses the same 509-point drawing and deletes edges; it provides no smaller or
new strict physical support. That edge-minimization claim was read for source
selection and was not independently reviewed in this pass.
