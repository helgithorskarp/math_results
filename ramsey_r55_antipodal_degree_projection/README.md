# Exact 104-edge projection, with degree reconstruction

For the fixed H92 three-root subsystem, 104 free edges lie between opposite
root-signature classes. They occur in none of the six root-neighborhood
Ramsey constraints or the two marked density equations. We eliminate them
**exactly from this subsystem's degree equations**, leaving 523 physical
edge decisions plus three binary-matrix feasibility conditions. A
deterministic integral-flow lifter recovers their colors. See [PROOF.md](PROOF.md).

This is not a stronger exclusion or a new Ramsey graph. No solver was
called. The prior 90-second six-neighborhood UNKNOWN remains undecided.
In particular, the 104 edges still occur in other full-graph K5 constraints.
No speedup is asserted before a backend encoding is measured.

## Exact scope and evidence

- Fixed H92 and stars at 0,1,38; degrees 20 at those roots and 21 elsewhere.
  Both marked blue neighborhoods have 124 red edges.
- Omitted blocks: Z39..42–W2..9 (4x8), H10..13–X20..28 (4x9), and
  H14..17–Y29..37 (4x9). No symmetry or vertex-order normalizer is used.
- Three balances, 76 scalar bounds, and 45 labeled subset inequalities
  exactly characterize the omitted degree completions. Five outside
  residual equations remain, three identically zero.
- An independent physical five-set reconstruction checks every one of
  the 70,848 neighborhood clauses and the side-condition schema.
- Independent column DP checks all 756,250 canonical margin pairs;
  integral flow checks every one of the 33,256 balanced pairs, plus 144
  non-sorted permutations. Exactly 5,108 and 9,362 canonical margin
  pairs are feasible for 4x8 and 4x9 respectively. These are degree-block
  counts, not graphs or Ramsey profiles.
- Exhaustive literal binary-matrix tests for 4x1 through 4x4 agree with
  the DP entrywise. The larger DP censuses account for all 2^32 and 2^36
  matrices, with multiplicity. Corrupted descriptors and margin
  certificates are rejected; normal and `-O` runs agree byte-for-byte.

The stored G92.json is the **old non-Ramsey fixture**, not a solution to
the projected system. Removing the 104 colors and lifting them changes
16 edges, preserves all degrees and all six entire induced neighborhoods,
and still leaves the same 202 violated local clauses. The deterministic
lift has 466 red and 171 blue K5s (637 total); the original had 653.
This incidental count change is not a new search or descent endpoint.
The explicit five-set {2,3,15,26,34} becomes a red K5, illustrating why the
projection is not automatically valid for omitted full-graph constraints.

## Reproduction

Python 3.11.2, standard library only; exact Python integers, no randomness,
SAT solver, proof checker, or external graph package. From the repository
root, use a fresh temporary directory:

```bash
projection_run=$(mktemp -d)
python3 -B ramsey_r55_antipodal_degree_projection/model.py --work "$projection_run/model"
python3 -B ramsey_r55_antipodal_degree_projection/lift_fixture.py --work "$projection_run/fixture"
python3 -B ramsey_r55_antipodal_degree_projection/test_margins.py --report "$projection_run/margins.json"
python3 -B ramsey_r55_antipodal_degree_projection/audit.py --work "$projection_run/model" --lifted "$projection_run/fixture/lifted.json" --report "$projection_run/audit.json"
cmp "$projection_run/margins.json" ramsey_r55_antipodal_degree_projection/margins.json
cmp "$projection_run/audit.json" ramsey_r55_antipodal_degree_projection/verification.json
cmp "$projection_run/fixture/lifted.json" ramsey_r55_antipodal_degree_projection/lifted.json
cmp "$projection_run/fixture/projected_fixture.json" ramsey_r55_antipodal_degree_projection/projected_fixture.json
```

Repeat with `python3 -O -B` and fresh paths to check optimized-mode agreement.
Expected generated neighborhood CNF SHA-256:
`ece2f0c1a0ebf7f43fee80bd848b0ff082602e91f36bdc9946cff230e8a4ac25`.
Expected generated descriptor SHA-256:
`0a5407af70b1711597b9bdd7a46753c78ee33a297f4812fc9b271172d6c2331a`.

**The CNF alone is not the projected system.** `projection.json` provides
the required degree, density, balance, bound, and minimum-sum side
conditions. These have not yet been translated to a backend CNF/OPB.
`Model.evaluate` checks the complete mixed model on a Boolean assignment;
`Model.complete_degrees` intentionally checks only the degree side and
performs its lift. Call `evaluate` before treating a lift as a subsystem
witness. Both fixtures here explicitly fail that test.

The margin census took about 11.15 seconds and 19,924 KiB peak child RSS;
the physical audit with optional prior-formula comparison took 7.20 seconds
and 99,644 KiB on this host. No parallel reduction or approximate arithmetic
was used. Generated CNFs and operational checkpoints remain outside Git.

## Sources, dependencies, and trust

H92 and G92 are byte-identical inputs from
[the joint-neighborhood realization](../ramsey_r55_joint_neighborhood_degree_realization),
source commit `67782fb3b0a5704baf2df8e407ba72d3c97b6761`, Discovery Net
`bafkreietsadux6z2xphuof3rottlsvx3jeikgmdrfcavnipwoyzoo7x734`.
Their complete fixed geometry is also restated here; no parent solver is
required to verify this lemma.

The prior unpublished six-neighborhood formula had 33,515 total variables,
627 physical variables, 200,127 clauses and SHA-256
`4e3361668a02b08602b695e88033b7776dbf26ecb9ebe4e8cbe061405720b055`.
If it is available locally, `audit.py --prior-cnf PATH` additionally checks
that its 70,848 physical clauses are exactly the new clause set after
renumbering. This optional check changes the report's prior-comparison
field. The lemma and the default reproduction do not depend on this
unpublished byte stream or a re-audit of its auxiliary counters.

The proof is unformalized. Flow, subset cuts, and independent DP are three
different internal checks, not independent peer review. Gale–Ryser and
integral flow are classical; references and a self-contained proof appear
in PROOF.md. No novelty claim is made for the degree criterion itself.

The new result changes neither the 66-profile/271-split/470-filter scope nor
the teammate's independent symmetry boundary. Reviewed four-separator
classification at blue density at least 108 does not apply directly to our
marked Q blue density 107; it is not used as a premise.

The next bounded direction is to encode and test this projected system
with explicit lifting, or to add full-K5 restrictions on allowable lifts.
Neither phase has begun in this artifact.
