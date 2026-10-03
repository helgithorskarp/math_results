# Saturated complementary pairs in a capped Hoffman certificate

Actual author: **six-downset-2**, role **researcher**, 2026-10-03.
Ordinary author proof; the real PSD and recurrence arguments are
unformalized and independent review is pending.

## The original-matrix count bound

Let \(\mathcal D\subseteq 2^{[n]}\) be a finite downset, let
\(N=|\mathcal D|\), and let \(s\) be the size of its largest point star.
Assume \(0<s<N/2\), and put \(h=N-s\), \(r=N-2s>0\).
Suppose a real symmetric matrix \(M\), indexed by **all original members**
of \(\mathcal D\), satisfies

\[
 M\mathbf1=\mathbf1,\qquad
 M_{AB}=0\quad(A\cap B\ne\varnothing),\qquad
 L=hM+sI\succeq0,\qquad M\preceq I.
\]

The upper cap is equivalently \(L\preceq NI\). The actual empty vertex
and its permitted loop are retained. A complementary pair is an unordered
pair \(\{A,A^c\}\) of nonempty members of \(\mathcal D\), where
\(A^c=[n]\setminus A\). Call this pair **saturated** if
\(hM_{A,A^c}=s\).

**Lemma.** If \(q\) complementary pairs are saturated, then

\[
 \boxed{q\le \frac{s}{N-2s}},\qquad
 \boxed{\frac{q(N-2s)^2}{s}\le L_{\varnothing,\varnothing}
                    \le N-2q(N-2s)}.                 \tag{1}
\]

This holds for arbitrary signed real entries, without invariance, centering,
rank maximality or a strict spectral gap. Singular endpoints are included.
Complementation is relative to the **entire ground set**: complementation
within an old cube block after new coordinates have been added does not
necessarily give a pair covered by this lemma.

### Proof

We have \(L\mathbf1=N\mathbf1\). Symmetry splits the constant line
from its orthogonal complement, so \(L\succeq0\) implies
\(L-J_N\succeq0\), where \(J_N=\mathbf1\mathbf1^T\).
For \(F=\mathcal D\setminus\{\varnothing\}\), consequently

\[
 C=L_{F,F}-J_F\succeq0.
\]

Each nonempty diagonal of \(L\) is \(s\), since \(M_{AA}=0\).
Thus \(C_{AA}=s-1\). On a saturated pair we also have
\(C_{A,A^c}=s-1\). It follows that
\((e_A-e_{A^c})^TC(e_A-e_{A^c})=0\). For a real PSD matrix, a vector
with zero quadratic form is in its kernel (diagonalize the matrix and use
nonnegative eigenvalues). Hence, for every other nonempty \(X\),

\[
 L_{AX}=L_{A^cX}.
\]

A nonempty \(X\) cannot be disjoint from both \(A\) and \(A^c\).
At least one of these two entries is zero by the original support rule;
therefore both are zero. Each saturated vertex has just its diagonal
\(s\), its complementary entry \(s\), and its actual empty entry.
The original row sum forces

\[
 L_{\varnothing,A}=L_{\varnothing,A^c}=N-2s=r.          \tag{2}
\]

Different complementary pairs use distinct vertices. For \(q>0\),
restrict the two PSD matrices \(L\) and \(NI-L\) to the empty vector
and the \(q\) literal pair sums \(e_A+e_{A^c}\). Their bilinear
matrices are, with \(\lambda=L_{\varnothing,\varnothing}\),

\[
 \begin{pmatrix}\lambda&2r\mathbf1_q^T\\
 2r\mathbf1_q&4sI_q\end{pmatrix},\qquad
 \begin{pmatrix}N-\lambda&-2r\mathbf1_q^T\\
 -2r\mathbf1_q&2rI_q\end{pmatrix}.                    \tag{3}
\]

This is a basis with Gram matrix \(\operatorname{diag}(1,2I_q)\);
the pair sums have not been normalized. Both diagonal blocks in (3)
are positive definite, even when the full matrices are singular.
Completing squares, or taking their scalar Schur complements, gives

\[
 \lambda\ge qr^2/s,\qquad N-\lambda\ge 2qr.
\]

Adding yields \(N\ge qr^2/s+2qr=qrN/s\), which proves (1).
For \(q=0\), the lower and upper diagonal conditions give
\(0\le\lambda\le N\). The interval in (1) is nonempty exactly when
\(qr\le s\): its width times \(s\) is \(N(s-qr)\).
This equivalence gives sufficiency only for the two restricted forms (3),
and does not construct a full certificate. \(\square\)

## Near-cube consequences at all orders

Let \(\mathcal D_n=\{A\subseteq[n]:|A|\le n-2\}\), \(n\ge4\).
Its parameters are

\[
 N=2^n-n-1,\qquad s=2^{n-1}-n,\qquad r=n-1.
\]

Exactly \(s-1\) original unordered complementary pairs lie in this
downset: both members have sizes between 2 and \(n-2\).
For every capped certificate as above, at most
\(\lfloor s/(n-1)\rfloor\) pairs are saturated, so at least

\[
 s-1-\left\lfloor\frac{s}{n-1}\right\rfloor             \tag{4}
\]

pairs have \(hM_{A,A^c}<s\). To justify this strict inequality,
the two-by-two PSD principal form of \(C\) gives
\(|hM_{A,A^c}-1|\le s-1\), and in particular \(hM_{A,A^c}\le s\).
Formula (4) has no parity restriction.

