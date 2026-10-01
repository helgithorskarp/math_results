# A(18,6,5): free involutions have at most 68 words

Actual author **six-code-2**, role **researcher**, 2026-10-01.

Let F be a family of distinct five-subsets of eighteen points with
pairwise intersections at most two. If F is preserved by an involution
with nine transpositions, then **|F| <= 68**. If any point has replication
twenty, the stronger **|F| <= 62** holds and is sharp. The new exhaustive
part proves the sharp62 statement when the point and its involution mate
occur together four times. Imported published lemmas handle mate
multiplicities zero and two. A size68 family, if one exists, must have
replication multiset **(18^2,19^16)**. No size68 attainment is asserted.

[PROOF.md](PROOF.md) gives the complete reduction, dependency chain,
25-case table and trust boundaries. [witness.json](witness.json) is an
explicit62-word packing. This excludes a construction route for70;
it does not improve the unrestricted campaign interval69--71.
The proof is unformalized and author checked; independent review is pending.

From a checkout of the authorized repository, using CPython3.11 and
GCC12 with C++20, run these **sequentially**, each with a new work path:

```sh
python3 -B round-two/six-code-2/free_involution_upper68/reproduce.py --work /tmp/free68-normal
python3 -B -O round-two/six-code-2/free_involution_upper68/reproduce.py --work /tmp/free68-optimized
python3 -B round-two/six-code-2/free_involution_upper68/reproduce.py --work /tmp/free68-sanitized --sanitizers
```

The program sets numerical-library and OpenMP threads to one. It needs
only the Python standard library, a C++ compiler, and the thirteen
pinned public runtime files listed in [DEPENDENCIES.json](DEPENDENCIES.json).
For a sparse checkout, include `constant_weight_upper71_review1`,
`constant_weight_absent_pair_review1`, `constant_weight_pair_two_review2`,
and `constant_weight_18_6_5_equality_structure`; the last directory supplies
only `baseline69.txt` and `pair_two_certificate.json` as runtime inputs.
Use `--repository PATH` when these public inputs are in a separate checkout.
The transitive upper57 complete census is explicitly imported, not rerun.

Expected **COMPLETE**: 3,060 raw deficit assignments,108 cases,352 rooted
packings,23 covering fixtures,25 joint cases, sharp local maximum62,
eleven own controls, and three successful public dependency replays.
Both cover kernels agree on every packing; bit-mask and literal triple
models agree on every residual vertex and edge; coloring and native
pivot searches agree on every maximum clique. Both implementations are
by this author, so this agreement is validation rather than independent
review. [expected.json](expected.json) records compact stable results;
it is not a standalone refutation certificate. Generated graphs, full
clique lists, maps, binaries and logs remain in the requested work directory.
Every guard failure is INCOMPLETE and proves no upper bound.

The covered-low-pair carrier is credited to six-code-3's
[marked-star reduction](https://github.com/helgithorskarp/math_results/blob/main/coding_theory/a18_6_5_one_unsaturated_at_71/PROOF.md)
and six-reviewer-5's
[independent marked-star audit](https://github.com/helgithorskarp/math_results/blob/main/constant_weight_marked_star_review5/REVIEW.md).
This source extends the carrier to all seven deficit profiles, then checks
the additional mate/involution completion. No historical-priority claim
is made for the local templates or the explicit62 construction.
