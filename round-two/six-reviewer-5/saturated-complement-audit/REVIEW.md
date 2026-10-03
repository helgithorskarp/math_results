# Independent saturation audit, spectral relaxation and odd orders

Actual author **six-reviewer-5**, role **independent mathematical reviewer**.
Target: six-downset-2's LEMMA **9942/0**, “Saturated complement count and
all-order deficit-class obstructions for capped Hoffman matrices”,
`bafkreibckhjcbvpj6b5pzpts455h34alrtmpi5oz2i6rsrhukqeoxbx7oa`.
Original source **034e8aadfe9b9409d506cd910ce3abaf8190497f**, directory
[saturated_complement_count](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-downset-2/saturated_complement_count).

**Verdict: CONFIRMED** for the entire defining ordinary lemma, including
arbitrary signed and noninvariant real matrices, singular strata, the
original empty vertex, and the all-even-order size-class conclusion.
The confirmation is an ordinary mathematical proof audit with exact
independent alignment checks and late native reproduction. It is
unformalized. The shared signing identity does not establish distinct
human authorship; the independent work here is by six-reviewer-5.

Two refinements are proved below and in [PROOF.md](PROOF.md): a necessary
largest-eigenvalue bound without the cap, and at least three deficit size
classes at every odd near-cube order \(n\ge9\). No general H/I resolution,
new capped construction, rank classification, globally sharp constant,
attainability or positive attenuation-magnitude estimate is claimed.

## Scope and ordinary proof audit

Let \(\mathcal D\) be a finite downset, indexed by all its original
members including \(\varnothing\), with \(N=|\mathcal D|\), largest star
size \(0<s<N/2\), \(h=N-s\), \(r=N-2s>0\). The hypotheses are real
symmetry, \(M\mathbf1=\mathbf1\), intersection support zeros, and
\(L=hM+sI\succeq0\). The original count additionally requires
\(M\preceq I\), equivalently \(L\preceq NI\). A saturated pair is an
unordered pair of nonempty members \(A,A^c\), with the complement in the
**entire ground set** and \(L_{A,A^c}=s\). Local old-cube mirrors after
adjoining new coordinates do not satisfy this condition automatically.

The constant-line split gives \(L-J\succeq0\). Saturation makes
\(e_A-e_{A^c}\) have zero energy, so its bilinear pairing with every
vector vanishes. This follows directly from positivity of a quadratic
in a real scalar and remains valid at singular endpoints. The two rows
of \(L\) coincide. For another nonempty vertex, the original support
forces at least one of the two entries to vanish; both therefore vanish.
The row sum fixes their actual empty entries at \(r\). No permutation
invariance or sign restriction was inserted.

Distinct complementary pairs have disjoint vertices. On the empty vector
and their unnormalized sums, the Gram matrix is
\(\operatorname{diag}(1,2I_q)\). With \(\lambda=L_{\varnothing,\varnothing}\),
the two complete restricted forms are

\[
\begin{pmatrix}\lambda&2r\mathbf1^T\\2r\mathbf1&4sI_q\end{pmatrix},
\qquad
\begin{pmatrix}N-\lambda&-2r\mathbf1^T\\-2r\mathbf1&2rI_q\end{pmatrix}.
\]

Completing squares proves
\(qr^2/s\le\lambda\le N-2qr\), hence \(q\le s/r\).
For \(q=0\) the statement reduces to \(0\le\lambda\le N\).
Restricted-form interval feasibility is not full-matrix sufficiency.

For \(\mathcal D_n=\{A:|A|\le n-2\}\), \(n\ge4\), the exact
parameters are \(N=2^n-n-1\), \(s=2^{n-1}-n\), \(r=n-1\), with
\(s-1\) unordered complementary pairs. PSD of \(L-J\) also bounds each
complementary entry above by \(s\), so nonsaturation means a strict
positive deficit. Thus at least \(s-1-\lfloor s/(n-1)\rfloor\) pairs
must be attenuated. This has no parity restriction.

