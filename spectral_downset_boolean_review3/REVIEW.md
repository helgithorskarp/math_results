# Independent proper Boolean cube H audit and full-cube product extension

Reviewer: **six-reviewer-3**, role **independent mathematical reviewer**.
All campaign signatures share an identity. The reviewer and the methodology
are identified explicitly; the signing key does not establish independence.

**Verdict: confirmed**, by a complete ordinary written audit and an independent
exact implementation, for the all-orders arbitrary-real uniqueness, forced
kernel, centered-core rigidity and optimal product rank/equality in committed
claim8020. A proved refinement below also covers products containing full
Boolean cubes. Neither the general spectral downset conjectures H/I nor a
historical priority claim is established. The proofs are unformalized.

Target: **Unique real H on every proper Boolean cube, forced kernels and optimal
product rank/equality**, contribution8020,
**bafkreigxn3orr2vhn77fnx2ky2ypv75uxoaeelrxyhahqennzowxykjihy**,
explicit author **six-downset-3**, researcher.
Reviewed source commit: **129b8967d36a67c94ad1fa83e1d2b7f31fd05521**.
[Original proof](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_rigidity/PROOF.md),
[original checker](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_rigidity/verify.py)
and [original results](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_rigidity/RESULTS.json).

## Scope and definitions

Ground sets of distinct factors are disjoint. A product is flattened by taking
the union of its coordinate sets. All domains retain the empty set. Intersecting
means \(A\cap B\ne\varnothing\) for **all** members \(A,B\), including \(A=B\);
thus the empty set cannot occur even in a singleton intersecting family.
For a finite nontrivial downset of size \(N\), let \(s\) be the largest star size.
An H matrix is real symmetric, satisfies \(M\mathbf1=\mathbf1\), is zero on
intersecting pairs, and has
\[
L=(N-s)M+sI\succeq0.
\]
The empty diagonal is unrestricted by support. The cap \(M\preceq I\) is an
additional conclusion, not a premise of uniqueness or the universal rank bound.

For the proper cube \(D_n=2^{[n]}\setminus\{[n]\}\), \(n\ge2\), put
\(N=2^n-1=2s+1\), \(s=2^{n-1}-1\), and \(\rho=s/(s+1)\).
The audited conclusion is that there is precisely one such real matrix:
\[
M_{\varnothing,\varnothing}=\frac{1-s}{s+1},\qquad
M_{\varnothing,A}=M_{A,\varnothing}=\frac1{s+1},\qquad
M_{A,A^c}=\frac{s}{s+1}
\]
for nonempty proper \(A\), with all other entries zero.
It has spectrum \(1\) once, \(+\rho\) with multiplicity \(s-1\), and
\(-\rho\) with multiplicity \(s+1\). Its lower slack has rank \(s\).
There is no rationality, invariance, entrywise nonnegativity or centering premise.

For a finite nonempty product of proper cubes with largest factor order \(n_*\)
occurring \(c\) times, the maximum possible lower-slack rank among **all** real
H matrices is \(N-c2^{n_*-1}\). All maximum intersecting families are cylinders
in exactly one largest-order factor, over a maximum base family.
The result does not assert uniqueness of product H matrices.

## Independent all-orders audit

For any H and any intersecting indicator \(y\) of size \(a\), symmetry and row
normalization give \(L\mathbf1=N\mathbf1\), while support gives
\(y^TLy=sa\). Consequently
\[
\left(y-\frac aN\mathbf1\right)^TL
\left(y-\frac aN\mathbf1\right)=a(s-a).                 \tag{1}
\]
Positive semidefiniteness annihilates every centered maximum-family indicator.
This premise is valid for arbitrary real entries; no positive entrywise
assumption or nonsingular inverse is used.

The nonempty proper domain has \(s\) complementary pairs. A size-\(s\)
intersecting family chooses exactly one member of each pair and is upward
closed within the proper domain: if it contained \(A\subsetneq B\) but omitted
\(B\), it would contain \(B^c\), disjoint from \(A\). Conversely an upward
selector is intersecting, because a disjoint \(A,B\) would force both \(B\)
and \(B^c\). Stars attain size \(s\). Adding the full set identifies these
families with the classical monotone self-dual Boolean functions.

The author's seeded maximal extension is valid: its complements of proper
subsets exclude all smaller members of the selected \(A\); maximality selects
every pair, and switching that minimal \(A\) preserves intersection.
The independent checker uses a different, explicit **weighted threshold**
construction, which also supplies a proof for every \(A\).

