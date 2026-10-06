# Theo's separate entire check of Quinn648

Author literature-researcher-3; checker literature-researcher-4, 2026-10-06 UTC.
I ACCEPT the ENTIRE submitted new partial scope: the uniform exact greedy cost,
the blocker/new-occurrence bijection, the original-history weighted expectation
identity, the uniform raw-RR drift obstruction, every specified deterministic
finite field/stream, and the explicit correction of the earlier oracle description.
This is an internal team check, not external peer review. The expectation BOUND,
useful completion density, other potentials (including separate655), novelty,
full410 and public/graph expansion are excluded. Full410 remains UNSOLVED.

The unchanged47-file author packet is `received/quinn_repair_path_cost_v2`,
391135 bytes plus manifest. Manifest SHA256:
62a38b24f083b16351a83c0b7111a9758ccf7aabc44ea101a36cd848d5862941.
New cost proof82a0a23681ce865fe3bb78f817ee82d3dce7257e14cd0ea939541c908e252869;
raw obstructionf4cb91a7bc2580e8436487ac7e35896f3a15341b090cb03da598334b6b49f1ed.
The ten actual632 review/transitive files match my previously received632
closure byte for byte. The actual534/592 reviews also match my originals.
Those accepted dependencies do not themselves accept the new statements.

## Uniform first-pair proof

The checked534 language characterizes a legal external gap by absence of RR
after an earlier L in its root-to-leaf word. Take an illegal target path
w=qRRv, with the displayed RR its first offending pair. The node j reached
by qR has left subtree B and right subtree C, and the target is in C. Every
external leaf of C has the offending prefix qRR. The leftmost leaf of B has
prefix qR followed only by L's and is legal. This remains true when B is
empty: its external leaf is the gap just before j. In inorder, all later
leaves before the target are inside C and are illegal. Thus the globally
rightmost legal gap before the target belongs to B. This does not depend
on unvisited subtree sizes or priorities.

Insert the auxiliary maximum at this gap. Its right subtree is the suffix
of the old inorder word. Every old R ancestor of j is before the cut and is
removed from the suffix path; every L ancestor is after the cut and stays
with its L direction. These comparisons hold because the cut is inside
j's left subtree, hence inside the whole subtree of each such ancestor.
j itself stays, and its entire right subtree C is unaffected by a cut in B.
Nodes inside B cannot become ancestors on j's right branch: j remains
larger than them. If ell is the number of L's in q, the new target path is

    R L^ell R v,    ell>=1.

Its displayed prefix has no offending pair. Pairs inside v, and a possible
pair between the preceding R and v's first letter, persist exactly; both
old and new prefixes have already seen L. Precisely the first offending
pair is lost. Therefore D falls by one at each repair, and the language
criterion says repair terminates exactly at D=0. This proves cost=D(initial)
for every finite shape/gap, including initially legal and outer gaps.
The original maximum is inserted only after repair. Every actual auxiliary
insertion is legal in the avoiding current parent.

The tree argument is label-free. My finite controls use one classical
avoiding representative per shape; they do not enumerate every heap labeling.
The accepted shape quotient and this arbitrary-shape proof give the stated
domain, rather than extrapolation from those representatives.

## Bijection and original-gap expectation

Each counted RR identifies the node reached after its first R. That node
is a right child with a right ancestor, hence exactly an eligible minimum.
The second R enters its right subtree. Its external leaves are precisely
gaps j+1 through r(j), inclusive, with the last external leaf at the boundary
before that nearest greater right ancestor. Distinct path pairs identify
distinct nodes. Conversely every eligible minimum whose interval covers
the target supplies precisely such a pair. This proves the COUNT bijection,
stronger than the previous existence criterion.

In an avoiding parent, a new box made by a hypothetical maximum must select
that maximum as its third point. Its selected minimum has uniquely determined
nearest greater points to left and right: a closer greater point would shade
the rectangle. The required left value below the right value is exactly
eligibility. Each covering minimum gives one occurrence and every such
occurrence gives that minimum. Old occurrences cannot survive from an avoiding
parent. Thus D equals the full hypothetical new-box count. The greedy algorithm
does not insert that illegal hypothetical maximum.

At n original arrivals, deterministic completion C(sigma) and its tags depend
only on the restricted source order sigma in S_n. To process the next rank,
its insertion place among the originals identifies the gap before the first
existing original to its right, or the final gap. It never assigns uniform
probability to a gap merely because it precedes an auxiliary. The separately
checked632 conditional law gives probability1/(n+1) to each ORIGINAL gap,
even after conditioning on the entire deterministic history. The history
retains sigma through its original tags; histories and their multiplicities
are not merged into an artificial uniform tree law.

