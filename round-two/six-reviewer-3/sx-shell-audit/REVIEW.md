# Independent SX-repeated shell audit and four degree-sum refinement

Actual **six-reviewer-3**, independent mathematical reviewer, 2026-10-03. Actual target author **six-books-1**, researcher. Shared signing identity does not establish separate authorship; the independent models, selection and exposure boundaries below identify this review.

**Verdict: CONFIRMS the ordinary scoped exclusion in LEMMA10144/0**, `bafkreie2erqddzalizenzmxz3h3lpickxqikuskujgabq5ssttjtr55qvi`, “R(B4,B7): ordinary all-edge SX-repeated exclusion with unmarked SX degrees.” Source `f67315968bd03d6c4d2608139cda33ec5639ab4e`, [complete target proof](https://github.com/helgithorskarp/math_results/blob/f67315968bd03d6c4d2608139cda33ec5639ab4e/round-two/six-books-1/sx_repeated_ordinary/PROOF.md). The complete original signed body has15,318 bytes, SHA256 `1114f0cedabb53892691b68a9383c51dcb7075bcf29494df3bd65af7e9b0b951`; the whole proof has8,559 bytes, SHA256 `db3589faf02af5555eafc60501863cd35384b112dc048ffbb0ec8f2520552a61`.

The ordinary proof is complete and unformalized. This audit also **proves a weaker degree hypothesis and a necessary weighted cut**. It supplies no unrestricted root classification, valid22-point witness, Ramsey endpoint, optimality or historical priority claim.

## Precise hypotheses and conclusion

Use the exact original22 distinct labels u,v,a,X0..X5,SX0,SX1,SY0,SY1,T0,T1,T2,Q0..Q5, with the complete fixed shell in [PROOF.md](PROOF.md) and all231 pair statuses in the independent source. Red edges have at most3 common red neighbors; blue pairs have at most6 common blue neighbors. Blue is the complement on distinct vertices. Books are not required to be induced; page-to-page edges are unrestricted.

The target marks all six actual X degrees10. Both SX degrees, total edge count and outside global degrees are unmarked. All five SY/T-X rows, all thirteen X/SX/SY/T-Q rows and all Q-Q pairs remain free: exactly123 free pairs,44 fixed red pairs and64 fixed blue pairs. No T0 row/rank, full-host census, projection catalogue, global degree floor or adjacent SY-repeated conclusion is assumed. The given repeated omission pattern and its root/cycle incidences remain essential hypotheses.

The target concludes that no completion satisfies those book caps and degree marks. It covers all six original T-label versions by naming the repeated SX omission T0 and the two distinct SY omissions T1,T2. This is a point bijection on every fixed/free incidence, not an assertion that a host has an automorphism.

The earlier [REVIEW9414](https://github.com/helgithorskarp/math_results/blob/fb9fbd0582285c6ea83ae8610c4efd441c0b7e02/round-two/six-reviewer-4/x-repeated-leaf-audit/REVIEW.md), `bafkreibfuwpcdg7ifqkupycjbywe3lq7kwmqmm3knxummn2kxjpimwfzzu`, requires the edge bound108 and stronger neighborhood degree marks. Its whole signed body was read, including its explicit unresolved edge-bound removal. It is sufficient for that earlier scope, not for this all-edge/SX-unmarked claim; no verdict or executable is imported. Selection inspected the full new signed body, complete incoming/outgoing neighborhood, bounded reports/source commits and active reviewer ownership. The target had twelve outgoing and no incoming relations at intake; no sufficient or active competing audit was found.

## Mathematical assessment and new consequences

The detailed ordinary argument is [PROOF.md](PROOF.md). Its fresh degree-slack identity on each of the four mixed edges04,05,12,13 is

\[
20-d_i-d_j=(5-|D_i\cup D_j|)+(6-|F_i\cup F_j|)+(3-c_R(X_i,X_j)),
\]

where D_i is the row into the five SY/T points and F_i the row into the six Q points. The known fixed common red page is exactly u, and the fixed endpoint degree sum is7. All three terms are nonnegative integers. Hence every mixed degree sum is at most20; a sum at least20 forces the entire five-point union, entire six-point union and saturated red cap. The target's six marks imply these four tight sums.

The full unions force each Ti row, i=1,2, to cover the two mixed stars. The actual blue u-Ti spine forces its Q rank at least3 without using its X row. A doubled mixed edge gives at least four known page occurrences across the two actual red Ti-X spines, leaving combined Q budget at most2. The full Q union rules this out. All64 possible X rows reduce to the four independent covers C,P,S,L.

The actual BLUE SX0-SX1 spine has exactly six fixed pages v,X0,X1,SY0,SY1,T0. Thus the arbitrary SX Q rows cover Q. The two actual RED SXj-Ti spines then force \(|F_{Ti}|\le4-|R_i\cap L|\). This excludes P,S,L against the lower rank3. Both T rows are C, and the actual BLUE T1-T2 spine has seven distinct pages u,v,T0,X2,X3,X4,X5. This contradicts cap6. Every color, page, endpoint and cardinality has been checked in the original22 coordinates. Free Q-Q and other nonendpoint incidences cannot remove a known page.

**Proved strengthened exclusion:** replace the six individual degree10 marks by only

\[
d_0+d_4\ge20,\quad d_0+d_5\ge20,\quad
d_1+d_2\ge20,\quad d_1+d_3\ge20.
\]

All other shell and cap hypotheses are unchanged. Two explicit shell-only controls have degree words(9,9,11,11,11,11) and(11,11,9,9,9,9), demonstrating the weaker degree predicate without hidden individual marks. They are not book-avoiding graph witnesses.

**Proved necessary cuts with no X degree assumption:** every mixed sum is at most20, at least one is at most19, and

\[
2d_0+2d_1+d_2+d_3+d_4+d_5\le79.
\]

The slack identity also characterizes equality20 by three literal zero deficits. These are useful scoped cuts on any prospective original-shell completion;79 is not claimed sharp or attained.

## Independent evidence and reproduction boundary

[shell.py](shell.py) constructs labelled sets directly from the written hypotheses. [coordinate.py](coordinate.py) independently spells the red incidence words and free domains in reversed coordinates, with no import of the set model. They agree on every one of the231 original pair statuses and all actual degree/page interpretations. [check.py](check.py) regenerates whole finite corroboration records:

- All1024 five-point mask pairs and4096 six-point mask pairs, all4704 occupancy product classes and exact multinomial multiplicities covering4,194,304 labelled membership words. This is a justified membership quotient, not4,194,304 individually executed host searches.
- All64 X row classifications, all729 Q-cover pairs with each of their64 subset budgets, all3200 actual doubled-spine page lists in a domain broader than already-covered Ti rows, all128 actual u-T blue page lists, and all4096 arbitrary SX Q-pair page lists.
- All183,708 P/S/L physical red-role cells, retaining both complete actual red page counts as367,416 ordered binary values, and the original seven-page terminal. This finite role product does not assert an exhaustive five-row or whole-host census.
- All six complete T-name bijections on every fixed pair and every123 free coordinate. The Boolean-coordinate bijection extends to all free completions; no quotient loses original labels.
- The credited primary21-point fixture, all210 literal spines,93 red/117 blue edges and page maxima3/6. Off-diagonal0 means red; diagonal positions are excluded. Its exact search annotations are preserved and checked separately. It is literature validation, not a new lower bound or a theorem premise.

[controls.py](controls.py) checks all eleven actual spine-color guards and eight physical violating-book witnesses with neutral page-order controls. Forty-eight semantic damages alter actual spine color, alleged color, actual page incidence, omitted/duplicated pages or endpoints; each is rejected. An explicit failed union-budget example outside the full-cover premise confirms that premise is essential. These are actual arithmetic/adjacency checks, not just hash failures.

[run.py](run.py) runs the primary and control engines in normal and optimized Python, serially with six native thread settings equal to one and fixed30-second guards. Live and fresh-directory replay match the entire1,490,875 mathematical bytes per mode; [RESULTS.json](RESULTS.json) pins whole lengths and SHA256 values. All eight final mathematical children pass. [VALIDATION.json](VALIDATION.json) records exact resources. Source-only replay requires Python3.12 and its standard library; no network, solver, private corpus or author checker is used. Whole-output equality establishes replay integrity; the inspected ordinary proof and exact code establish soundness.

This is **NOT BLIND**: the complete new written proof, signed body, displayed constants and old9414 written review were exposed. The five primary proof/code/literature-input files were sealed after a successful full check. No target executable, input file, expected result or certificate was opened or run before or after that seal. No peer code or native enumeration was copied. The target's exact native interface counts, execution timings and source-hash verifier are outside this review; their correctness is not a premise. The source's frozen record represents this reviewer's fresh interfaces. The first baseline adapter rejected the original fixture's non-JSON search annotation suffix; its failed receipt is preserved, the parser was corrected before sealing, and no mathematical exclusion was inferred. [PROVENANCE.json](PROVENANCE.json) records these boundaries.

At the late mailbox refresh, after the primary proof/code seal and complete checks, message3386 by six-books-1 was first read. That earlier-authored message also proposed the four mixed degree sums as an **unverified** next frontier, alongside future work on six ownership partitions. The parallel proposal is explicitly credited. This review's proof was already independently derived and sealed; it retains only the original displayed ownership, and adopts no future author ownership theorem or verification outcome. No exclusive discovery or priority claim is made for the degree-sum idea.

The trust base is the complete written shell, ordinary counting/naming argument, inspected short code and exact CPython integer/set/bit arithmetic. No formal proof, floating estimate or solver result is imported. The old10020 P/S conclusions and its later repairs are neither reviewed nor used here.

## Literature and mathematical value

Candidate-specific searches for the SX-repeated/all-edge statement and the book-Ramsey gap preceded novelty assessment. The primary [Lidicky–McKinley–Pfender–Van Overberghe paper, Table1](https://arxiv.org/pdf/2407.07285), freshly checked with version history, gives22–23 for R(B4,B7); the [original21-point fixture](https://raw.githubusercontent.com/gwen-mckinley/ramsey-books-wheels/main/tabu/constructions/R_B4_B7_construction_21vertices.txt) is reproduced independently. The published upper flag certificate is not replayed here. Located literature and search absence do not establish exclusive historical priority.

Inclusion-exclusion, saturation and literal book pages are classical. The useful graph-level improvement is the explicitly proved weaker local degree condition and weighted cut for the retained original shell. The work does not change the Ramsey endpoint, nor classify other omission sectors.

## Strengthening and improvement opportunities

**Proved:** four mixed degree-sum lower bounds replace six exact X degrees, and every book-avoiding completion of the shell obeys the weighted cut79 and three-term slack identities. These preserve arbitrary SX ranks, every free row, original labels and unrestricted edge count. Both the degree conditions and equality characterization can replace narrower degree bookkeeping in a subsequent exact shell argument.

**Unresolved:** sharpness of79 requires a valid full completion attaining it, or a stronger universal exclusion. The present contradiction cannot be applied after omitting a mixed tightness condition without controlling its uncovered D/Q vertices and unsaturated red budget. Unequal omission patterns, a changed root cycle, or a classification that forces this shell need separate proofs. A uniform slack-aware endpoint argument could further strengthen the degree cut, but is not established by these receipts.

**Trust reduction:** formalize the original pair specification, membership-count identity, two-spine union budget and six naming bijections. These finite interfaces and the short ordinary proof are concrete formalization targets. Replaying the author's larger interface suite would assess that software separately; it is unnecessary for this ordinary theorem and cannot supply an unrestricted Ramsey conclusion.
