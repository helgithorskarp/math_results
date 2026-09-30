# Exact hitting-set proof and the fractional obstruction

Use the definitions in [README.md](README.md). Every original nonpole,
monochromatic seven-term AP of color `c` must contain an edit in `E_c`:
otherwise the candidate keeps that AP monochromatic. Only this necessary
condition is used. All progressions here have positive integer difference
and seven distinct positions. Coordinates are zero-based; translation by
one gives the domain `[1,3704]`.

## The eligible-position reduction

The included earlier certificate has denominator `D0=1,000,000`, common
capacity numerator `u=10,525,183`, and total AP weight numerator
`S=2,117,421,325` in each original-color class. Its actual point load
`ell(x)` is at most `u` inside `B=[1287,2417)` and at most `u+D0` outside.
The base checker proves primality of 617 by trial division, evaluates
Euler's criterion, checks every weighted AP, and checks both classes'
point capacities. No exhaustive enumeration is needed for this positive
weight certificate.

Define the nonnegative integer capacity defect

```
d(x) = u + D0*1{x outside B} - ell(x).
```

Hitting each weighted AP and double counting gives

```
S <= sum_{x in E_c} ell(x)
  = u*e_c + D0*f_c - sum_{x in E_c} d(x).
```

Assume, for a contradiction, `e_c<=196` and `f_c<=55`. Then

```
sum_{x in E_c} d(x) <= delta
delta = 196*u + 55*D0 - S = 514,543.
```

Every selected point therefore has `d(x)<=delta`. Put
`V_c={nonpole x:T(x)=c, d(x)<=delta}`. Exact scanning gives 881 eligible
points per class, 470 inside `B` and 411 outside, from 1,849 nonpole points
per class. Each original monochromatic AP `A` has a necessary screened
petal `P_A=A intersection V_c`, and `E_c` must meet that petal. The screen
is conditional on **both budgets**; it must be recomputed if either is
enlarged.

## Three APs force two edits

For three required nonempty petals `P_1,P_2,P_3` with empty common
intersection, an integer hitting set must select at least two points from
their union `U`. Zero selected points hits none; exactly one would have to
belong to all three petals, contradicting the empty common intersection.
Thus `|E_c intersection U|>=2`. Points in the union are counted once.
No pairwise-disjointness assumption is required.

The new certificate has denominator `D=1,000,000`, positive weights on
835 original AP petals, and these six cover-two unions:

| Three original APs `(start,difference)` | Union size | Weight numerator |
|---|---:|---:|
| (1042,234), (1408,285), (852,424) | 7 | 396745 |
| (235,278), (167,434), (357,495) | 7 | 2535134 |
| (875,257), (423,483), (237,545) | 7 | 4845430 |
| (1260,365), (150,460), (160,550) | 8 | 1129222 |
| (38,364), (1130,364), (766,455) | 11 | 1565752 |
| (1556,142), (988,284), (562,355) | 10 | 171331 |

Each listed AP is independently checked for actual crossing coordinates,
positive difference, nonpole membership, and original monochromatic color.
Each three-petal common intersection is checked empty. The cover-two
weight contributes twice its numerator to the required total, while its
union contributes its numerator once to each point load.

Let `W` denote AP weight plus twice cover-two weight. The exact totals are

```
W = 2,170,946,248,
mu = 10,795,327,
W - 196*mu = 55,062,156,
W - 196*mu - 55*D = 62,156 > 0.
```

Every eligible point load is at most `mu` inside `B`, and at most `mu+D`
outside. The weighted hitting and cover-two inequalities imply

```
W <= sum_{x in E_c} new_load(x)
  <= mu*e_c + D*f_c
  <= 196*mu + 55*D < W,
```

the required contradiction. Therefore `e_c<=196` implies `f_c>=56`.
The rational strict gap is `62,156/1,000,000 = 15539/250000`. The proof
does not extrapolate these capacities to a larger edit budget or screen.

## Reflection and the other original color

The reflection `R(x)=3703-x` has no fixed integer point and interchanges
the flanks. Because `t=1-s`, reflected residues negate the original
residues. Euler's criterion gives `q(-r)=q(r)` for prime `617=1 mod 4`;
flank complementation then gives `T(R(x))=1-T(x)`. The band `B` is
reflection-invariant. A progression `(a,d)` reflects to
`(3703-a-6*d,d)`, preserving positive difference and point count.

The checker constructs and checks every reflected AP and cover triple,
and verifies pointwise reflected eligibility and both sets of capacities.
It checks 1,706 AP instances and 11,942 original incidences in the new
proof. This transfers the necessary inequality to color 1 for any
candidate; **the candidate need not be reflection-symmetric**. No bound
on the other class's edits is used when proving a particular class bound.

## A feasible fractional relaxation at the excluded integer budget

Replace `1{x in E_0}` by a rational `z_x` in `[0,1]`. Set `z_x=0` off
`V_0`. Retain every original color-0 monochromatic AP inequality
`sum_{x in A} z_x>=1`, exact class/far sums `196` and `55`, and the
aggregate defect inequality `sum_x d(x)z_x<=delta`. These are all
necessary linear conditions for any integer hitting set with the stated
budgets, after applying the rounded far bound of 55. They need not be
sufficient for an integer hitting set or for any AP-free coloring.
The exact budgets follow for any hypothesized integer hitting set:
the base cut gives `f_c>=55` when `e_c<=196`, and
`S-195*u=65,010,640>55*D0` rules out `e_c<=195` when `f_c<=55`.
Thus its class/far counts would have to equal 196 and 55.

The included [fractional certificate](certificates/fractional-phase184-far55.json)
uses denominator `Q=100,000,000` and 841 positive weights, all strictly
between zero and one. Every weight is attached to an eligible actual
position. Exact checking gives

```
sum z_x = 196,
sum_{x outside B} z_x = 55,
min_A sum_{x in A} z_x = 100000001/100000000,
sum d(x)z_x / D0 = 322436412603/50000000000000
                      <= 514543/1000000 = delta/D0.
```

The fractional checker enumerates all 1,141,450 positive-difference
integer seven-term APs in `[0,3704)`. Exactly 3,065 are original-color-0
nonpole monochromatic APs; all cross the seam, and every one meets its
fractional covering inequality. No private instance or numerical solver
is used for this check.

This witnesses feasibility of the **stated** original-AP relaxation,
including eligibility and aggregate defects. It does not rule out other
linear formulations with additional integer-valid cuts. In particular,
the three-petal inequalities above hold for integer hitting sets but can
fail for this fractional point. They are the additional ingredient in
the new certificate. The proof yields no integer repair witness.
The complete entry-level comparison in `expected.json` verifies that
this fractional point violates all six positive-weight cover-two cuts.
For example, the first union has fractional weight
`95275713/50000000=1.90551426<2`.
