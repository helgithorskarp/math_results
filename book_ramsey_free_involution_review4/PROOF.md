# Three forbidden quotient cores and the seven-pair refinement

Actual author: **six-reviewer-4**, role **independent mathematical reviewer**.
This proof extends the local obstructions in the independently selected
[h7914 target](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_free_involution/PROOF.md).
Shared signing identity does not establish separate authorship.

## 1. Statements and conventions

A valid coloring means a coloring of the edges of the complete graph on
22 vertices with no ordinary red \(B_4\) and no ordinary blue \(B_7\).
Pages need not be pairwise nonadjacent. Thus red and blue spines have at
most three and six monochromatic common neighbors, respectively.

Fix any color-preserving fixed-point-free involution and label its eleven
orbits \(i0,i1\), \(0\le i\le10\). A cross-orbit block is either uniformly
red, uniformly blue, or one of the two red matchings. Inside-orbit edges
are arbitrary. Labels may be switched independently within orbits.

**Theorem 1 (arbitrary-complement forbidden cores).** Select five orbits,
labelled \(0,\ldots,4\), and let \(H\) be the other six. Suppose every block
between a selected orbit and \(H\) is a matching. None of these three
complete patterns on the selected orbits is possible:

| Core | Uniformly red pairs | Uniformly blue pairs | Remaining pairs |
| --- | --- | --- | --- |
| A | 01,02 | 03,04,12,34 | matching |
| B | 01,23 | 02,04,13,34 | matching |
| X | 01,23 | 02,03,12,14,34 | matching |

All blocks inside \(H\) may be arbitrary: uniform of either color or
matching, with arbitrary matching signs and arbitrary inside-orbit colors.
This broadens the target's A/B obstructions, whose complements consisted
entirely of matching blocks, and adds X. The theorem is an ordinary
analytic proof with no finite enumeration premise.

**Theorem 2 (seven uniform pairs).** In every valid coloring with the
fixed involution, if exactly seven cross-orbit blocks are uniform, at
least three of them are uniformly red.

Theorem 2 combines the target's independently audited at-least-two-red
lemma, a complete finite quotient reduction below, and Theorem 1. The
finite reduction is computer assisted and has two independent complete
implementations. It never enumerates matching signings or all colorings
of the complete graph on 22 vertices. This theorem does not assert eight
uniform blocks or three red uniform blocks without the seven-block hypothesis.

## 2. Page identities and the common diagonal correction

Put \(\epsilon_i=1\) for a red inside-orbit edge and zero otherwise. Define
symmetric, zero-diagonal matrices
\[
 W_{ij}=\begin{cases}1&\text{uniformly red},\\-1&\text{uniformly blue},\\
 0&\text{matching},\end{cases}
 \qquad
 S_{ij}=\begin{cases}1&\text{parallel red matching},\\
 -1&\text{crossed red matching},\\0&\text{uniform}.\end{cases}
\]
Let \(u=W\mathbf1\). For a matching pair \(ij\), the red and blue page
counts are
\[
 [9+u_i+u_j+(W^2)_{ij}+S_{ij}(S^2)_{ij}]/2,\quad
 [9-u_i-u_j+(W^2)_{ij}-S_{ij}(S^2)_{ij}]/2.
\]
Each third orbit contributes these expressions with 9 replaced by 1
and the appropriate two links. Summing over nine third orbits gives
the formulas. Inside companions are never monochromatic pages here.
In particular
\[
 -3-u_i-u_j+(W^2)_{ij}\le S_{ij}(S^2)_{ij}
 \le-3-u_i-u_j-(W^2)_{ij}.                       \tag{1}
\]
Every matching pair has \((W^2)_{ij}\le0\); if it is zero,
\((S^2)_{ij}=-(3+u_i+u_j)S_{ij}\).

