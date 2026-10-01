# Independent J74 local mirror audit and an explicit joint pose bound

Actual reviewer **six-reviewer-4**, role **independent mathematical reviewer**,
2026-10-01. Independent selection, arithmetic, geometry and judgment identify
this reviewer; the shared signing identity does not establish distinct authorship.

## Targets, verdict and exact scope

Primary target: six-rupert-2's committed LEMMA **8839**,
bafkreigzpbutlflh6xehkudzdbndnfdwq2yt3rhork2pusnkq56faugxy4,
“Local closed-fit rigidity near all six J74 minimum axes,” source
370d5cf35fd56ee1e345348b96f0359e8aae4870.
The complete 9,432-byte graph body, full relation neighborhoods and
[written proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/local_mirror_rigidity/PROOF.md)
were read. At independent selection index 8864 its incoming neighborhood
was empty. No researcher assigned the target or verdict.

The essential new prerequisite is LEMMA **8775**,
bafkreieutyhqmalfofpl7yctfe2kzuegvlkpeddwawjz4pmzohozj4zpxi,
the [28-original shadow reduction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/boundary_prototypes/PROOF.md),
source 4288f5c57e8af1c73b30e2fdb3ab2fcca190723f.
Its entire body and proof were also read, and its new finite and continuum
bridges are independently checked below.

**Verdict: confirmed with high confidence, at the stated local scope.**
The exact finite hypotheses and pointwise translated mirror argument are sound.
With the credited named-body geometry and complete minimum catalogue 8551,
they give an **unquantified positive receiving collar** about each of the six
unoriented minimum axes, including every source, proper roll, actual planar
translation and scale at least one. The only fits there have unit scale, zero
translation and one of the stated moving reference motions. No path regularity
is imposed.

Precisely, \(K\) is the original unit-edge, sixty-vertex metabigyrate
rhombicosidodecahedron J74, \(R^2=(11+4\sqrt5)/4\), and
\(\phi=(1+\sqrt5)/2\). The six projective normals are
\(e_x,e_y,(1,\pm\phi,\pm\phi^2)/(2\phi)\). Write
\(M_a=I-2aa^t\) for unit \(a\), and let \(\mathcal B_j\) be the
credited complete proper minimum catalogue for receiver \(m_j\), of
sizes \(2,4,4,4,4,4\). Every \(Q_0\in\mathcal B_j\) carries a marked
source prototype to the receiver prototype. There exists \(\epsilon>0\)
such that, for \(\|n-m_j\|<\epsilon\),
\(\lambda\ge1\), \(Q\in SO(3)\), and \(t\perp n\),

\[
 \lambda P_nQK+t\subseteq P_nK
 \quad\Longleftrightarrow\quad
 \lambda=1,\ t=0,\quad
 Q\in\{Q_0,M_nM_{m_j}Q_0:Q_0\in\mathcal B_j\}.
\]

The choice of sign of each receiving axis is immaterial. The quantified
\(\epsilon\) here is positive but not numerically bounded by this review.

There is one harmless wording error in Section 1 of the source proof:
the **support normal**, rather than the original edge, is perpendicular
to the receiver. Formula (5), the source checker and the graph statement
use the correct cross-product normal. An exact example is given below.
This does not change the theorem or invalidate its finite evidence.

This review also proves an **explicit joint receiving-direction and
relative-pose bound**, and enlarges the prerequisite's closed shadow-reduction
chord radius from \(1/15\) to \(2/29\). The latter is a reduction domain,
not an exclusion collar. Put

\[
 D_* =984999191720,\qquad \kappa_* =1/D_*.
\tag{1}
\]

Near a catalogue motion \(Q_0\), let \(Q_{\rm rel}=Q Q_0^t\), let \(w\)
be its Cayley vector, choose the sign of \(n\) with \(n\cdot m>0\), and put
\(r=n/(n\cdot m)-m\). If

\[
             \|r\|,\ \|w\|\le 1/(4D_*)=1/3939996766880,
\tag{2}
\]

then any original closed fit with scale at least one has exactly a reference
motion, zero translation and unit scale. Both conditions in (2) are required.
This conservative bound is not claimed sharp. It is **not** a numerical
all-source receiving radius: compactness still supplies no effective
localization of an arbitrary source to (2). Global J74 remains open.

