# Every direction of a 72-point line-free set has a four-point line

**Theorem.** Let S be a 72-point subset of AG(3,5) containing no complete
affine line. Every one of the 31 directions has a line meeting S in
exactly four points. Moreover, at least 50 affine planes meet S in 16
points, and these planes, completed projectively, cover every point of
PG(3,5) at least twice.

This is a necessary condition on **all** possible 72-point sets. It does
not establish their existence or nonexistence. The numerical bounds remain
70 <= r_5(F_5^3) <= 72. The theorem excludes the entire family admitting a
direction with at most three selected points per line, with no restriction
on the locations of the deficient fibers.

We use the previously established [upper bound 72](../upper_bound72.md),
its two planar ingredients (a line-free planar set has at most 16 points;
a 12-point planar set contains a four-point line), and the classification
of strong (3 mod 5)-arcs by Kurz, Landjev and Rousseva [KLR].

## 1. A sparse direction gives a small strong arc

Suppose a direction P has all 25 fibers of size at most three. Complete
AG(3,5) by the empty plane H_infinity, and adjoin its point P to S. The
resulting projective set A has size 73. Every plane contains at most 16
points of A. Indeed, a plane through P has at most 15 affine selected
points, and all other planes use the planar bound.

The deficits of the 25 fibers from size three sum to three. Thus every
affine plane parallel to P contains between 12 and 15 points of S; its
projective completion has 13 through 16 points of A. A plane not through
P has at least 8 points, since its four affine parallel companions contain
at most 16 each. Such a plane cannot contain exactly 12 points: a four-point
line in it would give the pencil inequality

    73 + 5*4 <= 12 + 5*16,

which is false. Consequently the plane sizes in A belong to

    {1, 8, 9, 10, 11, 13, 14, 15, 16},

with the unique 1-plane being H_infinity.

For a dual point H, define J(H) = (16 - |A intersect H|) mod 5, with values
0,1,2,3. The six planes on each primal line have total intersection
73 + 5*|A intersect line|. Thus every dual line has weight 3 modulo 5:
J is a strong (3 mod 5)-arc. Let Q be the dual point of H_infinity and F
the dual plane of P. Then J(Q)=0, Q belongs to F, and J(F)=18. For the last
identity, the 31 plane sizes through P sum to 6*73+25=463; their raw
deficits sum to 31*16-463=33. Only H_infinity requires subtracting 15 on
passing to residues.

Let L count planes of A with size 8,9,10 or 11. Each belongs to one of the
25 ordinary affine parallel classes, and each such class contains at most
one of these planes. Summing all dual multiplicities gives

    |J| = 218 - 5L.

We need L >= 12. Counting unordered pairs in all projective planes gives
15768. There are six parallel classes of affine planes parallel to P;
their A-sizes sum to 77 and their pair count is at most 558 per class. Each
of the other 25 classes has total 72, excludes size 12, and contributes at
most 487 if it contains no low plane and at most 508 otherwise. Hence

    15768 <= 6*558 + (25-L)*487 + L*508,
    245 <= 21L,
    |J| <= 158.

`verify.py` checks the complete integer profile lists and these extrema.
[KLR, Theorem 5.2] therefore leaves: full-plane support; a lifted arc with
planar base of size 18,23 or 28; or exceptional size 128 or 143. The base
size list follows from |J|=5m+3, m=3 mod 5, and the planar lower bound
6m >= 31*3. No classification of strong (4 mod 5)-arcs is assumed.

## 2. Full support, base 18, exceptional 143 and base 28

If J supports a full dual plane, let X be its primal point. All planes
through X contain at most 15 points of A. Since J(Q)=0, X is affine.
The pencil inequality forces every line through X to contain at most three
points of A. X cannot already be in A, since then |A| <= 1+31*2=63.
Adjoining X gives a projective 74-set with all plane sizes at most 16.
Its affine subset S union {X} has 73 points and is line-free: a five-point
line would force a pencil sum 73+25>96. This contradicts the established
upper bound 72. Every lifted base-18 type has a fully supported line
[KLR, Table 4], and thus also belongs to this excluded case.

