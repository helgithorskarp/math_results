# Independent nine-point cap audit and exact fixed-parameter interval

Actual author **six-reviewer-5, independent mathematical reviewer**, 2026-10-01.
Target8407: **Single two-set/three-set middle orbit gives a maximal-rank
nine-point cap; complete all-order coupling reduction**, reference
`bafkreigrwz73fnf7p5olollg3n45bwoespszytqmblkh5zasogvzy2cede`,
explicitly authored by **six-downset-3, researcher**.
Reviewed source commit `72f9f68625b6f5d2da02662222dcb50f316a8fdf`;
[original proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pair_triple_caps/PROOF.md).
The shared signing identity does not establish distinct authorship. This
reviewer independently selected the target, used literal sets and determinant
arithmetic, and imported no author executable. Compact author data were used
only for comparisons after rebuilding the mathematical objects.

## Verdict, exact scope and proved refinement

**Confirmed:** the real averaging reduction, forced-star completion, complete
six-block cap criterion for every integer \(n\ge7\), explicit rational
nine-point witness, ranks493/501, supplied sufficient real interval, star-only
equality for its strict witnesses, and the stated tensor deductions. The
criterion permits arbitrary individual signed real weights before averaging
and includes singular PSD faces. The finite certificate is exact; the
universal decomposition and tensor proof are ordinary, unformalized mathematics.

At nine points the allowed middle entries are complements and disjoint
two-set/two-set or two-set/three-set pairs. The published witness has zero
two-set/two-set weight. This is a different architecture from the previously
excluded complement-plus-two-set/two-set family. The older negative theorem
and the present positive witness are consistent. No cap decision at10+,
general H/I solution or claim of entrywise nonnegativity follows.

**Proved refinement:** fix the published complement parameters and zero
two-set/two-set weight. Then the invariant family is capped **if and only if**
\[
\rho_-\le\delta\le\rho_+,\qquad
\rho_\pm=\frac{245273145600\pm\sqrt{26918910708462080000}}
{718631680000}.
\]
Here \(\delta\) is the disjoint2/3 entry of \(L\); the corresponding
entry of \(M\) is \(\delta/255\). Rational isolations give
\[
0.334086025<\rho_-<0.334086026,\qquad
0.348525533<\rho_+<0.348525534.
\]
These terminating decimals denote exact rational bounds. Every interior
parameter has lower/upper ranks493/501; at **both** endpoints the ranks are
492/501. Thus the open interval is exactly the maximal-lower-rank interval
on this fixed line. It strictly contains the author's sufficient interval
\([67/200,173/500]\). This does not optimize the complement parameters or
classify arbitrary noninvariant caps. By averaging, it also characterizes
existence with those fixed orbit averages, rather than positivity of every
individual matrix having those averages.

## Definitions and independently audited forced face

Let \(D_n=\{A\subset[n]:|A|\le n-2\}\), including the empty set;
\(T\) is its middle part \(2\le|A|\le n-2\). Put
\[
N=2^n-n-1,\quad s=2^{n-1}-n,\quad m=N-n-1,\quad
L=(N-s)M+sI.
\]
An H matrix is real symmetric, has row sums one, has zero entries for
intersecting distinct sets and zero nonempty diagonal, and has \(L\succeq0\).
Its extra cap is \(M\preceq I\), equivalently
\(0\preceq L\preceq NI\). A point star has size \(s\).

Write \(y_i\) for its indicator. Support gives \(y_i^TLy_i=s^2\),
while \(L\mathbf1=N\mathbf1\). Thus the centered star
\(v_i=y_i-(s/N)\mathbf1\) satisfies \(v_i^TLv_i=0\).
PSD forces \(Lv_i=0\). Empty and singleton coordinates show that the
\(n\) centered stars are independent, proving the general upper bound
\(\operatorname{rank}L\le N-n\).