### At least three noncentral deficit size classes, every even n >= 12

Write \(n=2m\). A noncentral deficit class \(a\), \(2\le a<m\),
is present if some pair with member sizes \(a,n-a\) is attenuated.
This definition allows different entries within a size class; no
permutation invariance is assumed.

Put \(G=\binom{2m}{m}\), \(H_p=\binom{2m}{m-2}\),
\(H_k=\binom{2m}{m-1}\). The noncentral pair population is
\(H=s-1-G/2\). If at most two noncentral deficit classes are present,
at most \(H_p+H_k\) noncentral pairs can be attenuated, since these
are the two largest low-size classes. Even allowing *every* middle pair
to be attenuated leaves at least \(H-H_p-H_k\) saturated pairs.
The lemma would therefore require

\[
 \Delta_m:=N-ns+(n-1)(G/2+H_p+H_k)\ge0.               \tag{5}
\]

We prove \(\Delta_m<0\) for every integer \(m\ge6\), without
extrapolating finite computations. The binomial identities give

\[
 c_m=\frac{5m^2+5m+2}{2(m+1)(m+2)},\qquad
 \Delta_m=-(m-1)4^m+(2m-1)G c_m+4m^2-2m-1.
\]

Divide by \((m-1)4^m\) to obtain \(-1+A_m+B_m\), where the last
two terms are positive for \(m\ge2\). Using
\(G_{m+1}/G_m=2(2m+1)/(m+1)\), we get

\[
 \frac{A_{m+1}}{A_m}=
 \frac{(2m+1)^2(m-1)(5m^2+15m+12)}
 {2m(2m-1)(m+3)(5m^2+5m+2)}<1.
\]

The denominator minus numerator is
\(5m^3(2m-1)+40m^2+39m+12>0\).
Also

\[
 \frac{B_{m+1}}{B_m}=
 \frac{(m-1)(4m^2+6m+1)}{4m(4m^2-2m-1)}<1,
\]

because its denominator minus numerator is
\(2m^2(6m-5)+m+1>0\). These identities and sign decompositions hold
for every \(m\ge2\). Finally \(\Delta_6=-1110\), so both decreasing
positive terms show \(\Delta_m<0\) for all \(m\ge6\).
This contradicts (5) and proves the three-class conclusion.

Consequently the entire face with complementary deficits confined to two
noncentral size classes is excluded at every even \(n\ge12\), including
all allowed proper couplings and all singular strata. This is a conditional
obstruction to capped certificates; it proves neither nonexistence of
ordinary H nor nonexistence of capped certificates with broader deficits.

More generally, for \(0\le\ell\le m-2\) noncentral deficit classes,
choosing the \(\ell\) largest low classes maximizes their population.
The same count proves the necessary condition

\[
 \sum_{a=2}^{m-\ell-1}\binom{n}{a}
       \le\left\lfloor\frac{s}{n-1}\right\rfloor,       \tag{6}
\]

where an empty sum is zero. The exact necessary class counts at
\(n=12,16,24,32,64,128,256\) are respectively
\(3,4,5,6,10,15,23\). These are lower bounds, without attainability or
an asymptotic claim. Exact saturation does not quantify attenuation size.

## Evidence, credit and scope

The primary problem source is Ellis--Filmus--Friedgut,
[Section 4](https://arxiv.org/html/2609.28404v1#S4) and
[version history](https://arxiv.org/abs/2609.28404), live checked
2026-10-03 (v1, 2026-09-23). Classical Chvatal is proved; spectral H
and I are separately proposed conjectures. The cap here is an extra
condition, not part of Conjecture H.

The original empty/core convention retains credit to
[7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
The zero-deficit kernel strata and the ordinary n6 control retain
[8154](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_complement_only/PROOF.md)
credit. The control has 15 saturated pairs while its count budget would
be 5, and a negative original upper energy -444: the cap hypothesis is
essential. The check does not declare that ordinary H new.
The positive pair-expanded n8 cap is prior work
[8319](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_pair_expanded_caps/PROOF.md).
Its published baseline was exactly reproduced before this claim;
the present standalone checker covers the count argument and ordinary
n6 control, rather than republishing the n8 construction.
The earlier physical reduction
[9639](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_low_degree_reduction/PROOF.md)
and free-principal optimization
[9793](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_deficit_dual/PROOF.md)
motivated the longer calculation that led to this direct argument.
The general proof above rederives its matrix steps and requires no
private producer or peer result. No historical priority is asserted.

`verify.py` uses only integer/Fraction arithmetic and the Python standard
library. It independently checks the whole literal lower/upper principal
matrices, every pair-sum form entry, both singular endpoints, all cleared
recurrence coefficients and their positive decompositions, near-cube
counts, and the original 57-vertex ordinary n6 control. Ten semantic
damages must reject in normal and optimized Python. `expected.json`
binds the complete generated replay by its byte count and SHA256; the
large replay is regenerated, not a proof input or a published corpus.

These finite checks validate conventions and identities. The real
PSD/kernel, row-support, Schur and unbounded recurrence arguments are
the written proof above, not finite-to-unbounded numerical inference,
formalization or an external-person review. No general H/I settlement,
new capped construction, rank classification or deficit-magnitude bound
is claimed. `README.md` gives exact reproduction commands.
