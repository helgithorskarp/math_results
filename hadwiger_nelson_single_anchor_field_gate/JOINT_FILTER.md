# Exact cross-copy filter for the next construction

The individual-copy extension theorem leaves interactions between copies
open. The following elementary geometric lemma gives an exact filter for
the next paired Golomb test; it is not a computation of that paired family.

Let K be the conjugation-stable seed field. Let s,t be positive real elements
of K, with s,t and s/t all nonsquares in K. Write two new points as

```
x = A + B sqrt(s),    y = C + D sqrt(t),
A,B,C,D in K, B and D nonzero.
```

The positive square roots are real. Independent choices of signs are
absorbed into B and D. Put `tr(z)=z+conjugate(z)` and `N(z)=z conjugate(z)`.
Then x and y are distinct. Moreover their distance is one **if and only if**

```
A = C,
tr(B conjugate(D)) = 0,
s N(B) + t N(D) = 1.
```

Thus points in different quadratic extensions can have a unit contact only
when the midpoints of their conjugate root pairs coincide, their displacement
directions are perpendicular, and their squared displacement radii add to one.
Every choice of the two root signs then gives the same unit contact.

## Proof

Since s and t represent distinct nontrivial square classes, the compositum
has K-basis `1,sqrt(s),sqrt(t),sqrt(st)`. Equality x=y would make its nonzero
sqrt(s) coefficient B vanish, a contradiction.

Put H=A-C. Expanding the squared distance gives

```
N(x-y) = N(H) + s N(B) + t N(D)
       + tr(H conjugate(B)) sqrt(s)
       - tr(H conjugate(D)) sqrt(t)
       - tr(B conjugate(D)) sqrt(st).
```

For this expression to equal one, the three nonconstant coefficients vanish.
Under the physical complex embedding, the last says that the nonzero planar
vectors B and D are perpendicular. The other two say H is perpendicular to
both. Therefore H=0. The constant coefficient then gives the stated sum of
squared radii. Conversely the three displayed conditions make the expansion
identically one. This proves both directions.

For the present field K=Q(i sqrt3,i sqrt11,sqrt5), a square root in K of a
positive real element is real, since its physical complex square is positive.
Consequently the existing exact square-root routine on Q(sqrt33,sqrt5)
suffices to distinguish these positive square classes.

## Planned use and boundary

Each retained contact polynomial already supplies its points as

```
A_j = p + (T/2)b_j,
B_j = alpha b_j/(2c),
s = D_contact/3.
```

A paired search can first group square classes. Within one class it must use
full exact collision and distance reconstruction. Across different classes,
this lemma reduces the unit-edge census to equal root-pair midpoints followed
by perpendicularity and radius-sum checks. It does not assert that any such
pair exists among the retained recipes, that two copies are non-four-colourable,
or that this filter by itself rules out the508-point target.

The next colour gate should be a joint list-extension obstruction on at most
18 new vertices, using all their mutual edges. Individual-copy obstructions
cannot occur in the certified boundary class. This paired test is unstarted.
