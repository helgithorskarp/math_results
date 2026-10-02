# Independent audit of the fixed origin-polar certificate and stronger coercivity

Reviewer **six-reviewer-1**, role **independent mathematical reviewer**, 2026-10-02.
The shared signing identity does not establish distinct authorship. This audit
independently selected committed LEMMA9111, exact reference
`bafkreic4fxdcl3inmfbvhyntgio362xbgle6edswct6igvw5ilcjxnvjga`,
“Coalesced critical relaxation: fixed origin-polar weight and vanishing-margin
coercivity”, by researcher **six-sendov-1**. Original source commit
`756a258f441731aff17d6d39bb493b12edb967f2`:
[proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/joint-polar-functional/PROOF.md),
[exact source](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-sendov-1/joint-polar-functional).

**Verdict: confirmed with independently proved stronger sufficient constants.**
The complete complex critical-coordinate relaxation, removable boundary,
nonlinear compactness argument, equality case and sharp quadratic dual onset
are valid. The computations below reconstruct the definitions in a simultaneous
eight-variable jet algebra. Neither previous review9078 nor the author's second
implementation supplies this verdict. Every primary hypothesis and proof bridge
is checked here. The common neighborhood remains existential and may shrink for
the stronger coefficients. The global first-power conjecture is unresolved by
this result, and the actual polynomial baseline and cutoff were already known.

## Exact domain and strengthened statement

Write \(a_0=5/8\), \(\ell=(1+a)^{-1}\), and
\(q^0=(9\ell,\ell,\ldots,\ell)\in\mathbb C^8\).
For nearby nonzero coordinates \(q_j=r_je^{i\theta_j}\), use the continuous
arguments near zero and define
\[
 O_a(q)=9\int_0^1\prod_{j=1}^8(1-atq_j)\,dt,\qquad
 C_a(q)=\int_0^1\prod_{j=1}^8(a+(1-a^2)tq_j)\,dt.
\]
For \(a<1\), let \(Q_a=(|C_a|-1)/(1-a^2)\), with the boundary value
\(Q_1=(\operatorname{Re}\sum q_j-8)/2\). The necessary relaxed constraints are
\[
 |a-1/q_j|\le1\quad(1\le j\le8),\qquad
 |O_a(q)|\le\prod r_j,\qquad Q_a(q)\ge0.                    \tag{1}
\]
No converse realization by disk-rooted polynomials is assumed. Set
\[
 h(a,\theta)=\frac1{\sqrt{1-a^2\sin^2\theta}+a\cos\theta},\quad
 s_j=r_j-h(a,\theta_j)\ (2\le j\le8),\quad
 \mu=\frac{22096964222976}{21378414915091},
\]
and \(J=|O_a|-\prod r_j-\mu Q_a\).

**Proved refinement.** For every \(5/8<A\le1\), there exists one \(d_A>0\)
such that for every \(a\in[A,1]\), every tuple satisfying(1) and
\(\max_j|q_j-q^0_j(a)|<d_A\) obeys
\[
 \sum_{j=1}^8r_j\ \ge\ \frac{16}{1+a}
 +(a-5/8)\left[\frac3{10}\sum_{j=2}^8s_j
                     +\frac1{100}\sum_{j=1}^8\theta_j^2\right].       \tag{2}
\]
All seven slacks are nonnegative. Equality in the baseline \(\sum r_j=16\ell\)
is equivalent to \(q=q^0\). This implies9111's coefficients \(1/8\) and
\(1/22500\), while making no claim about retaining its same neighborhood width.

Define reference radii \(r_j^*=h(a,\theta_j)+s_j\) for \(j\ge2\),
\(r_1^*=16\ell-\sum_{j=2}^8r_j^*\), and \(q_j^*=r_j^*e^{i\theta_j}\).
On a common product neighborhood, \(G(a,s,\theta)=J_a(q^*)\) satisfies
\[
 G\ge(a-5/8)\left[\frac38\sum s_j+\frac1{80}\|\theta\|^2\right]. \tag{3}
\]
For actual degree-nine disk-rooted polynomials, take
\(q_j=(a-\zeta_j)^{-1}\) with derivative roots counted with multiplicity.
Critical collision at the marked root gives infinite first-power sum and is
outside this finite reciprocal neighborhood. The finite case has a simple
marked root and satisfies(1), including at \(a=1\), as proved below.

## Analyticity, geometry and applicability

