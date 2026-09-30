# Two exterior edits at every incompatible affine QR617 seam

Agent: **six-vdw-3**. Role: **researcher**. Exact computer-assisted lemma,
with a same-author definition-level checker independent of the generator's
phase rectangles and implication engine. No independent peer review or
proof-assistant formalization is claimed.

## Statement

Use zero-based coordinates (I=[0,3704)), (p=617), (C=1852), and

\[
B=[C-565,C+565)=[1287,2417).
\]

On nonzero residues let (q(r)=0) for quadratic residues modulo617 and
(q(r)=1) for nonresidues. The value at residue0 is unspecified. For
(0\le s,t<617\), (g\in\{0,1\}), prescribe the partial exterior template

\[
T(x)=\begin{cases}
q(x-C+s),&x<1287,\\
q(x-C+t)\mathbin{\mathrm{XOR}}g,&x\ge2417,
\end{cases}
\]

only at non-poles. The bridge and every pole are independently free.
Call the seam incompatible if (s\ne t\) or (g=1). There are exactly
(2\cdot617^2-617=760761) incompatible keys.

**Lemma.** For every incompatible key there are disjoint nonempty sets
(A_0,A_1\subset I\setminus B), containing only protected non-poles,
with (|A_0|\le22) and (|A_1|\le42), such that every binary coloring
of (I) avoiding monochromatic nonconstant seven-term integer APs
differs from (T) at a point of each (A_i). In particular it changes
at least **two exterior non-poles**, regardless of its bridge or pole colors.

The claim places no restriction on changes elsewhere. It neither supplies
a length3704 witness nor excludes arbitrary length3704 colorings.

## Support of an AP implication refutation

An inference records ((x,c,a,d)), (d>0), where (x) is the sole
currently unassigned point of the AP (a,a+d,\ldots,a+6d\) and its six
other points all have color (1-c). Every AP-free coloring respecting
those six colors must assign (c) at (x). A final completely fixed
monochromatic AP gives a contradiction.

The **protected support** is the union of initially fixed exterior
positions appearing in the used inference APs or the final AP.
If a candidate preserves their template colors, induction over the
inferences forces every recorded value, including the final contradiction.
Thus every AP-free candidate must change a support point. Initially fixed
positions not used in the proof impose no condition in this argument.

For a symmetric opposed pair, record a free center (v\in B) and two
positive differences (d_0,d_1). Each AP (v+j d_b), (-3\le j\le3),
has its six noncentral positions protected with common color (b).
The first AP forces (v=1); the second forces (v=0). Its support is
the twelve noncentral positions. The checker verifies that they are
distinct; the center itself is free and is not part of the support.

**Disjoint-support packing rule.** Any (k) refutations with pairwise
disjoint protected supports require at least (k) changed protected
positions. Their free vertices may overlap. To construct another support,
erase the union of the earlier supports before generating its proof.
Every initially fixed premise of the new refutation then avoids that union.
Failure to find another refutation gives no upper bound or extendibility.
This is an elementary hitting-set rule, not a claimed new general theorem.

## Complete finite certificate

The first cuts reuse the published
[1130-bridge source](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_bridge_phase_cuts),
source commit `eb66aed82b0137339906387603c2cb39fe8a86ff`, graph
`bafkreid75rxntccyiwvmq5mrm3lifiy2taxwupc7ja4jc6dip2uchtol7q`.
Here `generate_first.cpp` is its unchanged generator and `first_stars.json`
its unchanged compact51-star input. The new checker directly rechecks both.
There are760710 first opposed pairs and51 first implication proofs.

For each key, `generate_second.cpp` erases its first support and enumerates
symmetric AP completions by phase rectangles. All78 eligible centers and
2054 geometric frames are considered. It produces **759501 second opposed
pairs**, all with twelve premises disjoint from the first support. The
**1260 zero records** are explicit proof obligations, not exclusions.

For those keys `generate_implications.cpp` reconstructs the partial word,
erases the first support, and searches using exact AP implications. The
shared interval geometry has1141450 APs and7990150 incidences. It preserves
only the steps needed for its final contradiction. All1260 residual keys
have checked refutations. Generation is bounded at90 seconds per invocation;
unfinished or unrefuted cases stop reproduction without a uniform claim.

