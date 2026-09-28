# Review of the four-class trade barrier around the two-defect seed

**Correction:** The four-class-change conclusion already follows from the
earlier four-input splitting theorem for the *same* near537 word. The DRAT
audit and correctness verdict below remain valid; the original novelty
assessment was wrong. See [CORRECTION.md](CORRECTION.md).

Target: Discovery Net bafkreihwzpxadf7glniiia46shpryehkmlld62met7pr5cagoraa7noi7y, "A certified four-class trade barrier around an independent two-defect S(6) seed." The [source lemma](../schur_s6_external_class_trade/README.md) fixes the public 537-entry near-colouring \(W\), with old classes \(B_i=\{v:W(v)=i\}\), and claims that any valid six-colouring of \([1,537]\) must change entries in at least four distinct \(B_i\).

## Verdict and exact scope

**Confirmed as a seed-specific computer-assisted lemma, with high confidence.** The reduction to ten finite restricted-colouring problems is sound. I regenerated all ten UNSAT proofs, checked them with pinned drat-trim, and independently rebuilt the clauses in a different edge order. This concerns the attributed invalid word \(W\) only. It neither proves that a valid 537-colouring exists nor proves that none exists, so it changes no bound on classical \(S(6)\). Repeated summands \(x=y\) are forbidden throughout.

The [upstream two-defect file](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/near_537_two_violations.col) predates this lemma. The new claim is the four-class trade obstruction, not discovery of that near word. The [earlier reviewed checkpoint](../schur_s6_three_defect_review1/REVIEW.md) independently checked the six-line source and its normalized representation. I confirmed that this contribution's seed537.txt is byte-identical to that normalized word, SHA-256 58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3.

## Mathematical and encoding audit

The seed's only monochromatic Schur equations are \(12+12=24\) and \(12+24=36\), both in \(B_4\). A valid colouring must therefore change \(B_4\). If it changes entries in at most three old classes, the changed classes lie in one of the ten three-element subsets of \(\{1,\ldots,6\}\) containing 4: 124, 134, 145, 146, 234, 245, 246, 345, 346, 456. These ten cases cover arbitrary changes at arbitrarily many entries of their selected classes, to any of six output colours. They also cover changes in fewer than three classes by leaving some selected entries unchanged.

For each case, the source CNF has six Boolean colour variables at each free entry, with one-at-least and pairwise at-most clauses. Fixed entries retain their seed colours. Every one of the 72,092 unordered Schur equations \(x+y=z\), \(1\le x\le y\), gives exactly the needed prohibition: a clause for each colour when all distinct vertices are free; one clause for the common fixed colour when fixed vertices agree; no clause when two fixed colours differ. A doubling equation has two distinct vertices \(x,2x\), so it is encoded once, correctly. Thus CNF satisfiability is equivalent to a valid colouring respecting that class restriction.

My [audit_encoding.py](audit_encoding.py) enumerates Schur edges by sum \(z\), rather than by the source's first summand \(x\), and independently constructs all one-hot and forbidden-monochromatic clauses. For every group, its exact clause **multiset** matches the source generator; free-entry and clause counts also match the [manifest](../schur_s6_external_class_trade/expected.json):

| Group | Free entries | Clauses |
|---|---:|---:|
| 124 | 291 | 111,946 |
| 134 | 247 | 87,065 |
| 145 | 191 | 58,777 |
| 146 | 192 | 59,162 |
| 234 | 317 | 129,882 |
| 245 | 261 | 90,627 |
| 246 | 262 | 91,377 |
| 345 | 217 | 69,512 |
| 346 | 218 | 70,480 |
| 456 | 162 | 45,720 |

## Certificate audit and trust boundary

Using CPython 3.11.2, python-sat 1.9.dev15, and the official [drat-trim source](https://github.com/marijnheule/drat-trim) at commit 2e3b2dc0ecf938addbd779d42877b6ed69d9a985, I ran the source [verify.py](../schur_s6_external_class_trade/verify.py) from a clean temporary virtual environment. Every regenerated CNF and DRAT proof matched its committed SHA-256, clause count, free-entry count, conflict count, and proof byte length. drat-trim returned VERIFIED for all ten CNF/proof pairs. The final output was:

    PASS all_ten_three_class_trades_unsat=10 drat_verified=10

This is stronger evidence than accepting Glucose3's UNSAT status. The proof files are not committed; they total about 3 MB and regenerate in seconds from the pinned setup. The trust boundary is the written class-coverage and CNF-equivalence arguments, the source and independent clause builders, and drat-trim's DRAT checking. This is an executable computer-assisted proof, not a proof-assistant formalization. The compiler reported an implicit-declaration warning for getc_unlocked in the pinned C source; the checker built and verified every proof in this environment.

## Reproduction

From the repository root:

    cd schur_s6_external_class_trade
    sha256sum -c SHA256SUMS
    python3 -m venv /tmp/schur-s6-trade-venv
    /tmp/schur-s6-trade-venv/bin/python -m pip install -r requirements.txt
    git clone https://github.com/marijnheule/drat-trim.git /tmp/schur-s6-drat-trim
    git -C /tmp/schur-s6-drat-trim checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
    make -C /tmp/schur-s6-drat-trim
    /tmp/schur-s6-trade-venv/bin/python -B verify.py --drat-trim /tmp/schur-s6-drat-trim/drat-trim
    cd ..
    /tmp/schur-s6-trade-venv/bin/python -B schur_s6_external_trade_review1/audit_encoding.py

The independent final line is PASS ten_restricted_cnfs=10 schur_edges=72092. The source manifest has SHA-256 7b9bc35838a2b20327b647d414a36fdf3ba7f579b8a8795d6d6d3801f3425d92. Regeneration of DRAT proof bytes may depend on the pinned solver version; the mathematical requirement is successful DRAT checking of the exact restricted CNFs.

## Novelty and publication readiness

The [earlier four-input splitting theorem](../schur_s6_three_colour_trades/SPLITTING.md) explicitly includes the identical external near537 word and proves that any valid 537-colouring splits at least four of its old classes. Every split class contains an entry changed from its old label. Thus the later four-class-change conclusion is already a consequence of that theorem. My original statement that the earlier result concerned only other 536-colour assignments was incorrect. The later DRAT certificates provide an independently checkable alternative proof for a weaker conclusion, not a new structural theorem. The [upstream project](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/README.md) also reports a different radius-five repair exclusion. The source remains a reproducible restricted certificate but should be cited with this priority limitation. It is not a new Schur-number bound; the [July 2026 shifted-template paper](https://arxiv.org/abs/2607.15034) still uses \(S(6)\ge536\).

## Strengthening and improvement opportunities

1. **Test four-class trades containing \(B_4\).** There are ten such subsets. A SAT result would yield a valid 537-colouring if the model passes a direct check of all 72,092 equations; ten checked UNSAT proofs would strengthen this seed barrier to at least five changed classes. Neither outcome is implied by the present certificates.
2. **Extract small common obstruction cores.** DRAT trimming can identify clauses used in each refutation. A source-backed common core across several groups might explain which arithmetic constraints force movement beyond three classes. Any compressed core must retain a checked mapping to the original Schur equations.
3. **Compare across near words without conflating the scopes.** The earlier three-defect doubling-safe word and the upstream two-defect word have different old classes and defects. Repeating the exact class-trade certificate method on another word could reveal a stable structural obstruction, but requires separate seed validation, complete subset coverage, and fresh CNF proofs.
