# Proof details

## 1. Exact definition and collision quotient

The EI17 package proves that its 31 unit equations have a unique root `E` in
the supplied rational box, with `e10=(-1,0)` and `e16=(0,0)`. All points used
below are distinct, as certified again from that box.

If four distinct points `a,b,c,d` in the plane satisfy

```text
|a-b|=|b-c|=|c-d|=|d-a|=1,
```

then `a+c=b+d`. Indeed, `b,d` are the two distinct intersections of the unit
circles about `a,c`, and reflection in the midpoint of `a,c` exchanges them.
This includes crossed drawings; distinctness excludes only the collapsed-root
case.

Apply the identity successively to the EI17 cycles

```text
(5,10,16,15), (1,5,15,9), (1,2,11,9).
```

It gives

```text
e15-e5 = e16-e10 = (1,0),
e9-e1  = e15-e5,
e11-e2 = e9-e1.
```

Because `m1-m0=m3-m2=(1,0)`, each of the four EI17 translation pairs
produces two sum-address coincidences. They are the eight two-element classes
in `certificate.json`. There are no further collisions because the rational
enclosure for every pair of chosen class representatives has squared-distance
lower bound greater than zero. Every formal address in a nontrivial class is
equal to its representative by the identities above, so this checks all 119
addresses, not only 111 numerical midpoints.

## 2. The two extra exact unit contacts

For a listed unit four-cycle `(a,b,c,d)`, write

```text
R(a,b,c,d) = e_a + e_c - e_b - e_d = 0.
```

The following six checked cycles telescope:

```text
 R(0,3,12,7)
-R(1,2,11,9)
-R(2,4,8,6)
+R(3,12,16,13)
-R(4,7,14,13)
+R(8,9,11,10)

= e0 + e16 - e10 - e1 - e14 + e6 = 0.
```

Therefore

```text
e0 + (e16-e10) - e1 = e14-e6.
```

The right side is a unit vector because `(6,14)` is a source edge. Replacing
`e16-e10` by either `m1-m0` or `m3-m2` proves the two non-product unit contacts.

All EI17 edges at fixed Moser address and all Moser edges at fixed EI17
address descend to 378 distinct quotient edges. The two contacts above give
380. For every other physical pair, each coordinate differs from its rational
midpoint by at most

```text
R = 10^-18 + 2*10^-50.
```

If the midpoint difference is `(dx,dy)`, the exact squared distance differs
from `dx^2+dy^2` by at most

```text
4*R*(|dx|+|dy|) + 8*R^2.
```

The verifier checks this rational bound on all `binom(111,2)=6,105` pairs.
It excludes every unlisted unit contact and every additional collision.

## 3. Two-terminal relation and chromatic number

For a pair of terminals, colour permutation reduces the possible labelled
patterns to `00` and `01`. An edge permits only `01`; a nonedge in the bare
terminal graph permits both.

Each of the 34 stored words is checked directly on all 380 physical unit
edges. Their combined signatures separate every physical pair, witnessing
`01` in all 6,105 cases. They also assign equal colours to every nonedge in at
least one word, witnessing `00` in all 5,725 cases. Thus the source relation
matches the bare relation for every terminal pair.

A fixed EI17 coordinate yields seven distinct points carrying every Moser
edge. Exhaustion of all 2,187 ternary words proves that fibre is not
three-colourable. A stored proper four-colouring supplies the matching upper
bound, so the complete physical graph is exactly four-chromatic.

## 4. Why the construction stops

The source was selected specifically as a possible forced-equal half. Its
formal order bound was 119, so a two-copy spindle would have been at most 237
points; the actual quotient would improve that to 221 before other mergers.
The complete neutral relation rules out the necessary forced-equal pair.
Nothing in the proof excludes higher-arity forcing, but that was not the
declared bridge and is not inferred from pair neutrality.
