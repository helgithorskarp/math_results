# Independent nine-point nonstar audit: exact certificates, Boolean kernels and sharp mixed-product gaps

Reviewer: **six-reviewer-1**, role **independent mathematical reviewer**,
2026-09-30. The shared campaign signing key does not establish distinct
authorship. Independence here means independently selected scope, a different
orbit decoder, separately implemented exact arithmetic, and the proof below.

Target: six-downset-3's committed lemma
`bafkreifgjzpwksxtwg67desxnwdqw3mg5t6avbdiwmib3q4mfq3bznsdjm`,
height 7794, **Exact capped H matrices attain forced nonstar ranks for two
nine-point downsets and their mixed products**. Reviewed source commit:
`9f9cf092322742672916c0e2af251631b9cc3593`, principally
[NINE_POINT_PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/NINE_POINT_PROOF.md)
and its rational certificate table.

**Verdict: verified within the stated literal finite-domain and finite-product
scope.** The independent exact computation confirms both rational supported
matrices, both spectral caps, all ranks, and the ten forced kernels. The
written argument independently confirms maximal rank among all real H
matrices, the ten base maximum families, and the arbitrary mixed-product
classification. No correctness defect was found in those claims.

Additional proved refinements are the complete 14-element Boolean affine-kernel
classification, a sharp uniform mixed-product lower gap, and a Euclidean
stability estimate. General Spectral Chvatal H and I remain open. This review
does not classify all nine-point downsets, reproduce the numerical discovery
search, establish its affine-search dimensions, or claim historical priority.

## Exact scope and certificate interpretation

Let \(K=\{0,1,2\}\), \(B=\{3,\ldots,8\}\),
\(B_0=\{3,4,5\}\), and \(B_1=\{6,7,8\}\).
Both domains contain every subset of size at most two and all eighteen
triples with two points in \(K\) and one in \(B\). In addition:

* \(D_0\) contains every three-subset of \(B\) except \(B_0,B_1\),
  and does not contain \(K\).
* \(D_1\) contains every three-subset of \(B\) and also \(K\).

There are no larger sets. These predicates exhaust all 512 masks, establish
downward closure, and give \((N_0,s_0)=(82,21)\) and
\((N_1,s_1)=(85,22)\). Every one of the nine coordinate stars has size
\(s_i\). Let \(I_i\) consist of the three pairs in \(K\), the eighteen
cross triples, and, for \(i=1\), the triple \(K\). Its size is \(s_i\).
It is intersecting, because any two of its sets contain two points of a
three-point set, and it has no common point.

For a domain of size \(N\), indexed with the empty set first, put
\(m=N-1\) and

\[
E=\begin{pmatrix}-\mathbf1_m^T\\I_m\end{pmatrix},\qquad
L=J_N+ECE^T,\qquad M=\frac{L-sI_N}{N-s},\qquad
U=NI_m-J_m-C.
\]

Here an H certificate means a real symmetric row-one matrix \(M\), zero
when \(A\cap B\ne\varnothing\), with \((N-s)M+sI_N\succeq0\).
The empty set remains a vertex with an allowed loop. An upper cap is the
additional condition \(M\preceq I_N\); entrywise nonnegativity is not
required by H.

The fixture [certificates.json](certificates.json) is a byte-for-byte copy of
the author's public 5208-byte rational orbit table, SHA256
`0a357b0e8ac63a23eeb69ca012276b0ea1aafcce4d3363b47229919b3c1e208d`.
It is an attributed proof input, not independently discovered matrix data.
On nonempty sets the decoded core has diagonal \(s-1\), entry \(-1\)
for distinct intersecting sets, and the specified rational value otherwise.

The decoder does not use the author's permutation-orbit traversal. For a
disjoint unordered pair \(A,B\), it records each set's counts in the blocks
\(K,B_0,B_1\) for \(D_0\), or \(K,B\) for \(D_1\), and chooses the
least tuple under exchanging \(A,B\), also allowing simultaneous exchange
of \(B_0,B_1\) for \(D_0\). These are complete orbit invariants: within
each block, the disjoint sets partition points into membership in \(A\),
membership in \(B\), and neither. Equal counts allow a block permutation
mapping the three parts separately. The optional block exchange gives the
remaining allowed symmetry. Thus no orbit is omitted or erroneously merged.
Every representative must be a legal pair, every canonical signature must
occur exactly once, and every disjoint pair must decode to it. This checks
44 signatures over 1593 pairs for \(D_0\), and 28 over 1695 for \(D_1\).

