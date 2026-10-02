# Independent majority-character normalization and positive packs

Actual author **six-reviewer-4**, role **independent mathematical reviewer**.
The defining graph proof of LEMMA9745 was visible. This is not a blind review.
Target executable, certificate and expected contents were unread when this
independent mathematical packet was first sealed.

Put \(p=103\), \(T=618\), and
\(\sigma=(0,0,0,1,1,1)\). On nonzero field elements let \(L\) distinguish
squares (zero) from nonsquares (one). Consider the majority of three
affine characters, with nonzero affine slopes, XOR an output palette and
an arbitrary binary six-row phase. All original root columns remain
free, including roots whose character disappears after cancellation.
Additional edited nonroot columns may have arbitrary nonperiodic colors.

For three distinct roots, normalize the first two to zero and one by
\(r=sx+a\), \(s\ne0\). Multiplicativity changes each character by its
leading sign. A simultaneous complement of three inputs complements
their majority. Thus the first input sign can be removed into the output
palette, leaving exactly the states
\((t,d_2,d_3)\), \(t\in\{2,\ldots,102\}\), \(d_2,d_3\in\{0,1\}\).
There are 404 states, with roots \(0,1,t\).

Permute the ordered signed roots, then normalize the first two again.
The induced state map is the formula in `relabel`. If the permutation's
first root has offset \(a\), its first-two difference is \(s\), and its
first palette is \(d\), then
\[
 f_z(sx+a)=f_w(x)\oplus L(s)\oplus d.
\]
The last two relative palettes are unchanged by the common \(L(s)\).
Normalization composes with root relabeling; this is an \(S_3\) action
on parameter states. It need not classify words under every automorphism.

Identity fixes 404 states. A transposition fixes two states: for swapping
the first two, \(t=1/2=52\), \(d_2=0\), and \(d_3\) is free. A three-cycle
fixes two states, with \(t^2-t+1=0\), \(t=47,57\), and both palettes zero.
Conjugacy supplies the other transpositions/cycle. Burnside gives
\((404+3\cdot2+2\cdot2)/6=69\) orbits. Independent breadth-first closure
under two generators checks the complete partition: 66 orbits of size
six, two of size three, and one of size two. Full six-map composition
and all 100 regular-point color identities per state/map are checked.

`construct.py` uses explicit square sets and the sign identity
\[
\operatorname{sign}(\operatorname{Maj})
 = (A+B+C-ABC)/2.
\]
It enumerates field seven-AP supports and matches their orientation words
to the six-row phase patterns. A fixed finite proposal budget selects
nine disjoint supports per representative. The output is a positive
certificate; proposal failure would prove no impossibility. Neither an
exact packing optimum nor a sufficient repair is claimed.

`independent.py` imports no constructor or target code. Its character
oracle is Gauss's lemma (parity of reduced half-system representatives
above \(p/2\)); it checks agreement with all explicit squares and all
10404 multiplicativity inputs. Majority uses the middle of three sorted
bits. Every certificate AP is checked term by term for a nonzero cyclic
step, absence of roots, one color, seven distinct columns, and support
disjointness. It reconstructs 69 parameter components independently.

For a map from an arbitrary normalized state to its representative,
lift \(s,a\) by CRT to \(\alpha\equiv s\pmod{103}\),
\(\alpha\equiv1\pmod6\), \(\beta\equiv a\pmod{103}\),
\(\beta\equiv0\pmod6\). The map \(n\mapsto\alpha n+\beta\) takes a
representative AP into the given state. \(\alpha\) is a unit modulo 618.
Directly checking the resulting seven points independently resolves the
coordinate direction and possible common color exchange. All 404 packs
are verified, with their full points, columns, colors, and integer lifts
retained in a regenerable compactly hashed record.

For a legal phase rotation, a separate CRT translation absorbs that
rotation. Any affine field normalization and either output palette
likewise preserve monochromaticity and disjoint supports. Roots and
arbitrary edit sets are transported bijectively; no invariance of a
coloring or edit set is assumed. Nine disjoint nonroot supports require
at least nine edited nonroot columns, regardless of colors inside edits.

