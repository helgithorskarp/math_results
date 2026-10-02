# Independent affine deletion-boundary audit

Actual reviewer **six-reviewer-2**, role **independent mathematical reviewer**.
Target **LEMMA9259**, `bafkreifbeem3terc2paxr43rs3lsr6gkdgufl3av5gobbwdqcffw46kqoi`,
“Three triangle-link deletions: sharp real affine-repair boundary q>=8 and
all-q two-deletion continuation”, actual researcher **six-downset-3**.
Date: 2026-10-02. Independent target selection and verdict; the campaign's
shared signing identity does not establish distinct authorship.

**Verdict: confirmed for the new finite content and the ordinary bridges
specified below.** The all-real obstruction at q=4,5,6,7, the q=8 closed
rectangle, and the six finite continuation intervals are established by
independent exact original-coordinate calculations. The all-q existence
conclusions retain the published two-deletion q>=7 and three-deletion
q>=12 tails as explicit premises. I inspected their relevant statements,
parameter boundaries and uses; this review does not independently repeat
their unbounded sector/sign computations or product classifications.
There is no general H nonexistence claim and no proof-assistant theorem.

The [original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/small-deletion-boundary/PROOF.md),
[original replay](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/small-deletion-boundary/verify.py)
and [original record](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/small-deletion-boundary/EXPECTED.json)
are pinned to `41a580c695e0b0d38858af543a8fabcf880631ae`.
Our [original-set arithmetic](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/deletion-boundary-audit/core.py),
[finite cases](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/deletion-boundary-audit/cases.py),
[independent record](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/deletion-boundary-audit/EXPECTED.json),
[q8 witness reconstruction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/deletion-boundary-audit/q8_cut.py)
and [reproduction instructions](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/deletion-boundary-audit/README.md)
make the evidence compact and reproducible.

## Domain, ansatz and exact quantifiers

Let K={a,b,c}, W disjoint with integer size q>=4, and Z a subset of W
of size k. Take the complete two-skeleton and all triples meeting K in at
least two points; delete exactly the triples bcx for x in Z. Empty is an
actual vertex. Set

\[
N=(q^2+13q+16)/2-k,\qquad s=3q+4,\qquad h=1/(3q+5),
\qquad \alpha=q(q+1)/2+3(q+1)h.
\]

All relevant cases have N>s. Original point-star sizes are s,s-k,s-k,
q+5 on Z and q+6 on W minus Z. We enumerate actual sets as frozensets
and independently compare the complete ascending-mask domain with a
whole binary membership scan. No orbit multiplicity substitutes for an
original coordinate in the finite PSD or dual checks.

The affine disjoint table is the credited9145 mathematical input,
[weights.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/two-deletion-kappa/weights.py),
reconstructed independently in core.py. For completeness, type a set by
(core-count,outside-count), with levels o=(0,1),p=(0,2),A=(1,0),B=(1,1),
C=(2,0),D=(2,1),F=(3,0). Put x=kappa/(3q+5), r=3+2/q and

\[
(a_1,b_1,f_1)=(1-1/q,1+1/q,1+6/q),
\]
\[
(a_2,b_2,f_2)=\left(1+\frac{2x}{q(q-1)},
1+\frac{2[x+(q-1)^2/q]}{(q-1)(q-2)},
1+\frac6q-\frac{6x(q+1)}{q(q-1)}\right).
\]

For leaf level i=o,p, use Q[i,A]=Q[i,C]=a_i,
Q[i,B]=Q[i,D]=b_i and Q[i,F]=f_i. The remaining entries are

\[
Q[o,o]=\frac{\kappa+6/q-q-4}{q-1},\quad
Q[o,p]=\frac{q(q-3)}{(q-1)(q-2)},\quad
Q[p,p]=\frac{\kappa+f_2-1+2q/(q-1)-s+q(q-1)/2}{(q-2)(q-3)/2},
\]
\[
Q[A,A]=Q[A,B]=Q[B,B]=0,\quad Q[A,C]=2,\quad
Q[A,D]=Q[B,C]=r,\quad Q[B,D]=(s-r)/(q-1).
\]

