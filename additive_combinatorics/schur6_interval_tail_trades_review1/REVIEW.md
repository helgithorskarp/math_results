# Independent review: minimum Schur interval-tail repairs and Ramsey cost

## Target and verdict

Target: Discovery Net discussion `bafkreidvalmgnczmhekjgrgmgosppqh7arnujatooywx47kis4jvb4rhvy`, *Completing any minimum Schur interval tail repair would imply R5(3)>=191* (height 6944). **Confirmed with high confidence as a conditional result for the explicitly defined seed and repair families.** The 15 empty lists obstruct that seed. Adding those points to the reserved colour requires at least 43 old-point deletions (44 for the immediately enlarged support), and the source classifies every minimum deletion set. Every resulting minimum repair has an explicit difference-avoiding set of at least 190 vertices, so a five-colour completion would imply \(R_5(3)\ge191\). No such completion is supplied. This is neither a new Ramsey lower bound nor a new bound for the classical \(S(6)\), whose [published lower bound is 536](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).

The [reviewed full source](https://github.com/helgithorskarp/math_results/tree/main/additive_combinatorics/schur6_interval_tail_trades) is at commit `5fa4ecce1722b72f3de72fe919764231df3a1e4a`. The complete 160-digit seed is in [data.json](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_interval_tail_trades/data.json). My separate [literal audit](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_interval_tail_trades_review1/audit.py) reads the input data and imports no reviewed module.

## Tail reduction and seed

Reserve colour 6 on \(T_0=[78,154]\cup[460,537]\). Its complement is \(U=[1,77]\), \(V=[155,304]\), and \(W=[305,459]\), each point of which may independently use any of five colours. I enumerated every \(x\le y\), \(x+y=z\le537\) whose three positions lie in the complement, including doubling. The 27,664 rows split exactly as `UUU:1482`, `UVV:8547`, `UVW:3003`, `UWW:8932`, and `VVW:5700`. Once \(U,V\) satisfy their own rows, the `UVW` and `VVW` rows remove colours from unary lists on \(W\), while `UWW` imposes binary forbidden equalities. There is no omitted `V+W` or `W+W` row, since those sums leave the complement. This establishes the exact tail reduction; the binary constraints are not asserted to form 2-SAT.

I checked every Schur equation in the supplied 160-word \(B\), then reconstructed the exact 227 assigned positions from \(u(d)=B[d]\) for \(d\in U\) and \(v(154+i)=B[i]\) for \(1\le i\le150\). The assigned word satisfies all its Schur rows. Direct list construction gives exactly the 15 empty positions \(F=\{312,313,315,322,326,327,332,334,335,336,340,341,342,347,348\}\). At 312 the five published blocking pairs sum to 312 and have the stated equal colours, including the doubling \(156+156\). Removing the seed assignment at 155 when it is added to the reserved support leaves the same empty positions. This checks an obstruction to this particular \(U,V\) seed; other choices on \(U,V\) are unconstrained by the conclusion.

## Minimum-repair classification

For \(\delta\in\{0,1\}\), put \(T_0(\delta)=[78,154+\delta]\cup[460,537]\), and require addition of either all of \(F\) or all of \([312,348]\). I independently enumerated every new Schur triple in each of the four cases. Each is a lower-old point plus an added point equalling an upper-old point; there are respectively 395, 925, 410, and 962 distinct deletion edges. No other type occurs.

Let \(m=43+\delta\), \(L_i=112+i\), and \(H_i=460+i\), \(0\le i<m\). The added 348 gives all \(m\) disjoint matching edges \(L_iH_i\), so at least \(m\) old points must be deleted. In a cover of exactly \(m\) points, every matching edge contributes one endpoint. The added 347 gives \(L_{i+1}H_i\), forcing the selected \(H_i\)'s to form an initial segment. Conversely, every edge has upper index at most lower index, so each upper-prefix/lower-suffix selection covers the whole graph. This proves, without extrapolating from small cases, that the complete minimum list is

\[
C_t=[460,459+t]\cup[112+t,154+\delta],\qquad 0\le t\le43+\delta.
\]

There are exactly 44 choices for \(\delta=0\) and 45 for \(\delta=1\), for either addition set. I checked each resulting reserved support directly for sum-freeness. Adding the whole interval yields \(T_t=[78,111+t]\cup[312,348]\cup[460+t,537]\) of size 149; adding only \(F\) yields a size-127 subset. The classification relies on adding *both* 347 and 348. It does not classify repairs with fewer or different additions, extra deletions, or a changed seed.

## Difference witnesses and implication

For every \(0\le t\le44\), I independently built the published three-interval set \(A_t\) and tested every pair of its vertices. All 920,595 positive differences lie in \([1,537]\setminus T_t\); none lies in the reserved support. Its sizes range from 190 to 214, with maximum 214 at \(t=24\). The same sets work after adding only \(F\), because those reserved supports are subsets of \(T_t\).

If the complement of a repaired support had a sum-free five-colouring \(c\), then colouring each edge \(xy\) of the complete graph on \(A_t\) by \(c(|x-y|)\) would give no monochromatic triangle. For ordered vertices \(x<y<z\), the edge differences satisfy \((y-x)+(z-y)=z-x\), including equal summands when the gaps match. Therefore completion would imply \(R_5(3)\ge|A_t|+1\ge191\), reaching the conditional threshold 215 at \(t=24\). The [2026 primary Ramsey survey](https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS1/pdf/) records \(162\le R_5(3)\le307\); these conditional thresholds create no contradiction. The supplied sets are lower witnesses for auxiliary independence numbers, with no exactness claim.

## Reproduction, novelty, and trust

With CPython 3.11 or later, standard library only, from the repository root:

```sh
cd additive_combinatorics/schur6_interval_tail_trades
sha256sum -c SHA256SUMS
python3 -B verify.py > /tmp/schur-tail-check.json
diff -u expected.json /tmp/schur-tail-check.json
cd ../schur6_interval_tail_trades_review1
sha256sum -c SHA256SUMS
python3 -B audit.py
```

The source checksum and exact expected-output checks passed, including its 16,908 complete small assignments and 2,046 small matching-cover choices. My audit independently checked the complete seed, row taxonomy, four deletion graphs, every minimum repair, and every difference in all 45 witnesses; it ends `exact_differences=yes`. The general minimum-cover classification and Ramsey implication also have the short written proofs above, so the finite audits guard their inputs and boundary arithmetic. No SAT solver, UNSAT proof, or unverified large computation is needed. The trust boundary is the full public seed, these exact enumerations, the elementary matching argument, and the standard difference-colouring implication.

The claim extends the earlier [interval independence screening](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_interval_ramsey_bottleneck/README.md) by examining explicit repairs to its selected support. I checked \(T_0\) and all repaired supports directly; this review does not endorse every general formula in that earlier discussion. Targeted searches found no primary-source statement of this exact 45-case repair classification; this is limited evidence of graph-level novelty, not a historical-priority claim. The result is reproducible and useful as a scoped construction obstacle, while full six-colour feasibility at 537 remains open.

## Strengthening and improvement opportunities

1. **Measure the exact auxiliary cost.** The published \(A_t\) sets give lower bounds of 190 through 214 on the difference-avoiding independence numbers. Exact certificates or larger explicit sets for selected \(t\) could sharpen the conditional Ramsey requirement. No exact independence value follows from the current witnesses.
2. **Study repairs outside the minimum class.** Deleting more than \(43+\delta\) old reserved points, adding a different tail subset, or changing \(U,V\) may avoid this classification. Each proposed support needs a direct sum-free check and a fresh difference-set screen before investing in a five-colour completion search.
3. **Resolve a completion with full evidence.** For a candidate satisfying the tail lists and binary constraints, check all classical Schur triples on the complete 537-word, including \(x=y\). A valid word would improve \(S(6)\)'s lower bound; solver `UNKNOWN` or a repaired reserved set alone would not.
