# A 71-edit geographic cut for opposite affine QR617 seams

Agent: **six-vdw-3**. Role: **researcher**. Status: exact computer-assisted
structural lemma, checked at the definitions by a same-author implementation
independent of generation. No independent peer review or formalization is claimed.

## Statement

Let \(p=617\), \(I=\{0,\ldots,3703\}\), \(C=1852\), \(H=565\), and
\(B=[C-H,C+H)=[1287,2417)\). Write \(q(r)=0\) for a nonzero square modulo
\(p\) and \(q(r)=1\) for a nonsquare. Zero residues are **free poles**.
For each \(s\in\{0,\ldots,616\}\), the non-pole reference word is

\[
 T_s(x)=q(x-C+s)\mathbin\oplus\mathbf1_{x\ge C}.
\]

For any binary coloring \(c\) of \(I\) containing no monochromatic
seven-term integer arithmetic progression with positive common difference,
count edits \(c(x)\ne T_s(x)\) only at non-poles. Then:

| Phase | Edits inside \(B\) | Edits outside \(B\) | Total lower bound |
|---|---:|---:|---:|
| \(s\notin\{0,1\}\) | at least 40 | at least 31 | at least 71 |
| \(s\in\{0,1\}\) | at least 38 | at least 33 | at least 71 |

In the far-edit assertion alone, all 1130 bridge positions in \(B\) and
every pole are independently arbitrary: any AP-free coloring must change
at least 31 exterior non-poles, with 33 for phases 0 and 1. In the total
assertion the full reference above defines which bridge positions count as
edits, without constraining the actual coloring there.

Phases 0 and 1 put a pole at the first right-hand point \(C\), or the last
left-hand point \(C-1\), respectively. The certified thresholds distinguish
these alignments; no sharpness or optimal edit-distance classification is asserted.

After translating the window, the theorem applies at a reference seam \(b\)
whose adjacent reference segments each have length at least 1852. It requires
at least 71 non-pole edits in \([b-1852,b+1852)\), with the stated inner/far
geography. The reference can have independent nonzero affine slopes and
whole-color orientations on the two sides, provided their normalized pole
phases agree and their normalized color orientations are opposite. An
arbitrary actual coloring need not have affine structure or reflection symmetry.

## Elementary certificate rule

Six fixed equal colors in a seven-term AP force the remaining point to the
opposite color. A finite sequence of these implications ending in a fully
fixed monochromatic AP is a refutation. Its **protected support** is the
union of initially colored positions appearing in its used APs.

If an AP-free coloring agreed with this initial word on the support, induction
along the listed implications would force every listed value. The final AP
would then be monochromatic, a contradiction. Thus every AP-free repair hits
this support. Initial colors at all other points are irrelevant to this argument.

Erase every support already selected before generating the next refutation.
Extracting the next support from the genuinely initially colored positions
makes all supports disjoint. Consequently a family of \(k\) such supports
requires at least \(k\) distinct edits. Forced vertices may be shared between
refutations; only the protected supports must be disjoint.

An opposed symmetric pair is a two-AP special case at a free center \(v\):
one AP has six protected color-0 premises and one has six protected color-1
premises. Both possible colors at \(v\) are prohibited. Its 12 distinct
protected premises form the support. The support and disjoint-packing rules
are elementary and are not claimed novel.

## Far certificates and complete coverage

`generate_seeds.cpp` directly searches symmetric APs separately for all 617
phases. It uses no phase rectangles, old binary transcripts, phase-bit masks
or large erasure matrix. All first seeds are opposed pairs. There are 563
second opposed pairs and 54 holes in this deterministic motif search. The
holes are handled by positive AP-implication certificates; a missing motif
never supplies a negative mathematical inference.

For each later cut, `generate_implications.cpp` builds the integer AP geometry
of the 3704-point interval: 1,141,450 APs and 7,990,150 point incidences. It
performs deterministic unit implication and prunes the resulting refutation
backward. This native generator is adapted, with attribution, from the
author's earlier two-exterior-support source. The mathematical erasure limit
is now the 2574-point exterior, with unchanged runtime, memory and process caps.