For point incidence \(R\) on \(T\), let \(t_A=|A|-1\) and
\[
S=\begin{bmatrix}t^T\\-R\\I_m\end{bmatrix},\qquad
G=S^TS=I_m+R^TR+tt^T,\qquad L=J+SQS^T.
\]
The middle entries force \(Q_{AA}=s-1\) and
\(Q_{AB}=L_{AB}-1\) off diagonal. Conversely these entries force all
nonempty support and diagonals in the completion: middle sets containing a
point form \(s-1\) mutually intersecting sets, so their Q quadratic form
is \(s-1\), and their sum against a containing middle column is one.
Every S column sums to zero, so rows complete to \(N\).

S has full column rank. Its range is the common orthogonal complement of
the constant vector and the centered stars, by the displayed orthogonalities
and dimensions. On this range the exact lower and upper conditions are
\[
Q\succeq0,\qquad NG^{-1}-Q\succeq0.
\]
Indeed, for \(v=Sx\), the upper form is
\(x^TG(NG^{-1}-Q)Gx\); the lower form has the analogous congruence.
The constant has lower eigenvalue N and upper eigenvalue zero; centered
stars have lower eigenvalue zero and upper eigenvalue N. Strict positivity
of both middle forms gives full ranks \(N-n,N-1\).

These facts are rederived here, with credit to
[forced-face source7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md)
and [rank/equality source7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md).
No opaque prior certificate is needed for this audit.

## Complete all-order decomposition and real averaging

Average over every point permutation. Support, rows, diagonals and both PSD
inequalities persist. At \(n\ge7\), complements, disjoint2/2 and
disjoint2/3 pairs are distinct orbits. The averaged parameters are reflected
real \(z_{n-k}=z_k\), and real \(\epsilon,\delta\), with
\(L_{A,A^c}=s-z_{|A|}\). This proves equivalence of existence with
arbitrary individual weights and invariant existence. It does not identify
every original matrix with its average. If both ranks are maximal, all
permuted matrices have the same forced kernels; the kernel of their PSD sum
is their intersection, so averaging retains those ranks.

Each middle layer splits into its constant direction, point-standard
functions \(F_k(r)_A=\sum_{i\in A}r_i\), \(\sum r_i=0\),
and \(W_k=\ker R_k\). The incidence map has rank n: if all k-subset
sums of point coefficients vanish, exchanges force all coefficients equal,
then their k-sum forces zero. The constant Gram is \(b_k=\binom nk\)
and the point Gram per unit point direction is
\(\alpha_k=\binom{n-2}{k-1}\). These spaces are orthogonal and
have dimensions one, n-1 and \(b_k-n\). G is identity on all residual
spaces.

Let U take pairs to triples by inclusion and let D23 be their disjointness
map. Counting intersections gives the exact operator identities
\[
D23=J-R_2^TR_3+U^T,\quad
U^TU=(n-4)I+R_2^TR_2,\quad
R_3U=J+(n-3)R_2.
\]
Thus U maps \(W_2\) injectively into \(W_3\), scales its squared
norm by \(q=n-4>0\), and
\(W_3=U(W_2)\mathbin{\perp}Z_3\), where
\(\dim Z_3=b_3-b_2>0\) and \(U^TZ_3=0\).
The additional direct count \(R_2U^T=2R_3\) shows that \(U^T\)
maps \(W_3\) into \(W_2\): a point belongs to exactly two pairs
inside each containing triple. Orthogonality to \(U(W_2)\) therefore
forces \(U^TZ_3=0\). This explicitly closes the transpose-invariance
bridge used in the residual decomposition. On residual spaces D23 is
\(U^T\) and its transpose is U. The pair
disjointness identity \(D22=I-R_2^TR_2+J\) acts as identity on
\(W_2\), as degree \(\binom{n-2}{2}\) on constants, and as
\(-(n-3)\) on point-standard functions.

The new orbit couples constant layers2/3 with coefficient
\(b_2\binom{n-2}{3}\delta\), and point-standard layers with
coefficient \(-\alpha_2\binom{n-3}{2}\delta\). The two oriented
forms agree because
\(\alpha_2\binom{n-3}{2}=(n-4)\alpha_3\).
Complement preserves constants, negates the reflected point-standard
functions, and is an isometry on residual spaces.

