# Independent n26 minimum-class and sharp-rank audit

Actual author **six-reviewer-1**, role **independent mathematical reviewer**,
2026-10-03. Target: committed LEMMA10188/index0, by
six-downset-2/researcher, reference
`bafkreid7zhqgjk3bycgl7l6dqhjnatrvsvf3dbfens6nlwxuiflu53osui`.
The author's 36 declarative rational coordinates are attributed in
[WITNESS.json](WITNESS.json). This checks their witness; it does not discover it.
The written target, its numbers and relevant prior proofs were exposed:
**NOT BLIND**. The target's executable source, expected files and controls
were not opened before sealing this primary calculation.

This audit explicitly reuses the reviewer's n24 exact backend and literal
n8 control unchanged, and adapts the reviewer's n24 decoder, physical-block
checker and stability argument. Their source commit is recorded in
[PRIMARY_SEAL.json](PRIMARY_SEAL.json). It is an independent audit of the
new n26 point, not a new-from-scratch implementation, or transport of the
earlier n24 or n26 fixed-slice verdict. The new full n26 arithmetic,
affine decoder comparison and original metric identities are checked here.
All ordinary mathematical bridges below remain unformalized.

## 1. Original domain and all-real obstruction

Let \(\mathcal D=\{A\subseteq[26]:|A|\le24\}\), including the empty set.
Put \(N=67108837\), \(s=33554406\), \(h=N-s=33554431\), and
\(g=N-2s=25\). An ordinary H matrix is real symmetric,
\(M\mathbf1=\mathbf1\), with \(M_{AB}=0\) if
\(A\cap B\ne\varnothing\), and \(L=sI+hM\succeq0\).
The additional cap is \(L\preceq NI\). Supported entries may be negative.
Original ground-set complements are used. A noncentral class a=2..12 is
present if some unordered original pair \(\{A,A^c\}\) of sizes a,26-a
has \(L_{A,A^c}<s\). Middle size13 is not counted.

Every nonempty diagonal is s. Its complementary 2-by-2 lower minor gives
\(L_{A,A^c}\le s\), so absence of a class forces equality for EVERY pair
in that class. Saturation kills \(e_A-e_{A^c}\) by PSD, and the two
columns are equal. For every other nonempty X at least one of the pair
intersects X; support sets the corresponding cross entry to zero, and
column equality kills the other. The row sum \(L\mathbf1=N\mathbf1\)
therefore forces both empty cross entries to g.

For q distinct saturated unordered pairs, let
\(\ell=L_{\varnothing,\varnothing}\). On the empty indicator and their
pair sums the original metric is diag(1,2,...,2). Lower and upper forms are
\[
 \begin{pmatrix}\ell&2g\mathbf1^T\\2g\mathbf1&4sI_q\end{pmatrix},\qquad
 \begin{pmatrix}N-\ell&-2g\mathbf1^T\\-2g\mathbf1&2gI_q\end{pmatrix}.
\]
The Schur complements give \(\ell\ge qg^2/s\) and
\(N-\ell\ge2qg\), hence \(qg\le s\) and
\(q\le1342176\). This reconstructs the credited9942 mechanism.
It needs the upper cap; an uncapped count obstruction is not claimed.

At most four present classes leave at least seven absent. Their least
possible population is
\(\sum_{a=2}^8\binom{26}a=2533960>1342176\).
Five present leave six absent. Their minimum is
\(q_0=\sum_{a=2}^7\binom{26}a=971685\).
Every different six-element absent set has population at least
\(\sum_{a=2}^6\binom{26}a+\binom{26}8=1876160>1342176\).
Thus all real capped original matrices need at least five present classes,
and equality forces the unique absent set2..7. `check.py` verifies all2048
class subsets as integer arithmetic. This is not enumeration of matrices,
and imposes no invariance, rationality, centering or sign condition on competitors.

## 2. Sharp rank ceiling and complete invariant face

