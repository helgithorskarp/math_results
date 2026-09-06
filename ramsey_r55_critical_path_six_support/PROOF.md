# A six-way support obstruction over a fixed eleven-vertex core

This is a finite, conditional extension lemma, not an exclusion of a
43-vertex degree profile, the whole core family, or Ramsey(5,5;43).

## Literal guard and footprint convention

Let K have vertices 0,...,10. Its red edges are exactly

```
01 02 03 04 05 06 07 08 09 0,10
34 35 36 37 45 46 48 57 58 59 67 68 6,10
79 7,10 89 8,10 9,10
```

Here two single digits denote a pair; commas disambiguate vertex 10.
The unambiguous integer-pair list in certificate.json is authoritative.
All other core pairs are blue. Equivalently, 0 is red to every other
core vertex, 1 and 2 are blue to one another and to 3,...,10, and the
blue graph on 3,...,10 has lexicographic eight-vertex edge mask 5388912.
There are 28 red and 27 blue core pairs. No catalogue completeness is
needed: the guard is the literal graph, checked directly.

An outside vertex of type t is red to core u exactly when bit u of t
is one. Name six distinct outside vertices as follows:

| Name | a | b | c | d | e | f |
|---|---:|---:|---:|---:|---:|---:|
| Type | 333 | 359 | 587 | 773 | 1579 | 1583 |
| Local vertex | 11 | 12 | 13 | 14 | 15 | 16 |

These 55 core pairs and 66 contacts fix 121 of the 136 pairs on
17 vertices. The fifteen pairs among a,...,f remain arbitrary.
Let x_uv=1 mean the outside pair uv is red.

## The joint three-outside kernel

For any fixed core and footprint list, consider each five-set with at
most three outside vertices. If its fixed pairs contain both colors,
it cannot be monochromatic. Otherwise, forbid the remaining outside
pairs from all having the common fixed color. With zero or one outside
vertex this is a fixed preflight check; with two it is a unit clause;
with three it is a monochromatic-triangle clause on three shared pair
variables. Duplicate clauses can be removed.

This is equivalent, not merely necessary, to avoiding all K5s with at
most three outside vertices. It makes no statement about five-sets with
four or five outside vertices. Footprints need not be distinct. A fixed
K5 is represented by an empty clause, not silently discarded.

There is also an exact *individual-triple* test. After unary and pair
consistency, the only possible triple conditions prohibit all-red or
all-blue on its three outside pairs. The triple is impossible exactly
when all three pairs are forced to the same color and their common
core neighborhood has an edge of that color. Otherwise one can choose
a mixed pair coloring whenever needed. Choosing such colorings for
different triples independently does not make them agree on shared
outside pairs. This distinction is the obstruction below.

## Fourteen explicit K5 clauses

The complete three-outside kernel for the six types has forty distinct
clauses. Fourteen suffice for a unit refutation. The table gives all
fourteen clauses, grouped by common fixed color; each listed core set
and outside set is an actual monochromatic K5 if the clause fails.

| Core vertices | Outside vertices | Fixed color | Consequence |
|---|---|---|---|
| 0,6,8 | a,b | red | x_ab=0 |
| 0,3,6 | a,c | red | x_ac=0 |
| 1,4,7 | a,d | blue | x_ad=1 |
| 2,4,7 | c,e | blue | x_ce=1 |
| 0,3,5 | e,f | red | x_ef=0 |
| 4,7 | a,b,c | blue | x_ab OR x_ac OR x_bc |
| 4,7 | a,c,f | blue | x_ac OR x_af OR x_cf |
| 0,2 | a,d,f | red | NOT x_ad OR NOT x_af OR NOT x_df |
| 0,1 | b,c,e | red | NOT x_bc OR NOT x_be OR NOT x_ce |
| 0,1 | b,c,f | red | NOT x_bc OR NOT x_bf OR NOT x_cf |
| 4,7 | b,e,f | blue | x_be OR x_bf OR x_ef |
| 0,9 | c,d,e | red | NOT x_cd OR NOT x_ce OR NOT x_de |
| 4,7 | c,d,f | blue | x_cd OR x_cf OR x_df |
| 4,7 | d,e,f | blue | x_de OR x_df OR x_ef |

Start with the five unit clauses. The blue abc clause forces bc red;
red bce then forces be blue; blue bef forces bf red; red bcf forces
cf blue; blue acf forces af red; red adf forces df blue. The blue
cdf and def clauses now force cd and de red. Together with ce red,
these violate the red cde clause. Thus the six types cannot coexist,
even if all other outside edges and all degree constraints are forgotten.

The certificate records thirteen unit assignments and the final
contradiction. A second check exhausts all 32,768 tail colorings against
the fourteen actual K5 witnesses, without relying on the propagation
procedure or a SAT solver.

## Every five types genuinely extend

For each deleted type, keep the other types in ascending order and
label their outside vertices 11,...,15. In lexicographic order on those
ten outside pairs, bit i of the following mask means red:

| Deleted type | 333 | 359 | 587 | 773 | 1579 | 1583 |
|---|---:|---:|---:|---:|---:|---:|
| Ten-edge mask | 230 | 230 | 186 | 220 | 188 | 316 |

Every one of these six complete 16-vertex graphs has no red or blue K5;
the checker tests all 6 times C(16,5)=26,208 five-sets, including those
with four and five outside vertices. All smaller subsets extend by
restriction. Hence this six-type support is minimal under deletion of
an outside type while retaining the whole core.

This is **not** a claim of vertex-minimality on all seventeen vertices,
edge-minimality, or global minimal order. It proves that even all local
forbidden-support tests involving at most five prescribed outside
vertices do not decide extension in general. This statement concerns
local extensions of the literal core, without a prescribed final order
or degree profile; the six 16-vertex witnesses are not 43-vertex witnesses.

## Sound interface cut

Let y_t count vertices of type t and z_t=1[y_t>0]. Under the exact core
guard, every Ramsey extension satisfies

```
z333 + z359 + z587 + z773 + z1579 + z1583 <= 5.
```

Equivalently, at least one of these six multiplicities is zero.
Do not replace the presence indicators by unrestricted integer counts.
In a separately imposed binary-type model y_t is itself a presence
indicator, so the corresponding binary sum cut is valid. No hypothesis
that every type has multiplicity at most one is used in the lemma.

## Relation to the 43-vertex fixture

EXAMPLE43.json contains all six types, so the lemma refutes **every**
choice of its 496 outside-pair colors while preserving its core and
footprints. It does not merely refute the displayed coloring or a
degree-constrained tail. Conversely, removing at least one forbidden
type is only a necessary change, not a certified feasible repair.
