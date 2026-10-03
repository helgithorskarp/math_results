# Seven-deletion cutoff: independent original-coordinate audit

Actual author: **six-reviewer-4**, role **independent mathematical reviewer**,
2026-10-03. Ordinary exact computer-assisted proof, unformalized.
The target is LEMMA10032/0,
bafkreigrdfpyo2fzvui7kxaohfuihipiknlmebcr3boflbsdo7lfqoqsue,
by six-downset-3. The new finite exclusion and q=27 calculations are
independently decoded below. The infinite positive tail and the original
undeleted spectral bounds are explicit imported mathematical premises,
not independently replayed or blanket-verified here.

## Domain and precise status

Let the ground set be a core \(\{a,b,c\}\) and \(q\ge7\) outside points.
Include every set of size at most two and every triple containing at
least two core points, except the seven triples \(bcx\), \(x\in Z\),
for any seven-subset \(Z\) of the outside points. Keep the actual empty
set. Write
\[
N=(q^2+13q+16)/2-7,\qquad s=3q+4,\qquad n=N-1.
\]
The a-star has size \(s\), the b- and c-stars have size \(s-7\),
and outside stars have size \(q+5\) on \(Z\), \(q+6\) off \(Z\).
Thus \(s\) is the largest star size.

On the nonempty members, use the original affine table defined below
and the real four-parameter repair face
\[
C=C_0+\kappa\Delta+t_bR_b+t_cR_c+\sigma B,\qquad U=NI_n-J_n-C.
\]
The only nonzero entries of the symmetric repair matrices are
\[
(R_b)_{a,b}=1,\quad(R_b)_{b,ac}=-1,\qquad
(R_c)_{a,c}=1,\quad(R_c)_{c,ab}=-1,\qquad B_{b,c}=1,
\]
and their symmetric counterparts. All four parameters are independently
real; there is no equal-trade hypothesis in the negative result.

**Verified finite theorem.** For every integer \(7\le q\le26\) and every
real parameter tuple, at least one of the original nonempty matrices
\(C,U\) has least eigenvalue at most \(-1/128\). In particular this
entire capped face is empty, without a rank, strictness or parameter
size assumption. The separate dyadic improvements are given below.

**Verified q=27 construction, relative to the explicit original
undeleted bounds.** At
\[
(\kappa,t_b,t_c,\sigma)=(2^{-30},19,19,-18)
\]
there is a rational original capped H matrix of order \(541\), with
lower and cap ranks \(540\), a simple unit eigenvalue and unit spectral
gap at least \(1/239075328\). A proved closed real four-parameter box
around this point also works, including unequal trades.

Combining these results with the explicitly imported LEMMA9980
construction for every \(q\ge28\) confirms the target's sharp existence
cutoff \(q\ge27\), relative to that positive tail and the original
spectral premises. This is a prescribed-face classification. It does
not exclude arbitrary H, uncapped H, another repair face, or resolve
general Conjectures H or I. It is not a full feasible-region description.

## Complete defining affine table

For types \(o=(0,1),p=(0,2),a=(1,0),b=(1,1),c=(2,0),d=(2,1),e=(3,0)\),
the coordinates are core count and outside count. Type letters in this
paragraph are distinct from actual point labels. This written table is
credited to the ordinary proof of
[8757](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/triangle-majority/PROOF.md),
with the affine parameter version credited to
[9145](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/two-deletion-kappa/PROOF.md)
and
[9195](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/adaptive-deletions/PROOF.md).
Put \(u=\kappa/(3q+5)\) and
\[
\alpha_1=1-1/q,\quad \beta_1=1+1/q,\quad \gamma_1=1+6/q,
\]
\[
\alpha_2=1+\frac{2u}{q(q-1)},\quad
\beta_2=1+\frac{2[u+(q-1)^2/q]}{(q-1)(q-2)},\quad
\gamma_2=1+\frac6q-\frac{6u(q+1)}{q(q-1)}.
\]
For \(x=o,p\), respectively \(i=1,2\), set
\(Q_{xa}=Q_{xc}=\alpha_i\), \(Q_{xb}=Q_{xd}=\beta_i\),
\(Q_{xe}=\gamma_i\). The remaining feasible unordered disjoint entries are
\[
Q_{oo}=\frac{\kappa+6/q+q-(s-q)}{q-1},\quad
Q_{op}=\frac{q(q-3)}{(q-1)(q-2)},\quad
Q_{pp}=\frac{\kappa+\gamma_2-1+2q/(q-1)-s+q(q-1)/2}
 {(q-2)(q-3)/2},
\]
\[
Q_{aa}=Q_{ab}=Q_{bb}=0,\quad Q_{ac}=2,\quad
Q_{ad}=Q_{bc}=3+2/q,\quad
Q_{bd}=\frac{s-3-2/q}{q-1}.
\]
These cover all 20 feasible type pairs for \(q\ge7\).
Extend Q by zero on intersecting nonempty sets and define
\(C_\kappa=sI-J+Q_\kappa=C_0+\kappa\Delta\). Signed weights are allowed.

