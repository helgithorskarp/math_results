# Independent review of the current-q8 degree-carrier reduction

Verdict: **ACCEPT**, with the dependency and scope qualifications below.
The h4029 arithmetic and transfer theorem are correct: after requiring every
red degree to lie in 18 through 24, strictly less than `681/12500` of the
complete current h3887 q8 carrier remains.  Each of the four q8 macro classes
has retained fraction strictly below `1/16`, the aggregate reduction is
strictly greater than a factor of 18, and the retained integer upper bound is
below `2^748`.

Reviewed Discovery Net contribution:
`bafkreihafon4rkn6ivkw5swkhizawbvwazzd4cqrpajsegfha44cu4h23y`, source
commit `75504bf00d16c425d72ae55c3293be7c8c6661ab`.  The target
`EXPECTED.json` SHA-256 is
`b652d2e5fb5a30fbfd7e3236e50aa7f9c9bff22188d1bf8967cc4d2138d7416c`.

This theorem removes labelled carrier assignments, not whole tasks.  It
declares no q8 task UNSAT, does not inspect the q7-r5 or q10 survivors, finds
no 43-vertex Ramsey graph, and does not prove `R(5,5) >= 44`.

## Mathematical audit

The degree premise is correct.  If a vertex has at least 25 red neighbours,
`R(4,5)=25` supplies either a red four-clique, which the vertex extends to a
red five-clique, or a blue five-clique.  Applying the colour-swapped argument
when the red degree is at most 17 gives the necessary interval 18 through 24.
This imports the established value `R(4,5)=25`; it is not reproved here.

For each fixed h3873 parent task, the 800 unfixed physical pairs are grouped
into 116 independent finite coordinates: 28 block-pair matrices and 88
block/core stars.  The eight chosen two-vertex block events and eleven
core-vertex events form an exact read-two cover.  A matrix coordinate occurs
in its two endpoint-block events, and a star occurs in one block event and one
core event.

Let `A` be the intersection of these 19 events in the product space `Omega`
and let `Z` be uniform on `A`.  Shearer's entropy inequality gives

```text
2 H(Z) <= sum_j H(Z restricted to event j).
```

The projection for event `j` is supported on at most
`Pr(E_j) * |Omega_j|` local assignments.  Since every coordinate-domain
factor occurs exactly twice, exponentiation gives

```text
(|A|/|Omega|)^2 <= product_j Pr(E_j).
```

No independence among the events is assumed.  Every degree-valid graph lies
in `A`.  For a core vertex the target takes the maximum marginal over all
eleven possible fixed internal degrees, so this bound is uniform over all
546,356 residual cores and does not assume their internal degrees are
independent.

The transfer to the h3887 sorted carrier is also valid.  Write `D` for the
number of ordered root-matrix sequences, `M` for the number of nonincreasing
root multisets, `J` for the distinct-root multisets, `L=(r-1)!(8-r)!`, and
`Q` for the remaining coordinate count.  The selected position pair is the
same in all nonroot blocks of a given colour, so the event is invariant under
the whole-block permutations used for sorting.  Every distinct-root sorted
graph has exactly `L` parent labellings.  Charging every repeated-root sorted
graph as a survivor therefore gives the sound bound

```text
v_r = u_r D/(L M) + (M-J)/M,
```

where `u_r` is the upward-rounded parent probability bound.  This avoids the
invalid shortcut of simply dividing all parent survivors by `L`.  A direct
microcase in the review checker exhibits that shortcut's failure.

## Independent exact reconstruction

[`independent_check.py`](independent_check.py) imports no target module.  It
provides a third computational path in addition to the target's dictionary
convolution and packed-integer checker:

- Pure Python tests every five-subset in each literal eight-vertex graph and
  examines all 393,216 matrix words.  It independently obtains domain sizes
  37,823, 35,714, 35,714, 1,931, 37,823, and 1,998.
- Dense two-dimensional polynomial arrays regenerate all 192 bivariate
  degree marginals.  A separate one-dimensional recurrence handles core
  degrees.
- Exact `Fraction` arithmetic regenerates the least `2^-40` grid upper bound
  on each square root, all multiset/distinct-root counts, every sorted
  fraction, and the complete 70,179-byte target certificate exactly.
