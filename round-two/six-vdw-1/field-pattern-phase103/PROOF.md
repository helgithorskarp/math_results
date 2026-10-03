# Independent phase tables over F103 require five extra field columns

six-vdw-1, actual role researcher, 2026-10-03. This is an exact positive
certificate and ordinary proof for the symmetric two-color/seven-term
van der Waerden family. It excludes a proposed construction family and
provides repair cuts. It supplies no new numerical lower bound.

Let q=103 and L(x)=0 for a nonzero square in Fq and 1 for a nonsquare.
L(0) is undefined. Choose p in Fq, u nonzero, and retain the three
**original** character roots

    R = {p+u, p+2u, p+4u}.

The physical pole p and all of R are free columns, including every
root of an ignored input or of a constant Boolean rule. These four
columns are distinct. Away from them put

    T(x) = (L(x-p-u), L(x-p-2u), L(x-p-4u)).

For any positive integer m coprime to103, choose a completely arbitrary
Boolean function F_s:{0,1}^3 -> {0,1} **separately for every phase**
s in Z/mZ. The background at integer n is

    B(n) = F_(n mod m)(T(n mod103)).

There is no common XOR phase word, scalar truth function, palette
anchor, phase legality hypothesis, subgroup invariance or antipodal
assumption. Nonzero leading coefficients of the three affine character
inputs, their ordering and global palettes can be absorbed into each
arbitrary F_s by permuting/complementing its abstract arguments/output.
Values at the four free columns may be arbitrary and nonperiodic.

Let H be any subset of F103 outside {p} union R. Suppose a binary
coloring c agrees with B outside these four columns and H, and c is
seven-term AP-free. Then:

* On Z/(103m)Z, **|H|>=5**.
* On [1,N], **|H|>=5 whenever N>=408m+1**.

There is also a statement about individual positions, without assuming
that discrepancies come from a fixed set of edited columns. On the
cyclic domain, c must differ from B at **at least five nonroot/nonpole
positions in every phase**, hence at least5m positions altogether.
On [1,N] the same5m lower bound holds already within [1,409m], whenever
N>=409m. Each phase may use a different Boolean function.

For m=6 this gives five extra field columns by N=2449, and at least30
actual changed nonroot/nonpole positions by N=2454. These conditions
therefore apply to a proposed coloring of [1,3704] in this family.
They are necessary conditions; no repair optimum or repair sufficiency
is asserted. The unedited independent-pattern/phase6 family is impossible,
even with arbitrary nonperiodic choices at all four free columns.

## Four original APs explain the basic obstruction

Normalize p=0 and u=1. Encode a character tuple b as the integer
4b1+2b2+b3. All eight labels occur away from 0,1,2,4, in blocks of
sizes11,14,14,11,14,11,11,13. The following are actual seven-term APs
in F103; the listed points are reduced modulo103.

| Start | Step | Seven field points | Pattern labels present |
| --- | --- | --- | --- |
| 16 | 17 | 16,33,50,67,84,101,15 | 1,2 |
| 6 | 32 | 6,38,70,102,31,63,95 | 1,4 |
| 74 | 45 | 74,16,61,3,48,93,35 | 1,5 |
| 28 | 5 | 28,33,38,43,48,53,58 | 2,4,5 |

If these APs are all nonmonochromatic, the first three force the colors
at labels2,4,5 to be the common opposite of the color at label1. The
last progression is then monochromatic. This proves the unedited
field-table obstruction for all256 truth tables, without a solver.
It also explains why simply adding an independent phase coordinate
does not repair this particular character geometry.

## Five disjoint positive witnesses for every truth table

A table is encoded by a word w in {0,...,255}, with bit k its value at
abstract argument k. A global color complement preserves monochromatic
APs, so the128 even words, those with bit0=0, represent all256 tables.
This gauge never evaluates a character at a root.

[five-packs.csv](five-packs.csv) has exactly128 ordered lines. Each line
contains w and five literal (start,step) pairs. Every AP has seven
distinct field points, avoids all four free columns, is monochromatic
under the entire table, and its five physical supports are pairwise
disjoint. Thus each line occupies35 distinct columns. The whole3735-byte
certificate SHA256 is

    296f67b8bf0cabe0682f7f5c8ae8c00d5e3d30173dab0fa1f8bd478e18bb891c

[produce.py](produce.py) constructs these positive witnesses with Euler
characters and an integer support-mask greedy search. Search failure
would be an incomplete proposal; the search is not used to establish
an optimum, maximum packing or absence. [check.py](check.py) imports
no producer function. It uses Gauss's character criterion, literal
points, explicit sets, actual table colors and independently searched
modular inverses. It checks every original case/point, whole certificate
bytes and every disjointness condition. Five is the verified achieved
packing size, not a claim that a larger packing is impossible.

If at most four columns are edited, one of the five disjoint APs avoids
them. It also avoids the original roots and physical pole. All its
points retain their background colors and it stays monochromatic,
regardless of values elsewhere and their periodicity. The same argument
requires at least five actual discrepancies in a fixed phase when
edits are specified as individual positions.

## Entire affine family, with the original roots preserved

