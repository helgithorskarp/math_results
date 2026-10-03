# Independent prime617 support audit

Actual author **six-reviewer-4**, role **independent mathematical reviewer**, 2026-10-03. This is an ordinary, unformalized proof plus exact independent finite validation. Shared signing identity does not establish distinct authorship.

## Scope and explicit premises

The target is LEMMA9940/0, CID `bafkreicqfy5ljhddz6vl7qjr7isnojjlw6cfg4xzpgrvsqthxpdbxk6asu`, source `7fc00626d381efcd4d0f41f63c2383ecdba23e9e`. Its claim concerns actual nonroot flips from a **constant-phase single affine quadratic character** on \(\mathbb F_{617}\). Original root occurrences are independently free. A nonroot column belongs to \(F\) precisely when at least one actual integer position differs from the baseline. Arbitrary nonperiodic edits are allowed. Nonzero affine slope is absorbed into the palette. No broader Boolean character combination or F103/H7 phase family is included.

We use two explicit premises: LEMMA9880's universal ordinary interval lift and five distinct opposite-character directed outneighbors for every selected flip column; LEMMA9904's exclusion of every nonempty \(|F|\le22\), and its statement that size23 can only split 10/13 or11/12 between character classes. The latter separate enumeration is **not reproved here**. My earlier REVIEW9914 independently checks9880, not9904 or9940. Reviewer2's ongoing separate audit is research context, not an imported verdict. All new size23 core and deficit calculations below are recomputed from field arithmetic.

## Field graph and complete coverage

Let \(V\) be the union of the six nonsquare endpoint supports \(\{1+jd:1\le j\le6\}\) with nonzero nonsquare entries. The six steps are285,314,362,381,409,570. Fresh exact arithmetic gives \(|V|=33\), \(V\cap V^{-1}=\varnothing\), and \(D=V\cup V^{-1}\) has66 elements. Define a bipartite graph on the308 squares and308 nonsquares by \(q\sim t\iff t/q\in D\). Every vertex has degree66. The premise's directed arcs have distinct unordered pairs, so for a selected support of size \(m=a+b\) with \(M\) missing cross-pairs,

\[
M\le ab-5m.
\]

Choose any row of a selected five-row set and divide all selected vertices by it. Ratios are preserved and the two character classes can be exchanged. This normalizes one row to1. This is a normalization of the necessary **field graph**, not a symmetry assertion for integer interval colorings.

`cover.py` generates every increasing square-row tuple containing1 whose **entire** common neighborhood has size at least6, through length7. If a final tuple qualifies, every prefix qualifies, proving that monotone pruning loses none. `cover_check.py` separately derives literal multiplication neighbors from explicit squares and checks every legal one-row extension, every retained entire neighborhood, every prefix and uniqueness. It computes whole closures and every intersection transition independently. The fresh producer uses my explicitly credited old Gauss/Euclidean ratio-mask arithmetic, not the target's implementation.

The whole enumeration yields1,685 five-row tuples:1,420 with6 common columns,240 with7,25 with8. There are180 six-row tuples, all with6 common columns, and no qualifying seven-row tuple. Hence no \(K_{5,9}\), \(K_{6,7}\) or \(K_{7,6}\). The unique intersections number11,092; all3,416,336 transitions are checked, with73,826 retained. Whole closures of size at least5 have histogram \((5,6):860,(5,7):240,(5,8):25,(6,6):180\). These are labeled coverage counts, not orbit counts.

## Sharp integer degree bound

For integer nondecreasing degrees \(0\le d_1\le\cdots\le d_a\le b\), let \(S=\sum_{i=1}^r d_i\) and \(\sum d_i\le M\). Then

\[
S+(a-r)\lceil S/r\rceil\le M,
\qquad
S\le\min\{rb,\psi(a,r,M)\},
\]

where \(\psi(a,r,M)=\max\{s\in\mathbb Z_{\ge0}:s+(a-r)\lceil s/r\rceil\le M\}\). Indeed \(d_r\ge\lceil S/r\rceil\) and every later degree is at least \(d_r\). The numeric bound is sharp: for the maximal allowable \(s\), distribute \(s\) among the first \(r\) entries as floors and ceilings, and set each later entry to \(\lceil s/r\rceil\). This attains the minimal total. Sharpness as degree vectors does not imply graph realizability. This is an elementary order-statistics argument, with no exclusive priority assertion.

For size23, \((a,b,M)=(10,13,15)\) or\((11,12,17)\); with \(r=5\), \(S\le5\). Equivalently \(S\ge6\) would force total at least16 or18. Choose the five rows \(A_0\) with least missing degree. If \(C=\bigcap_{q\in A_0}N(q)\) and \(B_0=B\cap C\), then \(|B_0|\ge b-S\). Thus the10/13 case has \(B_0=C\) of size8 (25 cores). The11/12 case has every subset \(B_0\subseteq C\) of size7 through\(|C|\) (465 cores). The independent checker produces every one of these490 cores canonically from its complete five-tuple list.

## Exact outside deficit allocation

Fix a core and put \(n=a-5\), \(k=b-|B_0|\). All additional selected columns lie outside the **entire** \(C\): unselected members of \(C\) cannot be chosen, because \(B_0=B\cap C\). For an extra row \(q\notin A_0\), define \(g(q)=|B_0\setminus N(q)|\). For \(t\notin C\), define \(d_0(t)=5-|A_0\cap N(t)|\in\{1,\ldots,5\}\). For any actual additional row set \(A'\) of size \(n\) and outside column set \(T\) of size \(k\),

\[
M=\sum_{q\in A'}g(q)+\sum_{t\in T}\left(d_0(t)+\sum_{q\in A'}\mathbf1_{q\not\sim t}\right).
\]

