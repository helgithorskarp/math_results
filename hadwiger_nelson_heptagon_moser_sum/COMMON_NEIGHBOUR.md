# Common neighbours remove every mixed contact with a unit H difference

**Subsequent factor-exchanged assessment:** [DUAL_NEIGHBOUR.md](DUAL_NEIGHBOUR.md)
verifies the complete H common-neighbour relation and sharpens the
remaining bound to 8484 angles, or 1212 classes under sevenfold rotation.
The necessary-event set remains unenumerated. The earlier milestone
below retains its historical scope and provenance.

**Theorem.** Fix the 21-point H and seven-point M defined in
[PROOF.md](PROOF.md), and let C be the 252 collision rotations closed
in [COLLISIONS.md](COLLISIONS.md). If |r|=1 and

```
|a+r*b|=1,  a in H-H, |a|=1,  b in M-M, b != 0,
```

then r belongs to C. Every such sum graph is therefore four-chromatic.
In particular an injective sum H+rM has no mixed unit edge whose H
factor difference has length one.

The proof is a general common-unit-neighbour lemma followed by a check
of all 21 spindle pairs. It handles all spindle difference lengths
at once. No new sum graph or colouring query was needed. The full
rotation family remains open, and no graph improving the 509-vertex
record is established.

The remaining possible non-four-colourable rotations lie in an explicit
necessary-event set of size **at most 11424**, defined below. This is an
upper bound with duplicates and impossible events still allowed; the
remaining angles have not been enumerated. Each unresolved member
would have 147 distinct vertices and an extra edge using a **nonunit
H difference**.

## General circle-intersection lemma

Let a,u,v be complex numbers of modulus one with u != v, and put b=v-u.
The solutions of |a+r*b|=1 on |r|=1 are exactly

```
r_1=a/u,   r_2=-a/v.
```

Indeed both are rotations, and

```
a+(a/u)*(v-u) = a*v/u,
a+(-a/v)*(v-u) = a*u/v.
```

Both right-hand sides have modulus one. Since a and b are nonzero,
expanding the squared-distance equation gives a line intersecting the
unit circle, so at most two rotations solve it. The two displayed
rotations are distinct unless v=-u. In that antipodal case b=-2u and
the equation gives Re(a*conjugate(r*u))=1. As both factors have modulus
one, this forces r*u=a, proving that the single displayed rotation is
the complete tangent case. The excluded case u=v has b=0 and would
allow every rotation; it cannot be included in this two-root claim.

Now let A,B be finite point sets, let a=h_p-h_q be a unit difference
of A, and suppose distinct m_i,m_j in B have a common unit neighbour
c **belonging to B**. Set u=m_i-c, v=m_j-c and b=m_j-m_i. Each solution
above gives an actual sum collision:

```
r=a/(m_i-c)   => h_p+r*c   = h_q+r*m_i,
r=-a/(m_j-c)  => h_p+r*m_j = h_q+r*c.
```

Thus a mixed unit contact of this kind cannot occur in an injective
sum map. The collision conclusion requires neither a colouring
assumption nor algebraic coordinates.

Membership c in B is essential. Take A={0,1}, B={0,2} and r=-1.
Then |1+r*2|=1 while the sum has the four distinct points {-2,-1,0,1}.
The endpoints 0,2 have the common unit neighbour 1 in the plane, but
it is absent from B. This is only a control showing why the hypothesis
is needed; its sum graph is a path, not a five-chromatic witness.

## Application to the complete spindle pair relation

The exact spindle edges, with the existing labels 0 through 6, are

```
01,02,04,05,12,13,23,36,45,46,56.
```

Twenty of its 21 unordered pairs have at least one common unit
neighbour in M. In particular, all ten nonedges do:

| Nonadjacent pair | All common unit neighbours |
|---|---|
| 0,3 | 1,2 |
| 0,6 | 4,5 |
| 1,4 | 0 |
| 1,5 | 0 |
| 1,6 | 3 |
| 2,4 | 0 |
| 2,5 | 0 |
| 2,6 | 3 |
| 3,4 | 6 |
| 3,5 | 6 |

The only uncovered pair is {3,6}, which is itself a unit edge. For
this pair both a and b are unit differences, so the previous
[unit-contact theorem](CONTACTS.md) puts every contact rotation in C.
For every other pair, the new geometric lemma produces a collision,
and the previous all-collision theorem again puts r in C. This covers
every nonzero M difference and proves the theorem.

The common-neighbour claim is not inferred from graph diameter or a
picture: [common_neighbour_certificate.json](common_neighbour_certificate.json)
lists every spindle pair, whether it is a unit edge, and its complete
common-neighbour set. All 21 rows are checked against exact coordinates.

For additional verification, the producer uses all 84 distinct directed
unit differences of H and, for each of the 20 covered spindle pairs,
its least labelled common neighbour. It generates both explicit roots
and checks the unit equations. There are 20*84*2=3360 such root records.
The alternate-basis audit compares them entrywise and verifies the
corresponding labelled sum collision for every record. The union of
these roots equals C. Equality is extra validation; the subset relation
is sufficient for the new theorem. The exceptional unit pair {3,6}
is handled by the explicitly inherited unit-contact theorem, rather
than counted among these 3360 records.

