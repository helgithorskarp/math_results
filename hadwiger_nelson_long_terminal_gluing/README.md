# Four-colour extension for terminal-only assemblies of the 159/214 gadgets

**Theorem.** Every terminal-only assembly of the two specified Parts gadgets
on at most **508 vertices** is four-colourable. Copies may independently
rotate, reflect and translate through arbitrary real isometries. The theorem
is proved by a geometric degree bound and five exact positive colouring
certificates. No placement enumeration or negative SAT premise is used.

The restriction **terminal-only** is essential: shared vertices must be
terminals of every copy containing them, and every unit edge not already
internal to a copy must join designated terminals. The theorem does not
exclude unrestricted unions of these gadgets, interior contacts, additional
connector graphs, reduced gadgets or other terminal sets. It supplies no new five-chromatic
graph and no record improvement.

## Specified graphs and positive terminal extension

Let A and B be the strict unit-distance graphs of the archived
[159-point](../hadwiger_nelson_nonmono159_214_lowden2/points159.tsv) and
[214-point](../hadwiger_nelson_nonmono159_214_lowden2/points214.tsv) coordinate
files. They have 646 and 977 edges respectively. Coordinates in those files
are divided by 12 and use the radical basis
`1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165`.
The relevant entries lie in Q(sqrt3,sqrt11).

Use zero-based indices in file order, with designated terminals

| Graph | Indices | Exact terminal coordinates | Internal terminal distances |
|---|---|---|---|
| A | 141,142,144 | `(1/2,5sqrt3/6)`, `(1,-2sqrt3/3)`, `(-3/2,-sqrt3/6)` | all sqrt7 |
| B | 186,187 | `(3/2,0)`, `(-3/2,0)` | 3 |

The A terminals form the unique centered equilateral sqrt7 triangle in the
specified file. Parts' [paper, Table 1](https://arxiv.org/html/2010.12665v2)
identifies 159- and 214-vertex gadgets for a non-monochromatic sqrt7 triple
and distance-three pair. The archived coordinate provenance is documented
[in the input package](../hadwiger_nelson_nonmono159_214_lowden2/SOURCE.md).
We do **not** need to assume or reprove the advertised exclusion of
monochromatic terminal colourings.

What we verify here is the positive direction:

- Every non-monochromatic four-colouring of A's three terminals extends to A.
- Every assignment of different colours to B's two terminals extends to B.

The [1,100-byte certificate](certificate.json) gives four complete A
colourings with terminal patterns `001`, `010`, `011`, `012`, and one B
colouring with pattern `01`. These represent every non-monochromatic equality
pattern. Renaming the palette covers all 60 labelled assignments for A and
all 12 for B. The checker actually performs every renaming and verifies each
resulting colouring on every strict unit edge. Thus the positive statement
has no colouring-library completeness assumption and needs no claim about
whether the missing monochromatic pattern extends.

## Separation lemma

Let T1,...,Tk be finite terminal sets in the plane, each with at least two
points, and with every within-set distance **strictly greater than 2**.
Sets may intersect. Suppose k is at most three.

Form a finite auxiliary graph on the union T of the terminal sets. Include
all actual unit edges among T. For each Ti, choose any one pair of its
points and add that pair as an auxiliary inequality edge. These chosen
edges encode non-monochromaticity; they are not claimed to have unit length.

For a vertex x, let r be the number of terminal sets containing x.
There are no unit neighbours of x in any such set. Each of the other k-r
sets contains at most one unit neighbour of x: two such neighbours y,z
would satisfy `distance(y,z)<=distance(y,x)+distance(x,z)=2`, contrary to
separation. Even if a neighbour belongs to several sets, this upper bound
remains valid by counting it in the union of those sets. Hence the actual
unit degree of x is at most k-r.

Only one of the r chosen pair edges per containing set can be incident with
x. The auxiliary degree is therefore at most `(k-r)+r=k<=3`. Multiple edges
are identified and there are no loops. Greedy colouring in any vertex order
uses at most four colours. It is proper on every terminal unit edge and
makes each Ti non-monochromatic because its selected pair has distinct
colours. This proves the lemma for **every** placement, including terminal
coincidences. The strict separation is needed for the one-neighbour bound;
at distance exactly two, a midpoint can be a unit neighbour of both ends.

## Lifting to complete gadgets

Here is the exact assembly definition. For finitely many copies indexed by i,
let Vi be the image of the full A or B vertex set, Ti its designated terminal
set, and Ei its strict internal unit-edge set. Let G be the complete unit
graph on `V=union Vi`. Require:

1. For distinct i,j, `Vi intersection Vj` is contained in `Ti intersection Tj`.
2. Every edge of G outside `union Ei` has both endpoints in `T=union Ti`.

The second condition concerns **new** edges only. An inherited internal edge
incident with a shared terminal is already handled within its copy and does
not violate the definition. No extra connector vertices are included.

For at most three copies, apply the separation lemma: their terminal
distances are sqrt7 or 3, both greater than two. Extend the resulting
non-monochromatic colouring of each Ti to Vi using the checked certificates
and palette renaming. The assignments agree on all shared points by condition
1. Each inherited edge is proper in its own copy. Each remaining unit edge
joins terminals by condition 2 and is proper in the auxiliary colouring.
Thus the assembled graph is four-colourable.

