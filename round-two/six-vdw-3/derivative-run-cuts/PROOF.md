# Derivative packing and three exact distance exclusions

Author: **six-vdw-3, researcher**, 2026-10-01. The combinatorial statements
below have written proofs and finite boundary checks. Three finite exclusions
are computer-assisted: complete encodings are audited separately, and every
positive-RUP proof addition is checked. This is same-author implementation
independence, without independent peer review or formalization.

Let q>=23 be an integer coprime to6, f=000111 on Z/6Z, and

```
c(t)=u(t mod q) XOR f(t mod6),   u:Z/qZ->{0,1}.
```

Cyclic seven-term progressions have nonzero step; repeated residues count.
The published pair-parity characterization says that c is valid exactly
when, for every a and every nonzero r modulo q, the four bits

```
u(a+jr) XOR u(a+(j+3)r),   j=0,1,2,3
```

are not all equal. We use this characterization, rather than assume that
u merely has no monochromatic seven-AP. That weaker assumption is inadequate.

**Theorem.** If c is valid, for every unit h modulo q, both colors of
Delta_h u have at least ceil(5q/19) entries. Its weight M_h is even, hence

```
2 ceil(5q/38) <= M_h <= 2 floor(7q/19).
```

At q=103, the stronger exact conclusion is

```
32 <= M_h <= 72,   M_h even,   every h!=0;
20 <= |u^{-1}(1)| <= 83.
```

At orientation weight20, every nonzero difference has multiplicity at
most4; at least74 of102 shifts have distance32. At least155 ordered
pairs (x,y) of distinct points in the one-set S have 3y-2x or 4y-3x
also in S. These are necessary conditions, not a classification or an
existence claim. The full separable family, other period618 colorings,
and arbitrary [1,3704] colorings remain unresolved; no W bound improves.

## 1. A twenty-two-position obstruction

Write h=3r with r a unit and read the original word in r coordinates,
calling it U. Put V(x)=U(x) XOR U(x+3). Cyclic telescoping gives

```
U(a) XOR U(a+3k) = XOR_(l=0)^(k-1) V(a+3l).
```

Suppose twenty-two consecutive positions of V agree with a four-periodic
pattern, with the first position numbered0. For j=0,1,2,3,

```
U(4j) XOR U(4j+12) = XOR_(l=0)^3 V(4j+3l).
```

The four indices have each residue modulo4 exactly once, so their XOR
is the parity of the pattern, independent of j. Every used V index is
between0 and21. This is the forbidden ladder with step4r in the original
coordinates. Since q is odd and r is a unit, 4r!=0. All arithmetic is
cyclic; the U endpoint at24 can wrap when q=23. No nonwrapping endpoint
assumption is made. Thus no such twenty-two-position segment exists.

## 2. Cyclic run packing

The step-r ladder says that V has no run of length4. Choose either
minority color, let m be its count, and let R be the number of runs of
each color. Both colors occur and every run has length1,2 or3. Decompose
the cycle into R blocks: one minority run of length a followed by its
majority run of length b. Call (a,b)=(1,3) regular, and count D defective
blocks.

Five consecutive regular blocks give twenty four-periodic positions.
The preceding final majority entry and following first minority entry
extend them to the forbidden twenty-two-position segment. This works
across the cyclic boundary and for either minority bit. Hence every
cyclic gap of regular blocks has length at most4. D is positive: if
all blocks were regular, q=4R, contrary to q odd. Consequently R<=5D.

Each defective block consumes at least one unit of minority excess or
majority deficiency, since (a-1)+(3-b)>=1 exactly outside (1,3). Summing,

```
D <= (m-R)+(3R-(q-m)) = 2R-q+2m.
R <= 5D  =>  5q <= 9R+10m <= 19m,
```

where R<=m. Thus m>=ceil(5q/19), proving the bound for both colors.
The XOR of all cyclic differences cancels every original bit twice,
so M_h is even. Rounding the two density bounds to even M_h gives the
stated general range. At103 it is28<=M_h<=74.
For example, a distance28 derivative would need at least27 runs of
each color, since 5*103<=9R+10*28. This argument has quantified coverage
of every word and every stated shift; finite tests are boundary checks,
not an enumeration substituted for that proof.

## 3. Complete distance fibers at103

Use the published cut encoding: one variable e_xy for every unordered
pair of distinct field points, with e_xy=u(x) XOR u(y). Fix u(0)=0 by
color exchange. The102 anchors e_0x determine the other5151 edges by
XOR3 equations. They use20604 clauses. All5253 unoriented ladders use
two NAE4 clauses each. The base has5253 variables and31110 clauses.
The independent auditor reconstructs this base from every103*102
directed field start/step pair and a separate edge-label formula.

For a putative distance d in {28,30,74}, normalize its shift to3.
Explicitly, if Delta_h u has weight d, pick a point a where that
derivative equals its minority bit b: b=1 for28,30 and b=0 for74.
Such a point exists. The affine/color pullback

```
U(x)=u(a+(h/3)x) XOR u(a)
```

preserves all ladders, gives U(0)=0, has weight d for Delta_3 U, and
Delta_3 U(0)=b. Translation, dilation and color exchange suffice; no
additional symmetry of U is assumed. In particular complementing the
original word does not complement its derivative. The distance74
model counts derivative zeros directly, with no derivative-color
symmetry reduction.

List the103 cut variables e_{x,x+3} in order x=0,...,102, and count
either their ones or their zeros as appropriate. Their labels are
distinct. The targets are28,30,29 respectively. A unary prefix cell
C_i,k records whether the first i counted inputs have at least k ones,
for1<=k<=min(i,target+1). It is fully defined by

