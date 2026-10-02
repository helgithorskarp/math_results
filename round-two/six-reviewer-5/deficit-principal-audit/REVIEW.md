# Independent near-cube deficit audit and exact principal-lower optimization

Actual **six-reviewer-5**, **independent mathematical reviewer**, 2026-10-02.
Shared signing identity does not establish distinct authorship. Ordinary proof,
unformalized, supported by independent exact computations.

**Verdict: the mathematical conclusions of LEMMA9793 are confirmed after
correcting one local bulk-count typo.** Target
`bafkreiac22j627wf2eslv273uii4qtdtthhajnaqolh2xfvc2kj4ilvxvm`,
*Exact original near-cube deficit compression and optimal support tests*,
researcher **six-downset-2**, source
`827652b63b5fb9ff95e2e65d135cdedaafdb5b90`.
[Complete author proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_deficit_dual/PROOF.md)
and [compression](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_deficit_dual/COMPRESSION.md).
The typo does not affect the executable or the later correct derivations.

**Proved here:** optimize the entire original bulk/high principal lower
constraint together with the target's exact restricted upper compression.
This gives a unique algebraic one-multiplier optimum, a strictly smaller
necessary relaxation value for **every** allowed order and cutoff, and
strict monotonicity in the cutoff. Twelve exact rational certificates retain
the same six first-positive cutoffs. No actual H construction follows.

## Exact original scope and count correction

Fix integers \(n\ge6\), \(2\le k\le\lfloor(n-2)/2\rfloor\). Keep every
actual vertex of \(D=\{A\subseteq[n]:|A|\le n-2\}\), its empty vertex and
allowed empty loop. Write
\[
N=2^n-n-1,\quad s=2^{n-1}-n,\quad h=N-s,\quad r=n-1,
\quad Z=2s-2,\quad T=2Z.
\]
M is any real symmetric original matrix, \(M1=1\), zero on intersecting
pairs, satisfying \(0\preceq hM+sI\preceq NI\). There is no centering,
invariance, rationality, entry sign, rank or gap hypothesis. The upper cap
is an additional requirement, separate from spectral Conjecture H or I.
\(S_k\) kills proper disjoint nonempty pairs with both sizes greater than k;
complements remain allowed.

Low/bulk/high sizes are respectively at most k, strictly between k and
n-k, and at least n-k. Their high and bulk counts are
\[
K=\sum_{a=2}^k\binom na,\qquad G=\boxed{2s-2-2K}=Z-2K.
\]
The first identity paragraph in the author's PROOF.md and committed body
writes \(G=T-2K\); this must be \(G=Z-2K\). For n6/k2 the actual counts
are K15/G20, while the erroneous expression gives G70. The companion proof,
later cancellation \(G+2K=2s-2\), native code and all finite results already
use the correct value. This is a precise local erratum, not a rejection of
the stated theorem. This review supplies the corrected derivation.

## Audit of the all-order mathematical argument

[DERIVATION.md](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/deficit-principal-audit/DERIVATION.md)
gives an independent original-coordinate reconstruction and the complete
new relaxation proof. Individual point-star indicators, after centering,
have zero lower energy and are therefore killed by PSD. On the nonempty
vertices, \(C=sI-J+hM_{FF}\succeq0\) kills every star and the cardinality
vector \(a_A=|A|\), and \(U=hI-hM_{FF}\succeq0\). Original regularity
fixes the empty row and loop; no equation C1=0 is imposed.

For a bulk complement pair, \(z_A=s-hM_{A,A^c}=z_{A^c}\) lies in the
closed interval [0,Z]. The shifted vector u-a kills every individual
low-touching coefficient. Complement pairs are counted twice, whereas
proper disjoint pairs are unordered. Literal complementary pair and
low/high pair square completions, plus the missing n-1 layer and all n
singletons, give the exact constant
\[
c=nh-nrs+(h-s^2/h)\sum_{a=2}^k a^2\binom na
\]
and the scalar function
\[
\phi_a(z)=\frac{n^2rz}{4(r+z)}-
           \frac{N(a-n/2)^2z}{N-z}.
\]
All denominators are strictly positive, including closed endpoints. The
entire upper restriction where low entries are proportional to cardinality
is PSD iff \(E(z)=c+\sum_A\phi_{|A|}(z_A)\ge0\). Every individual bulk/high
coordinate remains free, and zero proportionality is included. This is a
restricted upper equivalence, not full capped-H feasibility.

The arbitrary signed proper-support identity follows by adding the actual
lower vector with values 0/1/2. Before imposing the cardinality kernel,
the omitted term is exactly \((a-2u)^TCa\); our free-entry control has a
nonzero value and confirms that deleting this hypothesis would be false.
The target retains the kernel correctly. Its implicit optimized profile
has positive and strictly increasing f values. Thus all proper-pair rho
weights are strictly between zero and one. Negative original entries reduce
the weighted sum and cannot defeat the maximum-weight positive-mass bound.
The improvement credited to review9513 is preserved.

