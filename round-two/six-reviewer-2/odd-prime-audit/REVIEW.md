# Independent ordinary odd-prime audit and a sharp blue-page control

Reviewer: **six-reviewer-2**, role **independent mathematical reviewer**.
Date: 2026-10-01. The separate target selection, derivation and implementation
identify this reviewer; the shared campaign signing key does not establish
independent authorship.

## Target, verdict and exact scope

Target: six-books-2's **LEMMA 8810**,
`bafkreiawjbhlhlqjzcofnsyepidm2xj3pnqy4ltzoi22xawcambutadp2e`,
**R(B4,B7): ordinary order-seven obstruction; remaining group primes two
and three**. Its complete 19,698-byte body, four outgoing dependencies
and empty incoming neighborhood were read at index8829. The exact source
is **ede24e59395474df6f02cade83008a71bfa5f553**:
[original ordinary proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/odd_prime_symmetry/PROOF.md).
All eight files, total46,372 bytes, were extracted and their main/pinned
public bytes checked. The complete14,898-byte proof is embedded in the
graph body after six relative reader links are expanded to absolute URLs.

**Verdict: confirmed with high confidence for the new ordinary conditional
order7/13/17/19 theorem.** No mathematical gap was found in its fixed-point
counting, oriented correlation identities, scalar reductions, finite
three-set classification, equality arguments, phase normalization or
literal final book. The computation corroborates an ordinary proof; a
successful finite execution is not a premise of that theorem.

Here a valid graph is a simple red graph on22 vertices with at most three
common red neighbors at every red spine and at most six common blue
neighbors at every blue spine. Books are **ordinary, noninduced** subgraphs;
edges between pages are unrestricted. The conditional theorem assumes
maximum red degree at most ten and excludes automorphisms of each stated
prime order. It does not assume minimum degree eight or an edge count.

The group consequences have separate scopes. The conditional
\(|\operatorname{Aut}(G)|=2^a3^b5^c\) follows under the explicitly imported
[ordinary order-eleven theorem8767](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/order_eleven_correlation/PROOF.md),
source9d661fd0ac14a412f84c59a1cfa0315e73ada374. Its complete18,248-byte graph
body was read, but its entire proof/checker is not independently reproduced
or certified by this review. The logical prime/group bridge is correct.

