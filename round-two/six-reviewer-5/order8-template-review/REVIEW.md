# Independent H8 exclusion audit and sharp coset-interval classification

Actual author **six-reviewer-5**, role **independent mathematical reviewer**, 2026-10-01. Shared campaign signatures do not establish distinct authorship. The target was selected independently from committed claims and review coverage; neither a target nor a verdict was assigned.

**Target:** h8589, `bafkreig6vduxcumksa6rlxapslnw2rmgdb4uq3ht5dhzborxfqgbjsp5ki`, “W(2,7): complete order-eight F617 exclusion and nonquadratic stabilizer bound seven,” explicitly authored by six-vdw-2. [Original proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-2/order8-rigidity/PROOF.md). Audited target source commit: `9e470a87f252beba837e06a4e40278cba1953bc1`.

**Verdict:** confirmed with high confidence as a complete exact computer-assisted exclusion of the specified punctured-field template family. Every field constraint, every normalization clause and every positive-RUP proof addition was checked independently. The nonquadratic multiplicative-stabilizer corollary follows with its attributed earlier rigidity premise. The review also proves a sharp consecutive-coset AP-free classification and transfers the stronger threshold to the previously studied full affine stabilizer. No interval construction, unrestricted van der Waerden upper bound, historical priority or proof-assistant formalization is claimed.

## Statement and scope

Let \(F=\mathbb F_{617}\), \(H=\langle3^{77}\rangle\) of order eight. A binary coloring \(c:F^*\to\{0,1\}\) is admissible when every seven-term progression
\[
a,a+d,\ldots,a+6d,\qquad a\in F,\quad d\in F^*,
\]
whose seven terms are all nonzero contains both colors. This includes field wraparound and every nonzero difference. It places no color at zero. The theorem asserts that no admissible coloring is invariant under multiplication by every member of \(H\).

Invariance is equivalent to a word of 77 bits on the cosets \(3^iH\), with indices in \(\mathbb Z/77\mathbb Z\). The exclusion covers all \(2^{77}=151115727451828646838272\) labeled words, not an enumerated sample or a limited equal-pair subclass. It does not concern every coloring of a long integer interval. The earlier logarithmic equal-pair floor is not a premise of this complete proof.

## Independent field and encoding audit

[field.py](field.py) imports no author module. Complete trial division through 24 establishes primality. Repeated multiplication by \(3^{77}\) constructs the eight literal subgroup elements. Each successive representative \(3^i\) multiplies that subgroup to an eight-element set. These 77 literal orbits are disjoint and cover all 616 nonzero elements; the representative returns to \(H\). Direct membership checks verify that multiplication by three advances every coset label by one. This construction uses neither the author's full discrete-log table nor the author's auditor's Euler-quotient labels.

The independent AP census uses reversal classes. Reversing an ordered progression sends
\[
(a,d)\longmapsto(a+6d,-d).
\]
This involution has no fixed point, and exactly one difference of the pair is in \(\{1,\ldots,308\}\). Enumerating all 617 starts at each such difference therefore covers every one of the 380,072 ordered pairs, by 190,036 two-element classes. Reversal here means reversing the seven actual field terms; it does not identify a coset word with its reversed word or use field inversion as a symmetry.

Exactly 2,156 reversal classes contain zero and are removed; the other 187,880 classes give all 375,760 ordered nonzero APs. Repeated coset labels collapse to a set because invariance makes those terms have the same color. The complete set has 23,177 supports:

| Support size | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|
| Count | 77 | 231 | 4543 | 18326 |

Its canonical SHA256 is `8de2239f6c3e7f7c6926e11399eeb61ab205f6f9030fc7b636efc5f158e8a297`; the literal coset partition hash is `70b36c146f9cbc502b20b806a1a9dec88cd95ad0e9558f2967fdcc607228cf61`.

For each support \(E\), admissibility is exactly the conjunction
\[
\bigvee_{i\in E}y_i,\qquad \bigvee_{i\in E}\neg y_i.
\]
Every one of the seventeen case CNFs is parsed from its actual bytes and compared with the independently reconstructed complete clause multiset. Literal order is ignored, but clause multiplicities are retained. The resulting exact CNF hashes agree with every published reference. Proof clause identifiers are subsequently bound to the original clause order in those same audited files; multiset comparison does not reorder a proof input.

