# Every collision orientation of the heptagon–spindle sum is four-chromatic

**Theorem.** Fix exactly the H and M of [PROOF.md](PROOF.md), with 21 and
7 points respectively. For |r|=1, the sum map

```
(h,m) -> h+r*m
```

fails to be injective at exactly the 252 rotations classified in
[CONTACTS.md](CONTACTS.md). Every such sum graph is four-chromatic.
Thus every member of this rotation family with fewer than 147 distinct
points, and every subgraph of such a member, is four-colourable.

This closes **all collision orientations**, including the proposed
nonunit-length collision continuation: there are no additional angles
in that continuation. The proof uses a small exact distance-spectrum
certificate and the previous 252-angle colouring theorem. No old sum
graph or colouring search was repeated, and no new sum graph was needed.

The full rotation family remains open. In particular this does not
settle the injective sums whose extra unit edges arise from unequal
factor lengths. No five-chromatic graph on at most 508 vertices or
record improvement is established.

## Squared-distance spectra and the field obstruction

For a finite point set A, let

```
S(A) = {|a-a'|^2: a,a' in A, a != a'}.
```

The exact spectra satisfy

```
|S(H)|=25,                 S(H) intersect Q = {1},
S(M) = {1,3,1/3,(7+sqrt(33))/6,(7-sqrt(33))/6,
                 (9+sqrt(33))/6,(9-sqrt(33))/6},
S(H) intersect S(M) = {1}.
```

The H spectrum is certified by all 210 unordered pairs. The M spectrum
is certified by all 21 pairs, with multiplicities as follows:

| Squared distance in M | Unordered pairs |
|---|---:|
| 1 | 11 |
| 3 | 2 |
| 1/3 | 2 |
| (7+sqrt(33))/6 | 1 |
| (7-sqrt(33))/6 | 1 |
| (9+sqrt(33))/6 | 2 |
| (9-sqrt(33))/6 | 2 |

There is also a structural explanation for why the nonrational values
cannot coincide. Put K=Q(t), t=exp(pi*i/21), and s=i*sqrt(11). The
previous field-degree proof establishes s not in K and
K(s)=K direct-sum K*s as a K-vector space. Set omega=t^7, so
2*omega-1=i*sqrt(3), and put

```
gamma=(1-2*omega)*s=sqrt(33).
```

In particular gamma is not in K: otherwise division by the nonzero
element 1-2*omega of K would put s in K. Since gamma is quadratic over
Q, this proves K intersect Q(gamma)=Q. H has coordinates in K and K is
closed under complex conjugation, so S(H) is contained in K. The
displayed spindle spectrum is contained in Q(gamma). Any common squared
distance must therefore be rational; the exact H certificate leaves
only 1.

The field argument is uniform. Whenever finite A,B have squared-distance
spectra contained in fields E,F with E intersect F=Q, any equal nonzero
factor lengths have rational squared length. If the two rational
spectra meet only at d, every collision of A+rB uses that squared
length. The field condition alone does not assert that their rational
spectra are disjoint; that finite fact must still be established.

## Collision equivalence and complete coverage

A collision between two different formal sums satisfies

```
h_i+r*m_j = h_k+r*m_l,
h_i-h_k = r*(m_l-m_j).
```

Distinct H and M points imply that both differences are nonzero.
Because |r|=1, they have equal length. The spectrum intersection above
forces both lengths to be one. Conversely, any equal oriented unit
differences related by r yield such a collision. Thus the full collision
set is exactly

```
C = {a*conjugate(b): a in H-H, b in M-M, |a|=|b|=1}.
```

The previous unit-contact theorem proves that C is exactly its 252-angle
set and supplies proper colourings for all 36 C7 representatives. The
new calculation independently compares all 420*34=14280 pairs of
distinct directed difference values. Exactly 1176 pairs have equal
squared norm, all at norm one; their ratios give 252 rotations. Of
these, 168 have six ratio representations and 84 have two. These
multiplicities count distinct directed differences, not all possible
endpoint representations.

The new checker compares every rotation and ratio multiplicity with
the producer. It then reconstructs the sevenfold orbit of every exact
representative in the inherited colouring certificate, checks that
the 36 orbits are disjoint, and compares their union with C entrywise.
Hence this is a complete collision closure, not a check that some
sampled collision placements were in the earlier list.

The inherited theorem gives the following complete collision cases:

| Distinct sum points | Unit edges | Rotations |
|---:|---:|---:|
| 142 | 513 | 84 |
| 143 | 512 | 84 |
| 146 | 523 | 42 |
| 146 | 525 | 42 |

