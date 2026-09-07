# Validation and trust boundaries

Reproduce from the repository root with Python 3.11 and the standard library:

```bash
python3 -B ramsey_r55_global_clique_packing/reproduce.py
python3 -O -B ramsey_r55_global_clique_packing/reproduce.py
```

Both fresh public-source runs returned `VERIFIED_UNCONDITIONAL_GLOBAL_PACKING_HANDOFF`. They took 139.332815 and 150.191163 seconds, with peak resident sets of 56,384 and 56,512 KiB on this host. These checks were run concurrently; the timings are observations, not performance guarantees. Python optimization leaves every substantive check active. Reproduction creates one full formula at a time in a temporary directory and deletes it after checking. No network, compiler, external catalog, or solver is used.

## Exact checks

* Every entry in all 36 pair-domain bitmaps was compared with a separate physical-adjacency clique checker: 335,872 matrices. All 335,872 transpose transports were also checked.
* All six root-domain bitmaps were compared with independently enumerated child-automorphism orbit minima: 1,817,036 allowed-matrix group images. Burnside fixed-point sums agree exactly with the six orbit counts.
* Each of the 60 branch counts was recomputed through atom-type frequencies, separately from the producer's block-pair product. The 60 fixed internal colorings were checked distinct. Exact integer inequalities verify M<2^787, 2^65·M<60·2^846, and 2^36·M<N. The displayed closed formula was separately evaluated against all branch counts.
* Full physical five-set enumeration produced 962,598 sets and 3,272 internal-edge stencils. These independently match all 60 formula dimensions and the count of 1,971 five-sets in two blocks.
* All 180 first/middle/last branch indices round-trip. Sixty physical fixtures pass all pair domains and root comparisons, and every fixture fails good43. Arbitrary vertex transports preserve all 54,180 checked physical edges.
* The matrix interface was checked against each of its 846 actual edge coordinates. Representative five-set placements were tested on all 89,280 free Boolean assignments. All 3,072 assignments in twelve atom-specific root comparators match their numerical inequality.
* Seventeen invalid-input controls are rejected, including malformed indices, branches, matrices, graph sizes and SAT claims. Greedy-packing positive and negative controls pass. The separate known-good42 fixture passes its 850,668 physical five-sets; it is never accepted as the 43-vertex target.
* In six complete 43-vertex formulas, an independent physical-edge enumerator reconstructed all 8,414,656 Ramsey clauses and all 19,680 root-order clauses, as well as constants and headers. The corresponding fixture counts agree with a second recursive clique counter. Six is a representative formula audit, not an exhaustive enumeration of all candidate graphs or a solve of any branch.

`EXPECTED_AUDIT.json` stores every tested full formula's dimensions, SHA256, clause-length histogram and fixture counts. `EXPECTED_DOMAIN_AUDIT.json` stores the independent domain/orbit/cardinality audit. `PUBLIC_REPLAY.json` records the two fresh runs. Main audit SHA256:

```text
04294d5a0a82634da8938e9c2b4e933dd8a7a29cd941750561a070ed619b0029
```

Pair-domain bitmap file SHA256:

```text
5c36ea521e0e1470e0417671eea7d9f14fa85b625f4a052a448e76ee547bc68d
```

Root-domain bitmap file SHA256:

```text
2562a431f9ed3df1659d8821d38e59665209781ac6ac6f491a9f81b14e41dbb3
```

The six final full CNFs total 377,705,100 bytes and remain outside the repository. Six earlier unrooted full formulas total 377,066,220 bytes and are retained only as a private checkpoint of the bounded intermediate calculation. The final public source reproduces the rooted formulas. No large certificate, CNF, executable, cache or downloaded paper is published.

The standalone command-line pipeline also generated, ranked, reconstructed and normalized a retained state at seed 20260907. Its independent target check found 325 red and 1,107 blue five-cliques; an UNKNOWN transcript was rejected without writing a target. The exact index, graph hash and outputs are in `CLI_AUDIT.json`.

## Claim boundary

The external mathematical premise is R(4,5)<=25, with a direct primary-paper reference in `PROOF.md`. The original 1995 computation is not rerun here. Elementary proofs establish the two other Ramsey upper bounds used by the partition. The new proof is mathematical prose supported by exact finite checks, not proof-assistant formalization. The independent algorithms in this directory were run by the author; external review of this contribution is pending.

No SAT solver was called. No complete branch was excluded, no physical target was found, and no Ramsey bound changed. The index enumerates all retained physical states, most of which still fail five-set constraints across three or more blocks. The count concerns a relabeled existential search family; it is not an isomorphism census, a fraction of good graphs eliminated, or a measured solver acceleration.
