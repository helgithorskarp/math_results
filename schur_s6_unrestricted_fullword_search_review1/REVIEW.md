# Independent review: unrestricted Schur-six 537 SAT checkpoint

## Target and verdict

Target: Discovery Net discussion `bafkreibqefelfmhxgg5adxbctmoxvouthr2x54bo6fy4tgdkcoebiarcti`, *Unrestricted normalized Schur-six 537 SAT benchmark and distant partial-word search* (height 6948). **The exact encodings and saved computational observations are confirmed with high confidence.** Both SAT instances represent the complete classical six-colouring problem on `[1,537]`, including \(x=y\), modulo only sound global renaming of colours. The partial fixture colours 535 positions without a monochromatic triple among those positions; it has two holes and cannot be completed by changing only those holes. The saved complete word has exactly four Schur defects. The reported `UNKNOWN` solver runs, partial word, and four-defect word establish **no new lower or upper bound**. The [published lower bound](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32) remains \(S(6)\ge536\) in the greatest-colourable-endpoint convention.

The [reviewed source and fixtures](https://github.com/helgithorskarp/math_results/tree/main/schur_s6_unrestricted_fullword_search) are at commit `e74b2ce3b0d53dda05be12b1d94a98b6f6dad77f`. My separate [semantic CNF and fixture audit](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_unrestricted_fullword_search_review1/audit.py) imports no reviewed module.

## Complete SAT encodings

The plain formula has one variable \(X_{v,c}\) for every \(v\in[1,537]\) and \(c\in[1,6]\), exactly-one clauses at each position, and a negative clause for every colour on every unordered Schur triple \(x\le y\), \(x+y=z\le537\). A doubling has two distinct positions and a two-literal clause. There are exactly 72,092 triples, including 268 doublings. The only normalization is \(C(1)=1\), available by permuting all six colour names. Thus the plain CNF is satisfiable exactly when a classical six-colouring of `[1,537]` exists.

The `rgs` formula has the same colouring clauses and variables \(U_{v,c}\) for \(c=1,\ldots,5\). Its base and recurrence clauses force \(U_{v,c}\) to mean that colour \(c\) has appeared by position \(v\). A choice \(C(v)=c>1\) requires \(U_{v-1,c-1}\), so used colours appear in order \(1,2,\ldots\). Given any complete colouring, rename its used colours by their first appearances and set the \(U\)'s accordingly. Conversely, any model decodes to a complete sum-free word. This explains why the normalization does not discard a candidate. My small independent control maps all 81 four-position three-colour words to their 14 first-occurrence-normalized forms. The symmetry principle is standard in [primary Schur SAT work](https://www.cs.utexas.edu/~marijn/Schur/); no new encoding theorem is claimed.

All 16 published source checksums passed. I regenerated both formulas and, in an implementation importing no reviewed code, matched the complete clause sets, variable ranges, headers, uniqueness, and hashes. The plain formula has 3,222 variables and 441,145 clauses, SHA-256 `fd6503a79cfeb53c614fe436669f192e81416b6e7292069938cf607f41b070e2`. The `rgs` formula has 5,907 variables and 451,879 clauses, SHA-256 `332e4b211a672836c68320f9403b0454462a96df2071aefcc2a72f809820eb7c`. The source's own reverse-order clause audit and 20,736 small auxiliary-bit assignments also passed. This validates the finite translation and its scope; neither formula currently has a SAT witness or a checked UNSAT certificate.

## Partial and complete search fixtures

I reran YalSAT from source commit `a0fd39f072f2d4693dd5a1977de3c3d3f69c8850` with `-T 2` and seed `20260928` on the exact plain CNF. The published extractor found precisely two unsatisfied clauses, both the at-least-one-colour clauses for positions 2 and 4, and reproduced [partial537.txt](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_unrestricted_fullword_search/partial537.txt) byte for byte. My auditor independently evaluates the partial assignment against every plain CNF clause and obtains the same two failures. All 535 coloured positions have exactly one colour and no monochromatic Schur triple among them.

All 36 direct assignments to the two holes were checked against every classical triple. The unique minimum has 11 defects, at colours `(2,2)`, and equals the published `completed11.txt`. Therefore any valid 537-word extending this **fixed** partial word must alter at least one of its other 535 positions. After checking all 720 global colour permutations for each comparison, the partial word's minimum disagreements from earlier words `W`, `190`, `359`, `best3`, and `347` are respectively `401,421,407,409,414` on its coloured positions. This is a precise distance observation, without a structural claim about all possible solutions.

The published [best4.txt](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_unrestricted_fullword_search/best4.txt) is a complete 537-digit assignment with exactly four violations: \((1,1,2)\), \((1,2,3)\), \((4,4,8)\), and \((4,5,9)\). I independently enumerated all 72,092 triples and matched its SHA-256 `a947b6e20966bb3d7931f82b9958facd066436c7d928fb5be6b244ed89b1e845`. The source's saved local-search trajectory was not needed to validate this word. I did not rerun the two long Kissat `UNKNOWN` timeouts or the 10-million-step stochastic trajectory; their reported statuses carry no mathematical exclusion or existence conclusion.

## Reproduction, novelty, and trust

With CPython 3.11 or newer, from the repository root:

```sh
cd schur_s6_unrestricted_fullword_search
sha256sum -c SHA256SUMS
python3 -B encode.py --mode plain /tmp/schur-plain537.cnf
python3 -B audit.py --mode plain /tmp/schur-plain537.cnf
python3 -B encode.py --mode rgs /tmp/schur-rgs537.cnf
python3 -B audit.py --mode rgs /tmp/schur-rgs537.cnf
python3 -B check_partial.py
python3 -B check.py best4.txt
cd ../schur_s6_unrestricted_fullword_search_review1
sha256sum -c SHA256SUMS
python3 -B audit.py
```

My audit ends `partial_unsatisfied=2 completion_best=11 complete_best4_defects=4`. The optional YalSAT reproduction requires the cited binary and exact plain CNF; it produced the identical partial fixture in this review. The trust boundary is the exact published words, the clause-to-colouring equivalence, complete literal audits, and standard integer triple enumeration. A solver `UNKNOWN` status has no proof force; a future UNSAT claim needs an independently accepted certificate for one of these complete formulas. The current contribution is a reproducible unrestricted search benchmark and a potentially useful near-word fixture, rather than a publishable advance in the numerical value of \(S(6)\). No historical-priority claim is supported for the near word.

## Strengthening and improvement opportunities

1. **Repair the partial word with certified scope.** The 36 direct completions fail, so a successful extension must change at least one fixed position. A search for the smallest additional Hamming radius should report a full checked word if SAT or a checker-accepted UNSAT certificate for a precisely stated radius. The present distance figures from other near words do not bound that radius.
2. **Use the complete CNFs for a decisive result.** A checked SAT model would give \(S(6)\ge537\). A complete independently verified UNSAT proof for either formula would give \(S(6)=536\) together with the published 536-word. In either case, preserve the exact CNF hash and validate the word or proof against the classical definition, including doubling.
3. **Treat heuristic trajectories as leads.** The four defects of `best4` are concentrated at positions at most 9, including two doublings. A repair search can use that exact starting word, but must allow changes elsewhere and cannot infer a local repair exists from the defect locations alone.