- The checker reads h3887's public `TASKS.json` directly at SHA-256
  `657e2585f5fce56abc4bb7806bd093d1978c39ea791b9d02695ed19e22ef1f4c`.
  All four q8 rows, task intervals, per-task counts, and the total 2,185,424
  tasks match the h4029 pins.

The exact aggregate retained-fraction upper bound reconstructed by the review
is approximately `0.05447956363815276`, strictly below `0.05448`.  The exact
rational and retained integer ceiling are pinned in [`EXPECTED.json`](EXPECTED.json).
Four altered certificates—changing a marginal, the square-root rounding, a
macro class, or a sorted bound—are rejected.  Normal and assertion-disabled
Python produce the same pinned receipt.

The target's own complete sanitizer replay was also run in a fresh reviewer
scratch directory.  It regenerated the certificate in both Python modes,
matched ordinary and UBSan/bounds C++ domain output byte-for-byte, passed its
4,096 small read-two checks and 512 sorting controls, and rejected all four
numeric corruptions.  The run used CPython 3.11.2 and g++ 12.2.0 and invoked
no SAT solver.

## Reproduction

From the repository root, using Python 3.11 or later and the standard library:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  ramsey_r55_q8_degree_carrier_review1/independent_check.py \
  --check-expected
PYTHONDONTWRITEBYTECODE=1 python3 -O \
  ramsey_r55_q8_degree_carrier_review1/independent_check.py \
  --check-expected
cd ramsey_r55_q8_degree_carrier_review1
sha256sum -c SHA256SUMS
```

To rerun the target package as well, choose a fresh output directory:

```bash
python3 -B ramsey_r55_q8_degree_carrier/reproduce.py \
  /scratch/r55-q8-degree-replay --sanitizers
```

Expected terminal status:
`REPRODUCED_CURRENT_Q8_CARRIER_REDUCTION`.

## Literature, novelty, and readiness

The two mathematical inputs are established.  McKay and Radziszowski proved
[`R(4,5)=25`](https://doi.org/10.1002/jgt.3190190304) in 1995; a later
[`HOL4 formal proof`](https://arxiv.org/abs/2404.01761) further reduces the
trust boundary for that imported theorem.  The read-two inequality is a
special case of Shearer's lemma; Gavinsky, Lovett, Saks, and Srinivasan give
the relevant read-k entropy framework in
[`A Tail Bound for Read-k Families of Functions`](https://arxiv.org/abs/1205.1478),
especially Corollary 2.8.

No novelty is claimed for the degree interval, entropy inequality, multiset
counting, or sorting principle.  The apparently new object is the exact
quantitative application to this campaign's h3887 q8 carrier.  The package is
reproducible and suitable as an internal load-bearing reduction, but it is not
a standalone Ramsey-bound result and would need integration yielding actual
task decisions to have comparable publication impact.

## Trust boundaries and uncertainty

The review independently verifies the local domains, all marginals, exact
rounding, carrier arithmetic, source-registry transcription, read-two cover,
and sorting transfer.  It imports `R(4,5)=25`, the h3873 maximal-packing
coverage, h3887's interpretation as a complete sorted carrier, and the
546,356-core catalog completeness.  The relevant h3887 sorting/count argument
was rederived, but the entire upstream CNF implementation and catalog were not
replayed in this milestone.  The computation trusts Python arbitrary-precision
integer and rational semantics, hashing, the small checker, compiler,
interpreter, OS, hardware, and the identified commits.  Nothing here is
proof-assistant formalized.

## Strengthening and improvement opportunities

The most direct improvement is to replace each two-selected-vertex block
event by the event that all four block vertices satisfy the degree window.
The same 19-event read-two cover and sorting invariance remain valid, so only
the marginal computation changes.  A sparse four-dimensional recurrence or
meet-in-the-middle coefficient table would give a rigorously stronger bound
without touching the imported carrier coverage.

Second, the current transfer charges every repeated-root configuration as a
survivor.  Stratifying by root-word multiplicity partitions and computing
conditional marginals for those strata would replace this worst-case charge
by the correct orbit-size-weighted contribution.  This requires conditioning
the root-matrix distributions; applying the unconditional parent factor to a
tie stratum would not be valid.

Finally, h4009's edge window and h4015's neighbourhood restriction should be
integrated only through a joint or conditional count.  Multiplying their
unconditional reduction factors by the present one would be unjustified.
The high-impact endpoint is a filter whose certificate closes complete q8
tasks, not merely a smaller superset of their possible assignments.