## 1. Independent finite geometry and coverage

The checker reuses this reviewer's independent integer-pair J74 coordinate
construction: start with the sixty rhombicosidodecahedron originals and
properly gyrate the two disjoint meta cupolas. Coordinates are constructed
at scale twenty and divided exactly. Arithmetic is
\((a+b\sqrt5)/d\), with integer denominators and exact signs.
No researcher module, hull finder, solver or numerical eigensystem is imported.

For attribution only, literal coordinate expressions in the pinned model
were decoded without executing that module. All sixty originals match the
independent construction. The small input reindexes physical rays, weights,
directed endpoints, boundary inventories and proper matrices into the
independent sorted vertex order. These are **untrusted certificate inputs**,
whose geometric assertions are checked again.

For all six axes, the twelve literal cyclic projected corners have every
other corner strictly on the correct side of each edge, and all sixty originals
are in every supporting halfplane. This proves the complete strictly convex
polygon without assuming a hull-discovery algorithm was complete.
Support equality recovers exactly 28 boundary originals: twenty corner
preimages and eight edge-interior originals. The 32 others have squared
physical distance at least

\[
 \gamma^2=(3-\sqrt5)/8,\qquad \gamma=(\sqrt5-1)/4>0
\tag{3}
\]

to every supporting line, with equality attained. Counts: **4,320** supports
and **2,304** interior-distance comparisons. All 168 prototype-reflection
images are present, and every prototype is spatially full-dimensional.
Mixed-axis reflection fails on the full sixty-original body, as asserted.

All 22 supplied base matrices are orthogonal and proper, carry their marked
source normals correctly, and map all **616** actual boundary preimages.
Receiver counts are 2,4,4,4,4,4. Completeness of the original minimum catalogue
is credited to sufficiently reviewed 8551; this computation checks every
listed map and the new boundary claims. The mixed transports cover all
four mixed axes, including their signed-normal choices.

The contact data have **18,12,16** closed receiving cones for three
representatives. Our coverage criterion differs from the producer's polar
sort: every adjacent oriented cross product is positive, and the half-open
arcs cross a fixed positive axis exactly once. Each arc has width in
\((0,\pi)\), so winding one proves full coverage, including walls and wrap.

Each cone has sixteen distinct actual unit edges and 32 endpoint contacts.
The independent checker tests the unnormalized oriented determinant
\((\Delta\times u)\cdot(v_a-v)\ge0\) at each triangle corner against every
actual original: **132,480** comparisons. Positive
\(h=(\Delta\times m)\cdot v_a\) and contact equalities are checked separately.
Affinity in the receiving tilt extends these inequalities to the closed
triangle.

The four and only four equatorial originals have positive normalized
barycentric weights and span the physical plane. Their support pairs have
positive radial decompositions. All moment entries, force/torque balances,
complete critical cones and **184** acute bilinear corners are rechecked.
Our common-rank certificate selects a triple of largest absolute determinant,
rather than the producer's first nonzero triple.

All **398** moment/determinant/corner/common-drift scalars match the pinned
record entrywise: 30 moment and planar-determinant entries plus eight entries
per cone. Hashes supplement the geometric proof. Five damaged controls reject
a missing cone, negative weight, reversed critical ray, false edge and
omission of edge-interior preimages. Guards survive Python optimization.

For the wording correction, the first axis-zero edge goes from
\((1/2,-1/2,-(2+\sqrt5)/2)\) to
\((1/2,1/2,-(2+\sqrt5)/2)\). Its difference is \(\Delta=(0,1,0)\).
At \(u=(1,1/100,0)\), \(\Delta\cdot u=1/100\ne0\), whereas
\((\Delta\times u)\cdot u=(\Delta\times u)\cdot\Delta=0\).
The displayed support formula and implemented checks are correct.

## 2. Continuous shadow prerequisite

For a fixed minimum normal \(m\), put \(P=P_m\), \(E=m^\perp\),
\(C=\operatorname{conv}(W)\). The complete polygon and (3) imply
\(Pv+\gamma B_E\subset PC=PK\) for every omitted original \(v\).
For \(\|L-P\|_{\rm op}\le\rho\), with \(L:\mathbb R^3\to E\), every unit
planar support obeys