## Complete longest-run cover

The actual AP \((a,d)=(3,34)\) has terms
\[
3,37,71,105,139,173,207
\]
and labels \((1,8,1,2,0,18,8)\), hence support \(\{0,1,2,8,18\}\). Literal field arithmetic checks the ordered AP and all 77 multiplications by \(3^s\). A monochromatic cyclic run of length at least 19 contains one of these supports and is impossible. Constant words are also excluded. Since the cycle length is odd, an everywhere-alternating binary word cannot close, so the longest run \(L\) is at least two.

Choose any longest run, rotate its start to zero and complement its color to zero. Rotation is actual field multiplication; complementation preserves not-all-equal. Because the run is maximal and shorter than 77, its two neighbors have the other color:
\[
y_0=\cdots=y_{L-1}=0,\qquad y_{76}=y_L=1.
\]
No cyclic window of length \(L+1\) is monochromatic. Conversely the two not-all-equal clauses for every such window impose maximum run at most \(L\), and the displayed units exhibit a maximal run of length \(L\). Thus the normalized cases \(L=2,\ldots,18\) cover every possible admissible word. Cases may contain several equivalent representatives; orbit counts are unnecessary for an exclusion. No reflection symmetry, parity approximation or unjustified canonical representative is used.

Each case has 77 variables and exactly \(46510+L\) clauses: 46,354 field clauses, 154 window clauses and \(L+2\) normalization units. All boundaries and cyclic windows, including those crossing zero, match the independent definition-level construction.

## Independent proof replay

[rup.py](rup.py) reuses this reviewer's independently published signed-set positive-RUP implementation from h8522; [check.py](check.py) binds it to these seventeen new case files. Clauses are immutable sets of signed literals; separate true/false sets implement unit propagation. The target's checker instead uses tuple scans with a Boolean assignment dictionary. No author proof checker is imported. The reused mechanism is credited rather than presented as newly invented.

For an addition \(C\), assign every literal of \(C\) false and follow the supplied active clause identifiers. An unsatisfied hinted clause must be unit or conflicting. A unit forces its remaining literal; a conflicting clause ends the assumptions. Thus each accepted addition is a consequence of the active clauses. Deletions only remove available clauses and do not invalidate their already established consequences of the original formula. Induction therefore establishes the checked terminal empty clause as a consequence of the original CNF.

The checker requires fresh increasing addition identifiers, in-domain nontautological clauses, available deletion/hint identifiers, positive hints, proper terminators and a terminal checked empty clause. It rejects content after the empty conclusion. Its strict supported proof subset suffices for every actual trace; arbitrary RAT traces are not supported or implicitly trusted. Explicit exceptions implement every acceptance condition in both Python modes.

All seventeen refutations pass independent replay, with **88,429 additions and 1,297,242 propagation hints**. Every per-case input hash, addition count, deletion count and hint count matches the published reference. All seventeen regenerated proof files also match the reference SHA256 values. [EXPECTED.json](EXPECTED.json) records every exact case receipt. CaDiCaL195 and drat-trim propose these traces; their UNSAT/VERIFIED messages are outside the proof's soundness boundary.

## Strengthening and improvement opportunities

**Proved sharp consecutive-coset classification.** Fix this cyclic order, defined by the primitive element three. For \(s\in\mathbb Z/77\mathbb Z\) and \(0\le q\le77\), let
\[
B_{s,q}=\bigcup_{j=0}^{q-1}3^{s+j}H.
\]
Then \(B_{s,q}\) contains no nonconstant seven-term field AP **if and only if \(q\le18\)**. In particular every 144-element union of 18 consecutive cosets is a seven-AP-free field subset; adding the next entire coset introduces an AP. These are one-color subset statements, not two-color field certificates or interval records.

To prove sharpness, for each sorted support \(E=(e_0,\ldots,e_{r-1})\), compute its cyclic gaps. If \(g\) is the largest gap between successive support indices, its shortest containing cyclic window has width
\[
77-g+1.
\]
A covering arc omits a gap, so maximizing the omitted gap minimizes its width; inclusion of both end indices gives the final \(+1\). This covers every possible start without guessing one.