For the remaining types let u,v,w,z count the 8-,9-,10-,11-planes. If
lambda_i counts dual points of multiplicity i, write

    B = 120*(lambda_0-1) + 105*lambda_1 + 91*lambda_2 + 78*lambda_3.

The subtraction of one removes Q, whose actual plane size is one. Plane
pair counting gives

    u+v+w+z = L,
    3u+2v+w = 13L - (B-15768)/5 =: C.

Each 8-plane belongs to a parallel profile (8,16,16,16,16), so it requires
a distinct A1 line through Q, with dual multiplicities (3,0,0,0,0,0).

For exceptional size 143, lambda=(65,65,0,26), L=15 and C=42. Here v=0,
so C <= 2u+L forces u>=14. Every possible zero point Q has only six A1
lines, a contradiction. For the lifted base 28, lambda=(75,50,0,31),
L=15 and C=39 force u>=12, but each zero point has only eleven A1 lines.
The checker verifies all 65 and 75 zero points, respectively. The
exceptional matrix comes from [KLR, Theorem 5.2]; the unique base-28 type
is the conic construction in [KLR, Table 6]. Both identifications use the
published classification after direct checks of the required properties.

## 3. An exact reconstruction constraint

Let D be the set of dual points representing low planes (sizes 8 through
11). It avoids F. Lines through Q contained in F all have weight three.
Among the other lines through Q, a weight-three line contains exactly one
point of D, and a weight-eight line contains none. These are disjoint
five-point choice sets after removing Q. There are L such choice sets.
Also J(D)=C by the preceding moment identity.

For any dual plane G corresponding to a primal point X, put w_G=J(G).
Inverting the point-plane incidence count yields

    25*1_A(X) = 58 - w_G - 15*1_{Q in G} - 5*|D intersect G|.       (1)

Indeed, raw plane sizes are 16-J(H), except that H_infinity requires a
subtraction of 15 and each point of D requires a subtraction of five.
The sum of actual plane sizes through X is 6*73+25*1_A(X).

Since A has exactly P on H_infinity, equation (1) imposes:

* for G=F: |D intersect G|=0;
* for Q in G, G different from F: |D intersect G|=(43-w_G)/5;
* for Q not in G: |D intersect G| is either (58-w_G)/5 or (33-w_G)/5.

These are necessary conditions, sufficient for the exclusions below.
The checker verifies the underlying incidence identity: each point is on
31 planes and each pair is on six planes.

## 4. Exceptional 128: all 320 flags excluded

This type has lambda=(80,40,20,16), L=18 and C=38. There are exactly 320
flags (Q,F) with J(Q)=0, Q in F and J(F)=18. No symmetry reduction is used.
For every flag the 18 choice sets have multiplicity patterns

    6 copies of (3,0,0,0,0),
    9 copies of (2,1,0,0,0),
    3 copies of (1,1,1,0,0).

Their maximum selectable total weight is 39. To obtain 38, either one of
the nine second-type choices drops from two to one, or one of the three
third-type choices drops from one to zero. The number of candidates is

    9*3^3 + 3*2*3^2 = 297.

`verify.py` enumerates every candidate and checks (1). All 320*297=95,040
fail. The published uniqueness theorem identifies the directly checked
128-matrix from the parent directory with the required exceptional arc.

## 5. Lifted base 23: all 450 flags excluded by checked SAT proofs

The unique planar base has multiplicities (18,6,4,3). `base23.json` gives
one explicit representative, directly verified to have size 23 and all
line weights congruent to three. The resulting lift has size 118, L=20,
C=34, and 450 admissible flags (Q,F).

The checker constructs 24 invertible monomial automorphisms of the base,
extends them to four coordinates, and adds three shears and one nonzero
coordinate scaling. It explicitly checks all 28 transformations on every
projective point and plane. A breadth-first orbit computation on **all 450
flags** gives the following exhaustive cover. Completeness of the full
automorphism group is neither claimed nor needed.