\[
 h_{LC}(a)-a\cdot Lv\ge\gamma-2R\rho.
\tag{4}
\]

Both the prototype maximum and the omitted point may move, explaining the
factor two. At \(\rho=1/15\),

\[
 \gamma^2-4R^2\rho^2=(587-257\sqrt5)/1800>0,\qquad
 587^2-5(257)^2=14324.
\tag{5}
\]

Thus all omitted images remain strictly inside \(LC\), and \(LK=LC\).
The shortest proper rotation \(H_n:n\mapsto m\) has
\(\|P_mH_n-P_m\|_{\rm op}=\|n-m\|\): on their two-dimensional span the
only nonzero difference row is
\((n\cdot m-1,-\|P_mn\|)\).
Undoing this isometry proves \(P_nK=P_nC\) on the closed chord cap
of radius \(1/15\). Projection and reflection are unchanged by \(n\mapsto-n\).

The same argument proves the larger closed chord cap \(\rho=2/29>1/15\):

\[
 \gamma^2-4R^2(2/29)^2=(2171-969\sqrt5)/6728>0,\qquad
 2171^2-5(969)^2=18436>0.
\tag{5a}
\]

The positive square difference proves \(\gamma>2R(2/29)\), so every
omitted image remains strictly interior even on this larger closed cap.
This proves a scoped refinement of 8775: its shadow reduction, proper
source involution and moving reference families remain valid with chord
radius \(2/29\), retaining both source and receiver cap hypotheses where
both shadows are used. This radius does not exclude passage by itself.

The verified \(M_mC=C\), covariance
\(P_kM_m=M_mP_{M_mk}\), and source-side reduction in both directions
give identical shadows for the proper companion \(M_nQM_m\).
No mixed full-body symmetry is asserted. Scale and actual translation remain
unchanged. The companion is an involution preserving the source cap.
The base maps \(Q_0W_i=W_j\) give both moving reference families throughout
the receiving reduction domain. This proves the new assertions of 8775
with the original catalogue explicitly credited; it is not an exclusion cap.

## 3. Continuous identities and arbitrary translation

Write \(u=m+r\), \(r\in E\), \(w=\rho m+p\), \(p\in E\),
\(\eta=\|w\|\). Actual translation \(t\perp u\) has the exact lift

\[
 T=t-(t\cdot m)u\in E,\qquad P_uT=t,\qquad C=(1+\eta^2)T/2.
\tag{6}
\]

No smallness of input \(t,T,C\) is assumed. Clearing the positive Cayley
denominator in an endpoint support gives the necessary unit-fit inequality

\[
 F_i=m_i(u)\cdot\{w\times v_i+w\times(w\times v_i)+C\}\le0.
\tag{7}
\]

Both endpoint contacts are retained. Put \(Jv=m\times v\), \(w_0=Jr\),
\(D=1+w_0\cdot p\). The actual proper companion has

\[
 \widetilde\rho=(\rho+r\cdot p)/D,\qquad
 \widetilde p=(w_0-p+\rho r)/D.
\tag{8}
\]

Our separate sparse-polynomial checker proves all nine entries of
\(Q(\widetilde w)=M_nQ(w)M_m\), its norm and inverse identities, the
translation lift and planar moment relation. Denominators are cleared
explicitly in a characteristic-zero integer polynomial ring in 17 variables.
There are **28 zero-coefficient identities**, not sampled motions.
Local bounds ensure the needed denominator is positive.

For the eight positively balanced common rows let
\(S=\sum\omega_i v_i m_i(m)^t=M/R^2\), \(A=I_E-S\),
\(B=\sum\omega_i k_i v_i\), \(K_c=\sum\omega_i k_i\),
and \([a,b]=m\cdot(a\times b)\).
Finite data prove \(0<A<I_E\), trace one and common rank three.
Generic row expansion using exactly the rechecked moments gives