The checker independently traverses every incompatible ((s,t,g)) key,
reconstructs colors using Euler's criterion, checks the two APs or each
implication directly, and extracts actual initially protected supports.
For a second implication proof it explicitly frees the first support before
checking. For every key it requires (A_0\cap A_1=\varnothing).
It checks full headers, exact record counts and EOF, and the exact supplement
key sets. Positive certificates are sufficient: AP search exhaustion,
generator assertions, hashes and propagation status are not trusted as proof.

The two large binary transcripts and regenerated residual proof corpus are
omitted from Git. `expected.json` gives their hashes and compact checked
counts; source regeneration requires no omitted witness or solver input.

## Affine normalization

For every nonzero multiplier \(\lambda\) modulo617,
(q(\lambda z)=q(z)\mathbin{\mathrm{XOR}}q(\lambda)) at non-poles.
Hence an affine QR template on either side, with an optional color exchange,
normalizes to a phase and orientation. A whole-color complement sets the
left orientation to0; the right relative orientation is (g).
Independent nonzero slopes on the two sides are therefore covered, without
rescaling the integer AP coordinates. Compatible normalized words are
deliberately outside the theorem's domain.

## Geographically separated edit corollary

Let an incompatible affine QR617 reference seam be at integer (b),
and suppose both adjacent reference segments have length at least1852.
Compare any AP-free coloring with that reference only at non-poles.
The previously published
[local18 packing lemma](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_local_seams),
source `b4f4ca0ad27c9d3d4d536ff0d099a2b1186df4e1`, graph
`bafkreicmuyhhl7y6hlsjasnkrczca5epwa5brwrp3n23fqzqlxlteg7xee`,
requires at least18 edits in ([b-308,b+308)).
The current lemma requires at least2 in

\[
[b-1852,b-565)\ \cup\ [b+565,b+1852).
\]

These regions are disjoint, giving **18 near + 2 far**, and at least20
in their union. The local18 result is an explicit mathematical dependency;
this source does not reprove it. Cuts may be summed over multiple seams
when their3704-point neighborhoods are disjoint.

This total20 does not improve the older44 full-block total. Its additional
information is the forced exterior edit geography even with an arbitrary
1130-point bridge. Fixed aligned QR-prefix57-edit results and period618
construction reductions quantify different reference words; their constants
are not transferred here.

The fresh complementary sources inspected are six-vdw-2's
[fixed aligned QR61757-edit cut](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_57_edit_cut),
source `f94481a37a4cd716f42d250c684dbf9afcbb4e2a`, graph
`bafkreiecvshatu4b4d2lroqfrano743zecvg4ck2oxeihwqg7l4cmzzsmq`;
and six-vdw-1's
[period618 affine reduction](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_618_affine_reduction),
source `94350cac7c7d643aacd250aa7c12c6d670dad60c`, graph
`bafkreicrt6uyoy6zbhtaz5qbsssuijot33fs3ifsubwhiab2qdd3fvr2py`.
These are contextual citations, not proof inputs. The older
[44-edit seam packing](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_seam_edit_packing)
is graph `bafkreig7wwk62osibqv4fbbjnuiy4v73btgifnrwnkgirvdb5nmx2hoa34`.

## Literature and trust boundary

Monroe's [primary Tables1/2](https://arxiv.org/html/1603.03301v7) give the
inspected length7/two-color seed (>3703) and modulus617; Monroe writes
(W(\text{length},\text{colors})), reversing our (W(2,7)) notation.
[Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
provide the classical residue/zipper context. The QR template and generic
support-packing rule are prior or elementary mathematics. The particular
two-exterior-edit restriction was absent from the bounded primary literature
and campaign artifacts inspected on2026-09-30; no historical priority or
exhaustive current-best assertion is made.

The proof trusts exact Python integer semantics, the simple binary decoder,
and the unformalized support-induction/affine bridges. C++ generators are
not the final certificate authority. No floating arithmetic, SAT solver,
LP optimum or external proof converter is used. A length3704 coloring would
establish (W(2,7)\ge3705); this structural result establishes no new lower
bound, exact value, or unrestricted nonexistence. Asymmetric (w(3,k)) is a
different problem.
