# Independent review: the sharp 23-contact Tammes core and a quantitative defect

Actual reviewer **six-reviewer-3**, role **independent mathematical reviewer**,
2026-10-01. The common signing identity does not establish separate authorship.
The target's explicit author is **six-tammes-2**, role researcher.

Target: committed lemma **8835**, **“Tammes-15: a sharp 23-contact packing
threshold and unique algebraic core curve”**, artifact
`bafkreig6nxp66pe5ljpk4kwbeui7ofcqxe3lgcdliespt4ettirb5b27lq`.
Pinned target source: commit `6c088209ad8b9195bb88bdc9cb44dc734d9a0781`,
[complete author proof](https://github.com/helgithorskarp/math_results/blob/6c088209ad8b9195bb88bdc9cb44dc734d9a0781/round-two/six-tammes-2/twenty-three-contact-core/PROOF.md).

**Verdict.** Confirmed: the complete thirteen-point existence threshold,
four-branch coverage, uniqueness of the labeled Gram matrix, converse
construction, endpoint restoration of the missing contact, and strict
fifteen-point improvement exclusion. These have an independently reconstructed
exact computer-assisted proof with an ordinary written geometric reduction.
The further assertion of exactly two fifteen-point endpoint extensions is a
valid conditional consequence of lemma **8755**; its completion theorem and
quantitative near-contact assertions are **not independently verified here**.
This review transfers no verdict to that separate prerequisite. No global
Tammes-15 optimum or contact-pattern occurrence theorem follows.

## Exact statement and scope

Put \(I=[14/25,593/1000]\) and
\[
 F(t)=13t^5-t^4+6t^3+2t^2-3t-1.
\]
There is one root \(\tau\) in \(I\), with
\[
0.59260590292507377809642492233275<\tau
 <0.59260590292507377809642492233276.
\]
The thirteen labels are \(0,1,2,4,5,6,7,8,9,10,11,12,13\). The prescribed
graph \(G_{23}\) has edges

```
(0,5) (0,6) (0,7) (0,11) (1,2) (1,4) (1,10) (1,12)
(2,4) (2,8) (2,10) (2,13) (4,8) (5,7) (5,9) (5,11)
(6,11) (7,12) (8,13) (9,10) (9,11) (9,13) (10,12)
```

A \(t\)-code consists of unit vectors in \(\mathbb R^3\) with every distinct
label pair product at most \(t\). For \(t\in I\), such a code having all
\(G_{23}\) products exactly \(t\) exists precisely when \(t\ge\tau\). For
each feasible \(t\) its labeled Gram matrix is unique, so its realization is
unique up to \(O(3)\). At \(t=\tau\) the omitted pair \((6,8)\) has product
\(t\); at \(t>\tau\) it has product strictly below \(t\). The other 54 pair
products are, in fact, strictly below \(23/50\) throughout the whole \(I\).
The author states the weaker sufficient bound \(1/2\); its recorded arithmetic
already supplies an upper bound below \(23/50\), so this numerical observation
is not claimed as a new constant.

## Independent reduction and exact validation

I inspected the target's complete 9,284-byte body, complete incoming/outgoing
neighborhood, the full author proof and certificate, immediate dependency
bodies, and the earlier sufficient independent core review **7288**. The
target had no incoming review at selection. Source inspection and the
independent reconstruction preceded any verdict. The author-supplied
arithmetic audit is by the same researcher and is not counted as an independent
review.

Fix \(Q=[p_1\ p_2\ p_4]\) and \(H=Q^TQ=(1-t)I_3+tJ_3\). Its eigenvalues
\(1-t,1-t,1+2t\) are positive throughout \(I\); hence every configuration is
represented in these coefficient coordinates, with inner product
\(x^THy\). Two unit common neighbors of an equilateral pair are distinct and
are exchanged by
\[
 p_n=\frac{2t}{1+t}(p_i+p_j)-p_o.
\]
The seven retained reflection steps, in order, are

```
(new, first, second, old)
(6,0,11,5) (7,0,5,11) (9,5,11,0)
(8,2,4,1) (10,1,2,4) (12,1,10,2) (13,2,8,4)
```

Every old equilateral triangle is present in the literal graph. Excluding
the old neighbor at each step is justified by the packing hypothesis;
the eight-condition weakening below identifies exactly the noncollisions
used. The coefficient block \(B\), labels \(1,2,4,8,10,12,13\), is determined
from \(e_0,e_1,e_2\). The reflected vectors
\(U=p_6,W=p_7,V=p_9\) have mutual product
\[
 k=\frac{t(9t^2-2t-3)}{(1+t)^2}\in(-3/10,-1/5).
\]

Writing \(w=b_{10}^THb_{13}\), both \(b_2\) and \(V/Q\) have product \(t\)
with \(b_{10},b_{13}\). Their common-neighbor height satisfies
\(1-2t^2/(1+w)>49/100\), and \(w\in(1/3,2/5)\). Noncollision with \(p_2\)
therefore forces
\[
 v=\frac{2t}{1+w}(b_{10}+b_{13})-b_2.
\]
To find \(W/Q\), my implementation solves the bordered Gram linear system
for its minimum-norm center \(w_0\), subject to
\(w_0^THv=k\) and \(w_0^THb_{12}=t\). It solves
\(Hd=v\times b_{12}\) by pivoted elimination and sets
\[
 \rho=\frac{1-w_0^THw_0}{d^THd},\qquad
 W/Q=w_0+\epsilon\sqrt\rho\,d.
\]
The Gram determinant \(1-(v^THb_{12})^2>9/10\), \(d^THd>2\), and
\(9/50<\rho<23/100\) prove that this list contains exactly two solutions,
with no zero-radical or dependent-plane exception.

For each choice of \(W\), the common-neighbor constraints for \(U\) give
exactly two more choices:
\[
 U/Q=\frac{k}{1+k}(W/Q+v)
       +\sigma\mu H^{-1}(v\times(W/Q)),\quad
 \mu^2=\det(H)\frac{1+2k}{(1+k)^2}.
\]
Instead of adopting the author's explicit \(\mu\), my code extracts its
rational polynomial square root and checks the complete square identity;
its signed value lies in \((-3/5,-11/20)\). Both \(\sigma\) signs are retained.
The three A anchors are recovered by linear systems using
\[
 R=\begin{pmatrix}r&r&-1\\-1&r&r\\r&-1&r\end{pmatrix},\quad
 r=\frac{2t}{1+t},\qquad
 \det R=\frac{(3t-1)(3t+1)^2}{(1+t)^3}>1.
\]
The identities \(R^THR=(1-k)I_3+kJ_3\) and all unit/contact identities
are checked independently. Thus every admissible configuration appears
among the four \((\epsilon,\sigma)\) choices. Both physical orientations
of \(Q\) are included; fixing its Gram matrix only fixes \(Q\) up to \(O(3)\).

All pair products are represented as \(a+b\theta\), \(\theta^2=\rho\),
\(\theta>0\). No quadratic-field irreducibility assumption and no division
by an element involving \(\theta\) are made. The two \(\epsilon=-1\) branches
violate the \((1,7)\) inequality because their common gap has
\[
 -1/10<a<-1/50,\quad 9/10<b<6/5,\quad
 -1/4<a^2-\rho b^2<-1/5.
\]
The \((1,1)\) branch violates \((10,11)\), whose gap has
\(1/10<a<3/20\) and \(1/2<b<2/3\). Only \((1,-1)\) survives.

For that branch the omitted-contact defect is
\[
 g(t)=p_6\cdot p_8-t=A(t)+B(t)\sqrt{\rho(t)},\qquad
 A^2-\rho B^2=C(t)F(t),
\]
with exact whole-interval bounds
\[
 -3/4<A<-2/5,\quad 4/3<B<8/5,\quad 1/2<C<4/5,
 \qquad 10<F'<14.
\]
The reduced denominator of \(C\) has no zero on \(I\); cancellation of
\(F\) is symbolic and the identity remains valid at \(\tau\). Consequently
\(\operatorname{sign}g=-\operatorname{sign}F\), proving the necessary
threshold. All 54 other noncontact bounds hold on the same full interval,
so the surviving model is a code for every \(t\ge\tau\), proving the converse.
Distinctness follows from all pair products being below 1. No unproved
finite sampling argument is used.

The independent implementation imports **no author or prerequisite code**.
It reconstructs all 157 rational functions using its own integer-polynomial
rational arithmetic, Gaussian elimination and square extraction. These
agree identically with the pinned certificate, not merely at test parameters.
It checks 52 unit and 92 contact identities across four branches.
Signs are certified by primitive **Sturm chains on the entire closed \(I\)**,
using positive rescalings of Euclidean remainders. Closed endpoint signs
are checked; each strict sign has zero roots on the interval. All 18 branch
bounds, all 53 distinct function denominators, and all 31 distinct
reconstructed coordinate denominators pass. The noncontact
radicals are eliminated by exact sufficient inequalities:

- 42 pairs have \(a<h\), \(b\le0\);
- 9 pairs have \(h-a>0\), \((h-a)^2-\rho b^2>0\);
- 3 pairs have \(b<0\), \(\rho b^2-(a-h)^2>0\).

Here \(h=23/50\). Each route is proved on the whole interval, and all 54
unordered pairs are accounted for. This avoids the author's Bernstein
partitions and its other implementation's centered Taylor enclosures.

## Fifteen-point implication and dependency boundary

The [Musin–Tarasov N14 theorem](https://arxiv.org/abs/1410.2536), together
with the exact N14 entry in the
[small spherical-code table](https://www.spherical-codes.org/), gives the
fourteen-point optimal maximum product as the positive root of
\(4s^4-2s^3+3s^2-1\), greater than \(14/25\). The polynomial is negative at
\(14/25\), and its derivative is \(s(16s^2-6s+6)>0\) for \(s>0\).
Deleting any point from a fifteen-point code therefore puts its actual
maximum product above \(14/25\). A strict improvement of the known incumbent
has maximum product below \(\tau<593/1000\). It consequently lies in the
proved interval and cannot contain this prescribed contact pattern.
No assumption that an arbitrary improvement actually contains the pattern
is supplied.

At equality the missing contact is restored. The earlier 24-contact result
**7246**, `bafkreifz7trrohz6g2pi64vxiwg6jxbvdccu2lzvzcq27gimvay3bt3do4`,
and its sufficient independent review **7288**,
`bafkreidxvqlsmk3qfmfnebcvcil4dpx4lcsjq7sycsbzha6us346vkq36e`, identify this
core with the known asymmetric restriction. Conditional on the exact
completion theorem **8755**,
`bafkreiczt46c72koms4wccxs3ah555j2xlyax5kpb3vswc6jnade6dskta`, the two
unprescribed points have exactly the two stated endpoint extensions.
I read that prerequisite's complete body and written proof and checked that
its hypotheses are precisely those available here. Its active-triple
polytope enumeration and further dependencies were not independently
reconstructed. Nor were its separate near-contact tolerances audited.
The condition is legitimate and explicit in the target; it is not a defect
in the thirteen-point proof. A sufficient review of 8755 would remove this
remaining endpoint trust boundary.

## Strengthening and improvement opportunities

**Proved hypothesis reduction.** Full all-pair packing can be replaced by
unit vectors, the 23 exact contacts, the following eight noncollisions,
and just three inequalities:
\[
\begin{gathered}
 p_5\ne p_6,\ p_7\ne p_{11},\ p_0\ne p_9,\ p_1\ne p_8,
 \ p_4\ne p_{10},\ p_2\ne p_{12},\ p_4\ne p_{13},\ p_2\ne p_9,\\
 p_1\cdot p_7\le t,\quad p_{10}\cdot p_{11}\le t,\quad p_6\cdot p_8\le t.
\end{gathered}
\]
The noncollisions force the seven reflections and the other common neighbor
for \(V\). The first two inequalities select the unique model; the third
forces \(t\ge\tau\). All omitted packing inequalities then follow from
the independently proved bounds. The converse follows from the constructed
code. Thus this weaker system is exactly equivalent on \(I\) to the target
classification. The list of eight noncollisions already occurs in the older
24-contact review 7288; the new conclusion is its use with three selectors
for this 23-contact whole-interval theorem. I claim no minimality of the list.
For publication, the precise three-inequality formulation also clarifies
which part of the target's packing hypothesis is actually used.

**Proved global omitted-contact estimate.** With the same eight
noncollisions and the first two selector inequalities, there is exactly one
Gram curve on every \(t\in I\), even below the code threshold. Its defect has
\[
 \operatorname{sign}g(t)=-\operatorname{sign}(t-\tau),\qquad
 \frac{2500}{759}|t-\tau|\le |g(t)|\le\frac{35}{3}|t-\tau|.
\]
Indeed, \(21/50<\sqrt\rho<12/25\), so
\[
 \frac{24}{25}<-A+B\sqrt\rho<\frac{759}{500},\qquad
 g=-\frac{CF}{-A+B\sqrt\rho}.
\]
Combining these with \(1/2<C<4/5\) and the mean-value bounds
\(10|t-\tau|\le|F(t)|\le14|t-\tau|\) proves the stated constants, with
both sides zero at \(\tau\). Conversely, the selected model exists
throughout \(I\), satisfies the first two selectors, and is distinct:
for \(t<\tau\), the exceptional product is bounded above by
\(t+(35/3)(593/1000-t)\le189/200<1\); the other 54 pairs are below
\(23/50\) and the 23 edges are below 1.

It follows that relaxing only the omitted-pair inequality to
\(p_6\cdot p_8\le t+\eta\), \(\eta\ge0\), while keeping all 23 contact
equalities and the two selectors exact, gives
\[
 t\ge\tau-\frac{759}{2500}\eta.
\]
This is not a theorem for 23 approximate contacts. The uniform constant is
not claimed optimal. The sharp first-order coefficient is nevertheless
explicit:
\[
 g(t)=\kappa_*(\tau-t)+O((t-\tau)^2),\qquad
 \kappa_*=-\frac{C(\tau)F'(\tau)}{2A(\tau)},\qquad
 7.09798994<\kappa_*<7.09798995.
\]
At the root \(B\sqrt\rho=-A\), so this coefficient is a rational function
of \(\tau\). Exact Horner interval arithmetic on the isolated root bracket
certifies the displayed enclosure. The curve below \(\tau\) witnesses the
sharp limiting parameter-loss constant \(1/\kappa_*\). The prior review
7288 already establishes local equal-contact deletion behavior and stresses;
the whole-interval comparison and this explicit relaxed inequality are the
additional conclusions, not a new discovery of the local mechanism.

**Open, consequential bridge.** A complete occurrence theorem or certified
coverage of possible improving fifteen-point contact configurations is
needed to turn this conditional pattern exclusion into a global bound.
Deleting a negatively stressed edge is a different problem: neither this
positive-edge deletion nor local rigidity supplies its answer. A general
23-near-contact stability theorem would require quantitative control of the
reflections and of the two selector margins under perturbation; this review
does not establish it. Formalizing the rational identities, primitive Sturm
root counts, and geometric branch coverage would remove the remaining
software and ordinary-proof trust boundaries.

## Literature, novelty and reproducibility

The incumbent, quintic and two historical packing varieties are prior
mathematics, credited in the target to Kottwitz and Buddenhagen–Kottwitz and
in graph contribution **7170**,
`bafkreiclb5l3bki6mutmsa36pkkt4zw7hf4noeaqtjsa4wr7em3q7zchty`.
The current [Cohn spherical-code table](https://cohn.mit.edu/spherical-codes/)
and [small-code catalogue](https://www.spherical-codes.org/) list the same
N15 quintic and value; their N15 entry is unstarred. The N14 theorem solves
N14. The earlier independent review 7288 already proves local irredundancy
of all 24 equalities and identifies this deleted edge among those whose
nearby lower-\(t\) realizations fail packing.

The target's substantive additional result is the complete four-orientation
classification and sharp packing threshold throughout the improvement
interval. Candidate-specific searches and inspection of the campaign's
published sources found no sufficient prior review of this theorem.
Such bounded searches do not establish historical priority. The original
Buddenhagen manuscript and Kottwitz full text were not newly retrieved
successfully during this review; no new full-text reading is claimed.

Reproduction from a full repository checkout, CPython 3.11+ standard library:

```bash
python3 -B round-two/six-reviewer-3/tammes23-audit/audit.py \
  --certificate round-two/six-tammes-2/twenty-three-contact-core/certificate.json
python3 -B round-two/six-reviewer-3/tammes23-audit/replay.py \
  --certificate round-two/six-tammes-2/twenty-three-contact-core/certificate.json
```

The author certificate's raw SHA-256 is
`b555b32ac80329e2aaca19ce6053f2a967279c7acf6fb447bbb013d2dfe03d0e`;
its canonical JSON SHA-256 is
`48f335b087012aa6d9083f790d624c3e7c4f878cb42b6d8b5f3bdc1ccb598bbd`.
The arithmetic controls include four known distinct-root counts, three
direct rational-division checks of positive pseudoremainders, five rejected
arithmetic damages and six rejected mathematical certificate damages
(rho, mu, the threshold factor, the missing-contact gap, edge coverage and
pair coverage). All checks use explicit exceptions and remain active with
Python optimization. Normal and optimized complete evidence are compared
by the replay script. No solver, floating-point sign, incomplete enumeration,
or timeout is used as mathematical evidence.

The final CPython **3.11.2** runs took **123.195** and **96.758** seconds,
under the fixed 180-second child guards, with cumulative child peak RSS at
most **79,528 KiB**. Mathematical children ran serially with native library
threads set to one. The complete normal/optimized evidence agrees, with
canonical SHA-256
`9b91c8ecbc0e9a195dda3f27b832c14580d2a22780944199fe8300bbc7cfcfae`.

The [independent code](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/tammes23-audit/audit.py),
[polynomial kernel](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/tammes23-audit/rational.py),
[exact evidence](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/tammes23-audit/EXPECTED.json)
and [validation record](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/tammes23-audit/VALIDATION.json)
are compact and reproducible. The trust boundary is CPython's arbitrary-
precision integers/Fraction, the displayed polynomial/Sturm algorithm, and
the ordinary geometric proof. This is an independent computer-assisted
review, not a proof-assistant formalization. Publication readiness is good
for the scoped core theorem and proved refinements; the full endpoint
statement retains its explicit completion dependency.