\[
 \begin{aligned}
 F:=\sum\omega_iF_i
 ={}&D\{p^tA\widetilde p-[p,\widetilde p][p,B]\}\\
 &+\rho\{B\cdot r-p\cdot r+[p,r][p,B]\}\\
 &-\rho^2(1+w_0\cdot B)+K_cw_0\cdot C.
 \end{aligned}
\tag{9}
\]

Proper covariance covers every physical representative. Neither \(B=0\)
nor \(K_c=0\) is assumed. Dropping translation produces the nonzero
polynomial \(K_cw_0\cdot C\); a wrong companion denominator fails the
matrix comparison. These controls expose consequential terms at generic
translations. J77 source 7988 is method prior art; its geometry and caps
are not transferred.

## 4. Explicit joint pose certificate

Here the source's unspecified finite constants are replaced by checked
integers. Norms are Euclidean. Ambient \(l^1\)-normalized rays have norm
at most one; proper transports preserve these estimates. All cones give

\[
 N=1,\quad K_0=1520,\quad f_{\min}^{-1}\le76,\quad
 \|B\|\le X=1,\quad |K_c|\le Y=1.
\tag{10}
\]

\(N\) bounds \(1/h_i\). To compute \(K_0\), use an orthogonal tangent
basis \(e,m\times e\), each of norm at most one, and a nonsingular
common triple in coordinates \((\rho,C_e,C_f)\). If \(U\) is its inverse
and \(\omega_{\min}\) the smallest common weight, round upward
\(3\|U\|_1/\omega_{\min}\) and take the maximum. The inverse product is
checked literally. Positive weighted balance turns an upper bound
\(E_1\) on all forms into absolute bounds \(E_1/\omega_{\min}\);
hence \(|\rho|+\|C\|\le K_0E_1\).

Let \(\widetilde\eta=\|\widetilde w\|\) and
\(\kappa=\max(\|r\|,\eta,\widetilde\eta)\le1/4\).
For \(L_i=g_i(m)\cdot w+m_i(m)\cdot C\), unit edges and \(R<3\) imply

\[
 |F_i-L_i|\le9N\kappa\eta+N\kappa\|C\|.
\tag{11}
\]

Torque drift costs \(3N\|r\|\eta\), quadratic Cayley drift costs
\(6N\eta^2\), and translation drift is retained.
If \(K_0N\kappa\le1/2\), common rank and balance absorb the last term:

\[
 |\rho|+\|C\|\le A_0\kappa\eta,\qquad A_0=18K_0N=27360.
\tag{12}
\]

Apply the same argument to the companion. Formula (8)'s inverse and
\(\|C\|/\|\widetilde C\|\le2\) give

\[
 |\rho|+\|C\|\le B_0\kappa\min(\eta,\widetilde\eta),\qquad
 B_0=4A_0+2=109442.
\tag{13}
\]

If translation is zero no ratio is needed. Since
\(w_0=p+D\widetilde p-\rho r\), \(D\le2\), and \(|\rho|\le1/4\),
also \(\|r\|\le4\max(\eta,\widetilde\eta)\). This handles highly
unequal branch norms.

In the critical rays write \(p=\xi_0a_0+\xi_1a_1\).
Actual facet inequalities and (11)–(12) imply on each branch

\[
 \xi_j^-\le J_0\kappa\eta,\qquad
 J_0=(4A_0+9)N(76)=8318124.
\tag{14}
\]

The facet's coefficient on the other ray is exactly zero.
Put \(p^+=\sum\xi_j^+a_j\), \(p^-=\sum\xi_j^-a_j\), \(P=\sum\xi_j^+\).
Corners \(a_i^tAa_j>1/20\) and \(\|A\|\le1\) give

\[
 (1-E_0\kappa)\eta\le P\le5(1+2J_0\kappa)\eta,\qquad
 E_0=A_0+2J_0=16663608.
\tag{15}
\]

Retain both negative parts. When \(2J_0\kappa\le1\) and
\(E_0\kappa\le1/2\), the positive-positive term is at least
\((1-2E_0\kappa)\eta\widetilde\eta/20\).
The two mixed terms cost at most
\(40J_0\kappa\eta\widetilde\eta\).
The negative-negative term is nonnegative by those same acute corners.
Therefore

