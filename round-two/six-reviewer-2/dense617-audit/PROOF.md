# Independent dense prime-617 graph exclusion

Actual author **six-reviewer-2**, role **independent mathematical reviewer**.
This proof audits LEMMA9904, by researcher six-vdw-3, artifact
**bafkreiefyta3ncjhcfygyee3aufiihszvwzj3szbsze2aringbmtafpbsy**,
source **18553dd0f7bd4eef0914cc8bb33221c159b50920**.
Shared signing identity does not establish distinct authorship.

## Graph and complete independent domain

Let \(S,T\) be the nonzero square and nonsquare classes modulo 617.
For every nonzero step \(d\), test the six residues \(1+jd\), \(1\le j\le6\).
Exactly the steps285,314,362,381,409,570 put all six in \(T\).
Let \(V\) be their union and \(D=V\cup V^{-1}\). Exact field reconstruction
gives \( |V|=33\), \(V\cap V^{-1}=\varnothing\), and \( |D|=66\).
Define \(G\) on \(S\sqcup T\) by \(q\sim t\) if \(t/q\in D\).
Its308-by308 adjacency matrix is fully reconstructed, with every degree 66.

Dividing all selected vertices by any selected vertex preserves ratios.
If that vertex was nonsquare, the two parts exchange. Thus a specified
five-row set can always be normalized to contain 1 on the square side.
This is solely a graph symmetry, with no affine quotient of integer colorings.

The primary enumeration starts at row1 and its 66 neighbors. It visits
every increasing tuple of additional square residues, retaining an extension
if the common neighborhood still has at least6 elements. Any hypothetical
retained tuple survives every prefix because intersections only shrink.
The retained tuple counts for sizes 1 through7 are

\[
1,295,6090,6182,1685,180,0.
\]

The corresponding extension-trial counts for sizes 2 through7 are
307,45596,588482,418133,97002,9119. There is no seven-row tuple with
six common neighbors; five-row tuples have at most8 common neighbors;
six-row tuples have exactly6 whenever they survive. Hence there are no
\(K_{5,9},K_{6,7},K_{7,6}\), with every normalized row tuple covered.
This enumeration does not take a closed-intersection certificate as input.

The resulting intersections are 11092 distinct states. A supplementary
definition-level comparison reconstructs every entire closure and checks all
3416336 transitions, including discarded transitions, recovering73826
retained transitions. Closures with at least five rows have the following
size pairs (rows,columns), with multiplicities:
\((5,6):860,(5,7):240,(5,8):25,(6,6):180\).
These comparisons corroborate the author's state method; tuple coverage
supplies the independent primary proof of the biclique exclusions.

## Dense-core reduction

For selected parts \(A,B\) of sizes \(a,b\), let \(M\) be their missing
cross-pair count. Choose five rows \(A_0\) with the least missing degrees.
Their sum is at most \(\lfloor5M/a\rfloor\), so their full common
neighborhood \(C\) contains at least \(b-\lfloor5M/a\rfloor\) selected
columns. Normalize one member of \(A_0\) to1, and set \(B_0=B\cap C\).
Every one of the 1685 normalized five-row sets and every appropriate
subset of its **whole** common neighborhood is enumerated.

Put \(s=|B_0|\) and \(g(q)=|B_0\setminus N_G(q)|\). Every column of
\(B\setminus C\) misses a pair into \(A_0\), while all \(A_0\)-\(B_0\)
pairs are present. The missing-pair sets here are disjoint. Consequently

\[
M\ge(b-s)+\sum_{q\in A\setminus A_0}g(q)
\ge(b-s)+\text{sum of the }a-5\text{ smallest costs outside }A_0.
\]

For \(a=10,b=12,M\le10\), \(s\ge7\). All 465 core cases have lower
bound at least13. The complete histogram is
13:90,14:130,15:115,16:90,17:30,19:10.

For \(a=b=11,M\le11\), \(s\ge6\). There are 4265 core cases;
515 survive this first lower bound, all with \(s=6\). The six additional
rows must have total cost at most6. The independent row search processes
all 303 remaining rows in increasing (cost,residue) order. At each prefix,
the sum of the next required number of sorted weights is an exact lower
bound. This pruning excludes only impossible selections. It assumes no
list of cost0/1/2 patterns or closure-derived row categories.

For a complete selected eleven-row set \(A\), put
\(d_A(t)=11-|A\cap N_G(t)|\). The other five selected columns must lie
outside the **whole** \(C\): columns in \(C\setminus B_0\) are forbidden,
because \(B_0=B\cap C\). The exact minimum missing count for this
fixed row set and core is

\[
\sum_{q\in A\setminus A_0}g(q)
+\text{sum of the five smallest }d_A(t),\qquad t\notin C.
\]

All 68405 admissible row extensions are enumerated. Their minimum is 24,
and the complete histogram is
24:760,25:3970,26:10210,27:13845,28:15880,29:12160,30:8260,
31:3120,32:80,33:120. The minimum 24 concerns this conditional core
domain; it is not a universal24-missing-pair bound for arbitrary11-by11
subgraphs. It excludes \(M\le11\) and therefore also gives the universal
graph conclusion that every 11-by11 subgraph has at most109 edges.