## Independent exact verification

[audit.py](audit.py) imports no author code, solver, numerical package, or
proof-search output. It uses CPython integers and `fractions.Fraction`.
For PSD testing it clears denominators and applies symmetric fraction-free
Bareiss Schur elimination. At each stage the residual block is a positive
multiple of the Schur complement. A negative diagonal is a rejection; a
zero diagonal with a nonzero residual row is also a rejection, because a
PSD matrix satisfies \(|a_{ij}|^2\le a_{ii}a_{jj}\). Positive pivots can
be moved by symmetric permutation. Every division is required exact. A
zero residual block terminates with its exact rank. Exceeding the explicit
operation cap raises `INCOMPLETE`, never a nonexistence conclusion.

This arithmetic routine is reused from this reviewer's independently
published [sparse-trade audit](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_sparse_trade_review1/audit.py).
Controls compare its accept/reject result on all 729 symmetric three-by-three
matrices with entries in \(\{-1,0,1\}\) against the complete principal-minor
criterion (24 accepted). Rational Gram matrices, a required pivot swap,
malformed shapes, asymmetry, and cap rejection are checked separately.
Five damaged fixtures are rejected: an altered weight, duplicate signature,
omission, unsupported representative, and non-Boolean case flag. Every guard
is an explicit exception and remains active under Python `-O`.

Let \(X\) have as its ten columns the nine nonempty star indicators and
\(\mathbf1_I\). The checker establishes their independence, \(CX=0\),
all support entries, exact row sums, and the following stronger inequalities:

\[
P=I_m-X(X^TX)^{-1}X^T,\qquad
C_0\succeq P_0,\quad C_1\succeq\tfrac12P_1,\qquad
U_i\succeq I_{m_i}-\frac1{N_i}J_{m_i}.
\]

The inverse, projector identity, annihilation of every column of \(X\),
and both shifted PSD tests are exact. The checked results are:

| Domain | \(N,s\) | \(\operatorname{rank}C\) | \(\operatorname{rank}U\) | \(\operatorname{rank}L\) | \(M_{\varnothing,\varnothing}\) | Least off-diagonal \(M\) |
|---|---:|---:|---:|---:|---:|---:|
| \(D_0\) | 82,21 | 71 | 81 | 72 | \(25/244\) | \(-21/122\) |
| \(D_1\) | 85,22 | 74 | 84 | 75 | \(2/189\) | \(-25/126\) |

Full canonical hashes of \(C,L,M\), and all 14 Boolean patterns, are in
[expected.json](expected.json). All six matrix hashes agree with the author's
published expected results. The decoded matrices contain 41,515 entries in
total across the three matrices for both cases; the hash comparison bridges
the independently decoded matrices to the author's literal data. It is a
cryptographic identity check, distinct from the arithmetic PSD proof.

Because \(E^T\mathbf1_N=0\), the \(J_N\) summand and \(ECE^T\) have
orthogonal ranges, so \(L\succeq0\) and
\(\operatorname{rank}L=1+\operatorname{rank}C=N-10\).
The exact identity

\[
E(NI_m-J_m)E^T=NI_N-J_N
\]

gives \(NI_N-L=EUE^T\succeq0\). Since \(U\) is positive definite,
its full lift has kernel exactly \(\mathbb R\mathbf1_N\). Consequently
\(-\rho I\preceq M\preceq I\), where \(\rho=s/(N-s)\), with lower
endpoint multiplicity ten and a simple unit endpoint. Support and row sums
are checked for the lifted matrix, including the empty row and its loop.
Negative disjoint-pair weights are allowed by H and do occur here.

## Equality, forced rank, and all Boolean kernel indicators

For any real H matrix on either domain, write \(L=(N-s)M+sI\).
For an intersecting family \(F\) of nonempty sets of size \(t\), support
gives \(\mathbf1_F^TM\mathbf1_F=0\). With
\(z=\mathbf1_F-(t/N)\mathbf1\), row normalization therefore gives

\[
z^TLz=t(s-t)\ge0.
\]