For a uniform pair \(ij\), sum the pages at spines \(i0j0,i0j1\).
The sums are
\[
 \sum_{k\ne i,j}(1+W_{ik})(1+W_{jk})+2(\epsilon_i+\epsilon_j)
\]
in red and
\[
 \sum_{k\ne i,j}(1-W_{ik})(1-W_{jk})+2(2-\epsilon_i-\epsilon_j)
\]
in blue. Their caps are six and twelve. The difference of the two
spine counts is \((S^2)_{ij}\). Thus a saturated sum forces this entry
to vanish. These identities follow from literal common-page sets and
are also checked on all 512 lifts of three orbits in the independent audit.

Let \(r_i=(S_{ih})_{h\in H}\), \(C=S_{H,H}\), and
\[
 D=\operatorname{diag}(u_h:h\in H),\qquad T=C+D.
\]
The arbitrary links inside \(H\) change \(C,D\). Crucially \(T\) is
always symmetric. Since every selected-to-\(H\) block is a matching,
\((W^2)_{ih}=0\). Expanding \(S^2\) in (1) gives the exact row actions
\[
 r_iT=-(3+u_i)r_i-\sum_{j=0}^4 S_{ij}r_j.        \tag{2}
\]
The common diagonal absorbs every complement load \(u_h\); it cannot be
dropped when uniform blocks occur inside \(H\). The selected \(u_i\)
depend only on the displayed core. Thus (2) holds for all four block
types throughout \(H\), not only for its matching-only case.

For two balanced six-sign vectors the inner product is 2 modulo 4.
Writing the sets of their three positive coordinates as \(P,Q\), it is
\(4|P\cap Q|-6\). In particular balanced six-sign vectors cannot be
orthogonal.

## 3. Core A: a contradiction to linearity

Its red uniform sums have outside term six, so
\(\epsilon_0=\epsilon_1=\epsilon_2=0\). Its blue 03/04 outside sums
are ten, forcing \(\epsilon_3=\epsilon_4=1\). The uniform outside
sums at 12 and 34 are eight and twelve. Every displayed uniform
pair is therefore saturated, hence its \(S^2\) entry is zero.
Here \(u_0=u_1=u_2=0,\ u_3=u_4=-2\).

Switch the labels in \(H\) so \(r_0=a=\mathbf1\). Saturated pairs 01,
02,03,04 make \(r_1,r_2,r_3,r_4\) balanced. Put
\(P=(S_{ij})_{i=1,2;\ j=3,4}\). Saturation at 12 gives
\[
 r_1\cdot r_2=-(PP^{\mathsf T})_{12}.
\]
The left side is 2 modulo 4; the right side is one of \(-2,0,2\).
It cannot be zero, so the two rows of \(P\) are parallel or opposite.
Its rank is one, and switches in the four selected orbits make every
entry of \(P\) positive, preserving balance.

For every mixed pair \(i\in\{1,2\},j\in\{3,4\}\),
\((W^2)_{ij}=-1\), and (1) gives
\(S_{ij}(r_i\cdot r_j)\in\{-2,0\}\). Balanced-six parity excludes zero.
With \(P\) positive, every mixed inner product is \(-2\); saturation
at 12 and 34 supplies the other two inner products, also \(-2\).
Consequently the sum of all four rows has squared norm
\(24-24=0\). Put \(p=r_1+r_2,\ q=r_3+r_4=-p\); then \(\|p\|^2=8\).

Summing (2) separately in the two row groups gives
\[
 pT=-3p-2q=-p,\qquad qT=-q-2p=q.
\]
Since \(q=-p\), linearity instead gives \(qT=-pT=p\).
It follows that \(p=0\), contradicting its squared norm eight.
No condition on \(C\), other than it being a linear map, was used.

## 4. Core B: a four-unit self-adjointness discrepancy

