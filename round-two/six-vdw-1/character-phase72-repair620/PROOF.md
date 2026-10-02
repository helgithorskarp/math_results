# Phase72 character repairs at period620 need nine edited columns

Author: **six-vdw-1, researcher**, 2026-10-02. Exact restricted-family lemma,
checked by separate author algorithms. External review and formalization are
unclaimed. The requested coloring of [1,3704] remains open here.

Let L(r) be0 for a nonzero square in F31 and1 for a nonsquare; L(0) is
undefined. Write

    b72(s) = bit_(s mod10)(72) XOR floor(s/10),  0<=s<20.

Let G be its orbit under s->u*s+v in Z20, with u a unit. Its twenty absolute
low-ten-bit masks are

    72,118,142,145,237,285,291,440,452,475,
    548,571,583,732,738,786,878,881,905,951.

Every g in G is antipodal and has no monochromatic cyclic seven-term AP
with nonzero phase step. This is a specified orbit, not all580 legal rows.

**Cyclic repair lemma.** Let alpha be any nonzero element of F31, beta any
element, and g any member of G. Put t=-beta/alpha. Let C be any binary
coloring of the regular cyclic domain

    {(r,s) in F31 x Z20 : r!=0},

with no monochromatic AP of seven terms and nonzero cyclic step modulo620.
Modular terms can repeat. Count as an edited column any r outside {0,t}
where C(r,s) differs from L(alpha*r+beta) XOR g(s) for some s. Then at least
**nine** columns are edited. When t!=0, the entire actual regular root
column t is freely colored and is not counted. No H3 invariance of C is
assumed, and no earlier H3 cuts are used.

**Finite repair lemma.** For every N>=2164, let C be any coloring of [1,N]
without a monochromatic nonconstant integer AP7. Compare position i with
the reference L(alpha*((i-1) mod31)+beta) XOR g((i-1) mod20) wherever the
character argument is nonzero. All values at root positions are arbitrary,
including nonperiodic values. There must be at least **nine distinct
nonroot field columns** containing a changed position. For this unpunctured
interval assertion, field0 is a compared regular column whenever t!=0.
This gives at least nine changed positions, without a periodicity premise.

If the finite comparison also omits physical column0, the direct cover
argument instead gives at least eight other edited nonroot columns when
t!=0, and nine when t=0. The cyclic nine-column lemma is stronger because
cyclic half-step APs force antipodality; that extra step is not silently
transferred to arbitrary finite colorings.

The proof computes a hypergraph optimum, not a minimum feasible repair.
Nine edited columns are necessary; their sufficiency is unproved. Neither
lemma improves a numerical bound for W(2,7) or excludes arbitrary colorings.

## 1. The complete bad-support hypergraph

Use the CRT identification Z620=F31 x Z20 and the reference
T(r,s)=L(r) XOR b72(s) on r!=0. Let H consist of the distinct field supports
of all its monochromatic cyclic AP7s with nonzero cyclic step. The producer
uses Euler powers,9600 normalized patterns and all30 scalar images. The
independent checker uses the literal square set and scans **every383780
original start/nonzero-step pair**, including nonunits and repeated terms.
There are299400 regular pairs,84380 pairs touching the reference zero,
11400 constant-field regular pairs, and7680 monochromatic regular pairs.
All constant-field regular pairs are mixed.

H has **240 distinct seven-element edges** on the thirty nonzero field
vertices. Every vertex has degree56. The normalized field-start set is

    1,2,3,4,5,8,9,10,15,16,17,20,21,22,23,24.

There are256 bad primitive patterns, including nonunit phase steps. Whole
hypergraph equality is checked, not just a generator count. Its canonical
edge SHA256 is

    b44cf8af4cbb78425f5bfc3c4b82c9e050fe57bb82e691200c6756b5241d4846.

Every nonzero field scalar mu acts on H by r->mu*r. CRT lifts this to the
unit with field coordinate mu and phase coordinate1. Character
multiplicativity complements or preserves all colors together. The checker
verifies all7200 edge images and18000 regular point identities, in addition
to900 character multiplicativity inputs. This action is transitive.

