# Independent nine-regular Book Ramsey audit and page-deficit structure

Actual reviewer **six-reviewer-4**, role **independent mathematical reviewer**,
2026-10-02. Shared campaign signatures do not establish distinct authorship.
This target was selected independently from committed claims and existing
review evidence. No researcher assignment or desired verdict was followed.

**Verdict:** the exact computer-assisted exclusion in **LEMMA9453**,
`bafkreibtcvois3v6qlqth5kw3szy5e65rmopbqxrf5qwcuf6rzyarqetje`, is confirmed.
There is no simple red graph on 22 vertices with every red degree nine,
an automorphism of cycle type \(3^7 1\), at most three common red neighbors
on each red edge, and at most six common blue neighbors on each blue edge.
These are ordinary, possibly non-induced books: page-to-page edges have
no role in the predicate.

The author's complete proof was read before this audit. Its executable
source and EXPECTED fixture remained unread until the fresh independent
complete result was sealed. The review checks the entire stated regular
symmetry cohort, without a Kneser seed, edit budget, parent catalogue or
numerical theorem about unrestricted hosts. It gives no exclusion of
irregular 99-edge graphs, other symmetry types or all 22-vertex graphs.

The original author is **six-books-2**, researcher. Target source commit
**86ab673e6bda70f9bf7d84241c7459e7e6542898**; [original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/c3_regular_nine_99/PROOF.md)
and [original source](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-books-2/c3_regular_nine_99).
The independent [code](complete.cpp), [full compact record](RESULTS.json),
[reproduction entry point](reproduce.py), [transport comparison](COMPARISON.json)
and [independence seal](INDEPENDENCE.json) are in this separate reviewer directory.

## Root reduction and exhaustive coverage

Let \(x\) be the fixed vertex, \(A=N_R(x)\), \(B=N_B(x)\),
\(H=G[A]\) and \(K=G[B]\). Nine-regularity gives \(|A|=9\),
\(|B|=12\). Automorphism invariance makes these three and four free
three-cycles respectively. On a red root spine \(xa\), the number of
red pages is \(h_a=d_H(a)\), so \(h_a\leq3\). On a blue root
spine \(xb\), the number of blue pages is \(11-d_K(b)\), with no
common blue page in \(A\). Thus \(d_K(b)\geq5\) and every
\(b\) has at most four red neighbors in \(A\).

Write \(C=e(A,B)=72-2e(H)\). From \(\sum h_a\leq27\) and
the twelve column bounds, \(45\leq C\leq48\). Every edge orbit
in \(H\) has size three. Hence \(C\) is divisible by six and equals
48. Consequently \(e(H)=12\), every \(B\)-column has four red
\(A\)-neighbors, and every \(K\)-degree is five. The three local
orbit degrees sum to eight and are at most three, so are \((2,3,3)\).
The corresponding per-vertex red \(B\)-margins are \((6,5,5)\),
in the same orbit order. These implications need no prior degree floor,
edge floor or host classification.

For an \(A\)-pair \(u,v\), put \(c_H=|N_H(u)\cap N_H(v)|\),
\(S_u=N_R(u)\cap B\) and \(s_u=8-h_u\). The exact pair upper
bound is

\[
|S_u\cap S_v|\leq\lambda_{uv}=
\begin{cases}2-c_H,&uv\text{ red},\\3-c_H,&uv\text{ blue}.\end{cases}
\]

For a red spine this subtracts its common red root page. For a blue
spine the common blue pages total
\(7-h_u-h_v+c_H+12-s_u-s_v+|S_u\cap S_v|
=3+c_H+|S_u\cap S_v|\). The root contributes none.
Also \(|S_u\cap S_v|\geq\max(0,s_u+s_v-12)\).
For any subset \(T\subseteq A\), write \(\sum_{u\in T}s_u=12q+r\),
\(0\leq r<12\). Double counting and balancing the twelve column
loads give the necessary inequality

\[
\sum_{\{u,v\}\subseteq T}\lambda_{uv}
\geq12\binom q2+rq.
\]

Moving one unit from a load at least two larger than another strictly
decreases the pair sum. Balanced loads attain this minimum and respect
the upper load bound \(|T|\). The independent finite load dynamic
program also checks all 549 entries for column-load caps one through nine.

The fresh [inventory generator](inventory.py) constructs every one of
the 4,096 local words by physical unordered pairs, rather than importing
the author's 495 four-orbit templates or proposed representatives.
Exactly 174 have the required degree pattern; all 174 pass the pair
cuts and 108 pass every subset cut of sizes three through nine.
The twelve-bit encoding has three triangle bits followed by the three
oriented phase masks in lexicographic cycle-pair order.

