# Independent proof and strengthening

## 1. Cyclotomic coordinates and the norm form

Let `zeta=exp(2*pi*i/5)` and `q=1/abs(1-zeta)`. Since

```text
1 + zeta + zeta^2 + zeta^3 + zeta^4 = 0,
```

every element of `Q(zeta)` has a unique power-basis expression

```text
x = a0 + a1*zeta + a2*zeta^2 + a3*zeta^3.
```

Put

```text
P = a0*a1 + a1*a2 + a2*a3,
Q = a0*a2 + a0*a3 + a1*a3.
```

Using `2*cos(2*pi/5)=(sqrt(5)-1)/2` and
`2*cos(4*pi/5)=-(sqrt(5)+1)/2` gives

```text
2*x*conjugate(x)
 = R + S*sqrt(5),
R = 2*(a0^2+a1^2+a2^2+a3^2) - P - Q,
S = P - Q.
```

The reviewer uses this Gram form for all physical distance decisions. The
controls independently compare it with direct multiplication in `Q(zeta)` on
all `5^4=625` coefficient rows in `{-2,-1,0,1,2}^4`.

Because

```text
abs(1-zeta)^2 = (5-sqrt(5))/2,
```

two points `q*x` and `q*y` are unit-separated exactly when the coefficient
difference satisfies

```text
R = 5,  S = -1.                                      (1)
```

Golden separation similarly gives `(R,S)=(5,1)`.

## 2. A three-coloring of the localized cyclotomic module

Define

```text
Z_(3) = {m/n in Q : 3 does not divide n}.
```

Coefficient reduction modulo three is well-defined on `Z_(3)`. For

```text
x = a0+a1*zeta+a2*zeta^2+a3*zeta^3 in Z_(3)[zeta],
```

set

```text
c(q*x) = a1 + 2*a2 + a3 mod 3.                       (2)
```

If `q*x` and `q*y` are unit-separated, reduce (1) modulo three. Exhausting
the 81 coefficient rows in `F_3^4` leaves exactly these ten possible residues
for `x-y`:

```text
(0,0,1,2) (0,0,2,1) (0,1,2,0) (0,2,1,0) (1,1,1,2)
(1,2,0,0) (1,2,2,2) (2,1,0,0) (2,1,1,1) (2,2,2,1).
```

The values of the linear form `(0,1,2,1)` on those rows are

```text
1,2,2,1,2,2,2,1,1,1.
```

None is zero. Thus every unit edge has different endpoint colors in (2), so
the entire strict unit-distance graph on `q*Z_(3)[zeta]` is three-colorable.

The five source points with one-based labels `6,3,1,2,5`, in that cyclic
order, form an exact unit `C5`. They all lie in `q*Z[zeta]`. Hence the module
graph is not bipartite and has chromatic number exactly three.

This is an infinite-module statement, but its proof is the displayed norm
identity plus a complete 81-row residue calculation. It is not inferred from
the finite target word.

## 3. Frozen network reconstruction

Write `b=5*zeta^4` and `d_j=zeta^j-zeta^4`. The sixteen source points are
`b+sum epsilon_j*d_j` in the stated source order. The reviewer recovers
exactly 28 unit and 28 golden pairs. Source labels `1,2,3,5,6` form `K5` in
the union of the two distance classes, and the submitted proper five-word is
checked. The unit-only source contains the `C5` above and is exactly
three-chromatic by (2).

For `lambda=-zeta-zeta^3`, multiplication in the power basis is the integer
matrix

```text
(a0,a1,a2,a3) ->
(a1-a2+a3, -a0+a1, a3, -a0+a1-a2+a3).
```

Using this matrix, not a target field routine, the reviewer constructs the
448 grid points indexed by `{0,1,2,3}^3 x {0,...,6}`. Rational independence
of the four `d_j` makes these addresses distinct. The 162 cubes indexed by
`{0,1,2}^3 x {0,...,5}` cover the grid exactly.

In lexicographic order, each nonroot cube shares an already available
eight-point face with the predecessor obtained by decrementing its first
positive coordinate. Every such face has at least two points outside the
fixed base. The base-intersection histogram is

```text
0 points: 160 copies; 1 point: 1 copy; 2 points: 1 copy.
```

The grid and base meet in exactly two points, giving `448+16-2=462` physical
points. The address `(3,3,3,6)` occurs only in the last cube and becomes
canonical point 461.

The reviewer tests all `binom(462,2)=106,491` pairs with the Gram form and
finds exactly 1,532 unit pairs. Its sorted coordinate and edge streams match
the published CSV files byte-for-byte and reproduce their hashes.

Formula (2) gives a proper three-word with frequencies `(154,157,151)` and
SHA-256

```text
3d554880750584f595f70c72c1b76a26d5f64dd7b373973e61645741fae0987a.
```

Together with the unit `C5`, this proves the finite graph has chromatic
number exactly three. The submitted four-word is also checked but is no
longer the sharp certificate.

## 4. Registered-overlay boundary and corollary

The earlier registered family consists of every scale-`phi` or
scale-`1/phi` copy of the source meeting the fixed base twice. The reviewer
independently enumerates source pairs, target pairs, both endpoint orders,
and both orientations in the cyclotomic power basis. It reproduces 5,568
labelled specifications and 328 distinct copies at each scale, with the
published base-overlap histogram. Their union with the base has 1,386 points.

Exactly 406 of the generated network's points are outside that union, so the
target's noncontainment distinction is correct. Nevertheless every overlay
coordinate has power-basis coefficients in `Z_(3)` (in fact denominators
divide 11). Therefore formula (2) colors the entire overlay with three
colors. Since it contains the same base `C5`, its chromatic number is exactly
three. This sharpens but does not invalidate the earlier `chi<=4` theorem.

## 5. Scope

The module theorem applies precisely while all physical points remain in
`q*Z_(3)[zeta_5]`. It says nothing about arbitrary real points, coordinate
fields outside `Q(zeta_5)`, coefficients with denominator divisible by three,
or operations that leave the module. It is a strong exclusion for this
coordinate module, not a global Hadwiger--Nelson bound.
