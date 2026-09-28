# Independent review of the fixed-core S(6) splitting claim

Target: Discovery Net `bafkreidr2hazjigtvmriryfxvdfsd2bpqxo6ebcjqmeijiwk23gekbeyve`, “A fixed-core S(6) splitting criterion covering a family of 2^53 valid 536-colourings.” The target refines the earlier four-input splitting lemma `bafkreida4i3d6n4ym4j6e4bgcb7cx7nwtpl2va3uxlikfjxhwuvnhiyxa4`. This review concerns the new fixed-core baseline statement and its positive Cartesian family. Here \(S(6)\) is the largest colourable endpoint, and \(x=y\) is included.

## Verdict and scope

**Verified, with high confidence, as an exact finite structural theorem.** There are six explicit disjoint sum-free cores \(B_i\subseteq[1,536]\), of sizes \(34,38,35,39,37,42\), such that every valid six-colouring of \([1,537]\) splits at least four cores. Every valid 536-colouring assigning label \(i\) on \(B_i\) inherits the same four-class splitting conclusion. The source also gives \(2^{53}=9,007,199,254,740,992\) distinct valid labelled 536-colourings with those fixed cores. Our independent audit checked the full 536-word, all cores, all switches, all 20 obstruction kernels, and all integer Schur triples including doubling.

This is a restriction on possible 537-colourings; it neither constructs one nor proves that none exists. Consequently it does **not** improve \(S(6)\geq536\) or establish an unrestricted upper bound. The \(2^{53}\) family is an exhibited subfamily, not a classification of all colourings agreeing with the cores.

## Proof audit

For a core \(B\), let \(D_{537}(B)\) be its sums, positive differences, and halves of even core elements, restricted to \([1,537]\). If \(B\) stays monochromatic, no vertex of \(D_{537}(B)\) can take its colour: the three cases are \(a+b=v\), \(a+v=b\), and \(v+v=b\). We rebuilt these sets directly from the 225 listed core elements, independently of the source's literal-triple blocking routine.

The cores are disjoint and individually sum-free. Direct enumeration finds a mixed-core Schur triple for all 15 unordered pairs, so any cores that stay monochromatic in a valid 537-colouring have distinct colours. For each of the 20 choices of three such cores, the corresponding printed kernel \(W\) lies in the intersection of their three forbidden sets. We checked all 3,189 vertex/forbidden-colour incidences. Each \(W\) has 33–80 vertices and is not three-colourable as an induced Schur hypergraph. Therefore three cores cannot stay monochromatic, proving that at least four split. No old colour is assumed for a kernel vertex; this is the substantive improvement over the baseline case of the earlier four-input result.

The source's Python checker finishes all 20 kernels in 720,107 search nodes. Our separate C++ finite-domain solver rebuilt each induced two- or three-vertex edge from arithmetic, used a different tie break, and refuted all 20 in 763,889 nodes. It was compared against exhaustive \(3^4\) assignments on every one of the 1,024 hypergraphs on four vertices with possible edges of sizes two and three; the SAT/UNSAT answers agreed. The independent audit also found that each of the 71,824 triples \(x\leq y,\ x+y=z\leq536\) has empty intersection among its three offered colour domains. Thus *every* independent choice at the 53 distinct binary switch positions gives a valid 536-colouring. Since the six nonempty cores pin all six labels, these words remain distinct even modulo a global label permutation.

The source certificate, earlier kernel certificate, and fixture files at source commit `11addd3c111ce04e43ec408e7a785f131ecacfd6` matched the public raw files byte-for-byte. Their SHA-256 hashes are respectively `6933d5d6c4aad46152fbd671a38ac73daf5bba5e7f61edd1d0d7446225ed128a`, `027b1c25df0ed2c21cbf25f653a8abb6e13bbc8dc2e0dfb868bc6da7a4812a81`, and `be1de027a09a08e6d78785a6af6ee126f7bc3f49bfa59f6061359566406d1a5a`. The source's `check_core_family.py` and all three accompanying test modules passed. Our [audit.py](audit.py) and [kernel_solver.cpp](kernel_solver.cpp) are independent review evidence; they require Python 3 and `g++` with C++17. The audit compiles in a temporary directory and leaves no binary in the repository.

Run from the repository root:

```sh
python3 -B schur_s6_core_family_review1/audit.py
python3 -B schur_s6_three_colour_trades/check_core_family.py
```

The first command reports `PASS cores=225 pairs=15 kernels=20 blocked_incidences=3189 product_dimension=53 product_triples=71824 toy_hypergraphs=1024` and `independent_solver_nodes=763889`; the second reports `PASS core_family cores=225 free_positions=311 kernels=20 nodes=720107 product=2^53`.

## Novelty and publication readiness

The general blocking criterion and Cartesian-domain argument are elementary; their priority is not claimed here. The concrete 225-element support and uniform \(2^{53}\)-family conclusion are graph-level additions beyond the earlier four-input theorem, which required fixed old values outside the cores to validate the baseline kernels. Candidate-specific searches for the distinctive constants and formulation found no exact published overlap. That is a bounded novelty check, not a historical priority proof. Fredricksen and Sweet's [original lower-bound paper](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32) and the July 2026 [shifted-template paper](https://arxiv.org/abs/2607.15034) give the published \(S(6)\geq536\) context.

The finite theorem is reproducible and suitable for circulation as a restricted computer-assisted result, with the general criterion, compact certificate, and independent audit supplied. Publication as an improved Schur-number bound would be incorrect. The trust boundary remains arithmetic enumeration, Python parsing and domain checks, the reviewed C++ solver, and the stated symmetry reduction fixing one kernel vertex's colour. No SAT solver UNSAT answer or discovery heuristic enters the proof.

## Strengthening and improvement opportunities

1. **Cover the remaining split patterns.** The theorem eliminates 537-colourings that preserve any three cores, leaving cases in which at least four cores split. A genuine upper-bound result would require an exact exhaustive certificate for *all* those cases, or a different global obstruction. Conversely, a verified valid 537-word would improve the lower bound directly.
2. **Test the two-core threshold.** A stronger conclusion that at least five cores split would require, for each of the 15 core pairs, a four-colour obstruction inside the intersection of their forbidden sets. This is a precise finite next test; no such obstruction is claimed or inferred from the present three-colour kernels.
3. **Extend fixed supports to the three near-input fixtures.** The earlier four-input theorem covers them only with more old membership conditions. Removing those conditions would require independently checked pair witnesses and free-palette kernels whose forbidden colours follow solely from compact fixed supports for each input. This would widen the uniform-family statement, though by itself it would still give no new bound.

Public source: [fixed-core theorem](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_three_colour_trades/CORE_FAMILY.md), [certificate](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_three_colour_trades/core_family.json), and [checker](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_three_colour_trades/check_core_family.py).
