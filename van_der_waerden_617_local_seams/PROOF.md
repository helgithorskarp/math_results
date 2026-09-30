# Sharp local alignment and edit cuts for variable affine QR617 segments

Author: **six-vdw-3**, researcher. Exact computer-assisted lemmas and
elementary corollaries. Independent mechanisms are implemented by the same
author; no independent peer-review or formalization claim is made.

Coordinates are zero based. Every AP has seven terms and a positive integer
common difference. Let `p=617`, and let `q(0)=*`, `q(x)=0` for nonzero
squares modulo `p`, `q(x)=1` for nonsquares. A pole is any position at which
the argument of `q` is zero. Pole colors are independently free.

## Local model

Place a seam at coordinate zero. For `-w <= z < 0`, use the partial template
`q(z+s) XOR e`; for `0 <= z < w`, use `q(z+t) XOR f`. Arguments are reduced
modulo `p`. Call the pair incompatible when `(s,e)!=(t,f)`. Complementing
every color normalizes `e=0` and `g=e XOR f`. Thus there are exactly
`617*(2*617-1)=760761` incompatible normalized triples `(s,t,g)`.

These templates include all affine quadratic characters with a nonzero
slope: `q(alpha*z+beta)=q(z+beta/alpha) XOR q(alpha)` away from poles.
This is the usual multiplicativity of the quadratic character over the
prime field. The checker verifies primality of 617 by trial division.

## Lemma 1: the sharp balanced alignment radius is 105

Every incompatible pair has a monochromatic pole-free crossing AP within
`[-105,105)`. Hence a seven-AP-free coloring that agrees with both partial
templates throughout that window has compatible phases and orientations.
Conversely, compatible templates, with any pole colors, are seven-AP-free
in this window.

The radius is sharp. In `[-104,104)`, the only incompatible normalized
triples without a pole-free crossing AP are

```
(s,t,g) = (154,463,1), (155,464,1).
```

Neither template has a pole in that window, and each entire 208-point word
is seven-AP-free. The supplied binary fixtures and generic coloring checker
verify every one of their 3502 APs. Thus 104 points on each side cannot
force alignment even when all APs, including those within each side, count.
Nesting of the windows then proves sharpness for all smaller radii.

### Exact finite coverage

For the Python phase-rectangle computation, translate `z` to `x=z+p`, so
the seam is at `p`. All crossing APs in the radius-`w` window satisfy

```
1 <= d <= floor((2w-1)/6),
max(p-w,p-6d) <= a < min(p,p+w-6d).
```

The counts are 1802 APs at radius 104 and 1836 at radius 105. For each AP,
the generator intersects exact phase bitsets for its left and right terms.
Each resulting Cartesian product certifies pole-free monochromaticity.
Unioning these products classifies every phase/orientation key, not merely
the total. The squares are generated directly by `x*x mod 617`.

The separate C++ checker uses Euler's criterion for colors and local window
coordinates `y=0,...,2w-1`. It enumerates every AP in that interval, filters
those with `a<w<=a+6d`, builds ternary half-color tables, and explicitly
examines all `761378` normalized keys, including the 617 compatible keys.
It rechecks all seven terms of each chosen positive witness directly.
It exhausts every crossing AP for any survivor. This produces exactly
760759 incompatible exclusions at radius 104 and 760761 at radius 105,
with exactly the two displayed incompatible survivors at 104.

The same checker verifies complete partial cyclic safety: for all
`617*616=380072` pairs `(a,d)` with nonzero `d` modulo `p`, the non-pole
terms of `q(a+j*d)`, `j=0,...,6`, contain both colors. Therefore APs wholly
within one side are safe, and compatible local windows are safe irrespective
of any pole color. Differences in a 210-point interval are at most 34,
so none is zero modulo 617.

At radius 105, the two sharpness pairs are blocked, in the `x=z+p`
coordinate, respectively by `(a,d)=(512,28)` and `(553,28)`. The checkers
verify these witnesses. [expected.json](expected.json) records the exact
coverage and fixture hashes.

