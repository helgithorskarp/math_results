# Four-hub P23 C-row support lemma

Actual author **six-code-3**, role **researcher**, 2026-10-03.

For a 71-word packing of five-subsets on eighteen points with intersections
at most two, profile (18,19,19,19,20^14), hub-pair total P=23 and no word
containing three hubs (T=0), **four C rows force K>=17**. Therefore K<=16
permits at most three C rows. [PROOF.md](PROOF.md) defines C and K and gives
the ordinary argument. It imports only the universal twenty-star
no-LOW--LOW interface of graph lemma8323.

## Reproduce from this directory

Use CPython 3.10 or later, standard library only. Release verification uses
CPython 3.12.14. No solver, network, campaign database, private output,
generated instance list or earlier code package is required.

```sh
python3 reproduce.py --work /tmp/four-hub-c-support-new
```

The output directory must not exist and must lie outside this source
directory. Omitting `--work` creates a fresh directory under the system
temporary directory and prints its location. The runner verifies the
source/input manifest before and after every child, makes a cold copy,
and runs all three programs sequentially in both normal and `-O` modes.
Each child has an explicit sixty-second process timeout. Every finite
program retains its 500,000-state and twenty-second mathematical guards.
Native/BLAS/OpenMP thread variables are set to one. An incomplete run is
not a nonexistence result. No resource setting is escalated.

Expected mathematical scope is **199,920 cases**, **5,712 support tuples**,
**35 compositions**, **39 feasible necessary relaxations**, and minimum
relaxed support **17**. The runner compares whole normal/optimized output
bytes; the independent verifier compares complete masks, all positive
records and all 39 whole literal edge witnesses. It checks 7,168 elementary
degree identities and three semantic rejection controls. The full common
mathematical record has SHA256
`80fd352fb1bb26d84e0893b87acfcb7e16b750ab358578253e1c924fef17c613`.
[EXPECTED.json](EXPECTED.json) authenticates the complete outputs and controls.
Hashes support integrity; they do not replace the reconstructed domain or
the witness and mask checks.

The two mathematical algorithms are literal HH-star enumeration and an
independent 64-subset max-flow/min-cut test. Neither imports the other.
The positive and counterfactual controls are necessary-relaxation
assignments, not actual packings or sharpness claims. Generated output
and process receipts stay in the chosen external output tree.

## Trust and scope

This is an ordinary conditional author lemma, with complete exact support
checks by different algorithms. The packing-to-relaxation and flow bridges
are unformalized. Independent-person review is pending. Review9938 of the
earlier P22 proof does not review this result. No unrestricted endpoint
improvement, P23 exclusion, full-star classification or code construction
is asserted. The three-C/K15 column and mate realization remains open.
The private scalar census is not needed or reproduced by this packet.

The imported premise and primary literature, including live status and
credit for the established 69-word construction, are linked in the proof.
The finite checks are deterministic exact integers, with no floating-point
or solver soundness assumption. [MANIFEST.json](MANIFEST.json) freezes all
other packet files before release verification; it excludes itself to
avoid a circular hash.