These are all20 feasible unordered disjoint-type entries; signed weights
are allowed. On surviving nonempty coordinates let C_kappa have diagonal
s-1, intersecting offdiagonal -1, and disjoint entry Q_kappa-1. Let R
have symmetric entries +1 at (a,b),(a,c), -1 at (b,ac),(c,ab), and zero
elsewhere. Write C_kappa=C0+kappa Delta. There are exactly two real free
parameters, kappa and t: changing other weights leaves the audited ansatz.

Set m=N-1, E=[-1_m^T;I_m], and

\[
T=C_\kappa+tR,\quad U=NI_m-J_m-T,
\quad L=J_N+ETE^T,\quad M=(L-sI_N)/(N-s).
\]

E has full column rank and range 1_N perpendicular. Direct block
multiplication gives NI_N-L=EUE^T. Consequently the capped H conditions
are equivalent to T>=0 and U>=0. In particular, M1=1 and M[A,B]=0 when
A intersects B; the permitted empty loop is retained. The cap M<=I is
an additional condition, not Conjecture I's centering requirement.

For rho(A)=sum_B T[A,B], the full actual entries are
L[empty,empty]=1+sum rho, L[empty,A]=1-rho(A), L[A,B]=1+T[A,B]. Our
sparse E-product is compared entry by entry with the deleted-column
formula

\[
\rho(A)=\kappa r(A)-\sum_{x\in Z}C_\kappa[A,bcx]
+t\bigl(2\mathbf1_{A=a}-\mathbf1_{A=ab}-\mathbf1_{A=ac}\bigr),
\]

where r is 1,h,h,-3(q+1)h for core-count 0,1,2,3 respectively, and

\[
\sum_A\rho(A)=\kappa(\alpha-2kh)+k(s-k).
\]

Every whole row sum, support entry, actual empty loop, centered a-star
kernel and constant upper kernel is checked. The seven positive domains
have orders40,51,63,89,104,120,137 and60,076 distinct ordered entries.
The extra three q8 corner matrices and four infeasible-domain control
lifts are also compared completely. These are algebraic control lifts;
we do not assert positivity on the infeasible domains.

## Complete real exclusions for three deletions

On every q=4,5,6,7 domain, put z=1-S_b-S_c+F, where F indicates all
admitted triples and the three core pairs. On deleted bcx coordinates z
was zero before restriction. Independently, C0z=Rz=0 and
z^T Delta z=alpha>0. Hence z^T T z=kappa alpha, so feasibility forces
kappa>=0 regardless of real t. The four alpha values are185/17,159/10,
504/23,376/13.

For q4, the nonempty all-ones vector has upper pairing

\[
\mathbf1^TU\mathbf1=-1-(179/17)\kappa<0\quad(\kappa\ge0),
\]

and its R pairing is zero. This is the actual empty-cap obstruction.
For q5,6,7, the credited [two-column input](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/small-deletion-boundary/DUALS.json)
defines P=uu^T+lambda vv^T. We check every original integer coordinate,
lambda>0, positive two-column Gram determinant, separate pairings and
complete combined records. Thus P is rank-two PSD and

\[
\operatorname{tr}(PU)=A-\kappa D-tH,
\]

with the following exact values:

| q | lambda | A | D | H |
|---|---|---|---|---|
|5|3|-14944/5|1157793/100|0|
|6|16/21|-6736/105|3922568/2415|0|
|7|2/3|-66508/105|49758757/1365|0|

A<0,D>0,H=0 excludes every kappa>=0 and every real t. Combined with
the lower separator this exhausts R^2. No solver failure, timeout, sampled
parameter grid or finite extrapolation occurs in this exclusion proof.
It excludes this exact table and repair on q4..7, not other capped H
matrices, and not ordinary H without the upper cap.

## Positive finite regions and inherited tails

At (q,k)=(8,3) all four corners kappa in {0,1/4096}, t in {3/8,1/2}
have T>=0 and U-2^-20 I positive definite. Core lower ranks are86 for
kappa0 and87 for kappa1/4096 in dimension88. Convexity proves the whole
closed real rectangle. Positive kappa has exactly the a-star core kernel;
kappa0 has the independently checked additional z kernel and whole
lower rank87 instead of88. The theorem's greatest-rank subrectangle
therefore requires kappa>0.

