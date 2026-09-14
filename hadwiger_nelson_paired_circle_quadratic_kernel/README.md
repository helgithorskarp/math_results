# A quadratic paired-circle kernel without a common centre-neighbour

This package gives an exact strict plane unit-distance graph obtained from two
unit centre segments and the four paired-circle intersection slots.  It has
**50 distinct points**, **144 unit edges**, and chromatic number exactly
**four**.  Unlike the preceding 39-point realization of the same two-variable
phase obstruction, no plane point is at unit distance from all four centres.

The improvement is geometric, not chromatic.  The four marked centres realize
all seven colour patterns allowed by their two disjoint unit edges.  Thus this
kernel has **no stronger four-colour interface than the bare centre graph** and
does not improve the published 509-vertex five-chromatic record.

## Exact placement

Let

```text
omega = (1+i*sqrt(3))/2,
t     = (5+i*sqrt(11))/6.
```

Then `t^2-(5/3)t+1=0` and `|t|=1`.  In slot order `00,01,10,11`, use the
unit directions

```text
u = (1, 1, omega^4, omega^4),
v = (t, omega*t, omega^4*t, omega^3*t).
```

Writing `d_ij=u_ij-v_ij`, take

```text
a0=0,  a1=d00-d10,  b0=d00,  b1=d01.
```

The polynomial for `t` makes both `a0a1` and `b0b1` unit segments and gives
`b1-a1=d11`.  All four cross slots are regular: each pair of centre circles
has two distinct noncentre intersections, and its separation avoids
`0,1,sqrt(3),2`.

The directions lie in exactly two sixth-root orbits, `U` and `tU`.  The four
phase clauses are, up to the displayed variable order,

```text
(X=0 or Y=1), (X=1 or Y=1),
(X=1 or Y=0), (X=0 or Y=0).
```

They have no Boolean model.  Closing the owner-relative intersection
directions under `U`, translating by the two centres in each group, merging
collisions, and rebuilding unit edges from every point pair gives the claimed
50-point graph.

## What is certified

- exact quotient-field coordinates and all-pairs reconstruction of 144 unit
  edges;
- four regular circle-intersection slots and an unsatisfiable two-variable
  phase formula;
- absence of a common plane unit-neighbour of all four centres, by testing the
  only two equilateral completions of the first unit centre segment;
- a proper four-colouring;
- a 7-vertex, 11-edge Moser-spindle subgraph, checked against all `3^7`
  three-colour assignments, proving the graph is not three-colourable;
- direct proper four-colour witnesses for every one of the seven canonical
  terminal patterns, proving the marked interface is exactly the bare
  two-edge interface.

All equality and unit-distance decisions are rational coefficient comparisons
in

```text
Q(sqrt(3),i)[t] / (t^2-(5/3)t+1).
```

The chosen plane embedding sends `t` to `(5+i*sqrt(11))/6`.  The quotient is
faithful because its discriminant is `-11/9`, while `sqrt(-11)` is not in
`Q(sqrt(3),i)`.  The verifier uses an explicit multiplication formula distinct
from the producer's tensor loop and imports no producer module.

## Reproduce

CPython 3.11 or later and the standard library suffice.  From the repository
root:

```sh
python3 -B hadwiger_nelson_paired_circle_quadratic_kernel/make_certificate.py \
  --out /tmp/quadratic-kernel.json
cmp hadwiger_nelson_paired_circle_quadratic_kernel/certificate.json \
  /tmp/quadratic-kernel.json
python3 -B hadwiger_nelson_paired_circle_quadratic_kernel/verify.py --check-expected
python3 -O hadwiger_nelson_paired_circle_quadratic_kernel/verify.py --check-expected
(cd hadwiger_nelson_paired_circle_quadratic_kernel && sha256sum -c SHA256SUMS)
```

Expected certificate SHA-256:

```text
524dda10b44183ada83e34e2bc17737357db18f0ee5f02711c26c5c909e0e3e1
```

## Scope

This is a new exact physical forcing core and a negative interface gate.  It
is not an abstract-only graph, an approximate embedding, a five-chromatic
construction, a global Hadwiger--Nelson bound, or a classification of all
paired-circle placements.  The absence of a common centre-neighbour does not
by itself turn the coupled phase obstruction into an unrestricted four-colour
obstruction.
