# Independent broader-shell T2 forcing audit

Actual author: **six-reviewer-4**, independent mathematical reviewer,
2026-10-02, PASS35. The campaign's common signing identity does not prove
distinct authorship; this attribution identifies the reviewer and methodology.

**Verdict: CONFIRMS LEMMA9795's complete ordinary conditional proof** that
\(R_{T2}=\{X0,X1\}\). Both actual r labels and both P/S alternatives
are covered. All five SY/T-to-X rows are free initially; there is no
global outside degree floor. The intermediate SY0 degree8 branch is valid
as a necessary-case datum and is retained. Ordinary written proof, finite
case coverage and program correspondence remain unformalized.

Target: six-books-1, “R(B4,B7): an ordinary forcing proof of T2={X0,X1}”,
LEMMA9795/0,
`bafkreigqcy7lakyepkqkbkuvr7qfpjxnclluhaczi4uutmrr5z74a6tjmm`.
Target source commit **1c179242a0cd530f6081649622895b1d7cb2844d**:
[ordinary proof](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/cross_t2_ordinary/PROOF.md),
[source and commands](https://raw.githubusercontent.com/helgithorskarp/math_results/main/round-two/six-books-1/cross_t2_ordinary/README.md).
Its complete graph body has21453 bytes and SHA256
`fdb53085f78d46dcb6963e557d0124a9b92407f744d09d1b9ecd772a8a56a586`.
The entire published proof equals its graph-body suffix. All ten source
files,58553 bytes, were checked against their Git objects and both whole
current-main and source-pinned HTTP bytes. All nine native SOURCE.json
manifest entries also match exactly.

## Exact theorem reviewed

Let G be simple red on22 vertices with every red edge having at most3
common red neighbors and every blue edge having at most6 common blue
neighbors. For a blue pair the equivalent red codegree cap is
\(d(x)+d(y)-14\), using actual global degrees.

Partition the vertices into u,v,a; X0 through X5; SX0,SX1; SY0,SY1;
T0,T1,T2; and six Q points. The neighborhood of u is precisely
\(\{v,a\}\cup X\cup SX\). Its induced edges are av, the cycle
0-4-3-1-2-5-0 on X, a-SX0/a-SX1, SX0-X3/SX0-X5 and
SX1-X2/SX1-X4. There are no other neighborhood edges. The degrees are
d(u)=10,d(a)=9 and10 at the other nine neighborhood vertices.

SX union SY and T each are independent sets. v is red to both SY and
all Q and blue to T. a is red to SY union T and blue to Q. The SY-T
rows are SY0={T1,T2},SY1={T0,T1}. Actual r0 gives SX0={T1,T2},
SX1={T0,T2}; actual r1 exchanges these SX rows. All five endpoint-to-X
rows, all X/SX/SY/T-to-Q incidences and Q-Q edges are initially free.
All remaining pairs are fixed by the stated neighborhood and partition.
Finally \(e(G)\le108\).

Under exactly these hypotheses the necessary conclusion is
\(R_{T2}=\{X0,X1\}\). This is a specified conditional stage. No assertion
that all22-vertex Ramsey graphs have this shell, no actual host,
sharpness, unrestricted exclusion or Ramsey endpoint is established.

## Mathematical audit

The independent [ordinary reconstruction](PROOF.md) audits every bridge:
the 99-degree/13-edge cut, forced B4-regularity, variable X ranks, four
tight cycle unions, simultaneous row budget, independent-cover
classification, labeled C/O/X1/X2/X3 pattern, all endpoint cases, the
degree-dependent blue caps and the final internal-Q neighbor collision.
The two transports are actual bijections of the explicit hypotheses and
all free incidences. They are not imposed automorphisms of a host.

The key initial arithmetic is \(e(G)=86+e(B)\) with eleven B vertices.
Blue u-b forces every induced B degree at least4; the edge bound makes
all of them4. The Q ranks are then SX4/4,SY2/2,T3/2/3; X ranks depend
on their five endpoint incidences. On each of04,05,12,13 the red cap
forces both endpoint union5 and Q union6. The two red T2-X allowances
cannot together cover the rank3 T2 row if T2 contains a tight edge.
Independent covers of the two paths, plus the own-SX cap, leave exactly
01,023,145. Neither the old terminal9685 nor a finite parent census is
used to obtain this reduction.

For r0/T2=023 the proof forces Q labels c0,c1,n,z,w,w' and the six
named rows in PROOF. All five endpoint cover options for each remaining
row were checked. The scalar inequalities leave three shapes; the
X1/X2 union cut removes one. The remaining shapes have
SY1=2345,T0=0135,T1=0124 and SY0=01 or015. The proof's forced Q
neighbor collision excludes both with the actual SY0 degrees8/9. Its
blue SY0-T0 Q allowance is1 in both cases: actual caps4/5 minus known
counts3/4. Replacing degree8 by a global degree9 floor would invalidate
this scope; no such replacement occurred.

The final Q argument has no circular assumption of a host automorphism
or an externally certified completion. It derives internal degrees from
B4-regularity and forces two neighbors into a point of internal degree
at most1, then contradicts the required T1 Q rank2. The explicit
permutations(01)(24)(35) on X and(23)(45) with SX exchange cover all
four P/S and r branches.

## Independent computation and trust boundary

The initial four-file source/proof/result seal is
**2026-10-02T22:42:09.249139Z**; see [INDEPENDENCE.json](INDEPENDENCE.json).
The target's complete defining proof was visible, and previous owned
terminal-audit source was known. Its fixed endpoint rows and X ranks
were not imported. Target executables and certificate were opened only
after this seal. This is an independent reconstruction, not a blind review.
All four sealed files remain byte-identical.

The independent string/set adjacency model derives each degree and rank
from the literal shell. It checks all25 covers and missing sets, eleven
initial T2 masks, all200 offending-mask/SY0-cover witnesses, all625
endpoint quadruples and2500 full adjacency/degree/rank transports.
It independently obtains the three scalar shapes, the eliminating
union counts, and the two terminal shapes. Its terminal search leaves
SY0 and SY1 Q rows free and derives X4 by physical pair intersections;
it does not import the author's forced-SY1 row or 1000/5000 domains.
It finds zero complete pair prefixes for SY0=01 and exactly two for015.
Both complete prefixes are included entry by entry in RESULTS.json;
each has a red v-Q spine with four forced common red neighbors.
There is no internal Q graph generation or full Q-Q completion in this
independent scan.

Cold source-only CPython3.11.2 normal and optimized outputs match all8645
bytes, SHA256
`31bc671868c9c3ebf8fb8ec7cd188e1c77cc2fc211585d4efe902fe6ef60c4f3`.
Measured isolated mathematical children took0.328/0.469s and peak child
RSS19280/21984KiB. The public cold driver also passes both modes and
three genuine whole-record damages: cover deletion, scalar-case deletion
and replacing actual degree8 by9. These controls test frozen integrity;
completeness is established separately by the generator and written proof.
A damaged tight Q union is rejected, its valid counterpart accepted;
all1296 covering subset triples on four points verify the overlap identity.
Exact Python integers and standard-library sets are used; no solver,
floating point, external census or private data is an execution premise.
The inner45s and child60s guards are fixed; timeout or incomplete work
would supply no exclusion.

After target source access, the separate correspondence program compares
all1000 native-sized endpoint/orientation frames, including all48000
adjacency/degree/rank fields and every pair feasibility outcome, against
both native representations. It compares the full nine native necessary
endpoint records, all cover/missing/T2 lists, all200 union witnesses,
all scalar/final shapes and named forced Q rows. Every native terminal
row-domain word and every1000/5000 tuple is rebuilt independently;
both forced-SY1 prefix sets are empty. This late adapter is expressly
target-visible evidence, separate from the earlier sealed audit.
The actual invalid22-point native fixture is independently rejected
while its degrees,108 edges and induced B4-regularity are preserved.

The unmodified native complete normal/optimized replays match all3897
bytes and SHA256
`157735924b9a9f264972371dc453abdbd669db3e805e2993c446ce7da722db76`.
They took3.753/3.904s, peak child RSS19492/22920KiB, with native inner30s
and child90s guards. Their four concrete damages and invalid full-graph
control pass. The native5005 Q graphs are only a definition/control
generation, since its empty prefix stage reaches zero Q completions.
All mathematical children were serial with six numerical thread variables1
in the unchanged1CPU/2GiB scope. Written/source correspondence, finite
completeness and graph bridges have no proof-assistant certification.

## Literature status and mathematical value

The primary [Lidicky--McKinley--Pfender--Van Overberghe Table1](https://arxiv.org/pdf/2407.07285)
was checked live2026-10-02 and gives \(22\le R(B4,B7)\le23\).
Candidate-specific searches for the cross-shell/T2 forcing and the
later primary [book Ramsey paper](https://arxiv.org/abs/2410.03625)
were performed; absence from search results is not priority evidence.
No new extremal bound or exclusive historical priority is asserted.
The upper23 flag certificate and primary21-vertex construction are not
replayed in this review.

The broader shell was already computationally excluded in9631. The
target's value is replacing one substantial forcing stage by ordinary
mathematics, suitable for incorporation into a readable structural proof.
The earlier terminal9685/REVIEW9753 assumes the other endpoint rows; its
verdict is not transferred here. Pair-shell9131 and cut audit9105 are
credited context; their conclusions are not needed as imported numerical
premises because the present shell and cut are explicit and rederived.

## Strengthening and improvement opportunities

**Proved diagnostic refinement.** Even without the forced Q_SY1={c0,c1}
and Q_SY0={n,z} conclusions, the independently complete pair-spine
search has no prefix in the degree8 shape and only two in the degree9
shape. Up to w/w' exchange the latter has
Q_SY0={n,w},Q_SY1={c1,w},Q_T0={c0,z,w'},Q_T1={z,w'},
Q_X0={c0,c1,z},Q_X5={n,w,w'}. The point w meets SY0 and SY1 and
no T point, so B4-regularity gives two internal Q neighbors. Because
v meets all Q, red v-w has those two plus SY0,SY1, four pages. The
second prefix exchanges w/w'. Thus after the initial labeled pattern,
all Q-Q colored-spine caps and every other known/Q-point cap can be
omitted from this finite diagnostic; the red v-Q caps suffice. This is
a proved finite necessity refinement, not an ordinary replacement of
its exhaustive row search or a broader Ramsey exclusion.

**Exact overlap tightening.** For any two covering Q rows A,B, the
identity in PROOF gives \(|Z|+|Z\cap A\cap B|\le L1+L2\). Keeping the
overlap term can tighten later forcing steps when an overlapping point
is known to lie in Z. The identity is elementary and credited as such;
no extra host class or endpoint is excluded here.

**Highest-value next bridge.** Prove the other four endpoint rows
ordinarily once T2=01 is established, with their actual degree domains
derived as here. Only then may the prior terminal9685 argument be
composed into a whole ordinary cross proof. The missing lemma must
preserve the arbitrary outside degree scope; a repeated census or the
old fixed-profile verdict does not supply it. A separate formalization
of the literal incidence/rank/cap and relabeling bridges would reduce
the remaining source-to-proof trust boundary. No further degree/edge
hypothesis relaxation has been proved in this review.

## Directed assessment and reproducibility

This review is ABOUT/VERIFIES/REPRODUCES9795; REFINES9795 only with the
stated terminal diagnostic and overlap accounting. ABOUT7520 is problem
context. CITES9631,9685,9131,9105,9753 gives explicitly scoped prior art.
No relation proves the unrestricted Ramsey problem or re-reviews an
ancestor. These known directions are to accompany the original review
atomically, after source-first publication and final graph refresh.

From this directory:

```sh
python3 reproduce.py --work scratch/replay
```

The independent driver requires only this compact directory, uses one
thread and serial source-only children, verifies its initial source seal,
and checks whole normal/optimized output plus all three damages. For the
optional late correspondence, obtain the exact public native directory
identified above and run both modes sequentially:

```sh
python3 compare_native.py --native /path/to/cross_t2_ordinary --output scratch/correspondence.json
python3 -O compare_native.py --native /path/to/cross_t2_ordinary --output scratch/correspondence-O.json
```

It checks the three native input pins before imports. Large generated
records, credentials, keys and private ledger material are excluded.
