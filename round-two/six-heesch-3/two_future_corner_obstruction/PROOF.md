# Four original corners exclude two future surrounds

Actual author **six-heesch-3**, role **researcher**. This is an
exact computer-assisted, author-checked local lemma, independently
unreviewed and unformalized. The written argument proves the motion
domain complete; the compact certificate checks its finite geometric
exclusions. No priority or shape-wide Heesch upper is claimed.

Let T7 be the closed union, in coordinates meaning physical
(x,sqrt(3)y)/4, of seven regular hexagons centered at(4+8j,0), upper
triangles((8j+2,2),(8j+4,4),(8j+6,2)) for0<=j<7,
bridges((8j+6,2),(8j+8,0),(8j+10,2)) for0<=j<6, and the terminal
half-triangle((54,2),(56,0),(56,2)). Pose(a,f,x,y) first reflects y if
f=1, then rotates30a degrees, then translates.

**Fixed-prefix lemma.** Each of the two literal74-copy fourth prefixes
in `fixtures.json` has no TWO further complete strict surrounds by
congruent copies of T7. Equivalently, there are no larger disjoint-interior
copy packings with unions S1,S2 containing the fixed S0 and satisfying
S0 contained in int(S1), S1 contained in int(S2). Added copies may use
arbitrary translations, rotations and reflections. Holes elsewhere are
allowed. The exact normalized prefix keys are:

- bfe: `bfe0a1ac4726d42ba48ac83616a064b399237716fb3f11a5ad99bf313f7fc65e`;
- c0a: `c0a54a208ae29ab57ef26cf15c42691cb750bb585fec78c5a36c714869fe9fc2`.

Both have counts[1,6,10,21,36]. The first is the fourth prefix of the
included129-copy five-corona construction. The second changes its
last fourth pose from(6,1,96,-48) to(6,1,104,-48); all its four disc
prefixes are verified separately. The lemma excludes extension through
a sixth from these fixed fourths. It does not classify other fourths,
settle T7's finite Heesch number or provide a seven-corona construction.

## Finite corner domains beyond180 degrees

For a bounded simple polygon with minimum positive interior angle
alpha, consider an old boundary point leaving one exterior gap beta,
where pi<beta<pi+alpha. If a packing covers a neighborhood of that
point, all its new suppliers present vertices there. A straight edge
would occupy180 degrees and leave the positive angle beta-pi<alpha,
which no further vertex or edge could fill without overlap. An interior
point of a copy occupies360 degrees and conflicts with the old sector.

Local finiteness justifies considering only copies containing the
point. A fixed inscribed disc in each congruent copy has positive
radius; copies intersecting a bounded ball put their interior-disjoint
discs in a larger bounded ball because their diameters are fixed. Only
finitely many can occur there. Copies not containing the point can then
be discarded in a sufficiently small neighborhood.

The remaining sectors have prototype vertex angles, each at least
alpha, and partition the exterior gap. There are finitely many words
of those angles summing to beta. The old gap ray and each successive
angle pin every sector ray. A choice of prototype vertex and reflection
then pins the rotation, and matching the vertex pins the translation.
This is a complete arbitrary-motion domain, without a lattice premise.
The interval endpoints are excluded: at180 an edge alone may suffice;
at240 with alpha=60, an edge plus a60-degree vertex can occur.

For T7, the exact boundary angle counts, in30-degree units, are
{2:7,3:1,4:15,5:1,6:1,8:13,10:6}. Thus alpha=60. A210-degree exterior
gap has the seven words

    (2,2,3), (2,3,2), (2,5), (3,2,2), (3,4), (4,3), (5,2).

An edge would leave30 degrees and cannot participate. A150-degree gap
has words(2,3),(3,2),(5); a60-degree gap has only(2). The angle counts
come from the explicit atom boundary and are checked exactly.

## Three forces using only the first surround

Suppose S1 covers S0. The following three original angular units have
unique compatible suppliers, in this order, for both prefixes:

| Original point | Exterior gap | Required30-degree unit from the gap's initial ray | Forced pose | Complete supplier count |
|---|---|---|---|---|
| (24,-32) | 150 degrees | 3 | P32=(0,0,-32,-32) | 18 |
| (16,-40) | 150 degrees | 3 | P40=(0,0,-40,-40) | 18 |
| (12,-44) | 210 degrees | 0 | A=(0,0,-44,-44) | 48 |

At each step, the certificate lists EVERY pinned motion that could
supply the required original angular unit. All except the stated pose
have positive interior intersection with an old copy or a preceding
forced copy. The listed blocking-owner indices are recomputed, not
trusted. Fifty of these84 supplier motions have odd30-degree rotations;
none are rounded or omitted. Their pinned translations are represented
exactly in Q(sqrt(3)). The sole surviving supplier must be in S1.
No prescribed-mate claim, pair pruning or second surround is used by
these three forces. Only original S0 corners are demanded; no new
supplier is required to have its own corners filled in S1.

The finite exclusions are an exact computation over the literal inputs.
`check.py` reconstructs the atom boundary and the relevant complete word
roles, matches every prototype vertex/reflection, tests all convex-atom
intersections, and compares every resulting pose and blocker with the
certificate. `certificate.json` is the full small exclusion table.

## The fourth gap requires the second surround

The original point z=(20,-44) leaves60 degrees. Its complete supplier
set has14 motions:

    U_j=(0,0,16-8j,-48),
    V_j=(6,1,24+8j,-48), 0<=j<=6.

Let L be96 for bfe and104 for c0a. Both prefixes contain the actual
old copies H=(6,1,68,-44), Z=(6,1,L,-48).

For bfe, U_j with x=-32,-24,-16 forms a forbidden pair with the forced
A; the other four U_j overlap Z. For c0a, x=-32,-24,-16,-8 forms a
forbidden pair with A; its remaining three U_j overlap Z. In both cases
V_j with x=24,32,40,48,56 forms a forbidden pair with H; x=64,72
overlaps Z. These packing collisions and every positive pair image
are checked entrywise.

The pair exclusions invoke the published [uniform two-copy lemma9783](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-3/two_copy_strip_obstruction/PROOF.md),
verified source0bc5ae35b48015e64ac07d9ae25e0ba85d26ed7f. A packing pair
I,I+(8r+4,-4), 1<=r<=6, cannot both receive another surround. A common
arbitrary Euclidean isometry preserves this claim. For the U cases,
the common frame is A=(0,0,-44,-44), with r=1,2,3 and also4 for c0a.
For the five V cases it is H, with r=5,4,3,2,1 respectively.

Under two-future assumptions every copy in S1 must be surrounded by S2.
Consequently a proposed supplier at z cannot form one of these pairs
with A or H. Every14 possible suppliers is excluded, so S1 cannot fill
this original gap while also acquiring S2. This proves the fixed-prefix
lemma. The dependency is the local pair theorem, not an unproved
registration or mate rule.

The included actual fifth for bfe contains all three forced copies,
and also B=(0,0,-16,-48). Its uncovered final layer contains the
forbidden A,B pair and remains admissible. The fourth does have ONE
further surround. Demanding the second is essential. The six-corona
T6 positive control is reproduced with Bašić attribution; it is not
presented as a new record. See the [README](README.md) for commands,
complete expected evidence and the shared-code trust boundary.
