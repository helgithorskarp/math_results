# Proof of the large-`h` order-`2h+2` classification

## 1. Statement

Let `H=K_(n1) square ... square K_(nd)` be a finite Hamming graph. A coordinate line is obtained by fixing all but one coordinate. Let `h>=6`, and suppose `C subset V(H)` satisfies

```text
|C|=2h+2,                 delta(H[C])>=h.             (1)
```

Then one of the following holds.

- **(L)** `C` lies on one coordinate line.
- **(E)** `C` is the union of two vertex-disjoint `(h+1)`-point subsets of distinct coordinate lines; cross-edges between the subsets are allowed.
- **(U)** `C=L union R`, where `L` is an `(h+2)`-point coordinate-line subset, `R` is an `h`-point subset of a distinct coordinate line, and every point of `R` has a neighbour in `L`.

Conversely, each displayed form satisfies (1). Form (U) lies in a coordinate two-flat. A connected set satisfying (1) but lying in no coordinate two-flat is therefore of form (E), with different line directions and one cross-edge in a third direction.

## 2. Two elementary facts about Hamming lines

Every clique of order at least three in a Hamming graph lies on a coordinate line. Indeed, if two neighbours of a vertex differ from it in different coordinates, then they differ from one another in two coordinates and are nonadjacent.

A point outside a coordinate line has at most one neighbour on the line. This follows by comparing its fixed coordinates with those of the line.

## 3. The shell inequality

Fix `v in C`. Let `a_i` be the number of neighbours of `v` in `C` in coordinate direction `i`, and set `A=sum_i a_i`. A direction-`i` first-shell point already has `a_i` neighbours among `v` and the other selected points on that line. It therefore needs at least `h-a_i` selected second-shell neighbours.

Every second-shell point is adjacent to at most two first-shell points. Double-counting these incidences gives

```text
|C| >= 1+A+(1/2) sum_i a_i(h-a_i).                  (2)
```

## 4. Some line contains at least `h+1` selected points

Assume instead that every selected line has at most `h` points. Then each positive `a_i` is at most `h-1`.

If `A>=2h-1`, then `a_i(h-a_i)>=a_i`, and (2) gives

```text
|C| >= 1+3A/2 > 2h+2,
```

a contradiction. Thus `A=h+t` for some `0<=t<=h-2`.

For fixed `A`, the right side of (2) is minimized when `sum_i a_i^2` is maximized. Capped majorization gives the maximizing profile

```text
(h-1,t+1,0,...,0).
```

Substitution in (2) yields

```text
|C| >= 2h+t(h-t)/2.                                  (3)
```

If `1<=t<=h-2`, then `t(h-t)>=h-1>=5`, contradicting `|C|=2h+2`. Hence `A=h`.

Among partitions of `h` with largest part at most `h-1`, `(h-1,1)` uniquely maximizes the sum of squares. The next profile in the majorization order is `(h-2,2)`, whose shell penalty is `4h-8`. Any profile other than `(h-1,1)` would give

```text
|C| >= 1+h+(4h-8)/2 = 3h-3 > 2h+2,
```

because `h>=6`. Therefore every vertex has profile `(h-1,1)`.

Each vertex consequently lies on a unique selected `h`-point coordinate line. Two such lines cannot meet, because their intersection vertex would have two directions containing `h-1` neighbours. The lines partition `C`, forcing `h` to divide `2h+2`, which is impossible for `h>=3`. The assumption was false.

## 5. The maximum-line split

If `H[C]` is disconnected, every component has at least `h+1` vertices. Equality in the total order forces exactly two components of order `h+1`, each complete. By Section 2 they are coordinate-line subsets, giving (E).

Suppose now that `H[C]` is connected and is not a line. Choose a maximum selected coordinate line `L`, write `M=|L|`, and put `O=C-L`. For every `x in O`, Section 2 gives

```text
h <= deg_C(x) <= 1+(|O|-1)=|O|.
```

Hence `|O|>=h` and `M<=h+2`. Section 4 gives `M>=h+1`, so there are only two cases.

### Case `M=h+2`

Now `|O|=h`, and equality holds throughout the last degree bound. Thus `O` is a clique and every point of `O` has a neighbour in `L`. Section 2 places `O` on a coordinate line, yielding (U).

### Case `M=h+1`

Now `|O|=h+1`. A point of `O` with a neighbour in `L` has at least `h-1` neighbours in `O`; one without such a neighbour has all `h`. Thus every point has at most one non-neighbour in `O`.

The graph `H[O]` is a complete graph with at most a matching removed. Since `|O|=h+1>=7`, it contains a triangle. That triangle lies on a coordinate line. Every other point of `O` is adjacent to at least two triangle vertices, and Section 2 forces that point onto the same line. Thus `O` itself is a line clique, giving (E).

This proves the exhaustive list.

## 6. Incidence between two lines

Let two distinct coordinate lines have directions `i` and `j`.

If `i=j`, a cross-edge forces their fixed tuples to differ in one coordinate. Cross-edges then pair equal varying symbols, so they form a matching and the two lines lie in a coordinate two-flat.

Suppose `i!=j`, and let a cross-edge differ in coordinate `k`.

- If `k=i` or `k=j`, the fixed coordinates agree outside `{i,j}`. All cross-edges form a star, and the lines lie in one coordinate two-flat.
- If `k` is different from both `i` and `j`, the edge uniquely determines the varying symbol on each line. It is the only cross-edge. The union varies in exactly the three coordinates `i,j,k`.

These possibilities, together with no cross-edge, exhaust the coordinate comparison.

In form (U), every point of the smaller line needs a cross-edge. A matching or an appropriately centred star can do this, but both lie in a two-flat; the single-edge pattern cannot cover an `h`-point line. Thus (U) is two-dimensional.

In form (E), connectedness excludes no cross-edge. A matching and a star are two-dimensional. The remaining case consists of different line directions and a unique cross-edge in a third direction, and has essential dimension exactly three.

## 7. Converse and sharpness

Forms (L) and (E) have induced minimum degree at least `2h+1` and `h`, respectively. In (U), points of `L` have at least `h+1` neighbours in `L`; points of `R` have `h-1` neighbours in `R` and at least one in `L`. Hence all forms are `h`-cores.

For every `h`, the sets

```text
L={(a,0,0):0<=a<=h},       R={(0,b,1):0<=b<=h}
```

give the connected three-dimensional form, with the sole cross-edge between `(0,0,0)` and `(0,0,1)`.

Finally, the threshold in the full classification is sharp: `K_4 square K_3` has 12 vertices, minimum degree 5, and maximum selected line size 4, so at `h=5` it is not one of (L), (E), or (U).

## 8. Majority-C consequence

Put `h=s-1`. For `s>=7`, a connected legal minor-box part of order `2s` using three coordinates must be two `s`-point lines in distinct directions joined by a single edge in the third direction. A colour class in a maximum-colour majority-C colouring may be assumed connected: if it is disconnected, assigning distinct colours to its components preserves every same-colour degree and increases the number of colours. Thus this normal form is the only three-minor-coordinate repair at the order-`2s` boundary.