If a phase has \(g(y)=g(y+3)\), a step-309 seven-AP lies within one
field column and is monochromatic. If all three antipodal pairs are
opposite, the only two nonrotations of \(\sigma\) are alternating rows;
step 206 is then monochromatic within every field column. The verifier
checks all 64 phases, exactly six legal rows, and all 103 singleton
column lifts for every illegal row. Thus an illegal phase requires
editing every original nonroot column.

For exactly two distinct original roots, equal palettes on the repeated
root force its character, and opposite palettes force the other one.
For a single original root, all three characters reduce to one character
with the majority palette. The original root union is still free. The
genuine dependency is LEMMA9659's sixteen-regular-column character
obstruction: with two original roots one extra regular root is free, so
\(|H|+1\ge16\); with one original root, \(|H|\ge16\). The direct
repeated-root truth reductions are independently checked here. The
sixteen bound is imported with its own proof status, rather than inferred
from the majority certificate.

## Proved shorter interval bound

For a legal phase, a monochromatic cyclic AP cannot have zero field
step. Such a step would be 103,206,309,412 or515 modulo618; the resulting
phase progression, for each of the six legal rotations, is mixed.
Reverse an AP if necessary to give step \(1\le d\le309\).
The value 309 has zero field step and is excluded, so \(d\le308\).
Choose its first integer term \(a\) in \(1,\ldots,618\). The positive
seven integer terms are distinct and the last is at most
\[
618+6\cdot308=2466.
\]
Every untouched color agrees with the template at these integer terms,
even when edits elsewhere are nonperiodic. Consequently the distinct-
root nine-column obstruction already holds on every \([1,N]\),
\(N\ge2466\), uniformly in all original affine coefficients and phases.
This is a sufficient bound, not an optimal lift threshold.

For illegal phases choose the least positive residue among a full
step-309 two-cycle or step-206 three-cycle in the column. Its first term
is at most 309 or206; the endpoint is at most2163 or1442 respectively.
Thus the stronger all-nonroot-column edit condition holds already for
\(N\ge2163\).

The prior independently verified character review9693 proved its full
sixteen-column bound for \(N\ge2460\), and its illegal-phase bound for
\(N\ge2163\). Therefore the repeated-root15/16 branches, and hence the
entire majority theorem, hold for \(N\ge2466\). This citation supplies
only the character branch; it does not transfer a verdict to majority.

## Hamming and weighted consequences

Let \(u\) be an arbitrary field word with hole set \(E\). For a
distinct-root majority reference with root set \(R\), write
\(e=|E\setminus R|\), \(D=\mathbb F_{103}\setminus(E\cup R)\), and let
\(d\) be its Hamming distance from \(u\) on \(D\). Each reference
support must meet a nonroot hole or a disagreement; hence
\(d\ge9-e\). Applying the complemented reference gives
\((100-e)-d\ge9-e\), or \(d\le91\). Thus
\[
9-e\le d\le91,\qquad
\left|\sum_{x\in D}(-1)^{u(x)+f(x)}\right|\le82+e.
\]
With at most three holes the lower bound is at least six. These are
necessary conditions; they neither exclude all arbitrary words nor
suffice to construct a repair. The roots are never counted twice.

The disjoint-pack proof also gives a fractional consequence: any
nonnegative weight on regular columns whose weight sum on each of the
nine certified supports is at least one has total mass at least nine.
This follows simply by summing over disjoint supports. It applies only
to the specified supports and supplies no integer-cover optimum.

The normalization, phase, Burnside, CRT, lift, dependency interpretation
and hitting implications are ordinary unformalized mathematics. Finite
checks establish the positive packs and exact identities, with CPython,
integer arithmetic and input decoding in the trust boundary. The work
does not improve a numerical van der Waerden lower bound.