Squaring the disk condition gives exactly
\((1-a^2)r^2+2ar\cos\theta\ge1\). Its nearby positive root is \(h\), so the
seven slacks are nonnegative. The rationalized formula is jointly real analytic
near the compact reference curve, including
\(h(1,\theta)=1/(2\cos\theta)\).
The model heavy critical point \((8a-1)/9\) remains strictly interior on
\([5/8,1]\); at least \(2/9\) separates its modulus from one.
All reference radii remain positive after choosing a sufficiently small chart.

The integrands at \(q^0\) are respectively9 times the derivative of
\(t(1-at\ell)^8\) and the derivative of \(t(a+(1-a)t)^8\).
Thus \(O_a(q^0)=9\ell^8=P>0\), \(C_a(q^0)=1\), and \(G(a,0,0)=0\).
Both moduli are real analytic on a common neighborhood of this compact curve.
For all complex \(q\), \(C_1(q)=1\). Consequently \(|C_a(q)|-1\) has a
joint analytic factor \(a-1\), and division by \(1-a^2\) is removable.
Putting \(b=1-a^2\) and expanding the primitive factors gives
\[
 C_a(q)=1+b\left(\frac12\sum q_j-4\right)+O(b^2),
\]
which proves the displayed boundary value of \(Q\), including its derivatives.
This argument uses analytic division, rather than pointwise limits alone.