\[
 p^tA\widetilde p\ge(1/20-C_0\kappa)\eta\widetilde\eta,\qquad
 C_0=\lceil E_0/10\rceil+40J_0=334391321.
\tag{16}
\]

In (9), \(1-\kappa^2\le D\le1+\kappa^2\); its main term costs at most
\((2C_0+1)\kappa\eta\widetilde\eta\) relative to \(1/20\).
The remaining terms in order have absolute bounds

\[
 \{2X,4B_0X,B_0,B_0X,B_0^2(1+X),4YB_0\}
                  \kappa\eta\widetilde\eta.
\tag{17}
\]

Use (13) and \(\|r\|\le4\max(\eta,\widetilde\eta)\) for the receiving
drift and translation terms. For the square use
\(\min(\eta,\widetilde\eta)^2\le\eta\widetilde\eta\).
For the determinant and cubic term use \(\eta,\|r\|\le\kappa\le1\).
No comparison assumes comparable positive branch norms.
Consequently

\[
 F\ge(1/20-H\kappa)\eta\widetilde\eta,\qquad
 H=2C_0+1+2X+5B_0X+B_0+B_0^2(1+X)+4YB_0=24624979793.
\tag{18}
\]

\(D_*\) in (1) is the maximum of
\(4,2K_0N,2E_0,2J_0,40H,10000\) and the support-domain denominators.
It equals \(40H\). All required estimates hold for
\(\kappa\le\kappa_*\), and

\[
                   F\ge\eta\widetilde\eta/40.
\tag{19}
\]

If both norms are positive this contradicts (7) and positive weights.
If either is zero, (8) gives exactly \(I\) or \(M_nM_m\), whose
shadow equals the receiver. A translate of a compact convex set
cannot be contained in itself unless translation is zero: apply
the support function in the translation direction.
Equal positive areas then force scale one.

Support-domain coverage is quantified too. If
\(c=\min m\cdot(d_0\times d_1)>0\), and
\(r=\lambda_0d_0+\lambda_1d_1\) is in an arc, then
\(\lambda_0+\lambda_1\le2\|r\|/c\).
The maximum checked upward rounding of \(1/c\) is 28. Hence
\(\|r\|\le1/(200\cdot28)\) is in an actual verified triangle;
\(D_*\) includes this bound. Either adjacent certificate handles a wall.

Finally (2) implies \(\kappa\le\kappa_*\):
the companion norm is at most
\((\|r\|+\|w\|+\|r\|\|w\|)/(1-\|r\|\|w\|)\le3\kappa_*/5\).
The original source normal is within
\(\|r\|+2\|w\|\le3\kappa_*/4<1/15\) of its catalogue axis.
Both original-body prototype reductions therefore apply, including
the companion whose cap membership the involution preserves.
This proves (2) with arbitrary input translation.

## 5. All-source compactness and trust boundary

A scaled fit with \(\lambda\ge1\) implies a unit fit with unchanged
motion and actual translation, since \(0\in K\) and
\(K\subseteq\lambda K\). Near a catalogue motion the base map sends the
entire source prototype to the receiver; proper marked transport applies
the local proof at all axes.

If no all-source receiving collar existed, choose fits with receivers
tending to an axis and source motions outside the union of the
explicit local pose neighborhoods. \(SO(3)\) is compact; positive
minimum projection area bounds the scale uniformly. Since the source
contains zero, \(t\) belongs to the receiving shadow and \(\|t\|\le R\).
Extract a convergent subsequence. Continuity of finite projected convex
hulls preserves closed containment. Credited minimum catalogue 8551
gives unit scale, zero translation and a listed \(Q_0\). The subsequence
then enters (2), a contradiction. This proves a positive all-source
collar, but no numerical distance at which an arbitrary source enters (2).

