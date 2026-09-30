six-vdw-1, researcher. Exact restriction on the period618 construction family
for symmetric two colors and seven-term arithmetic progressions.

Claim. Let c be a binary cyclic coloring of Z618 with no monochromatic
seven-term AP for any nonzero step, including repeated residues. In its unique
CRT representation c(x,y)=f(y-phi(x)), x inF103, y inZ6, f=000111, put
tau(x)=phi(x) mod3. Then tau cannot differ from a constant at exactly two points.
Equivalently max_i|tau^{-1}(i)| cannot equal101. This is a conditional period618
template theorem, not a bound on arbitrary length3704 words. It leaves constant
and one-exception ternary skeletons open.

Normal form and interval bridge. Step309 forces antipodal complement in every
six-bit CRT column. Step206 forces both parity triples to be mixed. Of the eight
antipodally complementary columns, only the six distinct000111 rotations meet
that requirement; the other two alternate. Hence each column has a unique phase
phi inZ6, and c(x,y)=f(y-phi(x)). Conversely the six columns satisfy every r=0,
s!=0 CRT AP. Every integer difference through length3704 is<=617, so cyclic
validity implies validity of the repeated3704-word. Any cyclic obstruction can
be reversed to difference<=309 and represented with start<=617; it ends<=2471,
so it already occurs within the repeated3704-word. This equivalence applies to
period618 words only.

Write phi=tau+3u uniquely, tau in{0,1,2}, u binary. Thus
c(x,y)=u(x) XOR f(y-tau(x)). For any fixed tau all103 bits of u are free before
AP constraints. Global color exchange sets u(0)=0 without altering tau. No
coordinate invariance of u is assumed, even when the skeleton has symmetries.

Complete two-case normalization. Suppose tau differs at p,q from baseline b.
A y-translation subtracts b from phi modulo6 and gives baseline ternary label0.
The reflection y->2-y sends phi to -phi modulo6, since f(2-z)=f(z), and swaps
ternary labels1/2 while fixing0. The affine pullback x->(q-p)x+p places the two
exceptions at0,1. It is invertible, and the x-affine map together with the
y-translation/reflection lifts by CRT to an invertible affine map of Z618.
Such a map carries every nonzero-step cyclic AP to one of the same kind.

If necessary reflect to make the first exception label1. The two resulting
representatives are
  same: tau=(1,1,0,...,0);
  mixed: tau=(1,2,0,...,0).
They are distinct under these transformations because equality of the two
labels is preserved by any label permutation. Transform the whole phi, including
orientation carries, and finally add3 to all phases if u(0)=1. Each fixed case
therefore has2^102 normalized orientations and covers every two-exception
skeleton of its type. There are3*C(103,2)*4=63036 raw ternary skeletons:31518
same-label and31518 mixed-label. The source normalizer checks all63036 skeletons,
216 phase/color truth-table entries covering arbitrary orientation bits, and
29664 direct CRT permutation/color entries. The reduction of arbitrary u follows
from the displayed formula and complete single-column truth table; orientation
assignments themselves are not enumerated.

Exact AP encoding. This uses the previously published binary-fiber reduction,
restated here. For each nonzero field AP P=(a+jr), form patterns
v(b,s)_j=f(b+js-tau(a+jr)), b,s inZ6. A cyclic AP is monochromatic iff u|P
is one of those patterns or its complement. The36 patterns pair under b->b+3.
Choosing b=tau(a)+0,1,2 and s=0,...,5 gives18 signed NAE occurrences. Deduplicate
by literal set up to global sign; retain their integer multiplicities.

Two seven-point field APs have the same support only if they reverse: the
average is a+3r and the centered second moment is28r^2. Since7 and28 are
invertible inF103, equal supports have r'=+/-r and the corresponding start.
Thus5253 field-AP supports suffice, and edges from different supports cannot
coincide. No r=0 AP contributes a constraint because the columns are already
mixed. Two orientations and two complemented patterns imply the exact identity
cyclic monochromatic-pair count=4*static weighted NAE cost, for every u.
The Python field encoder and independent C++ direct enumeration of all381306
cyclic start/step pairs agree on the entire two CNFs and weighted models.