Every graph in these rows has an explicit four-colouring and contains
a translated rotated spindle, so its chromatic number is exactly four.
Restriction of that colouring proves the assertion about subgraphs.
All other rotations give 147 distinct points; their edge sets remain
unclassified here.

## Consequence for the remaining construction route

Any non-four-colourable graph in this fixed rotation family must have
exactly 147 distinct points and a unit edge outside the factor-edge
images. Without such an edge, the injective Cartesian-product XOR
colouring is proper. An extra edge has the form |a+r*b|=1 with both
factor differences nonzero. If their lengths were equal, the spectrum
intersection would make both unit; that is one of the already closed
unit-contact rotations. Thus an unresolved candidate must involve
**unequal factor lengths**.

This necessary condition does not assert that such a candidate exists,
nor that failure of one supplied XOR colouring proves a chromatic lower
bound. It only removes all collisions from the remaining exceptional
rotation search. Translation of the whole sum does not affect these
claims; no new reflection or other-family classification is implied.

## Reproduction and trust boundary

Use Python 3.11.2 (tested), the standard library, assertions enabled and
a full checkout. From this package, choose a fresh external output:

```bash
python3 -B collisions.py --out /scratch/fresh-heptagon-collisions
python3 -B collisions_audit.py --work /scratch/fresh-heptagon-collisions
sha256sum -c SHA256SUMS
```

Expected audit status:
`ONLY UNIT LENGTH IS SHARED; ALL COLLISION ORIENTATIONS ARE CLOSED`.

[collisions_certificate.json](collisions_certificate.json) contains
both complete squared-distance tables and a norm index for every one
of the 231 unordered pairs. Values use the parent's 24-coefficient
basis, with a positive common coefficient denominator reduced by gcd.
[collisions_expected.json](collisions_expected.json) fixes the result
and stream identities; [collisions_validation.json](collisions_validation.json)
records the input hashes and observed timings. Generation took
0.271 seconds and the new audit took 0.457 seconds, in one thread; peak
memory was not measured. The 252-angle ratio
transcript is regenerated locally rather than committed.

The producer uses the parent's cyclotomic-plus-s arithmetic. The checker
imports neither collisions.py nor field.py. It rebuilds H and M using
the previous alternate tensor basis in zeta7, omega6 and w=(1+s)/2,
recomputes all pair norms, and compares every pair label and norm value,
the spectrum multiplicities and the exact radical formula for M. It
checks gamma^2=33 and conjugate(gamma)=gamma and computes the common
norm set directly as well as checking the inputs to the field argument.

It rejects five corrupt certificates: an omitted pair, a changed norm,
a changed multiplicity, a missing rotation and a duplicate rotation.
A two-segment control has common nonunit length two, ensuring that
unit-only intersection is not treated as a universal geometric rule.
The original 36 sum graphs and their colourings were **not** rebuilt:
their four-colourability is an explicit dependency on the previously
published unit-contact theorem, source
`73513299bf4d669ce305a9e4c061fee5f0f7eb93`. To replay that dependency,
use the separate commands in CONTACTS.md.

The new checks are author-run implementations, not a separate-author
review. Exact Python arithmetic and finite-loop correctness, the
inherited field-degree and coordinate arguments, and the previous
colouring certificates remain the trust boundary. No approximate
distance, native solver, timeout or incomplete negative proof is used.

The named target is unchanged. [Parts' paper](https://arxiv.org/abs/2010.12665)
and [Haugland's August 2026 source](https://arxiv.org/html/2608.04542v4)
were checked live on 2026-09-05 for record calibration; the result here
does not improve the 509-vertex record. No priority claim is made for
the elementary field-intersection or sum-collision argument.

Stopping decision: all collision orientations are closed. Any next
phase must address injective sums with mixed contacts at unequal
factor lengths, beginning with a precise bounded reduction and a
go/no-go assessment. That phase has not begun. The old D421 pair
search stays parked and HN-2's Heule517 work remains separate. No
new rotation stratum, enlarged sum or minimization is in progress.


The final relevant Discovery Net refresh reached indexed height 3065.
HN-2's [exact H517 constraint-cost result](../hadwiger_nelson_heule517_cut_cost/README.md),
source `97a3f9e6c24d10c77d096f3001aa64f81e8a08a4`, was inspected. Its
526 fixed necessary constraints have optimum 339 and exactly four
minimum hitting sets; that is not a minimum five-chromatic order or a
closure of H517. Its proposed joint extension relation remains a
separate lane and supplies no premise here.