Thus \(t\le s\), and equality forces \(z\in\ker L\). The nine stars
and \(I\) attain equality. Their centered indicators are independent:
subtract the empty-coordinate equation and evaluate the singleton rows to
eliminate the nine star coefficients, then evaluate any set in \(I\) to
eliminate its coefficient. Hence every real H matrix has nullity at least
ten and rank at most \(N-10\), whether or not it satisfies the upper cap.
The literal certificates attain that upper bound.

In any maximal-rank H matrix the centered kernel is exactly this ten-dimensional
span. Consider a Boolean indicator \(y\) with \(y(\varnothing)=0\),
\(\sum_Ay(A)=s\), and \(y-(s/N)\mathbf1\in\ker L\). Its singleton
values give coefficients \(b_i\in\{0,1\}\), and the empty equation gives

\[
y(A)=\sum_i b_i\mathbf1_{i\in A}
 +(1-\sum_i b_i)\mathbf1_{A\in I}.
\tag{1}
\]

Put \(J=\{i:b_i=1\}\). A pair in \(B\) forces \(|J\cap B|\le1\).
If a point of \(B\) and a point of \(K\) are both selected, their pair
has value two. Thus a selected \(B\)-point forces \(J\) to be that one
point, giving six stars. If no \(B\)-point is selected, all eight subsets
\(J\subseteq K\) give Boolean values in (1): on the pairs and cross
triples in \(I\), the value is \(|J\cap A|+1-|J|\), which is zero or
one; on \(K\), if present, it is one; every other set also has value zero
or one. Their size is automatically \(s\), since the coefficients in
(1) sum to one and all ten component families have size \(s\).

There are exactly **14** such indicators. For \(J=\varnothing\) the
family is \(I\); for the nine singleton choices it is a star. For the
three two-subsets of \(K\) and for \(J=K\), it contains at least two
disjoint singleton sets, and is not intersecting. Hence precisely **ten**
are maximum intersecting families, as the target claims. Exhausting all
512 coefficient patterns independently checks this complete reduction.

The \(J=K\) pattern is particularly useful: its family \(T\) consists
of the three \(K\)-singletons, the eighteen \(K\)-\(B\) pairs, and
\(K\) when present, with

\[
\mathbf1_T=\sum_{i\in K}\mathbf1_{\text{star}_i}-2\mathbf1_I.
\tag{2}
\]

It gives no extra independent kernel direction. For every H matrix,
\(\mathbf1_T^TM\mathbf1_T=0\). Thus if an alternative H matrix has
nonnegative off-diagonal entries, all its entries on \(T\times T\) must
vanish: its diagonal there is already zero, and all terms of the sum would
be nonnegative. The exhibited signed certificates instead have ordered
positive and negative masses \(+72/61,-72/61\) on \(D_0\), and
\(+20/21,-20/21\) on \(D_1\). This proves a necessary zero constraint
for nonnegative alternatives, not their impossibility.

## Arbitrary finite products and sharp endpoint separation

Take any nonempty finite product of these domains on disjoint ground
supports. Write \(N=\prod_jN_j\), \(p=\max_j s_j/N_j\), \(s=pN\),
and \(c\) for the number of factors attaining this density. Largest
coordinate stars have size \(s\). The tensor \(M=\bigotimes_jM_j\)
is symmetric, supported and row one. For
\(\rho=p/(1-p)=\max_j\rho_j<1\), every tensor eigenvalue lies in
\([-\rho,1]\). Equality at \(-\rho\) requires one critical factor at
its lower endpoint and every other factor at its simple unit endpoint:
another nonunit factor has absolute value strictly less than one.
Thus its lower multiplicity is \(10c\), its unit endpoint is simple,
and \(\operatorname{rank}((N-s)M+sI)=N-10c\).

The ten centered maximum-family cylinders in each eligible factor are
independent, and the spans for different factors are orthogonal under
uniform product measure. They force the same rank upper bound for every
H matrix. For the tensor certificate, a Boolean indicator of size \(s\)
in the centered kernel has form \(p+\sum_{j\text{ eligible}} f_j(A_j)\),
with each summand mean zero. A nonconstant summand has width exactly one,
by fixing all other coordinates and comparing Boolean values. Independent
choices of extrema would give width at least two if two summands varied.
Therefore precisely one varies. The empty-product coordinate ensures that
its base indicator excludes the empty set. The base classification above
now gives exactly **\(14c\)** Boolean indicators, of which **\(10c\)**
are intersecting cylinders and **\(4c\)** are nonintersecting cylinders.
Intersectingness reduces to that of the base family by setting the other
coordinates empty. This also holds for any maximal-rank H matrix, whose
kernel is forced to be this same cylinder span.

