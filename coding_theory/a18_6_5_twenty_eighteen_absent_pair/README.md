# Sharp degree20/18 absent-pair maximum and a completion theorem

Agent: **six-code-3**, role: **researcher**, 2026-09-30.

For any18-point packing of five-subsets with intersections at most two,
an absent pair whose endpoint degrees are20 and18 forces at most **62**
words. The small [construction](witness62.json) attains62. The new geometric
step proves that an18-line packing of four-arcs of an order-four plane
completes uniquely to an orthogoval plane whenever its pair leave has
no collinear triangle. [PROOF.md](PROOF.md) gives the precise hypotheses,
complete covering argument, replacement proof and deletion bound.

Both the complete generator and the separately implemented checker
finish all34398 exclusion instances. They reconstruct the entire45100-orbit
domain, representing254704450 labeled twelve-edge leaves. There are10633
collinear-triangle branches and69 immediate unique-completion branches.
These counts concern leave representatives, not inequivalent global codes.

## Reproduce from the repository root

Requirements: Python3.11+ and a C++17 compiler supporting GCC-compatible
integer bit-count builtins. Used: CPython3.12.14 and g++12.2.0, standard
libraries only. Run the following commands sequentially. Working data and
binaries belong under local scratch, outside the source directory.

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1
p=coding_theory/a18_6_5_twenty_eighteen_absent_pair
mkdir -p scratch/a18_20_18
g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -pedantic "$p/bitset.cpp" -o scratch/a18_20_18/bitset
g++ -std=c++17 -O2 -Wall -Wextra -Wconversion -pedantic "$p/cover.cpp" -o scratch/a18_20_18/cover
python3 -B "$p/generate.py" --engine scratch/a18_20_18/bitset --work scratch/a18_20_18/primary
python3 -B "$p/verify.py" --primary scratch/a18_20_18/primary/summary.json --engine scratch/a18_20_18/cover --work scratch/a18_20_18/check
python3 -B "$p/audit.py" --bitset scratch/a18_20_18/bitset --cover scratch/a18_20_18/cover --domain scratch/a18_20_18/primary/domain.json
```

Expected: `COMPLETE finite exclusion`, then `COMPLETE separate-algorithm
check`, then `PASS`. The restricted maximum is62. The domain and exclusion
SHA256 values in [expected.json](expected.json) must match; the verifier
also checks the expected classification and fixture degrees. Native nodes
are153303954 for bitsets and113783648 for Dancing Links. Node order can
differ between the engines; the complete cover statements agree per case.

The generator enumerates all labelings of compact cubic/cycle catalogues
and explicit affine maps. The checker uses prescribed-degree neighborhood
recursion, set graphs and a generator closure for plane permutations.
Their complete domain byte strings agree. Each engine receives a separately
constructed exact-cover matrix. The checker imports no generator or prior
geometry module. The optional geometric audit compares both full native
cover lists with a Python integer reference on100 cases: all69 completable
leaves and31 selected exclusion leaves. These are bounded regression
checks, in addition to the complete two-engine exclusions.

## Dependencies and resources

This contribution requires sibling source
[a18_6_5_saturated_single_pair/geometry.py](../a18_6_5_saturated_single_pair/geometry.py)
for the generator's exact first-plane normalization. The written proof
imports the earlier
[saturated absent maximum56](../a18_6_5_saturated_absent_pair/PROOF.md) and
[degree20/19 single-pair upper57](../a18_6_5_twenty_nineteen_single_pair/PROOF.md).
Their statements are explicit dependencies; this run does not newly audit
those full proofs. The degree20/19 absent upper59 and Brouwer1975 degree
theorem are used only for the at-least63-word density corollary.

Full generation297.0902 seconds; independent reconstruction/replay173.0959
seconds. Parent/child high-water RSS upper bounds65560 and166016 KiB.
One CPU-intensive job ran at a time, one numerical thread, unchanged
1CPU/2GiB scope. Per leaf:200000 recursion nodes and ten seconds; either
guard aborts with `INCOMPLETE`. Fixed capacities120 pairs and840 candidate
quadruples are the mathematical input dimensions. Batches contain at most
1000 cases and permit resume with matching domain/binary/output hashes.

The audit examines490314 deficit compositions,1100 simple graphs through
five vertices,80 replacement interfaces,20 small hypergraphs by direct
subsets,26 malformed/raised-cap native rejections, two native and one
degree-enumeration incomplete-search rejections, and four corrupted
fixture rejections. Its geometric pilot includes both positive and empty
cover cases. The proof uses explicit checks, which survive Python `-O`.

For address/undefined-behavior sanitizer validation, compile each native
engine with `-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer`
and use these binaries in the same `audit.py --domain ...` command.
This bounded audit covers actual840-row geometric matrices as well as
small and malformed inputs. It is not a replacement for the full census.
Both sanitizer builds passed the complete100-case geometric audit in
24.6151 seconds, with zero diagnostics; all1927 positive cover lists
(395 cubic and1532 cone) agreed with the Python reference. All resulting
38-word unions passed direct checks of weights, intersections and degrees.

## Proof boundary and public data

The exact maximum and geometric completion statement are computer-assisted
results with written completeness bridges, not formalizations. Separate
same-researcher algorithms are not independent peer review. Every bound
uses a completed exact enumeration or a stated mathematical argument.
No timeout, incomplete branch, floating-point search or resource failure
supplies nonexistence evidence. The general69--72 gap remains open.

Ten compact source/documentation/fixture files suffice. The generated
domains, native matrices and outputs, resumable progress, and exploratory
residual-color lists are omitted local operational data. The compact
expected record is replay metadata, not a standalone UNSAT certificate.
Historical affine geometry, Algorithm X, code bound69 and orthogoval
constructions are attributed in the proof; no historical-priority claim
is made for the new restricted theorem.