It remains to justify why the at-most-508 family cannot contain more copies.
Each A copy has **156 private interior vertices**, and each B copy has **212**.
Condition 1 makes these interiors disjoint from every other copy, so four
copies already contribute at least `4*156=624` vertices. Therefore a
terminal-only assembly with at most 508 vertices has at most three copies.
In fact a three-copy assembly involving B already has at least
`2*156+212=524` private vertices, before counting terminals. Its only
three-copy possibility is A+A+A, whose raw order is at most 477. The preceding
three-copy proof also covers every one- and two-copy choice. This completes
the claimed size-restricted family exclusion. Every subgraph of any covered
assembly is four-colourable by restriction as well.

## Reproduction and independent checks

With Python 3.11.2 and the standard library, from the repository root:

```bash
python3 -B hadwiger_nelson_long_terminal_gluing/build.py --out /tmp/hn-long-terminals
python3 -B hadwiger_nelson_long_terminal_gluing/verify.py --work /tmp/hn-long-terminals
```

The output directory must be new, and assertions must be enabled. The
[producer](build.py) reconstructs both graphs with the pinned eight-component
radical arithmetic and checks the five supplied colourings. The
[separate checker](verify.py) imports no submitted or inherited arithmetic
module. It implements the quadratic tower Q(sqrt3)(sqrt11), independently
parses and checks the coordinates, and compares both complete labelled
point and edge lists entry by entry.

The exact check performs all **35,352** unordered pair tests, checks the
terminal coordinates and distances, checks **3,561** edge inequalities in the
five original witnesses, and checks **50,484** after expanding all 72 labelled
terminal assignments. Five small geometric fixtures exercise **57** choices
of auxiliary pair edges, including shared terminals, coincident terminal
sets and a triangular prism. Controls also check the strict-distance-two
boundary and reject three malformed witnesses or violated premises.
These finite controls validate the implementation; they do not enumerate
arbitrary placements. The universal quantifier follows from the analytic
separation, degree and gluing proof above.

Optional bounded witness rediscovery, after the graph build:

```bash
python -B hadwiger_nelson_long_terminal_gluing/discover.py \
  --work /tmp/hn-long-terminals --out /tmp/hn-long-terminal-witnesses
```

This optional command needs `python-sat==1.8.dev24` (CaDiCaL 1.9.5) and a new
output directory. It reuses two rows from the
[earlier A colouring library](../hadwiger_nelson_nonmono159_moser_triple/colors_A.txt)
and runs exactly three remaining-pattern queries, each bounded by 100,000
conflicts. All three were SAT. The standard exactly-one encoding has four
variables per vertex, one at-least-one clause and six pair exclusions per
vertex, and four equal-colour exclusions per unit edge. Terminal variables
are pinned to the specified pattern. The A and B formulas have respectively
636/856 variables and 3,697/5,406 clauses before terminal assumptions.
Every decoded witness is checked directly. A public-entry-point replay
reproduced the certificate byte for byte; discovery is outside the proof's
solver trust boundary.

[Expected results](expected.json), [validation details](validation.json) and
[hashes](SHA256SUMS) accompany the source. Original discovery took about
0.053 seconds; exact graph generation took about 0.32 seconds and the separate
audit about 0.27 seconds, on one thread. Peak memory was not measured.
The original and public rediscovery each used three native queries; proof
replay uses none. Generated graphs and operational state remain local.

Remaining trust lies in the exact archived coordinate files, independence of
the radical bases, Python integer and set arithmetic, faithful certificate
decoding, complete finite loops and the stated unformalized geometric proof.
There are no floating-point predicates or omitted negative proof traces.
The new checker is an author-run distinct implementation. External review
of this new family theorem is pending; no external acceptance is inferred
from earlier family reviews.

## Construction decision and shared context

Three A gadgets fit the target budget, but their terminal relations alone
cannot create the needed contradiction. Further work should introduce and
test a concrete interaction outside the theorem. One unstarted option is a
seven-point Moser connector with three A copies: its raw bound is
`7+3*159=484`. The first future test should concern its exact terminal/connector
unit-edge graph and compatible colour patterns, before constructing the
large copies. No such placement or interface obstruction is asserted here.

This differs from the earlier
[fixed-Moser three-copy angular exclusion](../hadwiger_nelson_nonmono159_moser_triple/README.md):
that theorem fixes an inner placement and permits all its interior contacts.
Here positions are unrestricted but interactions must obey the stated
terminal-only conditions. Neither family is claimed to contain the other.
The closed heptagon sums are not enlarged.

HN-2's new [H514 interface](../hadwiger_nelson_heule514_interface/README.md)
remains in the separate exact-certification lane: its 258,914 library residuals
are unresolved, not known non-four-colourable graphs. H517's accepted closure
and the parked HN-1 and heptagon-difference families remain undisturbed.
Primary-source calibration on 2026-09-06: Parts' paper gives the 509-vertex
record, and [Haugland's current manuscript](https://arxiv.org/html/2608.04542v4)
still identifies 509 as the record. This negative result does not improve it.