Define

\[
h(q)=n g(q)+\min_{|T'|=k,\ T'\subseteq C^c}
\sum_{t\in T'}\left(d_0(t)+n\mathbf1_{q\not\sim t}\right).
\]

Then \(nM\ge\sum_{q\in A'}h(q)\), which is at least the sum of the \(n\) smallest actual-row costs. Different rows may optimize different \(T'\); that relaxes the constraint and gives a valid lower bound, not a common minimizing column set.

The fresh producer computes costs over **all** outside columns using ratio-mask graph arithmetic and a full minimum selection. The literal checker uses only adjacent outside columns: adjacent costs are at most5, nonadjacent costs at least\(n+1\), and there are at least\(66-|C|\ge58\) adjacent outside columns. Therefore this reduction is valid for \(n\ge4\), including equal costs at\(n=4\), and there are more than the required \(k\) eligible columns. A small fixture shows that it fails without the degree-gap hypothesis.

For10/13, elementary lower \(M\) values16 (5 cores) and18 (20) already exceed15. Allocated lower \(nM\) values88,92,100 have multiplicities5,10,10, all exceeding75. For11/12,445 cores exceed102 immediately. The other20 give100 or101, ten each. The producer multiplies all303 **actual-row** factors \(1+xz^{h(q)}\) using suffix coefficient dictionaries, then un-ranks every admissible subset with total cost at most102. The independent checker instead enumerates increasing residue tuples with a suffix minimum; it compares the entire actual row tuple list and coefficient histogram, not just a count. There are exactly50 actual six-row tuples.

For each such tuple, both programs recompute all outside-column costs for the complete11-row set, compare their whole cost hash, literal five best columns and exact deficit. Minima are28 (10 tuples),30 (30),31 (10), each greater than17. The28 applies only to this completely covered surviving core/budget domain. It is not a global minimum over arbitrary11-by12 subgraphs. Thus both size23 cases are excluded. Together with the explicit9904 premise, every nonempty actual flip set at \(N\ge3702\) has at least24 columns.

## Interval conclusions

At3704, the nonconstant ordinary step617 progressions in columns1 and2 each have seven occurrences. Each must belong to the union of root and actual flip columns. One original root cannot cover both, so \(F\ne\varnothing\). Hence there are at least25 total free field columns including the root. An exactly25-column template that covers1 and2 has \(6\cdot25+2=152\) actual free positions. This is a necessary template count; independently free root occurrences need not actually differ from a baseline value, which is undefined at the root. No support or completion is exhibited.

At3703 an allowance of at most23 actual nonroot columns forces \(F=\varnothing\); the count252 then uses9880's root-word classification. This imported count is not a new enumeration here. The unrestricted van der Waerden witness problem remains open in this audit.

## Proved neighboring size24 restriction

For a size24 support, assume \(a\le b\). If \(a\le7\), then \(ab\le7\cdot17<120\), contradicting the edge bound. For8/16, \(M\le8\) and \(\psi(8,5,8)=5\), so five rows have at least11 common selected columns, contradicting no\(K_{5,9}\). For9/15, \(M\le15\) and \(\psi(9,5,15)=7\), so at least8 selected common columns occur. No\(K_{5,9}\) forces \(B_0=C\) of size8, and the same complete25 cores apply with \(n=4,k=7\). The independently recomputed allocated lower \(4M\) values are74 (5 cores),76 (10),84 (10), all greater than60. This excludes9/15.

Therefore a size24 actual flip support can only split10/14,11/13 or12/12, up to exchanging character classes. Existence of these supports and an actual3704 completion remain unresolved. This bounded extension uses the same25 complete cores, not a new broad search. After our extension implementation and pilot were completed, chat2880 from six-vdw-3 reported the same three remaining balances privately. We did not open that private proof/data and claim no priority or publication novelty for this convergent restriction.

## Proved general nonuniform allocation rule

For any such core, fix nonnegative weights \(\lambda_q\) on the available extra rows, with the sum of the \(n\) largest weights at most1. Define

\[
h_\lambda(q)=g(q)+\min_{|T'|=k,\ T'\subseteq C^c}
\sum_{t\in T'}\left(\lambda_q d_0(t)+\mathbf1_{q\not\sim t}\right).
\]

For any selected \(A'\), \(\sum_{q\in A'}\lambda_q\le1\), so summing its rowwise minima against the actual \(T\) gives \(\sum_{q\in A'}h_\lambda(q)\le M\). The sum of the \(n\) smallest \(h_\lambda\) is therefore a necessary lower bound. Uniform \(\lambda=1/n\) recovers the preceding rule. No nonuniform numerical exclusion for the remaining size24 cases is asserted. This elementary relaxation may be classical; no priority claim is made.

## Trust boundary

All finite values are exact standard-library integer/set/dictionary operations, with no solver or floating point mathematical decision. Python, these implementations, operating system execution and the two imported lemmas remain explicit trust boundaries. This is not proof-assistant formalization. The proof, cover and all515 core records were fully checked in normal and optimized execution. Details, full-domain hashes and finite semantic controls are in RESULT.json and VALIDATION.md. Native author executables, certificates and expected-result records were not used as inputs to this independent computation; the author's full signed statement and ordinary source proof were already exposed, so this is not a blind review.
