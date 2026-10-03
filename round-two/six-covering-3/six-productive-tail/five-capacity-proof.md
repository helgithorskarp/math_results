# Auxiliary five-original TAIL footprint bound for literal P

Actual author: **six-covering-3**, role **researcher**, 2026-10-03.
Status: **author-checked computer-assisted auxiliary lemma**.
Every phase and coupled-label record agrees between two integer algorithms,
normally and with-O. Ordinary completeness/CRT/half-fibre bridges are
unformalized; independent review is outstanding. This argument is included in the self-contained six-class proof package.
Public9859 is its separately published prerequisite.

## Statement and dependency scope

Use P=(8:0,9:0,10:1,14:1,12:10), period10080=32*315, BASE period2520,
and the ORIGINAL TAIL labels{16d,32d:d|315}. Original moduli are pairwise
distinct and at least8. BASE is the36 unused original divisors of2520,
including21, with one arbitrary phase or omission each. H is its actual
P/BASE hole set. Productive means hitting at least one physical10080 lift
of a point of H; all TAIL phases/presence remain free.

**If a full covering in this literal domain has exactly FIVE productive
TAIL originals, then |H|<=161. Its two occupied parents cannot both be
odd.** No completed BASE hole-set realizing161 is claimed, no full-P
exclusion follows, and global L_min(8) bounds remain unchanged.

Published9762 gives at least two occupied parents, and
[9859](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-covering-3/five-productive-tail/proof.md)
gives at least127 holes and at leastfive productive originals. Its verified
source is34db30c83087ea64776d3abb8ce0b8b63b172503 and actual graph reference
bafkreiens463ngz5w3jktsb6c2smwdbllhmcesyab7v6ifmlcud7wkes7u.
These published inputs are independently unreviewed. This new upper bound
does not use the private7006-record mixed-support exclusion or a
normalization of every cover toP.

## 1. Complete three-class classification

Each occupied parent needs at least two productive classes: an original16d
hits at most two of a hole's four lifts, and32d hits at most one. Hence
exactlyfive productive originals imply exactlytwo occupied parents, with
a2+3 allocation. The two-class parent uses16p and16q, p!=q, with opposite
phase residues modulo16. Its holes lie in the common projections modulo8p
and8q, an empty set or one class modulo8*lcm(p,q).

In the three-class parent, zero16d labels cannot cover four lifts. The
remaining cases are exhaustive:

1. **One16u and two32v/32w.** Every hole must meet all three projections;
   dropping any class's incidence leaves at mostthree covered lifts. Thus
   holes lie in one common class modulo8*lcm(u,v,w). The two32 phases must
   occupy the two distinct binary positions opposite the16 half. In the
   resource enumeration p,q,u are distinct; v!=w. A32d and16d are DIFFERENT
   original moduli, so v/w may equal p,q oru.
2. **Two16 labels and one32 label.** Every hole must meet both16 labels,
   and their phases must occupy opposite halves. The32 class cannot extend
   the hole set repaired by that pair. Across the two parents the four16
   labels are distinct, so the published ordinary four-class capacity bound
   is126. It contradicts |H|>=127; this case is impossible for a full cover
   with exactlyfive productive classes.
3. **Three16 labels.** Their phases modulo16 must use both halves, with
   one label16u in the singleton half and two labels16v/16w in the opposite
   half. Each hole lies in the singleton projection and at least one of
   the other two projections. Its footprint is contained in

       A(u,au) intersect (A(v,av) union A(w,aw)).

   Here A(d,a) denotes the odd-coordinate congruence y=amodd. All five
   cofactor labels p,q,u,v,w are distinct in this all16 case.

The phases au,av,aw above are ORIGINAL odd-coordinate phases. For a
productive double-half label, its projection must intersect the singleton
projection, requiring av=au modgcd(u,v), and similarly forw. These are
complete necessary CRT compatibility conditions. Phases violating them
cannot occur in a three-productive-class repair. Compatible phases with
no P-uncovered incidence are still included conservatively.

For fixed parentr, binary phase orientation and odd phase are independent
by CRT:16 and32 are coprime to everyd|315. The two orientations in the
all16 case give the same BASE footprint. This explains the universal
original-phase quantifier; projected labels8d are used only for incidence,
never added as covering resources.

## 2. Exact P-uncovered parent images

The map x -> y=xmod315 is a bijection from any mod8 parent in BASE2520
to Z/315Z. Its P-uncovered image is

| Parent type | Actual parents | Allowed odd-coordinate conditions | Points |
| --- | --- | --- | ---: |
| O |1,3,5,7|y!=0mod9, y!=1mod5, y!=1mod7|192|
| E2 |2,6|y!=0mod9, y!=1mod3|175|
| E4 |4|y!=0mod9|280|

P8 coversparent0. For odd parents,10:1 and14:1 become the indicated
5/7 exclusions, while12:10 is even. In2/6,12:10 is exactly the3-residue1
exclusion together with their fixed binary residue2mod4. In4 its binary
residue0mod4 makes12:10 impossible;10:1 and14:1 are odd. This is a
statement about the P complement and TAIL projection space, **not a
symmetry normalization of BASE assignments**.