Let O denote those n+1 original gaps and sum over ALL eligible current minima,
including eligible auxiliary minima. Finite double counting gives

    B(C(sigma)) = sum_j #{g in O : j+1<=g<=r(j)}
               = sum_(g in O) D(path(g)).

The rank<=n restriction of a uniform source in S_m is uniform S_n. Its
completion prefix equals C of that restriction, independently of the absolute
positions of future ranks. Conditional averaging, the exact cost theorem and
finite linearity of expectation therefore give

    E_(S_m)[total auxiliaries]
      = sum_(n=0)^(m-1) E_(S_n)[B(C(sigma))]/(n+1).

No integrability limit or independence among stages is needed: these are
finite populations and sums. Proving this sum=o(m log m) remains UNPROVED.
E[B]=O(n) would suffice, but is neither asserted nor derived. If the required
sum were proved, total length=m+auxiliaries would be o(m log m), Markov would
give a fixed positive fraction of bounded-length inputs, and the already
checked592 subsequence-fiber bridge would prove the full negative410 outcome.
This conditional implication is correct; an exact identity is not its bound.

## The precise raw-potential obstruction

Phi sums ALL adjacent RR pairs over original-gap paths, including those before
the first L. For p_(n,q)=(1,...,b,n,n-1,...,n-q), b=n-q-1, q>=1, the first
descent of any classical2143 would lie in the decreasing tail. No later point
is above its first selected value, contradicting2143. Every rank restriction
has the same form or is increasing. The rank-arrival algorithm consequently
reaches this all-original parent without any auxiliary. Its source probability
is exactly1/n!; the tags determine that source.

The maximum tree's left subtree is an all-left spine of length b and the right
subtree an all-right spine of length q. Its right external paths R^tL,
1<=t<=q, and R^(q+1) have t-1 and q adjacent RR pairs. Thus Phi_old=q(q+1)/2.
All parent paths are legal, so all next repairs cost0.

For each g<=b, the old right paths acquire one leading R, increasing Phi by
q+1; the newly added original gap and all increasing-prefix paths contribute0.
For g=b+t, 1<=t<=q+1, put r=q+1-t. The left suffix spine contributes t(t-1)/2
and the new right spine contributes r(r+1)/2. These count every n+2 ORIGINAL
gap of the child, including the new original gap before the inserted root.
The sum of these latter child potentials is q(q+1)(q+2)/3. Exact averaging gives

    Delta(n,q)=(q+1)*(n-q(q+5)/6)/(n+1).

At n=q^3, q>=2, q+5<=3q^2 gives q(q+5)/6<=n/2, and n/(2(n+1))>=1/3.
Hence Delta(q^3,q)>=(q+1)/3=Omega(n^(1/3)), which exceeds every constant and
every o(log n) all-parent upper bound along this reachable subsequence.
This rejects exactly the proposed uniform drift method for THIS Phi. Its
rare source probability leaves unconditional expected cost or unconditional
drift estimates open; it does not reject another potential or the full target.

An all-parent K(n)=o(log n) bound on cost+Phi_child-Phi_parent would, if true,
telescope: Phi>=0 and Phi_empty=0 imply expected total cost<=sum K(n), which
is o(m log m). The implication is correct, but the proposed premise is false.

## Entire independent finite check and correction boundaries

NEW completed checker `check_quinn_repair_path_cost_v3.py` imports no author
or teammate executable. It generates shapes by balanced Dyck words, assigns
decreasing preorder ranks with explicit indexed pointers, reconstructs maximum
trees by monotone stacks, and locates nearest greater points by direct position
searches. Full literal occurrence sets enumerate every selected quadruple and
count the strict open rectangle with a point-prefix table. Selected endpoint
points lie on position boundaries and the other two selected points on value
boundaries, so no selected point is falsely counted as a blocker.

ALL626 shapes/4707 gaps, ALL4707 hypothetical full box sets, EVERY1380 actual
auxiliary child and every target-path rewrite pass. Every D/cost/coverage/count
and every parent/child trace field agrees. The old canonical stream is
07841e7f30461c63aa40349d4ef55c03b4e6acd6a6099c32606c891c8bc82982;
the complete literal evidence stream is
3fb17c7423b137fb55799285cf40ca0522c6b688bdc6329f631168c22b54a25b.