Phase affine maps preserve all APs, leave field supports unchanged and take
b72 through G. Thus the same H and all its cover statements apply to G.
The phase orbit and its physical CRT actions are reconstructed locally;
no earlier580-row census is a mathematical premise.

## 2. Exact integer optimum and complete minimum-cover census

A cover is a subset meeting every edge. The fractional cover optimum is
30/7: weights1/7 at every vertex give a primal cover; weights1/56 at every
edge give a dual packing, with each vertex load1. In particular a cover of
at most four vertices cannot hit240 edges of degree56.

Every nonempty cover can be scaled to contain1. This normalizes the cover
problem only; it does not impose a symmetry on a repaired coloring. For
sizes5,6,7,8 the flat producer tests, respectively,

    23751,118755,475020,1560780

candidates containing1, with no cover found and no omitted candidate.
The independent checker partitions binary vertex assignments by including
or excluding the next vertex. An unavailable edge or a packing of more
pairwise disjoint projected edges than remaining choices refutes a whole
branch. Its exact binomial volume is credited once. Positive and negative
volumes must sum to the entire C(29,k-1) domain. All four complete negative
volumes agree with the flat producer. Tiny positive and negative fixtures
compare this weighted tree with every literal subset in their full domains.

The literal cover

    [1,2,3,4,8,12,17,22,27]

hits all240 edges, so **tau(H)=9**. The first-positive search at size9 is
not used as a full census. A separate complete weighted classification of
all **4292145** size-nine candidates containing1 finds **153** covers and
4291992 noncovers, in58399 recursion nodes. An untrusted edge-branch
producer lists153 distinct literal covers; independent checks verify each
against every edge and match the complete positive count. Uniqueness,
membership and this complete independent count establish the entire list.

The complete canonical cover-list SHA256 is

    75fe7d9e9bd583e1eaac92ec43ccb78ed2df0ef219444305367022d792543a9e.

## 3. Every normalized minimum mask has a physical unit contradiction

Normalize a nonzero reference root to actual field30=-1, keep physical
pole0 omitted, and fix phase b72. The background on actual regular nonroot
fields is L(r+1) XOR b72(s). For a minimum cover E containing1, allow the
actual fields

    F = {30} union {e-1 : e in E, e!=1}

to have independent arbitrary antipodal phase words. These are nine free
columns: eight edits plus the actual regular reference root. No pole
placeholder is made into a variable. Every other actual regular column is
fixed. Absolute lower-phase bits are used, with no palette anchor or
field-invariance constraint.

For **each of all153** E, the regenerated certificate gives two actual
regular cyclic APs. Each has exactly one free point and six fixed points
of one color. The two APs concern the same free column and lower phase
cell, and demand opposite lower bits. The independent checker imports no
rule generator or SAT encoder. It computes all2142 actual term colors and
field/phase coordinates of the306 AP witnesses by square membership,
checks avoidance of the physical pole, counts exactly one free point, and
checks both possible lower bits directly. All153 masks are contradicted.

For the displayed E, F=[1,2,3,7,11,16,21,26,30]. The conflicting cyclic
AP pairs are [start,step]=[3,422] and[3,610]. Their actual residue sequences
are

    3,425,227,29,451,253,55
    3,613,603,593,583,573,563.

Both free points are actual field3/phase3. The six fixed colors are1 in
the first AP and0 in the second, forcing the lower bit to0 and1 respectively.
Large steps, including nonunits, have not been discarded.

To prove the cyclic lemma, first absorb L(alpha) into a global palette
exchange and normalize the phase by a unit affine CRT map. If t=0, the
edited columns must cover H, hence number at least9. If t!=0, let R be the
edited nonroot fields outside physical0. Translation by -t shows that

    E0 = {-t} union {r-t : r in R}

must cover H: a reference bad AP disjoint from E0 is wholly fixed and
avoids both root and physical pole. Thus |R|>=8. If |R|=8, put h=-t and
scale reference field coordinates by h^-1. E=E0/h is a minimum cover
containing1. Equivalently the actual field map r=h*r' preserves physical
pole0 and sends the actual root to -1. The identity

    L(h*r'-t) = L(h) XOR L(r'+1)

is valid away from the freely colored root. It transports C to exactly
one of the153 masks above, up to a global complement.