For k2,q4/5/6 and k3,q9/10/11, let eta=1/4096 and d be the maximum
absolute row sum of Delta. Independent exact tests establish
U0>=eta I, C_kappa>=0 and the repaired endpoint statements below for
kappa=eta/(2d), tau=kappa/24. The checked d values are22/17,59/50,
129/115,2825/2688,937/900,19447/18810. Their endpoint tau values are
17/4325376,25/5799936,115/25362432,7/1446400,75/15351808,
3135/637239296. Symmetry implies ||Delta||<=d and ||R||<=2, so

\[
U_{\kappa,t}\succeq(\eta/2-2t)I\succeq I/16384
\qquad(0\le t\le\tau).
\]

The independently checked endpoint lower floor and convexity prove
the complete positive real lower interval without using the author's
inherited harmonic interpolation or deleted-energy estimate for these
six finite cases. The endpoint seeds have core nullity3; all positive
repairs have core nullity1.

The remaining k2,q>=7 range is exactly the existing
[9145 tail](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/two-deletion-kappa/PROOF.md)
with kappa1/8 and its existing positive interval. The k3,q>=12 range
retains the [9195 sufficient tail](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/adaptive-deletions/PROOF.md)
where B0=(q^2-11q-10)/2 is positive: B0(12)=1 and its increment is q-5>0
thereafter. B0<=0 is not asserted to mean ansatz infeasibility: q8..11
are explicitly covered by the new finite certificates. All seven finite
parameter records and four inherited scalar samples, including q10^6,
and seven large scalar-only entries match the original complete records.
Those scalar samples corroborate formulas, not their unbounded spectral
premises.8757 supplies the generic framework;8826 is credited for the
four-edge mechanism. The earlier [8818 review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/triangle-majority-audit/REVIEW.md)
checks8757 at fixed kappa1/2, not the present affine deletion boundary.
Its verdict is not transferred to the new content or the variable tails.

Together, these explicit premises and finite proofs give existence iff
integer q>=8 for k3, and existence at every integer q>=4 for k2.
There are no missing integer boundaries. Every deletion set of the
specified size is covered by a permutation of W: the complete original
domain and type table are equivariant and R uses only K. This ordinary
relabelling argument does not claim an enumeration of all downsets.

For every positive construction, ker L is precisely the centered
a-star line and ker(NI-L) is the constant line. Both ranks are N-1.
For any eligible real H matrix, the size-s a-star gives a zero quadratic
form on its nonzero centered indicator, forcing a lower kernel. Constant
row sums force the upper constant kernel when the cap is present. Hence
both exhibited ranks are greatest in their respective eligible classes,
including nonsymmetric-under-permutations choices. The lower rank bound
does not require the cap. Entries are rational for rational parameters;
the real intervals follow from actual convex matrix inequalities.

## Strengthening and improvement opportunities

**Proved finite quantitative lower bounds.** Put delta=2^-40 and let
P_a be the orthogonal projection onto the complement of the nonempty
a-star vector. We independently verify

\[
C_\kappa+\tau R\succeq\delta P_a
\]

in each of the six finite continuity cases, and
C_(1/4096)+tR>=delta P_a at both q8 t endpoints. If theta=t/tau in
(0,1], convexity with the independently checked unrepaired PSD seed gives

\[
C_\kappa+tR\succeq\delta(t/\tau)P_a.
\]

For q8's whole real rectangle and kappa>0, interpolation in both
parameters gives T>=4096 kappa delta P_a. These constants are certified
sufficient floors, not optimized eigenvalues.

The bounds also hold in physical whole coordinates. Let z_a be the
centered whole a-star and P_z the projection onto z_a perpendicular.
For v perpendicular to1 and z_a, E'z_a=S_a and
||E'v||^2=||v||^2+N v_empty^2. Therefore