The complete independent support census has minimum width exactly 19. Exactly **77** supports attain it, and every one, after moving the beginning of its shortest window to zero, is \(\{0,1,2,8,18\}\). They are precisely its 77 rotations. The next occurring width is 26. Therefore no AP can lie in any 18-coset block, while the literal scaled critical AP lies in every 19-coset block. At length 19 there is exactly one distinct quotient support in the block: the minimizing shape has unique largest gap 59 and both window endpoints, forcing its window start. The entire width histogram, minimizing count and a literal witness appear in the exact receipt.

This proves optimality of 19 for the target's single-AP consecutive-window barrier in the **specified** cyclic order. It is not optimality of a general CNF reduction, the number of cases, certificate size, or a run bound after another primitive generator reorders the cosets.

**Proved conditional affine refinement.** Let a binary full-field coloring \(C:F\to\{0,1\}\) avoid every nonconstant seven-term field AP, and let \(G\) be its color-preserving affine stabilizer. Either it is a quadratic-residue block centered at some \(b\), with either center color and optional global complement, and \(|G|=308\); or
\[
|G|\in\{1,2,4,7\}.
\]
In particular \(|G|\ge8\) forces the centered quadratic form. This strengthens the previously reviewed threshold 11 using the newly certified H8 exclusion. The fixed-point reduction is established prior work, explicitly re-derived here, and the order-at-least-eleven punctured-field rigidity theorem remains imported.

A nontrivial translation would generate all 617 translations and force \(C\) constant, contradicting admissibility. Hence the multiplier map \(G\to F^*\) is injective. Thus \(G\) is cyclic and its order divides 616. If it is nontrivial, choose \(x\mapsto ax+d\) with \(a\ne1\). It has unique fixed point \(b=d/(1-a)\). Every commuting member of \(G\) must fix \(b\), so translation to that center conjugates \(G\) to a multiplicative subgroup. Restriction of \(C(b+x)\) to nonzero \(x\) is exactly an admissible punctured-field coloring. The audited H8 theorem excludes stabilizer order eight; the older theorem forces the quadratic pattern at any order at least eleven. Divisibility leaves only \(1,2,4,7\) for a nonquadratic block. For a quadratic block, all 308 square multipliers preserve its color, independently of the center color. The full affine stabilizer fixes that center by the same injectivity/commutativity argument, and a nonsquare multiplier changes the nonzero colors. Its order is therefore exactly 308.

This gives no existence result for nonquadratic admissible colorings at orders 2, 4 or 7. The lower orders are possible subgroup orders, not demonstrated examples.

**Unproved practical directions.** Another primitive element may give a shorter single-AP window barrier and smaller proof workload; a complete reordered support census and certified replacement case cover would be needed. Extracting a smaller unsatisfiable AP-support core could reduce verification cost, but removed-clause completeness and every proof input would need independent checking. The natural unresolved stabilizer frontier remains order seven/index 88. A timeout or UNKNOWN there would establish no exclusion. No unrestricted interval conclusion follows from punctured-field symmetry restrictions.

## Earlier rigidity premise and provenance

The target's stabilizer corollary imports h `bafkreiebd2xk3lixbmcgk3ddfmgqwpgnmvhaa37vkweidlnweeyi7jggem`, the order-at-least-eleven rigidity theorem. Its stated domain is exactly the same punctured-field AP admissibility, not only a chosen interval. Its [published source](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_617_order11_rigidity/README.md) and the existing [independent review](https://github.com/helgithorskarp/math_results/blob/main/van_der_waerden_617_affine_rigidity_review3/README.md), h7272 `bafkreibziig3wb5bald3tkrlp3mdnnpylpjo2tbff3kku3z3smuqkh3sr4`, supply the attributed prior proof and affine reduction. Their graph bodies and quantifiers were inspected. This review does not duplicate that already sufficient exhaustive audit.

For the target's multiplicative corollary, the color-preserving stabilizer is a subgroup of order dividing \(616=8\cdot7\cdot11\). The earlier theorem excludes a nonquadratic stabilizer of order at least eleven. The only remaining divisor between eight and ten is eight, and its subgroup is uniquely \(H\); the newly checked exclusion removes it. Therefore its possible orders are exactly among \(\{1,2,4,7\}\), with no existence assertion. This bridge is an ordinary group argument; the earlier classification is the only additional mathematical premise.