Unordered spindle pairs suffice in this verification because reversing
b can be absorbed by replacing a with -a, which is also in the complete
directed H difference set. No reflection or unverified point-set
symmetry is used. The actual M has no antipodal endpoint pair relative
to the selected common neighbour; the general tangent case is checked
separately as a small control.

## Smaller necessary-event set

There are 420 distinct nonzero H differences, of which 84 are unit.
The 336 nonunit differences form 168 pairs {a,-a}. Choose one member
from each pair, giving a set D. The code uses lexicographic order in
its fixed coefficient basis, but the proof works with any choice.
M has 34 distinct nonzero directed differences. Define

```
E* = {r: |r|=1 and |a+r*b|=1 for some a in D, b in (M-M) minus {0}}.
```

Each (a,b) supplies at most two rotations, by the same line-circle
argument. Therefore

```
|E*| <= 2*168*34 = 11424.
```

Every unresolved non-four-colourable sum belongs to E*. To see this,
first exclude C by the all-collision colouring theorem. Outside C the
sum map is injective. If it has no mixed unit edges, its unit graph is
the Cartesian product of the two factor graphs, with a proper XOR
four-colouring. Thus a non-four-colourable sum must have a mixed edge.
The new theorem rules out a unit H difference in that edge, leaving
a nonunit difference a. If a is not the chosen member of its sign
pair, replace (a,b) by (-a,-b); the distance equation is unchanged and
-b is still a directed M difference. This gives membership in E*.

In fact every rotation outside E* is exactly four-chromatic, since
every sum contains a translated rotated spindle. Some rotations inside
E* may already belong to C or may be four-colourable for other reasons.
The bound neither asserts that 11424 distinct angles exist nor that
any produces the target graph. No E* roots were enumerated in this
pass. The bound combines the common-neighbour reduction with the
elementary simultaneous-sign symmetry; it is not a census of the
remaining exceptional rotations.

## Reproduction and trust boundary

Use a full checkout, Python 3.11.2 (tested), the standard library and
assertions enabled. From this directory choose a fresh external output:

```bash
python3 -B common_neighbour.py --out /scratch/fresh-heptagon-common-neighbour
python3 -B common_neighbour_audit.py --work /scratch/fresh-heptagon-common-neighbour
sha256sum -c SHA256SUMS
```

Expected audit status:
`ALL UNIT-H CONTACTS REDUCE TO THE CLOSED COLLISION SET`.
[common_neighbour_expected.json](common_neighbour_expected.json) fixes
the counts and hashes; [common_neighbour_validation.json](common_neighbour_validation.json)
records timing and pinned dependencies. Generation took 1.77 seconds
and the alternate-basis audit took 3.33 seconds, each in one thread; peak
memory was not measured. The full 3360-root transcript
is generated locally. Only its hash and the compact 21-pair certificate
are committed.

The producer uses the previous cyclotomic-plus-s arithmetic. The checker
imports neither common_neighbour.py nor field.py. It rebuilds H and M
in the previous alternate tensor basis, determines each common-neighbour
set directly from distances to every third spindle point, and compares
all certificate rows. It reconstructs the two roots independently and
checks every unit equation, root identity and labelled collision. The
root set is compared with the disjoint C7 orbit union of the inherited
colouring certificate. Sign classes are independently counted as
unordered two-element sets, without the producer's coefficient ordering.

Controls cover two distinct roots, antipodal tangency, a zero difference,
a nonunit a, an omitted neighbour, an omitted pair, and the example
where the common neighbour lies outside the factor. Four invalid
inputs or certificates are rejected. These controls do not substitute
for the general circle-intersection proof, which includes all real
rotations and its degenerate cases.

The new checks are author-run implementations, not a separate-author
review. Exact Python arithmetic and finite-loop correctness, the
inherited coordinate-field justification, the stated geometric proof,
and the earlier colouring theorems form the trust boundary. The old
sum graphs and their colourings were not rebuilt. The chromatic
conclusion explicitly depends on the all-collision source
`4ec850c8ba08f8beea0a811c49e3b526aa123e38` and unit-contact source
`73513299bf4d669ce305a9e4c061fee5f0f7eb93`.

The named target and record calibration were checked live on 2026-09-06
against [Parts' paper](https://arxiv.org/abs/2010.12665) and
[Haugland's August 2026 source](https://arxiv.org/html/2608.04542v4).
No record improvement or priority claim for the elementary geometric
lemma is made.

Stopping decision: the common-neighbour reduction and its complete
application to unit H differences are finished. Nonunit H contacts
remain a separate phase. Before graph generation, assess whether the
same lemma with the factor roles exchanged gives a useful further
reduction from H's common-neighbour relation. That incidence assessment
has not been performed here. No next contact class, enlarged sum,
minimization, native query or unfinished proof remains in progress.


The final relevant graph refresh reached indexed height 3083. HN-2's
[complete Heule375 interface](../hadwiger_nelson_heule517_joint_interface/README.md),
source `dfabbb59e9d59215737e0b8e6321ca0f1e6321a9`, was inspected. It
certifies 20 boundary-pattern classes and reduces its fixed-large-block
family to small-block cases; it does not close the full H517 family.
Its proposed selector pilot stays in the separate HN-2 lane and supplies
no mathematical premise here.
