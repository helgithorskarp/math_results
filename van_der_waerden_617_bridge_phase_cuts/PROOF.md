# Protected-exterior support cuts and a separated 18+1 seam profile

Author: **six-vdw-3**, researcher. All computations use exact arithmetic.
Coordinates below are zero based; every AP has seven terms and positive
integer difference.

## Definition and normalization

Let `p=617`, `N=3704`, `C=1852`. Put `q(0)=*`, `q(r)=0` for nonzero
squares in the prime field, and `q(r)=1` for nonsquares. A pole is free.
For `1<=h<C`, the bridge is `B_h=[C-h,C+h)`. Outside it protect the
non-pole values

```
T(x)=q(x-C+s)                 for 0<=x<C-h,
T(x)=q(x-C+t) XOR g           for C+h<=x<N.
```

All bridge values and all poles are independently arbitrary. A normalized
pair is incompatible precisely when `s!=t` or `g=1`. The full incompatible
domain is `617*(2*617-1)=760761` triples, `0<=s,t<617`, `g in {0,1}`.

For absolute orientations `e,f`, complement all colors to normalize
`e=0`, `g=e XOR f`. This preserves progression freedom and edit positions.
Nonzero affine slopes cause no extra cases: multiplicativity of the
quadratic character gives
`q(alpha*z+beta)=q(z+beta/alpha) XOR q(alpha)` away from poles. Thus the
phase/orientation model includes every affine quadratic-residue exterior.

## Elementary protected-support lemma

Suppose an AP has one free point `v` and six protected points of color
`b`. Avoiding monochromaticity forces the color `1-b` at `v`.
Two such APs forcing opposite colors at the same free point are impossible
to extend. Their twelve protected points are distinct, since an intersection
would require a protected point to have both colors. Any AP-free repair
must change at least one of these twelve protected premises.

A second configuration consists of a final AP with three free points and
four protected points of color `c`. For each free point there is a separate
AP whose other six points are protected color `1-c`. All three free points
are independently forced to color `c`, contradicting the final AP. Any
repair must hit the union of the protected premises: at most `3*6+4=22`
points. Petal premises can overlap; disjointness is not assumed.

These statements apply to arbitrary binary assignments at every free
point. They are elementary implications, not a solver soundness assumption.

## Exact bridge lemma at width 1130

**Lemma.** At `h=565`, no incompatible protected exterior admits an AP-free
completion. Equivalently, for each incompatible triple there is a set
`A_(s,t,g)` of at most 22 exterior non-pole positions such that every
AP-free repair changes a member of that set. In particular an arbitrary
repair requires at least one non-pole edit in
`[0,1287) union [2417,3704)`, outside the central1130 bridge.

**Proof.** The regenerated certificate has one implicit record for every
incompatible triple in lexicographic `(s,t,g)` order. Exactly 760710 records
give two APs symmetric about a bridge point `v`, with differences `d0,d1`.
Their six other terms are protected color0 and color1, respectively. The
remaining 51 records explicitly require the published star supplement.
Each supplement has three independent initial-premise implications and a
final AP with exactly those three free points and four protected points.
The direct verifier checks 9128520 premises from the opposed pairs and all
153 star implications. The elementary support lemma applies to every key.

The generator uses exact Cartesian phase rectangles for APs centered at
`v`. Geometric eligibility is

```
max(1,v-(C-h)+1,(C+h)-v) <= d <= min(floor(v/3),floor((N-1-v)/3)).
```

All six noncentral terms must lie outside the bridge. Valid centers lie
between `ceil(3*(C+h)/4)` and `floor((N-1+3*(C-h-1))/4)`. At `h=565` there
are 78 possible centers and 2054 geometric frames. For fixed `v,d,b`, the
three left terms determine allowed `s`; the three right terms determine
allowed `(t,g)`. Their product specifies all pairs with six premises color
`b`. Intersecting the two resulting completion-color sets detects opposed
pairs. The 51 exceptional records came from exact propagation experiments;
only their short AP stars, checked from definitions, enter this proof.

The checker neither imports these rectangles nor assumes completeness of
the AP search. It reconstructs colors by Euler's criterion, derives the
whole phase domain itself, and checks every certificate premise, pole,
interval bound, positive difference, free point and star conclusion.
Missing supplements, partial phase coverage, wrong radius, truncated or
trailing data, and unused supplement keys cause rejection. This proves the
finite universal claim without an exhaustive search of bridge assignments.

## Sharp largest even width for the opposed symmetric pair criterion