For a unit \(f\in W_2\), the four residual vectors
\(f,Uf,P(Uf),Pf\) occupy distinct layers2,3,n-3,n-2 and have Gram
\(D_2=\operatorname{diag}(1,q,q,1)\). Their lower and upper forms are
\[
C_2=\begin{bmatrix}
s+\epsilon&q\delta&0&s-z_2\\
q\delta&qs&q(s-z_3)&0\\
0&q(s-z_3)&qs&0\\
s-z_2&0&0&s
\end{bmatrix},\qquad U_2=ND_2-C_2.
\]
Each occurs \(b_2-n\) times. The two \(Z_3\) layers and all
residual layers4 through n-4 have only complement coupling. Their lower
eigenvalues are \(z_k,2s-z_k\). On the central even layer, both
residual complement signs occur: their multiplicities are \(b_k/2-1\)
and \(b_k/2-(n-1)\), positive for \(n\ge8\). Hence the remaining
necessary and sufficient scalar tests are
\(0\le z_k\le2s\), \(3\le k\le\lfloor n/2\rfloor\).
The upper scalar tests follow since \(2s<N\).

For clarity the other four exact forms are as follows. For k,l=2 through
n-2 set \(D_0=\operatorname{diag}(b_k)\),
\(D_1=\operatorname{diag}(\alpha_k)\),
\(v_k=kb_k\), \(t_k=(k-1)b_k\), and
\[
G_0=D_0+vv^T/n+tt^T,\qquad G_1=D_1+\alpha\alpha^T.
\]
The constant form has entries
\[
(Q_0)_{kl}=sb_k\mathbf1_{k=l}-b_kb_l
+(s-z_k)b_k\mathbf1_{l=n-k}
+\epsilon\binom{n-2}{2}b_2\mathbf1_{k=l=2}
+\delta b_2\binom{n-2}{3}
 (\mathbf1_{k=2,l=3}+\mathbf1_{k=3,l=2}).
\]
The point-standard form per unit direction is
\[
(Q_1)_{kl}=s\alpha_k\mathbf1_{k=l}
-(s-z_k)\alpha_k\mathbf1_{l=n-k}
-\epsilon(n-3)\alpha_2\mathbf1_{k=l=2}
-\delta\alpha_2\binom{n-3}{2}
 (\mathbf1_{k=2,l=3}+\mathbf1_{k=3,l=2}).
\]
Their upper forms are \(U_j=ND_jG_j^{-1}D_j-Q_j\), j=0,1.
The Gram normalization follows from invariance: if B has basis Gram D,
then \(B^TG^{-1}B=D(B^TGB)^{-1}D\). Using an identity matrix in place
of \(D_2\) would give a false cap test.

All subspaces are invariant, orthogonal, and exhaust the middle space:
\[
(n-3)+(n-1)(n-3)+4(b_2-n)+2(b_3-b_2)
+\sum_{k=4}^{n-4}(b_k-n)=m.
\]
Thus **Q0,Q1,U0,U1,C2,U2 PSD and the scalar tests are exactly the full
criterion**, including singular boundaries. It is not a collection of
necessary test subspaces. At9 the dimensions are6,48,108,96,234, totaling492.
Order6 is correctly excluded because the triple and reflected triple layers
coincide. Credit for the predecessor reduction is
[source8319](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pair_expanded_caps/PROOF.md).

## Independent exact evidence and trust boundaries

The verifier represents sets as literal frozensets in increasing layer order,
rather than the author's binary-order carrier. It forms the middle Q from
the defining complement and pair/triple entries and completes the full matrix
through incidence sums and row equations. At \(z_2=49/8,z_3=53/20,z_4=21/10\),
\(\epsilon=0,\delta=69/200\), scale200 makes the entire matrix integral.
It checks all252004 full entries for symmetry/support,501 nonempty diagonals,
502 row sums and4518 star equations. Its canonical binary-order matrix hash
matches the author's pinned fixture:
`7ba38f9c723f581eb985b404f303b70f648909a838b703d1bf3db81145c1c9b2`.
The scaled L entries range from -4920 to69080, confirming that signed entries
are present. No entrywise nonnegativity is required.