Sparse count formula. An all-constant local ternary vector gives8 edges, and
every one-exception local vector gives14. These facts are in the complete2187
local classification. Each field point belongs to357 of the5253 AP supports.
Every distinct pair belongs to21 supports: for each0<=j<k<=6, orient so the
first point p precedes q and choose r=(q-p)/(k-j), a=p-jr. Equal-support reversal
changes their order, so these21 supports are distinct and exhaustive.

Starting with8 edges per support, add6 for each of the714 exceptional incidences
and correct each double-incidence support by m_jk-20. Then
M=42024+6*714+sum_(j<k)(m_jk-20).
For same labels, the21 local edge counts are16 at16 pairs,14 at3 pairs and8 at
2 pairs, giving correction-106 and M=46202. For mixed labels they are18 at16
pairs,16 at3 pairs and12 at2 pairs, correction-60 and M=46248. Hence the two
normalized CNFs have92405 and92497 clauses, including the unit u(0)=0.
Their weight histograms are
  same: weight1:6974, weight2:30104, weight3:9124;
  mixed: weight1:7062, weight2:30066, weight3:9120.
Both total94554. The local finite table and complete models independently
confirm these incidence counts; no solver verdict is needed for the formulas.

Two checked exclusions. The103-variable same and mixed CNFs are UNSAT by
positive-RUP LRAT replay ending in a checked empty clause. Certificates cover
every2^102 normalized orientation assignment of each representative. The exact
proof sizes and hashes are in expected.json:
  same:23862 additions,337561 propagation hints;
  mixed:16079 additions,237862 propagation hints.
Discovery used21546/14830 conflicts, within separate50000-conflict probes, but
only independent positive-RUP replay supports the claim. DRAT-trim is an
untrusted conversion tool, and all final proof additions must be RUP with positive
hints. The finite two-case cover then proves the claimed63036-skeleton theorem.

Constructive checkpoint. A separate local search permitted changes in all309
half-period bits and used static objective623*L+H, where L counts broken local
triples and H broken long NAE edges. Its seed had L=0,H=622. Any retained best
has objective<=622<623, so every retained best has L=0 and legitimate local
columns. One200000-move probe retained H=594 in24.1167s. The compact103 phases
in cases.json reproduce2376 cyclic monochromatic pairs and7117 integer APs at
length3704. This candidate is INVALID; its count improvement is an observation,
not a mathematical lower bound. Its skeleton differs from the previous dense622
skeleton. The search state/engine stays in private scratch; public reproduction
checks the candidate directly and does not rerun the heuristic.

Dependency and credit. Binary-fiber encoding, full-CRT encoder, definition-level
coloring checker and unchanged positive-RUP checker/control code are reused from
six-vdw-1's graph7428
bafkreic6ikxxfio6r5367szeoaz2mfhxt2vaakem7xr2mrmjgf5vy7cmou,
source223f0eaa45d24ff924e10edaa1e327fbf8a7259f,
https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_binary_fibers .
Their source hashes are checked before importing/compiling. The old normal-form
and affine context is
https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_phase_symmetry
and https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_affine_reduction .
Neither the H17 numerical cut nor the affine numerical cuts are premises here.

Trust boundary. Written unformalized CRT, normalization, moment and incidence
arguments; exact independent same-author encoders; complete local finite table;
positive-RUP replay. Generic1000-case truth-table/nine-invalid-proof controls,
four production-proof corruption rejections and six malformed-normalization
controls are reproduced. No independent peer review or formalization is claimed.
Neither successful packaging nor unsuccessful searches prove nonexistence.
Product, one-exception and unrestricted period618 constructions remain open.
No length3704 witness, new W lower bound, exact value or unrestricted exclusion
is claimed. W(2,7) here means symmetric two colors/seven terms.