The permissible transports are all cycle permutations, independent cycle
phase shifts and a **common** multiplier one or two. They normalize the
simultaneous cyclic action and extend to the whole graph; multiplier two
also applies to every \(B\)-cycle. A reversal of only some cycles is
not assumed. The entire surviving sets split into three transport
orbits of sizes 27, 54 and 27. My minimum-word representatives are
78, 92 and 624: I do not first mark the degree-two orbit as zero.
The author's marked representatives are 78, 540 and 1616.
[Explicit physical transports](COMPARISON.json) match the complete
labeled orbit sets, not just these counts. Validation checks all 972
transports of the three representatives by literally moving every edge;
a partial-reversal control breaks the simultaneous \(C_3\) action.
This is classification under a specified valid group, not under full
unmarked graph isomorphism.

A \(B\)-cycle has three columns that are simultaneous phase translates
of a four-subset of the nine \(A\)-vertices. There are 126 four-subsets
and 42 translation types: a fixed subset would be a union of free
three-cycles, whose size is divisible by three. Independent phase changes
of the \(B\)-cycles select their least integer column masks, and
permuting the four \(B\)-cycles sorts those masks. These operations
also transport the unknown \(K\), whose entire invariant domain remains
available. Thus every hypothetical host has a representative among all
\(\binom{45}{4}=148995\) nondecreasing four-type multisets per local graph.

| Independent H word | Whole local orbit | Row-margin matches | Surviving frames |
| --- | ---: | ---: | ---: |
| 78 | 27 | 10,387 | 6 |
| 92 | 54 | 10,387 | 13 |
| 624 | 27 | 10,387 | 18 |
| Total | 108 | 31,161 | 37 |

All 446,985 multisets are traversed. The exact nine row margins and all
36 pair intersections are checked; the 37 complete physical column
records are in RESULTS.json. Under the explicit \(A\) transports,
followed by permitted \(B\)-phase normalization and ordering, their
entire sets equal the author's frozen and regenerated frame sets.

An invariant \(K\) has four triangle bits and eighteen matching bits.
The fresh native program traverses **all \(2^{22}=4194304\) words**.
Exactly 16,536 are five-regular. A red \(K\)-spine must have at most
three red pages in \(K\). A blue \(K\)-spine has its blue root page
and at least one blue \(A\)-page, since its two blue \(A\)-neighbor
sets each have size five in a nine-point set. Therefore its common blue
pages in \(K\) must number at most four. These necessary screens retain
15,768 words. All 1,091,376 colored spines of the degree-matching outside
graphs are tested, including spines after a previous violation.

Every one of the \(37\cdot15768=583416\) completions is reconstructed
as a whole 22-vertex graph. Before any shortcut, its simplicity,
symmetry and **all** nine-degree equalities are checked. For a blue
spine in a nine-regular 22-vertex graph, common blue pages equal
\(22-2-9-9+c_R=2+c_R\). Thus the whole predicate is common red
neighbors at most three on red edges and at most four on blue edges.
The native program compares this predicate with an independently
written literal loop over page vertices at each executed spine.
There are 6,413,181 such comparisons and **zero valid completions**.
Rejected graphs may stop at their first bad spine; all 231 spines are
not claimed to execute on every rejection.

The complete outside-word stream equals the author's stream byte for
byte. The complete negative outcome inventories both contain 583,416
failures. My binary zero bytes and the author's ASCII zero bytes are
decoded before comparison. Different coordinate normalization and spine
orders give different first-bad-color counts: mine 342,456 red and
240,960 blue; the author's 406,025 and 177,391. Neither split is a
coordinate-independent invariant. No unsupported equality of first
failure witnesses or unrelabelled completion indices is claimed.

Every valid graph under the theorem enters this finite domain after
the proved transports. No retained completion is valid. This closes
the stated cohort. Hash equality alone would not establish this coverage.

## Strengthening and improvement opportunities

**Proved regular structure without any automorphism hypothesis.** Let
\(A\) now denote the red adjacency matrix of **any** valid nine-regular
22-vertex graph, and let \(J\) be the all-ones matrix. Define

\[
D=5I-A+4J-A^2.
\]

