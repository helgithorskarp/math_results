# Complete family and proof

Let red denote the graph edges. Use 43 labelled vertices, root 0, and modules
M0={1,2,3,4}, M1={5,6,7,8}, M2={9,10,11,12}, M3={13,14,15},
M4={16,17,18}. All 18 root-module edges are red. Cross-module edges are
red precisely on the five-cycle 01,12,23,34,40; all other cross-module edges
are blue. Internal module edges and every edge involving vertices 19..42
are arbitrary. The complementary template reverses all specified colors.
These are restrictions on physical pairs, not an automorphism requirement.

There are 129 fixed cross-module edges, of which 65 are red. With the root
star this gives 147 fixed edges (83 red, 64 blue). There are 24 free edges
inside modules and 19*24+C(24,2)=732 other free edges, totaling 756. Every
assignment to these edges is included before the two explicit count filters.

## Elementary exclusion, independent of imported classifications

Call a module active when it contains an internal red edge. Two adjacent
active modules supply a red K4, which the root extends to a red K5. Thus,
if there is no monochromatic five-set, the active modules form an independent
set of C5 and number at most two.

Every inactive module is entirely blue. If two inactive modules are
nonadjacent on the cycle, their union is entirely blue and contains at least
six vertices, hence a blue K5. Thus inactive modules form a clique of C5
and also number at most two. Active and inactive modules cover all five
modules, a contradiction. Complementation proves the other template.
The elementary control enumerates all 32 active/inactive words and identifies
one of these two obstructions for each word.

The five-cycle covering mechanism is related to the earlier h3947
C5[C5] proper-extension obstruction. The present family does not fix that
25-vertex core: its module interiors and all outside attachments are free.
No containment or additive count relationship between the families is claimed,
and no old product-core search is resumed.

## Relation to the accepted global structural base

All completions of the 18-vertex module template are induced-P5-free.
To see this, the intersection of an induced P5 with each module would be a
module of the path. P5 has no proper module of size 2, 3 or 4 (all 25
possibilities are independently checked). Thus a path either lies in one
module, impossible because its size is at most four, or uses one vertex
from each module and induces C5, also impossible.

h4015 says every 18 vertices in either monochromatic neighborhood of a
good43 contain a P5. It therefore selects and excludes this whole family.
The elementary argument and the physical RUP certificate below establish
this particular cut independently. They do not remove the classification
trust boundary from the full h4015 theorem, sharpen its threshold, or
prove an analogous statement for other module templates.

h4009's accepted 390<=e<=513 edge window is retained as a count filter.
The root's chosen-color degree is also restricted to [18,24]. These filters
do not enter the cut proof; it excludes all fillings, including those
outside the filters. Degree conditions for other vertices are not counted.

## Physical proof certificate

The original Ramsey CNF has one variable x_uv for each of the 903 unordered
pairs, with positive meaning red. For each five-set S it contains
`OR(-x_uv : uv in pairs(S))` and `OR(x_uv : uv in pairs(S))`.
Canonical DIMACS variables are 1..903 in lexicographic pair order.

Enumerate all red K4 prohibitions and blue K5 prohibitions on the 18
neighbors, substitute the 129 cross edges, and discard satisfied clauses
and duplicates. This gives 257 clauses on the 24 internal-edge variables.
Each red K4 clause is the substitution of a literal global red K5 clause
on its four vertices plus the root. Each blue clause is already a literal
global five-set clause. TEMPLATE.json records one exact physical source
five-set and color for every distinct local clause.

One CaDiCaL call (seed 0, 100000-conflict/60-second cap) returned UNSAT after
four conflicts. The saved text proof has 19 additions, 92 bytes, SHA256
`069b0646c1c14f7f917a2547b39973f35ff9788793d3a486067ea4fb60c85019`.
Every addition is RUP. It was checked by drat-trim and by an independent
whole-formula bit-mask propagator; no solver is needed for replay.

Let A be the 147 signed fixed-edge assumptions and D their negated
disjunction. For each local proof clause C, map its variables to physical
pairs and add `D OR C`. Start with the 257 full, unsubstituted Ramsey
five-set clauses, with no assumption units. Negating `D OR C` assigns all
of A and negates C, so local RUP propagations replay using the original
physical premises and previous lifted clauses. The final local empty
clause therefore lifts to D. The independent verifier checks each physical
premise literally and replays all 19 lifted additions over 903 variables;
it performs 237 propagated units across the checks.

Vertex permutations and color reversal preserve these implications. The
emitter transports both the premises and every proof addition. Eight
transported proofs (both colors, four embeddings) are checked. This is a
transport of the proved theorem, not eight independent family counts.

## Exact global-family count

For the red template, choose t red root-outside edges, 0<=t<=6. The root
degree is 18+t. The other 732 unknown edges have k red edges, so total red
edges equal 83+t+k. The exact number of complete assignments passing both
filters is

```
N_red = sum(t=0..6) C(24,t) * sum(k=307-t..430-t) C(732,k).
N_total = 2*N_red > 2^750.
```

Complementation maps the edge window to itself because 903-513=390 and
903-390=513, and preserves chosen-color root degree. The two families are
disjoint since all 18 root-star edges have opposite fixed colors. Therefore
the factor two is exact. EXPECTED.json stores the complete decimal integer.
A second implementation multiplies the relevant integer generating
polynomials by Pascal additions and gives the same count.

This is the count for one specified embedding and its complementary color,
not for their union over all embeddings. It counts complete assignments to
physical pairs, not isomorphism classes, unresolved solver tasks or actual
Ramsey candidates. The excluded template still represents a small fraction
of all 43-vertex graphs; the absolute count does not imply practical coverage
of a construction search.

## Measured propagation effect and limits

Under A, direct enumeration of the two Ramsey clauses for each five-set
inside the 19 template vertices finds 22,734 satisfied clauses and 522
remaining clauses. Their unknown widths are 2:117, 3:102, 4:258, 6:45.
The other 1,901,940 clauses have a vertex outside the template. If exactly t
vertices lie outside, at least t*(5-t)+C(t,2)>=4 physical edges are unknown.
Consequently the full 1,925,196-clause Ramsey formula has no initial unit
or empty clause, and basic unit propagation stops without assigning a
physical edge. With D present it detects conflict immediately.

This is the entire measured downstream comparison. Native CDCL already
refuted the compact formula in four conflicts, so a search-time benefit is
not established. No q10 input was opened or run. Its 161 survivors remain
owned and undecided by team-r55-1. No q7-r5 task count changes. The proof is
exact but not proof-assistant formalized; residual trust includes the
handwritten reduction and Python/DRAT implementations, interpreter, OS,
integer and file semantics, and hardware.