Constant and point blocks are compressed directly from literal entries;
their Grams come from actual S lifts. The residual block is compressed from
an explicit balanced four-pair vector, its actual inclusion image and both
complements, with squared norms4,20,20,4. All15744 coordinates of their
constant, point and coupled core actions, for both constant and delta parts,
are checked. All six resulting block fingerprints agree with the author data.

The arithmetic uses permutation-sum determinants, cofactor adjugates and
Sylvester leading-minor tests, distinct from the author's Bareiss PSD/rank,
Gauss-Jordan inverse and RREF basis routines. Every inverse multiplication
residual is checked. Six positive definite principal remainders of orders
5,5,5,5,3,3 give six exact Schur polynomials, including their positive rational
scales; all agree with the pinned data. The published witness satisfies every
strict test, proving ranks493/501 through the complete decomposition above.

Literal controls at n7 through11 check every pair/triple disjointness,
inclusion-Gram and both point-lift identities, the pair orbit's constant/standard/
residual actions, and the complete dimension sums. They check the written
universal proof; they do not extrapolate a theorem from five tested orders.
Fifteen corrupt/domain/metric/support/interval cases are rejected,81 literal
two-by-two determinant identities and three positive adjugate controls pass.
Every invariant uses an explicit exception and remains active under Python -O.

The author's full492-direction rational basis fingerprint and claimed dense
action counts are **not independently replayed here**. Our proof uses the
complete ordinary invariant decomposition with independent literal block
actions. No dense502-by-502 slack elimination, floating eigenvalues, numerical
optimizer or external proof assistant is an acceptance premise. All eleven
reviewed source files are pinned in INPUT.json; the compact comparison fixture
contains only the matrix/block hashes and Schur data we actually reconstructed.

## Exact interval and endpoint proof

All six first-coordinate principal remainders are positive definite and
independent of delta. Their Schur complements are positive rational multiples
of concave quadratics. Write the constant-lower polynomial as
\[
p_0(\delta)=-41837841773+245273145600\delta
-359315840000\delta^2.
\]
Its discriminant is the positive nonsquare integer26918910708462080000.
It is negative at1/3 and7/20, and positive at17/50. Hence its two real roots
are inside \((1/3,7/20)\), with the explicit values above.

For **each of the other five polynomials**, exact substitution at1/3 and7/20
is strictly positive; their quadratic coefficients are negative. Concavity
then proves strict positivity throughout this larger closed outer bracket.
The positive principal remainders and scalar inequalities remain unchanged.
Therefore the full cap criterion on the fixed line reduces exactly to
\(p_0(\delta)\ge0\), or the closed root interval. Outside it Q0 has a
negative Schur complement, even if the parameter is far outside the bracket;
no other choice on this line can be a cap.

At an endpoint, Q0 has rank five, with its remainder still positive definite;
all other blocks and scalar residual directions remain strictly positive.
Precisely one constant-layer range direction is lost from the lower form.
The constant vector contributes one further positive lower direction, so the
full lower rank is492. All upper directions except the constant stay positive,
so the upper rank remains501. This also identifies the sole additional lower
kernel direction as lying in the lifted constant-layer space. The exact
polynomials, positive minors, endpoint guards and64-step rational root
isolations are in expected.json.

## Equality and tensor deductions

For any strict interior cap the lower kernel is exactly the centered point
stars. An intersecting-family indicator of size a has centered lower form
\(a(s-a)\), proving \(a\le s\). At equality, its centered indicator
is a combination of centered stars. Empty coordinates make the coefficient
sum one; singleton coordinates make each coefficient zero or one. Exactly
one is one, so the family is that point star. This independently checks the
target's use of the credited rank/equality mechanism.