For y=p+u*x and r in {1,2,4}, multiplicativity gives

    L(y-(p+u*r)) = L(u) XOR L(x-r).

The map is a field bijection, takes 0 to p, and takes all three original
roots to R. The whole tuple is complemented if u is a nonsquare; this
is absorbed into the arbitrary truth table in the chosen phase.
The positive packing and all support disjointness are preserved.
Hence every one of103*102=10506 ordered pole/unit configurations is
covered, including ignored-character truth functions with the same
four original free columns retained.

The checker literally verifies the **whole input basis** at every
configuration:1040094 nonroot/nonpole field points and3120282 actual
character entries, as well as every full103-point affine bijection and
free-column map. It additionally transports all four kernel APs through
all10506 configurations, checking42024 actual original cyclic618 APs
and their2449 integer lifts, with294168 literal points.

It separately transports the entire128-table five-pack certificate
through all102 scales at p=0 and **each of the six phases**, checking
78336 cases,391680 actual original APs and2741760 points with full
colors, disjointness and positive integer lifts. All translated
five-packs follow by ordinary substitution in the fully checked affine
input basis. We do not claim literal iteration over every translated
five-pack at every pole, or over the infinite set of phase moduli.

## CRT lifting and the exact interval bounds

Fix a phase s and choose its positive representative t in {1,...,m}.
Every field start A occurs at exactly one n=t+m*k, 0<=k<=102, because
m is invertible modulo103. For a transported field AP with nonzero
step D, let delta be the representative of m^-1*D in {1,...,102}.
If delta>51, reverse the seven-term field progression and use103-delta.
This preserves monochromaticity and its column support. With the
appropriate k, its integer lift is

    n, n+m*delta, ..., n+6m*delta.

All seven terms are distinct positive integers, share phase s, have
exactly the required field coordinates, and avoid every free column.
Its final term is at most

    t+102m+6*51m = t+408m.

For the single phase represented by t=1 this is408m+1, proving the
column bound at that length. For all phases t<=m gives409m, proving
the5m position bound. Within any one phase the five supports are
disjoint; positions in different phases cannot coincide.

On the cyclic domain103m the same formulas define nonzero steps
m*delta. Every seven-term AP has seven distinct field columns and
therefore seven distinct residues. This is valid under the campaign's
cyclic convention, which in general also allows repeated residues.
There are no cyclic-to-integer identification or endpoint assumptions.

## Prior work and trust boundary

Primary background is Monroe,
[New lower bounds for Van der Waerden numbers using distributed computing](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/),
Table1 length7/two colors >3703 and Table2 prime617; and Herwig et al.,
[A new method to construct lower bounds for van der Waerden numbers](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf),
for power residues and cyclic zippers. Rechecked2026-10-03. Monroe's
length-first W(7,2) is the campaign's color-first W(2,7). These are
seed/context checks, not an exhaustive current-world-record absence
or a historical method-priority claim. The asymmetric w(3,k) problem
is different.

The peer [Boolean-character result9785](../../six-vdw-3/boolean-character-obstruction618/PROOF.md)
(source dc3802580b5440773c6444a72e79a5e83459278d) and its independently
selected [review9851](../../six-reviewer-4/boolean-character-audit/REVIEW.md)
(source dedbf0a9731b7c708d869b10030c0385fc4afa0e) concern a **common XOR
phase word** and arbitrary affine root configurations. Their nine-edit
bound is stronger on their scalar family. Our five-edit bound concerns
independent phase truth tables at the specific four-column geometry
p,p+u,p+2u,p+4u, and all coprime phase moduli. It is not a numerical
strengthening or a restatement of that nine-edit theorem. No review
verdict transfers to this new result.

The earlier [independent-pattern phase310/620 result9844](../character-pattern-phase310/PROOF.md)
(source1e9ba75da05cbe9b0d642801384e38259e1efa2e) closed an F31 family.
Here the field103 obstruction and positive packing are checked directly;
there is no dependence on that RUP proof or a native solver. The peer
[constant-phase F617 cap9842](../../six-vdw-3/boolean617-core-filter/PROOF.md)
(source2ac23f7cc84ade9f135c1f14bbd3ffe70b3f406d) is complementary
construction context; it supplies no premise for this F103 theorem.
The current peer [H7 phase endpoint result9865](../../six-vdw-2/order7-phase-eleven/PROOF.md)
(source7d528cf2d6024800c8fbb199044b8371e1922694) restricts a separate
F617 subgroup family to nonconstant phase weights11..33. Its exclusion
and conditional exactTEN rules supply no premise or verdict here.

Trust consists of ordinary character multiplicativity, Boolean palette
substitution, finite disjointness and CRT/interval arguments, plus exact
standard-library Python checking of the compact positive certificates.
This is not a proof-assistant theorem or an independently selected
external review. Euler/mask generation and Gauss/set checking are two
algorithms owned by the same researcher; normal/O equality is a
regression check. No UNKNOWN, timeout, incomplete enumeration, proposed
repair-size cut or solver status is used as a mathematical premise.
The initial33-input full odd309/even618 model was independently audited
and remains private; the four-AP proof removes it from the public trust
chain. No bulky model or proof corpus is needed for replay.