Finally any AP-free regular cyclic C must be antipodal: the step310 AP at
a regular point alternates that point and its310-shift, so equality of
their colors would be monochromatic. Every freely colored root/edit word
therefore has the antipodal form tested above. All153 physical conflicts
contradict |R|=8. This proves |R|>=9 for every nonzero root as well.

## 4. Finite lift and arbitrary nonperiodic edits

Every bad reference AP has nonzero field difference, because its phase
word is legal. Transport it through the requisite field/phase affine CRT
map, retaining a nonzero field difference. Reverse terms if needed so its
step D is at most310. In fact D<=309: step310 has field difference0. Choose
the resulting start A modulo620, then subtract310 if A>=310. This last
shift retains every field residue and complements every defined reference
color, because the phase word is antipodal. The resulting actual integer
AP has start0<=A<=309 and endpoint

    A+6*D <=309+6*309=2163.

It is therefore contained in one-based [1,2164]. Its support avoids the
character root, and any other omitted columns it avoided before lifting.
An arbitrary nonperiodic coloring agreeing with the reference on all
columns of that support still contains this actual monochromatic AP.
Hence its edited nonroot columns, mapped to reference coordinates, cover
H and number at least9. With an additional nonroot physical pole omitted,
the pole can contribute at most one cover vertex, giving the stated8 bound.

This is a support lift for a periodic reference, not an affine symmetry of
arbitrary finite colorings. The sufficiency of prefix2164 is not an
optimal-endpoint claim. The literal bridge auditor checks all372000
original nonzero-field-step supports, all7680 actual bad integer lifts,
12400 phase CRT points,17400 normalized nonzero-root points,27900 nonzero
linear-coefficient regular points, and all7600 phase APs in G.

## 5. Reproduction, provenance and scope

[README.md](README.md) gives the standard-library reproduction command.
[EXPECTED.json](EXPECTED.json) retains all eighteen semantic records,
including complete coverage counts, full result objects and certificate
hashes. The public source regenerates H, all covers and all literal AP
refutations into local output; no stored proof corpus, model or solver is
required. All source/input bytes are pinned before checker imports. Normal
and optimized Python must match every complete mathematical result.
Controls reject eight physical hypergraph damages and twenty-one
cover/mask/AP damages, and include exact tiny positive/negative partitions.
See [VALIDATION.md](VALIDATION.md) for the trust and resource boundaries.

This is a quantitative, specified-character repair refinement of prior
[QR31 XOR C20 exclusion](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/qr31-x20-obstruction/PROOF.md).
The broader [outside-three-column result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/three-column-robust620/PROOF.md)
applies to every separable baseline but has a smaller repair count. Neither
old theorem is used to refute the present masks. Prior
[separable620 row work](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/separable620/PROOF.md),
[phase-power cores](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/phase-powers620/PROOF.md)
and [whole H3 exclusion](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/h3-core620-exclusion/PROOF.md)
motivate dropping global H3 invariance and freeing independent repair words.
Their numerical cuts are not premises here.

Character repair and affine field-support lifts are established campaign
methods, including the prior
[period622 degree-three result](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_622_degree3_character_repair/PROOF.md)
and six-vdw-3's
[F103 character repairs](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/character-orbit-repair618/PROOF.md),
[phase-independent linear repair](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/character-parity-repair618/PROOF.md)
and [polynomial repair](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/polynomial-character-obstruction618/PROOF.md).
No F103 count, cut, review or endpoint is transferred. The specific new
evidence is tau(H)=9 and the complete153-mask physical conflict cover for
the stated F31 phase orbit; generic character or hypergraph methods are not
claimed as new. Historical priority is not comprehensively established.

Primary [Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
report >3703 for seven terms/two colors and the associated prime617;
Monroe's notation is length-first W(7,2), while this campaign uses
color-first W(2,7). The [author's repository](https://github.com/hmonroe/vdw)
was refreshed live. Primary
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
is cyclic-construction background. These checks are not a comprehensive
current-record or priority survey. The asymmetric w(3,k) problem is distinct.

Construction remains the purpose: a cover is only necessary, and all
minimum masks fail. Larger masks and noncharacter backgrounds remain
unresolved. No general cyclic620 exclusion,3704-point witness, exact W,
numerical W improvement, external review or formal theorem is asserted.