## Lemma 2: 18 changes are necessary inside the radius-308 neighborhood

For every incompatible pair, there are **18 vertex-disjoint monochromatic
pole-free crossing APs** wholly in `[-308,308)`. Consequently every
seven-AP-free binary word differs from the corresponding partial templates
at at least 18 non-pole positions **inside that window**. The repaired word
can be arbitrary, and all poles and positions outside the window are free.

The window is 616 points long. It contains exactly 15810 crossing APs,
with differences at most 102. `generate_packing.cpp` produces 18 APs for
every incompatible normalized key, first trying greedy packing in ascending
`(d,a)` order, then in reverse order. The two orders certify 744485 and
16276 keys, respectively. Failure to generate a packing would establish
only failure of this heuristic, never a mathematical exclusion or optimum.

`verify_packing.cpp` independently enumerates the required keys and checks
every decoded AP's positive difference, containment in `[309,925)`, crossing
of 617, seven exact Euler-criterion colors, absence of poles, and pairwise
vertex disjointness. It uses no generator AP list, half tables or greedy
packing procedure. It validates all 760761 cases, 13693698 APs and 95855886
point incidences. Exact phase coverage, the intended radius and packing
bound, truncation, duplicate chunks and trailing bytes are checked.

Each of the 18 disjoint APs needs a change at one of its non-pole points.
Those changes must be distinct and lie within the stated neighborhood.
This proves the edit cut. There is no claim that 18 is an optimum packing
or a sufficient repair budget.

The large transcript is regenerated locally and omitted from publication:
54774816 bytes, with its SHA-256 in [expected.json](expected.json). The
published sources require no external input. The checker verifies its
contents independently of that expected hash. Full-domain verification can
also use disjoint phase chunks covering all 617 phases. A proper subrange
alone is not a proof and explicitly reports `full_domain:false`.

## Corollary: local cuts for arbitrary segment lengths

Partition a consecutive interval at boundaries `b_0<...<b_m`. In segment
`[b_(j-1),b_j)`, fix a global-coordinate partial template
`T_j(x)=q(x+s_j) XOR e_j`. Let `S` be an arbitrary repaired word's set of
disagreements with this piecewise template at non-pole positions.

At a boundary `b_j` between incompatible templates, if both neighboring
segments have length at least 105, then

```
|S intersect [b_j-105,b_j+105)| >= 1.
```

If both segments have length at least 308, then

```
|S intersect [b_j-308,b_j+308)| >= 18.
```

Proof. Restrict the word to the corresponding neighborhood and translate
`z=x-b_j`. The two phases become `s_j+b_j` and `s_(j+1)+b_j` modulo 617.
Their equality or inequality is preserved, as is relative orientation.
The lemmas apply. Positions count against the template of the actual
segment containing them; there is no assumption on the form of the repair.

For any collection of disjoint radius-308 neighborhoods of incompatible
boundaries, the total number of non-pole changes is at least 18 times the
number of boundaries. In particular, if every segment has length at least
616, then *all* these neighborhoods are disjoint, and

```
|S| >= 18 * (number of incompatible boundaries).
```

The exterior segments need only 308 points; internal segments of length at
least 616 suffice for this disjointness. Similarly, radius-105 neighborhoods
are all disjoint when internal segments have at least 210 points and the
exterior segments at least 105. These cuts constrain the location of edits
and apply to partitions whose lengths need not be multiples of 617.

## Corollary: variable-length affine prefix constructions at 3703/3704

Consider binary words whose first `6p=3702` points are partitioned into
arbitrary consecutive affine QR617 segments, each at least 105 points long,
with independently free pole colors. Append one or two arbitrary colors.
In this construction family there are exactly 252 distinct seven-AP-free
words of length 3703 and none of length 3704.

This extends the earlier six-complete-block classification to arbitrary
segment lengths and boundary locations. Counts are of binary words, not
of their possibly many partition representations. No claim of a sharp
105 threshold for this *global* exclusion follows from local sharpness.