## Proved stronger unbalanced density bound

Suppose an arbitrary10-by12 subgraph has \(M\le12\). Order its row missing
degrees \(d_1\le\cdots\le d_{10}\), and put \(S=d_1+\cdots+d_5\).
If \(S\ge6\), integrality gives \(d_5\ge2\), so

\[
M\ge S+5d_5\ge6+10=16>12.
\]

Thus \(S\le5\). The five least-missing rows have at least seven common
selected columns, so the **already independently checked 465-core domain**
applies. Every such core has lower missing bound at least13, contradicting
\(M\le12\). Therefore

\[
e_G(A,B)\le107\quad\text{whenever }|A|=10,\ |B|=12.
\]

This is an ordinary consequence of the verified finite core bound, requiring
no larger extension enumeration. It strengthens the target's implicit109-edge
bound by two. Sharpness, extremal realization and a larger physical repair
bound are not asserted.

The integral degree insight was recognized after reading the complete newer
LEMMA9940 body, artifact
**bafkreicqfy5ljhddz6vl7qjr7isnojjlw6cfg4xzpgrvsqthxpdbxk6asu**,
source **7fc00626d381efcd4d0f41f63c2383ecdba23e9e**:
[credited ordinary method](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/character617-quantized-support/PROOF.md).
Its numerical24-column conclusions are neither imported nor reviewed here.

A pre-native larger-domain computation had already corroborated this107 bound.
It is unnecessary for the shortened proof. Its partial secondary verification
was voluntarily retired and supplies no publication premise. The original
source, complete primary results,20s timeout receipt and retired work remain
private. The five retained pre-native mathematical kernels are unchanged.

## Independent completeness checks

Every primary row transcript is checked again against an independently
reconstructed adjacency matrix (Euler characters and multiplied neighbor
sets, instead of squares, Euclidean inverses and literal ratios). Every
record's rows, costs, whole common neighborhood, forbidden columns,
lexicographically resolved best columns and missing count are checked.
Distinctness is checked separately for every core.

Completeness is independently certified by coefficients of

\[
\prod_{q\notin A_0}(1+z x^{g(q)}).
\]

The sum of the coefficients of \(z^{a-5}x^j\), over the permitted budgets,
equals the number of admissible added row sets. All 303 factors participate.
The verifier uses a finite product recurrence, rather than the primary
selection recursion. Every listed selection is valid and distinct, and the
list length equals that coefficient count separately for every core. This
proves whole-set completeness and detects omissions, including the last row.

## Actual-column implication and dependencies

The ordinary interval lift and demand-to-arc bridge are explicit imports
from LEMMA9880, artifact
**bafkreifgnqlqj2qgdmsmcveou5y2clgz6vvle2d4xjrm7fevtptxme65x4**,
source **d7bcffe42dd185e552b22290628bf8912faca311**.
For a root \(r\), palette \(\sigma\), and actual flip set \(F\) relative to
\(\sigma\mathbin{\mathrm{XOR}}L(n-r)\), each actual flipped position
forces five distinct opposite-character actual flip columns, with ratios
in \(V\). For any representative step \(1\le\delta\le616\), use the
forward endpoint AP if \(m+6\delta\le N\); otherwise the backward AP
has start \(m+6\delta-3702>N-3702\ge0\). This covers every position,
every root and every \(N\ge3702\), with arbitrary independent colors at
each occurrence. Multiplicativity absorbs a nonzero affine slope into the
palette. Root colors remain entirely free.

There are no reciprocal arcs. Thus, for nonempty \(F\) of size \(m=a+b\),
\(5m\le ab\), and its underlying subgraph has at most \(ab-5m\) missing
pairs. This implies \(m\ge20\). The no-\(K_{5,9}\) fact proved above
independently excludes20,21 and the 22 splits8/14 and 9/13, by the least
missing-row argument. The only remaining 22 splits10/12 and 11/11 are
excluded by the complete graph computations. Hence \( |F|\ge23\).

At 23 the arc count leaves8/15,9/14,10/13,11/12. In8/15, five least
missing rows have at least12 common selected columns, impossible. In9/14,
they have at least8 common selected columns, so \(C=B\cap C\) has size8.
Every further row misses at least two into \(C\), or it creates \(K_{6,7}\).
The four extra rows and six columns outside \(C\) give at least14 disjoint
missing pairs, exceeding the permitted11. Only10/13 or11/12 remain.

At 3704, vertical APs in columns1 and 2 force nonempty \(F\), and both
columns lie in \(\{r\}\cup F\). A template with 23 actual extra columns
has24 free columns and \(6\cdot24+2=146\) actual positions. This does not
count valid assignments. At 3703, at most22 edits forces \(F=\varnothing\);
the 252-coloring root-word classification is imported from9880, not rerun
as an independent classification here. REVIEW9914 confirms9880 only;
neither it nor the different H7 phase result9910 supplied a verdict for 9904.

There is no unrestricted \(W(2,7)\) value, new numerical bound,23-column
construction, nonconstant-phase conclusion or global sufficiency theorem.
All proofs remain unformalized.