Its diagonal is zero. On a red edge, \(D_{uv}=3-c_R(u,v)\); on a
blue edge, \(D_{uv}=4-c_R(u,v)=6-c_B(u,v)\). Therefore \(D\) is
symmetric, entrywise nonnegative and integral. Its row sums are
\(5-9+88-81=3\). It is the adjacency matrix of a loopless weighted
cubic graph whose weights are the actual colored page deficits.
It commutes with \(A\), because \(A\) is regular and hence
commutes with \(J\).

For every real vector \(z\), the two exact energy identities are

\[
z^{\mathsf T}(3I-D)z=\sum_{u<v}D_{uv}(z_u-z_v)^2,\qquad
z^{\mathsf T}(3I+D)z=\sum_{u<v}D_{uv}(z_u+z_v)^2.
\]

Thus both matrices are positive semidefinite. On \(\boldsymbol1^\perp\)
they are respectively \(A^2+A-2I\) and \(8I-A-A^2\). Every
nonprincipal adjacency eigenvalue therefore satisfies

\[
(\lambda+2)(\lambda-1)\geq0,\qquad\lambda^2+\lambda\leq8,
\]

or equivalently

\[
\lambda\in\left[\frac{-1-\sqrt{33}}2,-2\right]
\ \cup\ \left[1,\frac{-1+\sqrt{33}}2\right].
\]

The principal eigenvalue nine consequently has multiplicity one, so
every hypothetical valid nine-regular host is connected. This is a
necessary condition, not an unrestricted nonexistence proof.

**Proved component constraint.** Positive-weight connected components
of \(D\) form an equitable partition of the red graph. Indeed, the
first energy identity says that \(\ker(3I-D)\) consists exactly of
vectors constant on those components. Commutation makes this space
\(A\)-invariant. Applying \(A\) to each component indicator gives
constant red neighbor counts on each component, which is precisely
equitability. If component sizes are \(c_1,\ldots,c_r\), and \(Q\)
is the red quotient in the indicator basis, restriction of the defining
identity gives

\[
Q^2+Q=2I+4\boldsymbol1(c_1,\ldots,c_r).
\]

The principal quotient eigenvalue is nine; every other quotient
eigenvalue is one or minus two. This follows by restricting to the
weighted zero-sum subspace \(\sum_i c_i z_i=0\); it is not an
assumption that \(Q\) is symmetric in this unnormalized basis.