The exact shifted PSD checks quantify the separation. Write
\(\alpha_0=1\), \(\alpha_1=1/2\). The nonzero eigenvalues of
\(ECE^T\) equal those of
\(C^{1/2}(I_m+J_m)C^{1/2}\succeq C\), so every positive eigenvalue of
\(L\) is at least \(\alpha_i\). Also

\[
E(I_m-J_m/N)E^T=I_N-J_N/N,
\]

so the upper inequality gives \(NI_N-L\succeq I_N-J_N/N\).
Every nonunit eigenvalue of a base \(M_i\) is therefore at most
\(1-1/(N_i-s_i)\), and every nonlower eigenvalue exceeds its lower
endpoint by at least \(\alpha_i/(N_i-s_i)\ge1/126\). In particular all
base nonunit absolute values are at most \(q=62/63\).

Set

\[
\rho_0=\frac{21}{61},\quad \rho_1=\frac{22}{63},\quad
\delta=\rho_1-\rho_0=\frac{19}{3843}.
\]

In a product, a negative eigenvalue with just one nonunit factor either
is the critical lower endpoint, is the noncritical endpoint \(-\rho_0\)
when \(D_1\) is present, or is separated by at least \(1/126\).
If a negative product has two or more nonunit factors, at least one factor
is negative with absolute value at most \(\rho\), and another has
absolute value at most \(q\). Its separation from \(-\rho\) is at least
\(\rho(1-q)\ge\rho_0/63=1/183>\delta\). Positive eigenvalues are
still farther away. Thus every finite product has a simple unit endpoint
with gap at least \(1/63\), and a lower endpoint with gap at least
\(\delta\).

For a genuinely mixed product with \(h\ge1\) copies of \(D_1\) and
\(k\ge1\) copies of \(D_0\), the lower eigenvalue is \(-\rho_1\)
with multiplicity \(10h\). The **second-lowest eigenvalue is exactly
\(-\rho_0\), with multiplicity \(10k\)**: one \(D_0\) lower factor
and all other factors unit produce it, whereas every other nonminimal
eigenvalue has strictly larger separation. Consequently its lower gap is
exactly \(\delta\), and the smallest positive eigenvalue of \(L\)
is exactly \((N-s)\delta\), with multiplicity \(10k\). This proves
sharpness uniformly in both factor counts without expanding any tensor.

For an intersecting family \(F\) in any such product, of size \(t\),
the earlier quadratic identity and the positive spectral gap give the
following proved stability estimate in the ordinary Euclidean norm:

\[
\operatorname{dist}^2\!\left(\mathbf1_F-\frac tN\mathbf1,\ker L\right)
\le\frac{t(s-t)}{(N-s)\delta}
\le\frac{1342}{19}(s-t).
\tag{3}
\]

The last step uses \(t\le s\) and
\(s/(N-s)\le\rho_1\), with \(\rho_1/\delta=1342/19\).
This is a distance to the spectral kernel. It does not assert a bound
on symmetric difference from an actual maximum intersecting family.

## Literature, attribution and trust boundary

