# Exact greedy completion cost for boxed 2143

This source proves exact tools for a completion approach and rules out one proposed potential method. The agreed growth problem remains **unsolved**: if `a_n` counts permutations of `[n]` avoiding the boxed pattern 2143, decide whether a finite constant `C` satisfies `a_n <= C^n` for every `n >= 1`, or `limsup a_n^(1/n) = infinity`.

A boxed occurrence consists of positions `i1 < i2 < i3 < i4` with `p[i2] < p[i1] < p[i4] < p[i3]` and no unselected point strictly inside the horizontal and vertical rectangle of those four points. Arbitrary subsequence deletion need not preserve avoidance. The maximum-insertion process here preserves the original input as a subsequence of an avoiding output.

Quinn (`literature-researcher-3`) authored the lemmas and controls. Theo (`literature-researcher-4`) accepted the entire submitted partial scope after a separate proof check and independent computation, recorded as review682 and actually read and acknowledged by the author692. This is an internal team check, not external peer review. Historical files retain their exact bytes, including their earlier pending headers and explicitly corrected descriptions.

## Checked statements and the missing estimate

The greedy algorithm processes source ranks increasingly. Its desired gap is immediately before the first processed original to the right of the new source rank, or the final gap. If this gap is illegal, it inserts an auxiliary global maximum at the rightmost earlier legal gap and repeats. The accepted termination and source-preservation proof gives an avoiding completion for every input; its general bound `2^m - 1` is too large for the growth argument.

In the maximum Cartesian tree, write the desired external-leaf path using `L` and `R`. A gap is legal precisely when its path contains no adjacent `RR` after an earlier `L`. The new checked cost theorem says that the number of auxiliaries used to repair that gap is exactly the number `D` of such pairs in its initial path. Each repair removes exactly one pair. The proof applies to every finite tree shape; finite controls use one classical avoiding representative per shape rather than enumerate every heap labeling.

Each counted pair identifies one eligible current minimum whose nearest-greater-right blocker interval covers that gap. This is a bijection, and `D` is also the number of boxed occurrences a hypothetical unrepaired new maximum would create. That hypothetical illegal child is used only for checking the identity.

For the deterministic tagged completion `C(sigma)` of `sigma` in `S_n`, let `B(C(sigma))` be the sum of the blocker intervals' **original-gap** masses, including eligible original and auxiliary minimum nodes. A gap has mass one immediately before an original point and at the final gap, and mass zero immediately before an auxiliary. Conditional on the actual source history the next original gap is uniform among its `n+1` choices, not among all current gaps. Therefore the exact finite identity is

```
E[total auxiliaries on uniform S_m]
    = sum_(0 <= n < m) E_(sigma uniform S_n)[B(C(sigma))] / (n+1).
```

The required bound on this sum is `o(m log m)` and remains **unproved**. That bound would give a fixed positive fraction of inputs with avoiding completions of length `o(m log m)` by Markov's inequality. The separately checked subsequence-fiber count then proves the negative growth answer, since an output of length `N` has at most `binomial(N,m)` standardized `m`-point subsequences. No ordinary growth limit is assumed.

The raw potential `Phi` counting every adjacent `RR` over original-gap paths, even before the first `L`, fails a proposed uniform conditional drift bound. The reachable all-original parents `(1,...,n-q-1,n,n-1,...,n-q)` have no next repair, but their exact drift is `(q+1)*(n-q*(q+5)/6)/(n+1)`. At `n=q^3`, this is at least `(q+1)/3`. Thus neither a constant nor `o(log n)` bounds this same potential's drift over every source history. These parents each have probability `1/n!`; the obstruction does not refute the unconditional expected-cost estimate or other potentials.

Read [the exact-cost proof](author_packet/GREEDY_REPAIR_PATH_COST_V2.md), [the drift obstruction](author_packet/RAW_RR_POTENTIAL_OBSTRUCTION_V1.md), [the termination and conditional entropy bridge](author_packet/GAP_OPENING_AND_FIBER_BRIDGE_V1.md), and [the entire internal review](internal_review/QUINN_REPAIR_PATH_COST_REVIEW_V2.md). The [oracle-scope correction](author_packet/VERIFICATION_SCOPE_CORRECTION_V1.md) distinguishes the preserved optimized-oracle probe from the separately added full literal controls.

## Reproduction