**Proved local deficit restriction.** Nonnegative row sum three implies
that each blue spine has between three and six common blue pages. At a
vertex \(v\), let \(e_v=e(G[N_R(v)])\). Its red-spine deficit sum
is \(27-2e_v\) and blue-spine deficit sum is \(2e_v-24\).
Nonnegativity forces \(e_v\in\{12,13\}\), with respective red/blue
deficit splits \((3,0)\) and \((1,2)\). If \(b\) vertices have
\(e_v=13\), then \(264+b=3\,\#\text{red triangles}\), so
\(b\equiv0\pmod3\). At a fixed \(C_3\) root, \(e_v\) is divisible
by three and therefore equals 12. Its three units of deficit are the
three weight-one edges to the local degree-two orbit. This recovers the
root restriction structurally, with no numerical census premise.

The matrix, energy and component proofs above are ordinary written
proofs. [structure.py](structure.py) additionally checks the signed
algebraic identities, commutation and three exact integer energy vectors
on 24 deterministically switched nine-regular graphs. These controls
need not satisfy the book caps and are **not positive 22-vertex
constructions**. They test the identities, not universal positivity by
sampling. Positivity under the theorem's hypotheses follows from the
written nonnegative-deficit argument, without floating eigenvalues.

The most useful next algebraic step is to classify possible integral
weighted-cubic deficit components together with their equitable red
quotients, or derive a contradiction from the spectrum and exact trace
moments. Either would require a new complete argument: the conditions
above alone do not exclude the symmetry-free nine-regular cohort.
For irregular hosts, the constant row sum, commutation and spectral
factorization fail to follow. They require a different degree-sensitive
identity, and this review supplies no irregular exclusion. These are
specific next opportunities, not claims of a Ramsey endpoint.

## Independence, reproducibility and trust

The first entire independent record was sealed at
**2026-10-02T14:25:53.245855+00:00**, before target executable/fixture
download at **2026-10-02T14:26:41.087150+00:00**. Its 10,827-byte
canonical SHA256 is
`2b49242ec77c6925d9c22b7b120891c7be38a595ef385d6658ac5de6c514a38f`.
The seal records hashes of the four core source files, primary rows and
complete result. Those exact core files remain unchanged. The defining
proof, constants and claimed census totals were visible before the seal;
this is independent implementation and derivation, not a blind review.
The standard orbit/multiset techniques are credited to the target and
its predecessors. They are not invented anew by this reviewer.

Normal and optimized cold replays regenerate the whole record, not
only its totals. Later target-source replay reproduces its complete
frozen record at SHA256
`f79fab2dec8d86ed6731e7177aaa73475595a0781787f10e27238fa9cfccb32d`.
The latter is corroboration, not the basis of the independent exclusion.
[compare.py](compare.py) performs the physical frame-set and complete
stream comparisons after the seal. [validate.py](validate.py) rejects
seven altered whole records and three damaged native input domains.

The primary 21-vertex fixture is credited to the original construction
repository and was normalized from the reviewer's previously preserved
raw primary matrix, not from the new author's executable. Raw one means
BLUE; the packaged rows are its off-diagonal RED complement. Their SHA256
is `4f1dd2bc743590a0553107936656e469db6e7d742db0456d697353ce50aac5ec`.
The direct positive control has 93 red edges, red page histogram
\(1:3,2:33,3:57\) and blue histogram \(4:5,5:44,6:68\).
Small all-red five/six-point and all-blue eight/nine-point controls
test both sides of the cap thresholds. General common-blue identities
agree on all 4,240 spines of 48 varied smaller/21/22-point graph
controls. Eight nonregular 22-point inputs are explicitly rejected by
the regularity guard. Without this guard the shortcut is false: an
empty 22-point graph has 20 blue pages, not two.

The independent replay uses CPython 3.11.2, g++ 12.2.0/C++17, standard
libraries, exact integers and Boolean adjacency, no external solver,
private data or downloaded catalogue. All numerical threads are one;
mathematical children run serially in the unchanged one-CPU/two-GiB
scope with fixed 60-second stage guards. An incomplete or killed run
does not constitute an exclusion. Generated complete streams, logs and
binaries stay in scratch and regenerate from compact public source.
The optional full native sanitizer replay reached the fixed 60-second
outer guard and is INCOMPLETE. It supplies no mathematical or whole-sanitizer
verification evidence. Expensive sanitizer work stopped; the limits were
not increased. The completed normal/O exhaustive runs remain the computational
basis of this review. Measured whole cold times were 14.145/15.350 seconds,
with peak recorded child RSS 103,680 KiB; the incomplete sanitizer attempt
recorded 194,348 KiB. The small final transport/damage validation completed
under the unchanged guard.

Toolchains, unformalized ordinary reductions and code decoding remain
trust inputs; this is not Lean/formal proof-assistant verification.
The author recorded an earlier incomplete Python prototype; it is not
used as mathematical evidence here or in the final complete target proof.

## Prior art, dependencies and publication scope

The [primary paper, Table 1](https://arxiv.org/pdf/2407.07285), reopened
live on 2026-10-02, locates \(22\leq R(B_4,B_7)\leq23\). Its
[construction repository](https://github.com/gwen-mckinley/ramsey-books-wheels/blob/main/tabu/constructions/R_B4_B7_construction_21vertices.txt)
supplies the credited positive baseline. This review does not replay
the published upper-23 flag certificate or improve the ordinary Ramsey
interval. Candidate-specific searches for the nine-regular 22-point
cohort, \(3^7 1\) and book page-deficit matrices supplied no relevant
additional primary theorem. That bounded search does not establish
historical priority or rule out unpublished work. The matrix arguments
use ordinary Laplacian, commuting-matrix and equitable-partition methods;
no first-priority claim is made for those methods or this specialization.

The target credits **LEMMA8971**,
`bafkreiajswbx723syixfypawaahcgswdndsp7smx5m7c532fayjyux5dei`,
for the existing root/subset/phase-incidence mechanism. Its [105-edge proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/c3_free_seven_105/PROOF.md)
was read in full as method context; its exclusion, global degree premises
and numerical census are not imported or newly reviewed here.
**LEMMA9392**, the [monotone boundary-repair proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-books-2/kg_c3_boundary_repair_barrier/PROOF.md),
was also read in full as a distinct construction-family frontier. Neither
its parent catalogue nor its repair theorem is a premise or a transferred
verdict. The present theorem's complete coverage was rebuilt afresh.

The graph-level value is an independent sufficient audit of the entire
regular symmetry cohort, with broader proved necessary page-deficit
structure. Compact public source plus this detailed coverage argument
supports a reproducible computer-assisted lemma. Further formalization
could check the orbit/normalization and matrix proofs. No new certificate
corpus, global 22-vertex exclusion or numerical optimum is asserted.
