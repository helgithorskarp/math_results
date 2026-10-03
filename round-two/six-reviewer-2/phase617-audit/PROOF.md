# Independent six-phase617 classification

Actual author **six-reviewer-2**, independent mathematical reviewer. Target
LEMMA9963 by six-vdw-1, artifact
**bafkreiaix7o5tw6djqvwsldeyhn5mgerxflhky57qx3exw374kfs2ebxuy**, source
**17138953c8048fd723606e7e8bfc21da786d7c36**. Shared signing identity is not
independent authorship. Written mathematics was exposed; the new executable
source, row certificates, CNF/LRAT and expected records were unopened during
the independent reconstruction.

## Exact family and conclusions

On actual positions \(0\le n<N\), let \(L\) be zero on nonzero squares modulo617,
one on nonsquares, and undefined at zero. For each \(s\in\{0,\ldots,5\}\), choose
an independent arbitrary Boolean function \(F_s:\{0,1\}^3\to\{0,1\}\).
Outside the original root residues \(R=\{0,1,4\}\), prescribe

\[
c(n)=F_{n\bmod6}(L(n),L(n-1),L(n-4)).
\]

Every actual occurrence in all three original root columns is independently
free, including ignored inputs. There is no fourth pole, extra edit, root
identification, affine normalization or imposed relation between phases.
AP7 means seven actual positions \(a,a+d,\ldots,a+6d\), \(a\ge0,d>0,a+6d<N\).

The original theorem is confirmed: for every \(N\ge632\), each \(F_s\) is a
coordinate projection or its complement; the family maximum is exactly3703.
The independent refinement is stronger: **for every \(N\ge632\), all six
\(F_s\) are the SAME projection with the SAME output complement.** Thus only
six regular assignments survive, instead of the original necessary46656.
Original root occurrences remain free until actual AP constraints are applied.

At3702 there are exactly384 actual AP7-free colorings in this entire family.
They are the three common coordinate choices, two palettes, and any six-bit
word on the chosen character's six actual roots. All other original-root
occurrences have their corresponding character color.

At3703 there are exactly252 actual colorings. The common rule must be
\(F_s(b_1,b_2,b_3)=b_1\oplus\sigma\) in all phases. Every occurrence in columns1
and4 has its character color; the seven positions in column0 have any
nonconstant seven-bit word. There are \(2(2^7-2)=252\) such colorings.
At3704 there are none. These are exact counts of actual words, without any
color, translation, reflection or orbit quotient.

## Independent one-phase reduction

Encode a triple by \(k=4b_1+2b_2+b_3\); a truth byte has bit \(k\) equal to its
output. The six projection/complement bytes are15,51,85,170,204,240.
`rows.py` builds the field by the complete nonzero square set. It visits all
188700 actual APs at3704 with positive step divisible by6;182084 avoid every
original root. For each phase and each distinct set of realized labels, it
computes all monochromatic truth bytes and the least witness by
(endpoint,start,step). No supplied row certificate is a premise.

All1536 table/phase entries are accounted for. Exactly1500 have positive
root-free monochromatic witnesses; exactly the six projection/complement
bytes survive in every phase. The maximum witness lengths by phase0..5 are
553,632,387,460,437,438. Their263 distinct actual APs have largest step78.
All nonprojection witnesses are therefore inside the first632 positions.
Their colors depend only on one whole truth byte, since the step is divisible
by6. Root colors and other phase rows cannot affect the obstruction. Restriction
proves the necessary table conclusion for all larger \(N\).

The independent checker uses Euler characters, literal truth values and
start-first enumeration. It reconstructs every distinct label set and every
canonical witness, rather than importing the producer's field or masks.
All48 phase/label slots are actually realized by632, checked separately in
`basis.py`. Hence different projection/palette choices give different regular
actual words; the later sums of coloring counts have no duplicates.

## Synchronization of the six rows

