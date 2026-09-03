# Independent audit of the Dean k=5 proof claim, version 1.0.1

## Verdict

I independently audited Elias Botsford, *Cycles of length divisible by five
in graphs of minimum degree five*, version 1.0.1
(<https://doi.org/10.5281/zenodo.22182448>), including its computational
supplement (<https://doi.org/10.5281/zenodo.22167084>).

**The main theorem argument is valid with high confidence after one local,
necessary statement repair.** Every finite simple graph of minimum degree at
least five therefore has a cycle whose length is divisible by five, assuming
the cited published rooted-path and tetragonal-core theorems. I found no fatal
gap in the reductions from arbitrary graphs to the nine finite propositions,
and a fresh run of all 47 prescribed verifier commands passed.

Version 1.0.1 is not literally error-free. Lemma 7.2, the “Literal end-block
arm” lemma, permits a nontrivial end-block, while the paper defines a bridge as
a block. The bridge `uz` has no `u`--`z` path after the lemma orders `uz`
deleted, even though part (a)'s nonroot degree premise is vacuous. Its proof
also invokes Li--Zhan under the section's standing triangle-free assumption,
which should be present in the lemma's local hypotheses if the statement is
read independently.

The exact repair is to require a non-bridge end-block and, for part (a), that
`B-u` is triangle-free (the standing Type-I hypothesis gives the latter).
Every downstream invocation already satisfies both conditions: bridge open
endpoints are separately excluded by component-degree lower bounds, and all
four uses occur in the triangle-free Type-I section. Thus the false literal
statement does not infect the theorem proof. A compact bridge witness is in
the sibling contribution `dean5_literal_endblock_arm_statement`.

## Scope of the mathematical audit

I reconstructed the entire dependency chain rather than inferring the theorem
from successful certificate replay.

- The arbitrary-graph reduction correctly extracts a 2-connected zero-free
  graph with second-smallest degree at least five and classifies it as Type I
  or as one subdivided edge of a 3-connected minimum-degree-five graph. The
  edge-deleted rooted shores, singleton-side classification, and smoothing
  lift are sound.
- The bipartite branch correctly uses lexicographically maximal tetragonal
  cores. The parameter-two and parameter-three closures are sound. For
  parameter four, the component normal forms preserve actual attachment
  edges, and the relaxed full-attachment census is genuinely one-way: it lets
  phases vary independently but keeps the full covered core set. Pair
  rejection uses paths from different exterior components and two
  vertex-disjoint core links, so every rejected row expands to a simple cycle.
- The triangle branch's trigonal-core contractions and the `K4-e`/`K4`
  reservoirs use only actual lifted edges and exhaust the maximum core orders.
- In the triangle-free Type-I branch, shortest-odd-cycle contacts, end-block
  arms, safe deletion, four-connectivity, cubic normalization, and the final
  exterior cash-out all satisfy the relevant degree and simplicity premises.
  The repaired form of Lemma 7.2 is all that is used.
- For Type II with nonbipartite deletion graph, the selected-root theorem and
  shortest-cycle contact law reduce disconnected exteriors to the `1+2` and
  `2+2` finite states. Replacing unmarked positive cycle gaps by least positive
  representatives preserves equality, cyclic order, residues, and incidence;
  the subsequent coverage argument is mathematical and does not silently
  assume that the finite programs checked it.
- In the connected Type-II branch, the two-low localization, exceptional-leaf
  repair, two-separation closure, and phase-one/three/four eliminations are
  sound. The v1.0.1 ordered boundary-deletion ladder treats separately a
  witness on the shortest odd cycle and one in its exterior; the support
  classification supplies the required zero-residue root subarc in both cases.
- In the saturated phase, the actual exterior is 2-connected, the contact
  alphabet is exact, and the Watkins--Mesner decomposition yields actual
  three-terminal carrier paths. The two-cap topology covers arbitrary cap
  intersections and carrier re-entry. Four distinct private landings have the
  three orders disjoint, nested, and alternating; shared landings and positive
  common tails are separately retained. Literal equality is never confused
  with a positive path of residue zero.
- The repeated-`04` contraction loses degree only at common endpoint
  neighbors, which form an independent set, so the quoted degree-sum theorem
  applies. Every contracted rooted path has an actual endpoint lift. The
  repeated-`04` cap interfaces cover all 13 weak landing orders and all nine
  private/trivial/positive common-tail combinations.
- The bipartite-deletion branch correctly creates a simple 4-connected split
  apex and has a length-preserving cycle/path correspondence. I separately
  audited its periodic theorem and finite tables in
  `dean5_periodic_split_apex_audit`; the shortest-path normalization, ternary
  modules, block-tree concentration, long residue classes, distances five and
  seven, and final lift are sound.

One subtle carrier inference is implicit but valid. In a serial cap through
two odd sources, both source-centered subcaps have the same ordered carrier
phases. Each of the three surviving phase pairs has a unique ordered arm pair.
If the middle source-to-source residue is `m`, the two arm pairs are
`(alpha,m+beta)` and `(alpha+m,beta)`. Both equal the unique survivor pair only
when `m=0`. This justifies the residue-zero middle edge in (B.10) and in the
repeated-`04` serial records.

## Independent finite checks

The downloaded versioned artifacts had these SHA-256 values:

```text
5e06b1e307b0b48c463bddf2880fdb3e9185e9b51f2740f5057e3f14e7aad7e2  dean5-source-v1.0.1.tex
abc41317fa70bc781b4b714b2ecf980eeeaf703a3e013aba25641a0779821f18  dean5-paper-v1.0.1.pdf
75b604acc53a38622e0fffddebcb27e3e883f5836d7da7e7ddb45c8378eebed5  dean5-computational-supplement-v1.0.1-upload.zip
923acce2a0ec30c9475f260863548035607d05e47821b77e58691c8f5a71a135  MANIFEST_SHA256.txt
```

All 86 entries in the supplement manifest matched. The POSIX wrapper
`rerun_supplement.py` reads the archive's frozen reference command list,
rewrites only generated-JSON destinations into a scratch directory, and runs
the current distributed source for all 47 entries, including the two v1.0.1
alternating-cap programs. The fresh run used Python 3.11.2 and Node.js
v22.23.2; all 47 processes returned zero, with total subprocess time
3,442,133 ms. Its `run_summary.json` has SHA-256
`01421402bfe60d2984d31a3af6ed3b2fef487a9d15e7cac52c2e0fc72cac135b`.
The two regenerated bipartite JSON certificates equal the distributed files
after normalizing CRLF to LF. Logs and generated multi-megabyte JSON were kept
under `/scratch` and are deliberately not committed.

The sibling contribution `dean5_typeii_carrier_interface_audit` contains a
clean-room algebra checker which does not import the supplement. It
independently enumerates the phase table, both Watkins--Mesner coordinate
systems, all 625 reduced one-cap tuples, the serial middle residue, and all 13
weak landing orders. The two distributed implementations additionally generate
all 216 alternating records and find a zero-cycle in every one; I do not
duplicate that already committed predicate here.

The carrier checker's output is:

```text
PASS Dean-5 Type-II carrier algebra
phase table survivors: 6
cubic Watkins-Mesner coordinate survivors: 2
aligned Watkins-Mesner coordinate survivors: 0
internally admissible one-cap tuples: 8 of 625
serial normalized rows: 3; every middle residue is 0
weak landing orders: 13
```

Run that checker from its sibling directory with:

```bash
python3 verify_carrier_algebra.py
```

To reproduce the full distributed suite after extracting the supplement:

```bash
python3 rerun_supplement.py /path/to/dean5-computational-supplement-v1.0.1 /scratch/dean5-rerun
```

## External dependencies and trust boundary

I checked the quoted hypotheses and conclusions against the primary sources:

- Chiba--Ota--Yamashita, rooted admissible paths:
  <https://arxiv.org/abs/2008.09783>;
- Li--Zhan, the three-good-path lemma:
  <https://arxiv.org/abs/2508.14915>;
- Bai--Grzesik--Li--Prorok, connectivity and residue results, including the
  reproduced degree-sum formulation: <https://arxiv.org/abs/2511.03085>;
- Luo--Ma--Zhao, tetragonal-core tools and the prior `k>=6` result:
  <https://arxiv.org/abs/2601.13552>;
- Hayashi--Kawarabayashi--Yoo's modern Watkins--Mesner formulation:
  <https://doi.org/10.1137/23M157082X>.

I rely on those theorems, Cauchy--Davenport, Menger/fan lemmas, and standard
block connectivity facts; I did not reprove the imported research theorems.
The conclusion is an independent mathematical/software audit, not a formal
proof assistant verification. No external review of the August 2026 upload
was discoverable at the time of this audit, so this verdict should be read as
strong positive evidence with an explicit repair, not as community consensus.