Let w_i indicate the star of sets containing point i; its size is s.
Support gives \(w_i^TLw_i=s^2\). Centering gives
\(v_i=w_i-(s/N)\mathbf1\) of zero lower energy, hence
\(Lv_i=0\) and \(Lw_i=s\mathbf1\). The 26 centered stars are independent:
evaluation at empty forces the sum of coefficients to zero; evaluation at
each singleton then forces its coefficient to zero. Saturated pair
differences vanish at empty and singletons and have disjoint supports.
They are independent of each other and of the stars. Consequently
\[
 \operatorname{rank}L\le N-26-q.
\]
For class minimum five this is \(66137126\). Equality means precisely
\(26+971685=971711\) kernel dimensions and excludes any additional
saturated pair, including middle13. The same ceiling applies to uncapped
ordinary H on this fixed saturated face. The star and rank mechanisms retain
10030 credit; earlier certificates supply no new-point feasibility here.

Permutation averaging preserves support, row sums and both PSD inequalities.
Each complementary deficit is nonnegative, so averaging preserves exactly
the present and absent classes. Saturated classes2..7 have no proper
nonempty couplings. The resulting invariant face has six complementary
deficits d8..d13 and thirty proper disjoint coefficients t(a,b),
8<=a<=b<=18 and a+b<26. All other nonsingleton proper coefficients are zero;
complementary entries2..7 equal s. This is a complete36-real-coordinate
affine face, not a positivity requirement on proper coefficients.

Write B_ab for the original disjoint nonempty entry of L. Every singleton
entry is forced by the excluding-point star equations
\[
 \sum_{b=1}^{24}\binom{25-a}{b-1}B_{ab}=s\quad(a=1,...,24).
\]
The primary decoder solves the entire24-variable rational system.
A separate weighted triangular decoder uses
\[
 B_{1a}=\frac{(26-a)s-\sum_{b=2}^{24}b\binom{26-a}b B_{ab}}{26-a}
 \ (a\ge2),\qquad
 B_{11}=\frac{25s-\sum_{b=2}^{24}b\binom{25}b B_{1b}}{25}.
\]
Both maps are affine. The baseline and all36 unit-coordinate directions
are compared on the ENTIRE25-by-25 B table, all24 empty cross entries and
the loop. These37 complete probes certify equality on the entire affine
36-real-coordinate face, rather than sampled numerical agreement.

## 3. Original empty completion and harmonic exhaustion

For nonempty A,B define
\(C_{AB}=s\mathbf1_{A=B}-1+B_{|A|,|B|}\mathbf1_{A\cap B=\varnothing}\).
With \(E=[-\mathbf1^T;I]\), put \(L=J_N+ECE^T\).
Independently, original row sums reconstruct
\[
 L_{\varnothing,a}=h-\sum_b\binom{26-a}b B_{ab},\qquad
 L_{\varnothing,\varnothing}=N-\sum_a\binom{26}aL_{\varnothing,a}.
\]
The second decoder instead uses C's row sums c_a, giving empty cross1-c_a
and loop1+sum binom(26,a)c_a. All size rows, all excluding-point star
equations and the actual empty star and row are checked. The actual loop is
\(219593185802261441/142800000000\); all24 cross entries in WITNESS are
regenerated, not taken from native expected results.

E has full column rank and range1-perp. Thus lower PSD and rank are those
of C, with rankL=1+rankC. The full upper identity
\(NI-L=E(NI_F-J_F-C)E^T\) retains the original empty row and loop.

For completeness, the classical harmonic bridge credited to9639 is
reconstructed. On subset layers let R add a point by summation and D be
its adjoint. Direct counting gives \(DR-RD=(26-2a)I\) on layer a.
R is injective below the middle (take inner products in this identity).
Its degree-j harmonic kernel has dimension
\(m_j=\binom{26}j-\binom{26}{j-1}\).
For harmonic f on j-subsets let
\(f_a(A)=\sum_{S\subseteq A,|S|=j}f(S)\).
The commutator gives
\(DR^tf=t(26-2j-t+1)R^{t-1}f\), and hence
\(\|f_a\|^2=\binom{26-2j}{a-j}\|f\|^2\).
Lowering shows different degrees orthogonal. The dimension telescope
\(\sum_{j\le\min(a,26-a)}m_j=\binom{26}a\) exhausts every retained layer.
Expanding exclusion over the j points, all lower-degree terms vanish by
harmonic lowering, giving
\[
 \sum_{B\cap A=\varnothing,|B|=b}f_b(B)
 =(-1)^j\binom{26-a-j}{b-j}f_a(A).
\]
With \(I_j=\{\max(1,j),...,\min(24,26-j)\}\) for j=0..13,
\[
 H_j[a,b]=\binom{26-2j}{a-j}
 \left[s\mathbf1_{a=b}-\mathbf1_{j=0}\binom{26}b
       +(-1)^jB_{ab}\binom{26-a-j}{b-j}\right].
\]
All full forms are checked symmetric; multiplicity-weighted dimensions sum
to N-1. No mean or highest middle parity direction is omitted.

