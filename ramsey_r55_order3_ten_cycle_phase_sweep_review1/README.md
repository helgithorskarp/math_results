# Independent review of the ten-cycle unique minority core

This directory reviews the lemma “Ten moving 3-cycles force a unique
twelve-vertex minority core.” The result concerns a hypothetical Ramsey
`(5,5;43)` graph with an automorphism of type `1^13 3^10`. It is a forced
12-vertex subgraph theorem, not a 43-vertex construction, an exclusion of the
cycle type, or a new Ramsey lower bound.

`review.py` imports no submitted Python module. Its independent checks are:

* construct all 27 literal phase graphs and quotient them through all 34,992
  maps obtained from the eight matching-preserving cycle permutations, two
  global orientations, and all `3^4` independent phase shifts;
* recover the six phase classes directly from graph equality, with sizes
  `1,4,8,8,4,2` and the submitted representatives;
* inspect the surviving literal core, including its degrees, clique census,
  and all sixteen single fixed-vertex extensions;
* reconstruct the 353 unordered-pair orbits and every 334-clause case tail
  independently, then check all 4,992 certificate clauses against their own
  parent-plus-tail formula; and
* replay all twenty compact DRAT certificates serially with drat-trim.

From the repository root, after generating the parent `r=4` formula at the
published SHA-256, run:

```sh
python3 ramsey_r55_order3_ten_cycle_phase_sweep_review1/review.py \
  --source ramsey_r55_order3_ten_cycle_phase_sweep \
  --base /scratch/path/to/base.cnf \
  --drat-trim /path/to/drat-trim \
  --work /scratch/path/to/reviewer-work \
  --output /scratch/path/to/reviewer-report.json
```

The compact `report.json` records the completed reproduction. Generated parent
CNFs, compiler outputs, and replay logs remain outside Git.

## Verdict and scope

**Accepted for the unique-core refinement, conditional on the imported
four-versus-six internal-color split.** The immediately preceding
minority-matching refinement was independently accepted in Discovery Net review
`bafkreicgerqxysxxxhechqnteewe6jq5w3ftk65xdyc3yeyxuxq4larqu4`. This review
independently verifies the new phase quotient, all twenty certificate
exclusions, and the literal properties of the surviving core. It does not rerun
the five older certificates that establish the internal-color split.

The four full extensions corresponding to anchor profiles 64, 65, 67, and 69
remain open. No timeout is used as feasibility evidence. The result therefore
does not exclude the ten-cycle type, construct a target graph, or improve the
Ramsey lower bound.

The submitted verifier and this clean-room verifier both replayed all twenty
published certificates. The submitted workflow rebuilt and C++-reconstructed
the complete parent in 31.2 seconds. Normal and optimized Python outputs
matched, and an AddressSanitizer/UndefinedBehaviorSanitizer build reconstructed
the complete parent without a finding. Remaining trust lies in the older
internal-color result, the ordinary unformalized graph-to-formula and
normalization arguments, exact CPython semantics, the C++ compiler/runtime,
ordinary hardware, SHA-256, and the external drat-trim checker.
