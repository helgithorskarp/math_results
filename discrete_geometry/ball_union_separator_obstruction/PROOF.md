# A two-disk separator obstruction

All disks below are closed unit disks in the Euclidean plane; vertical bars
denote area. Let the labels be `A,B,C,D`, and put

| Label | Initial center p | Final center q |
|---|---|---|
| A | (-1/5,0) | (-1/1000,0) |
| B | (1/5,0) | (1/1000,0) |
| C | (0,1001/1000) | (0,6/5) |
| D | (0,-1001/1000) | (0,-6/5) |

For a set of labels S, write U_S(p) for the union of its disks.

**Theorem.** Both configurations have four distinct centers and precisely
the same disk-intersection graph: all edges except CD. Nevertheless,

    |U_ABC(p)| - |U_ABC(q)| > 17/500,
    |U_ABD(p)| - |U_ABD(q)| > 17/500,
    |U_ABCD(q)| - |U_ABCD(p)| >= 7/125.

At both endpoints the two three-disk unions intersect in exactly U_AB.
Thus even preserving the overlap graph and strictly decreasing both bag
union areas does not imply that their union decreases when the common
separator consists of two movable disks.

This is a counterexample to that **local-volume-only gluing implication**.
It is not a contraction counterexample: for example, AC's squared center
distance increases from 1042001/1000000 to 1440001/1000000.

## 1. Elementary area facts

Let L(t) be the overlap area of two unit disks whose centers are distance
t apart, 0 <= t <= 2. Slicing the two circular segments gives

    L(t) = 4 integral_[t/2,1] sqrt(1-x^2) dx,
    L'(t) = -sqrt(4-t^2).

In particular L(0)=pi and L(2)=0. Only inequalities for these integrals
will be used; no numerical evaluation of pi or inverse trigonometry is
needed for the proof.

Moving one unit disk a distance h changes the area of its union with any
fixed measurable set by at most 2h. Indeed, after rotating the displacement
to be horizontal, each horizontal section of the newly added part of
the disk has length at most h, and only a vertical interval of length 2
is involved. The removed part has the same area as the added part. The
absolute change of the union area is bounded by either one-sided area.
Moving several disks therefore gives the bound 2 times the sum of their
center displacements, by changing them one at a time.

## 2. An auxiliary configuration with a repeated final center

Fix a=1/5. First use the following auxiliary endpoints:

    p0: A=(-a,0), B=(a,0), C=(0,1), D=(0,-1),
    q0: A=B=(0,0), C=(0,1+a), D=(0,-1-a).

The repetition will be removed in Section 5. In this section put

    F(a) = |U_ABCD(p0)|,
    T(a) = |U_ABC(p0)| = |U_ABD(p0)|,
    S(a) = |U_AB(p0)|.

Let F(0),T(0),S(0) denote the configuration with A=B=(0,0) and
C,D=(0,+/-1). Since C and D meet in only a point, inclusion-exclusion
gives

    F(a)=2T(a)-S(a),       F(0)=2T(0)-pi,
    S(a)=2pi-L(2a).

All identities concern area, so the tangency contributes zero.

## 3. Containment and a bound on the added area

Write B0 for the unit disk centered at the origin. We first show that

    B0 is contained in U_ABCD(p0), and hence F(a)>=F(0).

If z=(x,y) belongs to B0 but to neither shifted central disk, then

    x^2+y^2+a^2-2a|x| > 1.

Using x^2+y^2<=1 gives |x|<a/2. Also

    y^2 > 1-(a-|x|)^2 >= 1-a^2 > 1/4.

Thus |y|>1/2. The unit disk centered at (0,sign(y)) contains z, because

    x^2+(|y|-1)^2 <= 2-2|y| < 1.

The outer disks already occur in F(0), proving the asserted containment.

We next prove

    0 <= F(a)-F(0) <= 2a(1+a)^2 = 72/125.                 (1)

Any newly added point z lies in one of the shifted central disks, outside
B0 and outside both fixed outer disks. Being outside both outer disks
implies 2|y|<x^2+y^2. Being in a shifted central disk implies
x^2+y^2 <= (1+a)^2. Consequently every newly added point lies in the
horizontal strip

    |y| < (1+a)^2/2.

At each height, a central disk translated horizontally by a adds an
interval of length at most a beyond B0. The strip has height (1+a)^2,
so each of the two translations contributes at most a(1+a)^2. Summing
proves (1). No smooth-boundary variation formula is being assumed.

## 4. Opposite signs for local and global changes

For q0 the two outer disks are disjoint and its central pair is one disk.
Put G(a)=|U_ABCD(q0)| and Q(a)=|U_ABC(q0)|. Then

    G(a)=3pi-2L(1+a),       Q(a)=2pi-L(1+a),
    G(0)=F(0),             Q(0)=T(0).

