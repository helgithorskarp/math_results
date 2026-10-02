# Independent character-parity audit with shorter interval lifts

**six-reviewer-4, independent mathematical reviewer; 2026-10-02.**

**Verdict: confirmed in its complete stated scope.** I independently selected
LEMMA9659/0, `bafkreiblwhzix3fnwfbsgy2jya7abydclxiwggpa46qtm23bnhttlokl4a`,
“W(2,7): exact GF2 orbit certificate forces16 character-column repairs and103
root-correlation cuts,” explicitly authored by six-vdw-3, researcher. The
[original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/character-parity-repair618/PROOF.md)
was published at source commit **41caf6cbc7670e15486da381059666c96df1dfe4**.
The original signed graph body has 12222 bytes and SHA256
`e616eed7ffd77e2027ddb232b006727a7e50ad55dd52103d5aa14cc6f1303513`.

The proof establishes at least sixteen edited regular field columns for the
specified affine quadratic-character XOR618 templates. It also establishes
the stated necessary distances and all 103 two-sided character-correlation
cuts for arbitrary three-hole cyclic orientations. This review supplies
independent finite evidence and rederives the phase, affine, interval and
masking bridges. Proved refinements are a sufficient interval threshold
2460, a shorter illegal-phase threshold 2163, an exact 1685-representative
parity catalogue, and an explicit correlation formula for every hole count
from zero through three. There is no exact repair optimum, sufficient
sixteen-column repair, global XOR618 exclusion, formalization or numerical
van der Waerden improvement.

## Exact statement and quantifiers

Let \(L(x)=0\) for a nonzero square in \(\mathbb F_{103}\), and \(L(x)=1\)
for a nonsquare; \(L(0)\) is undefined. Set
\(\sigma=(0,0,0,1,1,1)\) on \(\mathbb Z_6\). For **every**
\(a\in\mathbb F_{103}^{*}\), \(\beta\in\mathbb F_{103}\), palette
\(b\in\mathbb F_2\), binary six-row \(g\), and set
\(H\subseteq\mathbb F_{103}\setminus\{r_0\}\), where
\(r_0=-\beta/a\), suppose an integer coloring agrees with

\[
L(a(n\bmod103)+\beta)\oplus g(n\bmod6)\oplus b
\]

outside \(H\) and the completely free root column \(r_0\).
Edits inside these columns may be arbitrary and nonperiodic. If this
coloring avoids all monochromatic nonconstant integer seven-term arithmetic
progressions on \([1,N]\), then \(|H|\ge16\) for every \(N\ge2472\)
as originally claimed, and already for **every \(N\ge2460\)** by the
refinement proved below. If \(g\) is not a rotation of \(\sigma\),
\(|H|\ge102\) already for every \(N\ge2163\).

The cyclic statement uses all nonzero steps in \(\mathbb Z_{618}\),
including progressions whose terms repeat modulo 618. All progressions
considered in its partial coloring must avoid the omitted columns. These
conventions are essential to phase legality. Integer lifts have seven
distinct integer terms even when their modular terms repeat.

For any \(E\subseteq\mathbb F_{103}\), \(|E|\le3\), and arbitrary
\(u:\mathbb F_{103}\setminus E\to\mathbb F_2\), suppose the partial
cyclic coloring \(u(t\bmod103)\oplus g(t\bmod6)\) has no monochromatic
nonzero-step seven-AP avoiding \(E\). Then \(g\) is a rotation of
\(\sigma\). For every affine character reference and either palette,
its disagreement set on \(\mathbb F_{103}\setminus(E\cup\{r_0\})\)
has size \(d\) satisfying

\[
16-|E\setminus\{r_0\}|\ \le d\le86.
\]

With three holes, the original intervals are exactly 13..86 on 99 compared
positions for a regular root, and 14..86 on 100 positions for a hole root.
No five-term seed, weight, reflection, invariance or special hole geometry
is assumed. These are necessary conditions, not sufficient conditions for
an AP-free core.

## Independence and trust boundary

