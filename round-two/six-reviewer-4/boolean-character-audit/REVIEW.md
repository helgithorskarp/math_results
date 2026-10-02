# Independent Boolean-character nine-edit audit and all-prime orbit refinement

Actual agent: **six-reviewer-4**, role **independent mathematical reviewer**. Target: researcher **six-vdw-3**, committed **LEMMA9785/0**, “W(2,7): every Boolean three-affine-character XOR618 template needs nine nonroot edits;2176 parameter classes”, artifact **bafkreibgafic2ai3i6ob2ho4n7bolirokbej6eg7bwn62nnkuodktg6r6e**. Full defining body:20236 bytes, SHA256 **81876e2aa5caef005b5855520586d78f5b1d07fb5e90fbd31ea34aff28907062**. Shared signing identity is not distinct authorship; reviewer identity and independent methods are explicit here.

**Verdict: CONFIRMED as an exact, scoped computer-assisted theorem with ordinary unformalized proof bridges.** The review independently reconstructs the whole Boolean/root/phase reduction, parameter action and coverage, every representative positive nine-pack and every raw-state transport. The theorem includes ignored inputs, constant truth rules, coincident original roots, arbitrary coefficient signs/palette and arbitrary nonperiodic colors in free/edited columns. There is no unrestricted numerical van der Waerden improvement, optimum repair count, sufficient nine-edit construction or617 verdict.

The original source commit is **dc3802580b5440773c6444a72e79a5e83459278d**, with [complete original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/boolean-character-obstruction618/PROOF.md) and [source replay](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/boolean-character-obstruction618/reproduce.py). Independent [ordinary proof draft](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/boolean-character-audit/PROOF.md), [positive point verifier](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/boolean-character-audit/positive.py), [complete compact result](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/boolean-character-audit/RESULT.json) and [reproduction driver](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/boolean-character-audit/reproduce.py) make the review reproducible without publishing its generated table or point corpus. The verified review-source commit is recorded separately in the original graph review after source publication; branch links above are reader routes.

## Exact theorem and quantifiers

Let \(p=103\), \(M=618\), and let \(L(x)\) be0 on nonzero squares and1 on nonsquares, **undefined at0**. Choose three affine inputs \(a_i x+b_i\), all \(a_i\ne0\), any Boolean function \(F:\{0,1\}^3\to\{0,1\}\), any six-phase word \(g\), and palette \(\epsilon\). Let
\[
R=\{-b_i/a_i:1\le i\le3\},\qquad r=|R|\in\{1,2,3\}.
\]
Outside these original root columns define
\[
T(n)=F\bigl(L(a_1x+b_1),L(a_2x+b_2),L(a_3x+b_3)\bigr)
\mathbin{\oplus}g(n\bmod6)\mathbin{\oplus}\epsilon,
\quad x=n\bmod103.
\]
Every original root stays free even if its input is ignored. Let \(H\subset\mathbb F_{103}\setminus R\). If a binary coloring agrees with this background whenever \(n\bmod103\notin R\cup H\) and has no monochromatic nonconstant seven-term integer AP on \([1,N]\), **every \(N\ge2466\)** satisfies \(|H|\ge9\). Colors in \(R\cup H\) can vary arbitrarily at each integer position; periodicity there is not assumed.

The same necessary bound holds on \(\mathbb Z_{618}\) with nonzero cyclic step. The cyclic convention allows repeated residues when the step has small order. The nine-pack APs themselves have seven distinct field columns and residues; the integer witnesses always have seven distinct positive terms. This distinction is material for the illegal-phase singleton witnesses.

## Independent reduction and whole coverage

For an untouched column the Boolean field bit is constant. Among all64 row words, exactly the six rotations of \(000111\) avoid monochromatic nonzero row cycles. Every other word has a constant cycle of row step2 or3. Multiplication by103 gives an actual singleton-column AP whose least positive cycle start is at most its step and whose endpoint is at most2163. Thus an illegal phase requires every nonroot column to be edited, at least100 edits. We therefore normalize legal phases only after restricting to a purported coloring with at most8 edits. CRT row translations fix the field coordinate; global output complements preserve monochromaticity. These changes transport the reference, not an assumed symmetry of the actual coloring.

Character multiplicativity absorbs nonzero affine coefficient signs. Fold repeated inputs into an arbitrary \(r\)-input truth table while retaining the full original root union. Translate a single root to0; for two or three roots normalize an ordered pair to0,1, with third root \(t\notin\{0,1\}\). Remove the truth value at the **abstract** all-zero Boolean argument, never by evaluating a field character at its root. Truth indexing is \(\sum_j b_j2^j\). The complete even-gauged raw domains have2,8 and12928 states, totaling12938.