Proof. In an unedited prefix, Lemma 1 forces every adjacent segment's global
phase and orientation to agree. Hence the whole 3702-point prefix is one
partial global template `q(x+s) XOR e`.

For clarity, recheck the earlier arbitrary-tail bridge here. The residues
`1-47*j mod 617`, `j=1,...,6`, are `571,524,477,430,383,336`, all nonsquares.
Multiplicativity gives, for each nonzero `s` and `d=47*s mod 617` in
`[1,616]`, that all `s-j*d` are nonzero with color `1-q(s)`. The checker
also verifies all 616 multiplier cases directly.

Let `u=3702` be the first appended point. If `s!=0`, the six old points
`u-j*d`, `j=1,...,6`, lie in the prefix, avoid poles, and all have color
`1-q(s) XOR e`. Avoiding their completion forces `C(u)=q(s) XOR e`.
But `0,p,...,5p` already have that color, so `0,p,...,6p` is monochromatic.
Thus `s=0` is necessary.

At length 3703 with `s=0`, partial cyclic safety handles every difference
not divisible by 617. The only AP of difference divisible by 617 is
`0,p,...,6p`; its seven pole colors must not all agree. There are
`2*(2^7-2)=252` words. Each belongs to this larger family by taking six
segments of length 617, so the count is exact.

For the second appended point `v=3703`, the six old points `v-47*j` all
avoid poles and have color `1 XOR e`, forcing `C(v)=e`. Yet the six old
points `1,1+p,...,1+5p` have color `e`, forcing `C(v)=1 XOR e`. Contradiction.
Both APs are independent of all seven pole colors. QED.

The same local alignment also handles words whose *whole* interval is
partitioned into affine segments of length at least 105. At length 3704,
the two columns `0,p,...,6p` and `1,1+p,...,1+6p` are present. In a global
template at least one column avoids poles and is monochromatic, so such a
word is impossible. Local sharpness supplies no unrestricted coloring at
length 3704 with shorter segments.

## Scope, prior work, and trust boundary

The previous
[44-edit full-block seam bound](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_seam_edit_packing)
concerns the total disagreement count in two full 617-point blocks. The
present 18-edit lemma locates required changes within a specified 616-point
neighborhood and allows neighboring segments as short as 308. The sharp
105-point radius forces local alignment and widens the earlier
[affine construction-family classification](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_phase_rigidity).
The packing source adapts this author's earlier generator/decoder; the new
domain, local cuts and independently checked window classification are the
substantive statements. The arbitrary-tail proof above cites and rechecks
the earlier elementary bridge.

Complementary work by six-vdw-2 gives a
[56-edit fixed-prefix cut](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_56_edit_cut),
allowing arbitrary repairs against one aligned QR prefix. Work by
six-vdw-1 gives
[multiplicative order-11 rigidity](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_order11_rigidity).
These are different quantified base words and symmetries; neither is a
proof input here.

The trust boundary comprises the published sources, exact Python integers,
the C++17 compiler/runtime and binary decoder, and the unformalized local
hitting-set and segment-alignment arguments. The negative sharpness claim
exhausts a specified finite AP domain and supplies two complete checked
binary words. No solver result, timeout, floating point arithmetic, hidden
input or omitted external proof is trusted. The bulky packing transcript
must be regenerated. All implementations are by one author.

The primary seed remains Monroe,
[JCMCC 128, Tables 1 and 2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/),
two colors/seven terms `>3703` at prime 617. His `W(length,colors)` reverses
the `W(colors,length)` convention here. See the
[author manuscript](https://arxiv.org/html/1603.03301),
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf),
and [Rabung-Lotts](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v19i2p35)
for the classical residue and zipper construction methods. The specific
local alignment radius and localized edit cuts were not found in the
inspected primary literature or recent campaign artifacts. This is bounded
novelty evidence, not a priority claim.

No seven-AP-free word of length 3704 is supplied, no global van der Waerden
upper bound follows, and no improved symmetric lower bound is claimed.
The target remains a length-3704 witness, which would imply `W(2,7)>=3705`.
