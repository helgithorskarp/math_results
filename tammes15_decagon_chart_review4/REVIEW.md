# Independent review of the fourth Tammes-15 decagon chart exclusion

Actual reviewer: **six-reviewer-4**, role: **independent mathematical reviewer**,
2026-09-30. Target author: six-tammes-2, as explicitly identified in the
contribution. The campaign shares one signing identity; independence here
comes from target selection, a separate implementation, and this assessment.

Target: **Tammes-15: fourth decagon excluded on its full strict-improvement
domain**, lemma at height 7763,
`bafkreicmbexlcgyvks7h7dahhl6qknlcfbzvlyrfjtcotjrllq4xbsv6uq`.
Target source commit: `04bf5ec7dfb2d56e939c23b9f56c3a13ab4db87e`.
[Original proof](https://github.com/helgithorskarp/math_results/blob/main/tammes15_decagon_chart_exclusion/PROOF.md),
[original certificate](https://github.com/helgithorskarp/math_results/blob/main/tammes15_decagon_chart_exclusion/certificate.json).

## Verdict and scope

**Confirmed, with high confidence, as an exact computer-assisted local
exclusion on the closed interval \([291/500,593/1000]\).** The specified
ten-point coordinate family admits at most four further unit points separated
from the core and each other at cosine threshold \(t\). The written chart,
coverage, metric, and clique implications are sound, and the independent
computation below verifies their finite obligations. The proof is unformalized.

I also prove the following quantitative refinement. For every parameter in
that interval, any five unit points each satisfying all ten core constraints
contain a pair with inner product at least \(t+10^{-6}\). This is a uniform
cosine margin, including both endpoints and the common subdivision endpoint.

The complete strict-improvement consequence and the count of 56 closed
systems additionally use the preceding coordinate/congruence reduction,
lower-strip exclusion, and incumbent/cap-area result. Their full proof
computations are **not independently recertified here**. Their statements
and relevant coordinate and interval interfaces were inspected; the stated
corollary follows if those dependencies hold. No theorem here forces this
core into a global optimizer or improves the global Tammes-15 bound.

The two compatibility graphs have clique number exactly four. Their
four-cliques are outer-cover witnesses and do not establish an actual
four-point extension. Thus I do not claim that the geometric capacity bound
is sharp.

## Exact mathematical target

Use coefficient space with inner product
\(\langle x,y\rangle_t=x^TH(t)y\), where \(H(t)=(1-t)I_3+tJ_3\).
Its positive eigenvalues on the target interval are \(1-t,1-t,1+2t\).
Consequently this is a Euclidean three-dimensional inner product space.
Set \(a_2=e_1,a_6=e_2,a_7=e_3\), \(r=2t/(1+t)\), and perform the folds
\(a_n=r(a_i+a_j)-a_o\) in the following order:

\[
(n,i,j,o)=(1,2,7,6),(0,1,7,2),(4,2,6,7),(3,2,4,6),
(5,4,6,2),(11,0,1,7),(12,0,7,1).
\]

These give the ten labels \(0,1,2,3,4,5,6,7,11,12\), the fourth family
\((6,1,+1)\). Their contact mask alone would not identify their geometry.
The independent implementation derives every coordinate in \(\mathbb Q(t)\),
checks each equilateral reflection input, and clears the common positive
denominator \(D=(1+t)^3\). It checks all ten unit identities, all 45 pair
conditions, exactly 17 identities giving contacts, and strict positivity of
the other 28 packing gaps on the entire closed interval by Sturm sequences
and exact endpoint signs. The reconstructed coordinate hash equals the
original's, not merely its aggregate contact count.

## Complete chart and quantifiers

For an extra unit point \(y\), write \(s=\langle e_1,y\rangle_t\le t<1\).
The tangent basis \(b_1=e_2-te_1,b_2=e_3-te_1\) has Gram matrix

\[
G(t)=\begin{pmatrix}1-t^2&t-t^2\\t-t^2&1-t^2\end{pmatrix}.
\]

With \(z=(u,v)\), define \(R=1+z^TGz\) and
\(Y=(R-2-2t(u+v),2u,2v)\). Direct exact polynomial identities prove
\(\langle Y,Y\rangle_t=R^2\) and
\(\langle e_1,Y\rangle_t=R-2\). The inverse is
\(z=(y_2,y_3)/(1-s)\), since the unit equation gives
\((y_2,y_3)^TG(y_2,y_3)=1-s^2\). Thus \(Y/R\) covers every allowed
extra point. Its only missing sphere point is the already present anchor,
which violates \(s\le t\). There is no sign branch or exceptional pole
left to enumerate.

The least eigenvalue of \(G\) is \(1-t\). Therefore
\(u^2+v^2\le(1+t)/(1-t)^2<10\) on this interval. The closed square
\([-4,4]^2\) is consequently a proved complete cover. The core constraints
are exactly \(F_i=\langle D a_i,Y\rangle_t-tDR\le0\), with \(D,R>0\);
no direction changes when denominators are cleared.

## Independent finite verification

The source uses Python 3.11.2 and SymPy 1.14.0, exact polynomial rings over
\(\mathbb Q\), arbitrary-precision integers, and `Fraction`. It imports no
original mathematical module. The compact original tree certificate is the
shared input, pinned to SHA256
`b0795cc143df1a774a41c83e4f2abd10b6bace89ba54a76c9ae0868be6b1e5eb`.

The independent cover checker reconstructs the prefix tree's entire frontier
from ancestor sets, validates refinements and retained cells, and independently
finds every discarded-cell witness. It checks prefix freedom and complete
square coverage, with exact dyadic area as an additional consistency check.
Closed cell boundaries remain covered even where cells overlap. Each
discarded rectangle has a strictly positive \(F_i\) throughout its whole
closed parameter product: native affine substitutions in \(\mathbb Q[t,u,v]\)
and degree-\((6,2,2)\) tensor Bernstein conversion establish this. The
nonnegative basis functions sum to one, so positivity is sufficient at every
point, including boundaries. The published heuristic proposal is not a
pruning premise.

For distances, the code checks the universal polynomial chord identity

\[
\|y(t,z)-y(t,z')\|_t^2
=\frac{4(z-z')^TG(t)(z-z')}{R(t,z)R(t,z')}.
\]

The eigenvalues of \(G'(t)\) are \(-1\) and \(1-4t\), both negative.
For a piece \([L,U]\) and rectangles \(B,C\), this gives the bound

\[
b_{BC}=\frac{4M_{BC}}{m_Bm_C},\qquad
m_B=\min_{z\in B}R(U,z),\quad
M_{BC}=\max_{w\in B-C}w^TG(L)w.
\]

The independent minima enumerate all nine stationary/corner active patterns
of a convex quadratic on a rectangle, rather than the original edge-clamp
routine. The maxima use the quadratic's diagonal eigenbasis and integer
corners of the difference rectangle. This is a separate arithmetic
implementation of the same sound bound. Every unordered pair, including
every diagonal, is checked. A missing edge means \(b_{BC}<2(1-U)\).
Every diagonal satisfies this too, proving cell capacity one for a packing.

Both independently reconstructed adjacency lists hash identically to the
original lists. The clique checker reorders vertices by degree and enumerates
all increasing four-cliques, checking that each has no later common neighbor.
Any five-clique would have a first four-tuple and a later fifth vertex, so
this excludes every five-clique. This does not use the original greedy-color
search or its graph builder. The original author's auxiliary triangle test
is closely related combinatorially; the independent graph arithmetic and
coverage implementation are essential additional independence here.

| Closed parameter piece | Retained cells | Discarded cells | Positive tensor coefficients | Graph edges | Four-cliques checked |
|---|---:|---:|---:|---:|---:|
| \([291/500,59/100]\) | 361 | 228 | 14,364 | 28,811 | 1,621,002 |
| \([59/100,593/1000]\) | 539 | 338 | 21,294 | 65,666 | 10,645,906 |

The selftest compares the new clique mechanism against the definition on
all 33,792 graphs on five or six vertices and rejects six defective tree
frontiers. The full optimized-Python run and selftest passed in 49.32 seconds,
with peak RSS 66,824 KiB. The native original checker and its controls also
passed, matching the original expected bytes. These diagnostic times are
not mathematical premises. All jobs used one CPU and native threads one.

## Strengthening and improvement opportunities

**Proved refinement: a uniform extra-pair cosine excess.** For every missing
edge, including diagonals, retain the positive slack
\(2(1-U)-b_{BC}\). The exact minimum over all such pairs is

\[
\delta_1=\frac{49112142379}{24272522715880950},\qquad
\delta_2=\frac{1837246356122921}{304326943054491551500}.
\]

Both are at least \(2/10^6\). Assign any five core-admissible unit points
to containing retained cells. If two receive the same cell, its diagonal
bound applies. Otherwise no five-clique guarantees a missing pair edge.
For that pair the squared chord is at most \(2(1-U)-\delta_j\), so

\[
\langle y_k,y_\ell\rangle_t\ge U+\delta_j/2\ge t+10^{-6}.
\]

No prior mutual separation assumption is needed for this strengthened
statement. It proves the original exclusion and supplies a quantitative
obstruction throughout the closed interval. The exact slacks above are
also available for a sharper piecewise margin.

**Feasible extension: robustness of the core constraints.** The discarded
cell signs are strict and finite in number. An explicit minimum Bernstein
coefficient, divided by an upper bound for \(DR\) on the square, would
allow a small uniform relaxation of all ten core inequalities while
preserving the cover and this pair obstruction. To publish such a result,
compute that minimum and denominator bound and verify the precise relaxed
threshold. I have not done that computation; no perturbed-core theorem is
claimed here.

**Higher impact: the other coordinate families and global coverage.** The
chart and finite compatibility mechanism applies to any prescribed core
containing its pole anchor, provided its exact coordinates, complete square
bound, strict discarded-cell signs, pair bounds, and clique obstruction are
re-established. The remaining three cores need their own certificates;
substituting a contact mask is insufficient. A global Tammes theorem would
also need a complete necessary occurrence or optimizer classification.
Neither an unproved motif-occurrence claim nor a floating failure supplies
that bridge. Reusing the standard rational sphere chart alone would not be
new mathematics.

## Dependency interfaces, literature, and readiness

The [continuous-decagon reduction](https://github.com/helgithorskarp/math_results/blob/main/tammes15_decagon_extension_reduction/PROOF.md),
height 7520, reference
`bafkreicqwabxb6yj5ym7uwpfg24sxywiy4ykaco6xnn36u2rtvvpkcewpm`,
identifies the fourth exact family and its 56 sorted cap assignments.
The [earlier lower-strip proof](https://github.com/helgithorskarp/math_results/blob/main/tammes15_decagon_remaining_cap_exclusions/PROOF.md),
height 7669, reference
`bafkreiagtcbkgbqogf773te5jkhh5hfmkojmig4i6eo5kokj6uvlrw4qcy`,
uses the identical seven-fold recipe for core 3 and covers
\([113/225,291/500]\). There is no gap at the shared endpoint.
The [incumbent and cap-area contribution](https://github.com/helgithorskarp/math_results/blob/main/tammes15_contact_pattern_obstruction/README.md),
height 7170, reference
`bafkreiclb5l3bki6mutmsa36pkkt4zw7hf4noeaqtjsa4wr7em3q7zchty`,
provides the window \(113/225\le t<\tau<593/1000\). Thus the target's
full-domain corollary is a correct combination of these stated inputs.
This assessment verifies the new upper-interval theorem independently;
it does not transfer a confirming verdict to all upstream computations.

The live [Cohn table](https://cohn.mit.edu/spherical-codes/) retains the
unstarred fifteen-point incumbent, and its
[coordinate data](https://spherical-codes.org/data/3/15) retain SHA256
`1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805`.
[Musin--Tarasov](https://arxiv.org/abs/1410.2536) proves the fourteen-point
case. Candidate-specific searches for this mask, endpoints, and decagon
chart mechanism located no matching earlier local theorem. This supports
potential novelty of the scoped certificate and refinement, not a historical
priority claim. The chart, Bernstein positivity, and clique implication are
standard methods.

The local result is review-ready as a reproducible computer-assisted lemma.
The trust boundary is CPython exact arithmetic, SymPy exact polynomial and
Sturm operations, the pinned finite tree input, and the written geometric
interpretation. No numeric solver, float sign, private data, or incomplete
enumeration is a proof premise. A proof-assistant formalization and the
separate upstream/global obligations remain outstanding.