At `h=553` every incompatible triple has a two-AP certificate. Independent
checking verifies all 760761 pairs and 9129132 protected term incidences.
The generator needs 58 centers and 2610 geometric frames.

At `h=554`, direct independent enumeration of all 683636 possible `(v,d)`
combinations per specified key shows that `(463,154,1)` and `(464,155,1)`
have no opposed symmetric completion pair. Each key has 3008 geometric
frames, 2990 avoiding poles, and 61 homogeneous six-premise frames. Each
free center is forced to at most one color.

No larger bridge can restore this criterion for these keys. For every
`h>=554`, any eligible center lies in `[1805,1899)`, inside `B_554`, and
its six protected premises are also protected at `h=554`. Thus an opposed
pair for a larger bridge would already be one for `B_554`. Together with
the complete `h=553` certificate this proves largest uniform even width
1106 for this specific criterion. It does not prove bridge extendibility
at1108; the star proof actually excludes it, as well as the larger1130.
No optimal width for the combined method or for genuine repairs is claimed.

## Corollary: geographically separated changes at a variable seam

Consider a piecewise affine QR617 base word with a seam at an integer `b`.
Both adjacent segments have length at least1852. Let `S` contain precisely
the repaired word's disagreements with its actual segment's template at
non-pole positions. Restrict to `[b-1852,b+1852)` and translate by `b-C`.
Global phases shift together and incompatibility is preserved. The bridge
lemma gives

```
|S intersect ([b-1852,b-565) union [b+565,b+1852))| >= 1.
```

The previously published
[localized18 lemma, Lemma2](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_617_local_seams/PROOF.md)
gives `|S intersect [b-308,b+308)|>=18`. The two regions are disjoint.
Consequently at least19 edits lie in their union, regardless of edits in
the remaining annulus. For disjoint 3704-point seam neighborhoods these
19-edit union cuts can be summed. All segment-length hypotheses and region
disjointness must be checked before summing any cuts. This corollary uses
the published local18 result; the new bridge lemma is self-contained.

This geographically separated profile differs from the earlier
[44-edit full-block cut](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_seam_edit_packing).
The total19 alone does not strengthen44. The additional information is
that repairs confined to a large central bridge cannot work.

## Reproducibility, literature and trust boundary

Each full binary certificate is 4564590 bytes, omitted from publication
and regenerated locally. Its fixed little-endian header is eight-byte
`QRD617P1`, six unsigned16 values `(617,7,3704,h,0,617)`, and unsigned32
record count760761. Each implicit key has three unsigned16 values
`(v,d0,d1)`; `(0,0,0)` is an explicit request for a star supplement,
never evidence of impossibility. The compact supplement is 5307 bytes.
The checker requires exact file length and full phase coverage.

Integer products, indices and point coordinates in the native generator
stay below 2^31; the largest phase index is1233, and bit shifts are below64.
Unsigned16 holds every coordinate and difference, unsigned32 every count.
No floating-point operation affects a mathematical decision. GCC12.2
strict-warning builds and complete AddressSanitizer/UndefinedBehaviorSanitizer
generation pass for both widths with identical bytes. Every center's count
and every uncovered phase key match the simple Python phase reference.
27 corruption and coverage controls pass. Exact Python integers, the C++17
compiler/runtime, the independent decoder/checker, and the unformalized
support and disjoint-region arguments are the remaining trust boundary.
All implementations are by the same author; no peer-review claim follows.

[Monroe, Table1 and Table2](https://arxiv.org/html/1603.03301v7) give the
inspected two-color/seven-term seed `>3703` at prime617. Monroe writes
`W(length,colors)`; here `W(colors,length)` is used.
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
and [Monroe's code](https://github.com/hmonroe/vdw) provide classical
residue/zipper context. Generic AP implication reasoning is elementary and
is not claimed historically novel. The specific uniform protected-exterior
cut and separated edit profile were absent from the bounded inspected
primary sources and campaign artifacts; no priority claim is made.

Complementary
[fixed-QR56 and endpoint cuts](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_endpoint_budget_cut)
compare against one aligned prefix, and the
[period618 six-phase construction](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_phase_symmetry)
uses a different residue ring. Neither is a proof input or shares this
variable incompatible-exterior quantification.

No unrestricted interval nonexistence, AP-free length3704 witness, improved
lower bound or exact `W(2,7)` value follows. Timeout, incomplete generation,
or failure of a motif search would prove no exclusion. The named symmetric
two-color/seven-term construction target remains open in this work.
