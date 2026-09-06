# Complete fixed-library extension test on H632

Exactly **22 of 544 published old colourings extend** over all 122
archived completion centres. The extension test is exact: it uses the
certified forest/four-cycle structure, including empty and singleton
lists. A separate arc-consistency implementation and independent
positive-recipe decoder agree on all **35,904 component decisions**.

This provides 22 checked old singleton-deletion colourings of the
632-point, 3,112-edge graph. It does not close that graph's subgraphs
through order 508, and produces no record improvement. Failure to
extend a fixed old colouring is not a graph non-four-colourability
certificate. The frozen batch is complete; no further colourings or
native search were added after observing its results.

[PROOF.md](PROOF.md) gives the quantified extension equivalence,
both algorithms' correctness arguments, the exact experiment and its
claim boundary. [oracle.py](oracle.py) is the producing extension
procedure; [independent.py](independent.py) uses a different algorithm.
Both support arbitrary selected fresh subsets and four-colour lists.
The experiment itself always retains all 122 fresh vertices.

## Reproduce

From the repository root, using CPython 3.11.2 and its standard library:

```sh
python3 -B hadwiger_nelson_heule632_transport/controls.py \
  --out /tmp/hn632-controls
python3 -B hadwiger_nelson_heule632_transport/run.py \
  --out /tmp/hn632-run --controls /tmp/hn632-controls/controls.json
cmp hadwiger_nelson_heule632_transport/cases.tsv /tmp/hn632-run/cases.tsv
cmp hadwiger_nelson_heule632_transport/positive.json /tmp/hn632-run/positive.json
cmp hadwiger_nelson_heule632_transport/result.json /tmp/hn632-run/result.json
python3 -B hadwiger_nelson_heule632_transport/verify.py \
  --out /tmp/hn632-check --run /tmp/hn632-run
```

The public certificate can instead be checked directly, with no raw run:

```sh
python3 -B hadwiger_nelson_heule632_transport/verify.py \
  --out /tmp/hn632-standalone
```

No SAT package, negative proof trace or source centre-enumeration dump
is required. The old positive strings use existing compact public
recipes, all input files being pinned in [plan.json](plan.json). The
old rows are numbered exactly as in the H514 whole-closure package:
516 interface rows, then 15 profile rows, then 13 final rows.

The controls check all 182,667 specified optional-vertex/list assignments
against direct colour enumeration. They took about 11.5 seconds. The
transport took about 1.8 seconds and independent verification about
3.9 seconds. [validation.json](validation.json) records actual timings
and checks. These are author implementation-independent checks; the
new result has no independent author review or formalization claim.

## Evidence format and expected results

[cases.tsv](cases.tsv) has 544 ASCII LF-terminated rows, without a header:

```
row_index<TAB>group:index<TAB>comma-separated old omissions<TAB>17-digit hexadecimal component mask
```

Bit j of the mask says that component j admits an extension. Components
are in the exact order of the pinned fresh-incidence certificate; bit
zero is the least significant bit. All 66 component outcomes, including
all failures, are compared entry by entry. The table SHA-256 is

```
1732ba3f438cec81bd83950bf8a54ac728ca6be7136489d9fc60688845fef630
```

[positive.json](positive.json) contains the 22 successful rows' fresh
colour strings, in increasing archived `centre_index` order. Every
string is checked with the decoded old colouring against all retained
unit edges. The 22 old singleton cuts are listed in
[result.json](result.json), along with the complete component statistics.

The canonical old-library stream has one line `group:index SPACE colours`
per row, where colours is exactly the first 510 characters of the old
H514 witness. Its SHA-256 is
`f35fc4fc4d9e42c8d877f05b344de4fa374b17f954bea6b2c00b365d359d52bc`.
The generated `lists.txt` contains 122 hexadecimal four-bit list masks
per row, followed by LF, in the same centre order; its SHA-256 is
`3d7edada6564ae03cf604276dbc58915077a8242132cb2b9861d356628dccb7d`.
These raw local streams are regenerable and not needed for the public
standalone check.

Of the 522 failures, 505 have an empty list somewhere; 17 have all lists
nonempty and fail due to coupled constraints. One explicit failure is
`interface:462`, omitting old vertex 486: adjacent fresh centres 809 and
1041 both require colour 1. The checker verifies this example directly.
It shows why the full extension procedure matters beyond single-point
availability checks.

## Dependencies, trust and handoff

The previous 122-centre incidence theorem supplies the finite support
and its unique even cycle. The verifier nevertheless recomputes every
one of the 199,396 unordered pairs of the full 632-point support. It
also decodes and checks the 544 inherited positive witnesses separately
from the producer, using the newly published H514 review's raw decoder.
That review accepts only the old H514 closure; it is not a review of
this new transport result. No old singleton forcing is assumed valid
on H632 without a checked extension.

Remaining trust is in the pinned coordinate/recipe interpretation,
the elementary tree and cycle proofs, the exact-field basis,
CPython integers and finite loops, and the independent checker's code.
There is no floating-point test, native solver verdict or assumed
completeness of an old colouring library.

The family-level closure threshold in the frozen plan was 509 distinct
fully extended old singleton cuts. The observed 22 leave the family
open. The next work must be a separately bounded support decision,
using this exact extension mechanism where useful; these cuts do not
justify another adaptive colouring-library ladder. A promising test
would deliberately omit at least two old H510 vertices, which every
at-most-508 subgraph must do. Any non-four-colourability verdict in
such a test would require its own independently checked certificate.
No such native test, graph shrink, new construction or background job
has started here. HN-3's dominating-clique geometry remains separate.