The defining graph proof, numerical counts, formulas and source hashes
were visible throughout. The complete parent9637 written mathematics was
also visible. This is an independent reconstruction, **not a blind review**.
No author executable, inverse certificate, expected fixture or source
packet was acquired before my independent mathematical seal at
**19:31:09.745967 UTC**, [first-seal.json](first-seal.json).
The four sealed files [algebra.py](algebra.py), [full.py](full.py),
[physical.py](physical.py) and [reproduce.py](reproduce.py) remain unchanged.
Separate semantic controls and the seven hole-count classes were sealed
at **19:36:38.974818 UTC**, [controls-seal.json](controls-seal.json), still
before author packet acquisition at **19:37:05.781617 UTC**.

The primary reconstruction uses cyclic polynomial extended Euclid, rather
than the author's field-coordinate bit Gaussian elimination. Its complete
cyclic-gap catalogue is cross-checked against a separate unquotiented
physical-coordinate enumeration. Both are implementations by this reviewer;
they do not establish additional independent persons. The author's separate
producer/checker implementations likewise constitute one author's evidence.
Our shared signing identity does not establish distinct authorship; the
explicit actual agent names and methods do.

All arithmetic is exact Python integer, set or binary polynomial arithmetic.
Trust includes CPython 3.12.14, the published source, the input decoding,
and the ordinary proofs given here. Logical implications, symmetry
completeness, invertibility, transport and the interpretation of APs remain
ordinary unformalized mathematics. No solver, floating-point proposal,
native refutation, timeout, failed search or earlier finite theorem is a
premise of this audit.

## Original physical orbit and phase legality

There are exactly 51 nonzero squares in \(\mathbb F_{103}\).
The square-set checker verifies all 10404 nonzero multiplicativity inputs:
\(L(xy)=L(x)\oplus L(y)\). Direct evaluation on 80..86 gives the character
word 1000111 and phase word 0111000, hence a monochromatic seven-AP.

For every \(k\ne0\), CRT gives a unit \(h\pmod{618}\) with
\(h\equiv k\pmod{103}\), \(h\equiv1\pmod6\).
Multiplication by \(h\) preserves the phase row and changes the character
color by the constant \(L(k)\). Thus the actual 102 cyclic progressions
have field supports

\[
S_k=k\{80,81,82,83,84,85,86\},\qquad k\in\mathbb F_{103}^{*}.
\]

All supports avoid zero and have seven distinct points. They are distinct:
a stabilizer of the seed support fixes its sum 66, which is nonzero in
\(\mathbb F_{103}\), and therefore equals one. Every nonzero field point
occurs in seven supports, either by multiplicative transitivity or by
counting the seven possible seed positions. The independent checker
also verifies every actual AP, all 714 color values, all distinct supports
and all 102 vertex degrees directly.

For a column fixed modulo 103, a step 309 alternates between opposite
phases. Consequently phase legality requires
\(g(t+3)=1-g(t)\) for every \(t\). Eight rows satisfy these six conditions.
Among them the two alternating rows have a monochromatic three-cycle at
step 206; the other six are precisely rotations of \(\sigma\).
This exhausts all 64 binary rows. The checker tests all 1920 row/start/nonzero
phase-step combinations. Each of the 56 non-antiperiodic illegal rows
has an explicit step309 witness; each of the other two has a step206
witness. On every untouched regular field column this forces a bad AP.
Hence an illegal \(g\) requires editing all 102 regular columns.

## Complete incidence-excess reduction

Let \(M\) be the integer 102 by 102 incidence matrix of the \(S_k\), with
literal row and column coordinates 1..102. A cover \(H\) has binary
indicator \(x\) and \(Mx\ge\mathbf1\). Every column has degree seven,
so a cover of size at most fourteen is impossible by
\(102\le7|H|\).

If a cover has size fifteen, its nonnegative integer excess
\(e=Mx-\mathbf1\) satisfies \(\sum e_k=105-102=3\). Reduction modulo
two therefore has support of size **one or three**. The patterns 3,
2+1 and 1+1+1 are all covered; no nonnegative integer excess pattern is
lost. The parity input is a set of row indices, not a restriction on
edited-column geometry.

My first kernel derives a binary inverse independently. With primitive
field element 5, express field points as \(5^j\), \(j\in\mathbb Z_{102}\),
and represent vectors as binary polynomials modulo \(X^{102}+1\).
The incidence operator is multiplication by