For each parent typeR define the exact projection maximum

    M_R(l)=max_a |R intersect A(l,a)|.

For three16 labels define

    S_R(u;v,w)=max_{au,av,aw compatible}
        |R intersect A(u,au) intersect(A(v,av) union A(w,aw))|.

Every original cofactor is inD={1,3,5,7,9,15,21,35,45,63,105,315}.
The conditional phase domain has

    sum_{u; v<w, v/w!=u} u*(v/gcd(u,v))*(w/gcd(u,w))=644512

entries summed over all660 original singleton/double triples for each
parent type. The two-parent capacities for each complete label choice are

    mixed: M_R(lcm(p,q)) + M_T(lcm(u,v,w));
    all16: M_R(lcm(p,q)) + S_T(u;v,w).

The mixed family has66*10*66=43560 original label choices; all16 has
66*10*36=23760. Only(E4,E4) is unavailable because parent4 is unique.
All other eight ordered type pairs occur among the42 actual ordered
distinct nonzero parent pairs. Global original labels and one phase per
modulus are retained in both formulas.

## 3. Complete capacity table and consequence

The entire phase and coupled-label records yield:

| Two-class parent / three-class parent | One16+two32 | Three16 |
| --- | ---: | ---: |
|O/O|120|114|
|O/E2|153|158|
|O/E4|153|158|
|E2/O|153|129|
|E2/E2|140|161|
|E2/E4|161|161|
|E4/O|153|129|
|E4/E2|161|161|

The largest value is161. The excluded two16+one32 case has capacity<=126,
so every possible full five-productive allocation satisfies |H|<=161.
Both-odd parents have capacity<=120, also below the published127-hole
lower bound. Consequently an exactlyfive allocation must occupy an even
parent. This footprint calculation alone does not infer a stronger uniform TAIL
count. The independent BASE162 proof in [proof.md](proof.md) supplies that
lower bound and the composed six-class conclusion.

The161 value is sharp for ABSTRACT P-uncovered two-parent demands. Set

    H2={xmod2520 : x=2mod24}, |H2|=105;
    H4={xmod2520 : x=4mod40, x!=0mod9}, |H4|=56.

All161 demand points avoidP. Their644 physical10080 lifts are repaired by
the FIVE DISTINCT original classes

    16:2,48:26,80:4,32:12,160:124.

The first pair repairs H2. For H4,80:4 occupies two binary positions,
32:12 and160:124 the two other positions. Replacing160:124 by160:44
keeps its odd projection and collides with the32:12 position, leaving56
demand lifts uncovered. Cofactor1 appears in original16 and32, and5 in
original80 and160; these legal repetitions across different original
families are essential. Repeating an ORIGINAL modulus is forbidden.

This control is not a completed BASE-hole-set realization. P plus the
five classes still leaves4584 physical10080 points uncovered. It gives
no full covering witness or global sharpness claim.

## 4. Replay and trust boundary

Sources [five-tail-footprint-pilot.py](five-tail-footprint-pilot.py) and [check-five-tail-footprint.py](check-five-tail-footprint.py), Python3.11.2
standard library only, with integer arithmetic throughout. Regenerate
raw data in an absolute own-workspace scratch directory, then audit:

    python3 -B five-tail-footprint-pilot.py --out /absolute/own-workspace/scratch/five-footprint
    python3 -B check-five-tail-footprint.py --data /absolute/own-workspace/scratch/five-footprint

Repeat both with-O and compare complete fields with
[five-capacity-certificate.json](five-capacity-certificate.json); timing fields are not mathematical.
The executed commands were externally guarded at20s per child with all
numerical thread variables1 and one CPU child at a time. Timeout, malformed
data or an incomplete trace proves no bound; no limits were increased.

The producer uses grouped315-coordinate residue masks and the written
P-complement recipes. The separate checker imports no producer module:
it constructs divisors from prime powers, rebuilds literal P/2520 AP masks
for ALL7 nonzero physical parents, and checks every one of4368 original
projected-phase CRT maps. Only after this complete parent/phase audit
does it identify equal scalar capacity spaces.

The checker visits phase indices in reverse order and reads each raw7H
record at its independently calculated offset. It compares all original
labels, phase values, capacities and canonical maxima witnesses for every
one of1933536 phase records. It then reconstructs every one of67320
coupled13H label records, including all538560 ordered-type capacities.
All producer normal/-O fields and all physical AP normal/-O fields match.
Complete AP mathematical SHA256:

    70ccf091d040ae1962c9c0bc68aae66c6ac7bb026f4c3023ae03118bec41f59f.

Normal producer2.499666s, normal physical audit5.009802s; optimized
producer6.199337s, optimized audit9.238829s. Maximum recorded RSS30568KiB,
all children below20s, thread1/oneCPU child, no native solver. Raw27MB phase
traces, coupled streams, full maxima witnesses and timing receipts remain
in workspace scratch. The compact certificate stores the complete scalar
mathematical verdict and trace hashes; source regenerates the raw data.

Ordinary classification, CRT compatibility, P-complement identification,
same-label resource coupling and published prerequisites remain
unformalized. Two owned exact algorithms are not independent peer review.
Historical priority of the generic fibre-counting mechanism is not claimed.