```
C_i,k <=> C_(i-1),k OR (X_i AND C_(i-1),(k-1)).
```

Missing C_(i-1),k is false when k=i; threshold0 is true. Induction on i
proves that every input assignment has a unique counter extension.
Enforcing C_103,target and NOT C_103,(target+1) is therefore exactly
the requested count. The four clauses for Z<=>A OR (X AND B) are

```
NOT A OR Z
NOT X OR NOT B OR Z
NOT Z OR A OR X
NOT Z OR A OR B
```

Constants are simplified. The minority-at-zero unit is e_03 for28,30,
and NOT e_03 for74. These are the only extra orientation restrictions.
The auditor derives the counter clauses from all prime implicates of
the Boolean relation, rather than import the encoder's clause list.

| Distance d | Counted color/count | Variables | Clauses | RUP additions | Checked hints |
|---|---|---:|---:|---:|---:|
|28|ones/28|7834|41305|8211|307231|
|30|ones/30|7981|41891|64025|2721590|
|74|zeros/29|7908|41600|29258|1101726|

Every model has an exactly replayed empty-clause refutation. The
normalization above covers every orientation having any shift in
these three distance classes. The elementary range28..74 then leaves
only the even distances32,34,...,72. UNKNOWN or an incomplete proposed
trace would establish nothing; none is a premise of these exclusions.

## 4. Orientation weight and the residual weight20 cohort

Write n=|u^{-1}(1)|. Ordered different-color pairs give

```
sum_(h!=0) M_h = 2n(103-n) >= 102*32 = 3264.
```

The two bordering values n=19,84 give3192, while n=20,83 give3320.
Concavity, or direct integer evaluation, proves20<=n<=83. At n=20,
write I_h=|S intersect (S-h)|. Then I_h=20-M_h/2<=4. The total distance
3320 is only56 above3264, so at most28 shifts can exceed32; at least74
have distance32.

Let T_h count transitions of Delta_h u in direction r=h/3. Its two
colors have T_h/2 runs, all of length at most3. Therefore

```
T_h >= 2 ceil(max(M_h,103-M_h)/3) >= 80-M_h
```

for the even range32..72. At32 and34 check directly; for M>=34 the
weaker bound 2(103-M)/3 already dominates80-M. Hence at n=20,

```
sum_(h!=0) T_h >= 102*80-3320 = 4840.
```

For r!=0 count triples A:(x,x+r,x+3r) in S, triples
B:(x,x+r,x+4r) in S, and quadruples Q:(x,x+r,x+3r,x+4r) in S,
with ordered parameters (x,r). Four-point parity equals the sum of
single indicators minus twice the six pair products plus four times
the four triple products minus eight times the quadruple product.
Summing over (x,r) gives

```
sum T_h = 4n(103-1)-12n(n-1)+8(A+B-Q).
```

Each ordered pair of distinct points occurs once for each of the six
pair shapes; reflection identifies the other two triple shapes with
A and B. At n=20 the constant part is3600. Thus A+B-Q>=155.
Inclusion-exclusion identifies A+B-Q with the number of ordered
(x,y) in S, x!=y, having at least one of3y-2x and4y-3x in S. There is
no claim that these necessary conditions are jointly achievable.

## Evidence, scope and dependencies

[VALIDATION.md](VALIDATION.md) records source-only reproduction, complete
model audits and exact proof replay in normal and optimized Python,
actual positive cyclic controls, coverage controls and corruption
rejection. The solver and DRAT converter are untrusted proposers.
The separate strict positive-RUP checker, CNF audits and unformalized
mathematical encoding/normalization arguments form the trust boundary.
No large certificate corpus is an external premise; traces regenerate.

The characterization and base model are
[six-vdw-3's parity-ladder lemma](../parity-ladders/PROOF.md), graph
`bafkreiensnfvevjsgj2lowwszcvrwecpinqmp7sahc6urkwoletzjmgqca`, height8565.
The period618 identification and interval bridge come from
[six-vdw-1's normal form](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_phase_symmetry),
graph `bafkreifqxeobdid7w5k2fkv4zg67yzcx534zi6c33uenbwzoqhq2jgpbfm`, height7294.
The strict checker is credited to
[six-vdw-1's binary fibers](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_binary_fibers),
graph `bafkreic6ikxxfio6r5367szeoaz2mfhxt2vaakem7xr2mrmjgf5vy7cmou`, height7428;
its mathematical dense-fiber exclusion is not a premise here.
The [single-exception exclusion](../signed-phase-defects/PROOF.md), graph
`bafkreidmpptm7jtlfdvngx7pm7ybx57xgfalcxrw76g2oqezzzydrvyfhm`, height8644,
and [affine symmetry reduction](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_affine_reduction),
height7350, provide context, not proof of the new three distance cuts.

At618, a cyclic obstruction lifts with reversed step<=309, start<=617
and final coordinate<=2471, so it appears in the3704-point repetition.
Conversely every interval step at length3704 is<=617, nonzero modulo618.
This bridge only concerns the specified periodic family. The new bounds
therefore restrict a candidate family without establishing W(2,7)>=3705.

Primary context: [Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
give >3703 and unzipped prime617, with reversed W(length,colors)
notation. [Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
and [Heule](https://www.cs.utexas.edu/~marijn/publications/JOC_08_03_A01.pdf)
provide established construction methods. Bounded current inspection
found no overlapping run-packing or three-distance statement; no
historical priority is asserted.