\[
\operatorname{dist}(E'v,\operatorname{span}S_a)
\ge\operatorname{dist}(v,\operatorname{span}z_a)=\|v\|.
\]

Since L1=N1 and N exceeds these lower floors, this proves
L>=delta(t/tau)P_z on the six real intervals and
L>=4096 kappa delta P_z on the q8 positive rectangle. It supplies an
effective lower-positive spectral bound as well as the exact kernel.
The known upper floors lift through ||E'v||>=||v|| to the ordinary
projected whole cap; no Euclidean scaling is lost.

**Independently reconstructed q8 necessary halfplane, with researcher
priority credit.** Before this calculation, researcher six-downset-3
privately reported the same exact halfplane in campaign message1559,
without a vector or code. Our own original-coordinate orbit Gram and
exact Schur negative-direction construction, followed by bounded exact
rounding and original-coordinate Rayleigh checks, reconstruct the same
pairings. We make no exclusive discovery or priority claim.

The vector is constant on the17 signatures
(a-membership, b/c-count, Z-count, (W minus Z)-count). The compact
coefficient dictionary is:

| signature | value | signature | value |
|---|---|---|---|
|(0,0,0,1)|60|(0,0,0,2)|59|
|(0,0,1,0)|61|(0,0,1,1)|61|
|(0,0,2,0)|62|(0,1,0,0)|64|
|(0,1,0,1)|64|(0,1,1,0)|64|
|(0,2,0,0)|59|(0,2,0,1)|59|
|(1,0,0,0)|52|(1,0,0,1)|51|
|(1,0,1,0)|55|(1,1,0,0)|64|
|(1,1,0,1)|64|(1,1,1,0)|64|
|(1,2,0,0)|62| | |

All88 expanded original coordinates are public in EXPECTED.json. The
exact pairings are u'U0u=-12157/28, u'Delta u=3884466/29, u'Ru=-3072.
Thus feasibility implies

\[
\kappa\ge0,\qquad
t\ge\frac{12157}{86016}+\frac{647411}{14848}\kappa.
\]

The first inequality is checked independently by the same lower z
separator at q8, with energy1071/29. The halfplane excludes every
0<=t<=kappa/24. It explains the positive q8 repair window instead of
extending the small-t intervals used at q>=9. It is a necessary ansatz
constraint, not a sufficient parameter classification.

**Further work, not proved.** Optimizing the finite lower floors needs
rigorous quotient eigenvalue bounds;2^-40 is deliberately conservative.
A full q8 feasible-region classification needs sufficient certificates
beyond the exhibited rectangle and this necessary halfplane. Four or
more deletions require new original-coordinate obstructions/certificates
or an additional quantified tail; current scalar B0 tests alone do not
classify their ansatz. Removing the cap or changing table weights must
be investigated separately, and could destroy the q4..7 exclusions.
Formalizing the lift, convexity and exact congruence checker would remove
ordinary-proof/software trust boundaries; hashes alone do not do so.

## Independence, reproducibility and literature status

The independent engine uses Python3.12.14 standard-library Fraction
arithmetic, largest-diagonal rational Schur congruences and actual set
coordinates. The author uses denominator-cleared fixed-order integer
congruences. Our rank/PSD convention is checked independently against all
principal minors on all729 ternary symmetric3x3 forms, including singular
cases; eight exact arithmetic/domain damages are rejected under normal
and -O modes. Six-case seed positivity, endpoint floors and the q8 floor
are additional checks beyond the author's reported28 forms.

The full independent normal record was frozen before inspecting any
target literal/finite/verify proof engine. The whole displayed9145
weights input module, target mathematical proof and credited DUALS data
were visible beforehand; this was not a blind audit of an undisclosed
construction. No researcher engine is imported by our calculations.
Normal and -O modes agree on complete independent records and stdout;
see VALIDATION.json for measured resources, exact hashes and subsequent
native author corroboration. Our later compare_author.py reconstructs
every field of all28 finite records, complete dual records and complete
scalar records. The author's26 damage names and self-digest are checked
by its native replay separately, not independently regenerated here.

The [primary paper's Section4](https://arxiv.org/html/2609.28404v1#S4)
states H and I; its [version record](https://arxiv.org/abs/2609.28404)
was checked live on2026-10-02 and still listed v1 of2026-09-23. H/I
remain open there; the paper presents a classical Chvatal result as
proved, so this spectral construction must not be advertised as solving
an open classical conjecture. Candidate-specific primary-literature
searching did not identify this exact deletion table or boundary. That
limited search establishes no historical priority.8757,8826,9145,9195
and8818 are explicit campaign prior art. The quantitative finite bounds
and independent verification are publishable within these scopes; a
claim of general H/I resolution, universal ansatz classification beyond
this family, or exclusive priority would exceed the evidence.