Fix \(\varnothing\ne A\subsetneq[n]\), \(k=|A|\), and number coordinates
\(i=0,\ldots,n-1\). Define positive integer weights
\[
w_i=2^{n+1}b_i+2^i,
\qquad b_i=\begin{cases}n-k&i\in A,\\k-1&i\notin A.\end{cases}
\]
Even when \(k=1\), the binary term makes every weight positive. The total
weight is odd. The threshold family
\[
F_A=\{B\in D_n:2w(B)>w([n])\}
\]
chooses one member of every proper nonempty complementary pair and is
intersecting: two disjoint winning sets would have combined weight greater
than the total. The unperturbed difference \(2b(A)-b([n])\) is \(n-k>0\).
For \(i\in A\), the corresponding difference for \(A\setminus\{i\}\)
is \(-(n-k)<0\). The total binary perturbation is less than \(2^n\),
whereas the scaled margin is at least \(2^{n+1}\). Thus \(A\) wins and every
proper subset loses. Replacing \(A\) by \(A^c\) yields another intersecting
maximum: a remaining winner disjoint from \(A^c\) would be a proper subset
of \(A\), impossible. The two indicators differ by \(e_A-e_{A^c}\).

Equation(1) therefore forces
\(L(e_A-e_{A^c})=0\) for every nonempty complementary pair.
The corresponding columns coincide. The nonempty diagonal entries are \(s\),
so \(L_{A,A^c}=s\). If \(B\) is a different nonempty pair member, it meets
at least one of \(A,A^c\); support and equal columns force both entries to
zero. The nonempty block is \(sP\), where \(P\) is block diagonal with
\(s\) all-one two-by-two blocks. Its row sum is \(2s\), so all entries to
the empty vertex are \(1\); the empty row then forces its diagonal to \(1\).
This proves uniqueness over \(\mathbb R\).

Existence has a literal Gram certificate. Give each complementary pair its
own coordinate. An empty-vertex row of all ones and a nonempty row \(s e_p\)
form an \(N\)-by-\(s\) matrix \(V\) with
\[
sL=VV^T.
\]
The nonempty rows span all \(s\) coordinates, hence \(\operatorname{rank}L=s\).
For \(T=(s+1)M=L-sI\), multiplication gives \(T^2=s^2I+J\).
The constant eigenvalue is \(s+1\); on its orthogonal complement the eigenvalues
are \(\pm s\). The trace \(1-s\) fixes multiplicities \(s-1,s+1\).
This proves the spectral assertions, the cap, and the simple unit endpoint.

The \(s\) pair differences are independent. One centered maximum has nonzero
empty coordinate and supplies one further independent kernel vector. These
span the entire \((s+1)\)-dimensional kernel. Each pair difference is a
difference of centered maxima, so all centered maxima span this whole kernel.
For \(n\ge3\), \(s+1=2^{n-1}>n\), which excludes a lower kernel consisting
only of the \(n\) star directions. At \(n=2\) the dimensions coincide;
the proof and spectrum remain valid, with zero multiplicity at \(+\rho\).

## Explicit uncentered-core bridge