For even \(n=2m\), the central class has \(\binom{2m}{m}/2\) pairs;
low noncentral classes \(a=2,\ldots,m-1\) have \(\binom n a\) pairs.
Allowing deficits in at most \(\ell\) such classes gives the necessary
condition

\[
\sum_{a=2}^{m-\ell-1}\binom n a\le\left\lfloor\frac{s}{n-1}\right\rfloor.
\]

The complete even-order recurrence and its positive decompositions were
independently rebuilt coefficient by coefficient. Its base is
\(\Delta_6=-1110\); both positive normalized terms strictly decrease
for every real \(m\ge2\). This proves the exclusion for **every even
\(n\ge12\)**, rather than extrapolating finite numerical checks.
The exact necessary minimum class counts at 12,16,24,32,64,128,256 are
3,4,5,6,10,15,23. They give no existence or attainability claim.

## Strengthening and improvement opportunities

**Proved spectral refinement.** Keep all original lower-PSD, support and
row hypotheses, and omit the upper cap. For \(q>0\), take an original
vector with empty coordinate \(qr/s\), value 1 on every saturated
vertex, and zero elsewhere. Its exact Rayleigh remainder is

\[
v^TLv-\left(2s+\frac{qr^2}{s}\right)\|v\|^2
=\left(\lambda-\frac{qr^2}{s}\right)\frac{q^2r^2}{s^2}\ge0.
\]

Therefore

\[
\lambda_{\max}(M)\ge
\max\left\{1,\frac{s+qr^2/s}{h}\right\}.
\]

The constant 1 follows separately from the row sum and applies at
\(q=0\) too. More generally an imposed \(M\preceq\kappa I\),
\(\kappa\ge1\), requires

\[
\frac{qr^2}{s}\le\lambda\le\kappa h+s-
\frac{2qr^2}{\kappa h-s},\qquad
q\le\frac{s(\kappa h-s)}{r^2}.
\]

Equality in the synthetic restricted block is not a globally feasible
supported-certificate construction or a global optimality proof.

**Proved odd-order extension.** If \(n=2m+1\), there is no central half
class. The necessary condition for at most \(\ell\) deficit classes is
\(\sum_{a=2}^{m-\ell}\binom n a\le\lfloor s/(n-1)\rfloor\).
For \(\ell=2\), the exact obstruction is

\[
\Delta'_m=-(2m-1)4^m+
\frac{4m(2m+1)}{m+2}\binom{2m}{m}+4m^2+2m-1.
\]

Divide by \((2m-1)4^m\) to get \(-1+A'_m+B'_m\). The two ratios are

\[
\frac{A'_{m+1}}{A'_m}=
\frac{(2m+3)(m+2)(2m-1)}{2m(m+3)(2m+1)},\qquad
\frac{B'_{m+1}}{B'_m}=
\frac{(2m-1)(4m^2+10m+5)}{4(2m+1)(4m^2+2m-1)}.
\]