The reviewer uses inverse empty-coordinate congruence. In degree0 set
b_a=binom(26,a), P=I+1b^T. An original mean vector with nonempty layer
values z has empty value -b^Tz and norm z^T(diag(b)+bb^T)z.
Its E^T image is y=Pz, with \(P^{-1}=I-\mathbf1b^T/N\). Therefore the
TRUE original metric in y coordinates is
\[
 R_0=(P^{-1})^T(\operatorname{diag}b+bb^T)P^{-1}
     =\operatorname{diag}b-bb^T/N.
\]
For j>0 use \(R_j=\operatorname{diag}\binom{26-2j}{a-j}\).
The original upper form in these coordinates is \(V_j=NR_j-H_j\).
Every entry of P-inverse, the full congruences back to original H/V/metric,
all transformed kernels, and the full endpoint sum are checked exactly.
Treating the degree0 physical norm as the original norm would be incorrect.

The reused [literal.py](literal.py) directly builds all247 original n8
vertices, all61009 upper-lift entries and all1976 original point-star rows.
Definition-level pair-difference harmonics check every entry of all five
n8 degree blocks, and centered original layer indicators check the metric
including empty. This is a reused convention control, not a new n8 theorem,
positive H example, or enumeration of the67108837 n26 vertices.

## 4. Exact n26 certificate and both original spectral gaps

Known lower kernels are the cardinality vector at j=0, the constant vector
at j=1, and \(e_a-(-1)^je_{26-a}\) for each saturated a=2..7 in I_j.
Their independent counts across all fourteen degrees are
(7,7,6,5,4,3,2,1,0,0,0,0,0,0). Every full kernel identity and independence
is checked. Rational elimination on the kernel vectors chooses complementary
coordinate planes. Exact diagonal-pivot completion of squares verifies
all full lower and upper PSD forms and all ranks; the reused backend uses
explicit checks which also run under Python -O.

Put \(\epsilon=1/100000000\). On each complementary lower plane,
the calculation proves \(H_j\succ\epsilon R_j\); on the COMPLETE upper
space, \(V_j\succ\epsilon R_j\). The weighted nullity is971711, giving
original lower rank66137126 and upper rankN-1=67108836. All six active
deficits are strictly positive. This establishes attainment of the minimum
class count and the constrained rank ceiling at this exact new point.

For the additional ORIGINAL lower spectral gap, take x orthogonal to the
fixed full kernel and write x=k+u, with k in the kernel and u in the chosen
complementary plane. Then
\(x^TLx=u^TLu\ge\epsilon\|u\|^2\ge\epsilon\|x\|^2\), since
\(u=x-k\) and \(\|u\|^2=\|x\|^2+\|k\|^2\).
The argument uses the actual metric R, and applies in every orthogonal
harmonic copy. The remaining constant direction has eigenvalue N. Hence
\[
 \operatorname{spec}(L)\subseteq\{0,N\}\cup[\epsilon,N-\epsilon].
\]
Zero has multiplicity971711; N is simple; the other66137125 eigenvalues
lie in the displayed interval. For M the nonendpoint gap from BOTH
\(-s/h\) and1 is at least \(1/3355443100000000\).
Thus the original Hoffman value is s and the unit eigenvalue is simple.
No spectral-gap optimality is claimed. The representative argument above
is essential to pass from a retained-plane bound to an orthogonal gap.

## 5. Proved closed36-real-coordinate stability box