Python 3.11.2 and its standard library were used; no solver, floating arithmetic or proof assistant is involved. From this directory, use a fresh output path:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B internal_review/check_quinn_repair_path_cost_v3.py --packet author_packet --output-directory /tmp/boxed2143-cost-fresh
```

This unchanged independent checker imports no author or teammate executable. It verifies every pinned author file, regenerates Cartesian shapes by Dyck words, uses a pointer-stack tree construction and direct greater-position searches, and enumerates complete strict-rectangle occurrence sets with a prefix table. It compares every deterministic field in four author reports and their stored stdout. Resource samples are documentary observations and are excluded from equalities with a fresh run.

The completed domain is all626 shapes of sizes0 through7 and all4707 gaps, all4707 hypothetical maximum children and1380 actual auxiliary children. Additional controls reproduce the stopped12-source raw-potential scan and the five directed family pairs `(2,1),(4,1),(8,2),(27,3),(64,4)`. The latter checks all110 next children and105 rank arrivals; only the45 children at sizes2/4/8/27 receive literal scans. Size64 has shape and direct-neighbor controls. Finally, all874 source histories of sizes0 through6 validate the tagged expectation identity; mean auxiliary counts at sizes4/5/6 are `1/24`, `2/15`, `97/360`. These finite values supply no all-size estimate.

Expected canonical SHA256 streams:

| Domain | SHA256 |
| --- | --- |
| Shape/path/cost | `07841e7f30461c63aa40349d4ef55c03b4e6acd6a6099c32606c891c8bc82982` |
| Full literal supplement | `3fb17c7423b137fb55799285cf40ca0522c6b688bdc6329f631168c22b54a25b` |
| Stopped raw-potential scan | `cd16d68006f05ca75cd820228840bdc089f75f4da9522df21f06b212cce30fb5` |
| Directed drift families | `bc5ec17f6c2d67534059ed42c24641ffdec53b0adb2f275c27ac708884ba4a87` |

The omitted3168981-byte full generated certificate is recreated by this command with SHA256 `265c758b1fcf701615491d22f875be972365de7b576f9e5074f9860697113040`. It contains all specified path records, rewrites, raw-scan and family records, and tagged population histories. The compact original [completed report](internal_review/quinn_repair_path_cost_reproduction_v3/quinn_repair_path_cost_reproduction_v2.json) and source are published here; the bulk certificate and operational review closure remain outside Git. The recorded independent run took1.342780462 seconds, including certificate creation;40516KiB was sampled before final report serialization, not as a claim about the later whole-process peak.

There were two checker attempts and one completed independent reproduction. The first added an invalid stronger assertion that legal insertion makes every future child gap legal. Its source, failure record and small stderr are retained. Version3 removes only that assertion. The author did not claim it. Original failed attempts and corrected oracle descriptions are preserved; they are not counted as successful reproductions.

## Literature and provenance

The target was selected from primary external literature before graph consultation. Kitaev, Qiu and Xu, [*Coincidences and Growth of Boxed Mesh Patterns*, September2026](https://arxiv.org/html/2609.13764v1), Section7 and Theorem4.4, leave the2143/3412 growth cases open in the examined version. The boxed-pattern source is [*Avoidance of boxed mesh patterns on permutations*, Discrete Applied Mathematics161(2013),43–51](https://doi.org/10.1016/j.dam.2012.08.015). This package makes no global novelty or priority claim and does not solve that published problem.

The47-file author packet and published checker retain their exact review682 hashes. [The public file manifest](PUBLIC_FILE_MANIFEST.json) pins this compact publication; [provenance](PUBLICATION_PROVENANCE.json) records scope, acceptance, omissions and the original full durable review-manifest hash. Pending normalized-potential, literature-inclusion and tagged-energy claims are excluded. Earlier checked gap and tree prerequisites have public source at [commit057746e13d1056047ddf0b7b59968e9a70f081ff](https://github.com/helgithorskarp/math_results/tree/057746e13d1056047ddf0b7b59968e9a70f081ff/boxed2143_insertion_obstructions_20261005), [commit39045c3ecd2156cfca6cd510c3647bf278b65cf1](https://github.com/helgithorskarp/math_results/tree/39045c3ecd2156cfca6cd510c3647bf278b65cf1/boxed2143_tree_join_dynamics_20261005), and [commit8d09e8249e536c3467717d28a551b6b3896d942a](https://github.com/helgithorskarp/math_results/tree/8d09e8249e536c3467717d28a551b6b3896d942a/boxed2143_completion_and_reciprocal_obstructions_20261005).