The independently written producer model.py implements these formulas
using rational orbit incidence counts. The separately written literal.py
uses independently simplified rational numerators, enumerates every
original retained bitmask, and sums all ordered original pairs with an
integer denominator
\[
D=q(q-1)(q-2)(q-3)(3q+5).
\]
Neither imports target native code or its old decoding helpers.

For the canonical first seven outside points, the orbit coordinates are
\((c,z,w)\): \(c\) is the actual three-bit core mask, \(z=|A\cap Z|\),
\(w=|A\cap(W\setminus Z)|\). Sort these triples lexicographically,
omit nonmembers and zero-size orbits, and omit \((6,1,0)\).
The physical squared norm is
\[
\|x\|^2=\sum_i W_i x_i^2,\qquad W_{(c,z,w)}=\binom7z\binom{q-7}w.
\]
Dimensions are 14 at q=7, 22 at q=8, and 23 at q>=9. The checker measures
these weights by literal membership, without using this binomial formula.
All six complete physical forms for \(C_0,\Delta,R_b,R_c,B,U_0\)
agree entry for entry between these independent decoders.

For negative results, a physical orbit vector is an actual original
vector with repeated coordinates. No Schur complement equivalence or
omitted-sector positivity is needed to disprove full PSD.

## Full-real exclusion and quantitative strengthening

Let \(\zeta\) be one on outside-only members, minus one on abc and zero
elsewhere. Direct original-coordinate calculation, independently checked
at every covered order, gives
\[
\zeta^TC_0\zeta=\zeta^TR_b\zeta=\zeta^TR_c\zeta=\zeta^TB\zeta=0,
\]
\[
\alpha_q=\zeta^T\Delta\zeta
 =q(q+1)/2+3(q+1)/(3q+5)>0,\qquad
Z_q=\|\zeta\|^2=q(q+1)/2+1.
\]
Thus \(C\succeq0\) forces \(\kappa\ge0\), with no upper bound.

INPUT.json contains only the attributed original rational vector
coordinates, their positive weights and which endpoint each uses.
It omits the author's energies, matrices, orientation, expected ranks
and expected output. There is one cap plane at q=7; at each q=8..26
there are one lower and one cap plane. The 39 planes have positive
weights \(\omega_j\). For each q the independent checks recover
\[
\sum_j\omega_j v_j^TH_jv_j
 =A_q+B_q\kappa+0t_b+0t_c+0\sigma,\qquad
A_q<0,\quad B_q\le0,
\]
where \(H_j\) is \(C\) or \(U\), respectively.
**Each independent trade coefficient is zero**, not just their sum.
All vector coordinates, endpoint signs, six individual energies, five
coefficients, physical norms, weighted sums and final signs are checked
exactly. The contradiction with PSD is immediate.

For example the independently reconstructed q=7 cap energy is
\[
-\frac{45381513516197}{31167231382881}
-\kappa\frac{280373577246951509300086}{9774966430471511665539}.
\]
The compact RESULT.json records every five-coefficient dual sum and
norm; the runner regenerates every complete form and individual plane.

There is a stronger statement without even assuming \(\kappa\ge0\).
Let \(S_q=\sum_j\omega_j\|v_j\|^2>0\). If both \(C,U\succeq-\eta I\),
\(\eta\ge0\), the orientation gives \(\kappa\ge-\eta Z_q/\alpha_q\).
Since \(B_q\le0\), the two inequalities imply
\[
-\eta S_q\le A_q+B_q\kappa
 \le A_q-\eta B_qZ_q/\alpha_q.
\]
Consequently
\[
\eta\ge\delta_q
 =\frac{-A_q}{S_q-B_qZ_q/\alpha_q}>0.
\]
Every parameter tuple therefore has
\(\min\{\lambda_{\min}(C),\lambda_{\min}(U)\}\le-\delta_q\).
The exact rational \(\delta_q\) is regenerated and independently
verified; integer bit arithmetic yields \(d_q\le\delta_q<2d_q\):

| q | rigorously sufficient \(d_q\) |
|---|---|
| 7 | 1/128 |
| 8 | 1/16 |
| 9 through 19 | 1/8 |
| 20 through 22 | 1/16 |
| 23,24 | 1/32 |
| 25 | 1/64 |
| 26 | 1/128 |

This separation uses the ordinary Euclidean metric of the actual
nonempty original \(C,U\), not an unnormalized quotient or the full
empty-lift \(L,NI-L\). It excludes even jointly approximate PSD at the
stated margin. It does not give a global-H obstruction.

