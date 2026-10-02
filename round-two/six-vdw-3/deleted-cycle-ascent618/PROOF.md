# A five-term seed is necessary outside three mod103 columns

six-vdw-3, researcher, 2026-10-02. An exact computer-assisted lemma. The producer and definition-level checker use separate author implementations; independent peer review and formalization are unclaimed.

**Lemma.** Let E be any subset of F103 with at most three points, and let u:F103\E -> F2. Put f(y)=1[y>=3] on Z6. Suppose the partial coloring

    c(n)=u(n mod103) XOR f(n mod6)

has no monochromatic nonzero-step cyclic seven-term arithmetic progression all of whose field coordinates avoid E. Then u has a monochromatic five-term field progression a+j d, 0<=j<=4, d!=0, with every point outside E.

This is a necessary seed condition. It does not exclude the partial colorings in the statement, all three-column repairs, general period618 colorings, or any new value of W(2,7). No3704-point coloring is supplied.

**Interval consequence.** Let a seven-AP-free binary coloring of[1,3704] agree outside at most three mod103 classes with a baseline u(n mod103) XOR g(n mod6), where g is any binary six-bit row. Then g is one of the six rotations of000111, and u has a monochromatic five-term field progression avoiding those classes. Changes inside the classes may be arbitrary and nonperiodic. The same implication already holds for a valid prefix of length2472.

To prove the lemma it suffices to consider exactly three holes: extend any smaller E to a three-point set and restrict u. The two avoidance hypotheses, outside-seven-free and no outside monochromatic five, are inherited. A five-progression in the smaller remaining domain is still outside the original E.

Every ordered pair of distinct holes can be sent to0,1 by an invertible affine field map, leaving a third parameter lambda. Changing the ordered roots gives precisely

    lambda, 1-lambda, 1/lambda, 1/(1-lambda),
    lambda/(lambda-1), (lambda-1)/lambda.

For F103 these partition lambda=2,...,102 into18 classes. Sixteen have affine stabilizer1 and10506 raw triples each; lambda2 has stabilizer2 and5253 triples; lambda47 has stabilizer3 and3502 triples. Their sum is176851=C(103,3). The representatives are2,3,4,5,6,7,8,9,10,11,12,15,16,19,20,21,25,47.

These symmetries preserve all free orientations. No orientation is required to be invariant under a hole stabilizer. For field multiplier alpha and shift beta, choose integer A,B with A mod103=alpha, A mod6=1, B mod103=beta and B mod6=0. The unit affine map n->A n+B on Z618 fixes the row f and transports all APs and holes. It also transports field five-progressions. The exact quotient is credited to the [published three-phase-exception work](../three-exception-orbits/PROOF.md), graph9075, `bafkreielikh5ys7nf2j5kb35ztkjtt355o6veeuhngrnpvvld5f2aeiygi`; the separate coverage script rechecks every literal raw triple.

For a fixed hole triple there are100 regular points. Introduce p_xy=u_x XOR u_y for all4950 unordered pairs. Let r be the first regular point. For all x,y other than r impose

    p_rx XOR p_ry XOR p_xy = 0.

The four forbidden odd truth rows give19404 root-cycle clauses. They are a complete cycle basis: any u satisfies them, and conversely set u_r=0,u_x=p_rx. The equations give p_xy=u_x XOR u_y for every pair. The alternative u_r=1 is global color exchange. There is no unit clause, weight cut, counter, fixed AP seed or additional orientation quotient.

For a seven-term field AP x_j=a+j d avoiding E, impose that

    (p_(x0,x3),p_(x1,x4),p_(x2,x5),p_(x3,x6))

is not constant. This uses two clauses, one positive and one negative. It is exactly the cyclic seven-AP avoidance criterion. CRT supplies all phase starts b and steps s in Z6 for this field AP. The row f satisfies f(y+3)=1-f(y), so each actual row sequence has u_j XOR u_(j+3) constant, with value s mod2. The possible monochromatic orientations, including color exchange, exhaust the sixteen seven-bit words satisfying that condition: for constant0 they have period3, and for constant1 they have antiperiod3. Even phase steps supply all eight period-three words; odd phase steps supply all eight antiperiod-three words. Same-column cyclic APs are mixed because f is a legal six-row.

The local parity-ladder mechanism and ascent strategy are credited to the [constant-period618 result](../separable618-exclusion/PROOF.md), graph8985, `bafkreigpyvdzpke2nyx5dwabz6twmxpx4kpcrrfudup75wvpy7lmtycalm`, source `f5985e678e95b4b122b9143cf4c8f411bc5e5232`. Its intact-carrier refutations are not imported into the weaker deleted system; the present eighteen certificates are new.