Their denominator-minus-numerator polynomials are
\(2m^2+m+6\) and \(24m^3+16m^2+1\), positive for all \(m\ge1\).
The exact base is \(\Delta'_4=-41\). Hence **every odd \(n\ge9\)**
requires deficits in at least three distinct low-size classes, preserving
arbitrary proper couplings and singular strata. The written induction
supplies unbounded scope.

**Further work, not proved here.** A useful recovery constraint would
quantify near-saturated rather than exactly saturated pairs and combine
it with every star row and both original cones. A proof would need
controlled cross-block energies and the empty coupling, including zero
deficits. Neither this count nor a permissible class population constructs
an H matrix. Another worthwhile question is whether a full original
downset realizes the restricted spectral bound; restricted principal
equality alone gives no such answer. Formalizing the real kernel and
incidence/induction bridges would remove the remaining ordinary-proof
trust boundary. No expensive enumeration is needed for this review.

## Independent computational evidence

Fresh `algebra.py`, `independent.py` and the entire ordinary `PROOF.md`
were sealed before the first target executable/expected/validation access.
The graph's written proof and formulas were exposed; this was not blind.
No prior producer code or reviewer kernel was copied. All three hashes
remain unchanged. `PRE_NATIVE_SEAL.json` records the precise seal.

The primary checker uses exact rational symmetric elimination, complete
pair-sum bilinear forms and Gram metrics, polynomial convolutions, literal
near-cube members and point stars through 12, and Pascal versus binomial
rows through 256. It records **480 synthetic restricted principal cases**
including singular and infeasible endpoints at three caps, **253 exact
order records**, four complete recurrence coefficient identities and
33 definition-level recurrence nodes, plus eight semantic rejections.
These finite checks align the ordinary proof; they do not establish
its all-real or all-order claims by numerical enumeration.

Normal and optimized primary records agree in their **entire 2,443,299
bytes**, SHA256
`fa8e157f4b4b0d3f2647a0adad6a5df9a06bbc1b61cd5d2a1a24567c55cfba03`.
There is no mathematical normalization, field projection or dropped record.
The public source-only cold runner verifies these exact full records.

After sealing, the seven target files (37,855 bytes) were checked against
the exact remote commit, entire pinned/main bytes and functioning readers.
Both native isolated modes reproduce the complete **430,995-byte** record,
SHA256 `f5ecf24efd597d3a15453c2f6434029e03e018ad4007852b1d1f45ab0955cfa7`,
and the entire compact expected file, including all ten original damages.
Native timings are about 1.6 seconds per mode, peak child 24,276 KiB.

The DATA-only late adapter independently reconstructs both full literal
matrices for **every 1,166 native principal case**, matching complete
matrix fingerprints, exact PSD decisions/ranks and both endpoints. It
matches all 31 entire recurrence nodes, the whole coefficient streams,
and all 18 original count records including preceding thresholds.
It imports no producer executable. Six altered correspondence records
reject at their intended mathematical fields.

For the credited ordinary n6 control, the adapter uses the defining
8154 incidence lift \([-R;I]Q[-R^T,I]\), followed by the original empty
lift, rather than the new author's direct entry formula. Every one of
the **3,249 full matrix entries**, all **336 star rows**, lower ranks
35/36, all 15 literal saturated pairs and the upper witness energy
\(-444\) agree. The full matrix fingerprint is
`d9e329021f048623c7037b4761e7fe4f4c0c0e5f23d1b18df030a9554d3fd97e`.
Its actual empty diagonal is 321. This known ordinary H violates the cap;
it is a positive lower-PSD control and demonstrates the cap's necessity,
not a new H construction. The separate 8319 n8 construction was not
rerun here and supplies no new verdict or proof premise.

All work uses CPython 3.12.14 standard-library integers/Fractions,
six native thread settings 1, one serial mathematical child, the unchanged
45-second child guard and 1 CPU/2 GiB scope. No solver, CAS, timeout,
UNKNOWN, incomplete enumeration or resource escalation supplies a claim.
Large streams, logs, private ledgers and credentials are omitted and can
be regenerated. `VALIDATION.json` records the cold and execution evidence.

## Literature, dependencies and publication readiness

The current primary problem is Ellis--Filmus--Friedgut,
[Section 4](https://arxiv.org/html/2609.28404v1#S4), with the
[version record](https://arxiv.org/abs/2609.28404) checked live on
2026-10-03 (v1, 2026-09-23). It formulates spectral H and I separately;
the upper cap in this review is extra. Its classical/projection results
do not supply the capped matrix sought here. Targeted searches for the
saturation count, complement-matrix domain and capped-H terminology found
no pertinent primary-paper match. That bounded evidence does not establish
exclusive historical priority. PSD kernel, Schur, Rayleigh and binomial
recurrences are classical tools.

Target 9942 receives credit for the original structural count and even-order
obstruction. The old empty/core lift 7578, weighted ordinary control 8154,
pair-expanded baseline 8319, and near-cube motivation 9639/9793 retain their
credit. None is promoted to an audited full classification by this review.
The count and both refinements rederive their needed matrix facts; there
is no imported classification or private peer proof premise. This is a
compact, reproducible confirming assessment with ordinary unformalized
bridges, not formal verification or an unrestricted spectral settlement.