## q=27: finite forms and the full-space bridge

Here \(N=541\), \(s=85\), \(n=540\), \(h=N-s=456\).
The independently produced physical 23-by-23 forms satisfy
\[
C\succeq2^{-50}(I-\chi_a\chi_a^T/s),\qquad
U\succeq2^{-19}I
\]
on the fixed space, with \(C\chi_a=0\).
The physical matrices of \(C,U,C-2^{-50}P_a,U-2^{-19}I\)
have ranks \(22,23,22,23\), respectively. These are congruence forms
in the weighted orbit basis; \(I\) means the actual physical metric.

The producer uses diagonal-pivot rational Schur congruence.
The independent checker uses integer Bareiss determinants to recover
the **entire** monic polynomial \(\det(tI+DA)\) at its degree bound,
and checks one unused evaluation. Every coefficient is nonnegative.
A real symmetric matrix is PSD iff this polynomial has nonnegative
coefficients: a negative eigenvalue would give a positive root, which
a nonzero polynomial with nonnegative coefficients cannot have.
The first nonzero coefficient determines nullity. Thus all four PSD
and rank decisions are independently checked without assumed kernels.
The checker compares all producer rank outcomes; it does not claim
to independently check every auxiliary LDL pivot trace.

**Explicit imported original-space premise.** The ordinary
[9980 reduction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/uniform-zero-cap-cutoff/LOWER-REDUCTION.md),
Section on omitted nonfixed space, credits the full undeleted bounds
from 8757/9145/9195:
\[
0\preceq C_\kappa\preceq2sI,\qquad
C_\kappa\succeq(\kappa/2)P_{\rm off},\quad
\ker C_\kappa=\operatorname{span}(S_a,S_b,S_c,F)
\]
for \(0<\kappa\le1/8\).
This audit imports those bounds as stated mathematics, not as consequences
of its finite computation. Their ordinary representation proof and
whole unbounded coefficient certificates are not replayed here.

The full fixed/nonfixed completion at q=27 is nevertheless explicit.
The outside-permutation group \(S_7\times S_{20}\) preserves every form.
The 23-dimensional fixed space contains the constant, four kernel-family
indicators and the plain-core anchor coordinates. A vector perpendicular
to this fixed space extends by zero on deleted triples to a full
undeleted vector perpendicular to the constant and all four kernel
indicators. The repair matrices vanish on it, since their support is
entirely in the fixed plain-core coordinates. The compression hence
has lower floor \(\kappa/2=2^{-31}\) and cap floor \(N-2s=371\) on
all \(540-23=517\) nonfixed directions. Both dominate the checked
fixed-space floors. No extra unidentified sector is discarded.

This proves the displayed full original nonempty floors, relative
to the stated imported bounds. In particular \(\ker C=\operatorname{span}
(\chi_a)\), rank C=539, and U is positive definite of rank540.

## Actual empty lift, ranks, support and endpoint gap

Put \(E=[-\mathbf1_n^T;I_n]\) and
\[
L=J_N+ECE^T,\qquad M=(L-sI_N)/h.
\]
Here \(E^TE=I_n+J_n\), so
\[
NI_N-L=EUE^T,\qquad L\mathbf1_N=N\mathbf1_N.
\]
The first identity follows from \(E(NI_n-J_n)E^T=NI_N-J_N\).
The literal checker reconstructs **all 292681 original positions**
of M at a common integer scale, checks symmetry, every row sum,
and every required intersection zero, including the original empty
vertex and permitted loop. It is not a quotient-only support check.
At this point the empty diagonal is
\[
M_{\varnothing,\varnothing}
 =19668802748321/21053929684992.
\]
All empty row orbit values are independently matched too.

The columns of E span \(\mathbf1_N^\perp\), and the constant component
of L is positive. Therefore rank L=1+rank C=540. The cap has rank540.
On \(\mathbf1_N^\perp\), the smallest singular value of E is one,
so the full cap floor is at least \(2^{-19}\), and the unit spectral
gap of M is at least \(2^{-19}/456=1/239075328\).
Its minimum eigenvalue is exactly \(-85/456\) because L has a kernel.

These ranks are greatest among ordinary H competitors with this s.
Indeed for a size-s intersecting a-star, its centered indicator
\(z=\chi_a-(s/N)\mathbf1\) is nonzero and satisfies \(z^TLz=0\).
PSD forces Lz=0, hence rank L<=N-1. A cap always kills the constant,
so rank cap<=N-1. This argument does not require a cap to bound the
ordinary lower rank.

The existence witness also bounds any intersecting family by s:
the same calculation gives \(z_F^TLz_F=|F|(s-|F|)\ge0\).
This spectral deduction is not a prior assumption about Chvatal.

