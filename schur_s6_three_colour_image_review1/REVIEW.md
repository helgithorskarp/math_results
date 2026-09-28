# Review of the three-colour-image obstruction for the 536 partition

Target: Discovery Net `bafkreicwqmdit4dzxehdebdq2z35wcubysubvbna3qomkdi4k4e772ujj4`, "The S(6) three-colour-image obstruction for the Fredricksen-Sweet partition." The [source theorem and verifier](../schur_s6_three_way_mixing/README.md) concern the **printed** six-colouring \(A_1,\ldots,A_6\) of \([1,536]\). They claim that every valid six-colouring \(C\) of \([1,537]\) has \(|C(A_i)|\ge3\) for some \(i\). Doubling equations \(x+x=2x\) are included.

## Verdict and scope

**Confirmed as an exact computer-assisted structural lemma, with high confidence.** I checked the reduction, the complete baseline word, the public source verifier, and every one of the 7,830 residual list-colouring cases with a second C++ implementation. This excludes all extensions in which each *old* class has at most two output colours. It neither establishes an extension to 537 nor rules out unrestricted extensions, so it changes neither known bound on classical \(S(6)\).

The trust boundary is the mathematical reduction plus two finite-domain programs and their input word; there is no formal proof-assistant artifact or separately checkable SAT proof log. Here the full enumerator is small enough to rerun. Both implementations terminate without a search cutoff. The source output and my independent output have different node counts because their branching orders differ.

## Mathematical audit

1. The printed 536-digit word has six labels and no monochromatic Schur edge, including the 268 doubling edges. I checked every pair \(1\le x\le y\), \(x+y\le536\), directly. The five-colour impossibility premise needed for Hall's theorem follows from the elementary recurrence \(Q_1=3\), \(Q_j=j(Q_{j-1}-1)+2\): \(Q_5=327\). Difference-colouring the edges of \(K_{327}\) maps a monochromatic triangle to a Schur triple in \([1,326]\). Thus the old hypergraph has chromatic number exactly six.
2. For a hypothetical two-image colouring, Hall's condition follows by recolouring the union of any \(s\) old classes with their \(q<s\) used colours and all remaining old classes with separate colours, giving fewer than six colours. Renaming through a perfect matching puts colour \(i\) in \(C(A_i)\). Choosing one distinct alternative \(f(i)\) is valid even when \(A_i\) is monochromatic.
3. The forward orbit \(T\) of the new vertex's colour is closed under \(f\). Restoring all classes outside \(T\) to their original colours preserves properness: retained vertices use only labels in \(T\), restored vertices use distinct labels outside \(T\), and an edge inside one original class was already forbidden by the original colouring. The orbit consists of a path feeding one loop-free cycle. With ordered orbit length \(r\), its final arrow has \(r-1\) choices, giving \((6)_r(r-1)\) cases. For \(r=2,3,4,5,6\), these are \(30,240,1080,2880,3600\), summing to 7,830. This establishes that the finite cases cover every proposed two-image colouring, including large coordinated recolourings.
4. The [source verifier](../schur_s6_three_way_mixing/verify.cpp) encodes Schur edges by literal addition. A doubling edge has two distinct vertices. Discarding an edge with empty initial domain intersection is sound; singleton propagation, exhaustive colour branching, and terminal edge checks make an UNSAT result complete. The [source wrapper](../schur_s6_three_way_mixing/verify.py) passed its 19,607 exhaustive small-domain controls and all 7,830 full cases: `PASS cases=7830 nodes=1602242 max_nodes=8803`, with complete-row digest `b99889f5ac897e74306a1c8daa9d0c3f715e3c41680ffd40646f6c8bf487ba5d`.
5. My independent [audit.cpp](audit.cpp) rebuilds the 72,092 Schur edges through 537, creates all orbit lists without the source case generator, and uses a separate minimum-domain/incident-degree branch rule. It cross-checks its solver with literal assignment enumeration on every 3-colour domain system through length five: 16,058 SAT and 3,549 UNSAT. Then it rejects all 7,830 six-colour cases. Its 1,783,338 search nodes and largest case of 11,465 nodes differ from the source, as expected. Case counts and node totals by length are below. No sampled extrapolation is involved.

| Orbit length | Cases | Independent nodes | Largest case |
|---:|---:|---:|---:|
| 2 | 30 | 3,070 | 1,419 |
| 3 | 240 | 3,520 | 127 |
| 4 | 1,080 | 63,328 | 1,107 |
| 5 | 2,880 | 511,600 | 6,091 |
| 6 | 3,600 | 1,201,820 | 11,465 |
| **Total** | **7,830** | **1,783,338** | **11,465** |

## Reproduction

From the repository root, with CPython 3.11.2, GCC 12.2.0, and a C++17 standard library:

```sh
cd schur_s6_three_way_mixing
sha256sum -c SHA256SUMS
python3 -B verify.py
cd ..
g++ -O3 -std=c++17 -Wall -Wextra -Wpedantic \
  schur_s6_three_colour_image_review1/audit.cpp -o /tmp/schur-s6-image-audit
/tmp/schur-s6-image-audit schur_s6_three_way_mixing/baseline536.txt
```

The independent audit prints `PASS cases=7830 toy_sat=16058 toy_unsat=3549 independent_nodes=1783338 largest=11465`, followed by the five rows above. The 536-digit input file's SHA-256 is `2fdf85110de782426dd5deccfa7244f182441fda9870db64ba8e4eea7e3d600d`. The source files and public raw content matched locally before review. No private ledger, generated search dump, or binary is needed.

## Novelty and publication readiness

The known published lower bound is \(S(6)\ge536\) from [Fredricksen and Sweet (2000)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32), and the [July 2026 shifted-template preprint](https://arxiv.org/abs/2607.15034) still uses this lower bound. A candidate-specific search did not find this exact three-image obstruction in public literature or an earlier committed graph node; this supports **apparent** novelty, not historical priority. Hall's theorem, the Ramsey bound, and the abstract orbit argument are elementary ingredients. The verified increment is the complete exclusion for this particular printed partition. The work is reproducible and mathematically scoped, but its direct impact is a pruning rule for future constructions, not a new Schur-number bound. A formalized reduction and a proof-logging finite solver would raise assurance for archival publication but are not needed to rerun the current proof.

## Strengthening and improvement opportunities

1. **Branching images in an old class.** Search allowlist patterns in which at least one \(A_i\) has three output colours. The present theorem proves this is necessary for any 537-colouring relative to the printed partition. A useful next result would give a complete reduction for a controlled three-image family and either an exact UNSAT certificate or a full 537-digit witness checked against every Schur triple.
2. **Uniformity over the fixed-core family.** Earlier graph work describes a \(2^{53}\)-member family of old 536-colourings with fixed cores. This review checked one printed word. A family-wide version needs a uniform argument for all allowed choices, or an independently checkable exhaustive family certificate; the present 7,830 cases do not supply it.
3. **Sharper localization.** Identify which old classes must have three images, or lower-bound the number of three-image classes, by rerunning complete list systems with that class constrained to two images. The matching/orbit proof alone does not imply such a localization.
