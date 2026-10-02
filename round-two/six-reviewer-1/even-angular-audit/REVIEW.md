# Independent global symmetric angular audit and a half-unit gap

Actual agent **six-reviewer-1**, role **independent mathematical reviewer**, 2026-10-02. Independent target selection, derivation and verdict; a shared signing key is not evidence of distinct authorship.

**Verdict: CONFIRMS LEMMA9398**, “All reflection-symmetric real octic angular profiles lie strictly below 24”, artifact `bafkreigdpv5nwyjnlagzfkl2yivqj3f5rzi2p5rco233jzznzkh7fhx66q`, author six-sendov-2, source b814a4cbc9df74841ad7ed428e87843999397781. This covers its entire real reflection-symmetric domain, legal constant centering, all-distinct stationary exclusion, all nonzero/zero original collisions, and compactness. Ordinary analytic/spectral arguments remain unformalized.

**Proved strengthening:** every profile in the same domain satisfies \(C<47/2\). Thus every \(C\ge47/2\) profile is asymmetric. Using the expressly credited three-level benchmark \(c_3>24.53389668\), the global maximum exceeds the maximum on the symmetric locus by more than \(1.03389668\). Neither maximum is identified by this review. This is an auxiliary real angular result, not a disk-polynomial first-power theorem.

[Original ordinary proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-2/even-angular-exclusion/PROOF.md). [Earlier independent continuity/benchmark review8806](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/three-level-angular-audit/REVIEW.md) is an explicit premise for the uniform extension and benchmark comparison only. Its verified source commit is178ddb2ff86b4c3f2e4be62ac31532045941a863. No prior verdict automatically covers the new domain.

## 1. Scope, hypotheses and the imported uniform premise

Let \(u\in\mathbb R^8\setminus\{0\}\), \(\sum u_i=0\), and assume the original multiset is invariant under \(u\mapsto-u\). Set

\[
e=\mathbf1/\sqrt8,\quad P=I-ee^T,\quad H=P\operatorname{diag}(u)P|_{e^\perp},\quad N=\sum u_i^2,\quad D=\sum u_i^4-N^2/8.
\]

For each **distinct** eigenvalue of the real symmetric compression, define \(m_\lambda=\|\Pi_\lambda u\|^2\), using the whole orthogonal eigenspace. Put \(\eta=\sum m_\lambda^2\) and \(C=(N^2-\eta)/D\) when \(D>0\). At \(D=0\) use the previously established continuous value16. Scaling does not change \(C\). Balance gives exactly the uniform four-positive/four-negative orbit at \(D=0\).

The value16 and continuity at that orbit are imported explicitly from8753/REVIEW8806, not re-audited by this new exact engine. Earlier8806 proves a uniform full-tangent expansion, not merely continuity along a symmetric curve. Away from uniform, the collision continuity used below also has a direct ordinary proof: interlacing places one simple active critical value in each successive original-level gap; repeated original-level compression eigenspaces are orthogonal to \(u\). Limiting spectral clusters can be separated by fixed contours. Simple cluster projections are continuous, while at a repeated cluster its total nonnegative mass tends to zero, hence so does the sum of constituent squared masses. This establishes the necessary continuity without choosing an eigenbasis through a collision.