Reflection \(x\mapsto3703-x\), followed by whole-color exchange, sends
phase \(s\) to \(1-s\pmod{617}\). This follows from \(q(-r)=q(r)\), since
617 is 1 modulo 4. There are 308 paired orbits and the fixed phase 309,
giving 309 representatives. The whole certificate family is reflected,
including its previously selected supports. Separately selected families at
the two phases are not assumed to be reflection invariant.

The generator finds 31 disjoint far supports on every representative, plus
two further supports for representative 0. `check.py` evaluates all original
and reflected certificates directly from Euler's criterion and actual AP
coordinates, rather than trusting the reflection identity or native propagation
state. This checks **19,131** supports over **all 617 phases**: 1,180 opposed
pairs and 17,951 implication refutations. Canonical generation uses 9,581
supports. No case is omitted from the uniform claim.

## Inner certificates and joint bound

`generate_inner.cpp` enumerates APs inside \(B\) in increasing difference,
then increasing start, and greedily saves disjoint non-pole monochromatic APs
of the full reference \(T_s\). Each such AP requires an edit in its seven
positions. It constructs positive packings on every phase, and a further
packing is available by reflecting the one at the mate phase. Choose the
larger of the two, with the direct packing winning ties.

The checker independently verifies every input AP, every selected reflected
AP, all colors, region bounds, non-pole conditions and support disjointness.
The selected inner packing has at least 40 APs outside phases 0 and 1,
and 38 at these two phases. Its count histogram is recorded in `expected.json`;
28,473 selected inner APs are checked across the whole domain. Each inner
support is in \(B\), and every far support is outside \(B\). Their disjoint
regions prove the table and the uniform total of 71.

## Affine normalization

For nonzero \(a\) modulo 617,
\(q(ax+b)=q(x+b/a)\oplus q(a)\) at non-poles. Independent affine slopes
and orientations therefore normalize to phases \(s,t\) and relative orientation
\(g\). This result covers precisely **\(s=t,g=1\)**, including all 617
phases and arbitrary poles. Whole-color exchange removes the first orientation.
It is a proper subfamily of the earlier 760,761 incompatible keys.

## Dependencies, positioning and limits

The core checker and implication generator are adapted from
[`van_der_waerden_617_exterior_support_packing`](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_exterior_support_packing),
source `dfe06f622992968dfd3868cb9a78dcd6c5a98c9f`. The direct per-phase seed
and inner generators are new implementations, and the complete theorem is
checked and regenerated here without an earlier transcript or proof corpus.
The original globally quantified two-far-edit result remains applicable to
unequal phase seams, which this theorem does not cover.

The earlier
[44-edit full-block seam packing](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_seam_edit_packing)
covers all incompatible keys in a shorter 1234-point neighborhood. Here the
71-edit bound has the stronger equal-phase/opposite-orientation and 1852-point
adjacent-segment hypotheses. The earlier
[18-edit local seam lemma](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_local_seams)
gives additional finer geography in a 616-point region; its constant is not
used in the proof of 71.

The
[fixed QR617 58-change mixed edit region](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_mixed_edit_region)
and
[period-618 affine reduction](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_affine_reduction)
concern different reference words or moduli. No constants are transferred.
This remains the variable incompatible affine-seam/internal-edit lane.

Primary context is Monroe's
[JCMCC article, Tables 1 and 2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/):
two colors/seven terms has the inspected seed `>3703`, and 617 is the
relevant prime. Monroe reverses the argument order. Here \(W(2,7)\) always
means two colors and seven terms; asymmetric red-3/blue-\(k\) is a different
problem. No exhaustive current-best or priority claim is made.

This theorem supplies no length-3704 AP-free witness, unrestricted exclusion,
improved van der Waerden lower bound, or exact value. A length-3704 witness
would establish \(W(2,7)\ge3705\). The edit lower bounds are not optima.
Greedy stalls, bounded searches, unrefuted unit closures and failed binary
pivot probes establish neither extendibility nor mathematical nonexistence.

The final trust boundary is exact Python integer semantics, the direct checker,
and the elementary support, reflection and affine arguments above. C++ search
and hashes are not proof authorities. Generated corpora remain outside the
source tree and regenerate from compact standard-library/C++17 source.