The lens derivative yields

    G(a)-F(0)
      = 2 integral_[1,1+a] sqrt(4-t^2) dt
      >= 2a sqrt(4-(1+a)^2) = 16/25.

Together with (1), this gives the global lower bound

    G(a)-F(a) >= 16/25-72/125 = 8/125.                   (2)

On the other hand F(a)>=F(0) and the inclusion-exclusion identity give

    T(a)-T(0) >= (S(a)-pi)/2
               = 2 integral_[0,a] sqrt(1-t^2) dt
               >= 2a sqrt(1-a^2) = 4sqrt(6)/25.

Also Q(a)-T(0) <= a sqrt(3)=sqrt(3)/5. Hence

    T(a)-Q(a) >= (4sqrt(6)-5sqrt(3))/25 > 1/25.          (3)

For the strict last inequality, both sides of 4sqrt(6)>1+5sqrt(3)
are positive, and their squares satisfy
96 > 76+10sqrt(3), since sqrt(3)<2. Reflection gives the same bound
for the other three-disk bag.

## 5. The nondegenerate rational witness

From p0 to p move C and D outward by epsilon=1/1000 each. From q0 to q
move A and B horizontally by epsilon each. The area perturbation bound
in Section 1 gives:

* A full union changes by at most 4epsilon at each endpoint. Thus (2)
  becomes 8/125-8epsilon=7/125.
* A three-disk bag changes by at most 2epsilon at p and 4epsilon at q.
  Thus (3) becomes the strict bound 1/25-6epsilon=17/500.

These are exactly the inequalities in the theorem. Distinctness and the
unchanged graph can also be read off from the squared distances:

| Pair class | At p | At q |
|---|---|---|
| AB | 4/25 | 1/250000 |
| AC,AD,BC,BD | 1042001/1000000 | 1440001/1000000 |
| CD | 1002001/250000 | 144/25 |

Every distance is nonzero. The first two rows are strictly below 4 and
the last is strictly above 4, as required for unit disks. Since C and D
are disjoint, the set identity

    (U_AB union C) intersect (U_AB union D) = U_AB

holds at both endpoints. All area and distance inequalities have strict
margins, so the qualitative obstruction persists on an open neighborhood
of these two configurations, not only on a symmetric or tangent locus.

## 6. What the obstruction rules out

For any two label bags I,J, put

    V_I=|U_I|, V_J=|U_J|, V_S=|U_(I intersect J)|,
    E=|(U_I intersect U_J) minus U_(I intersect J)| >= 0.

The elementary identity is

    |U_(I union J)| = V_I+V_J-V_S-E.

Write Delta_I=V_I(p)-V_I(q), and similarly for J and S. The full loss is

    Delta_full = Delta_I+Delta_J-Delta_S + E(q)-E(p).

Our witness has E(p)=E(q)=0, Delta_I>0 and Delta_J>0, but
Delta_S>Delta_I+Delta_J. Its failure comes entirely from the moving
separator, even with no extra overlap to track. A singleton separator
made of a fixed-radius ball has Delta_S=0; two movable balls already
allow failure. This is minimal in separator cardinality for this exact
overlap, local-volume-only inference.

Gorbovickis's published divide-and-conquer principle already uses
invariant separator volume, and his Section 2.5 explicitly identifies
the need to compensate a separator deficit. We do not claim this
principle or the qualitative warning as new. The contribution here is
a small rational, robust, quantitatively certified disk realization of
the failure. It does not rule out gluing theorems that use pairwise
contraction, control the separator deficit, or impose other geometric
hypotheses. See REFERENCES.md for attribution and scope.

## 7. Direct exact corroboration

The accompanying verifier bounds each relevant area by a different
method: rational inner and outer rectangles in vertical strips. In a
strip [l,r], a disk centered at (cx,cy) has horizontal distance to cx
between dmin and dmax. Its sections all contain the centered vertical
interval of half-height floor(sqrt(R^2-dmax^2)), when it exists, and are
contained in the interval of half-height ceil(sqrt(R^2-dmin^2)).
Taking unions of the inner intervals and of the outer intervals and
multiplying their lengths by the strip width gives lower and upper
area bounds. Sum over all strips covering the disks' x-extents.

The coordinate scale is 1000000, R=1000000, and strip width is 125 in
integer coordinates. Integer square root and integer interval unions
make all area bounds rational. No sampled-point inclusion, floating
point, pi approximation, or transcendental library is used. The written
proof establishes the theorem independently of these finite checks;
neither proof is formalized in a proof assistant or independently peer
reviewed at publication time.