The exceptional nonstar configuration is prior mathematics, identifiable
with the triangle-plus-cross-triples family in
[Czabarka--Hurlbert--Kamat, Theorem 1.4](https://arxiv.org/pdf/1703.00494).
The spectral question and signed empty-loop normalization are in
[Ellis--Filmus--Friedgut, Section 4](https://arxiv.org/html/2609.28404v1#S4);
its [arXiv record](https://arxiv.org/abs/2609.28404) was refreshed on
2026-09-30 and lists v1. Classical family bounds and these configurations
are not new results of this campaign. The constructed capped rational
matrices and the present literal kernel/gap refinements are separate claims.
A targeted primary-literature search establishes no historical-priority
guarantee. Zhang's [vertex-transitive direct-product classification](https://arxiv.org/abs/1007.0655)
does not automatically apply to these mixed-level, empty-loop domains;
the product equality bridge was proved explicitly above.

Campaign antecedents are the
[structural core lift](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md),
graph `bafkreibcaten54awe2plsr47by6exlnt6amzwzqvisiqnlbl7fvu5ijsom`;
the [sparse-trade kernel obstruction](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/KERNEL_TRADE_PROOF.md),
graph `bafkreife2xylkr325rm6jyy2ylfk2a7r5g66dqonqfmeopfg5wj5urwioy`;
and six-reviewer-5's independently exhibited examples and arbitrary-H bounds
in the [regular-six review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_regular_six_review5/REVIEW.md),
graph `bafkreiconcodpfzi5h4q72dqvnwxkzb7x65mtiujqlqynbbtudkcthcz3q`.
This reviewer's preceding sparse-trade review is
`bafkreidufjw5hkiess5w7wceffjfeyksg2qybx3ufsugqzxnq5c76th33q`.
The [four-STS9 review](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_four_sts9_review5/REVIEW.md),
graph `bafkreifpxwge2uxcot5agxkls3yoqac7mcgudiajybyw5cgy4s3nz72rby`,
explicitly treated this target as unaudited context. Its sufficient audit
of a different cohort is not repeated here.

The trust boundary is the public rational fixture, inspected decoder and
exact CPython arithmetic, plus the ordinary written reduction, lift,
equality and product proofs. Neither the fixture's discovery nor the
proofs are formally verified. Cryptographic hashes corroborate identity;
they do not replace arithmetic or the infinite-product argument. Failed
trial gap thresholds are failed candidates, not infeasibility evidence.
No numerical-search output, private data or large tensor is required.

## Strengthening and improvement opportunities

**Proved in this review:** the full 14-pattern affine-kernel classification
(and \(14c\) product version), the zero constraints for nonnegative
alternatives, the sharp mixed-product gap \(19/3843\), its exact second
eigenvalue multiplicity, and the kernel-distance bound (3).

**Highest-value next bridge:** turn (3) into a bound on distance to one of
the ten eligible extremizer cylinders. This needs a quantitative theorem
rounding a nearly Boolean additive kernel function to a one-factor
indicator, followed by an intersection argument excluding the four
nonintersecting patterns. The exact Boolean width argument alone proves
no quantitative edit-distance estimate. A dimension-independent rounding
bound would give stability for arbitrarily many factors.

**Concrete matrix frontier:** impose the necessary \(T\times T\) zero
constraints when seeking entrywise nonnegative maximal-rank certificates.
The four extra Boolean indicators give further analogous constraints, but
all lie in the existing ten-dimensional kernel. A complete exact PSD
construction or a rational dual obstruction is needed to decide that
stronger feasibility problem; signed cancellation and a failed search
would decide neither real feasibility nor Conjecture I generally.

**Broader classification:** identify other rank-three triangle-type
exceptional domains whose maximum-family indicators force a low-dimensional
kernel, then solve the remaining capped complement problem. Extending
these two literals to every such domain requires a uniform core formula
or a justified complete cohort and exact certificates, not these two
successful examples. The classical rank-three EKR theorem alone supplies
no spectral certificate. A proof-assistant encoding of the core/lift and
Boolean/product bridges could separately reduce the remaining ordinary
proof trust boundary.

## Reproduction and compact evidence

With CPython 3.11+ and the standard library, from the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B -O spectral_downsets_nonstar_nine_review1/audit.py \
  --check spectral_downsets_nonstar_nine_review1/expected.json \
  --compare-author spectral_downset_six_exact/NINE_POINT_RESULTS.json
```

The optional author comparison checks all matrix hashes and key metadata;
the audit otherwise runs from this directory's fixture alone. The compact
canonical result SHA256 is
`fcf7f2ac533d69f980573987129d88d60665b67147b8aac9cef21a7e226e8a1c`.
The completed CPython 3.11.2 run took 7.755 seconds and 25,068 KiB peak RSS,
one process with numeric/native thread limits one. Summary cases are
`[(82,"1","1",14),(85,"1/2","1",14)]`, recording each domain's size,
lower-core gap, upper-slack gap and Boolean-pattern count. All required
checks completed; no timeout, memory kill, UNKNOWN or partial enumeration
is used as mathematical evidence.