The red outside sums are six, forcing
\(\epsilon_0=\cdots=\epsilon_3=0\). Blue 04 and 34 have outside
sum ten, forcing \(\epsilon_4=1\). Blue 02 and 13 have outside sum
eight. All six uniform pairs are saturated.
Here \(u_0=u_3=-1,\ u_1=u_2=0,\ u_4=-2\).

Switch \(H\) so \(r_4=a=\mathbf1\). Saturation at 04/34 makes
\(r_0,r_3\) balanced, and the other four saturated pairs make both
orthogonal to \(r_1,r_2\). Write
\(p=S_{14}, q=S_{24}, y=S_{12}\). At matching 14 and 24,
\((W^2)_{ij}=0\), so (1) gives
\[
 a\cdot r_1=-p-yq,\qquad a\cdot r_2=-q-yp.       \tag{3}
\]
A six-sign vector orthogonal to a balanced six-sign vector has
coordinate sum 2 modulo 4: its sum is twice its sum on the balanced
vector's three positive coordinates, an odd number.
Thus neither right side of (3) is zero, forcing \(p=yq\).
Switch orbits 1,2 to make \(p=q=y=1\); then both row sums are \(-2\).

At matching 12, \((W^2)_{12}=-2\) and
\((S^2)_{12}=1+r_1\cdot r_2\). Inequality (1) therefore gives
\(r_1\cdot r_2\in[-6,-2]\). Each row has two positive coordinates,
so their possible inner products are \(-2,2,6\).
Hence \(r_1\cdot r_2=-2\).

Equation (2) now gives
\[
 aT=-a-r_1-r_2,\qquad r_1T=-a-3r_1-r_2.
\]
Using \(a\cdot r_1=a\cdot r_2=r_1\cdot r_2=-2\) and both squared
norms six,
\[
 (aT)\cdot r_1=2-6+2=-2,\qquad
 a\cdot(r_1T)=-6+6+2=2.
\]
These are equal for every symmetric \(T\), a contradiction with exact
discrepancy four. This replaces the target's invariant five-space and
last-eigenvalue argument and remains valid for arbitrary complement
blocks through the diagonal correction.

As a separate check, the target's two invariant restrictions have
squared traces 25 and 10. Their sum 35 already exceeds the squared
trace 30 of a six-by-six matching sign matrix. That is another shorter
contradiction in the original matching-only complement, but the
self-adjointness argument above proves the broader statement.

## 5. Core X: balanced vectors cannot be orthogonal

The two red sums have outside term six and force
\(\epsilon_0=\cdots=\epsilon_3=0\). Blue 34 has outside term ten
and forces \(\epsilon_4=1\), with saturated total twelve.
Blue 03 has outside term eight and is also saturated.

Switch \(H\) so \(r_4=a=\mathbf1\). Saturation at blue 34 gives
\(r_3\cdot a=0\). At matching 04, \(u_0=-1,u_4=-2\) and
\((W^2)_{04}=0\), so \((S^2)_{04}=0\). Its only nonzero two-step
contributions are in \(H\), giving \(r_0\cdot a=0\).
Finally saturated blue 03 gives \(r_0\cdot r_3=0\).
Both vectors are balanced six-sign vectors; their inner product
cannot be zero. This proves X, again independently of every block
inside \(H\).

## 6. Complete seven-uniform/two-red quotient reduction

Suppose exactly two of seven uniform blocks are red. Up to arbitrary
orbit relabeling the two red edges are either 01,02 or 01,23.
All eleven orbits, including isolated uniform-quotient vertices, remain
present. The blue edges are exactly a five-subset of the 53 other pairs.

For each red uniform pair \(ij\), the set of third indices with a
blue-uniform link to \(i\) or \(j\) has size at least three: each
other index contributes at least one to the combined red sum, whose
cap is six. Both implementations impose this cut, then
\((W^2)_{ij}\le0\) at every matching pair. They retain every inside
color assignment satisfying the uniform-spine sum caps and the
inside-orbit red/blue spine caps \(2d_R(i)\le3\) when \(\epsilon_i=1\)
and \(2d_B(i)\le6\) when \(\epsilon_i=0\).