The raw constant1 scan reproduces all12 states: complete sizes0..3 and only
the first two lexicographic size4 sources. The first failure in that stopped
order is1243, old Phi1, child potentials3,3,3,1,1, drift6/5; stream
cd16d68006f05ca75cd820228840bdc089f75f4da9522df21f06b212cce30fb5.
No global minimality beyond the specified complete/stopped domain is inferred.

The five directed family pairs (2,1),(4,1),(8,2),(27,3),(64,4) reproduce all110
children,105 rank arrivals, every shape/path, exact child potential and rational
drift. Exactly45 children in the n2/4/8/27 cases receive full literal scans,
as do their parents and all prefixes. The n64 case has shape/direct-neighbor
controls and NO literal census. Family stream:
bc5ec17f6c2d67534059ed42c24641ffdec53b0adb2f275c27ac708884ba4a87.
Every deterministic field in all FOUR author reports is reconstructed and
compared, including status text, source hashes, boundary counts and streams.
All stdout/report fields align, and all four author stderr files are empty.
Time/RSS fields are preserved documentary observations, excluded from equality
with the new independent resource sample.

The additional PREPLANNED checker control retains ALL874 distinct source histories
of sizes0..6, all original/auxiliary tags, all actual literal child sets and exact
blocker weights. The expectation equality holds exactly; means at m4/5/6 are
1/24,2/15,97/360. These are finite exact means, not an asymptotic estimate or
fitted bound. The 3168981-byte full certificate retains this entire domain and
all4707 path records,1380 rewrites,12 stopped records and five family controls.
Certificate SHA265c758b1fcf701615491d22f875be972365de7b576f9e5074f9860697113040.

Quinn's original probes call an OPTIMIZED complete occurrence oracle. Earlier
version1 prose/chat641 wrongly called those literal. The explicit correction
and separate literal supplement are valid; every historical source/result byte
is preserved. Neither that description error nor its correction is a detected
mathematical mismatch.

MY first new checker run also failed, for a separate reason: I added the false
stronger assertion that every gap of a family child remains legal. Legal
insertion preserves avoidance, not universal legality of future insertions.
For example legal insertion after21 produces avoiding213, whose gap2 would
produce2143 upon inserting4. Quinn makes no claim that every child gap is legal.
Failed source845b04e33f3d93c171f550a93c90615e1cedb1a90547d27ebdc5ec093d14b766,
traceback and empty stdout are preserved; no completed result was announced.
The corrected source differs ONLY by removal of that additional assertion.
The full fresh replay then completed once, exit0. This means two checker
attempts, one completed independent reproduction, not two successful checks.

Old-dependency packaging had two separate transport failures AFTER that
mathematical replay. A copied old manifest names files at its original Quinn
root rather than my earlier partial receiving directory. Resolving that root
then exposed two distinct MANIFEST.json files incorrectly mapped to one path.
Neither failure executed mathematics or changed an old packet. The receipt
preserves both errors and all44 partial copied files. The corrected separate
mirror `received/quinn648_explicit_old_closure_v2` hash-verifies all55 old
transitive files/662634 bytes and seven manifests, placing external dependency
manifests in a distinct directory. Its source-origin receipt is
`quinn_repair_path_cost_explicit_old_dependency_receipt_v2.json`, SHA
825ecc815f52db2a37f41849da0fcc976d97ac6e4854861daacb3ea1e79ccf52.
This is byte receiving, not another check of accepted534/592/632.

Completed code SHA15eec89d395d135b97841f355df947cc000692df59c3863e92c215a854eb3adc;
report `quinn_repair_path_cost_reproduction_v3/quinn_repair_path_cost_reproduction_v2.json`
SHA28a77dbd6179b006b6fcfa96d1e428a87721bf6ad3f8482bd8c66ce6f82c9140.
The output's v2 filenames denote the AUTHOR packet version; directory/checker
revision3 distinguishes the corrected independent code. Runtime1.342780462s
includes full certificate creation;40516KiB is sampled BEFORE final report
serialization, not a claimed complete later-process peak. Python3.11.2,
standard library, one process/native thread1. No local job remains. All47
author lengths/hashes match before and after the completed replay.

Reproduce from Theo's workspace using a fresh directory:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B research/boxed2143_theo_20261005/check_quinn_repair_path_cost_v3.py --packet research/boxed2143_theo_20261005/received/quinn_repair_path_cost_v2 --output-directory /tmp/theo-quinn648-fresh

The review manifest pins the actual whole review, new and failed code, both
attempts' logs/prerun receipts, the full report/certificate and explicit old
checked dependencies. Passing this partial review establishes useful exact
tools and a rejected method, not the o(m log m) theorem or full410.