For arbitrary valid22 graphs, the claimed \(2^a3^b\) corollary additionally
imports [maximum-degree theorem8012](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_b4_b7_degree11_gram_exclusion/PROOF.md)
and [order-five theorem8711](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/order_five_four_cycles/PROOF.md),
including [its fixed-point cases](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/order_five_four_cycles/FIXED_POINTS.md).
The full17,961-byte8012 and29,336-byte8711 graph bodies were inspected.
The former upper-degree assertion has the existing sufficient
[independent review8060](https://github.com/helgithorskarp/math_results/blob/main/book_ramsey_degree11_gram_review1/REVIEW.md),
`bafkreibor5a5i6qhsljhbabkuqgahgoy5ou3ts6gpnw27sexbiwtizzm2m`.
The order-five theorem retains its finite phase exclusion, regular
blue-codegree premise and the separate historical-classification-dependent
minimum-eight corollary. Those are real inherited premises of the combined
global consequence. This review confirms the derivation **under those
premises**; it does not independently audit their entire transitive chain.
No minimum-eight or historical-classification premise enters the new
order7/13/17/19 proof or the refinements below.

This restriction does not establish a22-point witness, exclude every
22-point host, or determine the Ramsey endpoint. The distinct109/108-edge
campaign claims are not premises.

## Independent ordinary audit

An order-seven permutation on22 points has cycle type
\(7^k1^{22-7k}\), with \(k=1,2,3\). Each fixed point has a uniform color
to every moving orbit. Maximum degree ten allows at most one whole red
seven-orbit at a fixed point.

For one moving orbit, let \(R\) be its red fixed neighbors and \(L\)
its blue fixed neighbors. A blue pair in \(L\) would have seven blue
pages, so \(L\) is a red clique. A red clique has at most five points,
because a spine in \(K_6\) has four red pages. Therefore
\(|R|\ge10\). A moving vertex's degree is \(|R|+s\), with even
internal degree \(s\), forcing \((|R|,|L|,s)=(10,5,0)\).
A blue moving pair now has five moving and five fixed blue pages.

For two moving orbits \(A,B\), partition the eight fixed points into
\(R_A,R_B,L\). A blue fixed pair must run between \(R_A,R_B\): every
other pairing shares a whole blue orbit. Thus each \(R\) is a red
clique, and \(L\) is red to all fixed points. Both \(R\)'s are nonempty,
otherwise all eight fixed points form a red clique. If their sizes are
\(a,b\) and \(|L|=z\), joined fixed degrees give
\(a+z,b+z\le4\), while \(a+b+z=8\). Hence \((a,b,z)=(4,4,0)\).
The joined fixed points use their full degree, so all \(R_A R_B\)
pairs are blue. An internal red moving edge would have four fixed red
pages, so both moving orbits are red independent. A blue pair in either
has five internal and four other-fixed blue pages. This closes both
fixed-rich cases without an enumeration or lower-degree premise.

### The three-cycle case and exact orientation

Let \(x\) be the unique fixed point. Its degree is a multiple of seven,
so it is zero or seven. If zero, a blue spine \(xy\) has
\(20-d(y)\ge10\) blue pages. Thus \(x\) is red to exactly one orbit,
called \(A\), and blue to \(B,C\).

Use common incrementing coordinates in \(\mathbb Z_7\). Let internal
inverse-symmetric connection sets be \(D_A,D_B,D_C\), with sizes
\(s_A,s_B,s_C\). Let \(P,R,Q\) be the arbitrary oriented red sets
\(A\to B,A\to C,B\to C\), with sizes \(m,n,q\). Reverse blocks
use \(-P,-R,-Q\); cross sets are not initially symmetric. Put
\(r_T(k)=|T\cap(T+k)|\). Ordered-pair counting gives
\(\sum_{k\ne0}r_T(k)=|T|(|T|-1)\), and \(r_{-T}=r_T\).

The red spine \(xa\) gives \(s_A\le3\), hence \(s_A=0\) or2.
The blue spines \(xb,xc\) give \(s_B+q,s_C+q\ge7\).
Degrees in \(B,C\) then imply \(m,n\le3\). If \(s_A=0\), a blue
internal pair in \(A\) has
\(19-2m-2n+r_P(k)+r_R(k)\ge7\) blue pages. Thus
\(D_A=\{\pm a\}\), and \(d_A=3+m+n\).

For a nonzero shift \(k\), put \(L(k)=r_{D_A}(k)+r_P(k)+r_R(k)\).
Red internal \(A\) spines give \(L\le2\); blue internal spines give
\(L\le2(m+n)-9\). Summing over the two red and four blue shifts yields

\[
m^2+n^2-9(m+n)+34\le0.
\]

For integers \(0\le m,n\le3\), only \((3,3)\) qualifies: outside that
corner the minimum is2 at \((2,3),(3,2)\). Consequently \(d_A=9\),
\(s_B=s_C=s\), \(q=7-s\), and \(d_B=d_C=10\). Total red edges
are105, and the degree profile is \((7;9^7;10^{14})\). No edge-count
or minimum-degree theorem was used.

In coordinates \(a,2a,3a\), the correlation of \(D_A\) is \((0,1,0)\),
so \(r_P+r_R\le(2,2,3)\). Every three-set in \(\mathbb Z_7\) has
one of the four correlation vectors
\((2,1,0),(0,2,1),(1,0,2),(1,1,1)\). Indeed, a repeated unordered
difference class makes the three points an arithmetic progression;
otherwise all three classes occur once. The progression has a unique
center and step class. There are seven progressions for each of the
three step classes, and fourteen remaining three-sets.

For an internal \(B\) spine, the red common-neighbor count is
\(r_{D_B}+r_P+r_Q\). On a blue spine it is also the blue page count:
both endpoints have degree ten and \(22-2-10-10=0\).
Its summed cap gives

\[
s(s-1)+6+(7-s)(6-s)\le3s+6(6-s).
\]

The left/right pairs for \(s=0,2,4,6\) are respectively
\((48,36),(28,30),(24,24),(36,18)\). Thus only2 or4 remain.

If \(s=2\), write \(D_B=\{\pm b\}\) and \(T=\mathbb Z_7\setminus Q\).
The red bound at \(b\) forces \(r_P(b)=r_T(b)=0\), because
\(r_Q=3+r_T\). The triple classification forces \(P\) to have step
class \(2b\). The blue bound at \(2b\) then makes \(r_T(2b)=0\),
so the two-set \(T\) has difference class \(3b\). The same reasoning
in \(C\) forces \(c=\pm b\) and gives \(R\) the same progression
class as \(P\). Their sum has a4, contradicting the \(A\) cap.

If \(s=4\), write \(D_B=\mathbb Z_7\setminus\{0,\pm b\}\), and
similarly for \(C\). Equality in the summed cap forces all six internal
inequalities to be equalities. In coordinates \(b,2b,3b\),
\(r_P+r_Q=(3,1,2)\). Its sole decomposition into the four triple
vectors is \((2,1,0)+(1,0,2)\). Thus \(P,Q\) have progression classes
\(b,3b\), and \(R,Q\) have classes \(c,3c\). If \(b=\pm c\),
\(P,R\) coincide in class, again giving a4. Otherwise their classes
are distinct. The three possible sums are \((2,3,1),(3,1,2),(1,2,3)\),
and only the last meets \((2,2,3)\). Hence \(P,R,Q\) have step classes
\(2a,3a,a\), and after exchanging \(B,C\),
\(b=\pm2a,c=\pm a\).

Multiply coordinates by \(a^{-1}\), then translate \(B,C\) to center
\(P,R\) at zero. These are actual relabelings; they neither restrict
the cross orientation initially nor discard the last free phase. The
complete remaining family is

\[
D_A=\{1,6\},\quad D_B=\{1,3,4,6\},\quad D_C=\{2,3,4,5\},
\qquad P=\{0,2,5\},\quad R=\{0,3,4\},\quad Q=h+\{0,1,6\},
\quad h\in\mathbb Z_7.
\]

For the red spine \(a_0c_k\), \(k\in R\), the \(A,C\) contribution
is2, and the \(B\) contribution is
\(f(k-h)=|P\cap(k-h+\{0,1,6\})|\).
Directly \(f=(1,2,1,1,1,1,2)\). Red cap three forbids
\(k-h\in\{1,6\}\). Since \(R+\{1,6\}=\mathbb Z_7\setminus\{0\}\),
all nonzero \(h\) fail. At \(h=0\), \(a_0b_1\) is blue and its
seven blue pages are
\(a_2,a_4,a_5,b_3,b_6,c_5,c_6\). This closes the final case.

### Larger primes and group quantifiers

For13,17,19, the only nonidentity cycle type on22 points is one prime
cycle with all other points fixed. A red fixed-to-cycle join would
exceed degree ten. All such joins are blue, so any blue pair of fixed
points would have the whole moving orbit as blue pages. Thus the fixed
points form a red clique. For13 that clique is \(K_9\), impossible.
For19 a blue fixed-to-cycle spine has \(18-s\ge8\) blue pages.
For17 it has \(16-s\le6\), forcing even internal degree \(s=10\).
Summing internal caps then gives the impossible inequality
\(90\le10\cdot3+6\cdot6=66\). These arguments cover all actions;
no connectedness, moving-orbit phase, or host classification is assumed.

The automorphism group is a finite faithful subgroup of \(S_{22}\).
Cauchy's theorem converts exclusions of prime-order elements into
exclusions of prime divisors. No prime greater than22 occurs in
\(22!\). With imported8767 the only allowed primes are2,3,5.
Orbit-stabilizer therefore permits precisely
\(1,2,3,4,5,6,8,9,10,12,15,16,18,20\) as orbit sizes at most22.
Only after importing8711 as well may one remove5 and use the smaller
list \(1,2,3,4,6,8,9,12,16,18\). These lists are necessary conditions;
no host or permutation-group sufficiency is asserted.

## Independent exact reproduction

[audit.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/odd-prime-audit/audit.py)
imports no researcher program. It constructs literal graphs as unions
of edge orbits, and computes correlations from unordered difference
inventories, independently checked against shift membership on all128
subsets. Its enumeration uses a factorization by the shared \(Q\) row,
rather than the author's scan of1,881,600 full templates.

The root-local domain exhausts16,384 \((D_A,P,R)\) choices, including
empty \(D_A\) and all cross sets of size at most three. The1470 surviving
keys all have sizes2,3,3. Independently generated compatible
\((D_B,P)\) keys per \(Q\) number0,147,294,0 for \(s=0,2,4,6\).
Joining the two outside lists and testing \(A\) makes15,435 joins and
recovers exactly2058 complete internal keys, all at \(s=4\).
Every candidate occurs: any graph determines its common \(Q\), both
outside keys and its \(A\) key. Repetitions are rejected.

Separately, the checker applies actual point permutations to all seven
normalized graphs: three step representatives, every pair of translations,
and optional exchange of \(B,C\). The resulting set of2058 actual keys
equals the factorized inventory entry by entry. Every key is rebuilt
as a22-point graph and all231 literal spines are checked. None satisfies
the caps. The first-violation split is882 red and1176 blue; it depends on
the chosen literal ordering and is not compared with the author's
search-dependent rejection counts. Inventory SHA256:
**2dce73618d81b05adc1537af4f5762f0fe5fdb33900025d34c6b3b4bcb0eccfd**.

For a genuinely feasible entry-level author comparison, a scratch copy
of the original verifier was instrumented only to export its already
constructed complete internal-key set. Every original mathematical
statement and search was unchanged. All2058 six-mask records agree
entrywise with this independent inventory. The instrumentation and
original hash are recorded in provenance. No author code is called or
imported by the independent checker. The full generated inventory is
regenerated in scratch and is not a hidden external input to reproduction.

All128 deliberately arbitrary oriented22-point controls, including all
eight fixed-incidence patterns, pass29,568 literal/formula/third-vertex
spine comparisons. All64 four-point graphs pass the independent literal
oracle. All56 inverse-symmetric degree-ten masks on \(\mathbb Z_{17}\)
obey the energy90 contradiction. All seven supplied books are checked
for color, complete page set and coverage. Six damaged book inputs, a
literal loop and three damaged inventories reject. The known primary21
fixture and \(KG(7,2)\) are positive controls, not new constructions.
The primary rows are exactly the off-diagonal complement of the fresh
original matrix, including its metadata-safe literal parsing.

Normal and optimized runs agree on their complete summary, full2058
records and phase-zero adjacency rows. Separately the original set and
bitset programs were replayed normally and optimized, reproducing both
complete expected summaries and their1,881,600-template supplementary
result. These author-algorithm replays are labeled separately from the
independent checks. The ordinary theorem does not require either scan.

## Strengthening and improvement opportunities

### Proved: the degree assumption can be localized in the three-cycle case

Suppose only the two page caps,22 points and cycle type \(7^3 1\) are
given, with unique fixed point \(x\). There is already a contradiction
under the weaker hypothesis

\[
d_R(x)<14,\qquad d_R(y)\le10\quad\text{for every }y\in N_B(x).
\]

Indeed \(d_R(x)\) is a multiple of seven, so it is zero or seven.
If zero, every other point is blue to \(x\), and
\(20-d_R(y)\ge10\) contradicts the blue cap. If seven, the ordinary
proof above uses the degree upper bound only on \(B,C=N_B(x)\): it
derives \(m,n\le3\) from their fixed-blue spines and degrees. No upper
bound on the seven red neighbors in \(A\) is needed. Their degree9
is then forced by the internal \(A\) inequalities. All subsequent
steps go through. Thus any hypothetical valid \(7^3 1\) action must
have fixed red degree at least14 or a blue neighbor of red degree at
least11. This is a localized refinement of this one cycle-type proof,
not a removal of the degree hypothesis for every prime or the entire
target theorem. It reuses and credits the author's mechanism.

### Proved: blue page cap six is sharp for the order-seven exclusion

The author's forced phase-zero graph, independently reconstructed in
[PHASE0.rows](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/odd-prime-audit/PHASE0.rows),
has22 points,105 red edges, degree profile \((7;9^7;10^{14})\), and the
actual order-seven action incrementing each orbit and fixing \(x\).
Its red page histogram is \(1:7,2:28,3:70\); its blue histogram is
\(5:14,6:98,7:14\). Thus it satisfies red cap three, maximum red
degree ten and blue cap **seven**. Replacing six by seven in the
order-seven component of the theorem makes that statement false.

There are33 spine orbits of size seven, covering all231 pairs; their
complete color/page table is in
[EXPECTED.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-2/odd-prime-audit/EXPECTED.json).
The only blue spines with seven pages are \(a_i b_{i\pm1}\), two whole
seven-orbits. The displayed connection sets give these counts directly
by membership in each of the three orbits and the fixed point.
Independent literal counting checks every physical pair and confirms
the table. This sharpness observation extracts a consequence of the
author's explicit phase, not a claim of first construction or an improved
Ramsey lower bound. It makes an essential hypothesis visible.

### Remaining directions and publication readiness

Removing the minimum-degree-eight import from the separate order-five
theorem requires new fixed-point reductions and complete additional
phase coverage; it is not achieved by the order-seven proof. A useful
next audit could isolate that historical trust boundary if independently
selected. The surviving order2/3 actions or asymmetric hosts still need
distinct construction/exclusion arguments. Orbit-size restrictions alone
do not imply a host census or the Ramsey endpoint.

The source is ready for scrutiny at the stated conditional scope. A
formalization would need the ordinary cycle-type coverage, oriented
correlation and equality bridges, unique progression centers and actual
phase relabelings. Checking output hashes alone would not formalize them.
No reproducibility or mathematical repair of the target was needed.

## Primary literature, priority and trust boundary

[Lidicky--McKinley--Pfender--Van Overberghe, Table1 and section3.3](https://arxiv.org/html/2407.07285v2)
and [Wesley, section3](https://arxiv.org/html/2410.03625v2) were reopened
this pass. Polycirculant/block-circulant correlation methods are prior
work. The former equal-size-orbit definition does not directly include
the fixed-point actions here; Wesley's stated complete critical-graph
enumeration does not include the B4/B7-on22 parameter. The current
[Small Ramsey Numbers TableIXa](https://www.cs.rit.edu/~spr/ElJC/sur.pdf)
and the first paper retain the located22..23 interval. The included
[primary21 construction](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
is known prior art. Candidate-specific searches for book/automorphism/
order-seven restrictions did not locate an earlier identical ordinary
statement; they do not establish historical priority. The phase-zero
sharp-cap example asserts no new adjacent Ramsey bound.

The important new ordinary proof belongs to six-books-2. This review
provides independent exact validation, the localized degree refinement,
and the explicit cap-sharpness consequence with credit. The underlying
family absence can also follow from the accepted minimum-eight result;
reducing that dependency is distinct from discovering the absence first.

The trust boundary is ordinary unformalized mathematics and CPython3.11.2
standard-library exact integer/set execution. There is no solver, floating
decision, incomplete-search absence claim or resource-failure premise.
The conditional group result additionally assumes8767. Only the combined
global group application imports8012/8060 and8711 with its named historical
and finite prerequisites. None of those imported computations was rerun
as part of this review. No unrestricted22-host census is claimed.

Independent normal/optimized runs took1.929/2.075 seconds, cumulative child
peak RSS24,152KiB. The four original author commands took at most1.539
seconds each, peak16,864KiB. All math jobs were sequential with numerical
threads one and fixed45-second external guards. No guard was hit. Full
inventories, temporary author exports and logs stay in scratch; the public
package contains only compact source, fixtures, expected summaries and
provenance.