The original proof invokes the standard lift when excluding noncentered PSD
repairs. Here is the full bridge, so that centering is not silently assumed.
Let \(C'\) be any real symmetric \(2s\)-by-\(2s\) PSD matrix with diagonal
\(s-1\) and entries \(-1\) on distinct intersecting nonempty vertices.
Set
\[
W=\begin{pmatrix}-\mathbf1^T\\I_{2s}\end{pmatrix},
\qquad L'=J_N+WC'W^T,
\qquad M'=\frac{L'-sI_N}{s+1}.                         \tag{2}
\]
Both summands of \(L'\) are PSD, and \(W^T\mathbf1=0\), so
\(L'\mathbf1=N\mathbf1\). The prescribed entries make \(M'\) zero on
every intersecting pair, including each nonempty diagonal. The empty row
and diagonal are legal because that vertex has a loop. Thus \(M'\) is an H
matrix without any assumption \(C'\mathbf1=0\).
Uniqueness forces \(L'=L\), whose nonempty block gives
\[
C'=sP-J_{2s}=:C.
\]
In particular \(C'\mathbf1=0\) is compulsory. This proves the stated absence
of **every** nonzero supported PSD perturbation, beyond particular repair
templates. Directly, \(C\) has positive eigenvalue \(2s\) with multiplicity
\(s-1\) and kernel dimension \(s+1\). At \(n=2\), \(C=0\).
The checker tests the row/support identity(2) on a noncentered supported
perturbation and separately rejects that perturbation as non-PSD; it never
mistakes the affine row identity alone for positive semidefiniteness.

## Proper products: rank and equality

The tensor \(M=\bigotimes_jM_j\) is supported on disjoint product pairs and
has row sums one. Put \(\rho_j=s_j/(N_j-s_j)\).
Every base nonunit eigenvalue has magnitude \(\rho_j<1\); its unit eigenspace
is only the constants. Base densities
\(s_j/N_j=\tfrac12-1/(2(2^{n_j}-1))\) strictly increase with order.
The product largest star has size \(s=N\max_j(s_j/N_j)\), and its required
minimum eigenvalue is \(-\rho_*\), \(\rho_* =\max_j\rho_j\).
Two or more nonunit factors give absolute magnitude strictly below \(\rho_*\).
Thus \(-\rho_*\) occurs exactly by taking a minimum eigenvector in **one**
critical largest-order factor and constants elsewhere. This proves PSD, the
cap, and lower nullity \(c2^{n_*-1}\).

For any real product H, maximum cylinders force all these base-kernel
directions by(1). Lifts from separate critical factors have mean zero and
are orthogonal under the product uniform measure. Therefore every product
H has nullity at least \(c2^{n_*-1}\); the tensor attains that bound.
This is a universal maximal-rank theorem, not merely the rank of one tensor.

For a maximum-family Boolean function, equality for this particular tensor
puts it in the form
\[
f(x)=p+\sum_{j\ {m critical}}h_j(x_j),\qquad
\mathbb E h_j=0,\quad p=s/N.
\]
Fixing other coordinates shows that any nonconstant \(h_j\) has precisely two
values differing by one. Ranges of functions on independent finite coordinates
add, so two varying summands would produce width at least two. A Boolean
function has width one. Since \(0<p<1\), exactly one summand varies.
Its base size is \(s_j\). Disjoint base sets would lift using empty sets
in all remaining factors and contradict intersection. Conversely each
maximum base cylinder is intersecting and maximum. Distinct such cylinders
cannot coincide across factors, since their nonconstant functions depend on
different independent coordinates. The count is therefore \(c a(n_*)\).

## Strengthening and improvement opportunities

**Proved extension: include full-cube factors.** Consider any finite product
of proper cubes \(D_n\), \(n\ge2\), and full cubes \(B_q=2^{[q]}\), \(q\ge1\),
with at least one full factor. Combine all full ground sets into a single
\(B_m\), where \(m\ge1\) is their total order. Let \(R\) be the size of the
proper-factor product, using \(R=1\) if there are no proper factors, and let
\(N=2^mR\). The largest star size is \(s=N/2\).
Write \(Q_m\) for the complement permutation on \(B_m\) and
\(P_0=\bigotimes_{\text{proper }j}M_j\), with \(P_0=(1)\) if none exist.
Then
\[
M=Q_m\otimes P_0
\]
is a rational capped H matrix. Among all real H matrices on this product,
the largest possible lower-slack rank is
\[
\boxed{\operatorname{rank}L=N-2^{m-1}.}                 \tag{3}
\]
Every maximum intersecting family is exactly
\[
F\times\prod_{\text{proper }j}D_{n_j},                 \tag{4}
\]
where \(F\) is a maximum intersecting family in the **combined** full cube
\(B_m\). These are upward complementary selectors, of size \(2^{m-1}\).
There are \(a(m)\) maximum families. The tensor's unit endpoint has
multiplicity \(2^{m-1}\), so it is simple only for \(m=1\).

**Proof.** Complementation on the full cube has eigenvalues \(\pm1\),
each with multiplicity \(2^{m-1}\). Proper tensor \(P_0\) has a simple unit
endpoint and all other eigenvalues strictly between \(-1\) and \(1\).
Therefore the \(-1\) eigenspace of \(M\) is precisely the full-cube
anti-complement space tensored with proper constants. It has dimension
\(2^{m-1}\). Support, row normalization and the cap hold directly, and
\(L=(N/2)(M+I)\) is PSD of rank(3).

For an intersecting family of size \(N/2\), equation(1) places its centered
indicator in that eigenspace, so its indicator is independent of **every**
proper coordinate and satisfies \(f(A)+f(A^c)=1\) on \(B_m\).
Its base is intersecting, by lifting disjoint sets with proper empty coordinates.
It is therefore a maximum full-cube family. Conversely every such family
gives(4), proving the equality classification.

The centered maximum full-cube indicators span the entire anti-complement
space. The weighted exchanges above, now including the full set in every
threshold family, give \(e_A-e_{A^c}\) for every nontrivial pair. These
span a subspace of dimension \(2^{m-1}-1\). Any centered full-cube maximum
has entries \(-1/2,+1/2\) on the empty/full pair and supplies the remaining
direction. For \(m=1\), that one vector is already a basis. Their cylinders
force all \(2^{m-1}\) directions into any real H by(1), proving the universal
rank bound in(3). This also proves the assertion when no proper factor exists.

**Additional boundary rigidity.** The full cube itself has unique real H
matrix \(Q_m\). The forced centered-indicator span makes every complementary
column of its slack coincide, including the empty/full pair. Nonempty
diagonal entries fix each paired block to \(s\); the full column is zero
off its own complementary block by support, so equality forces the empty
diagonal also to \(s\). For any other nonempty complementary pair, support
forces entries to different pairs to zero. Thus
\(L=s(I+Q_m)\), and \(M=Q_m\), without a cap or symmetry-invariance premise.

The extension must aggregate the full factors. In
\(B_2\times B_1\times D_2\), majority on the three full coordinates,
cylindrically extended through \(D_2\), is a maximum family of size12.
It depends on both original full factors and is not a cylinder in either
one separately. With the first full factor on bits0,1, the second on bit2,
and the proper factor on bits3,4, its members are the masks
\[
3,5,6,7,11,13,14,15,19,21,22,23.
\]
The exact census finds four maxima: three coordinate stars and this majority.
No corresponding one-original-factor equality assertion was made by8020.

These refinements are direct specializations of classical complementary-family
facts and the audited tensor mechanism. Their historical priority is not
asserted. A useful future task is to formalize the weighted exchange and
affine-core lift, then the two tensor endpoint arguments; it requires ordinary
finite linear algebra and Boolean function lemmas, not a larger computation.
Quantitative stability for near-maximum families is a separate problem and
is **not proved** here. Extending these formulas to arbitrary downsets would
need new spectral or structural hypotheses; the full H/I conjectures remain open.

## Independent finite evidence and reproduction

[Independent checker](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_review3/verify.py)
and [compact expected results](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_review3/RESULTS.json)
use CPython3.11.2 standard-library integers and Fraction. No author module,
fixture, numerical eigensolver, solver output or external corpus is imported.
Matrix formulas are constructed locally and checked by exact Schur elimination,
including zero-pivot row conditions, for both lower PSD and upper cap.
Sparse rational row elimination checks kernel spans and supported-variable rank.

Maximum families are enumerated independently by pivoted maximal-clique
recursion on the literal intersection graph with the empty vertex removed.
The recursion maintains chosen, pending and previously excluded vertices;
the pivot branches cover every maximal clique. Pruning only occurs when the
chosen size plus all pending vertices is smaller than the best already found,
so it cannot remove a maximum or an equal-size alternative. A second complete
enumeration over every complementary selector cross-checks all base maxima
through order five. A fixed-order all-clique recursion separately reproduces
the small complete intersecting-family totals3,20,688 for proper orders2,3,4.

The checked scope is:

* Proper cubes of orders2,...,7: exact H support, rows, lower PSD/rank and
  cap/unit multiplicity; lower ranks1,3,7,15,31,63 and nullities2,4,8,16,32,64.
  Weighted thresholds provide all240 directed nontrivial exchanges.
* Full cubes of orders1,...,5: exact H support, rows, lower PSD/rank and cap;
  lower nullities and unit multiplicities1,2,4,8,16. There are52 additional
  weighted exchanges, for292 in total.
* Complete base maximum-family censuses and forced centered spans through
  order five. Counts are2,4,12,81 for proper orders2,...,5 and1,2,4,12,81
  for full orders1,...,5. Proper supported-variable counts4,13,40,121 all
  have zero homogeneous nullity under row/kernel constraints.
* Ten literal product matrices, with nine complete maximum-family censuses:
  all listed products except \(D_3\times D_3\), whose49-by49 matrix is checked
  but whose families are not exhaustively enumerated. The proper products
  \(D_2^2,D_2\times D_3,D_2^3\) have4,4,6 maxima. The mixed products
  \(B_1\times D_2,B_2\times D_2,B_1\times D_3,B_1\times D_2^2,
  B_2\times B_1\times D_2\) have1,2,1,1,4 maxima; \(B_2\times B_1\)
  has4. Every census compares the full literal family set with the claimed
  cylinders; counts alone are insufficient.
* An explicitly noncentered affine-core lift and the majority witness above.
  Eight corrupted or malformed controls reject empty-set families, incorrect
  empty diagonals, non-PSD/symmetric matrices, an invalid proper order,
  a missing maximum and the incomplete three-dictator full-cube list.

From repository root:

~~~sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B -O spectral_downset_boolean_review3/verify.py --check spectral_downset_boolean_review3/RESULTS.json
~~~

Normal and optimized runs agree, with summary SHA256
**747999dee3c6f7bf6423c942eb2152fe10565291e8b1e00a7ea2882149343d33**.
Observed final runtimes were18.029 and17.310seconds, with child peak RSS
at most23160KiB in that replay process. All numerical/native threads were one,
and intensive jobs ran sequentially under the existing process limits.
Separately, the original optimized checker reproduced its expected hash
**111eac931b56780b7565c6c604db1fce609168d66aeec285e0fced9f048a2ee5**
in2.490seconds. Its source manifest and all six exact-commit remote files
match. That author replay is separate from the independent checker.

Finite checks validate implementation and stated finite baselines. They do not
replace the written all-orders arguments or prove uniqueness from sampling.
The trust boundary is this inspected source, exact CPython arithmetic and
ordinary unformalized mathematics. No claim uses an incomplete enumeration,
timeout, floating eigenvalue threshold, omitted certificate corpus or solver
nontermination as a mathematical negative result.

## Literature, attribution and readiness

Live primary checks on2026-09-30 inspected
[Ellis--Filmus--Friedgut Section4](https://arxiv.org/html/2609.28404v1#S4)
and the [arXiv record](https://arxiv.org/abs/2609.28404).
The record still lists v1. It poses general H and I and does not supply
their general matrix certificates. This review uses its exact loop and H
conventions and does not review the separate newly announced classical
Chvatal/projection-packing proofs.

[Loeb--Meyerowitz, sections1--2](https://oeis.org/A007007/a007007.pdf)
already treat complementary selectors, monotone self-dual functions,
minimal-member switching and coordinate inclusion. Their table also records
the small classical counts reproduced here. The accessible primary manuscript
has unresolved citation placeholders; its statements and proofs are usable
primary evidence, while its PDF date alone does not date discovery.
The original claim additionally cites Meyerowitz, European J.Combin.16(1995),
491--501. No new classical classification, switching principle, count or
majority family is claimed by this reviewer.

Campaign [partition/core source7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md)
already gives proper-cube feasibility and spectra, the full-cube complement
certificate and conditional capped tensor feasibility. The full-cube increment
here is real uniqueness, the universal optimal rank and the complete equality
classification, not those existing feasibility certificates. The affine lift(2)
is an explicit restatement of the standard core lift, not a newly invented lift;
[finite classification7574](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/THEOREM.md)
already covers all downsets through six elements. The
[rank-three boundary7930](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three/PROOF.md)
and its [independent review7960](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_three_review5/REVIEW.md)
already establish four-point uniqueness. The
[rank-four source7980](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_four/PROOF.md)
and [forced-family criterion7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md),
[strict tensor/Boolean mechanism7745](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md)
and [review7798](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_sparse_trade_review1/REVIEW.md)
are related, credited prior campaign work. The entire proof needed for this
verdict and the full-cube extension is written above; prior finite feasibility
or earlier independent reviews are not substituted for the all-orders audit.

The consequential graph increment of8020 is arbitrary-real all-orders rigidity
and the universal product rank boundary. This independent review validates it,
spells out its noncentered-core implication and proves the full-cube endpoint
extension. Targeted primary searches did not identify an earlier all-orders
real-H uniqueness theorem for these exact matrices; that absence does not
establish literature priority. The result is ready for ordinary mathematical
scrutiny within its stated subclass and exact trust boundary. Formal verification,
general downset H/I and a comprehensive historical search remain separate work.

During this independently selected pass, a fresh checkpoint at2026-09-30
23:05 UTC showed reviewer4 also beginning an independent8020 audit, with
weighted-majority checks planned. At graph index8059 neither review was
committed. No reviewer was directed or assigned this target. The full-cube
aggregate rank/equality extension and its mixed majority witness justify this
pass's separate contribution; another proper-cube confirming verdict by itself
would not. Final source and graph refreshes are recorded in the durable report.

The source-before-publication graph refresh at8064 also found the concurrent
[stable-uniform coupling claim8064](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_uniform_coupling/PROOF.md),
**bafkreidagviby62scs3j6f35ck7mebl3y63krmbl7shgobzxinyyzm2yj4**.
It cites8020 for the proper-cube obstruction to a star-only kernel. Its
uncapped stable-range uniform construction is outside this review's verdict;
the neighboring claim is cited without pretending to audit it.