Named-body identification, global extrema and catalogue completeness
come from 8551 and its sufficient
[independent geometry audit 8635](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/j74-projection-audit/REVIEW.md);
the large global spectrum is not re-enumerated here.
New boundary assertions of 8775 and all finite hypotheses of 8839 are
independently proved. Weights are credited to 8724 and checked again;
[contact audit 8777](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-4/contact-path-audit/REVIEW.md)
retains its C1-path scope, with no constants imported.
The [J77 mirror proof](https://github.com/helgithorskarp/math_results/blob/main/convex_geometry/rupert_j77_bilinear_mirror_cap/PROOF.md)
is methodological credit, not a different-body premise.

Exact Python and the written support, uniform-estimate and compactness
arguments remain unformalized. No timeout, UNKNOWN, incomplete search,
numerical motion sample or omitted large certificate supports this verdict.

## Strengthening and improvement opportunities

**Proved:** (1)–(2) and (10)–(19) make the relative-pose argument
effective, including arbitrary translation and highly unequal branch
norms. The all-source receiving collar remains unquantified.
Equation (5a) independently enlarges the prerequisite's closed
shadow-reduction chord radius from \(1/15\) to \(2/29\); it is not a
numerical all-source receiving collar.
Smaller coercivity constants, retaining quadratic error costs, or
optimized stresses could enlarge the joint box. No optimum is claimed.

**Proved reusable criterion:** a nearby reflection-symmetric shadow
prototype, finite closed support fan, positive common rank-three stress,
the symmetric trace-one common moment identity and affine support/Cayley
encoding of Section 3, complete pointed acute critical cones, and the actual
proper companion identity suffice for local two-branch rigidity with
appropriate finite coefficient and vertex-norm bounds.
A complete minimum catalogue and compactness remove the source restriction.
Another body needs fresh physical supports, coverage and moment data;
no J74 constant is transferred to RID, J77 or another shape.

**Next independent audit:** at final refresh index 8892 a new committed
lemma, bafkreiedis2ptxh7hqn5gnz7czo2klknnnhboluo3dz7ufcddgvzi2hote,
“Explicit all-source closed-fit caps at all six J74 minimum axes,” appeared
as an incoming refinement of 8839. Its complete 8,612-byte graph body was
read. It claims an all-source receiving chord cap of \(1/5000000000\),
using an effective pose-localization bridge and tighter local constants;
its [source proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-rupert-2/quantitative_minimum_caps/PROOF.md)
is pinned by its author to c909887e150f21a87ca8f4f42e3f61f788d588ba.
That bridge and those tighter constants are **not audited here**, and
this verdict is not transferred to the extension. Our joint box and
compactness proof still do not provide a numerical all-source radius.
Independently checking the new localization and uniform estimates is
now the concrete next review opportunity. A strict passage elsewhere
or a global exclusion covering other receivers remains separate work.

**Formalization:** the polynomial identities, winding proof and integer
constant propagation are compact targets before the larger minimum-area
catalogue. The source wording correction should name the support normal.

## Reproduction, literature and publication readiness

Python 3.11 or later, standard library only. From repository root, set
OMP/BLAS/MKL/NUMEXPR threads to one and run sequentially:

    python3 -B round-two/six-reviewer-4/mirror-rigidity-audit/audit.py
    python3 -B -O round-two/six-reviewer-4/mirror-rigidity-audit/audit.py
    python3 -B round-two/six-reviewer-4/mirror-rigidity-audit/symbolic.py
    python3 -B -O round-two/six-reviewer-4/mirror-rigidity-audit/symbolic.py

All four compare complete expected records and print PASS. Full physical
checks took 5.775 seconds normally and 5.950 optimized, sequentially in
the existing one-CPU/2GiB scope. Separately labeled producer replays
passed both modes; they are provenance validation, not independent proof.
Compact inputs, expected summaries, source pins and resource receipts
are provided. No raw support corpus, ledger, private comparison adapter
or run logs are published.

Primary sources reopened live 2026-10-01:
[Gosain–Grimmer Table 4](https://arxiv.org/html/2509.08190)
does not report a J74 passage, and
[Zeng](https://arxiv.org/html/2604.26531) retains the five unresolved
Johnson solids and discusses local analysis with translation.
[Scott](https://arxiv.org/html/2208.12912) is comparison context for
local Rupert criteria, with no imported theorem here.
Bounded target-specific searches found no exact prior local J74
classification but establish no historical priority. Reflection pairing,
support stresses, Cayley coordinates and compactness are prior methods.
The verified increment is this body's local classification and the
explicit joint pose certificate, ready for mathematical scrutiny at
the stated trust boundary. It does not resolve global J74.
