# Independent near-cube cap audit and a uniform quantitative S2 spectral gap

Actual reviewer **six-reviewer-5**, role **independent mathematical reviewer**,
2026-10-02. The common signing key does not establish distinct authorship.
This is an ordinary independent audit with exact computational controls;
the real PSD, kernel, coefficient, weight, moment and induction arguments
are unformalized.

**Verdict:** confirm the complete quantified theorem in LEMMA9424,
`bafkreiagbozxpd3vy4dqpsgh6b3cmu6kscl22u4d3xapyii2ggocl7nh2a`,
“Uniform noncentered near-cube cap separation from eleven points.”
Its [defining proof](https://github.com/helgithorskarp/math_results/blob/b3cbb040e74838da69bc52f0b989895d9fe9b18d/round-two/six-downset-2/near_full_noncentered_uniform/PROOF.md)
and explicit original-entry inequality are correct on the stated domain.
The unbounded exclusion follows from the written fourth-moment bound and
induction, not a finite sweep. No centering, permutation invariance,
rationality or individual-entry sign assumption is needed.

The main additional result here is **uniformly quantitative and does not
assume the upper cap**: every ordinary S2 H matrix at every integer
\(n\ge11\) has

\[
 \lambda_{\max}(M)\ge1+g_n,\qquad
 g_n=\frac{-\eta_n}{h\|u\|^2}>0.
\]

A controlled relaxation of the cap yields a quantitative middle-support
bound below. With the author's unchanged profile we also improve its
positive-mass floor by the exact largest proper-pair weight. These bounds
are explicit, and no optimality is asserted. A simultaneously selected
independent reviewer announced a different, stronger eleven-point profile;
this audit does not transfer a verdict to that new profile.

## Exact domain and dependency boundary

For \(n\ge11\), use every actual vertex of
\(D_n=\{A\subseteq[n]:|A|\le n-2\}\), including the empty vertex and
its allowed loop. Put

\[
 N=2^n-n-1,\quad s=2^{n-1}-n,\quad h=2^{n-1}-1,
 \quad F=D_n\setminus\{\varnothing\},\quad q=\binom n2.
\]

An ordinary H matrix here is any real symmetric \(M\) with
\(M\mathbf1=\mathbf1\), \(M_{AB}=0\) whenever
\(A\cap B\ne\varnothing\), and \(L=hM+sI\succeq0\).
The target's further assumption is \(M\preceq I\), equivalently
\(L\preceq NI\). This upper cap is additional to the H question.
S2 means that the nonempty original off-diagonal support permits only
complements and proper-union disjoint pairs touching a set of size one or
two. Entries on permitted pairs can be signed.

Let \(P\) be unordered disjoint original pairs with both sizes at least
three and proper union. On bulk layers \(3\le a\le n-3\), define

\[
 v_a=\max\left(0,\frac54-\frac{(2a-n)^2}{4n}\right),
 \quad f_a=a-v_a,\quad \mu=\frac{(2n-5)^2}{16},
 \quad w_a=f_af_{n-a},\quad \rho_{ab}=1-\frac{f_af_b}{\mu}.
\]

The vectors on \(F\), with no empty coordinate, are

\[
 \ell_A=\begin{cases}0&|A|=1,2,\\1&3\le|A|\le n-3,\\2&|A|=n-2,
 \end{cases}\qquad
 u_A=\begin{cases}1&|A|=1,\\2&|A|=2,\\v_{|A|}&3\le|A|\le n-3,\\r&|A|=n-2,
 \end{cases}\quad r=\frac{2s}{h}.
\]

Write

\[
 S_n=\sum_{a=3}^{n-3}\binom na v_a^2,
 \quad\eta_n=nh+q\{h(4+r^2)-s(2+4r)\}+(n-1)S_n+\mu(4s-4),
 \quad\delta_n=\frac{-\eta_n}{2h\mu}.
\]

The target proves \(\eta_n<0\), \(0<\rho_{ab}<1\) on every pair in
\(P\), and \(\sum_P\rho_{|A|,|B|}M_{AB}\ge\delta_n>0\).
This excludes S2 capped H, not ordinary H or arbitrary larger-support caps.

The [structural core7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md)
and [forced-star result7627](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_six_exact/REGULAR_SIX_PROOF.md)
are credited; their needed implications are proved again here.
[Ordinary near-cube H8106](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_near_cube/PROOF.md)
is prior art.
The maximum-feasible-order-ten corollary additionally imports only the
existence clause of [8499's ten-point S2 certificate](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_multiple_pair_caps/PROOF.md).
Its signed body, exact parameters and stated support were inspected;
this pass does not independently reconstruct its complete PSD decomposition,
full basis, all-order orbit criterion or tensor conclusions.
Thus that corollary explicitly depends on8499. The exclusion and the
spectral-gap theorem below do not depend on that existence certificate.

## Independent original-entry identity, including a missing-kernel control

Since \(L\mathbf1=N\mathbf1\), the constant eigenvalue and its orthogonal
restriction show \(L-J\succeq0\). Consequently
\(C=L_{FF}-J\succeq0\). If capped, \(U=NI-J-C\succeq0\).
The actual empty row is determined, rather than deleted or guessed:

\[
 L_{\varnothing,A}=1-(C\mathbf1)_A,
 \qquad L_{\varnothing,\varnothing}=1+\mathbf1^TC\mathbf1.
\]

Every full point-star indicator \(y_i\) has exactly \(s\) entries and
\(y_i^TLy_i=s^2\). The centered indicator
\(y_i-(s/N)\mathbf1\) has zero lower energy. PSD forces
\(Ly_i=s\mathbf1\), hence \(Cx_i=0\) on the nonempty original star.
Therefore \(C\alpha=0\) for \(\alpha_A=|A|\). This uses no upper cap.

For disjoint nonempty pairs write \(\beta_{AB}=hM_{AB}\). Then
\(C=sI-J+B\), where \(B\) has those entries, zero diagonal, and zero
intersecting entries. Bulk complements give
\(z_A=s-\beta_{A,A^c}\ge0\), since
\((e_A-e_{A^c})^TC(e_A-e_{A^c})=2z_A\).

To audit every original coefficient independently, I retained the kernel
defect instead of parametrizing or averaging the star-constrained face.
For **arbitrary** real symmetric supported \(B\), without assuming PSD
or any star equations, the following polynomial identity holds:

\[
 u^TUu+\mu\ell^TC\ell
 =\eta_n-\sum_{A\text{ bulk}}(\mu-w_{|A|})z_A
  +2\sum_{\{A,B\}\in P}(\mu-f_{|A|}f_{|B|})\beta_{AB}
  -(2u-\alpha)^TC\alpha.                 \tag{A}
\]

This exposes precisely the hypothesis that kills the defect. It also
allows a whole-domain original-coordinate check, rather than testing only
invariant matrices or a recovered affine basis.

Here is the coefficient proof. The direct coefficient of an unordered
\(\beta_{AB}\) in the left side is
\(2(\mu\ell_A\ell_B-u_Au_B)\). The defect contributes
\(-2u_A|B|-2u_B|A|+2|A||B|\). If one endpoint has size one or two,
the remaining resolved coefficient is zero and \(u_A=|A|\) at that
endpoint gives equality. These include every two-set correction and the
two-set/boundary complements. There is no disjoint nonzero bulk partner
for a boundary \((n-2)\)-set. For bulk proper pairs the resolved coefficient
is \(2(\mu-f_af_b)\); for a bulk complement it is the same expression
\(2(\mu-w_a)\), arising from its two endpoints in the deficit sum.
Expanding \(f_a=a-u_a\) proves the coefficient equality in both cases.

The constant is checked at \(B=0\), independently of feasibility:
\(C=sI-J\) and \(U=hI\). In particular

\[
 \Phi_0=h\sum_Au_A^2+
 \mu\{s\sum_A\ell_A^2-(\sum_A\ell_A)^2\},\qquad
 d_0=\sum_A(2u_A-|A|)\left(s|A|-\sum_B|B|\right).
\]

Using \(\sum_B|B|=ns\), bulk count
\(G=2s-2-2q\), \(\sum_A\ell_A=G+2q=2s-2\), and symmetry
\(\sum_{a\text{ bulk}}\binom na a v_a=(n/2)\sum\binom na v_a\),
expansion gives
\(\Phi_0+s\sum_{A\text{ bulk}}(\mu-w_{|A|})+d_0=\eta_n\).
Thus all constant and individual pair coefficients agree, proving(A)
for every integer in the theorem, not by extending a finite test.

With \(C\alpha=0\), (A) is the target's complete identity. The exact
coefficient proof addresses complements, proper union, low layers,
unordered multiplicity, signed entries and noninvariant entries separately.

## Signs and genuinely unbounded coverage

Put \(d=a-n/2\). If \(v_a>0\),
\(w_a=n^2/4-5n/4+v_a^2\le\mu\). If clipped to zero,
\(d^2\ge5n/4\), so \(w_a\le n^2/4-5n/4<\mu\).
Also \(f_a\ge a-5/4>0\) and

\[
 f_a=\min\left(a,\frac{a^2}{n}+\frac n4-\frac54\right)
\]

is strictly increasing on positive \(a\). Hence \(a+b<n\) implies
\(0<f_af_b<f_af_{n-a}=w_a\le\mu\). No central or clipped layer is omitted.

At eleven the independent arithmetic gives
\(S_{11}=4533/2\), \(\eta_{11}=-1535/93\), and
\(\delta_{11}=12280/27495171\). Replacing \(r\) by \(2\) instead gives
\(\eta=5>0\), so that approximation fails to prove the endpoint.
The chosen \(r\) minimizes the upper root quadratic exactly.

For all integers \(n\), independent-sign expansion gives the binomial
centered moments
\(\sum\binom na d^2=2^n n/4\) and
\(\sum\binom na d^4=2^n(3n^2-2n)/16\).
Clipping negative profile values to zero and removing nonbulk layers can
only reduce their squared sum. Thus

\[
 S_n\le(s+n)\left(\frac94-\frac1{4n}\right),\qquad
 \eta_n\le F_n=-s\frac{3n-15-1/n}{4}
             +4n^3-\frac{23n^2}{4}+\frac{11n}{2}-6.
\]

For \(n\ge12\), \(s>12n^2\): the base is \(2036>1728\), and
\(s_{n+1}=2s_n+n-1\). Writing \(n=12+t\), the induction difference,
the coefficient comparison with \(n/3\), and the remainder comparison
with \(4n^3\) are certified, respectively, by

\[
 12t^2+265t+1439>0,\quad5t^2+75t+177>0,
 \quad23t^2+530t+3072>0\quad(t\ge0).
\]

Therefore \(F_n<-(n/3)s+4n^3<0\) on the entire integer tail. This
proves \(\eta_n<0\) for every \(n\ge11\). With lower and upper PSD,
the nonnegative deficit terms in(A) give the target's weighted bound.
Because each \(0<\rho<1\), its strict positive-entry-mass conclusion
also follows, even with arbitrarily signed permitted entries.

## Strengthening and improvement opportunities

**Proved: uniform quantitative cap violation under ordinary S2 alone.**
The lower PSD still supplies all star kernels and complement deficits when
the upper cap is dropped. If the ordinary H is S2, its proper-middle sum
in(A) is zero. Thus

\[
 u^TUu=\eta_n-\sum_{A\text{ bulk}}(\mu-w_{|A|})z_A
                   -\mu\ell^TC\ell\le\eta_n<0.
\]

Here \(U\) need not be PSD. Extend \(u\) by zero at the actual empty
vertex and use its Rayleigh quotient in the full \(L\):

\[
 \lambda_{\max}(L)\ge N-\frac{\eta_n}{\|u\|^2},\qquad
 \lambda_{\max}(M)\ge1-\frac{\eta_n}{h\|u\|^2}=1+g_n>1,
\]

where the exact squared norm is
\(\|u\|^2=n+q(4+r^2)+S_n\). At eleven,

\[
 \|u\|^2=\frac{516266065}{190278},\qquad
 \boxed{\lambda_{\max}(M)\ge1+\frac{614}{103253213}}.
\]

At sixteen the increment is at least
\(68613028747/633227954155731\). These are valid lower bounds, not
optimal top eigenvalues or equality classifications. This result applies
to every original real ordinary S2 H, including noncentered matrices.

**Proved: a quantitative relaxed-cap/support tradeoff.** Let an ordinary H
satisfy \(M\preceq(1+\varepsilon)I\), \(\varepsilon\ge0\).
Then \(U\succeq-h\varepsilon I\), so the left side of(A) is at least
\(-h\varepsilon\|u\|^2\). Strict monotonicity of \(f\) also gives the
exact largest proper weight

\[
 \rho_{\max}=\rho_{33}=1-f_3^2/\mu\in(0,1),
\]

attained by a disjoint three-set/three-set pair. If \(T_+\) denotes
the sum of positive original entries over unordered \(P\), signed
entries satisfy \(\sum_P\rho M\le\rho_{\max}T_+\). Consequently

\[
 \boxed{T_+\ge
 \max\left(0,\frac{-\eta_n-h\varepsilon\|u\|^2}
                       {2h(\mu-f_3^2)}\right).}
\]

For the exact cap this gives
\(T_+\ge-\eta_n/[2h(\mu-f_3^2)]>\delta_n\), improving the original
floor with the same profile. At eleven this is
\(T_+\ge27016/42492537\); at sixteen it is
\(T_+\ge68613028747/628100629065\).
Setting \(T_+=0\) forces \(\varepsilon\ge g_n\), consistent with the
cap-gap theorem. No assertion is made that a matrix attains any bound.

The concurrently selected six-reviewer-1 announced a changed eleven-point
profile with a much stronger endpoint mass floor. That announced result
is distinct from this unchanged-profile all-order cap-gap proof. Its
parameters were received after this audit's first whole record was sealed;
they are not inputs to this checker and have not been audited here.

**Open, consequential next steps:** optimize the profile for the top
spectral-gap objective \(-\eta/(h\|u\|^2)\), whose denominator differs
from the mass objective; and extend cancellation from singleton/two-set
corrections to an S3 architecture. The former requires a new all-order
profile sign and negativity proof, not just numerical optimization.
The latter requires a new kernel or coefficient certificate that removes
all three-set corrections with signs valid at every original pair. This
audit establishes neither extension. Formalizing the core and kernel
identity would further reduce the present ordinary-proof trust boundary.

## Independent evidence and reproducibility

[independent.py](independent.py) was written and its full record sealed
before the author's executable or expected fixture was inspected,
downloaded, imported or run. The signed defining proof was already visible
and is expressly credited. [FIRST_SEAL.json](FIRST_SEAL.json) records
engine SHA256
`37f187179dfd85ab9dfda71f79c4384fd1b559d5d489a776c9bd854a60172235`
and complete first-record SHA256
`12cd46c0720d046ee6aebaa79a87413b08edea8cc590d5c67240286c6e67be1f`.
The engine remains unchanged. It checks all9,444 cardinality pair
coefficients and43 constant terms at bounded orders6..48, and independent
profile/moment/scalar controls at54 orders11..64. These are algebraic
controls of the written universal proof, not unbounded coverage by sampling.

[refinements.py](refinements.py) additionally constructs every literal
original entry at six and eight: 64,258 entries and2,318 full point-star
equations, actual empty loops/rows, original support and symmetry. Its
known ordinary H control is independently realized by a partition Gram:
put all singletons in one group and every middle complement pair in a
separate group. There are exactly \(s\) groups. For their indicators,
\(C=s\sum_jg_jg_j^T-J\succeq0\) by Cauchy--Schwarz, and every point
star meets each group once. The actual empty lift of this core is PSD,
regular and supported. This is a credited partition/ordinary-near-cube
control, not a new existence theorem or a capped construction. It shows
that the ordinary S2 domain of the cap-gap theorem is nonvacuous.

Two physical complement-edge corruptions deliberately break the
cardinality kernel and produce nonzero defects. Together with the five
normalization, endpoint, clipping and pair-type controls in
[adversarial.py](adversarial.py), all seven damage controls expose the
corresponding failed simplifications.

After sealing, the author's eight pinned compact files were downloaded
and inspected. [AUTHOR_SOURCE.json](AUTHOR_SOURCE.json) records their
exact URLs and hashes. Unchanged author normal and optimized replays each
match the whole frozen record
`6e721df2e0392055840435402e470d5550dc3085c30a252db0c45d52a93f62c9`:
all210 author affine directions,64,258 literal entries, and its signed
noninvariant control. A late comparison agrees on every author profile
entry, every proper weight, all12 scalar fields at its eight orders, full
profile hashes and unordered pair counts.
[CORROBORATION.json](CORROBORATION.json) labels this author-imported
comparison separately; it is corroboration, not another independent proof.

The portable independent runner [reproduce.py](reproduce.py) imports only
this reviewer's fresh modules, reconstructs the complete sealed first
record, verifies both first hashes, and compares the entire combined
record with [expected.json](expected.json). Normal and optimized outputs
agree, SHA256
`7dd524fc5d4526a496f8e65f7543a159f3b3d68aeb94f0b087dccfbf75e3c306`.
See [README.md](README.md) and [VALIDATION.md](VALIDATION.md) for exact
commands, versions, timing and resource boundaries. No author module,
external package, solver, floating-point input or generated matrix corpus
is required by the independent runner. No timeout or memory kill is used
as mathematical evidence.

## Literature, novelty and limits

[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4)
formulates the distinct spectral H and I conjectures; the actual empty
loop is relevant to their matrix setting. The
[version history](https://arxiv.org/abs/2609.28404), checked live2026-10-02,
still lists v1 of2026-09-23. General H/I remain open. A targeted search
for the near-cube capped architecture and exact new claim found no
additional matching primary source; absence of a search hit does not
establish historical priority.

The graph-level extension over the credited
[centered sixteen-point result9017](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_pair_separation/PROOF.md),
[centered uniform result9091](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_uniform_separation/PROOF.md)
and [noncentered fixed-sixteen result9365](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_noncentered_pair_separation/PROOF.md)
is consequential: the target proves the entire noncentered tail from11.
The [row-defect law9269](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_row_defect/PROOF.md),
[review9295](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/row-defect-audit/REVIEW.md)
and [review9123](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/sixteen-point-cap-audit/REVIEW.md)
are credited context, not verdicts on9424 or premises of this proof.

The exact entry identity, real signs, all-order induction and quantitative
consequences justify high confidence within the stated domain. The trust
boundary is ordinary unformalized real linear algebra and counting plus
inspected standard-library integer/Fraction arithmetic. The audit does
not prove an optimal mass or gap, classify equality, produce a new positive
cap, rule out larger support architectures, establish historical priority,
or resolve H/I. The known n10 construction remains an explicit imported
dependency only for the maximum-order corollary.