Perturb each defining real coordinate independently by at most
\[
 \delta=\epsilon/2^{101}
 =1/253530120045645880299340641075200000000.
\]
All prescribed zeros and saturated entries remain fixed; singleton and
empty entries follow the same affine equations. These36 coordinates are
injective original entries or deficits, so the box is genuinely36-dimensional.

Every nonsingleton coefficient changes by at most delta. The original
excluding-point equation for a>=2 bounds a singleton change by
\(2^{23}\delta\), and the a=1 equation bounds B11 by
\(2^{47}\delta\). More explicitly, for general n these bounds are
\(\delta(2^{n-a-1}-1)\le2^{n-3}\delta\) and
\(2^{n-3}\delta(2^{n-2}-1)\le2^{2n-5}\delta\).
The nonempty row decoder bounds every empty cross change by
\(2^{3n-6}\delta=2^{72}\delta\). Summing the binomial populations bounds
the loop change by \(2^{4n-6}\delta=2^{98}\delta\).
The empty absolute row sum is at most \(2^{99}\delta\); every nonempty
absolute row sum is at most \(2^{73}\delta\).
These sums cover ALL original vertices. Symmetry therefore gives
\[
 \|\Delta L\|_2\le\|\Delta L\|_\infty\le2^{99}\delta=\epsilon/4.
\]
The exact26 centered-star and971685 pair-difference kernels persist,
and the constant direction retains eigenvalue N. On their fixed orthogonal
complement, the two baseline gaps and this norm bound imply
\[
 (3\epsilon/4)I\preceq L\preceq(N-3\epsilon/4)I.
\]
Every active deficit stays positive: the minimum baseline exceeds1/2,
while delta<1/2. Consequently EVERY point in this CLOSED independent-coordinate
box, including all boundary choices, is an original capped H matrix with
exactly five present noncentral classes, sharp lower rank66137126, upper
rank67108836 and a simple unit eigenvalue. The nonendpoint M gaps remain
at least \(3/13421772400000000\) from both endpoints. This uses the credited
earlier n24 stability method with an independently checked n26 baseline;
it is not optimized, all-order attainment or classification of all caps.

## Strengthening and improvement opportunities

The two-endpoint n26 gap and explicit closed36-coordinate box in Sections4--5
are proved refinements of the target's point certificate and upper floor.
The unchanged n24 method has been credited, so these are new-order certified
consequences, not a claim of new historical proof machinery.

The most useful further improvement is a larger certified radius: use the
exact affine sensitivity matrices and optimize a bound in the original
Euclidean metric. That would require a new verified operator-norm bound;
the deliberately conservative row-sum estimate here does not establish it.
Further orders require their own complete decoder, rational point, all
physical degrees, kernel and original-metric certificates. There is no
automatic feasibility transfer from n24 or from this n26 point.
Classifying noninvariant five-class caps would require controlling their
full invariant-orthogonal components, beyond this36-coordinate face.

## 6. Trust, scope and prior-art boundary

The lift, saturation, harmonic, count and rank mechanisms retain7578,
9365,9639,9942,10008 and10030 credit. Earlier8319/9793/9968 and10123/10138
review contexts are not transported certificates. The reviewer's10093/index3
n24 audit supplies the explicitly reused source and stability method.
Unrestricted near-cube cap existence is earlier campaign mathematics; the
reviewed claim is constrained minimum-class count and rank attainment.

The primary calculation imports only Python standard-library modules and
this sealed local source, with exact Fraction arithmetic. It does not import
author programs, author expected output, SymPy, an SDP solution or a CAS.
Ordinary real linear algebra, support/rank arguments, harmonic completeness,
the original-coordinate bridge and perturbation estimates remain trusted
unformalized proofs. Hash matching alone is not a mathematical proof.
Full generated records stay in caller-selected scratch; compact hashes
and source suffice for cold regeneration.

The primary problem is spectral Conjecture H in
[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4).
Its [version history](https://arxiv.org/abs/2609.28404) was checked2026-10-03.
The cap is additional to H; this fixed-order theorem settles neither H nor I.
Candidate-specific searches justify no claim of historical priority.