The signed-set checker derives from this reviewer's [earlier independent QR617 review](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/qr617-three-run-review/audit.py), h8522 `bafkreieaq7gexuzk74iwimygbran3sejznknwk5fgrrmemsrwhbhoqxdhi`. Its empty-initial-formula parser boundary is broadened here to include the empty family in independent truth controls. That changes no production case or inference rule.

## Reproduction and adverse checks

From a full checkout with CPython 3.11+, GCC and the pinned [requirements.txt](requirements.txt), run

```bash
python3 -B round-two/six-reviewer-5/order8-template-review/reproduce.py \
  --repository-root . --output-dir /tmp/reviewer5-order8-run
```

Use a fresh output directory. [README.md](README.md) gives installation and sparse-checkout details. [INPUTS.json](INPUTS.json) pins the three author proposal inputs and official converter source. The runner independently audits all CNFs before proposing proofs, runs the solver with at most 50,000 conflicts, bounds conversion internally at 25 seconds, and gives every child an unchanged external 30-second guard. Children are sequential with all numerical threads set to one. A native status is never counted as a mathematical exclusion. Both exact audit/checker modes run, and every stable receipt must match the compact fixture.

The complete final run took **86.31 seconds**, peaked at **98,920 KiB child RSS**, and had largest stage **11.78 seconds**. All reference proof bytes matched. The original author reproduction also separately passed, including its one-conflict UNKNOWN control. That incomplete control supplied no exclusion. Generated CNFs, native binaries and proof corpora remain in local scratch and are not published.

[controls.py](controls.py) truth-classifies all 256 families of the eight nonempty nontautological clauses on two variables: its separately constructed complete assignment-tree RUP refutations pass for all 161 UNSAT families, and forged empty conclusions fail for all 95 SAT families. Boundary-gap analysis on all 2,728 small odd-cycle words checks 2,718 nonconstant normalizations and 25,488 complete cyclic-window equivalences. Ten actual production corruptions are rejected: removed field clause, missing or reversed boundary, altered window clause, unavailable or negative hint, out-of-domain literal, missing empty conclusion, unavailable deletion, and post-empty content. Both ordinary and optimized Python give identical results. These tests supplement the universal run-cover argument and proof induction; they do not replace them.

The trust boundary consists of exact Python integer/set arithmetic and interpreter, SHA256 input integrity, strict DIMACS/LRAT decoding, the finite-group and cyclic-cover proof bridges, and the explicitly imported older rigidity theorem for the stabilizer conclusions. No solver/transformer message, floating calculation, incomplete search or hidden symmetry quotient is a proof premise. No formal proof assistant was used.

## Literature status and readiness

Multiplicative prepartitioning and power-residue constructions are prior work, described in [Heule, Section 4.3](https://www.cs.cmu.edu/~mheule/publications/JOC_08_03_A01.pdf). [Herwig and collaborators](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf), Table 3, record the 617 power-residue construction. [Monroe, JCMCC 128](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/), Tables 1–2, record the two-color/seven-term \(>3703\) seed and prime 617, using the reversed argument convention. Here \(W(2,7)\) always means two colors and seven terms.

Bibliographic correction: the first graph review, `bafkreiaxrtekhdg6xo6bmttoo2rvx5s57v2usnbpsudyuidcjwxahxabpe`, incorrectly identified Herwig's table as Table 2. The 617 row is in Table 3 (PDF page 11). This revision corrects that citation; its mathematical statements, computations and verdict are unchanged.

Candidate-specific searches on 2026-10-01 included 617 with “order eight,” “H8,” “seven-term,” “stabilizer,” and van der Waerden terms, together with the inspected primary papers and pertinent graph. No identical external complete H8 exclusion or sharp coset-interval classification was located in this bounded search. This is not proof of historical priority. The target's complete H8 theorem is a genuine graph-level strengthening of its earlier defect restriction, while the prepartitioning method and older affine fixed-point argument are credited prior art.

The scoped theorem is ready as an independently checked exact computer-assisted lemma, with compact reproducible source and all known premises explicit. The affine and multiplicative corollaries retain the old rigidity dependency. Formalizing the encoding/run-cover bridge or independently checking with another proof kernel could strengthen assurance, but no unresolved mathematical gap was found in the audited claim. The main 3704-point coloring objective and unrestricted van der Waerden bounds are unchanged by this result.
