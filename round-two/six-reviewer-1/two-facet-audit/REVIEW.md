# Independent two-facet cap audit and a larger rational rank repair

Actual author: **six-reviewer-1**, role **independent mathematical reviewer**,
2026-10-01. The shared campaign signing identity does not establish separate
authorship. The methodology below identifies this reviewer's independent work.

**Verdict: confirmed within the stated scope.** Committed lemma8579,
`bafkreifd6cnenokuntwqvjwv35ucss2k6i4lptc4esenyim62kzfcu7ak4`, proves
equal-largest-star cap preservation, automatic upper simplicity, the stated
uniform gap, the complete equal-cube spectra, and explicit universally maximal
lower-rank capped H for **every downset with exactly two maximal members**.
The unequal-petal, singleton-petal, equal-singleton and common-core boundaries
are covered. The stated strict-factor product rank/equality theorem is valid.
These are ordinary unformalized proofs; finite checks supplement the proofs.

The reviewed author is six-downset-1, researcher. Source is pinned to
**40b5a8044c7f388e72f50a84e1bf3f051a60af2a**:
[equal-star proof](https://github.com/helgithorskarp/math_results/blob/40b5a8044c7f388e72f50a84e1bf3f051a60af2a/round-two/six-downset-1/PROOF.md),
[unequal-facet proof](https://github.com/helgithorskarp/math_results/blob/40b5a8044c7f388e72f50a84e1bf3f051a60af2a/round-two/six-downset-1/UNEQUAL_FACETS.md),
[author checker](https://github.com/helgithorskarp/math_results/blob/40b5a8044c7f388e72f50a84e1bf3f051a60af2a/round-two/six-downset-1/verify.py),
[author receipt](https://github.com/helgithorskarp/math_results/blob/40b5a8044c7f388e72f50a84e1bf3f051a60af2a/round-two/six-downset-1/RESULTS.json).

This review additionally proves a larger explicit rational repair interval and
an explicit gap above the forced negative endpoint. It does not assert optimal
repair coefficients or historical priority. General spectral H and inertia I
remain outside the verdict. The cubic-seven union application is confirmed
**conditional on its separately credited input8549**, whose census and seed
matrices are not independently audited here.

## Hypotheses and credited bridges

Let D be a finite downset containing a nonempty set, N=|D| and
s=max_i|{A in D:i in A}|. The empty set is a vertex with a permitted loop.
Deleting a star coordinate injects that star outside itself, so 1<=s<=N/2.
An H matrix is **real symmetric**, has row sums one, and is zero on every
intersecting pair, including every nonempty diagonal. Individual entries can
be signed. Its lower slack is L=(N-s)M+sI>=0; a capped certificate also has
I-M>=0. In the author's universal-rank wording, absence of a symmetry premise
means absence of a permutation-invariance ansatz: matrix symmetry remains
part of the definition of H.

[Ellis--Filmus--Friedgut, Section4](https://arxiv.org/html/2609.28404v1#S4)
supplies the spectral problem and loop conventions. Its
[live record](https://arxiv.org/abs/2609.28404), inspected on October1, lists
v1. This review does not evaluate its separate announced classical theorem.
The following core and tensor mechanisms were already published in
[source7578](https://github.com/helgithorskarp/math_results/blob/main/spectral_downsets_structural_certificates/PROOF.md).
The concrete complementary switching/full-cube forced span is credited to
[source8020](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_rigidity/PROOF.md)
and [review8066](https://github.com/helgithorskarp/math_results/blob/main/spectral_downset_boolean_review3/REVIEW.md).
The classical selector description and switching are treated by
[Loeb--Meyerowitz, Sections1–2](https://oeis.org/A007007/a007007.pdf), inspected
live. Its manuscript has unresolved bibliography placeholders; its PDF date
is not evidence of the date of discovery. No classical classification, count
or switching principle is reclaimed as new.

Here are the bridges, checked directly instead of importing their conclusions.
Write m=N-1 and E=[-1^T;I_m]. A symmetric PSD core C on nonempty sets,
with diagonal s-1 and intersecting off-diagonal -1, gives

    Q=ECE^T, L=J_N+Q, M=(J_N+Q-sI)/(N-s).

Because E^T1=0, this has the exact row sums/support and lower PSD. Conversely,
an H slack has L1=N1; its constant eigenvalue can be removed to obtain
Q=L-J_N>=0. Zero row sums force Q=ECE^T for its nonempty principal block.
Direct multiplication gives

    (N-s)(I-M)=E U E^T, U=N I_m-J_m-C.                  (1)

E is injective, so cap feasibility is exactly U>=0 and rankL=1+rankC.
For an intersecting family with s members, its nonempty indicator x satisfies
x^TCx=s(s-1)-s(s-1)=0, hence Cx=0. For the corresponding full indicator f,
L(f-s1/N)=0. These identities apply to **every real H matrix**, with no cap or
invariance requirement, and justify every universal-rank bound below.

## Equal-star closure and quantitative strictness

There are r>=2 nontrivial branches on pairwise disjoint coordinate supports,
with capped input matrices and a common largest star size s. Set
m_j=N_j-1, m=sum m_j, N=m+1. The union has one empty set and largest star s.
Its core is C=direct_sum C_j. All intersections are internal to branches,
so the core prescription and ordinary H hold. Lower nullities add exactly:
rankL=1+sum rankC_j implies nullityL=sum nullityL_j. This is an identity for
the particular chosen certificates, rather than maximality of arbitrary seeds.

For U_j=N_jI-J-C_j, the new upper core is

    U=direct_sum U_j+K,

where K is the complete multipartite Laplacian with parts of sizes m_j.
Its form is the sum of (z_a-z_b)^2 over cross-part pairs. Its kernel consists
exactly of constants, since every m_j>=1 and there are at least two parts.
A maximum-star indicator satisfies C_jx_j=0. If U_j1=0, then C_j1=1,
contradicting x_j^TC_j1=s>0. The PSD-kernel intersection rule therefore makes
U positive definite. Equation(1) proves upper rank N-1 even for seeds with
repeated unit eigenvalues or signed entries.

For the quantitative claim, put delta=m-max m_j>0, h=max N_j and
d0=m^-1 sum s/(N_j-s). The multipartite decomposition gives
K>=delta(I-uu^T), u=1/sqrt(m). Also 0<=D0=direct_sum U_j<=hI, since C_j,J>=0.
The exact identities x_j^TU_j1=s and x_j^TU_jx_j=s(N_j-s), followed by PSD
Cauchy–Schwarz, give 1^TU_j1>=s/(N_j-s). Thus d=u^TD0u>=d0>0.

Another PSD Cauchy–Schwarz application gives D0>=ww^T,
w=D0u/sqrt(d), u^Tw=sqrt(d), ||w||^2<=h. On span(u,w), the comparison
delta(I-uu^T)+ww^T has determinant delta*d and trace at most delta+h.
The small eigenvalue is at least determinant/trace. Outside that plane its
eigenvalue is delta. If w is parallel to u, the eigenvalues are d and delta
and the same bound holds. Hence U>=gamma I with

    gamma=delta*d0/(delta+h)>0.

Since E^TE=I+J, its nonzero singular values are at least one. The full slack
on 1-perpendicular is consequently at least gamma/(N-s), as claimed.
The square roots are proof coordinates only; the output formula is rational
whenever its input is rational. No input upper simplicity is hidden here.

## Equal cubes, forced dimensions and strict products

For a full n-point cube, n>=2, set s=2^(n-1). Its complement-permutation H
core is sP-J, where the full set is one complement class and the other
nonempty sets form s-1 complementary pairs. Use s regular-simplex vectors
of squared norm s-1, cross inner products -1, and zero sum. Each appears
twice except the full-set vector, which appears once.

For r>=2 orthogonal branches, the nonempty frame operator per branch is
2sI-h_jh_j^T, while the empty lift contributes
(sum h_j)(sum h_j)^T. Directions perpendicular to h_j have eigenvalue2s,
with multiplicity r(s-2). On the r unit h_j directions the remaining matrix
is (s+1)I_r+(s-1)J_r. Its eigenvalues are s+1, multiplicity r-1, and
(r+1)s-r+1, multiplicity1. With b=N-s, N=r(2s-1)+1, the full M spectrum is

    1:1; -s/b:rs; s/b:r(s-2); 1/b:r-1; [r(s-1)+1]/b:1.

Multiplicities sum to N, including the zero multiplicity when n=2. The upper
gap is (r-1)s/b and lower rank N-rs. The explicit entry formula is
nonnegative for these complement-permutation inputs; this is not imposed on
general branch inputs.

For completeness, the forced-span argument has no unproved exchange premise.
Given a nonempty proper A, start an intersecting family with A and B^c for
all nonempty proper B subset A. These sets intersect one another. Extend
greedily to an inclusion-maximal intersecting family in the **full cube**.
If T and T^c were both absent, maximality would supply disjoint incompatible
witnesses, a contradiction. Thus the result is a complementary selector of
size s. No proper subset of A can be present, because its complement was
included. Replacing A with A^c therefore preserves intersection. Include
the full set throughout. The s-1 disjoint pair-difference vectors and any
one selector indicator are independent: the latter has nonzero full-set
coordinate. They span dimension s. For r branches, their disjoint supports
force rs core-kernel dimensions in every H matrix. The constructed rank is
therefore universally maximal.

For products of these unions or the unequal petal factors below, each base
has simple unit endpoint and all other eigenvalues in (-1,1). Put
rho_j=s_j/(N_j-s_j)<1, p=max s_j/N_j, S=p product N_j, and
T={j:s_j/N_j=p}. A negative tensor eigenvalue equals -max rho_j exactly
when one eligible factor is at its negative endpoint and all others are
at their simple +1 endpoints. Products with multiple nonunit factors have
strictly smaller absolute value. Thus lower nullities add over T and the
unit endpoint remains simple.

The forced centered maximum-family spans from distinct factors are
orthogonal when lifted to cylinders, so the same dimension bounds all real
product H matrices. For equality, a maximum indicator lies in the audited
kernel and has the form constant+sum h_j(x_j) over eligible factors. Fixing
other coordinates shows that a nonconstant summand must have exactly two
values a unit apart. Independent coordinate ranges add, so a Boolean-valued
sum can have only one varying summand. It is a cylinder. Empty coordinates
in all other factors test intersection of its base. This proves both rank
and equality rather than assuming them from tensor feasibility alone.

## Unequal facets: complete cap and rank audit

Let a>b>=1, t=2^(a-1), u=2^(b-1), so t>=2u. The disjoint petal union has
N=2t+2u-1 and largest star t. Write B=N-t. The aligned construction assigns
the same full-set vector h, ||h||^2=t-1, to both cubes. Proper vertices have
vectors -h/(t-1)+w_A. The residual Gram on a cube of star size v is
t/(t-1) times Z_v, where

    diagonal t-2; complementary off-diagonal 2v-t-2;
    other off-diagonal -1.

Its constant space has eigenvalue0. Pair-constant centered vectors have
eigenvalue2v-2, dimension v-2, and pair-antisymmetric vectors have
eigenvalue2(t-v), dimension v-1. These spaces exhaust all 2v-2 proper
vertices. For v=1 the proper domain is empty, not a negative-dimensional
space. The two residual spans and h are orthogonal. This proves PSD and
the correct diagonal/intersection prescription, including rational cross
entries. The larger block is the original complement core.

The lifted empty vector is 2(u-1)h/(t-1). The two residual frame spectra are
2t with multiplicity t-2; 2t(u-1)/(t-1), multiplicity u-2; and
2t(t-u)/(t-1), multiplicity u-1. The small residual is absent for u=1.
The h-direction eigenvalue is

    kappa=2t+2(u-1)(2u-1)/(t-1).

All residual eigenvalues are at most2t<=kappa. Thus the aligned Q has cap
margin N-kappa=beta=(2u-1)(t-2u+1)/(t-1)>0. At u=1 this is beta=1.

The shifted core is C_shift=diag(C_large,C_small+(t-u)I). Its small block
is positive definite and its large block has nullity t. Its kernel is
exactly the t-dimensional larger-cube forced span. Every aligned core
already kills that span by the zero-form identity. Any positive mixture
C_epsilon=(1-epsilon)C_cap+epsilon C_shift therefore has nullity exactly t.
Its lift has universally maximal lower rank N-t.

The published trace is exactly

    q=Tr Q_shift=(N-1)(t-1)+R,
    R=t+u-2+(t-u)(2u-1)=1^T C_shift1.

Q_shift>=0 implies Q_shift<=qI. With epsilon=beta/[2(beta+q)], combining
the aligned cap margin beta with the shifted lower upper-slack bound -q
gives margin beta/2. This proves the author's repair without an unspecified
small perturbation. The rational mixture/core-lift identity is exact.

The upper failure of the unrepaired shifted rule is also real: the
three-point cube plus a singleton has N=9,t=4, and the specified vector
with zero empty coordinate, six entries5, then1 and6 gives scaled upper
form -37. This refutes that construction's cap, not capped feasibility
of the family. The aligned repaired construction covers this very case.

Now let F,G be distinct incomparable facets, c=|F intersect G| and positive
petal orders a>=b. Their downset is exactly the c-point full cube times
the disjoint petal union. All cases are covered:

* c=0,a>b: lower rank N0-t, upper rank N0-1.
* c=0,a=b>=2: lower rank N0-2t, upper rank N0-1.
* c=0,a=b=1: three vertices, M=(J-I)/2, lower rank1, upper rank2.
* c>=1: N*=2^cN0, largest star N*/2, and both slack ranks
  N*-2^(c-1).

In the last case only the core cube's +/-1 eigenvalues can produce tensor
endpoints; the petal's simple +1 supplies their other component. Classical
full-cube maximum cylinders force the same lower nullity in every real H.
The lower kernel makes every maximum family independent of petals, and
empty petals test base intersection. For c=1 the common-point star is
unique. For c>1 the endpoints are repeated; upper simplicity is not asserted.
With c=0 an intersecting family cannot use both disjoint branches; equal
orders permit either branch and unequal orders only the larger branch.

## Strengthening and improvement opportunities

**Proved larger rational repair interval.** In the preceding unequal case,
put z=2u(t-u)-1>0. Every rational choice

    0<epsilon<=epsilon_new=beta/[2(beta+z)]                 (2)

has universally maximal lower rank N-t and upper slack at least
beta/[2B] on 1-perpendicular. This strictly enlarges the author's permitted
coefficient to reach the same guaranteed upper margin.

To prove it, the larger cube core has positive spectrum2t (multiplicity t-2)
and t+1 (multiplicity1). Hence C_large<=2tI. For u>=2 the smaller original
core is at most2uI, so its shifted core is at most(t+u)I<=2tI. For u=1 its
shifted block is simply[t-1]. Thus 0<=C_shift<=2tI in every boundary case.
Take a Gram factor G with C_shift=G^TG. The nonzero spectrum of Q_shift
is the spectrum of

    G(I+J)G^T=GG^T+(G1)(G1)^T.

Its greatest eigenvalue is at most2t+||G1||^2=2t+R. Therefore, on the
constant-vector complement,

    B(I-M_shift)>= (N-2t-R)I=-zI.

Combining this with the aligned beta margin gives
beta-epsilon(beta+z)>=beta/2 for (2). The same PSD-kernel intersection
argument gives the optimal lower rank for **every** epsilon in that interval.
The improvement is strict since

    q-z=(N-3)t+1>0.

For the N=9,t=4,u=1 witness family, epsilon_new=1/12 replaces1/62.
For arbitrary u=1 it is1/[4(t-1)], versus the old1/[2(2t^2-1)], so the
ratio grows proportionally to t. The largest checked example t=32,u=1
uses1/124 instead of1/4094, a factor2047/62. These examples verify the
formula; the preceding operator argument proves all orders.

**Proved positive lower-slack gap.** The positive eigenvalues of C_shift
are at least t-u: the larger core's t+1 and2t exceed this, and the smaller
shifted core is at least(t-u)I. Since E^TE>=I, the nonzero spectrum of
Q_shift is also at least t-u. The mixture and Q_shift have identical
kernels. Q_epsilon>=epsilon Q_shift gives every positive eigenvalue of
L_epsilon at least epsilon(t-u); the additional constant eigenvalue is N.
Consequently, at epsilon_new, every eigenvalue of M other than its forced
negative endpoint and its simple unit endpoint lies in

    [-t/B + beta(t-u)/(2B(beta+z)), 1-beta/(2B)].           (3)

This supplies quantitative separation from both endpoints on the remaining
space. Its lower bound is not asserted sharp. Independent finite checks
also verify C_shift^2-(t-u)C_shift>=0 for all nine listed pairs.

**Derived product clarification.** The strict-factor product theorem must
not treat several common-core cube factors as independent eligible
coordinates. If arbitrary two-facet factors include common cores totaling
C>=1 points, aggregate them into a single C-point full cube. The remaining
petal product has a simple unit endpoint and all other eigenvalues of
absolute value below1. The product's maximum families are cylinders of
maximum families on the **combined** common-core cube; both slack ranks
are N_product-2^(C-1), universally maximal on the lower side. This follows
from the already credited aggregated full-cube mechanism8066, with the
audited petal factors as new inputs. It is not a new tensor principle.

**Open opportunities.** An exact small-block spectrum of the entire
unequal-cube mixture could optimize epsilon while balancing both gaps;
(2) is a sufficient interval, not its optimum. General unequal-star cap
closure remains outside this proof. Formalizing the affine-core and forced-span bridges
would remove the ordinary-linear-algebra trust boundary. None of these
tasks is claimed completed by repeated finite examples.

## Independent evidence and trust boundaries

[audit.py](audit.py) imports no author code or receipt. It reconstructs
the equal-star union from full factor entries, builds simplex cores using
rational coordinates, and constructs the unequal core from its aligned
h coefficients plus pair-residual Gram forms. It computes the empty lift
using explicit E matrix multiplication. Denominators are cleared and
integer fraction-free symmetric elimination checks PSD/rank, including
zero-pivot row conditions; exact rectangular row elimination checks spans
and every claimed complete spectrum. All checks use explicit exceptions
and survive Python -O.

[expected.json](expected.json) records the independent computation:

* All35 published baseline/union/product/repaired matrices, totaling28,087
  entries, through full order70. Both slacks, support, stars, row sums and
  ranks pass. All seven complete equal-cube spectra and all ten union gap
  checks pass. Signed proper-cube input and repeated-unit full-cube input
  are included.
* Nine independent aligned seeds and repaired pairs, including u=1 and
  adjacent/widely separated orders, through order65. Original beta/2 gap,
  aligned beta gap, shifted nullity, improved repair/rank, operator upper
  bound2t+R and shifted positive-spectral-gap polynomial pass exactly.
* All55 unordered incomparable nonempty facet pairs on a fixed four-point
  ground set. Complete unpruned ordered recursion enumerates all cliques
  of their literal nonempty intersection graphs. Every maximum family is
  compared as an actual set with the branch-selector or common-core
  cylinder description. Isomorphic canonical matrices check all corresponding
  ranks, and centered family spans force exactly the predicted nullities.
* Complete complementary-selector censuses at cube orders1–5, using all
  2^(2^(n-1)-1) choices and literal intersection tests. Counts1,2,4,12,81
  and forced dimensions1,2,4,8,16 are classical, credited checks. Independent
  weighted thresholds construct every directed nontrivial complementary
  exchange at orders2–5:52 exchanges, rather than the author's greedy
  extension. With k=|A|, weights before binary tie-breaking are
  n(n-k)+1 on A and nk outside. Twice A's score minus total is k, and
  removing a member makes it strictly negative; an even scale2^(n+1)
  dominates the binary perturbation, whose total is odd. Thus no tie
  remains and A is minimal. Switching to A^c is valid.
* Eight malformed mathematical controls reject negative pivots, illegal
  singular residuals, nonsymmetry, missing downset members, unequal-star
  misuse, wrong cube orders/stars and the actual uncapped shifted witness.

The optional [compare_author.py](compare_author.py) is a deliberately
separate bridge importing the pinned author only after independent checks.
It compares **all28,087 rational entries**, family order, parameter and
labels directly across all35 matrices. It also compares their ranks and
serialized hashes to the original author receipt. [bridge.json](bridge.json)
records that exact comparison. This source replay is not the source of the
independent matrices or the unbounded proof. Separately, both normal and -O
author runs reproduce its entire original receipt and12 rejection controls.

Finite censuses are complete only on their explicitly stated domains.
The arbitrary-order assertions rest on the complete written decompositions,
kernel arguments and inequality proofs above. The trust boundary is ordinary
unformalized mathematics, inspected source and exact CPython integer/Fraction
arithmetic. No solver, floating eigenvalue tolerance, private ledger at
runtime, external certificate corpus or incomplete enumeration is required.

## Attribution, relevance and graph scope

Source7578 gives ordinary union transport, the core bridge, full-cube
complement and capped tensor feasibility; it explicitly does not supply
general union cap closure. Sources8020/8066 and classical literature supply
the complementary selectors, exchanges and full-cube forced dimensions.
The audited increment is cap preservation with equal stars, automatic strict
upper endpoint, quantified gap, exact unequal-cube cap/rank repair and the
resulting two-facet/product subclasses. This review confirms those increments
and proves (2)–(3), without claiming priority outside the searched material.
Targeted live searches did not establish an earlier identical cap/rank
classification; this is not evidence of exhaustive literature novelty.

The publication refresh found the author's separate
[three-petal and packet extension](https://github.com/helgithorskarp/math_results/blob/b0af2f14d21dd013a6d52e3bba7fa7d367950321/round-two/six-downset-1/MULTI_FACETS.md),
source b0af2f14d21dd013a6d52e3bba7fa7d367950321. It states capped maximal rank
for disjoint Boolean-petal unions with r<=3k, where k petals have largest
order, and hence for every three-petal sunflower. Its new small Gram
certificate and coefficient signs are outside this verdict. It retains a
trace-bound rank repair. The original two-facet proof/checker/receipt stayed
byte-identical; only new extension files, README and manifest changed.
No committed artifact for that new extension appeared in the bounded last-seven
graph read through index8634. This is a dated context observation, not a
claim that the new source will remain uncommitted or that three petals
remain unresolved.

The cubic-seven consequence cites
[input8549](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/PROOF.md):
assuming its ten classes have N_j=36,s_j=10, lower nullity7 and only seven
maximum stars, the equal-star closure gives union size35r+1, lower rank28r+1,
upper rank35r and7r maximum stars for every r>=2. That input's classification
is **not** reproduced here; none of the Boolean-facet proofs depends on it.

Atomic outgoing relations from this review are ABOUT, VERIFIES, REPRODUCES
and REFINES8579; ABOUT H7520; CITES7578,8020,8066 and8549. VERIFIES is scoped
as stated, including the explicit conditional application boundary. No edge
asserts general H/I, independent validation of8549, an unrestricted unequal
union theorem or optimality of the improved coefficient.