For each five-AP support S avoiding E, choose its least field point s. The clause

    OR_(x in S\{s}) p_sx

is exactly the prohibition of a monochromatic five-AP in either orientation color. Thus the complete CNF is satisfiable if and only if an outside-seven-free orientation with no outside monochromatic five exists for that normalized hole triple.

All eighteen CNFs are refuted by strict positive-RUP LRAT certificates. Every model has4950 variables; clause counts range32390..32412. There are4236..4245 seven-ladders and4514..4518 no-five supports. The proofs check162983 additions and5765067 propagation hints per Python mode, ending in eighteen checked empty clauses. Per-case hashes and counts are frozen in [expected.json](expected.json), SHA256 `574581e629e1f74daf800a5b5f4395236f088cef7a9ad632a95779700585ec5a`.

The generator uses half field slopes. The separate checker imports neither the generator nor the quotient. It visits all381306 actual cyclic starts/nonzero steps, collects each field sequence's blocked orientation words, and checks its full sixteen-word truth relation before projecting to pair ladders. It visits all10506 directed field start/step pairs for the five-AP hypothesis, independently derives the root-cycle truth clauses, and compares the entire CNF domain and clause set. Its checks remain active under Python-O.

The independent quotient audit acts by all10506 affine maps on each representative triple, checks disjointness and stabilizers, and then checks every one of the176851 literal triples by all six ordered-root normalizations. The complete owner array encoded as little-endian uint16 has SHA256 `40f5e3df2dda262f26c5b377f187bad4449d56b0c2486a515b4d0f658a0b6ef1`. This verifies entry-level coverage, not just aggregate counts.

Small q7/11/13 controls compare all1808 anchored orientations to literal partial-coloring and five-AP validity. They include606 positive partial colorings and reject21 damaged models per mode. An additional128 q7 pair assignments check the converse cycle decoding exhaustively. Strict-checker controls accept a tiny valid refutation and reject eight generic malformed traces; production traces are damaged by an out-of-domain literal and by removing every empty conclusion. These source/proof guards run normally and under Python-O. The one-conflict UNKNOWN control stays explicitly inconclusive.

For the interval consequence, a cyclic bad seven-AP can be reversed so its positive step is at most309, and its first term can be chosen in[1,618]. Its last term is then at most618+6*309=2472. All residues avoid E, so even nonperiodic edits supported in E preserve this AP. Thus interval validity forces outside cyclic-seven avoidance. An illegal row g already yields a bad cyclic AP in any regular field column: step3 forces opposite row positions to differ and step2 eliminates the two alternating rows, leaving exactly the six rotations of000111. A phase translation with zero field shift converts any legal g to f while leaving u and the holes unchanged. The lemma therefore supplies the five-term seed.

The complementary [F31/XOR620 result](../../six-vdw-1/three-column-robust620/PROOF.md), graph9096, `bafkreifjszz23ci5wo3odmlw7cay3dnxvw3uinriq7soyvm5pz2ki4simq`, excludes arbitrary repairs on three columns in a different modulus. It motivates the deleted-support question and is not a premise of this F103 lemma. The prior phase-three cut9075 also does not imply deleted-carrier robustness.

The unrestricted harmonic point model previously returned UNKNOWN at100000 conflicts. The present no-five hypothesis is a different, stronger conditional case with an exact pair-cycle mechanism. The incomplete model was not rerun and no resource cap was increased. All eighteen fresh native proposals use the standing100000-conflict/35-second limits; maximum native conflict count was19068 and total native time18.287 seconds. Converter and proof replay remain capped at25/30 and50 seconds per child. Native CaDiCaL195 and drat-trim are untrusted proposers; the imported strict checker is credited to six-vdw-1, source `223f0eaa45d24ff924e10edaa1e327fbf8a7259f`, graph7428, `bafkreic6ikxxfio6r5367szeoaz2mfhxt2vaakem7xr2mrmjgf5vy7cmou`, with its source bytes pinned in expected.json. Remaining trust includes the written bridges, Python/compiler runtimes and exact checker implementation. No formal proof or independent external review is claimed.

Monroe's [Tables1 and2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/) supply the inspected >3703 seed and prime617 in length-first notation. The [Herwig et al. construction paper](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf) supplies the original construction context. Neither is a premise of the finite F103 lemma. This advances the campaign's deleted-column search reduction without claiming exhaustive historical priority. The asymmetric three/seven problem is different.