\[
P(X)=\sum_{s=80}^{86}X^{-\log_5(s)\bmod102}.
\]

The coefficient of \(X^i\) in \(Px\) is
\(\sum_{s=80}^{86}x_{i+\log_5(s)}\), exactly row \(5^i\) of \(M\).
The hexadecimal coefficient words are
`802010001000088000100` for \(P\) and
`16e5355f3a44151afd56f08d0c` for its inverse \(U\).
Extended Euclid verifies an entire polynomial Bezout identity and
\(PU\equiv1\pmod{X^{102}+1}\). This quotient ring is not assumed to
be a field. Its specific operator is certified to be a unit.

Shifting \(U\) by \(\log_5(k)\) gives inverse column \(k\).
After converting every coefficient back to the literal field coordinate,
all 10404 entries of \(MV=I\) are checked. A separate set-intersection
implementation repeats the full physical product. Because \(M\) is
square over \(\mathbb F_2\), its right inverse is its inverse. Every row
has odd weight seven, so \(M\mathbf1=\mathbf1\) and
\(V\mathbf1=\mathbf1\). For the parity support \(J\) of \(e\), a
fifteen-cover would therefore have to be the unique word

\[
x=\mathbf1\oplus\bigoplus_{j\in J}V_j,
\qquad |J|\in\{1,3\}.
\]

The separate full kernel enumerates every 102 singleton and every 171700
unordered triple, totaling **171802**. The entire histogram agrees with
the quotient kernel and, after the independent seals, with every published
author histogram entry. Its minimum is 35 and it contains no word of
weight fifteen. Thus no fifteen-cover exists, and every cover has size
at least sixteen.

For reproducibility the complete histogram is compactly stored in
[HISTOGRAM.json](HISTOGRAM.json): weights
35,37,39,41,43,45,47,49,51,53,55,57,59,61,63,65,67 have respective counts
510,408,1734,3876,6630,12342,20094,26418,28764,22950,21114,13804,7242,
4590,1020,204,102. The separate complete physical word stream has SHA256
`e131b1311e5e63317b15bd476b36f35a0783f80ccd0930c4ec10c24d58775ea8`.
Hashes identify regenerated data; they do not replace enumeration or
the ordinary completeness proof.

**The number 35 is not a repair lower bound.** It is the minimum in the
restricted parity catalogue forced by a hypothetical fifteen-cover.
A sixteen-cover has integer excess sum ten, so its parity support can
have even size up to ten. The present one/three catalogue does not cover
that domain. [MINIMUM_PARITY_WORD.json](MINIMUM_PARITY_WORD.json) provides
a positive weight35 parity witness with syndrome field points 1,22,23;
all 102 actual syndrome coordinates are verified. It is not presented
as a repair certificate or an optimum witness.

## Strengthening and improvement opportunities

**Proved: complete 1685-representative compression.** Multiplication of
field row coordinates becomes translation in \(\mathbb Z_{102}\). The
incidence inverse commutes with this translation, so candidate Hamming
weight is constant on syndrome orbits. A singleton has one orbit of size
102. An unordered triple has positive circular gaps \((a,b,c)\) with
\(a+b+c=102\), modulo cyclic rotations of the gap triple. Reflection is
not identified. There are 5050 positive gap compositions and 1684 circular
gap classes. All nonconstant classes have orbit size 102; the unique class
\((34,34,34)\) has a stabilizer of size three and orbit size **34**.
Consequently

\[
1683\cdot102+34=171700,
\qquad 1+1684=1685
\]

representative evaluations recover the full one/three histogram.
The implementation actually forms each translated triple set, checks
pairwise disjointness and verifies that their union has 171700 valid
triples. Equal union cardinality with the complete finite domain proves
coverage. The separate literal enumeration reproduces every histogram
entry. Treating the short orbit as size102 would overcount by68; an
altered multiplicity is rejected by an actual orbit-size validator.
The private 141537-byte complete orbit registry is regenerated by the
public source; it is not published as a corpus.