Order the six choices as (coordinate,palette)
\((0,0),(0,1),(1,0),(1,1),(2,0),(2,1)\). There are exactly \(6^6=46656\)
independent phase assignments. For each of all32970 actual APs in the first632
positions, discard it only if it meets an original root;32283 remain.

For a retained AP and color \(c\), at each phase form the set of choices that
make EVERY point of that phase in this AP have color \(c\). An assignment is
monochromatic exactly when all six of its choices belong to those six sets.
Unvisited phases have the entire six-choice domain. `synchronize.py` removes
these Cartesian boxes from a complete base-six-indexed bit set. The surviving
set is exactly the six constant-choice vectors. A history of273 eliminating
actual progressions records every before/after count; its final endpoint is145.

The separate checker literally enumerates every one of46656 six-tuples,
evaluates the seven actual colors in those273 root-free leaves, and independently
recovers each first-elimination count and the six survivors. It uses no
producer masks or membership construction. A subset of valid original APs
suffices for this necessary implication; no unseen AP is assumed. The146
history endpoint is not claimed to be an optimum synchronization threshold
for arbitrary truth tables, which need the separate632 projection reduction.

## Complete actual-root classification

For each common projection/palette, all regular positions have a fixed color.
Give every original-root occurrence its own Boolean variable. There are18,
19 and20 such variables at3702,3703 and3704 respectively. Every ordinary AP
produces the following exact root restriction. If its fixed regular colors
include both colors, it imposes nothing. If they contain only \(c\), its
unknown roots cannot all equal \(c\). If it has no fixed regular points,
its roots cannot all equal0 or all equal1. This is a logical equivalence,
including APs with repeated residue columns; actual occurrences remain distinct.

`roots.py` visits EVERY original AP:1140216,1140833 and1141450 respectively.
It reconstructs all distinct root clauses with a canonical actual witness.
Their counts by the six common choices are:

| length | clause counts |
| --- | --- |
|3702|24,24,24,24,24,24|
|3703|26,26,27,27,28,28|
|3704|29,29,29,29,31,31|

Explicit unit implications force all occurrences of the two ignored original
roots to their baseline character color. At3702, the remaining six chosen-root
variables satisfy no further clause, giving64 completions for each of six
different regular words, hence384. At3703, choices0/1 leave precisely the two
seven-root clauses requiring a nonconstant word. Choices2..5 contain a checked
literal conflict. At3704 every choice has a checked literal conflict, including
the vertical APs starting0 and1 with step617. No root variable is silently
removed or linked.

A separate start/step enumeration using Euler characters reconstructs the
ENTIRE clause/canonical-witness collection for every choice and length. It
checks every actual unit implication, fixed root value, remaining clause and
conflict. For nonconflicting cases it enumerates every residual root word and
checks every complete original clause. Thus the counts include both necessity
and sufficiency, not only successful propagation or a solver verdict.
All records and full leaf sets are regenerated from source.

For independent attainment controls, `seeds.py` checks every1140833 actual AP
for each of four explicit3703 words: the single exceptional root color at0 or
3702, and both palettes. The target's last-root seed has ASCII SHA256
6293a318f5517dd993264ddac3cd6cdd027f6a2119c2b8f743fcb19639030244.
Removing its exceptional root value yields the actual monochromatic AP
\((a,d)=(0,617)\), a negative boundary control. Known character seeds are prior
art, not a new numerical van der Waerden bound.

## Scope and trust

The proof uses no graph numerical lemma, author CNF, LRAT, solver proposal,
large saved corpus, symmetry quotient or failed-search inference. The later
native proof check is separate corroboration. The finite field computation,
Boolean reduction, ordinary restriction and exact Python execution remain
unformalized. The root geometry0/1/4, phase period6 and absence of additional
regular edits are essential scope limits. Nothing here settles unrestricted
\(W(2,7)\), permits a3704 coloring, covers a fourth input or another geometry,
or claims sharp632 or historical priority.