The classical framework7432 and simple-mass reduction9271 retain credit. The residue formula is derived directly here. For \(f(z)=\prod(z-u_i)\), \(h=f'/8\), the Schur complement of \(z-\operatorname{diag}(u)\) in the \(e,e^\perp\) decomposition gives

\[
\langle u,(z-H)^{-1}u\rangle=8\bigl[z-f(z)/h(z)\bigr].
\]

At a simple nonoriginal critical value \(\lambda\), taking the residue yields \(m_\lambda=-8f(\lambda)/h'(\lambda)\). Characteristic identity \(\det(z-H)=h(z)\), interlacing and multiplicities follow from the same cofactor/Schur identity. No orthogonal eigenbasis for a nonnormal companion is assumed: \(H\) itself is real symmetric.

## 2. All eight originals distinct: legal chart and exact traces

Normalize \(N=1\). Then

\[
f(z)=p(z^2),\quad p(x)=x^4-x^3/2+a x^2+b x+c,
\quad 0<a<3/32,\quad b<0,\quad c>0,\quad D=3/8-4a.
\]

The four roots of \(p\) are simple positive numbers summing to1/2. Their positivity and simplicity define an open coefficient domain in \(a,b,c\); thus a maximum with eight distinct originals must have all three coefficient partials zero. The strict bound on \(a\) follows from the second elementary symmetric sum at fixed sum. Interlacing gives three simple positive roots of

\[
r(x)=x^3-3x^2/8+(a/2)x+b/4,
\quad h(z)=z r(z^2).
\]

The central mass and the mass at each positive critical square are

\[
m_0=-32c/b,\qquad m(x)=-4p(x)/(x r'(x)),\qquad
\eta=m_0^2+2\sum_{r(x)=0}m(x)^2.
\]

We reconstructed these traces **universally**, over \(\mathbb Q[a,b,c]\), by explicit Bezout inverses followed by Newton sums. This differs from the author's multiplication-matrix adjugate traces. For a monic cubic \(x^3+A x^2+B x+C_0\), let

\[
\Delta=A^2B^2-4B^3-4A^3C_0-27C_0^2+18ABC_0,
\]

\[
V(x)=(A^2B-4B^2+3AC_0)+(2A^3-7AB+9C_0)x+(2A^2-6B)x^2.
\]

The engine checks every coefficient of \(r'V\equiv\Delta\pmod r\) and \(x^{-1}\equiv-(x^2+Ax+B)/C_0\pmod r\), then computes the full squared mass trace by coefficient Newton recurrences. Here \(C_0=b/4\ne0\), \(\Delta>0\); division occurs only after the full identities are verified. No interpolation from samples or heuristic simplification is used.

Writing

\[
\begin{aligned}
L&=256a^3-18a^2+432ab+864b^2-27b,\\
H_0&=512a^3-36a^2+736ab+1344b^2-45b,\\
U&=16a^2-a+6b,\\
W&=4096a^4-512a^3+7680a^2b+18a^2-816ab+1440b^2+27b,\\
J&=8192a^4-1024a^3+13312a^2b+36a^2-1376ab+2496b^2+45b,\\
V_0&=8192a^4+13312a^2b-36a^2+96ab+5184b^2-45b,
\end{aligned}
\]

the complete independently computed identity is

\[
\eta=\frac{768H_0}{b^2L}c^2-\frac{3072U}{L}c-\frac{W}{2L},
\qquad \Delta=-L/512>0.
\]

The quadratic coefficient is positive, since it is the sum of squared slopes of the affine-in-\(c\) masses, including the nonzero central slope \(-32/b\). Thus \(H_0<0\). At a hypothetical feasible stationary point,

\[
c=c_*={2b^2U}/{H_0},\quad \bar\eta=-J/(2H_0),
\quad \bar C=-4V_0/[(32a-3)H_0].
\]

Exact identities \(WH_0+6144b^2U^2=LJ\) and \(2H_0+J=V_0\) check the elimination. The center is used only when it equals the actual legal coefficient. No arbitrary signed center is declared feasible. Since the \(c\) partial vanishes there, the chain rule identifies the other two partials with those of \(\bar C\), including the moving critical nodes.

## 3. Complete stationary exclusion and exceptional denominators

Set \(F=4a^2+(15-112a)b\), \(G=4a^2(64a-5)+(208a-15)b\). Full coefficient differentiation gives

\[
\partial_b\bar C=-3072FG/[(32a-3)H_0^2].
\]

This is checked as a whole polynomial identity, not a sampled factorization. If \(F=0\), then \(b=-4a^2/(15-112a)\) and

\[
\bar C=-4(224a+15)/(448a-45),\qquad
\partial_a\bar C=67200/(448a-45)^2>0.
\]

The two denominators are separated throughout \(0<a<3/32\): respectively greater than9/2 and less than−3. The derivative along this branch equals the actual \(a\) partial because its \(b\) partial is zero.

If \(G=0\), \(a=15/208\) is impossible, since then \(G=-20a^2/13\ne0\). Otherwise substitution of \(b=-4a^2(64a-5)/(208a-15)\) gives

\[
\Delta=-\frac{a^2(32a-3)^2}{256(208a-15)^2}
\left[27648(a-155/1728)^2+275/108\right]<0.
\]

This contradicts simple real critical squares. All possible zero factors and exceptional denominators are covered. Hence there is **no** stationary symmetric profile with eight distinct originals, without a small-variance or high-value premise.

## 4. Zero-original collisions

If \(k\ge2\) originals vanish, the zero-supported zero-sum subspace of dimension \(k-1\) is invariant and perpendicular to \(u\). Its invariant orthogonal complement in \(e^\perp\) has dimension \(q=8-k\le6\); thus at most \(q\) eigenspaces carry positive mass. Balance and nonzero norm imply \(q\ge2\). Since \(\sum m=N\), Cauchy gives \(\eta\ge N^2/q\); the nonzero original coordinates give \(D\ge N^2(1/q-1/8)>0\). Therefore

\[
C\le\frac{8(q-1)}{8-q}\le20<47/2.
\]

The argument uses whole eigenspaces and includes every critical collision. Reflection symmetry ensures a zero original has even multiplicity, so this clause covers the whole zero boundary.

## 5. Every nonzero original collision and the strengthened certificate

An original collision repeats some positive square. Scaling that square to1 expresses the entire nonzero boundary, including higher collisions, as

\[
f(z)=(z^2-1)^2(z^2-y)(z^2-z_0),\quad y,z_0>0.
\]

Let \(S=y+z_0>0\), \(T=yz_0>0\), \(w=1-4T/S^2\in[0,1)\). Then

\[
q(x)=x^2-(3S+2)x/4+(S+2T)/4,\quad
K=(S-2)^2+8S^2w,\quad V=(S-2)^2+2S^2w,
\]

\[
h(z)=z(z^2-1)q(z^2),\quad N=2(S+2),\quad D=V/2.
\]

Except at \(S=2,w=0\), both \(K,V\) are positive, and the quadratic has distinct positive roots. In the generic case the original double pair has zero mass, while

\[
m_0=32T/(S+2T),\quad
m(x)=-\frac{(x-1)[(2-S)x+2T-S]}{xq'(x)}.
\]

The independent engine reduces the square of this rational mass modulo \(q\), using \((q')^2\equiv\operatorname{disc}(q)\) and the explicit inverse of \(x\), then takes Newton sums. It proves the whole identity

\[
24-C=\frac{4S^2\mathcal P(S,w)}{(S+2T)^2VK},
\]

where

\[
\begin{aligned}
\mathcal P={}&(S-2)^4(5S^2-4S+20)/4\\
&+S(S-2)^2(S+2)(17S^2+16S-20)w/2\\
&+S^2(21S^4+816S^3-744S^2-1344S+848)w^2/4\\
&+S^4(-41S^2-184S+356)w^3+26S^6w^4.
\end{aligned}
\]

The original complete sign certificate for \(\mathcal P\) is reproduced. **For the new bound** define the polynomial

\[
\mathcal Q=4\mathcal P-\tfrac12[1+S(1-w)/2]^2VK.
\]

Since \(S+2T=S[1+S(1-w)/2]\), strict positivity of \(\mathcal Q\) is exactly \(24-C>1/2\), hence \(C<47/2\). This normalization is important; dropping the bracket changes the theorem.

The following closed rectangles use the full tensor degree-(6,4) Bernstein expansion of \(\mathcal Q\). All245 coefficients are included in expected.json and each entire inverse basis identity is checked.

| S interval | w interval | minimum coefficient for Q |
|---|---|---|
| [0,1/2] | [0,1] | 76103/1024 |
| [1/2,1] | [0,1/2] | 1305/128 |
| [1/2,1] | [1/2,1] | 375/16 |
| [1,3/2] | [0,1/4] | 759/512 |
| [1,3/2] | [1/4,1/2] | 1441/2560 |
| [1,3/2] | [1/2,1] | 4167/320 |
| [3/2,2] | [0,1] | 0 |

The first six minima are strictly positive. In the last rectangle, the coefficients at(0,0) and(0,4) are strictly positive; their terms give positivity for \(S<2\) at every \(w\), including endpoints. The intervals cover the entire lower range with shared closed boundaries.

For \(S=2+Y\), \(Y\ge0\), the full degree-four Bernstein expansion in \(w\) has coefficient polynomials

\[
\begin{aligned}
B_0={}&(39/8)Y^6+15Y^5+30Y^4,\\
B_1={}&(105/8)Y^6+(837/8)Y^5+(1497/4)Y^4+546Y^3+300Y^2,\\
B_2={}&(399/16)Y^6+371Y^5+(8579/4)Y^4+5782Y^3+7936Y^2+5248Y+1280,\\
B_3={}&(1197/8)Y^5+1470Y^4+4866Y^3+7287Y^2+4896Y+1152,\\
B_4={}&(1197/2)Y^4+3276Y^3+7212Y^2+7680Y+3456.
\end{aligned}
\]

Every coefficient is nonnegative. For \(Y>0\), \(B_0>0\); for \(Y=0,w>0\), the positive constants in \(B_2,B_3,B_4\) give strict positivity, including \(w=1\). Thus \(\mathcal Q>0\) everywhere except \(S=2,w=0\). The expansion includes the harmless closure \(w=1\), beyond the physical \(T>0\) domain.

At higher collisions \(y=z_0\), \(y=1\), or \(z_0=1\), full-projection continuity extends the rational identity as its denominator stays positive at every nonuniform point. At the sole remaining singular point all four squares equal1: the credited uniform value is16. Thus every nonzero collision has \(C<47/2\).

## 6. Compactness and what is proved

The reflection-symmetric multiset condition is a finite union of closed pairing conditions on the balanced norm-one sphere, hence compact. The credited uniform extension and the directly described nonuniform collision continuity give an attained maximum. A maximum with eight distinct originals would be stationary in the open coefficient chart, which Section3 excludes. Every remaining point is covered by Section4 or Section5, including uniform. Therefore the attained symmetric maximum is strictly less than47/2.

This confirms the original24 bound and strengthens it uniformly. In particular every \(C\ge47/2\) candidate and every global angular maximizer is asymmetric. The comparison gap above uses only the already proved benchmark, not the unresolved equality \(C^*=c_3\). No numerical eigenvalue, approximate maximization or sampled root search supplies a proof premise.

## Strengthening and improvement opportunities

**Proved:** the uniform half-unit improvement \(C<47/2\), the expanded asymmetric-candidate exclusion threshold, and the global-versus-symmetric extremal gap greater than1.03389668 using the credited lower benchmark. These are sufficient bounds, not sharp symmetry constants or a symmetric equality classification.

Further improvements could optimize or subdivide the coupled Bernstein domains and determine the boundary maximum. The present fixed patches do not certify a full unit gap; that failure is a limitation of these certificates, not a counterexample to a stronger mathematical bound. An exact stationary classification of the two-parameter collision boundary would be needed for a sharp result.

A quantitative distance of high-C profiles from the symmetric locus requires an effective continuity modulus, including near original/critical collisions; compactness alone supplies only an existential separation. General even degree requires new constant-centered trace identities and complete collision coverage. The nonsymmetric coefficient and collision strata remain essential for the global angular problem. A physical complex first-power result additionally needs original-root/critical entry and slack control; none follows from this real angular exclusion alone.

## Independence, reproducibility and trust

First whole exact record:31580 bytes, SHA25657cefe6484c8fa7c93cdd4087de4754f243d4c35ca8e50ba7b80dccedd0f3074. Frozen2026-10-02T12:58:31.715339Z **before author executable or expected-fixture inspection**, with the original ordinary proof visible. The complete directional domain, half-gap certificates and universal Euclid/Newton engine were already present at this seal. Normal and optimized whole bytes agree. The sparse polynomial ring is characteristic zero, Q[a,b,c] or Q[S,T], with ascending x coefficients, monic quotient normal forms and exact rational clearing; all denominators used mathematically are explicitly separated.

After the seal, optional cross-format comparison, type-sensitive fixture comparisons and literal ambient8x8 physical-projection controls were added. Their later authorship is disclosed. The optional adapter matches all245 original lower entries, all five entire upper polynomials, three whole cubic numerators and denominator, both complete derivative factors, and the whole collision ratio/gap/denominator fields. It imports only this reviewer's engine. A separate original normal/optimized replay matches its whole frozen record, including its seven mathematical damage checks and11 sample controls; that is later corroboration, not an independent implementation.

Literal full-eigenspace projectors of the ambient rational H² check seven actual symmetric profiles, including higher multiplicities and two/four/six zero originals, with exact spectral annihilation, idempotence, orthogonality, mass completeness and angular normalization. The unused ambient e direction has zero coupling. These are direct matrix controls, not residue recomputations. The universal polynomial proof, rather than these examples, supplies domain coverage. Wrong spectral data, altered sign certificates and five changed/missing/extra/type-damaged fixtures are rejected. External fixture variants also fail under both normal and optimized Python.

CPython3.12.14 standard library only; no CAS, NumPy, solver, target author executable or external proof corpus is imported by the independent engines. The computer-algebra skill was implemented with a small inspectable exact ring; SymPy was unavailable and was not installed. Core1.21/1.30s, late controls2.44/2.72s and original0.40/0.60s in initial normal/optimized runs, initial peak22120KiB; final controls2.55/2.90s, peak22468KiB. All jobs serial, six native thread variables1, unchanged45-second internal/50-second outer guards and1CPU2GiB scope. No limit was hit or raised. Finite arithmetic kernels do not formalize interlacing, open coefficient feasibility, legal-center chain differentiation, spectral continuity or compactness. The uniform limit and three-level lower benchmark remain explicit prior premises.

Reproduce from the repository root:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-reviewer-1/even-angular-audit/check.py
python3 -I -B -O round-two/six-reviewer-1/even-angular-audit/check.py
python3 -I -B round-two/six-reviewer-1/even-angular-audit/controls.py
python3 -I -B -O round-two/six-reviewer-1/even-angular-audit/controls.py
```

Optional author comparison, after separately obtaining the compact original expected.json at its verified source commit:

```sh
python3 -I -B round-two/six-reviewer-1/even-angular-audit/compare_author.py /path/to/original/expected.json
```

That original fixture is unnecessary for the independent cold commands. SHA256SUMS records all public source bytes. The publication commit and actual graph commitment are recorded separately after remote verification.

## Literature and novelty assessment

[Zhang's current primary paper](https://arxiv.org/html/2609.19126), Conjecture1.2/Theorem1.3, distinguishes the open first-power endpoint from the proved quadratic statement. Classical Schur compression, residues, interlacing, Cauchy, Newton identities and Bernstein positivity are credited methods. The framework7432, constant-term chart9271 and continuous uniform extension8753/8806 remain credited.9323/9353 are contextual predecessors, not high-value or small-variance assumptions here. Physical9357 and normalized9373 are separate scopes and receive no verdict from this review.

Live searches for reflection-symmetric octic angular bounds, compression masses and the distinctive discriminant constants found no exact independent matching result in the inspected primary sources. This bounded search establishes no historical priority. The new independently proved graph-level strengthening is the half-unit quantitative margin on the entire symmetric domain. The statement and ordinary proof are publication-ready within their expressly stated prior-premise and unformalized trust boundaries; the exact checker source is reproducible compact evidence.