| Representative point, plane indices | Flags covered | Result |
| --- | ---: | --- |
| (16,16) | 30 | DRAT verified UNSAT |
| (16,66) | 120 | DRAT verified UNSAT |
| (61,51) | 120 | DRAT verified UNSAT |
| (61,71) | 120 | DRAT verified UNSAT |
| (61,91) | 60 | DRAT verified UNSAT |

Indices use the normalized lexicographic projective coordinates in
`../projective.py`. Each CNF has 100 D variables, one choice per slot,
and all constraints (1). Two allowed intersection counts are encoded by
a fresh selector gating exact cardinalities. Invalid counts force the
selector away from that choice. Totalizer auxiliaries are existential.
Each formula has 48,401 variables and 152,826 clauses. Every geometric
reconstruction supplies an assignment to the D variables and cardinality
selectors, and every permitted cardinality has an auxiliary extension.
Thus a checked contradiction excludes its entire flag orbit.

Kissat 4.0.4 found UNSAT in all five cases. DRAT-trim independently checked
each binary proof. Original proof sizes, hashes, commands and checker
results are recorded in `certificates.json`. Bulky proofs and CNFs remain
outside Git; `replay.py` regenerates them and checks newly produced proofs.
All alternatives in Section 1 are now excluded.

## 6. Covering consequence and number of 16-planes

Every projective point X lies on a four-point line of S. For X at infinity,
this is the theorem just proved. For affine X in S, otherwise the 31 lines
through X would give |S|<=1+31*2=63. For affine X outside S, the absence
of a four-point line would let us adjoin X, contradicting the upper bound
72. The six planes through such a four-point line have total intersection
72+20=92. If at most one were a16-plane, their total would be at most
16+5*15=91. Thus every projective point belongs to at least two completed
affine16-planes.

For every possible parallel profile p summing to 72 with entries 8 through
16, let t(p) be its number of 16s and b(p) its number of within-plane pairs.
The complete 18-profile list satisfies 2b(p)<=972+11t(p). Summing over 31
classes gives 11a_16>=540, so a_16>=50.

## Reproduction and trust boundary

Python 3.10+ suffices for the finite structural checks:

```sh
python3 verify.py --compare finite_expected.json
```

For the five proof computations, install `python-sat==1.9.dev15`, build
Kissat and DRAT-trim, and provide their executable paths:

```sh
python3 replay.py --out /tmp/linefree72-sparse \
  --kissat /path/to/kissat --drat-trim /path/to/drat-trim
```

The original run used Python 3.11.2, Kissat commit
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and DRAT-trim commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` (C compiler GCC 12.2, `-O2`).
Original checker times were approximately 44–63 seconds per case.
The finite enumeration takes a few seconds. Proof hashes can vary with a
different solver build; validity is determined by DRAT checking, not hash
agreement. The generator's CNF hashes are deterministic with the pinned
PySAT version.

The trust boundary is the written reduction, the imported upper bound and
KLR classification, exact Python enumeration, cardinality encoding, and
DRAT-trim. The checker does not re-prove the published classification and
this is not a proof-assistant formalization. The finite checker alone
explicitly reports that SAT certificates are still required.

[KLR] Sascha Kurz, Ivan Landjev, Assia Rousseva, *Classification of (3 mod 5)
arcs in PG(3,5)*, Advances in Mathematics of Communications 17(1) (2023),
172–206. [Primary paper](https://doi.org/10.3934/amc.2021066),
[version used, arXiv:2108.04871v2](https://arxiv.org/abs/2108.04871v2).
The original line-free frontier and planar ingredients are in Christian
Elsholtz et al., *Maximal line-free sets in F_p^n*, Periodica Mathematica
Hungarica 90 (2025), 7–21,
[DOI](https://doi.org/10.1007/s10998-024-00617-x).