These conditions are necessary and do not presume any sign assignment.
The complete result is:

| Red shape | All blue choices | Three-index cut | Matching-square cut | Surviving patterns | Surviving inside assignments |
| --- | ---: | ---: | ---: | ---: | ---: |
| disjoint | 2,869,685 | 47,040 | 2,016 | 448 | 21,952 |
| adjacent | 2,869,685 | 140,854 | 1,428 | 420 | 20,160 |

Every surviving pattern and every inside assignment is exactly a
labelled image of one of:
\[
 X;\qquad B\ \text{with an extra blue uniform pair }56;\qquad
 A\ \text{with an extra blue uniform pair }56.
\]
In the latter two patterns all pairs not specified are matching.
Their pattern/assignment counts are respectively
28/1792, 420/20160 and 420/20160. The X assignments fix
\(\epsilon_0=\cdots=\epsilon_3=0,\epsilon_4=1\), with the other six
free. The A/B-plus-blue assignments have their core-forced colors,
\(\epsilon_5+\epsilon_6\ge1\), and four free remaining colors.

The complete C++ generator visits the increasing five-index tuple
\((0,1,2,3,4)\), repeatedly increases its rightmost index with room,
and resets its suffix to consecutive values. This is the ordinary
lexicographic successor for all five-subsets of 53 indices. Every
tuple appears once; termination occurs precisely at the maximum tuple.
Every arithmetic intermediate is an integer of absolute value at most
36; all counters are below six million and stored in 64-bit unsigned
integers. There is no adaptive truncation, parallel partition, timeout
verdict, external input, overflow-dependent pruning or sign search.

The independent Python implementation uses itertools combinations,
per-orbit set cuts and signed neighborhood intersections rather than
the C++ matrix products. It enumerates inside variables only on the
active uniform quotient, then adds every free passive color.
Every individual pattern and complete inside-assignment list agrees
between the two implementations. A third direct template-image
generator computes all images under red-edge-preserving permutations
and injections of the active outside indices, and compares the full
pattern/assignment dictionaries entry by entry with both censuses.
Counts alone are not the classification certificate.

Each of the three surviving patterns contains a core from Theorem 1
with all six remaining-to-core blocks matching. The additional 56
uniform block in A/B lies entirely in the arbitrary complement allowed
by that theorem. Thus all surviving patterns are impossible.

The independently confirmed h7914 lemma supplies at least two red
uniform blocks in every valid coloring, so exactly seven uniform
blocks now require at least three red ones. This proves Theorem 2.

## 7. Evidence and trust boundary

[audit.py](audit.py) regenerates the two censuses and all template images,
6,144 direct page/degree/difference comparisons on all 512 small lifts,
720 A row tuples, 90 B row pairs, balanced-six parity, the exact
four-unit symmetry discrepancy and squared-trace shortage.
No campaign executable is imported. Four deliberately corrupted
formula/entry certificates reject. Guards remain active under optimized Python.

[EXPECTED.json](EXPECTED.json) is compact comparison evidence; the full
generated 868-pattern/42,112-assignment corpus stays in scratch and is
regenerated, not a required external artifact. Its two canonical entry
SHA256 values are 7c63d807eecdfe258a147a84b9c57867b8861864ba9474ffcc0d23e3d528c16b
and b098f5495d3a771e7c137152b32675526338b3b760325098cd2d268b8937a4a5.
[README.md](README.md) gives commands and resource measurements.

Theorem 1 trusts only the written page identities and real linear algebra.
Theorem 2 additionally trusts complete exact C++/CPython enumeration and
the independently audited predecessor's at-least-two-red conclusion.
Neither theorem is proof-assistant formalized. There is no universal
exclusion of involution-invariant colorings, enumeration of all matching
signings, claim of a valid 22-vertex construction or new Ramsey bound.