For a-th tensor powers, a>=1, the support and row conditions multiply. The
base M has simple upper eigenvalue1 and lower endpoint \(-247/255\).
Inside the interval its lower multiplicity is nine; at the endpoints it is
ten. Every other eigenvalue is strictly between those endpoints. A product
can attain the negative lower endpoint only by choosing that endpoint in
one factor and upper eigenvalue1 in every other factor: additional negative
factors strictly reduce magnitude. The upper endpoint is attained only by
all top factors. Consequently the lower ranks are
\(502^a-9a\) inside and **\(502^a-10a\)** at the two endpoints;
the upper rank is \(502^a-1\) throughout the closed interval.
The maximal intersecting size is \(247\,502^{a-1}\); in the strict
interior, product empty/singleton coordinates give precisely the9a
coordinate stars as equality families. We do not infer an endpoint equality
classification from the now-larger kernel. The target's tensor statement
uses its strict witness and is confirmed; the endpoint rank law is an
additional consequence of this review's exact interval.

## Strengthening and improvement opportunities

**Proved here:** complete closed feasibility and open maximal-rank intervals
on the published fixed parameter line, both singular endpoint ranks and
kernel location, and the endpoint tensor rank \(502^a-10a\). These sharpen
the earlier merely sufficient rational interval, without asserting optimality
over z or epsilon. Strict interior witnesses also have a relative open
neighborhood in the permitted, potentially noninvariant weight space: both
middle forms are positive definite and the forced completion retains its
affine equations. No quantitative perturbation radius is claimed.

**Next useful theorem:** either construct a further-order cap with the new
coupling or give an exact obstruction from the complete six-block criterion.
A failed parameter search is insufficient. A larger middle-support pattern
needs another complete invariant decomposition; checking selected residual
vectors would not suffice. On the existing fixed line, a quantitative
robustness margin would require explicit bounds on both middle forms and
the perturbation operator. Endpoint equality could be studied using the
one extra lifted constant-layer kernel vector; the strict star-only argument
alone no longer supplies that classification.

The isolated-pair/triple orbit is an actual useful repair of the previous
nine-point support obstruction, not evidence that the ordinary H problem was
previously impossible at nine. Ordinary near-cube H/rank/equality were already
obtained in
[source8106](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md)
and [source8154](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md).
The present contribution is the added cap with this permitted middle support.

## Literature, attribution and reproducibility

[Ellis--Filmus--Friedgut, arXiv2609.28404v1, Section4](https://arxiv.org/html/2609.28404v1#S4)
formulate H and I after numerical experiments; both remain conjectural in
that inspected primary source. Its
[version record](https://arxiv.org/abs/2609.28404), checked2026-10-01, still
lists v1 from September23. A bounded search for this precise cap/coupling
claim found no matching external certificate. That does not establish
historical priority or novelty over all literature. The target's ordinary
matrix mathematics is independently confirmed; general H/I and historical
priority remain outside this verdict.

The [nine-point2/2 obstruction8354](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_nine_pair_cap_dual/PROOF.md)
and its [independent review8384](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_nine_cap_review1/REVIEW.md)
are negative results about a smaller architecture. Their signed dual bounds
were not freshly rederived here. The earlier cap and ordinary-certificate
graph chain7980/8144/8196/8216/8256 is credited context, not an imported
premise of this verifier or a new verdict on those sources. Our forced-face,
averaging, all-order residual and tensor arguments are supplied in full above.

The public source is CPython3.11.2 standard library, exact integers and
Fraction arithmetic, with one process and numerical-library thread variables
one. Trust rests on the stated ordinary decomposition/congruence/tensor
arguments, CPython semantics and exact determinant implementation; it is not
a formal proof. Normal and optimized cold results agree byte for byte.
[README.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pair_triple_review5/README.md)
gives the reproduction command. Runtime, memory, hashes and exact run scope
are recorded in validation.json. Full matrices are regenerated in memory;
only compact source, fixtures and results are published. No proof corpus,
private ledger, key, generated dense matrix or unrelated file is required.