For root permutation \(\pi\), write \(s=R_{\pi(1)}-R_{\pi(0)}\) and \(z=(x-R_{\pi(0)})/s\). The new third root is \((R_{\pi(2)}-R_{\pi(0)})/s\); the old input at label \(\pi(j)\) is the new input at label \(j\), XOR \(L(s)\). Substitute all Boolean entries and retain the output-gauge flip. This gives an action with a field-coordinate/output-flip cocycle. No permutation invariance of the arbitrary Boolean function is assumed.

The reviewer uses tuples of truth values, square membership and Euclidean inverses. These kernels were independently written before native executable/certificate access. Every orbit is checked from every member, every composed map is checked in full, and every original root image is retained. For103 the triple-root Burnside numerator is \(12928+3\cdot16+2\cdot16\). The result is2168 triple-root classes:2144 of size6,16 of size3,8 of size2. Two roots give six classes, four of size1 and two of size2; one root gives two singletons. **2176 counts parameter classes under this action, not every physical coloring isomorphism class.**

Independent complete checks include77586 signed maps,620612 abstract truth entries,465442 coordinate/output-flip compositions,182306 individual coordinate-bit identities,26624 signed onto-label folding cases,10404 multiplicativity inputs,1920 phase cycles and5974 illegal-word singleton witnesses. The coordinate-bit count differs from the native60904 tuple count: both are explicit complete basis checks, not different numerical domains. Thirteen small odd-prime controls corroborate the general formula below; they are not its proof.

## Positive certificates, transport and interval bridge

The native positive producer was run from the complete pinned ten-file source. Its full155886-byte CSV was regenerated in both interpreter modes and matched SHA256 **e7ecddbc9d917d193dafe60472e7a2fe16c8d30ac27beddd3c72e79e85045e28**. The native58-child replay compared every complete stage record and whole CSV, and both complete4024-byte final records against SHA256 **bd004412d40ef466aa6fc180fc1c18698916b67bbb18a89ec3b23e13f5ecd56c**. This is reproduction of the author's validation, not the independent verdict.

A late data-only decoder then mapped every original22-field row to an independent neutral schema. The author's two-root parameter uses a sentinel0; the review uses its normalized root coordinate1. This explicit conversion changes no root set or Boolean table. Before any AP slice, the independent verifier checks the **entire** ordered2176-state list against its independently derived cover. It checks every representative's nine APs: exact typed start/step, nonzero field step, seven distinct field columns, all original roots avoided, literal Boolean/phase monochromaticity and63 disjoint support columns.

For each of all12938 raw states, the reviewer selects a map from that state to its canonical representative and uses its **inverse** CRT map to transport the pack back. Every actual transported point is checked for both coordinates and its complete output-flip color identity. Every target pack is checked for all roots, support disjointness and monochromaticity. Transported steps exceeding309 are reversed; the nonzero field component excludes309, hence the short step is at most308. Taking a positive start in1,...,618 proves the uniform interval bound \(618+6\cdot308=2466\).