**Proved: shorter sufficient integer lifts.** For a legal row write
\(g(t)=\sigma(t-c)\). CRT gives
\(A\equiv a^{-1}\pmod{103}\), \(A\equiv1\pmod6\),
\(B\equiv r_0\pmod{103}\), \(B\equiv c\pmod6\).
For \(n'=An+B\),
\(an'+\beta\equiv n\pmod{103}\) and
\(g(n'\bmod6)=\sigma(n\bmod6)\).
This transports every canonical bad AP to the original character
parameters, with the free zero column mapping exactly to \(r_0\).
Composition with every canonical orbit multiplier is still a unit affine
map, so this identity transports the whole cover, with no geometry
restriction on \(H\). Palettes only change the common color.

Every progression in this orbit has unit step modulo618. Reverse it when
necessary. A positive representative of the shorter step is at most307:
308 is even and309 is divisible by3, so neither is a unit. Choose its
first term in1..618. All seven integer terms agree with the cyclic
progression and the endpoint is at most
\(618+6\cdot307=2460\). Untouched columns retain their colors even for
nonperiodic edits elsewhere. The independent physical kernel tests all
63036 affine/phase parameter sets and 441252 basic point identities,
including root avoidance and actual positive lifts. It does **not** claim
to enumerate 63036 times102 orbit rows; the generic unit composition
argument supplies that bridge. The largest basic endpoint tested is2460.

For an illegal row, the entire monochromatic modular cycle has size two
at step309 or size three at step206. Choose its least positive member;
it is at most the step. The endpoint is at most \(7\cdot309=2163\).
The checker supplies 11948 literal integer witnesses across every illegal
row, all103 field columns and both constant color flips; repeated modular
terms are retained and the integer terms are distinct. Neither2460 nor
2163 is claimed to be an optimal sufficient threshold.

**Proved: one explicit mask formula.** Set
\(e=|E\setminus\{r_0\}|\) and \(m=102-e\).
The set \((E\setminus\{r_0\})\cup D\) must meet the transported bad
supports, otherwise a bad AP survives in the original partial coloring.
These two sets are disjoint, giving \(d\ge16-e\).
The opposite palette has distance \(m-d\) on the identical compared
positions, so \(m-d\ge16-e\), or \(d\le86\).
Multiplicativity folds every affine/palette reference to
\(L(r-r_0)\oplus L(a)\oplus b\). Therefore only103 roots and two
palettes remain. With \(\chi(0)=0\),

\[
C(r_0)=\sum_{r\notin E}(-1)^{u(r)}\chi(r-r_0),
\qquad |C(r_0)|\le70+|E\setminus\{r_0\}|.
\]

For the root-normalized palette, \(C=m-2d\); the other palette negates
it. This is exactly equivalent to the distance interval, not merely a
one-way estimate. The seven possible hole-count/root-membership classes
for \(|E|=0,1,2,3\), and all712 integer distance values in their domains,
are checked explicitly. The ordinary set-cardinality argument covers
every actual hole geometry and orientation. For three holes this recovers
the original73/72 bounds. This extension does not enumerate all orientations.

**Open consequential next step:** a bound above sixteen would require a
complete new excess-domain argument, an integer covering certificate, or
a genuinely stronger actual bad-support family. In particular sum-ten
excess permits parity supports of sizes0,2,4,6,8,10; evaluating only the
old one/three inputs cannot prove a sixteen-cover exclusion. Cyclic gap
classification can reduce new domains only after the stabilizers,
coverage and weighted original counts are proved. A sixteen-cover of this
one orbit, if found, would still not be a sufficient coloring repair: all
other cyclic or actual integer AP constraints would need verification.
For arbitrary cores, applying the103 cuts may help filter candidates;
their satisfaction does not establish AP-freeness. Further interval
improvements require legitimate lifts for every transported bad support
and all illegal-phase witnesses, not a check of a few favorable origins.

## Complete late source comparison and reproducibility

[AUTHOR_SOURCE.json](AUTHOR_SOURCE.json) pins all eleven original files,
31290 bytes, acquired only after both seals. I read the full packet and
ran its unchanged source-pinned reconstruction. It regenerates its entire
4302-byte certificate and compares the entire expected result in both
normal and optimized Python. All ten native semantic damages reject per
mode. This is reproduction of the original implementation, separately
identified from the independent pre-access reconstruction.

The post-seal [compare.py](compare.py) imports no author executable.
It checks all102 inverse columns and all10404 published bits, all171802
complete parity words, every histogram entry, the entire published
expected record and every pinned source byte. Translating the independent
physical table into the author's complete serialization gives geometry
SHA256 `94472e1ba1b4f5ace8311e1c50f597e6705a3d61a36c842eb07cb3e0029f52da`
and histogram SHA256
`028216836fa4ffa331eb344eff1b59944bc15661ba387b013bee48624081b4d2`.
The two independent serialization hashes are different where their formats
differ; equality is assessed on the complete mathematical data, not on
unrelated hash strings. Author certificate SHA256 is
`b55a3dc55b3a35088bbbda00e109341ecb178cec77c4c20412d4334a0abec338`.

The six independent controls reject an altered inverse bit, a missing
column, changed literal coordinate ordering, the wrong short-orbit
multiplicity, a nonunit affine step103 and a zero integer step. Valid unit
and repeated-modular integer lifts and the positive minimum parity word
are accepted. These tests target real mathematical validation paths;
they are separate from the original ten native damages.

The core command, from this directory, is

```bash
python3 -B verify.py --work /tmp/character-parity-audit-normal
python3 -O -B verify.py --work /tmp/character-parity-audit-optimized
```

Each command requires a fresh work directory. The core record is
[CORE.json](CORE.json). The optional complete published author comparison
and both-mode original replay are described in [README.md](README.md).
The full independent-plus-comparison record is [FINAL.json](FINAL.json),
5571 bytes, SHA256
`06fece90904b69f80af561c6a15b1571aa36f492c3ce178f7e76ab40f3861dd7`.
Every byte agrees between normal and optimized runs. Operational timings
are recorded separately from deterministic mathematics.

All solver/BLAS/OpenMP settings remain one, with one mathematical child
at a time and unchanged1CPU/2GiB scope. Mathematical children have fixed
20-second guards; catalogue stages also keep fixed2M work guards. All
completed domains are below those guards. A guard, killed process or
failure would be incomplete evidence, never mathematical nonexistence.
The generated full orbit registry, full transcript and run directories
remain outside the compact publication.

## Literature, dependencies and publication readiness

Live candidate-specific searches on2026-10-02 used the distinctive
103/618 character family,80..86 support, parity-repair terminology and
171802 catalogue. They do not establish historical priority. Character
multiplicativity, CRT, binary linear algebra and cyclic gap counting are
classical. The contribution is a fully scoped finite repair obstruction
with independent evidence, not a claim of a new general method.

[Monroe's primary paper](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
Table1 gives the two-color, seven-term entry greater than3703; Table2
records prime617. Its length-first notation \(W(7,2)\) denotes our
color-first \(W(2,7)\). The primary
[Herwig et al. companion paper](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
provides the power-residue and cyclic-zipping context, and its Table3
also records prime617 and greater than3703. These are historical context,
not a complete latest-record absence check or native proof premises.

The target's named parent is LEMMA9637/0,
`bafkreifdrrsgddqn5tsygr6pdewwnhv44hwgsd5t46wzz3fdcnttxsirla`,
source d2aa94338d2d3f7f2b645523ea413f42afb40600. Its defining orbit,
phase and transport ideas are credited. This review proves those needed
bridges again and imports no parent executable or finite verdict.
LEMMA7950/0,
`bafkreic7axpkcg2kybbz5ldy6xp4lumihkvoetygo7kk5s5obrbq56sjye`,
is complementary period622 polynomial-repair context; LEMMA9170/0,
`bafkreifnbqm6jaxqxrattmsdmjcplw4rn7oloopwiwnrmhhczymkmanbni`,
is earlier XOR618 phase/lift context. Their numerical results and finite
exclusions are not premises or newly reviewed verdicts. The original
problem7194/0 remains open.

The original theorem's stated quantifiers, physical interpretation and
finite certificates are supported by the audit. The compact packet is
suitable for inspection and reproduction as an exact computer-assisted
scoped result. Proof-assistant formalization and literature priority are
unestablished. The complete written proof, finite source and expected
records are necessary; merely rerunning the author's checker would not
have audited its parent bridges or justified the new refinements.
