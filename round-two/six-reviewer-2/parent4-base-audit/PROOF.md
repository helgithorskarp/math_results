# Two unavoidable BASE holes and a productive-TAIL capacity cut

Actual author **six-reviewer-2**, role **independent mathematical reviewer**.
This is an exact computer-assisted refinement of LEMMA9709, with ordinary,
unformalized reduction, induction, and Chinese-remainder arguments.

Fix
\[
P=(8:0,9:0,10:1,14:1,12:10)
\]
and the 36 unused original divisors \(B\) of 2520 that are at least eight.
Allow at most one arbitrary phase of each original label, including 21.
No A4, color, row, original-16, or hole-count premise is imposed.

**Refinement.** Every such P/BASE inventory leaves **at least two distinct
holes modulo 2520 outside parent four**. Its lift modulo 10080 therefore
has at least eight uncovered physical residues outside that parent before
TAIL. In any full covering by distinct divisors of 10080 extending P, at
least two original TAIL classes productively cover those outside-parent
holes. More precisely, for each actual BASE hole \(x\), if \(r_{16}(x)\)
and \(r_{32}(x)\) count the selected classes with respective original labels
\(16d\) and \(32d\), \(d\mid315\), which meet its four lifts, then
\[
2r_{16}(x)+r_{32}(x)\ge4.
\]
Each such class necessarily has phase different from four modulo eight.
These are necessary conditions, not a covering construction, a sharp hole
minimum, a full P exclusion, a global bound, or an unrestricted minimum-eight
theorem. The given modulus eight retains the exactly-eight convention.

## Exact complete reduction

Appending arbitrary phases of absent labels preserves distinctness and can
only remove holes. It suffices to prove the lower hole bound for completed
36-label inventories. No TAIL resource is spent in this step.

Define the physical required set
\[
R=\{x\in\mathbb Z/2520:x\text{ misses P},\ x\not\equiv4\pmod8\}.
\]
The exact original-set construction gives \(|R|=1118\). The independent
coordinate system uses all 2520 combinations on the axes 8, 9, 5, 7 and the
CRT identity
\[
x\equiv\sum_{m\in\{8,9,5,7\}}r_m(2520/m)u_m\pmod{2520},
\qquad (2520/m)u_m\equiv1\pmod m.
\]
Here each inverse \(u_m\) is taken modulo its corresponding \(m\). This is a
bijection of physical residues; no residue or original phase is quotiented.
Every original label partitions R into all its actual phases. A separate
literal arithmetic-progression check compares every point of every class.

For the actual phases of a selected original group F let U be their union
inside R. Every extension covers at most
\[
K(U)=|U|+\sum_{n\in B\setminus F}
 \max_{0\le a<n}|(R\setminus U)\cap(a\bmod n)|.
\]
The inequality is the union bound on additional coverage. Each original
label contributes once; independently maximizing phases need not coexist.
For an inventory to cover at least 1117 points, its actual prefix must have
\(K\ge1117\). Retaining **that threshold at every stage**, rather than
retaining 1118, is essential to the stronger claim.

Enumerate all 270 raw original 15/18 pairs, with no affine normalization,
then all phases of original 24, 36, and 20 in succession. Every retained
prefix is extended to every phase of the next original label.

| Ordered original group | Examined | K range | Retained at K >= 1117 |
| --- | ---: | ---: | ---: |
| 15,18 | 270 | 1046..1177 | 153 |
| 15,18,24 | 3672 | 1023..1147 | 360 |
| 15,18,24,36 | 12960 | 1040..1132 | 240 |
| 15,18,24,36,20 | 4800 | 1022..1116 | 0 |

All 21702 branch records, 693876 remaining original-resource marginal
entries, and 199406964 actual phase intersections are evaluated exactly.
At each discarded branch \(K\le1116\), so it cannot be the prefix of an
inventory covering 1117 points. By induction a hypothetical inventory
covering that many points would reach the final frontier, which is empty.
Hence every completed inventory covers at most 1116 of R's 1118 points.
An incomplete inventory has at least the holes of any completion, proving
the asserted two-hole minimum for the stated at-most-one domain.

At stage two, keeping K=1117 adds 24 raw prefixes beyond the original
1118-threshold screen. Their 864 actual phase-36 children are included.
None survives stage three. This closes the exact boundary which the
author appropriately left open in the original one-hole statement.
The terminal maximum 1116 has first witness phases (2,3,2,30,3), with
gain 448 and remaining marginal sum 668. This is a bound witness, not an
inventory attaining exactly two holes. No sharpness is asserted.

## Four physical lifts and the productive TAIL cut

The original divisors of 10080 at least eight split into P's five labels,
the 36 labels B, and
\[
T=\{16d,32d:d\mid315\},\qquad |T|=24.
\]
For a hole x modulo 2520, the four points \(x+2520j\), \(j=0,1,2,3\),
are distinct modulo 10080 and miss every P and BASE class. They have the
same residue modulo eight. Distinct holes have disjoint four-lift fibres,
giving the eight-hole statement.

For \(n=16d\), \(\gcd(n,2520)=8d\); the progression in j has period
two modulo n. A single n-class therefore meets either zero or exactly two
lifts. For \(n=32d\) the corresponding period is four, so it meets zero
or exactly one lift. All 24 labels and all 2520 four-lift fibres are checked
literally as a calibration of this algebra.

Covering the four lifts requires the displayed inequality by the ordinary
union bound. Since each original class supplies at most two of them, at
least two distinct productive TAIL classes are necessary, even when BASE
or TAIL labels are optional. Parent-four TAIL phases meet none of these
fibres. Two abstract classes, 16:2 and 48:26, cover the fibre
(2,2522,5042,7562), calibrating that the incidence cut can permit two
different labels. This is not a realizable BASE-hole witness or a full cover.
The per-hole cut does not assert that capacities from different holes add
without shared TAIL incidence.

## Audit and trust

The independent proof does not import the author's code, certificate,
canonical frontier, prior numerical obstructions, or affine normalization.
The defining written proof and disclosed counts were visible. Before late
native corroboration, the reviewer seals independent source, this proof,
and the whole [EXPECTED.json](EXPECTED.json). Shared signing identity does
not establish distinct authorship or blind review.

The separate affine control solves the five literal equations, checks all
288 maps and 82944 products, and reconstructs every one of the 60 orbits
of all 270 phase pairs. It confirms the target's simultaneous normalization
but is not a numerical proof premise of the stronger raw enumeration.
For supplementary comparison only, the independent enumeration marks
the original threshold-1118 canonical rows and records all four complete
row hashes and frontiers, with every marginal in original-label order.

Python integers, bit operations and exact congruences are used throughout.
There is no solver or floating arithmetic. All records fit 38 unsigned
little-endian 16-bit fields: the largest phase is below 2520, and total
K is below 65536. Digests identify complete evaluated records; they do not
replace successful enumeration or the written finite-reduction proof.
`reproduce.py` reconstructs the entire result in serial guarded children;
failure, timeout, or missing phase output proves no exclusion. Ordinary
completeness, union-bound, and CRT bridges remain unformalized.

The completion and partial-union filtering context is classical and is
credited to [Zhang and Zhang, Sections 2 and 6](https://arxiv.org/html/2607.19029)
and the target's campaign precursors. That paper concerns minimum seven.
No historical priority for these methods, or for the specific refinement,
is claimed. The global minimum-exactly-eight problem remains open in this work.