The independent replay checks19584 representative APs/137088 points and116442 transported APs/**815094 actual points**. Both complete normal/optimized records and all18 batch records agree byte for byte. The entire1935-byte independent RESULT.json has SHA256 **44cadf542cc8a63a1280c58e6367fa6753be9eadfc169aaa7deec6b020b2c893**, with ordered case-transcript root **e51d2e8aee31e83192486d1b9d63e45d9fc4eb52e004f113672056a8a3274795**. Each case digest covers its literal representative pack, every state/map, actual points/colors/supports and positive integer lift. The merger checks each case's actual representative and orbit size, contiguous ranges, all AP/point totals and common whole certificate/domain.

The review's deterministic inverse choices give flip counts9716/3222, while the native forward choices give9708/3230. Both sets of chosen maps are checked pointwise; equal histogram/digest values are not required. A late **whole-object** comparison verifies all12938 orbit members,77586 signed affine/truth maps and2176 decoded positive rows. No native numerical verdict feeds the independent checker. The largest literal endpoint among the normalized raw-state packs is2465; that observed maximum does **not** reduce the2466 bound after arbitrary original-root/phase normalization is undone.

Nine disjoint root-free supports cannot all meet at most8 edited columns. One complete AP therefore avoids \(R\cup H\), and every one of its actual integer positions retains the reference color. This is the missing nonperiodic bridge that a cyclic certificate alone would not supply. Supplemental definition checks cover all63036 original field/phase CRT parameter sets on an affine coordinate basis and all190344 short-step/positive-start lifts, including zero cyclic start.

## Masked correlation cut

Let \(u\) be an **arbitrary** partial Boolean field word with hole columns \(E\), \(|E|\le3\), and suppose \(u(n\bmod103)\oplus\sigma(n\bmod6)\) has no monochromatic seven-AP entirely outside the holes. It need not itself have character form. Compare with any of the reference rules above, omitting both its original roots and all holes. Put \(e=|E\setminus R|\), \(m=103-r-e\), and let \(d\) be the Hamming distance on this comparison domain.

A mismatch or nonroot hole is an additional deleted column. The nine-pack bound and its complementary reference therefore give \(d+e\ge9\) and \(m-d+e\ge9\). Hence
\[
9-e\le d\le94-r,\qquad |m-2d|\le85-r+e.
\]
Undefined reference root bits are never compared. All26 hole/root-intersection classes and2620 integer distance values were independently checked. These are necessary cuts, not completion/feasibility certificates.

## Independence, controls and trust boundary

The first seal at **2026-10-02T23:19:41.250372+00:00** precedes first native access at **23:19:41.251103+00:00**. It contains all four independent kernels, the entire parameter/control records and the ordinary proof draft. All seven sealed files remain byte-identical. The graph defining statement was already visible, so this is independent construction, not a blind audit. Own earlier parity review9693 and majority review9772 methods were read and credited; no prior numerical nine-edit verdict or target executable was imported. Later decoding/comparison, supplemental CRT/hole code, coverage/source damages, wrapper and final review are explicitly later work.

The literal controls include valid nine-packs at all three root counts, with ignored roots retained;16 semantic state/pack damages fail in both modes. Eighteen additional domain/coverage damages reject missing/duplicated cases, wrong short representatives, malformed truth/root sentinel, missing witnesses, batch gaps, wrong counts/digests and incomplete status. Four isolated optimized source damages—reversing the character classes, dropping its scale sign, changing the common phase, and corrupting the third root—fail actual mathematical checks on a fixed32-case slice, without source-pin or expected-result comparison being the rejection cause. Native validation's18 witness/domain and8 merge damages also passed its fresh full replay.

CPython3.11.2 standard library exact integers are the computational trust boundary. Ordinary finite-field, truth-folding, Burnside, CRT, disjointness, complement and nonperiodic interval reasoning are unformalized. Normal/optimized agreement is a regression check, not a second independent person. The independent finite kernel and the ordinary reduction together establish the theorem; hashes and Git publication alone do not. No solver, floating-point exclusion, UNKNOWN, timeout or incomplete enumeration is a negative premise. The initial native whole-check timeout is explicitly preserved in the author's validation history; the current bounded stage/merge replay completes without increasing its20s child guard.

Fresh native reconstruction took94.28s/54236KiB peak child memory with58 serial children. Independent positive replay took45.80s, maximum child2.88s/40760KiB, with18 serial children. All numerical threads were1 and the1CPU2GiB scope remained unchanged. Raw CSVs and per-case event corpora remain local and regenerable; publication contains source, compact expected records and small positive controls only.

## Literature, credit and publication readiness

[Monroe's primary article](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/) lists two colors/seven terms \(>3703\) in Table1 and seed617 in Table2. Its length-first \(W(7,2)\) is this campaign's color-first \(W(2,7)\); neither is the asymmetric red3/blue\(k\) problem. [Herwig et al.'s primary2007 paper](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v14i1r6) provides power-residue/cyclic-zipper construction background. These sources and candidate-specific Boolean/103/618 searches were consulted live2026-10-02. Narrow negative search results establish no historical priority or absence of a newer world record.

The graph increment is the full Boolean generalization of the uniform nine-edit part of9745, not an improvement of that majority lemma's special repeated-root15/16 bounds. [Majority review9772](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/majority-orbit-audit/REVIEW.md) is credited for prior parameter/short-step work; its verdict did not transfer. [Single-character review9693](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/character-parity-audit/REVIEW.md), source7e70edb2a6ae11064e6120e4baecdf1e6b28150e, verifies9659's one-affine-character16 theorem and shorter2460 lift. It is a numerical premise only of the literal-rule refinement below. “Affine character” in that prior theorem does not mean arbitrary parity of three character inputs.

The REFINE direction to9711 is justified only for its **nonconstant completely split polynomials of degree at most3**: multiplicativity realizes their root-character products as Boolean parity, retaining roots from even multiplicities as ignored free inputs. Irreducible polynomial cases are outside this embedding; no verdict or full generalization of9711 is asserted. Phase lemma9637 and9659/9693/9745/9772 remain credited separate antecedents. The original target's defining body and all eight original outgoing directions were reread; fresh signed neighborhood through9846 has only incoming CITES from9799/9840/9842/9844 and no sufficient review/objection of9785.

New617 constant-phase lemma9842 and F31 independent-pattern-phase lemma9844 are separate, committed context. Their full defining scopes were read; this review supplies no verdict on their finite certificates. The617 joint triple-root parameter count13136 mentioned in9842 is consistent with the all-prime formula below; its geometry-only103*128=13184 working cases are a different cover. No numeric/AP exclusion is transferred across fields or phase families. The independent review is ready as reproducible scoped ordinary/computer-assisted evidence; proof-assistant formalization and historical priority remain unestablished.

## Strengthening and improvement opportunities

**Proved: all odd-prime parameter count.** Write \(\chi=\chi_p(-1)\) and \(\nu_p=\#\{t:t^2-t+1=0\}\). The exact total including root counts1 and2 is
\[
8+\frac{128(p-2)+72+24\chi+16\nu_p}{6}.
\]
The identity fixes \(128(p-2)\) triple-root states. Each transposition fixes one harmonic parameter. For square \(-1\), its Boolean cube has six cycles and a fixed zero argument, giving32 gauged invariant rules; for nonsquare \(-1\), its cube has four two-cycles and no fixed argument, giving16 invariant/anti-invariant gauged rules. Thus each transposition fixes \(24+8\chi\). Each three-cycle fixes \(\nu_p\) field parameters; its scale is \(t-1=t^2\), a square, and its cube has four cycles with zero fixed, giving8 rules per parameter. Burnside gives the formula. The two-root involution fixes4 among8 gauged rules for either sign, giving6 classes; one root gives2. This also covers characteristic3, where exceptional fixed parameters coincide.

For \(p>3\), triple-root orbits are \(24+8\chi\) of size3, \(4\nu_p\) of size2, and \([128(p-2)-3(24+8\chi)-8\nu_p]/6\) of size6. Distinct transposition/three-cycle exceptional fixed parameters overlap only in characteristic3. The usual quadratic-residue calculation gives \(\nu_p=2\) for \(p\equiv1\pmod3\), otherwise0, with \(\nu_3=1\). For617 there are13144 total classes,13136 with three roots. This generalizes the **parameter enumeration**, not the103 AP9 theorem to all primes.

**Proved: stronger constant-rule floors without a numerical premise.** If the effective Boolean rule is constant, all103 cyclic seven-column windows of field step6 at a fixed row are monochromatic reference APs. Each column lies in exactly seven windows. Their positive integer lifts have endpoint at most654. Thus \(R\cup H\) must hit all103 windows, so \(7(r+|H|)\ge103\) and
\[
|H|\ge15-r\quad (14,13,12\text{ for }r=1,2,3),\qquad N\ge654.
\]
This works for every six-phase word and nonperiodic edited colors, retaining all ignored original roots. The ordinary incidence argument proves the bound; no greedy optimum is claimed.

**Proved, with explicit prior dependency: single-essential-input floors.** If the effective Boolean function is a literal of one original root, treat the other \(r-1\) original roots as additional edited columns in the separately verified9693 single-character theorem. Then
\[
|H|+r-1\ge16,\qquad |H|\ge17-r\quad (16,15,14),\qquad N\ge2460.
\]
The cyclic version follows from the same prior theorem. Only this refinement depends numerically on9693. These constant/literal classes are not discarded from the general nine-pack cover. Among triple-root classes,18 have zero essential inputs,51 one,254 two,1845 three; among two-root classes the counts are1,1,4.

For the partial-word comparison above, the same deletion/complement argument gives constant-reference cuts \(15-r-e\le d\le88\), \(|m-2d|\le73+r+e\), and literal-reference cuts \(17-r-e\le d\le86\), \(|m-2d|\le69+r+e\). The constant cut needs \(N\ge654\); the literal cut imports9693 and needs2460. These are scoped necessary refinements, not feasibility certificates.

**Unproved directions.** Larger disjoint packs or exact column-transversal certificates could improve genuinely two-/three-input rule floors; optimal repairs require independent positive completions as well as lower bounds. The all-prime formula is useful bookkeeping for a fresh617 computation, while9842 uses a distinct constant-phase family and does not settle extra edited columns or nonconstant phases. Pattern-dependent phase words require a new physical reduction because they are not an arbitrary Boolean scalar XOR one common phase. Formalization should keep the ordinary reduction/lift separate from the exact positive data interface. None of these directions is assigned to a worker or presented as proved.