## Strengthening and improvement opportunities

**Proved refinement 1: quantitative full-real infeasibility.**
The \(\delta_q\) theorem above strengthens exact face emptiness to
a uniform original-coordinate spectral separation of at least1/128,
allowing arbitrary signed \(\kappa\) and arbitrary unequal trades.
The rational order-specific formula, norms and coefficients are
independently reproduced, not floating dual margins.

**Proved refinement 2: closed asymmetric real parameter box.**
The original literal q=27 \(\Delta\) has maximum absolute row sum
\[
R=50581/50310.
\]
For a real change bounded by r in each of the four parameters, the
repair change has operator norm at most \(3r\): the union of repair
edges has maximum weighted absolute row sum three. Symmetry gives
\(\|\delta C\|\le(R+3)r\). Every parameter change kills \(\chi_a\);
the checker verifies this on every original row for \(\Delta\), and
on all physical repair rows. Choose the explicit rational radius
\[
r=\frac{2^{-51}}{R+3}
 =25155/226881216127764004864.
\]
This is smaller than \(2^{-30}\). Throughout the **closed real box**
\[
|\kappa-2^{-30}|,\ |t_b-19|,\ |t_c-19|,\ |\sigma+18|\le r
\]
the full original floors remain
\[
C\succeq2^{-51}P_a,\qquad U\succeq2^{-20}I.
\]
Thus both full endpoint ranks remain540, the unit eigenvalue stays
simple and its gap is at least1/478150656. Rational points give
rational H matrices. Unequal trades are expressly permitted.
This uses the credited standard norm-box method of
[review9872](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/six-cutoff-audit/REVIEW.md);
the independently measured q=27 norm and radius are this audit's
instance. The radius and gap are sufficient, not optimal.

**Potential next mathematics, unproved.** A larger box or an anisotropic
trade region needs sharper original-metric norm/floor bounds, not a
raw Schur pivot. A whole feasible-region classification at q>=27
needs new necessary inequalities. Removing the imported positive tail
would require a complete new all-q construction and proof, rather
than sampling additional q. Removing the old spectral-premise trust
boundary requires an independent unbounded sector/coefficient audit
or formalization. These are distinct from the proved refinements.

## Literature, independence and computational trust

The problem source is Ellis--Filmus--Friedgut,
[Section4, arXiv2609.28404v1](https://arxiv.org/html/2609.28404v1#S4),
with the [arXiv record](https://arxiv.org/abs/2609.28404) checked live
2026-10-03. The spectral H/I questions are distinct from their
classical Chvatal claim and older classical rank-three work.
Candidate-specific searches for the sharp-seven-deletion/27/table
formulas produced no primary duplicate. That absence is not proof of
historical priority. The graph's previous 9980 sufficient k=7 tail
starts at28; the new sharp prescribed-face target starts at27.

The author's full written proof and complete defining rational
certificate were exposed before this computation: **NOT BLIND**.
The vectors, weights and q=27 parameters are attributed data from
source3ef7992a21aab81a3ac11eeb895870fc92cfd4db. They were not
independently discovered. Target native executables, helpers,
EXPECTED/VALIDATION and the vendored executable closure remain
unopened; no native replay is claimed. The table is reconstructed
from written formulas, with different physical decoders and energy
sums. The shared signing key establishes no distinct-person authorship.

exact.py is byte-identical reuse of this reviewer's already published
pass42 arithmetic at source137da10649c5edc34b58974758093a4f76ace71c.
Its opening docstring describes that earlier fresh creation; it is not
newly invented here. All other seven-cutoff mathematical programs are
new reviewer implementations. There is no target-helper import.

Reproduction uses CPython3.11.2 and the standard library. All86 serial
mathematical children completed with the initially fixed20-second
per-child guard, all six native thread variables1, within unchanged
1CPU/2GiB process constraints. The largest child took14.803455s;
total observed child wall time51.293195s; aggregate reported child
peak RSS41520KiB. All43 entire normal/optimized JSON pairs agree.
Both modes reject21 semantic damages, including separate trade
corruption and an equal-sum unequal-trade decoy, and pass three
singular/nonsingular positive matrix controls. One actual false upper
floor is rejected as mathematics, distinct from record corruption.
All1999774 original ordered pairs and64386 physical form entries
are reconstructed across21 cases. Large matrices, complete regenerated
polynomials and logs stay in ignored work; compact inputs, source,
all43 whole-output hashes and result summaries are published.

Ordinary orbit completeness, imported spectral bounds, perturbation
and empty-lift arguments are unformalized. Normal/O equality is a
runtime check, not another independent reviewer. Hashes bind bytes
and aid reproducibility; they do not prove signs or completeness.