For a monic \(p(z)=(z-a)\prod_{k=1}^8(z-z_k)\),
\(p'(a)=\prod(a-z_k)=9/\prod q_j\).
Integrating its derivative from zero to \(a\) and from \(a\) to \(1/a\) gives
\[
 O_a(q)=\prod_kz_k\prod_jq_j,\qquad
 C_a(q)=\prod_k\frac{1-az_k}{a-z_k}\quad(0<a<1).             \tag{4}
\]
These are the classical origin and complex polar identities, credited to Zhang
Lemma3.1, not new machinery. Since \(|z_k|\le1\), the origin condition follows.
Each polar factor has modulus at least one because
\[
 |1-az|^2-|a-z|^2=(1-a^2)(1-|z|^2)\ge0.
\]
At \(a=1\), a direct calculation is required: if \(p=(z-1)g\), then
\[
 \sum_jq_j=\frac{p''(1)}{p'(1)}=2\sum_k(1-z_k)^{-1}.
\]
Each summand has real part at least \(1/2\), since
\(\operatorname{Re}(1-z)^{-1}-1/2=(1-|z|^2)/(2|1-z|^2)\ge0\).
Thus \(Q_1\ge0\). Gauss-Lucas supplies the critical-disk condition.
No inference of boundary applicability solely from continuation is needed.

## Independent full phase and radial derivation

The independent implementation uses the rational function field
\(\mathbb Q(i)(x)\), \(x=a/(1+a)\), and a polynomial ring in the integration
variable and **all eight phase variables simultaneously**. It truncates total
phase degree at two only after multiplying each primitive factor. The reference
radii expand as
\[
 r_j^*=\ell+x\theta_j^2/2\ (j\ge2),\qquad
 r_1^*=9\ell-x\sum_{j\ge2}\theta_j^2/2,
\]
and \(q_j=r_j^*(1+i\theta_j-\theta_j^2/2)\) to this degree.
Integrating literal product coefficients reconstructs both complex integrals
and the radius product; no author's formulas or executable are imported.

If a complex jet with positive real constant \(p\) has imaginary linear part
\(w\cdot\theta\) and real quadratic matrix \(B\), its modulus matrix is
\(B+ww^T/(2p)\). This supplies both required rank-one terms:
\[
 A_O=A_{\operatorname{Re}O-\prod r}+w_Ow_O^T/(2P),\qquad
 A_P=(A_{\operatorname{Re}C}+w_Cw_C^T/2)/(1-a^2).
\]
The polar correction is subtracted in \(A=A_O-\mu A_P\); discarding it would
invalidate an attempted lower bound. The factor two between a quadratic matrix
and the Hessian is retained. Every one of128 primitive matrix entries is checked
against its seven-small-coordinate symmetry type before conversion to
\(\mathbb Q(a)\). There is no phase-sum restriction or omitted collective mode.

Fresh primitive products in a separate radial perturbation variable reconstruct
\(c_O\), \(g\), \(H\) and \(J_1\):
\[
 c=c_O-\mu g,\quad H_\mu=H+\mu J_1,\quad
 g=8(1-a)J_2,\quad H=\frac{(1+a)^8-1}{8a(1+a)^6},
\]
where \(J_k=\int_0^1t^k(a+(1-a)t)^{8-k}\,dt\).
The multiplier is independently recovered as \(c_O(5/8)/g(5/8)\), not chosen
from the author JSON. At \(a=1\), \(g=0\), \(J_1=1/2\), and the four polar
matrix types are exactly \((-9/8,0,-1/8,0)\), agreeing with the boundary function.
Division by \(g\) is never used to prove the boundary case.

The compact record reconstructs all20 complete original polynomials, four full
original Bernstein expansions, and both64-direction Gaussian polarization record
hashes from these new simultaneous jets. Full equality with the original frozen
record is optional corroboration performed only after the independent engine was
implemented. The same frozen independent record is regenerated in normal and
optimized Python. In particular, author replay is additional evidence, rather
than the basis of the verdict.

## Stronger exact whole-interval certificates

Let \(L=1+a\), \(D=18L^7\), \(\delta=a-5/8\).
Write the four types of \(A\) as \(n_h/D,n_u/D,n_d/D,n_e/D\).
The six-dimensional small-coordinate sum-zero subspace has eigenvalue
\(\delta V/D\), where \(V=(n_d-n_e)/\delta\).
Its orthogonal complement has the matrix
\[
 D^{-1}\begin{pmatrix}n_h&\sqrt7n_u\\\sqrt7n_u&n_d+6n_e\end{pmatrix}.
\]
The independently reconstructed original85 positive Bernstein coefficients show
\(U=L^6c/\delta>48\) and
\(V\ge11958395335884135/60375209869312>2304/40\).
The new exact polynomials
\[
 n_h-D/100,\qquad
 (n_h-D/100)(n_d+6n_e-D/100)-7n_u^2                         \tag{5}
\]
have respectively22 and36 strictly positive Bernstein coefficients on the
**entire** interval \([5/8,1]\). These prove that the two-dimensional block is
strictly greater than \(I/100\). As \(D\le2304\), \(L^6\le64\), and
\(\delta\le3/8\), the block bound \(1/100>\delta/40\) and the transverse
bound together give
\[
 c\ge3\delta/4,\qquad A\ge(\delta/40)I.                  \tag{6}
\]
The boundary transverse eigenvalue vanishes only at \(a=5/8\), while the
collective block stays strictly positive there.

A further new degree-thirteen polynomial
\[
 (9/8-H_\mu)L^6                                           \tag{7}
\]
has fourteen strictly positive whole-interval Bernstein coefficients, establishing
\(H_\mu<9/8\). Its positivity is not an estimate from a numerical grid.
Also \(H_\mu>0\), from \(H>0\), \(J_1>0\) and \(\mu>0\).
The72 new coefficients and all85 original ones are stored as complete exact
rational lists. Every expansion is transformed back in full to the original
power polynomial. All cleared denominators are explicitly positive.

## Uniform nonlinear proof and equality

Fix \(A>5/8\). At the model, \(\partial_{s_j}G=c\) and
\(\operatorname{Hess}_\theta G=2A\).
By(6) and continuity on the compact parameter curve, choose one convex product
neighborhood on which
\[
 \partial_{s_j}G(a,s,0)\ge3\delta/8,\qquad
 \operatorname{Hess}_\theta G(a,s,\theta)\ge(\delta/40)I.   \tag{8}
\]
Specifically, bound absolute derivative errors by \(3(A-5/8)/8\) and
\((A-5/8)/40\), respectively. These are no larger than the relevant half
margins for every \(a\ge A\), so(8) retains the pointwise factor \(\delta\).
This compactness step is an ordinary universal argument, not extrapolation from
jets or a finite sample. Nonnegative slacks keep the segment from zero to \(s\)
inside the product neighborhood.

Conjugation gives \(G(a,s,-\theta)=G(a,s,\theta)\), hence
\(\nabla_\theta G(a,s,0)=0\) for every nearby real \(s\).
Integrating(8) first along slacks and then along phases with the Hessian weight
\(1-t\) proves(3).

For an actual nearby tuple, retain its seven slacks and phases and put
\(\Delta=\sum r_j-16\ell\). Its heavy radius equals \(r_1^*+\Delta\).
By(7), shrink the common neighborhood once more so that along every such
heavy-radius segment
\(0<-\partial_{r_1}J<5/4\). Positivity and the strict upper margin at the
compact model make this possible. The segment need not satisfy(1): analyticity
and positive radii suffice for this integral. The exact fundamental theorem of
calculus gives
\[
 J_a(q)=G-K_{\rm av}\Delta,\qquad0<K_{\rm av}<5/4.
\]
Since(1) and \(\mu>0\) imply \(J_a(q)\le0\), while(3) gives \(G\ge0\),
one first obtains \(\Delta\ge0\), then
\(\Delta\ge(4/5)G\). Substituting(3) proves(2).
The tuple-to-chart map, reference heavy radius and full segment are continuous
uniformly along the compact model curve. A sufficiently small common reciprocal
width \(d_A\) therefore places all needed coordinates and segments in the chosen
neighborhood. This closes the quantifier over every feasible nearby tuple.

Baseline equality forces all phases and slacks to vanish in(2), and then
\(\Delta=0\), giving exactly \(q=q^0\). Conversely this tuple satisfies all
constraints and equalities. For actual polynomials, integrating the critical
factorization with critical points \(((8a-1)/9,-1,\ldots,-1)\) and \(p(a)=0\)
gives \(p(z)=C(z-a)(z+1)^8\), \(C\ne0\), the already known equality family.

## Sharp quadratic onset and the excluded endpoint

For arbitrary real weight \(\nu\), the slack derivative is \(c_O-\nu g\),
and the six transverse eigenvalues are \(\lambda_O-\nu\lambda_P\).
The complete polar transverse numerator over \(2L^2\) has zero constant and
strictly negative remaining coefficients; thus \(\lambda_P<0\) for \(a>0\).
For \(0<a<1\), \(g>0\). Both quantities can be nonnegative only if
\[
 \lambda_O/\lambda_P\le\nu\le c_O/g.
\]
The complete exact identity is
\[
 L^8(g\lambda_O-c_O\lambda_P)=a(8a-5)
 \left(\tfrac12+\tfrac{71}{42}a+\tfrac{115}{42}a^2+
       \tfrac{39}{14}a^3+\tfrac{11}{6}a^4+
       \tfrac{31}{42}a^5+\tfrac17a^6\right).               \tag{9}
\]
The difference between the interval's upper and lower endpoints has the sign
of the left side of(9), since its denominator is \(g\lambda_P<0\) and its
numerator is the negative of that expression. Hence no real weight works below
\(5/8\), and at \(5/8\) the unique admissible weight is \(\mu\), with both
coefficients zero. Above it, the full matrix certificate proves positivity of
the fixed weight, including the remaining two modes and the boundary \(a=1\).
This sharpness concerns the specified quadratic dual method.

Nonnegative endpoint jets do not establish nonlinear minimality. To independently
check the already known actual-polynomial obstruction in7290, take
\(p(z)=(z-a)(z^2+2cz+1)^4\), \(c=\cos t\) near one. Its roots are in the disk.
The derivative factorization is
\[
 p'=(z^2+2cz+1)^3[9z^2+(10c-8a)z+1-8ac].
\]
The two roots of the last factor stay real and less than \(a\) near \(c=1\).
The first-power sum is therefore exactly
\[
 F(a,c)=\frac6{\sqrt{a^2+2ac+1}}+
              \frac{10(a+c)}{a^2+2ac+1}.
\]
At \(c=1\), \(F=16/L\),
\(F_c=(10-16a)/L^3\), and \(F_{cc}=a(58a-40)/L^5\).
Thus at \(a=5/8\), \(F(a,\cos t)-16/L\) has negative quartic coefficient
\(-9600/13^5=-9600/371293\), reproduced exactly by the independent checker.
Consequently an endpoint extension of the baseline itself is false. This family,
its cutoff and negative-side role are credited to7290 and are not new results of
this review. They do not refute \(F\ge8\); the baseline here exceeds8.

## Literature status and exact attribution

The live primary text
[Zhang, arXiv2609.19126v1](https://arxiv.org/html/2609.19126v1),
checked on2026-10-01, calls the first-power statement conjectural in Conjecture1.2;
Theorem1.3 proves its quadratic case. Its Lemma3.1 supplies the classical
origin and complex polar identities used here. The abstract record
[arXiv2609.19126](https://arxiv.org/abs/2609.19126) showed the September16 version.
[Tao's August12 exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
also separates the first-power strengthening from ordinary Sendov. No ordinary
Sendov open-problem or full first-power solution claim is made here.

The earlier campaign result
[7290 proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collapsed_radius_threshold/PROOF.md),
reference `bafkreiftx42zpt2qill6aofpxvxzyhom4ecyujv2fzbs26nmlb5fu67v7e`,
already proves the actual polynomial baseline with an effective original-root
neighborhood and its sharp cutoff. Its whole stronger theorem is not re-reviewed
here. Original9111 explicitly credits it; correction9084,
`bafkreib5t34yogna2movasj5hkyqbgltvr2pm2axb7mmww54mdrupcvvre`,
records the author's attribution correction to the earlier origin-only line.

Original9039,
`bafkreihpwyyqkf4h427jo5fhl62hbhtyezl7tgwjb5oxrigsvbx6g7co3m`, and
[own independent9078 audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/coalesced-phase-audit/REVIEW.md),
`bafkreifze47pjwvgz62hjwo2k3jgx7sdqhsxgzjwlkztpsvado32bru4ka`,
concern the origin-plus-critical-disk relaxation, with a different threshold and
an independently closed quartic obstruction. They do not verify the joint polar
certificate. The new source reuses only this reviewer's own prior jet engine and
small polynomial helpers, explicitly disclosed; the new polar and radial
products and stronger interval inequalities are derived anew. No campaign
review or theorem is a premise of the present functional proof.

The fixed functional representation and its joint quantitative certificate are
consequential additional content of9111. The stronger constants proved here
improve that precise certificate, not the previously known cutoff or its
already effective polynomial theorem. Targeted exact-weight and distinctive
functional literature searches found no additional matching source; this is
not proof of historical priority. Full priority and publication acceptance are
unassessed. The source and ordinary proof support a scoped confirming review,
with a reproducible derivative refinement.

## Strengthening and improvement opportunities

**Proved:** the same fixed functional gives the reference phase coefficient
\(1/80\), tuple phase coefficient \(1/100\), and tuple slack coefficient
\(3/10\), using the exact block and heavy-radius bounds(5)-(7). The tuple
improvements are225-fold and2.4-fold respectively. They are sufficient constants,
not asserted optimal. Their neighborhood width may be smaller.

**Next worthwhile bridge:** make the compact derivative neighborhoods effective.
This requires explicit uniform bounds on the higher derivatives of both complex
moduli, the removable normalized polar function and the chart map, plus an
explicit enclosure for the full heavy-radius segment. Exact jets and positive
Bernstein coefficients alone do not supply such a radius. It would turn the
new reciprocal-coordinate estimate into a directly applicable certified basin.

**Endpoint limit:** widening the parameter interval to include \(5/8\) while
retaining the baseline is impossible by the credited actual-polynomial family
above. A degenerate fourth-order correction must allow its negative mode and
retain sufficient additional structure. No relaxed tuple below the cutoff
is asserted to be an actual polynomial. A larger basin or the unrestricted
complex first-power inequality would require new global information beyond
this compact local chart; no such extension is proved here.

## Reproduction, controls and trust boundary

[Independent source](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-reviewer-1/joint-polar-audit),
[checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/joint-polar-audit/check.py),
[derivation](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/joint-polar-audit/derive.py),
[whole frozen record](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/joint-polar-audit/expected.json),
[reproduction guide](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/joint-polar-audit/README.md).

From repository root, CPython3.12.14, SymPy1.14.0, mpmath1.3.0:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
 python3 -I -B round-two/six-reviewer-1/joint-polar-audit/check.py
```

Repeat with `-O` before the script; optional `--vendor PATH` supplies isolated
pinned packages. Canonical independent record SHA256:
`10a63907d66f1cee9696e925ee157a10790c68b32c48e816862e41c0bd58e875`.
The default checker imports no author program and requires no external record.
It reconstructs128 primitive entries and64 joint entries, all20 original
polynomials,85 original and72 new complete positive Bernstein coefficients,
plus both entire64-direction record hashes. Eight mathematical damages test
omitted modulus terms, sign/weight/normalization mistakes, a boundary error,
symmetry damage and a negative block pivot. Eight full-record damages test
missing data, coefficients, constants, types and extra fields. These use explicit
exceptions active under optimization. The optional original-record comparison
checks all20 polynomials, all four complete interval expansions and both64-direction
record hashes (128 rows total), including every rational coefficient.

Exact computation trusts CPython, the pinned symbolic arithmetic library and
this published derivation. Characteristic zero, positive denominators, all
sectors and removable boundary values are explicit. The ordinary analytic
arguments above, applicability, equality and nonlinear neighborhoods have not
been formalized in a proof assistant. No solver, floating mathematical data,
incomplete enumeration, timeout or externally decoded certificate supports the
verdict. Numerical native threads are one and mathematical jobs are sequential,
with fixed90-second checker and110-second outer guards. The public packet
contains compact source and records; keys, ledgers, private reports and large
proof corpora are excluded.

Measured independent normal/optimized runs took15.54/38.06seconds, peak70,472KiB;
both reconstructed the identical complete record and all original comparisons.
The external optimized fixture with a falsely strengthened phase coefficient
`1/10` failed with the required complete-record mismatch. Original normal/optimized
standalone replay independently reproduced its full canonical
`35b18327d173fc1463565de2e6175c8d8e29bac836119bff997fd8fb05967e4c`
record in5.92/6.64seconds including all its own controls. That replay is separate
corroboration. No mathematical process or Git lock is left active when the review
is handed off.
