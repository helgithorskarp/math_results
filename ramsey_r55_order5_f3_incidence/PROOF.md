# Two incidence patterns for the residual order-five action

Let `G` be a graph on 43 vertices containing neither a clique nor an
independent set of order five. Color edges red and nonedges blue. Suppose
an automorphism has cycle type `1^3 5^8`. Write its fixed vertices as
`x,y,z` and its moving cycles as `C_0,...,C_7`.

**Theorem.** The fixed triangle is not monochromatic. After possibly
complementing the entire graph and relabeling the fixed vertices, `xy` is
red and `xz,yz` are blue. For some `h` in `{0,1}`, the numbers of moving
cycles whose red fixed neighbors are the indicated sets are exactly:

| red fixed neighbors | multiplicity |
|---|---:|
| empty set | 1 |
| `{x}` | 1 |
| `{y}` | 1 |
| `{x,y}` | 1 |
| `{z}` | `h` |
| `{x,z}` | `2-h` |
| `{y,z}` | `2-h` |
| `{x,y,z}` | `h` |

In this normalization the fixed vertices have red degrees `21,21,20`.
Without choosing a color, their degree multiset is either `{20,21,21}`
or `{21,21,22}`. The total number of red edges is congruent to `1` or `2`
modulo five. The two incidence patterns are inequivalent under fixed-vertex
permutations, moving-cycle permutations, and global color reversal: in the
`h=1` pattern all eight columns are distinct, whereas `h=0` has repetitions.

These are necessary conditions. Neither value of `h` is excluded here.

## 1. Ramsey bounds and incidence rows

We use the established upper bound `R(4,5)<=25`.
For any vertex, each color neighborhood has at most 24 vertices: within
its red neighborhood a red `K_4` would extend to a red `K_5`, while a blue
`K_5` is already forbidden. The blue case is identical. Thus every red
degree is between 18 and 24.

The smaller bounds used below have elementary proofs. The usual
three-neighbor argument gives `R(3,3)<=6`. In a hypothetical red-triangle-
free, blue-`K_4`-free graph on nine vertices, a red neighborhood is blue
complete, so every red degree is at most three. A blue neighborhood has
neither a red nor a blue triangle, so every blue degree is at most five;
every red degree is therefore at least three. This would be a 3-regular
graph on nine vertices, contradicting the handshake lemma. Hence
`R(3,4)<=9`. The standard vertex recurrence then gives
`R(3,5)<=R(2,5)+R(3,4)<=5+9=14`.

For each fixed vertex `u`, its incidence to a moving cycle is constant,
because the automorphism fixes `u` and acts transitively on that cycle.
If `s_u` moving cycles are red-adjacent to `u`, then

```text
d_R(u) = 5 s_u + t_u,       0 <= t_u <= 2.
```

The degree interval `[18,24]` forces `s_u=4`. Thus each row of the `3 x 8`
binary incidence matrix has weight four.

If two fixed vertices have a color-`c` edge, their common color-`c`
neighborhood has at most 13 vertices. It has neither a color-`c` triangle
nor an opposite-color `K_5`, so the assertion follows from `R(3,5)<=14`.
Consequently at most two moving cycles are common neighbors in color `c`.
Two binary rows of weight four in length eight have equally many common
ones and common zeros. Therefore **every pair of rows has at most two
common ones and at most two common zeros**, regardless of its fixed edge's
color.

## 2. Mixed common-neighborhood cap

Let fixed vertices `u,v` have a color-`c` edge and let `w` be the third
fixed vertex. Consider all moving vertices joined to `u,v` in color `c`
and to `w` in the opposite color. Their induced graph has neither a
color-`c` triangle (which would extend using `u,v`) nor an opposite-color
`K_4` (which would extend using `w`). By `R(3,4)<=9` this set has at most
eight vertices.

It is a union of moving 5-cycles. Hence **at most one moving cycle can
have the incidence pattern `(c,c,1-c)` toward `(u,v,w)`**. No assumption
about the other two fixed edges is needed for this cap.

## 3. The fixed triangle is mixed

Suppose first that the three fixed edges are red. There is no moving
cycle red-adjacent to all three fixed vertices. Otherwise its five
vertices must contain a red edge (they cannot themselves form a blue
`K_5`), and that edge with the fixed triangle would give a red `K_5`.

For each of the three pairs of fixed vertices, the mixed cap bounds by
one the number of cycles red-adjacent to exactly that pair. Thus at most
three columns have two ones, and none has three ones. The total number
of ones in the eight columns is then at most `8+3=11`. But the three
rows each have weight four, giving 12 ones. This contradiction excludes
an all-red triangle. Color reversal excludes an all-blue triangle.

Complementing if necessary and permuting fixed vertices now makes `xy`
the unique red fixed edge.

## 4. Solving the multiplicities

Let `n_A` count moving cycles whose set of red fixed neighbors is `A`.
The mixed cap for the red edge `xy` and the blue edges `xz,yz` gives

```text
n_{xy} <= 1,       n_y <= 1,       n_x <= 1.
```

The row equation at `x` is

```text
n_x + n_{xy} + n_{xz} + n_{xyz} = 4.
```

The first two terms sum to at most two. The last two terms are the
common-one count for rows `x,z`, also at most two. Equality therefore
holds throughout:

```text
n_x = n_{xy} = 1,       n_{xz} + n_{xyz} = 2.
```

The row equation at `y` similarly gives

```text
n_y = 1,               n_{yz} + n_{xyz} = 2.
```

Put `h=n_{xyz}`. The common-one count for rows `x,y` is `1+h<=2`, so
`h` is zero or one. We have `n_{xz}=n_{yz}=2-h`. The row equation at `z`
now gives `n_z=h`, and the total of eight columns gives `n_empty=1`.
This proves the table.

The degrees follow from the row weights and the fixed triangle:
`d_R(x)=d_R(y)=21`, `d_R(z)=20`. Complementation changes the last degree
to 22 and leaves the other two at 21. Every edge orbit outside the fixed
triangle has length five. There is one red fixed edge in the chosen
normalization, so `|E(G)|=1 (mod 5)`; reversal gives `2 (mod 5)`.

## 5. Scope of the finite audit

The proof above is analytic; it does not rely on an exhaustive search,
SAT solver, or a graph catalog. The accompanying programs check the finite
incidence algebra in two ways: all eight-column multiplicity vectors,
and ordered incidence rows after fixing the first row by a column
permutation. They agree on exactly the two displayed equivalence classes.

They also check a limitation of this reduction. Internally, each moving
cycle must be a red `C_5` and a blue `C_5`: its two invariant distance
classes cannot have the same color. For either displayed incidence
pattern, either internal choice on each of any two moving cycles admits
an invariant coloring between those cycles such that their union with
the three fixed vertices (13 vertices in total) has no monochromatic
`K_5`. This is verified directly on all 32 cross words and all five-sets.
The selected words for different pairs need not prevent a forbidden set
that meets three or more moving cycles. Nor does this local check impose
the full 43-vertex degree conditions.

The main imported mathematical input is `R(4,5)<=25`, due to
McKay--Radziszowski,
[*R(4,5)=25*](https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf),
J. Graph Theory 19 (1995), 309--322, DOI `10.1002/jgt.3190190304`.
The smaller Ramsey bounds were proved above. The finite audits rely on
ordinary exact integer computation and Python, not a proof assistant.