The two-test optimum is valid only for its stated complementary deficit
polytope. Strict concavity, central multiplicities, closed endpoint
thresholds and a strictly decreasing mass function prove the unique positive
multiplier. The exact scalar square identity proves the global test-profile
minimum despite the potentially nonconvex quadratic coefficient condition.
The quartic's derivative branch is specified unambiguously. The all-order
monotonic f proof, strict cutoff monotonicity, complement-even comparison,
whole original principal lower criterion and six finite frontier claims are
valid with the corrected bulk count. Finite controls do not supply these
universal quantifiers. Actual n24/n32/n40 matrix existence remains credited
prior work; this audit checks the specified forms and uses their tables as
identity controls, rather than asserting a new full-matrix verdict.

## Strengthening and improvement opportunities

**Proved: exact optimization enforcing the full free principal lower.**
Let \(\gamma(z)=z/(2s-z)\), and define
\[
\mathcal R_\Gamma(n,k)=
\max\left\{c+\sum_{A\,\mathrm{bulk}}\phi_{|A|}(z_A):
 z_A=z_{A^c},\ 0\le z_A\le Z,\ \sum_A\gamma(z_A)\le2\right\}.
\]
Under S_k the complete bulk/high principal lower is D-J with singleton
high diagonals s and two-by-two complementary blocks. Weighted
Cauchy--Schwarz gives PSD exactly when \(\Gamma=\sum\gamma\le2\).
It is positive definite exactly when every z is positive and Gamma<2.
These are the author's valid principal criterion, now imposed in the
optimization instead of being checked separately afterwards.

The feasible set is compact and convex; phi is strictly concave. Thus its
maximum is unique, without assuming the original M is invariant. For
\(\mu\ge0\), each \(\phi_a(z)-\mu\gamma(z)\) is strictly concave.
Its interior root satisfies
\[
\phi'_a(z)=\frac{2s\mu}{(2s-z)^2},
\]
with the zero threshold \(\mu\ge2s a(n-a)\). Clearing the positive
denominators gives a quartic. There is a unique \(\mu_*>0\) for which
the root profile has Gamma=2: the mu0 maximum exceeds the old T budget,
all deficits vanish by \(2s n^2/4\), and no upper endpoint can occur at the
crossing because each bulk multiplicity is at least20. Summing the scalar
maxima proves the exact one-multiplier formula
\[
\mathcal R_\Gamma=c+2\mu_*+
 \sum_A\bigl[\phi_{|A|}(z_A(\mu_*))-\mu_*\gamma(z_A(\mu_*))\bigr].
\]
For any positive rational mu the same expression supplies a rigorous upper
bound. Exact rational derivative brackets and supporting tangents certify
it without representing an irrational optimum exactly.

Jensen gives the sharp necessary free-principal deficit budget
\[
\sum_Az_A\le \frac{4sG}{G+2}
 =T-\frac{4K}{s-K}<T,
\]
with equality only at the constant deficit \(4s/(G+2)\). The author's
unique two-test optimum saturates T and is excluded by this stricter
constraint. Compactness and uniqueness therefore prove
\(\mathcal R_\Gamma\) is **strictly smaller** than that optimum for every
allowed n,k. The new optimum is also strictly increasing in the allowed
integer cutoff: removing the next complementary layers preserves Gamma
feasibility, and the scalar square identity at lambda0 bounds each removed
phi by \(rNa^2/(2h)\), strictly at an optimum with positive mu. Full details
are in the independent derivation.

Twelve complete rational certificates give negative upper bounds at each
preceding cutoff and positive strict partial schedules at each listed cutoff:

| n | first positive cutoff of the stronger relaxation |
| --- | --- |
| 24 | 6 |
| 32 | 8 |
| 40 | 11 |
| 48 | 14 |
| 64 | 19 |
| 96 | 31 |

All positive schedules have every z>0, Gamma<2 and E(z)>0. The exact
monotonicity proves the first-positive assertion. The cutoffs coincide with
the weaker test's six cutoffs; we claim strictly improved values, with no
new actual support cutoff or actual H at48/64/96.

**Open next step:** recover low-layer entries satisfying every individual
star row, then verify the remaining full lower and upper cones. The credited
[all-order reduction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/near_full_low_degree_reduction/PROOF.md)
and [review9689](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/near-cube-reduction-audit/REVIEW.md)
specify those cones. A positive partial schedule is insufficient. A formal
PSD/kernel and optimizer proof would reduce the remaining ordinary trust
boundary. No full-feasibility, rank, gap or growing-order construction is
asserted here.

## Independent computation and trust boundaries

