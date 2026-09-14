# A fixed 100-point VND sum fails its 199-point equality-bridge gate

The exact support `S=L+uL` specified below has **100 distinct plane points,
344 strict unit edges, and chromatic number four**. Every individual
two-terminal relation is neutral: all 4,606 nonunit pairs permit equal
colours, and all 4,950 distinct pairs permit different colours. The complete
certificate consists of 57 proper four-colour words.

The source was selected with an explicit physical bridge and point budget:
a forced-equal pair at distance at least one half would give a non-four
unit-distance union of two copies on at most 199 points. No such pair exists.
The first required relation milestone therefore fails. This fixed source is
retired without phase, factor, terminal-arity, or host expansion. No sub-509
candidate or record progress is claimed.

## One frozen physical support

Let `L` be the rectangular VND ten-point atom, with points in this order:

```text
0, 1, i*sqrt(2), 1+i*sqrt(2), f, 1+f,
1/2+s*sqrt(6)/6 + i*(sqrt(2)/2+t*sqrt(3)/6),
```

where `f=(-1+i)*sqrt(2)/2` and the final four points use
`(s,t)=(-1,-1),(-1,1),(1,-1),(1,1)`. This is the `L10,2` atom associated
with [Voronov, Neopryatnaya and Dergachev](https://arxiv.org/html/2106.11824v4).
The coordinates and chromatic demand are checked here; no imported graph
or chromatic certificate is needed.

Fix exactly

```text
u = (-3+i*sqrt(7))/4,      S = {L_i+u*L_j : 0<=i,j<10}.
```

The multiplier has norm one. It is selected by the actual contact identity
`|i*sqrt(2)*(1+u)|=1`, not by a floating angle. The atom coordinates lie in
`K0=Q(i,sqrt(2),sqrt(3))`, whereas `u` lies outside K0, by independence of
the square class of 7. If two different sum addresses coincided, their
difference would express u as a quotient of two K0 elements, unless both
factor addresses were already equal. Thus all 100 addresses give distinct
physical points. Direct exact tuple comparison also checks this.

Label a physical point by `10*i+j`. The atom has 17 unit edges, giving
`17*10+10*17=340` factor edges. Exhausting all 4,950 physical pairs gives
exactly four additional edges:

```text
(0,22), (1,23), (10,32), (11,33).
```

There are no other unit contacts. These extra edges are included in every
colouring check; the source is not assumed to be an abstract Cartesian
product. Its complete geometry is reconstructed from formulas by
[model.py](model.py), with coordinates multiplied by 24 in the real basis

```text
1, sqrt(2), sqrt(3), sqrt(6), sqrt(7), sqrt(14), sqrt(21), sqrt(42)
```

on each Cartesian axis. All arithmetic is exact Python integer arithmetic.

## Full pair relation and the selected physical bridge

For a distinct pair of marked points, colour renaming leaves two canonical
patterns: `00` and `01`. A physical unit edge forbids `00`; both patterns
are feasible on a bare nonunit pair. Each of the 57 words in
[certificate.json](certificate.json) is checked against all 344 unit edges.
Their equality and inequality sets cover every feasible canonical request:

| Checked quantity | Count |
|---|---:|
| Distinct physical pairs | 4,950 |
| Nonunit pairs with an equal-colour witness | 4,606 |
| Pairs with a different-colour witness | 4,950 |
| Canonical pair requests covered | 9,556 |
| Word-edge inequalities checked | 19,608 |
| Pairs at distance at least one half | 4,452 |
| Nonunit pairs at distance at least one half | 4,108 |
| Pairs at distance exactly one half | 0 |

The distance condition is checked by recursive exact radical comparisons.
An alternate checker decides every sign using rational square-root
enclosures with denominator `2^64`; none is ambiguous.

The composition rule was fixed before the relation census. For a proposed
forced-equal pair p,q, set `s=|p-q|^2>=1/4` and

```text
v = 1-1/(2*s) + i*sqrt(4*s-1)/(2*s).
```

The square root is real. Direct expansion gives `|v|=1` and
`s*|1-v|^2=1`. Therefore the union

```text
S union {p+v*(x-p) : x in S}
```

contains two copies sharing p, while q and its second image are distinct
points at unit distance. It has at most `2*100-1=199` distinct points after
all collisions are merged. A four-colouring would restrict to both source
copies, forcing both images of q to have p's colour, contrary to their
physical unit edge. Additional contacts or collisions cannot invalidate
this lower-bound argument.

This is a geometrically realizable *conditional* incidence bridge, not a
claim that its colour premise holds. The certificate disproves that premise
for every eligible pair. No two-copy union was promoted to a candidate or
grown after the neutral census. If a different source ever supplies the
premise, its actual union still requires complete physical-edge
reconstruction, a proper five-colouring, and replayable non-four evidence;
the bridge alone does not establish an upper bound of five.

Restricting the positive words proves the same complete pair neutrality on
every retained strict physical sub-support of S. In particular, deleting
interior vertices cannot extract an equality half. This does not classify
higher-arity relations, simultaneous prescriptions on several pairs, other
rotations of L, or arbitrary plane unit-distance graphs.

## Two exact geometry derivations

The main checker expands the squared norms of the 24-scaled coordinates
in the eight-radical basis. An alternate checker,
[direct_audit.py](direct_audit.py), imports none of the main model, verifier,
or SAT producer. It works with six-scaled atom differences

```text
a = ax+i*ay, b = bx+i*by,
A=|a|^2, B=|b|^2, R=Re(conj(a)*b), I=Im(conj(a)*b),
```

in the smaller real field `Q(sqrt(2),sqrt(3))`. It derives

```text
72*(squared physical distance) = 2*A+2*B-3*R-sqrt(7)*I.
```

Independence of sqrt(7) makes a unit contact equivalent to the two exact
coefficient conditions

```text
I=0,       2*A+2*B-3*R=72.
```

The alternate checker uses square-free radicands and gcd multiplication,
rather than bit-mask multiplication. It compares hashes of the *complete*
norm stream and edge list, not aggregate counts alone. Its colour check
transposes words into four bit sets per vertex and recovers both possible
pair patterns from bit intersections. The main checker instead collects
pair patterns row by row. Both complete relations agree.

The atom's triangle `(0,7,8)` can be pinned to three different colours.
Testing all `3^7=2,187` assignments to the other atom vertices gives no
three-colouring. The source contains an unchanged atom copy, and the
positive words prove a four-colouring, so its chromatic number is exactly
four. The statement is about physical plane graphs, not sphere embeddings
or two-distance auxiliaries.

## Reproduce

Use Python 3.11 or later, with only the standard library for proof replay:

```sh
python3 -B verify.py
python3 -B direct_audit.py
python3 -B controls.py
python3 -O -B verify.py
sha256sum -c SHA256SUMS
```

[EXPECTED.json](EXPECTED.json) records all outputs and hashes;
[VALIDATION.json](VALIDATION.json) records versions and measured runtimes.
Six damaged certificates are rejected without hash-based rejection,
including a collection of proper words that fails complete relation
coverage. Fourteen signed-radical control comparisons pass.

Optional positive-witness regeneration uses `python-sat==1.8.dev24` with its
bundled CaDiCaL 1.9.5:

```sh
python3 -m pip install -r requirements-discovery.txt
python3 -B produce.py /tmp/vnd-sqrt7-pair-certificate.json
cmp certificate.json /tmp/vnd-sqrt7-pair-certificate.json
```

The SAT encoding has one Boolean variable per point and colour, exactly one
colour per point, and the four ordinary inequality clauses per edge. A
requested equal pattern pins both endpoints to zero; a different pattern
pins them to zero and one. Global colour renaming proves those pins lose no
models. The generator selects the first uncovered pair lexicographically,
decodes and checks a positive word, and repeats. No solver UNSAT verdict is
used in the theorem. The compact positive words make a solver unnecessary
for replay.

Trust rests on the exact formulas, finite loops, colour decoding/checking,
Python integer arithmetic and hardware. The exact real sign algorithm uses
successive quadratic extensions; its alternate rational enclosures need no
floating-point assumption. This is not a proof-assistant formalization.
The two checks are author-side validation, not independent peer review.
There is no imported coordinate file or omitted large proof artifact.

## Scope and source selection

The fixed multiplier introduces sqrt(7) and creates four nonfactor edges.
This is a different support from the previously tested L+M+vM sources;
neither their colouring certificates nor the banked 11-point Moser relation
is used. It does not modify the latter's terminals or resume its composition.
The source and its 199-point bridge were fixed together before the census.
The neutral full relation now retires this source. A different source would
need fresh physical evidence and a new explicit capped bridge; this package
does not license a sweep of nearby rotations.

At the 2026-09-14 refresh, [Parts' primary record](https://arxiv.org/abs/2010.12665v2)
remains 509 vertices and 2,442 edges, also identified by
[Haugland's recent paper](https://arxiv.org/html/2608.04542v4). The present
result is a restricted construction failure, not progress on that record.
No priority claim is made for the atom, Minkowski sum, equality-half bridge,
or this single-source census. Teammate results were read to respect
ownership, not independently reproduced in this researcher lane.
