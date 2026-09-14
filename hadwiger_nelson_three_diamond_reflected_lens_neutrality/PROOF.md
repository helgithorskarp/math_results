# Exact proof

This interaction starts from the independently reviewed eight-point induced
core with internal vertices `P1,P2` and marked terminal edges

```text
E0=X0Y0, E1=X1Y1, E2=X2Y2.
```

Write `s=sqrt(3)` and `y^2=(4-s)/2`; all source coordinates lie in
`Q(s,y)`.  For every `a` on `E0` and `b` on `E1`, both `a,b` are unit
neighbours of `P1`.  The reflection of `P1` through the midpoint of `ab` is

```text
R1(a,b)=a+b-P1.
```

The two unit circles centred at `a,b` are interchanged by that reflection, so
`R1(a,b)` is their other common unit neighbour.  Adjoin all four choices.
Do the same for `E1,E2` around `P2`, giving four points `R2(a,b)`.

Exact enumeration of all 120 unordered squared distances proves that the 16
formal addresses are distinct and induce 35 unit edges.  No added point
collides with or is unit-separated from `P1` or `P2`, and none equals either
deleted outer cap.  Thus every new source-to-interaction incidence uses a
marked terminal, as required.

## The relation cannot weaken

The original eight-point core is an induced subgraph.  Its two internal
vertices already force

```text
palette(E0) intersects palette(E1),
palette(E1) intersects palette(E2).
```

Hence the interaction relation is contained in the 52-pattern input relation.

## Every input pattern still extends

Consider one adjacent pair of terminal edges `A=a0a1`, `B=b0b1` and its four
new vertices `rij=ai+bj-P`.  The complete edge reconstruction shows that the
`rij` form the four-cycle

```text
r00-r01-r11-r10-r00,
```

with `rij` additionally adjacent to `ai,bj`.  The two reflected-lens blocks
have no edges between their new vertices, so they may be coloured
independently after the terminals are fixed.

Suppose first that the two terminal-edge palettes are the same.  Colour the
opposite vertices `r00,r11` with one colour outside that palette and
`r01,r10` with the other.  Every terminal incidence and cycle edge is proper.

Otherwise the palettes intersect in exactly one colour.  Relabel and orient
the endpoints so that

```text
colour(a0)=colour(b0)=c,
colour(a1)=a, colour(b1)=b,
```

where `a,b,c` are distinct, and let `d` be the fourth colour.  Then

```text
colour(r00)=a, colour(r01)=d,
colour(r10)=b, colour(r11)=c
```

is proper on all incidences and on the four-cycle.  Applying this construction
to `E0,E1` and independently to `E1,E2` extends every input pattern.

Therefore the complete relation is unchanged: all 52 canonical and all 1,200
named input assignments extend, and the interaction forbids no new pattern.

Finally, `P1,X0,Y0` is a unit triangle and the certificate supplies a proper
three-colouring of the complete 35-edge graph.  Its chromatic number is
exactly three.  This is a neutrality theorem for one exact physical
interaction, not a record construction or a broader family exclusion.