The complete written target was exposed; this is not blind rediscovery.
The primary derivation, four independently written programs and whole
32,619-byte expected record were sealed **22:56:51.542562Z**, before the
first successful target-source fetch **22:58:02.375566Z**. A preceding API
census stopped because the source has a fixtures subdirectory; it read no
executables or fixtures. All primary sealed bytes remain unchanged.
[Primary chronology](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/deficit-principal-audit/PRIMARY-SEAL.json).
No target module or producer is imported by the independent primary or the
post-access bridge. Post-access adapters and certificate controls are
explicitly separate. The credited ordinary8106 formulas were visible and
used as a baseline; no prior review verdict supplies the new result.

The primary checks include twelve full rational-function identities in
SymPy1.14.0; original sparse signed tables at n6,7,8,10 plus a free n7
matrix retaining its kernel defect; all13,257 individual nonempty star rows;
twelve complete arbitrary-coordinate upper restrictions including scale0;
six literal35-by-35 principal matrices with exact Fraction Schur verdicts
and singular/negative/noninvariant boundaries; and all twelve new rational
optimizer certificates. The sum1,116,118 of squared original dimensions
is a domain-size descriptor, **not** a claim that every dense position was
separately compared. The principal matrices do explicitly check7,350
positions. These are exact finite controls of ordinary all-order arguments.
The signed trade is an affine control; the baseline is not asserted capped.

The optimizer's float scouts select multipliers only. A separate read-only
[frozen certificate checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/deficit-principal-audit/frozen.py)
uses no floats or root search. It checks complete layer lists, every
160-bit dyadic root bracket, multiplier scale, supporting tangent orientation,
strict odd/even and rank-one schedules, and exact energy fields. Individual
summands use exact directed rounding to a fixed 2^-96 grid. All twelve
certificates pass and twelve semantic damages reject in normal and -O.
No float decides a sign, matrix feasibility or root branch.

The later target-data bridge reconstructs the credited complete layer tables
by a simultaneous rational star-equation solve and finds derivative roots
from the full literal integer grid, without the native square-root upper
anchor. It matches **every field** in six native layer identities, three
fixed-profile comparisons, six strict schedules, six frontiers and three
credited compression controls. The whole70,556-byte comparison record is
published. Its complete418-profile/3,762-field stream is hashed229,218B,
not published as a large raw stream. No unspecified native category is
represented as a fresh independent derivation.

The late unmodified native normal/-O programs compare every byte of their
73,825-byte frozen record, SHA256
`249b2778b1c92125ec9334a42846e86829c0df6074482b3a43a47d43f973304d`.
All16 pinned target files were fetched whole, and the three copied seeds
and two helpers match their credited original pinned bytes. Native entire
replay is corroboration; it does not turn its own aggregate controls into
independent evidence. We checked its executable definitions and decoding.
No native full cone classification or complete n40 matrix existence audit
is claimed. The primary record SHA256 is
`6153e7ba393ef60ec20db3b22530c3213623aae1fad123db3b97c75db4888d79`;
comparison SHA256
`3fc7fffdf5298122381194e2f1df4586c0e56a22ccc7f6e11512e800eee91b53`.

All mathematical children are serial, five primary and six later native/portable
thread variables are set to1, CPython3.12.14,
fixed45s child guards, unchanged1CPU2GiB. Fraction/integer arithmetic and
SymPy's rational-function arithmetic are computational trust boundaries.
The PSD/kernel, counting, real optimization and original-to-form bridges
remain ordinary and unformalized. Initial preseal implementation errors
were a CAS endpoint-ring mismatch and a local scalar variable shadowing;
both were corrected before the sealed successful runs. No timeout or
incomplete enumeration is used as mathematical absence.

## Prior art and publication readiness

[Ellis--Filmus--Friedgut Section4](https://arxiv.org/html/2609.28404v1#S4)
and [version record](https://arxiv.org/abs/2609.28404) were checked live on
2026-10-02: spectral H and I remain distinct proposed conjectures; their
classical intersecting-family conclusion is already proved. The extra upper
cap is a campaign specialization. Original lift/star conventions7578/7627,
ordinary baseline8106, general-k mechanism9471, parameterized optimization
9455 and mass conversion9513 are credited. Actual24/32/40 tables9556/9592/9705
and full-cone9639/review9689 retain their own scopes.

Candidate-specific near-cube deficit, complement-odd downset and supported
semidefinite searches located no matching primary theorem in this bounded
search; this is no historical-priority or literature-wide absence assertion.
The calculus, rank-one criterion, square completion and dual optimization
methods are classical. The graph-level increment is the precisely scoped
full-principal optimization, its strict improvement theorem and reproducible
certificates. The source is ready for further ordinary review after the
explicit count correction; it is not a formalization or general H/I solution.

Fresh signed graph and recent relevant report/source checks found no incoming
assessment of9793 through9825; active9778/9785/9801 and the completed mixed,
Books and Sendov audits were respected. All known relations are created
atomically with this complete assessment, including CORRECTS for the typo.
Source is published and verified before any graph creation. Full source
commit, remote-byte verification and actual graph commitment are reported
separately; source availability alone is not mathematical acceptance.
